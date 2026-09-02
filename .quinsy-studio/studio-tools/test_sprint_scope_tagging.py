#!/usr/bin/env python3
"""Tests for sprint tagging (LO-0016)."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from backlog_paths import set_ticket_sprint
from sprint_planning import apply_sprint_scope


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


if __name__ == "__main__":
    unittest.main()
