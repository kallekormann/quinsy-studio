#!/usr/bin/env python3
"""
Quinsy Studio — Haupt-Orchestrator

Dual-Speed Operating Model:
  CORE: Für neue Plattformen & komplexe Systeme (6 Phasen mit Human-Gates)
  LEAN: Für Iterationen & Features in bestehenden Projekten (4 Phasen)

Verwendung:
  ./studio <command> [args...]

Befehle:
  # Projektmanagement
  ./studio init <project> --archetype <type>     Projekt initialisieren
  ./studio start <project> --mode [core|lean]    Projekt starten
  ./studio status <project>                      Stand anzeigen
  ./studio board <project>                       Board anzeigen

  # Phase 1: Intake
  ./studio intake <project> <input-file>         Intake verarbeiten

  # Phase 2: Concept & Design
  ./studio concept <project>                     Konzept-Iteration starten
  ./studio approve <project> --gate <n>          Human-Gate abnehmen

  # Phase 3: Sprint Management
  ./studio sprint <project>                      Sprint anlegen
  ./studio ticket <project> "Title"              Ticket erstellen
  ./studio move <project> <id> <status>          Ticket bewegen
  ./studio groom <project>                       Grooming durchführen

  # Phase 4: Implementation
  ./studio gate <project> [--level N]            QA-Gate ausführen

  # Phase 6: Learning
  ./studio learn "Titel" --signal <s>            Learning Item anlegen
  ./studio learn-list                            Learning Items anzeigen
  ./studio retro <project>                       Retrospektive starten
  ./studio sync <project>                        Global Assets synchronisieren

  # Tools
  ./studio adr <project> "Titel"                 ADR anlegen
  ./studio decide <project> "Titel"              Decision Record anlegen
  ./studio env <project> init|up|down|status     Docker-Env
  ./studio repo <project> create|status          GitHub-Repo
  ./studio promote <project> <asset>             Asset zur Library promote
"""

import sys
import os
import json
import re
import subprocess
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

# =============================================================================
# CONFIGURATION
# =============================================================================

STUDIO_ROOT = Path(__file__).parent.parent.parent
QUINSY_STUDIO = STUDIO_ROOT / ".quinsy-studio"
PROCESS_DIR = QUINSY_STUDIO / "process"
TEAMS_DIR = QUINSY_STUDIO / "teams"
PROJECTS_DIR = STUDIO_ROOT / "projects"
STUDIO_LIBRARY = QUINSY_STUDIO / "studio-library"
TEMPLATES_DIR = QUINSY_STUDIO / "studio-templates"
BACKLOG_DIR = QUINSY_STUDIO / "backlog"
RETROS_DIR = QUINSY_STUDIO / "retros"
TOOLS_DIR = Path(__file__).parent

# =============================================================================
# UTILITIES
# =============================================================================

def ensure_dirs():
    """Stellt sicher, dass alle benötigten Verzeichnisse existieren."""
    for d in [QUINSY_STUDIO, PROCESS_DIR, TEAMS_DIR, PROJECTS_DIR,
              STUDIO_LIBRARY, BACKLOG_DIR, RETROS_DIR,
              BACKLOG_DIR / "open", BACKLOG_DIR / "done", BACKLOG_DIR / "blocked"]:
        d.mkdir(parents=True, exist_ok=True)

def slugify(text: str) -> str:
    """Konvertiert Text in URL-freundlichen Slug."""
    text = text.lower()
    text = re.sub(r'[äöüß]', lambda m: {'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'ß': 'ss'}[m.group()], text)
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')[:50]

def get_next_ticket_id(project: str) -> str:
    """Gibt die nächste Ticket-ID für ein Projekt zurück."""
    counter_file = PROJECTS_DIR / project / ".ticket_counter"
    if counter_file.exists():
        count = int(counter_file.read_text().strip()) + 1
    else:
        count = 1
    counter_file.write_text(str(count))
    return f"{project[:4].upper()}-{count:04d}"

def get_project_backlog_dir(project: str, status: str = "open") -> Path:
    """Gibt das Backlog-Verzeichnis für ein Projekt zurück."""
    backlog_dir = PROJECTS_DIR / project / "backlog"
    target_dir = backlog_dir / status
    target_dir.mkdir(parents=True, exist_ok=True)
    return target_dir

def find_project_ticket(project: str, ticket_id: str) -> tuple:
    """Findet ein Ticket im Projekt-Backlog. Gibt (filepath, current_status) zurück."""
    project_backlog = PROJECTS_DIR / project / "backlog"
    
    for status in ["open", "done", "blocked", "implement", "design", "analyze", "qa", "review", "reuse"]:
        ticket_dir = project_backlog / status
        if ticket_dir.exists():
            for f in ticket_dir.glob(f"{ticket_id}-*.md"):
                return f, status
    
    return None, None

def load_status(project: str) -> Dict:
    """Lädt den Projektstatus."""
    status_file = PROJECTS_DIR / project / "status.json"
    if status_file.exists():
        return json.loads(status_file.read_text())
    return {
        "name": project,
        "phase": "0",
        "gate": "0",
        "gate_status": "offen",
        "mode": "core",
        "created": datetime.now().strftime("%Y-%m-%d"),
        "last_update": datetime.now().strftime("%Y-%m-%d"),
        "archetype": "unknown",
        "current_sprint": None,
        "active_ticket": None,
        "gate_history": [],
        "human_gates": {}
    }

def save_status(project: str, status: Dict):
    """Speichert den Projektstatus."""
    status["last_update"] = datetime.now().strftime("%Y-%m-%d")
    status_file = PROJECTS_DIR / project / "status.json"
    status_file.parent.mkdir(parents=True, exist_ok=True)
    status_file.write_text(json.dumps(status, indent=2, ensure_ascii=False))

def print_header(title: str, char: str = "="):
    """Gibt einen formatierten Header aus."""
    width = 60
    print(f"\n{char * width}")
    print(f"  {title}")
    print(f"{char * width}")

def print_check(label: str, passed: bool, details: str = ""):
    """Gibt ein Prüf-Element aus."""
    status = "✓" if passed else "✗"
    color = "\033[92m" if passed else "\033[91m"
    reset = "\033[0m"
    detail_str = f" ({details})" if details else ""
    print(f"  {color}[{status}]{reset} {label}{detail_str}")

# =============================================================================
# DUAL-SPEED ORCHESTRATOR
# =============================================================================

class StudioOrchestrator:
    """Haupt-Orchestrator für das Dual-Speed Operating Model."""
    
    def __init__(self):
        ensure_dirs()
    
    # -------------------------------------------------------------------------
    # PROJECT MANAGEMENT
    # -------------------------------------------------------------------------
    
    def cmd_init(self, project: str, archetype: str = "saas-application"):
        """Initialisiert ein neues Projekt."""
        
        project_dir = PROJECTS_DIR / project
        project_dir.mkdir(parents=True, exist_ok=True)
        
        # Create directory structure
        dirs_to_create = [
            "docs/intake",
            "docs/adr",
            "docs/decisions",
            "docs/definitions",
            "design",
            "ui",
            "backlog/open",
            "backlog/done",
            "backlog/blocked",
            "sprints",
            "docker"
        ]
        
        for d in dirs_to_create:
            (project_dir / d).mkdir(parents=True, exist_ok=True)
        
        # Create status.json
        status = {
            "name": project,
            "phase": "0",
            "gate": "0",
            "gate_status": "offen",
            "mode": "core",
            "created": datetime.now().strftime("%Y-%m-%d"),
            "last_update": datetime.now().strftime("%Y-%m-%d"),
            "archetype": archetype,
            "current_sprint": None,
            "active_ticket": None,
            "gate_history": [],
            "human_gates": {}
        }
        save_status(project, status)
        
        print(f"\n  Projekt initialisiert: {project}")
        print(f"  Archetyp: {archetype}")
        print(f"  Verzeichnis: {project_dir}")
        print(f"\n  Nächste Schritte:")
        print(f"    1. PRD erstellen: {project_dir}/docs/intake/prd.md")
        print(f"    2. Intake verarbeiten: ./studio intake {project} <input-file>")
    
    def cmd_start(self, project: str, mode: str = "core"):
        """Startet ein Projekt im gewählten Modus."""
        
        status = load_status(project)
        status["mode"] = mode
        status["phase"] = "1"
        save_status(project, status)
        
        print_header(f"PROJEKT STARTEN: {project} (Mode: {mode.upper()})")
        
        if mode == "core":
            print(f"\n  CORE MODE — Vollständiger Prozess mit Human-Gates")
            print(f"\n  Phase 1: Intake & PRD Processing")
            print(f"    → PRD einlesen und validieren")
            print(f"    → Archetyp bestimmen")
            print(f"    → Ticket-Manifest generieren")
            print(f"\n  HUMAN-GATE 1: Architecture & Design Blueprint")
            print(f"    → Warten auf Freigabe nach Phase 2")
        else:
            print(f"\n  LEAN MODE — Schneller Feature-Durchlauf")
            print(f"\n  Phase 1: Ticket Drop")
            print(f"    → Ticket direkt in Backlog")
            print(f"\n  HUMAN-GATE 1: Quick Align")
            print(f"    → Kurzer technischer Lösungsweg")
    
    def cmd_status(self, project: str):
        """Zeigt den Projektstatus an."""
        
        status = load_status(project)
        
        print_header(f"PROJECT STATUS: {project}")
        print(f"  Mode:         {status.get('mode', 'core').upper()}")
        print(f"  Phase:        {status['phase']}")
        print(f"  Gate:         {status['gate']} ({status['gate_status']})")
        print(f"  Archetyp:     {status['archetype']}")
        print(f"  Sprint:       {status.get('current_sprint', '-')}")
        print(f"  Ticket:       {status.get('active_ticket', '-')}")
        print(f"  Erstellt:     {status['created']}")
        print(f"  Aktualisiert: {status['last_update']}")
        
        # Gate history
        if status.get('gate_history'):
            print(f"\n  Gate-Historie:")
            for entry in status['gate_history'][-5:]:
                print(f"    Gate {entry['gate']}: {entry['status']} ({entry.get('passed_at', entry.get('failed_at', '-'))})")
        
        # Human gates
        if status.get('human_gates'):
            print(f"\n  Human-Gates:")
            for gate_id, gate_info in status['human_gates'].items():
                print(f"    Gate {gate_id}: {gate_info['status']} ({gate_info.get('date', '-')})")
        
        # Open tickets (im Projekt-Backlog)
        project_backlog = PROJECTS_DIR / project / "backlog"
        open_dir = project_backlog / "open"
        if open_dir.exists():
            open_tickets = list(open_dir.glob(f"{project[:4].upper()}-*.md"))
            if open_tickets:
                print(f"\n  Offene Tickets: {len(open_tickets)}")
                for t in sorted(open_tickets)[:5]:
                    print(f"    - {t.stem}")
    
    # -------------------------------------------------------------------------
    # PHASE 1: INTAKE
    # -------------------------------------------------------------------------
    
    def cmd_intake(self, project: str, input_file: str):
        """Verarbeitet Intake-Input zu einem strukturierten PRD."""
        
        print_header(f"PHASE 1: INTAKE — {project}")
        
        # Run process_intake.py
        cmd = [
            sys.executable,
            str(TOOLS_DIR / "process_intake.py"),
            project,
            input_file
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result.stdout)
        
        if result.returncode != 0:
            print(f"\n  ❌ Intake-Verarbeitung fehlgeschlagen")
            if result.stderr:
                print(f"  Fehler: {result.stderr}")
            return False
        
        # Generate ticket manifest
        print(f"\n  Generiere Ticket-Manifest...")
        cmd = [
            sys.executable,
            str(TOOLS_DIR / "generate_ticket_manifest.py"),
            project
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result.stdout)
        
        # Update status
        status = load_status(project)
        status["phase"] = "1"
        status["gate"] = "0"
        status["gate_status"] = "intake-abgeschlossen"
        save_status(project, status)
        
        print(f"\n  ✅ Phase 1 abgeschlossen")
        print(f"  Nächster Schritt: ./studio start {project} --mode core")
        
        return True
    
    # -------------------------------------------------------------------------
    # PHASE 2: CONCEPT & DESIGN
    # -------------------------------------------------------------------------
    
    def cmd_concept(self, project: str):
        """Startet die Konzept- und Designphase."""
        
        status = load_status(project)
        
        if status["phase"] != "1":
            print(f"  ⚠️  Projekt ist in Phase {status['phase']}. Erwartet: Phase 1")
            return False
        
        print_header(f"PHASE 2: CONCEPT & DESIGN — {project}")
        
        print(f"\n  📋 Konzept-Iteration gestartet")
        print(f"\n  Director-Level Rollen aktiviert:")
        print(f"    • Lead Experience Architect — Informationsarchitektur, User Journeys")
        print(f"    • Senior Fullstack Architect — Backend-Schema, Frontend-Setup")
        print(f"    • UI/Interaction Designer — Design Tokens, Anti-Slop")
        
        # Check if PRD exists
        prd_file = PROJECTS_DIR / project / "docs" / "intake" / "prd.md"
        if prd_file.exists():
            prd_content = prd_file.read_text()
            print(f"\n  PRD geladen: {prd_file}")
            
            # Extract key information
            print(f"\n  Analyse des PRDs...")
            
            # Check for existing design docs
            design_dir = PROJECTS_DIR / project / "design"
            design_file = design_dir / "DESIGN.md"
            
            if not design_file.exists():
                print(f"\n  Erstelle DESIGN.md Template...")
                design_dir.mkdir(parents=True, exist_ok=True)
                
                design_template = f"""# Design Blueprint — {project}

> Erstellt: {datetime.now().strftime('%Y-%m-%d')}
> Status: draft (wartet auf Human-Gate 1)

## Architektur-Entscheidungen

| Entscheidung | Option | Status |
|-------------|--------|--------|
| Frontend-Framework | Next.js App Router | pending |
| Backend | Supabase + Laravel | pending |
| Database | PostgreSQL (Supabase) | pending |
| Deployment | Vercel | pending |

## UI-Spezifikation

### Design Tokens
- Farbpalette: [Zu definieren]
- Typografie: [Zu definieren]
- Spacing: 8px Grid

### Component Hierarchy
- Atoms: Button, Input, Badge
- Molecules: Card, Form, Modal
- Organisms: Header, Footer, Navigation

## Datenmodell

[ER-Diagramm wird in Phase 2 generiert]

## API-Kontrakte

[OpenAPI-Spezifikation wird in Phase 2 generiert]
"""
                design_file.write_text(design_template)
                print(f"    → {design_file}")
        
        # Update status
        status["phase"] = "2"
        save_status(project, status)
        
        print(f"\n  ═══════════════════════════════════════════════════════════════")
        print(f"  🛑 HUMAN-GATE 1: Architecture & Design Blueprint")
        print(f"  ═══════════════════════════════════════════════════════════════")
        print(f"\n  Der Agent wartet auf Ihre Freigabe.")
        print(f"  Bitte überprüfen Sie:")
        print(f"    1. {PROJECTS_DIR / project / 'design' / 'DESIGN.md'}")
        print(f"    2. Architektur-Entscheidungen")
        print(f"    3. UI-Spezifikation")
        print(f"\n  Um freizugeben:")
        print(f"    ./studio approve {project} --gate 1")
        print(f"\n  Um Änderungen anzufordern:")
        print(f"    ./studio concept {project} (mit Feedback)")
        
        return True
    
    def cmd_approve(self, project: str, gate: int):
        """Genehmigt ein Human-Gate."""
        
        status = load_status(project)
        
        if gate == 1:
            if status["phase"] != "2":
                print(f"  ⚠️  Gate 1 kann nur in Phase 2 genehmigt werden")
                return False
            
            print_header(f"HUMAN-GATE 1 FREIGEGEBEN: {project}")
            
            # Record approval
            if "human_gates" not in status:
                status["human_gates"] = {}
            
            status["human_gates"]["1"] = {
                "status": "approved",
                "date": datetime.now().isoformat(),
                "next_phase": "3"
            }
            
            status["phase"] = "3"
            status["gate"] = "1"
            status["gate_status"] = "freigegeben"
            
            save_status(project, status)
            
            print(f"\n  ✅ Architecture & Design Blueprint freigegeben")
            print(f"\n  Nächster Schritt:")
            print(f"    ./studio sprint {project}")
            print(f"    ./studio ticket {project} \"Erstes Feature\"")
            
            return True
        
        print(f"  ⚠️  Unbekanntes Gate: {gate}")
        return False
    
    # -------------------------------------------------------------------------
    # PHASE 3: SPRINT MANAGEMENT
    # -------------------------------------------------------------------------
    
    def cmd_sprint(self, project: str):
        """Erstellt einen neuen Sprint."""
        
        status = load_status(project)
        
        if status["phase"] not in ["3", "4"]:
            print(f"  ⚠️  Sprint kann nur in Phase 3/4 erstellt werden")
            return False
        
        print_header(f"PHASE 3: SPRINT PLANNING — {project}")
        
        # Determine next sprint number
        sprints_dir = PROJECTS_DIR / project / "sprints"
        sprints_dir.mkdir(parents=True, exist_ok=True)
        
        existing_sprints = list(sprints_dir.glob("SPRINT-*"))
        if existing_sprints:
            numbers = [int(re.search(r'SPRINT-(\d+)', f.name).group(1)) for f in existing_sprints]
            next_num = max(numbers) + 1
        else:
            next_num = 1
        
        sprint_name = f"SPRINT-{next_num:02d}"
        sprint_dir = sprints_dir / sprint_name
        sprint_dir.mkdir(exist_ok=True)
        
        # Create sprint plan
        plan_file = sprint_dir / "plan.md"
        plan_template = f"""# Sprint-Planung — {sprint_name}

**Projekt:** {project}
**Ziel:** <Was soll in diesem Sprint erreicht werden?>
**Start:** {datetime.now().strftime('%Y-%m-%d')}
**Ende:** YYYY-MM-DD
**Kapazität:** <realistische Einschätzung>

## Tickets in diesem Sprint

| Ticket | Titel | Phase | Priorität | Geschätzt |
|--------|-------|-------|-----------|-----------|
| ... | ... | ... | ... | ... |

## Abhängigkeiten
- ...

## Risiken
- ...

## Definition of Done
- [ ] Alle Tickets im Status "done"
- [ ] QA-Test grün
- [ ] Anti-Slop-Audit: 0 Error
- [ ] Retrospektive durchgeführt
- [ ] Summary geschrieben
"""
        plan_file.write_text(plan_template)
        
        # Update project status
        status["current_sprint"] = sprint_name
        status["phase"] = "4"
        save_status(project, status)
        
        print(f"\n  Sprint angelegt: {sprint_name}")
        print(f"  Verzeichnis: {sprint_dir}")
        print(f"\n  Nächster Schritt:")
        print(f"    ./studio ticket {project} \"Feature Name\"")
        
        return True
    
    def cmd_ticket(self, project: str, title: str, phase: int = 4, 
                   priority: str = "P1", estimate: str = "M"):
        """Erstellt ein neues Ticket im Projekt-Backlog."""
        
        ticket_id = get_next_ticket_id(project)
        slug = slugify(title)
        
        # Tickets liegen im Projekt-Backlog
        ticket_dir = get_project_backlog_dir(project, "open")
        ticket_file = ticket_dir / f"{ticket_id}-{slug}.md"
        
        template = f"""---
id: {ticket_id}
title: {title}
status: open
phase: {phase}
priority: {priority}
estimate: {estimate}
created: {datetime.now().strftime('%Y-%m-%d')}
assignee: 
---

# {ticket_id} — {title}

## Akzeptanzkriterien
- [ ] Kriterium 1
- [ ] Kriterium 2
- [ ] Kriterium 3

## Technische Anforderungen
...

## Abhängigkeiten
- ...

## Begründung
Warum ist dieses Ticket wichtig?
"""
        ticket_file.write_text(template)
        
        print(f"\n  Ticket angelegt: {ticket_file}")
        print(f"  ID: {ticket_id}")
        print(f"  Status: open")
        print(f"  Projekt: {project}")
        print(f"\n  Nächster Schritt:")
        print(f"    ./studio move {project} {ticket_id} analyze")
        
        return ticket_id
    
    def cmd_move(self, project: str, ticket_id: str, new_status: str, reason: str = ""):
        """Bewegt ein Ticket zu einem neuen Status im Projekt-Backlog."""
        
        # Find ticket in project backlog
        ticket_file, current_status = find_project_ticket(project, ticket_id)
        
        if not ticket_file:
            print(f"  Ticket {ticket_id} nicht gefunden in Projekt {project}")
            return False
        
        # Determine new directory (within project)
        new_dir = get_project_backlog_dir(project, new_status)
        new_file = new_dir / ticket_file.name
        
        # Update ticket content
        content = ticket_file.read_text()
        content = content.replace(f"status: {current_status}", f"status: {new_status}")
        content += f"\n\n## Status-Änderung\n- **Von:** {current_status}\n- **Nach:** {new_status}\n- **Datum:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n- **Grund:** {reason}\n"
        
        new_file.write_text(content)
        ticket_file.unlink()
        
        print(f"\n  Ticket {ticket_id}: {current_status} → {new_status}")
        print(f"  Projekt: {project}")
        if reason:
            print(f"  Grund: {reason}")
        
        # If moving to done, check if all tickets are done
        if new_status == "done":
            project_backlog = PROJECTS_DIR / project / "backlog"
            open_dir = project_backlog / "open"
            if open_dir.exists():
                open_tickets = list(open_dir.glob(f"{project[:4].upper()}-*.md"))
                if not open_tickets:
                    print(f"\n  🎉 Alle Tickets abgeschlossen!")
                    print(f"  Nächster Schritt:")
                    print(f"    ./studio gate {project} --level 5")
                    print(f"    ./studio retro {project}")
        
        return True
    
    # -------------------------------------------------------------------------
    # PHASE 4-5: QA GATE
    # -------------------------------------------------------------------------
    
    def cmd_gate(self, project: str, level: int = 5, anti_slop: bool = False):
        """Führt das QA-Gate aus."""
        
        print_header(f"PHASE 5: QA-GATE — {project} (Level {level})")
        
        # Run run_qa_gate.py
        cmd = [
            sys.executable,
            str(TOOLS_DIR / "run_qa_gate.py"),
            project,
            "--level", str(level)
        ]
        
        if anti_slop:
            cmd.append("--anti-slop")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result.stdout)
        
        # Update status
        status = load_status(project)
        
        if result.returncode == 0:
            status["gate"] = str(level)
            status["gate_status"] = "bestanden"
            if "gate_history" not in status:
                status["gate_history"] = []
            status["gate_history"].append({
                "gate": level,
                "status": "grün",
                "passed_at": datetime.now().isoformat()
            })
        else:
            status["gate_status"] = "fehlgeschlagen"
            if "gate_history" not in status:
                status["gate_history"] = []
            status["gate_history"].append({
                "gate": level,
                "status": "rot",
                "failed_at": datetime.now().isoformat()
            })
        
        save_status(project, status)
        
        return result.returncode == 0
    
    # -------------------------------------------------------------------------
    # PHASE 6: LEARNING
    # -------------------------------------------------------------------------
    
    def cmd_learn(self, title: str, signal: str, source: str = "Studio-Entwicklung"):
        """Erstellt ein Learning Item."""
        
        lo_dir = BACKLOG_DIR / "open"
        lo_dir.mkdir(parents=True, exist_ok=True)
        
        # Find next LO number
        existing_lo = list(lo_dir.glob("LO-*.md"))
        if existing_lo:
            numbers = [int(re.search(r'LO-(\d+)', f.stem).group(1)) for f in existing_lo]
            next_num = max(numbers) + 1
        else:
            next_num = 0
        
        lo_id = f"LO-{next_num:04d}"
        slug = slugify(title)
        lo_file = lo_dir / f"{lo_id}-{slug}.md"
        
        template = f"""---
id: {lo_id}
title: {title}
status: open
signal: {signal}
source: {source}
priority: P2
created: {datetime.now().strftime('%Y-%m-%d')}
updated: {datetime.now().strftime('%Y-%m-%d')}
---

# {lo_id} — {title}

## Beobachtung
Was ist passiert / was fehlt?

## Auswirkung
Welche Folge hatte das (Rework, Unsicherheit, Qualitätsrisiko)?

## Vorschlag
Wie soll Prozess / Skill / Tooling verbessert werden?

## Status
- [ ] Im Meta-Retro besprochen
- [ ] Umgesetzt (CHANGELOG.md-Eintrag, Version aktualisiert)
"""
        lo_file.write_text(template)
        
        print(f"\n  Learning Item angelegt: {lo_file}")
        print(f"  ID: {lo_id}")
        print(f"  Signal: {signal}")
        
        return lo_id
    
    def cmd_learn_list(self):
        """Zeigt alle Learning Items an."""
        
        print_header("LEARNING ITEMS")
        
        lo_dir = BACKLOG_DIR / "open"
        if not lo_dir.exists():
            print("  Keine Learning Items vorhanden")
            return
        
        los = list(lo_dir.glob("LO-*.md"))
        if not los:
            print("  Keine Learning Items vorhanden")
            return
        
        print(f"\n  Gesamt: {len(los)}")
        for lo in sorted(los):
            content = lo.read_text()
            signal_match = re.search(r'signal:\s*(\w+)', content)
            signal = signal_match.group(1) if signal_match else "unknown"
            print(f"  - {lo.stem} [Signal: {signal}]")
    
    def cmd_retro(self, project: str):
        """Startet eine Retrospektive."""
        
        retro_dir = QUINSY_STUDIO / "retros"
        retro_dir.mkdir(parents=True, exist_ok=True)
        
        date_str = datetime.now().strftime("%Y-%m-%d")
        retro_file = retro_dir / f"meta-retro-{date_str}.md"
        
        template = f"""# Meta-Retro — {date_str}

## Eingegangene Learning Items
- LO-0000: ...

## Skill-Review
| Skill | Qualitätssignal | Aktion |
|-------|-----------------|--------|
| ... | ... | ... |

## Entscheidungen
- ... (jede Änderung → CHANGELOG.md-Eintrag)

## Action Items
- [ ] ... (Owner: ...)
"""
        retro_file.write_text(template)
        
        print(f"\n  Retrospektive gestartet: {retro_file}")
        print(f"  Learning Items einbeziehen: ./studio learn-list")
        
        return retro_file
    
    def cmd_update_skills(self, extra_args=None):
        """Abonniert/aktualisiert die externen Skill-Dependencies (Agent-as-a-Dependency)."""
        
        print_header("EXTERNAL SKILLS UPDATE")
        print(f"\n  Lade externe Skill-Dependencies aus skill-dependencies.json...")
        
        cmd = [
            sys.executable,
            str(TOOLS_DIR / "import_external_skills.py")
        ]
        if extra_args:
            cmd += extra_args
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        
        if result.returncode != 0:
            print(f"\n  ❌ Update fehlgeschlagen")
            return False
        
        print(f"\n  ✅ External Skills aktualisiert")
        print(f"  Skills liegen unter: {QUINSY_STUDIO / 'external-skills'}")
        print(f"  Siehe auch: {QUINSY_STUDIO / 'external-skills' / 'INDEX.md'}")
        return True
    
    def cmd_sync(self, project: str):
        """Synchronisiert Global Assets aus dem Projekt."""
        
        print_header(f"GLOBAL ASSET SYNC — {project}")
        
        # Run sync_global_assets.py
        cmd = [
            sys.executable,
            str(TOOLS_DIR / "sync_global_assets.py"),
            project
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result.stdout)
        
        return result.returncode == 0
    
    # -------------------------------------------------------------------------
    # TOOLS
    # -------------------------------------------------------------------------
    
    def cmd_adr(self, project: str, title: str):
        """Erstellt ein Architecture Decision Record."""
        
        adr_dir = PROJECTS_DIR / project / "docs" / "adr"
        adr_dir.mkdir(parents=True, exist_ok=True)
        
        # Find next ADR number
        existing_adrs = list(adr_dir.glob("ADR-*.md"))
        if existing_adrs:
            numbers = [int(re.search(r'ADR-(\d+)', f.stem).group(1)) for f in existing_adrs]
            next_num = max(numbers) + 1
        else:
            next_num = 1
        
        adr_id = f"ADR-{next_num:04d}"
        adr_file = adr_dir / f"{adr_id}-{slugify(title)}.md"
        
        template = f"""# {adr_id}: {title}

**Status:** proposed
**Datum:** {datetime.now().strftime('%Y-%m-%d')}
**Entscheider:** 
**Betroffene Phasen:** 

## Kontext
Was ist die Situation? Welches Problem soll gelöst werden?

## Entscheidung
Was wurde entschieden?

## Begründung
Warum wurde diese Entscheidung getroffen?

## Alternativen
Welche Alternativen wurden erwogen?

### Alternative A: [Name]
- Vorteile: ...
- Nachteile: ...

### Alternative B: [Name]
- Vorteile: ...
- Nachteile: ...

## Konsequenzen
Was bedeutet diese Entscheidung für das Projekt?

### Positiv
- ...

### Negativ
- ...

### Risiken
- ...

## Metriken
Wie wird der Erfolg dieser Entscheidung gemessen?

## Follow-up
Welche nächsten Schritte ergeben sich?
"""
        adr_file.write_text(template)
        
        print(f"\n  ADR angelegt: {adr_file}")
        print(f"  Status: proposed")
        print(f"  Nächster Schritt: ADR ausfüllen und auf 'accepted' setzen")
        
        return adr_file
    
    def cmd_board(self, project: str):
        """Zeigt das Ticket-Board eines Projekts an."""
        
        print_header(f"BACKLOG BOARD: {project}")
        
        project_backlog = PROJECTS_DIR / project / "backlog"
        statuses = ["open", "blocked", "done"]
        
        for status in statuses:
            ticket_dir = project_backlog / status
            if ticket_dir.exists():
                tickets = list(ticket_dir.glob(f"{project[:4].upper()}-*.md"))
                print(f"\n  {status.upper()}: {len(tickets)}")
                for t in sorted(tickets)[:10]:
                    print(f"    - {t.stem}")
            else:
                print(f"\n  {status.upper()}: 0")
    
    def cmd_groom(self, project: str):
        """Führt ein Grooming durch."""
        
        status = load_status(project)
        sprint = status.get("current_sprint", "SPRINT-01")
        
        print_header(f"GROOMING: {project} ({sprint})")
        
        project_backlog = PROJECTS_DIR / project / "backlog"
        
        # Show blocked tickets
        blocked_dir = project_backlog / "blocked"
        if blocked_dir.exists():
            blocked = list(blocked_dir.glob(f"{project[:4].upper()}-*.md"))
            if blocked:
                print(f"\n  Blockierte Tickets: {len(blocked)}")
                for t in blocked:
                    print(f"    - {t.stem}")
        
        # Show open tickets
        open_dir = project_backlog / "open"
        if open_dir.exists():
            open_tickets = list(open_dir.glob(f"{project[:4].upper()}-*.md"))
            if open_tickets:
                print(f"\n  Offene Tickets: {len(open_tickets)}")
                for t in open_tickets:
                    print(f"    - {t.stem}")
        
        # Create grooming protocol
        sprint_dir = PROJECTS_DIR / project / "sprints" / sprint
        sprint_dir.mkdir(parents=True, exist_ok=True)
        grooming_file = sprint_dir / "grooming.md"
        
        grooming_template = f"""# Grooming-Protokoll — {sprint}

**Datum:** {datetime.now().strftime('%Y-%m-%d')}
**Teilnehmer:** Project Manager, ...

## Blockierte Tickets
| Ticket | Grund | Aktion |
|--------|-------|--------|
| ... | ... | ... |

## Priorisierungsänderungen
| Ticket | Neue Priorität | Grund |
|--------|---------------|-------|
| ... | ... | ... |

## Neue Tickets
| Ticket | Titel | Priorität |
|--------|-------|-----------|
| ... | ... | ... |

## Kapazitätsanpassungen
- ...

## Nächste Schritte
- ...
"""
        grooming_file.write_text(grooming_template)
        print(f"\n  Grooming-Protokoll: {grooming_file}")
        
        return grooming_file
    
    def cmd_decide(self, project: str, title: str):
        """Erstellt ein Decision Record."""
        
        decisions_dir = PROJECTS_DIR / project / "docs" / "decisions"
        decisions_dir.mkdir(parents=True, exist_ok=True)
        
        # Find next DR number
        existing_drs = list(decisions_dir.glob("DR-*.md"))
        if existing_drs:
            numbers = [int(re.search(r'DR-(\d+)', f.stem).group(1)) for f in existing_drs]
            next_num = max(numbers) + 1
        else:
            next_num = 1
        
        dr_id = f"DR-{next_num:04d}"
        dr_file = decisions_dir / f"{dr_id}-{slugify(title)}.md"
        
        template = f"""# {dr_id}: {title}

**Status:** pending
**Datum:** {datetime.now().strftime('%Y-%m-%d')}
**Angefordert von:** 
**Entscheidung durch:** 

## Entscheidung
Was soll entschieden werden?

## Kontext
Warum ist diese Entscheidung nötig?

## Optionen

### Option A: <Name>
- Vorteile: ...
- Nachteile: ...
- Kosten: ...

### Option B: <Name>
- Vorteile: ...
- Nachteile: ...
- Kosten: ...

## Empfehlung
Welche Option empfiehlt der Agent und warum?

## Risiken
Was kann schiefgehen?

## Konsequenzen
Was bedeutet die Entscheidung für das Projekt?
"""
        dr_file.write_text(template)
        
        print(f"\n  Decision Record angelegt: {dr_file}")
        print(f"  Status: pending")
        print(f"  Nächster Schritt: Entscheidung herbeiführen")
        
        return dr_file
    
    def cmd_decisions(self, project: str):
        """Zeigt alle Decision Records an."""
        
        decisions_dir = PROJECTS_DIR / project / "docs" / "decisions"
        
        print_header(f"DECISION RECORDS: {project}")
        
        if not decisions_dir.exists():
            print("  Keine Decision Records vorhanden")
            return
        
        drs = list(decisions_dir.glob("DR-*.md"))
        if not drs:
            print("  Keine Decision Records vorhanden")
            return
        
        print(f"\n  Gesamt: {len(drs)}")
        for dr in sorted(drs):
            content = dr.read_text()
            status_match = re.search(r'\*\*Status:\*\*\s*(\w+)', content)
            status = status_match.group(1) if status_match else "unknown"
            print(f"  - {dr.stem} [{status}]")
    
    def cmd_env(self, project: str, action: str):
        """Verwaltet die Docker-Umgebung."""
        
        docker_dir = PROJECTS_DIR / project / "docker"
        
        print_header(f"DOCKER ENV: {project}")
        
        if action == "init":
            docker_dir.mkdir(parents=True, exist_ok=True)
            
            # Basis-Template aus dem Studio kopieren und projektspezifisch parametrisieren
            template_dir = TEMPLATES_DIR / "docker"
            if not template_dir.exists():
                print(f"\n  ⚠️  Basis-Docker-Template fehlt: {template_dir}")
                return False
            
            for f in template_dir.iterdir():
                if f.is_file():
                    content = f.read_text()
                    content = content.replace("{{PROJECT_NAME}}", project)
                    (docker_dir / f.name).write_text(content)
            
            print(f"\n  Docker-Environment initialisiert: {docker_dir}")
            print(f"  Basis-Template: {template_dir}")
            print(f"  → docker-compose.yml, .env.example (projektparametrisiert)")
            print(f"\n  Projekt-spezifische Services (Mailpit, Worker, ...) hier ergänzen:")
            print(f"    {docker_dir}/docker-compose.yml")
            print(f"\n  Nächster Schritt:")
            print(f"    cd {docker_dir} && cp .env.example .env && docker-compose up -d")
        
        elif action == "up":
            print(f"\n  Starte Docker-Environment...")
            print(f"  (cd {docker_dir} && docker-compose up -d)")
        
        elif action == "down":
            print(f"\n  Stoppe Docker-Environment...")
            print(f"  (cd {docker_dir} && docker-compose down)")
        
        elif action == "status":
            print(f"\n  Überprüfe Docker-Status...")
            print(f"  (cd {docker_dir} && docker-compose ps)")
        
        elif action == "logs":
            print(f"\n  Zeige Docker-Logs...")
            print(f"  (cd {docker_dir} && docker-compose logs -f)")
    
    def cmd_repo(self, project: str, action: str):
        """Verwaltet das GitHub-Repository."""
        
        print_header(f"GITHUB REPO: {project}")
        
        if action == "create":
            print(f"\n  Repository erstellen: {project}")
            print(f"  (gh repo create {project} --private --source=.)")
            print(f"  ⚠️  Kein Auto-Push ohne explizite Freigabe!")
        
        elif action == "status":
            print(f"\n  Überprüfe Repository-Status...")
            print(f"  (gh repo view {project})")
    
    def cmd_promote(self, project: str, asset_path: str):
        """Fördert ein Asset zur Studio-Library."""
        
        source = PROJECTS_DIR / project / asset_path
        dest = STUDIO_LIBRARY / asset_path
        
        print_header(f"PROMOTE ASSET: {asset_path}")
        
        if not source.exists():
            print(f"\n  Quelle nicht gefunden: {source}")
            return False
        
        dest.parent.mkdir(parents=True, exist_ok=True)
        
        if source.is_dir():
            shutil.copytree(source, dest, dirs_exist_ok=True)
        else:
            shutil.copy2(source, dest)
        
        # Update manifest
        manifest_file = STUDIO_LIBRARY / "manifest.json"
        if manifest_file.exists():
            manifest = json.loads(manifest_file.read_text())
        else:
            manifest = {"assets": []}
        
        asset_name = Path(asset_path).name
        asset_entry = {
            "name": asset_name,
            "kind": "component" if "components" in asset_path else "package" if "packages" in asset_path else "page-type" if "page-types" in asset_path else "other",
            "source_project": project,
            "promoted": datetime.now().strftime("%Y-%m-%d"),
            "title": f"{asset_name} (promoted from {project})"
        }
        
        existing = [a for a in manifest["assets"] if a["name"] == asset_name]
        if existing:
            existing[0].update(asset_entry)
        else:
            manifest["assets"].append(asset_entry)
        
        manifest_file.write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
        
        print(f"\n  Asset promoted: {asset_path}")
        print(f"  Ziel: {dest}")
        print(f"  Manifest aktualisiert")
        
        return True

# =============================================================================
# HELP & MAIN
# =============================================================================

def print_help():
    """Gibt die Hilfe aus."""
    print("""
Quinsy Studio — Dual-Speed Autonomous Enterprise Agency

Verwendung:
  ./studio <command> [args...]

Befehle:
  # Projektmanagement
  ./studio init <project> --archetype <type>     Projekt initialisieren
  ./studio start <project> --mode [core|lean]    Projekt starten
  ./studio status <project>                      Stand anzeigen
  ./studio board <project>                       Board anzeigen

  # Phase 1: Intake
  ./studio intake <project> <input-file>         Intake verarbeiten

  # Phase 2: Concept & Design
  ./studio concept <project>                     Konzept-Iteration starten
  ./studio approve <project> --gate <n>          Human-Gate abnehmen

  # Phase 3: Sprint Management
  ./studio sprint <project>                      Sprint anlegen
  ./studio ticket <project> "Title"              Ticket erstellen
  ./studio move <project> <id> <status>          Ticket bewegen
  ./studio groom <project>                       Grooming durchführen

  # Phase 4-5: QA
  ./studio gate <project> [--level N]            QA-Gate ausführen

  # Phase 6: Learning
  ./studio learn "Titel" --signal <s>            Learning Item anlegen
  ./studio learn-list                            Learning Items anzeigen
  ./studio retro <project>                       Retrospektive starten
  ./studio sync <project>                        Global Assets synchronisieren
  ./studio update-skills                         Externe Skill-Pakete abonnieren/aktualisieren

  # Tools
  ./studio adr <project> "Titel"                 ADR anlegen
  ./studio decide <project> "Titel"              Decision Record anlegen
  ./studio decisions <project>                   Decision Records anzeigen
  ./studio env <project> init|up|down|status     Docker-Env (Basis-Template)
  ./studio repo <project> create|status          GitHub-Repo
  ./studio promote <project> <asset>             Asset zur Library promote

Dual-Speed Operating Model:
  CORE — Für neue Plattformen & komplexe Systeme (6 Phasen mit Human-Gates)
  LEAN — Für Iterationen & Features in bestehenden Projekten (4 Phasen)

Beispiele:
  ./studio init nudge --archetype saas-application
  ./studio intake nudge intake/nudge-raw.md
  ./studio start nudge --mode core
  ./studio concept nudge
  ./studio approve nudge --gate 1
  ./studio sprint nudge
  ./studio ticket nudge "Button Component" --phase 3 --priority P1
  ./studio move nudge NUDG-0001 implement --reason "Implementierung gestartet"
  ./studio gate nudge --level 5
  ./studio learn "Gate-Check dauert zu lange" --signal tooling-gap
  ./studio sync nudge
""")

def main():
    orchestrator = StudioOrchestrator()
    
    if len(sys.argv) < 2:
        print_help()
        return
    
    command = sys.argv[1]
    
    # Parse arguments
    args = sys.argv[2:]
    
    if command == "init" and len(args) >= 1:
        project = args[0]
        archetype = "saas-application"
        for i, arg in enumerate(args):
            if arg == "--archetype" and i + 1 < len(args):
                archetype = args[i + 1]
        orchestrator.cmd_init(project, archetype)
    
    elif command == "start" and len(args) >= 1:
        project = args[0]
        mode = "core"
        for i, arg in enumerate(args):
            if arg == "--mode" and i + 1 < len(args):
                mode = args[i + 1]
        orchestrator.cmd_start(project, mode)
    
    elif command == "status" and len(args) >= 1:
        orchestrator.cmd_status(args[0])
    
    elif command == "intake" and len(args) >= 2:
        orchestrator.cmd_intake(args[0], args[1])
    
    elif command == "concept" and len(args) >= 1:
        orchestrator.cmd_concept(args[0])
    
    elif command == "approve" and len(args) >= 1:
        project = args[0]
        gate = 1
        for i, arg in enumerate(args):
            if arg == "--gate" and i + 1 < len(args):
                gate = int(args[i + 1])
        orchestrator.cmd_approve(project, gate)
    
    elif command == "sprint" and len(args) >= 1:
        orchestrator.cmd_sprint(args[0])
    
    elif command == "ticket" and len(args) >= 2:
        project = args[0]
        title = args[1]
        phase = 4
        priority = "P1"
        estimate = "M"
        for i, arg in enumerate(args):
            if arg == "--phase" and i + 1 < len(args):
                phase = int(args[i + 1])
            elif arg == "--priority" and i + 1 < len(args):
                priority = args[i + 1]
            elif arg == "--estimate" and i + 1 < len(args):
                estimate = args[i + 1]
        orchestrator.cmd_ticket(project, title, phase, priority, estimate)
    
    elif command == "move" and len(args) >= 3:
        project = args[0]
        ticket_id = args[1]
        new_status = args[2]
        reason = ""
        for i, arg in enumerate(args):
            if arg == "--reason" and i + 1 < len(args):
                reason = args[i + 1]
        orchestrator.cmd_move(project, ticket_id, new_status, reason)
    
    elif command == "gate" and len(args) >= 1:
        project = args[0]
        level = 5
        anti_slop = False
        for i, arg in enumerate(args):
            if arg == "--level" and i + 1 < len(args):
                level = int(args[i + 1])
            elif arg == "--anti-slop":
                anti_slop = True
        orchestrator.cmd_gate(project, level, anti_slop)
    
    elif command == "learn" and len(args) >= 1:
        title = args[0]
        signal = "process-gap"
        source = "Studio-Entwicklung"
        for i, arg in enumerate(args):
            if arg == "--signal" and i + 1 < len(args):
                signal = args[i + 1]
            elif arg == "--source" and i + 1 < len(args):
                source = args[i + 1]
        orchestrator.cmd_learn(title, signal, source)
    
    elif command == "learn-list":
        orchestrator.cmd_learn_list()
    
    elif command == "retro" and len(args) >= 1:
        orchestrator.cmd_retro(args[0])
    
    elif command == "update-skills":
        orchestrator.cmd_update_skills(args)
    
    elif command == "sync" and len(args) >= 1:
        orchestrator.cmd_sync(args[0])
    
    elif command == "adr" and len(args) >= 2:
        orchestrator.cmd_adr(args[0], args[1])
    
    elif command == "board" and len(args) >= 1:
        orchestrator.cmd_board(args[0])
    
    elif command == "groom" and len(args) >= 1:
        orchestrator.cmd_groom(args[0])
    
    elif command == "decide" and len(args) >= 2:
        orchestrator.cmd_decide(args[0], args[1])
    
    elif command == "decisions" and len(args) >= 1:
        orchestrator.cmd_decisions(args[0])
    
    elif command == "env" and len(args) >= 2:
        orchestrator.cmd_env(args[0], args[1])
    
    elif command == "repo" and len(args) >= 2:
        orchestrator.cmd_repo(args[0], args[1])
    
    elif command == "promote" and len(args) >= 2:
        orchestrator.cmd_promote(args[0], args[1])
    
    else:
        print_help()

if __name__ == "__main__":
    main()
