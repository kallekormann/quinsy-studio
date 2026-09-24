#!/usr/bin/env python3
"""HQ skill-enforcement scans (LO-0334 / LO-0338).

Warn (gate 5 soft): hardcoded #hex / rgb() in product UI; native <select>.
Hard (move … done): AI tickets need a filled ## Eval heading on the receipt.

Usage:
  python3 studio_skill_checks.py <project_dir>
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import List, Tuple

HEX_LITERAL = re.compile(r"#[0-9a-fA-F]{3,8}\b")
RGB_LITERAL = re.compile(r"\brgba?\s*\(", re.I)
NATIVE_SELECT = re.compile(r"<select\b", re.I)
SKILLS_LINE = re.compile(r"^skills:\s*(.+)$", re.M | re.I)
EVAL_HEADING = re.compile(r"^##\s*eval\b", re.I | re.M)
AI_EVAL_SKILLS = frozenset({"AI-001", "AI-004"})

UI_SUFFIXES = {".tsx", ".jsx", ".css", ".scss", ".vue", ".svelte"}
SKIP_DIR_NAMES = {
    "node_modules",
    ".next",
    "dist",
    "build",
    "coverage",
    "vendor",
    "__pycache__",
    "design-specs",
    "mocks",
}
ALLOWLIST_NAME_FRAGMENTS = (
    "token",
    "tokens.css",
    "tokens.ts",
    ".test.",
    ".spec.",
    "fixture",
    "storybook",
)
SCAN_ROOTS = ("app", "src", "resources/js", "resources/css")


def _is_allowlisted(path: Path) -> bool:
    name = path.name.lower()
    joined = str(path).lower()
    if any(frag in name or frag in joined for frag in ALLOWLIST_NAME_FRAGMENTS):
        return True
    if "ui/tokens" in joined or "/tokens/" in joined:
        return True
    if "studio-library" in joined:
        return True
    if "/primitives/" in joined or "/headless/" in joined:
        return True
    return False


def _iter_ui_files(project_dir: Path) -> List[Path]:
    files: List[Path] = []
    for root_name in SCAN_ROOTS:
        root = project_dir / root_name
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix.lower() not in UI_SUFFIXES:
                continue
            if any(part in SKIP_DIR_NAMES for part in path.parts):
                continue
            if _is_allowlisted(path):
                continue
            files.append(path)
    return files


def token_literal_warnings(project_dir: Path) -> List[str]:
    """Warn when product UI files use raw hex / rgb instead of tokens."""
    warnings: List[str] = []
    for path in _iter_ui_files(project_dir):
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if HEX_LITERAL.search(text) or RGB_LITERAL.search(text):
            rel = path.relative_to(project_dir)
            warnings.append(f"token-literal: {rel} contains #hex or rgb() (prefer tokens)")
    return warnings


def native_select_warnings(project_dir: Path) -> List[str]:
    """Warn native <select> in product UI (kit / Headless Select instead)."""
    warnings: List[str] = []
    for path in _iter_ui_files(project_dir):
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if NATIVE_SELECT.search(text):
            rel = path.relative_to(project_dir)
            warnings.append(f"native-select: {rel} uses <select> (use kit / Headless Select)")
    return warnings


def ticket_skill_ids(ticket_text: str) -> List[str]:
    m = SKILLS_LINE.search(ticket_text or "")
    if not m:
        return []
    raw = m.group(1).strip().strip("[]")
    return [p.strip().strip("\"'") for p in raw.split(",") if p.strip()]


def ai_eval_receipt_issues(receipt_text: str, ticket_text: str = "") -> List[str]:
    """Refuse AI-001 / AI-004 receipts that omit a filled ## Eval section."""
    skills = set(ticket_skill_ids(ticket_text))
    if not skills & AI_EVAL_SKILLS:
        return []
    match = EVAL_HEADING.search(receipt_text or "")
    if not match:
        return ["missing ## Eval (required when skills include AI-001 or AI-004)"]
    start = match.end()
    rest = receipt_text[start:]
    nxt = re.search(r"^##\s+", rest, re.M)
    body = rest[: nxt.start()] if nxt else rest
    lines = [
        ln.strip()
        for ln in body.splitlines()
        if ln.strip() and ln.strip() not in ("- ...", "...", "-", "- n/a")
    ]
    if not lines:
        return ["placeholder ## Eval (required when skills include AI-001 or AI-004)"]
    return []


def scan_project(project_dir: Path) -> Tuple[List[str], List[str]]:
    """Return (soft_warnings, hard_issues). Hard issues are unused at gate 5."""
    warns = token_literal_warnings(project_dir) + native_select_warnings(project_dir)
    return warns, []


def format_scan_report(warnings: List[str]) -> str:
    if not warnings:
        return "skill_application: no token-literal or native-select warnings"
    lines = [f"skill_application: {len(warnings)} warning(s) (soft — does not fail RESULT)"]
    for w in warnings[:40]:
        lines.append(f"  - {w}")
    if len(warnings) > 40:
        lines.append(f"  - … {len(warnings) - 40} more")
    return "\n".join(lines)


def main(argv: List[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv:
        print("Usage: studio_skill_checks.py <project_dir>")
        return 2
    project_dir = Path(argv[0]).resolve()
    if not project_dir.exists():
        print(f"Project dir not found: {project_dir}")
        return 2
    warnings, _hard = scan_project(project_dir)
    print(format_scan_report(warnings))
    return 0


if __name__ == "__main__":
    sys.exit(main())
