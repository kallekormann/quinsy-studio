#!/usr/bin/env python3
"""
Sprint human-in-the-loop: review, feedback, clarification, retrospective.

Raw feedback from sprint review never becomes a ticket directly —
it flows: raw → clarify → ready → ticket (via ./studio ticket --from-feedback).
"""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

STUDIO_ROOT = Path(__file__).parent.parent.parent
PROJECTS_DIR = STUDIO_ROOT / "projects"

BACKLOG_STATUSES = [
    "open", "plan", "analyze", "design", "implement",
    "qa", "review", "reuse", "blocked", "done",
]

FEEDBACK_RAW = "raw"
FEEDBACK_CLARIFYING = "clarifying"
FEEDBACK_READY = "ready"
FEEDBACK_TICKETED = "ticketed"
FEEDBACK_REJECTED = "rejected"

REVIEW_PENDING = "pending"
REVIEW_APPROVED = "approved"
REVIEW_REJECTED = "rejected"

RETRO_PENDING = "pending"
RETRO_DONE = "done"


def project_dir(project: str) -> Path:
    return PROJECTS_DIR / project


def ticket_prefix(project: str) -> str:
    return project[:4].upper()


def sprint_directory(project: str, sprint: str) -> Path:
    return project_dir(project) / "sprints" / sprint


def feedback_queue_path(project: str, sprint: str) -> Path:
    return sprint_directory(project, sprint) / "feedback-queue.json"


def load_feedback_queue(project: str, sprint: str) -> List[Dict]:
    path = feedback_queue_path(project, sprint)
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data.get("items", [])
    except json.JSONDecodeError:
        return []


def save_feedback_queue(project: str, sprint: str, items: List[Dict]) -> Path:
    sprint_directory(project, sprint).mkdir(parents=True, exist_ok=True)
    path = feedback_queue_path(project, sprint)
    path.write_text(
        json.dumps({"items": items, "updated": datetime.now().isoformat()}, indent=2),
        encoding="utf-8",
    )
    return path


def next_feedback_id(project: str, sprint: str) -> str:
    items = load_feedback_queue(project, sprint)
    if not items:
        return "FB-001"
    numbers = []
    for item in items:
        match = re.search(r"FB-(\d+)", item.get("id", ""))
        if match:
            numbers.append(int(match.group(1)))
    n = max(numbers, default=0) + 1
    return f"FB-{n:03d}"


def list_sprint_tickets(project: str, sprint: str) -> List[Dict]:
    """All backlog tickets tagged with this sprint, with current folder status."""
    root = project_dir(project)
    prefix = ticket_prefix(project)
    tickets: List[Dict] = []

    for status in BACKLOG_STATUSES:
        ticket_dir = root / "backlog" / status
        if not ticket_dir.exists():
            continue
        for f in ticket_dir.glob(f"{prefix}-*.md"):
            text = f.read_text(encoding="utf-8", errors="ignore")
            sprint_match = re.search(r"^sprint:\s*(\S+)", text, re.MULTILINE)
            if not sprint_match or sprint_match.group(1) != sprint:
                continue
            title_match = re.search(r"^title:\s*(.+)$", text, re.MULTILINE)
            tid_match = re.search(r"^id:\s*(\S+)", text, re.MULTILINE)
            prio_match = re.search(r"^priority:\s*(\S+)", text, re.MULTILINE)
            tickets.append({
                "id": tid_match.group(1) if tid_match else f.stem.split("-")[0] + "-" + f.stem.split("-")[1],
                "title": title_match.group(1).strip() if title_match else f.stem,
                "status": status,
                "priority": prio_match.group(1) if prio_match else "?",
                "file": str(f.relative_to(root)),
            })
    return sorted(tickets, key=lambda t: t["id"])


def sprint_ticket_summary(project: str, sprint: str) -> Dict:
    tickets = list_sprint_tickets(project, sprint)
    by_status: Dict[str, int] = {}
    for t in tickets:
        by_status[t["status"]] = by_status.get(t["status"], 0) + 1
    done = by_status.get("done", 0)
    total = len(tickets)
    in_progress = sum(
        by_status.get(s, 0) for s in ("implement", "qa", "review", "reuse", "design", "analyze", "plan")
    )
    return {
        "tickets": tickets,
        "total": total,
        "done": done,
        "open": by_status.get("open", 0) + by_status.get("blocked", 0),
        "in_progress": in_progress,
        "by_status": by_status,
        "all_done": total > 0 and done == total,
    }


def get_sprint_hitl(status: Dict) -> Dict:
    return status.setdefault("sprint_hitl", {
        "review_status": None,
        "review_pending_since": None,
        "last_review_at": None,
        "last_review_notes": None,
        "groom_status": None,
        "groom_validated_at": None,
        "groom_approved_at": None,
        "backlog_validation": None,
        "retro_status": None,
        "retro_completed_at": None,
    })


def maybe_flag_sprint_review(project: str, status: Dict) -> bool:
    """Set review_status=pending when all sprint tickets are done."""
    sprint = status.get("current_sprint")
    if not sprint:
        return False
    summary = sprint_ticket_summary(project, sprint)
    if not summary["all_done"]:
        return False
    hitl = get_sprint_hitl(status)
    if hitl.get("review_status") == REVIEW_APPROVED:
        return False
    hitl["review_status"] = REVIEW_PENDING
    hitl["review_pending_since"] = datetime.now().isoformat()
    return True


def needs_sprint_review(status: Dict) -> bool:
    hitl = status.get("sprint_hitl", {})
    return hitl.get("review_status") == REVIEW_PENDING


def is_sprint_closed(status: Dict, project: str) -> bool:
    """All sprint tickets done and human approved review — implementation frozen until next sprint."""
    sprint = status.get("current_sprint")
    if not sprint:
        return False
    summary = sprint_ticket_summary(project, sprint)
    if not summary["all_done"]:
        return False
    hitl = get_sprint_hitl(status)
    return hitl.get("review_status") == REVIEW_APPROVED


def is_autonomous_sprint_execution(status: Dict, project: str) -> bool:
    """
    Agent implements sprint tickets without human checkpoints until every sprint ticket is done.
    """
    sprint = status.get("current_sprint")
    if not sprint or needs_sprint_review(status) or is_sprint_closed(status, project):
        return False
    hitl = get_sprint_hitl(status)
    if hitl.get("groom_status") != "approved":
        return False
    summary = sprint_ticket_summary(project, sprint)
    return summary["total"] > 0 and not summary["all_done"]


def implement_blocked_reason(status: Dict, project: str) -> Optional[str]:
    """Return a user-facing message when ./studio move … implement must be blocked."""
    sprint = status.get("current_sprint") or "SPRINT-??"
    if needs_sprint_review(status):
        return (
            f"\n  ⏸  Sprint review pending for {sprint} — human tests shipped work before more code.\n"
            f"    ./studio review {project}\n"
            f"    ./studio review {project} --approve"
        )
    if is_sprint_closed(status, project):
        hitl = get_sprint_hitl(status)
        if hitl.get("retro_status") != RETRO_DONE:
            return (
                f"\n  ⏸  Sprint {sprint} is closed (review approved) — retrospective required.\n"
                f"    ./studio retro {project}"
            )
        return (
            f"\n  ⏸  Sprint {sprint} is closed — plan and groom the next sprint before implementing.\n"
            f"    ./studio groom {project}\n"
            f"    ./studio sprint {project}\n"
            f"    ./studio groom {project} --approve"
        )
    return None


def can_plan_next_sprint(project: str, status: Dict) -> Tuple[bool, str]:
    """
    Next sprint planning requires: current sprint finished, human review approved, retro done.
    """
    sprint = status.get("current_sprint")
    if not sprint:
        return True, ""

    summary = sprint_ticket_summary(project, sprint)
    if not summary["all_done"]:
        open_count = summary["total"] - summary["done"]
        return (
            False,
            f"{sprint} still has {open_count} ticket(s) not done "
            f"({summary['done']}/{summary['total']}). Finish the sprint before planning the next one.",
        )

    hitl = get_sprint_hitl(status)
    review = hitl.get("review_status")
    if review != REVIEW_APPROVED:
        if review == REVIEW_PENDING:
            return (
                False,
                f"Human sprint review pending for {sprint}. "
                f"Run ./studio review {project} → try shipped work → ./studio review {project} --approve",
            )
        if review == REVIEW_REJECTED:
            return (
                False,
                f"Sprint review rejected for {sprint}. Fix issues or re-open tickets, then re-approve review.",
            )
        return (
            False,
            f"Complete human sprint review for {sprint}: ./studio review {project} --approve",
        )

    if hitl.get("retro_status") != RETRO_DONE:
        return (
            False,
            f"Retrospective required for {sprint} before the next sprint: ./studio retro {project}",
        )

    return True, ""


def has_raw_feedback(project: str, sprint: str) -> bool:
    return any(
        item.get("status") in (FEEDBACK_RAW, FEEDBACK_CLARIFYING)
        for item in load_feedback_queue(project, sprint)
    )


def has_ready_feedback(project: str, sprint: str) -> bool:
    return any(
        item.get("status") == FEEDBACK_READY
        for item in load_feedback_queue(project, sprint)
    )


def prepare_review(project: str, sprint: str, status: Dict) -> Path:
    """Generate sprint review brief for the human."""
    sprint_dir = sprint_directory(project, sprint)
    sprint_dir.mkdir(parents=True, exist_ok=True)
    review_file = sprint_dir / "review.md"

    summary = sprint_ticket_summary(project, sprint)
    done_rows = "\n".join(
        f"- [x] **{t['id']}** — {t['title']} (`{t['status']}`)"
        for t in summary["tickets"] if t["status"] == "done"
    ) or "- (none yet)"
    not_done_rows = "\n".join(
        f"- [ ] **{t['id']}** — {t['title']} (`{t['status']}`)"
        for t in summary["tickets"] if t["status"] != "done"
    ) or "- (none)"

    feedback_items = load_feedback_queue(project, sprint)
    fb_section = ""
    if feedback_items:
        fb_lines = []
        for item in feedback_items:
            fb_lines.append(
                f"| {item['id']} | {item['status']} | {item.get('raw', '')[:60]}... |"
            )
        fb_section = f"""
## Feedback queue (not tickets yet)

| ID | Status | Summary |
|----|--------|---------|
{chr(10).join(fb_lines)}
"""

    rate = int(100 * summary["done"] / summary["total"]) if summary["total"] else 0
    content = f"""# Sprint Review — {sprint}

**Project:** {project}
**Prepared:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Review status:** {get_sprint_hitl(status).get('review_status') or 'not started'}

## Sprint goal
See [plan.md](plan.md)

## Shipped (done)
{done_rows}

## Not done / in progress
{not_done_rows}

## Metrics
| Metric | Value |
|--------|-------|
| Planned (sprint) | {summary['total']} |
| Completed | {summary['done']} |
| In progress | {summary['in_progress']} |
| Open / blocked | {summary['open']} |
| Completion rate | {rate}% |

## What to try (human)
- Run prototype: `cd projects/{project}/design/prototype && npm run dev`
- Check RUNBOOK: `projects/{project}/RUNBOOK.md`
- Board: `./studio board {project}`

## Human review checklist
- [ ] I reviewed all **done** tickets above
- [ ] The project state matches my expectations
- [ ] I captured new ideas via `./studio feedback {project} "..."` (not direct tickets)
- [ ] When satisfied: `./studio review {project} --approve`
- [ ] If not satisfied: `./studio review {project} --reject "..."`

> **Process:** During the sprint the agent implements autonomously. You are involved **here**, at sprint review — not ticket-by-ticket mid-sprint.

## After approval
1. Clarify feedback: `./studio clarify {project} FB-001` (repeat per item)
2. Ticket from feedback: `./studio ticket {project} "..." --from-feedback FB-001`
3. Groom backlog: `./studio groom {project}` (reprioritize for next sprint)
4. Retro: `./studio retro {project}`
5. Next sprint: `./studio sprint {project}` → `./studio groom {project} --approve` → implement
{fb_section}
"""
    review_file.write_text(content, encoding="utf-8")

    hitl = get_sprint_hitl(status)
    if summary["all_done"] and hitl.get("review_status") != REVIEW_APPROVED:
        hitl["review_status"] = REVIEW_PENDING
        hitl["review_pending_since"] = hitl.get("review_pending_since") or datetime.now().isoformat()

    return review_file


def approve_review(project: str, sprint: str, status: Dict, notes: str = "") -> None:
    hitl = get_sprint_hitl(status)
    hitl["review_status"] = REVIEW_APPROVED
    hitl["last_review_at"] = datetime.now().isoformat()
    hitl["last_review_notes"] = notes.strip() or None
    hitl["retro_status"] = RETRO_PENDING

    sprint_dir = sprint_directory(project, sprint)
    summary_file = sprint_dir / "summary.md"
    summary = sprint_ticket_summary(project, sprint)
    summary_file.write_text(
        f"""# Sprint Summary — {sprint}

**Approved:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Notes:** {notes.strip() or '(none)'}

## Completed
{chr(10).join(f"- {t['id']}: {t['title']}" for t in summary['tickets'] if t['status'] == 'done') or '- (none)'}

## Carried over
{chr(10).join(f"- {t['id']}: {t['title']} ({t['status']})" for t in summary['tickets'] if t['status'] != 'done') or '- (none)'}

## Metrics
- Completed: {summary['done']}/{summary['total']}
""",
        encoding="utf-8",
    )


def reject_review(project: str, sprint: str, status: Dict, reason: str) -> None:
    hitl = get_sprint_hitl(status)
    hitl["review_status"] = REVIEW_REJECTED
    hitl["last_review_at"] = datetime.now().isoformat()
    hitl["last_review_notes"] = reason.strip()

    review_file = sprint_directory(project, sprint) / "review.md"
    if review_file.exists():
        review_file.write_text(
            review_file.read_text(encoding="utf-8")
            + f"\n\n## Review rejected ({datetime.now().strftime('%Y-%m-%d')})\n{reason.strip()}\n",
            encoding="utf-8",
        )


def add_feedback(
    project: str,
    sprint: str,
    text: str,
    source: str = "sprint-review",
) -> Tuple[str, Path]:
    """Capture raw human feedback — does NOT create a ticket."""
    items = load_feedback_queue(project, sprint)
    fb_id = next_feedback_id(project, sprint)
    item = {
        "id": fb_id,
        "status": FEEDBACK_RAW,
        "source": source,
        "created": datetime.now().isoformat(),
        "raw": text.strip(),
        "clarification": None,
        "draft_title": None,
        "draft_scope": None,
        "draft_out_of_scope": None,
        "draft_acceptance": [],
        "open_questions": [],
        "linked_ticket": None,
    }
    items.append(item)
    save_feedback_queue(project, sprint, items)

    sprint_dir = sprint_directory(project, sprint)
    sprint_dir.mkdir(parents=True, exist_ok=True)
    md_file = sprint_dir / f"{fb_id.lower()}-feedback.md"
    md_file.write_text(
        f"""# {fb_id} — Feedback (raw)

**Status:** raw — not a ticket yet
**Source:** {source}
**Created:** {item['created']}

## Raw feedback (human)
{text.strip()}

## Next steps
1. Agent + human clarify: `./studio clarify {project} {fb_id} --title "..." --scope "..." --acceptance "..."`
2. Human approves draft: `./studio clarify {project} {fb_id} --approve`
3. Create ticket: `./studio ticket {project} "<title>" --from-feedback {fb_id}`
""",
        encoding="utf-8",
    )
    return fb_id, md_file


def find_feedback(project: str, sprint: str, fb_id: str) -> Optional[Dict]:
    fb_id = fb_id.upper()
    for item in load_feedback_queue(project, sprint):
        if item.get("id", "").upper() == fb_id:
            return item
    return None


def update_feedback(project: str, sprint: str, fb_id: str, updates: Dict) -> Optional[Dict]:
    items = load_feedback_queue(project, sprint)
    fb_id = fb_id.upper()
    for i, item in enumerate(items):
        if item.get("id", "").upper() == fb_id:
            items[i] = {**item, **updates, "updated": datetime.now().isoformat()}
            save_feedback_queue(project, sprint, items)
            return items[i]
    return None


def clarify_feedback(
    project: str,
    sprint: str,
    fb_id: str,
    title: str = "",
    scope: str = "",
    out_of_scope: str = "",
    acceptance: Optional[List[str]] = None,
    questions: Optional[List[str]] = None,
    approve: bool = False,
) -> Tuple[Optional[Dict], Path]:
    """Draft or approve clarification for raw feedback."""
    item = find_feedback(project, sprint, fb_id)
    if not item:
        return None, Path()

    if item.get("status") == FEEDBACK_TICKETED:
        raise ValueError(f"{fb_id} already linked to ticket {item.get('linked_ticket')}")

    updates: Dict = {"status": FEEDBACK_CLARIFYING}
    if title:
        updates["draft_title"] = title.strip()
    if scope:
        updates["draft_scope"] = scope.strip()
    if out_of_scope:
        updates["draft_out_of_scope"] = out_of_scope.strip()
    if acceptance:
        updates["draft_acceptance"] = acceptance
    if questions:
        updates["open_questions"] = questions

    merged = {**item, **updates}
    if approve:
        if not merged.get("draft_title"):
            raise ValueError(f"{fb_id}: draft_title required before --approve")
        if not merged.get("draft_acceptance"):
            raise ValueError(f"{fb_id}: at least one --acceptance required before --approve")
        updates["status"] = FEEDBACK_READY

    item = update_feedback(project, sprint, fb_id, updates)
    assert item is not None

    sprint_dir = sprint_directory(project, sprint)
    clarify_file = sprint_dir / f"{fb_id.lower()}-clarify.md"
    ac_lines = "\n".join(f"- [ ] {a}" for a in item.get("draft_acceptance", [])) or "- [ ] (define acceptance criteria)"
    q_lines = "\n".join(f"- {q}" for q in item.get("open_questions", [])) or "- (none)"

    clarify_file.write_text(
        f"""# {fb_id} — Clarification draft

**Status:** {item['status']}
**Raw feedback:** {item.get('raw', '')}

## Proposed ticket title
{item.get('draft_title') or '(set via --title)'}

## In scope
{item.get('draft_scope') or '(set via --scope)'}

## Out of scope
{item.get('draft_out_of_scope') or '(set via --out-of-scope)'}

## Acceptance criteria
{ac_lines}

## Open questions (resolve before --approve)
{q_lines}

## Commands
```bash
./studio clarify {project} {fb_id} --title "..." --scope "..." --acceptance "Criterion 1" --approve
./studio ticket {project} "<title>" --from-feedback {fb_id}
```
""",
        encoding="utf-8",
    )
    return item, clarify_file


def link_feedback_to_ticket(project: str, sprint: str, fb_id: str, ticket_id: str) -> bool:
    item = find_feedback(project, sprint, fb_id)
    if not item:
        return False
    if item.get("status") not in (FEEDBACK_READY,):
        raise ValueError(
            f"{fb_id} must be status 'ready' (run ./studio clarify {project} {fb_id} --approve first)"
        )
    update_feedback(project, sprint, fb_id, {
        "status": FEEDBACK_TICKETED,
        "linked_ticket": ticket_id,
    })
    return True


def get_ready_feedback_for_ticket(project: str, sprint: str, fb_id: str) -> Dict:
    item = find_feedback(project, sprint, fb_id)
    if not item:
        raise ValueError(f"Feedback {fb_id} not found in {sprint}")
    if item.get("status") != FEEDBACK_READY:
        raise ValueError(
            f"{fb_id} is '{item.get('status')}' — clarify and approve first: "
            f"./studio clarify {project} {fb_id} --approve"
        )
    return item


def prepare_retro(project: str, sprint: str) -> Path:
    """Create project sprint retro (not studio meta-retro)."""
    sprint_dir = sprint_directory(project, sprint)
    sprint_dir.mkdir(parents=True, exist_ok=True)
    retro_file = sprint_dir / "retro.md"

    summary = sprint_ticket_summary(project, sprint)
    feedback_items = load_feedback_queue(project, sprint)

    template = f"""# Retrospective — {sprint}

**Project:** {project}
**Date:** {datetime.now().strftime('%Y-%m-%d')}

## Sprint metrics
- Completed: {summary['done']}/{summary['total']} tickets
- Feedback items: {len(feedback_items)} ({sum(1 for i in feedback_items if i.get('status') == FEEDBACK_TICKETED)} ticketed)

## What went well?
- ...

## What went badly?
- ...

## What can we improve?
- ...

## Human feedback processed
| FB ID | Status | Linked ticket |
|-------|--------|---------------|
{chr(10).join(f"| {i['id']} | {i['status']} | {i.get('linked_ticket') or '-'} |" for i in feedback_items) or '| — | — | — |'}

## Action items
- [ ] ... (owner: human / agent)

## Studio learnings (if any)
```bash
./studio learn "..." --signal process-gap --source {project}
```
"""
    retro_file.write_text(template, encoding="utf-8")
    return retro_file


def format_feedback_list(project: str, sprint: str) -> str:
    items = load_feedback_queue(project, sprint)
    if not items:
        return "  (no feedback items — use ./studio feedback <project> \"...\")"
    lines = []
    for item in items:
        raw = item.get("raw", "")[:50]
        lines.append(
            f"  {item['id']} [{item['status']}] {raw}{'...' if len(item.get('raw', '')) > 50 else ''}"
        )
    return "\n".join(lines)
