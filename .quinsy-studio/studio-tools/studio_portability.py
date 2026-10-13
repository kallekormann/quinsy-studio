#!/usr/bin/env python3
"""
Portability gate for studio learnings — only generalizable rules enter HQ.

Project-local incidents stay in projects/<p>/docs/studio-learnings-local.md.
Train only when a skill ability gap is declared (train_skills).
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

TOOLS_DIR = Path(__file__).parent
QUINSY_STUDIO = TOOLS_DIR.parent
REPO_ROOT = QUINSY_STUDIO.parent
PROJECTS_DIR = REPO_ROOT / "projects"

# Product nouns are never written into HQ. Folder names come from projects/; a product's
# own surface names (screens, brands, hosts) live in its repo, one per line.
LOCAL_NOUNS_FILE = "docs/portability-nouns.txt"
NON_PRODUCT_FOLDERS = frozenset({"demo", "example", "sample", "testproj", "lo-0042", "--help"})

# Vendor brands OK as *examples inside playbooks* after generalization, but LO *titles*
# should use the generic rewrite — not the brand as the subject.
TITLE_BRAND_REWRITES: Tuple[Tuple[str, str], ...] = (
    (r"\bopenverse\b", "stock-media provider"),
    (r"\bunsplash\b", "optional stock provider"),
    (r"\bpexels\b", "optional stock provider"),
)

# Kinds that imply an agent skill/tooling ability gap → enqueue train.
TRAINABLE_KINDS = frozenset(
    {
        "backend",
        "frontend",
        "design",
        "ux",
        "ia",
        "layout",
        "usability",
        "tooling",
        "security",
        "database",
        "ui-component",
        "package",
    }
)

# Paths under .quinsy-studio/ scanned by infusion portability check.
HQ_SCAN_GLOBS: Tuple[str, ...] = (
    "knowledge-base/**/*.md",
    "process/**/*.md",
    "teams/**/skills/*.md",
)

def list_project_names() -> List[str]:
    """Real product projects — used to refuse HQ body text naming them."""
    if not PROJECTS_DIR.is_dir():
        return []
    names: List[str] = []
    for path in PROJECTS_DIR.iterdir():
        if not path.is_dir() or path.name.startswith("."):
            continue
        name = path.name.lower()
        if name in NON_PRODUCT_FOLDERS:
            continue
        if (
            (path / "status.json").exists()
            or (path / "INSTRUCTION.md").exists()
            or (path / "package.json").exists()
        ):
            names.append(name)
    return sorted(set(names))


def local_product_nouns() -> List[str]:
    """Surface names each product lists in its own repo (never in HQ)."""
    nouns: List[str] = []
    for name in list_project_names():
        path = PROJECTS_DIR / name / LOCAL_NOUNS_FILE
        if not path.is_file():
            continue
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = line.strip().lower()
            if line and not line.startswith("#"):
                nouns.append(line)
    return nouns


def ticket_prefixes() -> List[str]:
    """Ticket ID prefixes of the real products (first four letters, upper case)."""
    return sorted({n[:4].upper() for n in list_project_names() if len(n) >= 4})


def product_nouns() -> List[str]:
    nouns = local_product_nouns()
    nouns.extend(list_project_names())
    # longest first for rewrite stripping
    return sorted(set(nouns), key=len, reverse=True)


def find_product_nouns(text: str, *, nouns: Optional[Sequence[str]] = None) -> List[str]:
    blob = (text or "").lower()
    hits: List[str] = []
    for noun in nouns or product_nouns():
        if noun in blob:
            hits.append(noun)
    return hits


def rewrite_title_for_portability(title: str) -> str:
    """Strip/replace product brands in a candidate LO title."""
    out = (title or "").strip()
    for pattern, repl in TITLE_BRAND_REWRITES:
        out = re.sub(pattern, repl, out, flags=re.I)
    for noun in product_nouns():
        # only strip multi-word / project folder nouns from titles
        if " " in noun or noun in list_project_names():
            out = re.sub(re.escape(noun), "", out, flags=re.I)
    out = re.sub(r"\s*[—\-|:]\s*$", "", out)
    out = re.sub(r"\s{2,}", " ", out).strip(" -—|:")
    # Prefer principle-style casing: keep as rewritten
    return out[:120]


# Hosts, vendor admin, and named product surfaces — not studio principles.
_INCIDENT_MARKERS = re.compile(
    r"(?i)("
    r"\b(screenshot|ticket\s*#|fb-\d+|n-\d{3}|sprint-\d+|[a-z]{3,5}-\d{4,})\b"
    r"|\bboard\s+[a-f0-9]{8,}(-[a-f0-9]+)+"
    r"|\bboard/[a-z0-9_-]{4,}\b"
    r"|\b(?:[a-z0-9-]+\.)+(?:com|app|io|dev|net|org)\b"
    r")"
)

# Modal / reuse verbs only. "when/before/after/chrome/inbox" appear in incidents.
_RULE_CUE = re.compile(
    r"(?i)\b("
    r"must|never|always|should|must not|do not|prefer|"
    r"adapters?|reuse|generalize|promote|needs"
    r")\b"
)


def find_incident_markers(text: str) -> List[str]:
    blob = text or ""
    found: List[str] = []
    for match in _INCIDENT_MARKERS.finditer(blob):
        token = match.group(0).strip()
        if token and token.lower() not in {m.lower() for m in found}:
            found.append(token)
    lower = blob.lower()
    for noun in local_product_nouns():
        if noun in lower and noun not in {m.lower() for m in found}:
            found.append(noun)
    return found[:8]


def looks_like_principle(title: str) -> bool:
    """Reusable studio rule — not a one-project incident sentence."""
    t = (title or "").strip()
    if len(t) < 20:
        return False
    if find_incident_markers(t):
        return False
    return bool(_RULE_CUE.search(t))


def sanitize_observation(text: str) -> str:
    """Keep HQ observations generic — hosts and product tickets become placeholders."""
    out = text or ""
    out = re.sub(
        r"(?i)\b(?:[a-z0-9-]+\.)+(?:com|app|io|dev|net|org)\b",
        "<host>",
        out,
    )
    out = re.sub(r"\b[A-Z]{2,5}-\d{3,}\b", "<ticket>", out)
    names = set(list_project_names())
    for noun in product_nouns():
        out = re.sub(re.escape(noun), "<product>" if noun in names else "<surface>", out, flags=re.I)
    return re.sub(r"\s{2,}", " ", out).strip()[:600]


def portability_verdict(
    title: str,
    observation: str = "",
) -> Dict[str, object]:
    """
    Return whether text is studio-portable after rewrite.
    keys: portable, title, hits, reason
    """
    rewritten = rewrite_title_for_portability(title)
    hits = find_product_nouns(rewritten)
    if hits:
        return {
            "portable": False,
            "title": rewritten,
            "hits": hits,
            "reason": f"title still contains product nouns after rewrite: {', '.join(hits)}",
        }
    obs_hits = find_product_nouns(observation or "")
    if obs_hits:
        return {
            "portable": False,
            "title": rewritten,
            "hits": obs_hits,
            "reason": f"observation still contains product nouns: {', '.join(obs_hits)}",
        }
    incidents = find_incident_markers(f"{rewritten}\n{observation or ''}")
    if incidents:
        return {
            "portable": False,
            "title": rewritten,
            "hits": incidents,
            "reason": f"incident-shaped (host, ticket, or product surface): {', '.join(incidents)}",
        }
    if not looks_like_principle(rewritten):
        return {
            "portable": False,
            "title": rewritten,
            "hits": [],
            "reason": "cannot state a reusable principle without project-specific framing",
        }
    return {
        "portable": True,
        "title": rewritten,
        "hits": [],
        "reason": "",
    }


def train_skills_for_kind(kind: str, skills: Sequence[str]) -> List[str]:
    """Skills to train when this kind is an ability gap; empty = playbook-only."""
    if kind not in TRAINABLE_KINDS:
        return []
    out = [s for s in skills if s and s.upper() != "SO-002"]
    return out[:4]


def resolve_project_from_source(source: str) -> Optional[str]:
    raw = (source or "").strip().split("/")[0].strip().lower()
    if not raw:
        return None
    names = set(list_project_names())
    if raw in names:
        return raw
    return None


def append_project_local_learning(
    project: str,
    *,
    observation: str,
    title: str,
    reason: str,
) -> Optional[Path]:
    """Keep dropped (non-portable) notes in the project world."""
    proj_dir = PROJECTS_DIR / project
    if not proj_dir.is_dir():
        return None
    docs = proj_dir / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    path = docs / "studio-learnings-local.md"
    from datetime import datetime

    if not path.exists():
        path.write_text(
            "# Project-local learnings (not studio HQ)\n\n"
            "Incidents that failed the **portability gate** stay here.\n"
            "Studio HQ only receives generalized principles.\n\n",
            encoding="utf-8",
        )
    stamp = datetime.now().isoformat(timespec="seconds")
    block = (
        f"## {stamp}\n"
        f"- **Raw title:** {title}\n"
        f"- **Why not studio:** {reason}\n"
        f"- **Observation:** {observation[:800]}\n\n"
    )
    path.write_text(path.read_text(encoding="utf-8") + block, encoding="utf-8")
    return path


# A product folder name that is also an ordinary word, inside a fixed phrase that is not the product.
ORDINARY_PHRASES: Tuple[str, ...] = ("behavioral nudge engine",)


def find_product_nouns_in_hq_text(
    text: str,
    *,
    nouns: Optional[Sequence[str]] = None,
    prefixes: Optional[Sequence[str]] = None,
) -> List[Tuple[int, str, str]]:
    """Return (line_no, noun, line) for every product folder name or product ticket ID.

    HQ has no provenance exception: the name lives in the local LO, never in committed text.
    """
    project_names = nouns if nouns is not None else list_project_names()
    if prefixes is None:
        prefixes = [n[:4].upper() for n in project_names if len(n) >= 4]
    ticket_re = (
        re.compile(rf"\b(?:{'|'.join(re.escape(p) for p in prefixes)})-\d{{3,}}\b") if prefixes else None
    )
    hits: List[Tuple[int, str, str]] = []
    for i, line in enumerate((text or "").splitlines(), start=1):
        lower = line.lower()
        for phrase in ORDINARY_PHRASES:
            lower = lower.replace(phrase, "")
        found = ""
        for name in project_names:
            if re.search(rf"(?<![a-z0-9]){re.escape(name)}(?![a-z0-9])", lower):
                found = name
                break
        if not found and ticket_re:
            match = ticket_re.search(line)
            if match:
                found = match.group(0)
        if found:
            hits.append((i, found, line.strip()[:120]))
    return hits


def refuse_product_nouns_in_hq_body(text: str, *, nouns: Optional[Sequence[str]] = None) -> None:
    """Raise if a product name or product ticket ID appears in text bound for HQ."""
    hits = find_product_nouns_in_hq_text(text, nouns=nouns)
    if hits:
        _line, noun, snippet = hits[0]
        raise ValueError(
            f"HQ write aborted: product reference {noun!r} ({snippet!r}). "
            "Write <project> instead; keep incidents in projects/<p>/docs/studio-learnings-local.md."
        )


def scan_hq_for_project_nouns(
    *,
    roots: Optional[Sequence[str]] = None,
) -> List[Dict[str, object]]:
    """Scan studio HQ markdown for product folder names and product ticket IDs."""
    findings: List[Dict[str, object]] = []
    names = list_project_names()
    if not names:
        return findings
    globs = roots or HQ_SCAN_GLOBS
    for pattern in globs:
        for path in QUINSY_STUDIO.glob(pattern):
            if not path.is_file():
                continue
            try:
                rel_check = str(path.relative_to(QUINSY_STUDIO)).replace("\\", "/")
            except ValueError:
                rel_check = str(path)
            if "/learnings/archive/" in rel_check or rel_check.startswith("learnings/archive/"):
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            for line_no, noun, snippet in find_product_nouns_in_hq_text(text, nouns=names):
                try:
                    rel = str(path.relative_to(QUINSY_STUDIO))
                except ValueError:
                    rel = str(path)
                findings.append(
                    {
                        "path": rel,
                        "line": line_no,
                        "noun": noun,
                        "snippet": snippet,
                    }
                )
    return findings


def open_lo_title_portability_failures(open_items: Sequence[Dict[str, str]]) -> List[Dict[str, str]]:
    """Open LOs whose titles fail the portability gate."""
    bad: List[Dict[str, str]] = []
    for item in open_items:
        title = item.get("title") or ""
        verdict = portability_verdict(title)
        if not verdict["portable"]:
            bad.append(
                {
                    "id": item.get("id") or "",
                    "title": title,
                    "reason": str(verdict.get("reason") or "not portable"),
                }
            )
    return bad
