#!/usr/bin/env python3
"""
A studio lesson is finished when the file the next project follows has changed.

The LO ticket under .quinsy-studio/backlog/ is the local work order. It carries the
verdict (project or studio), what was assumed, what was signed, the rule for next
time, and the real target file. The committed result is the PB- bullet in that
target. There is no catalog folder.
"""

from __future__ import annotations

import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

TOOLS_DIR = Path(__file__).parent
QUINSY_STUDIO = TOOLS_DIR.parent
REPO_ROOT = QUINSY_STUDIO.parent
PROJECTS_DIR = REPO_ROOT / "projects"
BACKLOG_OPEN = QUINSY_STUDIO / "backlog" / "open"
BACKLOG_DONE = QUINSY_STUDIO / "backlog" / "done"
BACKLOG_DEFERRED = QUINSY_STUDIO / "backlog" / "deferred"
CHANGELOG = QUINSY_STUDIO / "CHANGELOG.md"

LOCAL_LOG_REL = "docs/studio-learnings-local.md"
FORBIDDEN_TARGET_PREFIX = "knowledge-base/learnings/"

# The target path sets the severity floor. The agent may raise, never lower.
HIGH_IMPACT_PREFIXES: Tuple[str, ...] = (
    "process/",
    "studio-tools/",
    "studio-templates/",
    "teams/",
)

LESSON_FIELDS = ("assumed", "signed", "verdict", "next", "target")
PB_RE = re.compile(r"\bPB-\d{8}-\d{3}\b")
LO_RE = re.compile(r"(LO-\d{4})")

IMPACT_TEMPLATE = """## Impact

- **files:** _which studio files change, and which commands or gates read them_
- **in-flight:** _would a sprint already running on any product behave differently on the next execute? yes/no and why_
- **compliance:** _does a signed packet, template, or library asset become non-compliant? yes/no_
- **pro:** _what the next product stops getting wrong_
- **contra:** _migration cost, retraining, risk of over-fitting one product_
- **severity:** {floor}
"""

IMPACT_KEYS = ("files", "in-flight", "compliance", "pro", "contra", "severity")


# --------------------------------------------------------------------------- files


def lo_path(lo_id: str) -> Optional[Path]:
    lid = (lo_id or "").strip().upper()
    for folder in (BACKLOG_OPEN, BACKLOG_DEFERRED, BACKLOG_DONE):
        if not folder.is_dir():
            continue
        for path in folder.glob(f"{lid}-*.md"):
            return path
        for path in folder.glob(f"{lid}.md"):
            return path
    return None


def parse_frontmatter(text: str) -> Dict[str, str]:
    fields: Dict[str, str] = {}
    if not text.startswith("---"):
        return fields
    parts = text.split("---", 2)
    if len(parts) < 3:
        return fields
    for line in parts[1].splitlines():
        match = re.match(r"^([\w-]+):\s*(.*)$", line.strip())
        if match:
            fields[match.group(1)] = match.group(2).strip().strip("'\"")
    return fields


def set_frontmatter(text: str, key: str, value: str) -> str:
    if not text.startswith("---"):
        return f"---\n{key}: {value}\n---\n{text}"
    head, rest = text.split("---", 2)[1], text.split("---", 2)[2]
    lines = head.splitlines()
    out: List[str] = []
    found = False
    for line in lines:
        if re.match(rf"^{re.escape(key)}:\s*", line.strip()):
            out.append(f"{key}: {value}")
            found = True
        else:
            out.append(line)
    if not found:
        out.append(f"{key}: {value}")
    body = "\n".join(l for l in out if l.strip() or l == "")
    return f"---\n{body.strip()}\n---{rest}"


def drop_frontmatter(text: str, key: str) -> str:
    if not text.startswith("---"):
        return text
    head, rest = text.split("---", 2)[1], text.split("---", 2)[2]
    kept = [l for l in head.splitlines() if not re.match(rf"^{re.escape(key)}:\s*", l.strip())]
    return f"---\n" + "\n".join(kept).strip() + f"\n---{rest}"


def section_body(text: str, heading: str) -> str:
    match = re.search(rf"^## {re.escape(heading)}\s*\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    return match.group(1).strip() if match else ""


def set_section(text: str, heading: str, body: str) -> str:
    block = f"## {heading}\n\n{body.strip()}\n"
    pattern = re.compile(rf"^## {re.escape(heading)}\s*\n.*?(?=^## |\Z)", re.M | re.S)
    if pattern.search(text):
        return pattern.sub(lambda _m: block + "\n", text, count=1).rstrip() + "\n"
    return text.rstrip() + "\n\n" + block


# --------------------------------------------------------------------------- lesson block


def lesson_block(
    *,
    assumed: str,
    signed: str,
    verdict: str,
    reason: str,
    next_rule: str,
    target: str,
) -> str:
    return (
        f"- **assumed:** {assumed.strip() or '_what the studio process, template, or default said_'}\n"
        f"- **signed:** {signed.strip() or '_what the human finally accepted_'}\n"
        f"- **verdict:** {verdict.strip() or 'project | studio'} — {reason.strip() or '_one sentence_'}\n"
        f"- **next:** {next_rule.strip() or '_the rule, written as the bullet that goes into the studio file_'}\n"
        f"- **target:** `{target.strip() or 'process/… | knowledge-base/….md | teams/…/skills/….md | studio-templates/… | studio-tools/…'}`\n"
    )


def parse_lesson(text: str) -> Dict[str, str]:
    body = section_body(text, "Lesson")
    out: Dict[str, str] = {k: "" for k in LESSON_FIELDS}
    out["reason"] = ""
    for key in LESSON_FIELDS:
        match = re.search(rf"^- \*\*{key}:\*\*\s*(.*)$", body, re.M)
        if not match:
            continue
        value = match.group(1).strip()
        if value.startswith("_") and value.endswith("_"):
            value = ""
        if key == "verdict":
            verdict, _sep, reason = value.partition("—")
            out["verdict"] = verdict.strip().lower()
            out["reason"] = reason.strip()
            if out["reason"].startswith("_"):
                out["reason"] = ""
            continue
        if key == "target":
            value = value.strip("`").strip()
            if "|" in value:
                value = ""
        out[key] = value
    return out


def lesson_missing(text: str) -> List[str]:
    """Fields the agent still has to fill before the LO is a work order."""
    data = parse_lesson(text)
    missing = [k for k in ("assumed", "signed", "next", "target") if not data.get(k)]
    if data.get("verdict") not in ("project", "studio"):
        missing.insert(2, "verdict")
    if not data.get("reason"):
        missing.append("verdict reason")
    return missing


def needs_verdict(text: str) -> bool:
    meta = parse_frontmatter(text)
    if meta.get("needs_verdict", "").lower() == "true":
        return True
    return bool(lesson_missing(text))


# --------------------------------------------------------------------------- target


def normalize_target(target: str) -> str:
    raw = (target or "").strip().strip("`")
    for prefix in (".quinsy-studio/", "./"):
        if raw.startswith(prefix):
            raw = raw[len(prefix):]
    return raw


def target_issues(target: str) -> List[str]:
    rel = normalize_target(target)
    issues: List[str] = []
    if not rel:
        return ["target is empty — name the studio file the next project follows"]
    if rel.startswith(FORBIDDEN_TARGET_PREFIX):
        issues.append(f"target `{rel}` is the old catalog — name a playbook, process file, skill, template, or tool")
    allowed = ("knowledge-base/", "process/", "teams/", "studio-templates/", "studio-tools/", "studio-library/")
    if not rel.startswith(allowed):
        issues.append(f"target `{rel}` must be under {', '.join(allowed)}")
    if not (QUINSY_STUDIO / rel).exists():
        issues.append(f"target `{rel}` does not exist under .quinsy-studio/")
    return issues


def severity_floor(target: str) -> str:
    rel = normalize_target(target)
    return "high" if rel.startswith(HIGH_IMPACT_PREFIXES) else "low"


# --------------------------------------------------------------------------- verdict


def _local_log_path(project: str) -> Optional[Path]:
    proj = PROJECTS_DIR / project
    if not proj.is_dir():
        return None
    path = proj / LOCAL_LOG_REL
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(
            "# Project-local learnings (not studio HQ)\n\n"
            "Lessons judged specific to this product, and lines that failed the portability gate.\n"
            "Studio HQ only receives rules the next product would need.\n\n",
            encoding="utf-8",
        )
    return path


def write_project_verdict(
    project: str,
    *,
    title: str,
    assumed: str,
    signed: str,
    reason: str,
    observation: str = "",
) -> Optional[Path]:
    path = _local_log_path(project)
    if path is None:
        return None
    stamp = datetime.now().isoformat(timespec="seconds")
    block = (
        f"## {stamp} — {title.strip()[:100]}\n"
        f"- **verdict:** project — {reason.strip()}\n"
        f"- **assumed:** {assumed.strip()}\n"
        f"- **signed:** {signed.strip()}\n"
    )
    if observation.strip():
        block += f"- **observation:** {observation.strip()[:600]}\n"
    block += "\n"
    path.write_text(path.read_text(encoding="utf-8") + block, encoding="utf-8")
    return path


def project_verdict_lines(project: str, *, limit: int = 8) -> List[Dict[str, str]]:
    """Recent lines the agent judged project-specific, so the human can overrule."""
    if not project:
        return []
    path = PROJECTS_DIR / project / LOCAL_LOG_REL
    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8", errors="ignore")
    out: List[Dict[str, str]] = []
    for block in re.split(r"^## ", text, flags=re.M)[1:]:
        head, _nl, rest = block.partition("\n")
        title = head.split(" — ", 1)[1].strip() if " — " in head else head.strip()
        reason_m = re.search(r"\*\*(?:verdict|Why not studio):\*\*\s*(.*)", rest)
        reason = reason_m.group(1).strip() if reason_m else ""
        reason = re.sub(r"^project\s*—\s*", "", reason)
        out.append({"title": title[:90], "reason": reason[:120]})
    return out[-limit:][::-1]


def set_lesson_verdict(
    lo_id: str,
    *,
    verdict: str,
    reason: str,
    assumed: str,
    signed: str,
    next_rule: str,
    target: str = "",
) -> Dict[str, object]:
    """Fill the verdict block. `project` closes the candidate into the product log."""
    verdict = (verdict or "").strip().lower()
    if verdict not in ("project", "studio"):
        raise ValueError("verdict must be project or studio")
    if not reason.strip():
        raise ValueError("verdict needs a one-sentence reason")
    path = lo_path(lo_id)
    if path is None:
        raise FileNotFoundError(f"{lo_id} not found under backlog/")
    text = path.read_text(encoding="utf-8")
    meta = parse_frontmatter(text)
    current = parse_lesson(text)
    assumed = assumed.strip() or current.get("assumed", "")
    signed = signed.strip() or current.get("signed", "")
    next_rule = next_rule.strip() or current.get("next", "")
    if not assumed or not signed:
        raise ValueError("assumed and signed are required for either verdict")

    if verdict == "project":
        project = (meta.get("source") or "").split("/")[0].strip().lower()
        local = write_project_verdict(
            project,
            title=meta.get("title", path.stem),
            assumed=assumed,
            signed=signed,
            reason=reason,
            observation=section_body(text, "Scope"),
        ) if project else None
        path.unlink()
        try:
            from studio_train import close_jobs_for_lo

            close_jobs_for_lo(lo_id)
        except Exception:
            pass
        return {"verdict": "project", "lo_id": lo_id, "removed": str(path), "local_log": str(local) if local else ""}

    if not next_rule:
        raise ValueError("verdict studio needs next: the rule as the bullet that goes into the target")
    target = normalize_target(target or current.get("target") or meta.get("infusion_path") or "")
    issues = target_issues(target)
    if issues:
        raise ValueError("; ".join(issues))
    from studio_portability import portability_verdict, refuse_product_nouns_in_hq_body

    refuse_product_nouns_in_hq_body(f"{assumed}\n{signed}\n{next_rule}")
    pv = portability_verdict(next_rule, f"{assumed} {signed}")
    if not pv["portable"]:
        raise ValueError(f"next rule is not portable: {pv.get('reason')}")

    text = set_section(
        text,
        "Lesson",
        lesson_block(assumed=assumed, signed=signed, verdict="studio", reason=reason, next_rule=next_rule, target=target),
    )
    text = set_frontmatter(text, "infusion_path", target)
    text = set_frontmatter(text, "verdict", "studio")
    text = set_frontmatter(text, "severity_floor", severity_floor(target))
    text = drop_frontmatter(text, "needs_verdict")
    path.write_text(text, encoding="utf-8")
    skills = [s.strip() for s in re.findall(r"[A-Z]{2}-\d{3}", meta.get("train_skills", ""))]
    if skills:
        try:
            from studio_train import enqueue_train

            for skill in skills[:2]:
                enqueue_train(skill, next_rule[:120], source="lo", observation=lo_id)
        except Exception:
            pass
    return {"verdict": "studio", "lo_id": lo_id, "path": str(path), "target": target, "severity_floor": severity_floor(target)}


# --------------------------------------------------------------------------- impact


def parse_impact(text: str) -> Dict[str, str]:
    body = section_body(text, "Impact")
    out: Dict[str, str] = {}
    for key in IMPACT_KEYS:
        match = re.search(rf"^- \*\*{re.escape(key)}:\*\*\s*(.*)$", body, re.M)
        value = match.group(1).strip() if match else ""
        if value.startswith("_") and value.endswith("_"):
            value = ""
        out[key] = value
    return out


def impact_missing(text: str) -> List[str]:
    data = parse_impact(text)
    return [k for k in IMPACT_KEYS if not data.get(k)]


def effective_severity(text: str) -> str:
    meta = parse_frontmatter(text)
    floor = meta.get("severity_floor") or severity_floor(meta.get("infusion_path", ""))
    declared = (parse_impact(text).get("severity") or "").lower()
    declared = "high" if declared.startswith("high") else ("low" if declared.startswith("low") else "")
    if floor == "high":
        return "high"
    return declared or "low"


def ensure_impact_template(lo_id: str) -> Tuple[Path, bool]:
    """Insert the Impact block once. Returns (path, inserted)."""
    path = lo_path(lo_id)
    if path is None:
        raise FileNotFoundError(f"{lo_id} not found under backlog/")
    text = path.read_text(encoding="utf-8")
    if section_body(text, "Impact"):
        return path, False
    meta = parse_frontmatter(text)
    floor = meta.get("severity_floor") or severity_floor(meta.get("infusion_path", ""))
    text = text.rstrip() + "\n\n" + IMPACT_TEMPLATE.format(floor=f"{floor} (floor; raise to high with a reason, never lower)")
    path.write_text(text, encoding="utf-8")
    return path, True


def assess(lo_id: str) -> Dict[str, object]:
    """Decide low or high. Low may infuse. High waits for --approve or --defer."""
    path = lo_path(lo_id)
    if path is None:
        raise FileNotFoundError(f"{lo_id} not found under backlog/")
    text = path.read_text(encoding="utf-8")
    if needs_verdict(text):
        return {"state": "needs_verdict", "missing": lesson_missing(text), "path": str(path)}
    if not section_body(text, "Impact"):
        return {"state": "needs_impact", "path": str(path)}
    missing = impact_missing(text)
    if missing:
        return {"state": "impact_stub", "missing": missing, "path": str(path)}
    meta = parse_frontmatter(text)
    severity = effective_severity(text)
    status = meta.get("train_status", "")
    if severity == "high" and status not in ("approved", "infused"):
        text = set_frontmatter(text, "train_status", "awaiting-approval")
        text = set_frontmatter(text, "severity", "high")
        path.write_text(text, encoding="utf-8")
        return {"state": "hitl", "severity": "high", "impact": parse_impact(text), "lesson": parse_lesson(text), "path": str(path)}
    if status not in ("infusing", "infused", "approved"):
        text = set_frontmatter(text, "train_status", "infusing")
    text = set_frontmatter(text, "severity", severity)
    path.write_text(text, encoding="utf-8")
    return {"state": "infuse", "severity": severity, "impact": parse_impact(text), "lesson": parse_lesson(text), "path": str(path)}


def approve_lesson(lo_id: str) -> Path:
    path = lo_path(lo_id)
    if path is None:
        raise FileNotFoundError(f"{lo_id} not found under backlog/")
    text = path.read_text(encoding="utf-8")
    if needs_verdict(text):
        raise ValueError(f"{lo_id} still needs its verdict block")
    if impact_missing(text):
        raise ValueError(f"{lo_id} Impact block is not filled: {', '.join(impact_missing(text))}")
    text = set_frontmatter(text, "train_status", "approved")
    text = set_frontmatter(text, "approved", datetime.now().isoformat(timespec="seconds"))
    path.write_text(text, encoding="utf-8")
    return path


def defer_lesson(lo_id: str, reason: str) -> Path:
    if not (reason or "").strip():
        raise ValueError("--defer needs --reason")
    path = lo_path(lo_id)
    if path is None:
        raise FileNotFoundError(f"{lo_id} not found under backlog/")
    text = path.read_text(encoding="utf-8")
    text = set_frontmatter(text, "status", "deferred")
    text = set_frontmatter(text, "train_status", "deferred")
    text = set_section(
        text,
        "Deferred",
        f"- **when:** {datetime.now().isoformat(timespec='seconds')}\n- **reason:** {reason.strip()}\n"
        "- The Impact block above holds the pro and contra. `./studio train <LO> --reopen` brings it back.",
    )
    BACKLOG_DEFERRED.mkdir(parents=True, exist_ok=True)
    dest = BACKLOG_DEFERRED / path.name
    dest.write_text(text, encoding="utf-8")
    if path != dest:
        path.unlink()
    return dest


def reopen_lesson(lo_id: str) -> Path:
    path = lo_path(lo_id)
    if path is None or path.parent != BACKLOG_DEFERRED:
        raise FileNotFoundError(f"{lo_id} is not in backlog/deferred/")
    text = path.read_text(encoding="utf-8")
    text = set_frontmatter(text, "status", "open")
    text = drop_frontmatter(text, "train_status")
    BACKLOG_OPEN.mkdir(parents=True, exist_ok=True)
    dest = BACKLOG_OPEN / path.name
    dest.write_text(text, encoding="utf-8")
    path.unlink()
    return dest


# --------------------------------------------------------------------------- infusion record and close


def record_infusion(lo_id: str, *, bullet_id: str, target: str) -> Optional[Path]:
    path = lo_path(lo_id)
    if path is None:
        return None
    text = path.read_text(encoding="utf-8")
    text = set_frontmatter(text, "infused_id", bullet_id)
    text = set_frontmatter(text, "infused_path", normalize_target(target))
    text = set_frontmatter(text, "train_status", "infused")
    path.write_text(text, encoding="utf-8")
    return path


def infusion_body_issues(body: str) -> List[str]:
    """A bullet that closes an LO carries the three parts, not a title alone."""
    lower = (body or "").lower()
    issues: List[str] = []
    for key in ("assumed", "signed", "next"):
        if f"{key}:" not in lower:
            issues.append(f"body lacks `{key}:`")
    return issues


def close_issues(lo_id: str) -> List[str]:
    """Everything that must be true before an LO moves to backlog/done/."""
    path = lo_path(lo_id)
    if path is None:
        return [f"{lo_id} not found under backlog/"]
    if path.parent == BACKLOG_DONE:
        return []
    text = path.read_text(encoding="utf-8")
    issues: List[str] = []
    if path.parent == BACKLOG_DEFERRED:
        issues.append(f"{lo_id} is deferred — ./studio train {lo_id} --reopen first")
    missing = lesson_missing(text)
    if missing:
        issues.append(f"verdict block incomplete: {', '.join(missing)}")
    if impact_missing(text):
        issues.append(f"Impact block incomplete: {', '.join(impact_missing(text))}")
    meta = parse_frontmatter(text)
    if effective_severity(text) == "high" and meta.get("train_status") not in ("approved", "infused"):
        issues.append("high impact — ./studio train <LO> --approve (or --defer --reason) before infusing")
    bullet = meta.get("infused_id", "")
    target = normalize_target(meta.get("infused_path") or meta.get("infusion_path") or "")
    if not bullet:
        issues.append(f"no infused PB- id — ./studio infusion-delta --lo {lo_id} --path {target or '<target>'} --op add --body \"assumed: … signed: … next: …\"")
    else:
        tpath = QUINSY_STUDIO / target if target else None
        if not tpath or not tpath.is_file():
            issues.append(f"infused target `{target}` missing")
        elif bullet not in tpath.read_text(encoding="utf-8", errors="ignore"):
            issues.append(f"{bullet} is not in `{target}`")
        if CHANGELOG.is_file() and bullet not in CHANGELOG.read_text(encoding="utf-8", errors="ignore"):
            issues.append(f"CHANGELOG.md has no line naming {bullet}")
    try:
        from studio_portability import scan_hq_for_project_nouns

        hits = scan_hq_for_project_nouns()
        if hits:
            first = hits[0]
            issues.append(f"verify-abstraction: {first['path']}:{first['line']} names {first['noun']!r}")
    except Exception:
        pass
    return issues


def move_lo_done(lo_id: str) -> Path:
    issues = close_issues(lo_id)
    if issues:
        raise ValueError("\n".join(issues))
    path = lo_path(lo_id)
    assert path is not None
    if path.parent == BACKLOG_DONE:
        return path
    text = path.read_text(encoding="utf-8")
    text = set_frontmatter(text, "status", "done")
    text = set_frontmatter(text, "closed", datetime.now().strftime("%Y-%m-%d"))
    BACKLOG_DONE.mkdir(parents=True, exist_ok=True)
    dest = BACKLOG_DONE / path.name
    dest.write_text(text, encoding="utf-8")
    path.unlink()
    try:
        from studio_train import close_jobs_for_lo

        close_jobs_for_lo(lo_id)
    except Exception:
        pass
    return dest


# --------------------------------------------------------------------------- TRAIN_DUE


def _lo_rows(folder: Path) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    if not folder.is_dir():
        return rows
    for path in sorted(folder.glob("LO-*.md")):
        text = path.read_text(encoding="utf-8", errors="ignore")
        meta = parse_frontmatter(text)
        lesson = parse_lesson(text)
        match = LO_RE.search(path.name)
        rows.append(
            {
                "id": match.group(1) if match else path.stem,
                "title": meta.get("title", path.stem),
                "next": lesson.get("next", ""),
                "target": lesson.get("target") or meta.get("infusion_path", ""),
                "needs_verdict": "yes" if needs_verdict(text) else "",
                "severity": meta.get("severity") or meta.get("severity_floor") or severity_floor(meta.get("infusion_path", "")),
                "train_status": meta.get("train_status", ""),
                "reason": lesson.get("reason", ""),
            }
        )
    return rows


def train_due(project: str = "") -> Dict[str, List[Dict[str, str]]]:
    return {
        "deferred": _lo_rows(BACKLOG_DEFERRED),
        "open": [r for r in _lo_rows(BACKLOG_OPEN) if not r["needs_verdict"]],
        "candidates": [r for r in _lo_rows(BACKLOG_OPEN) if r["needs_verdict"]],
        "project": project_verdict_lines(project) if project else [],
    }


def train_due_lines(project: str = "", *, compact: bool = False) -> List[str]:
    due = train_due(project)
    total = len(due["open"]) + len(due["candidates"])
    if not total and not due["deferred"] and not due["project"]:
        return []
    lines: List[str] = []
    if compact:
        parts = []
        if total:
            parts.append(f"TRAIN_DUE {total}")
        if due["deferred"]:
            parts.append(f"{len(due['deferred'])} deferred")
        if due["candidates"]:
            parts.append(f"{len(due['candidates'])} need a verdict")
        lines.append(" — ".join(parts) + ' — open a studio chat and say "run training".')
        return lines
    lines.append(f"TRAIN_DUE — {total} studio lesson(s) wait for a training chat. Say \"run training\" in a studio chat.")
    if due["deferred"]:
        lines.append("  Deferred (you said wait):")
        for r in due["deferred"]:
            lines.append(f"    {r['id']} [{r['severity']}] {r['next'][:90] or r['title'][:90]}")
            lines.append(f"      → {r['target']}   reopen: ./studio train {r['id']} --reopen")
    if due["open"]:
        lines.append("  Ready for training:")
        for r in due["open"]:
            tag = f" ({r['train_status']})" if r["train_status"] else ""
            lines.append(f"    {r['id']} [{r['severity']}]{tag} {r['next'][:90] or r['title'][:90]}")
            lines.append(f"      → {r['target']}")
    if due["candidates"]:
        lines.append("  Need a verdict (product agent fills assumed / signed / project-or-studio / next / target):")
        for r in due["candidates"]:
            lines.append(f"    {r['id']} {r['title'][:90]}")
            lines.append(f"      ./studio learn {r['id']} --verdict studio|project --reason \"…\" --assumed \"…\" --signed \"…\" --next \"…\" --target <file>")
    if due["project"]:
        lines.append("  Judged project-specific (overrule with ./studio train --promote <project> --topic \"<title>\"):")
        for r in due["project"]:
            lines.append(f"    · {r['title']} — {r['reason'] or 'no reason given'}")
    return lines


# --------------------------------------------------------------------------- search


SEARCH_GLOBS: Tuple[str, ...] = (
    "knowledge-base/*.md",
    "knowledge-base/skill-extensions/*.md",
    "process/*.md",
    "teams/*/skills/*.md",
)


def search_pb_bullets(query: str, *, limit: int = 20) -> List[Dict[str, str]]:
    """Find infused rules where the agent reads them: playbooks, process files, skills."""
    q = (query or "").strip().lower()
    if not q:
        return []
    hits: List[Dict[str, str]] = []
    for pattern in SEARCH_GLOBS:
        for path in sorted(QUINSY_STUDIO.glob(pattern)):
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            for line in text.splitlines():
                if PB_RE.search(line) and q in line.lower():
                    hits.append({"path": str(path.relative_to(QUINSY_STUDIO)), "line": line.strip()[:200]})
                    if len(hits) >= limit:
                        return hits
    return hits


def pb_id_exists(bullet_id: str) -> bool:
    bid = (bullet_id or "").strip()
    if not bid:
        return False
    for pattern in SEARCH_GLOBS:
        for path in QUINSY_STUDIO.glob(pattern):
            try:
                if bid in path.read_text(encoding="utf-8", errors="ignore"):
                    return True
            except OSError:
                continue
    return False
