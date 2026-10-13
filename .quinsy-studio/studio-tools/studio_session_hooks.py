"""Allow/deny decisions for the Cursor session-binding hooks.

Hook scripts call these. When HQ runtime is not cursor, every decision is allow.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Optional

from studio_agent_sessions import (
    bound_project,
    cursor_multi_project_enabled,
    session_id_from_hook,
)

_SECRET_NAMES = {".env", ".env.local"}
_STUDIO_CMDS = ("bind", "execute", "guard", "focus")


def _projects_dir(root: Path) -> Path:
    return root / "projects"


def project_of_path(path: str, *, studio_root: Path) -> str:
    """Return the projects/<slug> segment, or '' when the path is not a product tree."""
    if not path:
        return ""
    try:
        rel = Path(path).resolve().relative_to(_projects_dir(studio_root).resolve())
    except (OSError, ValueError):
        text = path.replace("\\", "/")
        marker = "/projects/"
        if marker not in text:
            return ""
        rest = text.split(marker, 1)[1]
        return rest.split("/", 1)[0]
    return rel.parts[0] if rel.parts else ""


def _is_secret(path: str) -> bool:
    name = Path(path).name
    return name in _SECRET_NAMES or name.endswith(".pem")


def read_decision(
    payload: dict,
    *,
    studio_root: Path,
    session_dir: Optional[Path] = None,
    settings: Optional[dict] = None,
) -> dict:
    if not cursor_multi_project_enabled(settings):
        return {"permission": "allow"}
    path = str(payload.get("file_path") or "")
    if _is_secret(path):
        return {
            "permission": "deny",
            "user_message": "Secret files stay unread. Use env.schema.json for names.",
        }
    sid = session_id_from_hook(payload)
    bound = bound_project(sid, session_dir=session_dir) if sid else ""
    if not bound:
        return {"permission": "allow"}
    slug = project_of_path(path, studio_root=studio_root)
    if slug and slug != bound:
        return {
            "permission": "deny",
            "user_message": f"This chat is bound to {bound}. {slug} needs its own chat and ./studio bind.",
        }
    return {"permission": "allow"}


def shell_decision(
    payload: dict,
    *,
    studio_root: Path,
    session_dir: Optional[Path] = None,
    settings: Optional[dict] = None,
) -> dict:
    if not cursor_multi_project_enabled(settings):
        return {"permission": "allow"}
    sid = session_id_from_hook(payload)
    bound = bound_project(sid, session_dir=session_dir) if sid else ""
    if not bound:
        return {"permission": "allow"}
    command = str(payload.get("command") or "")
    for match in re.finditer(r"(?:^|[\s;])(?:cd\s+)?(?:projects/)([A-Za-z0-9._-]+)", command):
        slug = match.group(1)
        if slug != bound:
            return _deny_shell(bound, slug)
    for match in re.finditer(r"-C\s+(\S+)", command):
        slug = project_of_path(match.group(1), studio_root=studio_root)
        if not slug and "projects/" in match.group(1).replace("\\", "/"):
            slug = project_of_path(
                str(studio_root / match.group(1).lstrip("./")),
                studio_root=studio_root,
            )
        if slug and slug != bound:
            return _deny_shell(bound, slug)
    return {"permission": "allow"}


def _deny_shell(bound: str, slug: str) -> dict:
    return {
        "permission": "deny",
        "user_message": f"This chat is bound to {bound}.",
        "agent_message": f"Do not git or enter projects/{slug}/. This chat is bound to {bound}.",
    }


def inject_session(payload: dict, *, settings: Optional[dict] = None) -> dict:
    """preToolUse: append --session to ./studio bind|execute|guard|focus when missing."""
    if not cursor_multi_project_enabled(settings):
        return {"permission": "allow"}
    if str(payload.get("tool_name") or "") not in {"", "Shell"}:
        return {"permission": "allow"}
    tool_input = payload.get("tool_input") or {}
    if not isinstance(tool_input, dict):
        return {"permission": "allow"}
    command = str(tool_input.get("command") or "")
    sid = session_id_from_hook(payload)
    if not sid or "--session" in command:
        return {"permission": "allow"}
    if not re.search(r"(?:^|[;&|]\s*)(?:\./)?studio\s+(" + "|".join(_STUDIO_CMDS) + r")\b", command):
        return {"permission": "allow"}
    updated = dict(tool_input)
    updated["command"] = command.rstrip() + f" --session {sid}"
    return {"permission": "allow", "updated_input": updated}


def session_start_message(
    payload: dict,
    *,
    session_dir: Optional[Path] = None,
    settings: Optional[dict] = None,
) -> dict:
    if not cursor_multi_project_enabled(settings):
        return {}
    sid = session_id_from_hook(payload)
    bound = bound_project(sid, session_dir=session_dir) if sid else ""
    if bound:
        text = f"This Cursor chat is bound to {bound}. Do not ./studio focus a sibling."
    else:
        text = (
            "This Cursor chat is not bound. Run ./studio bind <project> before product work. "
            "Do not guess a project. Claude Code and the CLI ignore this."
        )
    return {"additional_context": text}


def hook_response(payload: dict, *, studio_root: Path, session_dir: Optional[Path] = None, settings: Optional[dict] = None) -> dict:
    event = str(payload.get("hook_event_name") or "")
    if event == "sessionStart":
        return session_start_message(payload, session_dir=session_dir, settings=settings)
    if event == "beforeReadFile":
        return read_decision(payload, studio_root=studio_root, session_dir=session_dir, settings=settings)
    if event == "beforeShellExecution":
        return shell_decision(payload, studio_root=studio_root, session_dir=session_dir, settings=settings)
    if event == "preToolUse":
        return inject_session(payload, settings=settings)
    return {"permission": "allow"}


def loads_hook_payload(raw: str) -> dict:
    text = (raw or "").lstrip("\ufeff").strip()
    if not text:
        return {}
    data = json.loads(text)
    return data if isinstance(data, dict) else {}
