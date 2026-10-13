#!/usr/bin/env python3
"""Ticket production stream vs ready-for-implementation (silent execute)."""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from backlog_paths import PROJECTS_DIR, list_unscheduled_backlog, queue_ticket_paths, read_ticket_meta

DEFAULT_READY_MIN = 2
DEFAULT_REVIEW_EVERY = 2
ARCH_TYPES = frozenset(
    {"api", "backend", "database", "infra", "platform", "integration"}
)
ARCH_TITLE = re.compile(
    r"\b(api|schema|migrat|auth|queue|postgres|postgres|endpoint|adr)\b",
    re.I,
)


def production_ready_min(project: str = "") -> int:
    try:
        from studio_settings import load_settings

        settings = load_settings(project=project, ledger="project" if project else "hq")
        return max(1, int((settings.get("cost") or {}).get("production_ready_min") or DEFAULT_READY_MIN))
    except Exception:
        return DEFAULT_READY_MIN


def human_review_every_sprints(project: str = "") -> int:
    try:
        from studio_settings import load_settings

        settings = load_settings(project=project, ledger="project" if project else "hq")
        return max(1, int((settings.get("cost") or {}).get("human_review_every_sprints") or DEFAULT_REVIEW_EVERY))
    except Exception:
        return DEFAULT_REVIEW_EVERY


def needs_architecture_from_blob(ticket_type: str, title: str) -> bool:
    tt = (ticket_type or "").strip().lower()
    if tt in ARCH_TYPES:
        return True
    return bool(ARCH_TITLE.search(title or ""))


def inferred_stream(meta: Dict) -> str:
    """Ready vs production is computed from pending packets, not a cached stream: field."""
    if str(meta.get("design_status") or "").strip() == "pending":
        return "production"
    if str(meta.get("architecture_status") or "").strip() == "pending":
        return "production"
    return "ready"


def ticket_is_ready(meta: Dict) -> bool:
    return inferred_stream(meta) == "ready"


def count_ready_backlog(project: str) -> int:
    n = 0
    for meta in list_unscheduled_backlog(project):
        if ticket_is_ready(meta) and str(meta.get("status") or "backlog") in ("backlog", "open"):
            n += 1
    return n


def count_production_backlog(project: str) -> int:
    n = 0
    for meta in list_unscheduled_backlog(project):
        if inferred_stream(meta) == "production":
            n += 1
    return n


def pipeline_starved(project: str) -> bool:
    if count_production_backlog(project) <= 0:
        return False
    return count_ready_backlog(project) < production_ready_min(project)


def next_production_ticket(project: str) -> Optional[Dict]:
    rows = [
        m
        for m in list_unscheduled_backlog(project)
        if inferred_stream(m) == "production"
    ]
    rows.sort(key=lambda m: str(m.get("id") or ""))
    return rows[0] if rows else None


def architecture_note_path(project: str, ticket_id: str) -> Path:
    return PROJECTS_DIR / project / "docs" / "architecture" / f"{ticket_id}.md"


def architecture_packet_issues(project: str, ticket_id: str) -> List[str]:
    from architecture_checks import architecture_packet_issues as packet_issues
    from backlog_paths import find_ticket

    ticket, _status = find_ticket(project, ticket_id)
    ticket_text = ticket.read_text(encoding="utf-8", errors="ignore") if ticket else ""
    return packet_issues(PROJECTS_DIR / project, ticket_id, ticket_text)


def architecture_packet_ready(project: str, ticket_id: str) -> bool:
    return not architecture_packet_issues(project, ticket_id)


def set_architecture_approved(content: str) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    if re.search(r"^architecture_status:", content, re.MULTILINE):
        content = re.sub(
            r"^architecture_status:.*$",
            "architecture_status: approved",
            content,
            count=1,
            flags=re.MULTILINE,
        )
    else:
        content = re.sub(r"^---\n", "---\narchitecture_status: approved\n", content, count=1)
    if re.search(r"^architecture_approved_at:", content, re.MULTILINE):
        content = re.sub(
            r"^architecture_approved_at:.*$",
            f"architecture_approved_at: {now}",
            content,
            count=1,
            flags=re.MULTILINE,
        )
    else:
        content = re.sub(
            r"^---\n",
            f"---\narchitecture_approved_at: {now}\n",
            content,
            count=1,
        )
    return refresh_stream_field(content)


def refresh_stream_field(content: str) -> str:
    meta = {}
    for key in ("design_status", "architecture_status", "stream"):
        m = re.search(rf"^{key}:\s*(\S+)", content, re.M)
        if m:
            meta[key] = m.group(1)
    stream = inferred_stream(meta)
    if re.search(r"^stream:", content, re.M):
        return re.sub(r"^stream:.*$", f"stream: {stream}", content, count=1, flags=re.M)
    return re.sub(r"^---\n", f"---\nstream: {stream}\n", content, count=1)


def production_write_kind(project: str, ticket_id: str, meta: Dict) -> str:
    """write-design | hitl-design | write-arch | hitl-arch."""
    if str(meta.get("design_status") or "") == "pending":
        from design_ticket_helpers import design_deliverables_status

        path = None
        for p in queue_ticket_paths(project):
            if read_ticket_meta(p).get("id") == ticket_id or p.name.startswith(f"{ticket_id}-"):
                path = p
                break
        blob = path.read_text(encoding="utf-8") if path else ""
        st, _ = design_deliverables_status(PROJECTS_DIR / project, ticket_id, blob)
        if st == "write":
            return "write-design"
        if st == "approve":
            return "hitl-design"
    if str(meta.get("architecture_status") or "") == "pending":
        if architecture_packet_ready(project, ticket_id):
            return "hitl-arch"
        return "write-arch"
    return "write-design"
