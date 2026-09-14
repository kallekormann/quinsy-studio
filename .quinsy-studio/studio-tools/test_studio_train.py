#!/usr/bin/env python3
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import studio_train as st


class TrainQueueTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.queue = Path(self.tmp.name) / "train-queue.json"
        self.done = Path(self.tmp.name) / "done"
        self.open_dir = Path(self.tmp.name) / "open"
        self.done.mkdir()
        self.open_dir.mkdir()
        self.patchers = [
            patch.object(st, "QUEUE_PATH", self.queue),
            patch.object(st, "BACKLOG_DONE", self.done),
            patch.object(st, "BACKLOG_OPEN", self.open_dir),
            patch.object(st, "train_open_max", lambda: 2),
            patch(
                "studio_portability.portability_verdict",
                lambda topic: {"portable": True, "title": topic, "reason": ""},
            ),
        ]
        for p in self.patchers:
            p.start()

    def tearDown(self):
        for p in self.patchers:
            p.stop()
        self.tmp.cleanup()

    def test_enqueue_and_close(self):
        job = st.enqueue_train("FE-001", "Kit-first composition before custom markup")
        self.assertEqual(job["status"], "open")
        closed = st.close_job(job["id"])
        self.assertEqual(closed["status"], "done")
        self.assertEqual(st.open_jobs(), [])

    def test_close_for_lo(self):
        st.enqueue_train("UX-005", "Portable principle about mocks", observation="LO-0999")
        closed = st.close_jobs_for_lo("LO-0999")
        self.assertEqual(len(closed), 1)

    def test_cap(self):
        st.enqueue_train("FE-001", "Principle alpha about kit pull")
        st.enqueue_train("FE-002", "Principle beta about token reuse")
        with self.assertRaises(ValueError) as ctx:
            st.enqueue_train("FE-003", "Principle gamma about performance")
        self.assertIn("train queue full", str(ctx.exception))

    def test_lo_source_requires_observation(self):
        with self.assertRaises(ValueError) as ctx:
            st.enqueue_train("FE-001", "Kit-first composition before custom markup", source="lo")
        self.assertIn("observation", str(ctx.exception).lower())

    def test_duplicate_done_not_reopened(self):
        job = st.enqueue_train("FE-001", "Kit-first composition before custom markup", observation="LO-0998")
        st.close_job(job["id"])
        again = st.enqueue_train("FE-001", "Kit-first composition before custom markup", observation="LO-0998")
        self.assertEqual(again["id"], job["id"])
        self.assertEqual(again["status"], "done")

    def test_sync_done_los(self):
        st.enqueue_train("BE-001", "Portable API error envelope", observation="LO-0888")
        (self.done / "LO-0888-api-errors.md").write_text("---\nid: LO-0888\n---\n", encoding="utf-8")
        synced = st.sync_train_with_done_los()
        self.assertTrue(synced)
        self.assertEqual(st.open_jobs(), [])

    def test_backfill_closes_portability_rewrite_duplicate(self):
        original = st.enqueue_train(
            "BE-001",
            "Guard still queued HITL approved as inbox notes (N-008)",
            observation="LO-0129",
        )
        st.close_job(original["id"])
        data = st.load_queue()
        data["jobs"].append(
            {
                "id": "TR-9999",
                "skill_id": "BE-001",
                "topic": "Guard still queued HITL approved as inbox notes even though review is not queued",
                "source": "mistake",
                "observation": "",
                "status": "open",
                "created": "2026-09-08T11:24:41",
            }
        )
        st.save_queue(data)
        changed = st.backfill_observations()
        self.assertIn("TR-9999", changed)
        leftover = [j for j in st.load_queue()["jobs"] if j["id"] == "TR-9999"][0]
        self.assertEqual(leftover["status"], "done")
        self.assertEqual(leftover["observation"], "LO-0129")

    def test_sidecar_command_includes_lo(self):
        st.enqueue_train("FE-001", "Kit-first composition before custom markup", observation="LO-0444")
        cmds = st.sidecar_commands(1)
        self.assertIn("--lo LO-0444", cmds[0]["command"])
        self.assertIn("--from lo", cmds[0]["command"])

    def test_purge_empty_observations(self):
        st.enqueue_train("FE-001", "Kit-first composition before custom markup", observation="LO-0444")
        data = st.load_queue()
        data["jobs"].append(
            {
                "id": "TR-8888",
                "skill_id": "BE-001",
                "topic": "Recreate queue workers after compose env changes portable",
                "source": "mistake",
                "observation": "",
                "status": "open",
                "created": "2026-09-08T12:00:00",
            }
        )
        st.save_queue(data)
        closed = st.purge_empty_observations()
        self.assertIn("TR-8888", closed)
        leftover = [j for j in st.load_queue()["jobs"] if j["id"] == "TR-8888"][0]
        self.assertEqual(leftover["status"], "done")
        self.assertEqual(leftover["closed_reason"], "empty-observation-invalid")
        self.assertTrue(st.open_jobs())
