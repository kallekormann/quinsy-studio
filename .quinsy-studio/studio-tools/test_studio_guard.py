#!/usr/bin/env python3
"""Guard is studio-core: mid-execute chat ACKs into the inbox on every project."""

from __future__ import annotations

import unittest
from unittest.mock import patch

from studio_context import guard_request


def _review_pending_status(**kwargs):
    base = {
        "human_gates": {
            "0": {"status": "approved"},
            "1": {"status": "approved"},
            "2": {"status": "approved"},
        },
        "current_sprint": "SPRINT-01",
        "active_ticket": None,
        "sprint_hitl": {
            "scope_status": "approved",
            "groom_status": "approved",
            "review_status": "pending",
        },
        "phase": "5",
        "gate": "5",
    }
    base.update(kwargs)
    return base


class GuardInboxAckTests(unittest.TestCase):
    def test_in_flight_acks_even_when_sprint_review_is_pending(self):
        status = _review_pending_status(active_ticket="DEMO-0001")
        with patch(
            "studio_context._ack_inbox",
            return_value=("inbox_ack", "ACK queued N-001"),
        ) as ack:
            verdict, msg = guard_request("demo", "also consider denser type", status)
        self.assertEqual(verdict, "inbox_ack")
        self.assertIn("N-001", msg)
        ack.assert_called_once()

    def test_in_flight_abort_does_not_become_feedback_only(self):
        status = _review_pending_status(active_ticket="DEMO-0001")
        with patch(
            "studio_context._ack_inbox",
            return_value=("abort", "ACK queued N-001 (abort)"),
        ):
            verdict, _msg = guard_request("demo", "stop this ticket", status)
        self.assertEqual(verdict, "abort")

    def test_hitl_reply_is_not_queued_while_in_flight(self):
        status = _review_pending_status(active_ticket="DEMO-0001")
        with patch("studio_context._ack_inbox") as ack:
            verdict, _msg = guard_request("demo", "back on track", status)
        ack.assert_not_called()
        self.assertNotEqual(verdict, "inbox_ack")

    def test_looks_good_mid_sprint_is_not_hitl(self):
        status = {
            "human_gates": {
                "0": {"status": "approved"},
                "1": {"status": "approved"},
                "2": {"status": "approved"},
            },
            "current_sprint": "SPRINT-01",
            "active_ticket": "DEMO-0001",
            "sprint_hitl": {
                "scope_status": "approved",
                "groom_status": "approved",
            },
            "phase": "5",
            "gate": "5",
        }
        with patch("studio_context._ack_inbox") as ack:
            verdict, msg = guard_request("demo", "looks good", status)
        ack.assert_not_called()
        self.assertEqual(verdict, "in_scope")
        self.assertIn("Ticket ACK is not required", msg)

    def test_looks_good_at_sprint_review_is_not_queued(self):
        status = _review_pending_status(active_ticket=None)
        with patch("studio_context.implementation_in_flight", return_value=False):
            verdict, _msg = guard_request("demo", "looks good", status)
        self.assertNotEqual(verdict, "inbox_ack")
        self.assertNotEqual(verdict, "in_scope")

    def test_idle_review_still_feedback_only(self):
        status = _review_pending_status(active_ticket=None)
        with patch("studio_context.implementation_in_flight", return_value=False):
            verdict, _msg = guard_request("demo", "also consider denser type", status)
        self.assertEqual(verdict, "feedback_only")

    def test_architecture_loop_acks_without_active_ticket(self):
        status = {
            "human_gates": {
                "0": {"status": "approved"},
                "1": {"status": "open"},
            },
            "current_sprint": None,
            "active_ticket": None,
            "phase": "1",
        }
        with patch(
            "studio_context._ack_inbox",
            return_value=("inbox_ack", "ACK queued N-001"),
        ):
            verdict, _msg = guard_request("acme-app", "also use postgres", status)
        self.assertEqual(verdict, "inbox_ack")

    def test_studio_meta_does_not_win_while_implementing(self):
        status = _review_pending_status(active_ticket="DEMO-0001")
        with patch(
            "studio_context._ack_inbox",
            return_value=("inbox_ack", "ACK queued N-002"),
        ):
            verdict, _msg = guard_request(
                "demo", "quinsy studio process should queue this", status
            )
        self.assertEqual(verdict, "inbox_ack")

    def test_sibling_project_name_is_cross_project(self):
        status = {
            "human_gates": {
                "0": {"status": "approved"},
                "1": {"status": "approved"},
                "2": {"status": "approved"},
            },
            "current_sprint": None,
            "active_ticket": None,
        }
        with patch("studio_context.implementation_in_flight", return_value=False), patch(
            "studio_isolation.request_names_sibling", return_value="other-app"
        ):
            verdict, msg = guard_request("acme-app", "copy other-app git into this repo", status)
        self.assertEqual(verdict, "cross_project")
        self.assertIn("other-app", msg)

    def test_sibling_beats_inbox_ack_while_in_flight(self):
        status = _review_pending_status(active_ticket="DEMO-0001")
        with patch("studio_context._ack_inbox") as ack, patch(
            "studio_isolation.request_names_sibling", return_value="other-app"
        ):
            verdict, msg = guard_request(
                "acme-app", "copy other-app into this repo", status
            )
        ack.assert_not_called()
        self.assertEqual(verdict, "cross_project")
        self.assertIn("other-app", msg)


if __name__ == "__main__":
    unittest.main()
