#!/usr/bin/env python3
"""
run_qa_gate.py — QA orchestrator for Quinsy Studio

Runs complete QA checks:
- Linting (ESLint/Prettier)
- Type checking (TypeScript)
- Unit tests (Vitest/Jest)
- Build check
- Dependency check (npm audit)
- Anti-slop audit

Usage:
  python3 run_qa_gate.py <project> [--level N] [--fix]
  python3 run_qa_gate.py nudge
  python3 run_qa_gate.py nudge --level 5

Exit code:
  0 = all checks passed
  1 = at least one check failed
"""

import sys
import os
import json
import subprocess
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict

# =============================================================================
# CONFIGURATION
# =============================================================================

STUDIO_ROOT = Path(__file__).parent.parent.parent
PROJECTS_DIR = STUDIO_ROOT / "projects"

@dataclass
class QACheck:
    name: str
    command: str
    description: str
    required: bool = True
    timeout: int = 120  # seconds

@dataclass
class QAResult:
    check: str
    passed: bool
    output: str
    duration: float
    error: Optional[str] = None

@dataclass
class QAReport:
    project: str
    level: int
    timestamp: str
    results: List[Dict]
    passed: bool
    total_duration: float
    summary: Dict

# =============================================================================
# CHECK DEFINITIONS
# =============================================================================

def get_checks_for_level(level: int) -> List[QACheck]:
    """Return the checks for a given gate level."""
    
    checks = []
    
    # Level 0-1: Basis-Checks
    if level >= 0:
        checks.extend([
            QACheck(
                name="package_json_exists",
                command="test -f package.json",
                description="package.json exists"
            ),
            QACheck(
                name="node_modules_exists",
                command="test -d node_modules",
                description="node_modules exists (npm install run?)"
            ),
        ])
    
    # Level 2: Linting
    if level >= 2:
        checks.extend([
            QACheck(
                name="eslint",
                command="npx eslint . --max-warnings 0",
                description="ESLint (no warnings)",
                timeout=60
            ),
            QACheck(
                name="prettier",
                command="npx prettier --check .",
                description="Prettier formatting",
                timeout=30
            ),
        ])
    
    # Level 3: Type-Checking
    if level >= 3:
        checks.extend([
            QACheck(
                name="typescript",
                command="npx tsc --noEmit",
                description="TypeScript type check",
                timeout=120
            ),
        ])
    
    # Level 4: Tests
    if level >= 4:
        checks.extend([
            QACheck(
                name="unit_tests",
                command="npx vitest run --reporter=verbose",
                description="Unit tests (Vitest)",
                timeout=120
            ),
        ])
    
    # Level 5: Full QA
    if level >= 5:
        checks.extend([
            QACheck(
                name="build",
                command="npx next build",
                description="Build check",
                timeout=180
            ),
            QACheck(
                name="npm_audit",
                command="npm audit --audit-level=moderate",
                description="Dependency Security Check",
                timeout=60
            ),
            QACheck(
                name="anti_slop",
                command=f"python3 {Path(__file__).parent}/validate_anti_slop.py {sys.argv[1] if len(sys.argv) > 1 else '.'}",
                description="Anti-Slop Audit",
                timeout=60
            ),
        ])
    
    return checks

# =============================================================================
# CHECK EXECUTION
# =============================================================================

def run_check(check: QACheck, project_dir: Path) -> QAResult:
    """Run a single check."""
    
    start_time = datetime.now()
    
    try:
        result = subprocess.run(
            check.command,
            shell=True,
            cwd=str(project_dir),
            capture_output=True,
            text=True,
            timeout=check.timeout
        )
        
        duration = (datetime.now() - start_time).total_seconds()
        
        return QAResult(
            check=check.name,
            passed=result.returncode == 0,
            output=result.stdout + result.stderr,
            duration=duration,
            error=None if result.returncode == 0 else f"Exit code: {result.returncode}"
        )
        
    except subprocess.TimeoutExpired:
        duration = (datetime.now() - start_time).total_seconds()
        return QAResult(
            check=check.name,
            passed=False,
            output="",
            duration=duration,
            error=f"Timeout after {check.timeout}s"
        )
        
    except Exception as e:
        duration = (datetime.now() - start_time).total_seconds()
        return QAResult(
            check=check.name,
            passed=False,
            output="",
            duration=duration,
            error=str(e)
        )

# =============================================================================
# SPECIAL CHECKS
# =============================================================================

def check_project_structure(project_dir: Path) -> QAResult:
    """Check whether the project structure is correct."""
    
    required_dirs = [
        "docs",
        "backlog",
    ]
    
    required_files = [
        "docs/intake/prd.md",
        "status.json",
    ]
    
    missing = []
    
    for d in required_dirs:
        if not (project_dir / d).exists():
            missing.append(f"Directory: {d}")
    
    for f in required_files:
        if not (project_dir / f).exists():
            missing.append(f"File: {f}")
    
    if missing:
        return QAResult(
            check="project_structure",
            passed=False,
            output="\n".join(missing),
            duration=0,
            error=f"Missing elements: {', '.join(missing)}"
        )
    
    return QAResult(
        check="project_structure",
        passed=True,
        output="Project structure complete",
        duration=0
    )


def check_skill_matching() -> QAResult:
    """Run the skill-matching test (skill-registry integrity)."""
    
    test_script = Path(__file__).parent / "test_skill_matching.py"
    if not test_script.exists():
        return QAResult(
            check="skill_matching",
            passed=False,
            output="",
            duration=0,
            error=f"Test script missing: {test_script}"
        )
    
    start_time = datetime.now()
    try:
        result = subprocess.run(
            [sys.executable, str(test_script)],
            capture_output=True,
            text=True,
            timeout=60
        )
        duration = (datetime.now() - start_time).total_seconds()
        
        return QAResult(
            check="skill_matching",
            passed=result.returncode == 0,
            output=result.stdout + result.stderr,
            duration=duration,
            error=None if result.returncode == 0 else "Skill-matching test failed"
        )
    except subprocess.TimeoutExpired:
        return QAResult(
            check="skill_matching",
            passed=False,
            output="",
            duration=(datetime.now() - start_time).total_seconds(),
            error="Timeout nach 60s"
        )


def check_status_json(project_dir: Path) -> QAResult:
    """Check whether status.json is valid."""
    
    status_file = project_dir / "status.json"
    
    if not status_file.exists():
        return QAResult(
            check="status_json",
            passed=False,
            output="status.json not present",
            duration=0,
            error="File missing"
        )
    
    try:
        with open(status_file, 'r') as f:
            status = json.load(f)
        
        required_fields = ["name", "phase", "gate", "archetype"]
        missing = [f for f in required_fields if f not in status]
        
        if missing:
            return QAResult(
                check="status_json",
                passed=False,
                output=json.dumps(status, indent=2),
                duration=0,
                error=f"Missing fields: {', '.join(missing)}"
            )
        
        return QAResult(
            check="status_json",
            passed=True,
            output=json.dumps(status, indent=2),
            duration=0
        )
        
    except json.JSONDecodeError as e:
        return QAResult(
            check="status_json",
            passed=False,
            output="",
            duration=0,
            error=f"Invalid JSON: {e}"
        )

# =============================================================================
# REPORTING
# =============================================================================

def print_report(report: QAReport, use_json: bool = False):
    """Print the QA report."""
    
    if use_json:
        print(json.dumps(asdict(report), indent=2, ensure_ascii=False))
        return
    
    print(f"\n{'='*60}")
    print(f"  QA-GATE: {report.project} (Level {report.level})")
    print(f"{'='*60}")
    
    passed_count = sum(1 for r in report.results if r["passed"])
    total_count = len(report.results)
    
    for result in report.results:
        icon = "✅" if result["passed"] else "❌"
        duration_str = f" ({result['duration']:.1f}s)" if result["duration"] > 0 else ""
        print(f"\n  {icon} {result['check']}{duration_str}")
        
        if not result["passed"] and result.get("error"):
            print(f"     Error: {result['error']}")
            if result["output"]:
                # Show first few lines of output
                output_lines = result["output"].strip().split('\n')[:5]
                for line in output_lines:
                    print(f"     {line}")
    
    print(f"\n  {'='*50}")
    print(f"  RESULT: {report.passed}")
    print(f"  Passed: {passed_count}/{total_count}")
    print(f"  Duration: {report.total_duration:.1f}s")
    print(f"  {'='*50}")
    
    if report.passed:
        print(f"\n  ✅ All QA checks passed. Ticket can be marked as 'done'.")
    else:
        print(f"\n  ❌ QA checks failed. Ticket must go back to phase 4 (implementation).")
    
    print()

# =============================================================================
# MAIN
# =============================================================================

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 run_qa_gate.py <project> [--level N] [--json]")
        sys.exit(1)
    
    project = sys.argv[1]
    level = 5  # Default: Full QA
    json_mode = "--json" in sys.argv
    
    # Parse level
    for i, arg in enumerate(sys.argv):
        if arg == "--level" and i + 1 < len(sys.argv):
            level = int(sys.argv[i + 1])
    
    project_dir = PROJECTS_DIR / project
    if not project_dir.exists():
        print(f"Error: project not found: {project_dir}")
        sys.exit(1)
    
    print(f"\n  Starting QA gate level {level} for {project}...")
    
    # Get checks for level
    checks = get_checks_for_level(level)
    
    # Add special checks
    checks.insert(0, QACheck(
        name="project_structure",
        command="",
        description="Project structure"
    ))
    checks.insert(1, QACheck(
        name="status_json",
        command="",
        description="status.json valid"
    ))
    if level >= 5:
        checks.append(QACheck(
            name="skill_matching",
            command="",
            description="Skill-matching test (registry integrity)"
        ))
    
    # Execute checks
    results = []
    total_start = datetime.now()
    
    for check in checks:
        print(f"\n  Running: {check.description}...", end="", flush=True)
        
        if check.name == "project_structure":
            result = check_project_structure(project_dir)
        elif check.name == "status_json":
            result = check_status_json(project_dir)
        elif check.name == "skill_matching":
            result = check_skill_matching()
        else:
            result = run_check(check, project_dir)
        
        results.append(result)
        
        icon = "✅" if result.passed else "❌"
        print(f" {icon}")
    
    total_duration = (datetime.now() - total_start).total_seconds()
    
    # Build report
    passed = all(r.passed for r in results if r.check not in ["npm_audit"])  # npm audit is warning
    
    report = QAReport(
        project=project,
        level=level,
        timestamp=datetime.now().isoformat(),
        results=[asdict(r) for r in results],
        passed=passed,
        total_duration=total_duration,
        summary={
            "total_checks": len(results),
            "passed": sum(1 for r in results if r.passed),
            "failed": sum(1 for r in results if not r.passed)
        }
    )
    
    # Print report
    print_report(report, json_mode)
    
    # Save report
    report_file = project_dir / "docs" / f"qa-report-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    report_file.parent.mkdir(parents=True, exist_ok=True)
    report_file.write_text(json.dumps(asdict(report), indent=2, ensure_ascii=False))
    
    # Exit code
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
