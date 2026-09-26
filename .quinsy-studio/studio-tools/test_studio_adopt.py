#!/usr/bin/env python3
"""Overlay safety for brownfield adopt — never wipe source or re-init .git."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import studio_adopt
from pre_impl_workflow import validate_gate_2
from studio_execute import decide_from_state
from studio_adopt import (
    AS_BUILT_FILES,
    adopt_project,
    as_built_is_ready,
    looks_like_application_source,
    overlay_studio,
)


GIT_MARKER = "ref: refs/heads/keep-me-adopt-test\n"

FILLED_AS_BUILT = (
    "# Evidence\n\n"
    "Default path is `src/app.py` serving GET /. "
    "Auth lives in `src/auth.py`. This paragraph is long enough "
    "to pass the as-built min-length check without placeholders.\n"
)


def _write_source_tree(root: Path) -> None:
    (root / "src").mkdir(parents=True, exist_ok=True)
    (root / "src" / "app.py").write_text("print('hello')\n", encoding="utf-8")
    (root / "package.json").write_text('{"name": "demo-app"}\n', encoding="utf-8")
    git = root / ".git"
    git.mkdir(parents=True, exist_ok=True)
    (git / "HEAD").write_text(GIT_MARKER, encoding="utf-8")


def _fill_as_built(root: Path) -> None:
    dest = root / "docs" / "as-built"
    dest.mkdir(parents=True, exist_ok=True)
    for name in AS_BUILT_FILES:
        (dest / name).write_text(FILLED_AS_BUILT, encoding="utf-8")


class LooksLikeSourceTests(unittest.TestCase):
    def test_src_and_package_json(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            self.assertFalse(looks_like_application_source(root))
            (root / "docs").mkdir()
            self.assertFalse(looks_like_application_source(root))
            (root / "src").mkdir()
            self.assertTrue(looks_like_application_source(root))

    def test_manifest_files(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            (root / "go.mod").write_text("module x\n", encoding="utf-8")
            self.assertTrue(looks_like_application_source(root))


class OverlaySafetyTests(unittest.TestCase):
    def test_overlay_keeps_src_and_git_and_skips_prototype(self):
        with tempfile.TemporaryDirectory() as raw:
            projects = Path(raw) / "projects"
            projects.mkdir()
            source = Path(raw) / "upstream"
            _write_source_tree(source)
            with patch.object(studio_adopt, "PROJECTS_DIR", projects):
                result = adopt_project("demo", str(source))
                dest = Path(result["path"])
                self.assertEqual(result["source_action"], "copied")
                self.assertTrue((dest / "src" / "app.py").exists())
                self.assertEqual((dest / "src" / "app.py").read_text(encoding="utf-8"), "print('hello')\n")
                self.assertEqual((dest / ".git" / "HEAD").read_text(encoding="utf-8"), GIT_MARKER)
                self.assertFalse((dest / "design" / "prototype").exists())
                status = json.loads((dest / "status.json").read_text(encoding="utf-8"))
                self.assertEqual(status["mode"], "adopt")
                self.assertEqual(status.get("design_scope"), "as-built")
                self.assertFalse(as_built_is_ready("demo"))
                product = (dest / "docs" / "as-built" / "00-product.md").read_text(encoding="utf-8")
                self.assertIn("_TODO_", product)

    def test_overlay_on_existing_dest_does_not_wipe_source(self):
        with tempfile.TemporaryDirectory() as raw:
            projects = Path(raw) / "projects"
            dest = projects / "live"
            dest.mkdir(parents=True)
            _write_source_tree(dest)
            with patch.object(studio_adopt, "PROJECTS_DIR", projects):
                overlay_studio(dest, "live")
                self.assertTrue((dest / "docs" / "studio.settings.yaml").exists())
                self.assertTrue((dest / "src" / "app.py").exists())
                self.assertEqual((dest / ".git" / "HEAD").read_text(encoding="utf-8"), GIT_MARKER)
                self.assertFalse((dest / ".git" / "config").exists())  # no git init
                second = adopt_project("live", str(dest))
                self.assertEqual(second["source_action"], "existing")
                self.assertTrue((dest / "src" / "app.py").exists())

    def test_as_built_ready_requires_filled_files(self):
        with tempfile.TemporaryDirectory() as raw:
            projects = Path(raw) / "projects"
            dest = projects / "demo"
            dest.mkdir(parents=True)
            with patch.object(studio_adopt, "PROJECTS_DIR", projects):
                overlay_studio(dest, "demo")
                self.assertFalse(as_built_is_ready("demo"))
                _fill_as_built(dest)
                self.assertTrue(as_built_is_ready("demo"))

    def test_overlay_does_not_add_git_when_missing(self):
        with tempfile.TemporaryDirectory() as raw:
            dest = Path(raw) / "nogit"
            dest.mkdir()
            (dest / "src").mkdir()
            (dest / "src" / "main.py").write_text("x = 1\n", encoding="utf-8")
            overlay_studio(dest, "nogit")
            self.assertFalse((dest / ".git").exists())


class AdoptExecuteTests(unittest.TestCase):
    def test_as_built_not_ready_is_implement(self):
        step = decide_from_state(
            "demo",
            {"mode": "adopt", "human_gates": {}},
            [],
            as_built_ready=False,
            prd_exists=False,
            open_los=[{"id": "LO-0054", "title": "x", "path": "backlog/open/LO-0054.md"}],
        )
        self.assertEqual(step.kind, "IMPLEMENT")
        self.assertIn("as-built", step.reason)

    def test_as_built_ready_missing_prd_is_verify(self):
        step = decide_from_state(
            "demo",
            {"mode": "adopt", "human_gates": {}},
            [],
            as_built_ready=True,
            prd_exists=False,
        )
        self.assertEqual(step.kind, "VERIFY")
        self.assertIn("prd.md", step.reason)

    def test_as_built_and_prd_gate_0_is_hitl(self):
        step = decide_from_state(
            "demo",
            {"mode": "adopt", "human_gates": {}},
            [],
            as_built_ready=True,
            prd_exists=True,
        )
        self.assertEqual(step.kind, "HITL")
        self.assertIn("as-built", step.reason)

    def test_sprint_review_beats_open_lo_on_adopt(self):
        step = decide_from_state(
            "demo",
            {
                "mode": "adopt",
                "human_gates": {
                    "0": {"status": "approved"},
                    "1": {"status": "approved"},
                    "2": {"status": "approved"},
                },
                "current_sprint": "SPRINT-01",
                "sprint_hitl": {
                    "review_status": "pending",
                    "scope_status": "approved",
                    "groom_status": "approved",
                },
            },
            [{"id": "DEMO-0001", "status": "done", "deps": []}],
            open_los=[{"id": "LO-0054", "title": "x", "path": "backlog/open/LO-0054.md"}],
            as_built_ready=True,
            prd_exists=True,
        )
        self.assertEqual(step.kind, "HITL")
        self.assertIn("sprint-review", step.reason)


class AdoptGate2Tests(unittest.TestCase):
    def test_gate_2_skips_next_prototype_when_adopt(self):
        with tempfile.TemporaryDirectory() as raw:
            projects = Path(raw) / "projects"
            dest = projects / "demo"
            dest.mkdir(parents=True)
            _write_source_tree(dest)
            with patch.object(studio_adopt, "PROJECTS_DIR", projects), patch(
                "pre_impl_workflow.PROJECTS_DIR", projects
            ):
                overlay_studio(dest, "demo")
                design = dest / "design" / "DESIGN.md"
                design.write_text(
                    "# Design truth\n\nExisting UI in `src/` uses a single page. "
                    "Surface map documents the live routes. No parallel prototype.\n",
                    encoding="utf-8",
                )
                (dest / "design" / "DESIGN-SCOPE.md").write_text(
                    "# Design scope\n\n- **scope:** as-built (existing product)\n",
                    encoding="utf-8",
                )
                (dest / "docs" / "as-built" / "01-surfaces.md").write_text(
                    FILLED_AS_BUILT, encoding="utf-8"
                )
                (dest / "docs" / "ia" / "surface-map.md").write_text(
                    "# Surface map\n\n| Surface | Route | Status |\n|---------|-------|--------|\n"
                    "| Home | `/` via `src/app.py` | shipped |\n",
                    encoding="utf-8",
                )
                (dest / "ui" / "tokens").mkdir(parents=True, exist_ok=True)
                (dest / "ui" / "tokens" / "design-tokens.css").write_text(
                    ":root {\n  --surface: #faf8f5;\n  --ink: #1a1a1a;\n  --accent: #b45309;\n}\n",
                    encoding="utf-8",
                )
                ok, issues = validate_gate_2("demo")
                self.assertTrue(ok, issues)
                self.assertFalse(any("prototype" in i.lower() for i in issues))


if __name__ == "__main__":
    unittest.main()
