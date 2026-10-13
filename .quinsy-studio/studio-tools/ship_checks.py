#!/usr/bin/env python3
"""Checks before `./studio ship <p> --to main --approve` (agency integration L12).

- no secret token anywhere in git history (a deleted secret is still leaked)
- docs/security/secrets-inventory.md names every secret in env.schema.json / .env.example (PE-006)
- docs/ops/incident-runbook.md exists (PE-007)
- no expired row in docs/security/exceptions.md
- no database or cache port published on all interfaces in a Compose file

Values are never read: env names come from the schema and examples only.
"""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import List, Optional, Set

from security_checks import SECRET_NAME, TOKEN_PATTERNS, expired_exceptions

_DATA_IMAGE = re.compile(r"\b(postgres|pgvector|redis|valkey|mongo|mysql|mariadb|minio|pgbouncer|elasticsearch)\b", re.I)
_PORT = re.compile(r"^\s*-\s*['\"]?([^'\"\s]+)['\"]?\s*$")
_SECRET_ENV = re.compile(rf"^\s*({SECRET_NAME})\s*=", re.M)


def history_secret_findings(git_dir: Path) -> List[str]:
    try:
        result = subprocess.run(
            ["git", "-C", str(git_dir), "log", "--all", "-p", "--no-color", "--format=commit %h"],
            capture_output=True, text=True, timeout=120,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return [f"git history scan did not run: {exc}"]
    findings: List[str] = []
    commit = "?"
    for line in (result.stdout or "").splitlines():
        if line.startswith("commit "):
            commit = line.split(" ", 1)[1]
            continue
        if not line.startswith("+") or line.startswith("+++"):
            continue
        for label, pattern in TOKEN_PATTERNS:
            if pattern.search(line):
                findings.append(f"{label} added in commit {commit} — rotate it, then rewrite history or accept the leak in writing")
    return sorted(set(findings))


def secret_env_names(root: Path) -> Set[str]:
    names: Set[str] = set()
    for schema in (root / "env.schema.json", root / "docs" / "env.schema.json"):
        if schema.exists():
            try:
                data = json.loads(schema.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                continue
            props = data.get("properties") if isinstance(data, dict) else None
            keys = props.keys() if isinstance(props, dict) else (data.keys() if isinstance(data, dict) else [])
            names |= {k for k in keys if re.fullmatch(SECRET_NAME, k)}
    for example in list(root.glob("*.env.example")) + list(root.glob(".env.example")) + list(root.glob("docker/.env.example")):
        names |= set(_SECRET_ENV.findall(example.read_text(encoding="utf-8", errors="ignore")))
    return names


def inventory_issues(root: Path) -> List[str]:
    inventory = root / "docs" / "security" / "secrets-inventory.md"
    if not inventory.exists():
        return ["docs/security/secrets-inventory.md missing (PE-006)"]
    text = inventory.read_text(encoding="utf-8", errors="ignore")
    missing = sorted(n for n in secret_env_names(root) if n not in text)
    if missing:
        return ["secrets inventory lacks: " + ", ".join(missing)]
    return []


def published_data_ports(root: Path) -> List[str]:
    findings: List[str] = []
    for path in list(root.glob("*compose*.y*ml")) + list(root.glob("docker/*compose*.y*ml")):
        service, image, in_ports = "", "", False
        for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            if re.match(r"^  [\w.-]+:\s*$", raw):
                service, image, in_ports = raw.strip().rstrip(":"), "", False
                continue
            stripped = raw.strip()
            if stripped.startswith("image:"):
                image = stripped
            if re.match(r"^\s{4}ports:\s*$", raw):
                in_ports = True
                continue
            if in_ports and not stripped.startswith("-"):
                in_ports = False
            if in_ports:
                match = _PORT.match(raw)
                if not match:
                    continue
                mapping = match.group(1)
                data_service = _DATA_IMAGE.search(image) or _DATA_IMAGE.search(service)
                if data_service and mapping.count(":") >= 1 and not mapping.startswith(("127.0.0.1:", "localhost:")):
                    findings.append(f"{path.relative_to(root)}: {service} publishes {mapping} on all interfaces; bind 127.0.0.1 or drop the port")
    return findings


def pre_ship_main_issues(root: Path, git_dir: Optional[Path] = None) -> List[str]:
    issues: List[str] = []
    issues.extend(history_secret_findings(git_dir or root))
    issues.extend(inventory_issues(root))
    if not (root / "docs" / "ops" / "incident-runbook.md").exists():
        issues.append("docs/ops/incident-runbook.md missing (PE-007: contacts, severity, restore steps, breach clock)")
    issues.extend(f"security exception {row}" for row in expired_exceptions(root))
    issues.extend(published_data_ports(root))
    return issues
