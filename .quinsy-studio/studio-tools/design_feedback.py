#!/usr/bin/env python3
"""Design push-back capture (LO-0405, LO-0406).

Every time the human pushes back on design — `approve-design --reject`, a finish-gate HOLD,
`feedback`/`clarify --design-reason` — the reason gets a code, lands in the product's
`docs/design-specs/pushback-log.md`, and is harvested into studio HQ when portable.
Team 10 reads the log per ticket, the retro `## Design` section counts it per sprint, and
the milestone review carries it across milestones.
"""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

# code -> (label, harvest kind, learnings topic, one-line meaning)
REJECT_REASONS: Dict[str, Tuple[str, str, str, str]] = {
    "hierarchy": ("Hierarchy", "design", "visual", "the eye does not land where the task starts; levels are not distinct"),
    "density": ("Density", "layout", "layout", "too much or too little on the surface for the job; rhythm is off"),
    "motion": ("Motion", "ux", "interaction", "transitions missing, wrong, or decorative; reduced-motion path absent"),
    "copy": ("Copy", "ux", "craft", "microcopy is generic, blames, or fails the error rubric"),
    "flow": ("Flow", "ux", "interaction", "steps or states are missing; the path does not match the job"),
    "uniqueness": ("Uniqueness", "design", "craft", "looks like the default kit or a template, not this product"),
    "a11y": ("Accessibility", "usability", "interaction", "contrast, focus, keyboard, or announcement gap"),
    "brand": ("Brand", "design", "visual", "off the signed DESIGN.md: tokens, voice, or imagery drift"),
}

LOG_REL = "docs/design-specs/pushback-log.md"
_ENTRY = re.compile(r"^- (?P<date>\d{4}-\d{2}-\d{2}) \| (?P<ticket>\S+) \| (?P<source>[\w-]+) \| (?P<code>[a-z0-9]+) \| (?P<note>.*)$")


def reason_codes() -> List[str]:
    return list(REJECT_REASONS)


def reason_help() -> str:
    width = max(len(c) for c in REJECT_REASONS)
    return "\n".join(f"  {code:<{width}}  {meta[3]}" for code, meta in REJECT_REASONS.items())


def validate_reason(code: str) -> Optional[str]:
    code = (code or "").strip().lower()
    if code in REJECT_REASONS:
        return None
    return f"--reason must be one of: {', '.join(REJECT_REASONS)}"


def pushback_log_path(project_root: Path) -> Path:
    return project_root / LOG_REL


def append_pushback(project_root: Path, ticket_id: str, code: str, note: str, source: str) -> Path:
    """One line per push-back. `source` is reject | finish-hold | feedback | clarify."""
    code = code.strip().lower()
    path = pushback_log_path(project_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.is_file():
        path.write_text(
            "# Design push-back log\n\n"
            "Every human push-back on design, coded. Team 10 reads the lines for the ticket before writing the next spec; "
            "the retro counts them per code; the milestone review carries the top codes forward.\n\n"
            "Codes: " + ", ".join(REJECT_REASONS) + "\n\n",
            encoding="utf-8",
        )
    stamp = datetime.now().strftime("%Y-%m-%d")
    clean = re.sub(r"\s+", " ", (note or "").strip()) or REJECT_REASONS[code][3]
    with path.open("a", encoding="utf-8") as fh:
        fh.write(f"- {stamp} | {ticket_id} | {source} | {code} | {clean}\n")
    return path


def read_pushback(project_root: Path) -> List[Dict[str, str]]:
    path = pushback_log_path(project_root)
    if not path.is_file():
        return []
    out: List[Dict[str, str]] = []
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        m = _ENTRY.match(line)
        if m:
            out.append(m.groupdict())
    return out


def pushback_for(project_root: Path, ticket_ids: Sequence[str]) -> List[Dict[str, str]]:
    wanted = set(ticket_ids)
    return [e for e in read_pushback(project_root) if e["ticket"] in wanted]


def code_counts(entries: Sequence[Dict[str, str]]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for e in entries:
        counts[e["code"]] = counts.get(e["code"], 0) + 1
    return dict(sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])))


# code -> the studio rule a push-back of that kind re-states (principle-shaped for the harvest)
RULE_STEMS: Dict[str, str] = {
    "hierarchy": "A surface must put the primary action where the eye lands first; levels must stay distinct",
    "density": "A surface must match its density to the job; rhythm and whitespace must not fight the task",
    "motion": "Every state change must name its transition and a reduced-motion path; motion must never decorate",
    "copy": "Microcopy must say what happened and what to do next in the user's words; never generic, never blame",
    "flow": "A flow must cover every step and state the job needs; the path must match the user's goal",
    "uniqueness": "A surface must carry the product's own moves; it must never read as the default kit or a template",
    "a11y": "Contrast, focus, keyboard path and announcements must pass before a surface is shown for sign-off",
    "brand": "Every value and string must trace to the signed DESIGN.md and tokens; drift must become a token ticket",
}


def harvest_pushback(project: str, ticket_id: str, code: str, note: str) -> Dict[str, object]:
    """Send the push-back into the HQ learning loop as a principle. Ticket id stays in the project log only."""
    from studio_harvest import harvest_identified_learning

    label, kind, _topic, meaning = REJECT_REASONS[code]
    stem = RULE_STEMS[code]
    detail = (note or "").strip()
    title = f"{stem} — {label.lower()} push-back: {detail[:60]}" if detail else stem
    observation = f"{stem}. Human push-back ({label.lower()}): {detail or meaning}."
    return harvest_identified_learning(
        title,
        source=project,
        signal="design-gap",
        observation=observation,
        kind=kind,
        priority="P1",
    )


def record_pushback(project: str, project_root: Path, ticket_id: str, code: str, note: str, source: str) -> Dict[str, object]:
    """Log + harvest. Returns the harvest result with the log path added."""
    path = append_pushback(project_root, ticket_id, code, note, source)
    try:
        result = harvest_pushback(project, ticket_id, code, note)
    except Exception as exc:  # the log line must survive a harvest hiccup
        result = {"created": False, "dropped": True, "reason": str(exc), "lo_id": ""}
    result["log"] = str(path)
    return result


def retro_design_section(project_root: Path, ticket_ids: Sequence[str]) -> str:
    """`## Design` block for the sprint retro: counts per code and the lines themselves."""
    entries = pushback_for(project_root, ticket_ids)
    if not entries:
        return "## Design\n- No design push-back recorded this sprint (reject, finish HOLD, design feedback).\n"
    counts = code_counts(entries)
    lines = ["## Design", "", "| Code | Count | Meaning |", "|------|-------|---------|"]
    for code, n in counts.items():
        lines.append(f"| {code} | {n} | {REJECT_REASONS.get(code, ('', '', '', ''))[3]} |")
    lines += ["", "Lines:"]
    lines += [f"- {e['ticket']} · {e['source']} · {e['code']} — {e['note']}" for e in entries]
    top = next(iter(counts))
    lines += ["", f"Carry forward: the next design phase reads `{LOG_REL}` and the `{top}` lines before writing a spec."]
    return "\n".join(lines) + "\n"


def finish_hold_code(finish_text: str) -> str:
    """Reason code from a finish-gate file (`Reason: <code>` line) — defaults to `uniqueness`."""
    m = re.search(r"^\s*Reason:\s*([a-z0-9]+)", finish_text or "", re.M | re.I)
    code = (m.group(1).lower() if m else "")
    return code if code in REJECT_REASONS else "uniqueness"


def set_design_rejected(content: str) -> str:
    """Flip the ticket's design_status back to pending so the next design phase picks it up."""
    if re.search(r"^design_status:", content, re.M):
        return re.sub(r"^design_status:.*$", "design_status: pending", content, flags=re.M)
    return content


def to_json(result: Dict[str, object]) -> str:
    return json.dumps({k: v for k, v in result.items() if k in ("created", "dropped", "lo_id", "reason", "log")}, ensure_ascii=False)
