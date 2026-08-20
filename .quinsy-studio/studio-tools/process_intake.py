#!/usr/bin/env python3
"""
process_intake.py — Intake-Logik für Quinsy Studio

Liest rohes User-Input (Notizen, Ideen, Feature-Requests) und strukturiert
dies in ein sauberes, validiertes PRD gemäß dem PRD-Template.

Verwendung:
  python3 process_intake.py <project> <input-file>
  python3 process_intake.py nudge intake/nudge-raw.md
  python3 process_intake.py nudge --from-text "Ich will eine ToDo-App mit gamification"

Output:
  projects/<project>/docs/intake/prd.md (validiertes PRD)
  projects/<project>/docs/intake/validation.json (Validierungs-Report)
"""

import sys
import os
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# =============================================================================
# CONFIGURATION
# =============================================================================

STUDIO_ROOT = Path(__file__).parent.parent.parent
QUINSY_STUDIO = STUDIO_ROOT / ".quinsy-studio"
TEMPLATES_DIR = QUINSY_STUDIO / "studio-templates"
PROJECTS_DIR = STUDIO_ROOT / "projects"

# =============================================================================
# PRD STRUCTURE DEFINITION
# =============================================================================

PRD_SECTIONS = {
    "title": {
        "required": True,
        "description": "Projektname und kurze Beschreibung",
        "min_length": 10,
        "max_length": 200
    },
    "problem": {
        "required": True,
        "description": "Welches Problem wird gelöst?",
        "min_length": 50,
        "max_length": 2000
    },
    "target_audience": {
        "required": True,
        "description": "Wer sind die Nutzer?",
        "min_length": 20,
        "max_length": 1000
    },
    "goals": {
        "required": True,
        "description": "Was sind die Ziele und Erfolgskriterien?",
        "min_length": 30,
        "max_length": 1500
    },
    "scope_in": {
        "required": True,
        "description": "Was ist im Scope (P0)?",
        "min_length": 20,
        "max_length": 2000
    },
    "scope_out": {
        "required": False,
        "description": "Was ist out of scope?",
        "min_length": 10,
        "max_length": 1000
    },
    "requirements_functional": {
        "required": True,
        "description": "Funktionale Anforderungen",
        "min_length": 30,
        "max_length": 3000
    },
    "requirements_non_functional": {
        "required": False,
        "description": "Nicht-funktionale Anforderungen",
        "min_length": 20,
        "max_length": 1500
    },
    "monetization": {
        "required": False,
        "description": "Monetarisierungsmodell",
        "min_length": 10,
        "max_length": 1000
    },
    "compliance": {
        "required": False,
        "description": "Compliance & rechtliche Anforderungen",
        "min_length": 10,
        "max_length": 1000
    },
    "risks": {
        "required": False,
        "description": "Risiken und offene Fragen",
        "min_length": 10,
        "max_length": 1500
    }
}

# =============================================================================
# INPUT PARSING
# =============================================================================

def parse_raw_text(text: str) -> Dict[str, str]:
    """
    Parst rohen Text und extrahiert PRD-Sektionen.
    Erkennt Markdown-Headings oder freien Text.
    """
    sections = {}
    current_section = None
    current_content = []
    
    lines = text.strip().split('\n')
    
    for line in lines:
        # Check for Markdown headings
        heading_match = re.match(r'^#{1,3}\s+(.+)', line)
        if heading_match:
            # Save previous section
            if current_section and current_content:
                sections[current_section] = '\n'.join(current_content).strip()
            
            # Map heading to section
            heading = heading_match.group(1).strip().lower()
            current_section = map_heading_to_section(heading)
            current_content = []
        elif current_section:
            current_content.append(line)
    
    # Save last section
    if current_section and current_content:
        sections[current_section] = '\n'.join(current_content).strip()
    
    return sections


def map_heading_to_section(heading: str) -> Optional[str]:
    """Mappt Markdown-Headings zu PRD-Sektionen."""
    mappings = {
        "titel": "title",
        "title": "title",
        "überblick": "title",
        "übersicht": "title",
        "problem": "problem",
        "zielgruppe": "target_audience",
        "nutzer": "target_audience",
        "ziele": "goals",
        "erfolgskriterien": "goals",
        "north star": "goals",
        "umfang": "scope_in",
        "scope": "scope_in",
        "in scope": "scope_in",
        "out of scope": "scope_out",
        "anforderungen": "requirements_functional",
        "funktionale": "requirements_functional",
        "features": "requirements_functional",
        "nicht-funktionale": "requirements_non_functional",
        "performance": "requirements_non_functional",
        "monetarisierung": "monetization",
        "preise": "monetization",
        "compliance": "compliance",
        "recht": "compliance",
        "dsgvo": "compliance",
        "risiken": "risks",
        "offene fragen": "risks",
    }
    
    for key, value in mappings.items():
        if key in heading:
            return value
    
    return None


def extract_sections_from_structured_text(text: str) -> Dict[str, str]:
    """
    Extrahiert Sektionen aus strukturiertem Text (PRD-Format).
    Sucht nach bekannten Patterns wie "**Problem**:" oder "## Problem".
    """
    sections = {}
    
    # Pattern: **Section** oder ## Section oder Section:
    patterns = [
        r'\*\*([^*]+)\*\*[:\s]*\n(.*?)(?=\n\*\*|\n##|\Z)',
        r'##\s+([^#\n]+)\n(.*?)(?=\n##|\Z)',
        r'^([A-Z][a-zäöü]+(?:\s+[a-zäöü]+)*)[:\s]*\n(.*?)(?=\n[A-Z][a-zäöü]+:|\Z)',
    ]
    
    for pattern in patterns:
        matches = re.finditer(pattern, text, re.MULTILINE | re.DOTALL)
        for match in matches:
            heading = match.group(1).strip().lower()
            content = match.group(2).strip()
            section = map_heading_to_section(heading)
            if section and content:
                sections[section] = content
    
    return sections


def parse_input_file(filepath: str) -> Dict[str, str]:
    """Liest eine Datei und parst den Inhalt."""
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Try structured parsing first
    sections = extract_sections_from_structured_text(text)
    
    # If not enough sections found, try raw text parsing
    if len(sections) < 3:
        raw_sections = parse_raw_text(text)
        sections.update(raw_sections)
    
    return sections


def parse_text_input(text: str) -> Dict[str, str]:
    """Parst einen Text-Input direkt."""
    sections = extract_sections_from_structured_text(text)
    if len(sections) < 3:
        sections = parse_raw_text(text)
    return sections

# =============================================================================
# PRD VALIDATION
# =============================================================================

def validate_prd(sections: Dict[str, str]) -> Tuple[bool, List[Dict]]:
    """
    Validiert ob das PRD vollständig ist.
    Gibt (ist_valide, liste_der_probleme) zurück.
    """
    problems = []
    
    for section_key, section_def in PRD_SECTIONS.items():
        content = sections.get(section_key, "")
        
        if section_def["required"] and not content:
            problems.append({
                "section": section_key,
                "type": "missing",
                "message": f"Pflicht-Sektion '{section_key}' fehlt",
                "severity": "critical"
            })
        elif content:
            if len(content) < section_def.get("min_length", 0):
                problems.append({
                    "section": section_key,
                    "type": "too_short",
                    "message": f"Sektion '{section_key}' ist zu kurz ({len(content)} < {section_def['min_length']})",
                    "severity": "warning"
                })
            if len(content) > section_def.get("max_length", 999999):
                problems.append({
                    "section": section_key,
                    "type": "too_long",
                    "message": f"Sektion '{section_key}' ist zu lang ({len(content)} > {section_def['max_length']})",
                    "severity": "warning"
                })
    
    has_critical = any(p["severity"] == "critical" for p in problems)
    return not has_critical, problems


def detect_archetype(sections: Dict[str, str]) -> str:
    """Erkennt den Projekt-Archetyp basierend auf dem PRD-Inhalt."""
    text = json.dumps(sections).lower()
    
    # Check SaaS FIRST as it's more specific than generic "app"
    # SaaS indicators are weighted higher
    saas_score = sum(1 for s in ["saas", "subscription", "abo", "freemium",
                                   "pro-tier", "free-tier", "monatlich", "pro pass"]
                    if s in text)
    
    if saas_score >= 2:
        return "saas-application"
    
    archetype_signals = {
        "e-commerce": [
            "shop", "warenkorb", "bestellung", "zahlung", "produkt",
            "preis", "katalog", "versand"
        ],
        "content-platform": [
            "blog", "artikel", "content", "publishing", "redaktion",
            "newsletter", "beitrag"
        ],
        "mobile-app": [
            "ios", "android", "push-notification",
            "app store", "native app"
        ],
        "api-service": [
            "api", "webhook", "endpoint", "integration", "rest",
            "graphql", "microservice"
        ],
        "internal-tool": [
            "intern", "dashboard", "admin", "backoffice",
            "workflow", "automatisierung"
        ],
        "game": [
            "game", "spiel", "godot", "unity", "unreal", "platformer",
            "level", "player", "engine", "tilemap", "phaser", "pygame"
        ]
    }
    
    scores = {}
    for archetype, signals in archetype_signals.items():
        score = sum(1 for signal in signals if signal in text)
        scores[archetype] = score
    
    if scores:
        best = max(scores, key=scores.get)
        if scores[best] > 0:
            return best
    
    # Fallback: check for generic "app" but prefer SaaS
    if "app" in text and saas_score >= 1:
        return "saas-application"
    
    return "saas-application"  # Default

# =============================================================================
# PRD GENERATION
# =============================================================================

def generate_prd(sections: Dict[str, str], archetype: str) -> str:
    """Generiert ein vollständiges PRD im Markdown-Format."""
    
    now = datetime.now().strftime("%Y-%m-%d")
    
    # Extract a short title (first sentence or first 100 chars)
    full_title = sections.get('title', 'Unbekannt')
    # Try to get just the project name (first sentence)
    title_match = re.match(r'^(.+?\.\s|.{10,60})', full_title)
    if title_match:
        short_title = title_match.group(1).strip().rstrip('.')
    else:
        short_title = full_title[:60]
    
    prd = f"""# PRD — "{short_title}"

> **Archetyp & Komplexität**
> * **Archetyp:** {archetype.replace('-', ' ').title()}
> * **Generiert:** {now}
> * **Status:** draft

---

## Titel / Überblick

{sections.get('title', '_Noch nicht definiert_')}

---

## Problem

{sections.get('problem', '_Noch nicht definiert_')}

---

## Zielgruppe & Nutzer

{sections.get('target_audience', '_Noch nicht definiert_')}

---

## Ziele & Erfolgskriterien

{sections.get('goals', '_Noch nicht definiert_')}

---

## Umfang

### In Scope (P0)

{sections.get('scope_in', '_Noch nicht definiert_')}

### Out of Scope

{sections.get('scope_out', '_Noch nicht definiert_')}

---

## Anforderungen

### Funktionale Anforderungen

{sections.get('requirements_functional', '_Noch nicht definiert_')}

### Nicht-funktionale Anforderungen

{sections.get('requirements_non_functional', '_Noch nicht definiert_')}

---

## Monetarisierung

{sections.get('monetization', '_Noch nicht definiert_')}

---

## Compliance & Recht

{sections.get('compliance', '_Noch nicht definiert_')}

---

## Risiken & offene Fragen

{sections.get('risks', '_Noch nicht definiert_')}
"""
    return prd

# =============================================================================
# MAIN
# =============================================================================

def main():
    if len(sys.argv) < 3:
        print("Verwendung:")
        print("  python3 process_intake.py <project> <input-file>")
        print("  python3 process_intake.py <project> --from-text \"...\"")
        sys.exit(1)
    
    project = sys.argv[1]
    
    # Parse input
    if sys.argv[2] == "--from-text":
        text = " ".join(sys.argv[3:])
        sections = parse_text_input(text)
    else:
        input_file = sys.argv[2]
        if not os.path.exists(input_file):
            print(f"Fehler: Datei nicht gefunden: {input_file}")
            sys.exit(1)
        sections = parse_input_file(input_file)
    
    if not sections:
        print("Fehler: Keine Sektionen im Input erkannt.")
        print("Tipp: Verwende Markdown-Headings (## Problem, ## Zielgruppe, etc.)")
        sys.exit(1)
    
    # Validate
    is_valid, problems = validate_prd(sections)
    
    # Detect archetype
    archetype = detect_archetype(sections)
    
    # Generate PRD
    prd_content = generate_prd(sections, archetype)
    
    # Save PRD
    project_dir = PROJECTS_DIR / project
    intake_dir = project_dir / "docs" / "intake"
    intake_dir.mkdir(parents=True, exist_ok=True)
    
    prd_file = intake_dir / "prd.md"
    prd_file.write_text(prd_content)
    
    # Save validation report
    validation = {
        "project": project,
        "archetype": archetype,
        "is_valid": is_valid,
        "sections_found": list(sections.keys()),
        "sections_missing": [k for k, v in PRD_SECTIONS.items() 
                           if v["required"] and k not in sections],
        "problems": problems,
        "generated_at": datetime.now().isoformat()
    }
    
    validation_file = intake_dir / "validation.json"
    validation_file.write_text(json.dumps(validation, indent=2, ensure_ascii=False))
    
    # Report
    print(f"\n{'='*60}")
    print(f"  INTAKE VERARBEITET: {project}")
    print(f"{'='*60}")
    print(f"\n  Archetyp:     {archetype}")
    print(f"  Sektionen:    {len(sections)} von {len(PRD_SECTIONS)}")
    print(f"  Validiert:    {'✅ Ja' if is_valid else '❌ Nein'}")
    
    if problems:
        print(f"\n  Probleme:")
        for p in problems:
            icon = "❌" if p["severity"] == "critical" else "⚠️"
            print(f"    {icon} {p['message']}")
    
    print(f"\n  Output:")
    print(f"    PRD:        {prd_file}")
    print(f"    Validierung: {validation_file}")
    
    if not is_valid:
        print(f"\n  ⚠️  PRD ist unvollständig. Fehlende Pflicht-Sektionen müssen")
        print(f"     manuell ergänzt werden bevor Phase 2 starten kann.")
    
    print(f"\n  Nächster Schritt:")
    print(f"    1. PRD prüfen und ggf. ergänzen")
    print(f"    2. ./studio start {project} --mode core")
    print()


if __name__ == "__main__":
    main()
