#!/usr/bin/env python3
"""verify-worlds: allow example intake templates; skip leftover project dirs."""

from __future__ import annotations

import unittest
from pathlib import Path

from studio_context import _is_allowed_tracked_intake, _looks_like_real_project


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


if __name__ == "__main__":
    unittest.main()
