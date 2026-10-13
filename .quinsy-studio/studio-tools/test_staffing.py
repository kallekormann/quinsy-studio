#!/usr/bin/env python3
"""PM-004 ticket staffing: trigger matching, companion skills, groom findings."""

import unittest

from skill_matcher import (
    INTERNAL_SKILLS,
    match_skills,
    skill_file_index,
    staff_skills,
    staffing_text,
)
from sprint_backlog_validate import staffing_findings
from ticket_helpers import SKILL_ROLE_MAP, render_staffing_section


def _codes(findings):
    return [(f.code, f.message) for f in findings]


class TriggerMatchingTests(unittest.TestCase):
    def test_short_triggers_need_a_whole_word(self):
        self.assertNotIn("AI-001", match_skills("Send welcome email after signup"))
        self.assertNotIn("AI-001", match_skills("Product detail page"))
        self.assertNotIn("AI-001", match_skills("Release readiness before main"))
        self.assertNotIn("FE-006", match_skills("Latest posts list"))
        self.assertNotIn("FE-001", match_skills("Format dates in the table"))
        self.assertNotIn("PE-002", match_skills("Build the dashboard sidebar"))

    def test_whole_words_and_plurals_still_match(self):
        self.assertIn("AI-001", match_skills("AI summary of the report"))
        self.assertIn("FE-006", match_skills("Add e2e tests for checkout"))
        self.assertIn("BE-001", match_skills("Public APIs for partners"))

    def test_new_skills_are_reachable(self):
        cases = {
            "FE-008": "Add German and English translations",
            "BE-008": "Stripe subscription billing",
            "BE-009": "Generate PDF invoice as XRechnung",
            "GM-005": "Launch on Product Hunt",
            "GM-006": "Double opt-in newsletter",
            "PE-005": "Threat model for multi-tenant hosting",
            "PE-006": "Rotate the SMTP credential",
            "PE-007": "Incident runbook and backup restore",
            "SO-005": "Release readiness reality check",
        }
        for skill_id, title in cases.items():
            with self.subTest(skill_id=skill_id):
                self.assertIn(skill_id, match_skills(title, max_skills=8))


class StaffingTests(unittest.TestCase):
    def test_auth_ticket_gets_security_and_privacy(self):
        result = staff_skills("Authentication & Authorization", "## Target\nLogin, registration, RBAC.",
                              skills=["BE-003"])
        added = [sid for sid, _ in result["added"]]
        for skill_id in ("PE-003", "AI-005", "CL-001", "PE-005"):
            self.assertIn(skill_id, added)

    def test_lead_form_ui_gets_privacy_a11y_and_tests(self):
        result = staff_skills("Lead capture form on the funnel page", skills=["FE-002"])
        added = [sid for sid, _ in result["added"]]
        for skill_id in ("CL-001", "FE-004", "FE-006"):
            self.assertIn(skill_id, added)

    def test_design_phase_skips_build_only_companions(self):
        result = staff_skills("New filter menu", skills=["UX-002"],
                              ticket_type="ui-new-component", design_status="pending")
        added = [sid for sid, _ in result["added"]]
        self.assertIn("FE-004", added)
        self.assertNotIn("FE-006", added)
        self.assertNotIn("UX-009", added)

    def test_waived_skill_is_not_required(self):
        result = staff_skills("Login page", skills=["BE-003", "FE-001"], waived=["CL-001"])
        self.assertNotIn("CL-001", [sid for sid, _ in result["missing_required"]])

    def test_limit_reports_dropped_required_skills(self):
        full = ["FE-001", "FE-002", "FE-003", "FE-005", "BE-001", "BE-002", "BE-004", "BE-006"]
        result = staff_skills("Login page with analytics", skills=full)
        self.assertEqual(len(result["skills"]), 8)
        self.assertTrue(result["dropped"])
        self.assertTrue(result["missing_required"])

    def test_utm_register_is_not_account_registration(self):
        quiet = staff_skills("UTM register for launch links", "One row per channel in docs/growth/utm-register.md")
        self.assertNotIn("PE-003", quiet["skills"])
        loud = staff_skills("Users can register with email", "")
        self.assertIn("PE-003", loud["skills"])
        self.assertIn("CL-001", loud["skills"])

    def test_status_log_and_boilerplate_are_ignored(self):
        body = "## Target\nShow totals.\n\n## Status Change\n- **Reason:** login flow broke\n"
        self.assertNotIn("login", staffing_text("Totals", body))

    def test_staffing_section_lists_reasons(self):
        text = render_staffing_section({"added": [("PE-003", "touches auth")], "dropped": []})
        self.assertIn("## Staffing", text)
        self.assertIn("- PE-003: touches auth", text)


class GroomFindingTests(unittest.TestCase):
    def _ticket(self, **kw):
        base = {"id": "DEMO-0001", "title": "Totals table", "body": "## Target\nShow totals.\n",
                "skills": "[BE-002]", "folder": "backlog"}
        base.update(kw)
        return base

    def test_empty_skills_is_an_error(self):
        codes = [c for c, _ in _codes(staffing_findings(self._ticket(skills="[]")))]
        self.assertIn("SKILLS_MISSING", codes)

    def test_unknown_skill_is_an_error(self):
        codes = [c for c, _ in _codes(staffing_findings(self._ticket(skills="[XX-999]")))]
        self.assertIn("SKILL_UNKNOWN", codes)

    def test_missing_required_companion_is_an_error(self):
        findings = staffing_findings(self._ticket(title="Authentication & Authorization", skills="[BE-003]"))
        gaps = [m for c, m in _codes(findings) if c == "STAFFING_GAP"]
        self.assertTrue(any("PE-003" in m for m in gaps))
        self.assertTrue(all(f.severity == "error" for f in findings if f.code == "STAFFING_GAP"))

    def test_staffed_ticket_is_clean(self):
        findings = staffing_findings(self._ticket(skills="[BE-002]"))
        self.assertFalse([f for f in findings if f.severity == "error"])


class RegistryConsistencyTests(unittest.TestCase):
    def test_every_ticket_skill_has_a_role(self):
        missing = [sid for sid in INTERNAL_SKILLS if sid not in SKILL_ROLE_MAP]
        self.assertEqual(missing, [])

    def test_every_ticket_skill_has_a_file(self):
        index = skill_file_index()
        missing = [sid for sid in INTERNAL_SKILLS if sid not in index]
        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
