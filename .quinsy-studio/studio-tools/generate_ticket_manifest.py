#!/usr/bin/env python3
"""
generate_ticket_manifest.py — Ticket-Generierung für Quinsy Studio

Liest ein validiertes PRD und bricht es in verknüpfte Markdown/JSON-Tickets
herunter, inkl. Akzeptanzkriterien, Abhängigkeiten und Schätzungen.

Verwendung:
  python3 generate_ticket_manifest.py <project>
  python3 generate_ticket_manifest.py nudge

Output:
  projects/<project>/backlog/open/TICKET-NNNN-<slug>.md
  projects/<project>/docs/ticket-manifest.json
"""

import sys
import os
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# =============================================================================
# CONFIGURATION
# =============================================================================

STUDIO_ROOT = Path(__file__).parent.parent.parent
PROJECTS_DIR = STUDIO_ROOT / "projects"

# =============================================================================
# FEATURE EXTRACTION FROM PRD
# =============================================================================

def extract_features_from_prd(prd_content: str) -> List[Dict]:
    """
    Extrahiert Features aus dem PRD basierend auf:
    - Aufzählungen in "In Scope" Sektion
    - Funktionsanforderungen
    - User Stories
    """
    features = []
    
    # Find "In Scope" section - try multiple patterns
    scope_patterns = [
        r'##\s+Umfang.*?###\s+In Scope.*?\n(.*?)(?=###|##|\Z)',
        r'###\s+In Scope.*?\n(.*?)(?=###|##|\Z)',
        r'In Scope.*?\n(.*?)(?=Out of Scope|###|##|\Z)',
    ]
    
    for pattern in scope_patterns:
        scope_match = re.search(pattern, prd_content, re.DOTALL | re.IGNORECASE)
        if scope_match:
            scope_text = scope_match.group(1)
            features.extend(extract_bullet_features(scope_text, "scope"))
            if features:  # Stop if we found features
                break
    
    # Find functional requirements
    req_patterns = [
        r'##\s+Anforderungen.*?###\s+Funktionale.*?\n(.*?)(?=###|##|\Z)',
        r'###\s+Funktionale.*?\n(.*?)(?=###|##|\Z)',
        r'Funktionale Anforderungen.*?\n(.*?)(?=Nicht-funktionale|###|##|\Z)',
    ]
    
    for pattern in req_patterns:
        req_match = re.search(pattern, prd_content, re.DOTALL | re.IGNORECASE)
        if req_match:
            req_text = req_match.group(1)
            features.extend(extract_bullet_features(req_text, "requirement"))
            if features:  # Stop if we found features
                break
    
    # If still no features, scan entire document for bullet points
    if not features:
        # Find all bullet points that look like features
        all_bullets = re.finditer(r'^[\-\*]\s+\*?\*?(.+?)\*?\*?\s*:?:?\s*(.*)', prd_content, re.MULTILINE)
        for match in all_bullets:
            name = match.group(1).strip()
            description = match.group(2).strip()
            
            # Skip category headers and short names
            if len(name) < 5 or name.startswith('**'):
                continue
            
            # Clean up
            name = re.sub(r'^[*_]+', '', name).strip()
            name = re.sub(r'[*_]+$', '', name).strip()
            name = name.rstrip(':').strip()
            
            if len(name) >= 5:
                features.append({
                    "type": "feature",
                    "name": name,
                    "description": description,
                    "source": "prd",
                    "priority": "P0"
                })
    
    # Find user stories (pattern: "Als ... will ... damit ...")
    story_pattern = re.compile(
        r'(?:ALS|als)\s+(.+?)\s+(?:WILL|will)\s+(.+?)\s+(?:DAMIT|damit)\s+(.+?)(?:\.|$)',
        re.MULTILINE
    )
    
    for match in story_pattern.finditer(prd_content):
        features.append({
            "type": "user_story",
            "actor": match.group(1).strip(),
            "action": match.group(2).strip(),
            "benefit": match.group(3).strip(),
            "priority": "P0"
        })
    
    # Deduplicate features by name
    seen_names = set()
    unique_features = []
    for f in features:
        name = f.get('name', f.get('action', '')).lower().strip()
        if name and name not in seen_names:
            seen_names.add(name)
            unique_features.append(f)
    
    return unique_features


def extract_bullet_features(text: str, source: str) -> List[Dict]:
    """Extrahiert Features aus Aufzählungen."""
    features = []
    
    lines = text.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Skip category headers (e.g., "* **In Scope (P0):**")
        if re.match(r'^[\-\*]\s+\*\*[^*]+\*\*\s*:?\s*$', line):
            continue
        
        # Check for bullet point with content
        # Handle both * and - bullets, with optional **bold** text
        bullet_match = re.match(r'^[\-\*]\s+\*\*(.+?)\*\*\s*:?:?\s*(.*)', line)
        if not bullet_match:
            bullet_match = re.match(r'^[\-\*]\s+(.+?)\s*:?:?\s*(.*)', line)
        if bullet_match:
            name = bullet_match.group(1).strip()
            description = bullet_match.group(2).strip()
            
            # Skip empty or very short names (single characters, just punctuation)
            if len(name) < 3:
                continue
            
            # Skip if name is just a label prefix like "P0:" or "P1:"
            if re.match(r'^[Pp]\d:\s*$', name):
                continue
            
            # Clean up name - remove leading/trailing punctuation and bold markers
            name = re.sub(r'^[*_]+', '', name).strip()
            name = re.sub(r'[*_]+$', '', name).strip()
            name = name.rstrip(':').strip()
            
            # Skip if name is now empty or too short
            if len(name) < 3:
                continue
            
            # Determine priority from prefix
            priority = "P0"
            if "p1" in name.lower() or "p1" in description.lower():
                priority = "P1"
            elif "p2" in name.lower() or "p2" in description.lower():
                priority = "P2"
            
            features.append({
                "type": "feature",
                "name": name,
                "description": description,
                "source": source,
                "priority": priority
            })
    
    return features


def extract_archetype_from_prd(prd_content: str) -> str:
    """Extrahiert den Archetyp aus dem PRD."""
    # First check for explicit archetype mention
    match = re.search(r'Archetyp[:\s]*([\w\s-]+)', prd_content, re.IGNORECASE)
    if match:
        archetype_text = match.group(1).strip().lower()
        # Map common variations
        if 'saas' in archetype_text or 'micro-saas' in archetype_text:
            return "saas-application"
        if 'mobile' in archetype_text or 'app' in archetype_text:
            return "mobile-app"
        if 'shop' in archetype_text or 'ecommerce' in archetype_text:
            return "e-commerce"
        if 'api' in archetype_text:
            return "api-service"
        if 'content' in archetype_text or 'blog' in archetype_text:
            return "content-platform"
        return archetype_text.replace(' ', '-')
    
    # Fallback: detect from content (check SaaS FIRST as it's more specific)
    text = prd_content.lower()
    
    # Check SaaS indicators first (more specific than generic "app")
    if any(w in text for w in ["saas", "subscription", "abo", "freemium", "pro-tier", "free-tier"]):
        return "saas-application"
    if any(w in text for w in ["shop", "warenkorb", "produkt", "e-commerce"]):
        return "e-commerce"
    if any(w in text for w in ["api", "webhook", "endpoint", "microservice"]):
        return "api-service"
    if any(w in text for w in ["blog", "artikel", "content", "publishing"]):
        return "content-platform"
    # Only check mobile-app if no SaaS indicators found
    if any(w in text for w in ["ios", "android", "pwa", "progressive web app"]):
        return "mobile-app"
    
    return "saas-application"

# =============================================================================
# TICKET GENERATION
# =============================================================================

def generate_tickets_from_features(
    features: List[Dict], 
    project: str,
    archetype: str
) -> List[Dict]:
    """Generiert Tickets aus extrahierten Features."""
    
    tickets = []
    ticket_counter = 1
    
    # Phase-based ticket generation
    phase_mapping = {
        "setup": 2,
        "architecture": 2,
        "design": 3,
        "ui": 3,
        "ux": 3,
        "frontend": 4,
        "backend": 4,
        "api": 4,
        "database": 4,
        "auth": 4,
        "test": 5,
        "qa": 5,
        "deploy": 7,
        "seo": 5,
        "content": 5
    }
    
    # First: generate infrastructure/setup tickets
    setup_tickets = generate_setup_tickets(project, archetype)
    tickets.extend(setup_tickets)
    ticket_counter += len(setup_tickets)
    
    # Then: generate feature tickets
    for feature in features:
        ticket = create_ticket_from_feature(
            feature, project, ticket_counter, phase_mapping
        )
        if ticket:
            tickets.append(ticket)
            ticket_counter += 1
    
    # Add dependency links
    tickets = resolve_dependencies(tickets)
    
    return tickets


def generate_setup_tickets(project: str, archetype: str) -> List[Dict]:
    """Generiert Setup-Tickets für ein neues Projekt."""
    
    tickets = []
    
    # Ticket 1: Project Setup
    tickets.append({
        "id": f"{project[:4].upper()}-0001",
        "title": "Projekt-Setup & Tooling",
        "description": f"Monorepo, Dependencies, Linting, CI/CD für {archetype} aufsetzen",
        "phase": 2,
        "priority": "P0",
        "estimate": "M",
        "skills": ["PE-001", "PE-002"],
        "team": "08-platform-enterprise-engineering",
        "acceptance_criteria": [
            "Monorepo initialisiert (Turborepo/pnpm)",
            "Linting konfiguriert (ESLint, Prettier)",
            "TypeScript konfiguriert",
            "Build-Script funktioniert",
            "Test-Framework eingerichtet"
        ],
        "dependencies": []
    })
    
    # Ticket 2: Design System
    tickets.append({
        "id": f"{project[:4].upper()}-0002",
        "title": "Design System & Tokens",
        "description": "Design Tokens, Farbpalette, Typografie, Spacing definieren",
        "phase": 2,
        "priority": "P0",
        "estimate": "M",
        "skills": ["FE-002"],
        "team": "01-frontend-experience",
        "acceptance_criteria": [
            "Design Tokens (JSON) definiert",
            "CSS Custom Properties generiert",
            "Dark/Light Mode unterstützt",
            "Typografie-Skala definiert",
            "Spacing-System definiert"
        ],
        "dependencies": [f"{project[:4].upper()}-0001"]
    })
    
    # Ticket 3: Database Schema
    tickets.append({
        "id": f"{project[:4].upper()}-0003",
        "title": "Datenbank-Schema & Migrationen",
        "description": "Primäre Datenbank-Tabellen und Migrationen definieren",
        "phase": 2,
        "priority": "P0",
        "estimate": "M",
        "skills": ["BE-002"],
        "team": "02-backend-systems",
        "acceptance_criteria": [
            "ER-Diagramm definiert",
            "Migrationen erstellt",
            "Seeds für Test-Daten",
            "Indexierung definiert"
        ],
        "dependencies": [f"{project[:4].upper()}-0001"]
    })
    
    # Ticket 4: Auth Setup
    tickets.append({
        "id": f"{project[:4].upper()}-0004",
        "title": "Authentifizierung & Autorisierung",
        "description": "Login, Registration, Session-Management, RBAC",
        "phase": 3,
        "priority": "P0",
        "estimate": "L",
        "skills": ["BE-003"],
        "team": "02-backend-systems",
        "acceptance_criteria": [
            "Login/Registration funktioniert",
            "JWT/Session korrekt implementiert",
            "Passwort-Hashing (bcrypt)",
            "RBAC funktioniert",
            "Logout funktioniert"
        ],
        "dependencies": [
            f"{project[:4].upper()}-0001",
            f"{project[:4].upper()}-0003"
        ]
    })
    
    return tickets


def create_ticket_from_feature(
    feature: Dict,
    project: str,
    counter: int,
    phase_mapping: Dict
) -> Optional[Dict]:
    """Erstellt ein Ticket aus einem extrahierten Feature."""
    
    # Bestimme Phase basierend auf Feature-Inhalten
    feature_text = json.dumps(feature).lower()
    phase = 4  # Default: Implementierung
    
    for keyword, p in phase_mapping.items():
        if keyword in feature_text:
            phase = p
            break
    
    # Bestimme Skills
    skills = determine_skills_for_feature(feature_text)
    
    # Bestimme Team
    team = determine_team_for_skills(skills)
    
    # Generiere Ticket-ID
    ticket_id = f"{project[:4].upper()}-{counter:04d}"
    
    # Bestimme Titel
    title = feature.get("name", feature.get("action", "Feature"))
    
    # Bestimme Beschreibung
    if feature.get("type") == "user_story":
        description = f"Als {feature['actor']} will ich {feature['action']}, damit {feature['benefit']}"
    else:
        description = feature.get("description", title)
    
    # Akzeptanzkriterien
    acceptance_criteria = generate_acceptance_criteria(feature)
    
    return {
        "id": ticket_id,
        "title": title,
        "description": description,
        "phase": phase,
        "priority": feature.get("priority", "P1"),
        "estimate": estimate_effort(feature),
        "skills": skills,
        "team": team,
        "acceptance_criteria": acceptance_criteria,
        "dependencies": []
    }


def determine_skills_for_feature(text: str) -> List[str]:
    """Bestimmt relevante Skills für ein Feature."""
    
    skill_mapping = {
        "ui": ["FE-001", "FE-002"],
        "component": ["FE-001"],
        "button": ["FE-001"],
        "card": ["FE-001"],
        "modal": ["FE-001"],
        "form": ["FE-001"],
        "design": ["FE-002"],
        "token": ["FE-002"],
        "theme": ["FE-002"],
        "performance": ["FE-003"],
        "speed": ["FE-003"],
        "cache": ["FE-003"],
        "a11y": ["FE-004"],
        "accessibility": ["FE-004"],
        "pwa": ["FE-005"],
        "offline": ["FE-005"],
        "service worker": ["FE-005"],
        "test": ["FE-006"],
        "api": ["BE-001"],
        "endpoint": ["BE-001"],
        "rest": ["BE-001"],
        "database": ["BE-002"],
        "schema": ["BE-002"],
        "migration": ["BE-002"],
        "auth": ["BE-003"],
        "login": ["BE-003"],
        "jwt": ["BE-003"],
        "session": ["BE-003"],
        "error": ["BE-004"],
        "retry": ["BE-004"],
        "webhook": ["BE-005"],
        "stripe": ["BE-005"],
        "payment": ["BE-005"],
        "dsgvo": ["CL-001"],
        "gdpr": ["CL-001"],
        "privacy": ["CL-001"],
        "cookie": ["CL-002"],
        "consent": ["CL-002"],
        "seo": ["GM-001"],
        "ranking": ["GM-001"],
        "aeo": ["GM-002"],
        "ai search": ["GM-002"],
        "content": ["GM-003"],
        "blog": ["GM-003"],
        "security": ["PE-003"],
        "owasp": ["PE-003"],
        "monitoring": ["PE-004"],
        "deploy": ["PE-001"],
        "docker": ["PE-001"],
        "ci/cd": ["PE-002"],
        "pipeline": ["PE-002"]
    }
    
    skills = []
    for keyword, skill_ids in skill_mapping.items():
        if keyword in text:
            skills.extend(skill_ids)
    
    # Deduplicate while preserving order
    seen = set()
    unique_skills = []
    for skill in skills:
        if skill not in seen:
            seen.add(skill)
            unique_skills.append(skill)
    
    return unique_skills[:5]  # Max 5 skills per ticket


def determine_team_for_skills(skills: List[str]) -> str:
    """Bestimmt das Team basierend auf den Skills."""
    
    team_mapping = {
        "FE": "01-frontend-experience",
        "BE": "02-backend-systems",
        "CL": "03-compliance-legal",
        "PS": "04-product-strategy-architecture",
        "GM": "05-growth-marketing-content",
        "PM": "06-product-management-operating-model",
        "AI": "07-ai-autonomous-systems",
        "PE": "08-platform-enterprise-engineering",
        "SO": "09-studio-operations-evolution"
    }
    
    for skill in skills:
        prefix = skill.split("-")[0]
        if prefix in team_mapping:
            return team_mapping[prefix]
    
    return "01-frontend-experience"  # Default


def generate_acceptance_criteria(feature: Dict) -> List[str]:
    """Generiert Akzeptanzkriterien für ein Feature."""
    
    criteria = []
    
    if feature.get("type") == "user_story":
        criteria.append(f"Feature ist für {feature.get('actor', 'Nutzer')} nutzbar")
        criteria.append(f"{feature.get('action', 'Aktion')} funktioniert wie beschrieben")
        criteria.append(f"{feature.get('benefit', 'Nutzen')} wird erreicht")
    else:
        name = feature.get("name", "Feature")
        criteria.append(f"{name} ist implementiert")
        criteria.append(f"{name} hat Unit-Tests")
        criteria.append(f"{name} ist dokumentiert")
    
    # Always add quality criteria
    criteria.append("Code ist AI-slop-frei")
    criteria.append("Barrierefreiheit geprüft (falls UI)")
    
    return criteria


def estimate_effort(feature: Dict) -> str:
    """Schätzt den Aufwand für ein Feature."""
    
    text = json.dumps(feature).lower()
    
    # Simple heuristics
    if any(w in text for w in ["komplex", "complex", "viel", "umfangreich"]):
        return "XL"
    if any(w in text for w in ["einfach", "simple", "klein", "quick"]):
        return "S"
    if any(w in text for w in ["medium", "mittel", "moderat"]):
        return "M"
    
    return "M"  # Default

# =============================================================================
# DEPENDENCY RESOLUTION
# =============================================================================

def resolve_dependencies(tickets: List[Dict]) -> List[Dict]:
    """Verknüpft Tickets mit Abhängigkeiten basierend auf Phasen und Skills."""
    
    for i, ticket in enumerate(tickets):
        # Setup-Tickets haben keine Abhängigkeiten (außer intern)
        if ticket["id"].endswith(("0001", "0002", "0003")):
            continue
        
        # Features depend on setup
        setup_deps = [t["id"] for t in tickets[:4] 
                     if t["id"].endswith(("0001",))]
        if setup_deps:
            ticket["dependencies"].extend(setup_deps)
        
        # Features in later phases depend on earlier phases
        for other in tickets:
            if other["id"] == ticket["id"]:
                continue
            if other["phase"] < ticket["phase"]:
                # Check if skills overlap (same domain)
                if set(ticket["skills"][:1]) & set(other["skills"][:1]):
                    if other["id"] not in ticket["dependencies"]:
                        ticket["dependencies"].append(other["id"])
    
    # Deduplicate dependencies
    for ticket in tickets:
        ticket["dependencies"] = list(dict.fromkeys(ticket["dependencies"]))
    
    return tickets

# =============================================================================
# TICKET FILE GENERATION
# =============================================================================

def get_ticket_counter(project: str) -> int:
    """Liest den nächsten freien Ticket-Counter des Projekts."""
    counter_file = PROJECTS_DIR / project / ".ticket_counter"
    if counter_file.exists():
        try:
            return int(counter_file.read_text().strip())
        except ValueError:
            pass
    return 0


def set_ticket_counter(project: str, count: int):
    """Setzt den Ticket-Counter des Projekts."""
    counter_file = PROJECTS_DIR / project / ".ticket_counter"
    counter_file.parent.mkdir(parents=True, exist_ok=True)
    counter_file.write_text(str(count))


def assign_sequential_ids(tickets: List[Dict], project: str) -> List[Dict]:
    """Weist Tickets fortlaufende IDs ab dem bestehenden Counter zu und remappt
    Abhängigkeiten. Verhindert Kollisionen mit manuell angelegten Tickets."""
    prefix = project[:4].upper()
    start = get_ticket_counter(project)
    
    # Alte → neue ID Zuordnung
    id_map = {}
    counter = start
    for ticket in tickets:
        old_id = ticket["id"]
        counter += 1
        new_id = f"{prefix}-{counter:04d}"
        id_map[old_id] = new_id
        ticket["id"] = new_id
    
    # Abhängigkeiten remappen
    for ticket in tickets:
        ticket["dependencies"] = [
            id_map.get(dep, dep) for dep in ticket["dependencies"]
        ]
    
    set_ticket_counter(project, counter)
    return tickets


def write_ticket_files(tickets: List[Dict], project: str):
    """Schreibt Ticket-Dateien in das Projekt-Backlog."""
    
    # Fortlaufende IDs ab bestehendem Counter (keine Kollisionen mit manuellen Tickets)
    tickets = assign_sequential_ids(tickets, project)
    
    # Tickets liegen im Projekt-Backlog
    backlog_open = PROJECTS_DIR / project / "backlog" / "open"
    backlog_open.mkdir(parents=True, exist_ok=True)
    
    for ticket in tickets:
        slug = re.sub(r'[^a-z0-9]+', '-', ticket["title"].lower())[:50]
        filename = f"{ticket['id']}-{slug}.md"
        filepath = backlog_open / filename
        
        content = f"""---
id: {ticket['id']}
title: {ticket['title']}
status: open
phase: {ticket['phase']}
priority: {ticket['priority']}
estimate: {ticket['estimate']}
created: {datetime.now().strftime('%Y-%m-%d')}
team: {ticket['team']}
skills: {json.dumps(ticket['skills'])}
---

# {ticket['id']} — {ticket['title']}

{ticket['description']}

## Akzeptanzkriterien

"""
        for criterion in ticket['acceptance_criteria']:
            content += f"- [ ] {criterion}\n"
        
        content += f"""
## Abhängigkeiten

"""
        for dep in ticket['dependencies']:
            content += f"- {dep}\n"
        
        if not ticket['dependencies']:
            content += "- Keine\n"
        
        content += f"""
## Geschätzter Aufwand

{ticket['estimate']}

## Skills

"""
        for skill in ticket['skills']:
            content += f"- {skill}\n"
        
        filepath.write_text(content)
    
    return len(tickets)

# =============================================================================
# MAIN
# =============================================================================

def main():
    if len(sys.argv) < 2:
        print("Verwendung:")
        print("  python3 generate_ticket_manifest.py <project>")
        sys.exit(1)
    
    project = sys.argv[1]
    
    # Read PRD
    prd_file = PROJECTS_DIR / project / "docs" / "intake" / "prd.md"
    if not prd_file.exists():
        print(f"Fehler: PRD nicht gefunden: {prd_file}")
        print(f"Zuerst: python3 process_intake.py {project} <input>")
        sys.exit(1)
    
    prd_content = prd_file.read_text()
    
    # Extract features
    features = extract_features_from_prd(prd_content)
    archetype = extract_archetype_from_prd(prd_content)
    
    print(f"\n{'='*60}")
    print(f"  TICKET-MANIFEST GENERIEREN: {project}")
    print(f"{'='*60}")
    print(f"\n  PRD:             {prd_file}")
    print(f"  Archetyp:        {archetype}")
    print(f"  Features:        {len(features)}")
    
    # Generate tickets
    tickets = generate_tickets_from_features(features, project, archetype)
    
    # Write ticket files
    ticket_count = write_ticket_files(tickets, project)
    
    # Write manifest
    manifest = {
        "project": project,
        "archetype": archetype,
        "generated_at": datetime.now().isoformat(),
        "ticket_count": ticket_count,
        "tickets": [
            {
                "id": t["id"],
                "title": t["title"],
                "phase": t["phase"],
                "priority": t["priority"],
                "team": t["team"],
                "skills": t["skills"]
            }
            for t in tickets
        ]
    }
    
    manifest_file = PROJECTS_DIR / project / "docs" / "ticket-manifest.json"
    manifest_file.parent.mkdir(parents=True, exist_ok=True)
    manifest_file.write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
    
    print(f"\n  Tickets generiert: {ticket_count}")
    print(f"  Manifest:          {manifest_file}")
    
    # Print ticket summary
    print(f"\n  {'='*50}")
    print(f"  TICKET-ÜBERSICHT")
    print(f"  {'='*50}")
    
    for ticket in tickets:
        deps = ", ".join(ticket["dependencies"][:2]) if ticket["dependencies"] else "keine"
        print(f"  {ticket['id']} | P{ticket['priority'][-1]} | Phase {ticket['phase']} | {ticket['title'][:40]}")
    
    print(f"\n  Nächster Schritt:")
    print(f"    ./studio start {project} --mode core")
    print()


if __name__ == "__main__":
    main()
