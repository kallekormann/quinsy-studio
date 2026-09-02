"""LO-0025: review --approve refuses when sprint tickets are not all done."""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch


class ReviewApproveGateTests(unittest.TestCase):
    def test_approve_refuses_when_tickets_incomplete(self) -> None:
        from studio import StudioOrchestrator

        orch = StudioOrchestrator()
        status = {"current_sprint": "SPRINT-99", "sprint_hitl": {}}
        summary = {
            "total": 2,
            "done": 0,
            "all_done": False,
            "tickets": [
                {"id": "MOOD-0001", "status": "implement", "title": "A"},
                {"id": "MOOD-0002", "status": "open", "title": "B"},
            ],
        }

        with (
            patch("studio.load_status", return_value=status),
            patch("studio.sprint_ticket_summary", return_value=summary),
            patch("studio.approve_review") as approve_mock,
            patch("studio.save_status") as save_mock,
            patch("studio.print_header"),
            patch("builtins.print"),
        ):
            ok = orch.cmd_review("moody", approve=True, notes="premature")

        self.assertFalse(ok)
        approve_mock.assert_not_called()
        save_mock.assert_not_called()

    def test_approve_allowed_when_all_done(self) -> None:
        from studio import StudioOrchestrator

        orch = StudioOrchestrator()
        status = {"current_sprint": "SPRINT-99", "sprint_hitl": {}}
        summary = {
            "total": 1,
            "done": 1,
            "all_done": True,
            "tickets": [{"id": "MOOD-0001", "status": "done", "title": "A"}],
        }

        with (
            patch("studio.load_status", return_value=status),
            patch("studio.sprint_ticket_summary", return_value=summary),
            patch("studio.approve_review") as approve_mock,
            patch("studio.save_status") as save_mock,
            patch("studio.print_header"),
            patch("builtins.print"),
        ):
            ok = orch.cmd_review("moody", approve=True, notes="ok")

        self.assertTrue(ok)
        approve_mock.assert_called_once()
        save_mock.assert_called_once()


if __name__ == "__main__":
    unittest.main()
