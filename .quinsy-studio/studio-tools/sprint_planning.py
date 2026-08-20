#!/usr/bin/env python3
"""
Sprint planning: assign mature backlog tickets, defer immature ones with questions.
"""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

STUDIO_ROOT = Path(__file__).parent.parent.parent
PROJECTS_DIR = STUDIO_ROOT / "projects"

GENERIC_ACCEPTANCE = re.compile(
    r"^['\"].+['\"] is implemented$|^['\"].+['\"] has tests$",
    re.I,
)
PRIORITY_ORDER = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}


def _read_ticket(path: Path) -> Dict:
    text = path.read_text(encoding="utf-8")
    meta: Dict = {"path": path, "body": text, "file": path}
    for key in ("id", "title", "priority", "phase", "estimate", "sprint", "status"):
        match = re.search(rf"^{key}:\s*(.+)$", text, re.MULTILINE)
        if match:
            meta[key] = match.group(1).strip().strip("'\"")
    tid_match = re.match(r"^([A-Z]+-\d+)", path.name)
    if tid_match and "id" not in meta:
        meta["id"] = tid_match.group(1)
    return meta


def _extract_acceptance_criteria(body: str) -> List[str]:
    section = re.search(
        r"##\s*Acceptance Criteria.*?\n(.*?)(?:\n## |\Z)",
        body,
        re.DOTALL | re.I,
    )
    if not section:
        return []
    items: List[str] = []
    for line in section.group(1).splitlines():
        line = line.strip()
        if line.startswith("- "):
            items.append(line[2:].strip())
        elif re.match(r"^\d+\.\s+", line):
            items.append(re.sub(r"^\d+\.\s+", "", line).strip())
    return [item for item in items if item]


def assess_ticket_maturity(ticket_path: Path) -> Tuple[bool, List[str], Dict]:
    """Return (is_mature, open_questions, meta)."""
    meta = _read_ticket(ticket_path)
    questions: List[str] = []
    body = meta.get("body", "")
    acceptance = _extract_acceptance_criteria(body)
    from_feedback = "## Source feedback" in body

    if not meta.get("title"):
        questions.append("What is the ticket title?")

    specific = [a for a in acceptance if not GENERIC_ACCEPTANCE.match(a.strip())]
    if len(specific) < 2:
        questions.append(
            "Need at least 2 specific acceptance criteria (not generic 'is implemented' / 'has tests')."
        )

    if from_feedback and not re.search(r"\*\*Scope:\*\*", body):
        questions.append("Clarify scope from source feedback (run ./studio clarify … --scope).")

    if "phase:" not in body.lower():
        questions.append("Set ticket phase in frontmatter.")

    return len(questions) == 0, questions, meta


def list_open_backlog_tickets(project: str) -> List[Dict]:
    """Open tickets not yet assigned to a sprint."""
    open_dir = PROJECTS_DIR / project / "backlog" / "open"
    if not open_dir.exists():
        return []
    tickets: List[Dict] = []
    prefix = project[:4].upper()
    for path in sorted(open_dir.glob(f"{prefix}-*.md")):
        meta = _read_ticket(path)
        if meta.get("sprint"):
            continue
        meta["from_feedback"] = "## Source feedback" in meta.get("body", "")
        tickets.append(meta)
    return tickets


def _priority_rank(priority: str) -> int:
    return PRIORITY_ORDER.get((priority or "P1").upper(), 9)


def assign_backlog_to_sprint(
    project: str,
    sprint_name: str,
    max_tickets: int = 6,
) -> Dict:
    """
    Tag mature backlog tickets with sprint. Defer immature tickets with questions.
    Prioritize feedback-sourced tickets, then P0/P1.
    """
    candidates = list_open_backlog_tickets(project)
    candidates.sort(
        key=lambda t: (
            0 if t.get("from_feedback") else 1,
            _priority_rank(t.get("priority", "P1")),
            t.get("id", ""),
        ),
    )

    assigned: List[Dict] = []
    deferred_immature: List[Dict] = []
    deferred_capacity: List[Dict] = []
    planning_questions: List[Dict] = []

    for meta in candidates:
        path = meta["path"]
        mature, questions, _ = assess_ticket_maturity(path)
        tid = meta.get("id", path.stem)

        if not mature:
            deferred_immature.append(
                {
                    "id": tid,
                    "title": meta.get("title", path.stem),
                    "questions": questions,
                },
            )
            planning_questions.append({"id": tid, "title": meta.get("title", ""), "questions": questions})
            continue

        if len(assigned) >= max_tickets:
            deferred_capacity.append({"id": tid, "title": meta.get("title", path.stem)})
            continue

        content = path.read_text(encoding="utf-8")
        if "sprint:" not in content:
            content = content.replace("created:", f"sprint: {sprint_name}\ncreated:", 1)
            path.write_text(content)

        assigned.append(
            {
                "id": tid,
                "title": meta.get("title", path.stem),
                "phase": meta.get("phase", "?"),
                "priority": meta.get("priority", "P1"),
                "estimate": meta.get("estimate", "M"),
                "from_feedback": meta.get("from_feedback", False),
            },
        )

    return {
        "assigned": assigned,
        "deferred_immature": deferred_immature,
        "deferred_capacity": deferred_capacity,
        "planning_questions": planning_questions,
    }


def write_planning_questions_report(project: str, sprint: str, planning: Dict) -> Optional[Path]:
    questions = planning.get("planning_questions") or []
    if not questions:
        return None
    sprint_dir = PROJECTS_DIR / project / "sprints" / sprint
    sprint_dir.mkdir(parents=True, exist_ok=True)
    path = sprint_dir / "planning-questions.md"
    lines = [
        f"# Sprint Planning Questions — {sprint}",
        "",
        f"**Project:** {project}",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "These backlog tickets were **not** assigned — they need clarification before the sprint.",
        "The agent should ask the human, then update tickets or run `./studio clarify` on linked feedback.",
        "",
    ]
    for item in questions:
        lines.append(f"## {item['id']} — {item.get('title', '')}")
        for q in item.get("questions", []):
            lines.append(f"- [ ] {q}")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def format_planning_brief(planning: Dict) -> str:
    assigned = planning.get("assigned", [])
    immature = planning.get("deferred_immature", [])
    overflow = planning.get("deferred_capacity", [])
    lines = [
        f"  Assigned: {len(assigned)} ticket(s)",
        f"  Deferred (immature): {len(immature)}",
        f"  Deferred (capacity): {len(overflow)}",
    ]
    if immature:
        lines.append("  Immature backlog tickets (ask human before next sprint):")
        for t in immature[:6]:
            lines.append(f"    • {t['id']}: {t.get('title', '')[:50]}")
    if overflow:
        lines.append("  Backlog overflow (assign in a later sprint):")
        for t in overflow[:4]:
            lines.append(f"    • {t['id']}")
    return "\n".join(lines)
