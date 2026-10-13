"""Per-chat product binding. Cursor only — HQ runtime must be `cursor`."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

QUINSY_STUDIO = Path(__file__).parent.parent
STUDIO_ROOT = QUINSY_STUDIO.parent
PROJECTS_DIR = STUDIO_ROOT / "projects"
SESSION_DIR = QUINSY_STUDIO / ".cache" / "agent-sessions"

# LO-0419: Cursor docs. conversation_id is stable across turns.
# sessionStart sends session_id and documents it as the same value.
SESSION_ID_FIELDS = ("conversation_id", "session_id")
_SLUG = re.compile(r"[^a-zA-Z0-9._-]+")


def hq_runtime(settings: Optional[dict] = None) -> str:
    """Workspace runtime from HQ settings. Product yaml does not decide this."""
    if settings is None:
        from studio_settings import load_settings

        settings = load_settings(ledger="hq")
    return str((settings or {}).get("runtime") or "cursor").strip().lower()


def cursor_multi_project_enabled(settings: Optional[dict] = None) -> bool:
    return hq_runtime(settings) == "cursor"


def session_id_from_hook(payload: Optional[dict]) -> str:
    data = payload or {}
    for key in SESSION_ID_FIELDS:
        value = data.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def _slug(session_id: str) -> str:
    return _SLUG.sub("-", (session_id or "").strip()) or "session"


def session_path(session_id: str, *, session_dir: Optional[Path] = None) -> Path:
    return (session_dir or SESSION_DIR) / f"{_slug(session_id)}.json"


def bound_project(session_id: str, *, session_dir: Optional[Path] = None) -> str:
    if not (session_id or "").strip():
        return ""
    path = session_path(session_id, session_dir=session_dir)
    if not path.is_file():
        return ""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return ""
    return str(data.get("project") or "") if isinstance(data, dict) else ""


def bind_session(
    project: str,
    session_id: str,
    *,
    session_dir: Optional[Path] = None,
    projects_dir: Optional[Path] = None,
    settings: Optional[dict] = None,
) -> tuple[bool, str]:
    """Record this chat's product. Refuses non-cursor runtimes and unknown folders."""
    if not cursor_multi_project_enabled(settings):
        return False, (
            f"bind refused: HQ runtime is {hq_runtime(settings)!r}, not cursor. "
            "Claude Code and the CLI keep workspace focus isolation."
        )
    sid = (session_id or "").strip()
    if not sid:
        return False, "bind refused: pass --session <conversation_id> (Cursor hook field)."
    root = projects_dir or PROJECTS_DIR
    if not (root / project).is_dir():
        return False, f"bind refused: project '{project}' not found."
    dest_dir = session_dir or SESSION_DIR
    dest_dir.mkdir(parents=True, exist_ok=True)
    path = session_path(sid, session_dir=dest_dir)
    path.write_text(
        json.dumps(
            {
                "project": project,
                "session_id": sid,
                "bound_at": datetime.now().isoformat(timespec="seconds"),
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return True, f"bound session to {project}"


def clear_session(session_id: str, *, session_dir: Optional[Path] = None) -> bool:
    path = session_path(session_id, session_dir=session_dir)
    if not path.exists():
        return False
    path.unlink()
    return True
