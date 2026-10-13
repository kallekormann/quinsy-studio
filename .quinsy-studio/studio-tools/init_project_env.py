#!/usr/bin/env python3
"""
Project Environment Initializer — Automates git repos and docker-compose bootstrapping.

Usage:
    python3 init_project_env.py <project> [--archetype <type>]
"""

import sys
import os
import json
import subprocess
from pathlib import Path
from datetime import datetime
from ui_kit_peers import write_ui_kit_setup

# =============================================================================
# CONFIGURATION
# =============================================================================

PROJECTS_DIR = Path(__file__).parent.parent.parent / "projects"
QUINSY_STUDIO = Path(__file__).parent.parent
TEMPLATES_DIR = QUINSY_STUDIO / "studio-templates"

# =============================================================================
# INITIALIZATION
# =============================================================================

def init_project(project: str, archetype: str = 'saas-application'):
    """Initialize a new project environment."""
    project_dir = PROJECTS_DIR / project
    
    print(f"\n  Initializing project: {project}")
    print(f"  Archetype: {archetype}")
    
    # 1. Create directory structure
    create_directories(project_dir)
    create_phases_scaffold(project_dir)
    
    # 2. Create status.json
    create_status(project_dir, project, archetype)
    
    # 3. Create agent-briefing.md
    create_agent_briefing(project_dir, project, archetype)
    
    # 4. Create RUNBOOK.md
    create_runbook(project_dir, project)
    
    # 5. Initialize Docker
    init_docker(project_dir, project)
    
    # 6. Initialize Git (project-local repo — never studio HQ)
    init_git(project_dir)
    init_project_gitignore(project_dir)
    from studio_settings import init_project_settings

    init_project_settings(project, project_dir=project_dir)
    print(f"  ✓ docs/studio.settings.yaml (product execute ledger)")
    
    print(f"\n  \033[92m✓ Project initialized: {project_dir}\033[0m")
    print(f"  Next steps:")
    print(f"    1. Create PRD: {project_dir}/docs/intake/prd.md")
    print(f"    2. UI kit peers (mandatory in the React app): see docs/setup/ui-kit.md")
    print(f"    3. Start Docker: ./studio env {project} up")
    print(f"    4. GitHub repo: ./studio repo {project} create")

def create_directories(project_dir: Path):
    """Create project directory structure."""
    dirs = [
        "docs/intake",
        "docs/definitions",
        "docs/architecture",
        "docs/architecture/diagrams",
        "docs/adr",
        "docs/decisions",
        "docs/phases",
        "docs/modules",
        "design",
        "design/prototype",
        "ui/tokens",
        "ui/components/atoms",
        "ui/components/molecules",
        "ui/components/organisms",
        "ui/page-types",
        "backlog",
        "backlog/implement",
        "backlog/done",
        "backlog/blocked",
        "sprints",
        "docker",
        "packages",
        "apps",
    ]
    
    for d in dirs:
        (project_dir / d).mkdir(parents=True, exist_ok=True)
    
    seed_definitions(project_dir)
    write_ui_kit_setup(project_dir)
    print(f"  ✓ docs/setup/ui-kit.md (radix-ui + CVA + clsx + tailwind-merge + lucide-react)")
    
    print(f"  ✓ Directory structure created")


def create_phases_scaffold(project_dir: Path):
    """Seed docs/phases/ with index and revisions log."""
    phases = project_dir / "docs" / "phases"
    readme = phases / "README.md"
    if not readme.exists():
        readme.write_text(
            """# Project phases (milestones)

> Filled after gate 2. See `.quinsy-studio/process/milestone-planning.md`.

| Milestone | Goal | Status |
|-----------|------|--------|
| M0 | _TBD — first version from the PRD_ | planned |

**Current milestone:** — (set after roadmap approval)

Add M1, M2, M3, and as many later rows as `docs/intake/prd.md` and `docs/intake/sources/` need. There is no fixed count.

## Documents

- [revisions.md](revisions.md) — pre-implementation gate feedback
- One `M<n>-*.md` file per version, added during execution planning
""",
            encoding="utf-8",
        )
    revisions = phases / "revisions.md"
    if not revisions.exists():
        revisions.write_text(
            "# Pre-implementation revisions\n\n_Log gate 0–2 feedback here via `./studio revise`._\n",
            encoding="utf-8",
        )
    print(f"  ✓ docs/phases/ scaffold created")


DEFINITION_TEMPLATES = {
    "00-index.md": "# Definitions Index\n\nLinks to all definition documents for this project.\n",
    "01-glossary.md": "# Glossary\n\n| Term | Definition |\n|------|------------|\n| _TODO_ | _TODO_ |\n",
    "02-personas.md": (
        "# Personas\n\n"
        "Task-based segments (UX-004), not demographic posters. One block per persona.\n\n"
        "## <Persona name — the job they are doing>\n\n"
        "| Field | Value |\n|-------|-------|\n"
        "| Top tasks | _TODO_ |\n"
        "| Problem in their words | _TODO_ |\n"
        "| What they use today | _TODO_ |\n"
        "| Trigger to switch | _TODO_ |\n"
        "| Success in their words | _TODO_ |\n"
        "| Source (interviews, reviews, support, analytics) or **assumption** + date | _TODO_ |\n"
    ),
    "03-user-journeys.md": "# User Journeys\n\n_Key flows through the product._\n",
    "04-domain-model.md": "# Domain Model\n\n_Core entities and relationships._\n",
    "05-data-flows.md": "# Data Flows\n\n_How data moves through the system._\n",
    "06-api-overview.md": "# API Overview\n\n_Public and internal APIs._\n",
    "07-ui-states.md": "# UI States\n\n_Loading, empty, error, success states._\n",
    "08-non-goals.md": "# Non-Goals\n\n_Explicitly out of scope._\n",
    "09-constraints.md": "# Constraints\n\n_Technical and business constraints._\n",
    "10-kpis.md": "# KPIs\n\n_Measurable success metrics._\n",
    "11-assumptions.md": "# Assumptions\n\n_Document assumptions until validated._\n",
    "12-positioning.md": (
        "# Positioning\n\n"
        "Skill GM-007. Gate 0 refuses a stub. Every public surface, listing, and email derives from this file.\n\n"
        "## Positioning table\n\n"
        "| Field | Value |\n|-------|-------|\n"
        "| Audience (persona from 02-personas.md) | _TODO_ |\n"
        "| Problem in their words | _TODO_ |\n"
        "| Alternative they use today | _TODO_ |\n"
        "| Category we claim | _TODO_ |\n"
        "| The one difference that matters | _TODO_ |\n"
        "| Proof | _TODO_ |\n\n"
        "## Core message\n\n_One sentence a persona would repeat._\n\n"
        "## Message hierarchy per persona\n\n"
        "| Persona | Problem line | Mechanism line | Proof line | Next step |\n|---------|--------------|----------------|------------|-----------|\n| _TODO_ | _TODO_ | _TODO_ | _TODO_ | _TODO_ |\n\n"
        "## Proof list\n\n- _TODO_ (claim → number, quote with permission, or demo)\n"
    ),
}


def seed_definitions(project_dir: Path):
    """Create definition document scaffolds if missing."""
    defs_dir = project_dir / "docs" / "definitions"
    defs_dir.mkdir(parents=True, exist_ok=True)
    for filename, content in DEFINITION_TEMPLATES.items():
        path = defs_dir / filename
        if not path.exists():
            path.write_text(content)

def create_status(project_dir: Path, project: str, archetype: str):
    """Create initial status.json (aligned with studio.py schema)."""
    status = {
        "name": project,
        "phase": "0",
        "gate": "0",
        "gate_status": "open",
        "mode": "core",
        "created": datetime.now().strftime("%Y-%m-%d"),
        "last_update": datetime.now().strftime("%Y-%m-%d"),
        "archetype": archetype,
        "current_sprint": None,
        "active_ticket": None,
        "gate_history": [],
        "human_gates": {},
        "design_scope": None,
    }
    
    status_file = project_dir / "status.json"
    status_file.write_text(json.dumps(status, indent=2, ensure_ascii=False))
    print(f"  ✓ status.json created")

def create_agent_briefing(project_dir: Path, project: str, archetype: str):
    """Create agent-briefing.md."""
    content = f"""# Agent Briefing — {project}

You run the project `{project}` autonomously through the Quinsy Studio operating system.
- **Archetype:** {archetype} — roles/ADRs/decisions see `docs/intake/archetype-checklist.md` and `.quinsy-studio/process/project-archetypes.md`.

## Your mission (pre-implementation)
1. **Gate 0** — Fill `docs/definitions/` from PRD; user approves: `./studio approve {project} --gate 0`
2. **Gate 1** — Fill `docs/architecture/` + ADRs; user approves: `./studio approve {project} --gate 1`
3. **Gate 2a** — Unanswered questions in `docs/design/discovery.md`; fill `design/DESIGN.md` from human answers; user approves: `./studio approve {project} --gate 2a` (do **not** scaffold prototype)
4. **Gate 2b** — Project CSS tokens, coded atoms/molecules/organisms, sticker all-states; user picks mock scope (`journey` | `core-views`); user approves: `./studio approve {project} --gate 2b` (look stays in the project)
5. **Milestones** — Draft `docs/phases/` roadmap; user approves: `./studio approve {project} --milestones`; agent writes tickets for active milestone only
6. **Then** — Sprint + implementation within current milestone (see `.quinsy-studio/process/milestone-planning.md`)

## Iteration
- User feedback: `./studio revise {project} --gate <0|1|2a|2b> --feedback "..."`
- Log: `docs/phases/revisions.md`

## Non-negotiable
- No tickets or production implementation before gate 2b.
- Mocks live in `design/prototype/` using the target stack (e.g. Next.js).
- UI kit peers are mandatory in the React app: `radix-ui`, `class-variance-authority`, `clsx`, `tailwind-merge`, `lucide-react` (+ `@headlessui/react`). See `docs/setup/ui-kit.md`.
- Schema migrations: if you can reach the database (local Compose or documented VPS), **you run them**. Inform the human; do not ask them to migrate as sprint work.
- Sticker sheet: `design/prototype/app/sticker-sheet/` (tokens + components).
- `.quinsy-studio/process/` is the binding reference (lifecycle, gates, ADR, anti-slop, iteration).
- Role skills live in `.quinsy-studio/teams/` — activate the right role per phase.
- Every decision becomes an ADR; every ADR updates the named documentation.
- Anti-slop audit and QA gate must be green before a gate counts as passed.
- No `done` ticket without a definition of done; no sprint without summary.md.
- Human-in-the-loop: blocking decisions are escalated as decision records and wait for human approval (`.quinsy-studio/process/human-in-the-loop.md`).

## Tools
- `./studio focus {project}` / `./studio resume {project}` / `./studio guard {project} "..."`
- `./studio verify-worlds` — studio vs project git must be separate
- `./studio blueprint {project}` / `./studio design {project} --discovery` / `./studio design {project} --scope journey|core-views`
- `./studio approve {project} --gate 0|1|2a|2b` — project look stays in the project; milestone roadmap after 2b (`--milestones`)
- `./studio promote-library {project}` — Headless/generic kit only (not this product's visual system)
- `./studio revise {project} --gate <0|1|2a|2b> --feedback "..."` — iteration loop
"""
    
    briefing_file = project_dir / "agent-briefing.md"
    briefing_file.write_text(content)
    print(f"  ✓ agent-briefing.md created")

def create_runbook(project_dir: Path, project: str):
    """Create RUNBOOK.md."""
    content = f"""# RUNBOOK — {project}

Autonomous flow from intake to gate 7. The agent works through this document.

## Phase 1 — Intake (HUMAN GATE 0)
1. `./studio intake {project} intake/<prd>.md`
2. Fill `docs/definitions/00-index.md` … `11-assumptions.md`
3. User approves: `./studio approve {project} --gate 0`

## Phase 2 — Architecture blueprint (HUMAN GATE 1)
1. `./studio blueprint {project}`
2. Fill `docs/architecture/`, create ADRs
3. User approves: `./studio approve {project} --gate 1`

## Phase 3 — Design direction (HUMAN GATE 2a)
1. `./studio design {project} --discovery`
2. Human answers `docs/design/discovery.md`; agent fills `design/DESIGN.md` (uniqueness, token names, no indigo)
3. User approves: `./studio approve {project} --gate 2a`

## Phase 3b — Project kit (HUMAN GATE 2b)
1. User chooses: `./studio design {project} --scope journey` OR `--scope core-views`
2. Build Next.js prototype in `design/prototype/` on **project** CSS tokens, coded A/M/O, sticker all-states
   - First `npm install` in that app **must** include UI kit peers (`docs/setup/ui-kit.md`)
3. User approves: `./studio approve {project} --gate 2b` — tickets; do **not** promote product look into studio-library

## Execution planning — Milestones (HITL)
1. Agent drafts `docs/phases/README.md` and one outline per version the PRD and its source files need
2. User approves: `./studio approve {project} --milestones`
3. Agent writes tickets for **active milestone only** → product backlog (`milestone: M0`)
4. See `.quinsy-studio/process/milestone-planning.md`

## Phase 4 — Sprint setup (within milestone)
Roles: Product Manager, Backlog Owner.
Artifact: backlog board with estimated tickets.
Create tickets: `./studio ticket {project} "<title>" --phase 3 --priority P1 --estimate M`.

## Phase 5 — Autonomous Sprint Execution
Roles: Frontend/Backend Engineer, Database Specialist.
Flow per sprint:
1. `./studio sprint {project}` → fill `sprints/SPRINT-NN/plan.md`.
2. Assign and work tickets via `./studio move` (9-step ticket workflow incl. reuse review).
3. `./studio groom {project}` → blocked review + prioritization.
4. Write `summary.md` + `retro.md`; start the next sprint.

## Phase 6 — Comprehensive QA
`./studio gate {project}` green; anti-slop audit 0 violations; every done ticket has a green QA gate.

## Phase 6 — Dual-Loop Knowledge Harvesting
Roles: Process Guard, Platform Architect.
Local loop: project-specific learnings → `docs/studio-learnings-local.md`.
Global loop: universal improvements → `.quinsy-studio/knowledge-base/`.

## Phase 7 — Deployment & Iteration
Roles: Platform Architect, Growth Manager.

## Rules (always)
- Every change/decision → ADR + update of the affected definitions file.
- UI kit peers stay in the React app package.json (`docs/setup/ui-kit.md`).
- If the agent can reach the DB (local or VPS), **the agent applies migrations** and informs the human. Do not dump migrate commands for the operator to run as sprint work. Destructive reset (`migrate:fresh`, drop) is HITL.
- No gate without complete exit criteria (`.quinsy-studio/process/gates.md`).
- No ticket without acceptance criteria and definition of done.
- No sprint without `summary.md` (Process Guard).
- Follow the anti-slop policy (`.quinsy-studio/knowledge-base/anti_ai_slop_protocol.md`).
- Human-in-the-loop: budget/legal/irreversible steps → decision record (`./studio decide`) + human approval.
- Watch for learning signals → `./studio learn "..." --signal ... --source ...`; the meta-retro decides improvements (`.quinsy-studio/process/learning-loop.md`).
"""
    
    runbook_file = project_dir / "RUNBOOK.md"
    runbook_file.write_text(content)
    print(f"  ✓ RUNBOOK.md created")

def init_docker(project_dir: Path, project: str):
    """Initialize Docker environment from the studio base template."""
    docker_dir = project_dir / "docker"
    docker_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy the base template from the studio and parameterize it per project
    template_dir = TEMPLATES_DIR / "docker"
    if not template_dir.exists():
        print(f"  ⚠ Base docker template missing: {template_dir}")
        return
    
    for f in template_dir.iterdir():
        if f.is_file():
            content = f.read_text()
            content = content.replace("{{PROJECT_NAME}}", project)
            (docker_dir / f.name).write_text(content)
    
    print(f"  ✓ Docker environment created (from base template, project-specific)")

def init_project_gitignore(project_dir: Path):
    """Copy project .gitignore template (project world, not studio HQ)."""
    tpl = TEMPLATES_DIR / "project.gitignore"
    dest = project_dir / ".gitignore"
    if tpl.exists() and not dest.exists():
        dest.write_text(tpl.read_text())
        print(f"  ✓ .gitignore created (project repo)")

def init_git(project_dir: Path):
    """Initialize Git repository."""
    try:
        subprocess.run(['git', 'init'], cwd=str(project_dir), capture_output=True)
        subprocess.run(['git', 'checkout', '-b', 'main'], cwd=str(project_dir), capture_output=True)
        print(f"  ✓ Git repository initialized")
    except Exception as e:
        print(f"  \033[93m⚠ Git init failed: {e}\033[0m")

# =============================================================================
# MAIN
# =============================================================================

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 init_project_env.py <project> [--archetype <type>]")
        sys.exit(1)
    
    project = sys.argv[1]
    archetype = 'saas-application'
    
    for i, arg in enumerate(sys.argv[2:], 2):
        if arg == '--archetype' and i + 1 < len(sys.argv):
            archetype = sys.argv[i + 1]
    
    init_project(project, archetype)

if __name__ == '__main__':
    main()
