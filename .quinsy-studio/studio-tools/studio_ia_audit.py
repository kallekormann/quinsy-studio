#!/usr/bin/env python3
"""Parse design-spec IA nav metrics and wrap design_math.ia_nav_audit.

CLI:
  python3 studio_ia_audit.py <spec.md>
  python3 studio_ia_audit.py --top N --depth M

Studio:
  ./studio ia-audit <project> <TICKET>
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import List, Optional, Tuple

from design_math import ia_nav_audit

IA_NAV_INLINE = re.compile(
    r"ia_nav\s*:\s*\{\s*top\s*:\s*(\d+)\s*,\s*depth\s*:\s*(\d+)\s*\}",
    re.I,
)
IA_NAV_YAML = re.compile(
    r"^ia_nav:\s*\n(?:[ \t]+(?:top|depth):\s*\d+\s*\n){2}",
    re.I | re.M,
)
TOP_LINE = re.compile(
    r"top[- ]level(?:\s+items)?\s*[:\|]\s*(\d+)",
    re.I,
)
DEPTH_LINE = re.compile(
    r"(?:max\s+)?depth\s*[:\|]\s*(\d+)",
    re.I,
)
YAML_TOP = re.compile(r"^\s+top:\s*(\d+)\s*$", re.I | re.M)
YAML_DEPTH = re.compile(r"^\s+depth:\s*(\d+)\s*$", re.I | re.M)


def parse_ia_nav_counts(text: str) -> Optional[Tuple[int, int]]:
    """Return (top, depth) when the spec documents both metrics."""
    if not text:
        return None
    m = IA_NAV_INLINE.search(text)
    if m:
        return int(m.group(1)), int(m.group(2))
    yt = YAML_TOP.search(text)
    yd = YAML_DEPTH.search(text)
    if yt and yd and "ia_nav" in text.lower():
        return int(yt.group(1)), int(yd.group(1))
    tm = TOP_LINE.search(text)
    dm = DEPTH_LINE.search(text)
    if tm and dm:
        return int(tm.group(1)), int(dm.group(1))
    return None


def ia_nav_findings(text: str) -> List[str]:
    """Missing metrics or ia_nav_audit warnings."""
    parsed = parse_ia_nav_counts(text)
    if parsed is None:
        return [
            "IA nav metrics missing — document `ia_nav: { top: N, depth: M }` "
            "or Top-level items / Max depth in spec § Navigation IA"
        ]
    top, depth = parsed
    return ia_nav_audit(top, depth)


def ia_nav_error_for_ticket(spec_text: str, ticket_type: str) -> Optional[str]:
    """Hard gate for ia-navigation approve-design."""
    if (ticket_type or "").strip() != "ia-navigation":
        return None
    findings = ia_nav_findings(spec_text)
    if not findings:
        return None
    return "IA nav audit: " + "; ".join(findings)


def format_ia_audit_report(findings: List[str]) -> str:
    if not findings:
        return "IA nav audit: pass"
    lines = ["IA nav audit: fail"]
    for f in findings:
        lines.append(f"  - {f}")
    return "\n".join(lines)


def main(argv: List[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] in ("-h", "--help"):
        print("Usage: studio_ia_audit.py <spec.md> | --top N --depth M")
        return 0
    if argv[0] == "--top" and len(argv) >= 4 and argv[2] == "--depth":
        findings = ia_nav_audit(int(argv[1]), int(argv[3]))
        print(format_ia_audit_report(findings))
        return 0 if not findings else 1
    path = Path(argv[0])
    if not path.exists():
        print(f"Spec not found: {path}")
        return 2
    findings = ia_nav_findings(path.read_text(encoding="utf-8", errors="ignore"))
    print(format_ia_audit_report(findings))
    return 0 if not findings else 1


if __name__ == "__main__":
    sys.exit(main())
