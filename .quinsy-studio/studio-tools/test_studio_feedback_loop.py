#!/usr/bin/env python3
"""Drain notes to FB, HITL one question, ticket ready items into backlog."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from studio_execute import decide_from_state
from studio_feedback_loop import (
    apply_answer,
    process_feedback_queue,
    split_themes,
)
from studio_human_inbox import append_note, should_queue_as_note
from test_studio_execute import _approved_status


def _patch_roots(root: Path):
    return (
        patch("sprint_hitl.PROJECTS_DIR", root),
        patch("ticket_ids.PROJECTS_DIR", root),
        patch("backlog_paths.PROJECTS_DIR", root),
    )


class SplitAndQueueTests(unittest.TestCase):
    def test_split_two_bullets(self):
        parts = split_themes("- denser type on the list\n- empty state on /commands")
        self.assertEqual(len(parts), 2)

    def test_abort_not_queued_as_ticket_and_two_notes_two_questions(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "projects"
            (root / "demo" / "sprints" / "SPRINT-01").mkdir(parents=True)
            (root / "demo" / "docs").mkdir(parents=True)
            patches = _patch_roots(root)
            for p in patches:
                p.start()
            try:
                append_note("demo", "SPRINT-01", "stop this ticket")
                append_note(
                    "demo",
                    "SPRINT-01",
                    "- we could add a digest email\n- also consider denser type",
                )
                result = process_feedback_queue("demo", "SPRINT-01")
                self.assertEqual(result["action"], "hitl")
                self.assertEqual(len(result["questions"]), 2)
                self.assertTrue(all(item.get("open_questions") for item in result["questions"]))
                from sprint_hitl import load_feedback_queue

                ids = {i["id"] for i in load_feedback_queue("demo", "SPRINT-01")}
                self.assertEqual(len(ids), 2)
                backlog = list((root / "demo" / "backlog").glob("*.md")) if (root / "demo" / "backlog").exists() else []
                self.assertEqual(backlog, [])
            finally:
                for p in patches:
                    p.stop()

    def test_drain_executable_note_writes_backlog_ticket_without_sprint(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "projects"
            (root / "demo" / "sprints" / "SPRINT-01").mkdir(parents=True)
            patches = _patch_roots(root)
            for p in patches:
                p.start()
            try:
                append_note(
                    "demo",
                    "SPRINT-01",
                    "Empty state on /commands when there are no jobs: show a Create job CTA and keep the app sidebar.",
                )
                result = process_feedback_queue("demo", "SPRINT-01")
                self.assertEqual(result["action"], "ticketed")
                self.assertTrue(result["ticketed"])
                tickets = list((root / "demo" / "backlog").glob("DEMO-*.md"))
                self.assertEqual(len(tickets), 1)
                body = tickets[0].read_text(encoding="utf-8")
                self.assertNotIn("sprint:", body)
                self.assertIn("## Source feedback", body)
            finally:
                for p in patches:
                    p.stop()

    def test_design_note_tickets_pending_design(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "projects"
            (root / "demo" / "sprints" / "SPRINT-01").mkdir(parents=True)
            patches = _patch_roots(root)
            for p in patches:
                p.start()
            try:
                append_note(
                    "demo",
                    "SPRINT-01",
                    "Visual hierarchy on /pricing: put the primary Subscribe button where the eye lands first, keep plan cards secondary.",
                )
                result = process_feedback_queue("demo", "SPRINT-01")
                self.assertIn(result["action"], ("ticketed", "hitl"))
                if result["action"] == "hitl":
                    fb_id = result["questions"][0]["id"]
                    apply_answer(
                        "demo",
                        "SPRINT-01",
                        fb_id,
                        "hierarchy — Subscribe is the one action on /pricing",
                    )
                    process_feedback_queue("demo", "SPRINT-01")
                tickets = list((root / "demo" / "backlog").glob("DEMO-*.md"))
                self.assertTrue(tickets)
                body = tickets[0].read_text(encoding="utf-8")
                self.assertIn("design_status: pending", body)
            finally:
                for p in patches:
                    p.stop()

    def test_answer_then_ticket(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "projects"
            (root / "demo" / "sprints" / "SPRINT-01").mkdir(parents=True)
            patches = _patch_roots(root)
            for p in patches:
                p.start()
            try:
                append_note("demo", "SPRINT-01", "we could add a digest email")
                result = process_feedback_queue("demo", "SPRINT-01")
                self.assertEqual(result["action"], "hitl")
                fb_id = result["questions"][0]["id"]
                apply_answer(
                    "demo",
                    "SPRINT-01",
                    fb_id,
                    "Daily digest on /settings/notifications when a job finishes.",
                )
                process_feedback_queue("demo", "SPRINT-01")
                tickets = list((root / "demo" / "backlog").glob("DEMO-*.md"))
                self.assertEqual(len(tickets), 1)
            finally:
                for p in patches:
                    p.stop()

    def test_looks_good_is_not_a_ticket(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "projects"
            (root / "demo" / "sprints" / "SPRINT-01").mkdir(parents=True)
            patches = _patch_roots(root)
            for p in patches:
                p.start()
            try:
                append_note("demo", "SPRINT-01", "tweak later")
                result = process_feedback_queue("demo", "SPRINT-01")
                self.assertEqual(result["action"], "hitl")
                fb_id = result["questions"][0]["id"]
                item = apply_answer("demo", "SPRINT-01", fb_id, "looks good")
                self.assertNotEqual(item.get("status"), "ready")
                self.assertFalse(list((root / "demo" / "backlog").glob("DEMO-*.md")))
            finally:
                for p in patches:
                    p.stop()

    def test_should_not_queue_answers_during_clarify_hitl(self):
        self.assertFalse(
            should_queue_as_note(
                "Daily digest on /settings",
                named_hitl_waiting=True,
                clarify_feedback_waiting=True,
            )
        )
        self.assertTrue(should_queue_as_note("stop this ticket", clarify_feedback_waiting=True))


class DecideFeedbackTests(unittest.TestCase):
    def test_decide_hitl_when_questions_open(self):
        step = decide_from_state(
            "demo",
            _approved_status(),
            [{"id": "DEMO-0001", "status": "backlog", "deps": [], "card": {"id": "DEMO-0001", "ac": ["a"]}}],
            log={"entries": []},
            receipts_ok={},
            amendment_actions=[],
            prd_exists=True,
            open_los=[],
            feedback_queue=[
                {
                    "id": "FB-001",
                    "status": "clarifying",
                    "raw": "digest email",
                    "open_questions": ["Which surface?"],
                }
            ],
        )
        self.assertEqual(step.kind, "HITL")
        self.assertIn("clarify-feedback", step.reason)
        self.assertIn("Do not implement", step.reason)

    def test_decide_inform_drain_when_inbox_and_not_implementing(self):
        step = decide_from_state(
            "demo",
            _approved_status(),
            [{"id": "DEMO-0001", "status": "backlog", "deps": [], "card": {"id": "DEMO-0001", "ac": ["a"]}}],
            log={"entries": []},
            receipts_ok={},
            amendment_actions=[],
            prd_exists=True,
            open_los=[],
            inbox_open=[{"id": "N-001", "text": "we could add a digest email"}],
        )
        self.assertEqual(step.kind, "INFORM")
        self.assertIn("feedback-drain", step.command)

    def test_decide_skips_feedback_while_implementing(self):
        step = decide_from_state(
            "demo",
            _approved_status(gate="4", gate_status="failed"),
            [{"id": "DEMO-0001", "status": "implement", "deps": [], "card": {"id": "DEMO-0001"}}],
            log={"entries": [{"ticket": "DEMO-0001", "event": "implement", "ts": "2026-09-07T10:00:00"}]},
            receipts_ok={"DEMO-0001": False},
            amendment_actions=[],
            prd_exists=True,
            open_los=[],
            inbox_open=[{"id": "N-001", "text": "we could add a digest email"}],
            feedback_queue=[{"id": "FB-001", "status": "raw", "raw": "digest"}],
        )
        self.assertEqual(step.kind, "VERIFY")


if __name__ == "__main__":
    unittest.main()
