#!/usr/bin/env python3
"""
Quinsy Studio — Main Orchestrator

Dual-Speed Operating Model:
  CORE: For new platforms & complex systems (6 phases with human gates)
  LEAN: For iterations & features in existing projects (4 phases)

Usage:
  ./studio <command> [args...]

Commands:
  # Project management
  ./studio init <project> --archetype <type>     Initialize project
  ./studio bootstrap [project] [intake-file]     AI entry: init→intake→concept→sprint
  ./studio resume <project>                      Next actions from status.json
  ./studio focus <project>                       Set active project + scope banner
  ./studio guard <project> "request text"        Check if request is in scope
  ./studio verify-worlds                         Studio vs project git separation
  ./studio library list                           List studio-library assets
  ./studio library pull <project> auth billing    Copy library → project
  ./studio library promote <project> packages/billing [--force]
  ./studio library suggest <project> <query>      Find assets before coding
  ./studio promote-library <project> [--force]    Promote design system (gate 2)
  ./studio start <project> --mode [core|lean]    Start project
  ./studio status <project>                      Show status
  ./studio board <project>                       Show board

  # Phase 1: Intake (human gate 0)
  ./studio intake <project> <input-file>         Process intake (no tickets yet)

  # Phase 2: Architecture (human gate 1)
  ./studio blueprint <project>                   Scaffold architecture docs
  ./studio approve <project> --gate 0            Approve PRD + definitions
  ./studio approve <project> --gate 1            Approve architecture blueprint

  # Phase 3: Design (human gate 2)
  ./studio design <project> --scope journey|core-views
  ./studio approve <project> --gate 2            Approve design → generates tickets
  ./studio revise <project> --gate <0|1|2> --feedback "..."

  # Legacy
  ./studio concept <project>                     → blueprint / design

  # Phase 3: Sprint Management
  ./studio sprint <project>                      Create sprint
  ./studio ticket <project> "Title"              Create ticket
  ./studio move <project> <id> <status>          Move ticket
  ./studio groom <project>                       Run grooming

  # Phase 4: Implementation
  ./studio gate <project> [--level N]            Run QA gate

  # Phase 6: Learning
  ./studio learn "Title" --signal <s>            Create learning item
  ./studio learn-list                            Show learning items
  ./studio retro <project>                       Start retrospective
  ./studio sync <project>                        Sync global assets

  # Tools
  ./studio adr <project> "Title"                 Create ADR
  ./studio decide <project> "Title"              Create decision record
  ./studio env <project> init|up|down|status     Docker env
  ./studio repo <project> create|status          GitHub repo
  ./studio promote <project> <asset>             Promote asset to library
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

from ticket_helpers import render_ticket_markdown, role_for_skills
from ticket_ids import allocate_ticket_id
from skill_matcher import match_skills, team_for_skills
from init_project_env import init_project
from pre_impl_workflow import (
    PHASE_BLUEPRINT,
    PHASE_DESIGN,
    PHASE_IMPLEMENT,
    PHASE_INTAKE,
    PHASE_SPRINT,
    record_revision,
    scaffold_blueprint,
    scaffold_design,
    validate_human_gate,
)
from studio_context import (
    build_focus_report,
    guard_request,
    set_active_project,
    verify_worlds,
)
from library_manager import (
    check_reuse_before_done,
    format_library_first_hint,
    list_library_assets,
    promote_design_to_library,
    promote_path,
    pull_assets,
    snapshot_registry_files,
    suggest_assets,
)

# =============================================================================
# CONFIGURATION
# =============================================================================

STUDIO_ROOT = Path(__file__).parent.parent.parent
QUINSY_STUDIO = STUDIO_ROOT / ".quinsy-studio"
INTAKE_DIR = STUDIO_ROOT / "intake"
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
    """Ensure all required directories exist."""
    for d in [QUINSY_STUDIO, PROCESS_DIR, TEAMS_DIR, PROJECTS_DIR,
              STUDIO_LIBRARY, BACKLOG_DIR, RETROS_DIR,
              BACKLOG_DIR / "open", BACKLOG_DIR / "done", BACKLOG_DIR / "blocked"]:
        d.mkdir(parents=True, exist_ok=True)

def slugify(text: str) -> str:
    """Convert text into a URL-friendly slug."""
    text = text.lower()
    text = re.sub(r'[äöüß]', lambda m: {'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'ß': 'ss'}[m.group()], text)
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')[:50]

def get_next_ticket_id(project: str) -> str:
    """Return the next ticket ID for a project (unified counter + scan)."""
    return allocate_ticket_id(project)

def get_project_backlog_dir(project: str, status: str = "open") -> Path:
    """Return the backlog directory for a project."""
    backlog_dir = PROJECTS_DIR / project / "backlog"
    target_dir = backlog_dir / status
    target_dir.mkdir(parents=True, exist_ok=True)
    return target_dir

def find_project_ticket(project: str, ticket_id: str) -> tuple:
    """Find a ticket in the project backlog. Returns (filepath, current_status)."""
    project_backlog = PROJECTS_DIR / project / "backlog"
    
    for status in ["open", "done", "blocked", "plan", "analyze", "implement", "design", "qa", "review", "reuse"]:
        ticket_dir = project_backlog / status
        if ticket_dir.exists():
            for f in ticket_dir.glob(f"{ticket_id}-*.md"):
                return f, status
    
    return None, None

def load_status(project: str) -> Dict:
    """Load the project status."""
    status_file = PROJECTS_DIR / project / "status.json"
    if status_file.exists():
        return json.loads(status_file.read_text())
    return {
        "name": project,
        "phase": "0",
        "gate": "0",
        "gate_status": "open",
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
    """Save the project status."""
    status["last_update"] = datetime.now().strftime("%Y-%m-%d")
    status_file = PROJECTS_DIR / project / "status.json"
    status_file.parent.mkdir(parents=True, exist_ok=True)
    status_file.write_text(json.dumps(status, indent=2, ensure_ascii=False))

def resolve_intake_file(project: str, intake_file: Optional[str] = None) -> Optional[Path]:
    """Find the intake PRD for a project slug."""
    if intake_file:
        path = Path(intake_file)
        if not path.is_absolute():
            path = STUDIO_ROOT / intake_file
        return path if path.exists() else None

    if not INTAKE_DIR.exists():
        return None

    slug = slugify(project)
    for candidate in INTAKE_DIR.glob("*.md"):
        if candidate.name.lower() in {"readme.md", "index.md"}:
            continue
        if slugify(candidate.stem) == slug:
            return candidate

    files = [
        f for f in INTAKE_DIR.glob("*.md")
        if f.name.lower() not in {"readme.md", "index.md"}
    ]
    if len(files) == 1:
        return files[0]
    return None

def intake_path_for_cli(path: Path) -> str:
    """Return a repo-relative intake path for CLI output."""
    try:
        return str(path.relative_to(STUDIO_ROOT))
    except ValueError:
        return str(path)

def print_header(title: str, char: str = "="):
    """Print a formatted header."""
    width = 60
    print(f"\n{char * width}")
    print(f"  {title}")
    print(f"{char * width}")

def print_check(label: str, passed: bool, details: str = ""):
    """Print a check element."""
    status = "✓" if passed else "✗"
    color = "\033[92m" if passed else "\033[91m"
    reset = "\033[0m"
    detail_str = f" ({details})" if details else ""
    print(f"  {color}[{status}]{reset} {label}{detail_str}")


def read_prd_text(project: str) -> str:
    prd_file = PROJECTS_DIR / project / "docs" / "intake" / "prd.md"
    return prd_file.read_text(encoding="utf-8") if prd_file.exists() else ""


def design_stack_hints(project: str, archetype: str) -> Dict[str, str]:
    """Infer stack rows for DESIGN.md from PRD + archetype."""
    prd = read_prd_text(project).lower()
    hints = {
        "frontend": "Next.js App Router + TypeScript",
        "styling": "Tailwind CSS + design tokens",
        "animation": "Framer Motion",
        "backend": "Supabase (optional cloud sync)",
        "storage": "Local-first (IndexedDB) + optional Supabase",
        "deployment": "Vercel",
    }
    if "pwa" in prd or "progressive web app" in prd:
        hints["frontend"] = "Next.js PWA + TypeScript"
    if archetype == "game":
        hints = {
            "engine": "Godot 4 (or per PRD)",
            "frontend": "N/A — game client",
            "backend": "Optional leaderboard API",
            "deployment": "itch.io / Steam (per PRD)",
        }
    if archetype == "api-service":
        hints["frontend"] = "N/A"
        hints["backend"] = "Node.js / Hono or per ADR"
    return hints


def assign_open_tickets_to_sprint(project: str, sprint_name: str, max_tickets: int = 10) -> List[Dict]:
    """Tag open P0/P1 tickets with sprint and return metadata for plan.md."""
    open_dir = PROJECTS_DIR / project / "backlog" / "open"
    if not open_dir.exists():
        return []
    tickets = sorted(open_dir.glob(f"{project[:4].upper()}-*.md"))
    assigned = []
    for ticket_file in tickets[:max_tickets]:
        content = ticket_file.read_text(encoding="utf-8")
        title_match = re.search(r'^title:\s*(.+)$', content, re.MULTILINE)
        priority_match = re.search(r'^priority:\s*(.+)$', content, re.MULTILINE)
        phase_match = re.search(r'^phase:\s*(\d+)', content, re.MULTILINE)
        estimate_match = re.search(r'^estimate:\s*(.+)$', content, re.MULTILINE)
        tid_match = re.match(r'^([A-Z]+-\d+)', ticket_file.name)
        tid = tid_match.group(1) if tid_match else ticket_file.stem[:12]
        if "sprint:" not in content:
            content = content.replace("created:", f"sprint: {sprint_name}\ncreated:", 1)
            ticket_file.write_text(content)
        assigned.append({
            "id": tid,
            "title": title_match.group(1).strip() if title_match else ticket_file.stem,
            "phase": phase_match.group(1) if phase_match else "?",
            "priority": priority_match.group(1).strip() if priority_match else "P1",
            "estimate": estimate_match.group(1).strip() if estimate_match else "M",
        })
    return assigned

# =============================================================================
# DUAL-SPEED ORCHESTRATOR
# =============================================================================

class StudioOrchestrator:
    """Main orchestrator for the Dual-Speed Operating Model."""
    
    def __init__(self):
        ensure_dirs()
    
    # -------------------------------------------------------------------------
    # PROJECT MANAGEMENT
    # -------------------------------------------------------------------------

    def _print_bootstrap_discovery(self):
        """List intake PRDs and existing projects for AI/human discovery."""
        print_header("QUINSY STUDIO — BOOTSTRAP")
        print("\n  Place a PRD in intake/, then run:")
        print("    ./studio bootstrap <project>")
        print("    ./studio bootstrap <project> intake/<file>.md")
        print("\n  Resume an existing project:")
        print("    ./studio resume <project>")

        if INTAKE_DIR.exists():
            intake_files = sorted(
                f for f in INTAKE_DIR.glob("*.md")
                if f.name.lower() not in {"readme.md", "index.md"}
            )
            if intake_files:
                print("\n  Intake PRDs:")
                for f in intake_files:
                    suggested = slugify(f.stem)
                    print(f"    - {intake_path_for_cli(f)}  →  ./studio bootstrap {suggested}")

        if PROJECTS_DIR.exists():
            projects = sorted(p for p in PROJECTS_DIR.iterdir() if p.is_dir() and (p / "status.json").exists())
            if projects:
                print("\n  Existing projects:")
                for p in projects:
                    status = load_status(p.name)
                    print(
                        f"    - {p.name}  (phase {status.get('phase', '?')}, "
                        f"sprint {status.get('current_sprint') or '-'})  →  ./studio resume {p.name}"
                    )

    def cmd_bootstrap(
        self,
        project: Optional[str] = None,
        intake_file: Optional[str] = None,
        archetype: str = "saas-application",
        mode: str = "core",
    ):
        """Run init → intake → start; stop at the next human gate (0, 1, or 2)."""
        if not project:
            self._print_bootstrap_discovery()
            return True

        project_dir = PROJECTS_DIR / project
        intake_path = resolve_intake_file(project, intake_file)

        print_header(f"BOOTSTRAP: {project}")

        if not project_dir.exists() or not (project_dir / "status.json").exists():
            if not intake_path:
                print(f"\n  ❌ Project '{project}' not initialized and no intake PRD found.")
                print(f"     Place intake/<name>.md or run: ./studio bootstrap {project} intake/<file>.md")
                return False
            self.cmd_init(project, archetype)

        prd_file = project_dir / "docs" / "intake" / "prd.md"
        if not prd_file.exists():
            if not intake_path:
                print(f"\n  ❌ No intake file for '{project}'. Add intake/<name>.md or pass the path.")
                return False
            ok = self.cmd_intake(project, intake_path_for_cli(intake_path))
            if not ok:
                return False

        status = load_status(project)
        if not status.get("mode") or status.get("phase") == "0":
            self.cmd_start(project, mode)
            status = load_status(project)

        return self._bootstrap_from_status(project, status)

    def _bootstrap_from_status(self, project: str, status: Dict) -> bool:
        """Continue bootstrap from current phase / gate state."""
        hg = status.get("human_gates", {})

        if hg.get("0", {}).get("status") != "approved":
            self._print_gate_pause(project, 0, "Fill docs/definitions/ from PRD, then approve intake.")
            return True

        if status.get("phase") == PHASE_INTAKE or hg.get("1", {}).get("status") != "approved":
            blueprint = PROJECTS_DIR / project / "docs" / "architecture" / "BLUEPRINT.md"
            if not blueprint.exists():
                self.cmd_blueprint(project)
            if hg.get("1", {}).get("status") != "approved":
                self._print_gate_pause(project, 1, "Review docs/architecture/ and ADRs.")
                return True

        if status.get("phase") in (PHASE_INTAKE, PHASE_BLUEPRINT, PHASE_DESIGN) or hg.get("2", {}).get("status") != "approved":
            design = PROJECTS_DIR / project / "design" / "DESIGN.md"
            if not design.exists():
                scope = status.get("design_scope") or "core-views"
                self.cmd_design(project, scope)
            if hg.get("2", {}).get("status") != "approved":
                self._print_gate_pause(project, 2, "Review design/prototype mocks + sticker sheet.")
                return True

        status = load_status(project)
        if not status.get("current_sprint"):
            self.cmd_sprint(project)
            status = load_status(project)

        print(f"\n  ✅ Ready for implementation (phase {status.get('phase')}, {status.get('current_sprint')})")
        print(f"     Agent contract: projects/{project}/agent-briefing.md")
        print(f"     Next: ./studio resume {project}")
        return True

    def _print_gate_pause(self, project: str, gate: int, hint: str):
        labels = {
            0: "Intake — PRD & definitions",
            1: "Architecture blueprint",
            2: "Design — prototype mocks & sticker sheet",
        }
        print(f"\n  ⏸ HUMAN GATE {gate}: {labels.get(gate, 'Review')}")
        print(f"     {hint}")
        print(f"     ./studio approve {project} --gate {gate}")
        print(f"     Iteration: ./studio revise {project} --gate {gate} --feedback \"...\"")

    def cmd_resume(self, project: str):
        """Print the next actions for AI/human based on project status."""
        project_dir = PROJECTS_DIR / project
        if not project_dir.exists():
            print(f"\n  ❌ Project '{project}' not found.")
            print(f"     Run: ./studio bootstrap {project}")
            return False

        status = load_status(project)
        briefing = project_dir / "agent-briefing.md"
        hg = status.get("human_gates", {})

        print_header(f"RESUME: {project}")
        print(f"  Mode:          {status.get('mode', 'core').upper()}")
        print(f"  Phase:         {status.get('phase')}")
        print(f"  Gate:          {status.get('gate')} ({status.get('gate_status')})")
        print(f"  Design scope:  {status.get('design_scope') or '(not set)'}")
        print(f"  Sprint:        {status.get('current_sprint') or '-'}")
        print(f"  Ticket:        {status.get('active_ticket') or '-'}")

        actions: List[str] = []
        prd_file = project_dir / "docs" / "intake" / "prd.md"

        if not prd_file.exists():
            intake_path = resolve_intake_file(project)
            if intake_path:
                actions.append(f"./studio intake {project} {intake_path_for_cli(intake_path)}")
            else:
                actions.append(f"Add intake/<prd>.md, then ./studio bootstrap {project}")
        elif hg.get("0", {}).get("status") != "approved":
            actions.append("AI: fill projects/{p}/docs/definitions/ from PRD (no _TODO_)".format(p=project))
            actions.append(f"Human: review PRD + definitions → ./studio approve {project} --gate 0")
        elif hg.get("1", {}).get("status") != "approved":
            actions.append(f"./studio blueprint {project}")
            actions.append("AI: fill docs/architecture/, create ADRs")
            actions.append(f"Human: review blueprint → ./studio approve {project} --gate 1")
        elif hg.get("2", {}).get("status") != "approved":
            if not status.get("design_scope"):
                actions.append(f"Human: choose mock scope → ./studio design {project} --scope journey|core-views")
            else:
                actions.append(f"./studio design {project} --scope {status['design_scope']}")
            actions.append("AI: build design/prototype (Next.js), ui/tokens, sticker-sheet")
            actions.append(f"Human: review mocks → ./studio approve {project} --gate 2")
        elif not status.get("current_sprint"):
            actions.append(f"./studio sprint {project}")
        else:
            actions.append(f"./studio board {project}")
            actions.append(f"./studio move {project} <TICKET-ID> implement --reason \"Started\"")
            actions.append(f"Implement in projects/{project}/ — no code without a ticket")
            actions.append(f"./studio move {project} <TICKET-ID> done --reason \"DoD met\"")

        print("\n  Next actions:")
        for i, action in enumerate(actions, 1):
            print(f"    {i}. {action}")

        if briefing.exists():
            print(f"\n  Read first: projects/{project}/agent-briefing.md")
        print(f"  Process: .quinsy-studio/process/lifecycle.md")
        set_active_project(project, status)
        return True
    
    def cmd_focus(self, project: str):
        """Set active project context for IDE agent (scope banner)."""
        project_dir = PROJECTS_DIR / project
        if not project_dir.exists():
            print(f"\n  ❌ Project '{project}' not found.")
            return False
        status = load_status(project)
        set_active_project(project, status)
        print_header(f"FOCUS: {project}")
        print("\n" + build_focus_report(project, status))
        print(f"\n  Active context saved: .quinsy-studio/.active-project.json")
        return True

    def cmd_guard(self, project: str, request: str):
        """Check if a user request is in project/sprint scope."""
        status = load_status(project)
        verdict, message = guard_request(project, request, status)
        icons = {
            "in_scope": "✅",
            "needs_ticket": "🎫",
            "pre_impl": "⏸",
            "studio_meta": "🏢",
            "unclear": "❓",
        }
        print_header(f"GUARD: {project}")
        print(f"\n  {icons.get(verdict, '•')} {verdict.upper()}")
        print(f"  {message}")
        return verdict == "in_scope"

    def cmd_verify_worlds(self):
        """Verify studio git and project git are separated."""
        ok, issues = verify_worlds()
        print_header("VERIFY WORLDS")
        if ok:
            print("\n  ✅ Studio HQ and project repos are separated correctly.")
            return True
        print("\n  ❌ Issues found:")
        for issue in issues:
            print(f"    • {issue}")
        print("\n  See: .quinsy-studio/process/worlds.md")
        return False

    def cmd_promote_library(self, project: str, dry_run: bool = False, force: bool = False):
        """Promote design system artifacts to studio-library."""
        print_header(f"PROMOTE LIBRARY: {project}")
        result = promote_design_to_library(project, force=force, dry_run=dry_run)
        if dry_run:
            print("\n  Would promote:")
            for p in result.get("promoted", []):
                print(f"    + {p}")
            for p in result.get("skipped", []):
                print(f"    - skip/missing: {p}")
        elif result.get("promoted"):
            print("\n  Promoted to studio-library:")
            for p in result["promoted"]:
                print(f"    ✓ {p}")
            if result.get("skipped"):
                print("\n  Skipped (use --force to overwrite):")
                for p in result["skipped"]:
                    print(f"    - {p}")
        else:
            print("\n  ⚠️  Nothing to promote (complete gate 2 design artifacts first)")
        return bool(result.get("promoted"))

    def cmd_library(self, subcommand: str, args: List[str]):
        """Studio library: list, pull, promote, suggest."""
        if subcommand == "list":
            print_header("STUDIO LIBRARY")
            for asset in list_library_assets():
                ver = asset.get("version", "?")
                print(f"  [{asset.get('kind', '?')}] {asset.get('name')} v{ver} — {asset.get('path', '')}")
            print(f"\n  Registry: .quinsy-studio/studio-library/library_registry.md")
            return True

        if subcommand == "suggest" and len(args) >= 2:
            project, query = args[0], " ".join(args[1:])
            print_header(f"LIBRARY SUGGEST: {project}")
            hits = suggest_assets(query)
            if not hits:
                print("\n  No matches. Run ./studio library list")
                return True
            print(f"\n  Query: {query}\n")
            for h in hits:
                print(f"  • {h.get('name')} ({h.get('kind')}) — ./studio library pull {project} {h.get('name')}")
            print(f"\n  {format_library_first_hint(project, query)}")
            return True

        if subcommand == "pull" and len(args) >= 2:
            project = args[0]
            names = [a for a in args[1:] if not a.startswith("--")]
            force = "--force" in args
            print_header(f"LIBRARY PULL → {project}")
            result = pull_assets(project, names, force=force)
            for item in result.get("pulled", []):
                st = item.get("status", "?")
                print(f"  {st}: {item.get('name')} ({item.get('kind', '')})")
            print(f"\n  Log: projects/{project}/docs/library-usage.json")
            return True

        if subcommand == "promote" and len(args) >= 2:
            project = args[0]
            path = args[1]
            force = "--force" in args
            ticket_id = None
            for i, a in enumerate(args):
                if a == "--ticket" and i + 1 < len(args):
                    ticket_id = args[i + 1]
            print_header(f"LIBRARY PROMOTE ← {project}")
            result = promote_path(project, path, force=force, ticket_id=ticket_id)
            if result.get("error"):
                print(f"\n  ❌ {result['error']}")
                return False
            for p in result.get("promoted", []):
                print(f"  ✓ {p} (v{result.get('version', '?')})")
            print(f"\n  Log: projects/{project}/docs/library-promotions.json")
            return True

        if subcommand == "promote-design" and len(args) >= 1:
            project = args[0]
            force = "--force" in args
            return self.cmd_promote_library(project, force=force)

        print("Usage:")
        print("  ./studio library list")
        print("  ./studio library suggest <project> <query>")
        print("  ./studio library pull <project> auth billing tokens [button...]")
        print("  ./studio library promote <project> packages/billing [--force] [--ticket ID]")
        print("  ./studio library promote-design <project> [--force]")
        return False

    def cmd_init(self, project: str, archetype: str = "saas-application"):
        """Initialize a new project (full scaffold via init_project_env)."""
        init_project(project, archetype)
        project_dir = PROJECTS_DIR / project
        print(f"\n  Next steps:")
        print(f"    1. Process intake: ./studio intake {project} intake/<your-prd>.md")
        print(f"    2. Start project:  ./studio start {project} --mode core")
        return True
    
    def cmd_start(self, project: str, mode: str = "core"):
        """Start a project in the selected mode."""
        
        status = load_status(project)
        status["mode"] = mode
        status["phase"] = "1"
        save_status(project, status)
        
        print_header(f"START PROJECT: {project} (Mode: {mode.upper()})")
        
        if mode == "core":
            print(f"\n  CORE MODE — Full process with human gates")
            print(f"\n  Phase 1: Intake & PRD Processing")
            print(f"    → Read and validate PRD")
            print(f"    → Determine archetype")
            print(f"    → Generate ticket manifest")
            print(f"\n  HUMAN-GATE 1: Architecture & Design Blueprint")
            print(f"    → Wait for approval after phase 2")
        else:
            print(f"\n  LEAN MODE — Fast feature loop")
            print(f"\n  Phase 1: Ticket Drop")
            print(f"    → Ticket directly into backlog")
            print(f"\n  HUMAN-GATE 1: Quick Align")
            print(f"    → Short technical approach")
    
    def cmd_status(self, project: str):
        """Show the project status."""
        
        status = load_status(project)
        
        print_header(f"PROJECT STATUS: {project}")
        print(f"  Mode:         {status.get('mode', 'core').upper()}")
        print(f"  Phase:        {status['phase']}")
        print(f"  Gate:         {status['gate']} ({status['gate_status']})")
        print(f"  Archetyp:     {status['archetype']}")
        print(f"  Sprint:       {status.get('current_sprint', '-')}")
        print(f"  Ticket:       {status.get('active_ticket', '-')}")
        print(f"  Created:     {status['created']}")
        print(f"  Updated:     {status['last_update']}")
        
        # Gate history
        if status.get('gate_history'):
            print(f"\n  Gate history:")
            for entry in status['gate_history'][-5:]:
                print(f"    Gate {entry['gate']}: {entry['status']} ({entry.get('passed_at', entry.get('failed_at', '-'))})")
        
        # Human gates
        if status.get('human_gates'):
            print(f"\n  Human-Gates:")
            for gate_id, gate_info in status['human_gates'].items():
                print(f"    Gate {gate_id}: {gate_info['status']} ({gate_info.get('date', '-')})")
        
        # Open tickets (in project backlog)
        project_backlog = PROJECTS_DIR / project / "backlog"
        open_dir = project_backlog / "open"
        if open_dir.exists():
            open_tickets = list(open_dir.glob(f"{project[:4].upper()}-*.md"))
            if open_tickets:
                print(f"\n  Open tickets: {len(open_tickets)}")
                for t in sorted(open_tickets)[:5]:
                    print(f"    - {t.stem}")
    
    # -------------------------------------------------------------------------
    # PHASE 1: INTAKE
    # -------------------------------------------------------------------------
    
    def cmd_intake(self, project: str, input_file: str):
        """Process intake input into a structured PRD."""
        
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
            print(f"\n  ❌ Intake processing failed")
            if result.stderr:
                print(f"  Error: {result.stderr}")
            return False

        # Tickets are generated after human gate 2 (design approval), not at intake.
        print(f"\n  ℹ️  Tickets will be generated after design approval (gate 2).")
        
        # Update status
        status = load_status(project)
        status["phase"] = PHASE_INTAKE
        status["gate"] = "0"
        status["gate_status"] = "intake-complete"
        save_status(project, status)
        
        print(f"\n  ✅ Phase 1 (intake) complete")
        print(f"  Next: fill docs/definitions/, then ./studio approve {project} --gate 0")
        
        return True
    
    def _run_ticket_manifest(self, project: str) -> bool:
        cmd = [
            sys.executable,
            str(TOOLS_DIR / "generate_ticket_manifest.py"),
            project,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result.stdout)
        if result.returncode != 0:
            print(f"\n  ❌ Ticket manifest generation failed")
            if result.stderr:
                print(f"  Error: {result.stderr}")
            return False
        return True

    # -------------------------------------------------------------------------
    # PHASE 2a: ARCHITECTURE BLUEPRINT
    # -------------------------------------------------------------------------

    def cmd_blueprint(self, project: str):
        """Scaffold architecture blueprint artifacts (phase 2)."""
        status = load_status(project)
        hg = status.get("human_gates", {})

        if hg.get("0", {}).get("status") != "approved":
            print(f"  ⚠️  Gate 0 must be approved first: ./studio approve {project} --gate 0")
            return False

        print_header(f"PHASE 2: ARCHITECTURE BLUEPRINT — {project}")
        archetype = status.get("archetype", "saas-application")
        created = scaffold_blueprint(project, archetype)
        for path in created:
            print(f"  ✓ {path.relative_to(PROJECTS_DIR / project)}")

        from init_project_env import seed_definitions
        seed_definitions(PROJECTS_DIR / project)

        status["phase"] = PHASE_BLUEPRINT
        save_status(project, status)

        print(f"\n  AI: fill docs/architecture/ and docs/adr/")
        print(f"  Human: ./studio approve {project} --gate 1 when ready")
        return True

    # -------------------------------------------------------------------------
    # PHASE 2b: DESIGN (prototype + sticker sheet)
    # -------------------------------------------------------------------------

    def cmd_design(self, project: str, scope: str = "core-views"):
        """Scaffold design docs + Next.js prototype. scope: journey | core-views"""
        status = load_status(project)
        hg = status.get("human_gates", {})

        if hg.get("1", {}).get("status") != "approved":
            print(f"  ⚠️  Gate 1 (architecture) must be approved first")
            return False

        if scope not in ("journey", "core-views"):
            print(f"  ⚠️  scope must be 'journey' or 'core-views'")
            return False

        print_header(f"PHASE 3: DESIGN — {project} (scope: {scope})")
        created = scaffold_design(project, scope)
        for path in created:
            try:
                print(f"  ✓ {path.relative_to(PROJECTS_DIR / project)}")
            except ValueError:
                print(f"  ✓ {path}")

        status["phase"] = PHASE_DESIGN
        status["design_scope"] = scope
        save_status(project, status)

        print(f"\n  Mock scope: {scope}")
        print(f"  Prototype:  cd projects/{project}/design/prototype && npm install && npm run dev")
        print(f"  Human:      ./studio approve {project} --gate 2 when mocks + sticker sheet ready")
        return True

    def cmd_concept(self, project: str):
        """Deprecated — use ./studio blueprint and ./studio design."""
        print(f"  ℹ️  `concept` is deprecated. Use:")
        print(f"     ./studio blueprint {project}")
        print(f"     ./studio design {project} --scope journey|core-views")
        status = load_status(project)
        hg = status.get("human_gates", {})
        if hg.get("0", {}).get("status") == "approved" and hg.get("1", {}).get("status") != "approved":
            return self.cmd_blueprint(project)
        if hg.get("1", {}).get("status") == "approved":
            scope = status.get("design_scope") or "core-views"
            return self.cmd_design(project, scope)
        print(f"  Complete gate 0 first: ./studio approve {project} --gate 0")
        return False

    def cmd_revise(self, project: str, gate: int, feedback: str):
        """Record feedback and reopen a human gate for iteration."""
        if gate not in (0, 1, 2):
            print(f"  ⚠️  revise supports gates 0, 1, 2 only")
            return False
        if not feedback.strip():
            print(f"  ⚠️  --feedback is required")
            return False

        status = load_status(project)
        rev_file = record_revision(project, gate, feedback)
        hg = status.setdefault("human_gates", {})
        hg[str(gate)] = {
            "status": "changes-requested",
            "date": datetime.now().isoformat(),
            "feedback": feedback.strip(),
        }
        if gate == 0:
            status["phase"] = PHASE_INTAKE
        elif gate == 1:
            status["phase"] = PHASE_BLUEPRINT
        elif gate == 2:
            status["phase"] = PHASE_DESIGN
        status["gate"] = str(gate)
        status["gate_status"] = "changes-requested"
        save_status(project, status)

        print_header(f"REVISION RECORDED — gate {gate}")
        print(f"  Log: {rev_file}")
        print(f"  Update artifacts, then ./studio approve {project} --gate {gate}")
        return True
    
    def cmd_approve(self, project: str, gate: int):
        """Approve a human gate (0=intake, 1=architecture, 2=design)."""
        status = load_status(project)
        if "human_gates" not in status:
            status["human_gates"] = {}

        ok, issues = validate_human_gate(project, gate)
        if not ok:
            print_header(f"GATE {gate} NOT READY — {project}")
            print("\n  Fix before approving:")
            for issue in issues:
                print(f"    • {issue}")
            print(f"\n  Iteration: ./studio revise {project} --gate {gate} --feedback \"...\"")
            return False

        if gate == 0:
            if status.get("phase") not in (PHASE_INTAKE, "1", "0"):
                pass  # allow re-approve after revise
            print_header(f"HUMAN GATE 0 APPROVED: {project}")
            status["human_gates"]["0"] = {
                "status": "approved",
                "date": datetime.now().isoformat(),
            }
            status["phase"] = PHASE_BLUEPRINT
            status["gate"] = "0"
            status["gate_status"] = "approved"
            save_status(project, status)
            print(f"\n  ✅ Intake & definitions approved")
            print(f"  Next: ./studio blueprint {project}")
            return True

        if gate == 1:
            print_header(f"HUMAN GATE 1 APPROVED: {project}")
            status["human_gates"]["1"] = {
                "status": "approved",
                "date": datetime.now().isoformat(),
            }
            status["phase"] = PHASE_DESIGN
            status["gate"] = "1"
            status["gate_status"] = "approved"
            save_status(project, status)
            print(f"\n  ✅ Architecture blueprint approved")
            print(f"  Next: ./studio design {project} --scope journey|core-views")
            return True

        if gate == 2:
            print_header(f"HUMAN GATE 2 APPROVED: {project}")
            status["human_gates"]["2"] = {
                "status": "approved",
                "date": datetime.now().isoformat(),
            }
            status["phase"] = PHASE_SPRINT
            status["gate"] = "2"
            status["gate_status"] = "approved"
            save_status(project, status)

            print(f"\n  Generating tickets from approved PRD + design...")
            if not self._run_ticket_manifest(project):
                return False

            print(f"\n  Promoting base design system to studio-library...")
            lib = promote_design_to_library(project)
            for p in lib.get("promoted", []):
                print(f"    ✓ studio-library/{p}")

            print(f"\n  ✅ Design approved — tickets created")
            print(f"  Next: ./studio sprint {project}")
            return True

        print(f"  ⚠️  Unknown gate: {gate} (use 0, 1, or 2)")
        return False
    
    # -------------------------------------------------------------------------
    # PHASE 3: SPRINT MANAGEMENT
    # -------------------------------------------------------------------------
    
    def cmd_sprint(self, project: str):
        """Create a new sprint."""
        
        status = load_status(project)
        
        if status["phase"] not in [PHASE_SPRINT, PHASE_IMPLEMENT, "4", "5"]:
            print(f"  ⚠️  Sprint requires design approval (gate 2). Current phase: {status['phase']}")
            return False
        
        if status.get("human_gates", {}).get("2", {}).get("status") != "approved":
            print(f"  ⚠️  Gate 2 (design) must be approved before sprint")
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
        assigned = assign_open_tickets_to_sprint(project, sprint_name)
        rows = "\n".join(
            f"| {t['id']} | {t['title'][:40]} | {t['phase']} | {t['priority']} | {t['estimate']} |"
            for t in assigned
        ) or "| ... | ... | ... | ... | ... |"
        plan_template = f"""# Sprint Plan — {sprint_name}

**Project:** {project}
**Goal:** Complete setup tickets (0001–0004) and first P0 features
**Start:** {datetime.now().strftime('%Y-%m-%d')}
**End:** YYYY-MM-DD
**Capacity:** {len(assigned)} tickets assigned

## Tickets in this sprint

| Ticket | Title | Phase | Priority | Estimate |
|--------|-------|-------|----------|----------|
{rows}

## Dependencies
- Setup tickets (0001–0002) before feature tickets

## Risks
- ...

## Definition of Done
- [ ] All sprint tickets in status "done"
- [ ] QA test green (`./studio gate {project} --level 5`)
- [ ] Anti-slop audit: 0 errors
- [ ] Retrospective done
- [ ] Summary written
"""
        plan_file.write_text(plan_template)
        
        # Update project status
        status["current_sprint"] = sprint_name
        status["phase"] = PHASE_IMPLEMENT
        save_status(project, status)
        
        print(f"\n  Sprint created: {sprint_name}")
        print(f"  Tickets assigned: {len(assigned)}")
        print(f"  Directory: {sprint_dir}")
        print(f"\n  Next step:")
        print(f"    ./studio move {project} {assigned[0]['id'] if assigned else 'TICKET-ID'} implement")
        
        return True
    
    def cmd_ticket(self, project: str, title: str, phase: int = 4, 
                   priority: str = "P1", estimate: str = "M"):
        """Create a new ticket in the project backlog (strict studio schema)."""
        
        ticket_id = get_next_ticket_id(project)
        slug = slugify(title)
        
        ticket_dir = get_project_backlog_dir(project, "open")
        ticket_file = ticket_dir / f"{ticket_id}-{slug}.md"
        
        skills = match_skills(title)
        team = team_for_skills(skills)
        role = role_for_skills(skills)
        
        ticket = {
            "id": ticket_id,
            "title": title,
            "type": "feature",
            "status": "open",
            "phase": phase,
            "priority": priority,
            "estimate": estimate,
            "team": team,
            "skills": skills,
            "ist_zustand": f"The feature '{title}' does not exist yet in `projects/{project}/`.",
            "soll_zustand": f"The feature '{title}' is implemented and usable.",
            "value": f"'{title}' delivers visible progress in project {project}.",
            "modification_files": [f"projects/{project}/"],
            "constraints": [
                "Do not install unnecessary external packages without an ADR",
                "Follow the anti-slop protocol (no clichés, no god functions)",
                "Load the assigned skill files (see `skills`)"
            ],
            "scenarios": [{
                "name": "Feature is usable",
                "given": f"A user in project {project}",
                "when": f"They use the feature '{title}'",
                "then": f"'{title}' works as described and is tested"
            }],
            "acceptance_criteria": [
                f"'{title}' is implemented",
                f"'{title}' has tests",
                "Code is free of AI slop"
            ],
            "definition_of_done": [
                "Feature works (BDD scenario green)",
                "Tests present and green",
                "Anti-slop audit: 0 violations",
                "QA gate green (`./studio gate <project> --level 5`)"
            ],
            "dependencies": []
        }
        
        content = render_ticket_markdown(ticket)
        ticket_file.write_text(content)
        
        print(f"\n  Ticket created: {ticket_file}")
        print(f"  ID: {ticket_id}")
        print(f"  Role: {role}")
        print(f"  Team: {team}")
        print(f"  Skills: {', '.join(skills) if skills else '(auto-match)'}")
        print(f"  Status: open")
        print(f"  Project: {project}")
        print(f"\n  Next step:")
        print(f"    ./studio move {project} {ticket_id} implement")
        
        return ticket_id
    
    def _role_for_skills(self, skills: List[str]) -> str:
        """Derive the Director role from the skills."""
        return role_for_skills(skills)
    
    def cmd_move(self, project: str, ticket_id: str, new_status: str, reason: str = ""):
        """Move a ticket to a new status in the project backlog."""
        
        # Find ticket in project backlog
        ticket_file, current_status = find_project_ticket(project, ticket_id)
        
        if not ticket_file:
            print(f"  Ticket {ticket_id} not found in project {project}")
            return False
        
        # Determine new directory (within project)
        new_dir = get_project_backlog_dir(project, new_status)
        new_file = new_dir / ticket_file.name
        
        # Update ticket content
        content = ticket_file.read_text()
        content = content.replace(f"status: {current_status}", f"status: {new_status}")
        content += f"\n\n## Status Change\n- **From:** {current_status}\n- **To:** {new_status}\n- **Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n- **Reason:** {reason}\n"
        
        new_file.write_text(content)
        ticket_file.unlink()
        
        print(f"\n  Ticket {ticket_id}: {current_status} → {new_status}")
        print(f"  Project: {project}")
        if reason:
            print(f"  Reason: {reason}")

        status = load_status(project)
        title_match = re.search(r"^title:\s*(.+)$", content, re.MULTILINE)
        ticket_title = title_match.group(1).strip() if title_match else ticket_id

        if new_status == "implement":
            snapshots = status.setdefault("ticket_file_snapshots", {})
            snapshots[ticket_id] = snapshot_registry_files(project)
            status["active_ticket"] = ticket_id
            save_status(project, status)
            print(f"\n  📚 {format_library_first_hint(project, ticket_title)}")

        if new_status == "done":
            snapshots = status.get("ticket_file_snapshots", {})
            snap = snapshots.get(ticket_id, {})
            ok, warnings = check_reuse_before_done(project, ticket_id, snap)
            if warnings:
                print(f"\n  ⚠️  REUSE REVIEW — changed paths not promoted to studio-library:")
                for w in warnings[:10]:
                    print(f"    • {w}")
                print(f"\n  Promote if generic: ./studio library promote {project} <path> --ticket {ticket_id}")
                print(f"  Or document why it stays project-local in the ticket.")
            elif snap:
                print(f"\n  ✓ Reuse check: no unpromoted registry changes (or promotions logged).")
            status["active_ticket"] = None
            save_status(project, status)
        
        # If moving to done, check if all tickets are done
        if new_status == "done":
            project_backlog = PROJECTS_DIR / project / "backlog"
            open_dir = project_backlog / "open"
            if open_dir.exists():
                open_tickets = list(open_dir.glob(f"{project[:4].upper()}-*.md"))
                if not open_tickets:
                    print(f"\n  🎉 All tickets completed!")
                    print(f"  Next step:")
                    print(f"    ./studio gate {project} --level 5")
                    print(f"    ./studio retro {project}")
        
        return True
    
    # -------------------------------------------------------------------------
    # PHASE 4-5: QA GATE
    # -------------------------------------------------------------------------
    
    def cmd_gate(self, project: str, level: int = 5, anti_slop: bool = False):
        """Run the QA gate."""
        
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
            status["gate_status"] = "passed"
            if "gate_history" not in status:
                status["gate_history"] = []
            status["gate_history"].append({
                "gate": level,
                "status": "green",
                "passed_at": datetime.now().isoformat()
            })
        else:
            status["gate_status"] = "failed"
            if "gate_history" not in status:
                status["gate_history"] = []
            status["gate_history"].append({
                "gate": level,
                "status": "red",
                "failed_at": datetime.now().isoformat()
            })
        
        save_status(project, status)
        
        return result.returncode == 0
    
    # -------------------------------------------------------------------------
    # PHASE 6: LEARNING
    # -------------------------------------------------------------------------
    
    def cmd_learn(self, title: str, signal: str, source: str = "Studio Development"):
        """Create a learning item (strict studio schema, type: studio-evolution)."""
        
        lo_dir = BACKLOG_DIR / "open"
        lo_dir.mkdir(parents=True, exist_ok=True)
        
        # Find next LO number (scan open, done, blocked)
        numbers = []
        for sub in ("open", "done", "blocked"):
            lo_sub = BACKLOG_DIR / sub
            if lo_sub.exists():
                for f in lo_sub.glob("LO-*.md"):
                    m = re.search(r'LO-(\d+)', f.name)
                    if m:
                        numbers.append(int(m.group(1)))
        next_num = max(numbers) + 1 if numbers else 0
        
        lo_id = f"LO-{next_num:04d}"
        slug = slugify(title)
        lo_file = lo_dir / f"{lo_id}-{slug}.md"
        
        # Rollenzuweisung je Signal (Studio-Ebene)
        signal_roles = {
            "tooling-gap": "Studio Automation Engineer (Director)",
            "process-gap": "Process Guard (Director)",
            "design-gap": "UI/Interaction Designer (Director)",
            "quality-risk": "QA Specialist (Director)",
            "conflict": "Process Guard (Director)",
        }
        role = signal_roles.get(signal, "Process Guard (Director)")
        skills = {
            "tooling-gap": ["SO-001"],
            "process-gap": ["SO-002"],
            "design-gap": ["FE-002"],
            "quality-risk": ["SO-002"],
            "conflict": ["SO-002", "SO-003"],
        }.get(signal, ["SO-003"])
        
        ticket = {
            "id": lo_id,
            "title": title,
            "type": "studio-evolution",
            "status": "open",
            "phase": 6,
            "priority": "P2",
            "estimate": "M",
            "team": "09-studio-operations-evolution",
            "skills": skills,
            "assignee_role": role,
            "ist_zustand": f"Observation: {title} (signal: {signal}, source: {source})",
            "soll_zustand": "The studio is improved so this signal does not recur.",
            "value": "The studio learns from projects (dual loop) and improves process, skills, or tooling.",
            "modification_files": [".quinsy-studio/process/", ".quinsy-studio/studio-tools/", ".quinsy-studio/teams/"],
            "constraints": [
                "No changes to client projects (studio HQ only)",
                "Every change → CHANGELOG.md entry",
                "After implementation: skill-matching test + QA gate green",
                f"Signal: {signal} — Source: {source}"
            ],
            "scenarios": [{
                "name": "Studio improvement works",
                "given": f"The learning signal ({signal}) occurs again",
                "when": "The improved process/skill/tool is applied",
                "then": "The signal no longer occurs or is handled correctly"
            }],
            "acceptance_criteria": [
                "Improvement implemented in studio HQ",
                "CHANGELOG.md updated",
                "Test green"
            ],
            "definition_of_done": [
                "Discussed in meta retro",
                "Implemented (CHANGELOG.md entry)",
                "Skill-matching test green",
                "QA gate green"
            ],
            "dependencies": [],
        }
        
        content = render_ticket_markdown(ticket)
        lo_file.write_text(content)
        
        print(f"\n  Learning item created: {lo_file}")
        print(f"  ID: {lo_id}")
        print(f"  Signal: {signal}")
        print(f"  Role: {role}")
        
        return lo_id
    
    def cmd_learn_list(self):
        """Show all learning items."""
        
        print_header("LEARNING ITEMS")
        
        lo_dir = BACKLOG_DIR / "open"
        if not lo_dir.exists():
            print("  No learning items found")
            return
        
        los = list(lo_dir.glob("LO-*.md"))
        if not los:
            print("  No learning items found")
            return
        
        print(f"\n  Total: {len(los)}")
        for lo in sorted(los):
            content = lo.read_text()
            signal_match = re.search(r'signal:\s*(\w+)', content)
            signal = signal_match.group(1) if signal_match else "unknown"
            print(f"  - {lo.stem} [Signal: {signal}]")
    
    def cmd_retro(self, project: str):
        """Start a retrospective."""
        
        retro_dir = QUINSY_STUDIO / "retros"
        retro_dir.mkdir(parents=True, exist_ok=True)
        
        date_str = datetime.now().strftime("%Y-%m-%d")
        retro_file = retro_dir / f"meta-retro-{date_str}.md"
        
        template = f"""# Meta-Retro — {date_str}

## Incoming learning items
- LO-0000: ...

## Skill Review
| Skill | Quality signal | Action |
|-------|----------------|--------|
| ... | ... | ... |

## Decisions
- ... (every change → CHANGELOG.md entry)

## Action Items
- [ ] ... (Owner: ...)
"""
        retro_file.write_text(template)
        
        print(f"\n  Retrospective started: {retro_file}")
        print(f"  Include learning items: ./studio learn-list")
        
        return retro_file
    
    def cmd_update_skills(self, extra_args=None):
        """Subscribe/update the external skill dependencies (agent-as-a-dependency)."""
        
        print_header("EXTERNAL SKILLS UPDATE")
        print(f"\n  Loading external skill dependencies from skill-dependencies.json...")
        
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
            print(f"\n  ❌ Update failed")
            return False
        
        print(f"\n  ✅ External skills updated")
        print(f"  Skills located at: {QUINSY_STUDIO / 'external-skills'}")
        print(f"  See also: {QUINSY_STUDIO / 'external-skills' / 'INDEX.md'}")
        return True
    
    def cmd_sync(self, project: str):
        """Sync global assets from the project."""
        
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
        """Create an Architecture Decision Record."""
        
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
**Date:** {datetime.now().strftime('%Y-%m-%d')}
**Decision maker:** 
**Affected phases:** 

## Context
What is the situation? Which problem is being solved?

## Decision
What was decided?

## Rationale
Why was this decision made?

## Alternatives
What alternatives were considered?

### Alternative A: [Name]
- Pros: ...
- Cons: ...

### Alternative B: [Name]
- Pros: ...
- Cons: ...

## Consequences
What does this decision mean for the project?

### Positive
- ...

### Negative
- ...

### Risks
- ...

## Metrics
How is the success of this decision measured?

## Follow-up
What next steps result?
"""
        adr_file.write_text(template)
        
        print(f"\n  ADR created: {adr_file}")
        print(f"  Status: proposed")
        print(f"  Next step: fill in the ADR and set it to 'accepted'")
        
        return adr_file
    
    def cmd_board(self, project: str):
        """Show the ticket board of a project."""
        
        print_header(f"BACKLOG BOARD: {project}")
        
        project_backlog = PROJECTS_DIR / project / "backlog"
        statuses = [
            "open", "analyze", "plan", "design", "implement",
            "qa", "review", "reuse", "blocked", "done"
        ]
        
        for status in statuses:
            ticket_dir = project_backlog / status
            if ticket_dir.exists():
                tickets = list(ticket_dir.glob(f"{project[:4].upper()}-*.md"))
                if tickets or status in ("open", "implement", "done"):
                    print(f"\n  {status.upper()}: {len(tickets)}")
                    for t in sorted(tickets)[:8]:
                        print(f"    - {t.stem}")
            elif status in ("open", "done"):
                print(f"\n  {status.upper()}: 0")
    
    def cmd_groom(self, project: str):
        """Run a grooming session."""
        
        status = load_status(project)
        sprint = status.get("current_sprint", "SPRINT-01")
        
        print_header(f"GROOMING: {project} ({sprint})")
        
        project_backlog = PROJECTS_DIR / project / "backlog"
        
        # Show blocked tickets
        blocked_dir = project_backlog / "blocked"
        if blocked_dir.exists():
            blocked = list(blocked_dir.glob(f"{project[:4].upper()}-*.md"))
            if blocked:
                print(f"\n  Blocked tickets: {len(blocked)}")
                for t in blocked:
                    print(f"    - {t.stem}")
        
        # Show open tickets
        open_dir = project_backlog / "open"
        if open_dir.exists():
            open_tickets = list(open_dir.glob(f"{project[:4].upper()}-*.md"))
            if open_tickets:
                print(f"\n  Open tickets: {len(open_tickets)}")
                for t in open_tickets:
                    print(f"    - {t.stem}")
        
        # Create grooming protocol
        sprint_dir = PROJECTS_DIR / project / "sprints" / sprint
        sprint_dir.mkdir(parents=True, exist_ok=True)
        grooming_file = sprint_dir / "grooming.md"
        
        grooming_template = f"""# Grooming Protocol — {sprint}

**Date:** {datetime.now().strftime('%Y-%m-%d')}
**Participants:** Project Manager, ...

## Blocked tickets
| Ticket | Reason | Action |
|--------|--------|--------|
| ... | ... | ... |

## Priority changes
| Ticket | New priority | Reason |
|--------|--------------|--------|
| ... | ... | ... |

## New tickets
| Ticket | Title | Priority |
|--------|-------|----------|
| ... | ... | ... |

## Capacity adjustments
- ...

## Next steps
- ...
"""
        grooming_file.write_text(grooming_template)
        print(f"\n  Grooming protocol: {grooming_file}")
        
        return grooming_file
    
    def cmd_decide(self, project: str, title: str):
        """Create a decision record."""
        
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
**Date:** {datetime.now().strftime('%Y-%m-%d')}
**Requested by:** 
**Decision by:** 

## Decision
What needs to be decided?

## Context
Why is this decision necessary?

## Options

### Option A: <Name>
- Pros: ...
- Cons: ...
- Cost: ...

### Option B: <Name>
- Pros: ...
- Cons: ...
- Cost: ...

## Recommendation
Which option does the agent recommend and why?

## Risks
What could go wrong?

## Consequences
What does this decision mean for the project?
"""
        dr_file.write_text(template)
        
        print(f"\n  Decision record created: {dr_file}")
        print(f"  Status: pending")
        print(f"  Next step: reach a decision")
        
        return dr_file
    
    def cmd_decisions(self, project: str):
        """Show all decision records."""
        
        decisions_dir = PROJECTS_DIR / project / "docs" / "decisions"
        
        print_header(f"DECISION RECORDS: {project}")
        
        if not decisions_dir.exists():
            print("  No decision records found")
            return
        
        drs = list(decisions_dir.glob("DR-*.md"))
        if not drs:
            print("  No decision records found")
            return
        
        print(f"\n  Total: {len(drs)}")
        for dr in sorted(drs):
            content = dr.read_text()
            status_match = re.search(r'\*\*Status:\*\*\s*(\w+)', content)
            status = status_match.group(1) if status_match else "unknown"
            print(f"  - {dr.stem} [{status}]")
    
    def cmd_env(self, project: str, action: str):
        """Manage the Docker environment."""
        
        docker_dir = PROJECTS_DIR / project / "docker"
        
        print_header(f"DOCKER ENV: {project}")
        
        if action == "init":
            docker_dir.mkdir(parents=True, exist_ok=True)
            
            # Copy the base template from the studio and parametrize per project
            template_dir = TEMPLATES_DIR / "docker"
            if not template_dir.exists():
                print(f"\n  ⚠️  Base docker template missing: {template_dir}")
                return False
            
            for f in template_dir.iterdir():
                if f.is_file():
                    content = f.read_text()
                    content = content.replace("{{PROJECT_NAME}}", project)
                    (docker_dir / f.name).write_text(content)
            
            print(f"\n  Docker environment initialized: {docker_dir}")
            print(f"  Base template: {template_dir}")
            print(f"  → docker-compose.yml, .env.example (project-parametrized)")
            print(f"\n  Add project-specific services (Mailpit, Worker, ...) here:")
            print(f"    {docker_dir}/docker-compose.yml")
            print(f"\n  Next step:")
            print(f"    cd {docker_dir} && cp .env.example .env && docker-compose up -d")
        
        elif action == "up":
            print(f"\n  Starting docker environment...")
            print(f"  (cd {docker_dir} && docker-compose up -d)")
        
        elif action == "down":
            print(f"\n  Stopping docker environment...")
            print(f"  (cd {docker_dir} && docker-compose down)")
        
        elif action == "status":
            print(f"\n  Checking docker status...")
            print(f"  (cd {docker_dir} && docker-compose ps)")
        
        elif action == "logs":
            print(f"\n  Showing docker logs...")
            print(f"  (cd {docker_dir} && docker-compose logs -f)")
    
    def cmd_repo(self, project: str, action: str):
        """Manage the GitHub repository."""
        
        print_header(f"GITHUB REPO: {project}")
        
        if action == "create":
            print(f"\n  Create repository: {project}")
            print(f"  (gh repo create {project} --private --source=.)")
            print(f"  ⚠️  No auto-push without explicit approval!")
        
        elif action == "status":
            print(f"\n  Checking repository status...")
            print(f"  (gh repo view {project})")
    
    def cmd_promote(self, project: str, asset_path: str):
        """Promote an asset to the studio library."""
        
        source = PROJECTS_DIR / project / asset_path
        dest = STUDIO_LIBRARY / asset_path
        
        print_header(f"PROMOTE ASSET: {asset_path}")
        
        if not source.exists():
            print(f"\n  Source not found: {source}")
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
        print(f"  Target: {dest}")
        print(f"  Manifest updated")
        
        return True

# =============================================================================
# HELP & MAIN
# =============================================================================

def print_help():
    """Print the help text."""
    print("""
Quinsy Studio — Dual-Speed Autonomous Enterprise Agency

Usage:
  ./studio <command> [args...]

Commands:
  # Project management
  ./studio init <project> --archetype <type>     Initialize project
  ./studio bootstrap [project] [intake-file]     AI entry: init→intake→concept→sprint
  ./studio resume <project>                      Next actions from status.json
  ./studio focus <project>                       Set active project + scope banner
  ./studio guard <project> "request text"        Check if request is in scope
  ./studio verify-worlds                         Studio vs project git separation
  ./studio library list                           List studio-library assets
  ./studio library pull <project> auth billing    Copy library → project
  ./studio library promote <project> packages/billing [--force]
  ./studio library suggest <project> <query>      Find assets before coding
  ./studio promote-library <project> [--force]    Promote design system (gate 2)
  ./studio start <project> --mode [core|lean]    Start project
  ./studio status <project>                      Show status
  ./studio board <project>                       Show board

  # Phase 1: Intake (human gate 0)
  ./studio intake <project> <input-file>         Process intake (no tickets yet)

  # Phase 2: Architecture (human gate 1)
  ./studio blueprint <project>                   Scaffold architecture docs
  ./studio approve <project> --gate 0            Approve PRD + definitions
  ./studio approve <project> --gate 1            Approve architecture blueprint

  # Phase 3: Design (human gate 2)
  ./studio design <project> --scope journey|core-views
  ./studio approve <project> --gate 2            Approve design → generates tickets
  ./studio revise <project> --gate <0|1|2> --feedback "..."

  # Legacy
  ./studio concept <project>                     → blueprint / design

  # Phase 3: Sprint Management
  ./studio sprint <project>                      Create sprint
  ./studio ticket <project> "Title"              Create ticket
  ./studio move <project> <id> <status>          Move ticket
  ./studio groom <project>                       Run grooming

  # Phase 4-5: QA
  ./studio gate <project> [--level N]            Run QA gate

  # Phase 6: Learning
  ./studio learn "Title" --signal <s>            Create learning item
  ./studio learn-list                            Show learning items
  ./studio retro <project>                       Start retrospective
  ./studio sync <project>                        Sync global assets
  ./studio update-skills                         Subscribe/update external skill packages

  # Tools
  ./studio adr <project> "Title"                 Create ADR
  ./studio decide <project> "Title"              Create decision record
  ./studio decisions <project>                   Show decision records
  ./studio env <project> init|up|down|status     Docker env (base template)
  ./studio repo <project> create|status          GitHub repo
  ./studio promote <project> <asset>             Promote asset to library

Dual-Speed Operating Model:
  CORE — For new platforms & complex systems (6 phases with human gates)
  LEAN — For iterations & features in existing projects (4 phases)

Examples:
  ./studio bootstrap                              List intake PRDs + projects
  ./studio bootstrap nudge
  ./studio approve nudge --gate 0
  ./studio blueprint nudge
  ./studio approve nudge --gate 1
  ./studio design nudge --scope journey
  ./studio approve nudge --gate 2
  ./studio sprint nudge
  ./studio ticket nudge "Button Component" --phase 3 --priority P1
  ./studio move nudge NUDG-0001 implement --reason "Implementation started"
  ./studio gate nudge --level 5
  ./studio learn "Gate check takes too long" --signal tooling-gap
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

    if command == "bootstrap":
        project = None
        intake_file = None
        archetype = "saas-application"
        mode = "core"
        positional = [a for a in args if not a.startswith("--")]
        if len(positional) >= 1:
            project = positional[0]
        if len(positional) >= 2:
            intake_file = positional[1]
        for i, arg in enumerate(args):
            if arg == "--archetype" and i + 1 < len(args):
                archetype = args[i + 1]
            elif arg == "--mode" and i + 1 < len(args):
                mode = args[i + 1]
        orchestrator.cmd_bootstrap(project, intake_file, archetype, mode)

    elif command == "resume" and len(args) >= 1:
        orchestrator.cmd_resume(args[0])

    elif command == "focus" and len(args) >= 1:
        orchestrator.cmd_focus(args[0])

    elif command == "guard" and len(args) >= 2:
        orchestrator.cmd_guard(args[0], " ".join(args[1:]))

    elif command == "verify-worlds":
        orchestrator.cmd_verify_worlds()

    elif command == "promote-library" and len(args) >= 1:
        positional = [a for a in args if not a.startswith("--")]
        dry_run = "--dry-run" in args
        force = "--force" in args
        if positional:
            orchestrator.cmd_promote_library(positional[0], dry_run=dry_run, force=force)

    elif command == "library":
        lib_args = args[1:] if len(args) > 1 else []
        sub = args[0] if args else "list"
        orchestrator.cmd_library(sub, lib_args)

    elif command == "init" and len(args) >= 1:
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
    
    elif command == "blueprint" and len(args) >= 1:
        orchestrator.cmd_blueprint(args[0])

    elif command == "design" and len(args) >= 1:
        project = args[0]
        scope = "core-views"
        for i, arg in enumerate(args):
            if arg == "--scope" and i + 1 < len(args):
                scope = args[i + 1]
        orchestrator.cmd_design(project, scope)

    elif command == "revise" and len(args) >= 1:
        project = args[0]
        gate = 0
        feedback = ""
        for i, arg in enumerate(args):
            if arg == "--gate" and i + 1 < len(args):
                gate = int(args[i + 1])
            elif arg == "--feedback" and i + 1 < len(args):
                feedback = args[i + 1]
        orchestrator.cmd_revise(project, gate, feedback)

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
        source = "Studio Development"
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
