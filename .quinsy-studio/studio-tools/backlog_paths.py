#!/usr/bin/env python3
"""
Project backlog layout and ticket discovery.

Layout (sprint HITL):
  projects/<p>/backlog/*.md          — product backlog (unscheduled tickets)
  projects/<p>/backlog/implement/    — in current sprint execution
  projects/<p>/backlog/done/          — completed
  projects/<p>/backlog/blocked/       — blocked / waiting on human

Legacy folders (open, analyze, plan, design, qa, review, reuse) are migrated
to the layout above on ./studio sprint / ./studio focus.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

STUDIO_ROOT = Path(__file__).parent.parent.parent
PROJECTS_DIR = STUDIO_ROOT / "projects"

# Active workflow folders (subdirectories of backlog/)
WORKFLOW_FOLDERS = ("implement", "done", "blocked")

# Legacy folders from the old 9-step workflow — migrated away
LEGACY_FOLDERS = ("open", "analyze", "plan", "design", "qa", "review", "reuse")

QUEUE_STATUS = "backlog"


def backlog_root(project: str) -> Path:
    return PROJECTS_DIR / project / "backlog"


def ticket_prefix(project: str) -> str:
    return project[:4].upper()


def workflow_dir(project: str, status: str) -> Path:
    """Return folder for implement / done / blocked."""
    path = backlog_root(project) / status
    path.mkdir(parents=True, exist_ok=True)
    return path


def queue_ticket_paths(project: str) -> List[Path]:
    """Ticket files in the product backlog queue (backlog/*.md at root)."""
    root = backlog_root(project)
    if not root.exists():
        return []
    prefix = ticket_prefix(project)
    return sorted(
        p for p in root.glob(f"{prefix}-*.md") if p.is_file()
    )


def all_ticket_locations(project: str) -> List[Tuple[Path, str]]:
    """Yield (path, folder_status) for every ticket file."""
    root = backlog_root(project)
    if not root.exists():
        return []
    prefix = ticket_prefix(project)
    found: List[Tuple[Path, str]] = []
    for path in queue_ticket_paths(project):
        found.append((path, QUEUE_STATUS))
    for folder in WORKFLOW_FOLDERS:
        ticket_dir = root / folder
        if ticket_dir.exists():
            for path in sorted(ticket_dir.glob(f"{prefix}-*.md")):
                found.append((path, folder))
    for folder in LEGACY_FOLDERS:
        ticket_dir = root / folder
        if ticket_dir.exists():
            for path in sorted(ticket_dir.glob(f"{prefix}-*.md")):
                legacy_status = "backlog" if folder == "open" else folder
                found.append((path, legacy_status))
    return found


def find_ticket(project: str, ticket_id: str) -> Tuple[Optional[Path], Optional[str]]:
    for path, status in all_ticket_locations(project):
        if path.name.startswith(f"{ticket_id}-"):
            return path, status
    return None, None


def migrate_legacy_backlog(project: str) -> List[str]:
    """
    Move tickets from legacy folders into the current layout.
    open/ → backlog root (status backlog). Other legacy folders → backlog root with warning.
    """
    root = backlog_root(project)
    if not root.exists():
        return []
    actions: List[str] = []
    prefix = ticket_prefix(project)

    open_dir = root / "open"
    if open_dir.exists():
        for path in sorted(open_dir.glob(f"{prefix}-*.md")):
            dest = root / path.name
            if dest.exists():
                actions.append(f"skip duplicate {path.name} (already in backlog/)")
                continue
            content = path.read_text(encoding="utf-8")
            content = re.sub(r"^status:\s*open\s*$", "status: backlog", content, flags=re.MULTILINE)
            dest.write_text(content, encoding="utf-8")
            path.unlink()
            actions.append(f"moved {path.name}: backlog/open/ → backlog/")
        if not any(open_dir.iterdir()):
            try:
                open_dir.rmdir()
            except OSError:
                pass

    for folder in LEGACY_FOLDERS:
        if folder == "open":
            continue
        legacy_dir = root / folder
        if not legacy_dir.exists():
            continue
        for path in sorted(legacy_dir.glob(f"{prefix}-*.md")):
            dest = root / path.name
            if dest.exists():
                actions.append(f"legacy {folder}/{path.name} — resolve duplicate manually")
                continue
            content = path.read_text(encoding="utf-8")
            content = re.sub(
                rf"^status:\s*{re.escape(folder)}\s*$",
                "status: backlog",
                content,
                flags=re.MULTILINE,
            )
            dest.write_text(content, encoding="utf-8")
            path.unlink()
            actions.append(f"moved {path.name}: backlog/{folder}/ → backlog/ (legacy workflow)")
        if not any(legacy_dir.iterdir()):
            try:
                legacy_dir.rmdir()
            except OSError:
                pass

    return actions


def ensure_backlog_layout(project: str) -> None:
    """Create current backlog folders; migrate legacy layout if present."""
    root = backlog_root(project)
    root.mkdir(parents=True, exist_ok=True)
    for folder in WORKFLOW_FOLDERS:
        (root / folder).mkdir(parents=True, exist_ok=True)
    migrate_legacy_backlog(project)


def read_ticket_meta(path: Path) -> Dict:
    text = path.read_text(encoding="utf-8")
    meta: Dict = {"path": path, "body": text, "file": path}
    for key in ("id", "title", "priority", "phase", "estimate", "sprint", "status"):
        # [ \t]* only — \s would swallow the newline after empty `sprint:` fields
        match = re.search(rf"^{key}:[ \t]*([^\n]*)$", text, re.MULTILINE)
        if match:
            value = match.group(1).strip().strip("'\"")
            if value:
                meta[key] = value
    tid_match = re.match(r"^([A-Z]+-\d+)", path.name)
    if tid_match and "id" not in meta:
        meta["id"] = tid_match.group(1)
    return meta


def set_ticket_sprint(content: str, sprint_name: str) -> str:
    """Set or replace frontmatter sprint: on a ticket body."""
    if re.search(rf"^sprint:[ \t]*{re.escape(sprint_name)}[ \t]*$", content, re.MULTILINE):
        return content
    if re.search(r"^sprint:[ \t]*\S", content, re.MULTILINE):
        return content
    if re.search(r"^sprint:[ \t]*$", content, re.MULTILINE):
        return re.sub(
            r"^sprint:[ \t]*$",
            f"sprint: {sprint_name}",
            content,
            count=1,
            flags=re.MULTILINE,
        )
    if "sprint:" not in content:
        return content.replace("created:", f"sprint: {sprint_name}\ncreated:", 1)
    return content


def list_unscheduled_backlog(project: str) -> List[Dict]:
    """Product backlog tickets without a sprint tag."""
    tickets: List[Dict] = []
    for path in queue_ticket_paths(project):
        meta = read_ticket_meta(path)
        if meta.get("sprint"):
            continue
        status = (meta.get("status") or "backlog").lower()
        if status in ("cancelled", "done", "superseded"):
            continue
        meta["from_feedback"] = "## Source feedback" in meta.get("body", "")
        tickets.append(meta)
    return tickets


def list_sprint_tagged_in_queue(project: str, sprint: str) -> List[Dict]:
    """Tickets in backlog/ root tagged for a sprint (planned, not yet implement)."""
    tagged: List[Dict] = []
    for path in queue_ticket_paths(project):
        meta = read_ticket_meta(path)
        if meta.get("sprint") == sprint:
            tagged.append(meta)
    return tagged
