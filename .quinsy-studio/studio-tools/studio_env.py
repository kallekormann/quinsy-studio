"""Docker env inject — named variables from the host secret store after HITL --approve."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence

from studio_isolation import host_secret_dir

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "studio-templates" / "env.schema.json"
INJECT_ACTIONS = frozenset({"up", "migrate", "dev"})
RUNTIME_EXECUTE_KINDS = frozenset({"IMPLEMENT", "GATE", "VERIFY", "DEBUG"})

_SECRET_PATTERNS = (
    re.compile(r"(?i)postgres(?:ql)?://[^\s]+"),
    re.compile(r"(?i)(password|secret|api[_-]?key|token)=[^\s#]{3,}"),
    re.compile(r"sk-[A-Za-z0-9]{12,}"),
    re.compile(r"eyJ[A-Za-z0-9_-]{20,}"),
)


def docker_install_hint() -> str:
    return (
        "  ❌ Docker is required. There is no host fallback that reads .env into this chat.\n"
        "  Install Docker Desktop: https://docs.docker.com/get-docker/\n"
        "  Then: ./studio env <project> up --approve"
    )


def docker_cli_available() -> bool:
    if not shutil.which("docker"):
        return False
    try:
        result = subprocess.run(
            ["docker", "compose", "version"],
            capture_output=True,
            text=True,
            timeout=8,
        )
        return result.returncode == 0
    except (FileNotFoundError, OSError, subprocess.TimeoutExpired):
        return False


def redact_secret_patterns(text: str) -> str:
    out = text or ""
    for pattern in _SECRET_PATTERNS:
        out = pattern.sub("***", out)
    return out


def schema_variable_names(schema_path: Path = SCHEMA_PATH) -> List[str]:
    data = json.loads(schema_path.read_text(encoding="utf-8"))
    return [str(item["name"]) for item in data.get("variables", []) if item.get("name")]


def refuse_without_approve(project: str, action: str) -> str:
    return (
        f"  ❌ `{action}` copies named variables into Docker and needs HITL.\n"
        f"  Run: ./studio env {project} {action} --approve\n"
        f"  Intent: inject schema names from the host secret store into Compose "
        f"(values are never printed)."
    )


def parse_env_assignments(text: str) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, rest = line.partition("=")
        key = key.strip()
        if not key:
            continue
        out[key] = rest.strip().strip("'").strip('"')
    return out


def host_env_path(project: str) -> Path:
    return host_secret_dir(project) / ".env"


def ensure_host_env_file(project: str, names: Optional[Sequence[str]] = None) -> Path:
    """Create the host store with empty values for missing names. Never prints values."""
    dest = host_env_path(project)
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        os.chmod(dest.parent, 0o700)
    except OSError:
        pass
    existing = parse_env_assignments(dest.read_text(encoding="utf-8")) if dest.exists() else {}
    keys = list(names or schema_variable_names())
    lines = [
        "# Host secret store — not in the git workspace. Names only in env.schema.json.",
        f"# Project: {project}",
    ]
    for key in keys:
        value = existing.get(key, "")
        lines.append(f"{key}={value}")
    extra = [k for k in existing if k not in keys]
    for key in extra:
        lines.append(f"{key}={existing[key]}")
    dest.write_text("\n".join(lines) + "\n", encoding="utf-8")
    try:
        os.chmod(dest, 0o600)
    except OSError:
        pass
    return dest


def secret_values_for_redaction(assignments: Dict[str, str]) -> List[str]:
    values = []
    for key, value in assignments.items():
        if not value or len(value) < 3:
            continue
        if key.endswith("_PORT") or key in {"NODE_ENV", "PROJECT_NAME"}:
            continue
        values.append(value)
    values.sort(key=len, reverse=True)
    return values


def redact_output(text: str, values: Iterable[str]) -> str:
    out = text or ""
    for value in values:
        if value and value in out:
            out = out.replace(value, "***")
    return redact_secret_patterns(out)


def compose_argv(
    project: str,
    docker_dir: Path,
    compose_file: Path,
    host_env: Path,
    compose_args: Sequence[str],
) -> List[str]:
    return [
        "docker",
        "compose",
        "-p",
        project,
        "--project-directory",
        str(docker_dir),
        "-f",
        str(compose_file),
        "--env-file",
        str(host_env),
        *compose_args,
    ]


def public_command_line(argv: Sequence[str]) -> str:
    """Join argv; never expand env-file contents."""
    return " ".join(str(part) for part in argv)


def inject_summary(project: str, names: Sequence[str], host_env: Path) -> str:
    listed = ", ".join(names) if names else "(none)"
    return (
        f"  ✓ HITL approve: injecting {len(names)} named variable(s) into Compose for {project}\n"
        f"  Names: {listed}\n"
        f"  Store: {host_env} (values not printed)"
    )


def missing_required_secrets(assignments: Dict[str, str], names: Sequence[str]) -> List[str]:
    required = [n for n in names if "PASSWORD" in n or n in {"DATABASE_URL", "APP_KEY"}]
    return [n for n in required if not (assignments.get(n) or "").strip()]
