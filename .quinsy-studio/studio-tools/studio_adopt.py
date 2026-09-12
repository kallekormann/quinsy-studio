#!/usr/bin/env python3
"""
Brownfield adopt — overlay studio HQ folders on an existing codebase.

Never wipe application source. Never git init over an existing .git.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

TOOLS_DIR = Path(__file__).parent
QUINSY_STUDIO = TOOLS_DIR.parent
STUDIO_ROOT = QUINSY_STUDIO.parent
PROJECTS_DIR = STUDIO_ROOT / "projects"
TEMPLATES_DIR = QUINSY_STUDIO / "studio-templates"
AS_BUILT_TPL = TEMPLATES_DIR / "as-built"

AS_BUILT_FILES = [
    "00-product.md",
    "01-surfaces.md",
    "02-domain-and-data.md",
    "03-architecture.md",
    "04-auth-and-boundaries.md",
    "05-ui-inventory.md",
    "06-quality.md",
    "07-implemented-vs-gap.md",
]

SOURCE_MARKERS = (
    "src",
    "app",
    "apps",
    "lib",
    "packages",
    "server",
    "cmd",
    "internal",
    "pkg",
    "web",
    "frontend",
    "backend",
)

COPY_SKIP = {
    "node_modules",
    ".next",
    "dist",
    "build",
    "__pycache__",
    ".turbo",
    "coverage",
    ".venv",
    "venv",
}

OVERLAY_DIRS = [
    "docs/intake",
    "docs/definitions",
    "docs/architecture",
    "docs/architecture/diagrams",
    "docs/adr",
    "docs/decisions",
    "docs/phases",
    "docs/modules",
    "docs/as-built",
    "docs/ia",
    "design",
    "backlog",
    "backlog/implement",
    "backlog/done",
    "backlog/blocked",
    "sprints",
]


def project_dir(slug: str) -> Path:
    return PROJECTS_DIR / slug


def is_git_url(value: str) -> bool:
    text = (value or "").strip()
    return text.startswith(("git@", "ssh://", "https://", "http://", "git://")) or text.endswith(".git")


def looks_like_application_source(root: Path) -> bool:
    """True when the tree already has application code (not an empty studio scaffold)."""
    if not root.exists() or not root.is_dir():
        return False
    for name in SOURCE_MARKERS:
        if (root / name).is_dir():
            return True
    for fname in ("package.json", "pyproject.toml", "go.mod", "Cargo.toml", "composer.json"):
        if (root / fname).exists():
            return True
    return False


def has_runnable_env(root: Path) -> bool:
    names = (
        "docker-compose.yml",
        "docker-compose.yaml",
        "compose.yml",
        "compose.yaml",
        "Dockerfile",
        "Procfile",
    )
    if any((root / n).exists() for n in names):
        return True
    if (root / "docker").is_dir() and any((root / "docker").iterdir()):
        return True
    return False


def load_status_file(root: Path) -> Dict:
    path = root / "status.json"
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def is_adopt_project(slug: str) -> bool:
    status = load_status_file(project_dir(slug))
    return status.get("mode") == "adopt"


def _has_placeholders(content: str) -> bool:
    return bool(re.search(r"_TODO_", content))


def as_built_is_ready(slug: str) -> bool:
    root = project_dir(slug) / "docs" / "as-built"
    if not root.exists():
        return False
    for name in AS_BUILT_FILES:
        path = root / name
        if not path.exists():
            return False
        text = path.read_text(encoding="utf-8", errors="ignore").strip()
        if len(text) < 80 or _has_placeholders(text):
            return False
    return True


def as_built_missing(slug: str) -> List[str]:
    root = project_dir(slug) / "docs" / "as-built"
    missing: List[str] = []
    for name in AS_BUILT_FILES:
        path = root / name
        if not path.exists():
            missing.append(f"missing docs/as-built/{name}")
            continue
        text = path.read_text(encoding="utf-8", errors="ignore").strip()
        if len(text) < 80 or _has_placeholders(text):
            missing.append(f"fill docs/as-built/{name} (cite paths; no _TODO_)")
    return missing


def _ignore_copy(directory: str, names: List[str]) -> List[str]:
    skipped = []
    for name in names:
        if name in COPY_SKIP:
            skipped.append(name)
    return skipped


def materialize_source(slug: str, source: str) -> Tuple[Path, str]:
    """Clone or copy into projects/<slug>. Returns (dest, action)."""
    dest = project_dir(slug)
    source = (source or "").strip()
    if not source:
        raise ValueError("--from is required (git URL or local path)")

    if dest.exists() and not any(dest.iterdir()):
        dest.rmdir()

    if dest.exists() and any(dest.iterdir()):
        if looks_like_application_source(dest) or (dest / "status.json").exists():
            return dest, "existing"
        raise ValueError(
            f"projects/{slug}/ exists but is not a recognizable app or studio project"
        )

    if is_git_url(source):
        dest.parent.mkdir(parents=True, exist_ok=True)
        result = subprocess.run(
            ["git", "clone", source, str(dest)],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "git clone failed")
        return dest, "cloned"

    src_path = Path(source).expanduser().resolve()
    if not src_path.exists() or not src_path.is_dir():
        raise ValueError(f"source path not found: {source}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src_path, dest, ignore=_ignore_copy, dirs_exist_ok=False)
    return dest, "copied"


def _write_status_adopt(root: Path, slug: str, archetype: str) -> None:
    path = root / "status.json"
    if path.exists():
        data = load_status_file(root)
        data["mode"] = "adopt"
        data["name"] = data.get("name") or slug
        data["archetype"] = data.get("archetype") or archetype
        data["design_scope"] = data.get("design_scope") or "as-built"
        data["last_update"] = datetime.now().strftime("%Y-%m-%d")
        if "human_gates" not in data:
            data["human_gates"] = {}
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        return
    status = {
        "name": slug,
        "phase": "0",
        "gate": "0",
        "gate_status": "open",
        "mode": "adopt",
        "created": datetime.now().strftime("%Y-%m-%d"),
        "last_update": datetime.now().strftime("%Y-%m-%d"),
        "archetype": archetype,
        "current_sprint": None,
        "active_ticket": None,
        "gate_history": [],
        "human_gates": {},
        "design_scope": "as-built",
    }
    path.write_text(json.dumps(status, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _copy_as_built_templates(root: Path) -> List[Path]:
    dest_dir = root / "docs" / "as-built"
    dest_dir.mkdir(parents=True, exist_ok=True)
    created: List[Path] = []
    for name in AS_BUILT_FILES:
        dest = dest_dir / name
        if dest.exists():
            continue
        tpl = AS_BUILT_TPL / name
        if tpl.exists():
            dest.write_text(tpl.read_text(encoding="utf-8"), encoding="utf-8")
        else:
            dest.write_text(f"# {name}\n\n_TODO_\n", encoding="utf-8")
        created.append(dest)
    return created


def overlay_studio(root: Path, slug: str, archetype: str = "saas-application") -> Dict[str, object]:
    """Add studio folders/docs without deleting application source."""
    from init_project_env import (
        create_phases_scaffold,
        init_project_gitignore,
        seed_definitions,
    )
    from ui_kit_peers import ensure_project_kit_peers, write_ui_kit_setup

    notes: List[str] = []
    for rel in OVERLAY_DIRS:
        (root / rel).mkdir(parents=True, exist_ok=True)

    seed_definitions(root)
    create_phases_scaffold(root)
    write_ui_kit_setup(root)
    notes.append("docs/setup/ui-kit.md")
    for pkg in ensure_project_kit_peers(root):
        notes.append(f"kit peers merged → {pkg.relative_to(root)}")
    created_as_built = _copy_as_built_templates(root)

    surface_map = root / "docs" / "ia" / "surface-map.md"
    if not surface_map.exists():
        surface_map.write_text(
            f"# Surface map — {slug}\n\n"
            "> Adopt mode: map **existing** surfaces (from `docs/as-built/01-surfaces.md`). "
            "Do not invent a greenfield IA.\n\n"
            "| Surface | Route / entry | Placement | Status |\n"
            "|---------|---------------|-----------|--------|\n"
            "| _TODO_ | | | shipped / partial / stub |\n",
            encoding="utf-8",
        )
        notes.append("docs/ia/surface-map.md")

    design_md = root / "design" / "DESIGN.md"
    if not design_md.exists():
        design_md.write_text(
            f"# Design truth — {slug} (adopt)\n\n"
            "> Document **what exists**. Do not scaffold a parallel Next.js prototype.\n\n"
            "## Visual direction (from the live product)\n\n_TODO_ — cite tokens/CSS.\n\n"
            "## Surface map\n\nSee `docs/ia/surface-map.md` and `docs/as-built/01-surfaces.md`.\n\n"
            "## Debt vs studio-library\n\n_TODO_ — gaps become LO-*; do not copy project UI into the library.\n",
            encoding="utf-8",
        )
        notes.append("design/DESIGN.md")

    scope_md = root / "design" / "DESIGN-SCOPE.md"
    if not scope_md.exists():
        scope_md.write_text(
            f"# Design scope — {slug}\n\n"
            "- **scope:** as-built (existing product)\n"
            "- **Date:** {datetime.now().strftime('%Y-%m-%d')}\n\n"
            "Gate 2 approves the design **of what exists** plus debt. "
            "Mocks only for net-new surfaces in `docs/as-built/07-implemented-vs-gap.md`.\n",
            encoding="utf-8",
        )
        notes.append("design/DESIGN-SCOPE.md")

    val = root / "docs" / "intake" / "validation.json"
    if not val.exists():
        val.write_text(
            json.dumps(
                {
                    "is_valid": True,
                    "source": "adopt",
                    "note": "PRD will be synthesized from as-built + intent. Gate 0 also requires filled docs/as-built/.",
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        notes.append("docs/intake/validation.json")

    _write_status_adopt(root, slug, archetype)

    briefing = root / "agent-briefing.md"
    if not briefing.exists():
        briefing.write_text(
            f"# Agent Briefing — {slug} (adopt)\n\n"
            "This project was **adopted** with a live codebase. Follow "
            "`.quinsy-studio/process/brownfield-adopt.md`.\n\n"
            "1. Fill `docs/as-built/` from code (cite paths; no `_TODO_`)\n"
            "2. Synthesize `docs/intake/prd.md` from as-built + intent\n"
            f"3. Human: `./studio approve {slug} --gate 0`\n"
            "4. Blueprint **as-is** + ADRs for existing decisions\n"
            f"5. Human: `./studio approve {slug} --gate 1`\n"
            "6. Design truth of existing UI — **do not** create `design/prototype/` as a fake app\n"
            f"7. Human: `./studio approve {slug} --gate 2` then `--milestones`\n"
            "8. Tickets for active milestone → `./studio execute`\n",
            encoding="utf-8",
        )
        notes.append("agent-briefing.md")

    runbook = root / "RUNBOOK.md"
    if not runbook.exists():
        runbook.write_text(
            f"# RUNBOOK — {slug} (adopt)\n\n"
            "See `.quinsy-studio/process/brownfield-adopt.md`.\n\n"
            "## As-built\n"
            "Fill `docs/as-built/00-product.md` … `07-implemented-vs-gap.md`.\n\n"
            "## Gates\n"
            f"`./studio approve {slug} --gate 0|1|2` then `--milestones`.\n\n"
            "## Execute\n"
            f"`./studio execute {slug}` until HITL.\n",
            encoding="utf-8",
        )
        notes.append("RUNBOOK.md")

    init_project_gitignore(root)

    if not has_runnable_env(root):
        notes.append("no docker/compose found — document how to run in as-built 06-quality.md (do not assume a studio docker template)")
    else:
        notes.append("existing run/docker left in place")

    if (root / ".git").exists():
        notes.append("existing .git preserved")
    else:
        notes.append("no .git in dest — init only if the human wants a new project repo")

    return {
        "as_built": [str(p.relative_to(root)) for p in created_as_built],
        "notes": notes,
    }


def copy_intent(root: Path, intent_path: Optional[str]) -> Optional[Path]:
    if not intent_path:
        return None
    src = Path(intent_path).expanduser()
    if not src.is_absolute():
        src = (STUDIO_ROOT / src).resolve()
    if not src.exists():
        raise ValueError(f"intent file not found: {intent_path}")
    dest = root / "docs" / "intake" / "adopt-intent.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
    return dest


def adopt_project(
    slug: str,
    source: str,
    *,
    intent: Optional[str] = None,
    archetype: str = "saas-application",
) -> Dict[str, object]:
    dest, action = materialize_source(slug, source)
    overlay = overlay_studio(dest, slug, archetype=archetype)
    intent_dest = copy_intent(dest, intent)
    return {
        "slug": slug,
        "path": str(dest),
        "source_action": action,
        "intent": str(intent_dest.relative_to(dest)) if intent_dest else None,
        **overlay,
    }
