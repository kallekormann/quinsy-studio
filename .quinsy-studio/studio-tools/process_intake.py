#!/usr/bin/env python3
"""
process_intake.py — Intake logic for Quinsy Studio

Reads one file, a folder, or several files. Copies each one into the project
and writes a PRD that indexes them. The full text of text files is kept.
Other files are copied and named so architecture, design, and milestones
can read them. The PRD is not trimmed to fit a short template.

Usage:
  python3 process_intake.py <project> <file-or-folder> [more files...]
  python3 process_intake.py demo intake/demo/
  python3 process_intake.py demo --from-text "I want a to-do app with gamification"

Output:
  projects/<project>/docs/intake/prd.md
  projects/<project>/docs/intake/sources/
  projects/<project>/docs/intake/validation.json
"""

import sys
import os
import json
import re
import shutil
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
        "non functional": "requirements_non_functional",
        "non functional requirements": "requirements_non_functional",
        "non-functional requirements": "requirements_non_functional",
        "nfr": "requirements_non_functional",
        "nfrs": "requirements_non_functional",
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
        if key == "functional":
            # Avoid matching "functional" inside "non-functional" / "non functional"
            if re.search(r"\bnon[\s-]?functional\b", h):
                continue
        if key in h:
            return mappings[key]

    # Explicit NFR phrases
    if re.search(r"\b(nfr|non[\s-]?functional)\b", h):
        return "requirements_non_functional"

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


TEXT_SUFFIXES = {
    ".md", ".mdx", ".markdown", ".txt", ".rst", ".csv", ".json",
    ".yaml", ".yml", ".html", ".htm", ".xml",
}
SKIP_DIR_NAMES = {".git", "node_modules", "__pycache__", ".next"}


def gather_input_files(paths: List[Path]) -> List[Path]:
    """Every file under a path. A folder is read in full, not only its markdown."""
    found: List[Path] = []
    for path in paths:
        if path.is_dir():
            for child in sorted(path.rglob("*")):
                if not child.is_file():
                    continue
                if any(part in SKIP_DIR_NAMES for part in child.parts):
                    continue
                if child.name == ".DS_Store" or child.name.startswith("."):
                    continue
                found.append(child)
        elif path.is_file():
            found.append(path)
    return found


def _stored_name(src: Path, root: Optional[Path]) -> str:
    if root is not None:
        try:
            rel = src.relative_to(root)
        except ValueError:
            rel = Path(src.name)
    else:
        rel = Path(src.name)
    return str(rel).replace("\\", "__").replace("/", "__")


def read_text_if_possible(path: Path) -> Optional[str]:
    if path.suffix.lower() not in TEXT_SUFFIXES:
        return None
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def copy_sources(project: str, files: List[Path], folder_root: Optional[Path] = None) -> List[Dict]:
    """Copy each handed-in file. Text is kept for the PRD. Nothing is deleted to fit a template."""
    sources_dir = PROJECTS_DIR / project / "docs" / "intake" / "sources"
    sources_dir.mkdir(parents=True, exist_ok=True)
    records: List[Dict] = []
    for src in files:
        name = _stored_name(src, folder_root if folder_root and src.is_relative_to(folder_root) else None)
        dest = sources_dir / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        if src.resolve() != dest.resolve():
            shutil.copy2(src, dest)
        text = read_text_if_possible(src)
        records.append({
            "name": src.name,
            "stored": f"docs/intake/sources/{name}",
            "text": text,
        })
    return records


def sections_from_records(records: List[Dict]) -> Dict[str, str]:
    sections: Dict[str, str] = {}
    for record in records:
        text = record.get("text") or ""
        if not text.strip():
            continue
        parsed = parse_text_input(text)
        for key, value in parsed.items():
            if not value:
                continue
            previous = sections.get(key, "")
            sections[key] = f"{previous}\n\n{value}".strip() if previous else value
    return sections


PRD_FRAME_HEADING = "## Gate 0 frame"
_FILL = "_fill_"


def prd_frame(non_goals: str = "") -> str:
    """Blocks the agent fills before gate 0 (L10). Unknown numbers stay `unknown`."""
    goals = non_goals.strip() or f"- {_FILL}"
    return f"""{PRD_FRAME_HEADING}

The agent fills these from the sources before `./studio approve --gate 0`. Write `unknown` for a number nobody knows; never invent one.

### Press release

{_FILL} — one paragraph dated on launch day: who it is for, the problem in their words, what they can now do, and one quote from a user.

### Non-goals

{goals}

### Metrics

| Metric | Baseline | Target | Window |
|--------|----------|--------|--------|
| {_FILL} | {_FILL} | {_FILL} | {_FILL} |

### Pre-mortem

It is six months after launch and the product failed. The likely reasons:

- {_FILL}
- {_FILL}
- {_FILL}
"""


def _frame_part(frame: str, name: str) -> str:
    match = re.search(rf"^###\s*{name}\b[^\n]*\n(.*?)(?=^###\s|\Z)", frame, re.I | re.M | re.S)
    return match.group(1).strip() if match else ""


def prd_frame_issues(prd_text: str) -> List[str]:
    """Gate 0: press release, non-goals, metric table, pre-mortem — filled, no placeholders."""
    start = prd_text.find(PRD_FRAME_HEADING)
    if start < 0:
        return [f"docs/intake/prd.md needs `{PRD_FRAME_HEADING}` (press release, non-goals, metrics, pre-mortem)"]
    rest = prd_text[start + len(PRD_FRAME_HEADING):]
    nxt = re.search(r"^##\s", rest, re.M)
    frame = rest[: nxt.start()] if nxt else rest
    issues: List[str] = []

    press = _frame_part(frame, "Press release")
    if not press or _FILL in press or len(press.split()) < 40:
        issues.append("Gate 0 frame: write the press release paragraph (40+ words, no _fill_)")

    goals = [ln for ln in _frame_part(frame, "Non-goals").splitlines() if re.match(r"\s*[-*]\s+\S", ln)]
    if not goals or any(_FILL in ln for ln in goals):
        issues.append("Gate 0 frame: list at least one non-goal")

    table = _frame_part(frame, "Metrics")
    header = next((ln for ln in table.splitlines() if ln.strip().startswith("|")), "")
    cols = [c.strip().lower() for c in header.strip().strip("|").split("|")]
    if not all(any(want in c for c in cols) for want in ("metric", "baseline", "target", "window")):
        issues.append("Gate 0 frame: metric table needs Metric | Baseline | Target | Window")
    else:
        rows = [
            [c.strip() for c in ln.strip().strip("|").split("|")]
            for ln in table.splitlines()[1:]
            if ln.strip().startswith("|") and not re.match(r"^\|[\s:|-]+\|?$", ln.strip())
        ]
        if not rows:
            issues.append("Gate 0 frame: metric table has no rows")
        for row in rows:
            if len(row) < 4 or any(not c or _FILL in c for c in row[:4]):
                issues.append(f"Gate 0 frame: metric row incomplete — write `unknown` instead of a blank: {'|'.join(row)}")
                break
        if rows and all(row[2].lower() == "unknown" for row in rows if len(row) >= 3):
            issues.append("Gate 0 frame: at least one metric needs a target (baseline may stay unknown)")

    reasons = [ln for ln in _frame_part(frame, "Pre-mortem").splitlines() if re.match(r"\s*[-*]\s+\S", ln)]
    if len(reasons) < 3 or any(_FILL in ln for ln in reasons):
        issues.append("Gate 0 frame: pre-mortem needs three failure reasons")
    return issues


def build_index_prd(project: str, records: List[Dict], sections: Dict[str, str], archetype: str) -> str:
    """One PRD that points at every source and keeps the text."""
    now = datetime.now().strftime("%Y-%m-%d")
    lines = [
        f"# PRD — {project}",
        "",
        "> **Status:** draft",
        f"> **Archetype:** {archetype.replace('-', ' ').title()}",
        f"> **Generated:** {now}",
        "",
        "This file is the index for architecture, design, and the milestone roadmap.",
        "Every handed-in file is copied under `docs/intake/sources/`.",
        "Text sources are repeated below in full. Other files stay on disk and are named here.",
        "Nothing is cut to fit a short template.",
        "",
        "Plan as many milestones as these sources need. M0 is the first version.",
        "Add M1, M2, M3, and further versions until the PRD and its source files are delivered.",
        "",
        "## Source index",
        "",
        "| Handed in | Kept at | In this PRD |",
        "|-----------|---------|-------------|",
    ]
    for record in records:
        where = "full text below" if record.get("text") else "file kept — read it with the index"
        lines.append(f"| {record['name']} | `{record['stored']}` | {where} |")
    lines.extend(["", "## Sources", ""])
    for record in records:
        lines.append(f"### {record['name']}")
        lines.append("")
        lines.append(f"Kept at `{record['stored']}`.")
        lines.append("")
        if record.get("text"):
            lines.append(record["text"].rstrip())
        else:
            lines.append(
                "This file is not inlined. Read it before architecture, design, and milestone planning."
            )
        lines.append("")
    guide_keys = [key for key in PRD_SECTIONS if sections.get(key)]
    lines.extend(["## Reading guide", ""])
    if not guide_keys:
        lines.append("No heading matched the old short template. The sources above are the definition.")
        lines.append("")
    else:
        lines.append("These notes repeat headings the studio recognized. The source sections above stay complete.")
        lines.append("")
        for key in guide_keys:
            title = key.replace("_", " ")
            lines.append(f"### {title}")
            lines.append("")
            lines.append(sections[key].rstrip())
            lines.append("")
    lines.append(prd_frame(_bullets(sections.get("scope_out", ""))))
    return "\n".join(lines).rstrip() + "\n"


def _bullets(text: str) -> str:
    out = [ln.rstrip() for ln in (text or "").splitlines() if re.match(r"\s*[-*]\s+\S", ln)]
    return "\n".join(out)


def run_intake(project: str, paths: List[Path], pasted: str = "") -> int:
    """Copy sources and write the index PRD. Returns 0 when at least one source was kept."""
    folder_root = paths[0] if len(paths) == 1 and paths[0].is_dir() else None
    files = gather_input_files(paths)
    records = copy_sources(project, files, folder_root)
    if pasted.strip():
        records.append({
            "name": "pasted-notes.md",
            "stored": "docs/intake/sources/pasted-notes.md",
            "text": pasted.strip(),
        })
        sources_dir = PROJECTS_DIR / project / "docs" / "intake" / "sources"
        sources_dir.mkdir(parents=True, exist_ok=True)
        (sources_dir / "pasted-notes.md").write_text(pasted.strip() + "\n", encoding="utf-8")
    if not records:
        print("Error: no files found to keep.")
        return 1

    sections = sections_from_records(records)
    joined = "\n\n".join(record.get("text") or "" for record in records)
    archetype = detect_archetype(sections, joined) if joined.strip() else "saas-application"
    prd = build_index_prd(project, records, sections, archetype)

    intake_dir = PROJECTS_DIR / project / "docs" / "intake"
    intake_dir.mkdir(parents=True, exist_ok=True)
    prd_file = intake_dir / "prd.md"
    prd_file.write_text(prd, encoding="utf-8")

    missing = [key for key, spec in PRD_SECTIONS.items() if spec["required"] and key not in sections]
    validation = {
        "project": project,
        "archetype": archetype,
        "is_valid": True,
        "sources": [record["stored"] for record in records],
        "sections_found": list(sections.keys()),
        "sections_missing": missing,
        "problems": [
            {
                "section": key,
                "type": "note",
                "message": f"Reading guide has no '{key}'. The source files still hold that material.",
                "severity": "note",
            }
            for key in missing
        ],
        "generated_at": datetime.now().isoformat(),
    }
    (intake_dir / "validation.json").write_text(
        json.dumps(validation, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    status_file = PROJECTS_DIR / project / "status.json"
    if status_file.exists():
        try:
            status = json.loads(status_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            status = {}
    else:
        status = {"name": project}
    status["archetype"] = archetype
    status["last_update"] = datetime.now().strftime("%Y-%m-%d")
    status_file.write_text(json.dumps(status, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"\n{'=' * 60}")
    print(f"  INTAKE PROCESSED: {project}")
    print(f"{'=' * 60}")
    print(f"\n  Sources kept: {len(records)}")
    print(f"  Archetype:    {archetype}")
    print(f"\n  Output:")
    print(f"    PRD:          {prd_file}")
    print(f"    Sources:      {intake_dir / 'sources'}")
    print(f"\n  Next step:")
    print(f"    1. Read the PRD index and the source files")
    print(f"    2. Fill docs/definitions/ from them")
    print(f"    3. ./studio approve {project} --gate 0")
    print()
    return 0

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

---

{prd_frame(_bullets(sections.get('scope_out', '')))}"""
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

    if sys.argv[2] == "--from-text":
        text = " ".join(sys.argv[3:])
        code = run_intake(project, [], pasted=text)
    else:
        paths = []
        for raw in sys.argv[2:]:
            path = Path(raw)
            if not path.is_absolute():
                path = Path.cwd() / path
            if not path.exists():
                print(f"Error: not found: {raw}")
                sys.exit(1)
            paths.append(path)
        code = run_intake(project, paths)
    sys.exit(code)


if __name__ == "__main__":
    main()
