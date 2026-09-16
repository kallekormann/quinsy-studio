#!/usr/bin/env python3
"""Durable learnings store + inbox compact."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from studio_learnings_store import (
    INBOX_HEADER,
    commit_principle,
    compact_inbox,
    search_learnings,
    topic_relpath,
)


class TopicPathTests(unittest.TestCase):
    def test_layout_and_package(self):
        self.assertEqual(
            topic_relpath("layout", "Nested board overflow needs h-dvh"),
            "knowledge-base/learnings/design/layout.md",
        )
        self.assertEqual(
            topic_relpath("package", "Reuse harvest: generalize packages/auth", ""),
            "knowledge-base/learnings/library/packages.md",
        )
        self.assertIn("queues", topic_relpath("backend", "Worker queue topology must match Compose"))


class StoreWriteTests(unittest.TestCase):
    def test_commit_and_compact(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "learnings"
            rel = commit_principle(
                kind="backend",
                lo_id="LO-0400",
                title="Worker queues must match Compose topology",
                observation="leftover QUEUE_CONNECTION pin",
                root=root,
            )
            self.assertTrue((root / "backend" / "queues.md").exists())
            text = (root / "backend" / "queues.md").read_text(encoding="utf-8")
            self.assertIn("LO-0400", text)
            self.assertTrue((root / "index.md").exists())
            inbox = root / "inbox.md"
            inbox.write_text(
                INBOX_HEADER
                + "## LO-0400 — Worker queues must match Compose topology\n"
                "- **When:** 2026-09-16T12:00:00\n"
                "- **Status:** inbox — generalize\n\n"
                "## LO-0001 — old infused\n"
                "- **When:** 2026-09-01T12:00:00\n"
                "- **Status:** infused — SPRINT-01\n\n",
                encoding="utf-8",
            )
            open_dir = Path(raw) / "open"
            open_dir.mkdir()
            (open_dir / "LO-0400-queues.md").write_text("x", encoding="utf-8")
            result = compact_inbox(
                open_dir=open_dir,
                inbox_path=inbox,
                archive_dir=root / "archive",
            )
            self.assertEqual(result["kept"], 1)
            self.assertEqual(result["archived"], 1)
            kept = inbox.read_text(encoding="utf-8")
            self.assertIn("LO-0400", kept)
            self.assertNotIn("LO-0001", kept)
            self.assertTrue((root / "archive" / "inbox-2026-09.md").exists())
            _ = rel
            _ = search_learnings


if __name__ == "__main__":
    unittest.main()
