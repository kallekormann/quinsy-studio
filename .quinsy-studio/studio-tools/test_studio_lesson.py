#!/usr/bin/env python3
"""Lesson verdict, impact severity, defer/reopen, close gate, TRAIN_DUE, PB- search."""

from __future__ import annotations

import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch

import studio_harvest
import studio_lesson as L
import studio_train
from studio_harvest import harvest_identified_learning


@contextmanager
def _env():
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        open_dir, done_dir, blocked, deferred = (tmp / n for n in ("open", "done", "blocked", "deferred"))
        for d in (open_dir, done_dir, blocked, deferred):
            d.mkdir()
        studio = tmp / "studio"
        (studio / "process").mkdir(parents=True)
        (studio / "knowledge-base").mkdir()
        (studio / "process" / "gates.md").write_text("# Gates\n\n## Deltas\n\n", encoding="utf-8")
        (studio / "knowledge-base" / "design_playbook.md").write_text("# Design\n\n## Deltas\n\n", encoding="utf-8")
        changelog = studio / "CHANGELOG.md"
        changelog.write_text("# Changelog\n\n", encoding="utf-8")
        (tmp / "projects" / "demo").mkdir(parents=True)
        with patch.multiple(
            studio_harvest, BACKLOG_OPEN=open_dir, BACKLOG_DONE=done_dir, BACKLOG_BLOCKED=blocked
        ), patch.object(studio_harvest, "resolve_project_from_source", lambda s: "demo"), patch.multiple(
            L,
            BACKLOG_OPEN=open_dir,
            BACKLOG_DONE=done_dir,
            BACKLOG_DEFERRED=deferred,
            PROJECTS_DIR=tmp / "projects",
            QUINSY_STUDIO=studio,
            CHANGELOG=changelog,
        ), patch.multiple(
            studio_train, QUEUE_PATH=tmp / "q.json", BACKLOG_OPEN=open_dir, BACKLOG_DONE=done_dir
        ), patch("studio_portability.scan_hq_for_project_nouns", lambda: []):
            yield tmp, studio


def _candidate(title="Gate smoke must use the project cache", kind="tooling"):
    return harvest_identified_learning(title, source="demo/SPRINT-01", signal="tooling-gap", observation="x", kind=kind)["lo_id"]


def _fill_impact(path: Path, severity="low"):
    text = path.read_text(encoding="utf-8")
    text = L.set_section(
        text,
        "Impact",
        "- **files:** process/gates.md (read by ./studio gate)\n"
        "- **in-flight:** no — gate runs read the file fresh\n"
        "- **compliance:** no signed packet changes\n"
        "- **pro:** no more lost browsers\n"
        "- **contra:** one more line to read\n"
        f"- **severity:** {severity}\n",
    )
    path.write_text(text, encoding="utf-8")


class VerdictTests(unittest.TestCase):
    def test_candidate_needs_verdict_then_studio_fills_block(self):
        with _env():
            lo = _candidate()
            path = L.lo_path(lo)
            self.assertTrue(L.needs_verdict(path.read_text()))
            self.assertIn("verdict", L.lesson_missing(path.read_text()))
            res = L.set_lesson_verdict(
                lo,
                verdict="studio",
                reason="the gate template chose the cache",
                assumed="temp cache is fine",
                signed="project cache only",
                next_rule="Gate smoke must use the project cache, never a temp directory",
                target="process/gates.md",
            )
            self.assertEqual(res["severity_floor"], "high")
            text = path.read_text()
            self.assertFalse(L.needs_verdict(text))
            self.assertEqual(L.parse_lesson(text)["target"], "process/gates.md")
            self.assertEqual(L.parse_lesson(text)["reason"], "the gate template chose the cache")

    def test_project_verdict_removes_lo_and_logs(self):
        with _env() as (tmp, _studio):
            lo = _candidate()
            res = L.set_lesson_verdict(
                lo, verdict="project", reason="only this product", assumed="a", signed="b", next_rule=""
            )
            self.assertEqual(res["verdict"], "project")
            self.assertIsNone(L.lo_path(lo))
            local = tmp / "projects" / "demo" / "docs" / "studio-learnings-local.md"
            self.assertIn("only this product", local.read_text())
            rows = L.project_verdict_lines("demo")
            self.assertEqual(len(rows), 1)
            self.assertIn("only this product", rows[0]["reason"])

    def test_studio_verdict_refuses_catalog_target_and_missing_next(self):
        with _env():
            lo = _candidate()
            with self.assertRaises(ValueError):
                L.set_lesson_verdict(lo, verdict="studio", reason="r", assumed="a", signed="b", next_rule="")
            with self.assertRaises(ValueError) as ctx:
                L.set_lesson_verdict(
                    lo, verdict="studio", reason="r", assumed="a", signed="b",
                    next_rule="Gate smoke must use the project cache always", target="knowledge-base/learnings/process/tooling.md",
                )
            self.assertIn("old catalog", str(ctx.exception))

    def test_verdict_requires_reason(self):
        with _env():
            lo = _candidate()
            with self.assertRaises(ValueError):
                L.set_lesson_verdict(lo, verdict="studio", reason="", assumed="a", signed="b", next_rule="n")


class ImpactTests(unittest.TestCase):
    def _studio_lo(self, target="process/gates.md"):
        lo = _candidate()
        L.set_lesson_verdict(
            lo, verdict="studio", reason="r", assumed="a", signed="b",
            next_rule="Gate smoke must use the project cache, never a temp directory", target=target,
        )
        return lo

    def test_floor_by_path(self):
        self.assertEqual(L.severity_floor("process/gates.md"), "high")
        self.assertEqual(L.severity_floor("studio-tools/studio.py"), "high")
        self.assertEqual(L.severity_floor("teams/10-x/skills/a.md"), "high")
        self.assertEqual(L.severity_floor("studio-templates/x.md"), "high")
        self.assertEqual(L.severity_floor("knowledge-base/design_playbook.md"), "low")

    def test_assess_writes_template_then_hitl_on_high(self):
        with _env():
            lo = self._studio_lo()
            self.assertEqual(L.assess(lo)["state"], "needs_impact")
            path, inserted = L.ensure_impact_template(lo)
            self.assertTrue(inserted)
            self.assertEqual(L.assess(lo)["state"], "impact_stub")
            _fill_impact(path, severity="low")  # agent tries to lower: floor wins
            state = L.assess(lo)
            self.assertEqual(state["state"], "hitl")
            self.assertEqual(state["severity"], "high")
            self.assertIn("high impact", "; ".join(L.close_issues(lo)))
            L.approve_lesson(lo)
            self.assertEqual(L.assess(lo)["state"], "infuse")

    def test_low_target_infuses_without_signature_but_agent_may_raise(self):
        with _env():
            lo = self._studio_lo(target="knowledge-base/design_playbook.md")
            path, _ = L.ensure_impact_template(lo)
            _fill_impact(path, severity="low")
            self.assertEqual(L.assess(lo)["state"], "infuse")
            _fill_impact(path, severity="high — changes every signed spec")
            self.assertEqual(L.assess(lo)["state"], "hitl")

    def test_defer_and_reopen(self):
        with _env() as (tmp, _s):
            lo = self._studio_lo()
            path, _ = L.ensure_impact_template(lo)
            _fill_impact(path)
            L.assess(lo)
            with self.assertRaises(ValueError):
                L.defer_lesson(lo, "")
            dest = L.defer_lesson(lo, "mid-sprint on two products")
            self.assertEqual(dest.parent, tmp / "deferred")
            due = L.train_due()
            self.assertEqual(len(due["deferred"]), 1)
            self.assertEqual(due["open"], [])
            lines = L.train_due_lines()
            self.assertIn("Deferred", "\n".join(lines))
            self.assertIn("deferred", "; ".join(L.close_issues(lo)))
            back = L.reopen_lesson(lo)
            self.assertEqual(back.parent, tmp / "open")
            self.assertEqual(L.assess(lo)["state"], "hitl")


class CloseTests(unittest.TestCase):
    def test_close_requires_bullet_in_target_and_changelog(self):
        with _env() as (tmp, studio):
            lo = _candidate()
            L.set_lesson_verdict(
                lo, verdict="studio", reason="r", assumed="a", signed="b",
                next_rule="Design specs must list every state before sign-off", target="knowledge-base/design_playbook.md",
            )
            path, _ = L.ensure_impact_template(lo)
            _fill_impact(path)
            self.assertEqual(L.assess(lo)["state"], "infuse")
            issues = L.close_issues(lo)
            self.assertTrue(any("no infused PB- id" in i for i in issues))
            with self.assertRaises(ValueError):
                L.move_lo_done(lo)
            L.record_infusion(lo, bullet_id="PB-20261013-001", target="knowledge-base/design_playbook.md")
            issues = L.close_issues(lo)
            self.assertTrue(any("is not in" in i for i in issues))
            target = studio / "knowledge-base" / "design_playbook.md"
            target.write_text(target.read_text() + "- **PB-20261013-001** helpful=0 harmful=0 :: assumed: a signed: b next: c\n")
            issues = L.close_issues(lo)
            self.assertTrue(any("CHANGELOG" in i for i in issues))
            (studio / "CHANGELOG.md").write_text("# Changelog\n\n- PB-20261013-001 design states\n")
            self.assertEqual(L.close_issues(lo), [])
            dest = L.move_lo_done(lo)
            self.assertEqual(dest.parent, tmp / "done")
            self.assertIn("status: done", dest.read_text())

    def test_infusion_body_needs_three_parts(self):
        self.assertEqual(L.infusion_body_issues("assumed: a signed: b next: c"), [])
        self.assertEqual(len(L.infusion_body_issues("Just a title")), 3)
        self.assertEqual(L.infusion_body_issues("Assumed: x. Signed: y."), ["body lacks `next:`"])

    def test_close_issues_blocks_on_verify_abstraction(self):
        with _env() as (tmp, studio):
            lo = _candidate()
            L.set_lesson_verdict(
                lo, verdict="studio", reason="r", assumed="a", signed="b",
                next_rule="Design specs must list every state before sign-off", target="knowledge-base/design_playbook.md",
            )
            path, _ = L.ensure_impact_template(lo)
            _fill_impact(path)
            L.assess(lo)
            L.record_infusion(lo, bullet_id="PB-20261013-001", target="knowledge-base/design_playbook.md")
            target = studio / "knowledge-base" / "design_playbook.md"
            target.write_text(target.read_text() + "- **PB-20261013-001** :: assumed: a signed: b next: c\n")
            (studio / "CHANGELOG.md").write_text("- PB-20261013-001\n")
            with patch(
                "studio_portability.scan_hq_for_project_nouns",
                lambda: [{"path": "knowledge-base/design_playbook.md", "line": 3, "noun": "acme", "snippet": ""}],
            ):
                self.assertTrue(any("verify-abstraction" in i for i in L.close_issues(lo)))


class TrainDueAndSearchTests(unittest.TestCase):
    def test_train_due_lists_candidates_open_and_project_lines(self):
        with _env() as (tmp, _s):
            cand = _candidate("Gate smoke must never run against a cold cache")
            ready = _candidate("Design specs must list every state", kind="design")
            L.set_lesson_verdict(
                ready, verdict="studio", reason="r", assumed="a", signed="b",
                next_rule="Design specs must list every state before sign-off",
            )
            L.write_project_verdict("demo", title="Local only thing", assumed="a", signed="b", reason="one product")
            due = L.train_due("demo")
            self.assertEqual([r["id"] for r in due["candidates"]], [cand])
            self.assertEqual([r["id"] for r in due["open"]], [ready])
            self.assertEqual(due["project"][0]["title"], "Local only thing")
            text = "\n".join(L.train_due_lines("demo"))
            self.assertIn("TRAIN_DUE — 2", text)
            self.assertIn("Need a verdict", text)
            self.assertIn("--promote", text)
            compact = L.train_due_lines("demo", compact=True)[0]
            self.assertIn("TRAIN_DUE 2", compact)
            self.assertIn("run training", compact)

    def test_train_due_empty(self):
        with _env():
            self.assertEqual(L.train_due_lines(), [])

    def test_search_pb_bullets_covers_playbooks_process_skills(self):
        with _env() as (tmp, studio):
            (studio / "teams" / "10-x" / "skills").mkdir(parents=True)
            (studio / "teams" / "10-x" / "skills" / "a.md").write_text("- **PB-20261013-001** :: Motion must name its easing\n")
            (studio / "process" / "gates.md").write_text("- **PB-20261013-002** :: Gate smoke uses the project cache\n")
            (studio / "knowledge-base" / "design_playbook.md").write_text("- no id here about easing\n")
            hits = L.search_pb_bullets("easing")
            self.assertEqual([h["path"] for h in hits], ["teams/10-x/skills/a.md"])
            self.assertTrue(L.pb_id_exists("PB-20261013-002"))
            self.assertFalse(L.pb_id_exists("PB-20000101-001"))


if __name__ == "__main__":
    unittest.main()
