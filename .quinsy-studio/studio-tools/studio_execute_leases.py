"""Concurrent execute leases — cap parallel.max_projects (default 5)."""

from __future__ import annotations

import json
import os
import re
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

QUINSY_STUDIO = Path(__file__).parent.parent
LEASE_DIR = QUINSY_STUDIO / ".cache" / "execute-leases"
DEFAULT_MAX = 5
STALE_SECONDS = 4 * 3600
_SLUG = re.compile(r"[^a-zA-Z0-9._-]+")


def max_concurrent_projects(settings: Optional[Dict] = None) -> int:
    if settings is None:
        try:
            from studio_settings import load_settings

            settings = load_settings()
        except Exception:
            settings = {}
    parallel = (settings or {}).get("parallel") or {}
    raw = parallel.get("max_projects", DEFAULT_MAX)
    try:
        if raw is None or raw == "":
            n = DEFAULT_MAX
        else:
            n = int(raw)
    except (TypeError, ValueError):
        n = DEFAULT_MAX
    return max(1, n)


def _slug(project: str) -> str:
    return _SLUG.sub("-", (project or "").strip()) or "project"


def lease_path(project: str, *, lease_dir: Optional[Path] = None) -> Path:
    return (lease_dir or LEASE_DIR) / f"{_slug(project)}.json"


def _read_lease(path: Path) -> Optional[Dict]:
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else None
    except (OSError, json.JSONDecodeError):
        return None


def _is_stale(data: Dict, *, now: Optional[float] = None, stale_seconds: int = STALE_SECONDS) -> bool:
    now = time.time() if now is None else now
    try:
        acquired = float(data.get("acquired_at") or 0)
    except (TypeError, ValueError):
        return True
    return (now - acquired) > stale_seconds


def list_active_leases(
    *,
    lease_dir: Optional[Path] = None,
    now: Optional[float] = None,
    stale_seconds: int = STALE_SECONDS,
) -> List[str]:
    root = lease_dir or LEASE_DIR
    if not root.is_dir():
        return []
    active: List[str] = []
    for path in sorted(root.glob("*.json")):
        data = _read_lease(path)
        if not data:
            continue
        if _is_stale(data, now=now, stale_seconds=stale_seconds):
            try:
                path.unlink()
            except OSError:
                pass
            continue
        name = str(data.get("project") or path.stem)
        active.append(name)
    return active


def acquire_execute_lease(
    project: str,
    *,
    lease_dir: Optional[Path] = None,
    max_projects: Optional[int] = None,
    now: Optional[float] = None,
    stale_seconds: int = STALE_SECONDS,
) -> Tuple[bool, str]:
    """Return (granted, message). Same project refreshes. Sixth distinct project is queued."""
    from studio_hq_lock import hq_write_lock

    cap = max_projects if max_projects is not None else max_concurrent_projects()
    root = lease_dir or LEASE_DIR
    stamp = time.time() if now is None else now
    with hq_write_lock("execute-leases", cache_dir=root.parent if root else None):
        root.mkdir(parents=True, exist_ok=True)
        active = list_active_leases(lease_dir=root, now=stamp, stale_seconds=stale_seconds)
        mine = lease_path(project, lease_dir=root)
        if project in active:
            mine.write_text(
                json.dumps(
                    {"project": project, "acquired_at": stamp, "pid": os.getpid()},
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            return True, f"lease refreshed for {project} ({len(active)}/{cap})"
        others = [p for p in active if p != project]
        if len(others) >= cap:
            queued = ", ".join(others[:cap])
            return False, (
                f"QUEUED: {len(others)}/{cap} execute leases in use ({queued}). "
                f"Wait for HITL idle or ./studio execute <held> --release. "
                f"Did not rewrite isolation for {project}."
            )
        mine.write_text(
            json.dumps(
                {"project": project, "acquired_at": stamp, "pid": os.getpid()},
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        return True, f"lease acquired for {project} ({len(others) + 1}/{cap})"


def release_execute_lease(project: str, *, lease_dir: Optional[Path] = None) -> bool:
    path = lease_path(project, lease_dir=lease_dir)
    if not path.exists():
        return False
    try:
        path.unlink()
        return True
    except OSError:
        return False


def other_live_leases(project: str, *, lease_dir: Optional[Path] = None) -> List[str]:
    return [p for p in list_active_leases(lease_dir=lease_dir) if p != project]


def focus_isolation_blocked(
    project: str,
    *,
    force: bool = False,
    lease_dir: Optional[Path] = None,
) -> Optional[str]:
    """Warn when another product holds an execute lease (unless --force)."""
    if force:
        return None
    others = other_live_leases(project, lease_dir=lease_dir)
    if not others:
        return None
    held = ", ".join(others)
    return (
        f"FOCUS blocked: execute lease(s) held by {held}. "
        f"Rewriting .cursorignore would hide that live chat. "
        f"Use a separate IDE window, or ./studio focus {project} --force."
    )
