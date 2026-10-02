#!/usr/bin/env python3
"""
Studio context: active project focus, scope guard, two-worlds verification.
"""

from __future__ import annotations

import json
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    from sprint_hitl import (
        feedback_only_message,
        is_autonomous_sprint_execution,
        is_sprint_closed,
        list_sprint_tickets,
        looks_like_review_product_feedback,
        needs_sprint_review,
    )
except ImportError:
    needs_sprint_review = lambda status: False  # type: ignore
    is_sprint_closed = lambda status, project: False  # type: ignore
    is_autonomous_sprint_execution = lambda status, project: False  # type: ignore
    looks_like_review_product_feedback = lambda request: False  # type: ignore
    feedback_only_message = lambda project: "Sprint review pending."  # type: ignore
    list_sprint_tickets = lambda project, sprint: []  # type: ignore

STUDIO_ROOT = Path(__file__).parent.parent.parent
QUINSY_STUDIO = STUDIO_ROOT / ".quinsy-studio"
PROJECTS_DIR = STUDIO_ROOT / "projects"
ACTIVE_PROJECT_FILE = QUINSY_STUDIO / ".active-project.json"


def load_active_project() -> Optional[Dict]:
    if not ACTIVE_PROJECT_FILE.exists():
        return None
    try:
        return json.loads(ACTIVE_PROJECT_FILE.read_text())
    except json.JSONDecodeError:
        return None


def set_active_project(project: str, status: Dict) -> Dict:
    payload = {
        "project": project,
        "set_at": datetime.now().isoformat(),
        "phase": status.get("phase"),
        "gate": status.get("gate"),
        "gate_status": status.get("gate_status"),
        "current_sprint": status.get("current_sprint"),
        "active_ticket": status.get("active_ticket"),
        "design_scope": status.get("design_scope"),
    }
    ACTIVE_PROJECT_FILE.write_text(json.dumps(payload, indent=2))
    return payload


def _tokenize(text: str) -> set:
    words = re.findall(r"[a-z0-9]{3,}", text.lower())
    stop = {"the", "and", "for", "with", "from", "that", "this", "studio", "project"}
    return {w for w in words if w not in stop}


def _load_sprint_tickets(project: str, sprint: str) -> List[Dict]:
    root = PROJECTS_DIR / project
    tickets: List[Dict] = []
    prefix = project[:4].upper()

    for status_dir in root.glob("backlog/*"):
        if not status_dir.is_dir():
            continue
        for f in status_dir.glob(f"{prefix}-*.md"):
            text = f.read_text(encoding="utf-8", errors="ignore")
            sprint_match = re.search(r"^sprint:\s*(\S+)", text, re.MULTILINE)
            title_match = re.search(r"^title:\s*(.+)$", text, re.MULTILINE)
            tid_match = re.search(r"^id:\s*(\S+)", text, re.MULTILINE)
            if sprint_match and sprint_match.group(1) == sprint:
                tickets.append({
                    "id": tid_match.group(1) if tid_match else f.stem,
                    "title": title_match.group(1).strip() if title_match else f.stem,
                    "file": str(f.relative_to(root)),
                })
    return tickets


def _load_open_tickets(project: str) -> List[Dict]:
    from backlog_paths import queue_ticket_paths, read_ticket_meta

    tickets: List[Dict] = []
    for path in queue_ticket_paths(project):
        meta = read_ticket_meta(path)
        tickets.append({
            "id": meta.get("id", path.stem),
            "title": meta.get("title", path.stem),
        })
    # Legacy open/ folder
    open_dir = PROJECTS_DIR / project / "backlog" / "open"
    if open_dir.exists():
        prefix = project[:4].upper()
        for f in open_dir.glob(f"{prefix}-*.md"):
            meta = read_ticket_meta(f)
            tickets.append({
                "id": meta.get("id", f.stem),
                "title": meta.get("title", f.stem),
            })
    return tickets


def build_focus_report(project: str, status: Dict) -> str:
    lines = [
        f"ACTIVE PROJECT: {project}",
        f"Phase: {status.get('phase')} | Gate: {status.get('gate')} ({status.get('gate_status')})",
        f"Sprint: {status.get('current_sprint') or '-'} | Active ticket: {status.get('active_ticket') or '-'}",
        "",
        "Scope rules:",
        "  • Work only in projects/{p}/ unless improving .quinsy-studio/ (LO-* tickets)".format(p=project),
        "  • Sibling projects/ folders are opaque — never Read, copy, or git them into this repo",
        "  • No code without a backlog ticket (after gate 2)",
        "  • Off-sprint work → propose ticket or ./studio learn for studio improvements",
        "",
    ]

    sprint = status.get("current_sprint")
    if sprint:
        if needs_sprint_review(status):
            lines.append("⏸ SPRINT REVIEW — capture feedback only; agent must NOT implement product changes")
        elif is_sprint_closed(status, project):
            lines.append("⏸ SPRINT CLOSED — reuse review → retro → groom → ./studio sprint")
        elif is_autonomous_sprint_execution(status, project):
            lines.append(
                "🤖 AUTONOMOUS SPRINT — feature tickets loop without ACK; "
                "HITL on design-track approve-design, then sprint review"
            )

    if sprint:
        sprint_tickets = _load_sprint_tickets(project, sprint)
        lines.append(f"Current sprint ({sprint}) tickets:")
        if sprint_tickets:
            for t in sprint_tickets:
                lines.append(f"  - {t['id']}: {t['title']}")
        else:
            lines.append("  (none assigned — run ./studio sprint)")
    else:
        hg = status.get("human_gates", {})
        if hg.get("2", {}).get("status") != "approved":
            lines.append("Pre-implementation: follow gates 0→1→2a→2b (see ./studio resume)")
        else:
            open_t = _load_open_tickets(project)
            lines.append("Open backlog (top 8):")
            for t in open_t[:8]:
                lines.append(f"  - {t['id']}: {t['title']}")

    lines.extend([
        "",
        "Sprint HITL: autonomous execution → human sprint review → reuse → retro → next sprint",
        "Drift recovery: ./studio resume {p}  |  ./studio focus {p}".format(p=project),
    ])
    return "\n".join(lines)


def named_hitl_waiting(status: Dict, project: str = "") -> bool:
    """True when execute would STOP for a named human gate (not a ticket ACK)."""
    from sprint_hitl import needs_sprint_review

    from pre_impl_workflow import design_system_approved

    hg = status.get("human_gates") or {}
    if not design_system_approved(status):
        return True
    if needs_sprint_review(status) and not status.get("active_ticket"):
        return True
    veto = status.get("tech_veto") or {}
    if veto.get("status") == "open" and veto.get("decision"):
        return True
    if project and not status.get("active_ticket"):
        sprint = status.get("current_sprint") or ""
        if sprint:
            from design_ticket_helpers import DESIGN_TRACK_TYPES

            try:
                tickets = list_sprint_tickets(project, sprint)
            except (OSError, TypeError, ValueError):
                tickets = []
            for ticket in tickets:
                if ticket.get("status") not in ("backlog", "open"):
                    continue
                tt = str(ticket.get("ticket_type") or "").strip()
                if tt not in DESIGN_TRACK_TYPES:
                    continue
                ds = str(ticket.get("design_status") or "pending").strip()
                if ds not in ("approved", "n/a"):
                    return True
    return False


def implementation_in_flight(project: str, status: Dict) -> bool:
    """True for any project while a ticket or pre-gate execute loop is still working.

    Does not call decide_next_action (that function enqueues train jobs).
    """
    if status.get("active_ticket"):
        return True
    sprint = status.get("current_sprint") or ""
    if sprint:
        try:
            tickets = list_sprint_tickets(project, sprint)
        except (OSError, TypeError, ValueError):
            tickets = []
        if any(t.get("status") == "implement" for t in tickets):
            return True
    from pre_impl_workflow import design_system_approved

    hg = status.get("human_gates") or {}
    if hg.get("0", {}).get("status") == "approved" and hg.get("1", {}).get("status") != "approved":
        return True
    if hg.get("1", {}).get("status") == "approved" and not design_system_approved(status):
        return True
    return False


def _ack_inbox(project: str, status: Dict, request: str, *, abort: bool) -> Tuple[str, str]:
    from studio_human_inbox import append_note

    sprint = status.get("current_sprint") or ""
    note = append_note(project, sprint, request)
    if abort:
        return (
            "abort",
            f"ACK queued {note['id']} (abort) — stop the current ticket. "
            f"./studio note {project} --drain then wait.",
        )
    return (
        "inbox_ack",
        f"ACK queued {note['id']} — current ACTION continues. "
        f"Do not implement this note. Resume: ./studio execute {project}. "
        f"Drain after MOVE_DONE: ./studio note {project} --drain",
    )


def guard_request(project: str, request: str, status: Dict) -> Tuple[str, str]:
    """
    Classify a user request against project/sprint scope.
    Returns (verdict, message).
    Core mid-execute rule (every project): if work is in flight, queue the
    verbatim chat as an inbox note and tell the agent to resume ACTION.
    verdict: inbox_ack | abort | cross_project | in_scope | needs_ticket | pre_impl | sprint_review |
             sprint_closed | autonomous_sprint | feedback_only | studio_meta | ideate | unclear
    """
    from studio_human_inbox import (
        ABORT_RE,
        SHORT_HITL_RE,
        is_studio_hq_request,
        should_queue_as_note,
    )

    req_tokens = _tokenize(request)
    if not req_tokens:
        return "unclear", "Could not parse request."

    in_flight = implementation_in_flight(project, status)
    hitl_live = named_hitl_waiting(status, project)
    if in_flight and ABORT_RE.match(request or ""):
        return _ack_inbox(project, status, request, abort=True)

    from studio_isolation import request_names_sibling

    sibling = request_names_sibling(request, project)
    if sibling:
        return (
            "cross_project",
            f"Request names sibling project '{sibling}'. Stay in projects/{project}/. "
            f"Do not Read, copy, or git '{sibling}' into this repo. "
            f"Switch with ./studio focus {sibling} in a separate session.",
        )

    from studio_human_inbox import is_ideate_request

    from studio_ideate import FEASIBILITY_BAR, HUMAN_STOPS, is_desk_continuation, session_is_open

    if is_ideate_request(request or "") or is_desk_continuation(request or "", session_is_open()):
        return (
            "ideate",
            "This is the ideation desk, not the product sprint. "
            "If the session is waiting for a brief, ask once and do not search. "
            "After a brief, run ./studio ideate through the case in this turn. Do not ask the human to continue between sections. "
            "Do not call execute. "
            + HUMAN_STOPS
            + " "
            + FEASIBILITY_BAR,
        )

    if is_studio_hq_request(request or ""):
        return "studio_meta", (
            "This looks like studio-meta work (.quinsy-studio/). "
            "Use LO-* backlog or ./studio learn — not the product sprint inbox."
        )

    if in_flight and SHORT_HITL_RE.match(request or "") and not hitl_live:
        return (
            "in_scope",
            "Ticket ACK is not required. Resume ./studio execute until HITL "
            "Ticket ACK is not required. Resume ./studio execute until HITL "
            "(sprint-review, or approve-design once the design-track spec and mocks exist). "
            "Do not wait for looks good.",
        )

    if in_flight and should_queue_as_note(request, named_hitl_waiting=hitl_live):
        return _ack_inbox(project, status, request, abort=False)

    impl_signals = {
        "implement", "build", "deploy", "feature", "code", "api", "database",
        "continue", "next", "wire", "add", "create", "fix", "refactor",
    }
    direction_signals = {
        "change", "direction", "instead", "pivot", "rethink", "pause", "stop",
        "should", "continue", "proceed", "approve",
    }

    studio_signals = {"studio", "quinsy", "backlog", "lo-", "skill", "process", "gate", "tooling"}
    if req_tokens & studio_signals and "projects" not in request.lower():
        if not any(p.name == project for p in [PROJECTS_DIR / project]):
            pass
        if len(req_tokens & studio_signals) >= 2:
            return "studio_meta", (
                "This looks like studio-meta work (.quinsy-studio/). "
                "Use LO-* backlog or ./studio learn — not project implementation."
            )

    from pre_impl_workflow import design_system_approved

    hg = status.get("human_gates", {})
    if not design_system_approved(status):
        if req_tokens & impl_signals:
            return "pre_impl", (
                f"Project is pre-gate-2b (phase {status.get('phase')}). "
                "Complete intake → architecture → 2a direction → 2b kit before implementation."
            )

    if needs_sprint_review(status):
        read_only = {
            "review", "feedback", "approve", "reject", "board", "resume", "focus",
            "status", "clarify", "retro", "groom", "list",
        }
        if req_tokens & impl_signals or looks_like_review_product_feedback(request):
            return "feedback_only", feedback_only_message(project)
        if not (req_tokens & read_only):
            return "feedback_only", feedback_only_message(project)
        if req_tokens & {"feedback"} or "feedback" in request.lower():
            return "feedback_only", feedback_only_message(project)
        if req_tokens & (impl_signals | direction_signals):
            return "sprint_review", (
                f"Sprint review pending — human tests shipped work before more implementation. "
                f"./studio review {project} → ./studio review {project} --approve. "
                "Product ideas: ./studio feedback (never implement mid-review)."
            )

    if is_sprint_closed(status, project):
        if req_tokens & impl_signals:
            return "sprint_closed", (
                f"Sprint closed (review approved). Complete reuse review, then plan next sprint: "
                f"./studio reuse {project} --approve → ./studio retro {project} → ./studio groom {project} → ./studio sprint {project}"
            )
        if req_tokens & direction_signals:
            return "sprint_closed", (
                f"Direction changes belong in sprint review or the next sprint plan — not mid-closure. "
                f"Use ./studio feedback {project} \"...\" then ./studio sprint {project} after retro."
            )

    if is_autonomous_sprint_execution(status, project):
        if req_tokens & direction_signals:
            return "autonomous_sprint", (
                f"Sprint {status.get('current_sprint')} is in autonomous execution for "
                "non-design tickets (stay on the design system; no ticket ACK). "
                "Design-track tickets: write spec+mocks first, then ./studio approve-design. "
                f"Direction changes wait for ./studio review {project} when the sprint is done."
            )

    sprint = status.get("current_sprint")
    candidates: List[Tuple[str, str]] = []
    if sprint:
        for t in _load_sprint_tickets(project, sprint):
            title_tokens = _tokenize(t["title"])
            overlap = len(req_tokens & title_tokens)
            if overlap >= 2 or (overlap >= 1 and len(req_tokens) <= 4):
                candidates.append((t["id"], t["title"]))

    for t in _load_open_tickets(project):
        title_tokens = _tokenize(t["title"])
        if len(req_tokens & title_tokens) >= 2:
            candidates.append((t["id"], t["title"]))

    if candidates:
        best = candidates[0]
        return "in_scope", f"Matches ticket {best[0]}: {best[1]}"

    if hg.get("2", {}).get("status") == "approved":
        placement_signals = {
            "share", "dialog", "menu", "presentation", "builder", "surface",
            "placement", "workflow", "move", "wrong", "dumping", "layout", "redesign",
        }
        if len(req_tokens & placement_signals) >= 2 and req_tokens & impl_signals:
            return "needs_ticket", (
                "Multi-surface UI work detected. Create a ticket with "
                "ticket_type ia-feature-placement or ui-composition and require "
                "§2 Context & placement in the design spec "
                "(knowledge-base/contextual-ia-playbook.md) before implement."
            )
        return "needs_ticket", (
            "No matching sprint/backlog ticket. For sprint-review ideas use: "
            f'./studio feedback {project} "<idea>" → ./studio clarify → ticket --from-feedback. '
            f'For scoped work: ./studio ticket {project} "<title>".'
        )

    return "in_scope", "Pre-implementation phase — align with ./studio resume next steps."


_INTAKE_EXAMPLE_RE = re.compile(
    r"^intake/amendments/[^/]+/amendment_[^/]+\.example\.md$"
)
_CLI_JUNK_PROJECT_RE = re.compile(r"^(LO-\d+|testproj)$")


def _is_allowed_tracked_intake(path: str) -> bool:
    """Committed generic amendment templates — not a worlds leak."""
    return bool(_INTAKE_EXAMPLE_RE.match(path.replace("\\", "/")))


def _looks_like_real_project(child: Path) -> bool:
    """Skip CLI accidents (--help) and unit-test leftovers (testproj, LO-0042)."""
    name = child.name
    if name.startswith("-") or name.startswith("."):
        return False
    if _CLI_JUNK_PROJECT_RE.match(name):
        return False
    return (child / "status.json").exists() or (child / ".git").exists()


def verify_worlds() -> Tuple[bool, List[str]]:
    """Ensure studio git and project git are separated."""
    issues: List[str] = []

    if not (STUDIO_ROOT / ".git").exists():
        issues.append("Studio root is not a git repo (expected for Quinsy Studio HQ)")
    else:
        tracked = subprocess.run(
            ["git", "ls-files", "projects/", "intake/"],
            cwd=str(STUDIO_ROOT),
            capture_output=True,
            text=True,
        )
        paths = [
            p
            for p in tracked.stdout.strip().splitlines()
            if p and not _is_allowed_tracked_intake(p)
        ]
        if paths:
            issues.append(
                "Studio git tracks project/intake paths (must be gitignored): "
                + ", ".join(paths[:5])
                + (" ..." if len(paths) > 5 else "")
            )

    if PROJECTS_DIR.exists():
        for child in sorted(PROJECTS_DIR.iterdir()):
            if not child.is_dir() or child.name.startswith("."):
                continue
            if not _looks_like_real_project(child):
                continue
            if not (child / ".git").exists():
                issues.append(f"Project '{child.name}' missing local .git — run ./studio init {child.name}")
            if (STUDIO_ROOT / "projects" / child.name).resolve() == child.resolve():
                nested = subprocess.run(
                    ["git", "-C", str(STUDIO_ROOT), "ls-files", f"projects/{child.name}"],
                    capture_output=True,
                    text=True,
                )
                if nested.stdout.strip():
                    issues.append(f"Studio index still tracks projects/{child.name}/")

    from studio_isolation import apply_project_isolation, project_git_isolation_issues

    active = load_active_project()
    name = (active or {}).get("project") if isinstance(active, dict) else None
    if name and (PROJECTS_DIR / name).is_dir():
        apply_project_isolation(name)
        issues.extend(project_git_isolation_issues(name))

    return len(issues) == 0, issues


# Paths where project names are allowed (learning provenance, retros, tests)
_ABSTRACTION_ALLOWLIST_PREFIXES = (
    "backlog/",
    "retros/",
    "studio-library/manifest.json",
    "process/studio-abstraction.md",
    "studio-tools/studio_context.py",
    "studio-tools/studio_portability.py",
    "studio-tools/test_",
    "knowledge-base/learnings/archive/",
    "CHANGELOG.md",
)

_ABSTRACTION_SCAN_ROOTS = (
    "process",
    "knowledge-base",
    "studio-tools",
    "studio-templates",
    "teams",
    "GETTING_STARTED.md",
    "README.md",
)

_ABSTRACTION_PATTERNS = ()  # replaced by list_project_names() in verify_studio_abstraction


def verify_studio_abstraction() -> Tuple[bool, List[str]]:
    """Flag project-specific references in studio HQ docs/tools/templates."""
    issues: List[str] = []
    studio_dir = QUINSY_STUDIO
    from studio_portability import find_product_nouns_in_hq_text, list_project_names

    names = list_project_names()

    def _scan_file(path: Path) -> None:
        rel = path.relative_to(studio_dir).as_posix()
        if any(rel.startswith(prefix) for prefix in _ABSTRACTION_ALLOWLIST_PREFIXES):
            return
        if path.name == "CHANGELOG.md":
            return
        if rel.endswith(".pyc") or "/__pycache__/" in rel:
            return
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            return
        for line_no, noun, snippet in find_product_nouns_in_hq_text(text, nouns=names):
            issues.append(f"{rel}:{line_no}: project folder {noun!r} ({snippet})")

    for root_name in _ABSTRACTION_SCAN_ROOTS:
        target = studio_dir / root_name
        if target.is_file():
            _scan_file(target)
        elif target.is_dir():
            for path in target.rglob("*"):
                if path.is_file() and path.suffix in {
                    ".md",
                    ".py",
                    ".json",
                    ".mdc",
                    ".ts",
                    ".tsx",
                }:
                    _scan_file(path)

    tmp_dir = studio_dir / "tmp"
    if tmp_dir.is_dir():
        for path in tmp_dir.iterdir():
            if path.is_file():
                issues.append(
                    f"tmp/{path.name}: project-specific script in studio HQ — remove or move to project"
                )

    return len(issues) == 0, issues
