#!/usr/bin/env python3
"""
Sprint reuse review — mandatory after sprint review approval.

Scans done sprint tickets for unpromoted registry-path changes and records
promote / LO-ticket / project-local decisions before retro or next sprint planning.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from library_manager import check_reuse_before_done
from sprint_hitl import (
    REVIEW_APPROVED,
    get_sprint_hitl,
    list_sprint_tickets,
    project_dir,
    sprint_directory,
)

REUSE_PENDING = "pending"
REUSE_APPROVED = "approved"

UI_PREFIX = "ui/components/"
PACKAGE_PREFIX = "packages/"


def reuse_review_json_path(project: str, sprint: str) -> Path:
    return sprint_directory(project, sprint) / "reuse-review.json"


def reuse_review_md_path(project: str, sprint: str) -> Path:
    return sprint_directory(project, sprint) / "reuse-review.md"


def load_reuse_review(project: str, sprint: str) -> Dict:
    path = reuse_review_json_path(project, sprint)
    if not path.exists():
        return {"status": None, "decisions": [], "items": []}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"status": None, "decisions": [], "items": []}


def save_reuse_review(project: str, sprint: str, data: Dict) -> Path:
    sprint_directory(project, sprint).mkdir(parents=True, exist_ok=True)
    path = reuse_review_json_path(project, sprint)
    data["updated"] = datetime.now().isoformat()
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return path


def _promoted_paths(project: str) -> set:
    log_file = project_dir(project) / "docs" / "library-promotions.json"
    promoted: set = set()
    if not log_file.exists():
        return promoted
    try:
        log = json.loads(log_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return promoted
    for entry in log.get("promotions", []):
        for path in entry.get("paths", []):
            promoted.add(path.rstrip("/"))
    return promoted


def classify_reuse_path(path: str) -> Dict[str, str]:
    if path.startswith(UI_PREFIX):
        return {
            "kind": "ui",
            "action": "lo_ticket",
            "hint": "Create LO-* studio ticket; edit .quinsy-studio/studio-library/ (project ui/ promote blocked)",
        }
    if path.startswith(PACKAGE_PREFIX):
        pkg = path.split("/")[1] if "/" in path else path
        return {
            "kind": "package",
            "action": "promote",
            "hint": f"./studio library promote <project> packages/{pkg} --ticket <ID> [--force]",
        }
    if path.startswith("ui/"):
        return {
            "kind": "ui-other",
            "action": "lo_ticket",
            "hint": "Studio-owned UI path — promote via studio-library LO ticket or record project-local",
        }
    if path.startswith("hooks/") or path.startswith("src/hooks/"):
        return {
            "kind": "hook",
            "action": "promote_or_local",
            "hint": "Promote generic hook to studio-library or record project-local",
        }
    return {
        "kind": "other",
        "action": "review",
        "hint": "Promote generic code, LO ticket, or record project-local with --record",
    }


def _path_covered(path: str, promoted: set, decisions: List[Dict]) -> bool:
    for pp in promoted:
        if path.startswith(pp) or pp in path:
            return True
    for decision in decisions:
        dp = decision.get("path", "").rstrip("/")
        if not dp:
            continue
        if path.startswith(dp) or dp in path:
            return True
    return False


def analyze_sprint_reuse(project: str, sprint: str, status: Dict) -> Dict:
    snapshots = status.get("ticket_file_snapshots", {})
    promoted = _promoted_paths(project)
    tickets = list_sprint_tickets(project, sprint)
    items: List[Dict] = []
    seen_paths: set = set()

    for ticket in tickets:
        if ticket["status"] != "done":
            continue
        ticket_id = ticket["id"]
        snap = snapshots.get(ticket_id, {})
        # LO-0036: empty snap = design-only / never implement — skip (else entire packages/)
        if not snap:
            continue
        _ok, warnings = check_reuse_before_done(project, ticket_id, snap)
        for path in warnings:
            if path in seen_paths:
                continue
            seen_paths.add(path)
            classification = classify_reuse_path(path)
            items.append({
                "path": path,
                "ticket_id": ticket_id,
                "covered": _path_covered(path, promoted, []),
                **classification,
            })

    return {
        "sprint": sprint,
        "project": project,
        "items": items,
        "ticket_count": len([t for t in tickets if t["status"] == "done"]),
        "unresolved_count": len(items),
    }


def apply_decisions_to_items(items: List[Dict], promoted: set, decisions: List[Dict]) -> List[Dict]:
    enriched = []
    for item in items:
        covered = _path_covered(item["path"], promoted, decisions)
        enriched.append({**item, "covered": covered})
    return enriched


def write_reuse_report(project: str, sprint: str, analysis: Dict, decisions: List[Dict]) -> Path:
    promoted = _promoted_paths(project)
    items = apply_decisions_to_items(analysis["items"], promoted, decisions)
    unresolved = [i for i in items if not i["covered"]]

    rows = ""
    if items:
        for item in items:
            status_label = "✅ covered" if item["covered"] else "⚠️ pending"
            rows += (
                f"| `{item['path']}` | {item['ticket_id']} | {item['action']} | "
                f"{item['hint'][:60]} | {status_label} |\n"
            )
    else:
        rows = "| (none) | — | — | No unpromoted registry changes | ✅ |\n"

    decision_lines = ""
    if decisions:
        for d in decisions:
            decision_lines += (
                f"- `{d.get('path')}` → **{d.get('action')}**"
                f" ({d.get('ref', 'no ref')}) — {d.get('note', '')}\n"
            )
    else:
        decision_lines = "- (none yet)\n"

    md_path = reuse_review_md_path(project, sprint)
    content = f"""# Reuse Review — {sprint}

**Project:** {project}
**Prepared:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Done tickets scanned:** {analysis['ticket_count']}
**Unresolved paths:** {len(unresolved)}

## Unpromoted registry changes

| Path | Ticket | Action | Hint | Status |
|------|--------|--------|------|--------|
{rows}

## Recorded decisions

{decision_lines}

## Agent checklist

- [ ] For each **pending** path: promote to studio-library, open LO-* ticket, or record project-local
- [ ] Run `./studio reuse {project} --record <path> <action> [--ref LO-0001] [--note "..."]`
- [ ] Human signs off: `./studio reuse {project} --approve`

## Actions reference

| Action | When |
|--------|------|
| `promote` | Generic package under `packages/` |
| `lo_ticket` | Generic UI under `ui/components/` (studio-library only) |
| `local` | Project-specific; intentionally not shared |

```bash
./studio library promote {project} packages/auth --ticket TICKET-0026 --force
./studio reuse {project} --record ui/components/user-menu local --note "Project-specific chrome"
./studio reuse {project} --approve
```
"""
    md_path.write_text(content, encoding="utf-8")
    return md_path


def prepare_reuse_review(project: str, sprint: str, status: Dict) -> Tuple[Path, Dict]:
    analysis = analyze_sprint_reuse(project, sprint, status)
    existing = load_reuse_review(project, sprint)
    decisions = existing.get("decisions", [])
    promoted = _promoted_paths(project)
    items = apply_decisions_to_items(analysis["items"], promoted, decisions)

    data = {
        "status": existing.get("status") or REUSE_PENDING,
        "sprint": sprint,
        "project": project,
        "prepared_at": datetime.now().isoformat(),
        "items": items,
        "decisions": decisions,
        "ticket_count": analysis["ticket_count"],
        "unresolved_count": len([i for i in items if not i["covered"]]),
    }
    save_reuse_review(project, sprint, data)
    md_path = write_reuse_report(project, sprint, analysis, decisions)
    return md_path, data


def record_reuse_decision(
    project: str,
    sprint: str,
    path: str,
    action: str,
    ref: str = "",
    note: str = "",
) -> Dict:
    allowed = {"promote", "lo_ticket", "local", "review", "promote_or_local"}
    if action not in allowed:
        raise ValueError(f"action must be one of: {', '.join(sorted(allowed))}")

    data = load_reuse_review(project, sprint)
    decisions = [d for d in data.get("decisions", []) if d.get("path") != path]
    decisions.append({
        "path": path.rstrip("/"),
        "action": action,
        "ref": ref.strip() or None,
        "note": note.strip() or None,
        "recorded_at": datetime.now().isoformat(),
    })
    data["decisions"] = decisions
    data["status"] = data.get("status") or REUSE_PENDING
    save_reuse_review(project, sprint, data)
    return data


def approve_reuse_review(project: str, sprint: str, status: Dict, notes: str = "") -> Tuple[bool, str, Dict]:
    data = load_reuse_review(project, sprint)
    if not data.get("items") and not reuse_review_json_path(project, sprint).exists():
        _, data = prepare_reuse_review(project, sprint, status)

    promoted = _promoted_paths(project)
    decisions = data.get("decisions", [])
    unresolved = [
        item for item in data.get("items", [])
        if not _path_covered(item["path"], promoted, decisions)
    ]
    if unresolved:
        paths = ", ".join(f"`{i['path']}`" for i in unresolved[:5])
        extra = f" (+{len(unresolved) - 5} more)" if len(unresolved) > 5 else ""
        return (
            False,
            f"{len(unresolved)} path(s) still unresolved: {paths}{extra}. "
            f"Promote, record --record … local, or open LO ticket then --record … lo_ticket --ref LO-NNNN",
            data,
        )

    data["status"] = REUSE_APPROVED
    data["approved_at"] = datetime.now().isoformat()
    data["approval_notes"] = notes.strip() or None
    data["unresolved_count"] = 0
    save_reuse_review(project, sprint, data)

    hitl = get_sprint_hitl(status)
    hitl["reuse_status"] = REUSE_APPROVED
    hitl["reuse_approved_at"] = data["approved_at"]
    hitl["reuse_sprint"] = sprint

    analysis = analyze_sprint_reuse(project, sprint, status)
    write_reuse_report(project, sprint, analysis, decisions)
    return True, "", data


def find_sprint_needing_reuse(project: str, status: Optional[Dict] = None) -> Optional[str]:
    """Sprint with summary.md that still needs reuse approval.

    Sprints closed before mandatory reuse (no reuse-review.json) are grandfathered.
    """
    if status:
        hitl = get_sprint_hitl(status)
        if hitl.get("reuse_sprint") and hitl.get("reuse_status") not in (None, REUSE_APPROVED):
            return hitl["reuse_sprint"]

    sprints_root = project_dir(project) / "sprints"
    if not sprints_root.exists():
        return None
    candidates = sorted(sprints_root.glob("SPRINT-*"), reverse=True)
    for sprint_dir in candidates:
        sprint = sprint_dir.name
        if not (sprint_dir / "summary.md").exists():
            continue
        if not reuse_review_json_path(project, sprint).exists():
            continue
        reuse = load_reuse_review(project, sprint)
        if reuse.get("status") != REUSE_APPROVED:
            return sprint
    return None


def resolve_reuse_sprint(project: str, status: Dict) -> Optional[str]:
    pending = find_sprint_needing_reuse(project, status)
    if pending:
        return pending
    hitl = get_sprint_hitl(status)
    if hitl.get("reuse_sprint") and hitl.get("reuse_status") != REUSE_APPROVED:
        return hitl["reuse_sprint"]
    if hitl.get("review_status") == REVIEW_APPROVED and hitl.get("reuse_status") != REUSE_APPROVED:
        sprint = status.get("current_sprint")
        if sprint and (sprint_directory(project, sprint) / "summary.md").exists():
            return sprint
    return None


def reuse_gate_message(project: str, status: Dict) -> Optional[str]:
    sprint = find_sprint_needing_reuse(project, status)
    if not sprint:
        return None
    reuse = load_reuse_review(project, sprint)
    if reuse.get("status") == REUSE_APPROVED:
        return None
    unresolved = reuse.get("unresolved_count")
    extra = f" ({unresolved} path(s) pending)" if unresolved else ""
    return (
        f"Reuse review required for {sprint}{extra}.\n"
        f"    ./studio reuse {project}\n"
        f"    ./studio reuse {project} --record <path> <action> [--ref LO-NNNN]\n"
        f"    ./studio reuse {project} --approve"
    )


def format_reuse_brief(project: str, data: Dict) -> str:
    items = data.get("items", [])
    unresolved = [i for i in items if not i.get("covered")]
    lines = [
        f"  Done tickets scanned: {data.get('ticket_count', '?')}",
        f"  Unpromoted paths: {len(unresolved)}",
    ]
    for item in unresolved[:8]:
        lines.append(f"    ⚠️  {item['path']} ({item['ticket_id']}) → {item['action']}: {item['hint']}")
    if len(unresolved) > 8:
        lines.append(f"    … and {len(unresolved) - 8} more (see reuse-review.md)")
    if not unresolved:
        lines.append("  ✅ No unpromoted registry changes — ready for --approve")
    return "\n".join(lines)
