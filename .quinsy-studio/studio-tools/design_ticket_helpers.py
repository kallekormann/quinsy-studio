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
    "product catalog",
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


_I18N_AC_NOISE = (
    "no ui string is hardcoded",
    "see `docs/i18n.md`",
    "docs/i18n.md",
    "visible copy uses catalogs",
)


def _strip_catalog_ac(text: str) -> str:
    """i18n catalog AC mentions 'UI' and must not infer a design-track type (LO-0361)."""
    t = text.lower()
    for noise in _I18N_AC_NOISE:
        t = t.replace(noise, " ")
    return t


def infer_ticket_type(text: str) -> str:
    t = _strip_catalog_ac(text).strip()
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


_FIVE_SECOND = re.compile(r"^#{2,3}\s*Five-second test\b", re.I | re.M)
_WALKTHROUGH = re.compile(r"^##\s*Appendix\s*[—–-]\s*Persona walkthrough\b", re.I | re.M)


def design_spec_walkthrough_error(
    spec_text: str,
    ticket_type: str = "",
    ticket_blob: str = "",
) -> Optional[str]:
    """GD-003: five-second test on every packet; persona walkthrough appendix on commercial ones."""
    match = _FIVE_SECOND.search(spec_text or "")
    if not match:
        return (
            "Design spec needs a `### Five-second test` table (What is this? / Is it for me? / "
            "What do I do next?) at 390 and 1440 (GD-003)."
        )
    table = spec_text[match.end(): match.end() + 1200]
    if not ("390" in table and "1440" in table):
        return "Five-second test needs both widths, 390 and 1440 (GD-003)."
    commercial = (ticket_type or "").strip() == "marketing-page" or is_commercial_surface(ticket_blob)
    if commercial and not _WALKTHROUGH.search(spec_text):
        return (
            "Commercial packet needs `## Appendix — Persona walkthrough (GD-003)`: personas from the PRD "
            "and research only, fold-by-fold friction, hypotheses for §6."
        )
    return None


def design_spec_needs_story(ticket_type: str, ticket_blob: str = "") -> bool:
    tt = (ticket_type or "").strip()
    if tt in ("marketing-page", "workflow-explainer"):
        return True
    return tt == "ui-composition" and is_commercial_surface(ticket_blob or "")


def design_spec_story_error(
    spec_text: str,
    ticket_type: str = "",
    ticket_blob: str = "",
) -> Optional[str]:
    """Marketing and workflow specs must carry an arc, one CTA, and a reduced-motion path."""
    if not design_spec_needs_story(ticket_type, ticket_blob):
        return None
    match = re.search(r"^##\s+5\.\s+Story\b.*$", spec_text or "", re.M | re.I)
    if not match:
        return (
            "Marketing or workflow spec needs a ## 5. Story section "
            "(setup, tension, resolution, one CTA, reduced-motion path)."
        )
    rest = spec_text[match.end() :]
    nxt = re.search(r"^## ", rest, re.M)
    section = rest[: nxt.start()] if nxt else rest
    if "_fill_" in section:
        return (
            "Story section is still the template. Replace each _fill_ with the arc, "
            "the CTA, and the reduced-motion path."
        )
    missing = []
    for label, pattern in (
        ("setup", r"\bsetup\b"),
        ("tension", r"\btension\b"),
        ("resolution", r"\bresolution\b"),
        ("CTA", r"\bCTA\b|call to action"),
        ("reduced-motion", r"reduced[ -]motion"),
    ):
        if not re.search(pattern, section, re.I):
            missing.append(label)
    if missing:
        return "Story section missing: " + ", ".join(missing)
    return None


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


MOCK_ROUTE_GROUP = "(design-mocks)"
MOCK_ROUTE_SEGMENT = "design-mocks"
_MOCK_SOURCE_SUFFIXES = {".tsx", ".jsx", ".ts", ".js"}
_SCREENSHOT_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}

_REAL_IMPORT_RE = re.compile(r"""from\s+['"]((?:@|~)/[^'"]+|(?:\.\./){2,}[^'"]+)['"]""")
_SHELL_HINT_RE = re.compile(
    r"(Shell|Layout|AppFrame|Frame|Sidebar|Nav|Header|Topbar|View|Screen)\b|/\((?:app|marketing)\)/|/layouts?/",
)
_HAND_ROLLED_RES: Tuple[Tuple[str, "re.Pattern[str]"], ...] = (
    ("<style> block", re.compile(r"<style\b", re.I)),
    ("inline style={{…}}", re.compile(r"style=\{\{")),
    ("dangerouslySetInnerHTML", re.compile(r"dangerouslySetInnerHTML")),
    ("hex colour", re.compile(r"(?<![\w&])#[0-9a-fA-F]{3,8}\b")),
    ("arbitrary colour class", re.compile(r"-\[(?:#|rgb|hsl|oklch)", re.I)),
    ("raw <html>/<body>", re.compile(r"<(?:html|body)\b", re.I)),
)

DESIGN_MOCKS_LAYOUT = """import { notFound } from 'next/navigation'
import type { ReactNode } from 'react'

// Design mocks render the real app for approve-design. They never ship.
export default function DesignMocksLayout({ children }: { children: ReactNode }) {
  if (process.env.NODE_ENV === 'production') notFound()
  return children
}
"""


def product_app_root(project_root: Path) -> Optional[Path]:
    """The app the mocks must render in: apps/web, a brownfield root app, then the gate-2b kit."""
    for candidate in (
        project_root / "apps" / "web",
        project_root,
        project_root / "design" / "prototype",
    ):
        if (candidate / "package.json").exists() and _app_router_dir(candidate) is not None:
            return candidate
    return None


def _app_router_dir(app_root: Path) -> Optional[Path]:
    for candidate in (app_root / "src" / "app", app_root / "app"):
        if candidate.is_dir():
            return candidate
    return None


def real_ui_mock_dir(project_root: Path, ticket_id: str) -> Optional[Path]:
    app_root = product_app_root(project_root)
    if app_root is None:
        return None
    router = _app_router_dir(app_root)
    if router is None:
        return None
    return router / MOCK_ROUTE_GROUP / MOCK_ROUTE_SEGMENT / ticket_id


def _real_ui_mock_sources(project_root: Path, ticket_id: str) -> List[Path]:
    d = real_ui_mock_dir(project_root, ticket_id)
    if d is None or not d.is_dir():
        return []
    return sorted(p for p in d.rglob("*") if p.suffix.lower() in _MOCK_SOURCE_SUFFIXES)


def _mock_screenshots(project_root: Path, ticket_id: str) -> List[Path]:
    d = _mock_dir(project_root, ticket_id)
    if not d.is_dir():
        return []
    return sorted(p for p in d.rglob("*") if p.suffix.lower() in _SCREENSHOT_SUFFIXES)


def ensure_design_mocks_layout(project_root: Path) -> Optional[Path]:
    """Write the production guard for the mock route group. Leave an existing file alone."""
    app_root = product_app_root(project_root)
    router = _app_router_dir(app_root) if app_root else None
    if router is None:
        return None
    dest = router / MOCK_ROUTE_GROUP / "layout.tsx"
    if not dest.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(DESIGN_MOCKS_LAYOUT, encoding="utf-8")
    return dest


def design_mocks_real_ui_error(project_root: Path, ticket_id: str) -> Optional[str]:
    """Mocks are routes in the product app that render its real views and components."""
    route = f"{MOCK_ROUTE_GROUP}/{MOCK_ROUTE_SEGMENT}/{ticket_id}/"
    app_root = product_app_root(project_root)
    if app_root is None:
        return (
            "No product app to mock in (apps/web, a Next app at the project root, or the gate-2b "
            "kit in design/prototype). Mocks render the real app; there is nothing to render yet."
        )
    sources = _real_ui_mock_sources(project_root, ticket_id)
    pages = [p for p in sources if p.stem == "page"]
    rel_app = app_root.relative_to(project_root) if app_root != project_root else Path(".")
    if not pages:
        legacy = " Standalone HTML mocks are no longer accepted." if _mock_html_files(project_root, ticket_id) else ""
        return (
            f"No real-UI mock pages at {rel_app}/…/app/{route}.{legacy} "
            "Build each mock as a route in the product app that renders the real view "
            "(layout, shell, existing components) with the design solution woven in. "
            "The human only signs mocks that look exactly like the implemented app."
        )
    layout = _app_router_dir(app_root) / MOCK_ROUTE_GROUP / "layout.tsx"
    layout_text = layout.read_text(encoding="utf-8", errors="ignore") if layout.exists() else ""
    if "notFound" not in layout_text or "production" not in layout_text:
        return (
            f"Missing production guard {MOCK_ROUTE_GROUP}/layout.tsx (notFound() when NODE_ENV is "
            "production). Run the design stub again or copy DESIGN_MOCKS_LAYOUT."
        )
    real_imports: List[str] = []
    hand_rolled: List[str] = []
    for path in sources:
        text = path.read_text(encoding="utf-8", errors="ignore")
        real_imports.extend(_REAL_IMPORT_RE.findall(text))
        for label, pattern in _HAND_ROLLED_RES:
            if pattern.search(text):
                hand_rolled.append(f"{path.name}: {label}")
    if not real_imports:
        return (
            f"Mock pages under {route} import nothing from the app. Import the real view and "
            "components (`@/components/…`, the `(app)` or `(marketing)` layout, pulled library parts)."
        )
    if not any(_SHELL_HINT_RE.search(imp) for imp in real_imports):
        return (
            f"Mock pages under {route} render no app shell or view. Import the real layout, "
            "shell, or view the feature ships in, so the mock shows the surrounding product."
        )
    if hand_rolled:
        return (
            "Mocks redraw UI instead of using the app's components: "
            + "; ".join(sorted(set(hand_rolled))[:6])
            + ". Style lives in the real components and project tokens. "
            "If a part is missing, build it as a real component in the app (library-first) and import it."
        )
    shots = _mock_screenshots(project_root, ticket_id)
    if not shots:
        return (
            f"No screenshots in docs/design-specs/mocks/{ticket_id}/. Capture every state from the "
            "running mock route, e.g. `npx playwright screenshot --viewport-size=1440,900 "
            f"http://localhost:3000/{MOCK_ROUTE_SEGMENT}/{ticket_id}/<state> "
            f"docs/design-specs/mocks/{ticket_id}/<state>-1440.png` (and 390,844 for mobile)."
        )
    newest_source = max(p.stat().st_mtime for p in sources)
    newest_shot = max(p.stat().st_mtime for p in shots)
    if newest_shot + 1 < newest_source:
        return (
            f"Screenshots in docs/design-specs/mocks/{ticket_id}/ are older than the mock code. "
            "Capture them again from the running route so the human reviews what the code renders."
        )
    return None


_USE_CLIENT_RE = re.compile(r"""^\s*['"]use client['"]""", re.M)
_HANDLER_RE = re.compile(
    r"\buse(?:State|Reducer|Transition|Optimistic)\b"
    r"|\bon(?:Click|Change|KeyDown|KeyUp|PointerDown|PointerUp|MouseEnter|MouseLeave|Focus|Blur|Submit|OpenChange|ValueChange|CheckedChange|Select)\s*=",
)
_SCENARIO_RE = re.compile(
    r"\buseSearchParams\b|\bsearchParams\b|[?&]state=|data-state|MockScenarioPanel|mock-scenario-panel",
)
_MOTION_EVIDENCE_RE = re.compile(
    r"\btransition(?:-|\b)|\bduration-\d|\banimate-|\bmotion-|framer-motion|@/lib/motion"
    r"|data-\[state[=~]|\bease-(?:in|out|linear)",
)


def design_mocks_interactive_error(
    spec_text: str,
    project_root: Path,
    ticket_id: str,
) -> Optional[str]:
    """A mock is a prototype the human can use — not a folder of static frames.

    Requires at least one client page with real interaction wiring, scenario
    states reachable in the running route, and wired transitions when §2d
    Motion is not `motion: off`.
    """
    sources = _real_ui_mock_sources(project_root, ticket_id)
    if not sources:
        return None  # design_mocks_real_ui_error already covers the missing-route case
    route = f"{MOCK_ROUTE_GROUP}/{MOCK_ROUTE_SEGMENT}/{ticket_id}/"
    texts = {p: p.read_text(encoding="utf-8", errors="ignore") for p in sources}
    blob = "\n".join(texts.values())
    has_client = any(_USE_CLIENT_RE.search(t) for t in texts.values())
    has_handlers = bool(_HANDLER_RE.search(blob))
    if not (has_client and has_handlers):
        return (
            f"Mock pages under {route} are static frames — no 'use client' component with "
            "wired interactions (useState / event handlers) found. A mock is a prototype the "
            "human can use: wire hover, open/close, selection, and flow steps so the design "
            "can be felt, not guessed from screenshots."
        )
    if not _SCENARIO_RE.search(blob):
        return (
            f"Mock pages under {route} expose no way to reach scenario states in the running "
            "route (no `?state=` / useSearchParams / data-state / MockScenarioPanel). "
            "Pull `mock-scenario-panel` from the studio library (or wire in-mock controls) so "
            "empty/loading/error and open/closed are one click away — per-state static sibling "
            "pages are not a prototype."
        )
    motion_on = not _MOTION_OFF_RE.search(spec_text or "")
    if motion_on and not _MOTION_EVIDENCE_RE.search(blob):
        return (
            f"§2d Motion names transitions but the mock code under {route} wires none "
            "(no transition/duration/animate classes, motion import, or data-[state] animation). "
            "The mock must move the way the spec says the product will — or the spec must say "
            "`motion: off` (HITL opt-out)."
        )
    return None


def mock_states_from_shots(project_root: Path, ticket_id: str) -> List[str]:
    """Scenario state names, recovered from the screenshot record (hover-1440.png → hover)."""
    states: List[str] = []
    for shot in _mock_screenshots(project_root, ticket_id):
        name = re.sub(r"-(1440|390)$", "", shot.stem)
        if name and name not in states:
            states.append(name)
    return states


def mock_review_block(project_root: Path, ticket_id: str, spec_text: str) -> str:
    """The review script for the human: running route + states + §2e walkthrough."""
    base = f"http://localhost:3000/{MOCK_ROUTE_SEGMENT}/{ticket_id}/"
    lines = [
        "  Review the RUNNING prototype — the screenshots are only the record.",
        f"    Start the app:  ./studio env <project> dev   (or npm run dev in the product app)",
        f"    Mock route:     {base}",
    ]
    states = mock_states_from_shots(project_root, ticket_id)
    if states:
        lines.append("    States:         " + "  ".join(f"{base}?state={s}" for s in states[:8]))
    match = _INTERACTION_WALKTHROUGH_RE.search(spec_text or "")
    if match:
        lines.append("    Walkthrough (§2e) — follow each step on the route:")
        for raw in match.group(1).strip().splitlines():
            raw = raw.strip()
            if raw and not raw.startswith(("|--", "| #", "|---")):
                lines.append(f"      {raw}")
    return "\n".join(lines)


def _corpus_for_states(spec_text: str, project_root: Path, ticket_id: str) -> str:
    parts = [spec_text]
    for path in _real_ui_mock_sources(project_root, ticket_id) + _mock_html_files(project_root, ticket_id):
        parts.append(path.as_posix())
        try:
            parts.append(path.read_text(encoding="utf-8", errors="ignore"))
        except OSError:
            continue
    parts.extend(p.name for p in _mock_screenshots(project_root, ticket_id))
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


_MOTION_OFF_RE = re.compile(
    r"\bmotion\s*:\s*off\b|\btransitions\s*:\s*off\b",
    re.I,
)
_MOTION_HEADING_RE = re.compile(
    r"(?:##\s*2d\.[^\n]*\bmotion\b|##\s+Motion\b)[^\n]*\n([\s\S]*?)(?=\n##\s|\Z)",
    re.I,
)


def design_spec_motion_error(spec_text: str, ticket_blob: str = "") -> Optional[str]:
    """UI specs name motion. HITL opt-out is the line `motion: off`."""
    blob = f"{spec_text}\n{ticket_blob or ''}"
    if _MOTION_OFF_RE.search(blob):
        return None
    match = _MOTION_HEADING_RE.search(spec_text)
    if not match:
        return (
            "Design spec missing §2d Motion. Name the transitions (open/close, hover, reveal) "
            "and a reduced-motion path. The only opt-out is the line `motion: off` from HITL. "
            "See knowledge-base/skill-extensions/motion-transitions.md."
        )
    body = match.group(1)
    if not re.search(r"reduced[ -]motion", body, re.I):
        return "§2d Motion must name a reduced-motion path (same content, durations at 0ms)."
    if not re.search(r"\b(transition|duration|animation|ease|motion-duration)\b", body, re.I):
        return "§2d Motion must name at least one transition, duration, or easing."
    return None


_INTERACTION_WALKTHROUGH_RE = re.compile(
    r"^##\s*2e\.?\s*Interaction walkthrough.*?$(.*?)(?=^##\s|\Z)", re.M | re.S | re.I
)
_WALKTHROUGH_STEP_RE = re.compile(r"^\s*(?:\|\s*\d+\s*\||\d+\.\s)", re.M)


def design_spec_interaction_walkthrough_error(spec_text: str) -> Optional[str]:
    """§2e: the review script the human follows on the running mock route."""
    match = _INTERACTION_WALKTHROUGH_RE.search(spec_text or "")
    if not match:
        return (
            "Design spec missing §2e Interaction walkthrough — the review script for the running "
            "mock route. Write ordered steps `do X → expect Y` (3 minimum), naming the §2d "
            "transition where one fires, plus the mock route URL. The human reviews the prototype "
            "by following it; the implementation sprint ports the behavior from the mock code."
        )
    body = match.group(1)
    steps = [
        s for s in _WALKTHROUGH_STEP_RE.findall(body)
        if "---" not in s
    ]
    if len(steps) < 3:
        return (
            "§2e Interaction walkthrough needs at least 3 steps (happy path, one failure path, "
            "each scenario state). Each row is `do X → expect Y`."
        )
    if not re.search(r"\bexpect", body, re.I):
        return (
            "§2e Interaction walkthrough steps must state expectations — each step says what the "
            "human should see happen (`Expect …`), including the motion where §2d names one."
        )
    return None


_CATALOG_HEADING_RE = re.compile(r"^##\s*7b?\.?\s*Catalog applied.*?$(.*?)(?=^##\s|\Z)", re.M | re.S | re.I)
_CATALOG_ID_RE = re.compile(r"\b(PB-\d{8}-\d+|LO-\d{4})\b", re.I)


def design_spec_catalog_error(spec_text: str) -> Optional[str]:
    """Team 10 proves it read the design catalog: §7b names the PB/LO ids it applied (LO-0408).

    `catalog: none` is allowed only when the section says why nothing in the catalog matched.
    """
    match = _CATALOG_HEADING_RE.search(spec_text)
    if not match:
        return (
            "Design spec missing `## 7b. Catalog applied`. List the PB-/LO- ids from "
            "knowledge-base/design_playbook.md and knowledge-base/learnings/design/ you applied, "
            "one line each with where in this spec they land."
        )
    body = match.group(1)
    if _CATALOG_ID_RE.search(body):
        return None
    if re.search(r"catalog:\s*none", body, re.I) and len(re.sub(r"\s+", " ", body).strip()) > 40:
        return None
    return "§7b Catalog applied names no PB-/LO- id. Cite the catalog lines you applied, or write `catalog: none` with the reason."


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
        real_ui_err = design_mocks_real_ui_error(project_root, ticket_id)
        if real_ui_err:
            return real_ui_err
        interactive_err = design_mocks_interactive_error(text, project_root, ticket_id)
        if interactive_err:
            return interactive_err
        state_err = design_mocks_states_error(text, project_root, ticket_id, ticket_type)
        if state_err:
            return state_err
        growth_err = design_spec_growth_intent_error(text, ticket_type, ticket_blob)
        if growth_err:
            return growth_err
        walk_err = design_spec_walkthrough_error(text, ticket_type, ticket_blob)
        if walk_err:
            return walk_err
        story_err = design_spec_story_error(text, ticket_type, ticket_blob)
        if story_err:
            return story_err
        motion_err = design_spec_motion_error(text, ticket_blob)
        if motion_err:
            return motion_err
        interaction_err = design_spec_interaction_walkthrough_error(text)
        if interaction_err:
            return interaction_err
        catalog_err = design_spec_catalog_error(text)
        if catalog_err:
            return catalog_err
        from studio_ia_audit import ia_nav_error_for_ticket

        ia_err = ia_nav_error_for_ticket(text, ticket_type)
        if ia_err:
            return ia_err
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
            f"    and the mock routes `app/{MOCK_ROUTE_GROUP}/{MOCK_ROUTE_SEGMENT}/{ticket_id}/` in the\n"
            f"    **product app**: the real views and components with the solution woven in.\n"
            f"    No hand-drawn HTML. The mock is an **interactive prototype**: pull\n"
            f"    `mock-scenario-panel`, wire handlers, scenario states and §2d transitions,\n"
            f"    write §2e Interaction walkthrough. Then capture every state as screenshots in\n"
            f"    `docs/design-specs/mocks/{ticket_id}/` (rest/hover/pressed/disabled/focus;\n"
            f"    open/closed for menus; empty/loading/error for surfaces) — the record,\n"
            f"    not the deliverable.\n"
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
    ensure_design_mocks_layout(project_root)
    if dest.exists():
        return dest
    template = Path(__file__).resolve().parent.parent / "knowledge-base" / "design-spec-template.md"
    body = ""
    if template.exists():
        body = template.read_text(encoding="utf-8", errors="ignore")
    dest.write_text(
        f"# Design spec — {ticket_id}\n\n"
        f"**Status:** stub — Team 10 must fill every section before `./studio approve-design`.\n"
        f"An empty or template-only file **fails** the gate. Mocks: routes in the product app at "
        f"`app/{MOCK_ROUTE_GROUP}/{MOCK_ROUTE_SEGMENT}/{ticket_id}/`; screenshots in "
        f"`docs/design-specs/mocks/{ticket_id}/`.\n\n"
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
    paths = _mock_html_files(project_root, ticket_id) + _real_ui_mock_sources(project_root, ticket_id)
    if not paths:
        return None
    hits: List[str] = []
    for path in paths:
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
