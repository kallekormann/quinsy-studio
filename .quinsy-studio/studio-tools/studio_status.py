"""Project status.json — keep execute light.

ticket_file_snapshots (~8MB on a mature project) live in docs/ticket-file-snapshots.json.
gate_history is capped. load_status migrates old fat files on first read.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

STUDIO_ROOT = Path(__file__).parent.parent.parent
PROJECTS_DIR = STUDIO_ROOT / "projects"

GATE_HISTORY_KEEP = 40
SNAPSHOTS_REL = Path("docs") / "ticket-file-snapshots.json"


def status_path(project: str) -> Path:
    return PROJECTS_DIR / project / "status.json"


def snapshots_path(project: str) -> Path:
    return PROJECTS_DIR / project / SNAPSHOTS_REL


def default_status(project: str) -> Dict[str, Any]:
    today = datetime.now().strftime("%Y-%m-%d")
    return {
        "name": project,
        "phase": "0",
        "gate": "0",
        "gate_status": "open",
        "mode": "core",
        "created": today,
        "last_update": today,
        "archetype": "unknown",
        "current_sprint": None,
        "active_ticket": None,
        "gate_history": [],
        "human_gates": {},
    }


def load_snapshots(project: str) -> Dict[str, Any]:
    path = snapshots_path(project)
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    if isinstance(data, dict):
        return data
    return {}


def save_snapshots(project: str, snapshots: Dict[str, Any]) -> Path:
    path = snapshots_path(project)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(snapshots, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def _cap_gate_history(status: Dict[str, Any]) -> bool:
    hist = status.get("gate_history")
    if not isinstance(hist, list) or len(hist) <= GATE_HISTORY_KEEP:
        return False
    status["gate_history"] = hist[-GATE_HISTORY_KEEP:]
    return True


def peel_heavy_status_fields(project: str, status: Dict[str, Any]) -> bool:
    """Move snapshots to sidecar and cap gate_history. Returns True if status.json should be rewritten."""
    changed = False
    inline = status.pop("ticket_file_snapshots", None)
    if inline:
        merged = load_snapshots(project)
        if isinstance(inline, dict):
            merged.update(inline)
        save_snapshots(project, merged)
        changed = True
    if _cap_gate_history(status):
        changed = True
    return changed


def read_status_file(path: Path, project: str) -> Dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return default_status(project)
    if not isinstance(data, dict):
        return default_status(project)
    return data


def load_status(project: str) -> Dict[str, Any]:
    path = status_path(project)
    if not path.exists():
        return default_status(project)
    data = read_status_file(path, project)
    if peel_heavy_status_fields(project, data):
        write_status_file(path, data)
    return data


def write_status_file(path: Path, status: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(status, indent=2, ensure_ascii=False), encoding="utf-8")


def save_status(project: str, status: Dict[str, Any]) -> None:
    status["last_update"] = datetime.now().strftime("%Y-%m-%d")
    peel_heavy_status_fields(project, status)
    write_status_file(status_path(project), status)


def snapshot_for_ticket(project: str, ticket_id: str, status: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
    snaps = load_snapshots(project)
    if status:
        extra = status.get("ticket_file_snapshots") or {}
        if isinstance(extra, dict) and ticket_id in extra:
            return extra.get(ticket_id) or {}
    got = snaps.get(ticket_id) or {}
    return got if isinstance(got, dict) else {}
