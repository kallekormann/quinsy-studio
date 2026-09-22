import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import studio_env


class StudioEnvTests(unittest.TestCase):
    def test_refuse_without_approve_prints_hitl_command(self):
        msg = studio_env.refuse_without_approve("demo-app", "up")
        self.assertIn("./studio env demo-app up --approve", msg)
        self.assertIn("HITL", msg)
        self.assertNotIn("sk-", msg)

    def test_redact_strips_secret_values_not_names(self):
        text = "Connecting with POSTGRES_PASSWORD=hunter2secret and leftover hunter2secret"
        redacted = studio_env.redact_output(text, ["hunter2secret"])
        self.assertNotIn("hunter2secret", redacted)
        self.assertIn("POSTGRES_", redacted)
        self.assertIn("***", redacted)

    def test_compose_argv_uses_host_env_file(self):
        docker_dir = Path("/tmp/demo/docker")
        compose = docker_dir / "docker-compose.yml"
        host_env = Path("/tmp/secrets/demo/.env")
        argv = studio_env.compose_argv("demo", docker_dir, compose, host_env, ["up", "-d"])
        self.assertIn("--env-file", argv)
        self.assertIn(str(host_env), argv)
        line = studio_env.public_command_line(argv)
        self.assertNotIn("PASSWORD=", line)

    def test_ensure_host_env_keeps_existing_values(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp) / "secrets" / "demo"
            store.mkdir(parents=True)

            def _dir(_project: str) -> Path:
                return store

            with patch("studio_env.host_secret_dir", side_effect=_dir):
                path = studio_env.ensure_host_env_file("demo", names=["POSTGRES_PASSWORD", "REDIS_URL"])
                path.write_text("POSTGRES_PASSWORD=s3cretvalue\nREDIS_URL=\n", encoding="utf-8")
                path = studio_env.ensure_host_env_file("demo", names=["POSTGRES_PASSWORD", "REDIS_URL"])
                body = path.read_text(encoding="utf-8")
                self.assertIn("POSTGRES_PASSWORD=s3cretvalue", body)
                self.assertEqual(path, store / ".env")
                self.assertNotEqual(path, Path("projects/demo/docker/.env"))

    def test_cmd_env_up_without_approve_refuses(self):
        from studio import StudioOrchestrator

        orch = StudioOrchestrator()
        ok = orch.cmd_env("demo-app", "up", approve=False)
        self.assertFalse(ok)

    def test_secret_patterns_redact_dsn_not_names(self):
        raw = "fail postgresql://u:hunter2@db:5432/app with POSTGRES_PASSWORD=hunter2"
        out = studio_env.redact_secret_patterns(raw)
        self.assertNotIn("hunter2", out)
        self.assertNotIn("postgresql://u:", out)
        self.assertIn("POSTGRES_", out)

    def test_docker_missing_prints_install_not_env_dump(self):
        with patch("studio_env.shutil.which", return_value=None):
            self.assertFalse(studio_env.docker_cli_available())
        hint = studio_env.docker_install_hint()
        self.assertIn("docs.docker.com", hint)
        self.assertIn("no host fallback", hint)
        self.assertNotIn("cat .env", hint)


if __name__ == "__main__":
    unittest.main()
