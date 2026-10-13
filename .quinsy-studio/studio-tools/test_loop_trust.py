#!/usr/bin/env python3
"""Loop trust (agency integration L1, L2, L3, L6): receipts, QA verdicts, fail feedback."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from qa_review import qa_state, verdict_file_issues
from receipt_checks import (
    missing_paths,
    required_sections,
    section_is_stub,
    stub_sections,
    trust_issues,
    verdict_issues,
)
from studio_execute import (
    MAX_GATE_RETRIES,
    count_gate_fails,
    decide_from_state,
    receipt_issues,
    repeated_failure,
    should_escalate,
)

UI_TICKET = "---\nid: T-1\ntitle: Board export button\nticket_type: ui-composition\nskills: [FE-001]\n---\n## Target\nExport button on the board.\n"
API_TICKET = "---\nid: T-2\ntitle: Export endpoint\nskills: [BE-001]\n---\n## Target\nPOST /api/export returns a PDF.\n"
MIGRATION_TICKET = "---\nid: T-3\ntitle: Add invoices table\nskills: [BE-002]\n---\n## Scope\nNew migration for invoices.\n"


def _status():
    return {
        "human_gates": {k: {"status": "approved"} for k in ("0", "1", "2")},
        "current_sprint": "SPRINT-01",
        "sprint_hitl": {"scope_status": "approved", "groom_status": "approved", "review_status": None},
        "gate": "5",
        "gate_status": "passed",
    }


def _decide(log, tickets=None):
    tickets = tickets or [{"id": "T-1", "status": "implement", "deps": [], "card": {"id": "T-1"}}]
    return decide_from_state(
        "demo", _status(), tickets, log=log, receipts_ok={t["id"]: True for t in tickets},
        open_los=[], amendment_actions=[], prd_exists=True,
    )


class StubTextTests(unittest.TestCase):
    def test_untouched_template_counts_as_placeholder(self):
        stub = (
            "## Plan\n- (how this ticket will be implemented; library pull if any)\n"
            "## AC coverage\n- [x] export works — tests/export.test.ts\n"
            "## Default flow\n- Route / user path a real user would take (LO-0051):\n"
            "- Screenshot: (path or none — function-only ticket)\n"
            "## Playbook citations\n- playbook: none\n"
            "## Skill QA\n- gate 5 green; AC covered by tests or route check\n"
            "## Design skill\n- n/a (or: matches approved spec tokens/states)\n"
            "## Architecture skill\n- n/a\n"
        )
        issues = receipt_issues(stub)
        for name in ("plan", "default-flow", "skill-qa", "skill-design"):
            self.assertIn(f"placeholder ## {name}", issues)
        self.assertNotIn("placeholder ## skill-arch", issues)

    def test_section_is_stub(self):
        self.assertTrue(section_is_stub("- (files touched and why)\n- follow-ups: (noted here, not done in this ticket)\n"))
        self.assertFalse(section_is_stub("- apps/web/src/export.ts\n- follow-ups: none\n"))


class SectionsBySkillTests(unittest.TestCase):
    def test_ui_ticket_needs_evidence_and_a11y(self):
        need = required_sections(UI_TICKET)
        self.assertIn("Evidence", need)
        self.assertIn("A11y", need)
        self.assertIn("Security", need)
        self.assertIn("Scope", need)
        self.assertNotIn("API proof", need)

    def test_api_ticket_needs_api_proof(self):
        self.assertIn("API proof", required_sections(API_TICKET))

    def test_migration_needs_risk_and_rollback(self):
        self.assertIn("Risk & rollback", required_sections(MIGRATION_TICKET))

    def test_stub_has_only_the_needed_sections(self):
        stub = stub_sections(None, API_TICKET)
        self.assertIn("## API proof", stub)
        self.assertNotIn("## Evidence", stub)


class VerdictTests(unittest.TestCase):
    def test_lines_need_a_verdict_and_proof(self):
        issues = verdict_issues("Evidence", "- export button works\n", need_pass=True)
        self.assertTrue(any("no PASS / FAIL / NOT TESTED" in i for i in issues))
        issues = verdict_issues("Evidence", "- export: PASS\n", need_pass=True)
        self.assertTrue(any("PASS needs proof" in i for i in issues))
        self.assertEqual(
            verdict_issues("Evidence", "- export: PASS — docs/evidence/T-1/rest.png\n", need_pass=True), []
        )

    def test_fail_blocks_and_not_tested_needs_reason(self):
        issues = verdict_issues("Evidence", "- export: FAIL — docs/e.png\n- empty: NOT TESTED\n", need_pass=False)
        self.assertTrue(any("FAIL" in i for i in issues))
        self.assertTrue(any("needs a reason" in i for i in issues))
        self.assertEqual(verdict_issues("Evidence", "- empty: NOT TESTED — no seed data\n", need_pass=False), [])


class TrustIssuesTests(unittest.TestCase):
    def _good_ui_receipt(self) -> str:
        return (
            "## AC coverage\n- [x] export works — apps/web/tests/export.test.ts\n"
            "## Evidence\n- rest: PASS — docs/evidence/T-1/rest.png\n- smoke routes: NOT TESTED — no smoke config yet\n"
            "## A11y\n- tab reaches Export, focus ring visible, axe 0 violations\n"
            "## Security\n- no new input, route or secret\n"
            "## Scope\n- apps/web/src/board/Export.tsx\n- follow-ups: none\n"
        )

    def test_missing_screenshot_and_unchecked_ac(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            receipt = self._good_ui_receipt().replace("[x]", "[ ]")
            issues = trust_issues(receipt, UI_TICKET, root)
            self.assertTrue(any("still `- [ ]`" in i for i in issues))
            self.assertTrue(any("screenshot named on the receipt does not exist" in i for i in issues))

    def test_good_receipt_passes_when_files_exist(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs" / "evidence" / "T-1").mkdir(parents=True)
            (root / "docs" / "evidence" / "T-1" / "rest.png").write_bytes(b"png")
            (root / "apps" / "web" / "tests").mkdir(parents=True)
            (root / "apps" / "web" / "tests" / "export.test.ts").write_text("test")
            self.assertEqual(trust_issues(self._good_ui_receipt(), UI_TICKET, root), [])

    def test_smoke_not_tested_must_be_said(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs" / "evidence" / "T-1").mkdir(parents=True)
            (root / "docs" / "evidence" / "T-1" / "rest.png").write_bytes(b"png")
            (root / "apps" / "web" / "tests").mkdir(parents=True)
            (root / "apps" / "web" / "tests" / "export.test.ts").write_text("test")
            report = {"results": [{"check": "smoke_routes", "passed": True, "not_tested": True}]}
            (root / "docs" / "qa-report-20261012-100000.json").write_text(json.dumps(report))
            silent = self._good_ui_receipt().replace("- smoke routes: NOT TESTED — no smoke config yet\n", "")
            self.assertTrue(any("did not run smoke routes" in i for i in trust_issues(silent, UI_TICKET, root)))
            self.assertEqual(trust_issues(self._good_ui_receipt(), UI_TICKET, root), [])

    def test_scope_needs_follow_ups(self):
        with tempfile.TemporaryDirectory() as tmp:
            receipt = "## Security\n- none new\n## Scope\n- apps/web/src/x.ts edited\n"
            issues = trust_issues(receipt, "---\nskills: [SO-001]\n---\nTooling", Path(tmp))
            self.assertTrue(any("follow-ups" in i for i in issues))

    def test_hq_paths_resolve(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(missing_paths("- playbook: knowledge-base/frontend_playbook.md\n", [Path(tmp)]), ["knowledge-base/frontend_playbook.md"])
            self.assertEqual(trust_issues(
                "## Playbook citations\n- playbook: knowledge-base/frontend_playbook.md\n"
                "## Security\n- none new\n## Scope\n- x\n- follow-ups: none\n",
                "---\nskills: [SO-001]\n---\nTooling", Path(tmp),
            ), [])


class QaVerdictTests(unittest.TestCase):
    def test_state_resets_on_new_gate_pass(self):
        log = {"entries": [
            {"ticket": "T-1", "event": "gate-pass"},
            {"ticket": "T-1", "event": "qa-fail"},
        ]}
        self.assertEqual(qa_state(log, "T-1"), "fail")
        log["entries"].append({"ticket": "T-1", "event": "gate-pass"})
        self.assertEqual(qa_state(log, "T-1"), "none")
        log["entries"].append({"ticket": "T-1", "event": "qa-pass"})
        self.assertEqual(qa_state(log, "T-1"), "pass")

    def test_verdict_file_must_back_the_verdict(self):
        weak = "Verdict: PASS\n## AC\n- export: NOT TESTED — no browser\n## Findings\n- none\n"
        self.assertTrue(any("missing proof is a FAIL" in i for i in verdict_file_issues(weak, "PASS")))
        bare_fail = "Verdict: FAIL\n## AC\n- export: FAIL — button missing\n## Findings\n- none\n"
        self.assertTrue(verdict_file_issues(bare_fail, "FAIL"))
        good_fail = (
            "Verdict: FAIL\n## AC\n- export: FAIL — screenshot shows no button\n## Findings\n"
            "- Issue: no export button\n  Expected: button in toolbar\n  Actual: toolbar empty\n"
            "  Evidence: docs/evidence/T-1/rest.png\n  Fix: render ExportButton\n  Files: Board.tsx\n"
        )
        self.assertEqual(verdict_file_issues(good_fail, "FAIL"), [])
        self.assertTrue(any("says FAIL" in i for i in verdict_file_issues(good_fail, "PASS")))

    def test_qa_fail_goes_back_to_debug(self):
        log = {"entries": [
            {"ticket": "T-1", "event": "implement", "ts": "2026-10-12T10:00:00"},
            {"ticket": "T-1", "event": "gate-pass", "ts": "2026-10-12T10:10:00"},
            {"ticket": "T-1", "event": "qa-fail", "ts": "2026-10-12T10:20:00", "note": "qa fail: x"},
        ]}
        step = _decide(log)
        self.assertEqual(step.kind, "DEBUG")
        self.assertIn("qa/T-1.md", step.read)
        self.assertEqual(count_gate_fails(log, "T-1"), 1)


class EscalationTests(unittest.TestCase):
    def test_same_failure_twice_escalates_early(self):
        log = {"entries": [
            {"ticket": "T-1", "event": "gate-fail", "note": "gate red: eslint"},
            {"ticket": "T-1", "event": "gate-fail", "note": "gate red: eslint"},
        ]}
        self.assertTrue(repeated_failure(log, "T-1"))
        self.assertTrue(should_escalate(log, "T-1"))
        different = {"entries": [
            {"ticket": "T-1", "event": "gate-fail", "note": "gate red: eslint"},
            {"ticket": "T-1", "event": "gate-fail", "note": "gate red: typescript"},
        ]}
        self.assertFalse(should_escalate(different, "T-1"))

    def test_escalation_blocks_instead_of_hitl(self):
        log = {"entries": [
            {"ticket": "T-1", "event": "implement", "ts": "2026-10-12T10:00:00"},
        ] + [{"ticket": "T-1", "event": "gate-fail", "note": f"gate red: c{i}"} for i in range(MAX_GATE_RETRIES)]}
        step = _decide(log)
        self.assertEqual(step.kind, "BLOCK")
        self.assertTrue(step.loop)
        self.assertIn("blocked", step.command)

    def test_only_blocked_left_is_hitl(self):
        tickets = [
            {"id": "T-1", "status": "blocked", "deps": []},
            {"id": "T-2", "status": "done", "deps": []},
        ]
        step = _decide({"entries": []}, tickets)
        self.assertEqual(step.kind, "HITL")
        self.assertIn("escalations/T-1.md", step.read or "")


if __name__ == "__main__":
    unittest.main()
