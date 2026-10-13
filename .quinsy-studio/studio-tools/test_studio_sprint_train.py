#!/usr/bin/env python3
"""Sprint train: design, then architecture, then implementation. Empty phases skip."""

from __future__ import annotations

import unittest
from unittest.mock import patch

from studio_sprint_train import (
    advance_cycle,
    architecture_delta,
    first_schedulable_phase,
    mark_architecture_rejected,
    ticket_phase,
    design_phase_action,
)
from studio_execute import decide_from_state


def _approved_status(**kwargs):
    base = {
        "human_gates": {
            "0": {"status": "approved"},
            "1": {"status": "approved"},
            "2": {"status": "approved"},
        },
        "current_sprint": "SPRINT-01",
        "sprint_hitl": {
            "scope_status": "approved",
            "groom_status": "approved",
            "review_status": None,
        },
        "gate": "5",
        "gate_status": "passed",
    }
    base.update(kwargs)
    return base


class TrainPhaseTests(unittest.TestCase):
    def test_pending_design_is_not_implementation(self):
        self.assertEqual(ticket_phase({"design_status": "pending", "body": ""}), "design")
        self.assertEqual(
            ticket_phase({"design_status": "approved", "architecture_status": "pending", "body": ""}),
            "architecture",
        )
        self.assertEqual(ticket_phase({"design_status": "n/a", "body": ""}), "implementation")

    def test_empty_design_skips_to_implementation(self):
        rows = [{"id": "DEMO-0002", "design_status": "n/a", "body": "", "status": "backlog"}]
        with patch("studio_sprint_train.list_unscheduled_backlog", return_value=rows):
            phase, skipped = first_schedulable_phase("demo", "design")
        self.assertEqual(phase, "implementation")
        self.assertEqual(skipped, ["design", "architecture"])

    def test_architecture_delta_required(self):
        self.assertIsNone(architecture_delta("No line here"))
        self.assertEqual(architecture_delta("architecture delta: none"), "none")
        self.assertEqual(architecture_delta("architecture delta: DEMO-0109"), "DEMO-0109")

    def test_reject_returns_to_design(self):
        text = "---\ndesign_status: approved\narchitecture_status: pending\nsprint: SPRINT-02\n---\n"
        out = mark_architecture_rejected(text, "quota read does not exist")
        self.assertIn("design_status: pending", out)
        self.assertIn("cycle_return: design", out)
        self.assertIn("sprint: none", out)
        self.assertEqual(ticket_phase({"body": out}), "design")

    def test_design_phase_waits_for_delta_before_signature(self):
        ticket = {
            "id": "DEMO-0008",
            "status": "backlog",
            "path": "/tmp/projects/demo/backlog/DEMO-0008.md",
            "body": "design_status: pending\n",
        }
        with patch(
            "design_ticket_helpers.design_deliverables_status",
            return_value=("approve", None),
        ):
            action = design_phase_action([ticket])
        self.assertEqual(action["mode"], "delta")

    def test_ready_sibling_is_not_blocked_by_unsigned_ticket(self):
        step = decide_from_state(
            "demo",
            _approved_status(sprint_kind="implementation"),
            [
                {"id": "DEMO-0108", "status": "backlog", "deps": [], "design_status": "pending"},
                {"id": "DEMO-0109", "status": "backlog", "deps": []},
            ],
            open_los=[],
            amendment_actions=[],
            prd_exists=True,
            skip_ticket_ids={"DEMO-0108"},
        )
        self.assertEqual(step.kind, "IMPLEMENT")
        self.assertEqual(step.ticket_id, "DEMO-0109")

    def test_advance_after_implementation_starts_next_cycle_at_design(self):
        self.assertEqual(
            advance_cycle({"n": 2, "phase": "implementation"}),
            {"n": 3, "phase": "design"},
        )


if __name__ == "__main__":
    unittest.main()
