#!/usr/bin/env python3
"""status.json stays small; snapshots peel to a sidecar."""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from studio_status import (
    GATE_HISTORY_KEEP,
    load_snapshots,
    load_status,
    peel_heavy_status_fields,
    save_snapshots,
    save_status,
    snapshot_for_ticket,
)


class PeelTests(unittest.TestCase):
    def test_peel_moves_snapshots_and_caps_history(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            project = "demo"
            proj = root / "projects" / project
            proj.mkdir(parents=True)
            status = {
                "name": project,
                "gate_history": [{"gate": i, "status": "green"} for i in range(80)],
                "ticket_file_snapshots": {"T-1": {"ui/a.ts": "abc"}},
            }
            (proj / "status.json").write_text(json.dumps(status), encoding="utf-8")
            with patch("studio_status.PROJECTS_DIR", root / "projects"):
                loaded = load_status(project)
                self.assertNotIn("ticket_file_snapshots", loaded)
                self.assertEqual(len(loaded["gate_history"]), GATE_HISTORY_KEEP)
                self.assertEqual(load_snapshots(project)["T-1"]["ui/a.ts"], "abc")
                disk = json.loads((proj / "status.json").read_text(encoding="utf-8"))
                self.assertNotIn("ticket_file_snapshots", disk)
                self.assertLess(len(json.dumps(disk)), 4000)

    def test_save_status_does_not_embed_snapshots(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            project = "demo"
            (root / "projects" / project).mkdir(parents=True)
            with patch("studio_status.PROJECTS_DIR", root / "projects"):
                save_snapshots(project, {"T-9": {"x": "1"}})
                save_status(project, {"name": project, "ticket_file_snapshots": {"T-9": {"x": "2"}}})
                disk = json.loads((root / "projects" / project / "status.json").read_text(encoding="utf-8"))
                self.assertNotIn("ticket_file_snapshots", disk)
                self.assertEqual(snapshot_for_ticket(project, "T-9")["x"], "2")


if __name__ == "__main__":
    unittest.main()
