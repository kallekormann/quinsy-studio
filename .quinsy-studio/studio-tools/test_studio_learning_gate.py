#!/usr/bin/env python3
"""Studio learning infusion gate tests (unittest — discoverable)."""

from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from studio_learning_gate import can_infuse_project_sprint, infusion_gate_message, open_lo_tickets


class OpenLoTests(unittest.TestCase):
    def test_open_lo_list_is_list(self):
        self.assertIsInstance(open_lo_tickets(), list)


class InfusionMessageTests(unittest.TestCase):
    def test_infusion_message_when_open(self):
        with TemporaryDirectory() as tmp:
            backlog = Path(tmp) / "backlog" / "open"
            backlog.mkdir(parents=True)
            (backlog / "LO-0099-test.md").write_text(
                "---\nid: LO-0099\ntitle: Test item\npriority: P1\n---\n",
                encoding="utf-8",
            )
            with patch("studio_learning_gate.BACKLOG_OPEN", backlog):
                msg = infusion_gate_message()
                self.assertIsNotNone(msg)
                self.assertIn("LO-0099", msg)
                ok, _ = can_infuse_project_sprint()
                self.assertTrue(ok)

    def test_no_message_when_empty(self):
        with TemporaryDirectory() as tmp:
            backlog = Path(tmp) / "backlog" / "open"
            backlog.mkdir(parents=True)
            with patch("studio_learning_gate.BACKLOG_OPEN", backlog):
                self.assertIsNone(infusion_gate_message())


if __name__ == "__main__":
    unittest.main()
