#!/usr/bin/env python3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import studio_cite as cite
import studio_infusion_delta as delta


class CiteTests(unittest.TestCase):
    def test_parse_and_apply(self):
        tmp = tempfile.TemporaryDirectory()
        play = Path(tmp.name) / "frontend_playbook.md"
        play.write_text("# F\n", encoding="utf-8")
        with patch.object(delta, "QUINSY_STUDIO", Path(tmp.name)):
            added = delta.apply_delta(str(play), "add", body="Use kit first")
            receipt = (
                "## Playbook citations\n"
                f"- playbook: {play.name}\n"
                f"- helpful: {added['id']}\n"
                "- harmful: none\n"
            )
            applied = cite.apply_receipt_citations(receipt)
            self.assertEqual(len(applied), 1)
            self.assertEqual(applied[0]["helpful"], 1)
        tmp.cleanup()


if __name__ == "__main__":
    unittest.main()
