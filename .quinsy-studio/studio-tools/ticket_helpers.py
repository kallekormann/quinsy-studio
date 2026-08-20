#!/usr/bin/env python3
"""
ticket_helpers.py — Shared ticket schema for Quinsy Studio

Ensures that project tickets (JUMP-*, NUDG-*) and studio tickets (LO-*)
follow the same strict format:
  1. Unambiguous context & role assignment (assignee_role, current/target state)
  2. Strict constraints (file paths, playbook references, no external packages)
  3. BDD acceptance criteria (Given / When / Then)
  4. Definition of Done

Used by: generate_ticket_manifest.py, studio.py (cmd_ticket, cmd_learn)
"""

from datetime import datetime
from typing import Dict, List, Optional

# =============================================================================
# SKILL → DIRECTOR ROLE MAPPING
# =============================================================================

SKILL_ROLE_MAP = {
    # Team 01 — Frontend & Experience
    "FE-001": "Frontend Engineer (Lead)",
    "FE-002": "UI/Interaction Designer (Director)",
    "FE-003": "Frontend Architect (Director)",
    "FE-004": "QA Specialist (Director)",
    "FE-005": "Frontend Architect (Director)",
    "FE-006": "QA Specialist (Director)",
    # Team 02 — Backend & Systems
    "BE-001": "Backend Architect (Director)",
    "BE-002": "Database Specialist (Director)",
    "BE-003": "Backend Architect (Director)",
    "BE-004": "Backend Engineer (Lead)",
    "BE-005": "Backend Engineer (Lead)",
    # Team 03 — Compliance & Legal
    "CL-001": "Legal & Privacy Officer (Director)",
    "CL-002": "Legal & Privacy Officer (Director)",
    "CL-003": "Legal & Privacy Officer (Director)",
    "CL-004": "Legal & Privacy Officer (Director)",
    # Team 04 — Product Strategy & Architecture
    "PS-001": "Product Manager (Director)",
    "PS-002": "Systems Architect (Director)",
    "PS-003": "Systems Architect (Director)",
    "PS-004": "Product Manager (Director)",
    # Team 05 — Growth, Marketing & Content
    "GM-001": "SEO Specialist (Director)",
    "GM-002": "SEO/AEO Specialist (Director)",
    "GM-003": "Content Strategist (Director)",
    "GM-004": "Game-Dev Specialist (gamedev router)",
    # Team 06 — Product Management
    "PM-001": "Product Manager (Director)",
    "PM-002": "Product Manager (Director)",
    "PM-003": "Product Manager (Director)",
    # Team 07 — AI & Autonomous Systems
    "AI-001": "Autonomous Systems Director",
    "AI-002": "LLM Prompt Engineer",
    "AI-003": "Studio Automation Engineer (Director)",
    # Team 08 — Platform & Enterprise Engineering
    "PE-001": "Platform Architect (Director)",
    "PE-002": "Platform Architect (Director)",
    "PE-003": "Backend Security Specialist (Director)",
    "PE-004": "Infrastructure Specialist (Director)",
    # Team 09 — Studio Operations & Evolution
    "SO-001": "Studio Automation Engineer (Director)",
    "SO-002": "Process Guard (Director)",
    "SO-003": "Process Guard / Agile Coach (Directors)",
    "SO-004": "Documentation Writer (Lead)",
}

# Mandatory playbook reference per team (in the constraints block)
TEAM_PLAYBOOK_MAP = {
    "01-frontend-experience": "knowledge-base/frontend_playbook.md",
    "02-backend-systems": "knowledge-base/backend_playbook.md",
    "03-compliance-legal": "knowledge-base/compliance_playbook.md",
    "04-product-strategy-architecture": "knowledge-base/design_playbook.md",
    "05-growth-marketing-content": "knowledge-base/anti_ai_slop_protocol.md",
    "06-product-management-operating-model": "process/human-in-the-loop.md",
    "07-ai-autonomous-systems": "knowledge-base/ai_automation_playbook.md",
    "08-platform-enterprise-engineering": "knowledge-base/backend_playbook.md",
    "09-studio-operations-evolution": "process/learning-loop.md",
}

# =============================================================================
# HELPERS
# =============================================================================

def role_for_skills(skills: List[str]) -> str:
    """Derive the Director role from the skills (first skill wins)."""
    for skill in skills:
        if skill in SKILL_ROLE_MAP:
            return SKILL_ROLE_MAP[skill]
    return "TBD (assign role)"


def playbook_for_team(team: str) -> str:
    """Return the mandatory playbook reference for a team."""
    return TEAM_PLAYBOOK_MAP.get(team, "knowledge-base/anti_ai_slop_protocol.md")


def build_bdd_criteria(acceptance_criteria: List[str],
                       scenarios: Optional[List[Dict]] = None) -> List[str]:
    """Build BDD acceptance criteria from flat criteria OR explicit
    Given/When/Then scenarios. Always returns BDD blocks."""
    lines: List[str] = []
    if scenarios:
        for i, sc in enumerate(scenarios, 1):
            lines.append(f"**Scenario {i}:** {sc.get('name', 'Main scenario')}")
            lines.append(f"- **Given:** {sc.get('given', '...')}")
            lines.append(f"- **When:** {sc.get('when', '...')}")
            lines.append(f"- **Then:** {sc.get('then', '...')}")
        return lines
    # Fallback: convert flat criteria to BDD (simplest pattern)
    for crit in acceptance_criteria:
        lines.append(f"- **Given:** Current project state")
        lines.append(f"- **When:** The ticket is implemented")
        lines.append(f"- **Then:** {crit}")
    return lines


def render_ticket_markdown(ticket: Dict) -> str:
    """Render a ticket in the strict studio schema (Markdown)."""
    ticket_id = ticket["id"]
    title = ticket["title"]
    ttype = ticket.get("type", "feature")
    priority = ticket.get("priority", "P1")
    estimate = ticket.get("estimate", "M")
    phase = ticket.get("phase", 4)
    status = ticket.get("status", "open")
    role = ticket.get("assignee_role") or role_for_skills(ticket.get("skills", []))
    team = ticket.get("team", "")
    skills = ticket.get("skills", [])
    deps = ticket.get("dependencies", [])
    created = ticket.get("created", datetime.now().strftime("%Y-%m-%d"))

    # Context
    ist = ticket.get("ist_zustand", "Not implemented yet.")
    soll = ticket.get("soll_zustand", "Ticket is fully implemented.")
    value = ticket.get("value", "Visible progress in the project.")

    # Constraints
    files = ticket.get("modification_files", [])
    rules = ticket.get("constraints", [])
    playbook = ticket.get("playbook") or playbook_for_team(team)

    # BDD criteria
    bdd_lines = build_bdd_criteria(
        ticket.get("acceptance_criteria", []),
        ticket.get("scenarios")
    )

    # Definition of Done
    dod = ticket.get("definition_of_done", [
        "QA gate green (`./studio gate <project> --level 5`)",
        "Anti-slop audit: 0 violations",
        "Tests present and green",
        "Documentation/CHANGELOG updated",
    ])

    lines = [
        "---",
        f"id: {ticket_id}",
        f"title: {title}",
        f"type: {ttype}",
        f"status: {status}",
        f"phase: {phase}",
        f"priority: {priority}",
        f"estimate: {estimate}",
        f"assignee_role: {role}",
        f"team: {team}",
        f"skills: {skills}",
        f"dependencies: {deps}",
        f"created: {created}",
    ]
    if ticket.get("sprint"):
        lines.insert(-1, f"sprint: {ticket['sprint']}")
    lines += [
        "---",
        "",
        f"# {ticket_id} — {title}",
        "",
        "## 1. Context & Value",
        f"- **Current state:** {ist}",
        f"- **Target state:** {soll}",
        f"- **Value:** {value}",
        "",
        "## 2. Technical Constraints",
    ]
    if files:
        lines.append(f"- **Modification scope:** {', '.join(files)}")
    else:
        lines.append("- **Modification scope:** Project-specific (see scope)")
    for rule in rules:
        lines.append(f"- **Rule:** {rule}")
    lines.append(f"- **Playbook:** `{playbook}` (mandatory)")
    lines.append("- **Anti-slop:** No AI clichés, no unnecessary external packages without an ADR")

    lines += [
        "",
        "## 3. Acceptance Criteria (BDD)",
    ]
    lines.extend(bdd_lines)

    lines += [
        "",
        "## 4. Definition of Done",
    ]
    for item in dod:
        lines.append(f"- [ ] {item}")

    if deps:
        lines += [
            "",
            "## Dependencies",
        ]
        for dep in deps:
            lines.append(f"- {dep}")

    if skills:
        lines += [
            "",
            "## Skills",
        ]
        for skill in skills:
            lines.append(f"- {skill}")

    return "\n".join(lines)
