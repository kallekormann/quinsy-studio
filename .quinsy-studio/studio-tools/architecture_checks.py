#!/usr/bin/env python3
"""Gate 1 security/workflow files and per-ticket architecture packet checks (L7, L8).

Gate 1 (PE-005, CL-004, PE-006, workflow registry):
  docs/security/threat-model.md   seven headings
  docs/security/data-map.md
  docs/security/secrets-inventory.md
  docs/workflows/REGISTRY.md      journeys and their states

Architecture packet docs/architecture/<TICKET>.md:
  `threat delta: none — <reason>` or a `## Threat delta` section; `none` is refused when
  the ticket adds a webhook, upload, endpoint, role, tenant rule, job or collection.
  A flow-shaped ticket links docs/workflows/WORKFLOW-*.md with TC-nn branch cases, and
  its acceptance criteria cite those TC-nn.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import List

THREAT_MODEL_HEADINGS = ("System", "Data map", "Trust boundaries", "STRIDE", "Requirements", "Tenant model", "Change log")
_NONE_LINE = re.compile(r"^\s*-?\s*threat delta:\s*none\b\s*[—–:-]+\s*\S", re.I | re.M)
_BARE_NONE = re.compile(r"^\s*-?\s*threat delta:\s*none\b", re.I | re.M)
_DELTA_SECTION = re.compile(r"^##\s*Threat delta\b", re.I | re.M)
_BOUNDARY = re.compile(
    r"\b(webhooks?|uploads?|file upload|new endpoint|endpoints?|roles?|tenants?|tenant rule|payload jobs?|job queue|"
    r"new collection|add(?:s|ing)? (?:a |the )?collection)\b",
    re.I,
)
_FLOW = re.compile(r"\b(flow|wizard|checkout|onboarding|sign-?up|multi-step|journey)\b", re.I)
_TC = re.compile(r"\bTC-\d+\b")
_WORKFLOW_LINK = re.compile(r"docs/workflows/(WORKFLOW-[\w.-]+\.md)")


def _text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def _filled(path: Path, min_chars: int) -> bool:
    body = _text(path).strip()
    return len(body) >= min_chars and not re.search(r"_TODO_|TODO fill|\bTBD\b", body)


def gate_1_security_issues(root: Path) -> List[str]:
    issues: List[str] = []
    model = root / "docs" / "security" / "threat-model.md"
    if not _filled(model, 200):
        issues.append("Write docs/security/threat-model.md (PE-005)")
    else:
        text = _text(model)
        missing = [h for h in THREAT_MODEL_HEADINGS if not re.search(rf"^##\s*{re.escape(h)}\b", text, re.I | re.M)]
        if missing:
            issues.append("docs/security/threat-model.md missing ## " + ", ## ".join(missing))
    if not _filled(root / "docs" / "security" / "data-map.md", 80):
        issues.append("Write docs/security/data-map.md (CL-004 columns; PE-005 adds class and access path)")
    if not _filled(root / "docs" / "security" / "secrets-inventory.md", 60):
        issues.append("Write docs/security/secrets-inventory.md (PE-006: names, owner, rotation — never values)")
    return issues


def gate_1_workflow_issues(root: Path) -> List[str]:
    registry = root / "docs" / "workflows" / "REGISTRY.md"
    if not _filled(registry, 80):
        return ["Write docs/workflows/REGISTRY.md: each user journey with its states (entry, steps, end, failure)"]
    return []


def _ticket_body(ticket_text: str) -> str:
    if (ticket_text or "").startswith("---"):
        parts = ticket_text.split("---", 2)
        if len(parts) >= 3:
            return parts[2]
    return ticket_text or ""


def ticket_is_flow(ticket_text: str) -> bool:
    if re.search(r"^ticket_type:\s*workflow-explainer\b", ticket_text or "", re.M):
        return True
    title = re.search(r"^title:\s*(.*)$", ticket_text or "", re.M)
    return bool(_FLOW.search(title.group(1) if title else ""))


def threat_delta_issues(packet: str, ticket_text: str) -> List[str]:
    has_section = bool(_DELTA_SECTION.search(packet))
    if has_section:
        return []
    if not _BARE_NONE.search(packet):
        return ["architecture note needs `threat delta: none — <reason>` or a `## Threat delta` section (PE-005)"]
    if not _NONE_LINE.search(packet):
        return ["`threat delta: none` needs a one-line reason after a dash"]
    hit = _BOUNDARY.search(_ticket_body(ticket_text)) or _BOUNDARY.search(re.sub(_BARE_NONE, "", packet))
    if hit:
        return [f"`threat delta: none` but the ticket touches `{hit.group(1)}` — write ## Threat delta and update docs/security/threat-model.md"]
    return []


def workflow_issues(root: Path, packet: str, ticket_text: str) -> List[str]:
    if not ticket_is_flow(ticket_text):
        return []
    links = _WORKFLOW_LINK.findall(packet)
    if not links:
        return ["flow-shaped ticket: link docs/workflows/WORKFLOW-<name>.md (states, branches, TC-nn cases) from the architecture note"]
    issues: List[str] = []
    cases: set = set()
    for name in links:
        path = root / "docs" / "workflows" / name
        if not path.exists():
            issues.append(f"docs/workflows/{name} does not exist")
            continue
        found = set(_TC.findall(_text(path)))
        if not found:
            issues.append(f"docs/workflows/{name} has no TC-nn branch cases")
        cases |= found
    if cases and not (set(_TC.findall(_ticket_body(ticket_text))) & cases):
        issues.append("ticket acceptance criteria cite none of the workflow's TC-nn cases")
    return issues


def architecture_packet_issues(root: Path, ticket_id: str, ticket_text: str) -> List[str]:
    path = root / "docs" / "architecture" / f"{ticket_id}.md"
    if not path.is_file():
        return [f"write docs/architecture/{ticket_id}.md"]
    packet = _text(path)
    if len(packet.strip()) < 280 or re.search(r"stub\s*—|TODO fill", packet, re.I):
        return [f"docs/architecture/{ticket_id}.md is a stub"]
    return threat_delta_issues(packet, ticket_text) + workflow_issues(root, packet, ticket_text)
