#!/usr/bin/env python3
"""Studio learning infusion gate — open LO tickets block project sprint until closed."""

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
        items.append(
            {
                "id": meta.get("id", path.stem.split("-")[0] + "-" + path.stem.split("-")[1])
                if "-" in path.stem
                else path.stem,
                "title": meta.get("title", path.stem),
                "priority": meta.get("priority", "P2"),
                "signal": meta.get("signal", ""),
                "path": str(path.relative_to(QUINSY_STUDIO)),
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
        f"{len(items)} open studio learning item(s) (LO-*) must be infused before the next project sprint.",
        "Studio learnings → skills / process / tooling / studio-library — not project code.",
        "",
        "Open items:",
    ]
    for item in items[:12]:
        lines.append(f"  • {item['id']} [{item.get('priority', 'P2')}] {item.get('title', '')[:72]}")
    if len(items) > 12:
        lines.append(f"  … and {len(items) - 12} more")
    lines.extend(
        [
            "",
            "Run: ./studio learn-list",
            "Implement in .quinsy-studio/ → move LO to backlog/done/ → CHANGELOG entry",
            "Then: ./studio infusion  (verify gate clear)",
        ],
    )
    return "\n".join(lines)


def can_infuse_project_sprint() -> Tuple[bool, str]:
    """True when no open LO tickets remain."""
    msg = infusion_gate_message()
    if msg:
        return False, msg
    return True, ""
