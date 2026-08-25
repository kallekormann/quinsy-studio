#!/usr/bin/env python3
"""
Amendment intake — scaffold analysis artifacts from a vision brief.

Flow:
  ./studio amend <project> intake/amendments/<project>/amendment_NN.md
  ./studio amendments <project>
  ./studio approve <project> --amendment AM-001
  ./studio approve <project> --milestones   # after roadmap patch from amendment
"""

from __future__ import annotations

import json
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

STUDIO_ROOT = Path(__file__).parent.parent.parent
PROJECTS_DIR = STUDIO_ROOT / "projects"
INTAKE_AMENDMENTS_DIR = STUDIO_ROOT / "intake" / "amendments"
PROCESS_DOC = STUDIO_ROOT / ".quinsy-studio" / "process" / "amendment-intake.md"

AMENDMENT_ID_RE = re.compile(r"^AM-\d{3}$", re.I)
CHECKBOX_RE = re.compile(r"^- \[(x| )\]\s+(.+)$", re.MULTILINE | re.IGNORECASE)

ARTIFACT_SPECS: List[Tuple[str, str]] = [
    (
        "01-vision-synthesis.md",
        """# Vision synthesis — {am_id}

> **Agent:** Consolidate the brief into a narrative. Map to PRD and flag conflicts.

## North-star (synthesized)

## PRD fit

| PRD section | Alignment | Notes |
|-------------|-----------|-------|
| | | |

## Conflicts & risks

## Classification

- [ ] A — ticket-only (fits existing milestone)
- [ ] B — milestone (new/reordered M*)
- [ ] C — PRD tier change
""",
    ),
    (
        "02-requirements-addendum.md",
        """# Requirements addendum — {am_id}

> **Agent:** New FR/NFR, personas, journeys. Do not duplicate existing PRD without reason.

## Functional requirements (draft)

| ID | Requirement | Priority |
|----|-------------|----------|
| | | |

## Non-functional requirements

## Personas affected

## User journeys (amendment-specific)
""",
    ),
    (
        "03-milestone-roadmap.md",
        """# Milestone roadmap patch — {am_id}

> **Agent:** Propose insert/reorder/defer of M* phases. Human approves via `./studio approve {project} --milestones`.

## Current roadmap snapshot

## Proposed changes

| Action | Milestone | Rationale |
|--------|-----------|-----------|
| insert / extend / defer | | |

## Updated dependency chain

## Success criteria (per affected milestone)
""",
    ),
    (
        "04-ui-ux-concept.md",
        """# UI/UX concept — {am_id}

> **Team 10:** Flows, IA, concept direction. Link design-track tickets.

## Information architecture

## Key flows

## Concept direction (no pixel-perfect mocks here)

## Design-track tickets needed
""",
    ),
    (
        "05-frontend-architecture.md",
        """# Frontend architecture — {am_id}

> **Team 01:** Routes, components, state, studio-library impact.

## Surfaces affected

## Component / package map

## State & data flow

## studio-library pull/promote notes
""",
    ),
    (
        "06-backend-architecture.md",
        """# Backend architecture — {am_id}

> **Team 02:** APIs, schema, integrations.

## API changes

## Data model

## Integrations (email, billing, storage)
""",
    ),
    (
        "07-tooling-and-process.md",
        """# Tooling & process — {am_id}

> **Teams 08/09:** CI, env, Docker, new studio commands if needed.

## Tooling impact

## Environment / secrets

## Process changes
""",
    ),
    (
        "09-tickets-draft.md",
        """# Ticket drafts — {am_id}

> **Agent:** Stubs only — no `sprint:` tags. Each stub needs team, skills, milestone, ticket_type.

## Stubs

### TICKET-001 — Title

```yaml
team: 01-frontend-experience
skills: [FE-001]
ticket_type: feature
milestone: M6
estimate: M
priority: P1
```

**User story:** As a … I want … so that …

**Acceptance:**
- [ ] …
""",
    ),
    (
        "10-approval-checklist.md",
        """# Approval checklist — {am_id}

Human sign-off before materializing backlog tickets.

- [ ] Vision synthesis reviewed
- [ ] Requirements addendum reviewed
- [ ] Milestone roadmap patch reviewed (`./studio approve {project} --milestones` if changed)
- [ ] UI/UX concept reviewed (Team 10)
- [ ] FE/BE architecture reviewed
- [ ] Ticket drafts groomed
- [ ] No implementation until `./studio approve {project} --amendment {am_id}`

**Approved by:** _name_  
**Date:** _YYYY-MM-DD_
""",
    ),
]

REQUIRED_ARTIFACTS = [
    "source.md",
    "01-vision-synthesis.md",
    "02-requirements-addendum.md",
    "03-milestone-roadmap.md",
    "09-tickets-draft.md",
    "10-approval-checklist.md",
]

AGENT_BRIEFING = """# Amendment analysis — {am_id}

**Status:** analyzed (awaiting human)  
**Process:** {process_doc}

## Your job

1. Read `source.md` and checked teams/skills in `meta.json`
2. Fill every artifact `01`–`07`, `09` (skip `08-adrs/` unless ADRs needed)
3. Derive milestones in `03-milestone-roadmap.md` — never from the human brief
4. Do **not** create `backlog/*.md` until human runs `./studio approve {project} --amendment {am_id}`

## Artifact checklist

{artifact_list}
"""


def amendments_dir(project: str) -> Path:
    return PROJECTS_DIR / project / "docs" / "amendments"


def registry_path(project: str) -> Path:
    return amendments_dir(project) / "registry.json"


def load_registry(project: str) -> Dict:
    path = registry_path(project)
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"amendments": []}


def save_registry(project: str, registry: Dict) -> None:
    root = amendments_dir(project)
    root.mkdir(parents=True, exist_ok=True)
    registry_path(project).write_text(
        json.dumps(registry, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def resolve_amendment_file(project: str, input_file: str) -> Optional[Path]:
    path = Path(input_file)
    if not path.is_absolute():
        path = STUDIO_ROOT / input_file
    if path.exists():
        return path
    # project-scoped default
    slug_dir = INTAKE_AMENDMENTS_DIR / project
    if slug_dir.exists():
        candidate = slug_dir / input_file
        if candidate.exists():
            return candidate
    return None


def amendment_path_for_cli(path: Path) -> str:
    try:
        return str(path.relative_to(STUDIO_ROOT))
    except ValueError:
        return str(path)


def parse_title(content: str) -> str:
    for line in content.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
            title = re.sub(r"^Amendment brief\s*—\s*", "", title, flags=re.I)
            title = re.sub(r"\{\{title\}\}", "", title).strip()
            if title:
                return title
    return "amendment"


def parse_checked_items(content: str) -> List[str]:
    items: List[str] = []
    for match in CHECKBOX_RE.finditer(content):
        if match.group(1).lower() == "x":
            items.append(match.group(2).strip())
    return items


def parse_teams_and_skills(content: str) -> Tuple[List[str], List[str]]:
    teams: List[str] = []
    skills: List[str] = []
    for item in parse_checked_items(content):
        team_match = re.match(r"\*\*(\d{2})\s*—", item)
        if team_match:
            teams.append(item)
            continue
        skill_match = re.match(r"\*\*([A-Z]{2}-\d{3})\*\*", item)
        if skill_match:
            skills.append(skill_match.group(1))
    return teams, skills


def validate_brief(content: str) -> Tuple[bool, List[str], List[str]]:
    """Return (ok, errors, warnings)."""
    errors: List[str] = []
    warnings: List[str] = []

    if "{{title}}" in content or "{{your name}}" in content:
        warnings.append("Brief still contains template placeholders — fill before final submit")

    if not re.search(r"^##\s+1\.\s+Executive summary", content, re.MULTILINE | re.I):
        warnings.append("Missing §1 Executive summary (use template structure)")

    teams, skills = parse_teams_and_skills(content)
    if not teams:
        warnings.append("No teams checked in §8 — agent will infer, but human selection is preferred")

    if re.search(r"milestone:\s*M\d", content, re.I):
        errors.append("Human brief must not specify milestones — studio derives them in analysis")

    if len(content.strip()) < 200:
        warnings.append("Brief is very short — add vision detail in §3 for better analysis")

    return len(errors) == 0, errors, warnings


def next_amendment_id(registry: Dict) -> str:
    nums = []
    for entry in registry.get("amendments", []):
        am_id = entry.get("id", "")
        m = re.match(r"AM-(\d+)", am_id, re.I)
        if m:
            nums.append(int(m.group(1)))
    n = max(nums, default=0) + 1
    return f"AM-{n:03d}"


def find_amendment_folder(project: str, am_id: str) -> Optional[Path]:
    root = amendments_dir(project)
    if not root.exists():
        return None
    am_id = am_id.upper()
    for child in root.iterdir():
        if child.is_dir() and child.name.upper().startswith(am_id):
            return child
    return None


def find_amendment_entry(registry: Dict, am_id: str) -> Optional[Dict]:
    am_id = am_id.upper()
    for entry in registry.get("amendments", []):
        if entry.get("id", "").upper() == am_id:
            return entry
    return None


def update_readme_index(project: str, registry: Dict) -> Path:
    readme = amendments_dir(project) / "README.md"
    rows = []
    for entry in registry.get("amendments", []):
        rows.append(
            f"| {entry.get('id', '—')} | {entry.get('title', '—')} | "
            f"{entry.get('status', '—')} | {entry.get('milestone_impact', '—')} | "
            f"{entry.get('approved_at', '—') or '—'} |"
        )
    body = f"""# Product amendments — {project}

> Registry: `registry.json` · Process: `.quinsy-studio/process/amendment-intake.md`

| ID | Title | Status | Milestone impact | Approved |
|----|-------|--------|------------------|----------|
{chr(10).join(rows) if rows else "| — | (none yet) | — | — | — |"}

## Commands

```bash
./studio amend {project} intake/amendments/{project}/amendment_NN.md
./studio amendments {project}
./studio approve {project} --amendment AM-001
./studio approve {project} --milestones   # if roadmap changed
```
"""
    readme.parent.mkdir(parents=True, exist_ok=True)
    readme.write_text(body, encoding="utf-8")
    return readme


def scaffold_amendment(
    project: str,
    source_path: Path,
    *,
    force: bool = False,
) -> Tuple[bool, str, Optional[Dict]]:
    content = source_path.read_text(encoding="utf-8")
    ok, errors, warnings = validate_brief(content)
    if not ok:
        return False, "Brief validation failed:\n  • " + "\n  • ".join(errors), None

    registry = load_registry(project)
    am_id = next_amendment_id(registry)
    title = parse_title(content)
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:40] or "amendment"
    folder_name = f"{am_id}-{slug}"
    am_dir = amendments_dir(project) / folder_name

    if am_dir.exists() and not force:
        return False, f"{folder_name} already exists — use --force to re-scaffold", None

    if am_dir.exists():
        shutil.rmtree(am_dir)
    am_dir.mkdir(parents=True)
    (am_dir / "08-adrs").mkdir(exist_ok=True)
    (am_dir / "08-adrs" / ".gitkeep").write_text("", encoding="utf-8")

    shutil.copy2(source_path, am_dir / "source.md")

    teams, skills = parse_teams_and_skills(content)
    meta = {
        "id": am_id,
        "project": project,
        "title": title,
        "slug": slug,
        "source": amendment_path_for_cli(source_path),
        "status": "analyzed",
        "created_at": datetime.now().isoformat(),
        "teams_checked": teams,
        "skills_checked": skills,
        "warnings": warnings,
    }
    (am_dir / "meta.json").write_text(
        json.dumps(meta, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    for filename, template in ARTIFACT_SPECS:
        text = template.format(am_id=am_id, project=project)
        (am_dir / filename).write_text(text, encoding="utf-8")

    artifact_list = "\n".join(f"- [ ] `{name}`" for name, _ in ARTIFACT_SPECS)
    (am_dir / "AGENT.md").write_text(
        AGENT_BRIEFING.format(
            am_id=am_id,
            project=project,
            process_doc=amendment_path_for_cli(PROCESS_DOC)
            if PROCESS_DOC.exists()
            else ".quinsy-studio/process/amendment-intake.md",
            artifact_list=artifact_list,
        ),
        encoding="utf-8",
    )

    entry = {
        "id": am_id,
        "title": title,
        "slug": slug,
        "folder": folder_name,
        "status": "analyzed",
        "source": meta["source"],
        "milestone_impact": "pending analysis",
        "approved_at": None,
        "created_at": meta["created_at"],
    }
    registry.setdefault("amendments", []).append(entry)
    save_registry(project, registry)
    update_readme_index(project, registry)

    return True, folder_name, meta


def validate_analysis_ready(am_dir: Path) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    for name in REQUIRED_ARTIFACTS:
        if not (am_dir / name).exists():
            issues.append(f"Missing {name}")
    return len(issues) == 0, issues


def approve_amendment(
    project: str,
    am_id: str,
    *,
    prd_tier: bool = False,
) -> Tuple[bool, str]:
    registry = load_registry(project)
    entry = find_amendment_entry(registry, am_id)
    if not entry:
        return False, f"{am_id} not found in registry — run ./studio amend first"

    if entry.get("status") == "approved":
        return True, f"{am_id} already approved at {entry.get('approved_at')}"

    am_dir = find_amendment_folder(project, am_id)
    if not am_dir:
        return False, f"Folder for {am_id} not found under docs/amendments/"

    ok, issues = validate_analysis_ready(am_dir)
    if not ok:
        return False, "Analysis not ready:\n  • " + "\n  • ".join(issues)

    now = datetime.now().isoformat()
    entry["status"] = "approved"
    entry["approved_at"] = now
    if prd_tier:
        entry["prd_amendment"] = True
    save_registry(project, registry)
    update_readme_index(project, registry)

    revisions = PROJECTS_DIR / project / "docs" / "phases" / "revisions.md"
    if revisions.parent.exists():
        line = f"\n## {now[:10]} — {am_id} approved\n\n- Amendment: {entry.get('title')}\n"
        if prd_tier:
            line += "- PRD tier change flagged (class C)\n"
        line += f"- Artifacts: `docs/amendments/{am_dir.name}/`\n"
        if revisions.exists():
            revisions.write_text(revisions.read_text(encoding="utf-8") + line, encoding="utf-8")
        else:
            revisions.write_text("# Phase revisions\n" + line, encoding="utf-8")

    meta_path = am_dir / "meta.json"
    if meta_path.exists():
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        meta["status"] = "approved"
        meta["approved_at"] = now
        meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    msg = (
        f"✅ {am_id} approved\n"
        f"  Next: agent materializes `09-tickets-draft.md` → backlog/*.md\n"
        f"  If roadmap changed: ./studio approve {project} --milestones\n"
        f"  Then: ./studio groom {project} && ./studio sprint {project}"
    )
    return True, msg


def approve_milestones(project: str) -> Tuple[bool, str]:
    phases_readme = PROJECTS_DIR / project / "docs" / "phases" / "README.md"
    if not phases_readme.exists():
        return False, f"Missing docs/phases/README.md — draft roadmap first"

    pending = pending_amendments(project)
    analyzed = [a for a in pending if a.get("status") == "analyzed"]
    if analyzed:
        return (
            False,
            f"Pending amendment analysis: {', '.join(a['id'] for a in analyzed)} — "
            f"complete analysis and ./studio approve {project} --amendment <ID> first",
        )

    return True, (
        f"✅ Milestone roadmap approved for {project}\n"
        f"  Agent may write tickets for the active milestone only.\n"
        f"  Then: ./studio sprint {project}"
    )


def format_amendments_list(project: str) -> str:
    registry = load_registry(project)
    items = registry.get("amendments", [])
    if not items:
        return f"No amendments for {project}. Drop brief → ./studio amend {project} <file>"
    lines = [f"Amendments — {project}", ""]
    for entry in items:
        lines.append(
            f"  {entry.get('id')}  {entry.get('status', '?'):10}  "
            f"{entry.get('title', '')[:50]}  → docs/amendments/{entry.get('folder', '?')}"
        )
    return "\n".join(lines)


def pending_amendments(project: str) -> List[Dict]:
    return [
        e
        for e in load_registry(project).get("amendments", [])
        if e.get("status") in ("draft", "analyzed")
    ]


def resume_amendment_actions(project: str) -> List[str]:
    actions: List[str] = []
    pending = pending_amendments(project)
    if not pending:
        return actions
    for entry in pending:
        am_id = entry.get("id", "AM-???")
        if entry.get("status") == "analyzed":
            actions.append(f"⏸ HUMAN: review docs/amendments/{entry.get('folder')}/")
            actions.append(f"./studio approve {project} --amendment {am_id}")
            if entry.get("milestone_impact") != "pending analysis":
                actions.append(f"./studio approve {project} --milestones  # if roadmap changed")
        else:
            actions.append(
                f"Amendment {am_id} draft — ./studio amend {project} intake/amendments/{project}/..."
            )
    actions.append("Do not kick off next milestone until amendments approved")
    return actions


def gate2_approved(status: Dict) -> bool:
    hg = status.get("human_gates", {})
    if hg.get("2", {}).get("status") == "approved":
        return True
    phase = str(status.get("phase", ""))
    return phase in ("4", "5", PHASE_IMPLEMENT, PHASE_SPRINT)  # type: ignore[name-defined]


# Avoid circular import at module level for phase constants
PHASE_IMPLEMENT = "4"
PHASE_SPRINT = "3"
