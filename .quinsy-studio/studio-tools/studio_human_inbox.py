#!/usr/bin/env python3
"""Human notes during execute — queue, never preempt the current ACTION."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from sprint_hitl import sprint_directory


def _projects_dir() -> Path:
    from sprint_hitl import PROJECTS_DIR

    return PROJECTS_DIR

ABORT_RE = re.compile(r"^\s*(abort|stop this ticket|stop the ticket)\b", re.I)
# Human is answering HITL or recovering drift — do not treat as a mid-execute note.
HITL_REPLY_RE = re.compile(
    r"(?i)("
    r"\bback on track\b|"
    r"\bresume(?: the)? project\b|"
    r"approve-design|"
    r"approve\s+gate\s*[012]|"
    r"./studio approve|"
    r"review\s+--approve|"
    r"--approve\b|"
    r"\bapprove(?:d)?\s+(?:the\s+)?(?:review|amendment|design|gate|sprint)\b|"
    r"\b(?:review|amendment|design|sprint)\s+(?:is\s+)?approved\b"
    r")"
)
SHORT_HITL_RE = re.compile(
    r"(?i)^\s*(approved|looks good|lgtm|shipped looks good)\s*[.!]?\s*$"
)
# Studio HQ / LO / HQ-T — never a product-sprint inbox note (LO-0243).
STUDIO_HQ_RE = re.compile(
    r"(?i)("
    r"\bHQ-T\d+\b|"
    r"\bLO-\d{3,}\b|"
    r"\.quinsy-studio\b|"
    r"\bstudio[- ]hq\b|"
    r"\bstudio-meta\b|"
    r"\bback to (?:the )?quinsy[- ]studio process\b|"
    r"\bquinsy[- ]studio\b"
    r")"
)


def is_studio_hq_request(text: str) -> bool:
    """True when the bubble is studio process, not a product-sprint note."""
    return bool(STUDIO_HQ_RE.search(text or ""))


def should_queue_as_note(text: str, *, named_hitl_waiting: bool = True) -> bool:
    """True when a chat bubble must be ./studio note'd and the current ACTION resumed.

    Bare “looks good” / “approved” is a HITL reply only when execute is already STOP
    (gates, sprint review). Mid-sprint ticket ACK is queued/ignored, not a stop.
    """
    t = (text or "").strip()
    if not t:
        return False
    if ABORT_RE.match(t):
        return True
    if HITL_REPLY_RE.search(t):
        return False
    if is_studio_hq_request(t):
        return False
    if SHORT_HITL_RE.match(t):
        return not named_hitl_waiting
    return True


def inbox_json_path(project: str, sprint: str) -> Path:
    if (sprint or "").strip():
        return sprint_directory(project, sprint) / "human-inbox.json"
    return _projects_dir() / project / "docs" / "human-inbox.json"


def inbox_md_path(project: str, sprint: str) -> Path:
    if (sprint or "").strip():
        return sprint_directory(project, sprint) / "human-inbox.md"
    return _projects_dir() / project / "docs" / "human-inbox.md"


def load_inbox(project: str, sprint: str) -> Dict:
    path = inbox_json_path(project, sprint)
    label = sprint or "pre-sprint"
    if not path.exists():
        return {"sprint": label, "notes": []}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        data.setdefault("notes", [])
        return data
    except json.JSONDecodeError:
        return {"sprint": label, "notes": []}


def save_inbox(project: str, sprint: str, data: Dict) -> Path:
    path = inbox_json_path(project, sprint)
    path.parent.mkdir(parents=True, exist_ok=True)
    data["sprint"] = sprint or "pre-sprint"
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return path


def append_note(project: str, sprint: str, text: str) -> Dict:
    text = (text or "").strip()
    if not text:
        raise ValueError("note text is required")
    data = load_inbox(project, sprint)
    note = {
        "id": f"N-{len(data['notes']) + 1:03d}",
        "ts": datetime.now().isoformat(timespec="seconds"),
        "text": text,
        "abort": bool(ABORT_RE.match(text)),
        "status": "open",
    }
    data["notes"].append(note)
    save_inbox(project, sprint, data)
    md = inbox_md_path(project, sprint)
    md.parent.mkdir(parents=True, exist_ok=True)
    line = f"- **{note['id']}** `{note['ts']}` ({classify_note(text)}): {text}\n"
    if md.exists():
        md.write_text(md.read_text(encoding="utf-8") + line, encoding="utf-8")
    else:
        scope = sprint or "pre-sprint"
        md.write_text(
            f"# Human inbox — {scope}\n\nQueued mid-execute. Drain after MOVE_DONE.\n\n{line}",
            encoding="utf-8",
        )
    return note


def _open_from_scope(project: str, sprint: str) -> List[Dict]:
    return [n for n in load_inbox(project, sprint).get("notes", []) if n.get("status") == "open"]


def open_notes(project: str, sprint: str = "") -> List[Dict]:
    """Open notes in the pre-sprint docs inbox plus the current sprint inbox."""
    out: List[Dict] = []
    seen = set()
    scopes = [""]
    if sprint:
        scopes.append(sprint)
    for scope in scopes:
        for note in _open_from_scope(project, scope):
            key = f"{scope or 'pre'}:{note.get('id')}"
            if key in seen:
                continue
            seen.add(key)
            out.append(note)
    return out


def has_abort(project: str, sprint: str) -> bool:
    return any(n.get("abort") for n in open_notes(project, sprint))


def _drain_scope(project: str, sprint: str) -> List[Dict]:
    data = load_inbox(project, sprint)
    drained = []
    for note in data.get("notes", []):
        if note.get("status") == "open":
            note["status"] = "drained"
            note["drained_at"] = datetime.now().isoformat(timespec="seconds")
            drained.append(note)
    if drained:
        save_inbox(project, sprint, data)
    return drained


def drain_open_notes(project: str, sprint: str) -> List[Dict]:
    """Mark open notes drained (read after MOVE_DONE). Returns the drained list."""
    drained = _drain_scope(project, "")
    if sprint:
        drained.extend(_drain_scope(project, sprint))
    return drained


def classify_note(text: str) -> str:
    t = (text or "").lower()
    if ABORT_RE.match(text or ""):
        return "abort"
    if any(w in t for w in ("veto", "not lemon", "don't use", "do not use", "instead of")):
        return "tech-veto"
    if any(w in t for w in ("layout", "ux", "ia ", "placement", "visual", "spacing", "type")):
        return "design"
    if any(w in t for w in ("want", "idea", "could we", "add a", "new feature")):
        return "feedback"
    return "note"
