#!/usr/bin/env python3
"""Tests for sprint tagging (LO-0016)."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from backlog_paths import set_ticket_sprint
from sprint_planning import _ticket_seq, apply_sprint_scope


class TestFromFeedbackSort(unittest.TestCase):
    def test_newer_from_feedback_sorts_first(self):
        rows = [
            {"from_feedback": True, "priority": "P0", "id": "X-0252"},
            {"from_feedback": True, "priority": "P0", "id": "X-0275"},
            {"from_feedback": False, "priority": "P0", "id": "X-0300"},
        ]
        rows.sort(
            key=lambda t: (
                0 if t["from_feedback"] else 1,
                -_ticket_seq(t["id"]),
            ),
        )
        self.assertEqual([r["id"] for r in rows], ["X-0275", "X-0252", "X-0300"])


class TestSetTicketSprint(unittest.TestCase):
    def test_sets_when_missing(self):
        body = "---\nid: T-1\ncreated: 2026-08-26\n---\n\n# T\n"
        out = set_ticket_sprint(body, "SPRINT-41")
        self.assertIn("sprint: SPRINT-41", out)

    def test_replaces_existing_sprint(self):
        body = "---\nid: T-1\nsprint: SPRINT-40\ncreated: 2026-08-26\n---\n\n# T\n"
        out = set_ticket_sprint(body, "SPRINT-41")
        self.assertIn("sprint: SPRINT-41", out)
        self.assertNotIn("sprint: SPRINT-40", out)

    def test_idempotent_same_sprint(self):
        body = "---\nid: T-1\nsprint: SPRINT-41\ncreated: 2026-08-26\n---\n\n# T\n"
        self.assertEqual(set_ticket_sprint(body, "SPRINT-41"), body)


class TestApplySprintScope(unittest.TestCase):
    def test_tags_and_reports_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            backlog = root / "projects" / "demo" / "backlog"
            backlog.mkdir(parents=True)
            ticket = backlog / "MOOD-0204-dropdown.md"
            ticket.write_text(
                "---\nid: MOOD-0204\nsprint: SPRINT-40\ncreated: 2026-08-26\n---\n\n# D\n",
                encoding="utf-8",
            )
            proposal = {"proposed": [{"id": "MOOD-0204"}, {"id": "MOOD-9999"}]}

            with patch("backlog_paths.queue_ticket_paths", return_value=[ticket]):
                count, missing = apply_sprint_scope("demo", "SPRINT-41", proposal)

            self.assertEqual(count, 1)
            self.assertEqual(missing, ["MOOD-9999"])
            self.assertIn("sprint: SPRINT-41", ticket.read_text(encoding="utf-8"))


from sprint_hitl import open_sprint_ticket_ids


class TestOpenSprintTicketIds(unittest.TestCase):
    def test_move_done_does_not_treat_remaining_tickets_as_sprint_complete(self):
        remaining = open_sprint_ticket_ids(
            [
                {"id": "X-0807", "status": "done"},
                {"id": "X-0806", "status": "backlog"},
                {"id": "X-0805", "status": "implement"},
                {"id": "X-0808", "status": "backlog"},
            ]
        )
        self.assertEqual(remaining, ["X-0806", "X-0805", "X-0808"])

    def test_cancelled_is_not_remaining_work(self):
        self.assertEqual(
            open_sprint_ticket_ids(
                [{"id": "X-1", "status": "done"}, {"id": "X-2", "status": "cancelled"}]
            ),
            [],
        )


if __name__ == "__main__":
    unittest.main()
