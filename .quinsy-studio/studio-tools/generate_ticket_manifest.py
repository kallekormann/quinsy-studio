#!/usr/bin/env python3
"""
generate_ticket_manifest.py — Ticket generation for Quinsy Studio

Reads a validated PRD and breaks it down into linked Markdown/JSON tickets,
including acceptance criteria, dependencies, and estimates.

Usage:
  python3 generate_ticket_manifest.py <project>
  python3 generate_ticket_manifest.py nudge

Output:
  projects/<project>/backlog/TICKET-NNNN-<slug>.md
  projects/<project>/docs/ticket-manifest.json
"""

import sys
import os
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional

from ticket_helpers import render_ticket_markdown
from skill_matcher import match_skills, team_for_skills
from ticket_ids import assign_sequential_ids

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
    Extract features from the PRD based on:
    - Bullet lists in the "In Scope" section
    - Functional requirements
    - User stories
    """
    features = []
    
    # Find "In Scope" section - try multiple patterns
    scope_patterns = [
        r'##\s+Scope.*?###\s+In Scope.*?\n(.*?)(?=###|##|\Z)',
        r'###\s+In Scope.*?\n(.*?)(?=###|##|\Z)',
        r'##\s+Umfang.*?###\s+In Scope.*?\n(.*?)(?=###|##|\Z)',
        r'###\s+In Scope.*?\n(.*?)(?=Out of Scope|###|##|\Z)',
        r'In Scope.*?\n(.*?)(?=Out of Scope|###|##|\Z)',
    ]
    
    for pattern in scope_patterns:
        scope_match = re.search(pattern, prd_content, re.DOTALL | re.IGNORECASE)
        if scope_match:
            scope_text = scope_match.group(1)
            # Stop at inline "Out of Scope" markers within the section
            scope_text = re.split(
                r'\*?\*?\s*Out of Scope|Aus\s+Scope|Out\s+of\s+Scope',
                scope_text, maxsplit=1, flags=re.IGNORECASE
            )[0]
            features.extend(extract_bullet_features(scope_text, "scope"))
            if features:  # Stop if we found features
                break
    
    # Find functional requirements
    req_patterns = [
        r'##\s+Requirements.*?###\s+Functional.*?\n(.*?)(?=###|##|\Z)',
        r'###\s+Functional requirements.*?\n(.*?)(?=###|##|\Z)',
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
            
            # Skip Template-Platzhalter (keine echten Features)
            if re.search(r'noch nicht definiert|_TODO_|\[Zu definieren\]|\[.*\]', name, re.IGNORECASE):
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
    """Extract features from bullet lists."""
    features = []
    
    lines = text.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue

        if re.search(r'out of scope|aus scope', line, re.IGNORECASE):
            break
        
        # Skip category headers (e.g., "* **In Scope (P0):**")
        if re.match(r'^[\-\*]\s+\*\*[^*]+\*\*\s*:?\s*$', line):
            continue
        
        # Check for bullet point with content
        # Handle both * and - bullets, with optional **bold** text
        # IMPORTANT: (.+?) is non-greedy and matches only 1 character —
        # therefore do an explicit colon-split (name = remainder, not 1st char).
        bullet_match = None
        bold_match = re.match(r'^[\-\*]\s+\*\*(.+?)\*\*\s*:?\s*(.*)', line)
        if bold_match:
            bullet_match = (bold_match.group(1).strip(), bold_match.group(2).strip())
        else:
            content = re.sub(r'^[\-\*]\s*', '', line).strip()
            if content:
                parts = re.split(r'\s*:\s*', content, maxsplit=1)
                bullet_match = (parts[0].strip(), parts[1].strip() if len(parts) > 1 else "")
        if bullet_match:
            name, description = bullet_match
            name = name.strip()
            description = description.strip()
            
            # Skip empty or very short names (single characters, just punctuation)
            if len(name) < 3:
                continue
            
            # Skip Template-Platzhalter (keine echten Features)
            if re.search(r'noch nicht definiert|_TODO_|\[Zu definieren\]|out of scope', name, re.IGNORECASE):
                continue
            
            # Skip if name is just a label prefix like "P0:" or "P1:"
            if re.match(r'^[Pp]\d:\s*$', name):
                continue

            nfr_labels = {"performance", "usability", "plattformen", "platforms", "security", "scalability"}
            if source == "requirement" and name.lower().split(":")[0].strip() in nfr_labels:
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
    """Extract archetype from PRD content."""
    match = re.search(
        r'\*?\*?Archetype\*?\*?\s*[:\s]+([^\n*]+)',
        prd_content, re.IGNORECASE
    )
    if not match:
        match = re.search(r'Archetyp[:\s]+([^\n*]+)', prd_content, re.IGNORECASE)
    if match:
        archetype_text = match.group(1).strip().lower()
        if 'saas' in archetype_text or 'micro-saas' in archetype_text:
            return "saas-application"
        if 'mobile' in archetype_text:
            return "mobile-app"
        if 'shop' in archetype_text or 'ecommerce' in archetype_text or 'e-commerce' in archetype_text:
            return "e-commerce"
        if 'api' in archetype_text:
            return "api-service"
        if 'content' in archetype_text or 'blog' in archetype_text:
            return "content-platform"
        if 'game' in archetype_text:
            return "game"
        return re.sub(r'[^a-z0-9]+', '-', archetype_text).strip('-')
    
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
    """Generate setup tickets for a new project."""
    
    tickets = []
    
    # Ticket 1: Project Setup
    tickets.append({
        "id": f"{project[:4].upper()}-0001",
        "title": "Project Setup & Tooling",
        "description": f"Set up monorepo, dependencies, linting, CI/CD for {archetype}",
        "phase": 2,
        "priority": "P0",
        "estimate": "M",
        "skills": ["PE-001", "PE-002"],
        "team": "08-platform-enterprise-engineering",
        "ist_zustand": f"No project setup exists. The folder `projects/{project}/` exists but without tooling (package.json, linting, CI/CD).",
        "soll_zustand": f"`projects/{project}/` has a working setup: package.json with scripts (dev/build/test/lint), TypeScript config, ESLint/Prettier, CI/CD baseline (GitHub Actions).",
        "value": "Every other ticket works on a stable base — no tooling blockers during implementation.",
        "modification_files": [
            f"projects/{project}/package.json",
            f"projects/{project}/tsconfig.json",
            f"projects/{project}/.eslintrc.json",
            f"projects/{project}/.github/workflows/ci.yml"
        ],
        "constraints": [
            "Do not install external packages that are not required by the PRD",
            "Use the package manager from the PRD (pnpm/npm/yarn)",
            "No secrets, no pinned versions without an ADR"
        ],
        "scenarios": [
            {
                "name": "Project setup is complete",
                "given": f"A new project `{project}` was created with `./studio init`",
                "when": "The setup ticket is done and `npm run build` is executed",
                "then": "The build completes without errors and `npm run lint` reports 0 errors"
            }
        ],
        "definition_of_done": [
            "`package.json` exists with dev/build/test/lint scripts",
            "`npm run build` completes without errors",
            "`npm run lint` reports 0 errors",
            "CI workflow file is created (`.github/workflows/ci.yml`)",
            "QA gate green (`./studio gate {project} --level 2`)"
        ],
        "dependencies": []
    })
    
    # Ticket 2: Design System
    tickets.append({
        "id": f"{project[:4].upper()}-0002",
        "title": "Design System & Tokens",
        "description": "Define design tokens, color palette, typography, spacing",
        "phase": 2,
        "priority": "P0",
        "estimate": "M",
        "skills": ["FE-002"],
        "team": "01-frontend-experience",
        "ist_zustand": "No design tokens defined. UI code would be built with hardcoded values (anti-slop violation U1-U5).",
        "soll_zustand": f"`projects/{project}/ui/tokens/` contains design-tokens.json + .css with color palette, typography scale, spacing (8px grid), dark/light mode.",
        "value": "Consistent UI across all components; prevents generic LLM styling; basis for studio-library promotion.",
        "modification_files": [
            f"projects/{project}/ui/tokens/design-tokens.json",
            f"projects/{project}/ui/tokens/design-tokens.css"
        ],
        "constraints": [
            "Token-based values only (no hardcoded colors/radii/shadows)",
            "8px grid for spacing",
            "Load the external `design/skills` (hallmark) skill and apply slop gates",
            "Dark mode via CSS custom properties (no separate theme package)"
        ],
        "scenarios": [
            {
                "name": "Tokens are consumable",
                "given": "A fresh project without design tokens",
                "when": "The token files are created and imported",
                "then": "Every UI component can access `var(--token)` and dark mode works via theme switch"
            }
        ],
        "definition_of_done": [
            "design-tokens.json + .css exist under `ui/tokens/`",
            "At least 5 color steps + typography scale + 8px spacing defined",
            "Dark/light mode via CSS custom properties",
            "Anti-slop: no hardcoded values in new components",
            "QA gate green (`./studio gate {project} --level 5`)"
        ],
        "dependencies": [f"{project[:4].upper()}-0001"]
    })
    
    # Ticket 3: Database Schema
    tickets.append({
        "id": f"{project[:4].upper()}-0003",
        "title": "Database Schema & Migrations",
        "description": "Define the primary database tables and migrations",
        "phase": 2,
        "priority": "P0",
        "estimate": "M",
        "skills": ["BE-002"],
        "team": "02-backend-systems",
        "ist_zustand": "No data model defined. No tables, migrations, or seeds exist.",
        "soll_zustand": f"`projects/{project}/docs/definitions/` contains the data model; migrations are versioned and reversible; seeds provide test data.",
        "value": "Data integrity from the start; prevents schema rework in later phases.",
        "modification_files": [
            f"projects/{project}/docs/definitions/schema.md",
            f"projects/{project}/database/migrations/"
        ],
        "constraints": [
            "UUIDs for external IDs (no auto-increment)",
            "Every migration reversible (up + down)",
            "Load the external `all_domains/database/database-schema-design` skill",
            "GIN index for JSONb columns (if EAV model)"
        ],
        "scenarios": [
            {
                "name": "Migration is runnable",
                "given": "An empty database schema",
                "when": "`migrate` is executed",
                "then": "All tables are created without errors and `rollback` restores the initial state"
            }
        ],
        "definition_of_done": [
            "Data model documented in `docs/definitions/schema.md`",
            "Migrations versioned + reversible",
            "Seeds produce consistent test data",
            "QA gate green (`./studio gate {project} --level 5`)"
        ],
        "dependencies": [f"{project[:4].upper()}-0001"]
    })
    
    # Ticket 4: Auth Setup
    tickets.append({
        "id": f"{project[:4].upper()}-0004",
        "title": "Authentication & Authorization",
        "description": "Login, registration, session management, RBAC",
        "phase": 3,
        "priority": "P0",
        "estimate": "L",
        "skills": ["BE-003"],
        "team": "02-backend-systems",
        "ist_zustand": "No authentication exists. All routes are publicly accessible.",
        "soll_zustand": "Login, registration, session management, and RBAC are implemented; protected routes deny unauthorized access.",
        "value": "Security baseline for all protected features; prevents IDOR and broken access control (OWASP A01).",
        "modification_files": [
            f"projects/{project}/backend/routes/auth.php",
            f"projects/{project}/backend/middleware/auth.php"
        ],
        "constraints": [
            "Password hashing with bcrypt/argon2 (no plaintext, no md5)",
            "Load the external `all_domains/api-and-integration/oauth-2-0-setup` skill (if OAuth is needed)",
            "No secrets in code — environment variables",
            "Rate limiting on login/registration endpoints"
        ],
        "scenarios": [
            {
                "name": "Login with valid credentials",
                "given": "A registered user with correct credentials",
                "when": "The user logs in",
                "then": "A valid session/JWT is created and protected routes are reachable"
            },
            {
                "name": "Access without auth",
                "given": "A user who is not logged in",
                "when": "The user accesses a protected route",
                "then": "The route responds with 401/403 and no data leak occurs"
            }
        ],
        "definition_of_done": [
            "Login + registration + logout work",
            "Password hashing (bcrypt/argon2) active",
            "RBAC implemented for at least one role",
            "Unauthorized access → 401/403",
            "QA gate green (`./studio gate {project} --level 5`)"
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
    
    # Acceptance criteria
    acceptance_criteria = generate_acceptance_criteria(feature)
    
    # Strict context (current/target) + constraints + BDD scenario
    feature_name = title.lower()
    ist = f"The feature '{title}' does not exist yet in `projects/{project}/`."
    soll = f"The feature '{title}' is implemented and reachable via the intended UI/API."
    value = feature.get("benefit", f"'{title}' delivers visible value for the target audience.")
    constraints = [
        "Do not install unnecessary external packages without an ADR",
        "Follow the Anti-Slop-Protocol (no clichés, no god functions)",
        "Always load the assigned skill files (see `skills`)"
    ]
    scenarios = [{
        "name": "Feature is usable",
        "given": f"A user in project {project}",
        "when": f"They use the feature '{title}'",
        "then": acceptance_criteria[0] if acceptance_criteria else f"'{title}' works as described"
    }]
    
    return {
        "id": ticket_id,
        "title": title,
        "description": description,
        "phase": phase,
        "priority": feature.get("priority", "P1"),
        "estimate": estimate_effort(feature),
        "skills": skills,
        "team": team,
        "ist_zustand": ist,
        "soll_zustand": soll,
        "value": value,
        "modification_files": [f"projects/{project}/"],
        "constraints": constraints,
        "scenarios": scenarios,
        "acceptance_criteria": acceptance_criteria,
        "definition_of_done": [
            "Feature works (BDD scenario green)",
            "Tests present and green",
            "Anti-Slop audit: 0 violations",
            "QA gate green (`./studio gate <project> --level 5`)"
        ],
        "dependencies": []
    }


def determine_skills_for_feature(text: str) -> List[str]:
    """Determine relevant skills for a feature (via skill_matcher)."""
    return match_skills(text)


def determine_team_for_skills(skills: List[str]) -> str:
    """Determine team from skills."""
    return team_for_skills(skills)


def generate_acceptance_criteria(feature: Dict) -> List[str]:
    """Generate acceptance criteria for a feature."""
    
    criteria = []
    
    if feature.get("type") == "user_story":
        criteria.append(f"Feature is usable for {feature.get('actor', 'user')}")
        criteria.append(f"{feature.get('action', 'action')} works as described")
        criteria.append(f"{feature.get('benefit', 'benefit')} is achieved")
    else:
        name = feature.get("name", "Feature")
        criteria.append(f"{name} is implemented")
        criteria.append(f"{name} has unit tests")
        criteria.append(f"{name} is documented")
    
    # Always add quality criteria
    criteria.append("Code is AI-slop-free")
    criteria.append("Accessibility checked (if UI)")
    
    return criteria


def estimate_effort(feature: Dict) -> str:
    """Estimate the effort for a feature."""
    
    text = json.dumps(feature).lower()
    
    # Simple heuristics
    if any(w in text for w in ["complex", "large", "extensive"]):
        return "XL"
    if any(w in text for w in ["simple", "small", "quick"]):
        return "S"
    if any(w in text for w in ["medium", "moderate"]):
        return "M"
    
    return "M"  # Default

# =============================================================================
# DEPENDENCY RESOLUTION
# =============================================================================

def resolve_dependencies(tickets: List[Dict]) -> List[Dict]:
    """Link tickets with dependencies based on phases and skills."""
    
    for i, ticket in enumerate(tickets):
        # Setup tickets have no dependencies (except internal)
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

def write_ticket_files(tickets: List[Dict], project: str):
    """Schreibt Ticket-Dateien in das Projekt-Backlog (striktes Studio-Schema)."""
    
    # Fortlaufende IDs ab bestehendem Counter (keine Kollisionen mit manuellen Tickets)
    tickets = assign_sequential_ids(tickets, project)
    
    # Tickets liegen im Projekt-Backlog
    backlog_queue = PROJECTS_DIR / project / "backlog"
    backlog_queue.mkdir(parents=True, exist_ok=True)
    
    for ticket in tickets:
        slug = re.sub(r'[^a-z0-9]+', '-', ticket["title"].lower())[:50]
        filename = f"{ticket['id']}-{slug}.md"
        filepath = backlog_queue / filename
        ticket["status"] = "backlog"
        
        # Neues Schema: Rolle, Ist/Soll, Constraints, BDD, DoD
        content = render_ticket_markdown(ticket)
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
    
    print(f"\n  Tickets generated: {ticket_count}")
    print(f"  Manifest:          {manifest_file}")
    
    # Print ticket summary
    print(f"\n  {'='*50}")
    print(f"  TICKET OVERVIEW")
    print(f"  {'='*50}")
    
    for ticket in tickets:
        deps = ", ".join(ticket["dependencies"][:2]) if ticket["dependencies"] else "none"
        print(f"  {ticket['id']} | P{ticket['priority'][-1]} | Phase {ticket['phase']} | {ticket['title'][:40]}")
    
    print(f"\n  Next step:")
    print(f"    ./studio start {project} --mode core")
    print()


if __name__ == "__main__":
    main()
