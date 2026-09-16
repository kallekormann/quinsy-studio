#!/usr/bin/env python3
"""Portability gate unit tests."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import studio_portability
from studio_portability import (
    looks_like_principle,
    portability_verdict,
    rewrite_title_for_portability,
    train_skills_for_kind,
)


class PortabilityTests(unittest.TestCase):
    def test_rewrite_strips_openverse_brand(self):
        out = rewrite_title_for_portability(
            "Suggested still empty — Openverse returned 502 and mapper rejected by"
        )
        self.assertNotIn("openverse", out.lower())
        self.assertIn("stock-media", out.lower())

    def test_moody_incident_not_portable(self):
        v = portability_verdict(
            "Moody Suggested tab empty for Caziro board",
            observation="board xyz",
        )
        self.assertFalse(v["portable"])

    def test_generic_adapter_principle_portable(self):
        v = portability_verdict(
            "Provider licence adapters must map API short codes, not only display forms"
        )
        self.assertTrue(v["portable"], v.get("reason"))

    def test_principle_cues(self):
        self.assertTrue(looks_like_principle("Nested board overflow needs h-dvh on chrome"))
        self.assertTrue(looks_like_principle("Reuse harvest: generalize packages/auth patterns"))

    def test_product_ticket_and_vendor_incidents_are_not_principles(self):
        self.assertFalse(
            looks_like_principle(
                "Do not put AFFI-0007-0010 in a sprint until Awin has approved a live corpus"
            )
        )
        self.assertFalse(
            looks_like_principle(
                "SPRINT-03 originally still had Awin ingest and agent-loop tickets"
            )
        )
        v = portability_verdict(
            "Do not put AFFI-0007-0010 in a sprint until Awin has approved a live corpus"
        )
        self.assertFalse(v["portable"])

    def test_host_and_chrome_incidents_are_not_principles(self):
        self.assertFalse(
            looks_like_principle(
                "Live Inbox list stayed on Loading feedback inbox after host-scope landed"
            )
        )
        v = portability_verdict(
            "canonicalHost trusted the raw Host header while Chrome used the forwarded public host",
            observation="layout disagreed on im-sucher.com",
        )
        self.assertFalse(v["portable"])
        v2 = portability_verdict(
            "Diagnose delivery loadPublishedPage for the published Ratgeber before the next demo"
        )
        self.assertFalse(v2["portable"])

    def test_sanitize_strips_hosts(self):
        from studio_portability import sanitize_observation

        out = sanitize_observation("stuck on im-sucher.com after AFFI-0276")
        self.assertNotIn("im-sucher.com", out.lower())
        self.assertIn("<host>", out)

    def test_long_incident_sentence_is_not_a_principle(self):
        self.assertFalse(
            looks_like_principle(
                "Sprint review and retro lagged behind the two shipped tickets, so M0b planning could not start"
            )
        )

    def test_train_skills_empty_for_process(self):
        self.assertEqual(train_skills_for_kind("process", ["SO-002"]), [])
        self.assertIn("BE-001", train_skills_for_kind("backend", ["BE-001", "BE-004"]))


class HarvestPortabilityTests(unittest.TestCase):
    def test_drops_product_specific_to_local_log(self):
        import studio_harvest
        from studio_harvest import harvest_identified_learning

        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            open_dir = tmp / "open"
            done_dir = tmp / "done"
            blocked = tmp / "blocked"
            learnings = tmp / "learnings"
            projects = tmp / "projects" / "moody" / "docs"
            for d in (open_dir, done_dir, blocked, learnings, projects):
                d.mkdir(parents=True)
            with patch.multiple(
                studio_harvest,
                BACKLOG_OPEN=open_dir,
                BACKLOG_DONE=done_dir,
                BACKLOG_BLOCKED=blocked,
                LEARNINGS_DIR=learnings,
                INBOX_PATH=learnings / "inbox.md",
            ), patch.object(studio_portability, "PROJECTS_DIR", tmp / "projects"), patch.object(
                studio_portability, "list_project_names", lambda: ["moody"]
            ):
                result = harvest_identified_learning(
                    "Moody Mood Direction Suggested empty for Caziro",
                    source="moody/SPRINT-120",
                    observation="pixelated lead on review screenshot",
                )
                self.assertTrue(result.get("dropped"))
                self.assertFalse(result.get("created"))
                self.assertEqual(len(list(open_dir.glob("LO-*.md"))), 0)
                local = tmp / "projects" / "moody" / "docs" / "studio-learnings-local.md"
                self.assertTrue(local.exists())


if __name__ == "__main__":
    unittest.main()
