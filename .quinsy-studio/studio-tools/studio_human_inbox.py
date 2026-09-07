#!/usr/bin/env python3
"""Human notes during execute — queue, never preempt the current ACTION."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from sprint_hitl import sprint_directory

ABORT_RE = re.compile(r"^\s*(abort|stop this ticket|stop the ticket)\b", re.I)


def inbox_json_path(project: str, sprint: str) -> Path:
    return sprint_directory(project, sprint) / "human-inbox.json"


def inbox_md_path(project: str, sprint: str) -> Path:
    return sprint_directory(project, sprint) / "human-inbox.md"


def load_inbox(project: str, sprint: str) -> Dict:
    path = inbox_json_path(project, sprint)
    if not path.exists():
        return {"sprint": sprint, "notes": []}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        data.setdefault("notes", [])
        return data
    except json.JSONDecodeError:
        return {"sprint": sprint, "notes": []}


def save_inbox(project: str, sprint: str, data: Dict) -> Path:
    path = inbox_json_path(project, sprint)
    path.parent.mkdir(parents=True, exist_ok=True)
    data["sprint"] = sprint
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
        md.write_text(f"# Human inbox — {sprint}\n\nQueued mid-execute. Drain after MOVE_DONE.\n\n{line}", encoding="utf-8")
    return note


def open_notes(project: str, sprint: str) -> List[Dict]:
    if not sprint:
        return []
    return [n for n in load_inbox(project, sprint).get("notes", []) if n.get("status") == "open"]


def has_abort(project: str, sprint: str) -> bool:
    return any(n.get("abort") for n in open_notes(project, sprint))


def drain_open_notes(project: str, sprint: str) -> List[Dict]:
    """Mark open notes drained (read after MOVE_DONE). Returns the drained list."""
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
