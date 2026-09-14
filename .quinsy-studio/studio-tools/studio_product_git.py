#!/usr/bin/env python3
"""Product-repo git: one commit per MOVE_DONE; push `dev` before review; main is HITL."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import List, Tuple

from backlog_paths import PROJECTS_DIR

DEV_BRANCH = "dev"
PROD_BRANCHES = frozenset({"main", "master", "production", "prod"})


def product_git_dir(project: str) -> Path:
    return PROJECTS_DIR / project


def _git(project: str, args: List[str], check: bool = False) -> subprocess.CompletedProcess:
    cwd = product_git_dir(project)
    return subprocess.run(
        ["git", "-C", str(cwd), *args],
        capture_output=True,
        text=True,
        check=check,
    )


def is_product_git_repo(project: str) -> bool:
    root = product_git_dir(project)
    return (root / ".git").exists() or (root / ".git").is_file()


def has_origin(project: str) -> bool:
    if not is_product_git_repo(project):
        return False
    r = _git(project, ["remote", "get-url", "origin"])
    return r.returncode == 0 and bool((r.stdout or "").strip())


def working_tree_dirty(project: str) -> bool:
    if not is_product_git_repo(project):
        return False
    r = _git(project, ["status", "--porcelain"])
    return r.returncode == 0 and bool((r.stdout or "").strip())


def commit_ticket(project: str, ticket_id: str, title: str = "") -> Tuple[bool, str]:
    """Stage and commit product tree for one ticket. No push. Returns (ok, message)."""
    if not is_product_git_repo(project):
        return False, "no product .git — skip commit"
    if not working_tree_dirty(project):
        return True, "clean working tree — nothing to commit"
    msg = f"{ticket_id}: {title.strip() or 'ticket done'}".strip()
    add = _git(project, ["add", "-A"])
    if add.returncode != 0:
        return False, (add.stderr or add.stdout or "git add failed").strip()
    commit = _git(project, ["commit", "-m", msg])
    if commit.returncode != 0:
        err = (commit.stderr or commit.stdout or "git commit failed").strip()
        return False, err
    return True, f"committed {msg}"


def needs_dev_push(project: str) -> bool:
    """True when origin exists and local HEAD is not fully on origin/dev."""
    if not is_product_git_repo(project) or not has_origin(project):
        return False
    _git(project, ["fetch", "origin", DEV_BRANCH], check=False)
    ahead = _git(project, ["rev-list", "--count", f"origin/{DEV_BRANCH}..HEAD"])
    if ahead.returncode != 0:
        return True
    try:
        return int((ahead.stdout or "0").strip() or "0") > 0
    except ValueError:
        return True


def push_dev(project: str) -> Tuple[bool, str]:
    """Push current HEAD to origin/dev. Never pushes main/production."""
    if not is_product_git_repo(project):
        return False, "no product .git"
    if not has_origin(project):
        return True, "no origin — skip push (local-only)"
    _git(project, ["branch", DEV_BRANCH], check=False)
    r = _git(project, ["push", "-u", "origin", f"HEAD:{DEV_BRANCH}"])
    if r.returncode != 0:
        return False, (r.stderr or r.stdout or "git push failed").strip()
    return True, f"pushed HEAD → origin/{DEV_BRANCH}"


def refuse_prod_push(branch: str) -> bool:
    return (branch or "").strip().lower() in PROD_BRANCHES
