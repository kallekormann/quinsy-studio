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
    materialize_baseline,
    previous_human_gate_block,
    scaffold_design,
    scaffold_discovery,
    validate_gate_2a,
    validate_gate_2b,
    validate_human_gate,
)
from studio_design_discovery import (
    BARE_GATE_2_MSG,
    gate_2a_next,
    hand_rolled_control_issues,
    indigo_in_text,
    parse_cli_gate,
    record_critique_attempt,
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
        "## Aesthetic preset\n"
        "Substrate: `academic-editorial-ui`. Delta: copy-desk density for operators, not the catalog chrome.\n\n"
        "## Voice\nBanned: 'delightful', 'seamless'.\n\n"
        + indigo_line,
        encoding="utf-8",
    )
    if not stub:
        _write_critique(root)


def _write_critique(root: Path, *, fail: bool = False) -> None:
    verdict = "FAIL" if fail else "PASS"
    (root / "design").mkdir(parents=True, exist_ok=True)
    (root / "design" / "DIRECTION-CRITIQUE.md").write_text(
        "# Direction critique\n\n"
        f"- Audience: {verdict} — job taken from the PRD, not an invented persona\n"
        f"- Preset: {verdict} — academic-editorial-ui substrate with a product delta\n"
        f"- Type: {verdict} — Source Serif and IBM Plex Sans\n"
        f"- Color: {verdict} — surface, ink, accent, and danger roles\n"
        f"- Density: {verdict} — sovereign dense table\n"
        f"- Banned: {verdict} — no blobs, glass, hero type, emoji icons, or default indigo\n",
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

    def test_2a_allows_indigo_when_human_named_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_discovery(root, answered=True)
            disc = root / "docs" / "design" / "discovery.md"
            disc.write_text(
                disc.read_text(encoding="utf-8")
                + "\nQ: Accent hex?\nA: Primary CTA is #4f46e5.\n",
                encoding="utf-8",
            )
            _write_direction(root, indigo=False)
            design = root / "design" / "DESIGN.md"
            design.write_text(
                design.read_text(encoding="utf-8") + "\nHuman accent is #4f46e5.\n",
                encoding="utf-8",
            )
            with patch("pre_impl_workflow.project_dir", return_value=root):
                ok, issues = validate_gate_2a("demo")
            self.assertTrue(ok, issues)

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

    def test_2a_fails_when_reference_images_are_not_locked(self):
        with tempfile.TemporaryDirectory() as raw:
            projects = Path(raw) / "projects"
            root = projects / "demo"
            root.mkdir(parents=True)
            _write_discovery(root, answered=True)
            _write_direction(root)
            shots = root / "docs" / "design"
            shots.mkdir(parents=True, exist_ok=True)
            (shots / "home.png").write_bytes(b"\x89PNG\r\n")
            with patch("pre_impl_workflow.PROJECTS_DIR", projects), patch(
                "studio_adopt.is_adopt_project", return_value=False
            ):
                ok, issues = validate_gate_2a("demo")
            self.assertFalse(ok)
            self.assertTrue(any("home.png" in i or "Reference screens" in i for i in issues))

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

    def test_2b_requires_scoped_routes_and_headings(self):
        with tempfile.TemporaryDirectory() as raw:
            projects = Path(raw) / "projects"
            root = projects / "demo"
            (root / "design").mkdir(parents=True)
            (root / "design" / "DESIGN-SCOPE.md").write_text(
                "# Design scope\n\n**Selected scope:** `journey`\n\n"
                "## Required prototype routes\n\n"
                "- `/mocks/home`\n- `/mocks/app/emails`\n- `/mocks/app/invoices`\n\n"
                "## Required visible headings\n\n"
                "### `/mocks/home`\n- How does CraftOS clear a mailbox?\n",
                encoding="utf-8",
            )
            home = root / "design" / "prototype" / "app" / "mocks" / "home" / "page.tsx"
            home.parent.mkdir(parents=True)
            home.write_text("export default function Page(){return <h1>Less admin</h1>}\n", encoding="utf-8")
            from studio_design_discovery import mock_scope_issues

            issues = mock_scope_issues(root)
            blob = " ".join(issues)
            self.assertIn("/mocks/app/emails", blob)
            self.assertIn("How does CraftOS clear a mailbox?", blob)
            self.assertIn("navigable", blob)

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

    def test_decide_2a_critique_stays_implement(self):
        step = decide_from_state(
            "demo",
            {"human_gates": {"0": {"status": "approved"}, "1": {"status": "approved"}}},
            [],
            open_los=[],
            amendment_actions=[],
            prd_exists=True,
            gate2a_ready=False,
            gate2a_phase="write_critique",
        )
        self.assertEqual(step.kind, "IMPLEMENT")
        self.assertIn("DIRECTION-CRITIQUE", step.reason)
        self.assertNotEqual(step.kind, "HITL")


class CritiqueAndBaselineTests(unittest.TestCase):
    def test_2a_fails_without_preset_or_critique(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            _write_discovery(root, answered=True)
            _write_direction(root)
            (root / "design" / "DESIGN.md").write_text(
                (root / "design" / "DESIGN.md").read_text(encoding="utf-8").replace(
                    "academic-editorial-ui", "house-style"
                ),
                encoding="utf-8",
            )
            (root / "design" / "DIRECTION-CRITIQUE.md").unlink()
            with patch("pre_impl_workflow.project_dir", return_value=root):
                ok, issues = validate_gate_2a("demo")
            blob = " ".join(issues)
            self.assertFalse(ok)
            self.assertIn("preset", blob.lower())
            self.assertIn("DIRECTION-CRITIQUE", blob)

    def test_2a_fails_when_critique_line_is_fail(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            _write_discovery(root, answered=True)
            _write_direction(root)
            _write_critique(root, fail=True)
            with patch("pre_impl_workflow.project_dir", return_value=root):
                ok, issues = validate_gate_2a("demo")
            self.assertFalse(ok)
            self.assertTrue(any("FAIL" in i for i in issues))

    def test_gate_2a_next_is_critique_before_hitl(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            _write_discovery(root, answered=True)
            _write_direction(root)
            (root / "design" / "DIRECTION-CRITIQUE.md").unlink()
            self.assertEqual(gate_2a_next(root), "write_critique")
            _write_critique(root)
            self.assertEqual(gate_2a_next(root), "hitl")

    def test_critique_budget_after_distinct_fails(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            _write_discovery(root, answered=True)
            _write_direction(root)
            for n in range(4):
                (root / "design" / "DIRECTION-CRITIQUE.md").write_text(
                    f"# Direction critique {n}\n\n"
                    "- Audience: FAIL — invented persona\n"
                    "- Preset: FAIL — clone only\n"
                    "- Type: FAIL — unnamed\n"
                    "- Color: FAIL — indigo default\n"
                    "- Density: FAIL — unset\n"
                    "- Banned: FAIL — glass blobs\n"
                    f"attempt {n}\n",
                    encoding="utf-8",
                )
                record_critique_attempt(root)
            self.assertEqual(gate_2a_next(root), "critique_budget")

    def test_shell_routes_are_required(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            (root / "design").mkdir(parents=True)
            (root / "design" / "DESIGN-SCOPE.md").write_text(
                "# Design scope\n\n**Selected scope:** `core-views`\n\n"
                "## Required shell\n\n"
                "- `/mocks/sign-in`\n",
                encoding="utf-8",
            )
            from studio_design_discovery import mock_scope_issues

            blob = " ".join(mock_scope_issues(root))
            self.assertIn("/mocks/marketing", blob)
            self.assertIn("/mocks/app/settings", blob)
            self.assertIn("shell", blob)

    def test_internal_tool_skips_marketing_shell(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            (root / "status.json").write_text('{"archetype": "internal-tool"}\n', encoding="utf-8")
            (root / "design").mkdir(parents=True)
            (root / "design" / "DESIGN-SCOPE.md").write_text(
                "# Design scope\n\n**Selected scope:** `core-views`\n\n"
                "## Required prototype routes\n\n- `/mocks/home`\n",
                encoding="utf-8",
            )
            from studio_design_discovery import mock_scope_issues

            blob = " ".join(mock_scope_issues(root))
            self.assertNotIn("/mocks/marketing", blob)
            self.assertIn("Required shell", blob)

    def test_hand_rolled_popover_fails_when_kit_is_pulled(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            pulled = root / "ui" / "components" / "popover"
            pulled.mkdir(parents=True)
            (pulled / "popover.tsx").write_text("export function Popover(){return null}\n", encoding="utf-8")
            custom = root / "ui" / "components" / "atoms"
            custom.mkdir(parents=True)
            (custom / "Popover.tsx").write_text("function Popover(){return null}\n", encoding="utf-8")
            issues = hand_rolled_control_issues(root)
            self.assertTrue(any("popover" in i for i in issues))

    def test_materialize_copies_mocks_and_keeps_prototype(self):
        with tempfile.TemporaryDirectory() as raw:
            projects = Path(raw) / "projects"
            root = projects / "demo"
            page = root / "design" / "prototype" / "app" / "mocks" / "sign-in" / "page.tsx"
            page.parent.mkdir(parents=True)
            page.write_text("export default function Page(){return <h1>Sign in</h1>}\n", encoding="utf-8")
            nested = root / "design" / "prototype" / "app" / "mocks" / "app" / "settings" / "page.tsx"
            nested.parent.mkdir(parents=True)
            nested.write_text("export default function Page(){return <h1>Settings</h1>}\n", encoding="utf-8")
            with patch("pre_impl_workflow.PROJECTS_DIR", projects):
                created = materialize_baseline("demo")
            self.assertTrue((root / "app" / "sign-in" / "page.tsx").exists())
            self.assertTrue((root / "app" / "settings" / "page.tsx").exists())
            self.assertTrue((root / "docs" / "design" / "baseline.md").exists())
            self.assertTrue(page.exists())
            self.assertIn("visual baseline", (root / "docs" / "design" / "baseline.md").read_text(encoding="utf-8"))
            self.assertTrue(any(p.name == "baseline.md" for p in created))

    def test_materialize_lands_in_the_payload_app(self):
        with tempfile.TemporaryDirectory() as raw:
            projects = Path(raw) / "projects"
            root = projects / "demo"
            page = root / "design" / "prototype" / "app" / "mocks" / "sign-in" / "page.tsx"
            page.parent.mkdir(parents=True)
            page.write_text("export default function Page(){return <h1>Sign in</h1>}\n", encoding="utf-8")
            web = root / "apps" / "web"
            (web / "src" / "app" / "(app)").mkdir(parents=True)
            (web / "package.json").write_text("{}", encoding="utf-8")
            with patch("pre_impl_workflow.PROJECTS_DIR", projects):
                materialize_baseline("demo")
            self.assertTrue((web / "src" / "app" / "(app)" / "sign-in" / "page.tsx").exists())
            self.assertFalse((root / "app").exists())

    def test_receipt_requires_enhancement_when_baseline_is_rewritten(self):
        from studio_design_discovery import baseline_departure_issues

        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            (root / "docs" / "design").mkdir(parents=True)
            (root / "docs" / "design" / "baseline.md").write_text("# Design baseline\n", encoding="utf-8")
            pulled = root / "ui" / "components" / "dialog"
            pulled.mkdir(parents=True)
            (pulled / "dialog.tsx").write_text("export function Dialog(){return null}\n", encoding="utf-8")
            custom = root / "app" / "shell"
            custom.mkdir(parents=True)
            (custom / "page.tsx").write_text("function Dialog(){return null}\n", encoding="utf-8")
            issues = baseline_departure_issues(root, "## Plan\n- wired the screen\n")
            self.assertTrue(issues)
            clear = baseline_departure_issues(root, "## Plan\n- Enhancement: dialog copy for the desk voice\n")
            self.assertFalse(clear)

    def test_second_button_and_hardcoded_color_fail_ui_receipt(self):
        from studio_design_discovery import implementation_receipt_issues

        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            tokens = root / "ui" / "tokens"
            tokens.mkdir(parents=True)
            (tokens / "design-tokens.css").write_text(":root { --accent: #112233; }\n", encoding="utf-8")
            button = root / "ui" / "components" / "button"
            button.mkdir(parents=True)
            (button / "Button.tsx").write_text("export function Button(){return null}\n", encoding="utf-8")
            extra = root / "app" / "widgets"
            extra.mkdir(parents=True)
            (extra / "Again.tsx").write_text("function Button(){return null}\n", encoding="utf-8")
            (root / "docs").mkdir()
            (root / "docs" / "library-usage.json").write_text(
                '{"pulls":[{"name":"button"}]}\n', encoding="utf-8"
            )
            receipt = "## Design skill\n- n/a\n## Architecture skill\n- n/a\n"
            issues = implementation_receipt_issues(
                root,
                receipt,
                "ticket_type: ui-composition\nskills: FE-001\n",
                style_blobs=[("app/page.tsx", 'className="bg-indigo-600"')],
            )
            blob = " ".join(issues)
            self.assertIn("Second button", blob)
            self.assertIn("Hardcoded style", blob)
            self.assertIn("Design skill", blob)

    def test_ui_receipt_passes_when_it_cites_component_and_token(self):
        from studio_design_discovery import implementation_receipt_issues

        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            tokens = root / "ui" / "tokens"
            tokens.mkdir(parents=True)
            (tokens / "design-tokens.css").write_text(":root { --accent: #112233; }\n", encoding="utf-8")
            button = root / "ui" / "components" / "button"
            button.mkdir(parents=True)
            (button / "Button.tsx").write_text("export function Button(){return null}\n", encoding="utf-8")
            receipt = (
                "## Design skill\n"
                "- reused button with var(--accent) from ui/tokens/design-tokens.css\n"
            )
            issues = implementation_receipt_issues(
                root,
                receipt,
                "ticket_type: ui-composition\n",
                style_blobs=[],
            )
            self.assertFalse(issues)

    def test_architecture_skill_cannot_be_na_for_backend(self):
        from studio_design_discovery import implementation_receipt_issues

        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            bare = implementation_receipt_issues(
                root, "## Architecture skill\n- n/a\n", "skills: BE-001\n", style_blobs=[]
            )
            self.assertTrue(any("Architecture skill" in item for item in bare))
            filled = """## Architecture skill
- handler calls the service; the repository holds the parameterized query
- server authorization on the object
- allow-listed body
- idempotency key on the write
- errors omit the stack trace
- rate limit on the public route
- outbound timeout
- structured logs with a request id and no secrets
- Compose health check, temp cleanup, console drift written back
"""
            self.assertFalse(
                implementation_receipt_issues(root, filled, "skills: BE-003 PE-001\n", style_blobs=[])
            )

    def test_feature_receipt_may_leave_skill_sections_na(self):
        from studio_design_discovery import implementation_receipt_issues

        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            issues = implementation_receipt_issues(
                root,
                "## Design skill\n- n/a\n## Architecture skill\n- n/a\n",
                "ticket_type: feature\n",
                style_blobs=[("app/page.tsx", "color: #fff")],
            )
            self.assertFalse(issues)


if __name__ == "__main__":
    unittest.main()
