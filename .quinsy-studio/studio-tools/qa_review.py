#!/usr/bin/env python3
"""Independent QA verdict (agency integration L2) and fail feedback (L3).

After a green gate and before MOVE_DONE, a fresh-context subagent judges the
ticket against its AC from the card, the diff, the receipt and the evidence
only. It defaults to FAIL when proof is missing. The implementer never writes
its own verdict.

    ./studio qa <p> <TICKET>                     print the brief for the reviewer
    ./studio qa <p> <TICKET> --verdict PASS|FAIL record the reviewer's file

A FAIL counts toward the same retry budget as a red gate.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, List, Optional

from receipt_checks import VERDICT_RE, section

QA_EVENTS = ("gate-pass", "qa-pass", "qa-fail")
FAIL_EVENTS = ("gate-fail", "qa-fail")
_VERDICT_LINE = re.compile(r"^\s*verdict:\s*(PASS|FAIL)\b", re.I | re.M)
FINDING_FIELDS = ("Issue", "Expected", "Actual", "Evidence", "Fix", "Files")


def qa_path(sprint_dir: Path, ticket_id: str) -> Path:
    return sprint_dir / "qa" / f"{ticket_id}.md"


def qa_state(log: Dict[str, Any], ticket_id: str) -> str:
    """`pass` / `fail` when the latest gate-pass has a verdict after it; else `none`."""
    state = "none"
    for entry in log.get("entries", []):
        if entry.get("ticket") != ticket_id:
            continue
        event = entry.get("event")
        if event == "gate-pass":
            state = "none"
        elif event == "qa-pass":
            state = "pass"
        elif event == "qa-fail":
            state = "fail"
    return state


def parse_verdict(text: str) -> Optional[str]:
    match = _VERDICT_LINE.search(text or "")
    return match.group(1).upper() if match else None


def verdict_file_issues(text: str, claimed: str) -> List[str]:
    """The reviewer's file must back the verdict being recorded."""
    issues: List[str] = []
    written = parse_verdict(text)
    if not written:
        return ["qa file has no `Verdict: PASS` or `Verdict: FAIL` line"]
    if written != claimed:
        issues.append(f"qa file says {written}, --verdict says {claimed}")
    ac = section(text, "AC") or ""
    lines = [ln.strip() for ln in ac.splitlines() if ln.strip()]
    verdicts = [VERDICT_RE.search(ln) for ln in lines]
    if not lines or not any(verdicts):
        issues.append("## AC must list each AC with PASS / FAIL / NOT TESTED and the evidence looked at")
    weak = [ln for ln, v in zip(lines, verdicts) if v and v.group(1) != "PASS"]
    if written == "PASS" and weak:
        issues.append("PASS with an AC that is FAIL or NOT TESTED; missing proof is a FAIL")
    findings = (section(text, "Findings") or "").strip()
    if written == "FAIL":
        if not findings or re.fullmatch(r"-?\s*none\.?", findings, re.I):
            issues.append("FAIL needs ## Findings in Issue / Expected / Actual / Evidence / Fix / Files form")
        else:
            absent = [f for f in FINDING_FIELDS if not re.search(rf"\b{f}\s*:", findings)]
            if absent:
                issues.append("## Findings missing: " + ", ".join(absent))
    return issues


_REVIEWER_LINE = re.compile(r"^\s*Reviewer:\s*(\S.*)$", re.I | re.M)
REVIEWER_PLACEHOLDERS = {"", "(context id)", "<context id>", "tbd", "todo", "none", "me", "self"}


def context_id() -> str:
    """Identity of the running agent context. Set QUINSY_CONTEXT_ID per chat; falls back to the
    terminal session so two chats in one IDE still differ."""
    import os

    for key in ("QUINSY_CONTEXT_ID", "CURSOR_AGENT_ID", "CLAUDE_SESSION_ID", "TERM_SESSION_ID"):
        value = (os.environ.get(key) or "").strip()
        if value:
            return value
    return f"pid-{os.getppid()}"


def parse_reviewer(text: str) -> str:
    match = _REVIEWER_LINE.search(text or "")
    return match.group(1).strip() if match else ""


def reviewer_identity_issues(text: str, implementer_id: str) -> List[str]:
    """The reviewer is a different context than the implementer (LO-0400)."""
    reviewer = parse_reviewer(text)
    if reviewer.lower() in REVIEWER_PLACEHOLDERS:
        return ["qa file has no `Reviewer: <context id>` line — the fresh-context reviewer writes its own id"]
    if implementer_id and reviewer == implementer_id:
        return [f"Reviewer `{reviewer}` is the implementing context — QA must come from a different context"]
    return []


def implementer_id(log: Dict[str, Any], ticket_id: str) -> str:
    """Context recorded on the latest `implement-start` for this ticket."""
    for entry in reversed(log.get("entries", [])):
        if entry.get("ticket_id") == ticket_id and entry.get("event") == "implement-start":
            return str(entry.get("note") or "")
    return ""


def qa_template(ticket_id: str, ac: List[str]) -> str:
    rows = "\n".join(f"- {a}: (PASS / FAIL / NOT TESTED — evidence looked at)" for a in ac) or "- (AC: verdict — evidence)"
    return (
        f"# QA — {ticket_id}\n\n"
        "Verdict: (PASS or FAIL)\n"
        "Reviewer: (context id — print it with `./studio whoami`; must differ from the implementer)\n\n"
        f"## AC\n{rows}\n\n"
        "## Findings\n"
        "- none\n"
        "<!-- On FAIL, one block per finding:\n"
        "- Issue: …\n  Expected: …\n  Actual: …\n  Evidence: …\n  Fix: …\n  Files: …\n-->\n"
    )


def reviewer_brief(
    project: str,
    ticket_id: str,
    card: Optional[Dict[str, Any]],
    *,
    receipt_rel: str,
    qa_rel: str,
    ticket_rel: str,
) -> str:
    """Prompt for a fresh subagent. It gets artifacts, not the implementer's chat."""
    ac = (card or {}).get("ac") or []
    ac_lines = "\n".join(f"  - {a}" for a in ac) or "  - (read ## Acceptance criteria in the ticket)"
    return (
        f"You are the QA reviewer for {ticket_id}. You did not write this code.\n"
        f"Read only: the ticket {ticket_rel}, the receipt {receipt_rel}, the product diff "
        f"(`git -C projects/{project} diff HEAD`, plus untracked files), and the files the receipt names as evidence.\n"
        "Judge each AC:\n"
        f"{ac_lines}\n"
        "Rules:\n"
        "  - Default to FAIL. An AC passes only when you saw proof: a test that asserts it, a screenshot that shows it, "
        "or a request/response. A claim on the receipt is not proof.\n"
        "  - NOT TESTED on any AC means the verdict is FAIL.\n"
        "  - Check the default flow a real user takes, not only the happy unit test.\n"
        "  - Do not fix code. Do not suggest refactors outside the AC.\n"
        f"Write {qa_rel} in this shape (template already there), then stop:\n"
        "  Verdict: PASS | FAIL\n"
        "  Reviewer: <your context id from ./studio whoami>\n"
        "  ## AC — one line per AC with PASS / FAIL / NOT TESTED and the evidence path\n"
        "  ## Findings — `none`, or per finding: Issue / Expected / Actual / Evidence / Fix / Files\n"
    )


def findings_for_debug(text: str) -> str:
    return (section(text, "Findings") or "").strip()


# --------------------------------------------------------------------------
# UX-009 finish gate: shipped screen vs signed real-UI mock (L9)
# --------------------------------------------------------------------------

_IMAGE = re.compile(r"\.(png|jpe?g|webp)$", re.I)
_DECISION = re.compile(r"^\s*Decision:\s*(PASS|HOLD)\b", re.I | re.M)


def finish_path(sprint_dir: Path, ticket_id: str) -> Path:
    return sprint_dir / "qa" / f"{ticket_id}-finish-gate.md"


def mock_shots(project_root: Path, ticket_id: str) -> List[str]:
    folder = project_root / "docs" / "design-specs" / "mocks" / ticket_id
    if not folder.is_dir():
        return []
    return sorted(p.name for p in folder.iterdir() if p.is_file() and _IMAGE.search(p.name))


def needs_finish_gate(project_root: Path, ticket_id: str) -> bool:
    """A ticket with signed mock screenshots is compared against them before done."""
    return bool(mock_shots(project_root, ticket_id))


def finish_state(log: Dict[str, Any], ticket_id: str) -> str:
    state = "none"
    for entry in log.get("entries", []):
        if entry.get("ticket") != ticket_id:
            continue
        event = entry.get("event")
        if event == "gate-pass":
            state = "none"
        elif event == "finish-pass":
            state = "pass"
    return state


def finish_file_issues(text: str, claimed: str, sprint_dir: Path, project_root: Path, ticket_id: str) -> List[str]:
    issues: List[str] = []
    match = _DECISION.search(text or "")
    if not match:
        return ["finish-gate file has no `Decision: PASS` or `Decision: HOLD` line"]
    written = match.group(1).upper()
    if written != claimed:
        issues.append(f"finish-gate file says {written}, --finish says {claimed}")
    table = section(text, "Comparison") or ""
    rows = [ln for ln in table.splitlines() if ln.strip().startswith("|") and re.search(r"\b(PASS|HOLD|NOT TESTED)\b", ln)]
    if not rows:
        issues.append("## Comparison has no state rows")
    for shot in mock_shots(project_root, ticket_id):
        if shot not in table:
            issues.append(f"signed mock state {shot} is not compared")
    shipped_dir = sprint_dir / "qa" / f"{ticket_id}-finish"
    for name in sorted(set(re.findall(r"[\w-]+-(?:1440|390)\.(?:png|jpe?g|webp)", table))):
        if not (shipped_dir / name).exists():
            issues.append(f"shipped capture missing: qa/{ticket_id}-finish/{name}")
    if not ("1440" in table and "390" in table):
        issues.append("compare at both 1440 and 390")
    behavior = section(text, "Behavior (§2e walkthrough on the shipped surface)") or section(text, "Behavior") or ""
    behavior_rows = [
        ln for ln in behavior.splitlines()
        if ln.strip().startswith("|") and re.search(r"\b(PASS|HOLD|NOT TESTED)\b", ln)
    ]
    if not behavior_rows:
        issues.append(
            "## Behavior has no walkthrough rows — run every §2e step on the shipped surface "
            "and compare with the signed mock route (interactions, transitions, reduced-motion)"
        )
    weak = [ln for ln in rows + behavior_rows if re.search(r"\b(HOLD|NOT TESTED)\b", ln)]
    if written == "PASS" and weak:
        issues.append("PASS with a HOLD or NOT TESTED row")
    keep = (section(text, "Keep") or "").strip()
    if not keep:
        issues.append("## Keep must list what already matches the mock and must not regress")
    if written == "HOLD" and not (section(text, "Required before PASS") or "").strip():
        issues.append("HOLD needs ## Required before PASS, one checkable item per difference")
    return issues


def finish_template(ticket_id: str, sprint: str, shots: List[str]) -> str:
    rows = "\n".join(
        f"| {Path(s).stem} | {'390' if '390' in s else '1440'} | {s} | {s} | (PASS / HOLD) |" for s in shots
    )
    return (
        f"# UI finish gate — {ticket_id}\n\n"
        "Decision: (PASS or HOLD — default HOLD until every state is captured at both widths)\n"
        "Reason: (on HOLD, one code: hierarchy | density | motion | copy | flow | uniqueness | a11y | brand)\n"
        f"Spec: docs/design-specs/{ticket_id}.md\nMock: docs/design-specs/mocks/{ticket_id}/\n"
        f"Mock route: app/(design-mocks)/design-mocks/{ticket_id}/ (reference behavior)\n"
        f"Shipped: sprints/{sprint}/qa/{ticket_id}-finish/\n\n"
        "## Comparison\n| State | Width | Mock | Shipped | Result |\n|-------|-------|------|---------|--------|\n"
        f"{rows}\n\n"
        "## Behavior (§2e walkthrough on the shipped surface)\n"
        "Run every §2e walkthrough step against the shipped UI and compare with the signed mock "
        "route: interactions, transitions, reduced-motion. One row per step — PASS / HOLD.\n\n"
        "| Step | Expected (mock) | Shipped | Result |\n|------|-----------------|---------|--------|\n\n"
        "## Required before PASS\n\n## Keep\n\n## Not compared\n"
    )
