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

    def test_product_incident_not_portable(self):
        with patch.object(studio_portability, "list_project_names", lambda: ["acme-app"]):
            v = portability_verdict(
                "acme-app Suggested tab empty for one board",
                observation="board xyz",
            )
        self.assertFalse(v["portable"])

    def test_product_surface_names_come_from_the_product_repo(self):
        with tempfile.TemporaryDirectory() as raw:
            projects = Path(raw)
            docs = projects / "acme-app" / "docs"
            docs.mkdir(parents=True)
            (docs / "portability-nouns.txt").write_text("# surfaces\nlaunchpad\n", encoding="utf-8")
            with patch.object(studio_portability, "PROJECTS_DIR", projects), patch.object(
                studio_portability, "list_project_names", lambda: ["acme-app"]
            ):
                v = portability_verdict(
                    "Diagnose delivery for the published Launchpad before the next demo must not wait"
                )
                out = studio_portability.sanitize_observation("Launchpad broke in acme-app")
        self.assertFalse(v["portable"])
        self.assertNotIn("launchpad", out.lower())
        self.assertNotIn("acme-app", out.lower())

    def test_names_glued_to_hyphens_are_found(self):
        find = studio_portability.find_product_nouns_in_hq_text
        for text in (".acme-spark { }", "bg-[var(--acme)]", "data-acme-style"):
            self.assertEqual([hit[1] for hit in find(text, nouns=("acme",), prefixes=())], ["acme"], text)
        self.assertEqual(find("acmeware and macme", nouns=("acme",), prefixes=()), [])

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
                "Do not put ACME-0007-0010 in a sprint until the vendor has approved a live corpus"
            )
        )
        self.assertFalse(
            looks_like_principle(
                "SPRINT-03 originally still had vendor ingest and agent-loop tickets"
            )
        )
        v = portability_verdict(
            "Do not put ACME-0007-0010 in a sprint until the vendor has approved a live corpus"
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
            observation="layout disagreed on shop.example.com",
        )
        self.assertFalse(v["portable"])

    def test_sanitize_strips_hosts(self):
        from studio_portability import sanitize_observation

        out = sanitize_observation("stuck on shop.example.com after ACME-0276")
        self.assertNotIn("shop.example.com", out.lower())
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
            projects = tmp / "projects" / "acme-app" / "docs"
            for d in (open_dir, done_dir, blocked, projects):
                d.mkdir(parents=True)
            with patch.multiple(
                studio_harvest,
                BACKLOG_OPEN=open_dir,
                BACKLOG_DONE=done_dir,
                BACKLOG_BLOCKED=blocked,
            ), patch.object(studio_portability, "PROJECTS_DIR", tmp / "projects"), patch.object(
                studio_portability, "list_project_names", lambda: ["acme-app"]
            ):
                result = harvest_identified_learning(
                    "acme-app Suggested panel empty for one board",
                    source="acme-app/SPRINT-120",
                    observation="pixelated lead on review screenshot",
                )
                self.assertTrue(result.get("dropped"))
                self.assertFalse(result.get("created"))
                self.assertEqual(len(list(open_dir.glob("LO-*.md"))), 0)
                local = tmp / "projects" / "acme-app" / "docs" / "studio-learnings-local.md"
                self.assertTrue(local.exists())


if __name__ == "__main__":
    unittest.main()
