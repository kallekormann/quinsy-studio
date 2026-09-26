#!/usr/bin/env python3
"""Gate 2a design-direction packet (LO-0341) and 2b kit checks (LO-0342).

Discovery Q&A + signed DESIGN.md. Blocks prototype until unique, human-answered
direction exists. 2b requires a project-owned CSS kit, coded A/M/O, and a sticker
sheet that renders inventory children.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import List

INDIGO_MARKERS = (
    "#6366f1",
    "#4f46e5",
    "bg-indigo-500",
    "bg-indigo-600",
    "text-indigo-600",
)
STUB_MARKERS = (
    "describe look & feel from prd",
    "waiting for human gate 2",
    "replace with approved screen",
)
TEMPLATE_LEFTOVERS = (
    "what “done” looks like for the primary user",
    "what \"done\" looks like for the primary user",
    "_sovereign vs transient",
    "product-specific constraints from the human",
    "banned phrases from discovery",
)
CLONE_ONLY = re.compile(
    r"\b(stripe|linear|notion|apple|saas)\s*-?\s*like\b",
    re.I,
)
UNIQUENESS_HEAD = re.compile(
    r"^#{1,3}\s*(uniqueness|visual dna|what we are not|anti-pattern)",
    re.I | re.M,
)
ANSWER_LINE = re.compile(r"^a:\s+\S", re.I | re.M)
QUESTION_LINE = re.compile(r"^q:\s+\S", re.I | re.M)

BARE_GATE_2_MSG = (
    "Use --gate 2a (direction) then --gate 2b (project kit). "
    "Bare --gate 2 is refused."
)
HUMAN_GATES = ("0", "1", "2a", "2b")


def parse_cli_gate(raw: str) -> str:
    """CLI human-gate ids. Refuses legacy bare '2'."""
    s = str(raw).strip().lower()
    if s == "2":
        raise ValueError(BARE_GATE_2_MSG)
    if s in HUMAN_GATES:
        return s
    raise ValueError(f"Unknown gate {raw}. Use 0, 1, 2a, or 2b.")


def discovery_path(root: Path) -> Path:
    return root / "docs" / "design" / "discovery.md"


def design_md_path(root: Path) -> Path:
    return root / "design" / "DESIGN.md"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""


def indigo_in_text(text: str) -> bool:
    low = text.lower()
    return any(m.lower() in low for m in INDIGO_MARKERS)


def discovery_issues(root: Path) -> List[str]:
    """Fail 2a when the human interview is missing or unanswered."""
    path = discovery_path(root)
    if not path.exists():
        return [
            "Missing docs/design/discovery.md — write unanswered questions, wait for human answers, "
            "do not scaffold design/prototype"
        ]
    blob = _text(path)
    issues: List[str] = []
    if len(blob.strip()) < 120:
        issues.append("docs/design/discovery.md is too short — interview the human")
    qn = len(QUESTION_LINE.findall(blob))
    an = len(ANSWER_LINE.findall(blob))
    if qn < 4:
        issues.append("discovery.md needs at least 4 Q: lines (unanswered questions only from the PRD gaps)")
    unanswered = "_unanswered_" in blob.lower() or "todo" in blob.lower()
    filled_answers = [
        m.group(0)
        for m in ANSWER_LINE.finditer(blob)
        if "_unanswered_" not in m.group(0).lower()
    ]
    if unanswered or len(filled_answers) < 4:
        issues.append("discovery.md needs at least 4 A: lines with human answers — do not invent brand")
    if an < qn or len(filled_answers) < qn:
        issues.append("Every Q: in discovery.md must have an A: — HITL until the human answers")
    return list(dict.fromkeys(issues))


def design_direction_issues(root: Path) -> List[str]:
    """Fail 2a when DESIGN.md is a stub, indigo default, or a catalog clone with no product DNA."""
    path = design_md_path(root)
    if not path.exists():
        return ["Missing design/DESIGN.md — fill from discovery answers before approve --gate 2a"]
    blob = _text(path)
    low = blob.lower()
    issues: List[str] = []
    if len(blob.strip()) < 400:
        issues.append("design/DESIGN.md is too thin for a signed direction packet")
    for stub in STUB_MARKERS:
        if stub in low:
            issues.append("design/DESIGN.md is still the scaffold stub — write visual DNA from human answers")
            break
    leftover_hits = sum(1 for phrase in TEMPLATE_LEFTOVERS if phrase in low)
    if leftover_hits >= 2:
        issues.append("design/DESIGN.md still has template leftovers — write from discovery answers")
    for marker in INDIGO_MARKERS:
        if marker.lower() in low:
            issues.append(
                f"design/DESIGN.md still contains default slop token {marker} — pick product color roles, not indigo"
            )
            break
    if not UNIQUENESS_HEAD.search(blob):
        issues.append(
            "design/DESIGN.md must include a Uniqueness / Visual DNA / What we are not section "
            "(product-specific constraints, not a preset name)"
        )
    elif CLONE_ONLY.search(blob):
        uniq = UNIQUENESS_HEAD.search(blob)
        window = blob[uniq.start() : uniq.start() + 600] if uniq else ""
        if len(window.strip()) < 80:
            issues.append(
                "DESIGN.md names a catalog clone (Stripe/Linear-like) without uniqueness constraints"
            )
    role_hits = sum(
        1
        for word in ("typography", "type", "color role", "color roles", "posture", "voice")
        if word in low
    )
    if role_hits < 2:
        issues.append("DESIGN.md must name type/color roles, posture, or voice — not only a mood adjective")
    return list(dict.fromkeys(issues))


def gate_2a_issues(root: Path, adopt: bool = False) -> List[str]:
    issues = discovery_issues(root) + design_direction_issues(root)
    if adopt:
        ia = root / "docs" / "ia" / "surface-map.md"
        if not ia.exists() or len(_text(ia).strip()) < 60:
            issues.append("Adopt 2a: fill docs/ia/surface-map.md (keep vs evolve the existing UI)")
    return issues


def gate_2a_next(root: Path, adopt: bool = False) -> str:
    """Execute phase for 2a: write_questions | write_direction | hitl."""
    if not discovery_path(root).exists():
        return "write_questions"
    if discovery_issues(root):
        return "hitl"
    if design_direction_issues(root) or (adopt and gate_2a_issues(root, adopt=True)):
        return "write_direction"
    return "hitl"


def prototype_exists(root: Path) -> bool:
    return (root / "design" / "prototype" / "package.json").exists()


def sticker_inventory_issues(sticker_text: str) -> List[str]:
    """Title-only sticker sheet is a process fail (LO-0043 class)."""
    issues: List[str] = []
    low = sticker_text.lower()
    for label in ("atom", "molecule", "organism"):
        if label not in low:
            issues.append(f"Sticker sheet must group {label}s (atomic inventory)")
    if "data-state" not in low and "disabled" not in low:
        issues.append("Sticker sheet must show control states (data-state or disabled/hover/focus)")
    controls = (
        sticker_text.count("<button")
        + sticker_text.count("<input")
        + sticker_text.count("<select")
        + len(re.findall(r"\bButton\b", sticker_text))
    )
    if controls < 3:
        issues.append("Sticker sheet must render at least 3 real controls, not headings")
    if "replace placeholders" in low or (
        "tokens + components" in low and "data-state" not in low and controls < 3
    ):
        issues.append(
            "Sticker sheet is title-only / scaffold — render inventory children "
            "(atoms, molecules, organisms) with states, not section headlines"
        )
    if indigo_in_text(sticker_text):
        issues.append("Sticker sheet still uses default indigo — map project tokens from DESIGN.md")
    return list(dict.fromkeys(issues))


def coded_kit_issues(root: Path) -> List[str]:
    issues: List[str] = []
    css = root / "ui" / "tokens" / "design-tokens.css"
    if not css.exists():
        issues.append("Missing ui/tokens/design-tokens.css (full CSS tokens, not JSON-only)")
    else:
        blob = _text(css)
        if "--" not in blob or len(blob.strip()) < 80:
            issues.append("design-tokens.css must define CSS custom properties from the signed DESIGN.md")
        if indigo_in_text(blob):
            issues.append("design-tokens.css still contains default indigo")
    theme_hits = [
        root / "design" / "prototype" / "tailwind.config.ts",
        root / "design" / "prototype" / "tailwind.config.js",
        root / "design" / "prototype" / "app" / "globals.css",
        root / "ui" / "tokens" / "tailwind-theme.css",
    ]
    mapped = False
    for path in theme_hits:
        if not path.exists():
            continue
        blob = _text(path)
        if len(blob.strip()) > 40 and ("var(--" in blob or "design-tokens.css" in blob or "--" in blob):
            mapped = True
            break
    if not mapped:
        issues.append(
            "Map tokens into a Tailwind theme or prototype globals.css that uses var(--token) "
            "or imports ui/tokens/design-tokens.css"
        )
    for level, singular in (("atoms", "atom"), ("molecules", "molecule"), ("organisms", "organism")):
        folder = root / "ui" / "components" / level
        files = [
            f
            for f in (folder.glob("*") if folder.exists() else [])
            if f.is_file() and f.name != "README.md" and f.suffix in {".tsx", ".ts", ".jsx", ".js"}
        ]
        if not files:
            issues.append(f"Add at least one coded {singular} in ui/components/{level}/")
    return issues


def mock_scope_issues(root: Path) -> List[str]:
    issues: List[str] = []
    scope = root / "design" / "DESIGN-SCOPE.md"
    if not scope.exists() or len(_text(scope).strip()) < 40:
        issues.append("Fill design/DESIGN-SCOPE.md (journey vs core-views decision)")
        return issues
    blob = _text(scope)
    if "scope" not in blob.lower():
        issues.append("design/DESIGN-SCOPE.md must document mock scope (journey | core-views | as-built)")
    mocks_dir = root / "design" / "prototype" / "app" / "mocks"
    mock_pages = list(mocks_dir.glob("**/page.tsx")) if mocks_dir.exists() else []
    if not mock_pages:
        issues.append("No mock pages in design/prototype/app/mocks/ — add at least one page.tsx")
    return issues


def gate_2b_issues(root: Path, adopt: bool = False) -> List[str]:
    issues: List[str] = []
    if adopt:
        surfaces = root / "docs" / "as-built" / "01-surfaces.md"
        if not surfaces.exists() or len(_text(surfaces).strip()) < 80:
            issues.append("Fill docs/as-built/01-surfaces.md (existing routes/screens)")
        ia = root / "docs" / "ia" / "surface-map.md"
        if not ia.exists() or len(_text(ia).strip()) < 60:
            issues.append("Fill docs/ia/surface-map.md from existing UI (no greenfield prototype)")
        css = root / "ui" / "tokens" / "design-tokens.css"
        if not css.exists() or "--" not in _text(css):
            issues.append("Adopt 2b: map existing UI to ui/tokens/design-tokens.css (no fake prototype)")
        return issues

    issues.extend(coded_kit_issues(root))
    issues.extend(mock_scope_issues(root))
    sticker = root / "design" / "prototype" / "app" / "sticker-sheet" / "page.tsx"
    if not sticker.exists():
        issues.append("Missing design/prototype/app/sticker-sheet/page.tsx")
    else:
        issues.extend(sticker_inventory_issues(_text(sticker)))
    proto = root / "design" / "prototype" / "package.json"
    if not proto.exists():
        issues.append("Missing design/prototype/ Next.js app — run ./studio design <project> after gate 2a")
    return list(dict.fromkeys(issues))
