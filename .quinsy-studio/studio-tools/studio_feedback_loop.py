#!/usr/bin/env python3
"""Execute owns feedback after capture: drain notes → FB → clarify → backlog ticket."""

from __future__ import annotations

import re
from typing import Dict, List, Optional, Tuple

from design_ticket_helpers import (
    default_design_spec_path,
    enrich_design_skills,
    infer_ticket_type,
    requires_design_approval,
    write_design_spec_stub,
)
from skill_matcher import match_skills, staff_skills, team_for_skills
from sprint_hitl import (
    FEEDBACK_CLARIFYING,
    FEEDBACK_RAW,
    FEEDBACK_READY,
    FEEDBACK_SEVERITIES,
    add_feedback,
    clarify_feedback,
    find_feedback,
    get_ready_feedback_for_ticket,
    link_feedback_to_ticket,
    load_feedback_queue,
    update_feedback,
)
from studio_human_inbox import classify_note, drain_open_notes
from ticket_helpers import (
    apply_i18n_ticket_rules,
    render_staffing_section,
    render_ticket_markdown,
)
from ticket_ids import allocate_ticket_id
from backlog_paths import ensure_backlog_layout

MAX_QUESTION_ROUNDS = 2
DESIGN_REASON_CODES = (
    "hierarchy",
    "density",
    "motion",
    "copy",
    "flow",
    "uniqueness",
    "a11y",
    "brand",
)
CHROME_RE = re.compile(
    r"\b(auth|header|nav|tabs?|sign[- ]?out|masthead|shell|chrome)\b",
    re.I,
)
SURFACE_RE = re.compile(
    r"(/[a-z0-9_/-]+|\b(screen|page|route|dialog|modal|button|list|empty state|menu)\b)",
    re.I,
)
EMPTY_ANSWER_RE = re.compile(
    r"(?i)^\s*(approved|looks good|lgtm|ok|okay|shipped looks good)\s*[.!]?\s*$"
)
THEME_LINE_RE = re.compile(r"^\s*(?:[-*]|\d+[.)])\s+\S")


def split_themes(text: str) -> List[str]:
    """One FB per bullet/theme. A single paragraph stays one item."""
    raw = (text or "").strip()
    if not raw:
        return []
    lines = [ln.rstrip() for ln in raw.splitlines() if ln.strip()]
    bullets = [THEME_LINE_RE.sub("", ln).strip() for ln in lines if THEME_LINE_RE.match(ln)]
    if len(bullets) >= 2:
        return bullets
    return [raw]


def _looks_design(text: str) -> bool:
    return classify_note(text) == "design"


def _infer_severity(text: str) -> str:
    t = (text or "").lower()
    if any(w in t for w in ("blocker", "broken", "can't", "cannot", "won't load", "crash")):
        return "blocker"
    if any(w in t for w in ("wrong", "bug", "fails", "error", "major")):
        return "major"
    if any(w in t for w in ("polish", "nit", "tweak", "nice to")):
        return "polish"
    return "minor"


def _slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")
    return (slug or "feedback")[:50]


def draft_is_executable(item: Dict) -> bool:
    title = (item.get("draft_title") or "").strip()
    scope = (item.get("draft_scope") or "").strip()
    ac = [a for a in (item.get("draft_acceptance") or []) if str(a).strip()]
    severity = (item.get("severity") or "").strip().lower()
    questions = [q for q in (item.get("open_questions") or []) if str(q).strip()]
    if questions:
        return False
    if not title or not scope or len(ac) < 2:
        return False
    if severity not in FEEDBACK_SEVERITIES:
        return False
    return True


def _needs_human_fact(raw: str) -> bool:
    text = (raw or "").strip()
    if len(text) < 48:
        return True
    if not SURFACE_RE.search(text):
        return True
    return False


def _one_question(item: Dict) -> str:
    raw = (item.get("raw") or "").strip()
    if _looks_design(raw) and not item.get("design_reason"):
        codes = "|".join(DESIGN_REASON_CODES)
        return (
            f"Which surface should change, and which design reason ({codes}) "
            "plus what should look different?"
        )
    return "Which surface (route or control) and what should happen instead of today?"


def draft_from_raw(item: Dict) -> Dict:
    """Fill title/scope/AC/severity from the verbatim raw line. One question if facts are missing."""
    raw = (item.get("raw") or "").strip()
    title = (item.get("draft_title") or "").strip() or raw.split("\n")[0][:80].rstrip(" .")
    scope = (item.get("draft_scope") or "").strip() or raw
    severity = (item.get("severity") or "").strip() or _infer_severity(raw)
    ac = [a for a in (item.get("draft_acceptance") or []) if str(a).strip()]
    if len(ac) < 2:
        ac = [
            f"Given the current product, when a user hits the named surface, then: {raw[:160]}",
            "Given the change is shipped, when QA walks the default flow, then the new behaviour is visible without a harness.",
        ]
    rounds = int(item.get("question_rounds") or 0)
    questions: List[str] = []
    if _needs_human_fact(raw) and rounds < MAX_QUESTION_ROUNDS:
        questions = [_one_question(item)]
    return {
        "draft_title": title,
        "draft_scope": scope,
        "draft_acceptance": ac[:8],
        "severity": severity if severity in FEEDBACK_SEVERITIES else "minor",
        "open_questions": questions,
        "question_rounds": rounds,
    }


def has_open_feedback_questions(project: str, sprint: str) -> bool:
    if not sprint:
        return False
    for item in load_feedback_queue(project, sprint):
        if item.get("status") in (FEEDBACK_RAW, FEEDBACK_CLARIFYING) and any(
            str(q).strip() for q in (item.get("open_questions") or [])
        ):
            return True
    return False


def feedback_queue_needs_work(project: str, sprint: str) -> bool:
    if not sprint:
        return False
    for item in load_feedback_queue(project, sprint):
        status = item.get("status")
        if status in (FEEDBACK_RAW, FEEDBACK_CLARIFYING, FEEDBACK_READY):
            return True
    return False


def promote_notes_to_feedback(project: str, sprint: str, notes: List[Dict]) -> List[str]:
    """Turn drained product notes into FB items. Abort and tech-veto are skipped."""
    created: List[str] = []
    if not sprint:
        return created
    for note in notes:
        text = (note.get("text") or "").strip()
        kind = classify_note(text)
        if kind in ("abort", "tech-veto"):
            continue
        source = "inbox-design" if kind == "design" else "inbox"
        for theme in split_themes(text):
            fb_id, _md, dup = add_feedback(project, sprint, theme, source=source, force=False)
            if not dup:
                created.append(fb_id)
                if kind == "design":
                    update_feedback(project, sprint, fb_id, {"design_kind": True})
    return created


def apply_answer(project: str, sprint: str, fb_id: str, answer: str) -> Dict:
    """Record one human reply. Empty 'looks good' does not close the question."""
    item = find_feedback(project, sprint, fb_id)
    if not item:
        raise ValueError(f"{fb_id} not found")
    text = (answer or "").strip()
    if not text or EMPTY_ANSWER_RE.match(text):
        return item
    rounds = int(item.get("question_rounds") or 0) + 1
    scope = (item.get("draft_scope") or item.get("raw") or "").strip()
    scope = f"{scope}\nHuman: {text}".strip()
    ac = list(item.get("draft_acceptance") or [])
    if text and text not in ac:
        ac.append(f"Given the named surface, when the user acts, then {text}")
    questions: List[str] = []
    if _needs_human_fact((item.get("raw") or "") + " " + text) and rounds < MAX_QUESTION_ROUNDS:
        questions = [_one_question(item)]
    severity = item.get("severity") or _infer_severity(text)
    for code in DESIGN_REASON_CODES:
        if re.search(rf"\b{code}\b", text, re.I):
            update_feedback(project, sprint, fb_id, {"design_reason": code})
            break
    item, _path = clarify_feedback(
        project,
        sprint,
        fb_id,
        title=item.get("draft_title") or "",
        scope=scope,
        acceptance=ac,
        questions=questions,
        severity=severity,
        verbatim=[text],
        approve=False,
    )
    assert item is not None
    item = update_feedback(project, sprint, fb_id, {"question_rounds": rounds}) or item
    if rounds >= MAX_QUESTION_ROUNDS and not draft_is_executable(item):
        assumptions = f"{scope}\nAssumptions after two questions: ship the verbatim request on the named or default surface."
        item, _path = clarify_feedback(
            project,
            sprint,
            fb_id,
            title=item.get("draft_title") or (item.get("raw") or "Feedback")[:80],
            scope=assumptions,
            acceptance=(item.get("draft_acceptance") or [])[:8] or [
                f"Ship: {(item.get('raw') or '')[:160]}",
                "Default-flow proof exists for the change.",
            ],
            questions=[],
            severity=item.get("severity") or "minor",
            approve=True,
        )
    elif draft_is_executable({**item, "open_questions": questions, "draft_scope": scope, "draft_acceptance": ac, "severity": severity}):
        item, _path = clarify_feedback(
            project,
            sprint,
            fb_id,
            title=item.get("draft_title") or "",
            scope=scope,
            acceptance=ac,
            questions=[],
            severity=severity,
            approve=True,
        )
    return item or {}


def create_ticket_from_ready_feedback(project: str, sprint: str, fb_id: str) -> str:
    """Write a backlog ticket with no sprint tag. Same shape as ./studio ticket --from-feedback."""
    from sprint_hitl import PROJECTS_DIR, SEVERITY_PRIORITY

    fb_item = get_ready_feedback_for_ticket(project, sprint, fb_id)
    title = (fb_item.get("draft_title") or fb_item.get("raw") or "Feedback").strip()
    ticket_id = allocate_ticket_id(project)
    ensure_backlog_layout(project)
    ticket_dir = PROJECTS_DIR / project / "backlog"
    ticket_dir.mkdir(parents=True, exist_ok=True)
    ticket_file = ticket_dir / f"{ticket_id}-{_slugify(title)}.md"
    infer_blob = "\n".join(
        [
            title,
            str(fb_item.get("draft_scope") or ""),
            str(fb_item.get("raw") or ""),
        ]
    )
    skills = match_skills(title)
    ticket_type = infer_ticket_type(infer_blob)
    if ticket_type.startswith("ui-") or ticket_type in (
        "marketing-page",
        "workflow-explainer",
        "ia-navigation",
        "ia-feature-placement",
    ):
        skills = enrich_design_skills(skills, ticket_type, infer_blob)
    design_status = "pending" if requires_design_approval(
        f"ticket_type: {ticket_type}\n{infer_blob}"
    ) or fb_item.get("design_kind") or classify_note(fb_item.get("raw") or "") == "design" else "n/a"
    staffing = staff_skills(
        title,
        "\n".join(["## Scope", infer_blob]),
        skills=skills,
        ticket_type=ticket_type,
        design_status=design_status,
    )
    skills = list(staffing["skills"])
    design_spec = default_design_spec_path(ticket_id) if design_status == "pending" else ""
    acceptance = fb_item.get("draft_acceptance") or [
        f"'{title}' is implemented",
        f"'{title}' has tests",
    ]
    severity = fb_item.get("severity") or ""
    priority = SEVERITY_PRIORITY.get(severity, "P1")
    quotes = fb_item.get("verbatim") or [fb_item.get("raw", "")]
    recurring = fb_item.get("recurring") or []
    rationale_extra = (
        f"\n\n## Source feedback\n"
        f"- **{fb_id.upper()}** · severity: {severity or 'unset'} · "
        f"recurring: {', '.join(recurring) if recurring else 'first time'}\n"
        + "".join(f"> {q}\n" for q in quotes if q)
    )
    ticket = {
        "id": ticket_id,
        "title": title,
        "type": ticket_type if ticket_type != "feature" else "feature",
        "status": "backlog",
        "phase": 4,
        "priority": priority,
        "estimate": "M",
        "team": team_for_skills(skills),
        "skills": skills,
        "ist_zustand": f"The feature '{title}' does not exist yet in `projects/{project}/`.",
        "soll_zustand": f"The feature '{title}' is implemented and usable.",
        "value": (fb_item.get("draft_scope") or "").strip() or f"'{title}' from feedback.",
        "out_of_scope": (fb_item.get("draft_out_of_scope") or "").strip(),
        "modification_files": [f"projects/{project}/"],
        "constraints": [
            "Do not install unnecessary external packages without an ADR",
            "Follow the anti-slop protocol (no clichés, no god functions)",
            "Load the assigned skill files (see `skills`)",
        ],
        "scenarios": [],
        "acceptance_criteria": acceptance,
        "definition_of_done": [
            "Feature works (BDD scenario green)",
            "Tests present and green",
            "Anti-slop audit: 0 violations",
            "QA gate green (`./studio gate <project> --level 5`)",
        ],
        "dependencies": [],
    }
    ticket = apply_i18n_ticket_rules(ticket, project)
    ticket["ticket_type"] = ticket_type
    ticket["design_status"] = design_status
    ticket["design_spec"] = design_spec
    from studio_streams import needs_architecture_from_blob

    needs_arch = needs_architecture_from_blob(ticket_type, title)
    ticket["needs_design"] = design_status == "pending"
    ticket["needs_architecture"] = needs_arch
    ticket["architecture_status"] = "pending" if needs_arch else "n/a"
    ticket["stream"] = "production" if design_status == "pending" or needs_arch else "ready"
    content = render_ticket_markdown(ticket)
    content += render_staffing_section(staffing)
    content += rationale_extra
    ticket_file.write_text(content, encoding="utf-8")
    if design_status == "pending":
        write_design_spec_stub(PROJECTS_DIR / project, ticket_id, design_spec)
    link_feedback_to_ticket(project, sprint, fb_id, ticket_id)
    return ticket_id


def format_clarify_hitl(project: str, items: List[Dict]) -> Tuple[str, str]:
    """CARD text: one question per FB, verbatim, do not implement."""
    lines = [
        "Do not implement. Answer each question (one per FB). Then ./studio execute.",
    ]
    commands = []
    for item in items:
        fb_id = item.get("id")
        raw = (item.get("raw") or "")[:200]
        q = next((str(x).strip() for x in (item.get("open_questions") or []) if str(x).strip()), "")
        if not q:
            continue
        lines.append(f"  {fb_id}: {q}")
        lines.append(f"    verbatim: {raw}")
        commands.append(f'./studio clarify {project} {fb_id} --answer "<reply>"')
    command = " && ".join(commands) if commands else f"./studio feedback-list {project}"
    return command, "\n".join(lines)


def process_feedback_queue(project: str, sprint: str) -> Dict:
    """Drain inbox into FB, draft, ticket ready items. Returns action hitl | ticketed | idle."""
    drained = drain_open_notes(project, sprint)
    promoted = promote_notes_to_feedback(project, sprint, drained)
    ticketed: List[str] = []
    hitl_items: List[Dict] = []
    if not sprint:
        return {
            "action": "idle",
            "promoted": promoted,
            "ticketed": ticketed,
            "questions": [],
            "drained": [n.get("id") for n in drained],
        }
    for item in list(load_feedback_queue(project, sprint)):
        status = item.get("status")
        if status == FEEDBACK_READY:
            tid = create_ticket_from_ready_feedback(project, sprint, item["id"])
            ticketed.append(f"{item['id']}→{tid}")
            continue
        if status not in (FEEDBACK_RAW, FEEDBACK_CLARIFYING):
            continue
        if item.get("open_questions"):
            hitl_items.append(item)
            continue
        draft = draft_from_raw(item)
        merged = {**item, **draft}
        if draft_is_executable(merged):
            clarify_feedback(
                project,
                sprint,
                item["id"],
                title=draft["draft_title"],
                scope=draft["draft_scope"],
                acceptance=draft["draft_acceptance"],
                questions=[],
                severity=draft["severity"],
                approve=True,
            )
            tid = create_ticket_from_ready_feedback(project, sprint, item["id"])
            ticketed.append(f"{item['id']}→{tid}")
        else:
            clarify_feedback(
                project,
                sprint,
                item["id"],
                title=draft["draft_title"],
                scope=draft["draft_scope"],
                acceptance=draft["draft_acceptance"],
                questions=draft["open_questions"],
                severity=draft["severity"],
                approve=False,
            )
            hitl_items.append({**merged, "id": item["id"]})
    if hitl_items:
        command, reason = format_clarify_hitl(project, hitl_items)
        return {
            "action": "hitl",
            "promoted": promoted,
            "ticketed": ticketed,
            "questions": hitl_items,
            "command": command,
            "reason": reason,
            "drained": [n.get("id") for n in drained],
        }
    if ticketed or promoted:
        return {
            "action": "ticketed",
            "promoted": promoted,
            "ticketed": ticketed,
            "questions": [],
            "drained": [n.get("id") for n in drained],
        }
    return {
        "action": "idle",
        "promoted": promoted,
        "ticketed": ticketed,
        "questions": [],
        "drained": [n.get("id") for n in drained],
    }
