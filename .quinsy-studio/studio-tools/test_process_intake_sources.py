#!/usr/bin/env python3
"""Intake keeps every handed-in file and writes an index PRD."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import process_intake as intake


class IntakeSourceTests(unittest.TestCase):
    def test_folder_keeps_text_and_other_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            projects = root / "projects"
            projects.mkdir()
            folder = root / "brief"
            folder.mkdir()
            (folder / "vision.md").write_text(
                "# A long vision\n\n" + ("detail " * 80) + "\n\n## A custom chapter\n\nKeep this heading.\n",
                encoding="utf-8",
            )
            nested = folder / "legal"
            nested.mkdir()
            (nested / "terms.txt").write_text("The terms stay in full.\n", encoding="utf-8")
            (folder / "sketch.pdf").write_bytes(b"%PDF-1.4 fake")
            with patch.object(intake, "PROJECTS_DIR", projects):
                code = intake.run_intake("demo", [folder])
            prd = (projects / "demo" / "docs" / "intake" / "prd.md").read_text(encoding="utf-8")
            sources = projects / "demo" / "docs" / "intake" / "sources"
            self.assertEqual(code, 0)
            self.assertIn("Keep this heading.", prd)
            self.assertIn("The terms stay in full.", prd)
            self.assertIn("sketch.pdf", prd)
            self.assertIn("docs/intake/sources/sketch.pdf", prd)
            self.assertTrue((sources / "vision.md").exists())
            self.assertTrue((sources / "legal__terms.txt").exists())
            self.assertTrue((sources / "sketch.pdf").read_bytes().startswith(b"%PDF"))
            self.assertIn("as many milestones", prd.lower())

    def test_several_files_are_all_indexed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            projects = root / "projects"
            projects.mkdir()
            one = root / "one.md"
            two = root / "two.md"
            one.write_text("First document body.\n", encoding="utf-8")
            two.write_text("Second document body.\n", encoding="utf-8")
            with patch.object(intake, "PROJECTS_DIR", projects):
                code = intake.run_intake("demo", [one, two])
            prd = (projects / "demo" / "docs" / "intake" / "prd.md").read_text(encoding="utf-8")
            validation = (projects / "demo" / "docs" / "intake" / "validation.json").read_text(encoding="utf-8")
        self.assertEqual(code, 0)
        self.assertIn("First document body.", prd)
        self.assertIn("Second document body.", prd)
        self.assertIn('"is_valid": true', validation)


if __name__ == "__main__":
    unittest.main()
