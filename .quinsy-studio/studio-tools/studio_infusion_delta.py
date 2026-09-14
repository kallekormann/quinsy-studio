#!/usr/bin/env python3
"""Deterministic playbook deltas (ACE curator). Never rewrite the whole file."""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path
from typing import Dict, List, Optional

QUINSY_STUDIO = Path(__file__).parent.parent
OPS = ("add", "update", "remove")
ID_RE = re.compile(r"\*\*(PB-[0-9]{8}-\d+)\*\*")


def _resolve_path(rel: str) -> Path:
    raw = (rel or "").strip()
    path = Path(raw)
    if not path.is_absolute():
        if raw.startswith(".quinsy-studio/"):
            path = QUINSY_STUDIO.parent / raw
        elif raw.startswith("knowledge-base/") or raw.startswith("process/"):
            path = QUINSY_STUDIO / raw
        else:
            path = QUINSY_STUDIO / raw
    try:
        path.resolve().relative_to(QUINSY_STUDIO.resolve())
    except ValueError as exc:
        raise ValueError("infusion-delta path must stay under .quinsy-studio/") from exc
    return path


def next_bullet_id(text: str) -> str:
    stamp = date.today().strftime("%Y%m%d")
    nums = [int(m.group(1)) for m in re.finditer(rf"PB-{stamp}-(\d+)", text)]
    n = (max(nums) + 1) if nums else 1
    return f"PB-{stamp}-{n:03d}"


def _refuse_rewrite(body: str, existing: str) -> None:
    body = (body or "").strip()
    if not body:
        raise ValueError("delta body is empty")
    if len(body) > 4000:
        raise ValueError("delta too large — split or use --op update on one bullet")
    if existing and len(body) > max(800, int(len(existing) * 0.45)):
        raise ValueError("delta looks like a full-file rewrite — use ADD/UPDATE/REMOVE on one bullet")


def apply_delta(
    rel_path: str,
    op: str,
    *,
    section: str = "Deltas",
    body: str = "",
    bullet_id: str = "",
) -> Dict:
    op = (op or "").strip().lower()
    if op not in OPS:
        raise ValueError(f"op must be add|update|remove, got {op!r}")
    path = _resolve_path(rel_path)
    if not path.exists():
        raise FileNotFoundError(str(path))
    text = path.read_text(encoding="utf-8")
    if op == "add":
        _refuse_rewrite(body, text)
        bid = next_bullet_id(text)
        bullet = f"- **{bid}** helpful=0 harmful=0 :: {body.strip()}\n"
        heading = f"## {section.strip() or 'Deltas'}"
        if heading in text:
            # insert after heading line
            parts = text.split(heading, 1)
            after = parts[1]
            path.write_text(parts[0] + heading + "\n\n" + bullet + after.lstrip("\n"), encoding="utf-8")
        else:
            path.write_text(text.rstrip() + f"\n\n{heading}\n\n{bullet}", encoding="utf-8")
        return {"op": "add", "id": bid, "path": str(path.relative_to(QUINSY_STUDIO))}
    bid = (bullet_id or "").strip()
    if not bid:
        raise ValueError("update/remove require --id PB-YYYYMMDD-NNN")
    if bid not in text:
        raise ValueError(f"bullet {bid} not found in {path.name}")
    lines = text.splitlines(keepends=True)
    out: List[str] = []
    found = False
    for line in lines:
        if bid in line and line.lstrip().startswith("-"):
            found = True
            if op == "remove":
                continue
            _refuse_rewrite(body, text)
            out.append(f"- **{bid}** helpful=0 harmful=0 :: {body.strip()}\n")
            continue
        out.append(line)
    if not found:
        raise ValueError(f"bullet {bid} is not a list item")
    path.write_text("".join(out), encoding="utf-8")
    return {"op": op, "id": bid, "path": str(path.relative_to(QUINSY_STUDIO))}


COUNTS_RE = re.compile(r"helpful=(\d+)\s+harmful=(\d+)")


def bump_counts(rel_path: str, bullet_id: str, *, helpful: int = 0, harmful: int = 0) -> Dict:
    """Increment ACE helpful/harmful counters on one bullet."""
    path = _resolve_path(rel_path)
    bid = (bullet_id or "").strip()
    if not bid:
        raise ValueError("bullet id required")
    text = path.read_text(encoding="utf-8")
    if bid not in text:
        raise ValueError(f"bullet {bid} not found in {path.name}")
    out: List[str] = []
    found = False
    h_new = d_new = 0
    for line in text.splitlines(keepends=True):
        if bid in line and line.lstrip().startswith("-"):
            found = True
            match = COUNTS_RE.search(line)
            h = int(match.group(1)) if match else 0
            d = int(match.group(2)) if match else 0
            h_new = h + max(0, helpful)
            d_new = d + max(0, harmful)
            if match:
                line = COUNTS_RE.sub(f"helpful={h_new} harmful={d_new}", line, count=1)
            else:
                line = line.replace(f"**{bid}**", f"**{bid}** helpful={h_new} harmful={d_new}", 1)
            out.append(line)
            continue
        out.append(line)
    if not found:
        raise ValueError(f"bullet {bid} is not a list item")
    path.write_text("".join(out), encoding="utf-8")
    return {"id": bid, "helpful": h_new, "harmful": d_new, "path": str(path.relative_to(QUINSY_STUDIO))}

