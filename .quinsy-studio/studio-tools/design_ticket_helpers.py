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
    "homepage", "home page", "landing", "pricing page", "pricing table",
    "marketing", "hero section",
)
COMMERCIAL_TRIGGERS = (
    "landing",
    "pricing page",
    "pricing table",
    "checkout",
    "shopping cart",
    " pdp",
    "pdp ",
    "product detail",
    "product listing",
    " plp",
    "plp ",
    "catalog",
    "add to cart",
    "add-to-cart",
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
    if any(x in t for x in ("checkout", "product detail", "product listing", "pdp", "plp")):
        # In-app money surfaces: compose on the system, still commercial (GD skills).
        return "ui-composition"
    if any(x in t for x in WORKFLOW_TRIGGERS):
        return "workflow-explainer"
    if any(x in t for x in PLACEMENT_TRIGGERS):
        return "ia-feature-placement"
    if "information architecture" in t or re.search(r"\bia\b", t):
        if any(x in t for x in ("navigation", "nav structure", "wayfinding")):
            return "ia-navigation"
    if any(x in t for x in NEW_COMPONENT_TRIGGERS):
        return "ui-new-component"
    if any(
        x in t
        for x in (
            "fixture",
            "identity",
            "hardcoded profile",
            "demo profile",
            "kit identity",
        )
    ):
        return "feature"
    if any(x in t for x in ("component", "modal", "dialog", "menu", "ui", "layout")):
        return "ui-composition"
    if any(x in t for x in STYLING_TRIGGERS):
        return "ui-styling"
    return "feature"


def is_commercial_surface(text: str) -> bool:
    t = (text or "").lower()
    return any(x in t for x in COMMERCIAL_TRIGGERS) or any(
        x in t for x in MARKETING_TRIGGERS
    )


def enrich_design_skills(skills: List[str], ticket_type: str, text: str = "") -> List[str]:
    """Add UX skills for design-track tickets. Append GD-* on commercial surfaces."""
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
    if ticket_type == "marketing-page" or is_commercial_surface(text):
        for skill in ("GD-001", "GD-002"):
            if skill not in out:
                out.append(skill)
    seen: set[str] = set()
    unique: List[str] = []
    for skill in out:
        if skill not in seen:
            seen.add(skill)
            unique.append(skill)
    unique = unique[:8]
    if ticket_type == "marketing-page" or is_commercial_surface(text):
        for skill in ("GD-001", "GD-002"):
            if skill not in unique:
                if len(unique) >= 8:
                    unique.pop()
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


UI_TITLE_HINTS = (
    "chrome",
    "sidebar",
    "inbox",
    "header",
    "nav user",
    "operator chip",
    "kit identity",
    "demo identity",
)


def ticket_looks_like_ui(ticket_type: str, title: str = "") -> bool:
    """True when the ticket is design-track or ships a user-visible UI surface."""
    tt = (ticket_type or "").strip() or infer_ticket_type(title or "")
    if tt in DESIGN_TRACK_TYPES or tt in UI_IMPLEMENT_TYPES:
        return True
    blob = f"{title}".lower()
    return any(hint in blob for hint in UI_TITLE_HINTS)


def tickets_are_backend_only(tickets: List[Dict]) -> bool:
    """True when every ticket is explicitly non-UI. Unknown (no type, no title) is not backend-only."""
    if not tickets:
        return False
    for ticket in tickets:
        tt = str(ticket.get("ticket_type") or "").strip()
        title = str(ticket.get("title") or "").strip()
        if not tt and not title:
            return False
        if ticket_looks_like_ui(tt, title):
            return False
    return True


def design_implement_blocked_message(ticket_id: str, content: str) -> Optional[str]:
    """HITL approve-design only for design-track (major UX / UI / IA) tickets.

    Feature / styling / bug tickets stay on the approved design system — no block.
    Callers that have a project root should prefer `design_deliverables_status`
    so a missing spec is a write-step, not a fake approval.
    """
    if not requires_design_approval(content):
        return None
    fields = parse_design_fields(content)
    status = fields.get("design_status", "pending")
    if status in ("approved", "n/a") or fields.get("design_approved_at"):
        return None
    spec = fields.get("design_spec", f"docs/design-specs/{ticket_id}.md")
    return (
        f"\n  ⚠️  Design HITL required before implement ({ticket_id}) — major UX/UI/IA.\n"
        f"    Team 10 spec: {spec} (§2 + §2c + all-state in-context mocks)\n"
        f"    Human: ./studio approve-design <project> {ticket_id}\n"
        f"    Do not invent missing components in a feature ticket — open a design-track ticket instead.\n"
        f"    Do not ask the human to approve until the spec file and mocks exist on disk.\n"
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


def design_spec_has_growth_intent(spec_text: str) -> bool:
    if not re.search(r"growth intent", spec_text, re.I):
        return False
    return bool(
        re.search(r"\b(claim|hypothesis|metric|job)\b", spec_text, re.I)
    )


def design_spec_growth_intent_error(
    spec_text: str,
    ticket_type: str = "",
    ticket_blob: str = "",
) -> Optional[str]:
    tt = (ticket_type or "").strip()
    if tt != "marketing-page" and not is_commercial_surface(ticket_blob):
        return None
    if design_spec_has_growth_intent(spec_text):
        return None
    return (
        "Commercial surface missing Growth intent "
        "(job, falsifiable claim, metric or stand-in, one change). "
        "See knowledge-base/growth-mechanics-playbook.md. "
        "Do not approve-design until Team 11 has filled it."
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
    """Hard gate when the spec file or §2c in-context mocks section is missing."""
    if not spec_path.exists():
        return (
            f"Design spec does not exist: {spec_path}. "
            "Team 10 must write it from knowledge-base/design-spec-template.md "
            "before anyone runs approve-design. Referring to a missing spec is a process fail."
        )
    text = spec_path.read_text(encoding="utf-8", errors="ignore")
    if design_spec_has_in_context_mocks_section(text):
        return None
    return (
        "Design spec missing §2c Experienceable in-context mocks "
        "(AM-007). Embed mocks in the real UI shell — orphan artboards are not enough. "
        "See knowledge-base/design-spec-template.md §2c."
    )


_INTERACTIVE_STATE_GROUPS: Tuple[Tuple[str, str], ...] = (
    ("rest/up", r"\b(rest|default|up|idle)\b"),
    ("hover", r"\bhover\b"),
    ("pressed/down/active", r"\b(pressed|down|active|:active)\b"),
    ("disabled/inactive", r"\b(disabled|inactive)\b"),
    ("focus", r"\b(focus|focused|focus-visible)\b"),
)
_DISCLOSURE_WIDGET_RE = re.compile(
    r"\b(dropdown|select|combobox|menu|disclosure|popover|listbox)\b",
    re.I,
)
_INTERACTIVE_WIDGET_RE = re.compile(
    r"\b(button|dropdown|select|combobox|switch|checkbox|toggle|input|tabs?)\b",
    re.I,
)
_SURFACE_STATE_GROUPS: Tuple[Tuple[str, str], ...] = (
    ("empty", r"\bempty\b"),
    ("loading", r"\b(loading|skeleton|pending)\b"),
    ("error", r"\b(error|fail|failed|invalid)\b"),
)
_TOKEN_HINT_RE = re.compile(
    r"var\(--|"
    r"design-tokens|"
    r"ui/tokens|"
    r"--color-primary|"
    r"--primary|"
    r"bg-primary|"
    r"text-foreground|"
    r"text-muted-foreground|"
    r"--background",
    re.I,
)
_PLACEHOLDER_SPEC_RE = re.compile(
    r"What is the user trying to do\?|e\.g\. board chrome|Paths under `docs/design-specs",
    re.I,
)


def _mock_dir(project_root: Path, ticket_id: str) -> Path:
    return project_root / "docs" / "design-specs" / "mocks" / ticket_id


def _mock_html_files(project_root: Path, ticket_id: str) -> List[Path]:
    d = _mock_dir(project_root, ticket_id)
    if not d.is_dir():
        return []
    return sorted(p for p in d.rglob("*") if p.suffix.lower() in {".html", ".css"})


def _corpus_for_states(spec_text: str, project_root: Path, ticket_id: str) -> str:
    parts = [spec_text]
    for path in _mock_html_files(project_root, ticket_id):
        parts.append(path.name)
        try:
            parts.append(path.read_text(encoding="utf-8", errors="ignore"))
        except OSError:
            continue
    return "\n".join(parts)


def _missing_groups(blob: str, groups: Tuple[Tuple[str, str], ...]) -> List[str]:
    missing: List[str] = []
    for label, pattern in groups:
        if not re.search(pattern, blob, re.I):
            missing.append(label)
    return missing


def design_spec_is_unfilled_template(spec_text: str) -> bool:
    """True when the file is still the stock template / stub."""
    if "**Status:** stub" in spec_text:
        return True
    if spec_text.lstrip().startswith("# Design spec template") and _PLACEHOLDER_SPEC_RE.search(
        spec_text
    ):
        return True
    return False


def design_mocks_token_error(project_root: Path, ticket_id: str) -> Optional[str]:
    """HTML/CSS mocks must use project CSS tokens — not one-off hex-only artboards."""
    files = _mock_html_files(project_root, ticket_id)
    if not files:
        return (
            f"No HTML/CSS mocks at docs/design-specs/mocks/{ticket_id}/. "
            "PNG-only or a missing folder is incomplete. Write in-context HTML that "
            "imports or uses project `ui/tokens` (CSS variables). "
            "Screenshots may accompany HTML; they do not replace it."
        )
    token_ok = False
    for path in files:
        try:
            raw = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if _TOKEN_HINT_RE.search(raw):
            token_ok = True
            break
    if token_ok:
        return None
    return (
        f"Mocks under docs/design-specs/mocks/{ticket_id}/ do not use project CSS tokens "
        "(no `var(--…)`, `design-tokens`, or semantic token classes). "
        "Link `ui/tokens/design-tokens.css` (or the project token import) and style with "
        "those variables. Hardcoded hex-only mocks fail approve-design."
    )


def design_mocks_states_error(
    spec_text: str,
    project_root: Path,
    ticket_id: str,
    ticket_type: str = "",
) -> Optional[str]:
    """Every interactive control must be mocked in all states — one frame is incomplete."""
    blob = _corpus_for_states(spec_text, project_root, ticket_id)
    tt = (ticket_type or "").strip()
    missing: List[str] = []
    need_interactive = tt == "ui-new-component" or bool(_INTERACTIVE_WIDGET_RE.search(spec_text))
    if need_interactive:
        missing.extend(_missing_groups(blob, _INTERACTIVE_STATE_GROUPS))
    if _DISCLOSURE_WIDGET_RE.search(spec_text) or _DISCLOSURE_WIDGET_RE.search(blob):
        for label, pat in (("open", r"\bopen\b"), ("closed", r"\b(closed|collapsed)\b")):
            if not re.search(pat, blob, re.I):
                missing.append(label)
    if tt in (
        "ui-composition",
        "marketing-page",
        "workflow-explainer",
        "ia-feature-placement",
        "ia-navigation",
    ):
        missing.extend(_missing_groups(blob, _SURFACE_STATE_GROUPS))
    if not missing:
        return None
    return (
        "Incomplete mock states — approval would force implement to guess. Missing: "
        + ", ".join(missing)
        + ". For controls mock rest/up, hover, pressed/down, disabled/inactive, and focus; "
        "dropdowns/menus also need open and closed. For surfaces include empty, loading, and error. "
        "Put states in §2c and in `docs/design-specs/mocks/"
        + ticket_id
        + "/` (filenames, headings, or `data-state`)."
    )


def design_spec_completeness_error(
    spec_path: Path,
    project_root: Path,
    ticket_id: str,
    ticket_type: str = "",
    ticket_blob: str = "",
) -> Optional[str]:
    """All hard gates before a human may approve-design (or the agent may ask them to)."""
    missing_file = design_spec_in_context_mocks_error(spec_path)
    if spec_path.exists():
        text = spec_path.read_text(encoding="utf-8", errors="ignore")
        if design_spec_is_unfilled_template(text):
            return (
                f"Design spec at {spec_path} is still an unfilled template/stub. "
                "Fill §1–§7, §2, and §2c. Do not point the human at approve-design yet."
            )
        placement = design_spec_placement_warning(spec_path)
        if placement:
            return placement.replace("Approve only if", "Fill §2 before approve-design. Do not approve if")
        if missing_file:
            return missing_file
        token_err = design_mocks_token_error(project_root, ticket_id)
        if token_err:
            return token_err
        state_err = design_mocks_states_error(text, project_root, ticket_id, ticket_type)
        if state_err:
            return state_err
        growth_err = design_spec_growth_intent_error(text, ticket_type, ticket_blob)
        if growth_err:
            return growth_err
        return None
    return missing_file


def design_deliverables_status(
    project_root: Path,
    ticket_id: str,
    content: str,
) -> Tuple[str, Optional[str]]:
    """Return ('ok'|'write'|'approve', message).

    write  — agent must author spec + mocks; do not HITL approve-design
    approve — files complete; human approve-design
    ok — not design-track or already approved
    """
    if not requires_design_approval(content):
        return "ok", None
    fields = parse_design_fields(content)
    if fields.get("design_status") in ("approved", "n/a") or fields.get("design_approved_at"):
        return "ok", None
    spec_rel = fields.get("design_spec") or default_design_spec_path(ticket_id)
    spec_path = project_root / spec_rel
    tt = fields.get("ticket_type") or infer_ticket_type(content)
    err = design_spec_completeness_error(
        spec_path, project_root, ticket_id, tt, ticket_blob=content
    )
    if err:
        return "write", (
            f"\n  ✏️  Design-track deliverables missing for {ticket_id}.\n"
            f"    Write `{spec_rel}` from knowledge-base/design-spec-template.md\n"
            f"    and `docs/design-specs/mocks/{ticket_id}/` HTML using **project ui/tokens**,\n"
            f"    in the **real product view** (not an orphan artboard),\n"
            f"    with **all states** (rest/hover/pressed/disabled/focus; open/closed for menus).\n"
            f"    Do **not** run ./studio approve-design and do not ask the human to review\n"
            f"    until those files exist. Incomplete mocks = hallucinated implement.\n"
            f"    Gate: {err}\n"
        )
    return "approve", None


def write_design_spec_stub(project_root: Path, ticket_id: str, spec_rel: Optional[str] = None) -> Path:
    """Create the spec path from the Team 10 template so the file exists. Still must be filled."""
    rel = spec_rel or default_design_spec_path(ticket_id)
    dest = project_root / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        return dest
    template = Path(__file__).resolve().parent.parent / "knowledge-base" / "design-spec-template.md"
    body = ""
    if template.exists():
        body = template.read_text(encoding="utf-8", errors="ignore")
    dest.write_text(
        f"# Design spec — {ticket_id}\n\n"
        f"**Status:** stub — Team 10 must fill every section before `./studio approve-design`.\n"
        f"An empty or template-only file **fails** the gate. Mocks: `docs/design-specs/mocks/{ticket_id}/`.\n\n"
        f"{body}",
        encoding="utf-8",
    )
    return dest


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
