#!/usr/bin/env python3
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import studio_product_git as gitmod


def _init_repo(root: Path) -> None:
    subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=root, check=True)
    (root / "README").write_text("a\n", encoding="utf-8")
    subprocess.run(["git", "add", "README"], cwd=root, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=root, check=True, capture_output=True)


class ProductGitTests(unittest.TestCase):
    def test_commit_ticket_when_dirty(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _init_repo(root)
            (root / "src.txt").write_text("x\n", encoding="utf-8")
            with patch.object(gitmod, "PROJECTS_DIR", root.parent):
                # product name is tmp folder name under a fake PROJECTS_DIR
                pass
            project = root.name
            with patch.object(gitmod, "PROJECTS_DIR", root.parent):
                ok, msg = gitmod.commit_ticket(project, "DEMO-0001", "add src")
            self.assertTrue(ok, msg)
            log = subprocess.run(
                ["git", "-C", str(root), "log", "-1", "--oneline"],
                capture_output=True,
                text=True,
                check=True,
            )
            self.assertIn("DEMO-0001", log.stdout)

    def test_refuse_prod_push(self):
        self.assertTrue(gitmod.refuse_prod_push("main"))
        self.assertTrue(gitmod.refuse_prod_push("production"))
        self.assertFalse(gitmod.refuse_prod_push("dev"))


if __name__ == "__main__":
    unittest.main()
