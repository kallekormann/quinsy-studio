#!/usr/bin/env python3
import unittest

from studio_streams import inferred_stream, ticket_is_ready, needs_architecture_from_blob


class StreamTests(unittest.TestCase):
    def test_legacy_tickets_are_ready(self):
        self.assertEqual(inferred_stream({"title": "Fix lint"}), "ready")
        self.assertTrue(ticket_is_ready({"status": "backlog"}))

    def test_pending_design_is_production(self):
        self.assertEqual(inferred_stream({"design_status": "pending"}), "production")
        self.assertFalse(ticket_is_ready({"design_status": "pending"}))

    def test_arch_from_title(self):
        self.assertTrue(needs_architecture_from_blob("feature", "Persist API schema for jobs"))
        self.assertFalse(needs_architecture_from_blob("ui-styling", "Tighten button padding"))

    def test_cached_stream_does_not_override_pending(self):
        self.assertEqual(
            inferred_stream({"stream": "ready", "design_status": "pending"}),
            "production",
        )
        self.assertEqual(
            inferred_stream({"stream": "production", "design_status": "approved", "architecture_status": "n/a"}),
            "ready",
        )


if __name__ == "__main__":
    unittest.main()
