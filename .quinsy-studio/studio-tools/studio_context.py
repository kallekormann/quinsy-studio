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
        looks_like_review_product_feedback,
        needs_sprint_review,
    )
except ImportError:
    needs_sprint_review = lambda status: False  # type: ignore
    is_sprint_closed = lambda status, project: False  # type: ignore
    is_autonomous_sprint_execution = lambda status, project: False  # type: ignore
    looks_like_review_product_feedback = lambda request: False  # type: ignore
    feedback_only_message = lambda project: "Sprint review pending."  # type: ignore

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
            lines.append("🤖 AUTONOMOUS SPRINT — agent implements all tickets; human joins at sprint review only")

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
            lines.append("Pre-implementation: follow gates 0→1→2 (see ./studio resume)")
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


def guard_request(project: str, request: str, status: Dict) -> Tuple[str, str]:
    """
    Classify a user request against project/sprint scope.
    Returns (verdict, message).
    verdict: in_scope | needs_ticket | pre_impl | sprint_review | sprint_closed | autonomous_sprint | feedback_only | studio_meta | unclear
    """
    req_tokens = _tokenize(request)
    if not req_tokens:
        return "unclear", "Could not parse request."

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

    hg = status.get("human_gates", {})
    if hg.get("2", {}).get("status") != "approved":
        if req_tokens & impl_signals:
            return "pre_impl", (
                f"Project is pre-gate-2 (phase {status.get('phase')}). "
                "Complete intake → architecture → design approvals before implementation."
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
                f"Sprint {status.get('current_sprint')} is in autonomous execution — "
                "agent finishes all sprint tickets without human checkpoints. "
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
        paths = [p for p in tracked.stdout.strip().splitlines() if p]
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

    return len(issues) == 0, issues


# Paths where project names are allowed (learning provenance, retros, manifest)
_ABSTRACTION_ALLOWLIST_PREFIXES = (
    "backlog/",
    "retros/",
    "studio-library/manifest.json",
    "process/studio-abstraction.md",
    "studio-tools/studio_context.py",
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

_ABSTRACTION_PATTERNS = (
    (re.compile(r"\bmoody\b", re.IGNORECASE), "project name 'moody'"),
    (re.compile(r"\bMOOD-\d+\b"), "project ticket id MOOD-*"),
    (re.compile(r"intake/amendments/moody"), "moody-specific intake path"),
)


def verify_studio_abstraction() -> Tuple[bool, List[str]]:
    """Flag project-specific references in studio HQ docs/tools/templates."""
    issues: List[str] = []
    studio_dir = QUINSY_STUDIO

    def _scan_file(path: Path) -> None:
        rel = path.relative_to(studio_dir).as_posix()
        if any(rel.startswith(prefix) for prefix in _ABSTRACTION_ALLOWLIST_PREFIXES):
            return
        if rel.endswith(".pyc") or "/__pycache__/" in rel:
            return
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            return
        for line_no, line in enumerate(text.splitlines(), 1):
            for pattern, label in _ABSTRACTION_PATTERNS:
                if pattern.search(line):
                    issues.append(f"{rel}:{line_no}: {label}")
                    break

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
