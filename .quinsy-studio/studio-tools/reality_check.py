#!/usr/bin/env python3
"""Release reality check before cadence review (agency integration L11, skill SO-005).

After `ship --to dev`, a fresh-context check walks one journey on the dev
deployment and re-runs every done ticket's default flow. It writes
`sprints/SPRINT-NN/reality-check.md` with one verdict:

  READY       journey passes at 1440 and 390, every ticket row PASS, no trigger
  NEEDS WORK  no trigger, but a NOT TESTED row or findings the human should weigh
  FAILED      an automatic-fail trigger fired → bug tickets, review stays closed

The verdict is tied to the product commit. A new commit makes it stale.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path
from typing import Dict, List, Optional

from receipt_checks import section

VERDICTS = ("READY", "NEEDS WORK", "FAILED")
_VERDICT = re.compile(r"^\s*Verdict:\s*(READY|NEEDS WORK|FAILED)\b", re.I | re.M)
_COMMIT = re.compile(r"\bCommit:\s*([0-9a-f]{7,40})\b", re.I)
_DEV_URL = re.compile(r"\bDev URL:\s*(https?://\S+)", re.I)
_EVIDENCE = re.compile(r"(reality-check/[\w./-]+\.(?:png|jpe?g|webp|zip|json))")
_TICKET_ID = re.compile(r"\b[A-Z][A-Z0-9]+-\d{3,}\b")


def report_path(sprint_dir: Path) -> Path:
    return sprint_dir / "reality-check.md"


def head_sha(project_root: Path) -> Optional[str]:
    try:
        result = subprocess.run(
            ["git", "-C", str(project_root), "rev-parse", "HEAD"],
            capture_output=True, text=True, timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    sha = (result.stdout or "").strip()
    return sha if result.returncode == 0 and sha else None


def parse_report(text: str) -> Dict[str, str]:
    verdict = _VERDICT.search(text or "")
    commit = _COMMIT.search(text or "")
    url = _DEV_URL.search(text or "")
    return {
        "verdict": verdict.group(1).upper() if verdict else "",
        "commit": commit.group(1).lower() if commit else "",
        "dev_url": url.group(1) if url else "",
    }


def reality_state(sprint_dir: Path, project_root: Path) -> str:
    """missing | stale | ready | needs-work | failed"""
    path = report_path(sprint_dir)
    if not path.exists():
        return "missing"
    data = parse_report(path.read_text(encoding="utf-8", errors="ignore"))
    if not data["verdict"]:
        return "missing"
    head = head_sha(project_root)
    if head and (not data["commit"] or not head.startswith(data["commit"])):
        return "stale"
    return data["verdict"].lower().replace(" ", "-")


def report_issues(text: str, sprint_dir: Path) -> List[str]:
    data = parse_report(text)
    issues: List[str] = []
    if not data["verdict"]:
        issues.append("no `Verdict: READY | NEEDS WORK | FAILED` line")
    if not data["dev_url"]:
        issues.append("no `Dev URL:` — a local run is not evidence (dev not reachable → NEEDS WORK)")
    if not data["commit"]:
        issues.append("no `Commit:` SHA of the deployed build")
    journey = section(text, "Journey") or ""
    rows = [ln for ln in journey.splitlines() if ln.strip().startswith("|") and re.search(r"PASS|FAIL|NOT TESTED", ln)]
    if not rows:
        issues.append("## Journey has no step rows with results at 1440 and 390")
    tickets = section(text, "Done tickets") or ""
    if not re.search(r"PASS|FAIL|NOT TESTED", tickets):
        issues.append("## Done tickets: re-run each done ticket's default flow and record the result")
    for rel in sorted(set(_EVIDENCE.findall(text or ""))):
        if not (sprint_dir / rel).exists():
            issues.append(f"evidence missing on disk: {rel}")
    body = "\n".join([journey, tickets])
    if data["verdict"] == "READY" and re.search(r"NOT TESTED|\bFAIL\b", body):
        issues.append("READY with a NOT TESTED or FAIL row; that is NEEDS WORK or FAILED")
    triggers = section(text, "Automatic-fail triggers") or ""
    fired = [ln for ln in triggers.splitlines() if ln.strip().startswith("-") and not re.search(r"none fired", ln, re.I)]
    if data["verdict"] == "FAILED":
        if not fired:
            issues.append("FAILED needs the fired triggers listed")
        elif any(not _TICKET_ID.search(ln) for ln in fired):
            issues.append("FAILED: name the bug ticket filed for each trigger (`<trigger> → T-123`)")
    elif fired:
        issues.append(f"a trigger fired but the verdict is {data['verdict'] or 'missing'}; any trigger means FAILED")
    return issues


def template(sprint: str, commit: str, done_ids: List[str]) -> str:
    rows = "\n".join(f"| {tid} | (default-flow claim from the receipt) | (PASS / FAIL / NOT TESTED) | |" for tid in done_ids)
    return (
        f"# Reality check — {sprint}\n\n"
        "Verdict: (READY | NEEDS WORK | FAILED — default NEEDS WORK until dev evidence exists)\n"
        f"Dev URL: (from the runbook)  ·  Commit: {commit or '(deployed sha)'}  ·  Date: \n\n"
        "## Journey\nName: (from docs/workflows/REGISTRY.md or the PRD default flow)\n"
        "| # | Step | 1440 | 390 | Evidence |\n|---|------|------|-----|----------|\n\n"
        "## Done tickets\n| Ticket | Default-flow claim | Result | Evidence |\n|--------|--------------------|--------|----------|\n"
        f"{rows}\n\n"
        "## Automatic-fail triggers\n- none fired\n\n"
        "## Findings (not triggers)\n- none\n\n"
        "## Not tested\n- none\n"
    )


def brief(project: str, sprint: str, report_rel: str) -> str:
    return (
        f"You run the release reality check for {project} {sprint} (skill SO-005,"
        " teams/09-studio-operations-evolution/skills/release-reality-check.md). You did not build this sprint.\n"
        f"Read only: the runbook (dev URL), sprints/{sprint}/review.md, the done tickets' receipts and the signed specs.\n"
        "  - Walk one journey on the dev URL at 1440 and 390 with Playwright; screenshot each step into "
        f"sprints/{sprint}/reality-check/.\n"
        "  - Re-run each done ticket's default-flow claim on dev. Receipts are claims, not proof.\n"
        "  - Axe each journey route. Check private pages are not cached and one user cannot see another's data.\n"
        "  - Any automatic-fail trigger → Verdict FAILED and one bug ticket per trigger "
        f"(./studio ticket {project} \"…\", then set `sprint: {sprint}` in its frontmatter).\n"
        "  - Dev not reachable → NEEDS WORK, never READY from localhost.\n"
        f"Fill {report_rel}, then stop."
    )
