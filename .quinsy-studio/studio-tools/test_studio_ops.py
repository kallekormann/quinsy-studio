#!/usr/bin/env python3
"""Production ops from the agent seat (LO-0402..0404)."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import studio_ops
from studio_ops import (
    ensure_prod_env_file,
    explain_prod_env,
    missing_prod_names,
    op_needs_approve,
    prod_names,
    readiness_blockers,
    readiness_findings,
    run_op,
)

TEMPLATES = Path(__file__).resolve().parent.parent / "studio-templates"


def _materialize(root: Path) -> None:
    docker = root / "docker"
    docker.mkdir(parents=True)
    for name in ("docker-compose.yml", "compose.prod.yml"):
        docker.joinpath(name).write_text(
            (TEMPLATES / "docker" / name).read_text(encoding="utf-8").replace("{{PROJECT_NAME}}", "demo"),
            encoding="utf-8",
        )
    (root / "apps" / "web").mkdir(parents=True)
    (root / "apps" / "web" / "Dockerfile").write_text("FROM node:22-alpine\n", encoding="utf-8")
    (root / "docs" / "ops").mkdir(parents=True)
    (root / "docs" / "ops" / "incident-runbook.md").write_text("# Runbook\n", encoding="utf-8")


class SchemaTests(unittest.TestCase):
    def test_prod_group_names(self):
        names = prod_names()
        for n in ("VPS_SSH_HOST", "VPS_SSH_KEY_PATH", "COOLIFY_URL", "COOLIFY_TOKEN", "COOLIFY_APP_UUID", "PROD_DATABASE_URL"):
            self.assertIn(n, names)

    def test_explain_and_file_without_values(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            path = ensure_prod_env_file("demo", root)
            self.assertEqual(path.name, ".env.local")
            text = path.read_text(encoding="utf-8")
            self.assertIn("VPS_SSH_HOST=", text)
            explain = explain_prod_env("demo", root)
            self.assertIn(".env.local", explain)
            self.assertIn("[missing]", explain)
            path.write_text(text.replace("VPS_SSH_HOST=", "VPS_SSH_HOST=example.invalid"), encoding="utf-8")
            explain = explain_prod_env("demo", root)
            self.assertNotIn("example.invalid", explain)
            self.assertIn("VPS_SSH_HOST         [set]", explain)
            self.assertNotIn("VPS_SSH_HOST", missing_prod_names(root, ["VPS_SSH_HOST", "COOLIFY_URL"]))
            self.assertIn("COOLIFY_URL", missing_prod_names(root, ["VPS_SSH_HOST", "COOLIFY_URL"]))


class ReadinessTests(unittest.TestCase):
    def test_template_pair_is_ready(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            _materialize(root)
            self.assertEqual(readiness_blockers(root), [], readiness_findings(root))

    def test_missing_overlay_and_published_port_fail(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            _materialize(root)
            (root / "docker" / "compose.prod.yml").unlink()
            self.assertTrue(any("compose.prod.yml" in b for b in readiness_blockers(root)))
            _materialize_again = (TEMPLATES / "docker" / "compose.prod.yml").read_text(encoding="utf-8")
            (root / "docker" / "compose.prod.yml").write_text(
                _materialize_again.replace("  db:\n    ports: !reset []\n", "  db:\n"), encoding="utf-8"
            )
            self.assertTrue(any("db: no data port" in b for b in readiness_blockers(root)))


class RunOpTests(unittest.TestCase):
    def test_hitl_only_on_prod_migrate_and_destructive(self):
        self.assertTrue(op_needs_approve("migrate", ["--prod"]))
        self.assertTrue(op_needs_approve("cleanup", ["--prune-volumes"]))
        self.assertTrue(op_needs_approve("db", ["--reset"]))
        self.assertFalse(op_needs_approve("deploy", []))
        self.assertFalse(op_needs_approve("logs", ["--lines=50"]))
        self.assertFalse(op_needs_approve("status", []))
        self.assertFalse(op_needs_approve("cleanup", []))

    def test_refuses_without_names_and_logs(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            ok, text = run_op("demo", root, "deploy", [])
            self.assertFalse(ok)
            self.assertIn("COOLIFY_URL", text)
            self.assertTrue((root / ".env.local").is_file())
            ok, text = run_op("demo", root, "migrate", ["--prod"])
            self.assertFalse(ok)
            self.assertIn("--approve", text)

    def test_dry_run_redacts_and_logs(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            (root / ".env.local").write_text(
                "VPS_SSH_HOST=host.invalid\nVPS_SSH_USER=deploy\nVPS_SSH_KEY_PATH=/tmp/k\nVPS_COMPOSE_DIR=/srv/demo\n"
                "COOLIFY_URL=https://c.invalid\nCOOLIFY_TOKEN=tok_secret_value_123\nCOOLIFY_APP_UUID=u-1\n",
                encoding="utf-8",
            )
            ok, text = run_op("demo", root, "deploy", [], dry_run=True)
            self.assertTrue(ok, text)
            self.assertNotIn("tok_secret_value_123", text)
            ok, text = run_op("demo", root, "status", [], dry_run=True)
            self.assertTrue(ok)
            self.assertIn("compose.prod.yml", text)
            log = (root / "docs" / "ops" / "ops-log.md").read_text(encoding="utf-8")
            self.assertIn("`deploy` → dry-run", log)
            self.assertNotIn("tok_secret_value_123", log)

    def test_readiness_op(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            _materialize(root)
            ok, text = run_op("demo", root, "readiness", [])
            self.assertTrue(ok, text)
            self.assertIn("ship --to main: allowed", text)


if __name__ == "__main__":
    unittest.main()
