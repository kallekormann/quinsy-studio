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

    def test_approve_review_keeps_completed_retro(self) -> None:
        import tempfile
        from pathlib import Path

        from sprint_hitl import RETRO_DONE, approve_review

        status = {
            "sprint_hitl": {
                "retro_status": RETRO_DONE,
                "retro_completed_at": "2026-09-16T12:00:00",
            }
        }
        with tempfile.TemporaryDirectory() as tmp:
            sprint_dir = Path(tmp)
            with (
                patch("sprint_hitl.sprint_directory", return_value=sprint_dir),
                patch(
                    "sprint_hitl.sprint_ticket_summary",
                    return_value={"tickets": [], "done": 0, "total": 0},
                ),
            ):
                approve_review("demo", "SPRINT-1", status, notes="skill-qa")

        self.assertEqual(status["sprint_hitl"]["retro_status"], RETRO_DONE)
        self.assertEqual(status["sprint_hitl"]["review_status"], "approved")

    def test_approve_review_sets_pending_when_retro_not_done(self) -> None:
        import tempfile
        from pathlib import Path

        from sprint_hitl import RETRO_PENDING, approve_review

        status = {"sprint_hitl": {"retro_status": None}}
        with tempfile.TemporaryDirectory() as tmp:
            sprint_dir = Path(tmp)
            with (
                patch("sprint_hitl.sprint_directory", return_value=sprint_dir),
                patch(
                    "sprint_hitl.sprint_ticket_summary",
                    return_value={"tickets": [], "done": 0, "total": 0},
                ),
            ):
                approve_review("demo", "SPRINT-1", status, notes="ok")

        self.assertEqual(status["sprint_hitl"]["retro_status"], RETRO_PENDING)


if __name__ == "__main__":
    unittest.main()
