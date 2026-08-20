#!/usr/bin/env python3
"""
Quinsy Studio — External Skills Importer (Skill-Package-Manager)

Lädt die in `.quinsy-studio/skill-dependencies.json` deklarierten externen
Best-in-Class Skills und legt sie unter `.quinsy-studio/external-skills/<domain>/`
ab, damit der Agent sie in die jeweiligen Rollen-Profile einbinden kann.

Verwendung:
    python3 import_external_skills.py            # Alle Dependencies installieren/aktualisieren
    python3 import_external_skills.py --list     # Deklarierte Dependencies anzeigen
    python3 import_external_skills.py design     # Nur eine Domain installieren

Abhängigkeiten:
    - `npx` (Node) für `npx skills add <owner>/<repo>`
    - Fallback: `git clone` (ohne Node)

Regeln:
    - Externe Skills sind IMMER dem internen anti_ai_slop_protocol.md und
      der Zero-Data-Architecture untergeordnet.
    - Nach dem Import wird ein INDEX.md generiert, der die Zuordnung
      Domain → Team → Skill-Datei dokumentiert.
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
    """Lädt die Skill-Dependencies aus der JSON-Datei."""
    if not DEPENDENCIES_FILE.exists():
        print(f"  ⚠️  Keine skill-dependencies.json gefunden: {DEPENDENCIES_FILE}")
        return {}
    data = json.loads(DEPENDENCIES_FILE.read_text())
    # Meta-Keys (//, //2, ...) herausfiltern
    return {k: v for k, v in data.items() if isinstance(v, dict)}


def has_npx() -> bool:
    """Prüft, ob npx (Node) verfügbar ist."""
    return shutil.which("npx") is not None


def has_git() -> bool:
    """Prüft, ob git verfügbar ist."""
    return shutil.which("git") is not None


def npx_install(dep_name: str, spec: dict) -> bool:
    """Installiert ein Skill-Paket via `npx skills add`."""
    install_cmd = spec.get("install", f"npx skills add {dep_name}")
    print(f"    → npx: {install_cmd}")
    try:
        result = subprocess.run(
            install_cmd.split(), capture_output=True, text=True, timeout=120
        )
        if result.returncode != 0:
            print(f"    ⚠️  npx fehlgeschlagen ({result.returncode}): {result.stderr[:300]}")
            return False
        print(f"    ✓ via npx installiert")
        return True
    except FileNotFoundError:
        return False
    except subprocess.TimeoutExpired:
        print(f"    ⚠️  Timeout bei npx")
        return False


def git_clone(dep_name: str, spec: dict) -> bool:
    """Fallback: klont das Repository in external-skills/<domain>/."""
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
            print(f"    ✓ bereits vorhanden: {target} (git pull für Update)")
            subprocess.run(
                ["git", "-C", str(target), "pull"], capture_output=True, text=True, timeout=60
            )
            return True
        result = subprocess.run(
            ["git", "clone", "--depth", "1", url, str(target)],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode != 0:
            print(f"    ⚠️  git clone fehlgeschlagen: {result.stderr[:300]}")
            return False
        print(f"    ✓ geklont nach: {target}")
        return True
    except FileNotFoundError:
        print(f"    ⚠️  git nicht verfügbar")
        return False


def import_dependency(dep_name: str, spec: dict, use_npx: bool = False) -> bool:
    """Importiert eine einzelne Dependency.

    Standard: git clone in .quinsy-studio/external-skills/<domain>/ —
    so bleibt das Studio selbst-enthalten und projektreferenzierbar.
    Optional (--npx): `npx skills add` für lokale Agent-Integration
    (installiert in ~/.claude/skills o.ä., NICHT ins Studio).
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
        print(f"    → Fallback auf git clone")

    if has_git():
        return git_clone(dep_name, spec)

    print(f"    ⚠️  git nicht verfügbar — manueller Import nötig")
    return False


def generate_index(results: dict):
    """Generiert die INDEX.md mit Domain → Team → Skills Zuordnung."""
    EXTERNAL_SKILLS_DIR.mkdir(parents=True, exist_ok=True)
    index_file = EXTERNAL_SKILLS_DIR / "INDEX.md"

    lines = [
        "# External Skills — Index",
        "",
        f"> Generiert: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "> Quelle: `.quinsy-studio/skill-dependencies.json`",
        "",
        "Externe Best-in-Class Skills, die das Studio abonniert. Sie sind IMMER",
        "dem internen `anti_ai_slop_protocol.md` und der Zero-Data-Architecture untergeordnet.",
        "",
        "## Übersicht",
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
        "## Nutzung im Prozess",
        "",
        "1. `./studio update-skills` — alle Dependencies abonnieren/aktualisieren.",
        "2. Der Agent liest die jeweilige SKILL.md des importierten Pakets, bevor er",
        "   die zugehörige Rolle aktiviert (siehe `.quinsy-studio/teams/skill-registry.md`).",
        "3. Konflikte mit internen Regeln entscheidet IMMER das interne Studio-Regelwerk.",
    ]

    index_file.write_text("\n".join(lines))
    print(f"\n  INDEX.md generiert: {index_file}")


def main():
    deps = load_dependencies()
    if not deps:
        print("Keine Dependencies deklariert.")
        return

    if "--list" in sys.argv:
        print("\nDeklarierte Skill-Dependencies:")
        for name, spec in sorted(deps.items()):
            print(f"  [{name}] {spec.get('repo', '?')} → Team {spec.get('team', '?')}")
        print("\nOptionen:")
        print("  --npx   Lokale Agent-Installation via `npx skills add` (nicht ins Studio)")
        print("  <name>  Nur eine Domain importieren")
        return

    # Nur eine Domain, wenn angegeben; --npx für lokale Agent-Installation
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
    print(f"  Ergebnis: {ok_count}/{len(results)} Dependencies importiert")
    print(f"  Nächster Schritt: ./studio update-skills bei neuen Quellen, oder")
    print(f"  Skills manuell in die Team-Skills einarbeiten (.quinsy-studio/teams/).")


if __name__ == "__main__":
    main()
