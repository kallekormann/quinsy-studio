#!/usr/bin/env python3
"""
Durable studio learnings store.

inbox.md is the *open* harvest queue only.
Durable principles live in knowledge-base/learnings/<domain>/<topic>.md
and are indexed in index.md for CARD / ./studio learn-find.
"""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from studio_hq_lock import hq_write_lock

TOOLS_DIR = Path(__file__).parent
QUINSY_STUDIO = TOOLS_DIR.parent
LEARNINGS_ROOT = QUINSY_STUDIO / "knowledge-base" / "learnings"
INBOX_PATH = LEARNINGS_ROOT / "inbox.md"
INDEX_PATH = LEARNINGS_ROOT / "index.md"
ARCHIVE_DIR = LEARNINGS_ROOT / "archive"

KIND_DOMAIN = {
    "ui-component": "library",
    "package": "library",
    "design": "design",
    "ux": "design",
    "ia": "design",
    "layout": "design",
    "usability": "design",
    "frontend": "frontend",
    "backend": "backend",
    "database": "backend",
    "security": "backend",
    "process": "process",
    "tooling": "process",
}

KIND_TOPIC = {
    "ui-component": "components",
    "package": "packages",
    "design": "visual",
    "ux": "interaction",
    "ia": "information-architecture",
    "layout": "layout",
    "usability": "interaction",
    "frontend": "runtime",
    "backend": "services",
    "database": "data",
    "security": "security",
    "process": "workflow",
    "tooling": "tooling",
}

TOPIC_KEYWORDS: Tuple[Tuple[str, Tuple[str, ...]], ...] = (
    ("queues", ("queue", "worker", "horizon", "bullmq")),
    ("credentials", ("credential", ".env", "secret", "api_credentials")),
    ("host-resolution", ("canonicalhost", "canonical host", "host header", "host-scope")),
    ("cache", ("revalidate", "cache-bust", "cache")),
    ("canvas", ("konva", "canvas", "2d")),
    ("inbox", ("inbox", "feedback inbox")),
    ("gates", ("gate", "gold-path", "playwright")),
    ("sprint-cadence", ("cadence review", "sprint complete")),
)

DOMAIN_PLAYBOOK = {
    "library": "studio-library/library_registry.md",
    "design": "knowledge-base/design_playbook.md",
    "frontend": "knowledge-base/frontend_playbook.md",
    "backend": "knowledge-base/backend_playbook.md",
    "process": "process/learning-loop.md",
}

TEAM_LEARNING_CATALOG = {
    "01-frontend-experience": "knowledge-base/learnings/frontend/README.md",
    "02-backend-systems": "knowledge-base/learnings/backend/README.md",
    "03-compliance-legal": "knowledge-base/learnings/backend/README.md",
    "04-product-strategy-architecture": "knowledge-base/learnings/design/README.md",
    "08-platform-enterprise-engineering": "knowledge-base/learnings/backend/README.md",
    "09-studio-operations-evolution": "knowledge-base/learnings/process/README.md",
    "10-product-design-experience": "knowledge-base/learnings/design/README.md",
    "11-growth-design": "knowledge-base/learnings/design/README.md",
}

INBOX_HEADER = """# Studio learning inbox

Open harvest queue only. Do **not** Read this file on IMPLEMENT.

Durable principles live in `knowledge-base/learnings/<domain>/<topic>.md`.
Find them via [index.md](index.md) or `./studio learn-find "<topic>"`.
Infused / stale entries are in `archive/`.

See [learning-loop.md](../../process/learning-loop.md).

"""

_ENTRY_START = re.compile(r"^## (LO-\d+) — ", re.M)
_LO_OPEN = re.compile(r"(LO-\d+)")


def topic_for(kind: str, blob: str = "") -> Tuple[str, str]:
    domain = KIND_DOMAIN.get(kind or "", "process")
    lower = (blob or "").lower()
    topic = KIND_TOPIC.get(kind or "", "workflow")
    for name, keys in TOPIC_KEYWORDS:
        if any(k in lower for k in keys):
            topic = name
            break
    return domain, topic


def topic_relpath(kind: str, title: str = "", observation: str = "") -> str:
    domain, topic = topic_for(kind, f"{title} {observation}")
    return f"knowledge-base/learnings/{domain}/{topic}.md"


def _ensure_domain_readme(domain: str, *, root: Optional[Path] = None) -> Path:
    folder = (root or LEARNINGS_ROOT) / domain
    folder.mkdir(parents=True, exist_ok=True)
    readme = folder / "README.md"
    playbook = DOMAIN_PLAYBOOK.get(domain, "process/learning-loop.md")
    if not readme.exists():
        readme.write_text(
            f"# {domain.title()} learnings\n\n"
            f"Portable studio principles for this domain. "
            f"Also infuse `{playbook}` / matching skills on train.\n\n"
            "Topic files in this folder are the durable store. "
            "Inbox is only the open queue.\n\n"
            "## Topics\n\n"
            "_Generated — see files in this folder._\n",
            encoding="utf-8",
        )
    return readme


def ensure_topic_file(
    kind: str, title: str = "", observation: str = "", *, root: Optional[Path] = None
) -> Path:
    domain, topic = topic_for(kind, f"{title} {observation}")
    root = root or LEARNINGS_ROOT
    _ensure_domain_readme(domain, root=root)
    path = root / domain / f"{topic}.md"
    playbook = DOMAIN_PLAYBOOK.get(domain, "process/learning-loop.md")
    if not path.exists():
        path.write_text(
            f"# {domain} / {topic}\n\n"
            f"Portable studio principles (not project incidents).\n"
            f"Matching playbook/skill: `{playbook}`.\n\n"
            "## Principles\n\n",
            encoding="utf-8",
        )
    return path


def commit_principle(
    *,
    kind: str,
    lo_id: str,
    title: str,
    observation: str,
    root: Optional[Path] = None,
) -> str:
    """Append one principle to the domain topic file and rebuild the index."""
    from studio_portability import refuse_product_nouns_in_hq_body, sanitize_observation

    root = root or LEARNINGS_ROOT
    refuse_product_nouns_in_hq_body(f"{title}\n{observation}")
    with hq_write_lock("hq"):
        return _commit_principle_locked(
            kind=kind, lo_id=lo_id, title=title, observation=observation, root=root
        )


def _commit_principle_locked(
    *,
    kind: str,
    lo_id: str,
    title: str,
    observation: str,
    root: Path,
) -> str:
    from studio_portability import sanitize_observation
    path = ensure_topic_file(kind, title, observation, root=root)
    text = path.read_text(encoding="utf-8")
    if lo_id and lo_id in text:
        rebuild_index(root=root)
        return str(path)
    clean = sanitize_observation(observation or title)
    stamp = date.today().isoformat()
    bullet = f"- **{lo_id}** {stamp} :: {title.strip()}\n  - {clean}\n"
    if "## Principles" in text:
        parts = text.split("## Principles", 1)
        path.write_text(
            parts[0] + "## Principles\n\n" + bullet + parts[1].lstrip("\n"),
            encoding="utf-8",
        )
    else:
        path.write_text(text.rstrip() + "\n\n## Principles\n\n" + bullet, encoding="utf-8")
    _refresh_domain_topics(KIND_DOMAIN.get(kind or "", "process"), root=root)
    rebuild_index(root=root)
    try:
        return str(path.relative_to(QUINSY_STUDIO))
    except ValueError:
        return str(path)


def _refresh_domain_topics(domain: str, *, root: Optional[Path] = None) -> None:
    folder = (root or LEARNINGS_ROOT) / domain
    if not folder.is_dir():
        return
    readme = _ensure_domain_readme(domain, root=root)
    lines = [
        f"# {domain.title()} learnings\n",
        "",
        f"Portable studio principles. Playbook: `{DOMAIN_PLAYBOOK.get(domain, 'process/learning-loop.md')}`.\n",
        "",
        "On IMPLEMENT, Read the topic file that matches the ticket — not `inbox.md`.\n",
        "",
        "## Topics\n",
    ]
    for path in sorted(folder.glob("*.md")):
        if path.name.lower() == "readme.md":
            continue
        first = path.read_text(encoding="utf-8", errors="ignore").splitlines()[:1]
        label = first[0].lstrip("# ").strip() if first else path.stem
        lines.append(f"- [{path.stem}]({path.name}) — {label}")
    readme.write_text("\n".join(lines) + "\n", encoding="utf-8")


def rebuild_index(*, root: Optional[Path] = None) -> Path:
    root = root or LEARNINGS_ROOT
    root.mkdir(parents=True, exist_ok=True)
    index_path = root / "index.md"
    rows: List[str] = [
        "# Studio learnings catalog\n",
        "",
        "Durable store for portable principles. **Inbox is the open queue only.**",
        "IMPLEMENT: Read the domain README + topic file from the CARD, not `inbox.md` or `archive/`.",
        "",
        "`./studio learn-find \"<query>\"` searches this catalog.\n",
        "",
        "| Domain | Topic | File | Principles |",
        "|--------|-------|------|------------|",
    ]
    for domain_dir in sorted(
        p for p in root.iterdir() if p.is_dir() and p.name not in ("archive",)
    ):
        for path in sorted(domain_dir.glob("*.md")):
            if path.name.lower() == "readme.md":
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            count = len(re.findall(r"^- \*\*LO-\d+", text, re.M))
            try:
                rel = str(path.relative_to(QUINSY_STUDIO))
            except ValueError:
                rel = f"knowledge-base/learnings/{domain_dir.name}/{path.name}"
            rows.append(f"| {domain_dir.name} | {path.stem} | `{rel}` | {count} |")
    index_path.write_text("\n".join(rows) + "\n", encoding="utf-8")
    return index_path


def search_learnings(query: str, *, limit: int = 20) -> List[Dict[str, str]]:
    q = (query or "").strip().lower()
    if not q:
        return []
    hits: List[Dict[str, str]] = []
    for path in LEARNINGS_ROOT.glob("*/*.md"):
        if "archive" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if q not in text.lower() and q not in str(path).lower():
            continue
        try:
            rel = str(path.relative_to(QUINSY_STUDIO))
        except ValueError:
            rel = str(path)
        for line in text.splitlines():
            if line.startswith("- **LO-") and q in line.lower():
                hits.append({"path": rel, "line": line.strip()[:200]})
            elif q in path.stem.lower() and line.startswith("# "):
                hits.append({"path": rel, "line": line.strip()[:200]})
        if not any(h["path"] == rel for h in hits):
            hits.append({"path": rel, "line": path.stem})
        if len(hits) >= limit:
            break
    return hits[:limit]


def parse_inbox_entries(text: str) -> List[str]:
    starts = [m.start() for m in _ENTRY_START.finditer(text)]
    if not starts:
        return []
    blocks: List[str] = []
    for i, start in enumerate(starts):
        end = starts[i + 1] if i + 1 < len(starts) else len(text)
        blocks.append(text[start:end])
    return blocks


def _entry_lo_id(block: str) -> str:
    match = _ENTRY_START.search(block)
    return match.group(1) if match else ""


def _entry_status(block: str) -> str:
    match = re.search(r"- \*\*Status:\*\*\s*(.+)", block)
    return (match.group(1).strip() if match else "").lower()


def _entry_when_month(block: str) -> str:
    match = re.search(r"- \*\*When:\*\*\s*(\d{4}-\d{2})", block)
    if match:
        return match.group(1)
    return date.today().strftime("%Y-%m")


def _open_lo_ids(open_dir: Path) -> set:
    ids = set()
    if not open_dir.is_dir():
        return ids
    for path in open_dir.glob("LO-*.md"):
        match = _LO_OPEN.search(path.name)
        if match:
            ids.add(match.group(1))
    return ids


def compact_inbox(
    *,
    open_dir: Optional[Path] = None,
    inbox_path: Optional[Path] = None,
    archive_dir: Optional[Path] = None,
) -> Dict[str, int]:
    """Keep only still-open harvest rows in inbox.md; archive the rest by month."""
    with hq_write_lock("hq"):
        return _compact_inbox_locked(
            open_dir=open_dir, inbox_path=inbox_path, archive_dir=archive_dir
        )


def _compact_inbox_locked(
    *,
    open_dir: Optional[Path] = None,
    inbox_path: Optional[Path] = None,
    archive_dir: Optional[Path] = None,
) -> Dict[str, int]:
    inbox = inbox_path or INBOX_PATH
    archive = archive_dir or ARCHIVE_DIR
    if not inbox.exists():
        inbox.parent.mkdir(parents=True, exist_ok=True)
        inbox.write_text(INBOX_HEADER, encoding="utf-8")
        return {"kept": 0, "archived": 0}
    text = inbox.read_text(encoding="utf-8")
    prefix = text.split("## LO-", 1)[0] if "## LO-" in text else INBOX_HEADER
    if "Open harvest queue" not in prefix:
        prefix = INBOX_HEADER
    blocks = parse_inbox_entries(text)
    backlog_open = open_dir or (QUINSY_STUDIO / "backlog" / "open")
    open_ids = _open_lo_ids(backlog_open)
    kept: List[str] = []
    archived_by_month: Dict[str, List[str]] = {}
    for block in blocks:
        lo_id = _entry_lo_id(block)
        status = _entry_status(block)
        still_open = lo_id in open_ids and status.startswith("inbox")
        if still_open:
            kept.append(block if block.endswith("\n") else block + "\n")
            continue
        month = _entry_when_month(block)
        archived_by_month.setdefault(month, []).append(
            block if block.endswith("\n") else block + "\n"
        )
    archive.mkdir(parents=True, exist_ok=True)
    archived_n = 0
    for month, chunks in archived_by_month.items():
        dest = archive / f"inbox-{month}.md"
        existing = dest.read_text(encoding="utf-8") if dest.exists() else (
            f"# Inbox archive — {month}\n\n"
            "Closed / infused harvest rows. Not for IMPLEMENT. See index.md for live principles.\n\n"
        )
        dest.write_text(existing.rstrip() + "\n\n" + "\n".join(chunks), encoding="utf-8")
        archived_n += len(chunks)
    inbox.write_text(prefix.rstrip() + "\n" + "".join(kept), encoding="utf-8")
    return {"kept": len(kept), "archived": archived_n}


def ensure_inbox_header(*, inbox_path: Optional[Path] = None) -> None:
    inbox = inbox_path or INBOX_PATH
    inbox.parent.mkdir(parents=True, exist_ok=True)
    if not inbox.exists():
        inbox.write_text(INBOX_HEADER, encoding="utf-8")
