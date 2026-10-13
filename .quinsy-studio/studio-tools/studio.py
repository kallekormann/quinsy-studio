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
  ./studio ship <project> --to dev               Push product git to origin/dev (before review)
  ./studio ship <project> --to main --approve    Production push — HITL only
  ./studio settings [--reset-usage]              HQ train ledger (not Cursor billing)
  ./studio settings <project> [--init] [--reset-usage]  Product execute ledger
  ./studio note <project> "…"                    Queue mid-execute input (ACK; drain after MOVE_DONE)
  ./studio inform <project> --gate 1             Architecture is HITL — use approve, not inform
  ./studio veto <project> --decision ADR-…
  ./studio train LO-NNNN                         Training chat: Impact block; low infuses, high waits
  ./studio train LO-NNNN --approve | --defer --reason "…" | --reopen
  ./studio train --done LO-NNNN                  Close a lesson (PB- id in target + CHANGELOG required)
  ./studio train --promote <p> --topic "…"       Human overrules a project verdict
  ./studio train <skill-id> --from lo --topic "…" --lo LO-NNNN
  ./studio train --done TR-NNNN                  Mark train job infused
  ./studio train --purge-empty                 Close open jobs with blank observation
  ./studio approve-design <p> <TICKET>         After spec + all-state mocks exist
  ./studio mock <p> <TICKET>                   verify interactive mock + print review script
  ./studio ia-audit <p> <TICKET>               IA nav counts (≤7 top, depth ≤3)
  ./studio approve-arch <p> <TICKET>           After docs/architecture/<TICKET>.md exists
  ./studio cite knowledge-base/foo.md --helpful PB-YYYYMMDD-001
  ./studio ticket-card <project> <id>            Compact ticket card
  ./studio receipt <project> <id>                Scaffold execution receipt
  ./studio qa <project> <id> [--verdict PASS|FAIL]  Independent QA review before done
  ./studio qa <project> <id> --finish [PASS|HOLD]  UX-009: shipped screen vs signed mock
  ./studio lint-skills [--strict]                  Skill lists in sync (matcher, roles, files, registry)
  ./studio reality-check <project> [--check]      Dev-build journey check before cadence review
  ./studio health <project>                      Sprint state-graph check
  ./studio focus <project>                       Set active project + isolate siblings
  ./studio bind <project> --session <id>         Cursor only: bind this chat to one product
  ./studio isolate <project>                     Hide sibling projects/ from the agent
  ./studio guard <project> "request text"        Check if request is in scope
  ./studio verify-worlds                         Studio vs project git separation
  ./studio verify-abstraction                    Scan studio HQ for project-name leaks
  ./studio install [--with-skills]               npm deps after git clone (+ optional skills)
  ./studio library list                           List studio-library assets
  ./studio library pull <project> billing auth-login    Copy library → project
  ./studio library promote <project> packages/billing [--force]
  ./studio library suggest <project> <query>      Find assets before coding
  ./studio promote-library <project> [--force]    Optional Headless/generic kit (not product look)
  ./studio start <project> --mode [core|lean]    Start project
  ./studio status <project>                      Show status
  ./studio board <project>                       Show board

  # Phase 1: Intake (human gate 0)
  ./studio intake <project> <input-file>         Process intake (no tickets yet)
  ./studio ideate [focus] --budget small|normal|large   Shortlist only; promote after approve

  # Phase 2: Architecture (human gate 1)
  ./studio blueprint <project>                   Scaffold architecture docs
  ./studio approve <project> --gate 0            Approve PRD + definitions
  ./studio approve <project> --gate 1            Approve architecture blueprint

  # Phase 3: Design (human gates 2a then 2b)
  ./studio design <project> --discovery          2a interview packet (no prototype)
  ./studio design <project> --scope journey|core-views
  ./studio approve <project> --gate 2a           Approve direction (blocks prototype)
  ./studio approve <project> --gate 2b           Approve project kit → tickets (no library promote)
  ./studio revise <project> --gate <0|1|2a|2b> --feedback "..."

  # Legacy
  ./studio concept <project>                     → blueprint / design

  # Phase 3: Sprint Management
  ./studio sprint <project> [--kind design|architecture|implementation|hygiene]
  ./studio review <project> [--approve|--reject] Cadence review (every N implementation sprints)
  ./studio reuse <project> [--record path action] Reuse inform brief after sprint (not a HITL gate)
  ./studio feedback <project> "..."              Capture raw feedback (not a ticket)
  ./studio clarify <project> FB-001 [--severity blocker|major|minor|polish] [--verbatim "..."] [--approve]  Clarify feedback → executable draft
  ./studio feedback-list <project>               Show feedback queue
  ./studio ticket <project> "Title"              Create ticket
  ./studio move <project> <id> <status>          Move ticket
  ./studio groom <project> [--approve]              Validate sprint backlog + grooming

  # Amendment intake (post gate 2)
  ./studio amend <project> <brief-file>          Scaffold AM-NNN analysis folder
  ./studio amendments <project>                  List amendments + status
  ./studio approve <project> --amendment AM-001  Human sign-off on amendment
  ./studio approve <project> --milestones        Approve revised milestone roadmap
  ./studio whoami                                 Print this context's id (QUINSY_CONTEXT_ID) for QA reviewer lines
  ./studio milestone <project> [plan [--next] | review | --approve [--notes "..."]]  PM milestone ownership (plan tickets, review state, HITL sign)
  ./studio approve <project> --prd-amendment AM-001  PRD tier change (class C)

  # Phase 4: Implementation
  ./studio gate <project> [--level N]            Run QA gate

  # Phase 6: Learning
  ./studio learn "Title" --signal <s>            Open a lesson candidate (portable only)
  ./studio learn LO-NNNN --verdict studio|project --reason "…" --assumed "…" --signed "…" --next "…" [--target FILE]
  ./studio learn-list                            Show open LO items (TRAIN_DUE)
  ./studio learn-find "<topic>"                  Search infused PB- bullets in playbooks, process, skills
  ./studio infusion                              Open LO status (does not block IMPLEMENT)
  ./studio train LO-NNNN                         Training chat (see above)
  ./studio train --done TR-NNNN                  Close a train job after infusion
  ./studio infusion-delta --path FILE --op add --body "assumed: … signed: … next: …" [--lo LO-NNNN]
  ./studio cite knowledge-base/foo.md --helpful PB-YYYYMMDD-001
  ./studio retro <project> [--complete]          Sprint retrospective
  ./studio sync <project>                        Sync global assets

  # Tools
  ./studio adr <project> "Title"                 Create ADR
  ./studio decide <project> "Title"              Create decision record
  ./studio decisions <project>                   Show decision records
  ./studio env <project> init|up|down|status [--approve]
  ./studio env <project> prod --explain           Production names (.env.local) and what each is for
  ./studio ops <project> readiness|deploy|logs|status|migrate --prod|db|cleanup [--approve]
  ./studio repo <project> create|status          GitHub repo
  ./studio promote <project> <asset>             Promote asset to library
  ./studio update-skills                         Subscribe/update external skill packages
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

from ticket_helpers import (
    apply_i18n_ticket_rules,
    render_staffing_section,
    render_ticket_markdown,
    role_for_skills,
)
from ticket_ids import allocate_ticket_id
from skill_matcher import match_skills, staff_skills, team_for_skills
from design_ticket_helpers import (
    default_design_spec_path,
    design_deliverables_status,
    design_implement_blocked_message,
    design_spec_completeness_error,
    design_mocks_emoji_icon_warning,
    enrich_design_skills,
    infer_ticket_type,
    mock_review_block,
    parse_design_fields,
    requires_design_approval,
    set_design_approved,
    write_design_spec_stub,
)
from init_project_env import init_project
from studio_env import (
    INJECT_ACTIONS,
    RUNTIME_EXECUTE_KINDS,
    compose_argv,
    docker_cli_available,
    docker_install_hint,
    ensure_project_env_file,
    inject_summary,
    parse_env_assignments,
    public_command_line,
    redact_output,
    redact_secret_patterns,
    refuse_without_approve,
    merged_schema_names,
    secret_values_for_redaction,
)
from pre_impl_workflow import (
    PHASE_BLUEPRINT,
    PHASE_DESIGN,
    PHASE_IMPLEMENT,
    PHASE_INTAKE,
    PHASE_SPRINT,
    design_system_approved,
    direction_approved,
    record_revision,
    scaffold_blueprint,
    scaffold_design,
    scaffold_discovery,
    previous_human_gate_block,
    validate_human_gate,
)
from studio_design_discovery import BARE_GATE_2_MSG, parse_cli_gate
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
    open_sprint_ticket_ids,
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
    escalation_path,
    existing_gate_fail_lo,
    failure_signature,
    format_execute_step,
    format_health,
    health_report,
    load_execution_log,
    receipt_is_complete,
    receipt_path,
    repeated_failure,
    should_escalate,
    ticket_card_for,
    write_escalation,
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

def explicit_kind_is_not_hygiene(kind: str) -> bool:
    """Hygiene sprints sit outside the milestone train."""
    return (kind or "").strip().lower() != "hygiene"


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
    folder = INTAKE_DIR / slug
    if folder.is_dir():
        return folder
    named = INTAKE_DIR / project
    if named.is_dir():
        return named
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
        "backend": "Payload on Next.js (Postgres). Opt out only with an ADR.",
        "storage": "Postgres via Payload. Uploads: local disk in dev, Cloudflare R2 in production.",
        "deployment": "Coolify on a VPS. Local boot is Docker Desktop.",
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
        print("\n  Place a file or a folder in intake/, then run:")
        print("    ./studio bootstrap <project>")
        print("    ./studio bootstrap <project> intake/<project>/")
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

        if status.get("phase") in (PHASE_INTAKE, PHASE_BLUEPRINT, PHASE_DESIGN) or not design_system_approved(status):
            if status.get("mode") == "adopt":
                if not direction_approved(status):
                    self._print_gate_pause(
                        project,
                        "2a",
                        "Keep vs evolve the existing UI. Interview the human. Do not scaffold a fake prototype.",
                    )
                    return True
                self._print_gate_pause(
                    project,
                    "2b",
                    "Token-map of what exists. Do not scaffold an empty Next.js prototype.",
                )
                return True
            if not direction_approved(status):
                disc = PROJECTS_DIR / project / "docs" / "design" / "discovery.md"
                if not disc.exists():
                    self.cmd_design(project, discovery=True)
                self._print_gate_pause(
                    project,
                    "2a",
                    "Answer discovery questions; agent fills DESIGN.md. Do not scaffold prototype.",
                )
                return True
            design = PROJECTS_DIR / project / "design" / "prototype" / "package.json"
            if not design.exists():
                scope = status.get("design_scope") or "core-views"
                self.cmd_design(project, scope)
            if not design_system_approved(status):
                self._print_gate_pause(project, "2b", "Review project kit: CSS tokens, coded A/M/O, sticker all-states.")
                return True

        status = load_status(project)
        if not status.get("current_sprint"):
            self.cmd_sprint(project)
            status = load_status(project)

        print(f"\n  ✅ Ready for implementation (phase {status.get('phase')}, {status.get('current_sprint')})")
        print(f"     Agent contract: projects/{project}/agent-briefing.md")
        print(f"     Next: ./studio resume {project}")
        return True

    def _print_gate_pause(self, project: str, gate, hint: str):
        labels = {
            0: "Intake — PRD & definitions",
            "0": "Intake — PRD & definitions",
            1: "Architecture blueprint",
            "1": "Architecture blueprint",
            2: "Design — use 2a then 2b",
            "2a": "Design direction — discovery + DESIGN.md",
            "2b": "Design system — project kit + sticker sheet",
        }
        status = load_status(project)
        if status.get("mode") == "adopt":
            labels = {
                0: "As-built truth + synthesized PRD",
                "0": "As-built truth + synthesized PRD",
                1: "As-is architecture (no stack swap)",
                "1": "As-is architecture (no stack swap)",
                "2a": "Keep vs evolve the existing UI",
                "2b": "Token-map of what exists + debt",
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
        elif not design_system_approved(status):
            if not direction_approved(status):
                if adopt:
                    actions.append("AI: write unanswered questions in docs/design/discovery.md (keep vs evolve)")
                    actions.append("Do NOT scaffold design/prototype")
                    actions.append(f"Human: answer discovery → ./studio approve {project} --gate 2a")
                else:
                    actions.append(f"./studio design {project} --discovery")
                    actions.append("AI: unanswered questions only; fill DESIGN.md from human answers")
                    actions.append("Do NOT scaffold design/prototype until 2a is approved")
                    actions.append(f"Human: answer discovery → ./studio approve {project} --gate 2a")
            elif adopt:
                actions.append("AI: map existing UI to ui/tokens/design-tokens.css (no fake prototype)")
                actions.append(f"Human: review token-map of what exists → ./studio approve {project} --gate 2b")
            elif not status.get("design_scope"):
                actions.append(f"Human: choose mock scope → ./studio design {project} --scope journey|core-views")
            else:
                actions.append(f"./studio design {project} --scope {status['design_scope']}")
                actions.append("AI: project CSS tokens, coded A/M/O, sticker all-states, mocks on those tokens")
                actions.append(f"Human: review live prototype → ./studio approve {project} --gate 2b")
                actions.append(f"Iterate: ./studio revise {project} --gate 2b --feedback \"...\"")
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

    def cmd_execute(self, project: str, as_json: bool = False, release: bool = False, session: str = ""):
        """Emit exactly one next action. Agent must loop until HITL."""
        if not (PROJECTS_DIR / project).exists():
            print(f"\n  ❌ Project '{project}' not found.")
            return False
        from studio_agent_sessions import bound_project, cursor_multi_project_enabled
        from studio_execute_leases import acquire_execute_lease, release_execute_lease
        from studio_isolation import apply_project_isolation

        if release:
            release_execute_lease(project)
            print_header(f"EXECUTE LEASE RELEASED: {project}")
            print("  Next queued project may acquire a lease.")
            return True

        cursor = cursor_multi_project_enabled()
        sid = (session or "").strip() if cursor else ""
        bound = bound_project(sid) if sid else ""
        if bound and bound != project:
            print_header(f"EXECUTE REFUSED: {project}")
            print(f"\n  This chat is bound to {bound}. Run ./studio execute {bound}.")
            print("  A sibling product needs its own chat and ./studio bind.")
            return False

        granted, lease_msg = acquire_execute_lease(project, session_id=sid)
        if not granted:
            print_header(f"EXECUTE QUEUED: {project}")
            print(f"\n  {lease_msg}")
            return False

        # A bound Cursor chat must not rewrite the workspace sibling list.
        if not bound:
            apply_project_isolation(project)
        from payload_foundation import scaffold_needed, scaffold_payload_app

        if scaffold_needed(project):
            created = scaffold_payload_app(project)
            print(f"  Payload app written ({len(created)} files) under projects/{project}/apps/web")
        status = load_status(project)
        step = decide_next_action(project)
        if step.kind in RUNTIME_EXECUTE_KINDS and not docker_cli_available():
            print(docker_install_hint())
            return False
        if as_json:
            print(json.dumps(step.to_dict(), indent=2))
        else:
            print_header(f"EXECUTE: {project}")
            print(format_execute_step(project, step))
            print(f"  LEASE:   {lease_msg}")
        if not bound:
            set_active_project(project, status)
        if step.kind == "HITL":
            release_execute_lease(project)
            if not as_json:
                print("  LEASE:   released (HITL idle) — another product may execute")
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
        print("  Replace every template line. Tick each AC with its proof. Evidence and API proof lines say PASS / FAIL / NOT TESTED.")
        print("  Named screenshots and test files must exist. Then ./studio execute")
        return True

    def cmd_health(self, project: str):
        """Validate sprint / LO / receipt / gate state graph."""
        print_header(f"HEALTH: {project}")
        print(format_health(project, health_report(project)))
        return True

    def cmd_settings(self, project: str = "", reset_usage_flag: bool = False, init_flag: bool = False):
        """Show HQ or product studio-load policy + estimated usage."""
        from studio_settings import (
            format_settings_report,
            init_project_settings,
            load_settings,
            load_usage,
            reset_usage,
            usage_path_for,
        )

        print_header("STUDIO SETTINGS" + (f" — {project}" if project else " — HQ"))
        if init_flag:
            if not project:
                print("  Need ./studio settings <project> --init")
                return False
            written = init_project_settings(project)
            if written:
                print("  Wrote:")
                for path in written:
                    print(f"    {path}")
            else:
                print("  Already present (no overwrite).")
            print()
        ledger = "project" if project else "hq"
        usage_path = usage_path_for(ledger, project)
        if reset_usage_flag:
            reset_usage(project, usage_path)
            print("  Usage reset.\n")
        print(format_settings_report(load_settings(project=project, ledger=ledger), load_usage(usage_path)))
        self._print_train_due(project)
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

    def cmd_inform(self, project: str, gate: Optional[str] = None):
        """Inform-only steps (not architecture/design — those are HITL)."""
        g = str(gate) if gate is not None else ""
        if g in ("1",):
            print_header(f"GATE 1 IS HITL — {project}")
            print("  Architecture after PRD is a human decision.")
            print(f"  Agent: ./studio blueprint {project}")
            print(f"  Human: ./studio approve {project} --gate 1")
            print(f"  Iterate: ./studio revise {project} --gate 1 --feedback \"...\"")
            return False
        if g in ("2", "2a", "2b"):
            print_header(f"GATES 2a/2b ARE HITL — {project}")
            print("  Design is two signed packets: direction (2a) then project kit (2b).")
            print(f"  Agent: ./studio design {project} --discovery")
            print(f"  Human: ./studio approve {project} --gate 2a")
            print(f"  Then:  ./studio design {project}  and  ./studio approve {project} --gate 2b")
            print(f"  Iterate: ./studio revise {project} --gate 2b --feedback \"...\"")
            print(f"  {BARE_GATE_2_MSG}")
            return False
        print("  Architecture (gate 1) and design (gates 2a then 2b) require ./studio approve, not inform.")
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

    def cmd_train_lesson(
        self,
        lo_id: str,
        *,
        approve: bool = False,
        defer: bool = False,
        reopen: bool = False,
        done: bool = False,
        reason: str = "",
    ) -> bool:
        """Training chat on one studio lesson: impact → (HITL on high) → infuse → close."""
        from studio_lesson import (
            approve_lesson,
            assess,
            close_issues,
            defer_lesson,
            ensure_impact_template,
            lo_path,
            move_lo_done,
            parse_frontmatter,
            parse_lesson,
            reopen_lesson,
        )

        lo_id = lo_id.strip().upper()
        print_header(f"TRAIN — {lo_id}")
        try:
            if reopen:
                dest = reopen_lesson(lo_id)
                print(f"  Reopened → {dest.relative_to(QUINSY_STUDIO.parent)}")
                print(f"  Next: ./studio train {lo_id}")
                return True
            if defer:
                dest = defer_lesson(lo_id, reason)
                print(f"  Deferred → {dest.relative_to(QUINSY_STUDIO.parent)}")
                print("  It stays first in every TRAIN_DUE list. Bring it back: ./studio train " + lo_id + " --reopen")
                return True
            if approve:
                approve_lesson(lo_id)
                print(f"  Approved by the human. Infuse now:")
                self._print_infuse_hint(lo_id)
                return True
            if done:
                issues = close_issues(lo_id)
                if issues:
                    print(f"  ❌ {lo_id} cannot close:")
                    for issue in issues:
                        print(f"    • {issue}")
                    return False
                dest = move_lo_done(lo_id)
                print(f"  ✅ {lo_id} done → {dest.relative_to(QUINSY_STUDIO.parent)}")
                print("  Commit the target file and CHANGELOG.md in studio HQ. The LO stays local.")
                return True
        except (ValueError, FileNotFoundError) as exc:
            print(f"  ❌ {exc}")
            return False

        path = lo_path(lo_id)
        if path is None:
            print(f"  ❌ {lo_id} not found under backlog/")
            return False
        state = assess(lo_id)
        kind = state.get("state")
        if kind == "needs_verdict":
            print(f"  ❌ No verdict yet ({', '.join(state.get('missing') or [])}). The product agent answers first:")
            print(f"    ./studio learn {lo_id} --verdict studio|project --reason \"…\" --assumed \"…\" --signed \"…\" --next \"…\" [--target <file>]")
            return False
        if kind == "needs_impact":
            ensure_impact_template(lo_id)
            print(f"  Wrote the ## Impact block into {path.name}. Fill every line, then run this command again.")
            print("  files / in-flight / compliance / pro / contra / severity. The floor comes from the target path; raise it, never lower it.")
            return False
        if kind == "impact_stub":
            print(f"  ❌ Impact block still has placeholders: {', '.join(state.get('missing') or [])}")
            print(f"  Edit {path.relative_to(QUINSY_STUDIO.parent)} and run again.")
            return False
        lesson = state.get("lesson") or parse_lesson(path.read_text(encoding="utf-8"))
        impact = state.get("impact") or {}
        print(f"  next:   {lesson.get('next')}")
        print(f"  target: {lesson.get('target')}")
        print(f"  severity: {state.get('severity')}")
        if kind == "hitl":
            print("\n  HIGH IMPACT — the human decides before anything is written:")
            print(f"    files:      {impact.get('files')}")
            print(f"    in-flight:  {impact.get('in-flight')}")
            print(f"    compliance: {impact.get('compliance')}")
            print(f"    pro:        {impact.get('pro')}")
            print(f"    contra:     {impact.get('contra')}")
            print(f"\n    ./studio train {lo_id} --approve")
            print(f"    ./studio train {lo_id} --defer --reason \"…\"")
            return False
        meta = parse_frontmatter(path.read_text(encoding="utf-8"))
        if meta.get("infused_id"):
            print(f"\n  Already infused as {meta['infused_id']}. Close: ./studio train --done {lo_id}")
            return True
        print("\n  Low impact — infuse now (INFORM, no signature):")
        self._print_infuse_hint(lo_id)
        return True

    def _print_infuse_hint(self, lo_id: str) -> None:
        from studio_lesson import lo_path, parse_lesson

        path = lo_path(lo_id)
        lesson = parse_lesson(path.read_text(encoding="utf-8")) if path else {}
        target = lesson.get("target") or "<target>"
        print(f"    ./studio infusion-delta --lo {lo_id} --path {target} --op add --section Deltas \\")
        print(f"      --body \"assumed: {lesson.get('assumed', '…')[:60]} signed: {lesson.get('signed', '…')[:60]} next: {lesson.get('next', '…')[:80]}\"")
        print("    then a CHANGELOG.md line naming the PB- id, ./studio verify-abstraction, and")
        print(f"    ./studio train --done {lo_id}")

    def cmd_train_promote(self, project: str, topic: str) -> bool:
        """Human overrules a project verdict: the line becomes a studio lesson candidate."""
        from studio_harvest import harvest_identified_learning
        from studio_lesson import project_verdict_lines

        print_header(f"TRAIN — promote from {project}")
        rows = project_verdict_lines(project, limit=50)
        match = next((r for r in rows if topic.strip().lower() in r["title"].lower()), None)
        if not match:
            print(f"  ❌ No project-verdict line in projects/{project}/docs/studio-learnings-local.md matches {topic!r}")
            return False
        result = harvest_identified_learning(match["title"], source=f"{project}/promoted", observation=match["title"])
        if result.get("dropped"):
            print(f"  ❌ Still not portable as written: {result.get('reason')}. Rewrite the title as a must/should/never rule and run again.")
            return False
        print(f"  Candidate {result.get('lo_id')} opened (human overruled: {match['reason'] or 'no reason recorded'}).")
        print(f"  Fill the verdict as studio: ./studio learn {result.get('lo_id')} --verdict studio --reason \"human overrule\" --assumed \"…\" --signed \"…\" --next \"…\"")
        return True

    def cmd_train(self, skill_id: str, topic: str, source: str = "mistake", done: str = "", lo_id: str = "", close_mode: bool = False, purge_empty: bool = False):
        """Queue a parallel skill-training job. Does not block product IMPLEMENT."""
        from studio_train import (
            enqueue_train,
            skill_file_hint,
            close_job,
            close_jobs_for_lo,
            sync_train_with_done_los,
            open_jobs,
            purge_empty_observations,
        )

        print_header("TRAIN")
        if purge_empty:
            closed = purge_empty_observations()
            print(f"  Purged {len(closed)} empty-observation job(s): {', '.join(closed) or 'none'}")
            print(f"  Queue now {len(open_jobs())} open")
            return True
        synced = sync_train_with_done_los()
        if synced:
            print(f"  Synced {len(synced)} job(s) whose LO is already in backlog/done/")
        if close_mode and lo_id and re.fullmatch(r"LO-\d{4}", lo_id.upper()):
            from studio_lesson import close_issues

            issues = close_issues(lo_id.upper())
            if issues:
                print(f"  ❌ {lo_id.upper()} cannot close — the lesson is not in the studio yet:")
                for issue in issues:
                    print(f"    • {issue}")
                return False
        if close_mode:
            closed = close_jobs_for_lo(lo_id) if lo_id else []
            if done:
                job = close_job(done)
                if job:
                    closed = [job]
                elif not closed:
                    print(f"  ⚠️  Train job {done} not found")
                    return False
            if not done and lo_id and not closed:
                print(f"  ⚠️  No open train job for {lo_id}")
                return False
            ids = ", ".join(str(j.get("id")) for j in closed)
            print(f"  Closed {ids or 'none'} — queue now {len(open_jobs())} open")
            return True
        try:
            job = enqueue_train(
                skill_id,
                topic,
                source="lo" if lo_id else source,
                observation=lo_id,
            )
        except ValueError as exc:
            print(f"  ⚠️  {exc}")
            print("  Usage: ./studio train <skill-id> --topic \"…\" --lo LO-NNNN")
            print("         ./studio train --done TR-NNNN")
            return False
        hint = skill_file_hint(skill_id)
        print(f"  Queued {job['id']}  skill={job['skill_id']}  topic={job['topic']}  lo={job.get('observation') or '-'}")
        print("  Infuse with ./studio infusion-delta, then ./studio train --done")
        if hint:
            print(f"  Skill file: {hint}")
        return True

    def cmd_cite(self, rel_path: str, helpful: str = "", harmful: str = ""):
        """Increment helpful/harmful on playbook bullets (HQ-T18)."""
        from studio_infusion_delta import bump_counts

        print_header("CITE")
        ids_h = [p.strip() for p in (helpful or "").split(",") if p.strip() and p.strip().lower() != "none"]
        ids_d = [p.strip() for p in (harmful or "").split(",") if p.strip() and p.strip().lower() != "none"]
        if not rel_path or not (ids_h or ids_d):
            print("  Usage: ./studio cite knowledge-base/foo.md --helpful PB-YYYYMMDD-001 [--harmful PB-…]")
            return False
        try:
            for bid in ids_h:
                print(f"  {bump_counts(rel_path, bid, helpful=1)}")
            for bid in ids_d:
                print(f"  {bump_counts(rel_path, bid, helpful=0, harmful=1)}")
        except (ValueError, FileNotFoundError) as exc:
            print(f"  ⚠️  {exc}")
            return False
        return True

    def cmd_infusion_delta(self, rel_path: str, op: str, section: str = "Deltas", body: str = "", bullet_id: str = "", lo_id: str = ""):
        """Apply one ADD/UPDATE/REMOVE bullet to a studio HQ file. With --lo the bullet closes that lesson."""
        from studio_infusion_delta import apply_delta

        print_header("INFUSION DELTA")
        lo_id = (lo_id or "").strip().upper()
        if lo_id:
            from studio_lesson import (
                assess,
                effective_severity,
                infusion_body_issues,
                lo_path,
                normalize_target,
                parse_frontmatter,
                parse_lesson,
            )

            path = lo_path(lo_id)
            if path is None:
                print(f"  ❌ {lo_id} not found under backlog/")
                return False
            text = path.read_text(encoding="utf-8")
            if op == "add":
                issues = infusion_body_issues(body)
                if issues:
                    print(f"  ❌ A bullet that closes {lo_id} carries the lesson, not a title: {'; '.join(issues)}")
                    print("  --body \"assumed: <studio default> signed: <what the human accepted> next: <the rule>\"")
                    return False
            lesson = parse_lesson(text)
            target = normalize_target(lesson.get("target") or parse_frontmatter(text).get("infusion_path") or "")
            if target and normalize_target(rel_path) != target:
                print(f"  ❌ {lo_id} targets `{target}`, not `{rel_path}`. Change the LO target first if that is wrong.")
                return False
            state = assess(lo_id)
            if state.get("state") != "infuse":
                if state.get("state") == "hitl":
                    print(f"  ❌ {lo_id} is high impact and not approved. ./studio train {lo_id} --approve, or --defer --reason \"…\"")
                else:
                    print(f"  ❌ {lo_id} is not ready to infuse ({state.get('state')}). Run ./studio train {lo_id} first.")
                return False
        try:
            result = apply_delta(rel_path, op, section=section, body=body, bullet_id=bullet_id)
        except (ValueError, FileNotFoundError) as exc:
            print(f"  ⚠️  {exc}")
            print("  Usage: ./studio infusion-delta --path knowledge-base/foo.md --op add --section Deltas --body \"assumed: … signed: … next: …\" [--lo LO-NNNN]")
            return False
        print(f"  {result['op']} {result['id']} → {result['path']}")
        if lo_id:
            from studio_lesson import record_infusion

            record_infusion(lo_id, bullet_id=result["id"], target=result["path"])
            print(f"  Recorded on {lo_id}. Add a CHANGELOG.md line naming {result['id']}, run ./studio verify-abstraction, then ./studio train --done {lo_id}")
        return True

    def cmd_bind(self, project: str, session: str = "", show: bool = False, clear: bool = False) -> bool:
        """Bind this Cursor chat to one product. Refuses when HQ runtime is not cursor."""
        from studio_agent_sessions import bind_session, bound_project, clear_session
        from studio_isolation import write_session_isolation_surface

        if show:
            bound = bound_project(session) if session else ""
            print(bound or "(unbound)")
            return True
        if clear:
            if not session:
                print("  bind --clear needs --session <id>")
                return False
            print("  cleared" if clear_session(session) else "  no binding")
            return True
        ok, message = bind_session(project, session)
        if not ok:
            print(f"  {message}")
            return False
        write_session_isolation_surface()
        print(f"  {message}")
        print("  Sibling trees stay visible. Hooks deny the other chats' projects.")
        return True

    def cmd_focus(self, project: str, force: bool = False, session: str = ""):
        """Set active project context for IDE agent (scope banner)."""
        project_dir = PROJECTS_DIR / project
        if not project_dir.exists():
            print(f"\n  ❌ Project '{project}' not found.")
            return False
        from studio_agent_sessions import bound_project, cursor_multi_project_enabled
        from studio_execute_leases import focus_isolation_blocked

        sid = (session or "").strip() if cursor_multi_project_enabled() else ""
        bound = bound_project(sid) if sid else ""
        if bound and bound != project:
            print_header(f"FOCUS REFUSED: {project}")
            print(f"\n  This chat is bound to {bound}. Do not focus {project} from this chat.")
            return False
        if bound == project:
            print_header(f"FOCUS: {project}")
            print("\n  Session already bound. Isolation stays per chat; .cursorignore was not rewritten.")
            return True

        blocked = focus_isolation_blocked(project, force=force)
        if blocked:
            print_header(f"FOCUS BLOCKED: {project}")
            print(f"\n  {blocked}")
            print("  Five concurrent products need five chats/windows, not one .cursorignore.")
            return False
        status = load_status(project)
        set_active_project(project, status)
        from studio_settings import reset_usage, usage_path_for

        reset_usage(project, usage_path_for("project", project))
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

    def cmd_guard(self, project: str, request: str, session: str = ""):
        """Check if a user request is in project/sprint scope."""
        from studio_agent_sessions import bound_project, cursor_multi_project_enabled

        sid = (session or "").strip() if cursor_multi_project_enabled() else ""
        bound = bound_project(sid) if sid else ""
        if bound and bound != project:
            print_header(f"GUARD: {project}")
            print("\n  🚧 SESSION_BOUND")
            print(f"  This chat is bound to {bound}. Stay there. A sibling needs its own chat and ./studio bind.")
            return False
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
            "ideate": "💡",
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
        if verdict == "ideate":
            print("  Do not queue this on the product sprint. Follow the printed ./studio ideate section.")
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
        from studio_context import load_active_project
        from studio_isolation import install_studio_hq_git_hook, sibling_projects, write_cursorignore

        active = (load_active_project() or {}).get("project") or ""
        write_cursorignore(sibling_projects(active) if active else [])
        print("  Cursor ignore: QUINSY-SECRETS block (LO-0314)")
        hq_hook = install_studio_hq_git_hook()
        if hq_hook:
            print(f"  HQ pre-commit: {hq_hook} (refuses projects/ in the studio index)")

        from payload_foundation import skill_present

        if not skill_present():
            print("\n  ❌ Payload skill missing: teams/02-backend-systems/skills/payload/SKILL.md")
            return False
        print("  Payload skill: teams/02-backend-systems/skills/payload/SKILL.md")

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
            print("\n  ⚠️  Nothing to promote (product look stays in the project; library is Headless only)")
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
        print("  ./studio library pull <project> billing auth-login tokens [button...]")
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
        self._print_train_due(project)
    
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
        print(f"\n  ℹ️  Tickets will be generated after design approval (gate 2b).")
        
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

    def cmd_design(self, project: str, scope: str = "core-views", discovery: bool = False):
        """2a: discovery packet only. 2b: project kit + prototype. Never indigo defaults."""
        status = load_status(project)
        hg = status.get("human_gates", {})

        if hg.get("1", {}).get("status") != "approved":
            print(f"  ⚠️  Gate 1 (architecture) must be approved first")
            return False

        if discovery or not direction_approved(status):
            if direction_approved(status) and not discovery:
                pass
            else:
                print_header(f"GATE 2a: DESIGN DISCOVERY — {project}")
                created = scaffold_discovery(project)
                for path in created:
                    try:
                        print(f"  ✓ {path.relative_to(PROJECTS_DIR / project)}")
                    except ValueError:
                        print(f"  ✓ {path}")
                status["phase"] = PHASE_DESIGN
                save_status(project, status)
                print("  Skills: UX-001, UX-004, UX-006, UX-008 — unanswered questions only.")
                print("  Do NOT invent brand. Do NOT scaffold design/prototype until 2a is approved.")
                print(f"  Human: fill A: lines in docs/design/discovery.md")
                print(f"  Then:  ./studio approve {project} --gate 2a")
                return True

        if status.get("mode") == "adopt":
            from studio_adopt import overlay_studio

            print_header(f"GATE 2b: DESIGN TRUTH — {project} (as-built)")
            overlay_studio(PROJECTS_DIR / project, project, archetype=status.get("archetype") or "saas-application")
            status["phase"] = PHASE_DESIGN
            status["design_scope"] = "as-built"
            save_status(project, status)
            print("  Map existing UI to ui/tokens/design-tokens.css")
            print("  Do NOT scaffold design/prototype as a parallel app")
            print(f"  Human: ./studio approve {project} --gate 2b when the token-map is honest")
            return True

        if scope not in ("journey", "core-views"):
            print(f"  ⚠️  scope must be 'journey' or 'core-views'")
            return False

        print_header(f"GATE 2b: PROJECT KIT — {project} (scope: {scope})")
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
        print("  Fill CSS tokens, coded A/M/O, sticker inventory (all states). Title-only fails.")
        print(f"  Human:      ./studio approve {project} --gate 2b")
        print(f"  Iterate:    ./studio revise {project} --gate 2b --feedback \"...\"")
        return True

    def cmd_concept(self, project: str):
        """Deprecated — use ./studio blueprint and ./studio design."""
        print(f"  ℹ️  `concept` is deprecated. Use:")
        print(f"     ./studio blueprint {project}")
        print(f"     ./studio design {project} --discovery")
        print(f"     ./studio design {project} --scope journey|core-views")
        status = load_status(project)
        hg = status.get("human_gates", {})
        if hg.get("0", {}).get("status") == "approved" and hg.get("1", {}).get("status") != "approved":
            return self.cmd_blueprint(project)
        if hg.get("1", {}).get("status") == "approved" and not direction_approved(status):
            return self.cmd_design(project, discovery=True)
        if direction_approved(status) and not design_system_approved(status):
            scope = status.get("design_scope") or "core-views"
            return self.cmd_design(project, scope)
        print(f"  Complete gate 0 first: ./studio approve {project} --gate 0")
        return False

    def cmd_revise(self, project: str, gate, feedback: str):
        """Record feedback and reopen a human gate for iteration."""
        try:
            gate_id = parse_cli_gate(str(gate))
        except ValueError as exc:
            print(f"  ⚠️  {exc}")
            return False
        if not feedback.strip():
            print(f"  ⚠️  --feedback is required")
            return False

        status = load_status(project)
        rev_file = record_revision(project, gate_id, feedback)
        hg = status.setdefault("human_gates", {})
        packet = {
            "status": "changes-requested",
            "date": datetime.now().isoformat(),
            "feedback": feedback.strip(),
        }
        hg[gate_id] = packet
        if gate_id == "2b":
            hg["2"] = packet
        if gate_id == "0":
            status["phase"] = PHASE_INTAKE
        elif gate_id == "1":
            status["phase"] = PHASE_BLUEPRINT
        else:
            status["phase"] = PHASE_DESIGN
        status["gate"] = gate_id
        status["gate_status"] = "changes-requested"
        save_status(project, status)

        print_header(f"REVISION RECORDED — gate {gate_id}")
        print(f"  Log: {rev_file}")
        print(f"  Update artifacts, then ./studio approve {project} --gate {gate_id}")
        return True
    
    def _harvest_gate_rounds(self, project: str, gate_id: str) -> None:
        """A gate signed after ≥2 send-backs opens a lesson candidate. The verdict comes later."""
        try:
            from studio_harvest import GATE_ROUND_THRESHOLD, gate_revision_rounds, harvest_gate_rounds
        except ImportError:
            return
        rounds = gate_revision_rounds(PROJECTS_DIR / project, gate_id)
        if len(rounds) < GATE_ROUND_THRESHOLD:
            return
        result = harvest_gate_rounds(project, PROJECTS_DIR / project, gate_id) or {}
        print(f"\n  Gate {gate_id} needed {len(rounds)} revision rounds before this signature.")
        if result.get("created"):
            print(f"  Lesson candidate opened: {result.get('lo_id')} → {result.get('infusion_path')}")
            print("  Answer before the next retro closes: did this change because of this product, or because the studio default was wrong?")
            print(f"    ./studio learn {result.get('lo_id')} --verdict studio|project --reason \"…\" --assumed \"…\" --signed \"…\" --next \"…\" [--target <file>]")
        elif result.get("lo_id"):
            print(f"  Lesson candidate already open: {result.get('lo_id')}")
        elif result.get("dropped"):
            print(f"  Candidate kept project-local: {result.get('reason')}")

    def _print_train_due(self, project: str = "", *, compact: bool = False) -> None:
        try:
            from studio_lesson import train_due_lines
        except ImportError:
            return
        lines = train_due_lines(project, compact=compact)
        if lines:
            print()
            for line in lines:
                print(f"  {line}")

    def cmd_approve(self, project: str, gate):
        """Approve a human gate (0, 1, 2a direction, 2b project kit)."""
        status = load_status(project)
        if "human_gates" not in status:
            status["human_gates"] = {}

        try:
            gate_id = parse_cli_gate(str(gate))
        except ValueError as exc:
            print_header(f"GATE {gate} REFUSED — {project}")
            print(f"\n  {exc}")
            return False

        ok, issues = validate_human_gate(project, gate_id)
        if not ok:
            print_header(f"GATE {gate_id} NOT READY — {project}")
            print("\n  Fix before approving:")
            for issue in issues:
                print(f"    • {issue}")
            print(f"\n  Iteration: ./studio revise {project} --gate {gate_id} --feedback \"...\"")
            return False

        blocked = previous_human_gate_block(status, gate_id)
        if blocked:
            print_header(f"GATE {gate_id} BLOCKED — {project}")
            print(f"\n  {blocked}")
            return False

        self._harvest_gate_rounds(project, gate_id)

        if gate_id == "0":
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

        if gate_id == "1":
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
            print(f"  Next: ./studio design {project} --discovery  (gate 2a — do not scaffold prototype)")
            return True

        if gate_id == "2a":
            print_header(f"HUMAN GATE 2a APPROVED: {project}")
            status["human_gates"]["2a"] = {
                "status": "approved",
                "date": datetime.now().isoformat(),
            }
            status["phase"] = PHASE_DESIGN
            status["gate"] = "2a"
            status["gate_status"] = "approved"
            save_status(project, status)
            print(f"\n  ✅ Design direction signed")
            print("  Prototype is unblocked. Style the pulled library kit to this direction.")
            if status.get("mode") == "adopt":
                print(f"  Next: token-map of what exists — ./studio design {project} --scope as-built")
            else:
                print(f"  Next: ./studio design {project} --scope journey|core-views")
            print(f"        then ./studio approve {project} --gate 2b")
            return True

        if gate_id == "2b":
            approved = {
                "status": "approved",
                "date": datetime.now().isoformat(),
            }
            print_header(f"HUMAN GATE 2b APPROVED: {project}")
            status["human_gates"]["2b"] = approved
            status["human_gates"]["2"] = approved
            status["phase"] = PHASE_SPRINT
            status["gate"] = "2b"
            status["gate_status"] = "approved"
            save_status(project, status)

            if status.get("mode") == "adopt":
                print(f"\n  ✅ Token-map of what exists approved")
                print("  Do not copy project UI into studio-library.")
                print(f"  Next: draft docs/phases/ from as-built gap matrix")
                print(f"        ./studio approve {project} --milestones")
                return True

            from pre_impl_workflow import materialize_baseline
            from studio_design_discovery import NO_UI_ARCHETYPE, project_archetype

            if project_archetype(PROJECTS_DIR / project) != NO_UI_ARCHETYPE:
                print("\n  Materializing prototype into the product app (prototype stays the baseline)...")
                for path in materialize_baseline(project):
                    try:
                        print(f"  ✓ {path.relative_to(PROJECTS_DIR / project)}")
                    except ValueError:
                        print(f"  ✓ {path}")

            print(f"\n  Generating tickets from approved PRD + design...")
            if not self._run_ticket_manifest(project):
                return False

            print("\n  Project look stays in the project. Studio-library is Headless primitives only.")
            print("  (Do not promote this product's visual system into studio-library.)")

            print(f"\n  ✅ Design system approved — tickets created")
            print(f"  Next: ./studio sprint {project}")
            return True

        print(f"  ⚠️  Unknown gate: {gate} (use 0, 1, 2a, or 2b)")
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
            from studio_milestones import activate_next, active_milestone

            if not active_milestone(project, status):
                activate_next(project, status)
            elif not (status.get("milestones") or {}).get("active"):
                activate_next(project, status)
            save_status(project, status)
            print(f"  Active milestone: {(status.get('milestones') or {}).get('active')}")
        return ok

    def cmd_milestone(self, project: str, action: str = "", notes: str = "", next_: bool = False) -> bool:
        """Milestone ownership: plan | review | --approve | plan --next (PM-002)."""
        from studio_milestones import (
            activate_next,
            active_milestone,
            approve_review,
            coverage_issues,
            list_milestones,
            milestone_complete,
            milestone_tickets,
            planned_ticket_lines,
            pm_card_lines,
            replace_plan_line,
            roadmap_approved,
            review_state,
            stamp_milestone,
            write_review,
        )

        status = load_status(project)
        if not (PROJECTS_DIR / project).exists():
            print(f"\n  ❌ Project '{project}' not found.")
            return False
        rows = list_milestones(project)
        if not action:
            print_header(f"MILESTONES — {project}")
            if not rows:
                print("  No M<n>-*.md in docs/phases/. Draft from studio-templates/phases/milestone.md.")
            for row in rows:
                tickets = milestone_tickets(project, row["id"])
                done = sum(1 for t in tickets if t["status"] == "done")
                print(f"  {row['id']:4} {row['status']:8} {row['title'][:48]:48} tickets {done}/{len(tickets)}")
            print(f"\n  Roadmap approved: {'yes' if roadmap_approved(status) else 'no'}  active: {active_milestone(project, status) or '-'}")
            missing = coverage_issues(project)
            if missing:
                print("  Coverage gaps:")
                for m in missing:
                    print(f"    - {m}")
            return True

        if not roadmap_approved(status):
            print(f"\n  ❌ Roadmap not approved. Draft docs/phases/ and run ./studio approve {project} --milestones")
            return False

        if action == "approve":
            mid = active_milestone(project, status)
            if not mid:
                print("\n  ❌ No active milestone to approve.")
                return False
            ok, messages = approve_review(project, status, mid, notes=notes)
            for m in messages:
                print(f"  {m}")
            if not ok:
                return False
            save_status(project, status)
            print(f"\n  ✅ {mid} approved as done.")
            print(f"  Next: ./studio milestone {project} plan --next")
            return True

        if action == "review":
            mid = active_milestone(project, status)
            if not mid:
                print("\n  ❌ No active milestone.")
                return False
            if not milestone_complete(project, mid):
                open_rows = [t for t in milestone_tickets(project, mid) if t["status"] not in ("done", "cancelled")]
                print(f"\n  ❌ {mid} still has {len(open_rows)} open ticket(s) — review runs when every ticket is done or cancelled.")
                return False
            print_header(f"MILESTONE REVIEW — {project} {mid}")
            for line in pm_card_lines("review"):
                print(line)
            path = write_review(project, status, mid)
            save_status(project, status)
            print(f"\n  Review written: {path.relative_to(PROJECTS_DIR / project)}")
            print("  Fill `## Roadmap changes` and `## Catalog applied`, edit M<n>-*.md if the order changes, then HITL:")
            print(f"  ./studio milestone {project} --approve --notes \"...\"")
            return True

        if action == "plan":
            if next_:
                current = active_milestone(project, status)
                if current and review_state(project, status, current) != "approved":
                    print(f"\n  ❌ {current} is not approved. Run review, then --approve, before plan --next.")
                    return False
                mid = activate_next(project, status)
                if not mid:
                    print("\n  ✅ Every milestone is done. The roadmap is complete.")
                    save_status(project, status)
                    return True
                save_status(project, status)
                print(f"  Activated {mid}.")
            mid = active_milestone(project, status)
            if not mid:
                print("\n  ❌ No active milestone. Use plan --next.")
                return False
            row = next((r for r in rows if r["id"] == mid), None)
            if not row:
                print(f"\n  ❌ {mid} has no file in docs/phases/.")
                return False
            print_header(f"MILESTONE PLAN — {project} {mid}")
            for line in pm_card_lines("plan"):
                print(line)
            text = row["file"].read_text(encoding="utf-8")
            lines = planned_ticket_lines(text)
            if not lines:
                existing = milestone_tickets(project, mid)
                if existing:
                    print(f"\n  {mid} already has {len(existing)} ticket(s); nothing new under ## Tickets.")
                else:
                    print(f"\n  No `- <title> :: <scope>` lines under ## Tickets in {row['file'].name}. Write them, then rerun.")
                print(f"  Then: ./studio groom {project} && ./studio sprint {project}")
                return bool(existing)
            created = 0
            for title, scope in lines:
                before = set(p.name for p in (PROJECTS_DIR / project / "backlog" / "open").glob("*.md")) if (PROJECTS_DIR / project / "backlog" / "open").exists() else set()
                ok = self.cmd_ticket(project, f"{title}. {scope}".strip(". ") if scope else title)
                if not ok:
                    continue
                after = (PROJECTS_DIR / project / "backlog" / "open").glob("*.md")
                new = [p for p in after if p.name not in before]
                if not new:
                    continue
                ticket_path = sorted(new)[-1]
                content = ticket_path.read_text(encoding="utf-8")
                ticket_path.write_text(stamp_milestone(content, mid), encoding="utf-8")
                tid = re.match(r"^([A-Z]+-\d+)", ticket_path.name).group(1)
                text = replace_plan_line(text, title, tid)
                created += 1
            row["file"].write_text(text, encoding="utf-8")
            from studio_milestones import set_milestone_status

            set_milestone_status(row["file"], "active")
            print(f"\n  ✅ {created} ticket(s) created and stamped milestone: {mid}")
            print(f"  Next: ./studio groom {project} && ./studio sprint {project}")
            return True

        print("  ⚠️  Use: ./studio milestone <p> [plan [--next] | review | --approve [--notes \"...\"]]")
        return False

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
    
    def cmd_ship(self, project: str, to: str = "dev", approve_prod: bool = False):
        """Push product git to origin/dev (review). main/production is HITL."""
        from studio_product_git import (
            DEV_BRANCH,
            commit_ticket,
            push_dev,
            refuse_prod_push,
            working_tree_dirty,
        )
        import subprocess

        print_header(f"SHIP — {project}")
        dest = (to or DEV_BRANCH).strip().lower() or DEV_BRANCH
        if refuse_prod_push(dest) and not approve_prod:
            print("  HITL: never auto-push main/production.")
            print(f"  Review uses origin/{DEV_BRANCH}. Production: ./studio ship {project} --to {dest} --approve")
            return False
        if working_tree_dirty(project):
            ok, msg = commit_ticket(project, "SHIP", "leftover before ship")
            print(f"  {msg}" if ok else f"  ⚠️  {msg}")
            if not ok:
                return False
        if dest == DEV_BRANCH or dest == "develop":
            ok, msg = push_dev(project)
            print(f"  {msg}")
            return ok
        if refuse_prod_push(dest) and approve_prod:
            from ship_checks import pre_ship_main_issues
            from studio_product_git import product_git_dir

            from studio_ops import readiness_blockers

            blockers = pre_ship_main_issues(PROJECTS_DIR / project, product_git_dir(project))
            blockers.extend(readiness_blockers(PROJECTS_DIR / project))
            if blockers:
                print(f"  ❌ Not shipping to {dest}:")
                for line in blockers:
                    print(f"     • {line}")
                return False

            r = subprocess.run(
                ["git", "-C", str(product_git_dir(project)), "push", "-u", "origin", f"HEAD:{dest}"],
                capture_output=True,
                text=True,
            )
            if r.returncode != 0:
                print(f"  ⚠️  {(r.stderr or r.stdout or 'push failed').strip()}")
                return False
            print(f"  Pushed HEAD → origin/{dest} (HITL approved)")
            return True
        print(f"  ⚠️  Unknown branch {dest} — use --to dev or --to main --approve")
        return False

    def cmd_sprint(self, project: str, approve_scope: bool = False, kind: str = ""):  # noqa: C901
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
            print(f"  ⚠️  Sprint requires design approval (gate 2b). Current phase: {phase}")
            return False
        
        if not design_system_approved(status):
            print(f"  ⚠️  Gate 2b (project kit) must be approved before sprint")
            return False

        if explicit_kind_is_not_hygiene(kind):
            from studio_milestones import active_milestone, roadmap_approved

            if not roadmap_approved(status):
                print(f"  ⚠️  Milestone roadmap not approved. Draft docs/phases/ then ./studio approve {project} --milestones")
                return False
            if not active_milestone(project, status):
                print(f"  ⚠️  No active milestone. Run ./studio milestone {project} plan --next")
                return False

        ok, reason = can_plan_next_sprint(project, status)
        if not ok:
            print(f"\n  ⚠️  Cannot plan next sprint yet.")
            print(f"  {reason}")
            return False
        
        print_header(f"PHASE 3: SPRINT PLANNING — {project}")

        from studio_sprint_train import (
            advance_cycle,
            cycle_of,
            first_schedulable_phase,
        )

        explicit = (kind or "").strip().lower()
        cycle = cycle_of(status)
        skipped: List[str] = []
        if explicit == "hygiene":
            chosen = "hygiene"
        else:
            if status.get("current_sprint") and (status.get("sprint_kind") or "") == "implementation":
                cycle = advance_cycle({"n": cycle["n"], "phase": "implementation"})
            start = explicit if explicit in ("design", "architecture", "implementation") else cycle["phase"]
            chosen, skipped = first_schedulable_phase(project, start)
            if not chosen:
                print("\n  No design, architecture, or implementation tickets to schedule.")
                if skipped:
                    print("  Skipped empty phases: " + ", ".join(skipped))
                return False
            cycle = {"n": cycle["n"], "phase": chosen}
            if skipped:
                print("  Skipped empty phases: " + ", ".join(skipped))

        sprints_dir = PROJECTS_DIR / project / "sprints"
        sprints_dir.mkdir(parents=True, exist_ok=True)

        existing_sprints = list(sprints_dir.glob("SPRINT-*"))
        if existing_sprints:
            numbers = [int(re.search(r'SPRINT-(\d+)', f.name).group(1)) for f in existing_sprints]
            next_num = max(numbers) + 1
        else:
            next_num = 1

        sprint_name = f"SPRINT-{next_num:02d}"
        proposal = propose_sprint_scope(
            project,
            sprint_name,
            phase="" if chosen == "hygiene" else chosen,
        )
        if chosen != "hygiene" and not proposal.get("proposed"):
            print(f"\n  {chosen} phase has no mature tickets to scope.")
            for row in proposal.get("deferred_immature") or []:
                print(f"    • {row.get('id')}: {'; '.join(row.get('questions') or [])}")
            return False

        sprint_dir = sprints_dir / sprint_name
        sprint_dir.mkdir(exist_ok=True)
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
        status["sprint_kind"] = chosen
        if status["sprint_kind"] not in ("implementation", "hygiene", "design", "architecture"):
            status["sprint_kind"] = "implementation"
        if chosen in ("design", "architecture", "implementation"):
            status["cycle"] = cycle
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

        print(f"\n  Sprint created: {sprint_name} kind={status.get('sprint_kind')} (scope **pending**)")
        print(f"  Human steps:")
        print(f"    1. Read {rel_scope}")
        print(f"    2. Edit sprints/{sprint_name}/plan.md goal if needed")
        print(f"    3. ./studio sprint {project} --approve-scope")
        print(f"    4. ./studio groom {project} --approve")
        
        return True
    
    def cmd_review(self, project: str, approve: bool = False, reject: bool = False,
                   notes: str = "", reason: str = "", inform: bool = False):
        """Prepare or complete a sprint review. `--inform` writes the brief and closes the cadence stop (HQ autonomy)."""
        status = load_status(project)
        sprint = status.get("current_sprint")
        if not sprint:
            print(f"  ⚠️  No active sprint — run ./studio sprint {project}")
            return False

        print_header(f"SPRINT REVIEW — {project} ({sprint})")

        if inform:
            summary = sprint_ticket_summary(project, sprint)
            if summary["total"] == 0 or not summary["all_done"]:
                print(f"\n  ❌ Cannot close the cadence review — sprint tickets are not all done ({summary['done']}/{summary['total']}).")
                return False
            brief = prepare_review(project, sprint, status)
            approve_review(
                project, sprint, status,
                "Cadence review closed by the agent (HQ autonomy). Human feedback is asynchronous: "
                "./studio feedback / clarify / ticket --from-feedback. Design feedback waits for the next design phase.",
            )
            hitl = get_sprint_hitl(status)
            hitl["review_mode"] = "inform"
            save_status(project, status)
            print("\n  ℹ️  INFORM: cadence review brief is ready; the train continues.")
            if brief:
                print(f"     Brief: {brief}")
            print(f"     Feedback any time: ./studio feedback {project} \"…\" [--design-reason <code>]")
            print(f"  Next: ./studio reuse {project} → ./studio retro {project} → ./studio sprint {project}")
            return True

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

    def cmd_feedback(self, project: str, text: str, source: str = "sprint-review", force: bool = False, design_reason: str = ""):
        """Capture raw human feedback — does not create a ticket."""
        if design_reason:
            from design_feedback import record_pushback, validate_reason

            err = validate_reason(design_reason)
            if err:
                print(f"  ❌ {err}")
                return False
            record_pushback(project, PROJECTS_DIR / project, "sprint-review", design_reason.strip().lower(), text, "feedback")
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
        severity: str = "",
        verbatim: Optional[List[str]] = None,
        design_reason: str = "",
    ):
        """Clarify raw feedback into an executable ticket draft."""
        if design_reason:
            from design_feedback import record_pushback, validate_reason

            err = validate_reason(design_reason)
            if err:
                print(f"  ❌ {err}")
                return False
            record_pushback(project, PROJECTS_DIR / project, fb_id, design_reason.strip().lower(), title or scope, "clarify")
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
                severity=severity,
                verbatim=verbatim or [],
            )
        except ValueError as e:
            print(f"  ⚠️  {e}")
            return False

        if not item:
            print(f"  ⚠️  {fb_id} not found — ./studio feedback-list {project}")
            return False

        print(f"\n  Status: {item['status']}")
        print(f"  Severity: {item.get('severity') or 'not set'}")
        if item.get("recurring"):
            print(f"  Recurring: raised before in {', '.join(item['recurring'])}")
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
        staffing = staff_skills(
            title,
            "\n".join(["## Scope", infer_blob]),
            skills=skills,
            ticket_type=ticket_type,
            design_status=design_status,
        )
        skills = list(staffing["skills"])
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
            from sprint_hitl import SEVERITY_PRIORITY

            severity = fb_item.get("severity") or ""
            if priority == "P1" and severity in SEVERITY_PRIORITY:
                priority = SEVERITY_PRIORITY[severity]
            quotes = fb_item.get("verbatim") or [fb_item.get("raw", "")]
            recurring = fb_item.get("recurring") or []
            rationale_extra = (
                f"\n\n## Source feedback\n"
                f"- **{from_feedback.upper()}** · severity: {severity or 'unset'} · "
                f"recurring: {', '.join(recurring) if recurring else 'first time'}\n"
                + "".join(f"> {q}\n" for q in quotes if q)
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
        ticket = apply_i18n_ticket_rules(ticket, project)
        if design_status != "n/a":
            ticket["ticket_type"] = ticket_type
            ticket["design_status"] = design_status
            ticket["design_spec"] = design_spec
        from studio_streams import needs_architecture_from_blob

        needs_arch = needs_architecture_from_blob(ticket_type, title)
        ticket["ticket_type"] = ticket_type
        ticket["needs_design"] = design_status == "pending"
        ticket["needs_architecture"] = needs_arch
        ticket["architecture_status"] = "pending" if needs_arch else "n/a"
        ticket["stream"] = (
            "production" if design_status == "pending" or needs_arch else "ready"
        )
        
        content = render_ticket_markdown(ticket)
        content += render_staffing_section(staffing)
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
        print(f"  Skills: {', '.join(skills) if skills else '(none matched — PM must staff at groom)'}")
        for skill_id, reason in staffing["added"]:
            print(f"    + {skill_id}: {reason}")
        for skill_id, reason in staffing["dropped"]:
            print(f"    ⚠️  over {len(skills)} skills, not added: {skill_id} ({reason}) — split or waive at groom")
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
            # LO-0399: the done bar applies to every ticket, not only the current sprint.
            sprint_pre = ticket_sprint or sprint_pre
            if not sprint_pre:
                print(f"\n  ❌ Cannot mark {ticket_id} done: the ticket carries no sprint, so it has no receipt, QA or finish record.")
                print(f"     Tag it through ./studio sprint {project} --approve-scope, then run the ticket through execute.")
                return False
            if True:
                rec_text_pre = ticket_file.read_text()
                if not receipt_is_complete(
                    project, sprint_pre, ticket_id, ticket_text=rec_text_pre
                ):
                    rec = receipt_path(project, sprint_pre, ticket_id)
                    print(f"\n  ❌ Cannot mark {ticket_id} done without an execution receipt.")
                    print(f"     Fill: {rec.relative_to(STUDIO_ROOT)}")
                    print(f"     ./studio receipt {project} {ticket_id}")
                    print("     Required: Plan, AC coverage, Default flow, Playbook citations, Skill QA, Security, Scope,")
                    print("     plus Evidence/A11y (UI), API proof (BE-001/003/007), Risk & rollback, Threat delta, Eval when they apply")
                    from studio_execute import receipt_blocker_messages

                    for line in receipt_blocker_messages(
                        project, sprint_pre, ticket_id, rec_text_pre
                    ):
                        print(f"     • {line}")
                    return False
                from qa_review import qa_state

                if qa_state(load_execution_log(project, sprint_pre), ticket_id) != "pass":
                    print(f"\n  ❌ Cannot mark {ticket_id} done without a QA PASS after the last green gate.")
                    print(f"     ./studio qa {project} {ticket_id}  (fresh-context reviewer writes the verdict)")
                    return False
                from qa_review import finish_state, needs_finish_gate

                if needs_finish_gate(PROJECTS_DIR / project, ticket_id) and finish_state(
                    load_execution_log(project, sprint_pre), ticket_id
                ) != "pass":
                    print(f"\n  ❌ Cannot mark {ticket_id} done before the UX-009 finish gate passes.")
                    print(f"     ./studio qa {project} {ticket_id} --finish  (shipped screen vs signed mock)")
                    return False

        if new_status == "implement":
            status_pre = load_status(project)
            blocked = implement_blocked_reason(status_pre, project)
            if blocked:
                print(blocked)
                return False
            if status_pre.get("current_sprint"):
                from qa_review import context_id

                append_execution_event(project, status_pre["current_sprint"], "implement-start", ticket_id, note=context_id())
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
                sprint_now = status.get("current_sprint") or ""
                remaining = (
                    open_sprint_ticket_ids(sprint_ticket_summary(project, sprint_now)["tickets"])
                    if sprint_now
                    else []
                )
                if remaining:
                    print(
                        f"\n  Ticket done — {len(remaining)} sprint ticket(s) still open. "
                        f"Next: ./studio execute {project}"
                    )
                else:
                    hitl_now = get_sprint_hitl(status)
                    if hitl_now.get("review_status") == "informed":
                        print(
                            f"\n  Backend-only sprint complete — review is inform-only. Next: ./studio retro {project}"
                        )
                    else:
                        print(
                            f"\n  Implementation sprint complete — skill QA on receipts; "
                            f"cadence review not due. Next: ./studio retro {project} "
                            f"(optional later: ./studio sprint {project} --kind hygiene)"
                        )
            save_status(project, status)
            sprint_done = status.get("current_sprint") or ""
            if sprint_done:
                append_execution_event(project, sprint_done, "done", ticket_id, reason or "done")
                rec = receipt_path(project, sprint_done, ticket_id)
                if rec.exists():
                    print(f"  Receipt: {rec.relative_to(PROJECTS_DIR / project)}")
                from studio_product_git import commit_ticket

                ok_git, git_msg = commit_ticket(project, ticket_id, ticket_title)
                if ok_git:
                    print(f"  Product git: {git_msg} (no push to main; review uses origin/dev)")
                else:
                    print(f"  ⚠️  Product git commit skipped: {git_msg}")
                if rec.exists():
                    try:
                        from studio_cite import apply_receipt_citations

                        cited = apply_receipt_citations(rec.read_text(encoding="utf-8", errors="ignore"))
                        if cited:
                            print(f"  Citations: {len(cited)} playbook bullet counter(s) updated")
                    except Exception as exc:
                        print(f"  ⚠️  Playbook citations skipped: {exc}")
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

    def cmd_reject_design(self, project: str, ticket_id: str, reason: str, notes: str = "") -> bool:
        """HITL push-back on a design packet: coded reason, logged, harvested, ticket back to pending."""
        from design_feedback import reason_help, record_pushback, set_design_rejected, validate_reason

        err = validate_reason(reason)
        if err:
            print(f"  ❌ {err}")
            print(reason_help())
            return False
        ticket_file, _status = find_project_ticket(project, ticket_id)
        if not ticket_file:
            print(f"  Ticket {ticket_id} not found in project {project}")
            return False
        content = ticket_file.read_text(encoding="utf-8")
        updated = set_design_rejected(content)
        updated += (
            f"\n\n## Design rejection\n- **Rejected:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
            f"- **Reason:** {reason.strip().lower()}\n- **Notes:** {notes or '-'}\n"
        )
        ticket_file.write_text(updated, encoding="utf-8")
        result = record_pushback(project, PROJECTS_DIR / project, ticket_id, reason.strip().lower(), notes, "reject")
        print(f"\n  ↩ Design rejected for {ticket_id} ({reason.strip().lower()}) — design_status back to pending")
        print(f"    Log: {Path(str(result['log'])).relative_to(STUDIO_ROOT)}")
        if result.get("created"):
            print(f"    Learning: {result.get('lo_id')} harvested to studio HQ")
        elif result.get("local_log"):
            print(f"    Project-local note: {result.get('local_log')}")
        print(f"  Next: Team 10 revises the spec and mocks in the next design phase; re-sign with ./studio approve-design {project} --phase")
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
        spec_text = spec_path.read_text(encoding="utf-8", errors="ignore") if spec_path.exists() else ""
        print()
        print(mock_review_block(PROJECTS_DIR / project, ticket_id, spec_text).replace("<project>", project))
        updated = set_design_approved(content)
        from studio_streams import refresh_stream_field

        updated = refresh_stream_field(updated)
        if notes:
            updated += f"\n\n## Design approval\n- **Approved:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n- **Notes:** {notes}\n"
        ticket_file.write_text(updated)
        print(f"\n  ✓ Design approved for {ticket_id}")
        print(f"    Spec: {spec_rel}")
        print(f"  Next: implement only after stream is ready (approve-arch if required)")
        return True

    def cmd_mock(self, project: str, ticket_id: str) -> bool:
        """Verify the interactive mock packet and print the human review script (route + §2e)."""
        ticket_file, _status = find_project_ticket(project, ticket_id)
        if not ticket_file:
            print(f"  Ticket {ticket_id} not found in project {project}")
            return False
        content = ticket_file.read_text()
        fields = parse_design_fields(content)
        spec_rel = fields.get("design_spec") or default_design_spec_path(ticket_id)
        project_root = PROJECTS_DIR / project
        spec_path = project_root / spec_rel
        tt = fields.get("ticket_type") or infer_ticket_type(content)
        err = design_spec_completeness_error(
            spec_path, project_root, ticket_id, tt, ticket_blob=content
        )
        if err:
            print(f"\n  ❌ Mock packet incomplete for {ticket_id}:")
            print(f"     {err}")
            return False
        spec_text = spec_path.read_text(encoding="utf-8", errors="ignore")
        print(f"\n  ✓ Interactive mock packet complete for {ticket_id}")
        print(mock_review_block(project_root, ticket_id, spec_text).replace("<project>", project))
        print(f"\n  Next: HITL ./studio approve-design {project} {ticket_id}")
        return True

    def cmd_ia_audit(self, project: str, ticket_id: str):
        """Print IA nav findings for a ticket spec (empty list = pass)."""
        from studio_ia_audit import format_ia_audit_report, ia_nav_findings

        ticket_file, _status = find_project_ticket(project, ticket_id)
        if not ticket_file:
            print(f"  Ticket {ticket_id} not found in project {project}")
            return False
        content = ticket_file.read_text()
        spec_match = re.search(r"^design_spec:\s*(.+)$", content, re.MULTILINE)
        spec_rel = spec_match.group(1).strip() if spec_match else default_design_spec_path(ticket_id)
        spec_path = PROJECTS_DIR / project / spec_rel
        if not spec_path.exists():
            print(f"\n  ❌ Spec not found: {spec_rel}")
            print("     Write the design spec before ./studio ia-audit")
            return False
        findings = ia_nav_findings(spec_path.read_text(encoding="utf-8", errors="ignore"))
        print(f"\n  {format_ia_audit_report(findings)}")
        print(f"    Spec: {spec_rel}")
        return not findings

    def cmd_approve_arch(self, project: str, ticket_id: str, notes: str = ""):
        """HITL: approve architecture packet before implementation sprint."""
        from studio_streams import architecture_packet_ready, set_architecture_approved

        ticket_file, _status = find_project_ticket(project, ticket_id)
        if not ticket_file:
            print(f"  Ticket {ticket_id} not found in project {project}")
            return False
        content = ticket_file.read_text()
        if not re.search(r"^architecture_status:\s*pending", content, re.M):
            print(f"  Ticket {ticket_id} does not need architecture sign-off.")
            return True
        packet_issues = architecture_packet_issues(project, ticket_id)
        if packet_issues:
            print(f"\n  ❌ Cannot approve-arch {ticket_id}:")
            for line in packet_issues:
                print(f"     • {line}")
            return False
        updated = set_architecture_approved(content)
        if notes:
            updated += f"\n\n## Architecture approval\n- **Approved:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n- **Notes:** {notes}\n"
        ticket_file.write_text(updated)
        print(f"\n  ✓ Architecture approved for {ticket_id}")
        print(f"    Note: docs/architecture/{ticket_id}.md")
        return True

    def _release_train_phase(self, project: str) -> None:
        """Untag the current phase and point the cycle at the next one."""
        from backlog_paths import clear_ticket_sprint, queue_ticket_paths, read_ticket_meta
        from studio_sprint_train import advance_cycle, cycle_of

        status = load_status(project)
        sprint = status.get("current_sprint") or ""
        if sprint:
            for path in queue_ticket_paths(project):
                meta = read_ticket_meta(path)
                if meta.get("sprint") != sprint:
                    continue
                path.write_text(clear_ticket_sprint(path.read_text(encoding="utf-8")), encoding="utf-8")
        cycle = cycle_of(status)
        cycle["phase"] = (status.get("sprint_kind") or cycle["phase"])
        status["cycle"] = advance_cycle(cycle)
        status["current_sprint"] = ""
        save_status(project, status)
        print(f"  Cycle {status['cycle']['n']} next phase: {status['cycle']['phase']}")
        print(f"  Next: ./studio sprint {project}")

    def cmd_approve_design_phase(self, project: str) -> bool:
        """Sign every written design packet in the current phase, then open the next phase."""
        from sprint_hitl import list_sprint_tickets
        from studio_sprint_train import architecture_delta
        from studio_streams import refresh_stream_field

        status = load_status(project)
        sprint = status.get("current_sprint") or ""
        if not sprint:
            print("  No current sprint.")
            return False
        blocked = []
        for ticket in list_sprint_tickets(project, sprint):
            ticket_file, _ = find_project_ticket(project, ticket["id"])
            if not ticket_file:
                continue
            content = ticket_file.read_text(encoding="utf-8")
            if re.search(r"^design_status:\s*approved\b", content, re.M):
                continue
            if not requires_design_approval(content):
                continue
            if architecture_delta(content) is None:
                blocked.append(f"{ticket['id']}: missing architecture delta")
                continue
            fields = parse_design_fields(content)
            spec_match = re.search(r"^design_spec:\s*(.+)$", content, re.MULTILINE)
            spec_rel = spec_match.group(1).strip() if spec_match else default_design_spec_path(ticket["id"])
            err = design_spec_completeness_error(
                PROJECTS_DIR / project / spec_rel,
                PROJECTS_DIR / project,
                ticket["id"],
                fields.get("ticket_type", ""),
                ticket_blob=content,
            )
            if err:
                blocked.append(f"{ticket['id']}: {err}")
                continue
            ticket_file.write_text(refresh_stream_field(set_design_approved(content)), encoding="utf-8")
            print(f"  ✓ Design approved for {ticket['id']}")
        if blocked:
            print("\n  Design phase is not ready to release:")
            for line in blocked:
                print(f"    • {line}")
            return False
        self._release_train_phase(project)
        return True

    def cmd_approve_arch_phase(self, project: str) -> bool:
        """Sign every written architecture note in the current phase, then open the next phase."""
        from sprint_hitl import list_sprint_tickets
        from studio_streams import architecture_packet_issues, set_architecture_approved

        status = load_status(project)
        sprint = status.get("current_sprint") or ""
        if not sprint:
            print("  No current sprint.")
            return False
        blocked = []
        for ticket in list_sprint_tickets(project, sprint):
            ticket_file, _ = find_project_ticket(project, ticket["id"])
            if not ticket_file:
                continue
            content = ticket_file.read_text(encoding="utf-8")
            if not re.search(r"^architecture_status:\s*pending\b", content, re.M):
                continue
            packet_issues = architecture_packet_issues(project, ticket["id"])
            if packet_issues:
                blocked.append(f"{ticket['id']}: " + "; ".join(packet_issues))
                continue
            ticket_file.write_text(set_architecture_approved(content), encoding="utf-8")
            print(f"  ✓ Architecture approved for {ticket['id']}")
        if blocked:
            print("\n  Architecture phase is not ready to release:")
            for line in blocked:
                print(f"    • {line}")
            return False
        status = load_status(project)
        status["arch_auto_signed"] = {"sprint": sprint, "at": datetime.now().isoformat(), "by": "agent"}
        save_status(project, status)
        print("\n  ℹ️  INFORM: architecture phase signed by the agent (HQ autonomy).")
        print(f"     Tech-veto window: ./studio veto {project} --decision <TICKET> --reason \"…\" stops execute at the next IMPLEMENT boundary.")
        self._release_train_phase(project)
        return True

    def cmd_reject_arch(self, project: str, ticket_id: str, reason: str = "") -> bool:
        """The signed design cannot be built. Send it to the next design cycle."""
        from studio_sprint_train import mark_architecture_rejected

        ticket_file, _status = find_project_ticket(project, ticket_id)
        if not ticket_file:
            print(f"  Ticket {ticket_id} not found in project {project}")
            return False
        ticket_file.write_text(
            mark_architecture_rejected(ticket_file.read_text(encoding="utf-8"), reason),
            encoding="utf-8",
        )
        print(f"\n  ✓ {ticket_id} returned to the next design cycle")
        print("    It is out of this implementation scope.")
        return True

    # -------------------------------------------------------------------------
    # PHASE 4-5: QA GATE
    # -------------------------------------------------------------------------
    
    def cmd_gate(self, project: str, level: int = 5, anti_slop: bool = False):
        """Run the QA gate."""
        from studio_status import is_valid_project_slug

        if not is_valid_project_slug(project):
            print("  Usage: ./studio gate <project> [--level N] [--anti-slop]")
            print("  --help / flags are not project names.")
            return False
        
        print_header(f"PHASE 5: QA-GATE — {project} (Level {level})")

        if not docker_cli_available():
            print(docker_install_hint())
            return False
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
        print(redact_secret_patterns(result.stdout or ""))
        if result.stderr:
            print(redact_secret_patterns(result.stderr))
        
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
        excerpt = redact_secret_patterns((result.stdout or "")[-1500:])
        if sprint and ticket_id:
            if result.returncode == 0:
                append_execution_event(project, sprint, "gate-pass", ticket_id)
            else:
                from receipt_checks import latest_qa_report
                from run_qa_gate import SOFT_CHECKS

                report = latest_qa_report(PROJECTS_DIR / project) or {}
                failed = [
                    r for r in report.get("results") or []
                    if not r.get("passed") and r.get("check") not in SOFT_CHECKS
                ]
                signature = failure_signature(failed)
                fails = self._record_failure(
                    project, sprint, ticket_id, "gate-fail",
                    f"gate red: {signature}" if signature else "gate red",
                    symptom=f"QA gate level {level} failed", excerpt=excerpt, failed_checks=failed,
                )
                if fails >= MAX_GATE_RETRIES:
                    if not existing_gate_fail_lo(project):
                        lo_id = self.cmd_learn(
                            f"Gate fail retry exhausted ({ticket_id})",
                            "gate-fail",
                            project,
                        )
                        print(f"  Auto-harvested {lo_id} — spawn ./studio train beside product execute")

        return result.returncode == 0

    def _record_failure(
        self,
        project: str,
        sprint: str,
        ticket_id: str,
        event: str,
        note: str,
        *,
        symptom: str,
        excerpt: str = "",
        failed_checks=None,
        findings: str = "",
    ) -> int:
        """Log a red gate or QA FAIL, write the structured debug attempt, escalate when due."""
        append_execution_event(project, sprint, event, ticket_id, note)
        log = load_execution_log(project, sprint)
        fails = count_gate_fails(log, ticket_id)
        repeated = repeated_failure(log, ticket_id)
        dbg = append_debug_attempt(
            project, sprint, ticket_id, fails, symptom, excerpt,
            failed_checks=failed_checks, findings=findings, repeated=repeated,
        )
        print(f"\n  Debug log: {dbg.relative_to(STUDIO_ROOT)}")
        if should_escalate(log, ticket_id):
            why = f"failed {fails} times" if fails >= MAX_GATE_RETRIES else "failed twice the same way"
            esc = write_escalation(project, sprint, ticket_id, why)
            print(f"  Escalate: {why}. Packet: {esc.relative_to(STUDIO_ROOT)}")
            print(f"  ./studio move {project} {ticket_id} blocked — independent tickets continue")
        else:
            print(f"  Retry {fails}/{MAX_GATE_RETRIES}: fix only the listed issues, then ./studio gate {project} --level 5")
        return fails

    def cmd_reality_check(self, project: str, check: bool = False):
        """Release reality check (L11, SO-005): write the brief + template, or validate the report."""
        from reality_check import brief, head_sha, report_issues, report_path, template
        from sprint_hitl import list_sprint_tickets, sprint_directory

        status = load_status(project)
        sprint = status.get("current_sprint") or ""
        if not sprint:
            print("  No current sprint.")
            return False
        sdir = sprint_directory(project, sprint)
        path = report_path(sdir)
        rel = str(path.relative_to(STUDIO_ROOT))
        print_header(f"REALITY CHECK {project} {sprint}")
        if check:
            if not path.exists():
                print(f"  ❌ {rel} missing — run ./studio reality-check {project}")
                return False
            issues = report_issues(path.read_text(encoding="utf-8"), sdir)
            if issues:
                for line in issues:
                    print(f"  • {line}")
                return False
            print(f"  ✓ {rel} is complete. ./studio execute {project}")
            return True
        if not path.exists():
            done = [t["id"] for t in list_sprint_tickets(project, sprint) if t.get("status") == "done"]
            (sdir / "reality-check").mkdir(parents=True, exist_ok=True)
            path.write_text(template(sprint, head_sha(PROJECTS_DIR / project) or "", done), encoding="utf-8")
        print(brief(project, sprint, rel))
        return True

    def cmd_qa_finish(self, project: str, ticket_id: str, decision: str = ""):
        """UX-009 finish gate (L9): shipped screen vs signed mock. HOLD is a QA fail."""
        from qa_review import (
            finish_file_issues,
            finish_path,
            finish_template,
            mock_shots,
            qa_state,
        )
        from sprint_hitl import sprint_directory

        status = load_status(project)
        sprint = status.get("current_sprint") or ""
        if not sprint:
            print("  No current sprint — the finish gate runs on sprint tickets.")
            return False
        project_root = PROJECTS_DIR / project
        shots = mock_shots(project_root, ticket_id)
        if not shots:
            print(f"  {ticket_id} has no signed mock screenshots — no finish gate needed.")
            return True
        sprint_dir = sprint_directory(project, sprint)
        path = finish_path(sprint_dir, ticket_id)
        print_header(f"UI FINISH GATE {ticket_id}")
        if decision in ("", "BRIEF"):
            if qa_state(load_execution_log(project, sprint), ticket_id) != "pass":
                print(f"  ❌ Run the QA review first: ./studio qa {project} {ticket_id}")
                return False
            path.parent.mkdir(parents=True, exist_ok=True)
            (sprint_dir / "qa" / f"{ticket_id}-finish").mkdir(parents=True, exist_ok=True)
            if not path.exists():
                path.write_text(finish_template(ticket_id, sprint, shots), encoding="utf-8")
            print(f"  Skill: teams/10-product-design-experience/skills/ui-finish-gate.md (UX-009)")
            print(f"  Mock:  projects/{project}/docs/design-specs/mocks/{ticket_id}/ ({len(shots)} shots)")
            print(f"  Capture the shipped route with Playwright under the same names into")
            print(f"         {(sprint_dir / 'qa' / (ticket_id + '-finish')).relative_to(STUDIO_ROOT)}/")
            print(f"  Fill:  {path.relative_to(STUDIO_ROOT)}  (Comparison, Keep, Required before PASS)")
            print("  Any visible difference is HOLD, even one that looks better.")
            print(f"  Then: ./studio qa {project} {ticket_id} --finish PASS|HOLD")
            return True
        if decision not in ("PASS", "HOLD"):
            print("  --finish must be PASS or HOLD")
            return False
        if not path.exists():
            print(f"  ❌ {path.relative_to(STUDIO_ROOT)} missing — run ./studio qa {project} {ticket_id} --finish first")
            return False
        text = path.read_text(encoding="utf-8")
        issues = finish_file_issues(text, decision, sprint_dir, project_root, ticket_id)
        if issues:
            print("  ❌ The finish-gate file does not back this decision:")
            for line in issues:
                print(f"     • {line}")
            return False
        if decision == "PASS":
            append_execution_event(project, sprint, "finish-pass", ticket_id)
            print(f"  ✅ Finish gate PASS recorded. Next: ./studio execute {project}")
            return True
        from receipt_checks import section as _section

        required = (_section(text, "Required before PASS") or "").strip()
        first = re.search(r"^\s*\d+\.\s*([^\n]+)", required, re.M)
        keep = (_section(text, "Keep") or "").strip()
        from design_feedback import finish_hold_code, record_pushback

        hold_note = first.group(1).strip() if first else "finish gate HOLD"
        record_pushback(project, project_root, ticket_id, finish_hold_code(text), hold_note, "finish-hold")
        self._record_failure(
            project, sprint, ticket_id, "qa-fail",
            f"finish hold: {first.group(1).strip()[:80]}" if first else "finish hold",
            symptom="UX-009 finish gate HOLD",
            findings=f"{required}\n\nKeep (do not regress):\n{keep}",
        )
        return True

    def cmd_qa(self, project: str, ticket_id: str, verdict: str = ""):
        """Independent QA review (L2): print the reviewer brief, or record its verdict."""
        from qa_review import (
            findings_for_debug,
            qa_path,
            qa_template,
            reviewer_brief,
            verdict_file_issues,
        )
        from sprint_hitl import sprint_directory

        status = load_status(project)
        sprint = status.get("current_sprint") or ""
        if not sprint:
            print("  No current sprint — QA review runs on sprint tickets.")
            return False
        card = ticket_card_for(project, ticket_id)
        if not card:
            print(f"  Ticket not found: {ticket_id}")
            return False
        path = qa_path(sprint_directory(project, sprint), ticket_id)
        receipt = receipt_path(project, sprint, ticket_id)
        print_header(f"QA REVIEW {ticket_id}")
        if not verdict:
            log = load_execution_log(project, sprint)
            from studio_execute import has_fresh_gate_pass

            if not has_fresh_gate_pass(log, ticket_id):
                print(f"  ❌ No fresh green gate for {ticket_id}. Run ./studio gate {project} --level 5 first.")
                return False
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(qa_template(ticket_id, card.get("ac") or []), encoding="utf-8")
            print(reviewer_brief(
                project, ticket_id, card,
                receipt_rel=str(receipt.relative_to(STUDIO_ROOT)),
                qa_rel=str(path.relative_to(STUDIO_ROOT)),
                ticket_rel=str(card.get("path") or ""),
            ))
            print(f"  Then: ./studio qa {project} {ticket_id} --verdict PASS|FAIL")
            return True
        verdict = verdict.upper()
        if verdict not in ("PASS", "FAIL"):
            print("  --verdict must be PASS or FAIL")
            return False
        if not path.exists():
            print(f"  ❌ {path.relative_to(STUDIO_ROOT)} missing — run ./studio qa {project} {ticket_id} first")
            return False
        text = path.read_text(encoding="utf-8")
        from qa_review import implementer_id, reviewer_identity_issues

        issues = verdict_file_issues(text, verdict)
        issues += reviewer_identity_issues(text, implementer_id(load_execution_log(project, sprint), ticket_id))
        if issues:
            print("  ❌ The verdict file does not back this verdict:")
            for line in issues:
                print(f"     • {line}")
            return False
        if verdict == "PASS":
            append_execution_event(project, sprint, "qa-pass", ticket_id)
            print(f"  ✅ QA PASS recorded. Next: ./studio execute {project}")
            return True
        findings = findings_for_debug(text)
        first = re.search(r"Issue\s*:\s*([^\n]+)", findings)
        self._record_failure(
            project, sprint, ticket_id, "qa-fail",
            f"qa fail: {first.group(1).strip()[:80]}" if first else "qa fail",
            symptom="QA reviewer FAIL", findings=findings,
        )
        return True
    
    # -------------------------------------------------------------------------
    # PHASE 6: LEARNING
    # -------------------------------------------------------------------------
    
    def cmd_learn(
        self,
        title: str,
        signal: str,
        source: str = "Studio Development",
        *,
        verdict: str = "",
        reason: str = "",
        assumed: str = "",
        signed: str = "",
        next_rule: str = "",
        target: str = "",
    ):
        """Capture a learning as a local LO, or fill the verdict on an existing LO-NNNN."""
        from studio_harvest import harvest_identified_learning

        if re.fullmatch(r"LO-\d{4}", title.strip().upper()):
            from studio_lesson import set_lesson_verdict

            lo_id = title.strip().upper()
            if not verdict:
                print(f"\n  {lo_id}: give the verdict — --verdict studio|project --reason \"…\" --assumed \"…\" --signed \"…\" [--next \"…\" --target <file>]")
                return ""
            try:
                result = set_lesson_verdict(
                    lo_id,
                    verdict=verdict,
                    reason=reason,
                    assumed=assumed,
                    signed=signed,
                    next_rule=next_rule,
                    target=target,
                )
            except (ValueError, FileNotFoundError) as exc:
                print(f"\n  ❌ {lo_id}: {exc}")
                return ""
            if result["verdict"] == "project":
                print(f"\n  {lo_id} judged project-specific — {reason}")
                print(f"  Logged: {result.get('local_log') or '(no project folder resolved from source)'}; LO removed.")
                print("  The human can overrule from the TRAIN_DUE list: ./studio train --promote <project> --topic \"<title>\"")
                return ""
            print(f"\n  {lo_id} verdict: studio — {reason}")
            print(f"  Target: {result['target']}  (severity floor {result['severity_floor']})")
            print("  Training chat: ./studio train " + lo_id)
            return lo_id

        result = harvest_identified_learning(
            title,
            source=source,
            signal=signal,
            observation=title,
            assumed=assumed,
            signed=signed,
            verdict=verdict,
            reason=reason,
            next_rule=next_rule,
            target=target,
        )
        if result.get("project_verdict"):
            print(f"\n  Judged project-specific — {reason}")
            print(f"  Logged: {result.get('local_log') or '(no project folder resolved from --source)'}. No studio LO.")
            return ""
        if result.get("dropped"):
            print(f"\n  Learning dropped (not studio-portable): {title[:80]}")
            print(f"  Reason: {result.get('reason')}")
            if result.get("local_log"):
                print(f"  Project log: {result['local_log']}")
            else:
                print("  Rewrite as a reusable must/should/never rule, or keep it in the project local log.")
            return ""
        lo_id = result["lo_id"]
        if result.get("created"):
            print(f"\n  Learning captured: {lo_id}")
        else:
            print(f"\n  Learning already open: {lo_id} (deduped)")
        print(f"  Kind: {result.get('kind')} → target {result.get('infusion_path')}")
        print(f"  Signal: {result.get('signal')}")
        if result.get("needs_verdict"):
            print("  Candidate only. Fill the verdict before the retro can close:")
            print(f"    ./studio learn {lo_id} --verdict studio|project --reason \"…\" --assumed \"…\" --signed \"…\" --next \"…\" [--target <file>]")
        else:
            print(f"  Ready for a training chat: ./studio train {lo_id}")
        print("  Product execute continues IMPLEMENT; open LOs do not block.")
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

        from studio_lesson import needs_verdict

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
            extra += " needs-verdict" if needs_verdict(content) else ""
            print(f"  - {lo.stem} [Signal: {signal}{extra}]")
        self._print_train_due()
        print("\n  Next: ./studio execute <project> continues IMPLEMENT; a training chat runs ./studio train <LO>")
        print("  Find infused rules: ./studio learn-find \"<topic>\"")

    def cmd_learn_find(self, query: str):
        """Search infused PB- bullets where the agent reads them: playbooks, process files, skills."""
        from studio_lesson import SEARCH_GLOBS, search_pb_bullets

        print_header("INFUSED RULES")
        hits = search_pb_bullets(query)
        if not hits:
            print(f"\n  No PB- bullet matches {query!r} in {', '.join(SEARCH_GLOBS)}")
            return False
        for hit in hits:
            print(f"  {hit['path']}")
            print(f"    {hit['line']}")
        return True

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
            from studio_harvest import harvest_retro_text, open_candidates

            retro_path = PROJECTS_DIR / project / "sprints" / sprint / "retro.md"
            harvest_key = f"retro_harvested_{sprint}"
            if retro_path.exists() and not hitl.get(harvest_key):
                harvested = harvest_retro_text(
                    retro_path.read_text(encoding="utf-8", errors="ignore"), project
                )
                hitl[harvest_key] = True
                save_status(project, status)
                created = [h for h in harvested if h.get("created")]
                dropped = [h for h in harvested if h.get("dropped")]
                skipped = [h for h in harvested if not h.get("created") and not h.get("dropped")]
                if created or skipped or dropped:
                    print("\n  Retro harvest — lesson candidates (portable lines only):")
                    for h in created:
                        print(f"    {h.get('lo_id')} [{h.get('kind')}] → {h.get('infusion_path')}")
                    for h in skipped:
                        print(f"    {h.get('lo_id')} already open (deduped)")
                    for h in dropped:
                        print(f"    dropped (project-local): {h.get('reason')}")

            candidates = open_candidates()
            if candidates:
                print(f"\n  ❌ Retro stays open: {len(candidates)} lesson candidate(s) have no verdict.")
                print("  For each one answer: did the definition change because of this product, or because the studio default was wrong?")
                for path in candidates:
                    lo_id = re.search(r"(LO-\d{4})", path.name)
                    lid = lo_id.group(1) if lo_id else path.stem
                    print(f"    {lid}  {path.name}")
                    print(f"      ./studio learn {lid} --verdict studio --reason \"…\" --assumed \"…\" --signed \"…\" --next \"<rule as a bullet>\" [--target <studio file>]")
                    print(f"      ./studio learn {lid} --verdict project --reason \"…\" --assumed \"…\" --signed \"…\"")
                print(f"  Then: ./studio retro {project} --complete")
                return False

            hitl["retro_status"] = RETRO_DONE
            hitl["retro_completed_at"] = datetime.now().isoformat()
            save_status(project, status)
            print(f"\n  ✅ Retro complete: {message}")
            self._print_train_due(project)
            print(f"\n  Product loop continues: ./studio execute {project}  → IMPLEMENT (not STUDIO_LO)")
            print("  Studio lessons wait for a training chat; they do not run inside the product sprint.")
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

        print_header("STUDIO INFUSION")
        from studio_train import sync_train_with_done_los, open_jobs, sidecar_commands

        synced = sync_train_with_done_los()
        if synced:
            print(f"\n  Closed {len(synced)} train job(s) for LOs already in backlog/done/")
        items = open_lo_tickets()
        hq_hits = scan_hq_for_project_nouns()
        bad_titles = open_lo_title_portability_failures(items) if items else []
        if not items and not hq_hits:
            print("\n  ✅ No open LO tickets — safe to plan the next project sprint.")
            print("  Portability: no project folder names found in HQ playbooks/skills (excl. CHANGELOG).")
            print("  A lesson lands as a PB- bullet in the playbook, process file, skill, template, or tool it changes.")
            self._print_train_due()
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
            print("    Replace product names and ticket IDs with <project> / <ticket>; HQ has no provenance exception.")
        print("\n  Infusion targets (the file the next project follows):")
        print("    knowledge-base/*.md playbooks · process/ · teams/*/skills/ · studio-templates/ · studio-tools/ · studio-library/")
        self._print_train_due()
        print("\n  Product: ./studio execute <project>  → IMPLEMENT")
        if items:
            print("  Train:   ./studio train <LO>  → Impact block; low infuses, high waits for --approve / --defer")
            print("           ./studio infusion-delta --lo <LO> --path <target> --op add --body \"assumed: … signed: … next: …\"")
            print("           CHANGELOG line → ./studio train --done <LO>")
            queued = sidecar_commands(4)
            if queued:
                print("  Open train jobs (oldest first):")
                for q in queued:
                    print(f"    {q.get('id')} {q.get('command')}")
        return not bad_titles
    
    def cmd_update_skills(self, extra_args=None):
        """Subscribe/update the external skill dependencies (agent-as-a-dependency)."""
        if extra_args and extra_args[0] == "payload":
            from payload_foundation import refresh_payload_skills

            print_header("PAYLOAD SKILL")
            ok, detail = refresh_payload_skills()
            if ok:
                print("\n  Refreshed from https://github.com/payloadcms/skills")
                print("  teams/02-backend-systems/skills/payload/")
                print("  teams/02-backend-systems/skills/cms-migration/")
                return True
            print(f"\n  ❌ Payload skill refresh failed: {detail}")
            return False

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

    def _run_docker_compose(
        self,
        project: str,
        *compose_args: str,
        attach: bool = False,
        inject: bool = False,
    ) -> bool:
        """Run docker compose with project name (-p) so containers are <project>-*, not docker-*."""
        docker_dir = self._docker_dir(project)
        compose_file = docker_dir / "docker-compose.yml"
        if not compose_file.exists():
            rel = compose_file.relative_to(PROJECTS_DIR)
            print(f"\n  ❌ Missing {rel}")
            print(f"  Run: ./studio env {project} init")
            return False

        if not docker_cli_available():
            print(docker_install_hint())
            return False

        names = merged_schema_names(project, PROJECTS_DIR)
        env_file = ensure_project_env_file(project, PROJECTS_DIR, names=names)
        assignments = parse_env_assignments(env_file.read_text(encoding="utf-8"))
        redaction = secret_values_for_redaction(assignments)
        if inject:
            print(inject_summary(project, names, env_file))

        from payload_foundation import compose_extras

        extra_files, profiles = compose_extras(project, getattr(self, "_env_profiles", ()))
        cmd = compose_argv(
            project,
            docker_dir,
            compose_file,
            env_file,
            compose_args,
            extra_files=extra_files,
            profiles=profiles,
        )
        print(f"  → {public_command_line(cmd)}")
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
                    print(redact_output(result.stdout.rstrip(), redaction))
                if result.stderr:
                    print(redact_output(result.stderr.rstrip(), redaction))
            if result.returncode != 0:
                print(f"\n  ❌ docker compose failed (exit {result.returncode})")
                return False
            return True
        except FileNotFoundError:
            print("\n  ❌ Docker CLI not found.")
            print("  Install Docker Desktop: https://docs.docker.com/get-docker/")
            return False

    def cmd_env(self, project: str, action: str, approve: bool = False, profiles: list | None = None):
        """Manage the Docker environment (runs docker compose -p <project>)."""
        self._env_profiles = list(profiles or [])
        docker_dir = self._docker_dir(project)
        
        print_header(f"DOCKER ENV: {project}")

        if action == "prod":
            from studio_ops import ensure_prod_env_file, explain_prod_env

            root = PROJECTS_DIR / project
            ensure_prod_env_file(project, root)
            print()
            print(explain_prod_env(project, root))
            return True

        if action in INJECT_ACTIONS:
            from studio_env import inform_local_inject

            print(inform_local_inject(project, action))
        
        if action == "init":
            docker_dir.mkdir(parents=True, exist_ok=True)
            
            # Copy the base template from the studio and parametrize per project
            template_dir = TEMPLATES_DIR / "docker"
            if not template_dir.exists():
                print(f"\n  ⚠️  Base docker template missing: {template_dir}")
                return False
            
            for f in template_dir.iterdir():
                if f.is_file():
                    target = docker_dir / f.name
                    if target.exists():
                        continue
                    content = f.read_text()
                    content = content.replace("{{PROJECT_NAME}}", project)
                    target.write_text(content)
            
            print(f"\n  Docker environment initialized: {docker_dir}")
            print(f"  Base template: {template_dir}")
            print(f"  → docker-compose.yml, .env.example (project-parametrized)")
            print(f"\n  Add project-specific services (Mailpit, MinIO, ...) here:")
            print(f"    {docker_dir}/docker-compose.yml")
            print(f"\n  Next step:")
            print(f"    ./studio env {project} up --approve")
        
        elif action == "up":
            print(f"\n  Starting the local stack for **{project}** (Postgres, and the Payload app when it exists)…")
            if not self._run_docker_compose(project, "up", "-d", inject=True):
                return False
            print(f"\n  Status:")
            self._run_docker_compose(project, "ps")
            print(f"\n  Next: ./studio env {project} migrate --approve")
            return True

        elif action == "migrate":
            print(f"\n  Bringing Compose up, then running payload migrate for **{project}**…")
            if not self._run_docker_compose(project, "up", "-d", inject=True):
                return False
            override = docker_dir / "payload-app.compose.yml"
            if not override.exists():
                print("  No Payload app yet. Sign gate 1 with `Payload: in`, then ./studio execute.")
                return True
            return self._run_docker_compose(
                project, "exec", "-T", "app", "npm", "run", "migrate"
            )

        elif action == "dev":
            print(f"\n  Starting the same local stack as up for **{project}**…")
            if not self._run_docker_compose(project, "up", "-d", inject=True):
                return False
            print("  App container runs next dev. Open the published APP_HOST_PORT.")
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
            print(f"  Usage: ./studio env {project} init|up|down|status|logs|migrate|dev [--approve]")
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
                print(f"  Example: ./studio repo {project} link https://github.com/<owner>/{project}.git")
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
            "promoted": datetime.now().strftime("%Y-%m-%d"),
            "title": asset_name,
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
  ./studio ship <project> --to dev               Push product git to origin/dev (before review)
  ./studio ship <project> --to main --approve    Production push — HITL only
  ./studio settings [--reset-usage]              HQ train ledger (not Cursor billing)
  ./studio settings <project> [--init] [--reset-usage]  Product execute ledger
  ./studio note <project> "…"                    Queue mid-execute input (ACK; drain after MOVE_DONE)
  ./studio inform <project> --gate 1             Architecture is HITL — use approve, not inform
  ./studio veto <project> --decision ADR-…
  ./studio train LO-NNNN                         Training chat: Impact block; low infuses, high waits
  ./studio train LO-NNNN --approve | --defer --reason "…" | --reopen
  ./studio train --done LO-NNNN                  Close a lesson (PB- id in target + CHANGELOG required)
  ./studio train --promote <p> --topic "…"       Human overrules a project verdict
  ./studio train <skill-id> --from lo --topic "…" --lo LO-NNNN
  ./studio train --done TR-NNNN                  Mark train job infused
  ./studio train --purge-empty                 Close open jobs with blank observation
  ./studio approve-design <p> <TICKET>         After spec + all-state mocks exist
  ./studio mock <p> <TICKET>                   verify interactive mock + print review script
  ./studio ia-audit <p> <TICKET>               IA nav counts (≤7 top, depth ≤3)
  ./studio approve-arch <p> <TICKET>           After docs/architecture/<TICKET>.md exists
  ./studio cite knowledge-base/foo.md --helpful PB-YYYYMMDD-001
  ./studio ticket-card <project> <id>            Compact ticket card
  ./studio receipt <project> <id>                Scaffold execution receipt
  ./studio qa <project> <id> [--verdict PASS|FAIL]  Independent QA review before done
  ./studio qa <project> <id> --finish [PASS|HOLD]  UX-009: shipped screen vs signed mock
  ./studio lint-skills [--strict]                  Skill lists in sync (matcher, roles, files, registry)
  ./studio reality-check <project> [--check]      Dev-build journey check before cadence review
  ./studio health <project>                      Sprint state-graph check
  ./studio focus <project>                       Set active project + isolate siblings
  ./studio bind <project> --session <id>         Cursor only: bind this chat to one product
  ./studio isolate <project>                     Hide sibling projects/ from the agent
  ./studio guard <project> "request text"        Check if request is in scope
  ./studio verify-worlds                         Studio vs project git separation
  ./studio verify-abstraction                    Scan studio HQ for project-name leaks
  ./studio install [--with-skills]               npm deps after git clone (+ optional skills)
  ./studio library list                           List studio-library assets
  ./studio library pull <project> billing auth-login    Copy library → project
  ./studio library promote <project> packages/billing [--force]
  ./studio library suggest <project> <query>      Find assets before coding
  ./studio promote-library <project> [--force]    Optional Headless/generic kit (not product look)
  ./studio start <project> --mode [core|lean]    Start project
  ./studio status <project>                      Show status
  ./studio board <project>                       Show board

  # Phase 1: Intake (human gate 0)
  ./studio intake <project> <input-file>         Process intake (no tickets yet)
  ./studio ideate [focus] --budget small|normal|large   Shortlist only; promote after approve

  # Phase 2: Architecture (human gate 1)
  ./studio blueprint <project>                   Scaffold architecture docs
  ./studio approve <project> --gate 0            Approve PRD + definitions
  ./studio approve <project> --gate 1            Approve architecture blueprint

  # Phase 3: Design (human gates 2a then 2b)
  ./studio design <project> --discovery          2a interview packet (no prototype)
  ./studio design <project> --scope journey|core-views
  ./studio approve <project> --gate 2a           Approve direction (blocks prototype)
  ./studio approve <project> --gate 2b           Approve project kit → tickets (no library promote)
  ./studio revise <project> --gate <0|1|2a|2b> --feedback "..."

  # Legacy
  ./studio concept <project>                     → blueprint / design

  # Phase 3: Sprint Management
  ./studio sprint <project> [--kind design|architecture|implementation|hygiene]
  ./studio review <project> [--approve|--reject] Cadence review (every N implementation sprints)
  ./studio reuse <project> [--record path action] Reuse inform brief after sprint (not a HITL gate)
  ./studio feedback <project> "..."              Capture raw feedback (not a ticket)
  ./studio clarify <project> FB-001 [--severity blocker|major|minor|polish] [--verbatim "..."] [--approve]  Clarify feedback → executable draft
  ./studio feedback-list <project>               Show feedback queue
  ./studio ticket <project> "Title"              Create ticket
  ./studio move <project> <id> <status>          Move ticket
  ./studio groom <project> [--approve]              Validate sprint backlog + grooming

  # Amendment intake (post gate 2)
  ./studio amend <project> <brief-file>          Scaffold AM-NNN analysis folder
  ./studio amendments <project>                  List amendments + status
  ./studio approve <project> --amendment AM-001  Human sign-off on amendment
  ./studio approve <project> --milestones        Approve revised milestone roadmap
  ./studio whoami                                 Print this context's id (QUINSY_CONTEXT_ID) for QA reviewer lines
  ./studio milestone <project> [plan [--next] | review | --approve [--notes "..."]]  PM milestone ownership (plan tickets, review state, HITL sign)
  ./studio approve <project> --prd-amendment AM-001  PRD tier change (class C)

  # Phase 4-5: QA
  ./studio gate <project> [--level N]            Run QA gate

  # Phase 6: Learning
  ./studio learn "Title" --signal <s>            Open a lesson candidate (portable only)
  ./studio learn LO-NNNN --verdict studio|project --reason "…" --assumed "…" --signed "…" --next "…" [--target FILE]
  ./studio learn-list                            Show open LO items (TRAIN_DUE)
  ./studio learn-find "<topic>"                  Search infused PB- bullets in playbooks, process, skills
  ./studio infusion                              Open LO status (does not block IMPLEMENT)
  ./studio train LO-NNNN                         Training chat (see above)
  ./studio train --done TR-NNNN                  Close a train job after infusion
  ./studio infusion-delta --path FILE --op add --body "assumed: … signed: … next: …" [--lo LO-NNNN]
  ./studio cite knowledge-base/foo.md --helpful PB-YYYYMMDD-001
  ./studio retro <project> [--complete]          Sprint retrospective
  ./studio sync <project>                        Sync global assets
  ./studio update-skills                         Subscribe/update external skill packages

  # Tools
  ./studio adr <project> "Title"                 Create ADR
  ./studio decide <project> "Title"              Create decision record
  ./studio decisions <project>                   Show decision records
  ./studio env <project> init|up|down|status [--approve] (base template)
  ./studio env <project> prod --explain           Production names (.env.local) and what each is for
  ./studio ops <project> readiness|deploy|logs|status|migrate --prod|db|cleanup [--approve]
  ./studio repo <project> create|status          GitHub repo
  ./studio promote <project> <asset>             Promote asset to library

Dual-Speed Operating Model:
  CORE — For new platforms & complex systems (6 phases with human gates)
  LEAN — For iterations & features in existing projects (4 phases)

Examples:
  ./studio bootstrap                              List intake PRDs + projects
  ./studio bootstrap demo
  ./studio approve demo --gate 0
  ./studio blueprint demo
  ./studio approve demo --gate 1
  ./studio design demo --scope journey
  ./studio approve demo --gate 2a
  ./studio approve demo --gate 2b
  ./studio sprint demo
  ./studio ticket demo "Button Component" --phase 3 --priority P1
  ./studio move demo DEMO-0001 implement --reason "Implementation started"
  ./studio gate demo --level 5
  ./studio learn "Gate check takes too long" --signal tooling-gap
  ./studio sync demo
""")


HELP_FLAGS = frozenset({"-h", "--help"})


def cli_wants_help(command: str, args: list) -> bool:
    """`--help` / `-h` is a flag, never a project slug. `ideate` prints its own usage."""
    if command == "ideate":
        return False
    if command in HELP_FLAGS:
        return True
    return bool(args) and args[0] in HELP_FLAGS


def _pop_flag(args: list, flag: str) -> tuple:
    """Return (value, args_without_flag). Missing flag yields ('', args)."""
    out = []
    value = ""
    i = 0
    while i < len(args):
        if args[i] == flag and i + 1 < len(args):
            value = args[i + 1]
            i += 2
            continue
        out.append(args[i])
        i += 1
    return value, out


def first_project_arg(args: list) -> str:
    """First positional that can be a project name; empty if only flags."""
    from studio_status import is_valid_project_slug

    for arg in args:
        if arg.startswith("-"):
            continue
        return arg if is_valid_project_slug(arg) else ""
    return ""


def main():
    orchestrator = StudioOrchestrator()
    
    if len(sys.argv) < 2:
        print_help()
        return
    
    command = sys.argv[1]
    
    # Parse arguments
    args = sys.argv[2:]

    if cli_wants_help(command, args):
        print_help()
        return

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
        release = "--release" in args
        session, rest = _pop_flag(args, "--session")
        positional = [a for a in rest if not a.startswith("--")]
        if not positional:
            print("  Usage: ./studio execute <project> [--json] [--release] [--session <id>]")
            sys.exit(2)
        ok = orchestrator.cmd_execute(positional[0], as_json=as_json, release=release, session=session)
        if ok is False:
            sys.exit(2)

    elif command == "settings":
        positional = [a for a in args if not a.startswith("--")]
        project = positional[0] if positional else ""
        orchestrator.cmd_settings(
            project,
            reset_usage_flag="--reset-usage" in args,
            init_flag="--init" in args,
        )

    elif command == "note" and len(args) >= 1:
        drain = "--drain" in args
        text_parts = [a for a in args[1:] if a != "--drain"]
        orchestrator.cmd_note(args[0], " ".join(text_parts), drain=drain)

    elif command == "inform" and len(args) >= 1:
        gate = None
        for i, arg in enumerate(args):
            if arg == "--gate" and i + 1 < len(args):
                gate = args[i + 1]
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

    elif command == "train" and len(args) >= 1 and (
        re.fullmatch(r"LO-\d{4}", args[0].upper())
        or (args[0] == "--done" and len(args) >= 2 and re.fullmatch(r"LO-\d{4}", args[1].upper()))
        or args[0] == "--promote"
    ):
        # Lesson training: ./studio train LO-NNNN [--approve | --defer --reason "…" | --reopen]
        #                  ./studio train --done LO-NNNN
        #                  ./studio train --promote <project> --topic "<title>"
        reason = ""
        topic = ""
        for i, arg in enumerate(args):
            if arg == "--reason" and i + 1 < len(args):
                reason = args[i + 1]
            if arg == "--topic" and i + 1 < len(args):
                topic = args[i + 1]
        if args[0] == "--promote":
            project = args[1] if len(args) >= 2 and not args[1].startswith("--") else ""
            if not project or not topic:
                print("  Usage: ./studio train --promote <project> --topic \"<title from the project-verdict list>\"")
                sys.exit(2)
            ok = orchestrator.cmd_train_promote(project, topic)
        elif args[0] == "--done":
            ok = orchestrator.cmd_train_lesson(args[1], done=True)
        else:
            ok = orchestrator.cmd_train_lesson(
                args[0],
                approve="--approve" in args,
                defer="--defer" in args,
                reopen="--reopen" in args,
                reason=reason,
            )
        if ok is False:
            sys.exit(2)

    elif command == "train" and len(args) >= 1:
        done_id = ""
        lo_id = ""
        skill_id = ""
        topic = ""
        source = "mistake"
        i = 0
        while i < len(args):
            arg = args[i]
            if arg == "--done":
                if i + 1 < len(args) and not args[i + 1].startswith("--"):
                    done_id = args[i + 1]
                    i += 2
                    continue
                i += 1
                continue
            if arg == "--lo" and i + 1 < len(args):
                lo_id = args[i + 1]
                i += 2
                continue
            if arg == "--topic" and i + 1 < len(args):
                topic = args[i + 1]
                i += 2
                continue
            if arg == "--from" and i + 1 < len(args):
                source = args[i + 1]
                i += 2
                continue
            if arg == "--purge-empty":
                i += 1
                continue
            if not skill_id and not arg.startswith("--"):
                skill_id = arg
            i += 1
        if not topic and skill_id and len(args) >= 2 and not args[1].startswith("--") and args[0] != "--done":
            topic = topic or " ".join(a for a in args[1:] if not a.startswith("--"))
        orchestrator.cmd_train(skill_id, topic, source=source, done=done_id, lo_id=lo_id, close_mode="--done" in args, purge_empty="--purge-empty" in args)

    elif command == "infusion-delta":
        rel_path = ""
        op = "add"
        section = "Deltas"
        body = ""
        bullet_id = ""
        lo_ref = ""
        for i, arg in enumerate(args):
            if arg == "--path" and i + 1 < len(args):
                rel_path = args[i + 1]
            elif arg == "--op" and i + 1 < len(args):
                op = args[i + 1]
            elif arg == "--section" and i + 1 < len(args):
                section = args[i + 1]
            elif arg == "--body" and i + 1 < len(args):
                body = args[i + 1]
            elif arg == "--id" and i + 1 < len(args):
                bullet_id = args[i + 1]
            elif arg == "--lo" and i + 1 < len(args):
                lo_ref = args[i + 1]
        ok = orchestrator.cmd_infusion_delta(rel_path, op, section=section, body=body, bullet_id=bullet_id, lo_id=lo_ref)
        if ok is False:
            sys.exit(2)

    elif command == "cite":
        rel_path = args[0] if args and not args[0].startswith("--") else ""
        helpful = ""
        harmful = ""
        for i, arg in enumerate(args):
            if arg == "--path" and i + 1 < len(args):
                rel_path = args[i + 1]
            elif arg == "--helpful" and i + 1 < len(args):
                helpful = args[i + 1]
            elif arg == "--harmful" and i + 1 < len(args):
                harmful = args[i + 1]
        orchestrator.cmd_cite(rel_path, helpful=helpful, harmful=harmful)

    elif command == "ticket-card" and len(args) >= 2:
        orchestrator.cmd_ticket_card(args[0], args[1])

    elif command == "receipt" and len(args) >= 2:
        orchestrator.cmd_receipt(args[0], args[1])

    elif command == "reality-check" and len(args) >= 1:
        ok = orchestrator.cmd_reality_check(args[0], check="--check" in args)
        sys.exit(0 if ok else 1)

    elif command == "qa" and len(args) >= 2:
        verdict = ""
        if "--finish" in args:
            idx = args.index("--finish")
            nxt = args[idx + 1] if idx + 1 < len(args) else ""
            decision = nxt.upper() if nxt and not nxt.startswith("--") else "BRIEF"
            ok = orchestrator.cmd_qa_finish(args[0], args[1], decision)
            sys.exit(0 if ok else 1)
        if "--verdict" in args:
            idx = args.index("--verdict")
            verdict = args[idx + 1] if idx + 1 < len(args) else "?"
        ok = orchestrator.cmd_qa(args[0], args[1], verdict)
        sys.exit(0 if ok else 1)

    elif command == "lint-skills":
        from lint_skills import main as lint_skills_main

        sys.exit(lint_skills_main(args))

    elif command == "health" and len(args) >= 1:
        orchestrator.cmd_health(args[0])

    elif command == "bind":
        show = "--show" in args
        clear = "--clear" in args
        session, rest = _pop_flag(args, "--session")
        positional = [a for a in rest if not a.startswith("--")]
        project = positional[0] if positional else ""
        if not project and not show and not clear:
            print("  Usage: ./studio bind <project> --session <id> | --show --session <id> | --clear --session <id>")
            sys.exit(2)
        ok = orchestrator.cmd_bind(project, session=session, show=show, clear=clear)
        if ok is False:
            sys.exit(2)

    elif command == "focus" and len(args) >= 1:
        force = "--force" in args
        session, rest = _pop_flag(args, "--session")
        positional = [a for a in rest if not a.startswith("--")]
        if not positional:
            print("  Usage: ./studio focus <project> [--force] [--session <id>]")
            sys.exit(2)
        ok = orchestrator.cmd_focus(positional[0], force=force, session=session)
        if ok is False:
            sys.exit(2)

    elif command == "isolate" and len(args) >= 1:
        orchestrator.cmd_isolate(args[0])

    elif command == "guard" and len(args) >= 2:
        session, rest = _pop_flag(args, "--session")
        if len(rest) < 2:
            print("  Usage: ./studio guard <project> \"<request>\" [--session <id>]")
            sys.exit(2)
        orchestrator.cmd_guard(rest[0], " ".join(rest[1:]), session=session)

    elif command == "ideate":
        from studio_ideate import dispatch as ideate_dispatch

        code, message = ideate_dispatch(args)
        print(message)
        if code != 0:
            sys.exit(code)

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
        discovery = "--discovery" in args
        for i, arg in enumerate(args):
            if arg == "--scope" and i + 1 < len(args):
                scope = args[i + 1]
        orchestrator.cmd_design(project, scope, discovery=discovery)

    elif command == "revise" and len(args) >= 1:
        project = args[0]
        gate = "0"
        feedback = ""
        for i, arg in enumerate(args):
            if arg == "--gate" and i + 1 < len(args):
                gate = args[i + 1]
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
                gate = args[i + 1]
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
            print("  ⚠️  Use --gate 0|1|2a|2b, --amendment AM-NNN, --prd-amendment AM-NNN, or --milestones")
    
    elif command == "ops" and len(args) >= 2:
        from studio_ops import run_op

        project = args[0]
        action = args[1]
        flags = [a for a in args[2:] if a.startswith("--") and a not in ("--approve", "--dry-run")]
        print_header(f"OPS: {project} {action}")
        ok, text = run_op(project, PROJECTS_DIR / project, action, flags, approve="--approve" in args, dry_run="--dry-run" in args)
        print(text)
        if not ok:
            sys.exit(2)

    elif command == "whoami":
        from qa_review import context_id

        print(context_id())

    elif command == "milestone" and len(args) >= 1:
        action = ""
        notes = ""
        next_ = "--next" in args
        for i, arg in enumerate(args[1:], start=1):
            if arg in ("plan", "review"):
                action = arg
            elif arg == "--approve":
                action = "approve"
            elif arg == "--notes" and i + 1 < len(args):
                notes = args[i + 1]
        orchestrator.cmd_milestone(args[0], action=action, notes=notes, next_=next_)

    elif command == "amend" and len(args) >= 2:
        force = "--force" in args
        orchestrator.cmd_amend(args[0], args[1], force=force)

    elif command == "amendments" and len(args) >= 1:
        orchestrator.cmd_amendments(args[0])
    
    elif command == "ship" and len(args) >= 1:
        to = "dev"
        approve_prod = "--approve" in args
        for i, arg in enumerate(args):
            if arg == "--to" and i + 1 < len(args):
                to = args[i + 1]
        orchestrator.cmd_ship(args[0], to=to, approve_prod=approve_prod)

    elif command == "sprint" and len(args) >= 1:
        approve_scope = "--approve-scope" in args
        kind = ""
        for i, arg in enumerate(args):
            if arg == "--kind" and i + 1 < len(args):
                kind = args[i + 1]
        orchestrator.cmd_sprint(args[0], approve_scope=approve_scope, kind=kind)

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
        orchestrator.cmd_review(project, approve=approve, reject=reject, notes=notes, reason=reason, inform="--inform" in args)

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
        design_reason = ""
        for i, arg in enumerate(args):
            if arg == "--source" and i + 1 < len(args):
                source = args[i + 1]
            if arg == "--design-reason" and i + 1 < len(args):
                design_reason = args[i + 1]
        orchestrator.cmd_feedback(project, text, source=source, force=force, design_reason=design_reason)

    elif command == "feedback-list" and len(args) >= 1:
        orchestrator.cmd_feedback_list(args[0])

    elif command == "clarify" and len(args) >= 2:
        project = args[0]
        fb_id = args[1]
        title = ""
        scope = ""
        out_of_scope = ""
        acceptance: List[str] = []
        severity = ""
        verbatim: List[str] = []
        design_reason = ""
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
            elif arg == "--severity" and i + 1 < len(args):
                severity = args[i + 1]
                i += 2
            elif arg == "--verbatim" and i + 1 < len(args):
                verbatim.append(args[i + 1])
                i += 2
            elif arg == "--design-reason" and i + 1 < len(args):
                design_reason = args[i + 1]
                i += 2
            else:
                i += 1
        orchestrator.cmd_clarify(
            project, fb_id, title=title, scope=scope,
            out_of_scope=out_of_scope, acceptance=acceptance, approve=approve,
            severity=severity, verbatim=verbatim, design_reason=design_reason,
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
        if args[1] == "--phase":
            orchestrator.cmd_approve_design_phase(project)
        else:
            ticket_id = args[1]
            notes = ""
            reason = ""
            for i, arg in enumerate(args):
                if arg == "--notes" and i + 1 < len(args):
                    notes = args[i + 1]
                if arg == "--reason" and i + 1 < len(args):
                    reason = args[i + 1]
            if "--reject" in args:
                ok = orchestrator.cmd_reject_design(project, ticket_id, reason, notes=notes)
                if not ok:
                    sys.exit(2)
            else:
                orchestrator.cmd_approve_design(project, ticket_id, notes=notes)

    elif command == "mock" and len(args) >= 2:
        ok = orchestrator.cmd_mock(args[0], args[1])
        if ok is False:
            sys.exit(2)

    elif command == "ia-audit" and len(args) >= 2:
        ok = orchestrator.cmd_ia_audit(args[0], args[1])
        if ok is False:
            sys.exit(2)

    elif command == "approve-arch" and len(args) >= 2:
        project = args[0]
        if args[1] == "--phase":
            orchestrator.cmd_approve_arch_phase(project)
        elif "--reject" in args:
            reason = ""
            for i, arg in enumerate(args):
                if arg == "--reject" and i + 1 < len(args) and not args[i + 1].startswith("--"):
                    reason = args[i + 1]
            orchestrator.cmd_reject_arch(project, args[1], reason=reason)
        else:
            ticket_id = args[1]
            notes = ""
            for i, arg in enumerate(args):
                if arg == "--notes" and i + 1 < len(args):
                    notes = args[i + 1]
            orchestrator.cmd_approve_arch(project, ticket_id, notes=notes)
    
    elif command == "gate":
        project = first_project_arg(args)
        if not project:
            print("  Usage: ./studio gate <project> [--level N] [--anti-slop]")
            print("  --help / flags are not project names.")
            sys.exit(2)
        level = 5
        anti_slop = False
        for i, arg in enumerate(args):
            if arg == "--level" and i + 1 < len(args):
                level = int(args[i + 1])
            elif arg == "--anti-slop":
                anti_slop = True
        ok = orchestrator.cmd_gate(project, level, anti_slop)
        if ok is False:
            sys.exit(2)
    
    elif command == "learn" and len(args) >= 1:
        title = args[0]
        signal = "process-gap"
        source = "Studio Development"
        opts = {"verdict": "", "reason": "", "assumed": "", "signed": "", "next": "", "target": ""}
        for i, arg in enumerate(args):
            if arg == "--signal" and i + 1 < len(args):
                signal = args[i + 1]
            elif arg == "--source" and i + 1 < len(args):
                source = args[i + 1]
            elif arg.startswith("--") and arg[2:] in opts and i + 1 < len(args):
                opts[arg[2:]] = args[i + 1]
        orchestrator.cmd_learn(
            title,
            signal,
            source,
            verdict=opts["verdict"],
            reason=opts["reason"],
            assumed=opts["assumed"],
            signed=opts["signed"],
            next_rule=opts["next"],
            target=opts["target"],
        )
    
    elif command == "learn-list":
        orchestrator.cmd_learn_list()

    elif command == "learn-find" and args:
        orchestrator.cmd_learn_find(" ".join(args))

    elif command == "infusion":
        orchestrator.cmd_infusion()
    
    elif command == "retro":
        retro_complete = "--complete" in args
        project = first_project_arg(args)
        if not project:
            print("  Usage: ./studio retro <project> [--complete]")
            print("  --help / flags are not project names.")
            sys.exit(2)
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
        approve = "--approve" in args
        profiles = []
        skip = set()
        for i, arg in enumerate(args):
            if arg == "--profile" and i + 1 < len(args):
                profiles.append(args[i + 1])
                skip.add(i + 1)
        positional = [
            a
            for i, a in enumerate(args)
            if i not in skip and a != "--approve" and not a.startswith("--")
        ]
        if len(positional) < 2:
            print("  Usage: ./studio env <project> init|up|down|status|logs|migrate|dev [--approve] [--profile name]")
            sys.exit(2)
        ok = orchestrator.cmd_env(positional[0], positional[1], approve=approve, profiles=profiles)
        if ok is False:
            sys.exit(2)
    
    elif command == "repo" and len(args) >= 2:
        url = args[2] if len(args) >= 3 else ""
        orchestrator.cmd_repo(args[0], args[1], url=url)
    
    elif command == "promote" and len(args) >= 2:
        orchestrator.cmd_promote(args[0], args[1])
    
    else:
        print_help()

if __name__ == "__main__":
    main()
