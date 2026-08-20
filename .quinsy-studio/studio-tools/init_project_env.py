#!/usr/bin/env python3
"""
Project Environment Initializer — Automatisiert Git-Repos und Docker-Compose Bootstrapping.

Verwendung:
    python3 init_project_env.py <project> [--archetype <type>]
"""

import sys
import os
import json
import subprocess
from pathlib import Path
from datetime import datetime

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
    
    print(f"\n  Initialisiere Projekt: {project}")
    print(f"  Archetyp: {archetype}")
    
    # 1. Create directory structure
    create_directories(project_dir)
    
    # 2. Create status.json
    create_status(project_dir, project, archetype)
    
    # 3. Create agent-briefing.md
    create_agent_briefing(project_dir, project, archetype)
    
    # 4. Create RUNBOOK.md
    create_runbook(project_dir, project)
    
    # 5. Initialize Docker
    init_docker(project_dir, project)
    
    # 6. Initialize Git (optional)
    init_git(project_dir)
    
    print(f"\n  \033[92m✓ Projekt initialisiert: {project_dir}\033[0m")
    print(f"  Nächste Schritte:")
    print(f"    1. PRD erstellen: {project_dir}/docs/intake/prd.md")
    print(f"    2. Docker starten: ./studio env {project} up")
    print(f"    3. GitHub-Repo: ./studio repo {project} create")

def create_directories(project_dir: Path):
    """Create project directory structure."""
    dirs = [
        "docs/intake",
        "docs/definitions",
        "docs/adr",
        "docs/decisions",
        "docs/phases",
        "docs/modules",
        "design",
        "ui",
        "backlog/open",
        "backlog/done",
        "backlog/blocked",
        "sprints",
        "docker",
        "packages",
        "apps",
    ]
    
    for d in dirs:
        (project_dir / d).mkdir(parents=True, exist_ok=True)
    
    print(f"  ✓ Verzeichnisstruktur erstellt")

def create_status(project_dir: Path, project: str, archetype: str):
    """Create initial status.json."""
    status = {
        "name": project,
        "phase": "1",
        "gate": "0",
        "gate_status": "offen",
        "created": datetime.now().strftime("%Y-%m-%d"),
        "last_update": datetime.now().strftime("%Y-%m-%d"),
        "archetype": archetype,
        "current_sprint": None,
        "active_ticket": None,
        "gate_history": []
    }
    
    status_file = project_dir / "status.json"
    status_file.write_text(json.dumps(status, indent=2, ensure_ascii=False))
    print(f"  ✓ status.json erstellt")

def create_agent_briefing(project_dir: Path, project: str, archetype: str):
    """Create agent-briefing.md."""
    content = f"""# Agent-Briefing — {project}

Du führst das Projekt `{project}` autonom durch das Quinsy-Studio-Betriebssystem.
- **Archetyp:** {archetype} — Rollen/ADRs/Entscheidungen siehe `docs/intake/archetype-checklist.md` und `.quinsy-studio/process/project-archetypes.md`.

## Dein Auftrag
1. Lies `docs/intake/prd.md` und `docs/intake/validation.md`.
2. Führe **Phase 1 (Intake & PRD Processing)** aus: fülle `docs/definitions/`, kläre Details oder
   markiere sie als Annahmen, lege ADRs für Grundsatzentscheidungen an.
3. Bestätige **Gate 0**, dann arbeite **Phase 2 bis 7** ab (siehe `RUNBOOK.md`).
4. Ab Phase 3: arbeite **iterativ** — Backlog-Board, 9-Schritte-Ticket-Workflow,
   Grooming, Priorisierung, Sprints (`.quinsy-studio/process/iterative-delivery.md`).
5. Aktualisiere nach jedem Schritt `status.json` und die betroffene Dokumentation.
6. Beobachte **Lern-Signale** (Gate-Fail, Rework, Tooling-/Design-Lücke) und lege
   Learning Items an (`./studio learn "…" --signal … --source …`).

## Nicht verhandelbar
- `.quinsy-studio/process/` ist die verbindliche Referenz (Lifecycle, Gates, ADR, Anti-Slop, Iteration).
- Rollen-Skills liegen in `.quinsy-studio/teams/` — aktiviere die passende Rolle je Phase.
- Jede Entscheidung wird ein ADR; jedes ADR aktualisiert die benannte Dokumentation.
- Anti-Slop-Audit und QA-Gate müssen grün sein, bevor ein Gate als bestanden gilt.
- Kein `done`-Ticket ohne Definition of Done; kein Sprint ohne summary.md.
- Human-in-the-loop: blockierende Entscheidungen werden als Decision Record eskaliert und warten auf menschliche Freigabe (`.quinsy-studio/process/human-in-the-loop.md`).

## Werkzeuge
- `./studio status {project}` — Stand anzeigen
- `./studio gate {project}` — QA-Gate ausführen
- `./studio adr {project} "<Titel>"` — ADR anlegen
- `./studio ticket {project} "<Titel>"` — Ticket anlegen
- `./studio board {project}` / `./studio move {project} <id> <status>` — Board steuern
- `./studio sprint {project}` / `./studio groom {project}` — Sprint-Zyklus
- `./studio set-phase {project} <phase> --gate <n>` — Fortschritt festhalten
- `./studio decide {project} "<Titel>"` / `./studio decisions {project}` — Entscheidungen (HITL)
- `./studio env {project} init|up|down|status|logs` — Docker-Entwicklungsumgebung
- `./studio repo {project} create|status` — GitHub-Repo (nur mit expliziter Freigabe)
- `./studio learn "<Titel>" --signal …` / `./studio learn-list` / `./studio retro` — Studio-Learning-Loop
"""
    
    briefing_file = project_dir / "agent-briefing.md"
    briefing_file.write_text(content)
    print(f"  ✓ agent-briefing.md erstellt")

def create_runbook(project_dir: Path, project: str):
    """Create RUNBOOK.md."""
    content = f"""# RUNBOOK — {project}

Autonomer Ablauf von Intake bis Gate 7. Der Agent arbeitet dieses Dokument ab.

## Phase 1 — Intake & PRD Processing (Gate 0)
1. `docs/intake/validation.md` lesen; fehlende/leere PRD-Abschnitte schließen oder als
   Annahme in `docs/definitions/11-assumptions.md` markieren.
2. `docs/definitions/00-index.md` … `11-assumptions.md` befüllen (keine `_TODO_` mehr).
3. Grundsatzentscheidungen als ADR anlegen: `./studio adr {project} "<Titel>"`.
4. Gate 0 prüfen: PRD validiert, Definitions vollständig, Fragen/Annahmen explizit, ADRs da.

## Dev-Environment (nach Phase 1)
1. `./studio env {project} init` — Docker-Compose + Dockerfiles + Git-Init (main).
2. `./studio repo {project} create` — GitHub-Repo (nur mit Freigabe, kein Auto-Push).
3. `./studio env {project} up` — Postgres + Redis starten.

## Phase 2 — Architecture & Design Blueprinting (HUMAN-GATE 1)
Rollen: Systems Architect, Backend Architect, Frontend Architect.
Artefakt: Architecture Blueprint + UI-Specs.
**WARTEN AUF FREIGABE DES USERS.**

## Phase 3 — Sprint Setup & Backlog Grooming (Gate 3)
Rollen: Product Manager, Backlog Owner.
Artefakt: Backlog-Board mit geschätzten Tickets.
Tickets anlegen: `./studio ticket {project} "<Titel>" --phase 3 --priority P1 --estimate M`.

## Phase 4 — Autonomous Sprint Execution
Rollen: Frontend/Backend Engineer, Database Specialist.
Ablauf je Sprint:
1. `./studio sprint {project}` → `sprints/SPRINT-NN/plan.md` ausfüllen.
2. Tickets per `./studio move` zuordnen und abarbeiten (9-Schritte-Ticket-Workflow inkl. Reuse-Review).
3. `./studio groom {project}` → Blocked-Review + Priorisierung.
4. `summary.md` + `retro.md` schreiben; nächsten Sprint starten.

## Phase 5 — Comprehensive QA & Compliance Gate (Gate 5)
`./studio gate {project}` grün; Anti-Slop-Audit 0 Verstöße; jedes done-Ticket hat QA-Gate grün.

## Phase 6 — Dual-Loop Knowledge Harvesting
Rollen: Process Guard, Platform Architect.
Local Loop: Projektspezifische Learnings → `docs/local_learnings.md`.
Global Loop: Universelle Verbesserungen → `.quinsy-studio/knowledge-base/`.

## Phase 7 — Deployment & Iteration
Rollen: Platform Architect, Growth Manager.

## Regeln (immer)
- Jede Änderung/Entscheidung → ADR + Aktualisierung der betroffenen Definitions-Datei.
- Kein Gate ohne vollständige Exit-Kriterien (`.quinsy-studio/process/gates.md`).
- Kein Ticket ohne Akzeptanzkriterien und Definition of Done.
- Kein Sprint ohne `summary.md` (Process Guard).
- Anti-Slop-Policy beachten (`.quinsy-studio/knowledge-base/anti_ai_slop_protocol.md`).
- Human-in-the-loop: Budget/Recht/irreversible Schritte → Decision Record (`./studio decide`) + menschliche Freigabe.
- Lern-Signale beobachten → `./studio learn "…" --signal … --source …`; Meta-Retro entscheidet über Verbesserungen (`.quinsy-studio/process/learning-loop.md`).
"""
    
    runbook_file = project_dir / "RUNBOOK.md"
    runbook_file.write_text(content)
    print(f"  ✓ RUNBOOK.md erstellt")

def init_docker(project_dir: Path, project: str):
    """Initialize Docker environment from the studio base template."""
    docker_dir = project_dir / "docker"
    docker_dir.mkdir(parents=True, exist_ok=True)
    
    # Basis-Template aus dem Studio kopieren und projektspezifisch parametrisieren
    template_dir = TEMPLATES_DIR / "docker"
    if not template_dir.exists():
        print(f"  ⚠ Basis-Docker-Template fehlt: {template_dir}")
        return
    
    for f in template_dir.iterdir():
        if f.is_file():
            content = f.read_text()
            content = content.replace("{{PROJECT_NAME}}", project)
            (docker_dir / f.name).write_text(content)
    
    print(f"  ✓ Docker-Environment erstellt (aus Basis-Template, projektspezifisch)")

def init_git(project_dir: Path):
    """Initialize Git repository."""
    try:
        subprocess.run(['git', 'init'], cwd=str(project_dir), capture_output=True)
        subprocess.run(['git', 'checkout', '-b', 'main'], cwd=str(project_dir), capture_output=True)
        print(f"  ✓ Git-Repository initialisiert")
    except Exception as e:
        print(f"  \033[93m⚠ Git-Init fehlgeschlagen: {e}\033[0m")

# =============================================================================
# MAIN
# =============================================================================

def main():
    if len(sys.argv) < 2:
        print("Verwendung: python3 init_project_env.py <project> [--archetype <type>]")
        sys.exit(1)
    
    project = sys.argv[1]
    archetype = 'saas-application'
    
    for i, arg in enumerate(sys.argv[2:], 2):
        if arg == '--archetype' and i + 1 < len(sys.argv):
            archetype = sys.argv[i + 1]
    
    init_project(project, archetype)

if __name__ == '__main__':
    main()
