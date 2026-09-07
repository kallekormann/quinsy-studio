#!/usr/bin/env python3
"""Immediate harvest: classify, inbox + LO, exact-title dedupe."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import studio_harvest
from studio_harvest import (
    classify_learning,
    harvest_identified_learning,
    harvest_retro_text,
    harvest_reuse_items,
)
from ticket_helpers import render_ticket_markdown


def _patch_harvest_dirs(tmp: Path):
    open_dir = tmp / "open"
    done_dir = tmp / "done"
    blocked = tmp / "blocked"
    learnings = tmp / "learnings"
    open_dir.mkdir()
    done_dir.mkdir()
    blocked.mkdir()
    learnings.mkdir()
    inbox = learnings / "inbox.md"
    return patch.multiple(
        studio_harvest,
        BACKLOG_OPEN=open_dir,
        BACKLOG_DONE=done_dir,
        BACKLOG_BLOCKED=blocked,
        LEARNINGS_DIR=learnings,
        INBOX_PATH=inbox,
    )


class ClassifyTests(unittest.TestCase):
    def test_path_and_keywords(self):
        self.assertEqual(classify_learning("x", path="packages/auth"), "package")
        self.assertEqual(classify_learning("x", path="ui/components/button"), "ui-component")
        self.assertEqual(classify_learning("h-dvh overflow nested scroll"), "layout")
        self.assertEqual(classify_learning("information architecture placement"), "ia")
        self.assertEqual(classify_learning("gate smoke playwright", signal="gate-fail"), "tooling")
        self.assertEqual(classify_learning("CSP and XSS headers", signal="knowledge-gap"), "security")
        self.assertEqual(classify_learning("unclear groom step", signal="process-gap"), "process")


class HarvestWriteTests(unittest.TestCase):
    def test_creates_lo_inbox_and_frontmatter(self):
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            with _patch_harvest_dirs(tmp):
                result = harvest_identified_learning(
                    "Nested board overflow needs h-dvh",
                    source="demo/SPRINT-01",
                    observation="inner scroll clipped",
                )
                self.assertTrue(result["created"])
                self.assertEqual(result["kind"], "layout")
                lo_files = list((tmp / "open").glob("LO-*.md"))
                self.assertEqual(len(lo_files), 1)
                text = lo_files[0].read_text(encoding="utf-8")
                self.assertIn("infusion_kind: layout", text)
                self.assertIn("infusion_path: knowledge-base/design_playbook.md", text)
                inbox = (tmp / "learnings" / "inbox.md").read_text(encoding="utf-8")
                self.assertIn(result["lo_id"], inbox)
                self.assertIn("Nested board overflow", inbox)

    def test_dedupe_exact_title_only(self):
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            with _patch_harvest_dirs(tmp):
                first = harvest_identified_learning(
                    "Reuse harvest: generalize `packages/auth`",
                    source="demo",
                    path="packages/auth",
                )
                second = harvest_identified_learning(
                    "Reuse harvest: generalize `packages/auth`",
                    source="demo",
                    path="packages/auth",
                )
                other = harvest_identified_learning(
                    "Reuse harvest: generalize `packages/billing`",
                    source="demo",
                    path="packages/billing",
                )
                self.assertTrue(first["created"])
                self.assertFalse(second["created"])
                self.assertEqual(second["lo_id"], first["lo_id"])
                self.assertTrue(other["created"])
                self.assertNotEqual(other["lo_id"], first["lo_id"])

    def test_retro_harvests_badly_not_placeholders(self):
        retro = """# Retro
## What went well?
- tests were fast
## What went badly?
- gate smoke used a temp cache
## What can we improve?
- ...
"""
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            with _patch_harvest_dirs(tmp):
                results = harvest_retro_text(retro, "demo")
                self.assertEqual(len(results), 1)
                self.assertTrue(results[0]["created"])
                titles = [p.read_text() for p in (tmp / "open").glob("LO-*.md")]
                self.assertTrue(any("temp cache" in t for t in titles))

    def test_reuse_two_paths_do_not_collide(self):
        items = [
            {"path": "packages/auth", "action": "promote", "covered": False, "ticket_id": "D-1"},
            {"path": "ui/components/dock", "action": "lo_ticket", "covered": False, "ticket_id": "D-2"},
            {"path": "src/local.ts", "action": "local", "covered": False, "ticket_id": "D-3"},
        ]
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            with _patch_harvest_dirs(tmp):
                results = harvest_reuse_items(items, "demo/SPRINT-01")
                self.assertEqual(len(results), 2)
                kinds = {r["kind"] for r in results}
                self.assertEqual(kinds, {"package", "ui-component"})
                self.assertEqual(len(list((tmp / "open").glob("LO-*.md"))), 2)

    def test_render_emits_infusion_fields(self):
        md = render_ticket_markdown(
            {
                "id": "LO-0098",
                "title": "Classify harvest",
                "infusion_kind": "frontend",
                "infusion_path": "knowledge-base/frontend_playbook.md",
                "acceptance_criteria": ["inbox then playbook"],
            }
        )
        self.assertIn("infusion_kind: frontend", md)
        self.assertIn("infusion_path: knowledge-base/frontend_playbook.md", md)


if __name__ == "__main__":
    unittest.main()
