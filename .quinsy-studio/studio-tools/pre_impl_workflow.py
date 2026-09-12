#!/usr/bin/env python3
"""
Pre-implementation workflow: intake → blueprint → design → tickets.

Human gates 0 (intake), 1 (architecture), 2 (design + mocks).
Tickets are generated only after gate 2 approval.
"""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

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


def validate_gate_2(project: str) -> Tuple[bool, List[str]]:
    """Design + Next.js prototype mocks ready for human review."""
    from studio_adopt import is_adopt_project

    root = project_dir(project)
    issues: List[str] = []
    adopt = is_adopt_project(project)

    design = root / "design" / "DESIGN.md"
    scope = root / "design" / "DESIGN-SCOPE.md"
    tokens = root / "ui" / "tokens" / "design-tokens.json"
    prototype_pkg = root / "design" / "prototype" / "package.json"
    sticker = root / "design" / "prototype" / "app" / "sticker-sheet" / "page.tsx"
    mocks_dir = root / "design" / "prototype" / "app" / "mocks"

    if not _min_content(design, 100):
        issues.append("Fill design/DESIGN.md")
    if not scope.exists() or not _min_content(scope, 40):
        issues.append(
            "Fill design/DESIGN-SCOPE.md (as-built existing product)"
            if adopt
            else "Fill design/DESIGN-SCOPE.md (journey vs core-views decision)"
        )
    elif "scope:" not in _read_text(scope).lower() and "scope" not in _read_text(scope).lower():
        issues.append("design/DESIGN-SCOPE.md must document mock scope (journey | core-views | as-built)")

    if adopt:
        surfaces = root / "docs" / "as-built" / "01-surfaces.md"
        if not _min_content(surfaces, 80):
            issues.append("Fill docs/as-built/01-surfaces.md (existing routes/screens)")
        ia = root / "docs" / "ia" / "surface-map.md"
        if not _min_content(ia, 60):
            issues.append("Fill docs/ia/surface-map.md from existing UI (no greenfield prototype)")
        return len(issues) == 0, issues

    if not tokens.exists():
        issues.append("Missing ui/tokens/design-tokens.json")
    if not prototype_pkg.exists():
        issues.append("Missing design/prototype/ Next.js app — run ./studio design <project>")
    if not sticker.exists():
        issues.append("Missing design/prototype/app/sticker-sheet/page.tsx")
    mock_pages = list(mocks_dir.glob("**/page.tsx")) if mocks_dir.exists() else []
    if not mock_pages:
        issues.append("No mock pages in design/prototype/app/mocks/ — add at least one page.tsx")

    atoms = root / "ui" / "components" / "atoms"
    atom_files = [f for f in atoms.glob("*") if f.name != "README.md"] if atoms.exists() else []
    if not atom_files:
        issues.append("Add at least one atom component in ui/components/atoms/")

    return len(issues) == 0, issues


GATE_VALIDATORS = {
    0: validate_gate_0,
    1: validate_gate_1,
    2: validate_gate_2,
}


def validate_human_gate(project: str, gate: int) -> Tuple[bool, List[str]]:
    validator = GATE_VALIDATORS.get(gate)
    if not validator:
        return False, [f"Unknown human gate: {gate}"]
    return validator(project)


def ensure_pre_impl_dirs(root: Path) -> None:
    dirs = [
        "docs/architecture",
        "docs/architecture/diagrams",
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
    """Scaffold design docs + Next.js prototype structure. scope: journey | core-views"""
    root = project_dir(project)
    ensure_pre_impl_dirs(root)
    write_ui_kit_setup(root)
    created: List[Path] = []

    if scope not in ("journey", "core-views"):
        scope = "core-views"

    scope_file = root / "design" / "DESIGN-SCOPE.md"
    scope_tpl = TEMPLATES_DIR / "design_scope_template.md"
    if not scope_file.exists() or _has_placeholders(_read_text(scope_file)):
        base = scope_tpl.read_text() if scope_tpl.exists() else "# Design Scope\n"
        base = base.replace("{{PROJECT}}", project).replace("{{SCOPE}}", scope)
        base = base.replace("{{DATE}}", datetime.now().strftime("%Y-%m-%d"))
        scope_file.write_text(base)
        created.append(scope_file)

    design = root / "design" / "DESIGN.md"
    if not design.exists():
        design.write_text(
            f"# Design Specification — {project}\n\n"
            f"> Status: draft (waiting for human gate 2)\n"
            f"> Mock scope: {scope}\n\n"
            "## Visual direction\n\n_Describe look & feel from PRD._\n\n"
            "## Atomic design map\n\n"
            "- Atoms → `ui/components/atoms/`\n"
            "- Molecules → `ui/components/molecules/`\n"
            "- Organisms → `ui/components/organisms/`\n"
            "- Page types → `ui/page-types/`\n"
            "- Prototype routes → `design/prototype/app/mocks/`\n\n"
            "## Sticker sheet\n\n"
            "Combined tokens + components: `design/prototype/app/sticker-sheet/`\n"
        )
        created.append(design)

    tokens = root / "ui" / "tokens" / "design-tokens.json"
    if not tokens.exists():
        tokens.write_text(
            json.dumps(
                {
                    "color": {"primary": {"500": "#6366f1"}},
                    "typography": {"fontFamily": {"sans": "system-ui"}},
                    "spacing": {"unit": 8},
                    "shadow": {},
                    "radius": {},
                },
                indent=2,
            )
            + "\n"
        )
        created.append(tokens)

    proto_readme = root / "design" / "prototype" / "README.md"
    if not proto_readme.exists():
        proto_readme.write_text(
            f"# Design prototype — {project}\n\n"
            "Next.js app for **pre-implementation** mocks (gate 2 approval).\n\n"
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
            "import type { Config } from 'tailwindcss';\n"
            "import tokens from '../../ui/tokens/design-tokens.json';\n\n"
            "const config: Config = {\n"
            "  content: ['./app/**/*.{ts,tsx}', '../../ui/components/**/*.{ts,tsx}'],\n"
            "  theme: { extend: { colors: tokens.color } },\n"
            "  plugins: [],\n"
            "};\nexport default config;\n"
        ),
        "app/globals.css": (
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
            "      <p className=\"text-neutral-600\">Pre-implementation mocks for gate 2 approval.</p>\n"
            "      <ul className=\"list-disc pl-6 space-y-2\">\n"
            "        <li><Link className=\"text-indigo-600 underline\" href=\"/sticker-sheet\">Sticker sheet</Link></li>\n"
            "        <li><Link className=\"text-indigo-600 underline\" href=\"/mocks/home\">Mock: home</Link></li>\n"
            "      </ul>\n"
            "    </main>\n"
            "  );\n"
            "}\n"
        ),
        "app/sticker-sheet/page.tsx": (
            "/** Combined token sheet + component inventory for gate 2 approval */\n"
            "export default function StickerSheetPage() {\n"
            "  return (\n"
            "    <main className=\"p-8 space-y-12\">\n"
            "      <section>\n"
            "        <h1 className=\"text-2xl font-bold mb-4\">Sticker sheet</h1>\n"
            "        <p className=\"text-sm text-neutral-600\">Tokens + components (atoms → organisms). Replace placeholders.</p>\n"
            "      </section>\n"
            "      <section>\n"
            "        <h2 className=\"text-lg font-semibold mb-2\">Colors</h2>\n"
            "        <div className=\"flex gap-2\">\n"
            "          <div className=\"h-12 w-12 rounded bg-indigo-500\" title=\"primary-500\" />\n"
            "        </div>\n"
            "      </section>\n"
            "      <section>\n"
            "        <h2 className=\"text-lg font-semibold mb-2\">Buttons</h2>\n"
            "        <button type=\"button\" className=\"rounded-lg bg-indigo-600 px-4 py-2 text-white\">Primary</button>\n"
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


def record_revision(project: str, gate: int, feedback: str) -> Path:
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
