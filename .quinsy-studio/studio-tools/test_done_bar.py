#!/usr/bin/env python3
"""Done bar hardening (LO-0399, LO-0400, LO-0401)."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import gate_ui_checks
from qa_review import implementer_id, parse_reviewer, reviewer_identity_issues
from receipt_checks import skills_read_issues


def _ticket(folder: Path, tid: str, ticket_type: str, skills: str = "[FE-001]") -> None:
    folder.mkdir(parents=True, exist_ok=True)
    (folder / f"{tid}-x.md").write_text(
        f"---\nid: {tid}\ntitle: T\nticket_type: {ticket_type}\nskills: {skills}\n---\n", encoding="utf-8"
    )


class UiInFlightTests(unittest.TestCase):
    def test_ui_ticket_detected(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            self.assertFalse(gate_ui_checks.ui_ticket_in_flight(root))
            _ticket(root / "backlog" / "implement", "ACME-0001", "feature", "[BE-001]")
            self.assertFalse(gate_ui_checks.ui_ticket_in_flight(root))
            _ticket(root / "backlog" / "implement", "ACME-0002", "ui-styling")
            self.assertTrue(gate_ui_checks.ui_ticket_in_flight(root))

    def test_motion_findings_follow_the_spec(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            _ticket(root / "backlog" / "implement", "ACME-0003", "ui-composition")
            spec = root / "docs" / "design-specs"
            spec.mkdir(parents=True)
            (spec / "ACME-0003.md").write_text(
                "## 2d. Motion (required)\n\n| Surface | Enter | Leave | Scale | Token |\n|---|---|---|---|---|\n"
                "| menu | 250ms | 150ms | 0.97 | `--motion-scale-medium` |\n\n- Reduced motion: durations at 0ms.\n\n## 3. Next\n",
                encoding="utf-8",
            )
            app = root / "app"
            app.mkdir()
            (app / "menu.tsx").write_text("export const Menu = () => <div className='x' />;\n", encoding="utf-8")
            findings = gate_ui_checks.motion_findings(root)
            self.assertTrue(any("--motion-scale-medium" in f for f in findings), findings)
            self.assertTrue(any("prefers-reduced-motion" in f for f in findings), findings)
            (app / "globals.css").write_text(
                ".menu { transition: transform var(--motion-scale-medium); }\n@media (prefers-reduced-motion: reduce) { * { transition-duration: 0ms; } }\n",
                encoding="utf-8",
            )
            self.assertEqual(gate_ui_checks.motion_findings(root), [])
            (app / "wrapped.tsx").write_text(
                "import { Button } from '@/components/ui/button';\nimport { motion } from 'framer-motion';\n"
                "export const W = () => <motion.div animate={{ x: 1 }}><Button /></motion.div>;\n",
                encoding="utf-8",
            )
            self.assertTrue(any("second animation layer" in f for f in gate_ui_checks.motion_findings(root)))

    def test_motion_off_skips(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            _ticket(root / "backlog" / "implement", "ACME-0004", "ui-composition")
            spec = root / "docs" / "design-specs"
            spec.mkdir(parents=True)
            (spec / "ACME-0004.md").write_text("motion: off\n\n## 2d. Motion\n`--motion-x`\n", encoding="utf-8")
            self.assertEqual(gate_ui_checks.motion_findings(root), [])


class ReviewerIdentityTests(unittest.TestCase):
    def test_placeholder_refused(self):
        issues = reviewer_identity_issues("Verdict: PASS\nReviewer: (context id)\n", "ctx-a")
        self.assertTrue(issues)

    def test_same_context_refused(self):
        issues = reviewer_identity_issues("Verdict: PASS\nReviewer: ctx-a\n", "ctx-a")
        self.assertTrue(any("implementing context" in i for i in issues))

    def test_different_context_passes(self):
        self.assertEqual(reviewer_identity_issues("Verdict: PASS\nReviewer: ctx-b\n", "ctx-a"), [])
        self.assertEqual(parse_reviewer("Reviewer: ctx-b"), "ctx-b")

    def test_implementer_from_log(self):
        log = {"entries": [
            {"event": "implement-start", "ticket_id": "T-1", "note": "ctx-a"},
            {"event": "implement-start", "ticket_id": "T-1", "note": "ctx-c"},
            {"event": "gate-pass", "ticket_id": "T-1"},
        ]}
        self.assertEqual(implementer_id(log, "T-1"), "ctx-c")
        self.assertEqual(implementer_id(log, "T-9"), "")


class SkillsReadTests(unittest.TestCase):
    CARD = ["teams/01-frontend-experience/skills/ui-implementation.md", "knowledge-base/frontend_playbook.md"]

    def test_missing_section(self):
        self.assertTrue(skills_read_issues("## Plan\n- x\n", self.CARD))

    def test_each_card_file_needs_a_rule(self):
        receipt = (
            "## Skills read\n"
            "- teams/01-frontend-experience/skills/ui-implementation.md — composed the kit Select instead of a native select\n"
            "- knowledge-base/frontend_playbook.md — read\n"
        )
        issues = skills_read_issues(receipt, self.CARD)
        self.assertTrue(any("frontend_playbook.md has no applied rule" in i for i in issues), issues)

    def test_file_not_on_card_fails(self):
        receipt = (
            "## Skills read\n"
            "- teams/01-frontend-experience/skills/ui-implementation.md — composed the kit Select instead of a native select\n"
            "- knowledge-base/frontend_playbook.md — motion comes from tokens, no second catalog\n"
            "- knowledge-base/backend_playbook.md — ran the migration as sprint work\n"
        )
        issues = skills_read_issues(receipt, self.CARD)
        self.assertTrue(any("not on the CARD" in i for i in issues), issues)

    def test_complete_passes(self):
        receipt = (
            "## Skills read\n"
            "- teams/01-frontend-experience/skills/ui-implementation.md — composed the kit Select instead of a native select\n"
            "- knowledge-base/frontend_playbook.md — motion comes from tokens, no second catalog\n"
        )
        self.assertEqual(skills_read_issues(receipt, self.CARD), [])

    def test_no_card_accepts_none(self):
        self.assertEqual(skills_read_issues("## Skills read\n- none\n", []), [])


if __name__ == "__main__":
    unittest.main()
