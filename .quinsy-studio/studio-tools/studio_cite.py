#!/usr/bin/env python3
"""ACE citation: receipt → helpful/harmful counters on playbook bullets."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Tuple

from studio_infusion_delta import QUINSY_STUDIO, bump_counts

PB_RE = re.compile(r"PB-\d{8}-\d+", re.I)
HELP_LINE = re.compile(r"helpful\s*:\s*(.+)", re.I)
HARM_LINE = re.compile(r"harmful\s*:\s*(.+)", re.I)
PATH_LINE = re.compile(r"playbook\s*:\s*(\S+)", re.I)


def _ids(raw: str) -> List[str]:
    if not raw or raw.strip().lower() in ("none", "-", "n/a"):
        return []
    return [m.group(0).upper().replace("PB-", "PB-") for m in PB_RE.finditer(raw)]


def parse_receipt_citations(text: str) -> Dict[str, object]:
    playbook = ""
    helpful: List[str] = []
    harmful: List[str] = []
    for line in (text or "").splitlines():
        pm = PATH_LINE.search(line)
        if pm:
            playbook = pm.group(1).strip().strip("`")
        hm = HELP_LINE.search(line)
        if hm:
            helpful.extend(_ids(hm.group(1)))
        dm = HARM_LINE.search(line)
        if dm:
            harmful.extend(_ids(dm.group(1)))
    return {"playbook": playbook, "helpful": helpful, "harmful": harmful}


def apply_receipt_citations(text: str, default_playbook: str = "") -> List[Dict]:
    parsed = parse_receipt_citations(text)
    path = str(parsed.get("playbook") or default_playbook or "")
    if not path:
        # CARD playbooks line: - CARD: knowledge-base/foo.md
        for line in (text or "").splitlines():
            if "knowledge-base/" in line and line.strip().startswith("-"):
                m = re.search(r"(knowledge-base/[^\s,]+)", line)
                if m:
                    path = m.group(1)
                    break
    if not path or (not parsed["helpful"] and not parsed["harmful"]):
        return []
    applied: List[Dict] = []
    for bid in parsed["helpful"]:
        applied.append(bump_counts(path, bid, helpful=1, harmful=0))
    for bid in parsed["harmful"]:
        applied.append(bump_counts(path, bid, helpful=0, harmful=1))
    return applied
