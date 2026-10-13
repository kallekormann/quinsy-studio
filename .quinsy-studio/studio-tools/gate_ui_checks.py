#!/usr/bin/env python3
"""Gate-5 UI checks that depend on the tickets in flight (LO-0399, LO-0400).

- `ui_ticket_in_flight`: a UI ticket sits in `backlog/implement/`, so token literals and
  native `<select>` become hard failures instead of advisories.
- `motion_findings`: a design-track ticket in flight must ship what its §2d Motion
  section names: every motion token the spec names appears in product UI, the product
  carries a `prefers-reduced-motion` path, and no kit component is wrapped in a second
  animation layer. The counts come from the spec; nothing here invents a threshold.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List

from backlog_paths import read_ticket_meta
from design_ticket_helpers import DESIGN_TRACK_TYPES, UI_IMPLEMENT_TYPES
from studio_skill_checks import _iter_ui_files

UI_SKILL_PREFIXES = ("FE-001", "FE-002", "UX-")
MOTION_TOKEN_RE = re.compile(r"--motion-[a-z0-9-]+")
MOTION_OFF_RE = re.compile(r"^\s*motion:\s*off\s*$", re.M | re.I)
SECTION_2D_RE = re.compile(
    r"(?:##\s*2d\.[^\n]*\bmotion\b|##\s+Motion\b)[^\n]*\n([\s\S]*?)(?=\n##\s|\Z)", re.I
)
KIT_IMPORT_RE = re.compile(r"from\s+['\"][^'\"]*(?:components/ui|studio-library|@/components/ui)[^'\"]*['\"]")
SECOND_LAYER_RE = re.compile(r"from\s+['\"](?:framer-motion|motion/react|react-spring|@react-spring/web)['\"]")
MOTION_WRAP_RE = re.compile(r"<motion\.[A-Za-z]+|<animated\.[A-Za-z]+")


def implement_tickets(project_dir: Path) -> List[Dict]:
    folder = project_dir / "backlog" / "implement"
    if not folder.is_dir():
        return []
    return [read_ticket_meta(p) for p in sorted(folder.glob("*.md"))]


def _is_ui(meta: Dict) -> bool:
    ttype = (meta.get("ticket_type") or "").strip()
    if ttype in UI_IMPLEMENT_TYPES or ttype in DESIGN_TRACK_TYPES:
        return True
    skills = meta.get("skills") or ""
    return any(prefix in skills for prefix in UI_SKILL_PREFIXES)


def ui_ticket_in_flight(project_dir: Path) -> bool:
    return any(_is_ui(m) for m in implement_tickets(project_dir))


def _ui_blob(project_dir: Path) -> str:
    parts: List[str] = []
    for path in _iter_ui_files(project_dir):
        try:
            parts.append(path.read_text(encoding="utf-8", errors="ignore"))
        except OSError:
            continue
    for css in list(project_dir.rglob("*.css"))[:200]:
        if any(part in ("node_modules", ".next", "dist") for part in css.parts):
            continue
        try:
            parts.append(css.read_text(encoding="utf-8", errors="ignore"))
        except OSError:
            continue
    return "\n".join(parts)


def second_layer_findings(project_dir: Path) -> List[str]:
    out: List[str] = []
    for path in _iter_ui_files(project_dir):
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if KIT_IMPORT_RE.search(text) and SECOND_LAYER_RE.search(text) and MOTION_WRAP_RE.search(text):
            out.append(
                f"motion: {path.relative_to(project_dir)} wraps a kit component in a second animation layer — "
                "kit components already animate; use the motion tokens instead"
            )
    return out


def motion_findings(project_dir: Path) -> List[str]:
    """Empty list when no design-track ticket is in flight or every §2d promise is shipped."""
    tickets = [m for m in implement_tickets(project_dir) if (m.get("ticket_type") or "") in DESIGN_TRACK_TYPES]
    if not tickets:
        return []
    findings: List[str] = []
    blob = None
    for meta in tickets:
        tid = meta.get("id") or ""
        spec = project_dir / "docs" / "design-specs" / f"{tid}.md"
        if not spec.exists():
            continue
        spec_text = spec.read_text(encoding="utf-8", errors="ignore")
        if MOTION_OFF_RE.search(spec_text) or MOTION_OFF_RE.search(meta.get("body") or ""):
            continue
        match = SECTION_2D_RE.search(spec_text)
        if not match:
            continue
        if blob is None:
            blob = _ui_blob(project_dir)
        tokens = sorted(set(MOTION_TOKEN_RE.findall(match.group(1))))
        for token in tokens:
            if token not in blob:
                findings.append(f"motion: {tid} §2d names `{token}` but no product UI or CSS uses it")
        if "prefers-reduced-motion" not in blob:
            findings.append(f"motion: {tid} §2d promises a reduced-motion path; no `prefers-reduced-motion` rule in product CSS")
    if tickets and blob is not None:
        findings.extend(second_layer_findings(project_dir))
    return findings
