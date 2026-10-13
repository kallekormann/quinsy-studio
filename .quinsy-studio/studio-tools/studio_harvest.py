#!/usr/bin/env python3
"""
Immediate studio harvest — classify a learning the moment it is identified and
open a local LO-* work order when the line is **portable**, else write the
project-local log.

The LO points at the real studio file (playbook, process file, skill, template,
tool) and carries a `## Lesson` block: assumed / signed / verdict / next / target.
There is no catalog folder; the committed result is the PB- bullet in the target.
Train only when LO declares train_skills (ability gap).
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from ticket_helpers import render_ticket_markdown

try:
    from studio_portability import (
        append_project_local_learning,
        portability_verdict,
        resolve_project_from_source,
        sanitize_observation,
        train_skills_for_kind,
    )
    from studio_lesson import lesson_block, severity_floor, write_project_verdict
except ImportError:  # pragma: no cover
    from studio_tools.studio_portability import (  # type: ignore
        append_project_local_learning,
        portability_verdict,
        resolve_project_from_source,
        sanitize_observation,
        train_skills_for_kind,
    )
    from studio_tools.studio_lesson import lesson_block, severity_floor, write_project_verdict  # type: ignore

TOOLS_DIR = Path(__file__).parent
QUINSY_STUDIO = TOOLS_DIR.parent
BACKLOG_OPEN = QUINSY_STUDIO / "backlog" / "open"
BACKLOG_DONE = QUINSY_STUDIO / "backlog" / "done"
BACKLOG_BLOCKED = QUINSY_STUDIO / "backlog" / "blocked"

# kind → signal, skills, role, team, playbook (the real target file a lesson changes)
KIND_MAP: Dict[str, Dict[str, object]] = {
    "ui-component": {
        "signal": "library-gap",
        "skills": ["UX-005", "FE-002", "SO-001"],
        "role": "UI/Interaction Designer (Director)",
        "team": "10-product-design-experience",
        "playbook": "knowledge-base/atomic-design-playbook.md",
    },
    "package": {
        "signal": "library-gap",
        "skills": ["SO-001", "BE-001"],
        "role": "Studio Automation Engineer (Director)",
        "team": "09-studio-operations-evolution",
        "playbook": "studio-library/library_registry.md",
    },
    "design": {
        "signal": "design-gap",
        "skills": ["UX-005", "UX-001"],
        "role": "Product Designer (Director)",
        "team": "10-product-design-experience",
        "playbook": "knowledge-base/design_playbook.md",
    },
    "ux": {
        "signal": "design-gap",
        "skills": ["UX-002", "UX-004"],
        "role": "UX Designer (Director)",
        "team": "10-product-design-experience",
        "playbook": "knowledge-base/design-science-playbook.md",
    },
    "ia": {
        "signal": "design-gap",
        "skills": ["UX-003"],
        "role": "Information Architect (Director)",
        "team": "10-product-design-experience",
        "playbook": "knowledge-base/contextual-ia-playbook.md",
    },
    "layout": {
        "signal": "design-gap",
        "skills": ["UX-003", "FE-002"],
        "role": "UX Designer (Director)",
        "team": "10-product-design-experience",
        "playbook": "knowledge-base/design_playbook.md",
    },
    "usability": {
        "signal": "design-gap",
        "skills": ["UX-002", "FE-004"],
        "role": "UX Designer (Director)",
        "team": "10-product-design-experience",
        "playbook": "knowledge-base/design-science-playbook.md",
    },
    "craft": {
        "signal": "design-gap",
        "skills": ["UX-008", "UX-006"],
        "role": "UI/Visual Designer (Director)",
        "team": "10-product-design-experience",
        "playbook": "knowledge-base/anti-slop-design-ux.md",
    },
    "frontend": {
        "signal": "knowledge-gap",
        "skills": ["FE-001", "FE-003"],
        "role": "Frontend Architect (Director)",
        "team": "01-frontend-experience",
        "playbook": "knowledge-base/frontend_playbook.md",
    },
    "backend": {
        "signal": "knowledge-gap",
        "skills": ["BE-001", "BE-004"],
        "role": "Backend Architect (Director)",
        "team": "02-backend-systems",
        "playbook": "knowledge-base/backend_playbook.md",
    },
    "database": {
        "signal": "knowledge-gap",
        "skills": ["BE-002"],
        "role": "Database Specialist (Director)",
        "team": "02-backend-systems",
        "playbook": "knowledge-base/backend_playbook.md",
    },
    "security": {
        "signal": "knowledge-gap",
        "skills": ["PE-003", "BE-001"],
        "role": "Backend Security Specialist (Director)",
        "team": "08-platform-enterprise-engineering",
        "playbook": "knowledge-base/skill-extensions/frontend-security-auditor.md",
    },
    "process": {
        "signal": "process-gap",
        "skills": ["SO-002"],
        "role": "Process Guard (Director)",
        "team": "09-studio-operations-evolution",
        "playbook": "process/learning-loop.md",
    },
    "tooling": {
        "signal": "tooling-gap",
        "skills": ["SO-001"],
        "role": "Studio Automation Engineer (Director)",
        "team": "09-studio-operations-evolution",
        "playbook": "process/gates.md",
    },
}

KEYWORD_KINDS: List[Tuple[str, Tuple[str, ...]]] = [
    ("ui-component", ("atom", "molecule", "organism", "component", "button", "dialog", "modal", "sticker")),
    ("package", ("package", "promote", "boilerplate", "auth module", "billing")),
    ("ia", ("information architecture", "placement", "surface map", "ia ", "navigation ia")),
    ("usability", ("usability", "a11y", "accessibility", "empty state", "discover")),
    ("layout", ("layout", "chrome", "dock", "rail", "h-dvh", "overflow", "gutter")),
    ("ux", ("ux", "delight", "motion", "affordance", "mental model")),
    ("design", ("design spec", "token", "fidelity", "visual", "sticker sheet")),
    ("security", ("security", "xss", "csrf", "cors", "csp", "authz", "bola", "ssrf")),
    ("database", ("indexeddb", "dexie", "postgres", "schema", "migration", "sql")),
    ("backend", ("api", "endpoint", "server", "webhook", "queue")),
    ("frontend", ("next.js", "react", "tailwind", "bundle", "client")),
    ("tooling", ("cli", "gate", "playwright", "tooling", "studio-tools")),
]


def _slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:60] or "learning"


def _norm_title(title: str) -> str:
    return re.sub(r"\s+", " ", title.lower()).strip()[:80]


def classify_learning(text: str, *, path: str = "", signal: str = "") -> str:
    """Return infusion kind from free text + optional file path."""
    blob = f"{path} {text} {signal}".lower()
    if path.startswith("packages/") or "/packages/" in path:
        return "package"
    if path.startswith("ui/components/") or "ui/components/" in path:
        return "ui-component"
    if signal in ("gate-fail", "tooling-gap", "slow-gate"):
        if not any(k in blob for k in ("design", "ux", "layout", "component")):
            return "tooling"
    if signal == "design-gap":
        return "design"
    if signal == "library-gap":
        return "package" if "package" in blob else "ui-component"
    for kind, keys in KEYWORD_KINDS:
        if any(k in blob for k in keys):
            return kind
    if signal == "knowledge-gap":
        return "frontend"
    if signal in ("process-gap", "rework", "sloppy-code", "conflict"):
        return "process"
    return "process"


def kind_meta(kind: str) -> Dict[str, object]:
    return KIND_MAP.get(kind, KIND_MAP["process"])


def next_lo_id() -> str:
    numbers: List[int] = []
    for folder in (BACKLOG_OPEN, BACKLOG_DONE, BACKLOG_BLOCKED):
        if not folder.exists():
            continue
        for path in folder.glob("LO-*.md"):
            match = re.search(r"LO-(\d+)", path.name)
            if match:
                numbers.append(int(match.group(1)))
    return f"LO-{(max(numbers) + 1) if numbers else 0:04d}"


def _rel(path: Path) -> str:
    try:
        return str(path.relative_to(QUINSY_STUDIO))
    except ValueError:
        return str(path)


def _existing_lo_match(norm: str) -> Optional[str]:
    """Exact normalized title only — prefix match would collide on shared stems."""
    for folder in (BACKLOG_OPEN, BACKLOG_DONE):
        if not folder.exists():
            continue
        for path in folder.glob("LO-*.md"):
            text = path.read_text(encoding="utf-8", errors="ignore")
            title_m = re.search(r"^title:\s*(.+)$", text, re.M)
            title = title_m.group(1).strip() if title_m else path.stem
            if _norm_title(title) == norm:
                match = re.search(r"(LO-\d+)", path.name)
                return match.group(1) if match else path.stem
    return None


def target_for_kind(kind: str) -> str:
    """The real studio file a lesson of this kind changes (never the old catalog)."""
    meta = kind_meta(kind)
    return str(meta.get("playbook") or "knowledge-base/agentic-loop-playbook.md")


def harvest_identified_learning(
    title: str,
    *,
    source: str,
    signal: str = "",
    observation: str = "",
    path: str = "",
    kind: str = "",
    priority: str = "P1",
    assumed: str = "",
    signed: str = "",
    verdict: str = "",
    reason: str = "",
    next_rule: str = "",
    target: str = "",
) -> Dict[str, object]:
    """
    Capture immediately as a local LO work order when portable.

    Without a verdict the LO is a **candidate**: `needs_verdict: true`, and
    `./studio retro --complete` refuses until `./studio learn <LO> --verdict …`
    fills assumed / signed / project-or-studio / next / target.
    `verdict=project` writes the product's local log and opens no LO.

    Returns lo_id, kind, created. If not portable: created=False, dropped=True,
    and a project-local note may be written under projects/<p>/docs/.
    """
    title = (title or "").strip()
    if not title:
        raise ValueError("learning title required")
    observation = (observation or title).strip()
    verdict = (verdict or "").strip().lower()
    if verdict and verdict not in ("project", "studio"):
        raise ValueError("verdict must be project or studio")
    if verdict and not reason.strip():
        raise ValueError("a verdict needs a one-sentence reason")

    if verdict == "project":
        project = resolve_project_from_source(source)
        local = write_project_verdict(
            project,
            title=title,
            assumed=assumed or "(not recorded)",
            signed=signed or "(not recorded)",
            reason=reason,
            observation=observation,
        ) if project else None
        return {
            "created": False,
            "dropped": False,
            "project_verdict": True,
            "lo_id": "",
            "kind": kind or classify_learning(f"{title} {observation}", path=path, signal=signal),
            "signal": signal,
            "infusion_path": "",
            "reason": reason,
            "local_log": str(local) if local else "",
        }

    pv = portability_verdict(title, observation)
    if not pv["portable"]:
        project = resolve_project_from_source(source)
        local_path = ""
        if project:
            written = append_project_local_learning(
                project,
                observation=observation,
                title=title,
                reason=str(pv.get("reason") or "not portable"),
            )
            local_path = str(written) if written else ""
        return {
            "created": False,
            "dropped": True,
            "lo_id": "",
            "kind": kind or classify_learning(f"{title} {observation}", path=path, signal=signal),
            "signal": signal,
            "infusion_path": "",
            "reason": pv.get("reason"),
            "local_log": local_path,
        }

    title = str(pv["title"])
    kind = kind or classify_learning(f"{title} {observation}", path=path, signal=signal)
    meta = kind_meta(kind)
    signal = signal or str(meta["signal"])
    skills = list(meta["skills"])  # type: ignore[arg-type]
    train_skills = train_skills_for_kind(kind, skills)
    infusion_path = (target or "").strip() or target_for_kind(kind)
    for prefix in (".quinsy-studio/", "./"):
        if infusion_path.startswith(prefix):
            infusion_path = infusion_path[len(prefix):]
    if infusion_path.startswith("knowledge-base/learnings/"):
        infusion_path = target_for_kind(kind)
    observation = sanitize_observation(observation)
    norm = _norm_title(title)
    existing = _existing_lo_match(norm)
    if existing:
        return {
            "created": False,
            "dropped": False,
            "lo_id": existing,
            "kind": kind,
            "signal": signal,
            "infusion_path": infusion_path,
            "train_skills": train_skills,
        }

    complete = verdict == "studio" and bool(assumed.strip() and signed.strip() and next_rule.strip())
    BACKLOG_OPEN.mkdir(parents=True, exist_ok=True)
    lo_id = next_lo_id()
    ticket = {
        "id": lo_id,
        "title": title[:120],
        "type": "studio-evolution",
        "status": "open",
        "phase": 6,
        "priority": priority,
        "estimate": "S",
        "team": meta["team"],
        "skills": skills,
        "assignee_role": meta["role"],
        "soll_zustand": (
            f"`{infusion_path}` carries a PB- bullet with assumed / signed / next so the next project "
            "cannot repeat this. No product names or product ticket IDs anywhere in studio HQ, "
            "CHANGELOG included; the source stays in this local LO."
        ),
        "value": "Immediate harvest — portable principle only.",
        "signal": signal,
        "source": source,
        "infusion_kind": kind,
        "infusion_path": infusion_path,
        "train_skills": train_skills,
        "modification_files": [f".quinsy-studio/{infusion_path}", ".quinsy-studio/CHANGELOG.md"],
        "acceptance_criteria": [
            "`## Lesson` block filled: assumed, signed, verdict with reason, next, target",
            f"`./studio train {lo_id}` Impact block filled; high impact approved or deferred by the human",
            f"`./studio infusion-delta --lo {lo_id} --path {infusion_path} --op add --body \"assumed: … signed: … next: …\"` wrote the PB- bullet",
            "Bullet and CHANGELOG line pass ./studio verify-abstraction (no product names or ticket IDs)",
            f"`./studio train --done {lo_id}` moved the LO to backlog/done/",
        ],
        "scope": (
            f"Kind `{kind}`. Target `{infusion_path}`. "
            f"Train skills: {train_skills or 'none (playbook-only)'}. "
            f"Observation (provenance): {observation[:350]}"
        ),
    }
    text = render_ticket_markdown(ticket)
    if not complete:
        text = text.replace("---\n\n## Target", "needs_verdict: true\n---\n\n## Target", 1)
    else:
        text = text.replace("---\n\n## Target", f"verdict: studio\nseverity_floor: {severity_floor(infusion_path)}\n---\n\n## Target", 1)
    text = text.rstrip() + "\n\n## Lesson\n\n" + lesson_block(
        assumed=assumed,
        signed=signed,
        verdict="studio" if complete else "",
        reason=reason if complete else "",
        next_rule=next_rule,
        target=infusion_path,
    )
    lo_file = BACKLOG_OPEN / f"{lo_id}-{_slugify(title)}.md"
    lo_file.write_text(text, encoding="utf-8")
    if train_skills and complete:
        try:
            from studio_train import enqueue_train

            for skill in train_skills[:2]:
                enqueue_train(str(skill), next_rule[:120] or title, source="lo", observation=lo_id)
        except Exception:
            pass
    return {
        "created": True,
        "dropped": False,
        "lo_id": lo_id,
        "kind": kind,
        "signal": signal,
        "infusion_path": infusion_path,
        "train_skills": train_skills,
        "needs_verdict": not complete,
        "lo_path": _rel(lo_file),
    }


def harvest_retro_text(retro_text: str, source: str) -> List[Dict[str, object]]:
    """Open candidate LOs from filled retro bullets (badly / improve). Each needs a verdict."""
    results: List[Dict[str, object]] = []
    for section in (
        r"## What went badly\?\s*\n(.*?)(?=\n## |\Z)",
        r"## What can we improve\?\s*\n(.*?)(?=\n## |\Z)",
    ):
        match = re.search(section, retro_text, re.DOTALL | re.I)
        if not match:
            continue
        for raw in match.group(1).splitlines():
            line = raw.strip()
            if line.startswith("- "):
                line = line[2:].strip()
            if not line or line in ("...", "- ...") or line.endswith(": ..."):
                continue
            results.append(
                harvest_identified_learning(line[:80].rstrip("."), source=source, observation=line)
            )
    return results


GATE_ROUND_THRESHOLD = 2


def gate_revision_rounds(project_dir: Path, gate_id: str) -> List[str]:
    """Each `## Gate <id> — <date>` entry in docs/phases/revisions.md is one round the human sent back."""
    path = project_dir / "docs" / "phases" / "revisions.md"
    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8", errors="ignore")
    rounds: List[str] = []
    for match in re.finditer(rf"^## Gate {re.escape(str(gate_id))}\b[^\n]*\n(.*?)(?=^## Gate |\Z)", text, re.M | re.S):
        rounds.append(match.group(1).strip())
    return rounds


def harvest_gate_rounds(project: str, project_dir: Path, gate_id: str, *, signed_statement: str = "") -> Optional[Dict[str, object]]:
    """
    A definition signed only after ≥2 send-backs is a lesson candidate.

    Opens one LO quoting the rounds; the agent must answer: did the human push
    back because of this product, or because the studio's default was wrong?
    """
    rounds = gate_revision_rounds(project_dir, gate_id)
    if len(rounds) < GATE_ROUND_THRESHOLD:
        return None
    gate_kind = {"0": "process", "1": "backend", "2a": "design", "2b": "design"}.get(str(gate_id), "process")
    title = f"Gate {gate_id} packet must be right before the human sees it — signed after {len(rounds)} revision rounds"
    quoted = "\n".join(f"  round {i + 1}: {r.splitlines()[0][:160] if r else '(empty)'}" for i, r in enumerate(rounds))
    observation = (
        f"Gate {gate_id} needed {len(rounds)} send-backs before sign-off. "
        f"Revision feedback:\n{quoted}\n"
        f"Signed statement: {signed_statement[:300] or '(see the approved packet)'}"
    )
    return harvest_identified_learning(
        title,
        source=f"{project}/gate-{gate_id}",
        signal="process-gap",
        observation=observation,
        kind=gate_kind,
    )


def open_candidates() -> List[Path]:
    """LOs that still need the project-or-studio verdict."""
    from studio_lesson import needs_verdict

    out: List[Path] = []
    if not BACKLOG_OPEN.is_dir():
        return out
    for path in sorted(BACKLOG_OPEN.glob("LO-*.md")):
        if needs_verdict(path.read_text(encoding="utf-8", errors="ignore")):
            out.append(path)
    return out


# First-brand / client token trees stay in the project. Auto-opening HQ LOs for
# every file under packages/ui or theme-tokens floods the studio backlog.
_TOKEN_KIT_MARKERS = (
    "theme-tokens",
    "design-tokens",
    "/tokens/",
    "kit-utilities",
    "kit-root",
)
_REGISTRY_GENERIC_PACKAGES = (
    "packages/auth/",
    "packages/billing/",
    "packages/feature-gating/",
    "packages/color-extraction/",
    "packages/item-tags/",
    "packages/item-search/",
    "packages/canvas-export/",
    "packages/rate-limit/",
    "packages/slug/",
    "packages/password-gate/",
    "packages/rect-selection/",
    "packages/viewport-fit/",
)


def _normalized_reuse_path(path: str) -> str:
    return path.replace("\\", "/").lstrip("./")


def _is_token_kit_path(path: str) -> bool:
    lowered = _normalized_reuse_path(path).lower()
    return any(marker in lowered for marker in _TOKEN_KIT_MARKERS)


def _is_registry_generic_package(path: str) -> bool:
    normalized = _normalized_reuse_path(path)
    if not normalized.startswith("packages/"):
        return False
    parts = normalized.split("/")
    if len(parts) < 2 or not parts[1]:
        return False
    root = f"packages/{parts[1]}/"
    return root in _REGISTRY_GENERIC_PACKAGES


def harvest_reuse_items(items: List[Dict], source: str) -> List[Dict[str, object]]:
    """Uncovered generic registry packages → LOs. Token kits and project UI stay local."""
    results: List[Dict[str, object]] = []
    seen_packages: set[str] = set()
    for item in items:
        if item.get("covered"):
            continue
        action = item.get("action") or ""
        if action not in ("promote", "lo_ticket", "promote_or_local"):
            continue
        path = str(item.get("path") or "")
        if _is_token_kit_path(path):
            continue
        if _normalized_reuse_path(path).startswith("ui/"):
            continue
        if not _is_registry_generic_package(path):
            continue
        pkg = _normalized_reuse_path(path).split("/")[1]
        if pkg in seen_packages:
            continue
        seen_packages.add(pkg)
        ticket_id = str(item.get("ticket_id") or "")
        package_path = f"packages/{pkg}"
        harvested = harvest_identified_learning(
            f"Reuse harvest: generalize `{package_path}`",
            source=source,
            signal="library-gap",
            path=package_path,
            kind="package",
            observation=f"Sprint ticket {ticket_id} changed `{path}` without library promotion.",
        )
        harvested["path"] = package_path
        results.append(harvested)
    return results
