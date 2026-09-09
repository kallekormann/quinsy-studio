#!/usr/bin/env python3
"""Tests for the agentic execute protocol and compact tickets."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from studio_execute import (
    compact_card,
    count_gate_fails,
    decide_from_state,
    extract_ac,
    format_execute_step,
    harvest_retro_learn_prompts,
    has_fresh_gate_pass,
    pick_next_ticket,
    receipt_issues,
    ExecuteStep,
)
from ticket_helpers import render_ticket_markdown


def _approved_status(**kwargs):
    base = {
        "human_gates": {
            "0": {"status": "approved"},
            "1": {"status": "approved"},
            "2": {"status": "approved"},
        },
        "current_sprint": "SPRINT-01",
        "sprint_hitl": {
            "scope_status": "approved",
            "groom_status": "approved",
            "review_status": None,
        },
        "gate": "5",
        "gate_status": "passed",
    }
    base.update(kwargs)
    return base


class ExtractAndCardTests(unittest.TestCase):
    def test_extract_ac_compact_and_skips_filler_bdd(self):
        body = """## AC
- User can export PDF from the board
- **Given:** Current project state
- **When:** The ticket is implemented
- **Then:** Watermark appears on free plan
## Out of scope
- billing
"""
        ac = extract_ac(body)
        self.assertIn("User can export PDF from the board", ac)
        self.assertIn("Watermark appears on free plan", ac)
        self.assertFalse(any("Current project state" in x for x in ac))

    def test_compact_card_lists_skills_and_playbooks_not_a_skills_section(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "DEMO-0001-export.md"
            path.write_text(
                "---\n"
                "id: DEMO-0001\n"
                "title: Export PDF\n"
                "files: [src/export.ts]\n"
                "dependencies: [DEMO-0000]\n"
                "skills: [FE-001, SO-001]\n"
                "---\n\n"
                "## Target\nPDF download on free path\n\n"
                "## AC\n- downloads a file\n- shares type stack with screen\n",
                encoding="utf-8",
            )
            card = compact_card(path)
            self.assertEqual(card["id"], "DEMO-0001")
            self.assertIn("downloads a file", card["ac"])
            self.assertIn("src/export.ts", card["files"])
            self.assertEqual(card["deps"], ["DEMO-0000"])
            self.assertEqual(card["skills"], ["FE-001", "SO-001"])
            self.assertTrue(any("frontend_playbook" in p for p in card["playbooks"]))

    def test_render_ticket_omits_boilerplate_dod_and_filler_bdd(self):
        md = render_ticket_markdown(
            {
                "id": "LO-0099",
                "title": "Compact tickets",
                "acceptance_criteria": ["execute emits a card", "receipt required before done"],
                "scenarios": [
                    {
                        "given": "Current project state",
                        "when": "The ticket is implemented",
                        "then": "should not appear as wrapper",
                    }
                ],
                "definition_of_done": ["QA gate green"],
                "skills": ["SO-001"],
                "soll_zustand": "Agents load a short card first.",
            }
        )
        self.assertIn("## AC", md)
        self.assertIn("execute emits a card", md)
        self.assertNotIn("Current project state", md)
        self.assertNotIn("QA gate green", md)
        self.assertNotIn("## 4. Definition of Done", md)
        self.assertNotIn("## Skills", md)
        self.assertNotIn("Playbook:", md)


class PickAndReceiptTests(unittest.TestCase):
    def test_pick_next_respects_dependencies(self):
        tickets = [
            {"id": "A-0002", "status": "backlog", "deps": ["A-0001"]},
            {"id": "A-0001", "status": "backlog", "deps": []},
            {"id": "A-0003", "status": "done", "deps": []},
        ]
        nxt = pick_next_ticket(tickets)
        self.assertEqual(nxt["id"], "A-0001")
        tickets[1]["status"] = "done"
        nxt = pick_next_ticket(tickets, done_ids={"A-0001", "A-0003"})
        self.assertEqual(nxt["id"], "A-0002")

    def test_pick_next_accepts_cross_sprint_done_ids(self):
        """Deps completed in prior sprints are not in the current sprint ticket list."""
        tickets = [
            {"id": "A-0010", "status": "backlog", "deps": ["A-0009", "A-0008"]},
        ]
        self.assertIsNone(pick_next_ticket(tickets, done_ids=set()))
        nxt = pick_next_ticket(tickets, done_ids={"A-0009", "A-0008"})
        self.assertEqual(nxt["id"], "A-0010")

    def test_pick_next_follows_scope_order(self):
        tickets = [
            {"id": "A-0001", "status": "backlog", "deps": [], "priority": "P0"},
            {"id": "A-0002", "status": "backlog", "deps": [], "priority": "P0"},
        ]
        nxt = pick_next_ticket(tickets, done_ids=set(), scope_order=["A-0002", "A-0001"])
        self.assertEqual(nxt["id"], "A-0002")

    def test_pick_next_prefers_in_progress(self):
        tickets = [
            {"id": "A-0001", "status": "backlog", "deps": []},
            {"id": "A-0002", "status": "implement", "deps": []},
        ]
        self.assertEqual(pick_next_ticket(tickets)["id"], "A-0002")

    def test_receipt_requires_three_sections(self):
        self.assertEqual(receipt_issues(""), ["receipt empty"])
        stub = "# R\n## Plan\n- ...\n## AC coverage\n- ...\n## Default flow\n- ...\n"
        self.assertTrue(receipt_issues(stub))
        good = (
            "# R\n## Plan\n- pull library button\n"
            "## AC coverage\n- board export\n## Default flow\n- /board/:id export\n"
        )
        self.assertEqual(receipt_issues(good), [])

    def test_fresh_gate_pass_after_implement(self):
        log = {
            "entries": [
                {"ts": "2026-09-07T10:00:00", "ticket": "T-1", "event": "implement"},
                {"ts": "2026-09-07T10:05:00", "ticket": "T-1", "event": "gate-pass"},
            ]
        }
        self.assertTrue(has_fresh_gate_pass(log, "T-1"))
        self.assertFalse(has_fresh_gate_pass({"entries": log["entries"][:1]}, "T-1"))
        self.assertEqual(
            count_gate_fails(
                {"entries": [{"ticket": "T-1", "event": "gate-fail"}] * 3},
                "T-1",
            ),
            3,
        )


class DecideTests(unittest.TestCase):
    def test_decide_implement_next_unblocked(self):
        step = decide_from_state(
            "demo",
            _approved_status(),
            [{"id": "DEMO-0001", "status": "backlog", "deps": [], "card": {"id": "DEMO-0001", "ac": ["a"]}}],
            log={"entries": []},
            receipts_ok={},
            amendment_actions=[],
            prd_exists=True,
            open_los=[],
        )
        self.assertEqual(step.kind, "IMPLEMENT")
        self.assertEqual(step.ticket_id, "DEMO-0001")
        self.assertTrue(step.loop)

    def test_decide_hitl_on_sprint_review(self):
        step = decide_from_state(
            "demo",
            _approved_status(
                sprint_hitl={
                    "review_status": "pending",
                    "scope_status": "approved",
                    "groom_status": "approved",
                }
            ),
            [{"id": "DEMO-0001", "status": "done", "deps": []}],
            open_los=[],
            amendment_actions=[],
            prd_exists=True,
        )
        self.assertEqual(step.kind, "HITL")
        self.assertIn("sprint-review", step.reason)
        self.assertFalse(step.loop)

    def test_decide_verify_receipt_then_gate_then_done(self):
        tickets = [{"id": "DEMO-0002", "status": "implement", "deps": [], "card": {"id": "DEMO-0002"}}]
        status = _approved_status(gate="4", gate_status="failed")
        step = decide_from_state(
            "demo",
            status,
            tickets,
            log={"entries": [{"ticket": "DEMO-0002", "event": "implement", "ts": "2026-09-07T10:00:00"}]},
            receipts_ok={"DEMO-0002": False},
            open_los=[],
            amendment_actions=[],
            prd_exists=True,
        )
        self.assertEqual(step.kind, "VERIFY")
        step = decide_from_state(
            "demo",
            status,
            tickets,
            log={"entries": [{"ticket": "DEMO-0002", "event": "implement", "ts": "2026-09-07T10:00:00"}]},
            receipts_ok={"DEMO-0002": True},
            open_los=[],
            amendment_actions=[],
            prd_exists=True,
        )
        self.assertIn(step.kind, ("GATE", "DEBUG"))
        step = decide_from_state(
            "demo",
            _approved_status(),
            tickets,
            log={
                "entries": [
                    {"ticket": "DEMO-0002", "event": "implement", "ts": "2026-09-07T10:00:00"},
                    {"ticket": "DEMO-0002", "event": "gate-pass", "ts": "2026-09-07T10:10:00"},
                ]
            },
            receipts_ok={"DEMO-0002": True},
            open_los=[],
            amendment_actions=[],
            prd_exists=True,
        )
        self.assertEqual(step.kind, "MOVE_DONE")

    def test_decide_studio_lo_after_closed_sprint_retro(self):
        with patch("sprint_reuse_review.reuse_gate_message", return_value=None):
            step = decide_from_state(
                "demo",
                _approved_status(
                    sprint_hitl={
                        "scope_status": "approved",
                        "groom_status": "approved",
                        "review_status": "approved",
                        "retro_status": "done",
                    }
                ),
                [{"id": "DEMO-0001", "status": "done", "deps": []}],
                open_los=[
                    {
                        "id": "LO-0053",
                        "title": "execute loop",
                        "path": "backlog/open/LO-0053.md",
                        "priority": "P1",
                    }
                ],
                amendment_actions=[],
                prd_exists=True,
            )
        self.assertEqual(step.kind, "STUDIO_LO")
        self.assertEqual(step.ticket_id, "LO-0053")

    def test_decide_implement_with_open_lo_trains_in_parallel(self):
        step = decide_from_state(
            "demo",
            _approved_status(),
            [{"id": "DEMO-0001", "status": "backlog", "deps": [], "card": {"id": "DEMO-0001"}}],
            open_los=[
                {
                    "id": "LO-0055",
                    "title": "Nested board overflow needs h-dvh on chrome shells",
                    "path": "backlog/open/LO-0055.md",
                    "priority": "P1",
                    "infusion_kind": "layout",
                    "infusion_path": "knowledge-base/design_playbook.md",
                    "train_skills": "[UX-003, FE-002]",
                }
            ],
            amendment_actions=[],
            prd_exists=True,
        )
        self.assertEqual(step.kind, "IMPLEMENT")
        self.assertEqual(step.ticket_id, "DEMO-0001")
        self.assertTrue(step.parallel_train)
        self.assertIn("LO-0055", step.parallel_train[0]["lo"])
        self.assertEqual(step.parallel_train[0]["skill_id"], "UX-003")

    def test_decide_in_progress_beats_open_lo(self):
        step = decide_from_state(
            "demo",
            _approved_status(),
            [{"id": "DEMO-0002", "status": "implement", "deps": [], "card": {"id": "DEMO-0002"}}],
            log={"entries": [{"ticket": "DEMO-0002", "event": "implement", "ts": "2026-09-07T10:00:00"}]},
            receipts_ok={"DEMO-0002": False},
            open_los=[{"id": "LO-0055", "title": "x", "path": "backlog/open/LO-0055.md"}],
            amendment_actions=[],
            prd_exists=True,
        )
        self.assertEqual(step.kind, "VERIFY")
        self.assertEqual(step.ticket_id, "DEMO-0002")

    def test_decide_sprint_review_beats_open_lo(self):
        step = decide_from_state(
            "demo",
            _approved_status(
                sprint_hitl={
                    "review_status": "pending",
                    "scope_status": "approved",
                    "groom_status": "approved",
                }
            ),
            [{"id": "DEMO-0001", "status": "done", "deps": []}],
            open_los=[{"id": "LO-0055", "title": "x", "path": "backlog/open/LO-0055.md"}],
            amendment_actions=[],
            prd_exists=True,
        )
        self.assertEqual(step.kind, "HITL")
        self.assertIn("sprint-review", step.reason)

    def test_decide_studio_lo_when_project_ticket_blocked_on_deps(self):
        step = decide_from_state(
            "demo",
            _approved_status(),
            [{"id": "DEMO-0002", "status": "backlog", "deps": ["DEMO-0001"]}],
            open_los=[{"id": "LO-0055", "title": "x", "path": "backlog/open/LO-0055.md"}],
            amendment_actions=[],
            prd_exists=True,
        )
        self.assertEqual(step.kind, "STUDIO_LO")


    def test_decide_gate1_is_hitl_after_prd(self):
        step = decide_from_state(
            "demo",
            {
                "human_gates": {"0": {"status": "approved"}, "1": {"status": "pending"}},
                "current_sprint": "SPRINT-01",
                "sprint_hitl": {"scope_status": "approved", "groom_status": "approved"},
            },
            [{"id": "DEMO-0001", "status": "backlog", "deps": [], "ticket_type": "feature"}],
            open_los=[],
            amendment_actions=[],
            prd_exists=True,
        )
        self.assertEqual(step.kind, "HITL")
        self.assertIn("gate-1", step.reason)
        self.assertFalse(step.loop)

    def test_decide_gate1_produce_blueprint_when_not_ready(self):
        step = decide_from_state(
            "demo",
            {
                "human_gates": {"0": {"status": "approved"}, "1": {"status": "pending"}},
            },
            [],
            open_los=[],
            amendment_actions=[],
            prd_exists=True,
            gate1_ready=False,
        )
        self.assertEqual(step.kind, "IMPLEMENT")
        self.assertIn("blueprint", step.command)

    def test_decide_gate2_is_hitl_after_architecture(self):
        step = decide_from_state(
            "demo",
            {
                "human_gates": {
                    "0": {"status": "approved"},
                    "1": {"status": "approved"},
                    "2": {"status": "pending"},
                },
                "current_sprint": "SPRINT-01",
                "sprint_hitl": {"scope_status": "approved", "groom_status": "approved"},
                "gate": "5",
                "gate_status": "passed",
            },
            [{"id": "DEMO-0001", "status": "backlog", "deps": [], "ticket_type": "feature", "title": "API rate limit"}],
            open_los=[],
            amendment_actions=[],
            prd_exists=True,
        )
        self.assertEqual(step.kind, "HITL")
        self.assertIn("gate-2", step.reason)
        self.assertFalse(step.loop)

    def test_decide_gate2_produce_design_when_not_ready(self):
        step = decide_from_state(
            "demo",
            {
                "human_gates": {
                    "0": {"status": "approved"},
                    "1": {"status": "approved"},
                    "2": {"status": "pending"},
                },
            },
            [],
            open_los=[],
            amendment_actions=[],
            prd_exists=True,
            gate2_ready=False,
        )
        self.assertEqual(step.kind, "IMPLEMENT")
        self.assertIn("design", step.command)

    def test_decide_design_track_still_hitl(self):
        step = decide_from_state(
            "demo",
            _approved_status(),
            [{"id": "DEMO-0001", "status": "backlog", "deps": [], "ticket_type": "ui-composition"}],
            design_block="Design approval required before implement",
            open_los=[],
            amendment_actions=[],
            prd_exists=True,
        )
        self.assertEqual(step.kind, "HITL")
        self.assertIn("design-approve", step.reason)

    def test_decide_backend_sprint_skips_review_hitl(self):
        step = decide_from_state(
            "demo",
            _approved_status(
                sprint_hitl={
                    "review_status": "pending",
                    "scope_status": "approved",
                    "groom_status": "approved",
                }
            ),
            [{"id": "DEMO-0001", "status": "done", "deps": [], "ticket_type": "feature", "title": "API webhook"}],
            open_los=[],
            amendment_actions=[],
            prd_exists=True,
        )
        self.assertNotEqual(step.kind, "HITL")
        self.assertIn(step.kind, ("VERIFY", "STUDIO_LO"))

    def test_decide_inbox_does_not_preempt_in_progress(self):
        step = decide_from_state(
            "demo",
            _approved_status(),
            [{"id": "DEMO-0002", "status": "implement", "deps": [], "card": {"id": "DEMO-0002"}}],
            log={"entries": [{"ticket": "DEMO-0002", "event": "implement", "ts": "2026-09-07T10:00:00"}]},
            receipts_ok={"DEMO-0002": False},
            inbox_open=[{"id": "N-001", "text": "also consider a darker hero", "abort": False, "status": "open"}],
            open_los=[],
            amendment_actions=[],
            prd_exists=True,
        )
        self.assertEqual(step.kind, "VERIFY")
        self.assertEqual(step.ticket_id, "DEMO-0002")

    def test_format_execute_step_prints_mid_chat_when_looping(self):
        step = ExecuteStep(
            kind="IMPLEMENT",
            ticket_id="DEMO-0002",
            reason="next unblocked sprint ticket",
            command="./studio move demo DEMO-0002 implement",
            loop=True,
        )
        text = format_execute_step("demo", step)
        self.assertIn("ISOLATE:", text)
        self.assertIn("MID-CHAT:", text)
        self.assertIn("./studio guard demo", text)
        hitl = ExecuteStep(kind="HITL", reason="gate-1", command="./studio approve demo --gate 1", loop=False)
        self.assertNotIn("MID-CHAT:", format_execute_step("demo", hitl))

    def test_decide_abort_preempts(self):
        step = decide_from_state(
            "demo",
            _approved_status(),
            [{"id": "DEMO-0002", "status": "implement", "deps": [], "card": {"id": "DEMO-0002"}}],
            log={"entries": [{"ticket": "DEMO-0002", "event": "implement", "ts": "2026-09-07T10:00:00"}]},
            receipts_ok={"DEMO-0002": False},
            inbox_open=[{"id": "N-001", "text": "stop this ticket", "abort": True, "status": "open"}],
            open_los=[],
            amendment_actions=[],
            prd_exists=True,
        )
        self.assertEqual(step.kind, "HITL")
        self.assertIn("abort", step.reason.lower())

    def test_decide_reuse_is_not_hitl_after_closed_sprint(self):
        step = decide_from_state(
            "demo",
            _approved_status(
                sprint_hitl={
                    "scope_status": "approved",
                    "groom_status": "approved",
                    "review_status": "approved",
                    "retro_status": None,
                    "reuse_status": "pending",
                }
            ),
            [{"id": "DEMO-0001", "status": "done", "deps": []}],
            open_los=[],
            amendment_actions=[],
            prd_exists=True,
        )
        self.assertEqual(step.kind, "VERIFY")
        self.assertIn("retro", step.reason)
        self.assertNotIn("HITL", step.kind)
    def test_harvest_retro_prompts(self):
        retro = """# Retro
## What went well?
- tests were fast
## What went badly?
- gate smoke used a temp cache
## What can we improve?
- ...
"""
        prompts = harvest_retro_learn_prompts(retro, "demo")
        self.assertTrue(any("temp cache" in p for p in prompts))
        self.assertTrue(all("--source demo" in p for p in prompts))


if __name__ == "__main__":
    unittest.main()
