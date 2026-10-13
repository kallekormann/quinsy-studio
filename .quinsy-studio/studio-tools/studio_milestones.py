#!/usr/bin/env python3
"""Milestone ownership: roadmap coverage, plan, review, approve.

The PM (PM-002) drafts `docs/phases/` for the whole product. This module makes the
tooling drive that policy:

- `coverage_issues` — which required areas have no home in the roadmap
  (`./studio approve <p> --milestones` refuses on any).
- `plan` — create and staff the tickets a milestone file lists.
- `review` — collect production and implementation state when every ticket of the
  active milestone is done, and write `docs/phases/M<n>-review.md`.
- `approve` — HITL. Marks the milestone done; `plan --next` activates the next one.

All files live in the product tree. HQ keeps only this code and the checklist.
"""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from backlog_paths import PROJECTS_DIR, STUDIO_ROOT, all_ticket_locations, read_ticket_meta

QUINSY_STUDIO = STUDIO_ROOT / ".quinsy-studio"

# (area id, label, required-when, roadmap keywords, PRD trigger keywords or None for always)
COVERAGE_AREAS: List[Tuple[str, str, str, Tuple[str, ...], Optional[Tuple[str, ...]]]] = [
    ("scaffold", "Scaffolding and repo shape", "always",
     ("scaffold", "boilerplate", "repo layout", "separation of concerns"), None),
    ("data", "Data model and database", "always",
     ("database", "schema", "migration", "postgres"), None),
    ("api", "API and services", "always",
     ("api", "service layer", "endpoint"), None),
    ("jobs", "Background jobs and workers", "prd",
     ("worker", "queue", "job", "outbox"),
     ("job", "email", "import", "export", "llm", "ai", "scheduled", "cron", "notification")),
    ("cache", "Cache and realtime", "prd",
     ("redis", "cache", "realtime", "websocket"),
     ("cache", "realtime", "real-time", "presence", "rate limit", "live")),
    ("auth", "Authentication and access", "always",
     ("auth", "login", "session", "access control", "roles"), None),
    ("security", "Security hardening", "always",
     ("security", "threat model", "hardening", "csp"), None),
    ("privacy", "Privacy and legal", "always",
     ("privacy", "dsgvo", "gdpr", "consent", "impressum"), None),
    ("performance", "Performance", "always",
     ("performance", "core web vitals", "budget", "caching"), None),
    ("shell", "Frontend boilerplate and app shell", "always",
     ("app shell", "layout", "routing", "frontend boilerplate"), None),
    ("ux", "UX flows and interaction", "always",
     ("user flow", "interaction", "usability", "onboarding"), None),
    ("motion", "Motion and delight", "always",
     ("motion", "animation", "transition", "aha", "delight"), None),
    ("billing", "Billing", "prd",
     ("billing", "payment", "subscription", "checkout"),
     ("price", "pricing", "plan", "subscription", "checkout", "invoice", "billing", "payment")),
    ("i18n", "Internationalisation", "prd",
     ("i18n", "localisation", "localization", "language"),
     ("languages", "german and english", "multilingual", "locale", "markets")),
    ("ops", "Operations and production", "always",
     ("ops", "deploy", "coolify", "backup", "incident", "readiness"), None),
    ("quality", "Testing and quality", "always",
     ("test", "e2e", "accessibility", "a11y", "qa"), None),
    ("positioning", "Positioning and messaging", "public",
     ("positioning", "message", "persona page", "storytelling"), None),
    ("seo", "SEO and AEO foundation", "public",
     ("seo", "aeo", "sitemap", "schema.org", "llms.txt"), None),
    ("growth", "Growth loops", "public",
     ("growth loop", "invite", "referral", "activation", "upsell"), None),
    ("content", "Content engine", "public",
     ("blog", "posts", "content engine", "editorial"), None),
    ("launch", "Launch", "public",
     ("launch", "waitlist", "lifecycle email", "community"), None),
]

PUBLIC_TRIGGERS = (
    "marketing site", "landing page", "landing", "signup", "sign up", "organic",
    "seo", "waitlist", "public website", "homepage", "saas",
)

MILESTONE_FILE_RE = re.compile(r"^M(\d+)[-_].*\.md$")
REVIEW_SUFFIX = "-review.md"
PLAN_TICKET_LINE = re.compile(r"^-\s+(?!\[)(?P<title>[^:\n][^\n]*?)(?:\s*::\s*(?P<scope>.+))?\s*$")

PM_CARD = {
    "id": "MILESTONE",
    "title": "Milestone ownership (PM)",
    "skills": ["PM-002", "PM-004", "PS-002"],
    "playbooks": [
        "knowledge-base/milestone-coverage-checklist.md",
        "process/milestone-planning.md",
        "process/human-in-the-loop.md",
        "process/learning-loop.md",
        "knowledge-base/backend_playbook.md",
        "knowledge-base/frontend_playbook.md",
        "knowledge-base/design_playbook.md",
    ],
}

PB_RE = re.compile(r"\bPB-\d{8}-\d{3}\b")


# ---------------------------------------------------------------- paths


def phases_dir(project: str) -> Path:
    return PROJECTS_DIR / project / "docs" / "phases"


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def prd_text(project: str) -> str:
    root = PROJECTS_DIR / project / "docs"
    parts = [_read(root / "intake" / "prd.md")]
    defs = root / "definitions"
    if defs.is_dir():
        parts.extend(_read(p) for p in sorted(defs.glob("*.md")))
    return "\n".join(parts).lower()


# ------------------------------------------------------------- roadmap


def milestone_files(project: str) -> List[Path]:
    folder = phases_dir(project)
    if not folder.is_dir():
        return []
    files = [
        p for p in folder.glob("M*.md")
        if MILESTONE_FILE_RE.match(p.name) and not p.name.endswith(REVIEW_SUFFIX)
        and not p.name.endswith("-plan.md")
    ]
    return sorted(files, key=lambda p: int(MILESTONE_FILE_RE.match(p.name).group(1)))


def milestone_id(path: Path) -> str:
    m = MILESTONE_FILE_RE.match(path.name)
    return f"M{m.group(1)}" if m else path.stem


def list_milestones(project: str) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for path in milestone_files(project):
        text = _read(path)
        title_match = re.search(r"^#\s+M\d+\s*[—-]\s*(.+)$", text, re.MULTILINE)
        status_match = re.search(r"^\*\*Status:\*\*\s*([a-z]+)", text, re.MULTILINE | re.IGNORECASE)
        rows.append({
            "id": milestone_id(path),
            "title": (title_match.group(1).strip() if title_match else path.stem),
            "status": (status_match.group(1).lower() if status_match else "planned"),
            "file": path,
        })
    return rows


def is_public_product(prd: str) -> bool:
    return any(k in prd for k in PUBLIC_TRIGGERS)


def required_areas(prd: str) -> List[Tuple[str, str]]:
    """(area id, label) rows the PRD requires."""
    public = is_public_product(prd)
    out: List[Tuple[str, str]] = []
    for area_id, label, when, _kw, triggers in COVERAGE_AREAS:
        if when == "always":
            out.append((area_id, label))
        elif when == "public" and public:
            out.append((area_id, label))
        elif when == "prd" and triggers and any(t in prd for t in triggers):
            out.append((area_id, label))
    return out


def coverage_issues(project: str) -> List[str]:
    """Required areas with no mention in any M*.md. Empty list means covered."""
    files = milestone_files(project)
    if not files:
        return ["no M<n>-*.md files in docs/phases/ — draft the roadmap from studio-templates/phases/milestone.md"]
    roadmap = "\n".join(_read(p) for p in files).lower()
    if "_tbd" in roadmap or "<version name>" in roadmap:
        return ["roadmap still carries template placeholders"]
    missing: List[str] = []
    for area_id, label in required_areas(prd_text(project)):
        keywords = next(kw for aid, _l, _w, kw, _t in COVERAGE_AREAS if aid == area_id)
        if not any(k in roadmap for k in keywords):
            missing.append(f"{label} ({area_id}) has no milestone — see knowledge-base/milestone-coverage-checklist.md")
    return missing


# ------------------------------------------------------------ status


def milestone_state(status: Dict[str, Any]) -> Dict[str, Any]:
    return status.setdefault("milestones", {})


def roadmap_approved(status: Dict[str, Any]) -> bool:
    hg = status.get("human_gates") or {}
    return (hg.get("milestones") or {}).get("status") == "approved"


def active_milestone(project: str, status: Dict[str, Any]) -> Optional[str]:
    state = status.get("milestones") or {}
    if state.get("active"):
        return state["active"]
    done = set(state.get("done") or [])
    for row in list_milestones(project):
        if row["id"] not in done:
            return row["id"]
    return None


def milestone_tickets(project: str, mid: str) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for path, folder_status in all_ticket_locations(project):
        meta = read_ticket_meta(path)
        if (meta.get("milestone") or "").strip() != mid:
            continue
        rows.append({
            "id": meta.get("id", path.stem),
            "title": meta.get("title", path.stem),
            "status": folder_status,
            "ticket_type": meta.get("ticket_type", ""),
            "path": path,
        })
    return sorted(rows, key=lambda r: r["id"])


def milestone_complete(project: str, mid: str) -> bool:
    rows = milestone_tickets(project, mid)
    return bool(rows) and all(r["status"] in ("done", "cancelled") for r in rows)


def review_path(project: str, mid: str) -> Path:
    return phases_dir(project) / f"{mid}{REVIEW_SUFFIX}"


def review_state(project: str, status: Dict[str, Any], mid: str) -> str:
    """missing | written | approved"""
    state = status.get("milestones") or {}
    if mid in (state.get("done") or []):
        return "approved"
    return "written" if review_path(project, mid).exists() else "missing"


def execute_signal(project: str, status: Dict[str, Any]) -> Dict[str, Any]:
    """What execute needs: roadmap approval, coverage, active milestone, completion, review."""
    mid = active_milestone(project, status)
    signal: Dict[str, Any] = {
        "roadmap_approved": roadmap_approved(status),
        "coverage_issues": coverage_issues(project) if not roadmap_approved(status) else [],
        "active": mid,
        "complete": bool(mid) and milestone_complete(project, mid),
        "review": review_state(project, status, mid) if mid else "missing",
        "has_tickets": bool(mid) and bool(milestone_tickets(project, mid)),
    }
    return signal


# -------------------------------------------------------------- plan


def planned_ticket_lines(text: str) -> List[Tuple[str, str]]:
    """`- title :: scope` lines under `## Tickets` that do not carry a ticket id yet."""
    section = text.split("## Tickets", 1)
    if len(section) < 2:
        return []
    body = section[1].split("\n## ", 1)[0]
    out: List[Tuple[str, str]] = []
    for line in body.splitlines():
        m = PLAN_TICKET_LINE.match(line.strip())
        if not m:
            continue
        title = m.group("title").strip()
        if not title or title.startswith("<") or re.match(r"^[A-Z]+-\d+\b", title):
            continue
        if title.lower().startswith("written by"):
            continue
        out.append((title, (m.group("scope") or "").strip()))
    return out


def replace_plan_line(text: str, title: str, ticket_id: str) -> str:
    pattern = re.compile(rf"^-\s+{re.escape(title)}(\s*::.*)?$", re.MULTILINE)
    return pattern.sub(f"- {ticket_id} — {title}", text, count=1)


def stamp_milestone(content: str, mid: str) -> str:
    if re.search(rf"^milestone:[ \t]*{re.escape(mid)}[ \t]*$", content, re.MULTILINE):
        return content
    if re.search(r"^milestone:[ \t]*.*$", content, re.MULTILINE):
        return re.sub(r"^milestone:[ \t]*.*$", f"milestone: {mid}", content, count=1, flags=re.MULTILINE)
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            fm = parts[1]
            if "created:" in fm:
                fm = fm.replace("created:", f"milestone: {mid}\ncreated:", 1)
            else:
                fm = fm.rstrip("\n") + f"\nmilestone: {mid}\n"
            return f"---{fm}---{parts[2]}"
    return content


def set_milestone_status(path: Path, new_status: str) -> None:
    text = _read(path)
    if re.search(r"^\*\*Status:\*\*", text, re.MULTILINE):
        text = re.sub(r"^\*\*Status:\*\*.*$", f"**Status:** {new_status}", text, count=1, flags=re.MULTILINE)
    else:
        text = text.rstrip("\n") + f"\n\n**Status:** {new_status}\n"
    path.write_text(text, encoding="utf-8")


def pm_card_lines(action: str) -> List[str]:
    from skill_matcher import skill_files_for

    lines = [f"  PM CARD — milestone {action}"]
    lines.append(f"    skills: {', '.join(PM_CARD['skills'])}")
    lines.append(f"    skill files: {', '.join(skill_files_for(PM_CARD['skills']))}")
    lines.append(f"    playbooks: {', '.join(PM_CARD['playbooks'])}")
    lines.append(
        "    READ the skill files and the playbooks before writing. Cite the PB-ids from those "
        "playbooks and skills in the review (## Catalog applied). LO- ids are local tickets, not proof."
    )
    return lines


# ------------------------------------------------------------ review


def _latest_sprint_dir(project: str) -> Optional[Path]:
    sprints = PROJECTS_DIR / project / "sprints"
    if not sprints.is_dir():
        return None
    rows = [p for p in sprints.glob("SPRINT-*") if p.is_dir()]
    if not rows:
        return None
    return sorted(rows, key=lambda p: int(re.search(r"(\d+)", p.name).group(1)))[-1]


def _reality_verdict(project: str) -> str:
    sprint_dir = _latest_sprint_dir(project)
    if not sprint_dir:
        return "no sprint yet"
    try:
        from reality_check import reality_state

        return reality_state(sprint_dir, PROJECTS_DIR / project)
    except Exception:
        return "unknown"


def _loop_metrics(project: str) -> Dict[str, Any]:
    sprint_dir = _latest_sprint_dir(project)
    if not sprint_dir:
        return {}
    log_path = sprint_dir / "execution-log.json"
    if not log_path.exists():
        return {}
    try:
        from retro_metrics import loop_metrics

        return loop_metrics(json.loads(log_path.read_text(encoding="utf-8")), sprint_dir)
    except Exception:
        return {}


def _open_feedback(project: str) -> List[Dict[str, Any]]:
    sprint_dir = _latest_sprint_dir(project)
    if not sprint_dir:
        return []
    try:
        from sprint_hitl import load_feedback_queue

        rows = load_feedback_queue(project, sprint_dir.name)
    except Exception:
        return []
    return [r for r in rows if r.get("status") not in ("ticketed", "dismissed", "done")]


def recommendations(
    tickets: List[Dict[str, Any]],
    reality: str,
    feedback: List[Dict[str, Any]],
    next_missing: List[str],
) -> List[str]:
    recs: List[str] = []
    blocked = [t for t in tickets if t["status"] == "blocked"]
    if blocked:
        recs.append(
            f"Re-iterate the architecture: {len(blocked)} ticket(s) ended blocked "
            f"({', '.join(t['id'] for t in blocked)}). Write an architecture ticket (PS-002) before the next milestone plan."
        )
    if reality in ("needs-work", "failed", "stale"):
        recs.append(f"Production state is `{reality}`: schedule the reality-check bug tickets first in the next milestone.")
    design_fb = [f for f in feedback if (f.get("design_reason") or f.get("source") == "design")]
    if design_fb or any(t.get("ticket_type", "").startswith(("ui-", "marketing", "workflow", "ia-")) and t["status"] == "blocked" for t in tickets):
        recs.append("Open the next cycle with a design phase: unresolved design feedback or blocked design-track work exists.")
    if feedback:
        recs.append(f"{len(feedback)} feedback item(s) are still raw or clarified without a ticket — clarify and ticket them into the next milestone or park them.")
    for line in next_missing:
        recs.append(f"Add or re-order a milestone: {line}")
    if not recs:
        recs.append("No change to the roadmap. Activate the next milestone with `plan --next`.")
    return recs


def write_review(project: str, status: Dict[str, Any], mid: str) -> Path:
    tickets = milestone_tickets(project, mid)
    reality = _reality_verdict(project)
    metrics = _loop_metrics(project)
    feedback = _open_feedback(project)
    next_missing = coverage_issues(project)
    recs = recommendations(tickets, reality, feedback, next_missing)
    ms = {r["id"]: r for r in list_milestones(project)}
    title = ms.get(mid, {}).get("title", mid)
    lines = [
        f"# {mid} review — {title}",
        "",
        f"> Written by `./studio milestone {project} review` on {datetime.now().strftime('%Y-%m-%d %H:%M')}. "
        "The human signs with `./studio milestone <project> --approve`.",
        "",
        "## State",
        "",
        f"- Tickets: {len(tickets)} ({sum(1 for t in tickets if t['status'] == 'done')} done, "
        f"{sum(1 for t in tickets if t['status'] == 'blocked')} blocked, "
        f"{sum(1 for t in tickets if t['status'] == 'cancelled')} cancelled)",
        f"- Production (reality-check on the latest sprint): `{reality}`",
    ]
    for key in ("first_pass_rate", "avg_retries", "qa_fails", "blocked"):
        if key in metrics:
            lines.append(f"- Loop metric {key}: {metrics[key]}")
    lines += ["", "## Tickets", "", "| Ticket | Title | Status |", "|---|---|---|"]
    lines += [f"| {t['id']} | {t['title']} | {t['status']} |" for t in tickets]
    lines += ["", "## Open feedback", ""]
    lines += [f"- {f.get('id')}: {str(f.get('raw') or f.get('clarified') or '')[:140]}" for f in feedback] or ["- none"]
    lines += ["", "## Recommendations", ""]
    lines += [f"- {r}" for r in recs]
    lines += [
        "",
        "## Roadmap changes",
        "",
        "_PM fills: sub-milestones added, milestones re-ordered, scope moved. Edit the `M<n>-*.md` files, then list the change here._",
        "",
        "## Catalog applied",
        "",
        "_PM fills: PB-ids from the playbooks, process files, and skills that shaped the recommendations, one line each. LO- ids do not count._",
        "",
        "## Decision for the human",
        "",
        f"- Approve {mid} as done and activate the next milestone, or send this review back with notes.",
        "",
    ]
    path = review_path(project, mid)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
    state = milestone_state(status)
    state["review"] = {"id": mid, "status": "written", "date": datetime.now().isoformat()}
    return path


def catalog_citations(text: str) -> List[str]:
    section = text.split("## Catalog applied", 1)
    if len(section) < 2:
        return []
    body = section[1].split("\n## ", 1)[0]
    return sorted(set(PB_RE.findall(body)))


def approve_review(project: str, status: Dict[str, Any], mid: str, notes: str = "") -> Tuple[bool, List[str]]:
    path = review_path(project, mid)
    if not path.exists():
        return False, [f"no {path.name} — run ./studio milestone {project} review first"]
    text = _read(path)
    messages: List[str] = []
    cites = catalog_citations(text)
    if not cites:
        messages.append("soft: ## Catalog applied cites no PB-id — the PM did not show which HQ learning shaped this review")
    else:
        messages.append(f"catalog citations: {', '.join(cites)}")
    state = milestone_state(status)
    done = list(state.get("done") or [])
    if mid not in done:
        done.append(mid)
    state["done"] = done
    state["review"] = {"id": mid, "status": "approved", "date": datetime.now().isoformat(), "notes": notes}
    state["active"] = None
    rows = {r["id"]: r for r in list_milestones(project)}
    if mid in rows:
        set_milestone_status(rows[mid]["file"], "done")
    if notes:
        path.write_text(text.rstrip("\n") + f"\n\n## Human notes\n\n{notes}\n", encoding="utf-8")
    return True, messages


def activate_next(project: str, status: Dict[str, Any]) -> Optional[str]:
    state = milestone_state(status)
    done = set(state.get("done") or [])
    for row in list_milestones(project):
        if row["id"] not in done:
            state["active"] = row["id"]
            set_milestone_status(row["file"], "active")
            return row["id"]
    return None


def checklist_path() -> Path:
    return QUINSY_STUDIO / "knowledge-base" / "milestone-coverage-checklist.md"
