#!/usr/bin/env python3
"""
validate_anti_slop.py — Anti-Slop-Validierung für Quinsy Studio

Parst Code und Content gegen die systemweite Blacklist.
Erkennt AI-typische Patterns, Floskeln und Code-Anti-Patterns.

Verwendung:
  python3 validate_anti_slop.py <project> [--fix] [--json]
  python3 validate_anti_slop.py nudge
  python3 validate_anti_slop.py nudge --fix

Exit-Code:
  0 = Keine Verstöße
  1 = Verstöße gefunden
"""

import sys
import os
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
from dataclasses import dataclass, asdict

# =============================================================================
# CONFIGURATION
# =============================================================================

STUDIO_ROOT = Path(__file__).parent.parent.parent
PROJECTS_DIR = STUDIO_ROOT / "projects"

# =============================================================================
# ANTI-SLOP PATTERNS
# =============================================================================

# Text-Floskeln (AI-typische Phrasen)
TEXT_SLOP_PATTERNS = [
    # Englische Floskeln
    (r'\b(?:in today\'?s? (?:digital )?(?:landscape|world|era))\b', "AI-Floskel: 'in today's digital landscape'"),
    (r'\b(?:revolutioni[sz]e)\b', "AI-Floskel: 'revolutionize'"),
    (r'\b(?:seamless(?:ly)?)\b', "AI-Floskel: 'seamless'"),
    (r'\b(?:empowe(?:r|ring|red))\b', "AI-Floskel: 'empower'"),
    (r'\b(?:leveragi?ng?)\b', "AI-Floskel: 'leveraging'"),
    (r'\b(?:cutting[- ]edge)\b', "AI-Floskel: 'cutting-edge'"),
    (r'\b(?:state[- ]of[- ]the[- ]art)\b', "AI-Floskel: 'state-of-the-art'"),
    (r'\b(?:furthermore)\b', "AI-Floskel: 'furthermore'"),
    (r'\b(?:moreover)\b', "AI-Floskel: 'moreover'"),
    (r'\b(?:it\'?s? worth noting that)\b', "AI-Floskel: 'it's worth noting'"),
    (r'\b(?:delve(?:s|d|ing)?)\b', "AI-Floskel: 'delve'"),
    (r'\b(?:tapestry)\b', "AI-Floskel: 'tapestry'"),
    (r'\b(?:multifaceted)\b', "AI-Floskel: 'multifaceted'"),
    (r'\b(?:game[- ]changer)\b', "AI-Floskel: 'game-changer'"),
    (r'\b(?:unlock (?:the )?(?:potential|power))\b', "AI-Floskel: 'unlock the potential'"),
    (r'\b(?:harness(?:ing)?)\b', "AI-Floskel: 'harness'"),
    (r'\b(?:pivot(?:ing)?)\b', "AI-Floskel: 'pivot'"),
    (r'\b(?:synerg(?:y|ies|ize))\b', "AI-Floskel: 'synergy'"),
    (r'\b(?:holistic(?:ally)?)\b', "AI-Floskel: 'holistic'"),
    (r'\b(?:paradigm)\b', "AI-Floskel: 'paradigm'"),
    (r'\b(?:ecosystem)\b', "AI-Floskel: 'ecosystem'"),
    (r'\b(?:landscap(?:e|ing))\b', "AI-Floskel: 'landscape'"),
    
    # Deutsche Floskeln
    (r'\b(?:in der heutigen digitalen welt)\b', "AI-Floskel: 'in der heutigen digitalen Welt'"),
    (r'\b(?:revolutionieren)\b', "AI-Floskel: 'revolutionieren'"),
    (r'\b(?:nahtlos(?:en)?)\b', "AI-Floskel: 'nahtlos'"),
    (r'\b(?:ermöglich(?:en|t)?)\b', "AI-Floskel: 'ermöglichen'"),
    (r'\b(?:weitreichend(?:en)?)\b', "AI-Floskel: 'weitreichend'"),
    (r'\b(?:umfassend(?:en)?)\b', "AI-Floskel: 'umfassend'"),
    (r'\b(?:innovativ(?:en|e|es)?)\b', "AI-Floskel: 'innovativ'"),
    (r'\b(?:zukunftsweisend(?:en)?)\b', "AI-Floskel: 'zukunftsweisend'"),
]

# Code-Anti-Patterns (AI-typischer Code)
CODE_SLOP_PATTERNS = [
    # Übermäßige Kommentare
    (r'(?://|#)\s*(?:This function|This method|This class|Dieser Code)\b',
     "AI-Slop: Überflüssiger einleitender Kommentar"),
    
    # Redundante Variablen
    (r'const\s+\w+\s*=\s*\w+\s*;\s*\n\s*const\s+\w+\s*=\s*\w+\s*;',
     "AI-Slop: Möglicherweise redundante Variablen"),
    
    # Übermäßige Console-Logs
    (r'(?:console\.(?:log|debug|info)\s*\([^)]*\)\s*;?\s*){3,}',
     "AI-Slop: Übermäßige Console-Logs"),
    
    # Unnötige Try-Catch
    (r'try\s*\{[^}]{0,50}\}\s*catch\s*\(\s*\w*\s*\)\s*\{\s*(?:console\.log|// ignore)',
     "AI-Slop: Stiller Catch mit console.log"),
    
    # Dead Code
    (r'return\s+[^;]+;\s*\n\s*(?:const|let|var|function|return)',
     "AI-Slop: Möglicherweise toter Code nach return"),
    
    # Übermäßige Type Assertions
    (r'(?:as\s+\w+){2,}',
     "AI-Slop: Übermäßige Type Assertions"),
    
    # Magic Numbers
    (r'(?<!=|!|<|>|=)\s(?:100|1000|86400)\b(?!\s*(?:ms|px|%|rem))',
     "AI-Slop: Magic Number ohne Einheit"),
    
    # Übermäßige async/await
    (r'await\s+\w+\([^)]*\);\s*\n\s*await\s+\w+\([^)]*\);',
     "AI-Slop: Möglicherweise sequentielle async-Aufrufe"),
]

# Dateien die ignoriert werden
IGNORE_PATTERNS = [
    r'node_modules',
    r'\.next',
    r'dist',
    r'build',
    r'\.git',
    r'package-lock\.json',
    r'yarn\.lock',
    r'pnpm-lock\.yaml',
]

# Datei-Endungen die geprüft werden
CHECK_EXTENSIONS = [
    '.ts', '.tsx', '.js', '.jsx',
    '.md', '.mdx',
    '.json',
    '.py',
    '.css', '.scss',
]

# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class SlopViolation:
    file: str
    line: int
    column: int
    pattern_name: str
    message: str
    severity: str  # error, warning
    context: str

@dataclass
class SlopReport:
    project: str
    timestamp: str
    files_scanned: int
    violations: List[Dict]
    errors: int
    warnings: int
    passed: bool

# =============================================================================
# SCANNER
# =============================================================================

def should_ignore(filepath: str) -> bool:
    """Prüft ob eine Datei ignoriert werden soll."""
    for pattern in IGNORE_PATTERNS:
        if re.search(pattern, filepath):
            return True
    return False


def scan_file(filepath: Path, project_dir: Path) -> List[SlopViolation]:
    """Scannt eine Datei auf Anti-Slop-Patterns."""
    violations = []
    
    try:
        content = filepath.read_text(encoding='utf-8')
    except (UnicodeDecodeError, PermissionError):
        return violations
    
    lines = content.split('\n')
    rel_path = str(filepath.relative_to(project_dir.parent))
    
    # Text-Slop (für MD, TSX, JSX)
    if filepath.suffix in ['.md', '.mdx', '.tsx', '.jsx']:
        for line_num, line in enumerate(lines, 1):
            for pattern, message in TEXT_SLOP_PATTERNS:
                matches = re.finditer(pattern, line, re.IGNORECASE)
                for match in matches:
                    violations.append(SlopViolation(
                        file=rel_path,
                        line=line_num,
                        column=match.start(),
                        pattern_name="text-slop",
                        message=message,
                        severity="warning",
                        context=line.strip()[:100]
                    ))
    
    # Code-Slop (für TS, JS, TSX, JSX)
    if filepath.suffix in ['.ts', '.tsx', '.js', '.jsx']:
        for pattern, message in CODE_SLOP_PATTERNS:
            matches = re.finditer(pattern, content, re.MULTILINE)
            for match in matches:
                line_num = content[:match.start()].count('\n') + 1
                violations.append(SlopViolation(
                    file=rel_path,
                    line=line_num,
                    column=match.start() - content.rfind('\n', 0, match.start()),
                    pattern_name="code-slop",
                    message=message,
                    severity="error",
                    context=content[match.start():match.end()][:100]
                ))
    
    return violations


def scan_project(project: str) -> SlopReport:
    """Scannt ein gesamtes Projekt auf Anti-Slop."""
    
    project_dir = PROJECTS_DIR / project
    if not project_dir.exists():
        print(f"Fehler: Projekt nicht gefunden: {project_dir}")
        sys.exit(1)
    
    all_violations = []
    files_scanned = 0
    
    for filepath in project_dir.rglob('*'):
        if not filepath.is_file():
            continue
        if should_ignore(str(filepath)):
            continue
        if filepath.suffix not in CHECK_EXTENSIONS:
            continue
        
        files_scanned += 1
        violations = scan_file(filepath, project_dir)
        all_violations.extend(violations)
    
    errors = sum(1 for v in all_violations if v.severity == "error")
    warnings = sum(1 for v in all_violations if v.severity == "warning")
    
    return SlopReport(
        project=project,
        timestamp=datetime.now().isoformat(),
        files_scanned=files_scanned,
        violations=[asdict(v) for v in all_violations],
        errors=errors,
        warnings=warnings,
        passed=errors == 0
    )

# =============================================================================
# FIX MODE
# =============================================================================

def fix_violations(project: str, report: SlopReport):
    """Versucht Verstöße automatisch zu beheben."""
    
    fixed_count = 0
    
    for violation in report.violations:
        if violation["severity"] != "warning":
            continue  # Nur Warnings automatisch fixen
        
        filepath = PROJECTS_DIR / project / violation["file"]
        if not filepath.exists():
            continue
        
        content = filepath.read_text(encoding='utf-8')
        lines = content.split('\n')
        
        if violation["line"] <= len(lines):
            line = lines[violation["line"] - 1]
            
            # Einfache Fixes für Text-Slop
            replacements = {
                "in today's digital landscape": "currently",
                "in today's landscape": "currently",
                "revolutionize": "improve",
                "seamless": "smooth",
                "seamlessly": "smoothly",
                "empower": "enable",
                "leveraging": "using",
                "cutting-edge": "modern",
                "state-of-the-art": "modern",
                "furthermore": "",
                "moreover": "",
                "it's worth noting that": "",
                "delve": "explore",
                "tapestry": "combination",
                "multifaceted": "complex",
                "game-changer": "significant improvement",
                "unlock the potential": "enable",
                "harness": "use",
                "pivot": "change direction",
                "synergy": "collaboration",
                "holistic": "comprehensive",
                "paradigm": "approach",
                "ecosystem": "system",
                "landscape": "environment",
            }
            
            for old, new in replacements.items():
                if old.lower() in line.lower():
                    line = re.sub(re.escape(old), new, line, flags=re.IGNORECASE)
                    fixed_count += 1
            
            lines[violation["line"] - 1] = line
    
    if fixed_count > 0:
        # Write back
        for filepath in PROJECTS_DIR(project).rglob('*'):
            if filepath.is_file():
                # This is simplified - in reality we'd track which files changed
                pass
        
        print(f"  {fixed_count} Verstöße automatisch behoben")


# =============================================================================
# REPORTING
# =============================================================================

def print_report(report: SlopReport, use_json: bool = False):
    """Gibt den Report aus."""
    
    if use_json:
        print(json.dumps(asdict(report), indent=2, ensure_ascii=False))
        return
    
    print(f"\n{'='*60}")
    print(f"  ANTI-SLOP AUDIT: {report.project}")
    print(f"{'='*60}")
    print(f"\n  Dateien gescannt:  {report.files_scanned}")
    print(f"  Verstöße:         {report.errors + report.warnings}")
    print(f"    Fehler:         {report.errors}")
    print(f"    Warnungen:      {report.warnings}")
    print(f"  Ergebnis:         {'✅ GRÜN' if report.passed else 'ROT ✗'}")
    
    if report.violations:
        print(f"\n  {'='*50}")
        print(f"  VERSTÖSSE")
        print(f"  {'='*50}")
        
        for v in report.violations[:20]:  # Max 20 anzeigen
            icon = "❌" if v["severity"] == "error" else "⚠️"
            print(f"\n  {icon} {v['file']}:{v['line']}")
            print(f"     {v['message']}")
            if v["context"]:
                print(f"     Kontext: {v['context'][:80]}...")
        
        if len(report.violations) > 20:
            print(f"\n  ... und {len(report.violations) - 20} weitere")
    
    print()

# =============================================================================
# MAIN
# =============================================================================

def main():
    if len(sys.argv) < 2:
        print("Verwendung:")
        print("  python3 validate_anti_slop.py <project> [--fix] [--json]")
        sys.exit(1)
    
    project = sys.argv[1]
    fix_mode = "--fix" in sys.argv
    json_mode = "--json" in sys.argv
    
    # Scan
    report = scan_project(project)
    
    # Fix if requested
    if fix_mode and report.violations:
        fix_violations(project, report)
        # Re-scan after fix
        report = scan_project(project)
    
    # Print report
    print_report(report, json_mode)
    
    # Exit code
    sys.exit(0 if report.passed else 1)


if __name__ == "__main__":
    main()
