#!/usr/bin/env python3
"""Growth skills GD-004 / GM-007 registration, staffing, gate 0 positioning (LO-0409..0413)."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from init_project_env import DEFINITION_TEMPLATES
from lint_skills import template_gaps
from skill_matcher import INTERNAL_SKILLS, match_skills, staff_skills
from ticket_helpers import SKILL_EXTRA_PLAYBOOKS, SKILL_ROLE_MAP

HQ = Path(__file__).resolve().parent.parent


class RegistrationTests(unittest.TestCase):
    def test_registered_in_four_places(self):
        for sid, rel in (
            ("GD-004", "teams/11-growth-design/skills/in-product-growth-loops.md"),
            ("GM-007", "teams/05-growth-marketing-content/skills/positioning-messaging.md"),
        ):
            self.assertIn(sid, INTERNAL_SKILLS)
            self.assertIn(sid, SKILL_ROLE_MAP)
            self.assertIn(sid, SKILL_EXTRA_PLAYBOOKS)
            text = (HQ / rel).read_text(encoding="utf-8")
            self.assertIn(f"skill_id: {sid}", text)
            self.assertEqual(template_gaps(text), [])
            self.assertIn(sid, (HQ / "teams" / "skill-registry.md").read_text(encoding="utf-8"))

    def test_playbooks_exist(self):
        for sid in ("GD-004", "GM-007"):
            for rel in SKILL_EXTRA_PLAYBOOKS[sid]:
                self.assertTrue((HQ / rel).is_file(), rel)

    def test_triggers(self):
        self.assertIn("GD-004", match_skills("Referral invite flow for team workspaces"))
        self.assertIn("GM-007", match_skills("Positioning and hero copy for the persona page"))


class StaffingTests(unittest.TestCase):
    def test_marketing_page_requires_gm007(self):
        result = staff_skills("Pricing page", "## Scope\nPricing table with three plans.", ["GD-002"], ticket_type="marketing-page")
        self.assertIn("GM-007", result["skills"])

    def test_growth_flow_suggests_gd004(self):
        result = staff_skills("Workspace invites", "## Scope\nInvite a teammate by email after signup.", ["FE-001"], ticket_type="feature")
        proposed = {sid for sid, _ in result["added"]} | {sid for sid, _ in result["dropped"]} | set(result["skills"])
        self.assertIn("GD-004", proposed)

    def test_backend_ticket_not_staffed_with_growth(self):
        result = staff_skills("Index the jobs table", "## Scope\nAdd a composite index.", ["BE-002"], ticket_type="feature")
        self.assertNotIn("GD-004", result["skills"])
        self.assertNotIn("GM-007", result["skills"])


class DefinitionTests(unittest.TestCase):
    def test_positioning_template_and_personas(self):
        self.assertIn("12-positioning.md", DEFINITION_TEMPLATES)
        self.assertIn("Core message", DEFINITION_TEMPLATES["12-positioning.md"])
        self.assertIn("Problem in their words", DEFINITION_TEMPLATES["02-personas.md"])

    def test_gate0_refuses_positioning_stub(self):
        import pre_impl_workflow as piw

        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            defs = root / "docs" / "definitions"
            defs.mkdir(parents=True)
            for name, body in DEFINITION_TEMPLATES.items():
                (defs / name).write_text(body, encoding="utf-8")
            original = piw.project_dir
            piw.project_dir = lambda p: root  # type: ignore[assignment]
            try:
                ok, issues = piw.validate_gate_0("demo")
            finally:
                piw.project_dir = original  # type: ignore[assignment]
            self.assertFalse(ok)
            self.assertTrue(any("12-positioning.md" in i and "GM-007" in i for i in issues), issues)


class TemplateTests(unittest.TestCase):
    def test_growth_templates_exist(self):
        for name in ("growth-loop-map.md", "persona-page-set.md", "seo-foundation-pack.md", "content-engine-pack.md"):
            self.assertTrue((HQ / "studio-templates" / "growth" / name).is_file(), name)
        self.assertIn("posts", (HQ / "knowledge-base" / "payload-playbook.md").read_text(encoding="utf-8"))
        self.assertIn("Feature-list pages are slop", (HQ / "knowledge-base" / "anti-slop-design-ux.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
