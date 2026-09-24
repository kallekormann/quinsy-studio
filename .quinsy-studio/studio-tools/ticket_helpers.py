#!/usr/bin/env python3
"""
ticket_helpers.py — Shared ticket schema for Quinsy Studio

Ensures that project tickets (JUMP-*, NUDG-*) and studio tickets (LO-*)
follow the same compact format:
  1. Frontmatter is the machine record (id, skills, deps, files)
  2. Body is unique work only: Target, Scope, AC (no boilerplate DoD)
  3. No filler Given/When/Then wrappers; G/W/T only for real scenarios

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
    "FE-002": "Frontend Engineer (Lead)",
    "FE-003": "Frontend Architect (Director)",
    "FE-004": "QA Specialist (Director)",
    "FE-005": "Frontend Architect (Director)",
    "FE-006": "QA Specialist (Director)",
    "FE-007": "Frontend Security Engineer",
    # Team 02 — Backend & Systems
    "BE-001": "Backend Architect (Director)",
    "BE-002": "Database Specialist (Director)",
    "BE-003": "Backend Architect (Director)",
    "BE-004": "Backend Engineer (Lead)",
    "BE-005": "Backend Engineer (Lead)",
    "BE-006": "Backend Architect (Director)",
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
    "AI-004": "Autonomous Systems Director",
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
    # Team 10 — Product Design & Experience
    "UX-001": "Product Designer (Director)",
    "UX-002": "UX Designer (Director)",
    "UX-003": "Information Architect (Director)",
    "UX-004": "UX Researcher (Director)",
    "UX-005": "UI/Visual Designer (Director)",
    "UX-006": "Brand Guardian (Director)",
    "UX-007": "Visual Storyteller (Director)",
    "GD-001": "Growth Designer (Director)",
    "GD-002": "Growth Designer (Director)",
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
    "10-product-design-experience": "knowledge-base/design-science-playbook.md",
    "11-growth-design": "knowledge-base/growth-mechanics-playbook.md",
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


SKILL_PREFIX_TEAM = {
    "FE": "01-frontend-experience",
    "BE": "02-backend-systems",
    "CL": "03-compliance-legal",
    "PS": "04-product-strategy-architecture",
    "GM": "05-growth-marketing-content",
    "PM": "06-product-management-operating-model",
    "AI": "07-ai-autonomous-systems",
    "PE": "08-platform-enterprise-engineering",
    "SO": "09-studio-operations-evolution",
    "UX": "10-product-design-experience",
    "GD": "11-growth-design",
}


def playbook_for_team(team: str) -> str:
    """Return the mandatory playbook reference for a team."""
    return TEAM_PLAYBOOK_MAP.get(team, "knowledge-base/anti_ai_slop_protocol.md")


SKILL_EXTRA_PLAYBOOKS = {
    "FE-001": [
        "knowledge-base/frontend_playbook.md",
        "knowledge-base/atomic-design-playbook.md",
    ],
    "FE-002": ["knowledge-base/frontend_playbook.md"],
    "FE-003": ["knowledge-base/frontend_playbook.md"],
    "FE-004": ["knowledge-base/frontend_playbook.md", "knowledge-base/qa-gate-playbook.md"],
    "FE-005": ["knowledge-base/frontend_playbook.md"],
    "FE-006": ["knowledge-base/qa-gate-playbook.md"],
    "FE-007": [
        "knowledge-base/frontend_playbook.md",
        "knowledge-base/skill-extensions/frontend-security-auditor.md",
    ],
    "BE-001": ["knowledge-base/backend_playbook.md"],
    "BE-002": ["knowledge-base/backend_playbook.md"],
    "BE-003": ["knowledge-base/backend_playbook.md"],
    "BE-004": ["knowledge-base/backend_playbook.md"],
    "BE-005": ["knowledge-base/backend_playbook.md"],
    "BE-006": ["knowledge-base/backend_playbook.md"],
    "GD-001": ["knowledge-base/growth-mechanics-playbook.md"],
    "GD-002": [
        "knowledge-base/growth-mechanics-playbook.md",
        "knowledge-base/delight-playbook.md",
    ],
    "UX-001": [
        "knowledge-base/product-ux-playbook.md",
        "knowledge-base/workflow-definition-playbook.md",
    ],
    "UX-002": [
        "knowledge-base/interaction-ux-playbook.md",
        "knowledge-base/delight-playbook.md",
    ],
    "UX-003": ["knowledge-base/contextual-ia-playbook.md"],
    "UX-004": ["knowledge-base/ux-research-playbook.md"],
    "UX-005": ["knowledge-base/atomic-design-playbook.md"],
    "UX-007": [
        "knowledge-base/visual-storytelling-playbook.md",
        "knowledge-base/growth-mechanics-playbook.md",
    ],
    "AI-003": ["knowledge-base/ai_automation_playbook.md"],
    "AI-004": ["knowledge-base/ai_automation_playbook.md"],
}


from studio_learnings_store import TEAM_LEARNING_CATALOG


def playbooks_for_skills(skills: List[str]) -> List[str]:
    """Playbook paths the implementer must read for these skill IDs."""
    seen: List[str] = []
    for skill in skills or []:
        prefix = str(skill).split("-")[0]
        team = SKILL_PREFIX_TEAM.get(prefix)
        if team:
            path = playbook_for_team(team)
            if path not in seen:
                seen.append(path)
            catalog = TEAM_LEARNING_CATALOG.get(team)
            if catalog and catalog not in seen:
                seen.append(catalog)
        for extra in SKILL_EXTRA_PLAYBOOKS.get(str(skill), []):
            if extra not in seen:
                seen.append(extra)
    return seen


def _yaml_list(items) -> str:
    if not items:
        return "[]"
    return "[" + ", ".join(str(x) for x in items) + "]"


def _is_filler_scenario(sc: Dict) -> bool:
    given = str(sc.get("given", "")).lower()
    when = str(sc.get("when", "")).lower()
    then = str(sc.get("then", "")).lower()
    if "current project state" in given or "the ticket is implemented" in when:
        return True
    if "a user in project" in given and "they use the feature" in when:
        return True
    if "works as described and is tested" in then:
        return True
    return False


def _compact_ac_lines(ticket: Dict) -> List[str]:
    """Specific AC only — no filler Given/When/Then wrappers."""
    lines: List[str] = []
    scenarios = ticket.get("scenarios") or []
    real = [sc for sc in scenarios if not _is_filler_scenario(sc)]
    if real:
        for sc in real:
            lines.append(
                f"- G: {sc.get('given', '').strip()} / W: {sc.get('when', '').strip()} / T: {sc.get('then', '').strip()}"
            )
        return lines
    for crit in ticket.get("acceptance_criteria") or []:
        lines.append(f"- {crit}")
    if not lines:
        lines.append("- (add 2+ specific acceptance criteria)")
    return lines


def build_bdd_criteria(acceptance_criteria: List[str],
                       scenarios: Optional[List[Dict]] = None) -> List[str]:
    """Legacy BDD blocks. New tickets use `_compact_ac_lines` instead."""
    lines: List[str] = []
    if scenarios:
        for i, sc in enumerate(scenarios, 1):
            lines.append(f"**Scenario {i}:** {sc.get('name', 'Main scenario')}")
            lines.append(f"- **Given:** {sc.get('given', '...')}")
            lines.append(f"- **When:** {sc.get('when', '...')}")
            lines.append(f"- **Then:** {sc.get('then', '...')}")
        return lines
    for crit in acceptance_criteria:
        lines.append(f"- {crit}")
    return lines


def render_ticket_markdown(ticket: Dict) -> str:
    """Compact ticket: frontmatter is the machine record; body is unique work only."""
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
    soll = ticket.get("soll_zustand", "Ticket is fully implemented.")
    value = ticket.get("value", "")
    files = ticket.get("modification_files", [])

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
        f"skills: {_yaml_list(skills)}",
        f"dependencies: {_yaml_list(deps)}",
        f"files: {_yaml_list(files)}",
        f"created: {created}",
    ]
    if ticket.get("sprint"):
        lines.insert(-1, f"sprint: {ticket['sprint']}")
    if ticket.get("ticket_type"):
        lines.insert(-1, f"ticket_type: {ticket['ticket_type']}")
    if ticket.get("design_status"):
        lines.insert(-1, f"design_status: {ticket['design_status']}")
    if ticket.get("design_spec"):
        lines.insert(-1, f"design_spec: {ticket['design_spec']}")
    if ticket.get("epic"):
        lines.insert(-1, f"epic: {ticket['epic']}")
    if ticket.get("needs_design") is not None:
        lines.insert(-1, f"needs_design: {str(ticket['needs_design']).lower()}")
    if ticket.get("needs_architecture") is not None:
        lines.insert(-1, f"needs_architecture: {str(ticket['needs_architecture']).lower()}")
    if ticket.get("architecture_status"):
        lines.insert(-1, f"architecture_status: {ticket['architecture_status']}")
    if ticket.get("stream"):
        lines.insert(-1, f"stream: {ticket['stream']}")
    if ticket.get("signal"):
        lines.insert(-1, f"signal: {ticket['signal']}")
    if ticket.get("source"):
        lines.insert(-1, f"source: {ticket['source']}")
    if ticket.get("infusion_kind"):
        lines.insert(-1, f"infusion_kind: {ticket['infusion_kind']}")
    if ticket.get("infusion_path"):
        lines.insert(-1, f"infusion_path: {ticket['infusion_path']}")
    if ticket.get("train_skills") is not None:
        lines.insert(-1, f"train_skills: {_yaml_list(ticket.get('train_skills') or [])}")
    lines += ["---", "", "## Target", soll, ""]
    scope = ticket.get("scope") or value
    if scope:
        lines += ["## Scope", scope, ""]
    lines.append("## AC")
    lines.extend(_compact_ac_lines(ticket))
    out = ticket.get("out_of_scope")
    if out:
        lines += ["", "## Out of scope", out if isinstance(out, str) else "\n".join(f"- {x}" for x in out)]
    return "\n".join(lines) + "\n"
