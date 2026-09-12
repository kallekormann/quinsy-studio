"""Canonical UI kit peer deps for every Quinsy project (styled studio-library).

Projects that pull studio-library components need these in the **app** package.json
(design prototype, Next app, Vite app — wherever React UI is built). HQ `./studio install`
does not install them into the product.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

# Required for the shadcn-style kit. Optional extras stay per-component README.
UI_KIT_PEER_DEPS: Dict[str, str] = {
    "radix-ui": "^1.6.7",
    "class-variance-authority": "^0.7.1",
    "clsx": "^2.1.1",
    "tailwind-merge": "^2.6.0",
    "lucide-react": "^0.544.0",
}

HEADLESS_PEER_DEPS: Dict[str, str] = {
    "@headlessui/react": "^2.2.9",
}

NPM_INSTALL_KIT = (
    "npm install radix-ui class-variance-authority clsx tailwind-merge lucide-react"
)
NPM_INSTALL_HEADLESS = "npm install @headlessui/react"


def kit_peer_names() -> List[str]:
    return list(UI_KIT_PEER_DEPS.keys())


def merge_kit_peers(dependencies: Dict[str, str], *, include_headless: bool = True) -> Dict[str, str]:
    out = dict(dependencies)
    for name, ver in UI_KIT_PEER_DEPS.items():
        out.setdefault(name, ver)
    if include_headless:
        for name, ver in HEADLESS_PEER_DEPS.items():
            out.setdefault(name, ver)
    return out


def ensure_package_json_kit_peers(package_json: Path, *, include_headless: bool = True) -> bool:
    """Merge kit peers into an existing package.json. Returns True if the file was written."""
    if not package_json.is_file():
        return False
    data = json.loads(package_json.read_text(encoding="utf-8"))
    deps = dict(data.get("dependencies") or {})
    merged = merge_kit_peers(deps, include_headless=include_headless)
    if merged == deps:
        return False
    data["dependencies"] = merged
    package_json.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return True


def find_project_package_jsons(project_dir: Path) -> List[Path]:
    candidates = [
        project_dir / "package.json",
        project_dir / "design" / "prototype" / "package.json",
        project_dir / "apps" / "web" / "package.json",
        project_dir / "apps" / "webapp" / "package.json",
    ]
    found: List[Path] = []
    seen = set()
    for p in candidates:
        if p.is_file() and p.resolve() not in seen:
            seen.add(p.resolve())
            found.append(p)
    apps = project_dir / "apps"
    if apps.is_dir():
        for pkg in sorted(apps.glob("*/package.json")):
            if pkg.resolve() not in seen:
                found.append(pkg)
    return found


def ensure_project_kit_peers(project_dir: Path) -> List[Path]:
    """Merge kit peers into every known app package.json. Returns paths updated."""
    updated: List[Path] = []
    for pkg in find_project_package_jsons(project_dir):
        if ensure_package_json_kit_peers(pkg):
            updated.append(pkg)
    return updated


def kit_setup_markdown() -> str:
    return """# UI kit peers (mandatory)

Every Quinsy product that uses studio-library styled components **must** install:

```bash
npm install radix-ui class-variance-authority clsx tailwind-merge lucide-react
```

Plus Headless UI primitives:

```bash
npm install @headlessui/react
```

Install in the **app** that renders React (prototype, `apps/<web>/`, package root) — not only Studio HQ.

`./studio init` / `./studio design` bake these into the scaffolded `package.json`. `./studio adopt` writes this file and merges the same peers into any existing app `package.json`. `./studio library pull` of UI also merges if they were missing.

Optional extras (only if you pull that component): `cmdk`, `vaul`, `@base-ui/react`, `input-otp`, `react-day-picker`, `recharts`, `embla-carousel-react`, `react-resizable-panels`, `sonner`.

See `.quinsy-studio/studio-library/ui/docs/getting-started/installation.md`.
"""


def format_kit_peer_hint() -> str:
    return (
        "UI kit peers (required in the project app): "
        + NPM_INSTALL_KIT
        + " && "
        + NPM_INSTALL_HEADLESS
    )


def write_ui_kit_setup(project_dir: Path) -> Path:
    setup = project_dir / "docs" / "setup"
    setup.mkdir(parents=True, exist_ok=True)
    dest = setup / "ui-kit.md"
    if not dest.exists():
        dest.write_text(kit_setup_markdown(), encoding="utf-8")
    return dest
