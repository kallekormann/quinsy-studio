#!/usr/bin/env python3
"""
Quinsy Studio — External Skills Importer (Skill-Package-Manager)

Loads the external best-in-class skills declared in `.quinsy-studio/skill-dependencies.json`
and places them under `.quinsy-studio/external-skills/<domain>/` so the agent
can integrate them into the respective role profiles.

Usage:
    python3 import_external_skills.py            # Install/update all dependencies
    python3 import_external_skills.py --list     # Show declared dependencies
    python3 import_external_skills.py design     # Install a single domain

Dependencies:
    - `npx` (Node) for `npx skills add <owner>/<repo>`
    - Fallback: `git clone` (without Node)

Rules:
    - External skills are ALWAYS subordinate to the internal anti_ai_slop_protocol.md
      and the Zero-Data Architecture.
    - After the import an INDEX.md is generated documenting the mapping
      domain → team → skill file.
"""

import sys
import json
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

STUDIO_ROOT = Path(__file__).parent.parent.parent
QUINSY_STUDIO = STUDIO_ROOT / ".quinsy-studio"
TOOLS_DIR = QUINSY_STUDIO / "studio-tools"
DEPENDENCIES_FILE = QUINSY_STUDIO / "skill-dependencies.json"
EXTERNAL_SKILLS_DIR = QUINSY_STUDIO / "external-skills"


def load_dependencies() -> dict:
    """Load the skill dependencies from the JSON file."""
    if not DEPENDENCIES_FILE.exists():
        print(f"  ⚠️  No skill-dependencies.json found: {DEPENDENCIES_FILE}")
        return {}
    data = json.loads(DEPENDENCIES_FILE.read_text())
    # Filter out meta keys (//, //2, ...)
    return {k: v for k, v in data.items() if isinstance(v, dict)}


def has_npx() -> bool:
    """Check whether npx (Node) is available."""
    return shutil.which("npx") is not None


def has_git() -> bool:
    """Check whether git is available."""
    return shutil.which("git") is not None


def npx_install(dep_name: str, spec: dict) -> bool:
    """Install a skill package via `npx skills add`."""
    install_cmd = spec.get("install", f"npx skills add {dep_name}")
    print(f"    → npx: {install_cmd}")
    try:
        result = subprocess.run(
            install_cmd.split(), capture_output=True, text=True, timeout=120
        )
        if result.returncode != 0:
            print(f"    ⚠️  npx failed ({result.returncode}): {result.stderr[:300]}")
            return False
        print(f"    ✓ installed via npx")
        return True
    except FileNotFoundError:
        return False
    except subprocess.TimeoutExpired:
        print(f"    ⚠️  npx timeout")
        return False


def git_clone(dep_name: str, spec: dict) -> bool:
    """Fallback: clone the repository into external-skills/<domain>/."""
    repo = spec.get("repo", "")
    # "github:Nutlope/hallmark@main" → https://github.com/Nutlope/hallmark.git
    if repo.startswith("github:"):
        url = repo.replace("github:", "https://github.com/", 1)
        url = url.split("@")[0] + ".git"
    else:
        url = repo

    target = EXTERNAL_SKILLS_DIR / dep_name
    target.mkdir(parents=True, exist_ok=True)

    print(f"    → git clone: {url}")
    try:
        if (target / ".git").exists():
            print(f"    ✓ already present: {target} (git pull for update)")
            subprocess.run(
                ["git", "-C", str(target), "pull"], capture_output=True, text=True, timeout=60
            )
            return True
        result = subprocess.run(
            ["git", "clone", "--depth", "1", url, str(target)],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode != 0:
            print(f"    ⚠️  git clone failed: {result.stderr[:300]}")
            return False
        print(f"    ✓ cloned to: {target}")
        return True
    except FileNotFoundError:
        print(f"    ⚠️  git not available")
        return False


def import_dependency(dep_name: str, spec: dict, use_npx: bool = False) -> bool:
    """Import a single dependency.

    Default: git clone into .quinsy-studio/external-skills/<domain>/ —
    keeps the studio self-contained and project-referencable.
    Optional (--npx): `npx skills add` for local agent integration
    (installs into ~/.claude/skills etc., NOT into the studio).
    """
    team = spec.get("team", "?")
    why = spec.get("why", "")
    print(f"\n  [{dep_name}] → Team: {team}")
    if why:
        print(f"    {why}")

    if use_npx and has_npx():
        ok = npx_install(dep_name, spec)
        if ok:
            return True
        print(f"    → falling back to git clone")

    if has_git():
        return git_clone(dep_name, spec)

    print(f"    ⚠️  git not available — manual import required")
    return False


def generate_index(results: dict):
    """Generate the INDEX.md with the domain → team → skills mapping."""
    EXTERNAL_SKILLS_DIR.mkdir(parents=True, exist_ok=True)
    index_file = EXTERNAL_SKILLS_DIR / "INDEX.md"

    lines = [
        "# External Skills — Index",
        "",
        f"> Generiert: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "> Source: `.quinsy-studio/skill-dependencies.json`",
        "",
        "External best-in-class skills the studio subscribes to. They are ALWAYS",
        "subordinate to the internal `anti_ai_slop_protocol.md` and the Zero-Data Architecture.",
        "",
        "## Overview",
        "",
        "| Domain | Team | Status | Quelle |",
        "|--------|------|--------|--------|",
    ]

    for name, (spec, ok) in sorted(results.items()):
        status = "✅" if ok else "❌"
        repo = spec.get("repo", "-")
        lines.append(f"| `{name}` | {spec.get('team', '-')} | {status} | `{repo}` |")

    lines += [
        "",
        "## Usage in the process",
        "",
        "1. `./studio update-skills` — subscribe to/update all dependencies.",
        "2. The agent reads the respective SKILL.md of the imported package before",
        "   activating the associated role (see `.quinsy-studio/teams/skill-registry.md`).",
        "3. Conflicts with internal rules are ALWAYS decided by the internal studio rulebook.",
    ]

    index_file.write_text("\n".join(lines))
    print(f"\n  INDEX.md generated: {index_file}")


def main():
    deps = load_dependencies()
    if not deps:
        print("Keine Dependencies deklariert.")
        return

    if "--list" in sys.argv:
        print("\nDeclared skill dependencies:")
        for name, spec in sorted(deps.items()):
            print(f"  [{name}] {spec.get('repo', '?')} → Team {spec.get('team', '?')}")
        print("\nOptions:")
        print("  --npx   Local agent install via `npx skills add` (not into the studio)")
        print("  <name>  Import a single domain only")
        return

    # Only one domain if specified; --npx for local agent installation
    targets = None
    use_npx = "--npx" in sys.argv
    for arg in sys.argv[1:]:
        if arg in deps:
            targets = [arg]
            break

    results = {}
    for name, spec in sorted(deps.items()):
        if targets and name not in targets:
            continue
        results[name] = (spec, import_dependency(name, spec, use_npx))

    generate_index(results)

    ok_count = sum(1 for _, ok in results.values() if ok)
    print(f"\n  {'=' * 50}")
    print(f"  Result: {ok_count}/{len(results)} dependencies imported")
    print(f"  Next step: run ./studio update-skills for new sources, or")
    print(f"  work skills into the team skills manually (.quinsy-studio/teams/).")


if __name__ == "__main__":
    main()
