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
    SECRETS_BEGIN,
    _cursorignore_without_block,
    install_project_git_hook,
    path_escapes_project,
    request_names_sibling,
    secrets_ignore_block,
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
                self.assertIn(SECRETS_BEGIN, text)
                self.assertIn("**/.env", text)
                self.assertIn("projects/other-app/", text)
                write_cursorignore(["third-app"])
                text2 = ignore.read_text(encoding="utf-8")
                self.assertNotIn("projects/other-app/", text2)
                self.assertIn("projects/third-app/", text2)
                self.assertEqual(text2.count(ISOLATION_BEGIN), 1)
                self.assertEqual(text2.count(SECRETS_BEGIN), 1)
                self.assertIn("**/.env", text2)

    def test_secrets_block_covers_focused_project_env(self):
        block = secrets_ignore_block()
        self.assertIn("projects/*/.env", block)
        self.assertIn("**/.env.local", block)
        self.assertIn(".quinsy-studio/.secrets/", block)

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

    def test_hq_commit_blocked_projects_path(self):
        from studio_isolation import hq_commit_blocked

        self.assertIsNone(hq_commit_blocked([".quinsy-studio/CHANGELOG.md", "AGENTS.md"]))
        msg = hq_commit_blocked(["projects/foo/src/a.ts"])
        self.assertIsNotNone(msg)
        self.assertIn("projects/foo", msg)
        self.assertIsNotNone(hq_commit_blocked(["ideation/ideas/I-001.md"]))
        self.assertIsNotNone(hq_commit_blocked([".quinsy-studio/backlog/done/LO-0001.md"]))
        self.assertIsNotNone(hq_commit_blocked([".quinsy-studio/retros/meta-retro-2026-10-01.md"]))
        self.assertIsNone(hq_commit_blocked([".quinsy-studio/studio-templates/ideation/rubric.md"]))
        self.assertIsNone(hq_commit_blocked([".quinsy-studio/knowledge-base/learnings/process/workflow.md"]))

    def test_install_studio_hq_hook_refuses_projects_in_index(self):
        from studio_isolation import HQ_HOOK_MARKER, install_studio_hq_git_hook

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True)
            hook = install_studio_hq_git_hook(studio_root=root)
            self.assertIsNotNone(hook)
            text = hook.read_text(encoding="utf-8")
            self.assertIn(HQ_HOOK_MARKER, text)
            (root / "projects" / "foo").mkdir(parents=True)
            (root / "projects" / "foo" / "leak.txt").write_text("nope\n")
            subprocess.run(["git", "add", "projects/foo/leak.txt"], cwd=root, check=True)
            result = subprocess.run(
                ["sh", str(hook)],
                cwd=root,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0, result.stderr)
            self.assertIn("projects/foo", result.stderr)


if __name__ == "__main__":
    unittest.main()
