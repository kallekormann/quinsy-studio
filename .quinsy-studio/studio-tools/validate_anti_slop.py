#!/usr/bin/env python3
"""
validate_anti_slop.py — Anti-slop validation for Quinsy Studio

Parses code and content against the system-wide blacklist.
Detects AI-typical patterns, clichés and code anti-patterns.

Usage:
  python3 validate_anti_slop.py <project> [--fix] [--json]
  python3 validate_anti_slop.py nudge
  python3 validate_anti_slop.py nudge --fix

Exit code:
  0 = no violations
  1 = violations found
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

# Text clichés (AI-typical phrases)
TEXT_SLOP_PATTERNS = [
    (r'\b(?:in today\'?s? (?:digital )?(?:landscape|world|era))\b', "AI cliché: 'in today's digital landscape'"),
    (r'\b(?:revolutioni[sz]e)\b', "AI cliché: 'revolutionize'"),
    (r'\b(?:seamless(?:ly)?)\b', "AI cliché: 'seamless'"),
    (r'\b(?:empowe(?:r|ring|red))\b', "AI cliché: 'empower'"),
    (r'\b(?:leveragi?ng?)\b', "AI cliché: 'leveraging'"),
    (r'\b(?:cutting[- ]edge)\b', "AI cliché: 'cutting-edge'"),
    (r'\b(?:state[- ]of[- ]the[- ]art)\b', "AI cliché: 'state-of-the-art'"),
    (r'\b(?:furthermore)\b', "AI cliché: 'furthermore'"),
    (r'\b(?:moreover)\b', "AI cliché: 'moreover'"),
    (r'\b(?:it\'?s? worth noting that)\b', "AI cliché: 'it's worth noting'"),
    (r'\b(?:delve(?:s|d|ing)?)\b', "AI cliché: 'delve'"),
    (r'\b(?:tapestry)\b', "AI cliché: 'tapestry'"),
    (r'\b(?:multifaceted)\b', "AI cliché: 'multifaceted'"),
    (r'\b(?:game[- ]changer)\b', "AI cliché: 'game-changer'"),
    (r'\b(?:unlock (?:the )?(?:potential|power))\b', "AI cliché: 'unlock the potential'"),
    (r'\b(?:harness(?:ing)?)\b', "AI cliché: 'harness'"),
    (r'\b(?:pivot(?:ing)?)\b', "AI cliché: 'pivot'"),
    (r'\b(?:synerg(?:y|ies|ize))\b', "AI cliché: 'synergy'"),
    (r'\b(?:holistic(?:ally)?)\b', "AI cliché: 'holistic'"),
    (r'\b(?:paradigm)\b', "AI cliché: 'paradigm'"),
    (r'\b(?:ecosystem)\b', "AI cliché: 'ecosystem'"),
    (r'\b(?:landscap(?:e|ing))\b', "AI cliché: 'landscape'"),
    # Principal Product Designer anti-fluff vocabulary (anti-slop-design-ux.md §2.1)
    (r'\b(?:supercharge(?:s|d)?)\b', "Fluff copy: 'supercharge'"),
    (r'\b(?:streamlin(?:e|es|ed|ing))\b', "Fluff copy: 'streamline'"),
    (r'\b(?:turbo(?:charge)?)\b', "Fluff copy: 'turbo'"),
    (r'\b(?:next[- ]level)\b', "Fluff copy: 'next-level'"),
    (r'\b(?:hyper[-\s]?\w+)\b', "Fluff copy: 'hyper-' prefix"),
    (r'\b(?:empowerment)\b', "Fluff copy: 'empowerment'"),
    (r'\b(?:delight(?:ful|s|ed)?)\b', "Fluff copy: 'delight'"),
    (r'\b(?:robust)\b', "Fluff copy: 'robust' (use specific quality claim)"),
    (r'\b(?:unlock)\b', "Fluff copy: 'unlock'"),
    (r'\btransform(?:s|ed|ing)?\s+(?:your|the|our|their)\s+\w+', "Fluff copy: 'transform' (marketing)"),
]

# Generic mock / UI placeholder copy (design slop)
UI_PLACEHOLDER_PATTERNS = [
    (r'\bLorem ipsum\b', "Placeholder copy: Lorem ipsum — use domain-realistic text"),
    (r'\bFeature [1-9]\b', "Placeholder copy: generic 'Feature N' label"),
    (r'\bPrimary action\b', "Placeholder CTA: use literal action label"),
    (r'\bSecondary action\b', "Placeholder CTA: use literal action label"),
    (r'\bMake magic happen\b', "Vague CTA: state what happens on click"),
    (r"\bLet'?s do it\b", "Vague CTA: state what happens on click"),
    (r">(?:Proceed|Let's go|Let us go)<", "Vague CTA: state what happens on click"),
    (r'"(?:Proceed|Let\'s go|Let us go)"', "Vague CTA: state what happens on click"),
    (r"'(?:Proceed|Let's go|Let us go)'", "Vague CTA: state what happens on click"),
]

# Files scanned for placeholder / fluff copy in UI strings
COPY_SCAN_EXTENSIONS = {'.md', '.mdx', '.tsx', '.jsx', '.html'}


def is_copy_scan_path(rel_path: str) -> bool:
    """Limit fluff/placeholder detection to UI and design-spec surfaces."""
    normalized = rel_path.replace('\\', '/')
    if any(marker in normalized for marker in ('/src/', '/docs/design-specs/', 'brand-guide')):
        return True
    if '/packages/' in normalized and normalized.endswith(('.html', '.tsx', '.jsx')):
        return True
    return False

# Code anti-patterns (AI-typical code)
CODE_SLOP_PATTERNS = [
    # Excessive comments
    (r'(?://|#)\s*(?:This function|This method|This class)\b',
     "AI slop: redundant leading comment"),
    
    # Redundant variables
    (r'const\s+\w+\s*=\s*\w+\s*;\s*\n\s*const\s+\w+\s*=\s*\w+\s*;',
     "AI slop: possibly redundant variables"),
    
    # Excessive console logs
    (r'(?:console\.(?:log|debug|info)\s*\([^)]*\)\s*;?\s*){3,}',
     "AI slop: excessive console logs"),
    
    # Unnecessary try-catch
    (r'try\s*\{[^}]{0,50}\}\s*catch\s*\(\s*\w*\s*\)\s*\{\s*(?:console\.log|// ignore)',
     "AI slop: silent catch with console.log"),
    
    # Dead code after a completed return (same indent). Nested JSX returns are deeper indent.
    (r'(?m)^(\s*)return\s+[^;\n]+;\s*\n\1(?:const|let|var|function|return)\b',
     "AI slop: possible dead code after return"),
    
    # Excessive type assertions
    (r'(?:as\s+\w+){2,}',
     "AI slop: excessive type assertions"),
    
    # Magic numbers (LO-0029: fix with named consts — not test-file exemptions)
    (r'(?<!=|!|<|>|=)\s(?:100|1000|86400)\b(?!\s*(?:ms|px|%|rem))',
     "AI slop: magic number without unit — use a named constant (e.g. JPEG_QUALITY_PERCENT = 100)"),
    
    # Excessive async/await (LO-0029: chain, helper, or Promise.all — not disable rule)
    (r'await\s+\w+\([^)]*\);\s*\n\s*await\s+\w+\([^)]*\);',
     "AI slop: sequential await/await — chain, extract helper, or Promise.all"),
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

# File extensions that are checked
CHECK_EXTENSIONS = [
    '.ts', '.tsx', '.js', '.jsx',
    '.md', '.mdx',
    '.html',
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
    """Check whether a file should be ignored."""
    for pattern in IGNORE_PATTERNS:
        if re.search(pattern, filepath):
            return True
    return False


def scan_file(filepath: Path, project_dir: Path) -> List[SlopViolation]:
    """Scan a file for anti-slop patterns."""
    violations = []
    
    try:
        content = filepath.read_text(encoding='utf-8')
    except (UnicodeDecodeError, PermissionError):
        return violations
    
    lines = content.split('\n')
    rel_path = str(filepath.relative_to(project_dir))
    
    # Copy slop — scoped to UI / design-spec paths only
    if filepath.suffix in COPY_SCAN_EXTENSIONS and is_copy_scan_path(rel_path):
        for line_num, line in enumerate(lines, 1):
            for pattern, message in TEXT_SLOP_PATTERNS:
                matches = re.finditer(pattern, line, re.IGNORECASE)
                for match in matches:
                    violations.append(SlopViolation(
                        file=rel_path,
                        line=line_num,
                        column=match.start(),
                        pattern_name="copy-slop",
                        message=message,
                        severity="warning",
                        context=line.strip()[:100]
                    ))
            for pattern, message in UI_PLACEHOLDER_PATTERNS:
                matches = re.finditer(pattern, line, re.IGNORECASE)
                for match in matches:
                    violations.append(SlopViolation(
                        file=rel_path,
                        line=line_num,
                        column=match.start(),
                        pattern_name="ui-placeholder",
                        message=message,
                        severity="warning",
                        context=line.strip()[:100]
                    ))
    
    # Code slop (for TS, JS, TSX, JSX)
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
    """Scan an entire project for anti-slop."""
    
    project_dir = PROJECTS_DIR / project
    if not project_dir.exists():
        print(f"Error: project not found: {project_dir}")
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
    """Try to fix violations automatically (text slop warnings only)."""
    project_dir = PROJECTS_DIR / project
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
        "supercharge": "improve",
        "streamline": "simplify",
        "next-level": "improved",
        "delight": "satisfy",
        "unlock": "enable",
    }

    # Group violations by file
    by_file: Dict[str, List[dict]] = {}
    for violation in report.violations:
        if violation["severity"] != "warning":
            continue
        by_file.setdefault(violation["file"], []).append(violation)

    fixed_count = 0
    for rel_path, violations in by_file.items():
        filepath = project_dir / rel_path
        if not filepath.exists():
            continue
        lines = filepath.read_text(encoding="utf-8").split("\n")
        for violation in violations:
            line_idx = violation["line"] - 1
            if line_idx < 0 or line_idx >= len(lines):
                continue
            line = lines[line_idx]
            for old, new in replacements.items():
                if old.lower() in line.lower():
                    line = re.sub(re.escape(old), new, line, flags=re.IGNORECASE)
                    fixed_count += 1
            lines[line_idx] = line
        filepath.write_text("\n".join(lines), encoding="utf-8")

    if fixed_count > 0:
        print(f"  {fixed_count} violations fixed automatically")


# =============================================================================
# REPORTING
# =============================================================================

def print_report(report: SlopReport, use_json: bool = False):
    """Print the report."""
    
    if use_json:
        print(json.dumps(asdict(report), indent=2, ensure_ascii=False))
        return
    
    print(f"\n{'='*60}")
    print(f"  ANTI-SLOP AUDIT: {report.project}")
    print(f"{'='*60}")
    print(f"\n  Files scanned:  {report.files_scanned}")
    print(f"  Violations:     {report.errors + report.warnings}")
    print(f"    Errors:       {report.errors}")
    print(f"    Warnings:     {report.warnings}")
    print(f"  Result:         {'✅ GREEN' if report.passed else 'RED ✗'}")
    
    if report.violations:
        print(f"\n  {'='*50}")
        print(f"  VIOLATIONS")
        print(f"  {'='*50}")
        
        for v in report.violations[:20]:  # Show max 20
            icon = "❌" if v["severity"] == "error" else "⚠️"
            print(f"\n  {icon} {v['file']}:{v['line']}")
            print(f"     {v['message']}")
            if v["context"]:
                print(f"     Context: {v['context'][:80]}...")
        
        if len(report.violations) > 20:
            print(f"\n  ... and {len(report.violations) - 20} more")
    
    print()

# =============================================================================
# MAIN
# =============================================================================

def main():
    if len(sys.argv) < 2:
        print("Usage:")
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
