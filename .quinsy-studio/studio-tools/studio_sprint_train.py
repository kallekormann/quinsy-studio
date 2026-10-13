#!/usr/bin/env python3
"""After gate 2b, project work is a train: design, then architecture, then implementation.

An empty phase is skipped. Implementation only takes tickets whose design and
architecture are already signed. One unsigned spec does not freeze its siblings.
"""

from __future__ import annotations

import re
from typing import Dict, List, Optional, Tuple

from backlog_paths import list_unscheduled_backlog

PHASES = ("design", "architecture", "implementation")
SIGNED = {"approved", "n/a", ""}
DELTA_NONE = re.compile(r"architecture\s+delta\s*:\s*none\b", re.I)
DELTA_TICKET = re.compile(r"architecture\s+delta\s*:\s*([A-Z][A-Z0-9]*-\d+)\b")


def cycle_of(status: Optional[Dict]) -> Dict:
    raw = (status or {}).get("cycle") or {}
    phase = str(raw.get("phase") or "design").strip().lower()
    if phase not in PHASES:
        phase = "design"
    try:
        n = int(raw.get("n") or 1)
    except (TypeError, ValueError):
        n = 1
    return {"n": max(1, n), "phase": phase}


def next_phase(phase: str) -> str:
    if phase not in PHASES:
        return "design"
    index = PHASES.index(phase)
    if index + 1 >= len(PHASES):
        return "design"
    return PHASES[index + 1]


def advance_cycle(cycle: Dict) -> Dict:
    phase = str(cycle.get("phase") or "design")
    n = int(cycle.get("n") or 1)
    if phase == "implementation":
        return {"n": n + 1, "phase": "design"}
    return {"n": n, "phase": next_phase(phase)}


def _field(meta: Dict, key: str) -> str:
    if meta.get(key):
        return str(meta.get(key)).strip()
    body = meta.get("body") or ""
    match = re.search(rf"^{key}:[ \t]*([^\n]*)", body, re.MULTILINE)
    if not match:
        return ""
    return match.group(1).strip().strip("'\"")


def _ticket_type(meta: Dict) -> str:
    return (_field(meta, "ticket_type") or _field(meta, "type")).lower()


def architecture_delta(body: str) -> Optional[str]:
    """'none', a ticket id, or None when the design ticket has not said."""
    if DELTA_NONE.search(body or ""):
        return "none"
    match = DELTA_TICKET.search(body or "")
    if match:
        return match.group(1)
    return None


def ticket_phase(meta: Dict) -> Optional[str]:
    """Which train phase an unscheduled ticket belongs to."""
    design = _field(meta, "design_status").lower()
    arch = _field(meta, "architecture_status").lower()
    returned = _field(meta, "cycle_return").lower()
    if returned == "design" or design == "pending":
        return "design"
    if arch == "pending":
        return "architecture"
    if design in SIGNED and arch in SIGNED:
        return "implementation"
    return None


def phase_candidates(project: str, phase: str) -> List[Dict]:
    rows = [meta for meta in list_unscheduled_backlog(project) if ticket_phase(meta) == phase]
    rows.sort(key=lambda meta: str(meta.get("id") or ""))
    return rows


def first_schedulable_phase(project: str, start: str) -> Tuple[Optional[str], List[str]]:
    """Walk forward from start. Skip a phase with zero tickets. Do not wrap past implementation."""
    phase = start if start in PHASES else "design"
    skipped: List[str] = []
    for _ in PHASES:
        if phase_candidates(project, phase):
            return phase, skipped
        skipped.append(phase)
        if phase == "implementation":
            break
        phase = next_phase(phase)
    return None, skipped


def implementation_blocked(meta: Dict) -> bool:
    """True when this ticket must not be built in an implementation sprint."""
    design = _field(meta, "design_status").lower()
    arch = _field(meta, "architecture_status").lower()
    if _field(meta, "cycle_return").lower() == "design":
        return True
    if design == "pending" or arch == "pending":
        return True
    return False


def _ticket_body(ticket: Dict) -> str:
    from pathlib import Path

    path = ticket.get("path")
    if path:
        try:
            return Path(path).read_text(encoding="utf-8", errors="ignore")
        except OSError:
            return ticket.get("body") or ""
    return ticket.get("body") or ""


def _project_root_for(ticket: Dict):
    from pathlib import Path

    path = ticket.get("path")
    if not path:
        return None
    for parent in Path(path).parents:
        if parent.name == "backlog":
            return parent.parent
    return None


def design_phase_action(tickets: List[Dict]) -> Dict:
    """What execute should do inside a design phase. mode: write | delta | sign | done."""
    from design_ticket_helpers import design_deliverables_status

    open_rows = [t for t in tickets if (t.get("status") or "backlog") in ("backlog", "open")]
    if not open_rows:
        return {"mode": "done", "ticket_id": "", "detail": ""}
    writers: List[str] = []
    deltas: List[str] = []
    signable: List[str] = []
    for ticket in open_rows:
        tid = str(ticket.get("id") or "")
        body = _ticket_body(ticket)
        if _field({"body": body}, "design_status").lower() == "approved":
            continue
        root = _project_root_for(ticket)
        if root is None:
            writers.append(tid)
            continue
        status, _message = design_deliverables_status(root, tid, body)
        if status == "write":
            writers.append(tid)
            continue
        if architecture_delta(body) is None:
            deltas.append(tid)
            continue
        if status == "approve":
            signable.append(tid)
    if writers:
        return {
            "mode": "write",
            "ticket_id": writers[0],
            "detail": f"Write the spec and all-state mocks for {writers[0]} before any signature.",
        }
    if deltas:
        return {
            "mode": "delta",
            "ticket_id": deltas[0],
            "detail": (
                f"{deltas[0]} needs `architecture delta: none` or `architecture delta: <TICKET>` "
                "before the design phase can be signed."
            ),
        }
    if signable:
        return {
            "mode": "sign",
            "ticket_id": signable[0],
            "detail": "Design packets are written. Sign the phase: " + ", ".join(signable),
        }
    return {"mode": "done", "ticket_id": "", "detail": ""}


def architecture_phase_action(project: str, tickets: List[Dict]) -> Dict:
    """mode: write | sign | done. A rejected ticket is already out of this phase."""
    from studio_streams import architecture_packet_issues

    open_rows = [t for t in tickets if (t.get("status") or "backlog") in ("backlog", "open")]
    if not open_rows:
        return {"mode": "done", "ticket_id": "", "detail": ""}
    writers: List[str] = []
    signable: List[str] = []
    gaps: Dict[str, List[str]] = {}
    for ticket in open_rows:
        tid = str(ticket.get("id") or "")
        body = _ticket_body(ticket)
        arch = _field({"body": body}, "architecture_status").lower()
        if arch in ("approved", "rejected", "n/a"):
            continue
        issues = architecture_packet_issues(project, tid)
        if issues:
            writers.append(tid)
            gaps[tid] = issues
        else:
            signable.append(tid)
    if writers:
        first = writers[0]
        return {
            "mode": "write",
            "ticket_id": first,
            "detail": f"Write docs/architecture/{first}.md before any architecture signature: " + "; ".join(gaps[first]),
        }
    if signable:
        return {
            "mode": "sign",
            "ticket_id": signable[0],
            "detail": "Architecture notes are written. Sign the phase: " + ", ".join(signable),
        }
    return {"mode": "done", "ticket_id": "", "detail": ""}


def mark_architecture_rejected(content: str, reason: str) -> str:
    """Send a feature back to the next design cycle. It is not implementation scope."""
    text = content
    if re.search(r"^design_status:", text, re.M):
        text = re.sub(r"^design_status:.*$", "design_status: pending", text, count=1, flags=re.M)
    else:
        text = re.sub(r"^---\n", "---\ndesign_status: pending\n", text, count=1)
    if re.search(r"^architecture_status:", text, re.M):
        text = re.sub(
            r"^architecture_status:.*$",
            "architecture_status: rejected",
            text,
            count=1,
            flags=re.M,
        )
    else:
        text = re.sub(r"^---\n", "---\narchitecture_status: rejected\n", text, count=1)
    if re.search(r"^cycle_return:", text, re.M):
        text = re.sub(r"^cycle_return:.*$", "cycle_return: design", text, count=1, flags=re.M)
    else:
        text = re.sub(r"^---\n", "---\ncycle_return: design\n", text, count=1)
    from backlog_paths import clear_ticket_sprint

    text = clear_ticket_sprint(text)
    note = (reason or "architecture cannot build the signed design").strip()
    text += f"\n\n## Architecture return\n- Sent back to the next design cycle: {note}\n"
    return text
