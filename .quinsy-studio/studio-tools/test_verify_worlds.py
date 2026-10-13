#!/usr/bin/env python3
"""verify-worlds: intake stays untracked; skip leftover project dirs."""

from __future__ import annotations

import unittest
from pathlib import Path

from studio_context import _is_allowed_tracked_intake, _looks_like_real_project, verify_studio_abstraction


class IntakeAllowlistTests(unittest.TestCase):
    def test_no_intake_path_is_allowed(self):
        self.assertFalse(
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
    def test_any_product_reference_fails_including_provenance(self):
        from unittest.mock import patch
        import tempfile
        from pathlib import Path
        import studio_context

        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            studio = repo / ".quinsy-studio"
            kb = studio / "knowledge-base"
            kb.mkdir(parents=True)
            (kb / "frontend_playbook.md").write_text("# Guide\n\nNever ship acme-app chrome.\n", encoding="utf-8")
            (kb / "backend_playbook.md").write_text("- **Source:** `acme-app` (provenance only)\n", encoding="utf-8")
            lib = studio / "studio-library" / "ui"
            lib.mkdir(parents=True)
            (lib / "Toast.tsx").write_text("/** Bottom inset (ACME-0413). */\n", encoding="utf-8")
            (kb / "design_playbook.md").write_text("# Guide\n\nUse ./studio review <project>.\n", encoding="utf-8")
            (repo / "AGENTS.md").write_text("Example: ./studio focus acme-app\n", encoding="utf-8")
            with patch.object(studio_context, "QUINSY_STUDIO", studio), patch(
                "studio_portability.list_project_names", return_value=["acme-app"]
            ):
                ok, issues = verify_studio_abstraction()
            self.assertFalse(ok)
            blob = "\n".join(issues)
            for leak in ("frontend_playbook.md", "backend_playbook.md", "Toast.tsx", "AGENTS.md"):
                self.assertIn(leak, blob)
            self.assertIn("ACME-0413", blob)
            self.assertNotIn("design_playbook.md", blob)


if __name__ == "__main__":
    unittest.main()
