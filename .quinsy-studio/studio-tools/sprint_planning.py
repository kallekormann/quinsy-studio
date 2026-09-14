#!/usr/bin/env python3
"""
Sprint planning: propose scope from product backlog, human approves, then assign.
"""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from backlog_paths import (
    PROJECTS_DIR,
    list_unscheduled_backlog,
    read_ticket_meta,
    set_ticket_sprint,
)

GENERIC_ACCEPTANCE = re.compile(
    r"^['\"].+['\"] is implemented$|^['\"].+['\"] has tests$",
    re.I,
)
PRIORITY_ORDER = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}


def _extract_acceptance_criteria(body: str) -> List[str]:
    from studio_execute import extract_ac

    items = extract_ac(body)
    if items:
        return items
    section = re.search(
        r"##\s*(?:\d+\.\s*)?Acceptance Criteria.*?\n(.*?)(?:\n## |\Z)",
        body,
        re.DOTALL | re.I,
    )
    if not section:
        return []
    items = []
    for line in section.group(1).splitlines():
        line = line.strip()
        if line.startswith("- "):
            items.append(line[2:].strip())
        elif re.match(r"^\d+\.\s+", line):
            items.append(re.sub(r"^\d+\.\s+", "", line).strip())
    return [item for item in items if item]


def assess_ticket_maturity(ticket_path: Path) -> Tuple[bool, List[str], Dict]:
    """Return (is_mature, open_questions, meta)."""
    meta = read_ticket_meta(ticket_path)
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

    if from_feedback and not (
        re.search(r"\*\*Scope:\*\*", body) or re.search(r"^##\s*Scope\b", body, re.MULTILINE | re.I)
    ):
        questions.append("Clarify scope from source feedback (run ./studio clarify … --scope).")

    if not meta.get("phase"):
        questions.append("Set ticket phase in frontmatter (phase: N).")

    return len(questions) == 0, questions, meta


def _priority_rank(priority: str) -> int:
    return PRIORITY_ORDER.get((priority or "P1").upper(), 9)


def propose_sprint_scope(
    project: str,
    sprint_name: str,
    max_tickets: int = 6,
) -> Dict:
    """
    Assess backlog and build a scope proposal. Does NOT write sprint: tags yet.
  Human approves via ./studio sprint <p> --approve-scope.
    """
    candidates = list_unscheduled_backlog(project)
    candidates.sort(
        key=lambda t: (
            0 if t.get("from_feedback") else 1,
            _priority_rank(t.get("priority", "P1")),
            t.get("id", ""),
        ),
    )

    proposed: List[Dict] = []
    deferred_immature: List[Dict] = []
    deferred_capacity: List[Dict] = []
    planning_questions: List[Dict] = []

    for meta in candidates:
        path = meta["path"]
        mature, questions, _ = assess_ticket_maturity(path)
        tid = meta.get("id", path.stem)

        # Explicit deferral flags (e.g. AM-007 roadmap) — never auto-propose
        content_head = ""
        try:
            content_head = path.read_text(encoding="utf-8")[:800]
        except OSError:
            pass
        if re.search(r"^am007_deferred:\s*true\b", content_head, re.M | re.I) or re.search(
            r"^sprint_deferred:\s*true\b", content_head, re.M | re.I
        ):
            deferred_capacity.append(
                {
                    "id": tid,
                    "title": meta.get("title", path.stem),
                    "reason": "deferred flag (amendment/roadmap)",
                },
            )
            continue

        if not mature:
            deferred_immature.append(
                {
                    "id": tid,
                    "title": meta.get("title", path.stem),
                    "questions": questions,
                },
            )
            planning_questions.append(
                {"id": tid, "title": meta.get("title", ""), "questions": questions},
            )
            continue

        from studio_streams import ticket_is_ready

        if not ticket_is_ready(meta):
            q = "Ticket is on the production stream — design and/or architecture sign-off before implementation sprint."
            deferred_immature.append(
                {"id": tid, "title": meta.get("title", path.stem), "questions": [q]},
            )
            planning_questions.append({"id": tid, "title": meta.get("title", ""), "questions": [q]})
            continue

        if len(proposed) >= max_tickets:
            deferred_capacity.append({"id": tid, "title": meta.get("title", path.stem)})
            continue

        proposed.append(
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
        "sprint": sprint_name,
        "proposed": proposed,
        "deferred_immature": deferred_immature,
        "deferred_capacity": deferred_capacity,
        "planning_questions": planning_questions,
    }


def apply_sprint_scope(project: str, sprint_name: str, proposal: Dict) -> Tuple[int, List[str]]:
    """Tag proposed tickets with sprint: after human --approve-scope.

    Returns (tagged_count, missing_ids). tagged_count includes tickets already
    correctly tagged for this sprint. missing_ids are proposed IDs not found in
    the product backlog queue.
    """
    from backlog_paths import queue_ticket_paths

    count = 0
    missing: List[str] = []
    for item in proposal.get("proposed", []):
        tid = item["id"]
        found = False
        for file_path in queue_ticket_paths(project):
            meta = read_ticket_meta(file_path)
            if meta.get("id") != tid and not file_path.name.startswith(f"{tid}-"):
                continue
            content = file_path.read_text(encoding="utf-8")
            updated = set_ticket_sprint(content, sprint_name)
            if updated != content:
                file_path.write_text(updated, encoding="utf-8")
            count += 1
            found = True
            break
        if not found:
            missing.append(tid)
    return count, missing


def write_scope_proposal(project: str, sprint: str, proposal: Dict) -> Path:
    sprint_dir = PROJECTS_DIR / project / "sprints" / sprint
    sprint_dir.mkdir(parents=True, exist_ok=True)
    path = sprint_dir / "scope-proposal.md"
    proposed = proposal.get("proposed", [])
    immature = proposal.get("deferred_immature", [])
    overflow = proposal.get("deferred_capacity", [])

    lines = [
        f"# Sprint Scope Proposal — {sprint}",
        "",
        f"**Project:** {project}",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**Status:** pending human approval",
        "",
        "Human: review this list, then run:",
        f"`./studio sprint {project} --approve-scope`",
        "",
        "## Proposed for this sprint (mature)",
        "",
        "| Ticket | Title | Priority | Estimate |",
        "|--------|-------|----------|----------|",
    ]
    if proposed:
        for t in proposed:
            lines.append(
                f"| {t['id']} | {t.get('title', '')[:50]} | {t.get('priority', '?')} | {t.get('estimate', '?')} |",
            )
    else:
        lines.append("| (none) | — | — | — |")

    lines.extend(
        [
            "",
            "## Not ready — immature (stay in product backlog)",
            "",
            "These tickets need design/architecture/engineering input before they can enter a sprint.",
            "Update the ticket acceptance criteria, or run `./studio clarify` on linked feedback.",
            "",
        ],
    )
    if immature:
        for t in immature:
            lines.append(f"### {t['id']} — {t.get('title', '')}")
            for q in t.get("questions", []):
                lines.append(f"- [ ] {q}")
            lines.append(
                "- [ ] **Human decision:** defer / clarify / update blueprint",
            )
            lines.append("")
    else:
        lines.append("(none)")

    if overflow:
        lines.extend(["", "## Deferred — capacity (next sprint)", ""])
        for t in overflow:
            lines.append(f"- {t['id']}: {t.get('title', '')[:60]}")

    lines.extend(
        [
            "",
            "## Human checklist",
            "",
            "- [ ] Proposed tickets match sprint goal",
            "- [ ] Immature tickets have an owner action (defer vs clarify)",
            "- [ ] `./studio sprint {project} --approve-scope`",
            "- [ ] `./studio groom {project} --approve`",
            "",
        ],
    )
    path.write_text("\n".join(lines), encoding="utf-8")

    json_path = sprint_dir / "scope-proposal.json"
    json_path.write_text(json.dumps(proposal, indent=2), encoding="utf-8")
    return path


def load_scope_proposal(project: str, sprint: str) -> Optional[Dict]:
    json_path = PROJECTS_DIR / project / "sprints" / sprint / "scope-proposal.json"
    if not json_path.exists():
        return None
    return json.loads(json_path.read_text(encoding="utf-8"))


def write_planning_questions_report(project: str, sprint: str, proposal: Dict) -> Optional[Path]:
    questions = proposal.get("planning_questions") or []
    if not questions:
        return None
    sprint_dir = PROJECTS_DIR / project / "sprints" / sprint
    path = sprint_dir / "planning-questions.md"
    lines = [
        f"# Sprint Planning Questions — {sprint}",
        "",
        f"**Project:** {project}",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "These tickets stay in **product backlog** (`backlog/`) until mature.",
        "Owner (design / architecture / engineering) fills gaps, then re-run planning.",
        "",
    ]
    for item in questions:
        lines.append(f"## {item['id']} — {item.get('title', '')}")
        for q in item.get("questions", []):
            lines.append(f"- [ ] {q}")
        lines.append("- [ ] Human: defer to later sprint OR update ticket and re-plan")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def format_planning_brief(proposal: Dict) -> str:
    proposed = proposal.get("proposed", [])
    immature = proposal.get("deferred_immature", [])
    overflow = proposal.get("deferred_capacity", [])
    lines = [
        f"  Proposed (mature): {len(proposed)} ticket(s)",
        f"  Stay in backlog (immature): {len(immature)}",
        f"  Deferred (capacity): {len(overflow)}",
    ]
    if 0 < len(proposed) < 3:
        lines.append(
            "  ⚠️  Under capacity (<3) — add related mature backlog tickets before --approve-scope"
        )
    if proposed:
        lines.append("  Proposed for sprint:")
        for t in proposed[:8]:
            lines.append(f"    • {t['id']}: {t.get('title', '')[:50]}")
    if immature:
        lines.append("  Immature — need clarification before any sprint:")
        for t in immature[:6]:
            lines.append(f"    • {t['id']}: {t.get('title', '')[:50]}")
    if overflow:
        lines.append("  Backlog overflow (assign in a later sprint):")
        for t in overflow[:4]:
            lines.append(f"    • {t['id']}")
    return "\n".join(lines)


# Backward-compatible alias used during transition
def assign_backlog_to_sprint(project: str, sprint_name: str, max_tickets: int = 6) -> Dict:
    proposal = propose_sprint_scope(project, sprint_name, max_tickets=max_tickets)
    tagged, missing = apply_sprint_scope(project, sprint_name, proposal)
    return {
        "assigned": proposal["proposed"],
        "tagged": tagged,
        "missing": missing,
        "deferred_immature": proposal["deferred_immature"],
        "deferred_capacity": proposal["deferred_capacity"],
        "planning_questions": proposal["planning_questions"],
    }


def list_open_backlog_tickets(project: str) -> List[Dict]:
    return list_unscheduled_backlog(project)
