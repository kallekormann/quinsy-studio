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

from backlog_paths import (
    QUEUE_STATUS,
    WORKFLOW_FOLDERS,
    all_ticket_locations,
    read_ticket_meta,
)

BACKLOG_STATUSES = [QUEUE_STATUS, *WORKFLOW_FOLDERS]

FEEDBACK_RAW = "raw"
FEEDBACK_CLARIFYING = "clarifying"
FEEDBACK_READY = "ready"
FEEDBACK_TICKETED = "ticketed"
FEEDBACK_REJECTED = "rejected"

REVIEW_PENDING = "pending"
REVIEW_APPROVED = "approved"
REVIEW_REJECTED = "rejected"

REUSE_PENDING = "pending"
REUSE_APPROVED = "approved"

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
    tickets: List[Dict] = []

    for path, folder_status in all_ticket_locations(project):
        meta = read_ticket_meta(path)
        if meta.get("sprint") != sprint:
            continue
        tickets.append({
            "id": meta.get("id", path.stem),
            "title": meta.get("title", path.stem),
            "status": folder_status,
            "priority": meta.get("priority", "?"),
            "file": str(path.relative_to(root)),
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
        by_status.get(s, 0) for s in ("implement",)
    )
    queued = by_status.get(QUEUE_STATUS, 0)
    return {
        "tickets": tickets,
        "total": total,
        "done": done,
        "open": queued + by_status.get("blocked", 0),
        "in_progress": in_progress,
        "by_status": by_status,
        "all_done": total > 0 and done == total,
    }


_SMOKE_KEYWORDS = re.compile(
    r"\b(fidelity|qa|motion|delight|palette|responsive|plugin|figma|oauth|cors|"
    r"watermark|paywall|upgrade|export|presentation|smoke)\b",
    re.IGNORECASE,
)


def _ticket_review_smoke_steps(project: str, ticket: Dict) -> List[str]:
    """LO-0023 / LO-0034: numbered smoke steps matching the ticket's real surface."""
    root = project_dir(project)
    path = root / ticket["file"]
    body = path.read_text(encoding="utf-8") if path.exists() else ""
    explicit = re.search(
        r"##\s*Review smoke\s*\n(.*?)(?=\n##\s|\Z)",
        body,
        re.IGNORECASE | re.DOTALL,
    )
    if explicit:
        steps = [
            line.strip()[2:].strip() if line.strip().startswith("- ") else line.strip()
            for line in explicit.group(1).splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]
        return [s for s in steps if s]

    blob = f"{ticket.get('title', '')}\n{body}"
    if not _SMOKE_KEYWORDS.search(blob):
        return []

    steps: List[str] = []
    title_l = (ticket.get("title") or "").lower()
    # LO-0034: do not treat "Figma Companion later / out of scope" as a plugin ticket.
    is_figma_plugin = bool(
        re.search(r"figma-plugin|packages/figma", body, re.I)
        or re.search(r"\bfigma plugin\b|\bplugin oauth\b|^figma\b", title_l)
        or (
            re.search(r"\b(oauth|cors)\b", title_l)
            and re.search(r"\b(figma|plugin)\b", title_l)
        )
    )
    if is_figma_plugin:
        steps.extend(
            [
                "Load plugin in Figma desktop from packages/figma-plugin (or ticket path).",
                "Click Login / primary CTA — OAuth opens; no CORS error on plugin-auth.",
                "Confirm boards (or equivalent) load after login.",
            ]
        )
    if re.search(r"export|paywall|upgrade|watermark|brand kit", title_l) or re.search(
        r"UpgradeModal|watermark|raster|ExportBoardDialog|Brand kit", body, re.I
    ):
        steps.extend(
            [
                "Open a board on the live app → Brand kit / Export.",
                "Confirm the primary kit surface opens (dialog or guide) without a peer Presentation header CTA if demoted.",
                "Exercise one kit action (Open guide, PDF, or file download).",
            ]
        )
    if re.search(r"\bpresentation\b", title_l) and not re.search(
        r"brand.?kit|hub|demote|peer", title_l
    ):
        steps.extend(
            [
                "Open presentation builder or share presentation on the live app.",
                "Confirm deck chrome / slides render; smoke order or transition if shipped.",
            ]
        )
    if not steps:
        steps.append(
            f"Exercise the shipped surface for {ticket['id']} end-to-end on the live app "
            f"(prefer board / webapp routes over Figma unless this is a plugin ticket)."
        )
    # de-dupe preserving order
    seen = set()
    out: List[str] = []
    for s in steps:
        if s not in seen:
            seen.add(s)
            out.append(s)
    return out


def build_per_ticket_smoke_section(project: str, tickets: List[Dict]) -> str:
    """Markdown section for review.md (LO-0023)."""
    blocks: List[str] = []
    for t in tickets:
        if t.get("status") != "done":
            continue
        steps = _ticket_review_smoke_steps(project, t)
        if not steps:
            continue
        lines = "\n".join(f"  {i}. {step}" for i, step in enumerate(steps, 1))
        blocks.append(f"- **{t['id']}** — {t['title']}\n{lines}")
    if not blocks:
        return ""
    return (
        "## Per-ticket smoke (human)\n\n"
        "Numbered steps for QA / motion / plugin / paywall tickets "
        "(LO-0023). Skip only if the ticket has no user-visible surface.\n\n"
        + "\n\n".join(blocks)
        + "\n"
    )


def get_sprint_hitl(status: Dict) -> Dict:
    return status.setdefault("sprint_hitl", {
        "review_status": None,
        "review_pending_since": None,
        "last_review_at": None,
        "last_review_notes": None,
        "scope_status": None,
        "scope_approved_at": None,
        "groom_status": None,
        "groom_validated_at": None,
        "groom_approved_at": None,
        "backlog_validation": None,
        "retro_status": None,
        "retro_completed_at": None,
        "reuse_status": None,
        "reuse_sprint": None,
        "reuse_pending_since": None,
        "reuse_approved_at": None,
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


def feedback_only_message(project: str) -> str:
    """Agent-facing message: sprint-review feedback is backlog-only until the next sprint."""
    return (
        f"Sprint review pending — product feedback must NOT be implemented in code now.\n"
        f"  1. ./studio feedback {project} \"...\"  (raw — not a ticket)\n"
        f"  2. ./studio clarify {project} FB-NNN ... --approve\n"
        f"  3. ./studio ticket {project} \"...\" --from-feedback FB-NNN\n"
        f"  4. ./studio review {project} --approve → reuse → retro → ./studio sprint {project}\n"
        f"  Work lands in the **next** sprint backlog — never mid-review."
    )


def looks_like_review_product_feedback(request: str) -> bool:
    """Heuristic: user is describing product polish/features during sprint review."""
    lower = request.lower()
    if "feedback" in lower:
        return True
    polish = {
        "animation", "confetti", "nicer", "juicier", "prettier", "better", "improve",
        "polish", "transform", "burst", "motion", "should", "needs", "could", "want",
        "wish", "instead", "more", "less", "fix", "change", "add", "remove",
    }
    tokens = set(re.findall(r"[a-z0-9]{3,}", lower))
    return bool(tokens & polish)


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
    if hitl.get("scope_status") != "approved":
        return False
    if hitl.get("groom_status") != "approved":
        return False
    summary = sprint_ticket_summary(project, sprint)
    return summary["total"] > 0 and not summary["all_done"]


def implement_blocked_reason(status: Dict, project: str) -> Optional[str]:
    """Return a user-facing message when ./studio move … implement must be blocked."""
    sprint = status.get("current_sprint") or "SPRINT-??"
    if needs_sprint_review(status):
        return (
            f"\n  ⏸  Sprint review pending for {sprint} — no project code changes.\n"
            f"    Product ideas: ./studio feedback {project} \"...\" (never implement mid-review)\n"
            f"    ./studio review {project} --approve when ready"
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
            f"    ./studio sprint {project}\n"
            f"    ./studio sprint {project} --approve-scope\n"
            f"    ./studio groom {project} --approve"
        )
    hitl = get_sprint_hitl(status)
    if hitl.get("scope_status") not in (None, "approved") and sprint:
        return (
            f"\n  ⏸  Sprint scope pending approval for {sprint}.\n"
            f"    Read sprints/{sprint}/scope-proposal.md\n"
            f"    ./studio sprint {project} --approve-scope"
        )
    if hitl.get("scope_status") != "approved" and sprint:
        summary = sprint_ticket_summary(project, sprint)
        if summary["total"] > 0 and not summary["all_done"]:
            return (
                f"\n  ⏸  Approve sprint scope before implementing.\n"
                f"    ./studio sprint {project} --approve-scope"
            )
    return None


def can_plan_next_sprint(project: str, status: Dict) -> Tuple[bool, str]:
    """
    Next sprint planning requires: current sprint finished, human review approved,
    reuse review approved, retro done.
    """
    from sprint_reuse_review import reuse_gate_message

    reuse_msg = reuse_gate_message(project, status)
    if reuse_msg:
        return False, reuse_msg
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
            f"Retrospective required for {sprint} before the next sprint: "
            f"./studio retro {project} (fill retro) → ./studio retro {project} --complete",
        )

    from studio_learning_gate import can_infuse_project_sprint

    infusion_ok, infusion_msg = can_infuse_project_sprint()
    if not infusion_ok:
        return False, infusion_msg

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
    smoke_section = build_per_ticket_smoke_section(project, summary["tickets"])
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
- **Live app only (post-implement):** `cd projects/{project} && npm run dev` — use the port printed in the terminal (often 3000/3002). Hard-refresh after a clean `.next` if assets 404.
- **LO-0026:** Board/page **500** with webpack `reading 'call'` (or all routes 404 while Next says Ready) → kill listeners on that port, `rm -rf .next`, restart `npm run dev`, hard-refresh `127.0.0.1:<port>` before treating as a product bug.
- Open shipped routes on that port (home / board / feature under review). Do **not** use `design/prototype` for sprint review after implementation — that folder is gate-2 mocks only.
- If the sprint ships a browser extension: build under `packages/extension` (or project path in the ticket), Load unpacked from **`dist/`**, then reload the tab before Toggle / hotkey. Do not run `npm run build` from `design/prototype`.
- If the sprint ships a **Figma plugin**: load from `packages/figma-plugin` (or ticket path) in Figma desktop and run Login / boards smoke (LO-0022).
- Board: `./studio board {project}`

{smoke_section}## Human review checklist
- [ ] I reviewed all **done** tickets above
- [ ] I ran **Per-ticket smoke** steps where listed
- [ ] The project state matches my expectations
- [ ] I captured new ideas via `./studio feedback {project} "..."` (not direct tickets)
- [ ] When satisfied: `./studio review {project} --approve`
- [ ] If not satisfied: `./studio review {project} --reject "..."`

> **Process:** During the sprint the agent implements autonomously. You are involved **here**, at sprint review — not ticket-by-ticket mid-sprint.

## After approval
1. **Reuse review (mandatory):** `./studio reuse {project}` → promote / LO ticket / `--record local` → `./studio reuse {project} --approve`
2. Clarify feedback: `./studio clarify {project} FB-001` (one item per theme — duplicates rejected)
3. Ticket from feedback: `./studio ticket {project} "..." --from-feedback FB-001` → **backlog** (no sprint tag)
4. Groom backlog: `./studio groom {project}` (reprioritize for next sprint)
5. Retro: `./studio retro {project}`
6. Next sprint: `./studio sprint {project}` pulls mature backlog tickets → `./studio groom {project} --approve`
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
    hitl["reuse_status"] = REUSE_PENDING
    hitl["reuse_sprint"] = sprint
    hitl["reuse_pending_since"] = datetime.now().isoformat()
    hitl["reuse_approved_at"] = None

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


def _feedback_tokens(text: str) -> set:
    stop = {
        "the", "and", "for", "with", "from", "that", "this", "needs", "need", "task",
        "sprint", "review", "when", "not", "just", "more", "like", "should", "have",
    }
    words = re.findall(r"[a-z0-9]{3,}", text.lower())
    return {w for w in words if w not in stop}


def _feedback_themes(tokens: set) -> set:
    themes: set = set()
    if tokens & {"confetti", "burst", "spark", "completion"}:
        themes.add("completion_fx")
    if tokens & {"animation", "motion", "transform", "transformation", "juicy"}:
        themes.add("motion")
    if tokens & {"task", "add", "remove", "create", "complete", "quick"}:
        themes.add("tasks")
    return themes


def find_similar_feedback(project: str, sprint: str, text: str, threshold: float = 0.32) -> Optional[Dict]:
    """Find active feedback item similar to new text (dedupe per sprint)."""
    new_tokens = _feedback_tokens(text)
    if not new_tokens:
        return None
    new_themes = _feedback_themes(new_tokens)
    best: Optional[Dict] = None
    best_score = 0.0
    for item in load_feedback_queue(project, sprint):
        if item.get("status") in (FEEDBACK_TICKETED, FEEDBACK_REJECTED):
            continue
        old_text = " ".join(
            filter(
                None,
                [
                    item.get("raw", ""),
                    item.get("draft_title") or "",
                    item.get("draft_scope") or "",
                ],
            ),
        )
        old_tokens = _feedback_tokens(old_text)
        if not old_tokens:
            continue
        union = new_tokens | old_tokens
        score = len(new_tokens & old_tokens) / max(len(union), 1)
        theme_overlap = new_themes & _feedback_themes(old_tokens)
        if len(theme_overlap) >= 2 and len(new_tokens & old_tokens) >= 3:
            score = max(score, 0.5)
        if score >= threshold and score > best_score:
            best_score = score
            best = item
    return best


def add_feedback(
    project: str,
    sprint: str,
    text: str,
    source: str = "sprint-review",
    force: bool = False,
) -> Tuple[str, Path, bool]:
    """
    Capture raw human feedback — does NOT create a ticket.
    Returns (fb_id, md_path, is_duplicate_existing).
    """
    if not force:
        existing = find_similar_feedback(project, sprint, text)
        if existing:
            fb_id = existing["id"]
            sprint_dir = sprint_directory(project, sprint)
            md_file = sprint_dir / f"{fb_id.lower()}-feedback.md"
            return fb_id, md_file, True

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
   (ticket lands in **backlog** — sprint assigned at `./studio sprint`)
""",
        encoding="utf-8",
    )
    return fb_id, md_file, False


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


RETRO_PLACEHOLDER_MARKERS = (
    "- ...",
    "## What went well?\n- ...",
    "## What went badly?\n- ...",
    "## What can we improve?\n- ...",
)


def retro_is_filled(retro_path: Path) -> Tuple[bool, List[str]]:
    """True when project retro has substantive went well / badly / improve content."""
    if not retro_path.exists():
        return False, ["Project retro file missing"]
    text = retro_path.read_text(encoding="utf-8", errors="ignore")
    issues: List[str] = []
    for section, label in (
        (r"## What went well\?\s*\n(.*?)(?=\n## |\Z)", "What went well"),
        (r"## What went badly\?\s*\n(.*?)(?=\n## |\Z)", "What went badly"),
        (r"## What can we improve\?\s*\n(.*?)(?=\n## |\Z)", "What can we improve"),
    ):
        match = re.search(section, text, re.DOTALL | re.I)
        if not match:
            issues.append(f"Missing section: {label}")
            continue
        body = match.group(1).strip()
        lines = [ln.strip() for ln in body.splitlines() if ln.strip()]
        substantive = [ln for ln in lines if ln not in ("- ...", "...") and not ln.endswith(": ...")]
        if not substantive:
            issues.append(f"Section empty or placeholder: {label}")
    return len(issues) == 0, issues


def complete_retro(project: str, sprint: str) -> Tuple[bool, str]:
    """Validate retro content; return (ok, message)."""
    retro_path = sprint_directory(project, sprint) / "retro.md"
    ok, issues = retro_is_filled(retro_path)
    if not ok:
        return False, "Retro incomplete:\n  - " + "\n  - ".join(issues)
    return True, str(retro_path)


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
