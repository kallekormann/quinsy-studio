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

# Product / surface nouns that make a *title* project-local unless rewritten away.
# Project folder names are loaded dynamically from projects/.
STATIC_PRODUCT_NOUNS: Tuple[str, ...] = (
    "mood direction",
    "mood-direction",
    "suggested tab",
    "kit imagery",
    "caziro",
    "roven",
    "northwind",
    "sprint-119",
    "sprint-120",
)

# Brands OK as *examples inside playbooks* after generalization, but LO *titles*
# should use the generic rewrite — not the brand as the subject.
TITLE_BRAND_REWRITES: Tuple[Tuple[str, str], ...] = (
    (r"\bopenverse\b", "stock-media provider"),
    (r"\bunsplash\b", "optional stock provider"),
    (r"\bpexels\b", "optional stock provider"),
    (r"\bmoody\b", "the product"),
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

# Allow project names only in provenance-style lines.
_SOURCE_LINE = re.compile(
    r"(?i)^\s*(- )?(\*\*)?(source|provenance|from_feedback|project)(\*\*)?\s*[:`]",
)


def list_project_names() -> List[str]:
    """Real product projects — used to refuse HQ body text naming them."""
    placeholders = {"nudge", "demo", "example", "testproj", "sample"}
    if not PROJECTS_DIR.is_dir():
        return []
    names: List[str] = []
    for path in PROJECTS_DIR.iterdir():
        if not path.is_dir() or path.name.startswith("."):
            continue
        name = path.name.lower()
        if name in placeholders or name in ("--help", "lo-0042"):
            continue
        if (
            (path / "status.json").exists()
            or (path / "INSTRUCTION.md").exists()
            or (path / "package.json").exists()
        ):
            names.append(name)
    return sorted(set(names))


def product_nouns() -> List[str]:
    nouns = list(STATIC_PRODUCT_NOUNS)
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


def looks_like_principle(title: str) -> bool:
    """Cheap check: reusable rule, not a one-board incident."""
    t = (title or "").strip()
    if len(t) < 20:
        return False
    lower = t.lower()
    # Incident-shaped: screenshot / ticket ids / named feedback
    if re.search(r"\b(screenshot|ticket\s*#|fb-\d+|mood-\d+|lo-\d+)\b", lower):
        return False
    if re.search(r"\bboard\s+[a-f0-9]{8,}(-[a-f0-9]+)+\b", lower):
        return False
    if re.search(r"\bboard/[a-z0-9_-]{4,}\b", lower):
        return False
    # Prefer verb / modal / structural learning cues
    if re.search(
        r"\b(must|never|always|should|when|before|after|adapters?|budget|"
        r"degraded|map|prefer|reuse|generalize|promote|overflow|gate|smoke|"
        r"cache|licence|license|pixel|provider|playbook|skill|needs|chrome)\b",
        lower,
    ):
        return True
    return len(t.split()) >= 5
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
    if not looks_like_principle(rewritten):
        # observation may still be project-local; require principle-shaped title
        return {
            "portable": False,
            "title": rewritten,
            "hits": [],
            "reason": "cannot state a reusable principle without project-specific framing",
        }
    # Observation may keep provenance detail; title must be clean.
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


def line_is_provenance(line: str) -> bool:
    lower = line.lower()
    if _SOURCE_LINE.match(line):
        return True
    if "`source:" in lower or "--source" in lower:
        return True
    # Playbook "Signal (LO-NNNN / <project>):" provenance headers
    if re.search(r"\bsignal\s*\(lo-\d+", lower):
        return True
    if re.search(r"\bsource:\s*[a-z0-9_-]+", lower):
        return True
    # Process docs using example project placeholders in command samples
    if "./studio " in lower and re.search(r"\b(nudge|demo|example)\b", lower):
        return True
    return False


def find_product_nouns_in_hq_text(text: str, *, nouns: Optional[Sequence[str]] = None) -> List[Tuple[int, str, str]]:
    """Return (line_no, noun, line) for non-provenance hits of *project folder* names only."""
    # Infusion refuse: project folder names in HQ body (not static surface phrases —
    # playbooks may say "Suggested copy" generically). Strict on project ids.
    project_names = nouns if nouns is not None else list_project_names()
    hits: List[Tuple[int, str, str]] = []
    for i, line in enumerate((text or "").splitlines(), start=1):
        if line_is_provenance(line):
            continue
        lower = line.lower()
        for name in project_names:
            # word-ish boundary
            if re.search(rf"(?<![a-z0-9-]){re.escape(name)}(?![a-z0-9-])", lower):
                hits.append((i, name, line.strip()[:120]))
                break
    return hits


def scan_hq_for_project_nouns(
    *,
    roots: Optional[Sequence[str]] = None,
) -> List[Dict[str, object]]:
    """Scan studio HQ markdown for bare project folder names outside provenance lines."""
    findings: List[Dict[str, object]] = []
    names = list_project_names()
    if not names:
        return findings
    globs = roots or HQ_SCAN_GLOBS
    for pattern in globs:
        for path in QUINSY_STUDIO.glob(pattern):
            if not path.is_file():
                continue
            # CHANGELOG often cites projects — skip or soften
            if path.name == "CHANGELOG.md":
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
