#!/usr/bin/env python3
"""Design-track ticket helpers — ticket_type, design approval gates."""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

DESIGN_TRACK_TYPES = frozenset({
    "ui-new-component",
    "ui-composition",
    "marketing-page",
    "workflow-explainer",
    "ia-navigation",
    "ia-feature-placement",
})

UI_IMPLEMENT_TYPES = frozenset({
    "ui-new-component",
    "ui-composition",
    "ui-styling",
    "marketing-page",
    "workflow-explainer",
})

MARKETING_TRIGGERS = (
    "homepage", "home page", "landing", "pricing page", "marketing", "hero section"
)
WORKFLOW_TRIGGERS = (
    "workflow", "explainer", "onboarding", "diagram", "storyboard", "how it works"
)
IA_TRIGGERS = ("information architecture", "navigation", "nav structure", "wayfinding", "ia ")
PLACEMENT_TRIGGERS = (
    "wrong place",
    "wrong surface",
    "move to",
    "dumping ground",
    "feature placement",
    "context of use",
    "presentation builder",
    "share dialog",
    "menu merge",
    "information architecture",
)
NEW_COMPONENT_TRIGGERS = (
    "new component", "new modal", "new dialog", "new dropdown", "settings panel"
)
STYLING_TRIGGERS = ("dark mode", "styling", "polish", "contrast", "theme tweak")
# Titles/scopes from clarify that are design-track but miss "component/modal/ui"
DESIGN_BRIEF_TRIGGERS = (
    "team 10 design",
    "design spec +",
    "design spec and",
    "in-context mock",
    "in-context mocks",
)


def infer_ticket_type(text: str) -> str:
    t = text.lower().strip()
    if t.startswith("design:") or t.startswith("design —") or t.startswith("design -"):
        return "ui-composition"
    if any(x in t for x in DESIGN_BRIEF_TRIGGERS):
        return "ui-composition"
    if any(x in t for x in MARKETING_TRIGGERS):
        return "marketing-page"
    if any(x in t for x in WORKFLOW_TRIGGERS):
        return "workflow-explainer"
    if any(x in t for x in PLACEMENT_TRIGGERS):
        return "ia-feature-placement"
    if "information architecture" in t or re.search(r"\bia\b", t):
        if any(x in t for x in ("navigation", "nav structure", "wayfinding")):
            return "ia-navigation"
    if any(x in t for x in NEW_COMPONENT_TRIGGERS):
        return "ui-new-component"
    if any(x in t for x in ("component", "modal", "dialog", "menu", "ui", "layout")):
        return "ui-composition"
    if any(x in t for x in STYLING_TRIGGERS):
        return "ui-styling"
    return "feature"


def enrich_design_skills(skills: List[str], ticket_type: str) -> List[str]:
    """Add UX skills for design-track tickets."""
    out = list(skills)
    for skill in ("UX-006", "AI-002"):
        if skill not in out:
            out.append(skill)
    if ticket_type == "marketing-page" and "UX-007" not in out:
        out.insert(0, "UX-007")
    if ticket_type == "workflow-explainer" and "UX-007" not in out:
        out.insert(0, "UX-007")
    if ticket_type in ("ui-new-component", "ui-composition", "marketing-page"):
        for skill in ("UX-002", "UX-005"):
            if skill not in out:
                out.append(skill)
    if ticket_type == "ia-navigation" and "UX-003" not in out:
        out.insert(0, "UX-003")
    if ticket_type == "ia-feature-placement":
        for skill in ("UX-003", "UX-002"):
            if skill not in out:
                out.insert(0, skill)
    seen: set[str] = set()
    unique: List[str] = []
    for skill in out:
        if skill not in seen:
            seen.add(skill)
            unique.append(skill)
    return unique[:8]


def parse_design_fields(content: str) -> Dict[str, str]:
    fields: Dict[str, str] = {}
    for key in (
        "ticket_type",
        "design_status",
        "design_spec",
        "design_approved_at",
        "team",
    ):
        m = re.search(rf"^{key}:\s*(.+)$", content, re.MULTILINE)
        if m:
            fields[key] = m.group(1).strip().strip("'\"")
    return fields


def requires_design_approval(content: str) -> bool:
    fields = parse_design_fields(content)
    ticket_type = fields.get("ticket_type", infer_ticket_type(content))
    return ticket_type in DESIGN_TRACK_TYPES


def design_implement_blocked_message(ticket_id: str, content: str) -> Optional[str]:
    if not requires_design_approval(content):
        return None
    fields = parse_design_fields(content)
    status = fields.get("design_status", "pending")
    if status == "approved" or fields.get("design_approved_at"):
        return None
    spec = fields.get("design_spec", f"docs/design-specs/{ticket_id}.md")
    return (
        f"\n  ⚠️  Design approval required before implement ({ticket_id}).\n"
        f"    Team 10 must complete design spec: {spec}\n"
        f"    Human: ./studio approve-design <project> {ticket_id}\n"
    )


def _insert_frontmatter_field(content: str, field_line: str) -> str:
    """Insert a YAML field before the closing --- of frontmatter."""
    if not content.startswith("---"):
        return f"{field_line}\n\n{content}"
    parts = content.split("---", 2)
    if len(parts) < 3:
        return content
    body = parts[1].rstrip()
    return f"---{body}\n{field_line}\n---{parts[2]}"


def set_design_approved(content: str) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    if re.search(r"^design_status:", content, re.MULTILINE):
        content = re.sub(
            r"^design_status:.*$",
            "design_status: approved",
            content,
            flags=re.MULTILINE,
        )
    else:
        content = _insert_frontmatter_field(content, "design_status: approved")
    if re.search(r"^design_approved_at:", content, re.MULTILINE):
        content = re.sub(
            r"^design_approved_at:.*$",
            f"design_approved_at: {now}",
            content,
            flags=re.MULTILINE,
        )
    else:
        if not re.search(
            r"^(design_status: approved)$",
            content,
            flags=re.MULTILINE,
        ):
            content = _insert_frontmatter_field(content, f"design_approved_at: {now}")
        else:
            content = re.sub(
                r"^(design_status: approved)$",
                rf"\1\ndesign_approved_at: {now}",
                content,
                flags=re.MULTILINE,
            )
    return content


def default_design_spec_path(ticket_id: str) -> str:
    return f"docs/design-specs/{ticket_id}.md"


def design_spec_has_placement_section(spec_text: str) -> bool:
    """True if spec includes Context & placement with substantive content."""
    patterns = (
        r"##\s*2\.\s*Context\s*&\s*placement",
        r"##\s*2\.\s*Context and placement",
        r"###\s*User intent\s*&\s*surface",
        r"\*\*Home surface\*\*",
    )
    if not any(re.search(p, spec_text, re.IGNORECASE) for p in patterns):
        return False
    # Reject placeholder-only sections
    placeholders = ("| | |", "What is the user", "__", "TBD", "…")
    section_match = re.search(
        r"(##\s*2\.\s*Context[^\n]*\n)([\s\S]*?)(?=\n##\s|\Z)",
        spec_text,
        re.IGNORECASE,
    )
    if not section_match:
        return any(re.search(p, spec_text, re.IGNORECASE) for p in patterns)
    body = section_match.group(2)
    lines = [ln.strip() for ln in body.splitlines() if ln.strip() and not ln.strip().startswith(">")]
    substantive = [ln for ln in lines if not any(p in ln for p in placeholders)]
    return len(substantive) >= 4


def design_spec_placement_warning(spec_path: Path) -> Optional[str]:
    if not spec_path.exists():
        return None
    text = spec_path.read_text(encoding="utf-8", errors="ignore")
    if design_spec_has_placement_section(text):
        return None
    return (
        "Design spec missing §2 Context & placement "
        "(see knowledge-base/contextual-ia-playbook.md). "
        "Approve only if this ticket is nav-only or single-surface styling."
    )


def design_spec_has_in_context_mocks_section(spec_text: str) -> bool:
    """True if spec includes experienceable / in-context mocks section with substance."""
    patterns = (
        r"##\s*2c\.\s*Experienceable",
        r"##\s*2c\.\s*In-context",
        r"in-context\s+mocks",
        r"Experienceable in-context mocks",
        r"\*\*Shell\s*/\s*surface\*\*",
        r"\*\*Anti-orphan check\*\*",
    )
    if not any(re.search(p, spec_text, re.IGNORECASE) for p in patterns):
        return False
    placeholders = (
        "| | |",
        "e.g. board chrome",
        "Paths under",
        "__",
        "TBD",
        "…",
        "list which",
    )
    section_match = re.search(
        r"(##\s*2c\.[^\n]*\n)([\s\S]*?)(?=\n##\s|\Z)",
        spec_text,
        re.IGNORECASE,
    )
    body = section_match.group(2) if section_match else spec_text
    lines = [ln.strip() for ln in body.splitlines() if ln.strip() and not ln.strip().startswith(">")]
    substantive = [ln for ln in lines if not any(p.lower() in ln.lower() for p in placeholders)]
    has_shell = bool(
        re.search(
            r"\*\*Shell\s*/\s*surface\*\*\s*\|\s*[^|]+",
            spec_text,
            re.IGNORECASE,
        )
    )
    has_asset = bool(
        re.search(
            r"(docs/design-specs/mocks/|\.png|\.jpg|\.webp|figma\.com|Mock assets)",
            spec_text,
            re.IGNORECASE,
        )
    )
    return has_shell and has_asset and len(substantive) >= 3


def design_spec_in_context_mocks_error(spec_path: Path) -> Optional[str]:
    """Hard gate when in-context mocks section is missing (AM-007 / MOOD-0202)."""
    if not spec_path.exists():
        return None
    text = spec_path.read_text(encoding="utf-8", errors="ignore")
    if design_spec_has_in_context_mocks_section(text):
        return None
    return (
        "Design spec missing §2c Experienceable in-context mocks "
        "(AM-007). Embed mocks in the real UI shell — orphan artboards are not enough. "
        "See knowledge-base/design-spec-template.md §2c."
    )


# Common emoji / pictograph ranges used as faux icons in mocks (LO-0037)
_EMOJI_ICON_RE = re.compile(
    "["
    "\U0001F300-\U0001FAFF"  # Misc symbols & pictographs, supplemental
    "\U00002700-\U000027BF"  # Dingbats
    "\U0001F1E0-\U0001F1FF"  # Flags
    "\U00002600-\U000026FF"  # Misc symbols
    "]+"
)


def design_mocks_emoji_icon_warning(project_root: Path, ticket_id: str) -> Optional[str]:
    """Warn if design-spec mock HTML appears to use emoji as UI icons (LO-0037)."""
    mock_dir = project_root / "docs" / "design-specs" / "mocks" / ticket_id
    if not mock_dir.is_dir():
        return None
    hits: List[str] = []
    for path in sorted(mock_dir.rglob("*.html")):
        try:
            raw = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        # Ignore long prose; flag emoji inside tags that look like controls
        for m in _EMOJI_ICON_RE.finditer(raw):
            start = max(0, m.start() - 40)
            ctx = raw[start : m.end() + 40]
            if any(
                k in ctx.lower()
                for k in ("btn", "button", "icon", "toolbar", "rail", "tool", "aria-label")
            ):
                hits.append(f"{path.relative_to(project_root)}: {m.group(0)!r}")
                break
        if len(hits) >= 5:
            break
    if not hits:
        return None
    sample = "; ".join(hits[:3])
    return (
        "Emoji-as-icon in design mocks (LO-0037) — use SVG / Icon only. "
        f"Examples: {sample}"
    )
