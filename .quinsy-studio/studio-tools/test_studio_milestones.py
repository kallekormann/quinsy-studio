#!/usr/bin/env python3
"""Milestone ownership: coverage, plan lines, review, execute wiring."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import studio_milestones as sm
from studio_execute import decide_from_state


def _status_2b(**extra):
    status = {"human_gates": {"0": {"status": "approved"}, "1": {"status": "approved"},
                              "2a": {"status": "approved"}, "2b": {"status": "approved"}},
              "phase": "4"}
    status.update(extra)
    return status


FULL_ROADMAP = """# M0 — Foundation

**Status:** planned

## Coverage
scaffold, database schema and migration, api endpoints, auth and login with roles,
security hardening and threat model, privacy and consent, performance budget,
app shell layout and routing, user flow and onboarding, motion and transition,
ops deploy and backup, tests and a11y.

## Tickets

- Project scaffold :: repo layout and app shell
- Login and session :: Payload auth
"""


class CoverageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.projects = Path(self.tmp.name)
        self.root = self.projects / "acme-app"
        (self.root / "docs" / "phases").mkdir(parents=True)
        (self.root / "docs" / "intake").mkdir(parents=True)
        (self.root / "docs" / "intake" / "prd.md").write_text("An internal tool.\n", encoding="utf-8")
        self.p1 = patch.object(sm, "PROJECTS_DIR", self.projects)
        self.p1.start()

    def tearDown(self):
        self.p1.stop()
        self.tmp.cleanup()

    def test_no_files_is_an_issue(self):
        self.assertTrue(sm.coverage_issues("acme-app"))

    def test_full_roadmap_passes(self):
        (self.root / "docs" / "phases" / "M0-foundation.md").write_text(FULL_ROADMAP, encoding="utf-8")
        self.assertEqual(sm.coverage_issues("acme-app"), [])

    def test_missing_security_is_named(self):
        text = FULL_ROADMAP.replace("security hardening and threat model, ", "")
        (self.root / "docs" / "phases" / "M0-foundation.md").write_text(text, encoding="utf-8")
        issues = sm.coverage_issues("acme-app")
        self.assertTrue(any("Security hardening" in i for i in issues), issues)

    def test_public_product_requires_growth_rows(self):
        (self.root / "docs" / "intake" / "prd.md").write_text("A SaaS with a landing page and signup.\n", encoding="utf-8")
        (self.root / "docs" / "phases" / "M0-foundation.md").write_text(FULL_ROADMAP, encoding="utf-8")
        issues = sm.coverage_issues("acme-app")
        labels = " ".join(issues)
        for label in ("SEO and AEO", "Growth loops", "Positioning", "Content engine", "Launch"):
            self.assertIn(label, labels)

    def test_billing_required_only_when_prd_prices(self):
        (self.root / "docs" / "phases" / "M0-foundation.md").write_text(FULL_ROADMAP, encoding="utf-8")
        self.assertEqual(sm.coverage_issues("acme-app"), [])
        (self.root / "docs" / "intake" / "prd.md").write_text("Monthly subscription with checkout.\n", encoding="utf-8")
        self.assertTrue(any("Billing" in i for i in sm.coverage_issues("acme-app")))

    def test_plan_lines_and_replacement(self):
        lines = sm.planned_ticket_lines(FULL_ROADMAP)
        self.assertEqual(lines, [("Project scaffold", "repo layout and app shell"), ("Login and session", "Payload auth")])
        out = sm.replace_plan_line(FULL_ROADMAP, "Project scaffold", "ACME-0001")
        self.assertIn("- ACME-0001 — Project scaffold", out)
        self.assertEqual(len(sm.planned_ticket_lines(out)), 1)

    def test_stamp_milestone_frontmatter(self):
        content = "---\nid: ACME-0001\ncreated: 2026-10-13\n---\n\nbody\n"
        out = sm.stamp_milestone(content, "M0")
        self.assertIn("milestone: M0\ncreated:", out)
        self.assertEqual(sm.stamp_milestone(out, "M1").count("milestone:"), 1)

    def test_review_written_with_recommendations(self):
        (self.root / "docs" / "phases" / "M0-foundation.md").write_text(FULL_ROADMAP, encoding="utf-8")
        for folder, tid in (("done", "ACME-0001"), ("blocked", "ACME-0002")):
            d = self.root / "backlog" / folder
            d.mkdir(parents=True, exist_ok=True)
            (d / f"{tid}-x.md").write_text(
                f"---\nid: {tid}\ntitle: T {tid}\nmilestone: M0\nticket_type: ui-composition\n---\n", encoding="utf-8"
            )
        status = _status_2b()
        status["human_gates"]["milestones"] = {"status": "approved"}
        with patch("backlog_paths.PROJECTS_DIR", self.projects):
            self.assertFalse(sm.milestone_complete("acme-app", "M0"))  # blocked is not done
            path = sm.write_review("acme-app", status, "M0")
        text = path.read_text(encoding="utf-8")
        self.assertIn("## Recommendations", text)
        self.assertIn("Re-iterate the architecture", text)
        self.assertIn("design phase", text)
        self.assertIn("## Catalog applied", text)
        self.assertEqual(status["milestones"]["review"]["status"], "written")

    def test_approve_marks_done_and_next_activates(self):
        (self.root / "docs" / "phases" / "M0-foundation.md").write_text(FULL_ROADMAP, encoding="utf-8")
        (self.root / "docs" / "phases" / "M1-growth.md").write_text("# M1 — Growth\n\n**Status:** planned\n", encoding="utf-8")
        status = _status_2b()
        with patch("backlog_paths.PROJECTS_DIR", self.projects):
            sm.write_review("acme-app", status, "M0")
        ok, messages = sm.approve_review("acme-app", status, "M0", notes="ship it")
        self.assertTrue(ok)
        self.assertTrue(any("soft:" in m for m in messages))
        self.assertIn("M0", status["milestones"]["done"])
        self.assertEqual(sm.activate_next("acme-app", status), "M1")
        self.assertIn("**Status:** active", (self.root / "docs" / "phases" / "M1-growth.md").read_text(encoding="utf-8"))

    def test_catalog_citations(self):
        text = "## Catalog applied\n\n- PB-20261001-003 shaped the order\n\n## Next\nPB-20261001-999"
        self.assertEqual(sm.catalog_citations(text), ["PB-20261001-003"])


class ExecuteWiringTests(unittest.TestCase):
    def test_roadmap_gap_is_pm_implement(self):
        step = decide_from_state("acme-app", _status_2b(), [], milestone={
            "roadmap_approved": False, "coverage_issues": ["Security hardening (security) has no milestone"],
            "active": None, "complete": False, "review": "missing", "has_tickets": False,
        })
        self.assertEqual(step.kind, "IMPLEMENT")
        self.assertIn("PM-002", step.reason)
        self.assertEqual(step.card["id"], "MILESTONE")

    def test_covered_roadmap_is_hitl(self):
        step = decide_from_state("acme-app", _status_2b(), [], milestone={
            "roadmap_approved": False, "coverage_issues": [], "active": None,
            "complete": False, "review": "missing", "has_tickets": False,
        })
        self.assertEqual(step.kind, "HITL")
        self.assertIn("--milestones", step.command)

    def test_complete_milestone_routes_to_review_then_hitl(self):
        base = {"roadmap_approved": True, "coverage_issues": [], "active": "M0", "has_tickets": True, "complete": True}
        step = decide_from_state("acme-app", _status_2b(), [], milestone={**base, "review": "missing"})
        self.assertEqual(step.command, "./studio milestone acme-app review")
        step = decide_from_state("acme-app", _status_2b(), [], milestone={**base, "review": "written"})
        self.assertEqual(step.kind, "HITL")
        self.assertIn("--approve", step.command)

    def test_active_without_tickets_plans(self):
        step = decide_from_state("acme-app", _status_2b(), [], milestone={
            "roadmap_approved": True, "coverage_issues": [], "active": "M0",
            "has_tickets": False, "complete": False, "review": "missing",
        })
        self.assertEqual(step.command, "./studio milestone acme-app plan")

    def test_no_milestone_signal_keeps_old_path(self):
        step = decide_from_state("acme-app", _status_2b(), [])
        self.assertIn("./studio sprint", step.command)


if __name__ == "__main__":
    unittest.main()
