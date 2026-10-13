#!/usr/bin/env python3
"""The launch ticket pack passes PM-004 staffing and names only real skills."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

from skill_matcher import is_known_skill, staff_skills

PACK = Path(__file__).resolve().parent.parent / "studio-templates" / "growth" / "launch-ticket-pack.md"
UI_TICKETS = {"L2", "L3", "L6"}


def _tickets():
    text = PACK.read_text(encoding="utf-8")
    for block in re.split(r"^### ", text, flags=re.M)[1:]:
        head, body = block.split("\n", 1)
        tid = head.split(" ", 1)[0]
        title = head.split("—", 1)[1].strip()
        staffing = body.split("## Staffing", 1)[1]
        skills = re.findall(r"^- ([A-Z]{2}-\d{3})", staffing, re.M)
        yield tid, title, body.split("## Staffing", 1)[0], skills


class LaunchPackTests(unittest.TestCase):
    def test_pack_has_eight_tickets(self):
        self.assertEqual([t[0] for t in _tickets()], [f"L{i}" for i in range(1, 9)])

    def test_every_skill_is_known(self):
        for tid, _, _, skills in _tickets():
            with self.subTest(ticket=tid):
                self.assertTrue(skills)
                self.assertEqual([s for s in skills if not is_known_skill(s)], [])

    def test_every_ticket_passes_staffing(self):
        for tid, title, body, skills in _tickets():
            with self.subTest(ticket=tid):
                ticket_type = "marketing-page" if tid == "L2" else ("ui-composition" if tid in UI_TICKETS else "")
                result = staff_skills(title, body, skills=skills, ticket_type=ticket_type)
                self.assertEqual(result["missing_required"], [])
                self.assertLessEqual(len(skills), 8)

    def test_playbook_lists_the_same_tickets(self):
        playbook = (PACK.parent.parent.parent / "knowledge-base" / "launch-playbook.md").read_text(encoding="utf-8")
        for tid, title, _, _ in _tickets():
            self.assertIn(f"| {tid} | {title}", playbook)


if __name__ == "__main__":
    unittest.main()
