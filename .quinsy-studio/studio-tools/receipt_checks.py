#!/usr/bin/env python3
"""Receipt trust checks (agency integration L1, L6).

A receipt is the agent's own claim that a ticket is done. These checks make the
claim hard to fake:

- template text left as written counts as empty (L1)
- every `## Evidence` / `## API proof` line carries PASS, FAIL or NOT TESTED (L1)
- file paths named on the receipt must exist (screenshots, tests) (L1)
- a smoke check the gate did not run is NOT TESTED, never a silent pass (L1)
- the sections a ticket needs follow from its skills (L6)
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Set

QUINSY_DIR = Path(__file__).resolve().parent.parent

VERDICT_RE = re.compile(r"\b(PASS|FAIL|NOT TESTED)\b")
# Template hints: a whole line in parentheses, "(or: …)" alternatives, and the
# fixed sentences write_receipt_stub emits.
_PAREN_LINE = re.compile(r"^\(.*\)\.?$")
_OR_HINT = re.compile(r"\(or:", re.I)
STUB_SENTENCES = (
    "gate 5 green; ac covered by tests or route check",
    "route / user path a real user would take (lo-0051):",
    "screenshot: (path or none — function-only ticket)",
    "follow-ups: (noted here, not done in this ticket)",
)
_UNCHECKED = re.compile(r"^-\s*\[\s\]\s+")
_PATH_TOKEN = re.compile(
    r"(?<![\w:/.-])((?:\./)?[\w.@()\[\]-]+(?:/[\w.@()\[\]-]+)+\.(?:png|jpe?g|webp|gif|tsx?|m?js|py|json|md))\b"
)
_IMAGE = re.compile(r"\.(png|jpe?g|webp|gif)$", re.I)

UI_SKILL = re.compile(r"^(FE|UX)-\d{3}$")
API_PROOF_SKILLS = {"BE-001", "BE-003", "BE-007"}
THREAT_SKILLS = {"PE-005"}
RISK_SKILLS = {"BE-002", "BE-003", "PE-001", "PE-002"}
_RISK_TEXT = re.compile(r"\b(migrations?|schema change|auth(?:entication)?|login|infra(?:structure)?|deploy|coolify|docker)\b", re.I)


def section(text: str, *headings: str) -> Optional[str]:
    """Body of the first `## <heading>` that matches (case-insensitive); None when absent."""
    for heading in headings:
        match = re.search(rf"^##\s*{re.escape(heading)}\b[^\n]*$", text or "", re.I | re.M)
        if match:
            rest = text[match.end():]
            nxt = re.search(r"^##\s+", rest, re.M)
            return rest[: nxt.start()] if nxt else rest
    return None


def _content_lines(body: str) -> List[str]:
    return [ln.strip() for ln in (body or "").splitlines() if ln.strip()]


def is_stub_line(line: str) -> bool:
    bare = line.strip().lstrip("-").strip()
    if bare in ("", "...", "…"):
        return True
    if _PAREN_LINE.match(bare) or _OR_HINT.search(bare):
        return True
    return bare.lower() in STUB_SENTENCES


def section_is_stub(body: Optional[str]) -> bool:
    lines = _content_lines(body or "")
    return not lines or all(is_stub_line(ln) for ln in lines)


def unchecked_ac(text: str) -> List[str]:
    body = section(text, "AC coverage", "AC", "Acceptance") or ""
    return [ln for ln in _content_lines(body) if _UNCHECKED.match(ln)]


def verdict_issues(heading: str, body: Optional[str], *, need_pass: bool) -> List[str]:
    """Each claim line states PASS, FAIL or NOT TESTED. FAIL blocks done."""
    if body is None:
        return []
    issues: List[str] = []
    passes = 0
    for line in _content_lines(body):
        if is_stub_line(line):
            continue
        verdicts = VERDICT_RE.findall(line)
        if not verdicts:
            issues.append(f"## {heading}: `{line[:60]}` has no PASS / FAIL / NOT TESTED")
            continue
        verdict = verdicts[0]
        if verdict == "FAIL":
            issues.append(f"## {heading}: FAIL — `{line[:60]}`. Fix it, or file a follow-up and say NOT TESTED with why")
        elif verdict == "NOT TESTED":
            if not re.search(r"NOT TESTED\s*[—–:-]+\s*\S", line):
                issues.append(f"## {heading}: NOT TESTED needs a reason after a dash — `{line[:60]}`")
        else:
            passes += 1
            if not (_PATH_TOKEN.search(line) or "`" in line):
                issues.append(f"## {heading}: PASS needs proof (a file path or a `command`) — `{line[:60]}`")
    if need_pass and passes == 0:
        issues.append(f"## {heading}: at least one PASS with proof is required")
    return issues


def missing_paths(text: str, roots: Sequence[Path]) -> List[str]:
    """Relative file paths on the receipt that exist under none of the roots."""
    missing: List[str] = []
    seen: Set[str] = set()
    claims = "\n".join(ln for ln in (text or "").splitlines() if not is_stub_line(ln))
    for match in _PATH_TOKEN.finditer(claims):
        token = match.group(1)
        if token in seen or token.startswith(("http", "www.")):
            continue
        seen.add(token)
        rel = token.lstrip("./") if token.startswith("./") else token
        if not any((root / rel).exists() for root in roots):
            missing.append(token)
    return missing


def ticket_skills(ticket_blob: str) -> Set[str]:
    """Skills on the ticket plus required PM-004 companions (same set the CARD shows)."""
    meta, body = ticket_blob or "", ticket_blob or ""
    if meta.startswith("---"):
        parts = meta.split("---", 2)
        if len(parts) >= 3:
            meta, body = parts[1], parts[2]
    match = re.search(r"^skills:\s*(.*)$", meta, re.M)
    raw = match.group(1) if match else ""
    skills = set(re.findall(r"\b[A-Z]{2}-\d{3}\b", raw))
    try:
        from skill_matcher import staff_skills

        title = re.search(r"^title:\s*(.*)$", meta, re.M)
        ttype = re.search(r"^ticket_type:\s*(.*)$", meta, re.M)
        staffed = staff_skills(
            title.group(1) if title else "",
            body,
            skills=sorted(skills),
            ticket_type=ttype.group(1).strip() if ttype else "",
        )
        skills |= {sid for sid, _ in staffed["missing_required"]}
    except Exception:
        pass
    return skills


def required_sections(ticket_blob: str) -> Dict[str, str]:
    """Section name → why it is required for this ticket (L6)."""
    skills = ticket_skills(ticket_blob)
    from studio_design_discovery import ticket_is_ui

    ui = ticket_is_ui(ticket_blob) or any(UI_SKILL.match(s) for s in skills)
    need: Dict[str, str] = {
        "Security": "every ticket says what it changed for security (or `no new input, route or secret`)",
        "Scope": "every ticket lists follow-ups it noticed but did not do",
    }
    if ui:
        need["Evidence"] = "UI ticket: PASS / FAIL / NOT TESTED per state, with screenshot or test path"
        need["A11y"] = "UI ticket: keyboard, focus and axe result (FE-004)"
    if skills & API_PROOF_SKILLS:
        need["API proof"] = "API, auth or Payload ticket: request and response per AC (curl or test)"
    if skills & THREAT_SKILLS or re.search(r"^threat delta:\s*(?!none)\S", ticket_blob or "", re.I | re.M):
        need["Threat delta"] = "threat-modeled ticket: which threats changed and how they are mitigated (PE-005)"
    body = ticket_blob.split("---", 2)[2] if (ticket_blob or "").startswith("---") and ticket_blob.count("---") >= 2 else ticket_blob
    if skills & RISK_SKILLS or _RISK_TEXT.search(body or ""):
        need["Risk & rollback"] = "migration, auth or infra ticket: what can break and the forward-fix"
    return need


def latest_qa_report(project_root: Path) -> Optional[Dict]:
    reports = sorted((project_root / "docs").glob("qa-report-*.json"))
    if not reports:
        return None
    try:
        return json.loads(reports[-1].read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def not_tested_checks(project_root: Path) -> List[str]:
    report = latest_qa_report(project_root) or {}
    return [r.get("check", "") for r in report.get("results") or [] if r.get("not_tested")]


_SKILLS_READ_LINE = re.compile(r"^\s*-\s*(?P<file>\S+\.md)\s*(?:—|-|::|:)\s*(?P<rule>.*)$", re.M)


def skills_read_issues(receipt: str, card_files: List[str]) -> List[str]:
    """`## Skills read` names each CARD skill file and playbook with one applied rule (LO-0401).

    An entry naming a file not on the CARD, or with a blank rule, fails. A CARD file with no
    entry fails. Without a CARD (no skills, no playbooks) the section may say `none`.
    """
    body = section(receipt, "Skills read")
    expected = [f for f in (card_files or []) if f]
    if body is None:
        return ["missing ## Skills read — list each CARD skill file and playbook with the rule you applied"] if expected else []
    text = body.strip()
    if not expected:
        return [] if text and not section_is_stub(text) or re.fullmatch(r"-?\s*none\.?", text, re.I) else ["## Skills read: write `none` when the CARD listed no files"]
    if section_is_stub(text):
        return ["stub ## Skills read — one line per CARD file: `- <file.md> — <rule you applied>`"]
    issues: List[str] = []
    seen: List[str] = []
    expected_names = {Path(f).name: f for f in expected}
    for m in _SKILLS_READ_LINE.finditer(text):
        name = Path(m.group("file")).name
        rule = (m.group("rule") or "").strip()
        if name not in expected_names:
            issues.append(f"## Skills read names {m.group('file')}, which is not on the CARD")
            continue
        seen.append(name)
        if len(rule) < 12 or rule.lower() in ("n/a", "none", "read", "applied", "(rule)"):
            issues.append(f"## Skills read: {name} has no applied rule — write the rule from that file you followed")
    for name in expected_names:
        if name not in seen:
            issues.append(f"## Skills read is missing {name} (on the CARD) — read it and name one rule you applied")
    return issues


def trust_issues(
    receipt: str,
    ticket_blob: str,
    project_root: Path,
    *,
    receipt_dir: Optional[Path] = None,
) -> List[str]:
    """L1 + L6 findings for one receipt. Empty list = trustworthy enough to move done."""
    issues: List[str] = []
    ac_open = unchecked_ac(receipt)
    if ac_open:
        issues.append(
            f"## AC coverage: {len(ac_open)} AC still `- [ ]`; tick each and name the test or route that proves it"
        )
    need = required_sections(ticket_blob)
    for name, why in need.items():
        aliases = (name, "Risk and rollback") if name == "Risk & rollback" else (name,)
        body = section(receipt, *aliases)
        if body is None:
            issues.append(f"missing ## {name} — {why}")
        elif section_is_stub(body):
            issues.append(f"stub ## {name} — replace the template text ({why})")
    scope = section(receipt, "Scope")
    if scope is not None and not section_is_stub(scope) and not re.search(r"follow-?ups?", scope, re.I):
        issues.append("## Scope needs a `follow-ups:` line (or `follow-ups: none`)")
    if "Evidence" in need:
        issues.extend(verdict_issues("Evidence", section(receipt, "Evidence"), need_pass=True))
    if "API proof" in need:
        issues.extend(verdict_issues("API proof", section(receipt, "API proof"), need_pass=True))
    risk = section(receipt, "Risk & rollback", "Risk and rollback")
    if "Risk & rollback" in need and risk and not section_is_stub(risk):
        if not re.search(r"roll ?back|forward-?fix|revert|restore", risk, re.I):
            issues.append("## Risk & rollback must name the rollback or forward-fix")
    roots = [project_root, QUINSY_DIR, QUINSY_DIR.parent]
    if receipt_dir:
        roots.append(receipt_dir)
    web = project_root / "apps" / "web"
    if web.is_dir():
        roots.append(web)
    # Screenshots anywhere; other files only where they are cited as proof
    # (Scope may list deleted files).
    proof = "\n".join(
        section(receipt, name) or ""
        for name in ("AC coverage", "Evidence", "API proof", "Playbook citations")
    )
    images = "\n".join(m.group(0) for m in _PATH_TOKEN.finditer(receipt or "") if _IMAGE.search(m.group(1)))
    for token in missing_paths(proof + "\n" + images, roots):
        kind = "screenshot" if _IMAGE.search(token) else "proof file"
        issues.append(f"{kind} named on the receipt does not exist: {token}")
    if "Evidence" in need and "smoke_routes" in not_tested_checks(project_root):
        evidence = section(receipt, "Evidence") or ""
        if not re.search(r"smoke[^\n]*NOT TESTED|NOT TESTED[^\n]*smoke", evidence, re.I):
            issues.append(
                "The gate did not run smoke routes (no docs/smoke-routes.json or QUINSY_SKIP_SMOKE). "
                "Say `smoke routes: NOT TESTED — <why>` under ## Evidence, or add smoke config and re-gate"
            )
    return issues


def stub_sections(card: Optional[Dict], ticket_blob: str = "") -> str:
    """Extra receipt template sections for this ticket (appended by write_receipt_stub)."""
    blob = ticket_blob
    if not blob and card:
        blob = "---\nskills: [{}]\nticket_type: {}\n---\n{}".format(
            ", ".join(card.get("skills") or []),
            card.get("ticket_type") or "",
            card.get("title") or "",
        )
    need = required_sections(blob)
    blocks: List[str] = []
    if "Evidence" in need:
        blocks.append(
            "## Evidence\n"
            "- (state or flow: PASS — docs/evidence/<TICKET>/<state>.png, or a test path)\n"
            "- (a state you could not check: NOT TESTED — why)"
        )
    if "A11y" in need:
        blocks.append("## A11y\n- (keyboard path, visible focus, axe result; FE-004)")
    if "API proof" in need:
        blocks.append("## API proof\n- (AC n: PASS — `curl -i …` → 200 body shape, or test path; one line per AC)")
    if "Threat delta" in need:
        blocks.append("## Threat delta\n- (threats this ticket added or removed, and the mitigation; PE-005)")
    if "Risk & rollback" in need:
        blocks.append("## Risk & rollback\n- (what can break, how you would notice, the forward-fix or rollback)")
    blocks.append("## Security\n- (what changed for security: inputs, access rules, secrets — or `no new input, route or secret`)")
    blocks.append("## Scope\n- (files touched and why)\n- follow-ups: (noted here, not done in this ticket)")
    return "\n\n".join(blocks) + "\n"
