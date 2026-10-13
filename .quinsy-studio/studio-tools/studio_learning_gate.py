#!/usr/bin/env python3
"""Studio learning infusion status — open LOs do not block product IMPLEMENT or sprint."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

QUINSY_STUDIO = Path(__file__).parent.parent
BACKLOG_OPEN = QUINSY_STUDIO / "backlog" / "open"
BACKLOG_DONE = QUINSY_STUDIO / "backlog" / "done"


def _parse_lo_frontmatter(text: str) -> Dict[str, str]:
    fields: Dict[str, str] = {}
    if not text.startswith("---"):
        return fields
    parts = text.split("---", 2)
    if len(parts) < 3:
        return fields
    for line in parts[1].splitlines():
        match = re.match(r"^(\w+):\s*(.+)$", line.strip())
        if match:
            fields[match.group(1)] = match.group(2).strip().strip("'\"")
    return fields


def open_lo_tickets() -> List[Dict[str, str]]:
    """Return open studio learning items (LO-*) sorted by priority."""
    if not BACKLOG_OPEN.exists():
        return []
    items: List[Dict[str, str]] = []
    for path in sorted(BACKLOG_OPEN.glob("LO-*.md")):
        meta = _parse_lo_frontmatter(path.read_text(encoding="utf-8", errors="ignore"))
        try:
            rel = str(path.relative_to(QUINSY_STUDIO))
        except ValueError:
            rel = str(path)
        items.append(
            {
                "id": meta.get("id", path.stem.split("-")[0] + "-" + path.stem.split("-")[1])
                if "-" in path.stem
                else path.stem,
                "title": meta.get("title", path.stem),
                "priority": meta.get("priority", "P2"),
                "signal": meta.get("signal", ""),
                "infusion_kind": meta.get("infusion_kind", ""),
                "infusion_path": meta.get("infusion_path", ""),
                "train_skills": meta.get("train_skills", ""),
                "path": rel,
            },
        )
    # Fix id extraction - use LO-NNNN from filename
    for item in items:
        match = re.search(r"(LO-\d+)", Path(item["path"]).name)
        if match:
            item["id"] = match.group(1)
    priority_order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
    items.sort(key=lambda x: (priority_order.get(x.get("priority", "P2"), 9), x["id"]))
    return items


def infusion_gate_message(open_items: Optional[List[Dict[str, str]]] = None) -> Optional[str]:
    """Block message when open LO tickets must be implemented before next project sprint."""
    items = open_items if open_items is not None else open_lo_tickets()
    if not items:
        return None
    lines = [
        f"{len(items)} open studio learning item(s) (LO-*). Product IMPLEMENT is not blocked.",
        "Idle product loop → STUDIO_LO. Mid-sprint: ./studio train (then ./studio train --done when infused).",
        "Harvest is immediate (inbox + LO) **only when portable**. Skill gaps enqueue train; playbook-only LOs skip the queue.",
        "",
        "Open items:",
    ]
    for item in items[:12]:
        lines.append(f"  • {item['id']} [{item.get('priority', 'P2')}] {item.get('title', '')[:72]}")
    if len(items) > 12:
        lines.append(f"  … and {len(items) - 12} more")
    try:
        from studio_portability import open_lo_title_portability_failures, scan_hq_for_project_nouns
    except ImportError:  # pragma: no cover
        open_lo_title_portability_failures = None  # type: ignore
        scan_hq_for_project_nouns = None  # type: ignore
    if open_lo_title_portability_failures:
        bad = open_lo_title_portability_failures(items)
        if bad:
            lines.extend(["", "⚠️  Non-portable open LO titles (rewrite or move to project-local log):"])
            for b in bad[:6]:
                lines.append(f"  • {b['id']}: {b['reason'][:90]}")
    if scan_hq_for_project_nouns:
        hq_hits = scan_hq_for_project_nouns()
        if hq_hits:
            lines.extend(
                [
                    "",
                    f"⚠️  Portability: {len(hq_hits)} HQ doc hit(s) with project folder names "
                    "(fix or confine to provenance lines):",
                ]
            )
            for h in hq_hits[:8]:
                lines.append(f"  • {h['path']}:{h['line']} ({h['noun']}) {h['snippet'][:60]}")
    lines.extend(
        [
            "",
            "Run: ./studio learn-list",
            "Per lesson: ./studio train <LO> (impact; high waits for --approve) → infusion-delta --lo <LO> → CHANGELOG line → ./studio train --done <LO>",
            "Then: ./studio infusion  (verify gate clear)",
        ],
    )
    return "\n".join(lines)


def can_infuse_project_sprint() -> Tuple[bool, str]:
    """Open LOs no longer block project sprints (parallel train). Message is informational."""
    items = open_lo_tickets()
    if not items:
        return True, ""
    msg = infusion_gate_message(items)
    return True, msg or ""
