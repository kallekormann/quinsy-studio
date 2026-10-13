#!/usr/bin/env python3
"""Clarify fields: verbatim, recurring, severity (Feedback Synthesizer)."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest import mock

import sprint_hitl
from sprint_hitl import add_feedback, clarify_feedback, find_feedback


class ClarifyFieldTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self._patch = mock.patch.object(sprint_hitl, "PROJECTS_DIR", Path(self._tmp.name))
        self._patch.start()

    def tearDown(self):
        self._patch.stop()
        self._tmp.cleanup()

    def test_approve_needs_severity(self):
        fb, _, _ = add_feedback("demo", "SPRINT-02", "The invoice list is slow to load on mobile")
        with self.assertRaises(ValueError) as err:
            clarify_feedback("demo", "SPRINT-02", fb, title="Faster invoice list", acceptance=["loads under 1 s"], approve=True)
        self.assertIn("--severity", str(err.exception))
        item, _ = clarify_feedback(
            "demo", "SPRINT-02", fb, title="Faster invoice list", acceptance=["loads under 1 s"],
            severity="major", approve=True,
        )
        self.assertEqual(item["status"], "ready")

    def test_unknown_severity_is_refused(self):
        fb, _, _ = add_feedback("demo", "SPRINT-02", "Buttons too small")
        with self.assertRaises(ValueError):
            clarify_feedback("demo", "SPRINT-02", fb, severity="urgent")

    def test_verbatim_keeps_the_human_words(self):
        raw = "honestly the reminder email reads like a robot wrote it"
        fb, _, _ = add_feedback("demo", "SPRINT-02", raw)
        item, path = clarify_feedback(
            "demo", "SPRINT-02", fb, title="Rewrite reminder email", verbatim=["and it goes out at 3am"],
        )
        self.assertEqual(item["verbatim"], [raw, "and it goes out at 3am"])
        text = path.read_text(encoding="utf-8")
        self.assertIn(f"> {raw}", text)
        self.assertIn("never edit or summarize", text)

    def test_recurring_finds_earlier_sprints(self):
        old, _, _ = add_feedback("demo", "SPRINT-01", "The invoice list is slow to load on mobile")
        sprint_hitl.update_feedback("demo", "SPRINT-01", old, {"status": "ticketed", "linked_ticket": "DEMO-0007"})
        add_feedback("demo", "SPRINT-01", "Dark mode please")
        fb, _, _ = add_feedback("demo", "SPRINT-03", "invoice list still slow on mobile")
        item, path = clarify_feedback("demo", "SPRINT-03", fb, severity="major")
        self.assertEqual(item["recurring"], [f"SPRINT-01/{old} (ticketed DEMO-0007)"])
        self.assertIn("SPRINT-01", path.read_text(encoding="utf-8"))
        self.assertEqual(find_feedback("demo", "SPRINT-03", fb)["severity"], "major")

    def test_first_time_feedback_is_not_recurring(self):
        fb, _, _ = add_feedback("demo", "SPRINT-01", "Add CSV export")
        item, path = clarify_feedback("demo", "SPRINT-01", fb, severity="minor")
        self.assertEqual(item["recurring"], [])
        self.assertIn("first time raised", path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
