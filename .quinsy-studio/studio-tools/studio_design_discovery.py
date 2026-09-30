#!/usr/bin/env python3
"""Gate 2a design-direction packet (LO-0341) and 2b kit checks (LO-0342).

Discovery Q&A + signed DESIGN.md. Blocks prototype until unique, human-answered
direction exists. 2b requires a project-owned CSS kit, coded A/M/O, and a sticker
sheet that renders inventory children.
"""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Sequence, Tuple

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

# Craft substrate pulled into the prototype. Look stays in the project.
BASE_KIT = (
    "button",
    "input",
    "popover",
    "tooltip",
    "dropdown-menu",
    "dialog",
    "sidebar",
    "auth-login",
)
SAAS_RAIL = "studio-rail"
BASE_KIT_LEVELS = {
    "button": "atoms",
    "input": "atoms",
    "popover": "molecules",
    "tooltip": "molecules",
    "dropdown-menu": "molecules",
    "dialog": "molecules",
    "auth-login": "molecules",
    "studio-rail": "molecules",
    "sidebar": "organisms",
}
HAND_ROLLED_CONTROLS = {
    "popover": re.compile(r"\bfunction\s+Popover\b"),
    "tooltip": re.compile(r"\bfunction\s+Tooltip\b"),
    "dropdown-menu": re.compile(r"\bfunction\s+DropdownMenu\b"),
    "dialog": re.compile(r"\bfunction\s+Dialog\b"),
}
CONTROL_PATTERNS = {
    **HAND_ROLLED_CONTROLS,
    "button": re.compile(r"\bfunction\s+Button\b"),
}
RAW_COLOR = re.compile(r"#[0-9a-fA-F]{3,8}\b|\brgb(?:a)?\s*\(|\bhsl(?:a)?\s*\(")
PALETTE_CLASS = re.compile(
    r"\b(?:bg|text|border|ring|from|to|via|fill|stroke)-"
    r"(?:slate|gray|zinc|neutral|stone|red|orange|amber|yellow|lime|green|emerald|"
    r"teal|cyan|sky|blue|indigo|violet|purple|fuchsia|pink|rose)-\d{2,3}\b"
)
ARBITRARY_SPACE = re.compile(r"\[[0-9.]+(?:px|rem)\]")
ARCH_CHECKS = (
    ("route / service / data split", r"service|repositor|handler"),
    ("server authorization", r"authori[sz]"),
    ("parameterized queries", r"parameter"),
    ("allow-listed bodies", r"allow-?list"),
    ("idempotency", r"idempoten|repeat is safe|safe to repeat"),
    ("no stack traces", r"stack trace"),
    ("rate limit or internal-only", r"rate limit|quota|internal-only"),
    ("outbound timeout", r"timeout"),
    ("structured logs and request id", r"request id"),
    ("no secrets in logs", r"secret"),
    ("health check", r"health"),
    ("temp cleanup", r"cleanup|temp"),
    ("drift written back or reverted", r"drift"),
)
CRITIQUE_RUBRIC = ("audience", "preset", "type", "color", "density", "banned")
MAX_CRITIQUE_ATTEMPTS = 3
NO_UI_ARCHETYPE = "api-service"


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


def critique_path(root: Path) -> Path:
    return root / "design" / "DIRECTION-CRITIQUE.md"


def preset_catalog() -> Path:
    return Path(__file__).resolve().parent.parent / "knowledge-base" / "aesthetic-presets"


def preset_slugs() -> List[str]:
    catalog = preset_catalog()
    if not catalog.exists():
        return []
    return sorted(p.parent.name for p in catalog.glob("*/SKILL.md"))


def project_archetype(root: Path) -> str:
    status = root / "status.json"
    if not status.exists():
        return "saas-application"
    try:
        data = json.loads(status.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return "saas-application"
    return str(data.get("archetype") or "saas-application")


def kit_names_for(archetype: str) -> List[str]:
    names = list(BASE_KIT)
    if archetype == "saas-application":
        names.append(SAAS_RAIL)
    return names


def pull_names_for(archetype: str) -> List[str]:
    if archetype == NO_UI_ARCHETYPE:
        return []
    return ["cn", *kit_names_for(archetype)]


def shell_routes_for(archetype: str) -> List[str]:
    """Screens around the PRD journey. api-service has no UI prototype."""
    if archetype == NO_UI_ARCHETYPE:
        return []
    app = [
        "/mocks/sign-in",
        "/mocks/register",
        "/mocks/app/shell",
        "/mocks/app/settings",
        "/mocks/app/empty",
        "/mocks/app/loading",
        "/mocks/app/error",
    ]
    if archetype == "internal-tool":
        return app
    return ["/mocks/marketing", "/mocks/legal/privacy", "/mocks/legal/terms", *app]


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""


def indigo_in_text(text: str) -> bool:
    low = text.lower()
    return any(m.lower() in low for m in INDIGO_MARKERS)


def human_answer_blob(root: Path) -> str:
    """Full A: lines the human filled. ANSWER_LINE alone is only the line prefix."""
    lines = []
    for line in _text(discovery_path(root)).splitlines():
        stripped = line.strip()
        if ANSWER_LINE.match(stripped) and "_unanswered_" not in stripped.lower():
            lines.append(stripped.lower())
    return "\n".join(lines)


def indigo_marker_unless_human(text: str, human_answers: str) -> str | None:
    """Default indigo fails. The same marker in a filled A: line is a signed choice."""
    low = text.lower()
    allowed = human_answers.lower()
    for marker in INDIGO_MARKERS:
        token = marker.lower()
        if token in low and token not in allowed:
            return marker
    return None


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
    marker = indigo_marker_unless_human(blob, human_answer_blob(root))
    if marker:
        issues.append(
            f"design/DESIGN.md still contains default slop token {marker} — pick product color roles, not indigo"
        )
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
    if not _named_preset(blob):
        issues.append(
            "DESIGN.md must name one aesthetic preset slug as craft substrate "
            "(type, elevation, motion, density) plus a product delta — the preset is not the identity"
        )
    issues.extend(reference_image_issues(root, blob))
    return list(dict.fromkeys(issues))


def _named_preset(blob: str) -> str:
    for slug in preset_slugs():
        if re.search(rf"`{re.escape(slug)}`|\b{re.escape(slug)}\b", blob):
            return slug
    return ""


def critique_issues(root: Path) -> List[str]:
    """UX-008 second pass. A missing file or any FAIL blocks gate 2a HITL."""
    path = critique_path(root)
    if not path.exists() or len(_text(path).strip()) < 40:
        return [
            "Missing design/DIRECTION-CRITIQUE.md — UX-008 grades DESIGN.md in a second pass "
            "before the human signs the direction"
        ]
    blob = _text(path)
    issues: List[str] = []
    for label in CRITIQUE_RUBRIC:
        match = re.search(rf"^.*\b{re.escape(label)}\b.*$", blob, re.I | re.M)
        if not match:
            issues.append(f"DIRECTION-CRITIQUE.md missing rubric line: {label}")
            continue
        line = match.group(0)
        if re.search(r"\bFAIL\b", line):
            issues.append(
                f"DIRECTION-CRITIQUE.md {label} is FAIL — revise the direction before HITL"
            )
        elif not re.search(r"\bPASS\b", line):
            issues.append(f"DIRECTION-CRITIQUE.md {label} must be marked PASS or FAIL")
    return issues


def _critique_fingerprint(root: Path) -> str:
    path = critique_path(root)
    if not path.exists():
        return "missing"
    digest = hashlib.sha256(_text(path).encode("utf-8")).hexdigest()
    return digest[:16]


def critique_log_path(root: Path) -> Path:
    return root / "design" / "critique-log.json"


def record_critique_attempt(root: Path) -> int:
    """Log a new failing critique. Repeating the same file does not burn another attempt."""
    log_path = critique_log_path(root)
    data: dict = {"attempts": []}
    if log_path.exists():
        try:
            data = json.loads(log_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            data = {"attempts": []}
    attempts = list(data.get("attempts") or [])
    fingerprint = _critique_fingerprint(root)
    issues = critique_issues(root)
    if not attempts or attempts[-1].get("fingerprint") != fingerprint:
        attempts.append(
            {
                "at": datetime.now().isoformat(timespec="seconds"),
                "fingerprint": fingerprint,
                "issues": issues,
            }
        )
        data["attempts"] = attempts
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        rev = root / "docs" / "phases" / "revisions.md"
        rev.parent.mkdir(parents=True, exist_ok=True)
        if not rev.exists():
            rev.write_text("# Pre-implementation revisions\n", encoding="utf-8")
        lines = "\n".join(f"- {item}" for item in issues) or "- (no rubric lines)"
        rev.write_text(
            rev.read_text(encoding="utf-8")
            + (
                f"\n## Gate 2a critique — {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
                f"{lines}\n"
            ),
            encoding="utf-8",
        )
    return len(attempts)


def critique_budget_exhausted(root: Path) -> bool:
    log_path = critique_log_path(root)
    if not log_path.exists() or not critique_issues(root):
        return False
    try:
        data = json.loads(log_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False
    return len(data.get("attempts") or []) > MAX_CRITIQUE_ATTEMPTS


def reference_image_issues(root: Path, design_text: str = "") -> List[str]:
    """If the human dropped reference rasters, the signed direction must lock them."""
    folder = root / "docs" / "design"
    if not folder.exists():
        return []
    images = sorted(
        p.name
        for p in folder.iterdir()
        if p.is_file() and p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}
    )
    if not images:
        return []
    blob = design_text or _text(design_md_path(root))
    issues: List[str] = []
    for name in images:
        if name not in blob:
            issues.append(
                f"design/DESIGN.md must name reference image {name} and lock that screen"
            )
    heading = re.search(r"^## Reference screens\b", blob, re.M)
    if not heading:
        issues.append(
            "design/DESIGN.md must include ## Reference screens locking layout to the reference images"
        )
        return issues
    rest = blob[heading.end() :]
    nxt = re.search(r"^## ", rest, re.M)
    body = rest[: nxt.start()] if nxt else rest
    if len(body.strip()) < 800:
        issues.append(
            "## Reference screens is too thin to lock the reference images"
        )
    return issues


def gate_2a_issues(root: Path, adopt: bool = False) -> List[str]:
    issues = discovery_issues(root) + design_direction_issues(root) + critique_issues(root)
    if adopt:
        ia = root / "docs" / "ia" / "surface-map.md"
        if not ia.exists() or len(_text(ia).strip()) < 60:
            issues.append("Adopt 2a: fill docs/ia/surface-map.md (keep vs evolve the existing UI)")
    return issues


def gate_2a_next(root: Path, adopt: bool = False) -> str:
    """Execute phase for 2a: write_questions | write_direction | write_critique | critique_budget | hitl."""
    if not discovery_path(root).exists():
        return "write_questions"
    if discovery_issues(root):
        return "hitl"
    direction_bad = bool(design_direction_issues(root))
    if adopt:
        ia = root / "docs" / "ia" / "surface-map.md"
        if not ia.exists() or len(_text(ia).strip()) < 60:
            direction_bad = True
    if direction_bad:
        return "write_direction"
    if critique_issues(root):
        if critique_budget_exhausted(root):
            return "critique_budget"
        return "write_critique"
    return "hitl"


def prototype_exists(root: Path) -> bool:
    return (root / "design" / "prototype" / "package.json").exists()


def sticker_inventory_issues(sticker_text: str, *, allowed_indigo: str = "") -> List[str]:
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
    marker = indigo_marker_unless_human(sticker_text, allowed_indigo)
    if marker:
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
        marker = indigo_marker_unless_human(blob, human_answer_blob(root))
        if marker:
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
        if not _level_satisfied(root, level):
            issues.append(f"Add at least one coded {singular} in ui/components/{level}/")
    return issues


def _level_satisfied(root: Path, level: str) -> bool:
    folder = root / "ui" / "components" / level
    files = [
        f
        for f in (folder.glob("*") if folder.exists() else [])
        if f.is_file() and f.name != "README.md" and f.suffix in {".tsx", ".ts", ".jsx", ".js"}
    ]
    if files:
        return True
    for slug, slug_level in BASE_KIT_LEVELS.items():
        if slug_level != level:
            continue
        comp = root / "ui" / "components" / slug
        if comp.is_dir() and any(comp.glob("*.tsx")):
            return True
    return False


def library_kit_issues(root: Path) -> List[str]:
    """Prototype styles the pulled kit. Hand-rolled popovers fail while the pull exists."""
    archetype = project_archetype(root)
    if archetype == NO_UI_ARCHETYPE:
        return []
    issues: List[str] = []
    names = kit_names_for(archetype)
    missing = [
        slug
        for slug in names
        if not any((root / "ui" / "components" / slug).glob("*.tsx"))
    ]
    if missing:
        issues.append(
            "Pull the studio-library base kit before drawing controls: " + ", ".join(missing)
        )
    sticker = root / "design" / "prototype" / "app" / "sticker-sheet" / "page.tsx"
    sticker_text = _text(sticker)
    for slug in names:
        if slug not in sticker_text:
            issues.append(f"Sticker sheet must render pulled `{slug}`")
    issues.extend(hand_rolled_control_issues(root))
    return issues


def hand_rolled_control_issues(root: Path) -> List[str]:
    issues: List[str] = []
    search_roots = [root / "ui" / "components", root / "design" / "prototype", root / "app"]
    for slug, pattern in HAND_ROLLED_CONTROLS.items():
        pulled = root / "ui" / "components" / slug
        if not pulled.is_dir():
            continue
        for base in search_roots:
            if not base.exists():
                continue
            for path in base.rglob("*.tsx"):
                try:
                    path.relative_to(pulled)
                    continue
                except ValueError:
                    pass
                if pattern.search(_text(path)):
                    try:
                        rel = path.relative_to(root)
                    except ValueError:
                        rel = path
                    issues.append(
                        f"Hand-rolled {slug} in {rel} while ui/components/{slug} is already pulled"
                    )
    return list(dict.fromkeys(issues))


def _iter_product_tsx(root: Path) -> List[Path]:
    found: List[Path] = []
    for base in (root / "ui" / "components", root / "app", root / "src" / "app"):
        if not base.exists():
            continue
        for path in base.rglob("*.tsx"):
            if "node_modules" in path.parts or "design" in path.parts:
                continue
            found.append(path)
    return found


def duplicate_control_issues(root: Path) -> List[str]:
    """A second Popover, Tooltip, DropdownMenu, Dialog, or Button fails the ticket."""
    issues: List[str] = []
    for slug, pattern in CONTROL_PATTERNS.items():
        owners = [path for path in _iter_product_tsx(root) if pattern.search(_text(path))]
        if len(owners) < 2:
            continue
        try:
            rel = owners[1].relative_to(root)
        except ValueError:
            rel = owners[1]
        issues.append(
            f"Second {slug} in {rel}. Reuse the component already in the project."
        )
    return issues


def known_component_names(root: Path) -> set:
    names = set()
    usage = root / "docs" / "library-usage.json"
    if usage.exists():
        try:
            data = json.loads(usage.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            data = {}
        for pull in data.get("pulls") or []:
            if isinstance(pull, dict) and pull.get("name"):
                names.add(str(pull["name"]).lower())
    comp = root / "ui" / "components"
    if comp.is_dir():
        for path in comp.rglob("*"):
            if "node_modules" in path.parts:
                continue
            if path.is_file() and path.suffix.lower() in {".tsx", ".jsx"}:
                names.add(path.stem.lower())
            elif path.is_dir() and path.parent == comp:
                names.add(path.name.lower())
    return {name for name in names if len(name) >= 3}


def reuse_citation_issues(root: Path, receipt: str) -> List[str]:
    names = known_component_names(root)
    low = (receipt or "").lower()
    if names and any(name in low for name in names):
        return []
    return [
        "UI receipt must name an existing project component or a pulled library slug"
    ]


def hardcoded_style_issues(blobs: Sequence[Tuple[str, str]]) -> List[str]:
    issues: List[str] = []
    for rel, text in blobs:
        norm = str(rel).replace("\\", "/")
        if "design-tokens" in norm:
            continue
        if not norm.endswith((".tsx", ".css", ".jsx")):
            continue
        if RAW_COLOR.search(text) or PALETTE_CLASS.search(text) or ARBITRARY_SPACE.search(text):
            issues.append(
                f"Hardcoded style in {norm}. Use a token from ui/tokens/design-tokens.css, "
                "or add the missing semantic token and reference var(--role)."
            )
    return issues


def added_style_blobs(diff: str) -> List[Tuple[str, str]]:
    blobs: List[Tuple[str, str]] = []
    current: Optional[str] = None
    added: List[str] = []
    for line in (diff or "").splitlines():
        if line.startswith("+++ b/"):
            if current:
                blobs.append((current, "\n".join(added)))
            current = line[6:]
            added = []
        elif line.startswith("+") and not line.startswith("+++") and current:
            added.append(line[1:])
    if current:
        blobs.append((current, "\n".join(added)))
    return [(rel, text) for rel, text in blobs if rel and rel != "/dev/null"]


def changed_ui_blobs(root: Path) -> List[Tuple[str, str]]:
    if not (root / "ui" / "tokens" / "design-tokens.css").exists():
        return []
    import subprocess

    try:
        proc = subprocess.run(
            ["git", "diff", "-U0", "HEAD", "--", "*.tsx", "*.css", "*.jsx"],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=8,
        )
    except (OSError, subprocess.TimeoutExpired):
        return []
    if proc.returncode != 0:
        return []
    return added_style_blobs(proc.stdout or "")


def _section_is_na(body: str) -> bool:
    lines = [ln.strip().lstrip("-").strip() for ln in (body or "").splitlines() if ln.strip()]
    if not lines:
        return True
    return all(re.fullmatch(r"n/a\.?", ln, re.I) for ln in lines)


def ticket_is_ui(blob: str) -> bool:
    return bool(
        re.search(
            r"ticket_type:\s*(?:ui-[\w-]+|marketing-page|workflow-explainer)\b|\bFE-\d{3}\b",
            blob or "",
        )
    )


def ticket_needs_architecture(blob: str) -> bool:
    return bool(re.search(r"\b(?:BE-\d{3}|PE-001)\b", blob or ""))


def architecture_receipt_issues(receipt: str) -> List[str]:
    body = _markdown_section(receipt or "", "Architecture skill")
    if _section_is_na(body):
        return [
            "## Architecture skill cannot be n/a when the ticket includes API, auth, data, "
            "security, or infrastructure"
        ]
    missing = [label for label, pattern in ARCH_CHECKS if not re.search(pattern, body, re.I)]
    if missing:
        return ["Architecture skill missing: " + ", ".join(missing)]
    return []


def implementation_receipt_issues(
    root: Path,
    receipt: str,
    ticket_blob: str,
    style_blobs: Optional[Sequence[Tuple[str, str]]] = None,
) -> List[str]:
    issues: List[str] = []
    if ticket_is_ui(ticket_blob):
        issues.extend(duplicate_control_issues(root))
        issues.extend(reuse_citation_issues(root, receipt))
        if (root / "ui" / "tokens" / "design-tokens.css").exists():
            blobs = changed_ui_blobs(root) if style_blobs is None else style_blobs
            issues.extend(hardcoded_style_issues(blobs))
        design = _markdown_section(receipt or "", "Design skill")
        if _section_is_na(design) or not re.search(r"token|var\(--", design, re.I):
            issues.append(
                "## Design skill on a UI ticket must cite the component and a project token, not n/a"
            )
    if ticket_needs_architecture(ticket_blob):
        issues.extend(architecture_receipt_issues(receipt))
    return issues


def baseline_departure_issues(root: Path, receipt_text: str) -> List[str]:
    """Move-to-done fails a silent rewrite once the prototype has been materialized."""
    if not (root / "docs" / "design" / "baseline.md").exists():
        return []
    dupes = hand_rolled_control_issues(root)
    if not dupes:
        return []
    if re.search(r"enhancement\s*:", receipt_text or "", re.I):
        return []
    return [
        "Baseline kit already exists. Add an `Enhancement:` line on the receipt, "
        "or stay on the pulled control. " + dupes[0]
    ]


def _markdown_section(blob: str, heading: str) -> str:
    match = re.search(rf"^## {re.escape(heading)}\b", blob, re.M)
    if not match:
        return ""
    rest = blob[match.end() :]
    nxt = re.search(r"^## ", rest, re.M)
    return rest[: nxt.start()] if nxt else rest


def _mock_page(root: Path, route: str) -> Path:
    rel = route.strip().strip("`").strip("/")
    return root / "design" / "prototype" / "app" / rel / "page.tsx"


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
    routes = re.findall(r"`(/mocks/[^`]+)`", _markdown_section(blob, "Required prototype routes"))
    if routes:
        app_routes = [route for route in routes if route.startswith("/mocks/app/")]
        app_text = ""
        app_root = root / "design" / "prototype" / "app" / "mocks" / "app"
        if app_root.exists():
            app_text = "\n".join(
                path.read_text(encoding="utf-8", errors="ignore") for path in app_root.rglob("*.tsx")
            )
        if len(app_routes) >= 2 and "href=" not in app_text and "<Link" not in app_text:
            issues.append("Webapp prototype views must link to each other so the shell is navigable")
        for route in routes:
            page = _mock_page(root, route)
            if not page.exists():
                issues.append(f"Prototype missing {route}")
                continue
            page_text = page.read_text(encoding="utf-8", errors="ignore")
            for heading in _headings_for_route(blob, route):
                if heading not in page_text:
                    issues.append(f"{route} must show heading: {heading}")
        for rel in re.findall(r"`([^`]+\.json)`", _markdown_section(blob, "Locale catalog")):
            catalog = root / rel
            if not catalog.exists():
                issues.append(f"Prototype missing locale catalog {rel}")
    elif not mock_pages:
        issues.append("No mock pages in design/prototype/app/mocks/ — add at least one page.tsx")
    issues.extend(_shell_route_issues(root, blob))
    return issues


def _shell_route_issues(root: Path, scope_text: str) -> List[str]:
    archetype = project_archetype(root)
    required = shell_routes_for(archetype)
    if not required:
        return []
    issues: List[str] = []
    section = _markdown_section(scope_text, "Required shell")
    if not section.strip():
        issues.append(
            "design/DESIGN-SCOPE.md must include ## Required shell "
            "(marketing, auth, settings, empty/loading/error — not only the PRD journey)"
        )
        return issues
    listed = re.findall(r"`(/mocks/[^`]+)`", section)
    for route in required:
        if route not in listed:
            issues.append(f"Required shell missing {route} for {archetype}")
        page = _mock_page(root, route)
        if not page.exists():
            issues.append(f"Prototype missing shell {route}")
    scope_kind = ""
    selected = re.search(r"selected scope:\s*`?(journey|core-views)`?", scope_text, re.I)
    if selected:
        scope_kind = selected.group(1).lower()
    if scope_kind == "journey":
        shell_text = []
        for route in required:
            page = _mock_page(root, route)
            if page.exists():
                shell_text.append(_text(page))
        joined = "\n".join(shell_text)
        if required and joined and "href=" not in joined and "<Link" not in joined:
            issues.append("Journey shell routes must link to each other so the baseline is navigable")
    return issues


def _headings_for_route(scope_text: str, route: str) -> List[str]:
    headings: List[str] = []
    current = ""
    for line in _markdown_section(scope_text, "Required visible headings").splitlines():
        stripped = line.strip()
        match = re.match(r"^###\s+`(/mocks/[^`]+)`", stripped)
        if match:
            current = match.group(1)
            continue
        item = re.match(r"^-\s+(.+)$", stripped)
        if item and current == route:
            headings.append(item.group(1).strip())
    return headings


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

    if project_archetype(root) == NO_UI_ARCHETYPE:
        return []

    issues.extend(coded_kit_issues(root))
    issues.extend(library_kit_issues(root))
    issues.extend(mock_scope_issues(root))
    sticker = root / "design" / "prototype" / "app" / "sticker-sheet" / "page.tsx"
    if not sticker.exists():
        issues.append("Missing design/prototype/app/sticker-sheet/page.tsx")
    else:
        issues.extend(
            sticker_inventory_issues(_text(sticker), allowed_indigo=human_answer_blob(root))
        )
    proto = root / "design" / "prototype" / "package.json"
    if not proto.exists():
        issues.append("Missing design/prototype/ Next.js app — run ./studio design <project> after gate 2a")
    return list(dict.fromkeys(issues))
