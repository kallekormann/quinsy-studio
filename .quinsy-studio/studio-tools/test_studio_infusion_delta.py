#!/usr/bin/env python3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import studio_infusion_delta as delta


class InfusionDeltaTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.kb = self.root = self.root
        self.play = Path(self.tmp.name) / "frontend_playbook.md"
        self.play.write_text("# Frontend\n\n## Kit\n\nExisting prose.\n", encoding="utf-8")
        self.patcher = patch.object(delta, "QUINSY_STUDIO", Path(self.tmp.name))
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()
        self.tmp.cleanup()

    def test_add_has_counters(self):
        result = delta.apply_delta(str(self.play), "add", section="Deltas", body="Do pull the kit before custom CSS.")
        self.assertEqual(result["op"], "add")
        text = self.play.read_text(encoding="utf-8")
        self.assertIn("helpful=0 harmful=0", text)
        bumped = delta.bump_counts(str(self.play), result["id"], helpful=1)
        self.assertEqual(bumped["helpful"], 1)

    def test_update_and_remove(self):
        delta.apply_delta(str(self.play), "add", section="Deltas", body="First bullet")
        text = self.play.read_text(encoding="utf-8")
        bid = [p for p in text.split() if p.startswith("**PB-")][0].strip("*")
        delta.apply_delta(str(self.play), "update", body="Updated rule", bullet_id=bid)
        self.assertIn("Updated rule", self.play.read_text(encoding="utf-8"))
        delta.apply_delta(str(self.play), "remove", bullet_id=bid)
        self.assertNotIn(bid, self.play.read_text(encoding="utf-8"))

    def test_refuse_rewrite(self):
        huge = "x" * 2000
        self.play.write_text("# tiny\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            delta.apply_delta(str(self.play), "add", body=huge)


if __name__ == "__main__":
    unittest.main()
