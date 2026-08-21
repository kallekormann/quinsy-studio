#!/usr/bin/env python3
"""
Studio library manager: pull, promote, list, suggest, reuse tracking.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

STUDIO_ROOT = Path(__file__).parent.parent.parent
STUDIO_LIBRARY = STUDIO_ROOT / ".quinsy-studio" / "studio-library"
PROJECTS_DIR = STUDIO_ROOT / "projects"
REGISTRY_FILE = STUDIO_LIBRARY / "library_registry.json"
MANIFEST_FILE = STUDIO_LIBRARY / "manifest.json"

STUDIO_HEADER = """/**
 * Studio Library — generic reusable artifact.
 * Token values come from studio-library/ui/tokens/; projects override locally.
 */
"""

# Project paths that must never overwrite studio-library (studio-owned generics).
STUDIO_OWNED_BLOCK_PREFIXES = (
    "ui/tokens/",
    "ui/tokens/design-tokens.json",
    "ui/tokens/design-tokens.css",
)


def _slug(name: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return s or "component"


def _load_registry() -> Dict:
    if REGISTRY_FILE.exists():
        return json.loads(REGISTRY_FILE.read_text())
    return {"kinds": {}, "watch_paths": []}


def _load_manifest() -> Dict:
    if MANIFEST_FILE.exists():
        return json.loads(MANIFEST_FILE.read_text())
    return {"assets": [], "schema_version": 2}


def _save_manifest(manifest: Dict) -> None:
    manifest["schema_version"] = 2
    MANIFEST_FILE.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")


def _bump_version(current: str) -> str:
    parts = current.split(".")
    if len(parts) == 3 and all(p.isdigit() for p in parts):
        parts[2] = str(int(parts[2]) + 1)
        return ".".join(parts)
    return "1.0.1"


def _file_hash(path: Path) -> str:
    h = hashlib.md5()
    h.update(path.read_bytes())
    return h.hexdigest()


def _resolve_alias(name: str) -> Optional[Tuple[str, Dict]]:
    """Resolve pull alias to (kind_id, kind_config)."""
    reg = _load_registry()
    name_lower = name.lower().strip()

    for kind_id, cfg in reg.get("kinds", {}).items():
        short = kind_id.replace("package-", "").replace("ui-", "")
        if name_lower == short:
            return kind_id, cfg
        for alias in cfg.get("aliases", []):
            if name_lower == alias.lower():
                return kind_id, cfg

    comp_dir = STUDIO_LIBRARY / "ui" / "components" / _slug(name)
    if comp_dir.exists():
        return "ui-atom", reg["kinds"].get("ui-atom", {})

    page_dir = STUDIO_LIBRARY / "ui" / "page-types" / _slug(name)
    if page_dir.exists():
        return "ui-page-type", reg["kinds"].get("ui-page-type", {})

    return None


def list_library_assets() -> List[Dict]:
    manifest = _load_manifest()
    assets = list(manifest.get("assets", []))
    # Also scan filesystem for unstaged assets
    seen = {a.get("name") for a in assets}
    for pkg in (STUDIO_LIBRARY / "packages").glob("*"):
        if pkg.is_dir() and pkg.name not in seen:
            assets.append({"name": pkg.name, "kind": f"package-{pkg.name}", "path": f"packages/{pkg.name}/", "version": "0.0.0"})
    for comp in (STUDIO_LIBRARY / "ui" / "components").glob("*"):
        if comp.is_dir() and comp.name not in seen:
            assets.append({"name": comp.name, "kind": "ui-component", "path": f"ui/components/{comp.name}/", "version": "0.0.0"})
    return assets


def suggest_assets(query: str) -> List[Dict]:
    q = query.lower()
    tokens = set(re.findall(r"[a-z0-9]+", q))
    results = []
    for asset in list_library_assets():
        hay = " ".join(
            str(asset.get(k, "")) for k in ("name", "kind", "title", "path")
        ).lower()
        score = sum(1 for t in tokens if t in hay)
        if score > 0 or q in hay:
            results.append({**asset, "_score": score})
    results.sort(key=lambda x: x["_score"], reverse=True)
    return results[:10]


def _copy_tree(src: Path, dest: Path, force: bool = False) -> List[str]:
    copied: List[str] = []
    if not src.exists():
        return copied
    if src.is_file():
        if dest.exists() and not force:
            return copied
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        copied.append(str(dest))
        return copied
    for item in src.rglob("*"):
        if item.is_file() and "node_modules" not in item.parts:
            rel = item.relative_to(src)
            target = dest / rel
            if target.exists() and not force:
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)
            copied.append(str(target))
    return copied


def _library_path_for_kind(kind_id: str, cfg: Dict, name: str) -> Path:
    if cfg.get("library_path"):
        return STUDIO_LIBRARY / cfg["library_path"].rstrip("/")
    if cfg.get("library_pattern"):
        return STUDIO_LIBRARY / cfg["library_pattern"].format(slug=_slug(name), name=_slug(name))
    return STUDIO_LIBRARY / name


def _project_path_for_kind(kind_id: str, cfg: Dict, name: str) -> Path:
    if cfg.get("project_path"):
        return Path(cfg["project_path"].rstrip("/"))
    if cfg.get("project_pattern"):
        return Path(cfg["project_pattern"].format(name=_slug(name)))
    if kind_id.startswith("ui-") and kind_id != "ui-page-type" and kind_id != "ui-token":
        level = kind_id.replace("ui-", "")
        return Path(f"ui/components/{level}/{name}.tsx")
    return Path(name)


def pull_assets(project: str, names: List[str], force: bool = False) -> Dict[str, Any]:
    project_dir = PROJECTS_DIR / project
    if not project_dir.exists():
        return {"error": f"Project not found: {project}", "pulled": []}

    pulled: List[Dict] = []
    usage_file = project_dir / "docs" / "library-usage.json"
    usage: Dict = {"pulls": []}
    if usage_file.exists():
        usage = json.loads(usage_file.read_text())

    for name in names:
        resolved = _resolve_alias(name)
        if not resolved:
            pulled.append({"name": name, "status": "not_found"})
            continue
        kind_id, cfg = resolved
        comp_lib = STUDIO_LIBRARY / "ui" / "components" / _slug(name)
        if comp_lib.is_dir() and kind_id.startswith("ui-"):
            dest_dir = project_dir / "ui" / "components" / _slug(name)
            files = _copy_tree(comp_lib, dest_dir, force=force)
            if files:
                entry = {
                    "name": name,
                    "kind": kind_id,
                    "at": datetime.now().isoformat(),
                    "paths": [str(Path(f).relative_to(project_dir)) for f in files],
                }
                usage["pulls"].append(entry)
                pulled.append({**entry, "status": "ok"})
                continue
            if not force and any(dest_dir.iterdir()) if dest_dir.exists() else False:
                pulled.append({"name": name, "kind": kind_id, "status": "skipped_exists"})
                continue

        lib_path = _library_path_for_kind(kind_id, cfg, name)
        proj_rel = _project_path_for_kind(kind_id, cfg, name if kind_id == "ui-page-type" else name)
        if not name.endswith(".tsx") and kind_id in ("ui-atom", "ui-molecule", "ui-organism"):
            comp_lib = STUDIO_LIBRARY / "ui" / "components" / _slug(name)
            if comp_lib.exists():
                lib_path = comp_lib
                level = kind_id.replace("ui-", "")
                proj_rel = Path(f"ui/components/{level}") / f"{name.title().replace('-', '')}.tsx"
                for f in comp_lib.glob("*.tsx"):
                    proj_rel = Path(f"ui/components/{level}") / f.name
                    lib_path = f
                    break

        dest = project_dir / proj_rel
        if kind_id.startswith("package-"):
            dest = project_dir / cfg.get("project_path", f"packages/{name}/").rstrip("/")

        files = _copy_tree(lib_path, dest, force=force)
        if files:
            entry = {
                "name": name,
                "kind": kind_id,
                "at": datetime.now().isoformat(),
                "paths": [str(Path(f).relative_to(project_dir)) for f in files],
            }
            usage["pulls"].append(entry)
            pulled.append({**entry, "status": "ok"})
        else:
            pulled.append({"name": name, "kind": kind_id, "status": "skipped_exists"})

    usage_file.parent.mkdir(parents=True, exist_ok=True)
    usage_file.write_text(json.dumps(usage, indent=2) + "\n")
    return {"project": project, "pulled": pulled}


def _update_manifest_entry(
    name: str,
    kind: str,
    path: str,
    project: str,
    force: bool,
    ticket_id: Optional[str] = None,
) -> str:
    manifest = _load_manifest()
    assets: List[Dict] = manifest.setdefault("assets", [])
    by_name = {a["name"]: a for a in assets}
    version = "1.0.0"
    if name in by_name:
        if not force:
            return by_name[name].get("version", "1.0.0")
        version = _bump_version(by_name[name].get("version", "1.0.0"))
    by_name[name] = {
        "name": name,
        "kind": kind,
        "path": path,
        "version": version,
        "source_project": project,
        "promoted": datetime.now().strftime("%Y-%m-%d"),
        "promoted_at": datetime.now().isoformat(),
        "title": f"{name} (promoted from {project})",
    }
    if ticket_id:
        by_name[name]["ticket_id"] = ticket_id
    manifest["assets"] = list(by_name.values())
    manifest["last_promotion"] = {"project": project, "at": datetime.now().isoformat()}
    _save_manifest(manifest)
    return version


def _log_project_promotion(project: str, paths: List[str], ticket_id: Optional[str], command: str) -> None:
    log_file = PROJECTS_DIR / project / "docs" / "library-promotions.json"
    log: Dict = {"promotions": []}
    if log_file.exists():
        log = json.loads(log_file.read_text())
    log["promotions"].append({
        "paths": paths,
        "ticket_id": ticket_id,
        "command": command,
        "at": datetime.now().isoformat(),
    })
    log_file.parent.mkdir(parents=True, exist_ok=True)
    log_file.write_text(json.dumps(log, indent=2) + "\n")


def promote_path(
    project: str,
    asset_path: str,
    force: bool = False,
    ticket_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Promote a project path to studio-library (packages only — not tokens/UI)."""
    project_dir = PROJECTS_DIR / project
    src = project_dir / asset_path.rstrip("/")
    if not src.exists():
        return {"error": f"Not found: {asset_path}", "promoted": []}

    promoted: List[str] = []
    asset_path_norm = asset_path.rstrip("/")

    if any(asset_path_norm.startswith(p) or asset_path_norm == p.rstrip("/") for p in STUDIO_OWNED_BLOCK_PREFIXES):
        return {
            "error": (
                "Studio library tokens and base UI are studio-owned generics. "
                "Edit .quinsy-studio/studio-library/ directly (LO-* ticket). "
                "Project design stays in projects/<name>/ui/tokens/."
            ),
            "promoted": [],
        }

    if asset_path_norm.startswith("ui/components") or (
        asset_path.endswith(".tsx") and "ui/components" in asset_path
    ):
        return {
            "error": (
                "Project UI components are not promoted to studio-library. "
                "Pull library → adapt in project. Add generic patterns to "
                ".quinsy-studio/studio-library/ui/components/ via studio ticket."
            ),
            "promoted": [],
        }

    if asset_path_norm.startswith("packages/"):
        name = asset_path_norm.split("/")[1]
        kind = (
            f"package-{name}"
            if name
            in (
                "auth",
                "billing",
                "feature-gating",
                "color-extraction",
                "qa-smoke",
                "item-tags",
                "item-search",
                "canvas-export",
            )
            else "package"
        )
        dest = STUDIO_LIBRARY / asset_path_norm
        if dest.exists() and not force:
            return {"error": f"Exists in library (use --force): {asset_path_norm}", "promoted": []}
        _copy_tree(src, dest, force=True)
        ver = _update_manifest_entry(name, kind, asset_path_norm + "/", project, force, ticket_id)
        promoted.append(asset_path_norm)
        _log_project_promotion(project, promoted, ticket_id, f"library promote {asset_path}")
        return {"promoted": promoted, "version": ver}

    if asset_path_norm.startswith("ui/page-types/"):
        name = asset_path_norm.split("/")[2]
        dest = STUDIO_LIBRARY / asset_path_norm
        _copy_tree(src, dest, force=True)
        ver = _update_manifest_entry(name, "ui-page-type", asset_path_norm + "/", project, force, ticket_id)
        promoted.append(asset_path_norm)
        _log_project_promotion(project, promoted, ticket_id, f"library promote {asset_path}")
        return {"promoted": promoted, "version": ver}

    # Fallback: mirror path under library (packages, hooks, lib)
    dest = STUDIO_LIBRARY / asset_path_norm
    if dest.exists() and not force:
        return {"error": f"Exists (use --force): {asset_path_norm}", "promoted": []}
    _copy_tree(src, dest, force=True)
    name = Path(asset_path_norm).name
    ver = _update_manifest_entry(name, "other", asset_path_norm, project, force, ticket_id)
    promoted.append(asset_path_norm)
    _log_project_promotion(project, promoted, ticket_id, f"library promote {asset_path}")
    return {"promoted": promoted, "version": ver}


def _deep_merge(base: Dict, incoming: Dict) -> Dict:
    out = dict(base)
    for key, val in incoming.items():
        if key in out and isinstance(out[key], dict) and isinstance(val, dict):
            out[key] = _deep_merge(out[key], val)
        else:
            out[key] = val
    return out


def promote_design_to_library(project: str, force: bool = False, dry_run: bool = False) -> Dict[str, Any]:
    """
    Gate 2 library sync — validate project design exists; refresh studio sticker catalog.

    Studio library tokens and UI are **studio-owned generics** (Tailwind-default).
    Project gate-2 design (brand tokens, domain components) stays in projects/<name>/ only.
    """
    project_dir = PROJECTS_DIR / project
    result: Dict[str, Any] = {
        "project": project,
        "promoted": [],
        "skipped": [],
        "validated": [],
        "note": "Library tokens/UI are studio-owned; project design is not merged into studio-library.",
    }

    required = [
        project_dir / "ui" / "tokens" / "design-tokens.json",
        project_dir / "design" / "prototype" / "app" / "sticker-sheet" / "page.tsx",
    ]
    for path in required:
        rel = str(path.relative_to(project_dir))
        if path.exists():
            result["validated"].append(rel)
        else:
            result["skipped"].append(f"missing:{rel}")

    if dry_run:
        return result

    if result["skipped"]:
        return result

    # Refresh sticker-sheet catalog from studio library components (not project copies)
    dest_dir = STUDIO_LIBRARY / "ui" / "sticker-sheet"
    dest_dir.mkdir(parents=True, exist_ok=True)
    components = sorted(
        p.parent.name for p in (STUDIO_LIBRARY / "ui" / "components").glob("*/*.tsx")
    )
    catalog = dest_dir / "catalog.md"
    catalog.write_text(
        f"# Studio Library — Sticker Sheet Catalog\n\n"
        f"Updated: {datetime.now().strftime('%Y-%m-%d')}\n"
        f"Gate 2 validated project: `{project}`\n"
        f"**Components listed are studio-owned generics.**\n\n"
        "## Components\n\n"
        + "\n".join(f"- `{c}`" for c in components)
        + "\n"
    )
    result["promoted"].append("ui/sticker-sheet/catalog.md")

    return result


def snapshot_registry_files(project: str) -> Dict[str, str]:
    """Hash all files under registry watch paths."""
    project_dir = PROJECTS_DIR / project
    reg = _load_registry()
    hashes: Dict[str, str] = {}
    for watch in reg.get("watch_paths", []):
        base = project_dir / watch.rstrip("/")
        if not base.exists():
            continue
        if base.is_file():
            hashes[str(base.relative_to(project_dir))] = _file_hash(base)
            continue
        for f in base.rglob("*"):
            if f.is_file() and "node_modules" not in f.parts and ".next" not in f.parts:
                rel = str(f.relative_to(project_dir))
                hashes[rel] = _file_hash(f)
    return hashes


def check_reuse_before_done(project: str, ticket_id: str, snapshot: Dict[str, str]) -> Tuple[bool, List[str]]:
    """
    Return (ok, warnings). ok=False means unpromoted changes detected.
    """
    project_dir = PROJECTS_DIR / project
    current = snapshot_registry_files(project)
    changed = [p for p in current if snapshot.get(p) != current[p]]

    if not changed:
        return True, []

    log_file = project_dir / "docs" / "library-promotions.json"
    promoted_paths: set = set()
    if log_file.exists():
        log = json.loads(log_file.read_text())
        for entry in log.get("promotions", []):
            if entry.get("ticket_id") == ticket_id:
                for p in entry.get("paths", []):
                    promoted_paths.add(p.rstrip("/"))

    warnings = []
    for path in changed:
        covered = any(path.startswith(pp) or pp in path for pp in promoted_paths)
        if not covered:
            warnings.append(path)

    if warnings:
        return False, warnings
    return True, []


def format_library_first_hint(project: str, ticket_title: str) -> str:
    suggestions = suggest_assets(ticket_title)
    if not suggestions:
        return f"Library-first: ./studio library list — check before writing new code."
    names = [s.get("name") for s in suggestions[:5]]
    return (
        f"Library-first: consider ./studio library pull {project} "
        + " ".join(names)
        + " before implementing from scratch."
    )
