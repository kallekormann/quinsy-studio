#!/usr/bin/env python3
"""Payload is the default web server. Gate 1 records in or out. Execute scaffolds apps/web."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable, List, Tuple

STUDIO = Path(__file__).resolve().parent.parent
TEMPLATES = STUDIO / "studio-templates" / "payload"
SKILL_DIR = STUDIO / "teams" / "02-backend-systems" / "skills" / "payload"
CMS_SKILL_DIR = STUDIO / "teams" / "02-backend-systems" / "skills" / "cms-migration"
SKILL_FILE = SKILL_DIR / "SKILL.md"
SKILL_SOURCE = "https://github.com/payloadcms/skills"
_RAW = "https://raw.githubusercontent.com/payloadcms/skills/main/skills"
_PAYLOAD_FILES = (
    "SKILL.md",
    "README.md",
    "reference/ACCESS-CONTROL-ADVANCED.md",
    "reference/ACCESS-CONTROL.md",
    "reference/ADAPTERS.md",
    "reference/ADVANCED.md",
    "reference/COLLECTIONS.md",
    "reference/ENDPOINTS.md",
    "reference/FIELD-TYPE-GUARDS.md",
    "reference/FIELDS.md",
    "reference/HOOKS.md",
    "reference/PLUGIN-DEVELOPMENT.md",
    "reference/QUERIES.md",
)
_CMS_FILES = (
    "SKILL.md",
    "reference/PAYLOAD-FIELD-REFERENCE.md",
)
PROJECTS = STUDIO.parent / "projects"

WEB_ARCHETYPES = {
    "saas-application",
    "ecommerce",
    "content-platform",
    "marketplace",
    "internal-tool",
    "prototype",
    "mobile-app",
}

SECOND_CONTENT_I18N = ("next-intl", "i18next", "react-intl")


def project_root(project: str) -> Path:
    return PROJECTS / project


def blueprint_text(project: str) -> str:
    path = project_root(project) / "docs" / "architecture" / "BLUEPRINT.md"
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def payload_choice(text: str) -> str:
    """in, out, or missing. The blueprint line is `Payload: in` or `Payload: out`."""
    match = re.search(r"(?im)^payload:\s*(in|out)\b", text or "")
    if not match:
        return "missing"
    return match.group(1).lower()


def opt_out_adr(root: Path) -> bool:
    adr = root / "docs" / "adr"
    if not adr.exists():
        return False
    for path in adr.glob("ADR-*.md"):
        body = path.read_text(encoding="utf-8", errors="ignore").lower()
        if "payload" in body and ("opt out" in body or "opt-out" in body or "without payload" in body):
            return True
    return False


def archetype_of(root: Path) -> str:
    status = root / "status.json"
    if not status.exists():
        return "saas-application"
    import json

    try:
        return str(json.loads(status.read_text(encoding="utf-8")).get("archetype") or "saas-application")
    except json.JSONDecodeError:
        return "saas-application"


def gate_1_payload_issues(project: str) -> List[str]:
    root = project_root(project)
    text = blueprint_text(project)
    choice = payload_choice(text)
    issues: List[str] = []
    if archetype_of(root) in WEB_ARCHETYPES and choice == "missing":
        issues.append(
            "BLUEPRINT.md must say `Payload: in` or `Payload: out`. "
            "Out requires an ADR that opts out of Payload."
        )
    if choice == "out" and not opt_out_adr(root):
        issues.append("Payload: out needs docs/adr/ADR-*.md that says opt out of Payload.")
    if choice == "in":
        lowered = text.lower()
        if any(token in lowered for token in SECOND_CONTENT_I18N):
            issues.append(
                "Content translations use Payload localization. Remove the second i18n package from the blueprint."
            )
        if not re.search(r"(?im)^locales:\s*\S+", text):
            issues.append("BLUEPRINT.md needs `Locales:` (one default, or a list with a fallback).")
    return issues


def payload_is_in(project: str) -> bool:
    return payload_choice(blueprint_text(project)) == "in"


def app_ready(project: str) -> bool:
    return (project_root(project) / "apps" / "web" / "package.json").exists()


def scaffold_needed(project: str) -> bool:
    root = project_root(project)
    status_path = root / "status.json"
    if not status_path.exists():
        return False
    import json

    try:
        status = json.loads(status_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False
    gate = ((status.get("human_gates") or {}).get("1") or {}).get("status")
    return gate == "approved" and payload_is_in(project) and not app_ready(project)


def _copy_tree(src: Path, dest: Path, project: str) -> List[Path]:
    created: List[Path] = []
    for path in src.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(src)
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            continue
        body = path.read_text(encoding="utf-8")
        body = body.replace("{{PROJECT}}", project)
        target.write_text(body, encoding="utf-8")
        created.append(target)
    return created


def scaffold_payload_app(project: str) -> List[Path]:
    """Write apps/web and the Compose override. Skip files that already exist."""
    if not TEMPLATES.exists():
        raise FileNotFoundError(f"Missing Payload template: {TEMPLATES}")
    root = project_root(project)
    created = _copy_tree(TEMPLATES / "app", root / "apps" / "web", project)
    override = root / "docker" / "payload-app.compose.yml"
    override.parent.mkdir(parents=True, exist_ok=True)
    if not override.exists():
        body = (TEMPLATES / "payload-app.compose.yml").read_text(encoding="utf-8")
        override.write_text(body.replace("{{PROJECT}}", project), encoding="utf-8")
        created.append(override)
    worker = root / "apps" / "worker" / "worker.py"
    if not worker.exists():
        worker.parent.mkdir(parents=True, exist_ok=True)
        worker.write_text((TEMPLATES / "worker.py").read_text(encoding="utf-8"), encoding="utf-8")
        created.append(worker)
    return created


def profiles_from_blueprint(text: str, extra: Iterable[str] = ()) -> List[str]:
    """Compose profiles named on the `Profiles:` line, plus any CLI extras."""
    allowed = {"redis", "pooler", "minio", "rag"}
    found: List[str] = []
    match = re.search(r"(?im)^profiles:\s*(.+)$", text or "")
    raw = match.group(1) if match else ""
    for part in re.split(r"[, ]+", raw):
        name = part.strip().lower()
        if name in allowed and name not in found:
            found.append(name)
    for name in extra:
        cleaned = name.strip().lower()
        if cleaned in allowed and cleaned not in found:
            found.append(cleaned)
    if "rag" in found and "redis" not in found:
        found.append("redis")
    return found


def compose_extras(project: str, extra_profiles: Iterable[str] = ()) -> Tuple[List[Path], List[str]]:
    root = project_root(project)
    files: List[Path] = []
    override = root / "docker" / "payload-app.compose.yml"
    if override.exists():
        files.append(override)
    return files, profiles_from_blueprint(blueprint_text(project), extra_profiles)


def skill_present() -> bool:
    cms = CMS_SKILL_DIR / "SKILL.md"
    if not SKILL_FILE.exists() or not cms.exists():
        return False
    payload = SKILL_FILE.read_text(encoding="utf-8").lower()
    migration = cms.read_text(encoding="utf-8").lower()
    return "collections" in payload and "wordpress" in migration


def refresh_payload_skills() -> Tuple[bool, str]:
    """Replace the vendored Payload skills with the current files from payloadcms/skills."""
    import urllib.request

    pairs = [(f"{_RAW}/payload/{name}", SKILL_DIR / name) for name in _PAYLOAD_FILES]
    pairs += [(f"{_RAW}/cms-migration/{name}", CMS_SKILL_DIR / name) for name in _CMS_FILES]
    try:
        for url, dest in pairs:
            dest.parent.mkdir(parents=True, exist_ok=True)
            with urllib.request.urlopen(url, timeout=30) as response:
                dest.write_bytes(response.read())
    except Exception as exc:
        return False, str(exc)
    if not skill_present():
        return False, "downloaded files did not contain the expected Payload skill text"
    return True, SKILL_SOURCE


def cms_migration_ticket(text: str) -> bool:
    """The CMS skill is for moving content in from another CMS, not for schema migrate."""
    return bool(
        re.search(
            r"wordpress|contentful|strapi|sanity|webflow|cms[- ]migration|migrate content",
            text or "",
            re.I,
        )
    )


def augment_card_skills(project: str, ticket_text: str, skills: List[str]) -> List[str]:
    if not payload_is_in(project):
        return list(skills or [])
    head = ["BE-007"]
    if cms_migration_ticket(ticket_text):
        head.append("cms-migration")
    rest = [skill for skill in (skills or []) if skill not in head]
    return (head + rest)[:8]


def receipt_payload_issues(project: str, receipt: str, ticket: str) -> List[str]:
    if not payload_is_in(project):
        return []
    blob = f"{receipt}\n{ticket}".lower()
    issues: List[str] = []
    if "supabase auth" in blob or "clerk" in blob:
        issues.append("Payload project: do not add a second auth system")
    if "prisma" in blob:
        issues.append("Payload project: do not add a second ORM")
    if any(token in blob for token in SECOND_CONTENT_I18N):
        issues.append("Payload project: content translations stay in Payload localization")
    if "collection" in ticket.lower() and "access" not in receipt.lower():
        issues.append("Payload collection ticket: receipt must name the access rule")
    concepts = ("access", "collection", "local api", "hook", "locale", "job", "rest", "graphql")
    server_ticket = any(
        word in ticket.lower() for word in ("payload", "collection", "auth", "locale", "upload")
    )
    if server_ticket and not any(concept in receipt.lower() for concept in concepts):
        issues.append("Payload ticket: receipt must name the Payload concept it used")
    return issues
