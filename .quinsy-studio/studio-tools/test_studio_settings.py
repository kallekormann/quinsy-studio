#!/usr/bin/env python3
"""Studio settings merge, secret refusal, per-step cost caps."""

from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from studio_settings import (
    apply_cost_policy,
    cost_cap_hit,
    estimate_tokens,
    load_settings,
    parse_simple_yaml,
    reset_usage,
    resolve_cost_step,
)


class YamlAndMergeTests(unittest.TestCase):
    def test_parse_nested_settings(self):
        data = parse_simple_yaml(
            "runtime: cursor\ncost:\n  profile: standard\n  steps:\n    design:\n      context: 40000\n      budget: 400000\n"
        )
        self.assertEqual(data["runtime"], "cursor")
        self.assertEqual(data["cost"]["steps"]["design"]["context"], 40000)

    def test_economy_scales_unless_overridden(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            committed = root / "studio.settings.yaml"
            local = root / "studio.settings.local.yaml"
            committed.write_text("runtime: cursor\ncost:\n  profile: standard\n", encoding="utf-8")
            local.write_text(
                "cost:\n  profile: economy\n  steps:\n    design:\n      context: 60000\n",
                encoding="utf-8",
            )
            settings = load_settings(committed=committed, local=local)
            self.assertEqual(settings["cost"]["profile"], "economy")
            self.assertEqual(settings["cost"]["steps"]["design"]["context"], 60000)
            self.assertEqual(settings["cost"]["steps"]["intake"]["context"], 12000)

    def test_refuses_secret_keys(self):
        with TemporaryDirectory() as tmp:
            local = Path(tmp) / "local.yaml"
            local.write_text("ANTHROPIC_API_KEY: sk-ant-secret-value-here\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                load_settings(committed=Path(tmp) / "missing.yaml", local=local)

    def test_standard_design_is_medium(self):
        settings = load_settings(committed=Path("nonexistent.yaml"), local=Path("nonexistent-local.yaml"))
        self.assertEqual(settings["cost"]["steps"]["design"]["context"], 40000)
        self.assertEqual(settings["cost"]["steps"]["implement"]["context"], 28000)
        self.assertEqual(settings["cost"]["session_token_budget"], 400_000)


class StepAndCapTests(unittest.TestCase):
    def test_resolve_steps(self):
        self.assertEqual(resolve_cost_step("IMPLEMENT", "./studio blueprint p", "architecture after PRD", "docs/architecture/"), "architecture")
        self.assertEqual(resolve_cost_step("IMPLEMENT", "./studio design p", "design track after architecture", "design/"), "design")
        self.assertEqual(resolve_cost_step("IMPLEMENT", "./studio resume p", "adopt: fill docs/as-built/", "docs/as-built/"), "intake")
        self.assertEqual(resolve_cost_step("VERIFY", "./studio sprint p --approve-scope", "agent-owned sprint scope", ""), "planning")
        self.assertEqual(resolve_cost_step("VERIFY", "./studio groom p --approve", "agent-owned groom", ""), "scoping")
        self.assertEqual(resolve_cost_step("IMPLEMENT", "./studio move p X implement", "next unblocked sprint ticket", ""), "implement")
        self.assertEqual(resolve_cost_step("STUDIO_LO", "./studio infusion", "idle infusion", ""), "learning")
        self.assertEqual(resolve_cost_step("VERIFY", "./studio retro p", "fill project retro", ""), "retro")
        self.assertEqual(resolve_cost_step("HITL", "./studio review p", "sprint-review: human tries shipped UI", ""), "review")
        self.assertEqual(resolve_cost_step("PRODUCTION", "./studio approve-design p T", "write design packet", ""), "design")

    def test_estimate_chars_div_4(self):
        self.assertEqual(estimate_tokens("abcd"), 1)
        self.assertEqual(estimate_tokens("a" * 40), 10)

    def test_cap_names_yaml_key(self):
        settings = load_settings(committed=Path("nope.yaml"), local=Path("nope-local.yaml"))
        hit = cost_cap_hit(
            step="design",
            turn=50_000,
            usage={"session": 0, "steps": {}},
            settings=settings,
        )
        self.assertIsNotNone(hit)
        self.assertEqual(hit["hit"], "cost.steps.design.context")

    def test_apply_policy_informs_without_recording(self):
        from studio_execute import ExecuteStep

        with TemporaryDirectory() as tmp:
            usage = Path(tmp) / "usage.json"
            reset_usage("demo", usage)
            settings = load_settings(committed=Path("nope.yaml"), local=Path("nope-local.yaml"))
            step = ExecuteStep(
                kind="IMPLEMENT",
                reason="design track after architecture: direction",
                command="./studio design demo",
                read="design/",
                loop=True,
                card={"id": "x", "files": [], "title": "x" * 200_000},
            )
            out = apply_cost_policy("demo", step, settings=settings, usage_path=usage)
            self.assertEqual(out.kind, "INFORM")
            self.assertFalse(out.loop)
            self.assertIn("cost.steps.design.context", out.reason)
            from studio_settings import load_usage as load_u

            self.assertEqual(load_u(usage).get("session"), 0)

    def test_apply_policy_records_under_cap(self):
        from studio_execute import ExecuteStep
        import studio_settings as ss

        with TemporaryDirectory() as tmp:
            usage = Path(tmp) / "usage.json"
            reset_usage("demo", usage)
            settings = load_settings(committed=Path("nope.yaml"), local=Path("nope-local.yaml"))
            step = ExecuteStep(
                kind="IMPLEMENT",
                reason="next unblocked sprint ticket",
                command="./studio move demo T-1 implement",
                loop=True,
                card={"id": "T-1", "title": "small", "files": []},
            )
            out = apply_cost_policy("demo", step, settings=settings, usage_path=usage)
            self.assertEqual(out.kind, "IMPLEMENT")
            self.assertGreater(ss.load_usage(usage)["session"], 0)
            self.assertIn("implement", ss.load_usage(usage)["steps"])


class ProjectLedgerTests(unittest.TestCase):
    def test_project_overlay_wins_session(self):
        import studio_settings as ss

        with TemporaryDirectory() as tmp:
            root = Path(tmp) / "demo"
            docs = root / "docs"
            docs.mkdir(parents=True)
            (docs / "studio.settings.yaml").write_text(
                "cost:\n  session_token_budget: 111000\n",
                encoding="utf-8",
            )
            orig = ss.PROJECTS_DIR
            ss.PROJECTS_DIR = Path(tmp)
            try:
                settings = ss.load_settings(project="demo", ledger="project")
                self.assertEqual(settings["cost"]["session_token_budget"], 111000)
                self.assertEqual(settings["cost"]["_ledger"], "project")
            finally:
                ss.PROJECTS_DIR = orig

    def test_studio_lo_uses_hq_usage_file(self):
        from studio_execute import ExecuteStep
        import studio_settings as ss

        with TemporaryDirectory() as tmp:
            hq_usage = Path(tmp) / "hq.json"
            proj = Path(tmp) / "demo"
            proj.mkdir()
            orig = ss.PROJECTS_DIR
            ss.PROJECTS_DIR = Path(tmp)
            try:
                reset_usage("demo", hq_usage)
                step = ExecuteStep(
                    kind="STUDIO_LO",
                    reason="idle infusion",
                    command="./studio infusion",
                    loop=True,
                    card={"id": "LO", "title": "small", "files": []},
                )
                out = apply_cost_policy("demo", step, usage_path=hq_usage)
                self.assertEqual(out.kind, "STUDIO_LO")
                self.assertEqual(out.cost.get("ledger"), "hq")
            finally:
                ss.PROJECTS_DIR = orig

    def test_init_writes_settings(self):
        import studio_settings as ss

        with TemporaryDirectory() as tmp:
            root = Path(tmp) / "demo"
            root.mkdir()
            written = ss.init_project_settings("demo", project_dir=root)
            self.assertTrue((root / "docs" / "studio.settings.yaml").exists())
            self.assertIn("docs/studio.settings.yaml", written)
            git = (root / ".gitignore").read_text(encoding="utf-8")
            self.assertIn("studio.settings.local.yaml", git)


if __name__ == "__main__":
    unittest.main()
