#!/usr/bin/env python3
"""Human inbox queues notes; abort is the only preempt."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from studio_human_inbox import ABORT_RE, classify_note
from studio_train import enqueue_train, load_queue


class ClassifyTests(unittest.TestCase):
    def test_abort_and_veto_and_note(self):
        self.assertTrue(ABORT_RE.match("stop this ticket"))
        self.assertEqual(classify_note("stop this ticket"), "abort")
        self.assertEqual(classify_note("not lemon, use Stripe"), "tech-veto")
        self.assertEqual(classify_note("also consider denser type"), "design")
        self.assertEqual(classify_note("we could add a digest email"), "feedback")
        self.assertEqual(classify_note("nudge the copy later"), "note")


class TrainQueueTests(unittest.TestCase):
    def test_enqueue_is_idempotent_on_topic(self):
        with tempfile.TemporaryDirectory() as tmp:
            queue = Path(tmp) / "train-queue.json"
            with patch("studio_train.QUEUE_PATH", queue):
                a = enqueue_train("SO-001", "layout overflow", source="mistake")
                b = enqueue_train("SO-001", "layout overflow", source="mistake")
                self.assertEqual(a["id"], b["id"])
                self.assertEqual(len(load_queue()["jobs"]), 1)


if __name__ == "__main__":
    unittest.main()
