#!/usr/bin/env python3
"""Immediate harvest: classify, LO candidate with ## Lesson block, exact-title dedupe, gate rounds."""

from __future__ import annotations

import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch

import studio_harvest
import studio_lesson
import studio_train
from studio_harvest import (
    classify_learning,
    gate_revision_rounds,
    harvest_gate_rounds,
    harvest_identified_learning,
    harvest_retro_text,
    harvest_reuse_items,
    open_candidates,
    target_for_kind,
)
from ticket_helpers import render_ticket_markdown


@contextmanager
def _patch_harvest_dirs(tmp: Path):
    open_dir = tmp / "open"
    done_dir = tmp / "done"
    blocked = tmp / "blocked"
    deferred = tmp / "deferred"
    for d in (open_dir, done_dir, blocked, deferred):
        d.mkdir(exist_ok=True)
    queue = tmp / "train-queue.json"
    harvest = patch.multiple(
        studio_harvest,
        BACKLOG_OPEN=open_dir,
        BACKLOG_DONE=done_dir,
        BACKLOG_BLOCKED=blocked,
    )
    lesson = patch.multiple(
        studio_lesson,
        BACKLOG_OPEN=open_dir,
        BACKLOG_DONE=done_dir,
        BACKLOG_DEFERRED=deferred,
        PROJECTS_DIR=tmp / "projects",
    )
    train = patch.multiple(
        studio_train,
        QUEUE_PATH=queue,
        BACKLOG_OPEN=open_dir,
        BACKLOG_DONE=done_dir,
    )
    with harvest, lesson, train:
        yield


class ClassifyTests(unittest.TestCase):
    def test_path_and_keywords(self):
        self.assertEqual(classify_learning("x", path="packages/auth"), "package")
        self.assertEqual(classify_learning("x", path="ui/components/button"), "ui-component")
        self.assertEqual(classify_learning("h-dvh overflow nested scroll"), "layout")
        self.assertEqual(classify_learning("information architecture placement"), "ia")
        self.assertEqual(classify_learning("gate smoke playwright", signal="gate-fail"), "tooling")
        self.assertEqual(classify_learning("CSP and XSS headers", signal="knowledge-gap"), "security")
        self.assertEqual(classify_learning("unclear groom step", signal="process-gap"), "process")

    def test_target_is_a_real_studio_file_never_the_catalog(self):
        for kind in studio_harvest.KIND_MAP:
            target = target_for_kind(kind)
            self.assertFalse(target.startswith("knowledge-base/learnings/"), kind)
            self.assertTrue((studio_harvest.QUINSY_STUDIO / target).exists(), f"{kind} → {target}")


class HarvestWriteTests(unittest.TestCase):
    def test_creates_candidate_lo_with_lesson_block(self):
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            with _patch_harvest_dirs(tmp):
                result = harvest_identified_learning(
                    "Nested board overflow needs h-dvh",
                    source="demo/SPRINT-01",
                    observation="inner scroll clipped",
                )
                self.assertTrue(result["created"])
                self.assertTrue(result["needs_verdict"])
                self.assertEqual(result["kind"], "layout")
                self.assertEqual(result["infusion_path"], "knowledge-base/design_playbook.md")
                lo_files = list((tmp / "open").glob("LO-*.md"))
                self.assertEqual(len(lo_files), 1)
                text = lo_files[0].read_text(encoding="utf-8")
                self.assertIn("infusion_kind: layout", text)
                self.assertIn("infusion_path: knowledge-base/design_playbook.md", text)
                self.assertIn("needs_verdict: true", text)
                self.assertIn("## Lesson", text)
                for key in ("assumed", "signed", "verdict", "next", "target"):
                    self.assertIn(f"**{key}:**", text)
                self.assertNotIn("knowledge-base/learnings", text)
                self.assertEqual(len(open_candidates()), 1)
                # candidates do not queue skill training until the verdict is studio
                self.assertEqual(studio_train.open_jobs(), [])

    def test_complete_studio_verdict_is_not_a_candidate(self):
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            with _patch_harvest_dirs(tmp):
                result = harvest_identified_learning(
                    "Gate smoke must use the project cache",
                    source="demo",
                    signal="tooling-gap",
                    observation="temp cache lost browsers",
                    assumed="gate smoke could use a temp cache",
                    signed="gate smoke must use the project cache",
                    verdict="studio",
                    reason="the default gate template chose the cache",
                    next_rule="Gate smoke must use the project cache, never a temp directory",
                )
                self.assertTrue(result["created"])
                self.assertFalse(result["needs_verdict"])
                text = next((tmp / "open").glob("LO-*.md")).read_text(encoding="utf-8")
                self.assertIn("verdict: studio", text)
                self.assertIn("severity_floor: high", text)  # process/gates.md
                self.assertEqual(open_candidates(), [])

    def test_project_verdict_writes_local_log_and_no_lo(self):
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            (tmp / "projects" / "demo").mkdir(parents=True)
            with _patch_harvest_dirs(tmp), patch.object(
                studio_harvest, "resolve_project_from_source", lambda s: "demo"
            ):
                result = harvest_identified_learning(
                    "Board needs a second rail",
                    source="demo/SPRINT-02",
                    assumed="one rail",
                    signed="two rails",
                    verdict="project",
                    reason="only this product has two board kinds",
                )
                self.assertTrue(result["project_verdict"])
                self.assertFalse(result["created"])
                self.assertEqual(list((tmp / "open").glob("LO-*.md")), [])
                local = tmp / "projects" / "demo" / "docs" / "studio-learnings-local.md"
                self.assertTrue(local.exists())
                self.assertIn("verdict:** project — only this product", local.read_text(encoding="utf-8"))

    def test_verdict_needs_reason(self):
        with tempfile.TemporaryDirectory() as raw:
            with _patch_harvest_dirs(Path(raw)):
                with self.assertRaises(ValueError):
                    harvest_identified_learning("x rule", source="demo", verdict="studio")

    def test_dedupe_exact_title_only(self):
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            with _patch_harvest_dirs(tmp):
                first = harvest_identified_learning(
                    "Reuse harvest: generalize `packages/auth`",
                    source="demo",
                    path="packages/auth",
                )
                second = harvest_identified_learning(
                    "Reuse harvest: generalize `packages/auth`",
                    source="demo",
                    path="packages/auth",
                )
                other = harvest_identified_learning(
                    "Reuse harvest: generalize `packages/billing`",
                    source="demo",
                    path="packages/billing",
                )
                self.assertTrue(first["created"])
                self.assertFalse(second["created"])
                self.assertEqual(second["lo_id"], first["lo_id"])
                self.assertTrue(other["created"])
                self.assertNotEqual(other["lo_id"], first["lo_id"])

    def test_retro_harvests_badly_not_placeholders(self):
        retro = """# Retro
## What went well?
- tests were fast
## What went badly?
- Gate smoke must not use a temp cache
## What can we improve?
- ...
"""
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            with _patch_harvest_dirs(tmp):
                results = harvest_retro_text(retro, "demo")
                self.assertEqual(len(results), 1)
                self.assertTrue(results[0]["created"])
                self.assertTrue(results[0]["needs_verdict"])
                titles = [p.read_text() for p in (tmp / "open").glob("LO-*.md")]
                self.assertTrue(any("temp cache" in t for t in titles))

    def test_gate_rounds_open_candidate_at_two(self):
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            proj = tmp / "projects" / "demo"
            (proj / "docs" / "phases").mkdir(parents=True)
            rev = proj / "docs" / "phases" / "revisions.md"
            rev.write_text("# Revisions\n\n## Gate 1 — 2026-10-01\nStack must be the one named in the PRD\n", encoding="utf-8")
            with _patch_harvest_dirs(tmp):
                self.assertEqual(len(gate_revision_rounds(proj, "1")), 1)
                self.assertIsNone(harvest_gate_rounds("demo", proj, "1"))
                rev.write_text(
                    rev.read_text(encoding="utf-8") + "\n## Gate 1 — 2026-10-02\nHost named in the PRD must win over the archetype default\n",
                    encoding="utf-8",
                )
                self.assertEqual(len(gate_revision_rounds(proj, "1")), 2)
                self.assertEqual(len(gate_revision_rounds(proj, "2a")), 0)
                result = harvest_gate_rounds("demo", proj, "1")
                self.assertIsNotNone(result)
                self.assertTrue(result["created"])
                self.assertTrue(result["needs_verdict"])
                text = next((tmp / "open").glob("LO-*.md")).read_text(encoding="utf-8")
                self.assertIn("round 1:", text)
                self.assertIn("round 2:", text)
                self.assertIn("2 revision rounds", text)

    def test_reuse_two_paths_do_not_collide(self):
        items = [
            {"path": "packages/auth", "action": "promote", "covered": False, "ticket_id": "D-1"},
            {"path": "packages/auth/src/index.ts", "action": "promote", "covered": False, "ticket_id": "D-1"},
            {"path": "ui/components/dock", "action": "lo_ticket", "covered": False, "ticket_id": "D-2"},
            {"path": "src/local.ts", "action": "local", "covered": False, "ticket_id": "D-3"},
        ]
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            with _patch_harvest_dirs(tmp):
                results = harvest_reuse_items(items, "demo/SPRINT-01")
                self.assertEqual(len(results), 1)
                self.assertEqual(results[0]["kind"], "package")
                self.assertEqual(results[0]["path"], "packages/auth")
                self.assertEqual(len(list((tmp / "open").glob("LO-*.md"))), 1)

    def test_reuse_skips_token_kits_and_project_ui(self):
        items = [
            {"path": "packages/theme-tokens/design-tokens.json", "action": "promote", "covered": False, "ticket_id": "D-1"},
            {"path": "packages/ui/src/kit-root.tsx", "action": "promote", "covered": False, "ticket_id": "D-1"},
            {"path": "ui/components/molecules/media-frame.tsx", "action": "lo_ticket", "covered": False, "ticket_id": "D-1"},
        ]
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            with _patch_harvest_dirs(tmp):
                results = harvest_reuse_items(items, "demo/SPRINT-01")
                self.assertEqual(results, [])
                self.assertEqual(len(list((tmp / "open").glob("LO-*.md"))), 0)

    def test_render_emits_infusion_fields(self):
        md = render_ticket_markdown(
            {
                "id": "LO-0098",
                "title": "Classify harvest",
                "infusion_kind": "frontend",
                "infusion_path": "knowledge-base/frontend_playbook.md",
                "acceptance_criteria": ["bullet then CHANGELOG"],
            }
        )
        self.assertIn("infusion_kind: frontend", md)
        self.assertIn("infusion_path: knowledge-base/frontend_playbook.md", md)


if __name__ == "__main__":
    unittest.main()
