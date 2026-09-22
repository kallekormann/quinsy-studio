#!/usr/bin/env python3
"""
Immediate studio harvest — classify a learning the moment it is identified,
write it into studio HQ (inbox + LO-*) when **portable**, else project-local log.

Does not copy project code or client names into playbooks/library.
Train only when LO declares train_skills (ability gap).
"""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from ticket_helpers import render_ticket_markdown
from studio_hq_lock import hq_write_lock

try:
    from studio_portability import (
        append_project_local_learning,
        portability_verdict,
        resolve_project_from_source,
        sanitize_observation,
        train_skills_for_kind,
    )
    from studio_learnings_store import (
        INBOX_PATH as STORE_INBOX,
        LEARNINGS_ROOT,
        commit_principle,
        compact_inbox,
        ensure_inbox_header,
        topic_relpath,
    )
except ImportError:  # pragma: no cover
    from studio_tools.studio_portability import (  # type: ignore
        append_project_local_learning,
        portability_verdict,
        resolve_project_from_source,
        sanitize_observation,
        train_skills_for_kind,
    )
    from studio_tools.studio_learnings_store import (  # type: ignore
        INBOX_PATH as STORE_INBOX,
        LEARNINGS_ROOT,
        commit_principle,
        compact_inbox,
        ensure_inbox_header,
        topic_relpath,
    )

TOOLS_DIR = Path(__file__).parent
QUINSY_STUDIO = TOOLS_DIR.parent
BACKLOG_OPEN = QUINSY_STUDIO / "backlog" / "open"
BACKLOG_DONE = QUINSY_STUDIO / "backlog" / "done"
BACKLOG_BLOCKED = QUINSY_STUDIO / "backlog" / "blocked"
LEARNINGS_DIR = LEARNINGS_ROOT
INBOX_PATH = STORE_INBOX

# kind → (signal, infusion_path, skills, role, team)
KIND_MAP: Dict[str, Dict[str, object]] = {
    "ui-component": {
        "signal": "library-gap",
        "path": "knowledge-base/learnings/library/components.md",
        "skills": ["UX-005", "FE-002", "SO-001"],
        "role": "UI/Interaction Designer (Director)",
        "team": "10-product-design-experience",
        "playbook": "knowledge-base/atomic-design-playbook.md",
    },
    "package": {
        "signal": "library-gap",
        "path": "knowledge-base/learnings/library/packages.md",
        "skills": ["SO-001", "BE-001"],
        "role": "Studio Automation Engineer (Director)",
        "team": "09-studio-operations-evolution",
        "playbook": "studio-library/library_registry.md",
    },
    "design": {
        "signal": "design-gap",
        "path": "knowledge-base/learnings/design/visual.md",
        "skills": ["UX-005", "UX-001"],
        "role": "Product Designer (Director)",
        "team": "10-product-design-experience",
        "playbook": "knowledge-base/design_playbook.md",
    },
    "ux": {
        "signal": "design-gap",
        "path": "knowledge-base/learnings/design/interaction.md",
        "skills": ["UX-002", "UX-004"],
        "role": "UX Designer (Director)",
        "team": "10-product-design-experience",
        "playbook": "knowledge-base/design-science-playbook.md",
    },
    "ia": {
        "signal": "design-gap",
        "path": "knowledge-base/learnings/design/information-architecture.md",
        "skills": ["UX-003"],
        "role": "Information Architect (Director)",
        "team": "10-product-design-experience",
        "playbook": "knowledge-base/contextual-ia-playbook.md",
    },
    "layout": {
        "signal": "design-gap",
        "path": "knowledge-base/learnings/design/layout.md",
        "skills": ["UX-003", "FE-002"],
        "role": "UX Designer (Director)",
        "team": "10-product-design-experience",
        "playbook": "knowledge-base/design_playbook.md",
    },
    "usability": {
        "signal": "design-gap",
        "path": "knowledge-base/learnings/design/interaction.md",
        "skills": ["UX-002", "FE-004"],
        "role": "UX Designer (Director)",
        "team": "10-product-design-experience",
        "playbook": "knowledge-base/design-science-playbook.md",
    },
    "frontend": {
        "signal": "knowledge-gap",
        "path": "knowledge-base/learnings/frontend/runtime.md",
        "skills": ["FE-001", "FE-003"],
        "role": "Frontend Architect (Director)",
        "team": "01-frontend-experience",
        "playbook": "knowledge-base/frontend_playbook.md",
    },
    "backend": {
        "signal": "knowledge-gap",
        "path": "knowledge-base/learnings/backend/services.md",
        "skills": ["BE-001", "BE-004"],
        "role": "Backend Architect (Director)",
        "team": "02-backend-systems",
        "playbook": "knowledge-base/backend_playbook.md",
    },
    "database": {
        "signal": "knowledge-gap",
        "path": "knowledge-base/learnings/backend/data.md",
        "skills": ["BE-002"],
        "role": "Database Specialist (Director)",
        "team": "02-backend-systems",
        "playbook": "knowledge-base/backend_playbook.md",
    },
    "security": {
        "signal": "knowledge-gap",
        "path": "knowledge-base/learnings/backend/security.md",
        "skills": ["PE-003", "BE-001"],
        "role": "Backend Security Specialist (Director)",
        "team": "08-platform-enterprise-engineering",
        "playbook": "knowledge-base/skill-extensions/frontend-security-auditor.md",
    },
    "process": {
        "signal": "process-gap",
        "path": "knowledge-base/learnings/process/workflow.md",
        "skills": ["SO-002"],
        "role": "Process Guard (Director)",
        "team": "09-studio-operations-evolution",
        "playbook": "process/learning-loop.md",
    },
    "tooling": {
        "signal": "tooling-gap",
        "path": "knowledge-base/learnings/process/tooling.md",
        "skills": ["SO-001"],
        "role": "Studio Automation Engineer (Director)",
        "team": "09-studio-operations-evolution",
        "playbook": "process/gates.md",
    },
}

KEYWORD_KINDS: List[Tuple[str, Tuple[str, ...]]] = [
    ("ui-component", ("atom", "molecule", "organism", "component", "button", "dialog", "modal", "sticker")),
    ("package", ("package", "promote", "boilerplate", "auth module", "billing")),
    ("ia", ("information architecture", "placement", "surface map", "ia ", "navigation ia")),
    ("usability", ("usability", "a11y", "accessibility", "empty state", "discover")),
    ("layout", ("layout", "chrome", "dock", "rail", "h-dvh", "overflow", "gutter")),
    ("ux", ("ux", "delight", "motion", "affordance", "mental model")),
    ("design", ("design spec", "token", "fidelity", "visual", "sticker sheet")),
    ("security", ("security", "xss", "csrf", "cors", "csp", "authz", "bola", "ssrf")),
    ("database", ("indexeddb", "dexie", "postgres", "schema", "migration", "sql")),
    ("backend", ("api", "endpoint", "server", "webhook", "queue")),
    ("frontend", ("next.js", "react", "tailwind", "bundle", "client")),
    ("tooling", ("cli", "gate", "playwright", "tooling", "studio-tools")),
]


def _slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:60] or "learning"


def _norm_title(title: str) -> str:
    return re.sub(r"\s+", " ", title.lower()).strip()[:80]


def classify_learning(text: str, *, path: str = "", signal: str = "") -> str:
    """Return infusion kind from free text + optional file path."""
    blob = f"{path} {text} {signal}".lower()
    if path.startswith("packages/") or "/packages/" in path:
        return "package"
    if path.startswith("ui/components/") or "ui/components/" in path:
        return "ui-component"
    if signal in ("gate-fail", "tooling-gap", "slow-gate"):
        if not any(k in blob for k in ("design", "ux", "layout", "component")):
            return "tooling"
    if signal == "design-gap":
        return "design"
    if signal == "library-gap":
        return "package" if "package" in blob else "ui-component"
    for kind, keys in KEYWORD_KINDS:
        if any(k in blob for k in keys):
            return kind
    if signal == "knowledge-gap":
        return "frontend"
    if signal in ("process-gap", "rework", "sloppy-code", "conflict"):
        return "process"
    return "process"


def kind_meta(kind: str) -> Dict[str, object]:
    return KIND_MAP.get(kind, KIND_MAP["process"])


def next_lo_id() -> str:
    numbers: List[int] = []
    for folder in (BACKLOG_OPEN, BACKLOG_DONE, BACKLOG_BLOCKED):
        if not folder.exists():
            continue
        for path in folder.glob("LO-*.md"):
            match = re.search(r"LO-(\d+)", path.name)
            if match:
                numbers.append(int(match.group(1)))
    return f"LO-{(max(numbers) + 1) if numbers else 0:04d}"


def _rel(path: Path) -> str:
    try:
        return str(path.relative_to(QUINSY_STUDIO))
    except ValueError:
        return str(path)


def _existing_lo_match(norm: str) -> Optional[str]:
    """Exact normalized title only — prefix match would collide on shared stems."""
    for folder in (BACKLOG_OPEN, BACKLOG_DONE):
        if not folder.exists():
            continue
        for path in folder.glob("LO-*.md"):
            text = path.read_text(encoding="utf-8", errors="ignore")
            title_m = re.search(r"^title:\s*(.+)$", text, re.M)
            title = title_m.group(1).strip() if title_m else path.stem
            if _norm_title(title) == norm:
                match = re.search(r"(LO-\d+)", path.name)
                return match.group(1) if match else path.stem
    return None


def _ensure_inbox_header() -> None:
    ensure_inbox_header(inbox_path=INBOX_PATH)


def append_inbox(entry: Dict[str, str]) -> Path:
    with hq_write_lock("hq"):
        _ensure_inbox_header()
        observation = sanitize_observation(entry.get("observation") or entry.get("title") or "")
        block = (
            f"## {entry['id']} — {entry['title']}\n"
            f"- **When:** {entry['when']}\n"
            f"- **Source:** `{entry['source']}` (provenance only)\n"
            f"- **Kind:** {entry['kind']}\n"
            f"- **Infuse into:** `{entry['infusion_path']}`\n"
            f"- **Playbook:** `{entry['playbook']}`\n"
            f"- **Signal:** {entry['signal']}\n"
            f"- **Observation:** {observation}\n"
            f"- **Status:** inbox — generalize into topic file + playbook, CHANGELOG, close LO\n\n"
        )
        INBOX_PATH.write_text(INBOX_PATH.read_text(encoding="utf-8") + block, encoding="utf-8")
        compact_inbox(open_dir=BACKLOG_OPEN, inbox_path=INBOX_PATH, archive_dir=LEARNINGS_DIR / "archive")
        return INBOX_PATH


def harvest_identified_learning(
    title: str,
    *,
    source: str,
    signal: str = "",
    observation: str = "",
    path: str = "",
    kind: str = "",
    priority: str = "P1",
) -> Dict[str, object]:
    """
    Capture immediately into studio HQ when portable.

    Returns lo_id, kind, created. If not portable: created=False, dropped=True,
    and a project-local note may be written under projects/<p>/docs/.
    """
    title = (title or "").strip()
    if not title:
        raise ValueError("learning title required")
    observation = (observation or title).strip()

    verdict = portability_verdict(title, observation)
    if not verdict["portable"]:
        project = resolve_project_from_source(source)
        local_path = ""
        if project:
            written = append_project_local_learning(
                project,
                observation=observation,
                title=title,
                reason=str(verdict.get("reason") or "not portable"),
            )
            local_path = str(written) if written else ""
        return {
            "created": False,
            "dropped": True,
            "lo_id": "",
            "kind": kind or classify_learning(f"{title} {observation}", path=path, signal=signal),
            "signal": signal,
            "infusion_path": "",
            "reason": verdict.get("reason"),
            "local_log": local_path,
            "inbox": "",
        }

    title = str(verdict["title"])
    kind = kind or classify_learning(f"{title} {observation}", path=path, signal=signal)
    meta = kind_meta(kind)
    signal = signal or str(meta["signal"])
    skills = list(meta["skills"])  # type: ignore[arg-type]
    train_skills = train_skills_for_kind(kind, skills)
    infusion_path = topic_relpath(kind, title, observation)
    playbook = str(meta["playbook"])
    observation = sanitize_observation(observation)
    norm = _norm_title(title)
    existing = _existing_lo_match(norm)
    if existing:
        return {
            "created": False,
            "dropped": False,
            "lo_id": existing,
            "kind": kind,
            "signal": signal,
            "infusion_path": infusion_path,
            "train_skills": train_skills,
            "inbox": _rel(INBOX_PATH) if INBOX_PATH.exists() else "",
        }

    BACKLOG_OPEN.mkdir(parents=True, exist_ok=True)
    lo_id = next_lo_id()
    ticket = {
        "id": lo_id,
        "title": title[:120],
        "type": "studio-evolution",
        "status": "open",
        "phase": 6,
        "priority": priority,
        "estimate": "S",
        "team": meta["team"],
        "skills": skills,
        "assignee_role": meta["role"],
        "soll_zustand": (
            f"General rule lives in `{infusion_path}` so the next project cannot repeat this. "
            "No client / product names in studio HQ titles or infused body "
            "(provenance `--source` / CHANGELOG only)."
        ),
        "value": "Immediate harvest — portable principle only.",
        "signal": signal,
        "source": source,
        "infusion_kind": kind,
        "infusion_path": infusion_path,
        "train_skills": train_skills,
        "modification_files": [f".quinsy-studio/{infusion_path}", ".quinsy-studio/CHANGELOG.md"],
        "acceptance_criteria": [
            f"Inbox item {lo_id} generalized into `{infusion_path}` (or matching playbook/skill/package)",
            "Infused text passes portability gate (no project folder names outside provenance)",
            "CHANGELOG.md updated",
            "LO moved to backlog/done/",
        ],
        "scope": (
            f"Kind `{kind}`. Promote or author in `{infusion_path}` using `{playbook}`. "
            f"Principle title must stay product-agnostic. "
            f"Train skills: {train_skills or 'none (playbook-only)'}. "
            f"Observation (provenance): {observation[:350]}"
        ),
    }
    lo_file = BACKLOG_OPEN / f"{lo_id}-{_slugify(title)}.md"
    lo_file.write_text(render_ticket_markdown(ticket), encoding="utf-8")
    commit_principle(
        kind=kind,
        lo_id=lo_id,
        title=title[:120],
        observation=observation,
        root=LEARNINGS_DIR,
    )
    append_inbox(
        {
            "id": lo_id,
            "title": title[:120],
            "when": datetime.now().isoformat(timespec="seconds"),
            "source": source,
            "kind": kind,
            "infusion_path": infusion_path,
            "playbook": playbook,
            "signal": signal,
            "observation": observation[:600],
        }
    )
    if train_skills:
        try:
            from studio_train import enqueue_train

            for skill in train_skills[:2]:
                enqueue_train(str(skill), title, source="lo", observation=lo_id)
        except Exception:
            pass
    return {
        "created": True,
        "dropped": False,
        "lo_id": lo_id,
        "kind": kind,
        "signal": signal,
        "infusion_path": infusion_path,
        "train_skills": train_skills,
        "inbox": _rel(INBOX_PATH),
        "lo_path": _rel(lo_file),
    }



def harvest_retro_text(retro_text: str, source: str) -> List[Dict[str, object]]:
    """Auto-create LOs from filled retro bullets (badly / improve)."""
    results: List[Dict[str, object]] = []
    for section in (
        r"## What went badly\?\s*\n(.*?)(?=\n## |\Z)",
        r"## What can we improve\?\s*\n(.*?)(?=\n## |\Z)",
    ):
        match = re.search(section, retro_text, re.DOTALL | re.I)
        if not match:
            continue
        for raw in match.group(1).splitlines():
            line = raw.strip()
            if line.startswith("- "):
                line = line[2:].strip()
            if not line or line in ("...", "- ...") or line.endswith(": ..."):
                continue
            results.append(
                harvest_identified_learning(line[:80].rstrip("."), source=source, observation=line)
            )
    return results


# First-brand / client token trees stay in the project. Auto-opening HQ LOs for
# every file under packages/ui or theme-tokens floods the studio backlog.
_TOKEN_KIT_MARKERS = (
    "theme-tokens",
    "design-tokens",
    "/tokens/",
    "kit-utilities",
    "kit-root",
)
_REGISTRY_GENERIC_PACKAGES = (
    "packages/auth/",
    "packages/billing/",
    "packages/feature-gating/",
    "packages/color-extraction/",
    "packages/item-tags/",
    "packages/item-search/",
    "packages/canvas-export/",
    "packages/rate-limit/",
    "packages/slug/",
    "packages/password-gate/",
    "packages/rect-selection/",
    "packages/viewport-fit/",
)


def _normalized_reuse_path(path: str) -> str:
    return path.replace("\\", "/").lstrip("./")


def _is_token_kit_path(path: str) -> bool:
    lowered = _normalized_reuse_path(path).lower()
    return any(marker in lowered for marker in _TOKEN_KIT_MARKERS)


def _is_registry_generic_package(path: str) -> bool:
    normalized = _normalized_reuse_path(path)
    if not normalized.startswith("packages/"):
        return False
    parts = normalized.split("/")
    if len(parts) < 2 or not parts[1]:
        return False
    root = f"packages/{parts[1]}/"
    return root in _REGISTRY_GENERIC_PACKAGES


def harvest_reuse_items(items: List[Dict], source: str) -> List[Dict[str, object]]:
    """Uncovered generic registry packages → LOs. Token kits and project UI stay local."""
    results: List[Dict[str, object]] = []
    seen_packages: set[str] = set()
    for item in items:
        if item.get("covered"):
            continue
        action = item.get("action") or ""
        if action not in ("promote", "lo_ticket", "promote_or_local"):
            continue
        path = str(item.get("path") or "")
        if _is_token_kit_path(path):
            continue
        if _normalized_reuse_path(path).startswith("ui/"):
            continue
        if not _is_registry_generic_package(path):
            continue
        pkg = _normalized_reuse_path(path).split("/")[1]
        if pkg in seen_packages:
            continue
        seen_packages.add(pkg)
        ticket_id = str(item.get("ticket_id") or "")
        package_path = f"packages/{pkg}"
        harvested = harvest_identified_learning(
            f"Reuse harvest: generalize `{package_path}`",
            source=source,
            signal="library-gap",
            path=package_path,
            kind="package",
            observation=f"Sprint ticket {ticket_id} changed `{path}` without library promotion.",
        )
        harvested["path"] = package_path
        results.append(harvested)
    return results
