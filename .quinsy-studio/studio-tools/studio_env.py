"""Docker env inject — named variables from projects/<p>/.env after HITL --approve."""

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


def merged_schema_names(project: str, projects_dir: Path) -> List[str]:
    names = schema_variable_names()
    product = projects_dir / project / "env.schema.json"
    if product.is_file():
        names = list(dict.fromkeys(names + schema_variable_names(product)))
    return names


def inform_local_inject(project: str, action: str) -> str:
    """Local Docker inject is agent-run (LO-0403). One INFORM line; `--approve` is accepted as a no-op."""
    return (
        f"  ℹ️  INFORM: `{action}` injects schema names from projects/{project}/.env into the local Compose stack "
        f"(values are never printed). No signature needed; production steps live under `./studio ops`."
    )


def refuse_without_approve(project: str, action: str) -> str:
    """Kept for callers that still print the old HITL hint; local inject no longer refuses."""
    return (
        f"  ℹ️  `{action}` runs without a signature since LO-0403. The old form still works:\n"
        f"  ./studio env {project} {action} --approve"
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


def project_env_path(project: str, projects_dir: Path) -> Path:
    return projects_dir / project / ".env"


def example_assignments(project: str, projects_dir: Path) -> Dict[str, str]:
    """Non-secret defaults from committed examples. The product example wins on a shared name."""
    root = projects_dir / project
    merged: Dict[str, str] = {}
    for rel in ("docker/.env.example", ".env.example"):
        path = root / rel
        if path.is_file():
            merged.update(parse_env_assignments(path.read_text(encoding="utf-8")))
    return merged


def host_env_path(project: str) -> Path:
    return host_secret_dir(project) / ".env"


def ensure_project_env_file(
    project: str,
    projects_dir: Path,
    names: Optional[Sequence[str]] = None,
) -> Path:
    """Create or extend projects/<p>/.env. Never prints values and never rewrites a value already set."""
    dest = project_env_path(project, projects_dir)
    dest.parent.mkdir(parents=True, exist_ok=True)
    keys = list(dict.fromkeys(list(names or schema_variable_names())))
    examples = example_assignments(project, projects_dir)
    if dest.exists():
        existing = parse_env_assignments(dest.read_text(encoding="utf-8"))
        missing = [key for key in list(dict.fromkeys(keys + list(examples))) if key not in existing]
        if missing:
            text = dest.read_text(encoding="utf-8")
            extra = "".join(f"{key}={examples.get(key, '')}\n" for key in missing)
            prefix = "" if text.endswith("\n") or not text else "\n"
            dest.write_text(text + prefix + extra, encoding="utf-8")
    else:
        ordered = list(dict.fromkeys(keys + list(examples)))
        lines = [
            "# Local Docker Desktop. Gitignored. Names in env.schema.json. Production: Coolify.",
            f"# Project: {project}",
        ]
        lines.extend(f"{key}={examples.get(key, '')}" for key in ordered)
        dest.write_text("\n".join(lines) + "\n", encoding="utf-8")
    try:
        os.chmod(dest, 0o600)
    except OSError:
        pass
    return dest


def ensure_host_env_file(project: str, names: Optional[Sequence[str]] = None) -> Path:
    """Backward name. Desktop store is the project .env; path is unused by cmd_env."""
    dest = host_env_path(project)
    dest.parent.mkdir(parents=True, exist_ok=True)
    existing = parse_env_assignments(dest.read_text(encoding="utf-8")) if dest.exists() else {}
    keys = list(names or schema_variable_names())
    lines = [
        "# Unused when projects/<p>/.env exists. Kept for older tests.",
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
    extra_files: Sequence[Path] = (),
    profiles: Sequence[str] = (),
) -> List[str]:
    cmd = [
        "docker",
        "compose",
        "-p",
        project,
        "--project-directory",
        str(docker_dir),
        "-f",
        str(compose_file),
    ]
    for extra in extra_files:
        cmd.extend(["-f", str(extra)])
    for profile in profiles:
        cmd.extend(["--profile", profile])
    cmd.extend(["--env-file", str(host_env), *compose_args])
    return cmd


def public_command_line(argv: Sequence[str]) -> str:
    """Join argv; never expand env-file contents."""
    return " ".join(str(part) for part in argv)


def inject_summary(project: str, names: Sequence[str], host_env: Path) -> str:
    listed = ", ".join(names) if names else "(none)"
    return (
        f"  ✓ HITL approve: injecting {len(names)} named variable(s) into Compose for {project}\n"
        f"  Names: {listed}\n"
        f"  File: {host_env} (values not printed)"
    )


def missing_required_secrets(assignments: Dict[str, str], names: Sequence[str]) -> List[str]:
    required = [n for n in names if "PASSWORD" in n or n in {"DATABASE_URL", "APP_KEY"}]
    return [n for n in required if not (assignments.get(n) or "").strip()]
