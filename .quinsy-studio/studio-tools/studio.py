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
  ./studio adopt <project> --from <git-url|path> Overlay studio docs on an existing repo
  ./studio bootstrap [project] [intake-file]     AI entry: init→intake→concept→sprint
  ./studio resume <project>                      Next actions from status.json
  ./studio execute <project> [--json]            One next action; loop until HITL
  ./studio settings [--reset-usage]              Policy + estimated token usage (no API keys)
  ./studio note <project> "…"                    Queue mid-execute input (ACK; drain after MOVE_DONE)
  ./studio inform <project> --gate 1             Architecture is HITL — use approve, not inform
  ./studio veto <project> --decision ADR-…
  ./studio train <skill-id> --from mistake --topic "…"
  ./studio ticket-card <project> <id>            Compact ticket card
  ./studio receipt <project> <id>                Scaffold execution receipt
  ./studio health <project>                      Sprint state-graph check
  ./studio focus <project>                       Set active project + isolate siblings
  ./studio isolate <project>                     Hide sibling projects/ from the agent
  ./studio guard <project> "request text"        Check if request is in scope
  ./studio verify-worlds                         Studio vs project git separation
  ./studio verify-abstraction                    Scan studio HQ for project-name leaks
  ./studio install [--with-skills]               npm deps after git clone (+ optional skills)
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
  ./studio review <project> [--approve|--reject] Sprint review (human)
  ./studio reuse <project> [--record path action] Reuse inform brief after sprint (not a HITL gate)
  ./studio feedback <project> "..."              Capture raw feedback (not a ticket)
  ./studio clarify <project> FB-001 [--approve]  Clarify feedback → executable draft
  ./studio feedback-list <project>               Show feedback queue
  ./studio ticket <project> "Title"              Create ticket
  ./studio move <project> <id> <status>          Move ticket
  ./studio groom <project> [--approve]              Validate sprint backlog + grooming

  # Amendment intake (post gate 2)
  ./studio amend <project> <brief-file>          Scaffold AM-NNN analysis folder
  ./studio amendments <project>                  List amendments + status
  ./studio approve <project> --amendment AM-001  Human sign-off on amendment
  ./studio approve <project> --milestones        Approve revised milestone roadmap
  ./studio approve <project> --prd-amendment AM-001  PRD tier change (class C)

  # Phase 4: Implementation
  ./studio gate <project> [--level N]            Run QA gate

  # Phase 6: Learning
  ./studio learn "Title" --signal <s>            Create learning item
  ./studio learn-list                            Show learning items
  ./studio infusion                              Studio LO gate — open learnings before project sprint
  ./studio retro <project> [--complete]          Sprint retrospective
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
from design_ticket_helpers import (
    default_design_spec_path,
    design_deliverables_status,
    design_implement_blocked_message,
    design_spec_completeness_error,
    design_mocks_emoji_icon_warning,
    enrich_design_skills,
    infer_ticket_type,
    parse_design_fields,
    requires_design_approval,
    set_design_approved,
    write_design_spec_stub,
)
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
    verify_studio_abstraction,
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
from sprint_backlog_validate import (
    format_validation_brief,
    validate_sprint_backlog,
    write_validation_report,
)
from backlog_paths import (
    QUEUE_STATUS,
    WORKFLOW_FOLDERS,
    ensure_backlog_layout,
    find_ticket,
    list_unscheduled_backlog,
    migrate_legacy_backlog,
    queue_ticket_paths,
    workflow_dir,
)
from sprint_planning import (
    apply_sprint_scope,
    format_planning_brief,
    load_scope_proposal,
    propose_sprint_scope,
    write_planning_questions_report,
    write_scope_proposal,
)
from sprint_reuse_review import (
    approve_reuse_review,
    format_reuse_brief,
    prepare_reuse_review,
    record_reuse_decision,
    resolve_reuse_sprint,
    reuse_gate_message,
)
from sprint_hitl import (
    add_feedback,
    approve_review,
    can_plan_next_sprint,
    clarify_feedback,
    format_feedback_list,
    get_ready_feedback_for_ticket,
    get_sprint_hitl,
    has_raw_feedback,
    has_ready_feedback,
    implement_blocked_reason,
    is_autonomous_sprint_execution,
    is_sprint_closed,
    link_feedback_to_ticket,
    load_feedback_queue,
    maybe_flag_sprint_review,
    needs_sprint_review,
    complete_retro,
    prepare_retro,
    prepare_review,
    reject_review,
    RETRO_DONE,
    RETRO_PENDING,
    REVIEW_APPROVED,
    sprint_ticket_summary,
)
from studio_execute import (
    MAX_GATE_RETRIES,
    append_debug_attempt,
    append_execution_event,
    count_gate_fails,
    decide_next_action,
    existing_gate_fail_lo,
    format_execute_step,
    format_health,
    health_report,
    load_execution_log,
    receipt_is_complete,
    receipt_path,
    ticket_card_for,
    write_receipt_stub,
)
from amendment_intake import (
    amendment_path_for_cli,
    approve_amendment,
    approve_milestones,
    format_amendments_list,
    gate2_approved,
    pending_amendments,
    resolve_amendment_file,
    resume_amendment_actions,
    scaffold_amendment,
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

def get_project_backlog_dir(project: str, status: str = QUEUE_STATUS) -> Path:
    """Return the folder for a ticket status. 'backlog' = product backlog queue at backlog/*.md."""
    ensure_backlog_layout(project)
    root = PROJECTS_DIR / project / "backlog"
    if status in (QUEUE_STATUS, "open"):
        root.mkdir(parents=True, exist_ok=True)
        return root
    if status in WORKFLOW_FOLDERS:
        return workflow_dir(project, status)
    return workflow_dir(project, "implement")

def find_project_ticket(project: str, ticket_id: str) -> tuple:
    """Find a ticket in the project backlog. Returns (filepath, current_status)."""
    ensure_backlog_layout(project)
    path, status = find_ticket(project, ticket_id)
    if path:
        return path, status
    return None, None

def load_status(project: str) -> Dict:
    """Load project status.json (snapshots live in docs/ticket-file-snapshots.json)."""
    from studio_status import load_status as _load_status

    return _load_status(project)

def save_status(project: str, status: Dict):
    """Save project status.json without embedding file-hash snapshots."""
    from studio_status import save_status as _save_status

    _save_status(project, status)

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


def assign_open_tickets_to_sprint(project: str, sprint_name: str, max_tickets: int = 6) -> List[Dict]:
    """Tag mature open backlog tickets with sprint (feedback-sourced first)."""
    planning = assign_backlog_to_sprint(project, sprint_name, max_tickets=max_tickets)
    return planning["assigned"]

# =============================================================================
# DUAL-SPEED ORCHESTRATOR
# =============================================================================

# Minimum QA level required before ./studio move … done
MIN_DONE_GATE_LEVEL = 5

class StudioOrchestrator:
    """Main orchestrator for the Dual-Speed Operating Model."""
    
    def __init__(self):
        ensure_dirs()
    
    # -------------------------------------------------------------------------
    # PROJECT MANAGEMENT
    # -------------------------------------------------------------------------

    def cmd_adopt(
        self,
        project: str,
        source: str,
        intent: Optional[str] = None,
        archetype: str = "saas-application",
    ):
        """Overlay studio process on an existing codebase. Never wipe source."""
        from studio_adopt import adopt_project

        print_header(f"ADOPT: {project}")
        try:
            result = adopt_project(project, source, intent=intent, archetype=archetype)
        except (ValueError, RuntimeError) as exc:
            print(f"\n  ❌ {exc}")
            print(f"     Usage: ./studio adopt {project} --from <git-url-or-path> [--intent intake/{project}.md]")
            return False

        print(f"\n  Path:    {result.get('path')}")
        print(f"  Source:  {result.get('source_action')}")
        if result.get("intent"):
            print(f"  Intent:  {result['intent']}")
        for note in result.get("notes") or []:
            print(f"  • {note}")
        print("\n  Overlay complete. Application source was not wiped.")
        print("  Next (agent): fill docs/as-built/ from the live code (cite paths).")
        print(f"    ./studio focus {project}")
        print(f"    ./studio execute {project}   # until HITL gate 0 (as-built + PRD)")
        print("  Process: .quinsy-studio/process/brownfield-adopt.md")
        return True

    def _print_bootstrap_discovery(self):
        """List intake PRDs and existing projects for AI/human discovery."""
        print_header("QUINSY STUDIO — BOOTSTRAP")
        print("\n  Place a PRD in intake/, then run:")
        print("    ./studio bootstrap <project>")
        print("    ./studio bootstrap <project> intake/<file>.md")
        print("\n  Existing codebase (do not empty-init):")
        print("    ./studio adopt <project> --from <git-url-or-path>")
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

        from studio_adopt import looks_like_application_source

        if project_dir.exists() and looks_like_application_source(project_dir):
            if not (project_dir / "status.json").exists():
                print(f"\n  ❌ '{project}' already has application source and is not a studio project.")
                print(f"     Overlay instead of empty scaffold:")
                print(f"       ./studio adopt {project} --from {project_dir}")
                return False

        if not project_dir.exists() or not (project_dir / "status.json").exists():
            if not intake_path:
                print(f"\n  ❌ Project '{project}' not initialized and no intake PRD found.")
                print(f"     Place intake/<name>.md or run: ./studio bootstrap {project} intake/<file>.md")
                print(f"     Existing codebase: ./studio adopt {project} --from <git-url-or-path>")
                return False
            self.cmd_init(project, archetype)

        prd_file = project_dir / "docs" / "intake" / "prd.md"
        status = load_status(project) if (project_dir / "status.json").exists() else {}

        if not prd_file.exists() and status.get("mode") != "adopt":
            if not intake_path:
                print(f"\n  ❌ No intake file for '{project}'. Add intake/<name>.md or pass the path.")
                print(f"     Existing codebase: ./studio adopt {project} --from <git-url-or-path>")
                return False
            ok = self.cmd_intake(project, intake_path_for_cli(intake_path))
            if not ok:
                return False

        status = load_status(project)
        if status.get("mode") == "adopt":
            return self._bootstrap_from_status(project, status)
        if not status.get("mode") or status.get("phase") == "0":
            self.cmd_start(project, mode)
            status = load_status(project)

        return self._bootstrap_from_status(project, status)

    def _bootstrap_from_status(self, project: str, status: Dict) -> bool:
        """Continue bootstrap from current phase / gate state."""
        hg = status.get("human_gates", {})

        if hg.get("0", {}).get("status") != "approved":
            adopt = status.get("mode") == "adopt"
            hint = (
                "Fill docs/as-built/ from code, synthesize PRD, then approve as-built truth."
                if adopt
                else "Fill docs/definitions/ from PRD, then approve intake."
            )
            self._print_gate_pause(project, 0, hint)
            return True

        if status.get("phase") == PHASE_INTAKE or hg.get("1", {}).get("status") != "approved":
            blueprint = PROJECTS_DIR / project / "docs" / "architecture" / "BLUEPRINT.md"
            if not blueprint.exists():
                self.cmd_blueprint(project)
            if hg.get("1", {}).get("status") != "approved":
                self._print_gate_pause(project, 1, "Review docs/architecture/ and ADRs.")
                return True

        if status.get("phase") in (PHASE_INTAKE, PHASE_BLUEPRINT, PHASE_DESIGN) or hg.get("2", {}).get("status") != "approved":
            if status.get("mode") == "adopt":
                self._print_gate_pause(
                    project,
                    2,
                    "Document design of what exists (surface map). Do not scaffold an empty Next.js prototype.",
                )
                return True
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
        status = load_status(project)
        if status.get("mode") == "adopt":
            labels = {
                0: "As-built truth + synthesized PRD",
                1: "As-is architecture (no stack swap)",
                2: "Design of what exists + debt",
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
        actions.extend(resume_amendment_actions(project))
        reuse_msg = reuse_gate_message(project, status)
        if reuse_msg:
            actions.append("Reuse inform brief (not a gate)")
            actions.append(f"./studio reuse {project}")

        prd_file = project_dir / "docs" / "intake" / "prd.md"
        adopt = status.get("mode") == "adopt"

        if adopt and not prd_file.exists() and not (project_dir / "docs" / "as-built" / "00-product.md").exists():
            actions.append("AI: fill docs/as-built/ from the live codebase (cite paths; no _TODO_)")
            actions.append(f"Then synthesize docs/intake/prd.md — Human: ./studio approve {project} --gate 0")
        elif adopt and hg.get("0", {}).get("status") != "approved":
            from studio_adopt import as_built_is_ready

            if not as_built_is_ready(project):
                actions.append("AI: fill docs/as-built/ (cite paths; high-level summary is not done)")
            else:
                actions.append("AI: synthesize docs/intake/prd.md + fill docs/definitions/ from as-built")
            actions.append(f"Human: confirm as-built truth → ./studio approve {project} --gate 0")
        elif not prd_file.exists():
            intake_path = resolve_intake_file(project)
            if intake_path:
                actions.append(f"./studio intake {project} {intake_path_for_cli(intake_path)}")
            else:
                actions.append(f"Add intake/<prd>.md, then ./studio bootstrap {project}")
                actions.append(f"Existing codebase: ./studio adopt {project} --from <git-url-or-path>")
        elif hg.get("0", {}).get("status") != "approved":
            actions.append("AI: fill projects/{p}/docs/definitions/ from PRD (no _TODO_)".format(p=project))
            actions.append(f"Human: review PRD + definitions → ./studio approve {project} --gate 0")
        elif hg.get("1", {}).get("status") != "approved":
            actions.append(f"./studio blueprint {project}")
            actions.append(
                "AI: fill docs/architecture/ from as-is + ADRs for existing decisions"
                if adopt
                else "AI: fill docs/architecture/, create ADRs"
            )
            actions.append(f"Human: review blueprint → ./studio approve {project} --gate 1")
        elif hg.get("2", {}).get("status") != "approved":
            if adopt:
                actions.append("AI: fill design/DESIGN.md + docs/ia/surface-map.md from existing UI")
                actions.append("Do NOT scaffold design/prototype as a fake app")
                actions.append(f"Human: review design of what exists → ./studio approve {project} --gate 2")
            elif not status.get("design_scope"):
                actions.append(f"Human: choose mock scope → ./studio design {project} --scope journey|core-views")
            else:
                actions.append(f"./studio design {project} --scope {status['design_scope']}")
                actions.append("AI: build design/prototype (Next.js), ui/tokens, sticker-sheet")
                actions.append(f"Human: review mocks → ./studio approve {project} --gate 2")
        elif not status.get("current_sprint"):
            actions.append(f"./studio sprint {project}")
        elif needs_sprint_review(status):
            actions.append(f"⏸ HUMAN: sprint review pending — ./studio review {project}")
            actions.append(f"Human: try shipped work, then ./studio review {project} --approve")
            actions.append(f"Product feedback: ./studio feedback {project} \"...\" (NOT implementation)")
            actions.append(f"Flow: feedback → clarify → ticket --from-feedback → next sprint")
            actions.append("Agent: do NOT edit projects/{p}/ for review feedback — backlog only".format(p=project))
        elif is_sprint_closed(status, project):
            hitl = get_sprint_hitl(status)
            reuse_msg = reuse_gate_message(project, status)
            if reuse_msg:
                actions.append(f"Reuse inform brief (not a gate): ./studio reuse {project}")
            elif hitl.get("retro_status") != RETRO_DONE:
                actions.append(f"./studio retro {project}")
            else:
                actions.append(f"⏸ Sprint closed (review approved) — plan next sprint with human")
                actions.append(f"./studio sprint {project}")
                actions.append(f"./studio sprint {project} --approve-scope")
                actions.append(f"./studio groom {project} --approve")
            actions.append(f"./studio feedback {project} \"...\"  (ideas for next sprint)")
            actions.append(f"./studio clarify {project} FB-001 ... --approve")
            actions.append(f"./studio ticket {project} \"...\" --from-feedback FB-001")
        else:
            sprint = status.get("current_sprint", "")
            hitl = get_sprint_hitl(status)
            if is_autonomous_sprint_execution(status, project):
                summary = sprint_ticket_summary(project, sprint)
                actions.append(
                    f"🤖 AUTONOMOUS SPRINT ({sprint}): implement remaining tickets "
                    f"({summary['done']}/{summary['total']} done) — no human checkpoint mid-sprint"
                )
                actions.append("Agent: do NOT pause for approval between tickets; human joins at sprint review")
                next_open = next(
                    (t for t in summary["tickets"] if t["status"] in ("backlog", "blocked")),
                    None,
                )
                if next_open:
                    actions.append(
                        f"./studio move {project} {next_open['id']} implement --reason \"Sprint execution\""
                    )
            elif hitl.get("scope_status") != "approved":
                actions.append(f"⏸ HUMAN: approve sprint scope — read sprints/{sprint}/scope-proposal.md")
                actions.append(f"./studio sprint {project} --approve-scope")
            elif hitl.get("groom_status") != "approved":
                actions.append(f"./studio groom {project}")
                actions.append(f"./studio groom {project} --approve")
            if has_raw_feedback(project, sprint):
                actions.append(f"Queue only (act after review): ./studio feedback-list {project}")
            if has_ready_feedback(project, sprint):
                actions.append(
                    f"Ticket from feedback after review: ./studio ticket {project} \"...\" --from-feedback FB-NNN"
                )
            actions.append(f"./studio board {project}")
            actions.append(f"./studio move {project} <TICKET-ID> done --reason \"DoD met\"")
            actions.append(f"When all sprint tickets done: ./studio review {project} → human --approve")

        print("\n  Next actions:")
        for i, action in enumerate(actions, 1):
            print(f"    {i}. {action}")

        if briefing.exists():
            print(f"\n  Read first: projects/{project}/agent-briefing.md")
        print(f"  Process: .quinsy-studio/process/lifecycle.md")
        set_active_project(project, status)
        print(f"\n  Agentic loop: ./studio execute {project}")
        print("  Do NEXT, then execute again, until ACTION is HITL. Do not ask to continue.")
        return True

    def cmd_execute(self, project: str, as_json: bool = False):
        """Emit exactly one next action. Agent must loop until HITL."""
        if not (PROJECTS_DIR / project).exists():
            print(f"\n  ❌ Project '{project}' not found.")
            return False
        from studio_isolation import apply_project_isolation

        apply_project_isolation(project)
        status = load_status(project)
        step = decide_next_action(project)
        if as_json:
            print(json.dumps(step.to_dict(), indent=2))
        else:
            print_header(f"EXECUTE: {project}")
            print(format_execute_step(project, step))
        set_active_project(project, status)
        return True

    def cmd_ticket_card(self, project: str, ticket_id: str):
        """Print a compact card — not the full ticket or backlog."""
        card = ticket_card_for(project, ticket_id)
        if not card:
            print(f"  Ticket {ticket_id} not found in {project}")
            return False
        print_header(f"CARD {ticket_id}")
        print(f"  {card.get('id')}: {card.get('title')}")
        if card.get("target"):
            print(f"  target: {card['target']}")
        if card.get("scope"):
            print(f"  scope:  {card['scope']}")
        for ac in card.get("ac") or []:
            print(f"  ac: {ac}")
        if card.get("files"):
            print(f"  files: {', '.join(card['files'])}")
        if card.get("deps"):
            print(f"  deps:  {', '.join(card['deps'])}")
        if card.get("skills"):
            print(f"  skills: {', '.join(card['skills'])}")
        if card.get("playbooks"):
            print(f"  playbooks: {', '.join(card['playbooks'])}")
        print(f"  path:  {card.get('path')}  (read this file only when implementing)")
        return True

    def cmd_receipt(self, project: str, ticket_id: str):
        """Scaffold the execution receipt required before move … done."""
        status = load_status(project)
        sprint = status.get("current_sprint") or ""
        if not sprint:
            print("  No current sprint — cannot write a receipt.")
            return False
        card = ticket_card_for(project, ticket_id)
        path = write_receipt_stub(project, sprint, ticket_id, card)
        print_header(f"RECEIPT {ticket_id}")
        print(f"  {path.relative_to(STUDIO_ROOT)}")
        print("  Fill Plan, AC coverage, and Default flow (LO-0051), then ./studio execute")
        return True

    def cmd_health(self, project: str):
        """Validate sprint / LO / receipt / gate state graph."""
        print_header(f"HEALTH: {project}")
        print(format_health(project, health_report(project)))
        return True

    def cmd_settings(self, reset_usage_flag: bool = False):
        """Show merged studio policy + estimated token usage."""
        from studio_settings import format_settings_report, load_settings, load_usage, reset_usage

        print_header("STUDIO SETTINGS")
        if reset_usage_flag:
            reset_usage()
            print("  Usage reset.\n")
        print(format_settings_report(load_settings(), load_usage()))
        return True

    def cmd_note(self, project: str, text: str = "", drain: bool = False):
        """Queue a mid-execute human note (ACK only) or drain after MOVE_DONE."""
        from studio_human_inbox import append_note, classify_note, drain_open_notes, open_notes

        status = load_status(project)
        sprint = status.get("current_sprint") or ""
        scope = sprint or "pre-sprint"
        print_header(f"NOTE — {project} ({scope})")
        if drain:
            drained = drain_open_notes(project, sprint)
            if not drained:
                print("  Inbox empty.")
                return True
            print(f"  Drained {len(drained)} note(s):")
            for note in drained:
                kind = classify_note(note.get("text") or "")
                print(f"    {note.get('id')} [{kind}] {note.get('text')}")
                if kind == "feedback":
                    print(f"      → ./studio feedback {project} \"...\" if this is a product idea")
                if kind == "tech-veto":
                    print(f"      → ./studio veto {project} --decision \"...\" --reason \"...\"")
            print(f"  Resume: ./studio execute {project}")
            return True
        if not text.strip():
            pending = open_notes(project, sprint)
            print(f"  Open notes: {len(pending)}")
            for note in pending:
                print(f"    {note.get('id')} {note.get('text')}")
            print(f"  Usage: ./studio note {project} \"...\"  or  ./studio note {project} --drain")
            return True
        note = append_note(project, sprint, text)
        print(f"  ACK queued {note['id']} — current ACTION continues. Do not preempt.")
        print(f"  Drain after MOVE_DONE: ./studio note {project} --drain")
        return True

    def cmd_inform(self, project: str, gate: Optional[int] = None):
        """Inform-only steps (not architecture/design — those are HITL)."""
        if gate == 1:
            print_header(f"GATE 1 IS HITL — {project}")
            print("  Architecture after PRD is a human decision.")
            print(f"  Agent: ./studio blueprint {project}")
            print(f"  Human: ./studio approve {project} --gate 1")
            print(f"  Iterate: ./studio revise {project} --gate 1 --feedback \"...\"")
            return False
        if gate == 2:
            print_header(f"GATE 2 IS HITL — {project}")
            print("  Design track after architecture is a human decision")
            print("  (direction, design system, stills/mocks or clickable prototype).")
            print(f"  Agent: ./studio design {project}")
            print(f"  Human: ./studio approve {project} --gate 2")
            print(f"  Iterate: ./studio revise {project} --gate 2 --feedback \"...\"")
            return False
        print("  Architecture (gate 1) and design (gate 2) require ./studio approve, not inform.")
        return False

    def cmd_veto(self, project: str, decision: str = "", reason: str = "", ack: bool = False):
        """Record or acknowledge a tech-veto at the ticket boundary."""
        status = load_status(project)
        print_header(f"TECH-VETO — {project}")
        if ack:
            veto = status.get("tech_veto") or {}
            veto["status"] = "acked"
            veto["acked_at"] = datetime.now().isoformat()
            status["tech_veto"] = veto
            save_status(project, status)
            print("  Veto acknowledged — revise the ADR; do not ship the addition.")
            return True
        if not decision.strip():
            print("  Usage: ./studio veto <project> --decision ADR-… --reason \"…\"")
            print("         ./studio veto <project> --ack")
            return False
        status["tech_veto"] = {
            "status": "open",
            "decision": decision.strip(),
            "reason": reason.strip(),
            "at": datetime.now().isoformat(),
        }
        save_status(project, status)
        print(f"  Queued: {decision} — takes effect at the next IMPLEMENT boundary (not mid-file).")
        print(f"  Loop: ./studio execute {project}  → HITL tech-veto before the next ticket")
        return True

    def cmd_train(self, skill_id: str, topic: str, source: str = "mistake"):
        """Queue a parallel skill-training job. Does not block product IMPLEMENT."""
        from studio_train import enqueue_train, skill_file_hint

        print_header("TRAIN")
        try:
            job = enqueue_train(skill_id, topic, source=source)
        except ValueError as exc:
            print(f"  ⚠️  {exc}")
            print("  Usage: ./studio train <skill-id> --from book|url|mistake --topic \"…\"")
            return False
        hint = skill_file_hint(skill_id)
        print(f"  Queued {job['id']}  skill={job['skill_id']}  topic={job['topic']}")
        print("  Second agent: research (cited), derive principles (no copyrighted verbatim),")
        print("  append to the skill toolbox and a playbook. Product execute continues IMPLEMENT.")
        if hint:
            print(f"  Skill file: {hint}")
        return True

    def cmd_focus(self, project: str):
        """Set active project context for IDE agent (scope banner)."""
        project_dir = PROJECTS_DIR / project
        if not project_dir.exists():
            print(f"\n  ❌ Project '{project}' not found.")
            return False
        status = load_status(project)
        set_active_project(project, status)
        from studio_settings import reset_usage

        reset_usage(project)
        from studio_isolation import apply_project_isolation

        siblings, _ignore, _rule = apply_project_isolation(project)
        print_header(f"FOCUS: {project}")
        print("\n" + build_focus_report(project, status))
        if siblings:
            print(f"\n  ISOLATION: sibling trees hidden from the agent: {', '.join(siblings)}")
            print("  Do not Read, copy, or git those folders into this project.")
        else:
            print("\n  ISOLATION: no sibling projects under projects/")
        print(f"\n  Active context saved: .quinsy-studio/.active-project.json")
        return True

    def cmd_isolate(self, project: str):
        """Hide sibling project trees from the IDE agent (also runs on focus)."""
        project_dir = PROJECTS_DIR / project
        if not project_dir.exists():
            print(f"\n  ❌ Project '{project}' not found.")
            return False
        from studio_isolation import apply_project_isolation

        siblings, ignore, rule = apply_project_isolation(project)
        print_header(f"ISOLATE: {project}")
        print(f"\n  Active tree: projects/{project}/")
        if siblings:
            print(f"  Hidden: {', '.join('projects/' + s + '/' for s in siblings)}")
        else:
            print("  Hidden: (no siblings)")
        print(f"  Cursor ignore: {ignore}")
        print(f"  Agent rule:    {rule}")
        print("  Git: only `git -C projects/{p} …` — never add a sibling into this repo.".format(p=project))
        return True

    def cmd_guard(self, project: str, request: str):
        """Check if a user request is in project/sprint scope."""
        status = load_status(project)
        verdict, message = guard_request(project, request, status)
        icons = {
            "in_scope": "✅",
            "inbox_ack": "📥",
            "abort": "🛑",
            "needs_ticket": "🎫",
            "pre_impl": "⏸",
            "sprint_review": "⏸",
            "sprint_closed": "⏸",
            "autonomous_sprint": "🤖",
            "feedback_only": "📝",
            "studio_meta": "🏢",
            "cross_project": "🚧",
            "unclear": "❓",
        }
        print_header(f"GUARD: {project}")
        print(f"\n  {icons.get(verdict, '•')} {verdict.upper()}")
        print(f"  {message}")
        if verdict == "inbox_ack":
            print(f"  Continue the current ACTION — do not start a new task.")
        if verdict == "cross_project":
            print("  Stay in this project tree. Switch products with ./studio focus <other>.")
        return verdict in {"in_scope", "inbox_ack"}

    def cmd_verify_worlds(self):
        """Verify studio git and project git are separated."""
        ok, issues = verify_worlds()
        print_header("VERIFY WORLDS")
        if ok:
            print("\n  ✅ Studio HQ and project repos are separated correctly.")
        else:
            print("\n  ❌ Issues found:")
            for issue in issues:
                print(f"    • {issue}")
            print("\n  See: .quinsy-studio/process/worlds.md")
        if not (STUDIO_ROOT / "node_modules").is_dir():
            print("\n  ⚠️  Studio UI dependencies not installed — run: ./studio install")
        return ok

    def cmd_verify_abstraction(self):
        """Scan studio HQ for project-specific names in docs/tools/templates."""
        ok, issues = verify_studio_abstraction()
        print_header("VERIFY STUDIO ABSTRACTION")
        if ok:
            print("\n  ✅ Studio HQ docs/tools are project-agnostic.")
        else:
            print("\n  ❌ Project-specific references found:")
            for issue in issues[:40]:
                print(f"    • {issue}")
            if len(issues) > 40:
                print(f"    … and {len(issues) - 40} more")
            print("\n  See: .quinsy-studio/process/studio-abstraction.md")
        return ok

    def cmd_install(self, with_skills: bool = False):
        """Install studio HQ dependencies after git clone (npm + optional external skills)."""
        import shutil
        import subprocess

        print_header("STUDIO INSTALL")
        pkg = STUDIO_ROOT / "package.json"
        if not pkg.exists():
            print("\n  ❌ package.json not found at repo root")
            return False
        if not shutil.which("npm"):
            print("\n  ❌ npm not found. Install Node.js 20+ (https://nodejs.org/)")
            return False

        print("\n  Installing npm dependencies (tailwindcss, @headlessui/react)…")
        try:
            subprocess.run(
                ["npm", "install"],
                cwd=STUDIO_ROOT,
                check=True,
            )
        except subprocess.CalledProcessError:
            print("\n  ❌ npm install failed")
            return False

        print("\n  ✅ npm dependencies installed")
        print(f"     {STUDIO_ROOT / 'node_modules'}")

        if with_skills:
            print("\n  Importing external skill packages…")
            self.cmd_update_skills([])
        else:
            print("\n  Optional: ./studio install --with-skills  (external skill packages)")
            print("  UI reference: .quinsy-studio/studio-library/ui/docs/README.md")
        return True

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
                stub = " [STUB — not pullable]" if asset.get("stub") else ""
                print(f"  [{asset.get('kind', '?')}] {asset.get('name')} v{ver}{stub} — {asset.get('path', '')}")
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
                extra = f" — {item.get('reason')}" if item.get("reason") else f" ({item.get('kind', '')})"
                print(f"  {st}: {item.get('name')}{extra}")
            print(f"\n  Log: projects/{project}/docs/library-usage.json")
            if result.get("kit_peer_hint"):
                print(f"\n  {result['kit_peer_hint']}")
                for rel in result.get("kit_package_json_updated") or []:
                    print(f"  merged kit peers → {rel} (run npm install in that app)")
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
        from studio_adopt import looks_like_application_source

        project_dir = PROJECTS_DIR / project
        if project_dir.exists() and looks_like_application_source(project_dir):
            print(f"\n  ❌ '{project}' already has application source.")
            print(f"     Do not run empty init. Overlay studio docs:")
            print(f"       ./studio adopt {project} --from {project_dir}")
            return False
        init_project(project, archetype)
        print(f"\n  Next steps:")
        print(f"    1. Process intake: ./studio intake {project} intake/<your-prd>.md")
        print(f"    2. Start project:  ./studio start {project} --mode core")
        return True
    
    def cmd_start(self, project: str, mode: str = "core"):
        """Start a project in the selected mode."""
        
        status = load_status(project)
        if status.get("mode") == "adopt":
            print_header(f"START PROJECT: {project} (Mode: ADOPT)")
            print("  Existing codebase — do not switch to CORE empty-scaffold.")
            print("  See .quinsy-studio/process/brownfield-adopt.md")
            print(f"  Loop: ./studio execute {project}")
            return True
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
        hitl = status.get("sprint_hitl", {})
        if hitl.get("review_status"):
            print(f"  Sprint review: {hitl.get('review_status')}")
        sprint = status.get("current_sprint")
        if sprint:
            summary = sprint_ticket_summary(project, sprint)
            print(f"  Sprint progress: {summary['done']}/{summary['total']} done")
            if summary["all_done"] and hitl.get("review_status") != "approved":
                print(f"  ⏸ Human sprint review pending: ./studio review {project}")
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

        if status.get("mode") == "adopt":
            print(f"\n  AI: fill docs/architecture/ from **as-is** (cite paths). ADRs for decisions already in the code.")
            print("  Do not invent a greenfield stack swap unless the intent brief asks for it.")
        else:
            print(f"\n  AI: fill docs/architecture/ and docs/adr/")
        print(f"  Human: ./studio approve {project} --gate 1 when ready")
        return True

    # -------------------------------------------------------------------------
    # PHASE 2b: DESIGN (prototype + sticker sheet)
    # -------------------------------------------------------------------------

    def cmd_design(self, project: str, scope: str = "core-views"):
        """Scaffold design docs + Next.js prototype. scope: journey | core-views | as-built"""
        status = load_status(project)
        hg = status.get("human_gates", {})

        if hg.get("1", {}).get("status") != "approved":
            print(f"  ⚠️  Gate 1 (architecture) must be approved first")
            return False

        if status.get("mode") == "adopt":
            from studio_adopt import overlay_studio

            print_header(f"PHASE 3: DESIGN TRUTH — {project} (as-built)")
            overlay_studio(PROJECTS_DIR / project, project, archetype=status.get("archetype") or "saas-application")
            status["phase"] = PHASE_DESIGN
            status["design_scope"] = "as-built"
            save_status(project, status)
            print("  Document existing UI in design/DESIGN.md and docs/ia/surface-map.md")
            print("  Do NOT scaffold design/prototype as a parallel app")
            print(f"  Human: ./studio approve {project} --gate 2 when the surface map is honest")
            return True

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
        print(f"  UI kit:     radix-ui class-variance-authority clsx tailwind-merge lucide-react @headlessui/react (in prototype package.json)")
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
            if status.get("mode") == "adopt":
                print(f"  Next: ./studio blueprint {project}  (as-is architecture; no stack swap)")
            else:
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
            if status.get("mode") == "adopt":
                print(f"  Next: fill design truth of existing UI (no new prototype)")
                print(f"        ./studio design {project} --scope as-built")
            else:
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

            if status.get("mode") == "adopt":
                print(f"\n  ✅ Design of what exists approved")
                print("  Do not copy project UI into studio-library.")
                print(f"  Next: draft docs/phases/ from as-built gap matrix")
                print(f"        ./studio approve {project} --milestones")
                return True

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

    def cmd_approve_amendment(self, project: str, am_id: str, prd_tier: bool = False) -> bool:
        """Human sign-off on a analyzed amendment."""
        print_header(f"AMENDMENT APPROVAL — {project} ({am_id})")
        ok, msg = approve_amendment(project, am_id.upper(), prd_tier=prd_tier)
        print(f"\n  {msg}")
        if ok:
            status = load_status(project)
            if "amendments" not in status:
                status["amendments"] = {}
            status["amendments"]["last_approved"] = am_id.upper()
            status["amendments"]["last_approved_at"] = datetime.now().isoformat()
            save_status(project, status)
        return ok

    def cmd_approve_milestones(self, project: str) -> bool:
        """Approve milestone roadmap (initial or post-amendment revision)."""
        print_header(f"MILESTONE ROADMAP APPROVAL — {project}")
        ok, msg = approve_milestones(project)
        print(f"\n  {msg}")
        if ok:
            status = load_status(project)
            status.setdefault("human_gates", {})
            status["human_gates"]["milestones"] = {
                "status": "approved",
                "date": datetime.now().isoformat(),
            }
            save_status(project, status)
        return ok

    def cmd_amend(self, project: str, input_file: str, force: bool = False) -> bool:
        """Scaffold amendment analysis artifacts from intake brief."""
        project_dir = PROJECTS_DIR / project
        if not project_dir.exists():
            print(f"\n  ❌ Project '{project}' not found.")
            return False

        status = load_status(project)
        if not gate2_approved(status):
            print(f"\n  ⚠️  Gate 2 (design) must be approved before amendment intake.")
            print(f"     Current phase: {status.get('phase')} gate: {status.get('gate')}")
            return False

        source = resolve_amendment_file(project, input_file)
        if not source:
            print(f"\n  ❌ Amendment brief not found: {input_file}")
            print(f"     Drop at intake/amendments/{project}/amendment_NN.md")
            return False

        print_header(f"AMENDMENT INTAKE — {project}")
        print(f"  Source: {amendment_path_for_cli(source)}")

        ok, result, meta = scaffold_amendment(project, source, force=force)
        if not ok:
            print(f"\n  ❌ {result}")
            return False

        rel = (PROJECTS_DIR / project / "docs" / "amendments" / result).relative_to(
            PROJECTS_DIR / project
        )
        print(f"\n  ✅ {meta['id']} scaffolded → {rel}")
        if meta.get("warnings"):
            print("\n  Warnings:")
            for w in meta["warnings"]:
                print(f"    • {w}")
        print(f"\n  Teams checked: {len(meta.get('teams_checked', []))}")
        print(f"  Skills checked: {len(meta.get('skills_checked', []))}")
        print(f"\n  AI: fill artifacts in docs/amendments/{result}/ (see AGENT.md)")
        print(f"  Human: review → ./studio approve {project} --amendment {meta['id']}")
        if meta.get("id"):
            print(f"  If roadmap changes: ./studio approve {project} --milestones")
        return True

    def cmd_amendments(self, project: str) -> bool:
        """List amendment registry for a project."""
        print_header(f"AMENDMENTS — {project}")
        print(f"\n{format_amendments_list(project)}")
        pending = pending_amendments(project)
        if pending:
            print(f"\n  ⏸ {len(pending)} pending — complete analysis + human approve before next milestone")
        return True
    
    # -------------------------------------------------------------------------
    # PHASE 3: SPRINT MANAGEMENT
    # -------------------------------------------------------------------------
    
    def cmd_sprint(self, project: str, approve_scope: bool = False):
        """Propose or approve sprint scope from product backlog."""
        
        status = load_status(project)
        ensure_backlog_layout(project)
        migrated = migrate_legacy_backlog(project)
        if migrated:
            print(f"  ℹ️  Migrated legacy backlog folders → backlog/ ({len(migrated)} file(s))")
        
        if approve_scope:
            sprint = status.get("current_sprint")
            if not sprint:
                print(f"  ⚠️  No active sprint — run ./studio sprint {project} first")
                return False
            reuse_msg = reuse_gate_message(project, status)
            if reuse_msg:
                print(f"\n  ⚠️  Cannot approve sprint scope until reuse review is complete.")
                print(f"  {reuse_msg}")
                return False
            proposal = load_scope_proposal(project, sprint)
            if not proposal:
                print(f"  ⚠️  No scope proposal for {sprint} — run ./studio sprint {project}")
                return False
            print_header(f"APPROVE SPRINT SCOPE — {project} ({sprint})")
            proposed = proposal.get("proposed") or []
            tagged, missing = apply_sprint_scope(project, sprint, proposal)
            if proposed and missing:
                print(f"\n  ❌ Scope approve blocked — {len(missing)} proposed ticket(s) not in backlog/:")
                for tid in missing:
                    print(f"    • {tid}")
                print("  Fix: ensure tickets exist under backlog/, or re-run ./studio sprint to refresh scope-proposal.json")
                print("  (Editing scope-proposal.md alone does not update the JSON used by --approve-scope.)")
                return False
            if proposed and tagged == 0:
                print(f"\n  ❌ Scope approve blocked — 0/{len(proposed)} ticket(s) tagged (empty sprint).")
                print("  Fix: check scope-proposal.json matches intended tickets, then retry --approve-scope.")
                return False
            hitl = get_sprint_hitl(status)
            hitl["scope_status"] = "approved"
            hitl["scope_approved_at"] = datetime.now().isoformat()
            hitl["groom_status"] = "pending"
            save_status(project, status)
            validation = validate_sprint_backlog(project, sprint)
            report = write_validation_report(project, validation)
            print(f"\n  ✅ Sprint scope approved — {tagged} ticket(s) tagged")
            print(f"  Scope: {report.relative_to(PROJECTS_DIR / project)}")
            print(format_validation_brief(validation))
            print(f"\n  Next: ./studio groom {project} --approve")
            return True
        
        phase = str(status.get("phase", ""))
        sprint_phases = {PHASE_SPRINT, PHASE_IMPLEMENT, "4", "5"}
        milestone_phase = phase.isdigit() and int(phase) >= 4
        if phase not in sprint_phases and not milestone_phase:
            print(f"  ⚠️  Sprint requires design approval (gate 2). Current phase: {phase}")
            return False
        
        if status.get("human_gates", {}).get("2", {}).get("status") != "approved":
            print(f"  ⚠️  Gate 2 (design) must be approved before sprint")
            return False

        ok, reason = can_plan_next_sprint(project, status)
        if not ok:
            print(f"\n  ⚠️  Cannot plan next sprint yet.")
            print(f"  {reason}")
            return False
        
        print_header(f"PHASE 3: SPRINT PLANNING — {project}")
        
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
        
        proposal = propose_sprint_scope(project, sprint_name)
        scope_file = write_scope_proposal(project, sprint_name, proposal)
        questions_file = write_planning_questions_report(project, sprint_name, proposal)
        proposed = proposal["proposed"]
        
        rows = "\n".join(
            f"| {t['id']} | {t['title'][:40]} | {t['phase']} | {t['priority']} | {t['estimate']} |"
            for t in proposed
        ) or "| (pending approval) | — | — | — | — |"
        plan_file = sprint_dir / "plan.md"
        plan_template = f"""# Sprint Plan — {sprint_name}

**Project:** {project}
**Goal:** _Edit after scope approval_
**Start:** {datetime.now().strftime('%Y-%m-%d')}
**End:** YYYY-MM-DD
**Capacity:** {len(proposed)} tickets proposed (scope pending)

## Tickets in this sprint

| Ticket | Title | Phase | Priority | Estimate |
|--------|-------|-------|----------|----------|
{rows}

> **Scope not final** until `./studio sprint {project} --approve-scope`

## Dependencies
- ...

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

        print(format_planning_brief(proposal))
        rel_scope = scope_file.relative_to(PROJECTS_DIR / project)
        print(f"\n  Scope proposal: {rel_scope}")
        if questions_file:
            rel = questions_file.relative_to(PROJECTS_DIR / project)
            print(f"  Immature tickets: {rel}")

        status["current_sprint"] = sprint_name
        status["phase"] = PHASE_IMPLEMENT
        hitl = get_sprint_hitl(status)
        hitl["review_status"] = None
        hitl["review_pending_since"] = None
        hitl["retro_status"] = None
        hitl["retro_completed_at"] = None
        hitl["reuse_status"] = None
        hitl["reuse_sprint"] = None
        hitl["reuse_pending_since"] = None
        hitl["reuse_approved_at"] = None
        hitl["scope_status"] = "pending"
        hitl["scope_approved_at"] = None
        hitl["groom_status"] = None
        save_status(project, status)

        print(f"\n  Sprint created: {sprint_name} (scope **pending**)")
        print(f"  Human steps:")
        print(f"    1. Read {rel_scope}")
        print(f"    2. Edit sprints/{sprint_name}/plan.md goal if needed")
        print(f"    3. ./studio sprint {project} --approve-scope")
        print(f"    4. ./studio groom {project} --approve")
        
        return True
    
    def cmd_review(self, project: str, approve: bool = False, reject: bool = False,
                   notes: str = "", reason: str = ""):
        """Prepare or complete a human sprint review."""
        status = load_status(project)
        sprint = status.get("current_sprint")
        if not sprint:
            print(f"  ⚠️  No active sprint — run ./studio sprint {project}")
            return False

        print_header(f"SPRINT REVIEW — {project} ({sprint})")

        if approve:
            summary = sprint_ticket_summary(project, sprint)
            if summary["total"] == 0 or not summary["all_done"]:
                print(f"\n  ❌ Cannot approve review — sprint tickets are not all done (LO-0025).")
                print(f"     Progress: {summary['done']}/{summary['total']} done")
                for ticket in summary["tickets"]:
                    if ticket.get("status") != "done":
                        print(f"     • {ticket['id']}: {ticket.get('status')} — {ticket.get('title', '')}")
                print(f"  Finish remaining tickets, then ./studio review {project} → human --approve")
                return False
            if not notes:
                notes = "Human approved sprint deliverables."
            approve_review(project, sprint, status, notes)
            save_status(project, status)
            print(f"\n  ✅ Sprint review approved")
            print(f"  Implementation frozen until the next sprint is planned.")
            print(f"  Next:")
            print(f"    ./studio reuse {project}  (inform brief — not a gate)")
            print(f"    ./studio retro {project}")
            print(f"  Then:")
            print(f"    ./studio feedback {project} \"...\"  (capture new ideas)")
            print(f"    ./studio clarify {project} FB-001 ... --approve")
            print(f"    ./studio ticket {project} \"...\" --from-feedback FB-001")
            print(f"    ./studio groom {project}")
            print(f"    ./studio retro {project}")
            print(f"    ./studio sprint {project}  (plan next sprint)")
            return True

        if reject:
            if not reason.strip():
                print(f"  ⚠️  --reject requires --reason \"...\"")
                return False
            reject_review(project, sprint, status, reason)
            save_status(project, status)
            print(f"\n  ❌ Sprint review rejected")
            print(f"  Logged in sprints/{sprint}/review.md")
            print(f"  Re-open or create tickets, then ./studio review {project} --prepare")
            return True

        review_file = prepare_review(project, sprint, status)
        save_status(project, status)
        summary = sprint_ticket_summary(project, sprint)

        print(f"\n  Review brief: {review_file}")
        print(f"  Progress: {summary['done']}/{summary['total']} tickets done")
        if summary["all_done"]:
            print(f"\n  ⏸ All sprint tickets done — human review required")
        print(f"\n  Human steps:")
        print(f"    1. Read {review_file.relative_to(STUDIO_ROOT)}")
        print(f"    2. Try the project (RUNBOOK / prototype)")
        print(f"    3. ./studio feedback {project} \"your ideas\"  (agent: capture only — never implement)")
        print(f"    4. ./studio review {project} --approve [--notes \"...\"]")
        print(f"       or: ./studio review {project} --reject --reason \"...\"")
        return True

    def cmd_reuse(
        self,
        project: str,
        approve: bool = False,
        record_path: str = "",
        record_action: str = "",
        record_ref: str = "",
        record_note: str = "",
        notes: str = "",
    ):
        """Mandatory library reuse review after sprint review approval."""
        status = load_status(project)
        sprint = resolve_reuse_sprint(project, status)
        if not sprint:
            hitl = get_sprint_hitl(status)
            if hitl.get("review_status") != REVIEW_APPROVED:
                print(f"  ⚠️  Reuse review runs after ./studio review {project} --approve")
                return False
            print(f"  ✅ No sprint pending reuse review")
            return True

        print_header(f"REUSE REVIEW — {project} ({sprint})")

        if record_path and record_action:
            try:
                record_reuse_decision(
                    project, sprint, record_path, record_action,
                    ref=record_ref, note=record_note,
                )
                print(f"\n  ✅ Recorded: {record_path} → {record_action}")
            except ValueError as exc:
                print(f"  ⚠️  {exc}")
                return False
            md_path, data = prepare_reuse_review(project, sprint, status)
            ok, _reason, data = approve_reuse_review(
                project, sprint, status, notes="inform-auto after --record",
            )
            if ok:
                save_status(project, status)
                print(f"\n  ✅ Reuse inform complete for {sprint} (paths resolved — no --approve)")
            print(format_reuse_brief(project, {**data, "ticket_count": len(data.get('items', []))}))
            print(f"\n  Report: {md_path.relative_to(STUDIO_ROOT)}")
            return True

        if approve:
            ok, reason, _data = approve_reuse_review(project, sprint, status, notes=notes)
            if not ok:
                print(f"\n  ⚠️  Cannot approve reuse review yet.")
                print(f"  {reason}")
                print(f"\n  Record decisions:")
                print(f"    ./studio reuse {project} --record <path> promote --ref TICKET-0026")
                print(f"    ./studio reuse {project} --record ui/components/foo local --note \"project-specific\"")
                print(f"    ./studio library promote {project} packages/auth --ticket TICKET-0026 --force")
                return False
            save_status(project, status)
            print(f"\n  ✅ Reuse review approved for {sprint}")
            print(f"  Next:")
            print(f"    ./studio retro {project}")
            print(f"    ./studio sprint {project}")
            return True

        md_path, data = prepare_reuse_review(project, sprint, status)
        hitl = get_sprint_hitl(status)
        hitl["reuse_status"] = hitl.get("reuse_status") or "pending"
        hitl["reuse_sprint"] = sprint
        save_status(project, status)

        from studio_harvest import harvest_reuse_items

        harvested = harvest_reuse_items(data.get("items") or [], f"{project}/{sprint}")
        recorded = False
        for item in harvested:
            path = str(item.get("path") or "")
            lo_id = str(item.get("lo_id") or "")
            if not path or not lo_id:
                continue
            record_reuse_decision(
                project,
                sprint,
                path,
                "lo_ticket",
                ref=lo_id,
                note="auto-harvest",
            )
            recorded = True
            created = "created" if item.get("created") else "existing"
            print(
                f"  Harvested {lo_id} [{created}] {item.get('kind')} → {item.get('infusion_path')} ({path})"
            )
        if recorded:
            md_path, data = prepare_reuse_review(project, sprint, status)

        ok, _reason, data = approve_reuse_review(
            project, sprint, status, notes="inform-auto when paths resolved",
        )
        if ok:
            save_status(project, status)
            print(f"\n  ✅ Reuse inform complete for {sprint} (paths resolved — no --approve)")

        analysis_ticket_count = len([
            t for t in sprint_ticket_summary(project, sprint)["tickets"] if t["status"] == "done"
        ])
        print(format_reuse_brief(project, {**data, "ticket_count": analysis_ticket_count}))
        print(f"\n  Report: {md_path.relative_to(STUDIO_ROOT)}")
        print(f"\n  Agent: promote only if the generic asset improved; otherwise leave the project copy.")
        print(f"  Inform only — no ./studio reuse --approve required.")
        return True

    def cmd_feedback(self, project: str, text: str, source: str = "sprint-review", force: bool = False):
        """Capture raw human feedback — does not create a ticket."""
        status = load_status(project)
        sprint = status.get("current_sprint")
        if not sprint:
            print(f"  ⚠️  No active sprint — run ./studio sprint {project}")
            return False
        if not text.strip():
            print(f"  ⚠️  Feedback text is required")
            return False

        print_header(f"FEEDBACK — {project} ({sprint})")
        fb_id, md_file, is_duplicate = add_feedback(project, sprint, text, source, force=force)
        if is_duplicate:
            print(f"\n  ⚠️  Similar feedback already captured as {fb_id} — not creating a duplicate.")
            print(f"  File: {md_file}")
            print(f"  Update existing item:")
            print(f"    ./studio clarify {project} {fb_id} --title \"...\" --scope \"...\" --acceptance \"...\"")
            print(f"  Or force a separate item: ./studio feedback {project} \"...\" --force")
            return True

        print(f"\n  Captured {fb_id} (status: raw — NOT a ticket)")
        print(f"  File: {md_file}")
        print(f"\n  ⛔ DO NOT implement this in project code during sprint review.")
        print(f"     Flow: clarify → ticket --from-feedback → **backlog** → ./studio sprint assigns.")
        print(f"\n  Next:")
        print(f"    ./studio clarify {project} {fb_id} --title \"...\" --scope \"...\" --acceptance \"...\"")
        print(f"    ./studio clarify {project} {fb_id} --approve")
        print(f"    ./studio ticket {project} \"<title>\" --from-feedback {fb_id}")
        return True

    def cmd_feedback_list(self, project: str):
        """List feedback queue for current sprint."""
        status = load_status(project)
        sprint = status.get("current_sprint")
        if not sprint:
            print(f"  ⚠️  No active sprint")
            return False
        print_header(f"FEEDBACK QUEUE — {project} ({sprint})")
        print(format_feedback_list(project, sprint))
        print(f"\n  Flow: feedback → clarify → --approve → ticket --from-feedback")
        return True

    def cmd_clarify(
        self,
        project: str,
        fb_id: str,
        title: str = "",
        scope: str = "",
        out_of_scope: str = "",
        acceptance: Optional[List[str]] = None,
        approve: bool = False,
    ):
        """Clarify raw feedback into an executable ticket draft."""
        status = load_status(project)
        sprint = status.get("current_sprint")
        if not sprint:
            print(f"  ⚠️  No active sprint")
            return False

        print_header(f"CLARIFY FEEDBACK — {fb_id}")
        try:
            item, clarify_file = clarify_feedback(
                project, sprint, fb_id,
                title=title,
                scope=scope,
                out_of_scope=out_of_scope,
                acceptance=acceptance or [],
                approve=approve,
            )
        except ValueError as e:
            print(f"  ⚠️  {e}")
            return False

        if not item:
            print(f"  ⚠️  {fb_id} not found — ./studio feedback-list {project}")
            return False

        print(f"\n  Status: {item['status']}")
        print(f"  Draft: {clarify_file}")
        if item["status"] == "ready":
            print(f"\n  ✅ Ready for ticket:")
            print(f"    ./studio ticket {project} \"{item.get('draft_title')}\" --from-feedback {fb_id}")
        elif approve:
            print(f"  ⚠️  Could not approve — check draft_title and acceptance criteria")
        else:
            print(f"\n  Add fields, then: ./studio clarify {project} {fb_id} --approve")
        return True

    def cmd_ticket(self, project: str, title: str, phase: int = 4, 
                   priority: str = "P1", estimate: str = "M", from_feedback: str = ""):
        """Create a new ticket in the project backlog (strict studio schema)."""
        
        status = load_status(project)
        sprint = status.get("current_sprint", "")
        fb_item = None
        if from_feedback:
            if not sprint:
                print(f"  ⚠️  --from-feedback requires an active sprint")
                return False
            try:
                fb_item = get_ready_feedback_for_ticket(project, sprint, from_feedback)
            except ValueError as e:
                print(f"  ⚠️  {e}")
                return False
            title = fb_item.get("draft_title") or title
            if not title.strip():
                print(f"  ⚠️  Title required (or set via clarify --title)")
                return False

        ticket_id = get_next_ticket_id(project)
        slug = slugify(title)
        
        ticket_dir = get_project_backlog_dir(project, QUEUE_STATUS)
        ticket_file = ticket_dir / f"{ticket_id}-{slug}.md"
        
        skills = match_skills(title)
        infer_blob = title
        if fb_item:
            infer_blob = "\n".join(
                [
                    title,
                    str(fb_item.get("draft_scope") or ""),
                    str(fb_item.get("raw") or ""),
                    str(fb_item.get("draft_title") or ""),
                ]
            )
        ticket_type = infer_ticket_type(infer_blob)
        if ticket_type.startswith("ui-") or ticket_type in (
            "marketing-page",
            "workflow-explainer",
            "ia-navigation",
            "ia-feature-placement",
        ):
            skills = enrich_design_skills(skills, ticket_type, infer_blob)
            team = team_for_skills(skills)
        else:
            team = team_for_skills(skills)
        role = role_for_skills(skills)
        design_status = "pending" if requires_design_approval(
            f"ticket_type: {ticket_type}\n{infer_blob}"
        ) else "n/a"
        design_spec = default_design_spec_path(ticket_id) if design_status == "pending" else ""

        acceptance = [
            f"'{title}' is implemented",
            f"'{title}' has tests",
            "Code is free of AI slop",
        ]
        rationale_extra = ""
        draft_scope = ""
        draft_oos = ""
        if fb_item:
            acceptance = fb_item.get("draft_acceptance") or acceptance
            draft_scope = (fb_item.get("draft_scope") or "").strip()
            draft_oos = (fb_item.get("draft_out_of_scope") or "").strip()
            rationale_extra = (
                f"\n\n## Source feedback\n"
                f"- **{from_feedback.upper()}:** {fb_item.get('raw', '')}\n"
            )
        
        ticket = {
            "id": ticket_id,
            "title": title,
            "type": ticket_type if ticket_type != "feature" else "feature",
            "status": "backlog",
            "phase": phase,
            "priority": priority,
            "estimate": estimate,
            "team": team,
            "skills": skills,
            "ist_zustand": f"The feature '{title}' does not exist yet in `projects/{project}/`.",
            "soll_zustand": f"The feature '{title}' is implemented and usable.",
            "value": draft_scope or f"'{title}' delivers visible progress in project {project}.",
            "out_of_scope": draft_oos,
            "modification_files": [f"projects/{project}/"],
            "constraints": [
                "Do not install unnecessary external packages without an ADR",
                "Follow the anti-slop protocol (no clichés, no god functions)",
                "Load the assigned skill files (see `skills`)"
            ],
            "scenarios": [] if (fb_item and fb_item.get("draft_acceptance")) else [{
                "name": "Feature is usable",
                "given": f"A user in project {project}",
                "when": f"They use the feature '{title}'",
                "then": f"'{title}' works as described and is tested"
            }],
            "acceptance_criteria": acceptance,
            "definition_of_done": [
                "Feature works (BDD scenario green)",
                "Tests present and green",
                "Anti-slop audit: 0 violations",
                "QA gate green (`./studio gate <project> --level 5`)"
            ],
            "dependencies": []
        }
        if design_status != "n/a":
            ticket["ticket_type"] = ticket_type
            ticket["design_status"] = design_status
            ticket["design_spec"] = design_spec
        
        content = render_ticket_markdown(ticket)
        if rationale_extra:
            content += rationale_extra
        ticket_file.write_text(content)

        if fb_item and sprint:
            link_feedback_to_ticket(project, sprint, from_feedback, ticket_id)
        
        print(f"\n  Ticket created: {ticket_file}")
        print(f"  ID: {ticket_id}")
        if from_feedback:
            print(f"  From feedback: {from_feedback.upper()}")
            print(f"  Backlog: unscheduled (no sprint tag) — assigned at ./studio sprint {project}")
        print(f"  Role: {role}")
        print(f"  Team: {team}")
        print(f"  Skills: {', '.join(skills) if skills else '(auto-match)'}")
        if design_status == "pending":
            spec_file = write_design_spec_stub(
                PROJECTS_DIR / project, ticket_id, design_spec
            )
            print(f"  Ticket type: {ticket_type}")
            print(f"  Design spec stub: {spec_file} — fill it (do not approve-design until filled + mocks)")
        print(f"  Status: open")
        print(f"  Project: {project}")
        print(f"\n  Next step:")
        print(f"    ./studio groom {project}  (prioritize before implement)")
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

        if new_status == "done":
            status_pre = load_status(project)
            gate_level = int(str(status_pre.get("gate", "0") or "0"))
            gate_status = status_pre.get("gate_status")
            if gate_status != "passed" or gate_level < MIN_DONE_GATE_LEVEL:
                print(
                    f"\n  ❌ Cannot mark {ticket_id} done without QA gate level {MIN_DONE_GATE_LEVEL} green."
                )
                print(f"     Current: gate={gate_level}, status={gate_status}")
                print(f"     Run: ./studio gate {project} --level {MIN_DONE_GATE_LEVEL}")
                return False
            sprint_pre = status_pre.get("current_sprint") or ""
            content_pre = ticket_file.read_text()
            sprint_match = re.search(r"^sprint:\s*(\S+)", content_pre, re.MULTILINE)
            ticket_sprint = sprint_match.group(1) if sprint_match else None
            if sprint_pre and ticket_sprint == sprint_pre:
                if not receipt_is_complete(project, sprint_pre, ticket_id):
                    rec = receipt_path(project, sprint_pre, ticket_id)
                    print(f"\n  ❌ Cannot mark {ticket_id} done without an execution receipt.")
                    print(f"     Fill: {rec.relative_to(STUDIO_ROOT)}")
                    print(f"     ./studio receipt {project} {ticket_id}")
                    print("     Required sections: Plan, AC coverage, Default flow (LO-0051)")
                    return False

        if new_status == "implement":
            status_pre = load_status(project)
            blocked = implement_blocked_reason(status_pre, project)
            if blocked:
                print(blocked)
                return False
            content_pre = ticket_file.read_text()
            d_status, d_msg = design_deliverables_status(
                PROJECTS_DIR / project, ticket_id, content_pre
            )
            if d_status == "write":
                print(d_msg)
                return False
            if d_status == "approve":
                print(design_implement_blocked_message(ticket_id, content_pre))
                return False
        
        # Determine new directory (within project)
        new_dir = get_project_backlog_dir(project, new_status)
        new_file = new_dir / ticket_file.name
        
        # Update ticket content
        content = ticket_file.read_text()
        content = content.replace(f"status: {current_status}", f"status: {new_status}", 1)
        content += f"\n\n## Status Change\n- **From:** {current_status}\n- **To:** {new_status}\n- **Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n- **Reason:** {reason}\n"
        
        # LO-0047: same-path move (e.g. already implement → implement) must not unlink
        # after write — Path.unlink() would delete the ticket we just wrote.
        same_path = ticket_file.resolve() == new_file.resolve()
        new_file.write_text(content)
        if not same_path:
            ticket_file.unlink()
        
        print(f"\n  Ticket {ticket_id}: {current_status} → {new_status}")
        print(f"  Project: {project}")
        if reason:
            print(f"  Reason: {reason}")
        if same_path and current_status == new_status:
            print(f"  (same status — ticket updated in place, not moved)")

        status = load_status(project)
        title_match = re.search(r"^title:\s*(.+)$", content, re.MULTILINE)
        ticket_title = title_match.group(1).strip() if title_match else ticket_id

        if new_status == "implement":
            from studio_status import load_snapshots, save_snapshots

            snapshots = load_snapshots(project)
            snapshots[ticket_id] = snapshot_registry_files(project)
            save_snapshots(project, snapshots)
            status["active_ticket"] = ticket_id
            save_status(project, status)
            print(f"\n  📚 {format_library_first_hint(project, ticket_title)}")
            sprint_now = status.get("current_sprint") or ""
            if sprint_now:
                append_execution_event(project, sprint_now, "implement", ticket_id, reason or "implement")
                print(f"  Next: ./studio receipt {project} {ticket_id}  then implement from the CARD, then ./studio execute {project}")

        if new_status == "done":
            from studio_status import snapshot_for_ticket

            snap = snapshot_for_ticket(project, ticket_id, status)
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
            if maybe_flag_sprint_review(project, status):
                sprint = status.get("current_sprint", "")
                print(f"\n  ⏸ All sprint tickets done — UI sprint review required")
                print(f"    ./studio review {project}")
            else:
                hitl_now = get_sprint_hitl(status)
                if hitl_now.get("review_status") == "informed":
                    print(f"\n  Backend-only sprint complete — review is inform-only. Next: ./studio retro {project}")
            save_status(project, status)
            sprint_done = status.get("current_sprint") or ""
            if sprint_done:
                append_execution_event(project, sprint_done, "done", ticket_id, reason or "done")
                print(f"  Loop: ./studio execute {project}")
        
        # If moving to done, check if all tickets are done
        if new_status == "done":
            project_backlog = PROJECTS_DIR / project / "backlog"
            open_dir = project_backlog / "open"
            if open_dir.exists():
                open_tickets = list(open_dir.glob(f"{project[:4].upper()}-*.md"))
                if not open_tickets and not needs_sprint_review(status):
                    print(f"\n  🎉 All open backlog tickets completed!")
                    print(f"  Next step:")
                    print(f"    ./studio review {project}")
                    print(f"    ./studio gate {project} --level 5")
                    print(f"    ./studio retro {project}")
        
        return True

    def cmd_approve_design(self, project: str, ticket_id: str, notes: str = ""):
        """HITL: approve Team 10 spec for design-track (major UX/UI/IA) before FE implement."""
        ticket_file, _status = find_project_ticket(project, ticket_id)
        if not ticket_file:
            print(f"  Ticket {ticket_id} not found in project {project}")
            return False
        content = ticket_file.read_text()
        if not requires_design_approval(content):
            print(f"  Ticket {ticket_id} is not a design-track UI ticket (no design approval needed).")
            return True
        spec_match = re.search(r"^design_spec:\s*(.+)$", content, re.MULTILINE)
        spec_rel = spec_match.group(1).strip() if spec_match else default_design_spec_path(ticket_id)
        spec_path = PROJECTS_DIR / project / spec_rel
        fields = parse_design_fields(content)
        complete_err = design_spec_completeness_error(
            spec_path,
            PROJECTS_DIR / project,
            ticket_id,
            fields.get("ticket_type", ""),
            ticket_blob=content,
        )
        if complete_err:
            print(f"\n  ❌ Cannot approve-design — deliverables incomplete.")
            print(f"    {complete_err}")
            print(
                "    There is nothing to review until the spec and in-context, "
                "token-based, all-state mocks exist."
            )
            return False
        emoji_warn = design_mocks_emoji_icon_warning(PROJECTS_DIR / project, ticket_id)
        if emoji_warn:
            print(f"\n  ⚠️  {emoji_warn}")
        updated = set_design_approved(content)
        if notes:
            updated += f"\n\n## Design approval\n- **Approved:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n- **Notes:** {notes}\n"
        ticket_file.write_text(updated)
        print(f"\n  ✓ Design approved for {ticket_id}")
        print(f"    Spec: {spec_rel}")
        print(f"  Next: ./studio move {project} {ticket_id} implement")
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

        sprint = status.get("current_sprint") or ""
        ticket_id = status.get("active_ticket")
        excerpt = (result.stdout or "")[-1500:]
        if sprint and ticket_id:
            if result.returncode == 0:
                append_execution_event(project, sprint, "gate-pass", ticket_id)
            else:
                log = load_execution_log(project, sprint)
                fails = count_gate_fails(log, ticket_id) + 1
                append_execution_event(project, sprint, "gate-fail", ticket_id, "gate red")
                dbg = append_debug_attempt(
                    project, sprint, ticket_id, fails, f"QA gate level {level} failed", excerpt
                )
                print(f"\n  Debug log: {dbg.relative_to(STUDIO_ROOT)}")
                print(f"  Retry {fails}/{MAX_GATE_RETRIES}: fix from hypotheses, then ./studio gate {project} --level 5")
                if fails >= MAX_GATE_RETRIES:
                    print(f"  Exhausted retries — ./studio move {project} {ticket_id} blocked")
                    if not existing_gate_fail_lo(project):
                        lo_id = self.cmd_learn(
                            f"Gate fail retry exhausted ({ticket_id})",
                            "gate-fail",
                            project,
                        )
                        print(f"  Auto-harvested {lo_id} — spawn ./studio train beside product execute")

        return result.returncode == 0
    
    # -------------------------------------------------------------------------
    # PHASE 6: LEARNING
    # -------------------------------------------------------------------------
    
    def cmd_learn(self, title: str, signal: str, source: str = "Studio Development"):
        """Capture a learning immediately (classified LO + inbox). Execute will STUDIO_LO next."""
        from studio_harvest import harvest_identified_learning

        result = harvest_identified_learning(
            title, source=source, signal=signal, observation=title
        )
        lo_id = result["lo_id"]
        if result.get("created"):
            print(f"\n  Learning captured: {lo_id}")
        else:
            print(f"\n  Learning already open: {lo_id} (deduped)")
        print(f"  Kind: {result.get('kind')} → {result.get('infusion_path')}")
        print(f"  Signal: {result.get('signal')}")
        if result.get("inbox"):
            print(f"  Inbox: .quinsy-studio/{result['inbox']}")
        print("  Harvested. Product execute continues IMPLEMENT; train agent infuses in parallel:")
        print("    ./studio train SO-001 --from mistake --topic \"<gap>\"")
        print("    ./studio execute <project>  → ACTION IMPLEMENT (open LOs do not block)")
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
            signal_match = re.search(r"signal:\s*(\S+)", content)
            kind_match = re.search(r"infusion_kind:\s*(\S+)", content)
            path_match = re.search(r"infusion_path:\s*(.+)", content)
            signal = signal_match.group(1) if signal_match else "unknown"
            kind = kind_match.group(1) if kind_match else ""
            path = path_match.group(1).strip() if path_match else ""
            extra = f" kind={kind}" if kind else ""
            extra += f" → {path}" if path else ""
            print(f"  - {lo.stem} [Signal: {signal}{extra}]")
        print("\n  Next: ./studio execute <project> continues IMPLEMENT; TRAIN sidecar infuses LOs")
    
    def cmd_retro(self, project: str, complete: bool = False):
        """Start or complete a project sprint retrospective."""
        status = load_status(project)
        sprint = status.get("current_sprint", "SPRINT-01")

        print_header(f"RETROSPECTIVE — {project} ({sprint})")

        reuse_msg = reuse_gate_message(project, status)
        if reuse_msg:
            print(f"\n  Reuse brief (inform-only, not a gate):")
            print(f"  {reuse_msg.split(chr(10))[0]}")

        hitl = get_sprint_hitl(status)

        if complete:
            ok, message = complete_retro(project, sprint)
            if not ok:
                print(f"\n  ⚠️  {message}")
                print(f"  Fill: projects/{project}/sprints/{sprint}/retro.md")
                return False
            hitl["retro_status"] = RETRO_DONE
            hitl["retro_completed_at"] = datetime.now().isoformat()
            save_status(project, status)
            print(f"\n  ✅ Retro complete: {message}")
            retro_path = PROJECTS_DIR / project / "sprints" / sprint / "retro.md"
            if retro_path.exists():
                from studio_harvest import harvest_retro_text

                harvested = harvest_retro_text(
                    retro_path.read_text(encoding="utf-8", errors="ignore"), project
                )
                created = [h for h in harvested if h.get("created")]
                skipped = [h for h in harvested if not h.get("created")]
                if created or skipped:
                    print("\n  Harvested into studio HQ (inbox + LO) — not waiting for a human learn prompt:")
                    for h in created:
                        print(
                            f"    {h.get('lo_id')} [{h.get('kind')}] → {h.get('infusion_path')}"
                        )
                    for h in skipped:
                        print(f"    {h.get('lo_id')} already open (deduped)")
            print("  Harvested. Product loop continues; spawn train beside it:")
            print(f"    ./studio execute {project}  → IMPLEMENT (not STUDIO_LO)")
            print(f"    ./studio train SO-001 --from mistake --topic \"retro gap\"")
            return True

        retro_file = prepare_retro(project, sprint)
        hitl["retro_status"] = RETRO_PENDING
        hitl["retro_completed_at"] = None
        save_status(project, status)

        print(f"\n  Project retro scaffold: {retro_file}")
        print(f"  Agent must fill went well / badly / improve (not template-only), then:")
        print(f"    ./studio retro {project} --complete")

        # Studio meta-retro for cross-project learnings (optional)
        meta_dir = QUINSY_STUDIO / "retros"
        meta_dir.mkdir(parents=True, exist_ok=True)
        date_str = datetime.now().strftime("%Y-%m-%d")
        meta_file = meta_dir / f"meta-retro-{date_str}.md"
        if not meta_file.exists():
            meta_file.write_text(
                f"""# Meta-Retro — {date_str}

## Project: {project} ({sprint})
- See: projects/{project}/sprints/{sprint}/retro.md

## Incoming learning items
- (Agent: harvest is automatic on retro --complete / gate-fail / reuse; execute STUDIO_LO immediately)

## Action Items
- [ ] Agent filled project retro (went well / badly / improve) — not template-only
- [ ] Meta-retro updated with cross-project learnings
- [ ] LO tickets created or closed for actionable items
"""
            )
            print(f"  Studio meta-retro (if needed): {meta_file}")

        return retro_file

    def cmd_infusion(self):
        """Show studio learning infusion gate status (open LO-* tickets)."""
        from studio_learning_gate import can_infuse_project_sprint, open_lo_tickets
        from studio_portability import open_lo_title_portability_failures, scan_hq_for_project_nouns

        print_header("STUDIO INFUSION GATE")
        items = open_lo_tickets()
        hq_hits = scan_hq_for_project_nouns()
        bad_titles = open_lo_title_portability_failures(items) if items else []
        if not items and not hq_hits:
            print("\n  ✅ No open LO tickets — safe to plan the next project sprint.")
            print("  Portability: no project folder names found in HQ playbooks/skills (excl. CHANGELOG).")
            print("  Generalize learnings into: process/, teams/skills/, knowledge-base/, studio-library/")
            return True
        if items:
            print(f"\n  {len(items)} open studio learning item(s) — train skill gaps in parallel; product IMPLEMENT is not blocked.")
            ok, msg = can_infuse_project_sprint()
            print(f"\n{msg}")
        else:
            print("\n  ✅ No open LO tickets.")
        if bad_titles:
            print("\n  ❌ Portability: rewrite or drop non-portable open LO titles before infusion.")
        if hq_hits:
            print(f"\n  ⚠️  Portability: {len(hq_hits)} HQ markdown hit(s) with project folder names:")
            for h in hq_hits[:10]:
                print(f"    • {h['path']}:{h['line']} ({h['noun']}) {h['snippet'][:70]}")
            print("    Confine project names to provenance/`source:` lines, or replace with <project>.")
        print("\n  Infusion targets:")
        print("    process/ · teams/*/skills/ · knowledge-base/ · studio-tools/ · studio-library/")
        print("\n  Product: ./studio execute <project>  → IMPLEMENT")
        if items:
            skills = items[0].get("train_skills") or "SO-001"
            print(f"  Train:   ./studio train <skill-id> --from mistake --topic \"<principle>\"  (skills: {skills})")
        return not bad_titles
    
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
        ensure_backlog_layout(project)

        queue = queue_ticket_paths(project)
        unscheduled = [p for p in queue if "sprint:" not in p.read_text(encoding="utf-8")]
        sprint_planned = [p for p in queue if "sprint:" in p.read_text(encoding="utf-8")]

        print(f"\n  PRODUCT BACKLOG: {len(unscheduled)}")
        for t in sorted(unscheduled)[:10]:
            print(f"    - {t.stem}")

        if sprint_planned:
            print(f"\n  SPRINT PLANNED (in backlog/, tagged): {len(sprint_planned)}")
            for t in sorted(sprint_planned)[:10]:
                print(f"    - {t.stem}")

        for status in WORKFLOW_FOLDERS:
            ticket_dir = PROJECTS_DIR / project / "backlog" / status
            if ticket_dir.exists():
                tickets = list(ticket_dir.glob(f"{project[:4].upper()}-*.md"))
                if tickets or status in ("implement", "done"):
                    print(f"\n  {status.upper()}: {len(tickets)}")
                    for t in sorted(tickets)[:8]:
                        print(f"    - {t.stem}")
    
    def cmd_groom(self, project: str, approve: bool = False):
        """Run a grooming session with sprint backlog validation."""
        
        status = load_status(project)
        sprint = status.get("current_sprint", "SPRINT-01")
        
        print_header(f"GROOMING: {project} ({sprint})")

        validation = validate_sprint_backlog(project, sprint)
        report = write_validation_report(project, validation)
        print(f"\n  Backlog validation: {report.relative_to(PROJECTS_DIR / project)}")
        print(format_validation_brief(validation))

        hitl = get_sprint_hitl(status)
        hitl["groom_validated_at"] = validation.get("validated_at")
        hitl["backlog_validation"] = validation.get("summary", {})

        if approve:
            if validation.get("summary", {}).get("errors", 0) > 0:
                print(f"\n  ⚠️  Validation has errors — fix backlog-validation.md / plan.md first.")
                print(f"  Re-run: ./studio groom {project} --approve")
                hitl["groom_status"] = "pending"
                save_status(project, status)
                return False
            hitl["groom_status"] = "approved"
            hitl["groom_approved_at"] = datetime.now().isoformat()
            save_status(project, status)
            print(f"\n  ✅ Sprint backlog grooming approved — safe to ./studio move … implement")
            return True

        hitl["groom_status"] = "pending"
        save_status(project, status)
        
        project_backlog = PROJECTS_DIR / project / "backlog"
        
        # Show blocked tickets
        blocked_dir = project_backlog / "blocked"
        if blocked_dir.exists():
            blocked = list(blocked_dir.glob(f"{project[:4].upper()}-*.md"))
            if blocked:
                print(f"\n  Blocked tickets: {len(blocked)}")
                for t in blocked:
                    print(f"    - {t.stem}")
        
        # Show product backlog tickets
        for path in queue_ticket_paths(project):
            print(f"    - {path.stem}")
        
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

        print(f"\n  Feedback queue:")
        print(format_feedback_list(project, sprint))
        ready = [i for i in load_feedback_queue(project, sprint) if i.get("status") == "ready"]
        if ready:
            print(f"\n  Ready for tickets ({len(ready)}):")
            for item in ready:
                print(f"    ./studio ticket {project} \"{item.get('draft_title')}\" --from-feedback {item['id']}")
        print(f"\n  Rule: sprint-review ideas → ./studio feedback (never direct ticket)")
        
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
    
    def _docker_dir(self, project: str) -> Path:
        return PROJECTS_DIR / project / "docker"

    def _ensure_docker_env_file(self, docker_dir: Path) -> None:
        env_file = docker_dir / ".env"
        env_example = docker_dir / ".env.example"
        if not env_file.exists() and env_example.exists():
            shutil.copy(env_example, env_file)
            rel = env_file.relative_to(PROJECTS_DIR)
            print(f"  ℹ️  Created {rel} from .env.example")

    def _run_docker_compose(
        self,
        project: str,
        *compose_args: str,
        attach: bool = False,
    ) -> bool:
        """Run docker compose with project name (-p) so containers are <project>-*, not docker-*."""
        docker_dir = self._docker_dir(project)
        compose_file = docker_dir / "docker-compose.yml"
        if not compose_file.exists():
            rel = compose_file.relative_to(PROJECTS_DIR)
            print(f"\n  ❌ Missing {rel}")
            print(f"  Run: ./studio env {project} init")
            return False

        self._ensure_docker_env_file(docker_dir)

        cmd = [
            "docker",
            "compose",
            "-p",
            project,
            "--project-directory",
            str(docker_dir),
            "-f",
            str(compose_file),
            *compose_args,
        ]
        print(f"  → {' '.join(cmd)}")
        try:
            result = subprocess.run(
                cmd,
                cwd=str(docker_dir),
                check=False,
                capture_output=not attach,
                text=True,
            )
            if not attach:
                if result.stdout:
                    print(result.stdout.rstrip())
                if result.stderr:
                    print(result.stderr.rstrip())
            if result.returncode != 0:
                print(f"\n  ❌ docker compose failed (exit {result.returncode})")
                return False
            return True
        except FileNotFoundError:
            print("\n  ❌ Docker CLI not found.")
            print("  Install Docker Desktop: https://docs.docker.com/get-docker/")
            return False

    def cmd_env(self, project: str, action: str):
        """Manage the Docker environment (runs docker compose -p <project>)."""
        
        docker_dir = self._docker_dir(project)
        
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
            print(f"\n  Add project-specific services (Mailpit, MinIO, ...) here:")
            print(f"    {docker_dir}/docker-compose.yml")
            print(f"\n  Next step:")
            print(f"    ./studio env {project} up")
        
        elif action == "up":
            print(f"\n  Starting backing services (Postgres, Redis, …) as project **{project}**…")
            if not self._run_docker_compose(project, "up", "-d"):
                return False
            print(f"\n  Status:")
            self._run_docker_compose(project, "ps")
            print(f"\n  Next: cd projects/{project} && npm run dev")
            return True
        
        elif action == "down":
            print(f"\n  Stopping backing services for **{project}**…")
            return self._run_docker_compose(project, "down")
        
        elif action == "status":
            return self._run_docker_compose(project, "ps")
        
        elif action == "logs":
            print(f"\n  Streaming logs for **{project}** (Ctrl+C to exit)…")
            return self._run_docker_compose(project, "logs", "-f", "--tail", "100", attach=True)
        
        else:
            print(f"\n  ⚠️  Unknown action: {action}")
            print(f"  Usage: ./studio env {project} init|up|down|status|logs")
            return False
        
        return True
    
    def cmd_repo(self, project: str, action: str, url: str = ""):
        """Manage the project GitHub repository (project world — not studio HQ)."""
        project_dir = PROJECTS_DIR / project
        if not project_dir.exists():
            print(f"\n  ❌ Project '{project}' not found.")
            return False

        print_header(f"GITHUB REPO: {project}")

        if action == "link":
            if not url.strip():
                print(f"\n  Usage: ./studio repo {project} link <git-url>")
                print(f"  Example: ./studio repo {project} link https://github.com/kallekormann/nudge.git")
                return False

            git_dir = project_dir / ".git"
            if not git_dir.exists() or not (git_dir / "HEAD").exists():
                subprocess.run(["git", "init"], cwd=str(project_dir), check=False, capture_output=True)
                subprocess.run(["git", "checkout", "-B", "main"], cwd=str(project_dir), check=False, capture_output=True)
                print(f"\n  ✓ Git initialized in projects/{project}/")

            existing = subprocess.run(
                ["git", "remote", "get-url", "origin"],
                cwd=str(project_dir),
                capture_output=True,
                text=True,
            )
            if existing.returncode == 0:
                subprocess.run(
                    ["git", "remote", "set-url", "origin", url.strip()],
                    cwd=str(project_dir),
                    check=False,
                )
                print(f"\n  ✓ Updated origin: {url.strip()}")
            else:
                subprocess.run(
                    ["git", "remote", "add", "origin", url.strip()],
                    cwd=str(project_dir),
                    check=False,
                )
                print(f"\n  ✓ Linked origin: {url.strip()}")

            status = load_status(project)
            status["repository_url"] = url.strip()
            save_status(project, status)
            print(f"  Saved to status.json → repository_url")
            print(f"\n  Project git ops run inside projects/{project}/ — never from studio root.")
            return True

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
  ./studio adopt <project> --from <git-url|path> Overlay studio docs on an existing repo
  ./studio bootstrap [project] [intake-file]     AI entry: init→intake→concept→sprint
  ./studio resume <project>                      Next actions from status.json
  ./studio execute <project> [--json]            One next action; loop until HITL
  ./studio settings [--reset-usage]              Policy + estimated token usage (no API keys)
  ./studio note <project> "…"                    Queue mid-execute input (ACK; drain after MOVE_DONE)
  ./studio inform <project> --gate 1             Architecture is HITL — use approve, not inform
  ./studio veto <project> --decision ADR-…
  ./studio train <skill-id> --from mistake --topic "…"
  ./studio ticket-card <project> <id>            Compact ticket card
  ./studio receipt <project> <id>                Scaffold execution receipt
  ./studio health <project>                      Sprint state-graph check
  ./studio focus <project>                       Set active project + isolate siblings
  ./studio isolate <project>                     Hide sibling projects/ from the agent
  ./studio guard <project> "request text"        Check if request is in scope
  ./studio verify-worlds                         Studio vs project git separation
  ./studio verify-abstraction                    Scan studio HQ for project-name leaks
  ./studio install [--with-skills]               npm deps after git clone (+ optional skills)
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
  ./studio review <project> [--approve|--reject] Sprint review (human)
  ./studio reuse <project> [--record path action] Reuse inform brief after sprint (not a HITL gate)
  ./studio feedback <project> "..."              Capture raw feedback (not a ticket)
  ./studio clarify <project> FB-001 [--approve]  Clarify feedback → executable draft
  ./studio feedback-list <project>               Show feedback queue
  ./studio ticket <project> "Title"              Create ticket
  ./studio move <project> <id> <status>          Move ticket
  ./studio groom <project> [--approve]              Validate sprint backlog + grooming

  # Amendment intake (post gate 2)
  ./studio amend <project> <brief-file>          Scaffold AM-NNN analysis folder
  ./studio amendments <project>                  List amendments + status
  ./studio approve <project> --amendment AM-001  Human sign-off on amendment
  ./studio approve <project> --milestones        Approve revised milestone roadmap
  ./studio approve <project> --prd-amendment AM-001  PRD tier change (class C)

  # Phase 4-5: QA
  ./studio gate <project> [--level N]            Run QA gate

  # Phase 6: Learning
  ./studio learn "Title" --signal <s>            Create learning item
  ./studio learn-list                            Show learning items
  ./studio infusion                              Studio LO gate — open learnings before project sprint
  ./studio retro <project> [--complete]          Sprint retrospective
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

    if command == "adopt" and len(args) >= 1:
        project = args[0]
        source = ""
        intent = None
        archetype = "saas-application"
        for i, arg in enumerate(args):
            if arg == "--from" and i + 1 < len(args):
                source = args[i + 1]
            elif arg == "--intent" and i + 1 < len(args):
                intent = args[i + 1]
            elif arg == "--archetype" and i + 1 < len(args):
                archetype = args[i + 1]
        if not source:
            print("  Usage: ./studio adopt <project> --from <git-url-or-path> [--intent intake/<p>.md]")
        else:
            orchestrator.cmd_adopt(project, source, intent=intent, archetype=archetype)

    elif command == "bootstrap":
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

    elif command == "execute" and len(args) >= 1:
        as_json = "--json" in args
        orchestrator.cmd_execute(args[0], as_json=as_json)

    elif command == "settings":
        orchestrator.cmd_settings(reset_usage_flag="--reset-usage" in args)

    elif command == "note" and len(args) >= 1:
        drain = "--drain" in args
        text_parts = [a for a in args[1:] if a != "--drain"]
        orchestrator.cmd_note(args[0], " ".join(text_parts), drain=drain)

    elif command == "inform" and len(args) >= 1:
        gate = None
        for i, arg in enumerate(args):
            if arg == "--gate" and i + 1 < len(args):
                gate = int(args[i + 1])
        orchestrator.cmd_inform(args[0], gate=gate)

    elif command == "veto" and len(args) >= 1:
        ack = "--ack" in args
        decision = ""
        reason = ""
        for i, arg in enumerate(args):
            if arg == "--decision" and i + 1 < len(args):
                decision = args[i + 1]
            elif arg == "--reason" and i + 1 < len(args):
                reason = args[i + 1]
        orchestrator.cmd_veto(args[0], decision=decision, reason=reason, ack=ack)

    elif command == "train" and len(args) >= 1:
        skill_id = args[0]
        topic = ""
        source = "mistake"
        for i, arg in enumerate(args):
            if arg == "--topic" and i + 1 < len(args):
                topic = args[i + 1]
            elif arg == "--from" and i + 1 < len(args):
                source = args[i + 1]
        if not topic and len(args) >= 2 and not args[1].startswith("--"):
            topic = " ".join(a for a in args[1:] if not a.startswith("--"))
        orchestrator.cmd_train(skill_id, topic, source=source)

    elif command == "ticket-card" and len(args) >= 2:
        orchestrator.cmd_ticket_card(args[0], args[1])

    elif command == "receipt" and len(args) >= 2:
        orchestrator.cmd_receipt(args[0], args[1])

    elif command == "health" and len(args) >= 1:
        orchestrator.cmd_health(args[0])

    elif command == "focus" and len(args) >= 1:
        orchestrator.cmd_focus(args[0])

    elif command == "isolate" and len(args) >= 1:
        orchestrator.cmd_isolate(args[0])

    elif command == "guard" and len(args) >= 2:
        orchestrator.cmd_guard(args[0], " ".join(args[1:]))

    elif command == "verify-worlds":
        orchestrator.cmd_verify_worlds()
    elif command == "verify-abstraction":
        orchestrator.cmd_verify_abstraction()

    elif command == "install":
        with_skills = "--with-skills" in args
        orchestrator.cmd_install(with_skills=with_skills)

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
        amendment_id = ""
        prd_amendment = False
        milestones = False
        gate = None
        for i, arg in enumerate(args):
            if arg == "--gate" and i + 1 < len(args):
                gate = int(args[i + 1])
            elif arg == "--amendment" and i + 1 < len(args):
                amendment_id = args[i + 1]
            elif arg == "--prd-amendment" and i + 1 < len(args):
                amendment_id = args[i + 1]
                prd_amendment = True
            elif arg == "--milestones":
                milestones = True
        if amendment_id:
            orchestrator.cmd_approve_amendment(project, amendment_id, prd_tier=prd_amendment)
        elif milestones:
            orchestrator.cmd_approve_milestones(project)
        elif gate is not None:
            orchestrator.cmd_approve(project, gate)
        else:
            print("  ⚠️  Use --gate 0|1|2, --amendment AM-NNN, --prd-amendment AM-NNN, or --milestones")
    
    elif command == "amend" and len(args) >= 2:
        force = "--force" in args
        orchestrator.cmd_amend(args[0], args[1], force=force)

    elif command == "amendments" and len(args) >= 1:
        orchestrator.cmd_amendments(args[0])
    
    elif command == "sprint" and len(args) >= 1:
        approve_scope = "--approve-scope" in args
        orchestrator.cmd_sprint(args[0], approve_scope=approve_scope)

    elif command == "review" and len(args) >= 1:
        project = args[0]
        approve = "--approve" in args
        reject = "--reject" in args
        notes = ""
        reason = ""
        for i, arg in enumerate(args):
            if arg == "--notes" and i + 1 < len(args):
                notes = args[i + 1]
            elif arg == "--reason" and i + 1 < len(args):
                reason = args[i + 1]
        orchestrator.cmd_review(project, approve=approve, reject=reject, notes=notes, reason=reason)

    elif command == "reuse" and len(args) >= 1:
        project = args[0]
        approve = "--approve" in args
        notes = ""
        record_path = ""
        record_action = ""
        record_ref = ""
        record_note = ""
        i = 1
        while i < len(args):
            arg = args[i]
            if arg == "--notes" and i + 1 < len(args):
                notes = args[i + 1]
                i += 2
            elif arg == "--record" and i + 2 < len(args):
                record_path = args[i + 1]
                record_action = args[i + 2]
                i += 3
            elif arg == "--ref" and i + 1 < len(args):
                record_ref = args[i + 1]
                i += 2
            elif arg == "--note" and i + 1 < len(args):
                record_note = args[i + 1]
                i += 2
            else:
                i += 1
        orchestrator.cmd_reuse(
            project,
            approve=approve,
            record_path=record_path,
            record_action=record_action,
            record_ref=record_ref,
            record_note=record_note,
            notes=notes,
        )

    elif command == "feedback" and len(args) >= 2:
        project = args[0]
        text = args[1]
        source = "sprint-review"
        force = "--force" in args
        for i, arg in enumerate(args):
            if arg == "--source" and i + 1 < len(args):
                source = args[i + 1]
        orchestrator.cmd_feedback(project, text, source=source, force=force)

    elif command == "feedback-list" and len(args) >= 1:
        orchestrator.cmd_feedback_list(args[0])

    elif command == "clarify" and len(args) >= 2:
        project = args[0]
        fb_id = args[1]
        title = ""
        scope = ""
        out_of_scope = ""
        acceptance: List[str] = []
        approve = "--approve" in args
        i = 2
        while i < len(args):
            arg = args[i]
            if arg == "--title" and i + 1 < len(args):
                title = args[i + 1]
                i += 2
            elif arg == "--scope" and i + 1 < len(args):
                scope = args[i + 1]
                i += 2
            elif arg == "--out-of-scope" and i + 1 < len(args):
                out_of_scope = args[i + 1]
                i += 2
            elif arg == "--acceptance" and i + 1 < len(args):
                acceptance.append(args[i + 1])
                i += 2
            else:
                i += 1
        orchestrator.cmd_clarify(
            project, fb_id, title=title, scope=scope,
            out_of_scope=out_of_scope, acceptance=acceptance, approve=approve,
        )
    
    elif command == "ticket" and len(args) >= 2:
        project = args[0]
        title = args[1]
        phase = 4
        priority = "P1"
        estimate = "M"
        from_feedback = ""
        for i, arg in enumerate(args):
            if arg == "--phase" and i + 1 < len(args):
                phase = int(args[i + 1])
            elif arg == "--priority" and i + 1 < len(args):
                priority = args[i + 1]
            elif arg == "--estimate" and i + 1 < len(args):
                estimate = args[i + 1]
            elif arg == "--from-feedback" and i + 1 < len(args):
                from_feedback = args[i + 1]
        orchestrator.cmd_ticket(project, title, phase, priority, estimate, from_feedback=from_feedback)
    
    elif command == "move" and len(args) >= 3:
        project = args[0]
        ticket_id = args[1]
        new_status = args[2]
        reason = ""
        for i, arg in enumerate(args):
            if arg == "--reason" and i + 1 < len(args):
                reason = args[i + 1]
        orchestrator.cmd_move(project, ticket_id, new_status, reason)

    elif command == "approve-design" and len(args) >= 2:
        project = args[0]
        ticket_id = args[1]
        notes = ""
        for i, arg in enumerate(args):
            if arg == "--notes" and i + 1 < len(args):
                notes = args[i + 1]
        orchestrator.cmd_approve_design(project, ticket_id, notes=notes)
    
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

    elif command == "infusion":
        orchestrator.cmd_infusion()
    
    elif command == "retro" and len(args) >= 1:
        retro_complete = "--complete" in args
        project = args[0]
        orchestrator.cmd_retro(project, complete=retro_complete)
    
    elif command == "update-skills":
        orchestrator.cmd_update_skills(args)
    
    elif command == "sync" and len(args) >= 1:
        orchestrator.cmd_sync(args[0])
    
    elif command == "adr" and len(args) >= 2:
        orchestrator.cmd_adr(args[0], args[1])
    
    elif command == "board" and len(args) >= 1:
        orchestrator.cmd_board(args[0])
    
    elif command == "groom" and len(args) >= 1:
        project = args[0]
        approve = "--approve" in args
        orchestrator.cmd_groom(project, approve=approve)
    
    elif command == "decide" and len(args) >= 2:
        orchestrator.cmd_decide(args[0], args[1])
    
    elif command == "decisions" and len(args) >= 1:
        orchestrator.cmd_decisions(args[0])
    
    elif command == "env" and len(args) >= 2:
        orchestrator.cmd_env(args[0], args[1])
    
    elif command == "repo" and len(args) >= 2:
        url = args[2] if len(args) >= 3 else ""
        orchestrator.cmd_repo(args[0], args[1], url=url)
    
    elif command == "promote" and len(args) >= 2:
        orchestrator.cmd_promote(args[0], args[1])
    
    else:
        print_help()

if __name__ == "__main__":
    main()
