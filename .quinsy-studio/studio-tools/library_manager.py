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
 * Studio Library — base artifact (functional + neutral defaults).
 * Promoted from a project; adapt in projects via local config/tokens.
 */
"""


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
        if comp_lib.exists() and kind_id.startswith("ui-"):
            for f in comp_lib.glob("*.tsx"):
                dest = project_dir / "ui" / "components" / "atoms" / f.name
                if dest.exists() and not force:
                    continue
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, dest)
                entry = {
                    "name": name,
                    "kind": "ui-atom",
                    "at": datetime.now().isoformat(),
                    "paths": [str(dest.relative_to(project_dir))],
                }
                usage["pulls"].append(entry)
                pulled.append({**entry, "status": "ok"})
            if pulled and pulled[-1].get("name") == name:
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
    """Promote a project path to studio-library."""
    project_dir = PROJECTS_DIR / project
    src = project_dir / asset_path.rstrip("/")
    if not src.exists():
        return {"error": f"Not found: {asset_path}", "promoted": []}

    promoted: List[str] = []
    asset_path_norm = asset_path.rstrip("/")

    if asset_path_norm.startswith("packages/"):
        name = asset_path_norm.split("/")[1]
        kind = f"package-{name}" if name in ("auth", "billing", "feature-gating") else "package"
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

    if asset_path.endswith(".tsx") and "ui/components" in asset_path:
        f = src if src.is_file() else None
        if not f:
            return {"error": "Expected .tsx file", "promoted": []}
        slug = _slug(f.stem)
        dest_dir = STUDIO_LIBRARY / "ui" / "components" / slug
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_file = dest_dir / f.name
        content = f.read_text(encoding="utf-8")
        if "Studio Library" not in content:
            content = STUDIO_HEADER + content
        dest_file.write_text(content)
        level = "ui-atom"
        if "/molecules/" in asset_path:
            level = "ui-molecule"
        elif "/organisms/" in asset_path:
            level = "ui-organism"
        ver = _update_manifest_entry(slug, level, f"ui/components/{slug}/", project, force, ticket_id)
        promoted.append(str(dest_file.relative_to(STUDIO_LIBRARY)))
        _log_project_promotion(project, [asset_path], ticket_id, f"library promote {asset_path}")
        return {"promoted": promoted, "version": ver}

    # Fallback: mirror path under library
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
    """Gate 2 design promotion: tokens, atomic UI, page-types, sticker sheet."""
    project_dir = PROJECTS_DIR / project
    result: Dict[str, Any] = {"project": project, "promoted": [], "skipped": []}

    checks = [
        project_dir / "ui" / "tokens" / "design-tokens.json",
        project_dir / "design" / "prototype" / "app" / "sticker-sheet" / "page.tsx",
    ]
    if dry_run:
        for c in checks:
            (result["promoted"] if c.exists() else result["skipped"]).append(
                str(c.relative_to(project_dir)) if c.exists() else str(c.relative_to(project_dir))
            )
        return result

    # Tokens
    tok_src = project_dir / "ui" / "tokens" / "design-tokens.json"
    if tok_src.exists():
        dest = STUDIO_LIBRARY / "ui" / "tokens" / "design-tokens.json"
        dest.parent.mkdir(parents=True, exist_ok=True)
        incoming = json.loads(tok_src.read_text())
        if dest.exists() and not force:
            merged = _deep_merge(json.loads(dest.read_text()), incoming)
        else:
            merged = incoming if not dest.exists() else _deep_merge(json.loads(dest.read_text()), incoming)
        dest.write_text(json.dumps(merged, indent=2) + "\n")
        _update_manifest_entry("design-tokens", "ui-token", "ui/tokens/design-tokens.json", project, force)
        result["promoted"].append("ui/tokens/design-tokens.json")

    # Atomic components
    for level, kind in [("atoms", "ui-atom"), ("molecules", "ui-molecule"), ("organisms", "ui-organism")]:
        src_dir = project_dir / "ui" / "components" / level
        if not src_dir.exists():
            continue
        for f in src_dir.glob("*.tsx"):
            slug = _slug(f.stem)
            dest_dir = STUDIO_LIBRARY / "ui" / "components" / slug
            dest_dir.mkdir(parents=True, exist_ok=True)
            dest_file = dest_dir / f.name
            if dest_file.exists() and not force:
                result["skipped"].append(str(f.relative_to(project_dir)))
                continue
            content = f.read_text(encoding="utf-8")
            if "Studio Library" not in content:
                content = STUDIO_HEADER + content
            dest_file.write_text(content)
            _update_manifest_entry(slug, kind, f"ui/components/{slug}/", project, force)
            result["promoted"].append(f"ui/components/{slug}/{f.name}")

    # Page types
    page_types = project_dir / "ui" / "page-types"
    if page_types.exists():
        for pt_dir in page_types.iterdir():
            if not pt_dir.is_dir():
                continue
            dest = STUDIO_LIBRARY / "ui" / "page-types" / pt_dir.name
            if dest.exists() and not force:
                result["skipped"].append(f"ui/page-types/{pt_dir.name}/")
                continue
            _copy_tree(pt_dir, dest, force=True)
            _update_manifest_entry(pt_dir.name, "ui-page-type", f"ui/page-types/{pt_dir.name}/", project, force)
            result["promoted"].append(f"ui/page-types/{pt_dir.name}/")

    # Sticker sheet
    sticker_src = project_dir / "design" / "prototype" / "app" / "sticker-sheet" / "page.tsx"
    if sticker_src.exists():
        dest_dir = STUDIO_LIBRARY / "ui" / "sticker-sheet"
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_page = dest_dir / "page.tsx"
        content = sticker_src.read_text(encoding="utf-8")
        if "Studio Library" not in content:
            content = STUDIO_HEADER + content
        dest_page.write_text(content)
        components = sorted(p.parent.name for p in (STUDIO_LIBRARY / "ui" / "components").glob("*/*.tsx"))
        catalog = dest_dir / "catalog.md"
        catalog.write_text(
            f"# Studio Library — Sticker Sheet Catalog\n\n"
            f"Updated: {datetime.now().strftime('%Y-%m-%d')}\n"
            f"Source project: `{project}`\n\n"
            "## Components\n\n"
            + "\n".join(f"- `{c}`" for c in components)
            + "\n"
        )
        _update_manifest_entry("sticker-sheet", "sticker-sheet", "ui/sticker-sheet/", project, force)
        result["promoted"].extend(["ui/sticker-sheet/page.tsx", "ui/sticker-sheet/catalog.md"])

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
