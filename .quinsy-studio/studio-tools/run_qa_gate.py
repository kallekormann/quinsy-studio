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
  python3 run_qa_gate.py demo
  python3 run_qa_gate.py demo --level 5

Exit code:
  0 = all checks passed
  1 = at least one check failed
"""

import sys
import os
import json
import subprocess
import re
import platform
from pathlib import Path
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from studio_env import redact_secret_patterns

# =============================================================================
# CONFIGURATION
# =============================================================================

STUDIO_ROOT = Path(__file__).parent.parent.parent
QUINSY_DIR = Path(__file__).parent.parent  # .quinsy-studio/
PROJECTS_DIR = STUDIO_ROOT / "projects"

from security_checks import HARD_LEVEL_2, HARD_LEVEL_5, WARN_CHECKS
from quality_checks import QUALITY_HARD, QUALITY_SOFT

# Advisory checks: shown as ⚠️, never fail RESULT.
SOFT_CHECKS = {"npm_audit", "skill_application", *WARN_CHECKS, *QUALITY_SOFT}
# Static checks run in-process (security_checks / quality_checks), not as shell commands.
STATIC_CHECKS = {*HARD_LEVEL_2, *HARD_LEVEL_5, *WARN_CHECKS, *QUALITY_HARD, *QUALITY_SOFT}

# Durable Playwright browser cache (LO-0052) — not Cursor sandbox temp paths.
PLAYWRIGHT_CACHE_ROOT = QUINSY_DIR / ".cache" / "playwright"

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
    # Did not run (no config, sandbox opt-out). Does not fail RESULT, but the
    # receipt must say NOT TESTED; it is never reported as a pass.
    not_tested: bool = False

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
                command="npx --no-install eslint . --max-warnings 0",
                description="ESLint (no warnings)",
                timeout=60
            ),
            QACheck(
                name="prettier",
                command=(
                    "npx --no-install prettier --check . "
                    "--ignore-path .prettierignore"
                ),
                description="Prettier formatting",
                timeout=30
            ),
        ])
        checks.extend(
            QACheck(name=name, command="", description=f"Security: {name}", timeout=60)
            for name in HARD_LEVEL_2
        )
    
    # Level 3: Type-Checking
    if level >= 3:
        checks.extend([
            QACheck(
                name="typescript",
                command="npx --no-install tsc --noEmit",
                description="TypeScript type check",
                timeout=120
            ),
        ])
    
    # Level 4: Tests
    if level >= 4:
        checks.extend([
            QACheck(
                name="unit_tests",
                command="npx --no-install vitest run --reporter=verbose",
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
                name="smoke_routes",
                command="",  # special handler
                description="Runtime smoke tests (critical routes)",
                timeout=180
            ),
            QACheck(
                # LO-0165 / LO-0261: moderate @vitest/mocker (and the same class)
                # stays a warning — excluded from RESULT in hard_failed below.
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
            QACheck(
                name="skill_application",
                command="",
                description="Skill application (token literals / native select — soft)",
                timeout=30,
                required=False,
            ),
            QACheck(
                name="npm_audit_policy",
                command="",
                description="Dependency policy (high/critical in production deps)",
                timeout=90,
            ),
            QACheck(
                name="ui_motion",
                command="",
                description="Motion shipped as the §2d spec names it (design-track tickets in flight)",
                timeout=30,
            ),
        ])
        checks.extend(
            QACheck(name=name, command="", description=f"Security: {name}", timeout=60)
            for name in HARD_LEVEL_5
        )
        checks.extend(
            QACheck(name=name, command="", description=f"Quality: {name}", timeout=60)
            for name in QUALITY_HARD
        )
        checks.extend(
            QACheck(name=name, command="", description=f"Advisory: {name}", timeout=60, required=False)
            for name in (*WARN_CHECKS, *QUALITY_SOFT)
        )
    
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

def check_skill_application(project_dir: Path) -> QAResult:
    """Soft warn: token hex / rgb and native <select> in product UI (LO-0334 / LO-0338)."""
    from studio_skill_checks import format_scan_report, scan_project

    start_time = datetime.now()
    warnings, _hard = scan_project(project_dir)
    duration = (datetime.now() - start_time).total_seconds()
    report = format_scan_report(warnings)
    return QAResult(
        check="skill_application",
        passed=len(warnings) == 0,
        output=report,
        duration=duration,
        error=None if not warnings else f"{len(warnings)} skill-application warning(s)",
    )


def check_ui_motion(project_dir: Path) -> QAResult:
    """Hard at level 5: §2d motion tokens, reduced-motion path, no second animation layer (LO-0400)."""
    from gate_ui_checks import motion_findings

    start_time = datetime.now()
    findings = motion_findings(project_dir)
    duration = (datetime.now() - start_time).total_seconds()
    return QAResult(
        check="ui_motion",
        passed=not findings,
        output="\n".join(findings) if findings else "clean (or no design-track ticket in flight)",
        duration=duration,
        error=None if not findings else f"{len(findings)} motion finding(s)",
    )


def harden_for_ui(project_dir: Path) -> bool:
    """A UI ticket in implement makes skill_application a hard check (LO-0399)."""
    from gate_ui_checks import ui_ticket_in_flight

    if ui_ticket_in_flight(project_dir):
        SOFT_CHECKS.discard("skill_application")
        return True
    return False


def check_static(name: str, project_dir: Path) -> QAResult:
    """In-process static check (security_checks / quality_checks). Findings fail it."""
    from quality_checks import CHECKS as QUALITY
    from security_checks import run_check as run_security

    start_time = datetime.now()
    if name in QUALITY:
        findings, not_tested = QUALITY[name](project_dir)
    else:
        findings, not_tested = run_security(name, project_dir), False
    duration = (datetime.now() - start_time).total_seconds()
    shown = findings[:15] + ([f"… {len(findings) - 15} more"] if len(findings) > 15 else [])
    return QAResult(
        check=name,
        passed=not findings,
        output="\n".join(shown) if findings else ("NOT TESTED — " + not_tested if not_tested else "clean"),
        duration=duration,
        error=None if not findings else f"{len(findings)} finding(s)",
        not_tested=bool(not_tested) and not findings,
    )


def check_npm_audit_policy(npm_dir: Path) -> QAResult:
    """High or critical advisories in production dependencies fail the gate."""
    from security_checks import _expired, load_exceptions

    waivers = [
        row
        for row in load_exceptions(npm_dir)
        if row["check"] == "npm_audit_policy" and not _expired(row)
    ]
    if waivers:
        row = waivers[0]
        return QAResult(
            check="npm_audit_policy",
            passed=True,
            output=f"waived until {row['expires']} — {row['reason']}",
            duration=0.0,
        )
    start_time = datetime.now()
    try:
        result = subprocess.run(
            "npm audit --omit=dev --audit-level=high",
            shell=True, cwd=str(npm_dir), capture_output=True, text=True, timeout=90,
        )
    except subprocess.TimeoutExpired:
        return QAResult("npm_audit_policy", True, "NOT TESTED — npm audit timed out", 90, not_tested=True)
    duration = (datetime.now() - start_time).total_seconds()
    output = (result.stdout or "") + (result.stderr or "")
    if result.returncode != 0 and re.search(r"ENOTFOUND|EAI_AGAIN|ECONNREFUSED|network|audit endpoint", output, re.I):
        return QAResult("npm_audit_policy", True, "NOT TESTED — registry unreachable", duration, not_tested=True)
    return QAResult(
        check="npm_audit_policy",
        passed=result.returncode == 0,
        output=output[-1500:],
        duration=duration,
        error=None if result.returncode == 0 else "high/critical advisory in production dependencies",
    )


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


def durable_playwright_browsers_path(project_dir: Path) -> Path:
    """Per-project Playwright browsers under studio cache (survives Cursor sandbox temp)."""
    return PLAYWRIGHT_CACHE_ROOT / project_dir.name


def _darwin_arm64_playwright_host_platform() -> Optional[str]:
    """Playwright hostPlatform for Apple Silicon when os.cpus() is empty (Cursor sandbox)."""
    if sys.platform != "darwin":
        return None
    machine = platform.machine().lower()
    if machine not in ("arm64", "aarch64"):
        return None
    # Mirror playwright-core macVersion (darwin 20 → mac11, …; ≥25 caps at mac26).
    try:
        major = int(platform.release().split(".")[0])
    except (TypeError, ValueError):
        major = 24
    if 20 <= major < 25:
        mac_version = 11 + (major - 20)
    elif major >= 25:
        mac_version = min(major + 1, 26)
    else:
        mac_version = 15
    return f"mac{mac_version}-arm64"


def smoke_env_with_durable_playwright(project_dir: Path) -> Dict[str, str]:
    """Force PLAYWRIGHT_BROWSERS_PATH away from ephemeral sandbox caches (LO-0052)."""
    env = os.environ.copy()
    browsers_path = durable_playwright_browsers_path(project_dir)
    browsers_path.mkdir(parents=True, exist_ok=True)
    env["PLAYWRIGHT_BROWSERS_PATH"] = str(browsers_path)
    # Drop stale sandbox overrides, then set arm64 when the host is Apple Silicon.
    # Empty os.cpus() makes Playwright pick mac-x64 and miss durable arm64 browsers.
    env.pop("PLAYWRIGHT_HOST_PLATFORM_OVERRIDE", None)
    arm64_host = _darwin_arm64_playwright_host_platform()
    if arm64_host:
        env["PLAYWRIGHT_HOST_PLATFORM_OVERRIDE"] = arm64_host
    return env


def check_smoke_routes(project_dir: Path) -> QAResult:
    """Run runtime smoke tests when docs/smoke-routes.json is present."""
    smoke_config = project_dir / "docs" / "smoke-routes.json"
    start_time = datetime.now()

    # Agent / CI sandboxes may SIGSEGV Chromium (kill EPERM). Opt out explicitly —
    # never silent. Before marking tickets done, re-run smoke outside the sandbox
    # (LO-0071 / LO-0132). Human local machines should leave this unset.
    if os.environ.get("QUINSY_SKIP_SMOKE", "").strip() in ("1", "true", "yes"):
        return QAResult(
            check="smoke_routes",
            passed=True,
            output=(
                "NOT TESTED — QUINSY_SKIP_SMOKE set (Chromium unavailable in this environment). "
                "Re-run smoke unrestricted, or say `smoke routes: NOT TESTED — <why>` on the receipt."
            ),
            duration=0,
            not_tested=True,
        )

    if not smoke_config.exists():
        return QAResult(
            check="smoke_routes",
            passed=True,
            output="NOT TESTED — no docs/smoke-routes.json (add smoke config for web apps)",
            duration=0,
            not_tested=True,
        )

    try:
        with open(smoke_config, "r") as f:
            config = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        return QAResult(
            check="smoke_routes",
            passed=False,
            output="",
            duration=0,
            error=f"Invalid smoke-routes.json: {e}",
        )

    command = config.get("command", "npm run smoke")
    # Install once into durable cache; subsequent gates reuse browsers (LO-0052).
    playwright_install = "npx playwright install chromium"
    full_command = f"{playwright_install} && {command}"
    env = smoke_env_with_durable_playwright(project_dir)

    try:
        result = subprocess.run(
            full_command,
            shell=True,
            cwd=str(project_dir),
            capture_output=True,
            text=True,
            timeout=240,
            env=env,
        )
        duration = (datetime.now() - start_time).total_seconds()
        hint = f"PLAYWRIGHT_BROWSERS_PATH={env['PLAYWRIGHT_BROWSERS_PATH']}"
        return QAResult(
            check="smoke_routes",
            passed=result.returncode == 0,
            output=f"{hint}\n{result.stdout}{result.stderr}",
            duration=duration,
            error=None if result.returncode == 0 else f"Exit code: {result.returncode}",
        )
    except subprocess.TimeoutExpired:
        duration = (datetime.now() - start_time).total_seconds()
        return QAResult(
            check="smoke_routes",
            passed=False,
            output="",
            duration=duration,
            error="Timeout after 240s",
        )
    except Exception as e:
        duration = (datetime.now() - start_time).total_seconds()
        return QAResult(
            check="smoke_routes",
            passed=False,
            output="",
            duration=duration,
            error=str(e),
        )

# =============================================================================
# REPORTING
# =============================================================================

def print_report(report: QAReport, use_json: bool = False):
    """Print the QA report."""
    
    if use_json:
        blob = json.dumps(asdict(report), indent=2, ensure_ascii=False)
        print(redact_secret_patterns(blob))
        return
    
    print(f"\n{'='*60}")
    print(f"  QA-GATE: {report.project} (Level {report.level})")
    print(f"{'='*60}")
    
    passed_count = sum(1 for r in report.results if r["passed"])
    total_count = len(report.results)
    
    for result in report.results:
        soft = result["check"] in SOFT_CHECKS
        if result.get("not_tested"):
            print(f"\n  ⚪ {result['check']} NOT TESTED")
            print(f"     {redact_secret_patterns(result['output'].strip().splitlines()[0] if result['output'] else '')}")
            continue
        if result["passed"]:
            icon = "✅"
        elif soft:
            icon = "⚠️"
        else:
            icon = "❌"
        duration_str = f" ({result['duration']:.1f}s)" if result["duration"] > 0 else ""
        soft_tag = " (soft — does not fail RESULT)" if soft and not result["passed"] else ""
        print(f"\n  {icon} {result['check']}{duration_str}{soft_tag}")
        
        if not result["passed"] and result.get("error"):
            print(f"     Error: {result['error']}")
            if result["output"]:
                # Show first few lines of output
                output_lines = result["output"].strip().split('\n')[:5]
                for line in output_lines:
                    print(f"     {redact_secret_patterns(line)}")
    
    hard_failed = [
        r
        for r in report.results
        if not r["passed"] and r["check"] not in SOFT_CHECKS
    ]
    soft_failed = [
        r
        for r in report.results
        if not r["passed"] and r["check"] in SOFT_CHECKS
    ]
    not_tested = [r["check"] for r in report.results if r.get("not_tested")]
    print(f"\n  {'='*50}")
    print(f"  RESULT: {report.passed}")
    print(f"  Passed: {passed_count - len(not_tested)}/{total_count}")
    if not_tested:
        print(f"  NOT TESTED: {', '.join(not_tested)} (receipt must say so)")
    if soft_failed and report.passed:
        print(f"  Soft fail ignored for RESULT: {', '.join(r['check'] for r in soft_failed)}")
    print(f"  Duration: {report.total_duration:.1f}s")
    print(f"  {'='*50}")
    
    if report.passed:
        if soft_failed:
            print(
                f"\n  ✅ QA RESULT green (hard checks). "
                f"Soft advisory still open: {', '.join(r['check'] for r in soft_failed)} — not a done-blocker."
            )
        else:
            print(f"\n  ✅ All QA checks passed. Ticket can be marked as 'done'.")
    else:
        print(f"\n  ❌ QA checks failed. Ticket must go back to phase 4 (implementation).")
        if hard_failed:
            print(f"     Hard fails: {', '.join(r['check'] for r in hard_failed)}")
    
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

    # Payload-foundation projects (payload_foundation.py) scaffold the Next/
    # Payload app into apps/web/ rather than the project root, and run
    # `npm install` *inside* Docker, not on the host (see BE-007 /
    # payload-playbook.md). Point the npm-related checks at apps/web when it
    # has its own package.json; project-level checks (structure, status.json,
    # anti-slop, skill checks) still run against project_dir.
    npm_dir = project_dir
    web_app_dir = project_dir / "apps" / "web"
    if (web_app_dir / "package.json").exists():
        npm_dir = web_app_dir
    
    print(f"\n  Starting QA gate level {level} for {project}...")

    if level >= 2:
        from studio_settings import ensure_prettierignore_cost_lines

        ensure_prettierignore_cost_lines(project_dir)

    if level >= 5 and harden_for_ui(project_dir):
        print("  UI ticket in flight — token literals and native <select> fail the gate (LO-0399).")

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
        elif check.name == "smoke_routes":
            result = check_smoke_routes(project_dir)
        elif check.name == "skill_application":
            result = check_skill_application(project_dir)
        elif check.name == "ui_motion":
            result = check_ui_motion(project_dir)
        elif check.name in STATIC_CHECKS:
            result = check_static(check.name, project_dir)
        elif check.name == "npm_audit_policy":
            result = check_npm_audit_policy(npm_dir)
        elif check.name in (
            "package_json_exists",
            "node_modules_exists",
            "eslint",
            "prettier",
            "typescript",
            "unit_tests",
            "build",
        ):
            result = run_check(check, npm_dir)
        else:
            result = run_check(check, project_dir)
        
        results.append(result)
        
        icon = "⚪ not tested" if result.not_tested else ("✅" if result.passed else "❌")
        print(f" {icon}")
    
    total_duration = (datetime.now() - total_start).total_seconds()
    
    # Build report
    passed = all(r.passed for r in results if r.check not in SOFT_CHECKS)
    
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
