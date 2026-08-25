#!/usr/bin/env python3
"""Tests for sprint reuse review."""

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

TOOLS = Path(__file__).parent
sys.path.insert(0, str(TOOLS))

from sprint_reuse_review import (  # noqa: E402
    REUSE_APPROVED,
    _path_covered,
    classify_reuse_path,
    find_sprint_needing_reuse,
    record_reuse_decision,
)


class TestClassifyReusePath(unittest.TestCase):
    def test_ui_component_is_lo_ticket(self):
        result = classify_reuse_path("ui/components/user-menu/UserMenu.tsx")
        self.assertEqual(result["action"], "lo_ticket")

    def test_package_is_promote(self):
        result = classify_reuse_path("packages/auth/next/env.ts")
        self.assertEqual(result["action"], "promote")


class TestPathCovered(unittest.TestCase):
    def test_promoted_prefix(self):
        self.assertTrue(_path_covered("packages/auth/foo.ts", {"packages/auth"}, []))

    def test_decision_prefix(self):
        decisions = [{"path": "ui/components/user-menu", "action": "local"}]
        self.assertTrue(
            _path_covered("ui/components/user-menu/UserMenu.tsx", set(), decisions)
        )


class TestFindSprintNeedingReuse(unittest.TestCase):
    def test_finds_sprint_with_summary_but_no_reuse_approval(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project = "demo"
            sprint = "SPRINT-01"
            sprint_dir = root / "projects" / project / "sprints" / sprint
            sprint_dir.mkdir(parents=True)
            (sprint_dir / "summary.md").write_text("# summary", encoding="utf-8")
            (sprint_dir / "reuse-review.json").write_text(
                json.dumps({"status": "pending", "decisions": []}),
                encoding="utf-8",
            )

            with patch("sprint_reuse_review.project_dir", return_value=root / "projects" / project), patch(
                "sprint_hitl.project_dir", return_value=root / "projects" / project
            ):
                found = find_sprint_needing_reuse(project)
            self.assertEqual(found, sprint)

    def test_skips_when_reuse_approved(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project = "demo"
            sprint = "SPRINT-01"
            sprint_dir = root / "projects" / project / "sprints" / sprint
            sprint_dir.mkdir(parents=True)
            (sprint_dir / "summary.md").write_text("# summary", encoding="utf-8")
            (sprint_dir / "reuse-review.json").write_text(
                json.dumps({"status": REUSE_APPROVED, "decisions": []}),
                encoding="utf-8",
            )

            with patch("sprint_reuse_review.project_dir", return_value=root / "projects" / project), patch(
                "sprint_hitl.project_dir", return_value=root / "projects" / project
            ):
                found = find_sprint_needing_reuse(project)
            self.assertIsNone(found)

    def test_grandfathers_sprint_without_reuse_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project = "demo"
            sprint = "SPRINT-01"
            sprint_dir = root / "projects" / project / "sprints" / sprint
            sprint_dir.mkdir(parents=True)
            (sprint_dir / "summary.md").write_text("# summary", encoding="utf-8")

            with patch("sprint_reuse_review.project_dir", return_value=root / "projects" / project), patch(
                "sprint_hitl.project_dir", return_value=root / "projects" / project
            ):
                found = find_sprint_needing_reuse(project)
            self.assertIsNone(found)


class TestRecordDecision(unittest.TestCase):
    def test_record_writes_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project = "demo"
            sprint = "SPRINT-01"
            sprint_dir = root / "projects" / project / "sprints" / sprint
            sprint_dir.mkdir(parents=True)

            with patch("sprint_reuse_review.project_dir", return_value=root / "projects" / project), patch(
                "sprint_hitl.project_dir", return_value=root / "projects" / project
            ), patch("sprint_reuse_review.sprint_directory", return_value=sprint_dir):
                record_reuse_decision(project, sprint, "packages/auth", "promote", ref="TICKET-0001")
                data = json.loads((sprint_dir / "reuse-review.json").read_text(encoding="utf-8"))

            self.assertEqual(len(data["decisions"]), 1)
            self.assertEqual(data["decisions"][0]["path"], "packages/auth")


if __name__ == "__main__":
    unittest.main()
