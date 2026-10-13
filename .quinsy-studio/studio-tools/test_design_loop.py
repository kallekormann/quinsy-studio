#!/usr/bin/env python3
"""Design loop (L9), gate 0 PRD frame (L10), skill lint (L13), retro metrics (L14)."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest import mock

import studio_execute
from design_ticket_helpers import design_spec_walkthrough_error
from lint_skills import lint, lint_studio, template_gaps
from process_intake import prd_frame, prd_frame_issues
from qa_review import finish_file_issues, finish_state, finish_template, needs_finish_gate
from retro_metrics import loop_metrics, metrics_lines
from studio_execute import decide_from_state

FIVE_SECOND = (
    "### Five-second test\n| Question | 390 | 1440 |\n|---|---|---|\n"
    "| What is this? | yes | yes |\n| Is it for me? | yes | yes |\n| What do I do next? | yes | yes |\n"
)
WALKTHROUGH = "## Appendix — Persona walkthrough (GD-003)\n\n### Persona: buyer\n"


class WalkthroughTests(unittest.TestCase):
    def test_every_packet_needs_a_five_second_test(self):
        self.assertIn("Five-second test", design_spec_walkthrough_error("## 1. Goal\nx\n", "ui-composition"))

    def test_five_second_test_needs_both_widths(self):
        one_width = "### Five-second test\n| Question | 1440 |\n| What is this? | yes |\n"
        self.assertIn("390", design_spec_walkthrough_error(one_width, "ui-composition"))

    def test_product_packet_passes_without_walkthrough(self):
        self.assertIsNone(design_spec_walkthrough_error(FIVE_SECOND, "ui-composition", "Settings panel"))

    def test_commercial_packet_needs_walkthrough(self):
        err = design_spec_walkthrough_error(FIVE_SECOND, "marketing-page", "Pricing page")
        self.assertIn("Persona walkthrough", err)
        self.assertIsNone(design_spec_walkthrough_error(FIVE_SECOND + WALKTHROUGH, "marketing-page"))


class FinishGateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.root = base / "demo"
        mocks = self.root / "docs" / "design-specs" / "mocks" / "T-1"
        mocks.mkdir(parents=True)
        for name in ("rest-1440.png", "rest-390.png"):
            (mocks / name).write_bytes(b"png")
        self.sprint = base / "SPRINT-01"
        shipped = self.sprint / "qa" / "T-1-finish"
        shipped.mkdir(parents=True)
        for name in ("rest-1440.png", "rest-390.png"):
            (shipped / name).write_bytes(b"png")

    def tearDown(self):
        self.tmp.cleanup()

    def _file(
        self,
        decision="PASS",
        result="PASS",
        keep="- 8px row rhythm",
        required="",
        behavior="| 1 | menu opens 250ms | matches mock route | PASS |\n",
    ):
        return (
            f"# UI finish gate — T-1\n\nDecision: {decision}\n\n## Comparison\n"
            "| State | Width | Mock | Shipped | Result |\n|---|---|---|---|---|\n"
            f"| rest | 1440 | rest-1440.png | rest-1440.png | PASS |\n"
            f"| rest | 390 | rest-390.png | rest-390.png | {result} |\n\n"
            "## Behavior (§2e walkthrough on the shipped surface)\n"
            "| Step | Expected (mock) | Shipped | Result |\n|---|---|---|---|\n"
            f"{behavior}\n"
            f"## Required before PASS\n{required}\n\n## Keep\n{keep}\n"
        )

    def test_ticket_with_mock_shots_needs_the_gate(self):
        self.assertTrue(needs_finish_gate(self.root, "T-1"))
        self.assertFalse(needs_finish_gate(self.root, "T-2"))

    def test_complete_pass_is_clean(self):
        self.assertEqual(finish_file_issues(self._file(), "PASS", self.sprint, self.root, "T-1"), [])

    def test_pass_with_a_hold_row_is_refused(self):
        issues = finish_file_issues(self._file(result="HOLD"), "PASS", self.sprint, self.root, "T-1")
        self.assertTrue(any("HOLD" in i for i in issues))

    def test_missing_state_and_capture_are_refused(self):
        (self.root / "docs/design-specs/mocks/T-1/open-390.png").write_bytes(b"png")
        (self.sprint / "qa/T-1-finish/rest-390.png").unlink()
        issues = finish_file_issues(self._file(), "PASS", self.sprint, self.root, "T-1")
        self.assertTrue(any("open-390.png is not compared" in i for i in issues))
        self.assertTrue(any("shipped capture missing" in i for i in issues))

    def test_keep_list_and_hold_items_are_required(self):
        issues = finish_file_issues(self._file("HOLD", "HOLD", keep=""), "HOLD", self.sprint, self.root, "T-1")
        self.assertTrue(any("Keep" in i for i in issues))
        self.assertTrue(any("Required before PASS" in i for i in issues))

    def test_template_lists_every_mock_shot(self):
        text = finish_template("T-1", "SPRINT-01", ["rest-1440.png", "rest-390.png"])
        self.assertIn("rest-390.png", text)
        self.assertIn("Decision:", text)
        self.assertIn("Behavior (§2e walkthrough", text)

    def test_missing_behavior_walkthrough_is_refused(self):
        issues = finish_file_issues(self._file(behavior=""), "PASS", self.sprint, self.root, "T-1")
        self.assertTrue(any("§2e" in i for i in issues))

    def test_pass_with_behavior_hold_row_is_refused(self):
        issues = finish_file_issues(
            self._file(behavior="| 1 | menu opens 250ms | instant, no motion | HOLD |\n"),
            "PASS",
            self.sprint,
            self.root,
            "T-1",
        )
        self.assertTrue(any("HOLD" in i for i in issues))

    def test_new_green_gate_resets_finish_state(self):
        log = {"entries": [
            {"ticket": "T-1", "event": "finish-pass"},
            {"ticket": "T-1", "event": "gate-pass"},
        ]}
        self.assertEqual(finish_state(log, "T-1"), "none")

    def test_execute_runs_the_finish_gate_before_move_done(self):
        status = {
            "human_gates": {k: {"status": "approved"} for k in ("0", "1", "2")},
            "current_sprint": "SPRINT-01",
            "sprint_hitl": {"scope_status": "approved", "groom_status": "approved", "review_status": None},
            "gate": "5",
            "gate_status": "passed",
        }
        tickets = [{"id": "T-1", "status": "implement", "deps": [], "card": {"id": "T-1"}}]
        entries = [
            {"ticket": "T-1", "event": "implement", "ts": "2026-10-12T10:00:00"},
            {"ticket": "T-1", "event": "gate-pass", "ts": "2026-10-12T10:10:00"},
            {"ticket": "T-1", "event": "qa-pass", "ts": "2026-10-12T10:20:00"},
        ]

        def decide(log):
            return decide_from_state(
                "demo", status, tickets, log=log, receipts_ok={"T-1": True},
                open_los=[], amendment_actions=[], prd_exists=True,
            )

        with mock.patch.object(studio_execute, "PROJECTS_DIR", Path(self.tmp.name)):
            step = decide({"entries": entries})
            self.assertEqual(step.kind, "QA_REVIEW")
            self.assertIn("--finish", step.command)
            step = decide({"entries": entries + [{"ticket": "T-1", "event": "finish-pass"}]})
            self.assertEqual(step.kind, "MOVE_DONE")


FILLED_FRAME = """## Gate 0 frame

### Press release

Today small trades in Bavaria can send a reminder for an unpaid invoice in one tap from the job list. Until now they chased payments by phone after hours, which cost an evening a week. "I got paid for March before April started," says a tiler from Augsburg who tried the early version during the pilot.

### Non-goals

- No accounting or tax filing

### Metrics

| Metric | Baseline | Target | Window |
|--------|----------|--------|--------|
| Invoices paid within 14 days | unknown | 70% | first 8 weeks |

### Pre-mortem

- Trades never connect their invoice tool
- Reminders land in spam
- The price is above what a two-person shop pays for software
"""


class PrdFrameTests(unittest.TestCase):
    def test_missing_frame_is_refused(self):
        self.assertTrue(prd_frame_issues("# PRD\n\n## Problem\nx\n"))

    def test_generated_frame_is_not_filled(self):
        issues = prd_frame_issues("# PRD\n\n" + prd_frame())
        for want in ("press release", "non-goal", "metric row", "pre-mortem"):
            self.assertTrue(any(want in i for i in issues), want)

    def test_filled_frame_passes(self):
        self.assertEqual(prd_frame_issues("# PRD\n\n" + FILLED_FRAME), [])

    def test_all_unknown_targets_are_refused(self):
        text = FILLED_FRAME.replace("| 70% |", "| unknown |")
        self.assertTrue(any("target" in i for i in prd_frame_issues(text)))

    def test_source_headings_outside_the_frame_do_not_count(self):
        text = "## Sources\n\n### Pre-mortem\n- a\n- b\n- c\n\n" + prd_frame()
        self.assertTrue(any("pre-mortem" in i for i in prd_frame_issues(text)))

    def test_scope_out_bullets_seed_non_goals(self):
        self.assertIn("- No payroll", prd_frame("- No payroll"))


class SkillLintTests(unittest.TestCase):
    def test_studio_skill_lists_are_in_sync(self):
        errors = [str(f) for f in lint_studio() if f.severity == "error"]
        self.assertEqual(errors, [])

    def test_drift_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            teams = Path(tmp) / "teams"
            (teams / "01-frontend-experience" / "skills").mkdir(parents=True)
            (teams / "02-backend-systems" / "skills").mkdir(parents=True)
            (teams / "01-frontend-experience/skills/a.md").write_text("skill_id: FE-001\n", encoding="utf-8")
            (teams / "02-backend-systems/skills/b.md").write_text("skill_id: FE-002\n", encoding="utf-8")
            (teams / "skill-registry.md").write_text("| A | FE-001 |\n| Old | FE-099 |\n", encoding="utf-8")
            findings = lint(
                ["FE-001", "FE-002", "FE-003"],
                {"FE-001": "Lead", "FE-002": "Lead"},
                {"FE": "01-frontend-experience", "BE": "02-backend-systems"},
                ["FE-777"],
                teams,
            )
            text = "\n".join(str(f) for f in findings if f.severity == "error")
            self.assertIn("FE-003 is in skill_matcher but has no role", text)
            self.assertIn("FE-003 has no skill file", text)
            self.assertIn("prefix FE belongs to teams/01-frontend-experience/", text)
            self.assertIn("staffing rule names FE-777", text)
            self.assertIn("FE-002 is missing from teams/skill-registry.md", text)
            self.assertIn("names FE-099", text)

    def test_template_file_has_every_section(self):
        template = Path(__file__).resolve().parent.parent / "knowledge-base" / "skill-template.md"
        self.assertEqual(template_gaps(template.read_text(encoding="utf-8")), [])


class RetroMetricsTests(unittest.TestCase):
    def test_metrics_come_from_the_log(self):
        log = {"entries": [
            {"ticket": "T-1", "event": "gate-pass"},
            {"ticket": "T-1", "event": "qa-pass"},
            {"ticket": "T-2", "event": "gate-fail", "note": "gate red: a11y_axe,secret_scan"},
            {"ticket": "T-2", "event": "gate-pass"},
            {"ticket": "T-2", "event": "qa-fail", "note": "qa fail: AC2"},
            {"ticket": "T-3", "event": "gate-fail", "note": "gate red: a11y_axe"},
            {"ticket": "T-3", "event": "qa-fail", "note": "finish hold: menu covers save"},
        ]}
        with tempfile.TemporaryDirectory() as tmp:
            sprint = Path(tmp)
            (sprint / "escalations").mkdir()
            (sprint / "escalations" / "T-3.md").write_text("x", encoding="utf-8")
            metrics = loop_metrics(log, sprint)
        self.assertEqual(metrics["gated"], 3)
        self.assertEqual(metrics["first_pass"], 1)
        self.assertEqual(metrics["per_check"], {"a11y_axe": 2, "secret_scan": 1})
        self.assertAlmostEqual(metrics["avg_retries"], 4 / 3)
        self.assertEqual((metrics["qa_fails"], metrics["finish_holds"]), (1, 1))
        self.assertEqual(metrics["blocked"], ["T-3"])
        lines = "\n".join(metrics_lines(metrics))
        self.assertIn("First-pass gate: 1/3", lines)
        self.assertIn("a11y_axe: 1/3", lines)

    def test_empty_log_says_so(self):
        with tempfile.TemporaryDirectory() as tmp:
            lines = metrics_lines(loop_metrics({"entries": []}, Path(tmp)))
        self.assertIn("no ticket reached the gate", lines[0])


if __name__ == "__main__":
    unittest.main()
