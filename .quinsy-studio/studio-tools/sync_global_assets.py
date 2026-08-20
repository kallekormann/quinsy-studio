#!/usr/bin/env python3
"""
sync_global_assets.py — Global Asset Synchronization für Quinsy Studio

Scannt Projektcode auf generische, wiederverwendbare Logik und extrahiert
diese in die globale Studio-Library.

Verwendung:
  python3 sync_global_assets.py <project> [--dry-run]
  python3 sync_global_assets.py nudge
  python3 sync_global_assets.py nudge --dry-run

Output:
  studio-library/ui/components/    — UI-Komponenten
  studio-library/packages/         — Backend-Packages/Services
  studio-library/ui/tokens/        — Design Tokens
"""

import sys
import os
import json
import re
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# =============================================================================
# CONFIGURATION
# =============================================================================

STUDIO_ROOT = Path(__file__).parent.parent.parent
PROJECTS_DIR = STUDIO_ROOT / "projects"
STUDIO_LIBRARY = STUDIO_ROOT / ".quinsy-studio" / "studio-library"

# Pattern für wiederverwendbare Dateien
REUSABLE_PATTERNS = {
    "ui_component": [
        r'components?/[a-z]+/[A-Z]\w+\.tsx$',
        r'ui/[a-z]+/[A-Z]\w+\.tsx$',
    ],
    "ui_hook": [
        r'hooks?/use[A-Z]\w+\.ts$',
        r'hooks?/use[A-Z]\w+\.tsx$',
    ],
    "ui_utility": [
        r'utils?/[a-z]+\.ts$',
        r'lib/[a-z]+\.ts$',
    ],
    "design_token": [
        r'tokens?/design-tokens\.(json|css)$',
        r'theme/[a-z]+\.(ts|js)$',
    ],
    "api_service": [
        r'services?/[a-z]+\.ts$',
        r'api/[a-z]+\.ts$',
    ],
    "database_migration": [
        r'migrations?/\d+_[a-z]+\.sql$',
        r'schema/[a-z]+\.sql$',
    ],
}

# Dateien die NICHT extrahiert werden
EXCLUDE_PATTERNS = [
    r'node_modules',
    r'\.next',
    r'dist',
    r'build',
    r'\.git',
    r'test/',
    r'__tests__/',
    r'\.test\.',
    r'\.spec\.',
    r'package-lock\.json',
]

# =============================================================================
# SCANNING
# =============================================================================

def should_exclude(filepath: str) -> bool:
    """Prüft ob eine Datei ausgeschlossen werden soll."""
    for pattern in EXCLUDE_PATTERNS:
        if re.search(pattern, filepath):
            return True
    return False


def classify_file(filepath: Path) -> Optional[str]:
    """Klassifiziert eine Datei nach Typ."""
    rel_path = str(filepath)
    
    for asset_type, patterns in REUSABLE_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, rel_path):
                return asset_type
    
    return None


def analyze_reusability(filepath: Path, project_dir: Path) -> Dict:
    """Analysiert ob eine Datei wiederverwendbar ist."""
    
    try:
        content = filepath.read_text(encoding='utf-8')
    except (UnicodeDecodeError, PermissionError):
        return {"reusable": False, "reason": "Kann nicht gelesen werden"}
    
    # Heuristiken für Wiederverwendbarkeit
    score = 0
    reasons = []
    
    # 1. Komplexe Logik (viele Imports, Exports)
    imports = len(re.findall(r'^import\s', content, re.MULTILINE))
    exports = len(re.findall(r'^export\s', content, re.MULTILINE))
    
    if imports > 3 and exports > 1:
        score += 2
        reasons.append(f"Mehrere Imports ({imports}) und Exports ({exports})")
    
    # 2. Komponente mit Props
    if re.search(r'interface\s+\w+Props', content):
        score += 3
        reasons.append("Hat definierte Props-Schnittstelle")
    
    # 3. Hook mit generischer Logik
    if re.search(r'^export\s+(?:function|const)\s+use[A-Z]', content, re.MULTILINE):
        score += 2
        reasons.append("Generischer Hook")
    
    # 4. Keine projektspezifischen Referenzen
    project_name = project_dir.name
    if project_name.lower() not in content.lower():
        score += 1
        reasons.append("Keine projektspezifischen Referenzen")
    
    # 5. Keine hardcoded URLs oder Konfiguration
    if not re.search(r'https?://(?!api\.|cdn\.)', content):
        score += 1
        reasons.append("Keine hardcoded URLs")
    
    # 6. Dokumentation vorhanden
    if re.search(r'(?:/\*\*|///|^\s*\*)', content):
        score += 1
        reasons.append("Dokumentation vorhanden")
    
    # Threshold: Score >= 3意味着 wiederverwendbar
    return {
        "reusable": score >= 3,
        "score": score,
        "reasons": reasons,
        "size": len(content),
        "lines": content.count('\n') + 1
    }


def scan_project_for_assets(project: str) -> Dict:
    """Scannt ein Projekt auf wiederverwendbare Assets."""
    
    project_dir = PROJECTS_DIR / project
    if not project_dir.exists():
        print(f"Fehler: Projekt nicht gefunden: {project_dir}")
        sys.exit(1)
    
    assets = {
        "ui_components": [],
        "ui_hooks": [],
        "ui_utilities": [],
        "design_tokens": [],
        "api_services": [],
        "other": []
    }
    
    scanned_files = 0
    reusable_files = 0
    
    for filepath in project_dir.rglob('*'):
        if not filepath.is_file():
            continue
        if should_exclude(str(filepath)):
            continue
        
        scanned_files += 1
        asset_type = classify_file(filepath)
        
        if asset_type:
            analysis = analyze_reusability(filepath, project_dir)
            
            if analysis["reusable"]:
                reusable_files += 1
                
                asset_info = {
                    "path": str(filepath.relative_to(project_dir)),
                    "type": asset_type,
                    "analysis": analysis
                }
                
                if asset_type.startswith("ui_"):
                    if "component" in asset_type:
                        assets["ui_components"].append(asset_info)
                    elif "hook" in asset_type:
                        assets["ui_hooks"].append(asset_info)
                    else:
                        assets["ui_utilities"].append(asset_info)
                elif asset_type == "design_token":
                    assets["design_tokens"].append(asset_info)
                elif asset_type == "api_service":
                    assets["api_services"].append(asset_info)
                else:
                    assets["other"].append(asset_info)
    
    return {
        "project": project,
        "scanned_files": scanned_files,
        "reusable_files": reusable_files,
        "assets": assets
    }

# =============================================================================
# EXTRACTION
# =============================================================================

def extract_assets(project: str, scan_result: Dict, dry_run: bool = False):
    """Extrahiert gefundene Assets in die Studio-Library."""
    
    project_dir = PROJECTS_DIR / project
    extracted_count = 0
    
    for category, asset_list in scan_result["assets"].items():
        for asset in asset_list:
            source_path = project_dir / asset["path"]
            
            # Determine destination
            if asset["type"] == "ui_component":
                dest_dir = STUDIO_LIBRARY / "ui" / "components"
            elif asset["type"] == "ui_hook":
                dest_dir = STUDIO_LIBRARY / "ui" / "hooks"
            elif asset["type"] == "ui_utility":
                dest_dir = STUDIO_LIBRARY / "ui" / "utilities"
            elif asset["type"] == "design_token":
                dest_dir = STUDIO_LIBRARY / "ui" / "tokens"
            elif asset["type"] == "api_service":
                dest_dir = STUDIO_LIBRARY / "packages"
            else:
                dest_dir = STUDIO_LIBRARY / "other"
            
            # Create destination directory
            dest_path = dest_dir / source_path.name
            
            if dry_run:
                print(f"  [DRY-RUN] Würde extrahieren: {asset['path']} → {dest_path.relative_to(STUDIO_ROOT)}")
            else:
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source_path, dest_path)
                print(f"  Extrahiert: {asset['path']} → {dest_path.relative_to(STUDIO_ROOT)}")
            
            extracted_count += 1
    
    return extracted_count

# =============================================================================
# MANIFEST UPDATE
# =============================================================================

def update_manifest(project: str, scan_result: Dict, extracted_count: int):
    """Aktualisiert das Studio-Library Manifest."""
    
    manifest_file = STUDIO_LIBRARY / "manifest.json"
    
    if manifest_file.exists():
        manifest = json.loads(manifest_file.read_text())
    else:
        manifest = {"assets": [], "last_sync": None}
    
    # Add extracted assets
    for category, asset_list in scan_result["assets"].items():
        for asset in asset_list:
            # Check if already exists
            existing = [a for a in manifest["assets"] 
                       if a.get("source_path") == asset["path"]]
            
            if not existing:
                manifest["assets"].append({
                    "name": Path(asset["path"]).stem,
                    "kind": asset["type"],
                    "source_project": project,
                    "source_path": asset["path"],
                    "promoted": datetime.now().strftime("%Y-%m-%d"),
                    "reusability_score": asset["analysis"]["score"],
                    "title": f"{Path(asset['path']).stem} (promoted from {project})"
                })
    
    manifest["last_sync"] = datetime.now().isoformat()
    manifest["last_project"] = project
    
    manifest_file.write_text(json.dumps(manifest, indent=2, ensure_ascii=False))

# =============================================================================
# REPORTING
# =============================================================================

def print_report(scan_result: Dict, extracted_count: int, dry_run: bool):
    """Gibt den Sync-Report aus."""
    
    print(f"\n{'='*60}")
    print(f"  GLOBAL ASSET SYNC: {scan_result['project']}")
    print(f"{'='*60}")
    print(f"\n  Dateien gescannt:      {scan_result['scanned_files']}")
    print(f"  Wiederverwendbar:      {scan_result['reusable_files']}")
    print(f"  Extrahiert:            {extracted_count}")
    
    # Breakdown by type
    print(f"\n  {'='*50}")
    print(f"  ASSETS NACH TYP")
    print(f"  {'='*50}")
    
    for category, asset_list in scan_result["assets"].items():
        if asset_list:
            print(f"\n  {category}: {len(asset_list)}")
            for asset in asset_list[:5]:
                print(f"    - {asset['path']} (Score: {asset['analysis']['score']})")
    
    if dry_run:
        print(f"\n  ℹ️  DRY-RUN Modus — keine Dateien wurden kopiert.")
    
    print()

# =============================================================================
# MAIN
# =============================================================================

def main():
    if len(sys.argv) < 2:
        print("Verwendung:")
        print("  python3 sync_global_assets.py <project> [--dry-run]")
        sys.exit(1)
    
    project = sys.argv[1]
    dry_run = "--dry-run" in sys.argv
    
    # Scan project
    print(f"\n  Scanne {project} auf wiederverwendbare Assets...")
    scan_result = scan_project_for_assets(project)
    
    # Extract assets
    if scan_result["reusable_files"] > 0:
        print(f"\n  Extrahiere {scan_result['reusable_files']} Assets...")
        extracted_count = extract_assets(project, scan_result, dry_run)
        
        # Update manifest
        if not dry_run:
            update_manifest(project, scan_result, extracted_count)
    else:
        extracted_count = 0
        print(f"\n  Keine wiederverwendbaren Assets gefunden.")
    
    # Print report
    print_report(scan_result, extracted_count, dry_run)


if __name__ == "__main__":
    main()
