#!/usr/bin/env python3
"""Gate 1 records Payload in or out. Execute scaffolds apps/web only after that."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import payload_foundation as pf


def _project(root: Path, name: str, blueprint: str, archetype: str = "saas-application") -> None:
    base = root / name
    (base / "docs" / "architecture").mkdir(parents=True)
    (base / "docs" / "adr").mkdir(parents=True)
    (base / "docs" / "architecture" / "BLUEPRINT.md").write_text(blueprint, encoding="utf-8")
    (base / "status.json").write_text(
        json.dumps({"archetype": archetype, "human_gates": {"1": {"status": "approved"}}}),
        encoding="utf-8",
    )


class PayloadFoundationTests(unittest.TestCase):
    def test_gate_refuses_a_web_project_with_no_decision(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _project(root, "demo", "# Architecture\n\nNo decision yet.\n" + ("x" * 200))
            with patch.object(pf, "PROJECTS", root):
                issues = pf.gate_1_payload_issues("demo")
        self.assertTrue(any("Payload: in" in item for item in issues))

    def test_gate_accepts_payload_in(self):
        text = "Payload: in\nLocales: en\nFallback locale: en\n"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _project(root, "demo", text)
            with patch.object(pf, "PROJECTS", root):
                self.assertEqual(pf.gate_1_payload_issues("demo"), [])

    def test_gate_refuses_opt_out_without_adr(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _project(root, "demo", "Payload: out\n")
            with patch.object(pf, "PROJECTS", root):
                issues = pf.gate_1_payload_issues("demo")
        self.assertTrue(any("opt out" in item for item in issues))

    def test_scaffold_writes_the_app_after_gate_1(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _project(root, "demo", "Payload: in\nLocales: en\n")
            with patch.object(pf, "PROJECTS", root):
                self.assertTrue(pf.scaffold_needed("demo"))
                created = pf.scaffold_payload_app("demo")
                self.assertTrue((root / "demo" / "apps" / "web" / "package.json").exists())
                self.assertTrue((root / "demo" / "docker" / "payload-app.compose.yml").exists())
                self.assertGreater(len(created), 5)
                again = pf.scaffold_payload_app("demo")
                self.assertEqual(again, [])

    def test_skill_file_exists(self):
        self.assertTrue(pf.skill_present())
        self.assertIn("wordpress", (pf.CMS_SKILL_DIR / "SKILL.md").read_text(encoding="utf-8").lower())

    def test_card_lists_be007_and_cms_migration_only_for_a_cms_move(self):
        import backlog_paths
        from studio_execute import ticket_card_for

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _project(root, "demo", "Payload: in\nLocales: en\n")
            folder = root / "demo" / "backlog" / "implement"
            folder.mkdir(parents=True)
            (folder / "DEMO-0001-pages.md").write_text(
                "---\nid: DEMO-0001\nskills: []\n---\nAdd a page.\n",
                encoding="utf-8",
            )
            (folder / "DEMO-0002-wp.md").write_text(
                "---\nid: DEMO-0002\nskills: []\n---\nMigrate content from WordPress.\n",
                encoding="utf-8",
            )
            with patch.object(pf, "PROJECTS", root), patch.object(backlog_paths, "PROJECTS_DIR", root):
                page = ticket_card_for("demo", "DEMO-0001")
                move = ticket_card_for("demo", "DEMO-0002")
        self.assertIsNotNone(page)
        self.assertIn("BE-007", page["skills"])
        self.assertNotIn("cms-migration", page["skills"])
        self.assertIn("knowledge-base/payload-playbook.md", page["playbooks"])
        self.assertIn("cms-migration", move["skills"])
        self.assertIn("BE-007", move["skills"])

    def test_profiles_include_redis_when_rag_is_named(self):
        self.assertEqual(pf.profiles_from_blueprint("Profiles: rag\n"), ["rag", "redis"])

    def test_receipt_flags_a_second_auth_system(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _project(root, "demo", "Payload: in\nLocales: en\n")
            with patch.object(pf, "PROJECTS", root):
                issues = pf.receipt_payload_issues("demo", "used clerk for login", "add users collection")
        self.assertTrue(any("auth" in item for item in issues))
        self.assertTrue(any("access" in item for item in issues))


if __name__ == "__main__":
    unittest.main()
