#!/usr/bin/env python3
"""verify-worlds: allow example intake templates; skip leftover project dirs."""

from __future__ import annotations

import unittest
from pathlib import Path

from studio_context import _is_allowed_tracked_intake, _looks_like_real_project, verify_studio_abstraction


class IntakeAllowlistTests(unittest.TestCase):
    def test_example_amendment_is_allowed(self):
        self.assertTrue(
            _is_allowed_tracked_intake("intake/amendments/acme/amendment_01.example.md")
        )

    def test_png_and_live_brief_not_allowed(self):
        self.assertFalse(
            _is_allowed_tracked_intake("intake/amendments/acme/ref-moodboard.png")
        )
        self.assertFalse(
            _is_allowed_tracked_intake("intake/amendments/acme/amendment_01.md")
        )


class ProjectDirTests(unittest.TestCase):
    def test_skips_cli_junk_names(self):
        self.assertFalse(_looks_like_real_project(Path("projects/--help")))
        self.assertFalse(_looks_like_real_project(Path("projects/LO-0042")))
        self.assertFalse(_looks_like_real_project(Path("projects/testproj")))


class AbstractionVerifyTests(unittest.TestCase):
    def test_fixture_project_folder_fails_and_provenance_passes(self):
        from unittest.mock import patch
        import tempfile
        from pathlib import Path
        import studio_context

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            kb = root / "knowledge-base"
            kb.mkdir()
            leak = kb / "frontend_playbook.md"
            leak.write_text("# Guide\n\nNever ship acme-app chrome.\n", encoding="utf-8")
            ok_file = kb / "backend_playbook.md"
            ok_file.write_text("# Guide\n\n- **Source:** `acme-app` (provenance only)\n", encoding="utf-8")
            with patch.object(studio_context, "QUINSY_STUDIO", root), patch(
                "studio_portability.list_project_names", return_value=["acme-app"]
            ):
                ok, issues = verify_studio_abstraction()
            self.assertFalse(ok)
            blob = "\n".join(issues)
            self.assertIn("acme-app", blob)
            self.assertIn("frontend_playbook.md", blob)
            self.assertNotIn("backend_playbook.md", blob)


if __name__ == "__main__":
    unittest.main()
