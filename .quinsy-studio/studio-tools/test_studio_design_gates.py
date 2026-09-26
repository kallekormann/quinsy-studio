#!/usr/bin/env python3
"""Gate 2a/2b: discovery before scaffold, project kit, no indigo, no library promote."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from pre_impl_workflow import (
    design_system_approved,
    direction_approved,
    previous_human_gate_block,
    scaffold_design,
    scaffold_discovery,
    validate_gate_2a,
    validate_gate_2b,
    validate_human_gate,
)
from studio_design_discovery import (
    BARE_GATE_2_MSG,
    indigo_in_text,
    parse_cli_gate,
    sticker_inventory_issues,
)
from studio_execute import decide_from_state


def _write_discovery(root: Path, answered: bool = True) -> None:
    (root / "docs" / "design").mkdir(parents=True, exist_ok=True)
    answers = "operator console, dense, not a Linear clone, dark default" if answered else "_unanswered_"
    body = (
        f"# Discovery\n\n"
        f"Q: What job is done in one sitting?\nA: {answers}\n\n"
        f"Q: Sovereign or transient?\nA: {answers}\n\n"
        f"Q: What must we not look like?\nA: {answers}\n\n"
        f"Q: Density and mode?\nA: {answers}\n"
    )
    (root / "docs" / "design" / "discovery.md").write_text(body, encoding="utf-8")


def _write_direction(root: Path, *, stub: bool = False, indigo: bool = False) -> None:
    (root / "design").mkdir(parents=True, exist_ok=True)
    if stub:
        (root / "design" / "DESIGN.md").write_text(
            "# Design\n\n> Status: draft (waiting for human gate 2)\n\n"
            "_Describe look & feel from PRD._\n",
            encoding="utf-8",
        )
        return
    indigo_line = "Accent is #6366f1.\n" if indigo else "Accent token `--accent` is ink-on-paper ochre from the publisher.\n"
    (root / "design" / "DESIGN.md").write_text(
        "# Design specification — demo\n\n"
        "## Goals\nOperators finish a partner match in one sitting without a marketing hero.\n\n"
        "## Posture\nSovereign dense table. Dark default working surface.\n\n"
        "## Visual DNA\nNewsprint tables, ochre accent `--accent`, never a SaaS gradient dashboard.\n\n"
        "## Uniqueness / what we are not\n"
        "Not a Linear clone. No default SaaS indigo. No empty hero on operator lists. "
        "Chrome voice is a copy desk, not a growth banner.\n\n"
        "## Type\nSource Serif for titles, IBM Plex Sans for tables.\n\n"
        "## Color roles\nSurface `--surface`, ink `--ink`, accent `--accent`, danger `--danger`.\n\n"
        "## Voice\nBanned: 'delightful', 'seamless'.\n\n"
        + indigo_line,
        encoding="utf-8",
    )


class ParseGateTests(unittest.TestCase):
    def test_bare_2_refused(self):
        with self.assertRaises(ValueError) as ctx:
            parse_cli_gate("2")
        self.assertIn("2a", str(ctx.exception))
        self.assertEqual(str(ctx.exception), BARE_GATE_2_MSG)

    def test_2a_2b_ok(self):
        self.assertEqual(parse_cli_gate("2a"), "2a")
        self.assertEqual(parse_cli_gate("2b"), "2b")
        self.assertEqual(parse_cli_gate("0"), "0")


class PreviousGateTests(unittest.TestCase):
    def test_2a_needs_gate_1(self):
        msg = previous_human_gate_block({"human_gates": {"0": {"status": "approved"}}}, "2a")
        self.assertIsNotNone(msg)
        self.assertIn("Gate 1", msg)

    def test_2b_needs_2a(self):
        status = {
            "human_gates": {
                "0": {"status": "approved"},
                "1": {"status": "approved"},
            }
        }
        msg = previous_human_gate_block(status, "2b")
        self.assertIsNotNone(msg)
        self.assertIn("2a", msg)

    def test_2b_ok_when_2a_approved(self):
        status = {
            "human_gates": {
                "1": {"status": "approved"},
                "2a": {"status": "approved"},
            }
        }
        self.assertIsNone(previous_human_gate_block(status, "2b"))

    def test_legacy_2_counts_as_complete(self):
        status = {"human_gates": {"2": {"status": "approved"}}}
        self.assertTrue(design_system_approved(status))
        self.assertTrue(direction_approved(status))

    def test_bare_2_block_message(self):
        msg = previous_human_gate_block({"human_gates": {}}, 2)
        self.assertIn("2a", msg or "")


class DiscoveryValidatorTests(unittest.TestCase):
    def test_2a_fails_unanswered_and_stub(self):
        with tempfile.TemporaryDirectory() as raw:
            projects = Path(raw) / "projects"
            root = projects / "demo"
            root.mkdir(parents=True)
            _write_discovery(root, answered=False)
            _write_direction(root, stub=True)
            with patch("pre_impl_workflow.PROJECTS_DIR", projects), patch(
                "studio_adopt.is_adopt_project", return_value=False
            ):
                ok, issues = validate_gate_2a("demo")
            self.assertFalse(ok)
            self.assertTrue(any("human answers" in i.lower() or "unanswered" in i.lower() for i in issues))
            self.assertTrue(any("stub" in i.lower() for i in issues))

    def test_2a_fails_indigo(self):
        with tempfile.TemporaryDirectory() as raw:
            projects = Path(raw) / "projects"
            root = projects / "demo"
            root.mkdir(parents=True)
            _write_discovery(root, answered=True)
            _write_direction(root, indigo=True)
            with patch("pre_impl_workflow.PROJECTS_DIR", projects), patch(
                "studio_adopt.is_adopt_project", return_value=False
            ):
                ok, issues = validate_gate_2a("demo")
            self.assertFalse(ok)
            self.assertTrue(any("indigo" in i.lower() or "#6366f1" in i for i in issues))

    def test_2a_passes_unique_packet(self):
        with tempfile.TemporaryDirectory() as raw:
            projects = Path(raw) / "projects"
            root = projects / "demo"
            root.mkdir(parents=True)
            _write_discovery(root, answered=True)
            _write_direction(root)
            with patch("pre_impl_workflow.PROJECTS_DIR", projects), patch(
                "studio_adopt.is_adopt_project", return_value=False
            ):
                ok, issues = validate_gate_2a("demo")
            self.assertTrue(ok, issues)

    def test_2a_validate_human_gate_bare_2_refuses(self):
        ok, issues = validate_human_gate("demo", 2)
        self.assertFalse(ok)
        self.assertTrue(any("2a" in i for i in issues))


class ScaffoldIndigoTests(unittest.TestCase):
    def test_scaffold_design_has_no_indigo(self):
        with tempfile.TemporaryDirectory() as raw:
            projects = Path(raw) / "projects"
            root = projects / "demo"
            root.mkdir(parents=True)
            with patch("pre_impl_workflow.PROJECTS_DIR", projects):
                created = scaffold_design("demo", "core-views")
            blob = "\n".join(p.read_text(encoding="utf-8") for p in created if p.suffix in {".tsx", ".css", ".json", ".md"})
            self.assertFalse(indigo_in_text(blob), blob[:400])
            self.assertTrue((root / "ui" / "tokens" / "design-tokens.css").exists())

    def test_scaffold_discovery_does_not_create_prototype(self):
        with tempfile.TemporaryDirectory() as raw:
            projects = Path(raw) / "projects"
            root = projects / "demo"
            root.mkdir(parents=True)
            with patch("pre_impl_workflow.PROJECTS_DIR", projects):
                scaffold_discovery("demo")
            self.assertTrue((root / "docs" / "design" / "discovery.md").exists())
            self.assertFalse((root / "design" / "prototype" / "package.json").exists())


class KitValidatorTests(unittest.TestCase):
    def test_2b_fails_title_only_sticker(self):
        issues = sticker_inventory_issues(
            "<main><h1>Sticker sheet</h1><h2>Atoms</h2><h2>Molecules</h2><h2>Organisms</h2></main>"
        )
        self.assertTrue(any("controls" in i.lower() or "title-only" in i.lower() for i in issues))

    def test_2b_fails_missing_css_and_molecules(self):
        with tempfile.TemporaryDirectory() as raw:
            projects = Path(raw) / "projects"
            root = projects / "demo"
            root.mkdir(parents=True)
            with patch("pre_impl_workflow.PROJECTS_DIR", projects), patch(
                "studio_adopt.is_adopt_project", return_value=False
            ):
                ok, issues = validate_gate_2b("demo")
            self.assertFalse(ok)
            blob = " ".join(issues).lower()
            self.assertIn("design-tokens.css", blob)
            self.assertIn("molecule", blob)
            self.assertIn("organism", blob)


class ExecuteGateTests(unittest.TestCase):
    def test_decide_2a_discovery_when_not_ready(self):
        step = decide_from_state(
            "demo",
            {"human_gates": {"0": {"status": "approved"}, "1": {"status": "approved"}}},
            [],
            open_los=[],
            amendment_actions=[],
            prd_exists=True,
            gate2a_ready=False,
        )
        self.assertEqual(step.kind, "IMPLEMENT")
        self.assertIn("--discovery", step.command)
        self.assertNotIn("prototype", step.command)

    def test_decide_2a_hitl_when_packet_ready(self):
        step = decide_from_state(
            "demo",
            {"human_gates": {"0": {"status": "approved"}, "1": {"status": "approved"}}},
            [],
            open_los=[],
            amendment_actions=[],
            prd_exists=True,
            gate2a_ready=True,
        )
        self.assertEqual(step.kind, "HITL")
        self.assertIn("gate-2a", step.reason)
        self.assertIn("--gate 2a", step.command)

    def test_decide_2b_design_after_2a(self):
        step = decide_from_state(
            "demo",
            {
                "human_gates": {
                    "0": {"status": "approved"},
                    "1": {"status": "approved"},
                    "2a": {"status": "approved"},
                }
            },
            [],
            open_los=[],
            amendment_actions=[],
            prd_exists=True,
            gate2b_ready=False,
        )
        self.assertEqual(step.kind, "IMPLEMENT")
        self.assertIn("design", step.command)
        self.assertNotIn("--discovery", step.command)

    def test_decide_2b_hitl_when_kit_ready(self):
        step = decide_from_state(
            "demo",
            {
                "human_gates": {
                    "0": {"status": "approved"},
                    "1": {"status": "approved"},
                    "2a": {"status": "approved"},
                }
            },
            [],
            open_los=[],
            amendment_actions=[],
            prd_exists=True,
            gate2b_ready=True,
        )
        self.assertEqual(step.kind, "HITL")
        self.assertIn("gate-2b", step.reason)
        self.assertIn("--gate 2b", step.command)

    def test_legacy_gate_2_skips_design_hitl(self):
        step = decide_from_state(
            "demo",
            {
                "human_gates": {
                    "0": {"status": "approved"},
                    "1": {"status": "approved"},
                    "2": {"status": "approved"},
                },
                "current_sprint": "SPRINT-01",
                "sprint_hitl": {"scope_status": "approved", "groom_status": "approved"},
            },
            [],
            open_los=[],
            amendment_actions=[],
            prd_exists=True,
        )
        self.assertNotIn("gate-2a", step.reason)
        self.assertNotIn("gate-2b", step.reason)


if __name__ == "__main__":
    unittest.main()
