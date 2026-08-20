#!/usr/bin/env python3
"""
process_intake.py — Intake logic for Quinsy Studio

Reads raw user input (notes, ideas, feature requests) and structures it
into a clean, validated PRD following the PRD template.

Usage:
  python3 process_intake.py <project> <input-file>
  python3 process_intake.py nudge intake/nudge-raw.md
  python3 process_intake.py nudge --from-text "I want a to-do app with gamification"

Output:
  projects/<project>/docs/intake/prd.md (validated PRD)
  projects/<project>/docs/intake/validation.json (validation report)
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
        "description": "Project name and short description",
        "min_length": 10,
        "max_length": 200
    },
    "problem": {
        "required": True,
        "description": "Which problem is solved?",
        "min_length": 50,
        "max_length": 2000
    },
    "target_audience": {
        "required": True,
        "description": "Who are the users?",
        "min_length": 20,
        "max_length": 1000
    },
    "goals": {
        "required": True,
        "description": "What are the goals and success criteria?",
        "min_length": 30,
        "max_length": 1500
    },
    "scope_in": {
        "required": True,
        "description": "What is in scope (P0)?",
        "min_length": 20,
        "max_length": 2000
    },
    "scope_out": {
        "required": False,
        "description": "What is out of scope?",
        "min_length": 10,
        "max_length": 1000
    },
    "requirements_functional": {
        "required": True,
        "description": "Functional requirements",
        "min_length": 30,
        "max_length": 3000
    },
    "requirements_non_functional": {
        "required": False,
        "description": "Non-functional requirements",
        "min_length": 20,
        "max_length": 1500
    },
    "monetization": {
        "required": False,
        "description": "Monetization model",
        "min_length": 10,
        "max_length": 1000
    },
    "compliance": {
        "required": False,
        "description": "Compliance & legal requirements",
        "min_length": 10,
        "max_length": 1000
    },
    "risks": {
        "required": False,
        "description": "Risks and open questions",
        "min_length": 10,
        "max_length": 1500
    }
}

# =============================================================================
# INPUT PARSING
# =============================================================================

def parse_raw_text(text: str) -> Dict[str, str]:
    """
    Parse raw text and extract PRD sections.
    Recognizes markdown headings or free text.
    """
    sections = {}
    current_section = None
    current_content = []
    
    lines = text.strip().split('\n')
    
    for line in lines:
        # Check for Markdown headings (supports "## ## Title" double-hash style)
        heading_match = re.match(r'^#{1,3}\s+(?:#{1,3}\s+)?(.+)', line)
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
    """Map markdown headings to PRD sections (English + German)."""
    h = heading.strip().lower()
    # Strip leading hashes if captured
    h = re.sub(r'^#+\s*', '', h).strip()

    mappings = {
        # English
        "title": "title",
        "overview": "title",
        "summary": "title",
        "problem": "problem",
        "target audience": "target_audience",
        "users": "target_audience",
        "audience": "target_audience",
        "goals": "goals",
        "success criteria": "goals",
        "north star": "goals",
        "scope": "scope_in",
        "in scope": "scope_in",
        "out of scope": "scope_out",
        "requirements": "requirements_functional",
        "functional": "requirements_functional",
        "features": "requirements_functional",
        "non-functional": "requirements_non_functional",
        "performance": "requirements_non_functional",
        "monetization": "monetization",
        "pricing": "monetization",
        "compliance": "compliance",
        "legal": "compliance",
        "gdpr": "compliance",
        "risks": "risks",
        "open questions": "risks",
        # German
        "titel": "title",
        "überblick": "title",
        "ueberblick": "title",
        "zielgruppe": "target_audience",
        "nutzer": "target_audience",
        "ziele": "goals",
        "erfolgskriterien": "goals",
        "umfang": "scope_in",
        "anforderungen": "requirements_functional",
        "funktionale": "requirements_functional",
        "nicht-funktionale": "requirements_non_functional",
        "monetarisierung": "monetization",
        "recht": "compliance",
        "dsgvo": "compliance",
        "risiken": "risks",
        "offene fragen": "risks",
    }

    for key in sorted(mappings.keys(), key=len, reverse=True):
        if key in h:
            return mappings[key]

    return None


def extract_sections_from_structured_text(text: str) -> Dict[str, str]:
    """
    Extract sections from structured text (PRD format).
    Looks for known patterns like "**Problem**:" or "## Problem".
    """
    sections = {}
    
    # Pattern: **Section** oder ## Section oder Section:
    patterns = [
        r'\*\*([^*]+)\*\*[:\s]*\n(.*?)(?=\n\*\*|\n##|\Z)',
        r'##\s+([^#\n]+)\n(.*?)(?=\n##|\Z)',
        r'^([A-Z][a-z]+(?:\s+[a-z]+)*)[:\s]*\n(.*?)(?=\n[A-Z][a-z]+:|\Z)',
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
    """Read a file and parse its content."""
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    sections = extract_sections_from_structured_text(text)
    
    if len(sections) < 3:
        raw_sections = parse_raw_text(text)
        sections.update(raw_sections)
    
    sections["_source_text"] = text
    return sections


def parse_text_input(text: str) -> Dict[str, str]:
    """Parse a text input directly."""
    sections = extract_sections_from_structured_text(text)
    if len(sections) < 3:
        sections = parse_raw_text(text)
    return sections

# =============================================================================
# PRD VALIDATION
# =============================================================================

def validate_prd(sections: Dict[str, str]) -> Tuple[bool, List[Dict]]:
    """
    Validate whether the PRD is complete.
    Returns (is_valid, list_of_problems).
    """
    problems = []
    
    for section_key, section_def in PRD_SECTIONS.items():
        content = sections.get(section_key, "")
        
        if section_def["required"] and not content:
            problems.append({
                "section": section_key,
                "type": "missing",
                "message": f"Required section '{section_key}' is missing",
                "severity": "critical"
            })
        elif content:
            if len(content) < section_def.get("min_length", 0):
                problems.append({
                    "section": section_key,
                    "type": "too_short",
                    "message": f"Section '{section_key}' is too short ({len(content)} < {section_def['min_length']})",
                    "severity": "warning"
                })
            if len(content) > section_def.get("max_length", 999999):
                problems.append({
                    "section": section_key,
                    "type": "too_long",
                    "message": f"Section '{section_key}' is too long ({len(content)} > {section_def['max_length']})",
                    "severity": "warning"
                })
    
    has_critical = any(p["severity"] == "critical" for p in problems)
    return not has_critical, problems


def detect_archetype(sections: Dict[str, str], full_text: str = "") -> str:
    """Detect the project archetype based on the PRD content."""
    text = (full_text or json.dumps(sections)).lower()

    # Explicit archetype in PRD header (e.g. "Archetyp: SaaS-Application")
    explicit = re.search(
        r'archetyp[:\s]*([\w\s-]+(?:saas|application|e-?commerce|game|api|mobile|content|internal|marketplace|prototype)[\w\s-]*)',
        text, re.IGNORECASE
    )
    if explicit:
        arch = explicit.group(1).strip().lower()
        if 'saas' in arch or 'micro-saas' in arch:
            return "saas-application"
        if 'e-commerce' in arch or 'ecommerce' in arch or 'shop' in arch:
            return "e-commerce"
        if 'game' in arch and 'gamification' not in arch:
            return "game"
        if 'api' in arch:
            return "api-service"
        if 'mobile' in arch:
            return "mobile-app"
        if 'content' in arch:
            return "content-platform"
        return arch.replace(' ', '-')

    saas_score = sum(1 for s in ["saas", "subscription", "freemium",
                                   "pro-tier", "free-tier", "monthly", "pro pass", "freemium"]
                    if s in text)

    if saas_score >= 1:
        return "saas-application"

    archetype_signals = {
        "e-commerce": [
            "shop", "cart", "checkout", "warenkorb", "produkt", "shipping"
        ],
        "content-platform": [
            "blog", "article", "content", "publishing", "editorial", "newsletter"
        ],
        "mobile-app": [
            "ios", "android", "push-notification", "app store", "native app"
        ],
        "api-service": [
            "webhook", "endpoint", "graphql", "microservice"
        ],
        "internal-tool": [
            "internal", "dashboard", "admin", "backoffice", "back-office"
        ],
        "game": [
            "godot", "unity", "unreal", "platformer", "tilemap", "phaser", "pygame", "game engine"
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

    return "saas-application"

# =============================================================================
# PRD GENERATION
# =============================================================================

def generate_prd(sections: Dict[str, str], archetype: str) -> str:
    """Generate a complete PRD in markdown format."""
    
    now = datetime.now().strftime("%Y-%m-%d")
    
    # Extract a short title (first sentence or first 100 chars)
    full_title = sections.get('title', 'Unknown')
    # Try to get just the project name (first sentence)
    title_match = re.match(r'^(.+?\.\s|.{10,60})', full_title)
    if title_match:
        short_title = title_match.group(1).strip().rstrip('.')
    else:
        short_title = full_title[:60]
    
    prd = f"""# PRD — "{short_title}"

> **Archetype & complexity**
> * **Archetype:** {archetype.replace('-', ' ').title()}
> * **Generated:** {now}
> * **Status:** draft

---

## Title / Overview

{sections.get('title', '_Not defined yet_')}

---

## Problem

{sections.get('problem', '_Not defined yet_')}

---

## Target audience & users

{sections.get('target_audience', '_Not defined yet_')}

---

## Goals & success criteria

{sections.get('goals', '_Not defined yet_')}

---

## Scope

### In Scope (P0)

{sections.get('scope_in', '_Not defined yet_')}

### Out of Scope

{sections.get('scope_out', '_Not defined yet_')}

---

## Requirements

### Functional requirements

{sections.get('requirements_functional', '_Not defined yet_')}

### Non-functional requirements

{sections.get('requirements_non_functional', '_Not defined yet_')}

---

## Monetization

{sections.get('monetization', '_Not defined yet_')}

---

## Compliance & legal

{sections.get('compliance', '_Not defined yet_')}

---

## Risks & open questions

{sections.get('risks', '_Not defined yet_')}
"""
    return prd

# =============================================================================
# MAIN
# =============================================================================

def main():
    if len(sys.argv) < 3:
        print("Usage:")
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
            print(f"Error: file not found: {input_file}")
            sys.exit(1)
        sections = parse_input_file(input_file)
    
    if not sections:
        print("Error: no sections recognized in the input.")
        print("Tip: use markdown headings (## Problem, ## Target audience, etc.)")
        sys.exit(1)
    
    # Validate
    source_text = sections.pop("_source_text", "")
    is_valid, problems = validate_prd(sections)
    
    # Detect archetype
    archetype = detect_archetype(sections, source_text)
    
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
    print(f"  INTAKE PROCESSED: {project}")
    print(f"{'='*60}")
    print(f"\n  Archetype:    {archetype}")
    print(f"  Sections:     {len(sections)} of {len(PRD_SECTIONS)}")
    print(f"  Validated:    {'✅ Yes' if is_valid else '❌ No'}")
    
    if problems:
        print(f"\n  Problems:")
        for p in problems:
            icon = "❌" if p["severity"] == "critical" else "⚠️"
            print(f"    {icon} {p['message']}")
    
    print(f"\n  Output:")
    print(f"    PRD:          {prd_file}")
    print(f"    Validation:   {validation_file}")
    
    if not is_valid:
        print(f"\n  ⚠️  PRD is incomplete. Missing required sections must be")
        print(f"     added manually before phase 2 can start.")
        sys.exit(1)

    # Persist archetype to status.json
    status_file = project_dir / "status.json"
    if status_file.exists():
        try:
            status = json.loads(status_file.read_text())
        except json.JSONDecodeError:
            status = {}
    else:
        status = {"name": project}
    status["archetype"] = archetype
    status["last_update"] = datetime.now().strftime("%Y-%m-%d")
    status_file.write_text(json.dumps(status, indent=2, ensure_ascii=False))

    print(f"\n  Next step:")
    print(f"    1. Review the PRD and complete it if needed")
    print(f"    2. ./studio start {project} --mode core")
    print()


if __name__ == "__main__":
    main()
