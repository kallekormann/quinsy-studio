#!/usr/bin/env python3
"""Sibling project isolation — Cursor ignore, path gate, request names."""

from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import studio_isolation
from studio_isolation import (
    HOOK_MARKER,
    ISOLATION_BEGIN,
    _cursorignore_without_block,
    install_project_git_hook,
    path_escapes_project,
    request_names_sibling,
    write_cursorignore,
)


class IsolationTests(unittest.TestCase):
    def test_path_escapes_other_project(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            projects = root / "projects"
            (projects / "acme-app").mkdir(parents=True)
            (projects / "other-app").mkdir(parents=True)
            with patch.object(studio_isolation, "STUDIO_ROOT", root), patch.object(
                studio_isolation, "PROJECTS_DIR", projects
            ):
                self.assertTrue(
                    path_escapes_project("acme-app", str(projects / "other-app" / "src" / "a.ts"))
                )
                self.assertFalse(
                    path_escapes_project("acme-app", str(projects / "acme-app" / "src" / "a.ts"))
                )
                self.assertTrue(
                    path_escapes_project("acme-app", "projects/other-app/src/a.ts")
                )
                self.assertFalse(path_escapes_project("acme-app", ".quinsy-studio/process/x.md"))

    def test_request_names_sibling(self):
        with patch.object(
            studio_isolation, "sibling_projects", lambda _p: ["other-app"]
        ):
            self.assertEqual(
                request_names_sibling("copy from other-app into this repo", "acme-app"),
                "other-app",
            )
            self.assertEqual(
                request_names_sibling("git add projects/other-app", "acme-app"),
                "other-app",
            )
            self.assertIsNone(request_names_sibling("add a login form", "acme-app"))

    def test_cursorignore_rewrites_isolation_block(self):
        with tempfile.TemporaryDirectory() as tmp:
            ignore = Path(tmp) / ".cursorignore"
            ignore.write_text("node_modules/\n", encoding="utf-8")
            with patch.object(studio_isolation, "CURSORIGNORE_PATH", ignore):
                write_cursorignore(["other-app"])
                text = ignore.read_text(encoding="utf-8")
                self.assertIn("node_modules/", text)
                self.assertIn(ISOLATION_BEGIN, text)
                self.assertIn("projects/other-app/", text)
                write_cursorignore(["third-app"])
                text2 = ignore.read_text(encoding="utf-8")
                self.assertNotIn("projects/other-app/", text2)
                self.assertIn("projects/third-app/", text2)
                self.assertEqual(text2.count(ISOLATION_BEGIN), 1)

    def test_strip_block_keeps_manual_lines(self):
        raw = "foo\n" + ISOLATION_BEGIN + "\nold\n# END QUINSY-ISOLATION\nbar\n"
        out = _cursorignore_without_block(raw)
        self.assertIn("foo", out)
        self.assertIn("bar", out)
        self.assertNotIn("old", out)

    def test_install_hook_embeds_expected_toplevel(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            projects = root / "projects"
            proj = projects / "acme-app"
            proj.mkdir(parents=True)
            init = subprocess.run(
                ["git", "init"],
                cwd=proj,
                capture_output=True,
                text=True,
            )
            if init.returncode != 0:
                self.skipTest("git init unavailable")
            with patch.object(studio_isolation, "PROJECTS_DIR", projects):
                hook = install_project_git_hook("acme-app")
            self.assertIsNotNone(hook)
            text = hook.read_text(encoding="utf-8")
            self.assertIn(HOOK_MARKER, text)
            self.assertIn(str(proj.resolve()), text)
            self.assertIn("mktemp", text)
            self.assertNotIn(" | while ", text)


if __name__ == "__main__":
    unittest.main()
