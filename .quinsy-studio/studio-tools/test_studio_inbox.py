#!/usr/bin/env python3
"""Human inbox queues notes; abort is the only preempt."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from studio_human_inbox import (
    ABORT_RE,
    append_note,
    classify_note,
    drain_open_notes,
    open_notes,
    should_queue_as_note,
)


class ClassifyTests(unittest.TestCase):
    def test_abort_and_veto_and_note(self):
        self.assertTrue(ABORT_RE.match("stop this ticket"))
        self.assertEqual(classify_note("stop this ticket"), "abort")
        self.assertEqual(classify_note("not lemon, use Stripe"), "tech-veto")
        self.assertEqual(classify_note("also consider denser type"), "design")
        self.assertEqual(classify_note("we could add a digest email"), "feedback")
        self.assertEqual(classify_note("tweak the copy later"), "note")

    def test_should_queue_as_note(self):
        self.assertTrue(should_queue_as_note("also consider denser type"))
        self.assertTrue(should_queue_as_note("stop this ticket"))
        self.assertFalse(should_queue_as_note("back on track"))
        self.assertFalse(should_queue_as_note("approve gate 1"))
        self.assertFalse(should_queue_as_note("./studio approve demo --gate 0"))
        self.assertFalse(should_queue_as_note("approved"))
        self.assertFalse(should_queue_as_note("approved the review"))
        self.assertFalse(should_queue_as_note("looks good"))
        self.assertTrue(should_queue_as_note("looks good", named_hitl_waiting=False))
        self.assertFalse(
            should_queue_as_note(
                "Daily digest on /settings",
                named_hitl_waiting=True,
                clarify_feedback_waiting=True,
            )
        )
        self.assertFalse(should_queue_as_note("please implement HQ-T18 as well"))
        self.assertFalse(should_queue_as_note("back to quinsy-studio process"))
        self.assertFalse(should_queue_as_note("update getting started in quinsy-studio"))
        self.assertFalse(should_queue_as_note(""))


class InboxPersistTests(unittest.TestCase):
    def test_note_without_sprint_writes_docs_inbox(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "demo" / "docs").mkdir(parents=True)
            with patch("sprint_hitl.PROJECTS_DIR", root):
                note = append_note("demo", "", "also consider denser type")
                self.assertEqual(note["id"], "N-001")
                self.assertTrue((root / "demo" / "docs" / "human-inbox.json").exists())
                self.assertEqual(len(open_notes("demo", "")), 1)

    def test_open_notes_merges_pre_sprint_and_sprint(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "demo" / "docs").mkdir(parents=True)
            (root / "demo" / "sprints" / "SPRINT-01").mkdir(parents=True)
            with patch("sprint_hitl.PROJECTS_DIR", root):
                append_note("demo", "", "pre-sprint thought")
                append_note("demo", "SPRINT-01", "sprint thought")
                opened = open_notes("demo", "SPRINT-01")
                texts = [n["text"] for n in opened]
                self.assertIn("pre-sprint thought", texts)
                self.assertIn("sprint thought", texts)
                drained = drain_open_notes("demo", "SPRINT-01")
                self.assertEqual(len(drained), 2)
                self.assertEqual(open_notes("demo", "SPRINT-01"), [])


if __name__ == "__main__":
    unittest.main()
