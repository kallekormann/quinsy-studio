#!/usr/bin/env python3
"""Keep the skill lists in sync (agency integration L13).

Four places name skills: `skill_matcher.INTERNAL_SKILLS` (what tickets can
carry), `ticket_helpers.SKILL_ROLE_MAP` (who owns it), the `skill_id:` line in
each `teams/*/skills/*.md` file, and `teams/skill-registry.md`. They drift when
one is edited alone. Errors are drift; warnings are template gaps.

    python3 lint_skills.py            # errors fail, warnings print
    python3 lint_skills.py --strict   # warnings fail too
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional

ID_RE = re.compile(r"\b([A-Z]{2}-\d{3})\b")
SKILL_ID_LINE = re.compile(r"^\**skill_id:\**\s*`?([A-Z]{2}-\d{3})`?\s*$", re.M)

# knowledge-base/skill-template.md — the sections every skill file carries.
TEMPLATE_SECTIONS = (
    ("Metadata", ("Metadata",)),
    ("Rules", ("Rules", "Core rules", "Principles")),
    ("Workflow", ("Workflow", "Process", "Steps")),
    ("Deliverables", ("Deliverables", "Output", "Outputs")),
    ("Done evidence", ("Done evidence", "Quality bar", "Acceptance")),
    ("Anti-patterns", ("Anti-patterns", "Anti patterns", "Never")),
    ("Handoff", ("Handoff", "Handoffs")),
)


@dataclass
class Finding:
    severity: str
    message: str

    def __str__(self) -> str:
        return f"{'❌' if self.severity == 'error' else '⚠️ '} {self.message}"


def _headings(text: str) -> List[str]:
    return [m.group(1).strip().lower() for m in re.finditer(r"^#{2,3}\s+(.+)$", text, re.M)]


def template_gaps(text: str) -> List[str]:
    heads = _headings(text)
    gaps = []
    if not re.search(r"^>\s*\S", text, re.M):
        gaps.append("Mission (opening `>` line)")
    for label, names in TEMPLATE_SECTIONS:
        if not any(h.startswith(n.lower()) for h in heads for n in names):
            gaps.append(label)
    return gaps


def file_ids(teams_dir: Path) -> Dict[str, List[str]]:
    """skill_id -> every file declaring it (more than one is a duplicate)."""
    found: Dict[str, List[str]] = {}
    for path in sorted(teams_dir.glob("*/skills/**/*.md")):
        if "reference" in path.parts:
            continue
        match = SKILL_ID_LINE.search(path.read_text(encoding="utf-8", errors="ignore")[:1500])
        if match:
            found.setdefault(match.group(1), []).append(str(path.relative_to(teams_dir.parent)))
    return found


def lint(
    internal: Iterable[str],
    roles: Dict[str, str],
    prefix_team: Dict[str, str],
    rule_skills: Iterable[str],
    teams_dir: Path,
    fixed_files: Optional[Dict[str, str]] = None,
) -> List[Finding]:
    internal = set(internal)
    out: List[Finding] = []
    declared = file_ids(teams_dir)
    files = {sid: paths[0] for sid, paths in declared.items()}
    for sid, rel in (fixed_files or {}).items():
        if ID_RE.fullmatch(sid):
            files.setdefault(sid, rel)
            declared.setdefault(sid, [rel])

    for sid in sorted(internal - set(roles)):
        out.append(Finding("error", f"{sid} is in skill_matcher but has no role in ticket_helpers.SKILL_ROLE_MAP"))
    for sid in sorted(set(roles) - internal):
        out.append(Finding("error", f"{sid} has a role but skill_matcher cannot match it"))
    for sid in sorted(internal - set(files)):
        out.append(Finding("error", f"{sid} has no skill file with a `skill_id: {sid}` line"))
    for sid in sorted(set(files) - internal):
        out.append(Finding("error", f"{files[sid]} declares {sid}, which skill_matcher does not know"))
    for sid, paths in sorted(declared.items()):
        if len(paths) > 1:
            out.append(Finding("error", f"{sid} is declared by more than one file: {', '.join(paths)}"))

    for sid, rel in sorted(files.items()):
        team = prefix_team.get(sid[:2])
        if not team:
            out.append(Finding("error", f"{sid}: prefix {sid[:2]} has no team in SKILL_PREFIX_TEAM"))
        elif f"teams/{team}/" not in rel:
            out.append(Finding("error", f"{sid} lives in {rel}, but prefix {sid[:2]} belongs to teams/{team}/"))

    for sid in sorted(set(rule_skills) - internal):
        out.append(Finding("error", f"staffing rule names {sid}, which skill_matcher does not know"))

    registry = teams_dir / "skill-registry.md"
    if not registry.exists():
        out.append(Finding("error", "teams/skill-registry.md is missing"))
    else:
        listed = set(ID_RE.findall(registry.read_text(encoding="utf-8", errors="ignore")))
        for sid in sorted(internal - listed):
            out.append(Finding("error", f"{sid} is missing from teams/skill-registry.md"))
        for sid in sorted(listed - internal - set(files)):
            out.append(Finding("error", f"teams/skill-registry.md names {sid}, which no skill file or matcher entry defines"))

    root = teams_dir.parent
    for sid, rel in sorted(files.items()):
        path = root / rel
        if not path.exists():
            continue
        gaps = template_gaps(path.read_text(encoding="utf-8", errors="ignore"))
        if gaps:
            out.append(Finding("warning", f"{rel} ({sid}) lacks template sections: {', '.join(gaps)}"))
    return out


def lint_studio() -> List[Finding]:
    from skill_matcher import _FIXED_SKILL_FILES, INTERNAL_SKILLS, STAFFING_RULES, TEAMS_DIR
    from ticket_helpers import SKILL_PREFIX_TEAM, SKILL_ROLE_MAP

    return lint(
        INTERNAL_SKILLS,
        SKILL_ROLE_MAP,
        SKILL_PREFIX_TEAM,
        [rule[0] for rule in STAFFING_RULES],
        TEAMS_DIR,
        _FIXED_SKILL_FILES,
    )


def main(argv: List[str]) -> int:
    strict = "--strict" in argv
    findings = lint_studio()
    errors = [f for f in findings if f.severity == "error"]
    warnings = [f for f in findings if f.severity == "warning"]
    for f in errors + warnings:
        print(f"  {f}")
    print(f"\n  skills lint: {len(errors)} error(s), {len(warnings)} template warning(s)")
    if errors or (strict and warnings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
