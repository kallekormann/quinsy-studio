#!/usr/bin/env python3
"""
Sprint backlog validation — align sprint tickets with blueprint, ADRs, and non-goals.

Run before implementing sprint work:
  python3 sprint_backlog_validate.py <project> [--sprint SPRINT-01]
"""

from __future__ import annotations

import re
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

STUDIO_ROOT = Path(__file__).parent.parent.parent
PROJECTS_DIR = STUDIO_ROOT / "projects"

AUTH_PATTERNS = re.compile(
    r"\b(auth|authentication|authorization|oauth|login|registration|session|rbac)\b",
    re.I,
)
SQL_MIGRATION_PATTERNS = re.compile(
    r"\b(sql|postgres|mysql|migration|schema\.md|database/migrations)\b",
    re.I,
)
DEXIE_PATTERNS = re.compile(r"\b(dexie|indexeddb|local-first)\b", re.I)


@dataclass
class Finding:
    severity: str  # error | warning | info
    ticket_id: Optional[str]
    code: str
    message: str
    suggestion: str = ""


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _parse_ticket_meta(path: Path) -> Dict:
    text = _read(path)
    meta: Dict = {"path": str(path), "body": text}
    for key in ("id", "title", "priority", "phase", "estimate", "sprint", "status"):
        m = re.search(rf"^{key}:\s*(.+)$", text, re.MULTILINE)
        if m:
            meta[key] = m.group(1).strip().strip("'\"")
    deps = re.search(r"^dependencies:\s*\[(.*?)\]", text, re.MULTILINE | re.DOTALL)
    if deps:
        meta["dependencies"] = [
            d.strip().strip("'\"") for d in deps.group(1).split(",") if d.strip()
        ]
    else:
        meta["dependencies"] = []
    return meta


def _collect_sprint_tickets(project_dir: Path, sprint: str) -> List[Dict]:
    tickets: List[Dict] = []
    backlog = project_dir / "backlog"
    if not backlog.exists():
        return tickets
    prefix_match = re.compile(r"^[A-Z]+-\d+")
    # Product backlog queue (backlog/*.md)
    for f in backlog.glob("*.md"):
        if not prefix_match.match(f.name):
            continue
        meta = _parse_ticket_meta(f)
        if meta.get("sprint") == sprint:
            meta["folder"] = "backlog"
            tickets.append(meta)
    for folder in ("implement", "done", "blocked", "open"):
        d = backlog / folder
        if not d.exists():
            continue
        for f in d.glob("*.md"):
            meta = _parse_ticket_meta(f)
            if meta.get("sprint") == sprint:
                meta["folder"] = "backlog" if folder == "open" else folder
                tickets.append(meta)
    return tickets


def _p0_boundary_text(project_dir: Path) -> str:
    parts = [
        _read(project_dir / "docs" / "architecture" / "BLUEPRINT.md"),
        _read(project_dir / "docs" / "definitions" / "08-non-goals.md"),
    ]
    return "\n".join(parts).lower()


def _storage_from_adrs(project_dir: Path) -> str:
    adr_dir = project_dir / "docs" / "adr"
    if not adr_dir.exists():
        return "unknown"
    text = "\n".join(_read(f) for f in adr_dir.glob("*.md"))
    if DEXIE_PATTERNS.search(text):
        return "dexie"
    if SQL_MIGRATION_PATTERNS.search(text):
        return "sql"
    return "unknown"


def _done_ticket_ids(project_dir: Path) -> set:
    done = set()
    done_dir = project_dir / "backlog" / "done"
    if not done_dir.exists():
        return done
    for f in done_dir.glob("*.md"):
        m = re.match(r"^([A-Z]+-\d+)", f.name)
        if m:
            done.add(m.group(1))
    return done


def validate_sprint_backlog(project: str, sprint: Optional[str] = None) -> Dict:
    project_dir = PROJECTS_DIR / project
    if not project_dir.exists():
        return {"error": f"Project not found: {project}", "findings": []}

    if not sprint:
        status_file = project_dir / "status.json"
        if status_file.exists():
            import json

            sprint = json.loads(status_file.read_text()).get("current_sprint")
        if not sprint:
            sprints = sorted((project_dir / "sprints").glob("SPRINT-*"))
            sprint = sprints[-1].name if sprints else "SPRINT-01"

    findings: List[Finding] = []
    tickets = _collect_sprint_tickets(project_dir, sprint)
    p0_text = _p0_boundary_text(project_dir)
    storage = _storage_from_adrs(project_dir)
    done_ids = _done_ticket_ids(project_dir)

    p0_no_auth = any(
        x in p0_text
        for x in (
            "no server",
            "no accounts",
            "no auth",
            "authentication | none",
            "p0 boundary:** no server",
        )
    )
    p0_local_first = "local-first" in p0_text or storage == "dexie"

    if not tickets:
        findings.append(
            Finding(
                "warning",
                None,
                "EMPTY_SPRINT",
                f"No tickets tagged with sprint: {sprint}",
                "Assign tickets in plan.md and add `sprint: {sprint}` to ticket frontmatter.",
            )
        )

    if len(tickets) > 6:
        findings.append(
            Finding(
                "warning",
                None,
                "CAPACITY",
                f"Sprint has {len(tickets)} tickets — likely over capacity for one iteration.",
                "Move deferrable tickets out via grooming; target 4–6 tickets per sprint.",
            )
        )

    titles_seen: Dict[str, str] = {}
    for t in tickets:
        tid = t.get("id", "?")
        title = t.get("title", "")
        body = t.get("body", "")
        hay = f"{title}\n{body}".lower()

        for dep in t.get("dependencies", []):
            if dep and dep not in done_ids:
                dep_in_sprint = any(x.get("id") == dep for x in tickets)
                if not dep_in_sprint and t.get("folder") in ("open", "implement"):
                    findings.append(
                        Finding(
                            "error",
                            tid,
                            "DEP_UNSATISFIED",
                            f"Depends on {dep} which is not done and not in active sprint work.",
                            f"Complete {dep} first or remove from this sprint.",
                        )
                    )

        if p0_no_auth and AUTH_PATTERNS.search(hay):
            findings.append(
                Finding(
                    "error",
                    tid,
                    "P0_AUTH_MISMATCH",
                    "Ticket implies auth, but blueprint P0 says no accounts / local-only.",
                    "Defer to Pro/P1 sprint or update blueprint + ADR with human gate approval.",
                )
            )

        if p0_local_first and storage == "dexie" and SQL_MIGRATION_PATTERNS.search(hay):
            if "dexie" not in hay and "indexeddb" not in hay:
                findings.append(
                    Finding(
                        "warning",
                        tid,
                        "STORAGE_MISMATCH",
                        "Ticket reads like SQL migrations; ADRs specify Dexie/IndexedDB for P0.",
                        "Reword ticket for Dexie schema + client repositories.",
                    )
                )

        norm_title = re.sub(r"[^a-z0-9]+", " ", title.lower()).strip()
        for keyword, label in (
            ("design system", "design-system"),
            ("color concept", "color-concept"),
            ("token", "tokens"),
        ):
            if keyword in norm_title:
                bucket = titles_seen.setdefault(label, tid)
                if bucket != tid:
                    findings.append(
                        Finding(
                            "warning",
                            tid,
                            "DUPLICATE_THEME",
                            f"Overlaps with {bucket} on {label} work.",
                            "Close or merge duplicate tickets; gate 2 may already cover design tokens.",
                        )
                    )

        if t.get("folder") == "done" and tid in {x.get("id") for x in tickets}:
            pass  # ok

        ticket_path = Path(t.get("path", ""))
        if ticket_path.exists():
            try:
                from sprint_planning import assess_ticket_maturity

                mature, questions, _ = assess_ticket_maturity(ticket_path)
                if not mature:
                    findings.append(
                        Finding(
                            "error",
                            tid,
                            "IMMATURE_TICKET",
                            "Ticket lacks mature acceptance criteria / scope for sprint work.",
                            "Ask human: "
                            + "; ".join(questions[:3])
                            + " Then update ticket or ./studio clarify on source feedback.",
                        )
                    )
            except ImportError:
                pass

    # Sprint goal sanity
    plan = _read(project_dir / "sprints" / sprint / "plan.md")
    if plan and "0001–0004" in plan and p0_no_auth:
        if any(AUTH_PATTERNS.search(t.get("title", "")) for t in tickets):
            findings.append(
                Finding(
                    "warning",
                    None,
                    "PLAN_GOAL_GENERIC",
                    "plan.md uses generic setup goal but sprint includes auth — goals should match grooming.",
                    "Edit sprints/{sprint}/plan.md with a concrete P0 MVP goal.",
                )
            )

    errors = sum(1 for f in findings if f.severity == "error")
    warnings = sum(1 for f in findings if f.severity == "warning")

    return {
        "project": project,
        "sprint": sprint,
        "validated_at": datetime.now().isoformat(),
        "ticket_count": len(tickets),
        "storage_stack": storage,
        "p0_local_only": p0_no_auth,
        "summary": {"errors": errors, "warnings": warnings, "ready": errors == 0},
        "findings": [asdict(f) for f in findings],
        "tickets": [
            {
                "id": t.get("id"),
                "title": t.get("title"),
                "folder": t.get("folder"),
                "priority": t.get("priority"),
            }
            for t in tickets
        ],
    }


def write_validation_report(project: str, result: Dict) -> Path:
    sprint = result["sprint"]
    out_dir = PROJECTS_DIR / project / "sprints" / sprint
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "backlog-validation.md"

    lines = [
        f"# Sprint Backlog Validation — {sprint}",
        "",
        f"**Validated:** {result.get('validated_at', '')[:19]}",
        f"**Tickets in sprint:** {result.get('ticket_count', 0)}",
        f"**P0 local-only (blueprint):** {result.get('p0_local_only')}",
        f"**Storage (ADRs):** {result.get('storage_stack')}",
        "",
        f"## Summary",
        "",
        f"- Errors: **{result['summary']['errors']}**",
        f"- Warnings: **{result['summary']['warnings']}**",
        f"- Ready to implement: **{'yes' if result['summary']['ready'] else 'no — fix errors first'}**",
        "",
    ]

    if result.get("findings"):
        lines.append("## Findings")
        lines.append("")
        lines.append("| Severity | Ticket | Code | Message | Suggestion |")
        lines.append("|----------|--------|------|---------|------------|")
        for f in result["findings"]:
            lines.append(
                f"| {f['severity']} | {f.get('ticket_id') or '—'} | {f['code']} | "
                f"{f['message']} | {f.get('suggestion', '')} |"
            )
        lines.append("")
    else:
        lines.append("No issues found.")
        lines.append("")

    lines.extend(
        [
            "## Human grooming checklist",
            "",
            "- [ ] Sprint goal in `plan.md` matches P0 blueprint",
            "- [ ] Out-of-scope tickets moved to backlog (or later sprint)",
            "- [ ] Dependencies ordered",
            "- [ ] Capacity realistic (≤6 tickets)",
            "- [ ] `./studio groom <project> --approve` after edits",
            "",
        ]
    )

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def format_validation_brief(result: Dict) -> str:
    if result.get("error"):
        return result["error"]
    s = result["summary"]
    lines = [
        f"  Tickets: {result.get('ticket_count', 0)} | "
        f"errors: {s['errors']} | warnings: {s['warnings']} | "
        f"ready: {'✅' if s['ready'] else '❌'}",
    ]
    for f in result.get("findings", [])[:8]:
        icon = "❌" if f["severity"] == "error" else "⚠️" if f["severity"] == "warning" else "ℹ️"
        tid = f.get("ticket_id") or "sprint"
        lines.append(f"  {icon} [{f['code']}] {tid}: {f['message']}")
    if len(result.get("findings", [])) > 8:
        lines.append(f"  … +{len(result['findings']) - 8} more (see backlog-validation.md)")
    return "\n".join(lines)
