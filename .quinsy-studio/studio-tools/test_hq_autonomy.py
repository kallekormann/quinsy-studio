#!/usr/bin/env python3
"""HQ autonomy: guard order, loop separation, agent-signed architecture, cadence INFORM (LO-0415..0417)."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from studio_context import guard_request, loop_separation_issues
from studio_execute import decide_from_state


def _status(**over):
    base = {
        "human_gates": {"0": {"status": "approved"}, "1": {"status": "approved"}, "2": {"status": "approved"}},
        "current_sprint": "SPRINT-01",
        "sprint_kind": "implementation",
        "gate": "5",
        "gate_status": "passed",
        "sprint_hitl": {"review_status": None, "scope_status": "approved", "groom_status": "approved"},
    }
    base.update(over)
    return base


class GuardOrderTests(unittest.TestCase):
    def test_hq_work_about_ideation_is_studio_meta(self):
        with patch("studio_context.implementation_in_flight", return_value=False), patch(
            "studio_context.named_hitl_waiting", return_value=False
        ), patch("studio_isolation.request_names_sibling", return_value=None):
            verdict, _ = guard_request("demo", "LO-0416: fix the guard so HQ work about the ideation loop is not an ideate session", {})
        self.assertEqual(verdict, "studio_meta")

    def test_plain_ideate_still_ideates(self):
        with patch("studio_context.implementation_in_flight", return_value=False), patch(
            "studio_context.named_hitl_waiting", return_value=False
        ), patch("studio_isolation.request_names_sibling", return_value=None), patch(
            "studio_ideate.session_is_open", return_value=False
        ):
            verdict, _ = guard_request("demo", "ideate: tools for independent bakers", {})
        self.assertEqual(verdict, "ideate")


class LoopSeparationTests(unittest.TestCase):
    def test_clean_root_passes(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            (root / ".gitignore").write_text("projects/\nintake/\nideation/\n", encoding="utf-8")
            (root / ".quinsy-studio").mkdir()
            (root / "ideation" / "sessions").mkdir(parents=True)
            (root / "projects" / "demo").mkdir(parents=True)
            self.assertEqual(loop_separation_issues(root), [])

    def test_mixed_loops_fail(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            (root / ".gitignore").write_text("projects/\n", encoding="utf-8")
            (root / ".quinsy-studio" / "apps").mkdir(parents=True)
            (root / "ideation" / "cases" / "src").mkdir(parents=True)
            (root / "projects" / "demo" / ".quinsy-studio").mkdir(parents=True)
            issues = loop_separation_issues(root)
            joined = "\n".join(issues)
            self.assertIn("ideation/", joined)
            self.assertIn("projects/demo/.quinsy-studio", joined)
            self.assertIn(".quinsy-studio/apps", joined)
            self.assertIn("intake/", joined)


class ExecuteAutonomyTests(unittest.TestCase):
    def test_cadence_review_is_inform(self):
        status = _status(sprint_hitl={"review_status": "pending", "scope_status": "approved", "groom_status": "approved"})
        tickets = [{"id": "T-1", "status": "done", "deps": []}]
        with patch("reality_check.reality_state", return_value="ready"):
            step = decide_from_state("demo", status, tickets, open_los=[], amendment_actions=[], prd_exists=True)
        self.assertEqual(step.kind, "VERIFY")
        self.assertIn("--inform", step.command)
        self.assertTrue(step.inform)

    def test_no_hitl_step_names_approve_arch(self):
        import studio_execute

        src = Path(studio_execute.__file__).read_text(encoding="utf-8")
        # the phase sign-off and per-ticket sign-off are VERIFY now; only the help text may mention approve-arch as HITL history
        self.assertNotIn('_hitl(\n                "arch-approve"', src)
        self.assertNotIn('reason="production packet ready — human approve-arch"', src)


if __name__ == "__main__":
    unittest.main()
