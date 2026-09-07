#!/usr/bin/env python3
"""
Immediate studio harvest — classify a learning the moment it is identified,
write it into studio HQ (inbox + LO-*), and queue parallel train (product IMPLEMENT continues).

Does not copy project code or client names into playbooks/library.
The inbox entry + classified LO is the capture; the train agent generalizes.
"""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from ticket_helpers import render_ticket_markdown

TOOLS_DIR = Path(__file__).parent
QUINSY_STUDIO = TOOLS_DIR.parent
BACKLOG_OPEN = QUINSY_STUDIO / "backlog" / "open"
BACKLOG_DONE = QUINSY_STUDIO / "backlog" / "done"
BACKLOG_BLOCKED = QUINSY_STUDIO / "backlog" / "blocked"
LEARNINGS_DIR = QUINSY_STUDIO / "knowledge-base" / "learnings"
INBOX_PATH = LEARNINGS_DIR / "inbox.md"

# kind → (signal, infusion_path, skills, role, team)
KIND_MAP: Dict[str, Dict[str, object]] = {
    "ui-component": {
        "signal": "library-gap",
        "path": "studio-library/ui/components/",
        "skills": ["UX-005", "FE-002", "SO-001"],
        "role": "UI/Interaction Designer (Director)",
        "team": "10-product-design-experience",
        "playbook": "knowledge-base/atomic-design-playbook.md",
    },
    "package": {
        "signal": "library-gap",
        "path": "studio-library/packages/",
        "skills": ["SO-001", "BE-001"],
        "role": "Studio Automation Engineer (Director)",
        "team": "09-studio-operations-evolution",
        "playbook": "studio-library/library_registry.md",
    },
    "design": {
        "signal": "design-gap",
        "path": "knowledge-base/design_playbook.md",
        "skills": ["UX-005", "UX-001"],
        "role": "Product Designer (Director)",
        "team": "10-product-design-experience",
        "playbook": "knowledge-base/design_playbook.md",
    },
    "ux": {
        "signal": "design-gap",
        "path": "knowledge-base/design-science-playbook.md",
        "skills": ["UX-002", "UX-004"],
        "role": "UX Designer (Director)",
        "team": "10-product-design-experience",
        "playbook": "knowledge-base/design-science-playbook.md",
    },
    "ia": {
        "signal": "design-gap",
        "path": "knowledge-base/contextual-ia-playbook.md",
        "skills": ["UX-003"],
        "role": "Information Architect (Director)",
        "team": "10-product-design-experience",
        "playbook": "knowledge-base/contextual-ia-playbook.md",
    },
    "layout": {
        "signal": "design-gap",
        "path": "knowledge-base/design_playbook.md",
        "skills": ["UX-003", "FE-002"],
        "role": "UX Designer (Director)",
        "team": "10-product-design-experience",
        "playbook": "knowledge-base/design_playbook.md",
    },
    "usability": {
        "signal": "design-gap",
        "path": "knowledge-base/design-science-playbook.md",
        "skills": ["UX-002", "FE-004"],
        "role": "UX Designer (Director)",
        "team": "10-product-design-experience",
        "playbook": "knowledge-base/design-science-playbook.md",
    },
    "frontend": {
        "signal": "knowledge-gap",
        "path": "knowledge-base/frontend_playbook.md",
        "skills": ["FE-001", "FE-003"],
        "role": "Frontend Architect (Director)",
        "team": "01-frontend-experience",
        "playbook": "knowledge-base/frontend_playbook.md",
    },
    "backend": {
        "signal": "knowledge-gap",
        "path": "knowledge-base/backend_playbook.md",
        "skills": ["BE-001", "BE-004"],
        "role": "Backend Architect (Director)",
        "team": "02-backend-systems",
        "playbook": "knowledge-base/backend_playbook.md",
    },
    "database": {
        "signal": "knowledge-gap",
        "path": "knowledge-base/local-first-sync-playbook.md",
        "skills": ["BE-002"],
        "role": "Database Specialist (Director)",
        "team": "02-backend-systems",
        "playbook": "knowledge-base/backend_playbook.md",
    },
    "security": {
        "signal": "knowledge-gap",
        "path": "knowledge-base/skill-extensions/backend-security-auditor.md",
        "skills": ["PE-003", "BE-001"],
        "role": "Backend Security Specialist (Director)",
        "team": "08-platform-enterprise-engineering",
        "playbook": "knowledge-base/skill-extensions/frontend-security-auditor.md",
    },
    "process": {
        "signal": "process-gap",
        "path": "process/",
        "skills": ["SO-002"],
        "role": "Process Guard (Director)",
        "team": "09-studio-operations-evolution",
        "playbook": "process/learning-loop.md",
    },
    "tooling": {
        "signal": "tooling-gap",
        "path": "studio-tools/",
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
    LEARNINGS_DIR.mkdir(parents=True, exist_ok=True)
    if INBOX_PATH.exists():
        return
    INBOX_PATH.write_text(
        "# Studio learning inbox\n\n"
        "Entries are appended **when a learning is identified** (gate, retro, reuse, `./studio learn`).\n"
        "They are **generic** (no client product names). The agent promotes each item into the\n"
        "listed infusion path on `STUDIO_LO`, then moves the LO to `backlog/done/`.\n"
        "Do not copy project source here — generalize the rule or extract a library asset.\n\n",
        encoding="utf-8",
    )


def append_inbox(entry: Dict[str, str]) -> Path:
    _ensure_inbox_header()
    block = (
        f"## {entry['id']} — {entry['title']}\n"
        f"- **When:** {entry['when']}\n"
        f"- **Source:** `{entry['source']}` (provenance only)\n"
        f"- **Kind:** {entry['kind']}\n"
        f"- **Infuse into:** `{entry['infusion_path']}`\n"
        f"- **Playbook:** `{entry['playbook']}`\n"
        f"- **Signal:** {entry['signal']}\n"
        f"- **Observation:** {entry['observation']}\n"
        f"- **Status:** inbox — generalize into infusion path, CHANGELOG, close LO\n\n"
    )
    INBOX_PATH.write_text(INBOX_PATH.read_text(encoding="utf-8") + block, encoding="utf-8")
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
    Capture immediately into studio HQ. Returns lo_id, kind, created (False if deduped).
    """
    title = (title or "").strip()
    if not title:
        raise ValueError("learning title required")
    observation = (observation or title).strip()
    kind = kind or classify_learning(f"{title} {observation}", path=path, signal=signal)
    meta = kind_meta(kind)
    signal = signal or str(meta["signal"])
    norm = _norm_title(title)
    existing = _existing_lo_match(norm)
    if existing:
        return {
            "created": False,
            "lo_id": existing,
            "kind": kind,
            "signal": signal,
            "infusion_path": meta["path"],
        "inbox": _rel(INBOX_PATH) if INBOX_PATH.exists() else "",
                }

    BACKLOG_OPEN.mkdir(parents=True, exist_ok=True)
    lo_id = next_lo_id()
    infusion_path = str(meta["path"])
    playbook = str(meta["playbook"])
    ticket = {
        "id": lo_id,
        "title": title[:120],
        "type": "studio-evolution",
        "status": "open",
        "phase": 6,
        "priority": priority,
        "estimate": "S",
        "team": meta["team"],
        "skills": meta["skills"],
        "assignee_role": meta["role"],
        "soll_zustand": (
            f"General rule lives in `{infusion_path}` so the next project cannot repeat this. "
            "No client names in studio HQ."
        ),
        "value": "Immediate harvest — context is still in this session.",
        "signal": signal,
        "source": source,
        "infusion_kind": kind,
        "infusion_path": infusion_path,
        "modification_files": [f".quinsy-studio/{infusion_path}", ".quinsy-studio/CHANGELOG.md"],
        "acceptance_criteria": [
            f"Inbox item {lo_id} generalized into `{infusion_path}` (or matching playbook/skill/package)",
            "CHANGELOG.md updated",
            "LO moved to backlog/done/",
        ],
        "scope": (
            f"Kind `{kind}`. Promote or author in `{infusion_path}` using `{playbook}`. "
            f"Observation: {observation[:400]}"
        ),
    }
    lo_file = BACKLOG_OPEN / f"{lo_id}-{_slugify(title)}.md"
    lo_file.write_text(render_ticket_markdown(ticket), encoding="utf-8")
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
    return {
        "created": True,
        "lo_id": lo_id,
        "kind": kind,
        "signal": signal,
        "infusion_path": infusion_path,
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


def harvest_reuse_items(items: List[Dict], source: str) -> List[Dict[str, object]]:
    """Uncovered reuse paths → classified LOs immediately (no wait for --approve)."""
    results: List[Dict[str, object]] = []
    for item in items:
        if item.get("covered"):
            continue
        action = item.get("action") or ""
        if action not in ("promote", "lo_ticket", "promote_or_local"):
            continue
        path = str(item.get("path") or "")
        ticket_id = str(item.get("ticket_id") or "")
        kind = "package" if action == "promote" or path.startswith("packages/") else "ui-component"
        title = f"Reuse harvest: generalize `{path}`"
        harvested = harvest_identified_learning(
            title,
            source=source,
            signal="library-gap",
            path=path,
            kind=kind,
            observation=f"Sprint ticket {ticket_id} changed `{path}` without library promotion.",
        )
        harvested["path"] = path
        results.append(harvested)
    return results
