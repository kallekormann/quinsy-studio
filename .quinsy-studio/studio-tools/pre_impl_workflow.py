#!/usr/bin/env python3
"""
Pre-implementation workflow: intake → blueprint → design → tickets.

Human gates 0 (intake), 1 (architecture), 2a (direction), 2b (project kit).
Tickets are generated only after gate 2b approval. Legacy human_gates.2 still
counts as design-complete. Bare --gate 2 is refused.
"""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

from ui_kit_peers import merge_kit_peers, write_ui_kit_setup

STUDIO_ROOT = Path(__file__).parent.parent.parent

STUDIO_ROOT = Path(__file__).parent.parent.parent
PROJECTS_DIR = STUDIO_ROOT / "projects"
TEMPLATES_DIR = Path(__file__).parent.parent / "studio-templates"

PLACEHOLDER_PATTERNS = [
    r"\[To be defined",
    r"\[ER diagram",
    r"\[OpenAPI",
    r"_TODO_",
    r"\.\.\.",
    r"^\s*-\s*\.\.\.\s*$",
]

PHASE_INTAKE = "1"
PHASE_BLUEPRINT = "2"
PHASE_DESIGN = "3"
PHASE_SPRINT = "4"
PHASE_IMPLEMENT = "5"


def project_dir(project: str) -> Path:
    return PROJECTS_DIR / project


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _has_placeholders(content: str) -> bool:
    for pattern in PLACEHOLDER_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE | re.MULTILINE):
            return True
    return False


def _min_content(path: Path, min_chars: int = 80) -> bool:
    if not path.exists():
        return False
    text = _read_text(path).strip()
    if len(text) < min_chars:
        return False
    return not _has_placeholders(text)


def validate_gate_0(project: str) -> Tuple[bool, List[str]]:
    """Intake + definitions ready for human review."""
    from studio_adopt import as_built_missing, is_adopt_project

    root = project_dir(project)
    issues: List[str] = []
    adopt = is_adopt_project(project)

    prd = root / "docs" / "intake" / "prd.md"
    validation = root / "docs" / "intake" / "validation.json"

    if adopt:
        issues.extend(as_built_missing(project))

    if not prd.exists():
        issues.append(
            "Missing docs/intake/prd.md"
            + (" — synthesize from as-built + intent" if adopt else "")
        )
    elif not _min_content(prd, 200):
        issues.append("docs/intake/prd.md is empty or has placeholders")

    if validation.exists():
        try:
            data = json.loads(validation.read_text())
            if not data.get("is_valid") and not adopt:
                issues.append("PRD validation failed — fix validation.json problems or document assumptions")
        except json.JSONDecodeError:
            issues.append("docs/intake/validation.json is invalid JSON")
    elif not adopt:
        issues.append("Missing docs/intake/validation.json — run ./studio intake")

    defs_dir = root / "docs" / "definitions"
    required_defs = [
        "00-index.md",
        "02-personas.md",
        "03-user-journeys.md",
        "10-kpis.md",
        "11-assumptions.md",
    ]
    for name in required_defs:
        path = defs_dir / name
        if not _min_content(path, 40):
            issues.append(f"Fill docs/definitions/{name} (no _TODO_ / placeholders)")

    return len(issues) == 0, issues


def validate_gate_1(project: str) -> Tuple[bool, List[str]]:
    """Architecture blueprint ready for human review."""
    root = project_dir(project)
    issues: List[str] = []

    blueprint = root / "docs" / "architecture" / "BLUEPRINT.md"
    data_model = root / "docs" / "architecture" / "data-model.md"
    adr_dir = root / "docs" / "adr"

    if not _min_content(blueprint, 120):
        issues.append("Fill docs/architecture/BLUEPRINT.md")
    if not _min_content(data_model, 60):
        issues.append("Fill docs/architecture/data-model.md")

    adrs = list(adr_dir.glob("ADR-*.md")) if adr_dir.exists() else []
    if not adrs:
        issues.append("At least one ADR required in docs/adr/")

    return len(issues) == 0, issues


def validate_gate_2a(project: str) -> Tuple[bool, List[str]]:
    """Signed design direction (discovery Q&A + DESIGN.md). Blocks prototype."""
    from studio_adopt import is_adopt_project
    from studio_design_discovery import gate_2a_issues

    issues = gate_2a_issues(project_dir(project), adopt=is_adopt_project(project))
    return len(issues) == 0, issues


def validate_gate_2b(project: str) -> Tuple[bool, List[str]]:
    """Project-owned kit: CSS tokens, coded A/M/O, sticker inventory, mocks."""
    from studio_adopt import is_adopt_project
    from studio_design_discovery import gate_2b_issues

    issues = gate_2b_issues(project_dir(project), adopt=is_adopt_project(project))
    return len(issues) == 0, issues


def validate_gate_2(project: str) -> Tuple[bool, List[str]]:
    """Legacy alias — kit check is gate 2b. CLI refuses bare --gate 2."""
    return validate_gate_2b(project)


GATE_VALIDATORS = {
    0: validate_gate_0,
    1: validate_gate_1,
    2: validate_gate_2b,
    "0": validate_gate_0,
    "1": validate_gate_1,
    "2a": validate_gate_2a,
    "2b": validate_gate_2b,
}


def _gate_id(gate: Union[int, str]) -> str:
    return str(gate).strip().lower()


def previous_human_gate_block(status: Dict, gate: Union[int, str]) -> Optional[str]:
    """Refuse gate N until the previous human gate is approved (re-approve is allowed)."""
    from studio_design_discovery import BARE_GATE_2_MSG

    g = _gate_id(gate)
    hg = status.get("human_gates") or {}
    if g == "2":
        return BARE_GATE_2_MSG
    if g == "0":
        return None
    if (hg.get(g) or {}).get("status") == "approved":
        return None
    if g == "1":
        prev = "0"
    elif g == "2a":
        prev = "1"
    elif g == "2b":
        prev = "2a"
        if (hg.get("2") or {}).get("status") == "approved":
            return None
    else:
        return None
    if (hg.get(prev) or {}).get("status") != "approved":
        return (
            f"Gate {prev} is not approved. Run ./studio approve <project> --gate {prev} first."
        )
    return None


def direction_approved(status: Dict) -> bool:
    """Gate 2a signed, or legacy full gate 2."""
    hg = status.get("human_gates") or {}
    if (hg.get("2a") or {}).get("status") == "approved":
        return True
    return (hg.get("2") or {}).get("status") == "approved"


def design_system_approved(status: Dict) -> bool:
    """Gate 2b signed, or legacy human_gates.2."""
    hg = status.get("human_gates") or {}
    if (hg.get("2b") or {}).get("status") == "approved":
        return True
    return (hg.get("2") or {}).get("status") == "approved"


def validate_human_gate(project: str, gate: Union[int, str]) -> Tuple[bool, List[str]]:
    g = _gate_id(gate)
    if g == "2":
        from studio_design_discovery import BARE_GATE_2_MSG

        return False, [BARE_GATE_2_MSG]
    validator = GATE_VALIDATORS.get(g) or GATE_VALIDATORS.get(gate)  # type: ignore[arg-type]
    if not validator:
        return False, [f"Unknown human gate: {gate}"]
    return validator(project)


def ensure_pre_impl_dirs(root: Path) -> None:
    dirs = [
        "docs/architecture",
        "docs/architecture/diagrams",
        "docs/design",
        "docs/ia",
        "design/prototype/app/mocks",
        "design/prototype/app/sticker-sheet",
        "design/prototype/components",
        "ui/tokens",
        "ui/components/atoms",
        "ui/components/molecules",
        "ui/components/organisms",
        "ui/page-types",
        "docs/phases",
    ]
    for d in dirs:
        (root / d).mkdir(parents=True, exist_ok=True)


def scaffold_discovery(project: str) -> List[Path]:
    """2a packet only — questions + direction template. No prototype, no indigo."""
    root = project_dir(project)
    ensure_pre_impl_dirs(root)
    created: List[Path] = []
    date = datetime.now().strftime("%Y-%m-%d")

    discovery = root / "docs" / "design" / "discovery.md"
    if not discovery.exists():
        tpl = TEMPLATES_DIR / "design_discovery_template.md"
        body = tpl.read_text() if tpl.exists() else (
            f"# Design discovery — {project}\n\nQ: What job is done?\nA: _unanswered_\n"
        )
        body = body.replace("{{PROJECT}}", project).replace("{{DATE}}", date)
        discovery.write_text(body)
        created.append(discovery)

    design = root / "design" / "DESIGN.md"
    if not design.exists():
        tpl = TEMPLATES_DIR / "design_direction_template.md"
        body = tpl.read_text() if tpl.exists() else f"# Design specification — {project}\n"
        body = body.replace("{{PROJECT}}", project).replace("{{DATE}}", date)
        design.write_text(body)
        created.append(design)

    return created


def scaffold_blueprint(project: str, archetype: str) -> List[Path]:
    root = project_dir(project)
    ensure_pre_impl_dirs(root)
    created: List[Path] = []

    blueprint_tpl = TEMPLATES_DIR / "blueprint_template.md"
    blueprint = root / "docs" / "architecture" / "BLUEPRINT.md"
    if not blueprint.exists():
        content = blueprint_tpl.read_text() if blueprint_tpl.exists() else "# Architecture Blueprint\n"
        content = content.replace("{{PROJECT}}", project).replace("{{ARCHETYPE}}", archetype)
        content = content.replace("{{DATE}}", datetime.now().strftime("%Y-%m-%d"))
        blueprint.write_text(content)
        created.append(blueprint)

    data_model = root / "docs" / "architecture" / "data-model.md"
    if not data_model.exists():
        data_model.write_text(
            f"# Data Model — {project}\n\n"
            "## Entities\n\n| Entity | Description |\n|--------|-------------|\n| _TODO_ | _TODO_ |\n\n"
            "## Relationships\n\n_Describe entity relationships (mermaid ER diagram recommended)._\n"
        )
        created.append(data_model)

    api_overview = root / "docs" / "architecture" / "api-overview.md"
    if not api_overview.exists():
        api_overview.write_text(
            f"# API Overview — {project}\n\n"
            "_Document APIs only if the project has a backend or cloud sync._\n\n"
            "## Endpoints\n\n| Method | Path | Purpose |\n|--------|------|--------|\n"
        )
        created.append(api_overview)

    return created


def scaffold_design(project: str, scope: str = "core-views") -> List[Path]:
    """Scaffold project kit after gate 2a. Token names from DESIGN.md — never indigo defaults."""
    root = project_dir(project)
    ensure_pre_impl_dirs(root)
    write_ui_kit_setup(root)
    created: List[Path] = []

    if scope not in ("journey", "core-views"):
        scope = "core-views"

    scope_file = root / "design" / "DESIGN-SCOPE.md"
    scope_tpl = TEMPLATES_DIR / "design_scope_template.md"
    from studio_design_discovery import project_archetype, pull_names_for, shell_routes_for

    archetype = project_archetype(root)
    if not scope_file.exists() or _has_placeholders(_read_text(scope_file)):
        base = scope_tpl.read_text() if scope_tpl.exists() else "# Design Scope\n"
        shell_lines = "\n".join(f"- `{route}`" for route in shell_routes_for(archetype))
        if not shell_lines:
            shell_lines = "_No UI shell — api-service has no prototype._"
        base = base.replace("{{PROJECT}}", project).replace("{{SCOPE}}", scope)
        base = base.replace("{{DATE}}", datetime.now().strftime("%Y-%m-%d"))
        base = base.replace("{{ARCHETYPE}}", archetype).replace("{{SHELL_ROUTES}}", shell_lines)
        scope_file.write_text(base)
        created.append(scope_file)

    created.extend(scaffold_discovery(project))

    css = root / "ui" / "tokens" / "design-tokens.css"
    if not css.exists():
        css.write_text(
            "/* Fill values from signed design/DESIGN.md. Do not paste catalog indigo. */\n"
            ":root {\n"
            "  --surface: ;\n"
            "  --ink: ;\n"
            "  --accent: ;\n"
            "  --danger: ;\n"
            "  --font-sans: ;\n"
            "  --space-unit: 8px;\n"
            "}\n"
        )
        created.append(css)

    tokens = root / "ui" / "tokens" / "design-tokens.json"
    if not tokens.exists():
        tokens.write_text(
            json.dumps(
                {
                    "color": {
                        "surface": {"token": "--surface"},
                        "ink": {"token": "--ink"},
                        "accent": {"token": "--accent"},
                        "danger": {"token": "--danger"},
                    },
                    "typography": {"fontFamily": {"sans": "var(--font-sans)"}},
                    "spacing": {"unit": "var(--space-unit)"},
                    "shadow": {},
                    "radius": {},
                },
                indent=2,
            )
            + "\n"
        )
        created.append(tokens)

    if archetype == "api-service":
        return created

    from library_manager import pull_assets

    pull_assets(project, pull_names_for(archetype), project_root=root)

    proto_readme = root / "design" / "prototype" / "README.md"
    if not proto_readme.exists():
        proto_readme.write_text(
            f"# Design prototype — {project}\n\n"
            "Next.js app for **gate 2b** mocks (project tokens — not studio-library look).\n\n"
            "```bash\n"
            "cd design/prototype && npm install && npm run dev\n"
            "```\n\n"
            "UI kit peers are already in this `package.json` "
            "(`radix-ui`, `class-variance-authority`, `clsx`, `tailwind-merge`, `lucide-react`, `@headlessui/react`).\n\n"
            "## Routes\n\n"
            "- `/sticker-sheet` — tokens + all component states\n"
            "- `/mocks/*` — screen mocks (journey or core views per DESIGN-SCOPE.md)\n"
        )
        created.append(proto_readme)

    created.extend(_scaffold_next_prototype(root, project, scope))
    return created


def product_app_dir(root: Path) -> Path:
    src_app = root / "src" / "app"
    app = root / "app"
    if src_app.is_dir() and not app.is_dir():
        return src_app
    return app


def materialize_baseline(project: str) -> List[Path]:
    """Copy prototype mocks into the product app. Leave design/prototype/ in place.

    The prototype stays the visual baseline. Implementation wires and may enhance
    those screens. Adopt projects must not call this.
    """
    root = project_dir(project)
    created: List[Path] = []
    proto_mocks = root / "design" / "prototype" / "app" / "mocks"
    dest_root = product_app_dir(root)
    copied: List[str] = []
    if proto_mocks.exists():
        for page in sorted(proto_mocks.rglob("page.tsx")):
            rel = page.relative_to(proto_mocks)
            parts = rel.parts
            if parts and parts[0] == "app":
                rel = Path(*parts[1:])
            target = dest_root / rel
            if target.exists():
                copied.append(f"{rel.as_posix()} (already present)")
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            body = page.read_text(encoding="utf-8")
            note = (
                "/** Materialized from design/prototype. "
                "Wire data here. The prototype remains the visual baseline. */\n"
            )
            target.write_text(note + body, encoding="utf-8")
            created.append(target)
            copied.append(rel.as_posix())

    baseline = root / "docs" / "design" / "baseline.md"
    baseline.parent.mkdir(parents=True, exist_ok=True)
    route_lines = "\n".join(f"- `{item}`" for item in copied) or "- (no mock pages copied)"
    baseline.write_text(
        "# Design baseline\n\n"
        "The prototype at `design/prototype/` is the visual baseline. Reopen it when "
        "implementation drifts.\n\n"
        "Gate 2b copied shell and journey mocks into the product app as the first screens. "
        "They still use mock data and the same `ui/components` and `ui/tokens`.\n\n"
        "Implementation wires data and may improve UX, IA, structure, and infrastructure. "
        "A change that leaves this baseline (a new popover, tooltip, dropdown, dialog, or "
        "app shell) needs an `Enhancement:` line on the receipt, or a design-track ticket "
        "when it changes tokens, the shell, or a new component.\n\n"
        "## Materialized routes\n\n"
        f"{route_lines}\n",
        encoding="utf-8",
    )
    created.append(baseline)
    return created


def _scaffold_next_prototype(root: Path, project: str, scope: str) -> List[Path]:
    created: List[Path] = []
    proto = root / "design" / "prototype"

    files: Dict[str, str] = {
        "package.json": json.dumps(
            {
                "name": f"{project}-design-prototype",
                "private": True,
                "scripts": {"dev": "next dev", "build": "next build", "start": "next start"},
                "dependencies": merge_kit_peers(
                    {
                        "next": "^14.2.0",
                        "react": "^18.3.0",
                        "react-dom": "^18.3.0",
                    }
                ),
                "devDependencies": {
                    "@types/node": "^20.0.0",
                    "@types/react": "^18.3.0",
                    "typescript": "^5.0.0",
                    "tailwindcss": "^3.4.0",
                    "postcss": "^8.4.0",
                    "autoprefixer": "^10.4.0",
                },
            },
            indent=2,
        )
        + "\n",
        "tsconfig.json": json.dumps(
            {
                "compilerOptions": {
                    "target": "ES2017",
                    "lib": ["dom", "dom.iterable", "esnext"],
                    "allowJs": True,
                    "skipLibCheck": True,
                    "strict": True,
                    "noEmit": True,
                    "esModuleInterop": True,
                    "module": "esnext",
                    "moduleResolution": "bundler",
                    "resolveJsonModule": True,
                    "isolatedModules": True,
                    "jsx": "preserve",
                    "incremental": True,
                    "plugins": [{"name": "next"}],
                    "paths": {"@/*": ["./*"], "@ui/*": ["../../ui/*"]},
                },
                "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx"],
                "exclude": ["node_modules"],
            },
            indent=2,
        )
        + "\n",
        "next.config.js": "/** @type {import('next').NextConfig} */\nmodule.exports = { reactStrictMode: true };\n",
        "postcss.config.js": "module.exports = { plugins: { tailwindcss: {}, autoprefixer: {} } };\n",
        "tailwind.config.ts": (
            "import type { Config } from 'tailwindcss';\n\n"
            "const config: Config = {\n"
            "  content: ['./app/**/*.{ts,tsx}', '../../ui/components/**/*.{ts,tsx}'],\n"
            "  theme: {\n"
            "    extend: {\n"
            "      colors: {\n"
            "        surface: 'var(--surface)',\n"
            "        ink: 'var(--ink)',\n"
            "        accent: 'var(--accent)',\n"
            "        danger: 'var(--danger)',\n"
            "      },\n"
            "    },\n"
            "  },\n"
            "  plugins: [],\n"
            "};\nexport default config;\n"
        ),
        "app/globals.css": (
            "@import '../../ui/tokens/design-tokens.css';\n"
            "@tailwind base;\n@tailwind components;\n@tailwind utilities;\n"
        ),
        "app/layout.tsx": (
            "import './globals.css';\n\n"
            "export default function RootLayout({ children }: { children: React.ReactNode }) {\n"
            "  return (\n"
            "    <html lang=\"en\">\n"
            "      <body className=\"min-h-screen bg-white text-neutral-900 antialiased\">{children}</body>\n"
            "    </html>\n"
            "  );\n"
            "}\n"
        ),
        "app/page.tsx": (
            "import Link from 'next/link';\n\n"
            "export default function Home() {\n"
            "  return (\n"
            "    <main className=\"mx-auto max-w-2xl p-8 space-y-4\">\n"
            "      <h1 className=\"text-2xl font-bold\">Design prototype</h1>\n"
            "      <p className=\"text-neutral-600\">Gate 2b mocks — import project tokens, not a second palette.</p>\n"
            "      <ul className=\"list-disc pl-6 space-y-2\">\n"
            "        <li><Link className=\"underline\" href=\"/sticker-sheet\">Sticker sheet</Link></li>\n"
            "        <li><Link className=\"underline\" href=\"/mocks/home\">Mock: home</Link></li>\n"
            "      </ul>\n"
            "    </main>\n"
            "  );\n"
            "}\n"
        ),
        "app/sticker-sheet/page.tsx": (
            "/** Gate 2b sticker: render inventory children with states. Title-only fails. */\n"
            "export default function StickerSheetPage() {\n"
            "  return (\n"
            "    <main className=\"p-8 space-y-12\">\n"
            "      <h1 className=\"text-2xl font-bold mb-4\">Sticker sheet</h1>\n"
            "      <p className=\"text-sm text-neutral-600\">Fill from ui/components — atoms, molecules, organisms, all states.</p>\n"
            "      <section>\n"
            "        <h2 className=\"text-lg font-semibold mb-2\">Atoms</h2>\n"
            "      </section>\n"
            "      <section>\n"
            "        <h2 className=\"text-lg font-semibold mb-2\">Molecules</h2>\n"
            "      </section>\n"
            "      <section>\n"
            "        <h2 className=\"text-lg font-semibold mb-2\">Organisms</h2>\n"
            "      </section>\n"
            "    </main>\n"
            "  );\n"
            "}\n"
        ),
        f"app/mocks/home/page.tsx": (
            f"/** Core view mock — scope: {scope} */\n"
            "export default function MockHome() {\n"
            "  return (\n"
            "    <main className=\"p-8\">\n"
            "      <h1 className=\"text-xl font-bold\">Home (mock)</h1>\n"
            "      <p className=\"mt-2 text-neutral-600\">Replace with approved screen design.</p>\n"
            "    </main>\n"
            "  );\n"
            "}\n"
        ),
    }

    for rel, content in files.items():
        path = proto / rel
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
            created.append(path)

    atom_readme = root / "ui" / "components" / "atoms" / "README.md"
    if not atom_readme.exists():
        atom_readme.write_text(
            "# Atoms\n\nSmallest UI primitives (Button, Input, Badge). Used by prototype and final app.\n"
        )
        created.append(atom_readme)

    return created


def record_revision(project: str, gate: Union[int, str], feedback: str) -> Path:
    root = project_dir(project)
    rev_dir = root / "docs" / "phases"
    rev_dir.mkdir(parents=True, exist_ok=True)
    rev_file = rev_dir / "revisions.md"
    if not rev_file.exists():
        rev_file.write_text("# Pre-implementation revisions\n\n")
    entry = (
        f"\n## Gate {gate} — {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        f"{feedback.strip()}\n"
    )
    rev_file.write_text(rev_file.read_text() + entry)
    return rev_file
