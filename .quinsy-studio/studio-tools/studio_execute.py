#!/usr/bin/env python3
"""
Agentic execution protocol — next action until a typed HITL stop.

Markdown tickets stay the source of truth. This module:
  - emits one machine-readable step (IMPLEMENT / GATE / VERIFY / MOVE_DONE / HITL / STUDIO_LO)
  - loads a compact ticket card instead of the whole backlog
  - tracks execution-log, receipts, and bounded gate-fail retries
  - health-checks the sprint state graph
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from backlog_paths import find_ticket, read_ticket_meta
from design_ticket_helpers import design_implement_blocked_message
from sprint_hitl import (
    get_sprint_hitl,
    list_sprint_tickets,
    needs_sprint_review,
    sprint_directory,
)
from studio_learning_gate import open_lo_tickets

TOOLS_DIR = Path(__file__).parent
QUINSY_STUDIO = TOOLS_DIR.parent
STUDIO_ROOT = QUINSY_STUDIO.parent
PROJECTS_DIR = STUDIO_ROOT / "projects"

MAX_GATE_RETRIES = 3

HITL_KINDS = (
    "gate-0",
    "gate-1",
    "gate-2",
    "milestones",
    "design-approve",
    "sprint-scope",
    "sprint-groom",
    "sprint-review",
    "reuse",
    "next-sprint",
    "blocked-retries",
    "intake",
    "amendment",
)

RECEIPT_REQUIRED_HEADINGS = (
    ("plan", re.compile(r"^##\s*plan\b", re.I | re.M)),
    ("ac", re.compile(r"^##\s*(ac|acceptance|ac coverage)\b", re.I | re.M)),
    ("default-flow", re.compile(r"^##\s*(default flow|default-flow|lo-0051)\b", re.I | re.M)),
)

FILLER_GIVEN = re.compile(r"current project state", re.I)
FILLER_WHEN = re.compile(r"the ticket is implemented", re.I)


@dataclass
class ExecuteStep:
    kind: str
    ticket_id: Optional[str] = None
    reason: str = ""
    command: str = ""
    card: Optional[Dict[str, Any]] = None
    read: Optional[str] = None
    retries: int = 0
    loop: bool = True

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            "action": self.kind,
            "ticket_id": self.ticket_id,
            "reason": self.reason,
            "command": self.command,
            "read": self.read,
            "retries": self.retries,
            "loop": self.loop and not self.kind.startswith("HITL") and self.kind != "HITL",
            "card": self.card,
        }
        return data


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def load_project_status(project: str) -> Dict:
    path = PROJECTS_DIR / project / "status.json"
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def parse_yaml_list(value: str) -> List[str]:
    text = (value or "").strip().strip("'\"")
    if not text or text in ("[]", "none", "-"):
        return []
    if text.startswith("[") and text.endswith("]"):
        inner = text[1:-1].strip()
        if not inner:
            return []
        return [p.strip().strip("'\"") for p in inner.split(",") if p.strip().strip("'\"")]
    return [text]


def extract_ac(body: str) -> List[str]:
    """Acceptance lines from compact ## AC or legacy Acceptance Criteria sections."""
    section = re.search(
        r"^##\s*(?:\d+\.\s*)?(?:AC|Acceptance Criteria)[^\n]*\n(.*?)(?=^## |\Z)",
        body,
        re.DOTALL | re.I | re.M,
    )
    if not section:
        return []
    items: List[str] = []
    for raw in section.group(1).splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("- "):
            line = line[2:].strip()
        elif re.match(r"^\d+\.\s+", line):
            line = re.sub(r"^\d+\.\s+", "", line).strip()
        else:
            continue
        then_m = re.match(r"^\*\*Then:\*\*\s*(.+)$", line, re.I)
        given_m = re.match(r"^\*\*Given:\*\*\s*(.+)$", line, re.I)
        when_m = re.match(r"^\*\*When:\*\*\s*(.+)$", line, re.I)
        if given_m and FILLER_GIVEN.search(given_m.group(1)):
            continue
        if when_m and FILLER_WHEN.search(when_m.group(1)):
            continue
        if then_m:
            items.append(then_m.group(1).strip())
            continue
        gw = re.match(r"^G:\s*(.+?)\s*/\s*W:\s*(.+?)\s*/\s*T:\s*(.+)$", line, re.I)
        if gw:
            items.append(gw.group(3).strip())
            continue
        if line.startswith("**Scenario"):
            continue
        items.append(line)
    return [i for i in items if i]


def extract_target(body: str) -> str:
    match = re.search(
        r"^##\s*Target\s*\n+(.+?)(?=\n## |\Z)",
        body,
        re.DOTALL | re.I | re.M,
    )
    if match:
        return " ".join(match.group(1).strip().split())
    soll = re.search(r"\*\*Target state:\*\*\s*(.+)", body)
    if soll:
        return soll.group(1).strip()
    return ""


def extract_scope(body: str) -> str:
    match = re.search(
        r"^##\s*Scope\s*\n+(.*?)(?=\n## |\Z)",
        body,
        re.DOTALL | re.I | re.M,
    )
    if match:
        text = match.group(1).strip()
        star = re.search(r"\*\*Scope:\*\*\s*(.+)", text)
        if star:
            return star.group(1).strip()
        first = next((ln[2:].strip() for ln in text.splitlines() if ln.strip().startswith("- ")), "")
        return first or " ".join(text.split()[:40])
    star = re.search(r"\*\*Scope:\*\*\s*(.+)", body)
    return star.group(1).strip() if star else ""


def extract_files(meta: Dict, body: str) -> List[str]:
    raw = meta.get("files")
    if raw:
        parsed = parse_yaml_list(str(raw))
        if parsed:
            return parsed
    match = re.search(r"\*\*Modification scope:\*\*\s*(.+)", body)
    if match:
        return [p.strip() for p in match.group(1).split(",") if p.strip() and "project-specific" not in p.lower()]
    return []


def extract_deps(meta: Dict, body: str = "") -> List[str]:
    raw = meta.get("dependencies")
    ids: List[str] = []
    if raw:
        ids.extend(parse_yaml_list(str(raw)))
    for match in re.finditer(r"\b([A-Z]{2,8}-\d{3,})\b", " ".join(ids)):
        pass
    extra = re.findall(r"^-\s*([A-Z]{2,8}-\d{3,})\b", body, re.M) if body else []
    seen: Set[str] = set()
    out: List[str] = []
    for item in ids + extra:
        tid = item.strip()
        dep_match = re.match(r"^([A-Z]{2,8}-\d{3,})", tid)
        if dep_match:
            tid = dep_match.group(1)
        if tid and tid not in seen:
            seen.add(tid)
            out.append(tid)
    return out


def compact_card(path: Path) -> Dict[str, Any]:
    """~150–400 token implementer card. Agent reads the full .md only on IMPLEMENT."""
    text = path.read_text(encoding="utf-8", errors="ignore")
    meta = read_ticket_meta(path)
    body = text
    if text.startswith("---"):
        parts = text.split("---", 2)
        body = parts[2] if len(parts) >= 3 else text
    ac = extract_ac(body)
    files = extract_files(meta, body)
    deps = extract_deps(meta, body)
    try:
        rel = str(path.relative_to(STUDIO_ROOT))
    except ValueError:
        rel = str(path)
    return {
        "id": meta.get("id") or path.stem.split("-")[0] + "-" + path.stem.split("-")[1],
        "title": meta.get("title") or path.stem,
        "status": meta.get("status") or "",
        "priority": meta.get("priority") or "",
        "target": extract_target(body),
        "scope": extract_scope(body),
        "ac": ac[:6],
        "files": files[:8],
        "deps": deps,
        "path": rel,
    }


def ticket_card_for(project: str, ticket_id: str) -> Optional[Dict[str, Any]]:
    path, _status = find_ticket(project, ticket_id)
    if not path:
        return None
    return compact_card(path)


def execution_log_path(project: str, sprint: str) -> Path:
    return sprint_directory(project, sprint) / "execution-log.json"


def load_execution_log(project: str, sprint: str) -> Dict[str, Any]:
    path = execution_log_path(project, sprint)
    if not path.exists():
        return {"sprint": sprint, "entries": []}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        data.setdefault("sprint", sprint)
        data.setdefault("entries", [])
        return data
    except json.JSONDecodeError:
        return {"sprint": sprint, "entries": []}


def append_execution_event(
    project: str,
    sprint: str,
    event: str,
    ticket_id: Optional[str] = None,
    note: str = "",
) -> Path:
    if not sprint:
        raise ValueError("sprint required for execution log")
    path = execution_log_path(project, sprint)
    path.parent.mkdir(parents=True, exist_ok=True)
    log = load_execution_log(project, sprint)
    log["entries"].append(
        {
            "ts": _now(),
            "ticket": ticket_id,
            "event": event,
            "note": note,
        }
    )
    path.write_text(json.dumps(log, indent=2) + "\n", encoding="utf-8")
    return path


def count_gate_fails(log: Dict[str, Any], ticket_id: str) -> int:
    return sum(
        1
        for e in log.get("entries", [])
        if e.get("ticket") == ticket_id and e.get("event") == "gate-fail"
    )


def has_fresh_gate_pass(log: Dict[str, Any], ticket_id: str) -> bool:
    """True when a gate-pass for this ticket was logged after its implement event."""
    entries = log.get("entries", [])
    implement_ts = None
    for e in entries:
        if e.get("ticket") == ticket_id and e.get("event") == "implement":
            implement_ts = e.get("ts")
    if not implement_ts:
        return False
    for e in entries:
        if e.get("event") == "gate-pass" and e.get("ts", "") >= implement_ts:
            if e.get("ticket") in (ticket_id, None, ""):
                return True
            if e.get("ticket") == ticket_id:
                return True
    return False


def receipt_path(project: str, sprint: str, ticket_id: str) -> Path:
    return sprint_directory(project, sprint) / "receipts" / f"{ticket_id}.md"


def debug_path(project: str, sprint: str, ticket_id: str) -> Path:
    return sprint_directory(project, sprint) / "debug" / f"{ticket_id}.md"


def receipt_issues(text: str) -> List[str]:
    if not (text or "").strip():
        return ["receipt empty"]
    issues: List[str] = []
    for name, pattern in RECEIPT_REQUIRED_HEADINGS:
        match = pattern.search(text)
        if not match:
            issues.append(f"missing ## {name}")
            continue
        start = match.end()
        rest = text[start:]
        nxt = re.search(r"^##\s+", rest, re.M)
        body = rest[: nxt.start()] if nxt else rest
        lines = [ln.strip() for ln in body.splitlines() if ln.strip() and ln.strip() not in ("- ...", "...", "-")]
        if not lines:
            issues.append(f"placeholder ## {name}")
    return issues


def receipt_is_complete(project: str, sprint: str, ticket_id: str) -> bool:
    path = receipt_path(project, sprint, ticket_id)
    if not path.exists():
        return False
    return not receipt_issues(path.read_text(encoding="utf-8", errors="ignore"))


def write_receipt_stub(project: str, sprint: str, ticket_id: str, card: Optional[Dict] = None) -> Path:
    path = receipt_path(project, sprint, ticket_id)
    if path.exists():
        return path
    path.parent.mkdir(parents=True, exist_ok=True)
    ac = "\n".join(f"- [ ] {a}" for a in (card or {}).get("ac") or ["(map each AC to a file or route)"])
    path.write_text(
        f"""# Receipt — {ticket_id}

## Plan
- (how this ticket will be implemented; library pull if any)

## AC coverage
{ac}

## Default flow
- Route / user path a real user would take (LO-0051):
- Screenshot: (path or none — function-only ticket)
""",
        encoding="utf-8",
    )
    return path


def append_debug_attempt(
    project: str,
    sprint: str,
    ticket_id: str,
    attempt: int,
    symptom: str,
    excerpt: str = "",
) -> Path:
    path = debug_path(project, sprint, ticket_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    block = (
        f"\n## Attempt {attempt} — {_now()}\n"
        f"### Symptom\n{symptom.strip() or 'Gate failed'}\n\n"
        f"### Hypotheses\n- (agent: most likely cause)\n\n"
        f"### Evidence\n```\n{(excerpt or '')[:2000]}\n```\n\n"
        f"### Fix\n- (what you will try next)\n"
    )
    if path.exists():
        path.write_text(path.read_text(encoding="utf-8") + block, encoding="utf-8")
    else:
        path.write_text(f"# Debug — {ticket_id}\n{block}", encoding="utf-8")
    return path


def pick_next_ticket(
    tickets: List[Dict[str, Any]],
    done_ids: Optional[Set[str]] = None,
) -> Optional[Dict[str, Any]]:
    """Prefer in-progress; else first backlog ticket whose deps are all done."""
    done_ids = done_ids or {t["id"] for t in tickets if t.get("status") == "done"}
    in_progress = [t for t in tickets if t.get("status") == "implement"]
    if in_progress:
        return sorted(in_progress, key=lambda t: t["id"])[0]
    queued = [t for t in tickets if t.get("status") in ("backlog", "open")]
    for ticket in sorted(queued, key=lambda t: t["id"]):
        deps = ticket.get("deps") or []
        if all(d in done_ids for d in deps):
            return ticket
    return None


def unmet_deps(ticket: Dict[str, Any], done_ids: Set[str]) -> List[str]:
    return [d for d in (ticket.get("deps") or []) if d not in done_ids]


def _enrich_sprint_tickets(project: str, tickets: List[Dict]) -> List[Dict]:
    root = PROJECTS_DIR / project
    enriched: List[Dict] = []
    for ticket in tickets:
        row = dict(ticket)
        rel = ticket.get("file")
        path = (root / rel) if rel else None
        if path and path.exists():
            meta = read_ticket_meta(path)
            body = path.read_text(encoding="utf-8", errors="ignore")
            row["deps"] = extract_deps(meta, body)
            row["path"] = str(path)
        else:
            row["deps"] = row.get("deps") or []
        enriched.append(row)
    return enriched


def _hitl(kind: str, project: str, command: str, reason: str, ticket_id: Optional[str] = None) -> ExecuteStep:
    return ExecuteStep(
        kind="HITL",
        ticket_id=ticket_id,
        reason=kind if not reason else f"{kind}: {reason}" if kind not in reason else reason,
        command=command,
        loop=False,
    )


def _has_in_progress(sprint_tickets: List[Dict[str, Any]]) -> bool:
    return any(t.get("status") == "implement" for t in (sprint_tickets or []))


def _studio_lo_step(open_los: List[Dict]) -> ExecuteStep:
    lo = open_los[0]
    lo_id = lo.get("id", "")
    kind = lo.get("infusion_kind") or ""
    path = lo.get("infusion_path") or ""
    reason = "infusion: implement studio learning while context is hot (before next project ticket)"
    if kind or path:
        reason = f"infusion [{kind or 'process'}] → {path or '.quinsy-studio/'} while context is hot"
    return ExecuteStep(
        kind="STUDIO_LO",
        ticket_id=lo_id,
        reason=reason,
        command="./studio infusion",
        read=lo.get("path"),
        card={
            "id": lo_id,
            "title": lo.get("title", ""),
            "path": lo.get("path"),
            "priority": lo.get("priority", "P2"),
            "target": f"Infuse into `{path}`" if path else "Generalize into studio HQ",
            "scope": kind,
        },
        loop=True,
    )


def _studio_lo_if_idle(
    open_los: List[Dict], sprint_tickets: Optional[List[Dict[str, Any]]] = None
) -> Optional[ExecuteStep]:
    """Infuse as soon as a learning exists — do not wait for sprint close or a human learn prompt."""
    if not open_los:
        return None
    if _has_in_progress(sprint_tickets or []):
        return None
    return _studio_lo_step(open_los)


def decide_from_state(
    project: str,
    status: Dict,
    sprint_tickets: List[Dict[str, Any]],
    *,
    open_los: Optional[List[Dict]] = None,
    log: Optional[Dict[str, Any]] = None,
    receipts_ok: Optional[Dict[str, bool]] = None,
    design_block: Optional[str] = None,
    amendment_actions: Optional[List[str]] = None,
    prd_exists: bool = True,
    as_built_ready: bool = True,
) -> ExecuteStep:
    """Pure next-step machine. Disk I/O lives in decide_next_action."""
    hg = status.get("human_gates") or {}
    open_los = open_los if open_los is not None else []
    log = log or {"entries": []}
    receipts_ok = receipts_ok or {}
    sprint = status.get("current_sprint") or ""
    adopt = (status.get("mode") or "core") == "adopt"

    if amendment_actions:
        return ExecuteStep(
            kind="HITL",
            reason=f"amendment: {amendment_actions[0]}",
            command=amendment_actions[0],
            loop=False,
        )

    if adopt and not as_built_ready:
        return ExecuteStep(
            kind="IMPLEMENT",
            reason="adopt: fill docs/as-built/ from the live codebase (cite paths; not a README restatement)",
            command=f"./studio resume {project}",
            read="docs/as-built/",
            loop=True,
        )

    if not prd_exists:
        if adopt:
            return ExecuteStep(
                kind="VERIFY",
                reason="adopt: synthesize docs/intake/prd.md from as-built + intent",
                command=f"./studio resume {project}",
                read="docs/intake/",
                loop=True,
            )
        return _hitl("intake", project, f"./studio bootstrap {project}", "PRD missing")

    if hg.get("0", {}).get("status") != "approved":
        return _hitl(
            "gate-0",
            project,
            f"./studio approve {project} --gate 0",
            "human must approve as-built truth + synthesized PRD"
            if adopt
            else "human must approve PRD + definitions",
        )
    if hg.get("1", {}).get("status") != "approved":
        return _hitl(
            "gate-1",
            project,
            f"./studio approve {project} --gate 1",
            "human must approve as-is architecture (no greenfield stack swap)"
            if adopt
            else "human must approve architecture",
        )
    if hg.get("2", {}).get("status") != "approved":
        return _hitl(
            "gate-2",
            project,
            f"./studio approve {project} --gate 2",
            "human must approve design of what exists + debt"
            if adopt
            else "human must approve design",
        )

    if needs_sprint_review(status):
        return _hitl(
            "sprint-review",
            project,
            f"./studio review {project}",
            "human tries shipped work — do not implement feedback",
        )

    hitl = get_sprint_hitl(status)
    all_done = bool(sprint_tickets) and all(t.get("status") == "done" for t in sprint_tickets)
    sprint_closed = bool(sprint) and all_done and hitl.get("review_status") == "approved"

    if sprint_closed:
        hitl = get_sprint_hitl(status)
        from sprint_reuse_review import reuse_gate_message

        reuse_msg = reuse_gate_message(project, status)
        if reuse_msg:
            return _hitl("reuse", project, f"./studio reuse {project}", reuse_msg.split("\n")[0][:120])
        if hitl.get("retro_status") != "done":
            return ExecuteStep(
                kind="VERIFY",
                reason="fill project retro then ./studio retro --complete",
                command=f"./studio retro {project}",
                loop=True,
            )
        lo_step = _studio_lo_if_idle(open_los, sprint_tickets)
        if lo_step:
            return lo_step
        return _hitl(
            "next-sprint",
            project,
            f"./studio sprint {project}",
            "human approves next sprint scope",
        )

    if not sprint:
        lo_step = _studio_lo_if_idle(open_los, sprint_tickets)
        if lo_step:
            return lo_step
        return ExecuteStep(
            kind="HITL",
            reason="sprint-scope: no current sprint — propose then human --approve-scope",
            command=f"./studio sprint {project}",
            loop=False,
        )

    if hitl.get("scope_status") != "approved":
        lo_step = _studio_lo_if_idle(open_los, sprint_tickets)
        if lo_step:
            return lo_step
        return _hitl(
            "sprint-scope",
            project,
            f"./studio sprint {project} --approve-scope",
            "human must approve sprint scope",
        )
    if hitl.get("groom_status") != "approved":
        lo_step = _studio_lo_if_idle(open_los, sprint_tickets)
        if lo_step:
            return lo_step
        return _hitl(
            "sprint-groom",
            project,
            f"./studio groom {project} --approve",
            "human must approve groom",
        )

    tickets = sprint_tickets
    done_ids = {t["id"] for t in tickets if t.get("status") == "done"}
    current = pick_next_ticket(tickets, done_ids)
    if current is None:
        lo_step = _studio_lo_if_idle(open_los, tickets)
        if lo_step:
            return lo_step
        waiting = [
            t
            for t in tickets
            if t.get("status") in ("backlog", "open") and unmet_deps(t, done_ids)
        ]
        if waiting:
            w = waiting[0]
            missing = ", ".join(unmet_deps(w, done_ids))
            return ExecuteStep(
                kind="HITL",
                ticket_id=w["id"],
                reason=f"blocked-retries: {w['id']} waits on {missing}",
                command=f"./studio board {project}",
                loop=False,
            )
        if tickets and all(t.get("status") == "done" for t in tickets):
            return _hitl(
                "sprint-review",
                project,
                f"./studio review {project}",
                "all sprint tickets done",
            )
        return ExecuteStep(
            kind="HITL",
            reason="sprint-scope: no executable sprint ticket",
            command=f"./studio board {project}",
            loop=False,
        )

    tid = current["id"]
    card = current.get("card")
    read_path = current.get("path") or current.get("file")

    if current.get("status") in ("backlog", "open"):
        lo_step = _studio_lo_if_idle(open_los, tickets)
        if lo_step:
            return lo_step
        if design_block:
            return _hitl(
                "design-approve",
                project,
                f"./studio approve-design {project} {tid}",
                design_block[:160],
                ticket_id=tid,
            )
        return ExecuteStep(
            kind="IMPLEMENT",
            ticket_id=tid,
            reason="next unblocked sprint ticket",
            command=f'./studio move {project} {tid} implement --reason "Sprint execution"',
            card=card,
            read=read_path,
            loop=True,
        )

    # in implement
    fails = count_gate_fails(log, tid)
    if fails >= MAX_GATE_RETRIES:
        return _hitl(
            "blocked-retries",
            project,
            f"./studio move {project} {tid} blocked --reason \"gate failed {fails} times\"",
            f"gate failed {fails} times — write debug then block",
            ticket_id=tid,
        )

    receipt_ok = receipts_ok.get(tid, False)
    if not receipt_ok:
        return ExecuteStep(
            kind="VERIFY",
            ticket_id=tid,
            reason="write execution receipt (plan, AC coverage, default flow)",
            command=f"./studio receipt {project} {tid}",
            card=card,
            read=read_path,
            retries=fails,
            loop=True,
        )

    gate_level = int(str(status.get("gate", "0") or "0"))
    gate_passed = status.get("gate_status") == "passed" and gate_level >= 5
    fresh = has_fresh_gate_pass(log, tid)
    log_empty = not log.get("entries")
    if not gate_passed or (not log_empty and not fresh):
        if fails:
            return ExecuteStep(
                kind="DEBUG",
                ticket_id=tid,
                reason=f"gate red — diagnose in debug/{tid}.md then re-run gate (attempt {fails + 1}/{MAX_GATE_RETRIES})",
                command=f"./studio gate {project} --level 5",
                card=card,
                read=read_path,
                retries=fails,
                loop=True,
            )
        return ExecuteStep(
            kind="GATE",
            ticket_id=tid,
            reason="QA level 5 required before done (fresh run after implement)",
            command=f"./studio gate {project} --level 5",
            card=card,
            read=read_path,
            loop=True,
        )

    return ExecuteStep(
        kind="MOVE_DONE",
        ticket_id=tid,
        reason="receipt + fresh gate 5 — mark done and continue",
        command=f'./studio move {project} {tid} done --reason "DoD met"',
        card=card,
        read=read_path,
        loop=True,
    )


def decide_next_action(project: str) -> ExecuteStep:
    from amendment_intake import resume_amendment_actions
    from sprint_reuse_review import reuse_gate_message

    project_dir = PROJECTS_DIR / project
    if not project_dir.exists():
        return ExecuteStep(
            kind="HITL",
            reason=f"intake: project '{project}' not found",
            command=f"./studio bootstrap {project}",
            loop=False,
        )

    status = load_project_status(project)
    prd = project_dir / "docs" / "intake" / "prd.md"
    sprint = status.get("current_sprint") or ""
    tickets: List[Dict] = []
    log: Dict[str, Any] = {"entries": []}
    receipts_ok: Dict[str, bool] = {}
    design_block = None
    if sprint:
        tickets = _enrich_sprint_tickets(project, list_sprint_tickets(project, sprint))
        log = load_execution_log(project, sprint)
        for t in tickets:
            receipts_ok[t["id"]] = receipt_is_complete(project, sprint, t["id"])
            if t.get("path"):
                t["card"] = compact_card(Path(t["path"]))
        current = pick_next_ticket(tickets)
        if current and current.get("status") in ("backlog", "open") and current.get("path"):
            content = Path(current["path"]).read_text(encoding="utf-8", errors="ignore")
            design_block = design_implement_blocked_message(current["id"], content)

    # reuse_gate_message imported for decide_from_state sprint-closed path
    _ = reuse_gate_message
    from studio_adopt import as_built_is_ready

    adopt = (status.get("mode") or "core") == "adopt"
    return decide_from_state(
        project,
        status,
        tickets,
        open_los=open_lo_tickets(),
        log=log,
        receipts_ok=receipts_ok,
        design_block=design_block,
        amendment_actions=resume_amendment_actions(project),
        prd_exists=prd.exists(),
        as_built_ready=as_built_is_ready(project) if adopt else True,
    )


def format_execute_step(project: str, step: ExecuteStep) -> str:
    lines = [f"EXECUTE {project}"]
    lines.append(f"  ACTION:  {step.kind}" + (f" {step.ticket_id}" if step.ticket_id else ""))
    if step.reason:
        lines.append(f"  REASON:  {step.reason}")
    if step.command:
        lines.append(f"  NEXT:    {step.command}")
    if step.read:
        lines.append(f"  READ:    {step.read}  (this ticket only — not the backlog)")
    if step.retries:
        lines.append(f"  RETRIES: {step.retries}/{MAX_GATE_RETRIES}")
    if step.kind == "HITL" or (isinstance(step.reason, str) and step.reason.startswith("HITL")):
        lines.append("  STOP. Wait for the human. Do not implement past this gate.")
    elif step.kind == "STUDIO_LO":
        lines.append("  Studio HQ only (.quinsy-studio/). Infuse now — do not start the next project ticket.")
        lines.append("  Then loop: ./studio execute <project>")
    else:
        lines.append("  Loop: do NEXT, then ./studio execute again. Do not ask to continue.")
    card = step.card
    if card:
        lines.append("")
        lines.append("  CARD")
        lines.append(f"    {card.get('id', '')}: {card.get('title', '')}")
        if card.get("target"):
            lines.append(f"    target: {card['target']}")
        if card.get("scope"):
            lines.append(f"    scope:  {card['scope']}")
        for ac in card.get("ac") or []:
            lines.append(f"    ac: {ac}")
        if card.get("files"):
            lines.append(f"    files: {', '.join(card['files'])}")
        if card.get("deps"):
            lines.append(f"    deps:  {', '.join(card['deps'])}")
    return "\n".join(lines)


def harvest_retro_learn_prompts(retro_text: str, source: str) -> List[str]:
    """Turn non-placeholder 'went badly' / 'improve' bullets into learn command prompts."""
    prompts: List[str] = []
    for section in (
        r"## What went badly\?\s*\n(.*?)(?=\n## |\Z)",
        r"## What can we improve\?\s*\n(.*?)(?=\n## |\Z)",
    ):
        match = re.search(section, retro_text, re.DOTALL | re.I)
        if not match:
            continue
        for raw in match.group(1).splitlines():
            line = raw.strip()
            if line.startswith("- "):
                line = line[2:].strip()
            if not line or line in ("...", "- ...") or line.endswith(": ..."):
                continue
            title = line[:80].rstrip(".")
            prompts.append(
                f'./studio learn "{title}" --signal process-gap --source {source}'
            )
    return prompts[:8]


def health_report(project: str) -> List[Dict[str, str]]:
    """State-graph checks. level: error | warn | ok."""
    findings: List[Dict[str, str]] = []
    project_dir = PROJECTS_DIR / project
    if not project_dir.exists():
        return [{"level": "error", "code": "no-project", "message": f"{project} not found", "fix": f"./studio bootstrap {project}"}]

    status = load_project_status(project)
    sprint = status.get("current_sprint") or ""
    los = open_lo_tickets()
    if los:
        findings.append(
            {
                "level": "warn",
                "code": "open-lo",
                "message": f"{len(los)} open LO-* (infuse now — blocks next project ticket)",
                "fix": f"implement {los[0].get('id')} in .quinsy-studio/ then ./studio execute {project}",
            }
        )

    if needs_sprint_review(status):
        findings.append(
            {
                "level": "ok",
                "code": "review-pending",
                "message": "sprint review is the correct HITL stop",
                "fix": f"./studio review {project}",
            }
        )

    if sprint:
        tickets = _enrich_sprint_tickets(project, list_sprint_tickets(project, sprint))
        log = load_execution_log(project, sprint)
        hitl = get_sprint_hitl(status)
        mid_sprint = (
            hitl.get("scope_status") == "approved"
            and hitl.get("groom_status") == "approved"
            and not needs_sprint_review(status)
            and hitl.get("review_status") != "approved"
            and any(t.get("status") != "done" for t in tickets)
        )
        if mid_sprint and not log.get("entries"):
            findings.append(
                {
                    "level": "warn",
                    "code": "no-exec-log",
                    "message": f"{sprint} has no execution-log.json yet",
                    "fix": f"./studio execute {project}",
                }
            )
        for t in tickets:
            if t.get("status") == "implement":
                if not receipt_is_complete(project, sprint, t["id"]):
                    findings.append(
                        {
                            "level": "warn",
                            "code": "no-receipt",
                            "message": f"{t['id']} in implement without complete receipt",
                            "fix": f"./studio receipt {project} {t['id']}",
                        }
                    )
                gate_level = int(str(status.get("gate", "0") or "0"))
                if status.get("gate_status") != "passed" or gate_level < 5:
                    findings.append(
                        {
                            "level": "warn",
                            "code": "implement-no-gate",
                            "message": f"{t['id']} in implement; gate not level 5 passed",
                            "fix": f"./studio gate {project} --level 5",
                        }
                    )
            waiting = unmet_deps(t, {x["id"] for x in tickets if x.get("status") == "done"})
            if t.get("status") in ("backlog", "open") and waiting:
                findings.append(
                    {
                        "level": "ok",
                        "code": "deps",
                        "message": f"{t['id']} waits on {', '.join(waiting)}",
                        "fix": "execute unblocked tickets first",
                    }
                )

    if not findings:
        findings.append(
            {
                "level": "ok",
                "code": "healthy",
                "message": "no state-graph issues",
                "fix": f"./studio execute {project}",
            }
        )
    return findings


def format_health(project: str, findings: List[Dict[str, str]]) -> str:
    lines = [f"HEALTH {project}"]
    for item in findings:
        mark = {"error": "✗", "warn": "!", "ok": "·"}.get(item["level"], "·")
        lines.append(f"  {mark} [{item['code']}] {item['message']}")
        lines.append(f"      {item['fix']}")
    return "\n".join(lines)


def gate_fail_should_open_lo(log: Dict[str, Any], ticket_id: str) -> bool:
    return count_gate_fails(log, ticket_id) >= MAX_GATE_RETRIES


def existing_gate_fail_lo(source: str) -> bool:
    for item in open_lo_tickets():
        path = QUINSY_STUDIO / item["path"] if not Path(item["path"]).is_absolute() else Path(item["path"])
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if "gate-fail" in text and source in text:
            return True
    return False
