#!/usr/bin/env python3
"""Production operations from the agent seat (LO-0402, LO-0403, LO-0404).

The agent runs readiness, deploy, logs, status, db and cleanup itself. Human stops are
`migrate --prod --approve` and every destructive step. Values stay in
`projects/<p>/.env.local`; this module reads **names** from the schema and passes the file
to `ssh`/`curl` through the environment. No value is printed or returned to the chat.
Every action appends one line to `projects/<p>/docs/ops/ops-log.md`.
"""

from __future__ import annotations

import json
import os
import re
import shlex
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

from studio_env import SCHEMA_PATH, parse_env_assignments, redact_output, secret_values_for_redaction

PROD_GROUP = "prod"
PROD_ENV_FILE = ".env.local"
DESTRUCTIVE_OPS = frozenset({"cleanup --prune-volumes", "db --reset", "db --drop"})
HITL_OPS = frozenset({"migrate --prod"}) | DESTRUCTIVE_OPS

_DATA_SERVICE = re.compile(r"^(db|postgres|redis|valkey|pgbouncer|minio|mongo|mysql)$", re.I)


# ----------------------------------------------------------------------------- schema


def prod_variables(schema_path: Path = SCHEMA_PATH, product_schema: Optional[Path] = None) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for path in (schema_path, product_schema):
        if not path or not path.is_file():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        for item in data.get("variables", []):
            if item.get("group") == PROD_GROUP and item.get("name"):
                rows.append({"name": str(item["name"]), "purpose": str(item.get("purpose", "")), "where": str(item.get("where", PROD_ENV_FILE))})
    return rows


def prod_names(**kw) -> List[str]:
    return [row["name"] for row in prod_variables(**kw)]


def explain_prod_env(project: str, project_root: Path) -> str:
    """Human-facing text: which names, where to put them, what each is for. No values."""
    rows = prod_variables(product_schema=project_root / "env.schema.json")
    present = prod_env_present(project_root)
    lines = [
        f"Production access for {project} — names only, values never enter the chat.",
        f"File: projects/{project}/{PROD_ENV_FILE} (gitignored). Add one line per name: NAME=value",
        "",
    ]
    for row in rows:
        mark = "set" if present.get(row["name"]) else "missing"
        lines.append(f"  {row['name']:<20} [{mark}]  {row['purpose']}")
    lines += [
        "",
        "What the agent does with them:",
        "  SSH (VPS_SSH_*)          ./studio ops <p> status | db | cleanup — compose ps, psql over ssh, docker prune",
        "  Coolify (COOLIFY_*)      ./studio ops <p> deploy | logs — trigger a deployment, tail application logs",
        "  PROD_DATABASE_URL        ./studio ops <p> migrate --prod --approve — the only prod step that waits for you",
        "",
        "Rotate a value: edit the line, nothing else changes. Remove access: delete the line.",
    ]
    return "\n".join(lines)


def prod_env_present(project_root: Path) -> Dict[str, bool]:
    """Which prod names have a non-empty value. Values are not returned."""
    path = project_root / PROD_ENV_FILE
    if not path.is_file():
        return {}
    assignments = parse_env_assignments(path.read_text(encoding="utf-8"))
    return {k: bool(v) for k, v in assignments.items()}


def missing_prod_names(project_root: Path, needed: Sequence[str]) -> List[str]:
    present = prod_env_present(project_root)
    return [n for n in needed if not present.get(n)]


def ensure_prod_env_file(project: str, project_root: Path) -> Path:
    """Create or extend .env.local with every prod name (empty), never touching set values."""
    dest = project_root / PROD_ENV_FILE
    names = prod_names(product_schema=project_root / "env.schema.json")
    existing = parse_env_assignments(dest.read_text(encoding="utf-8")) if dest.is_file() else {}
    missing = [n for n in names if n not in existing]
    if not dest.is_file():
        header = [
            f"# Production access for {project}. Gitignored. Names from env.schema.json group `prod`.",
            "# `./studio env <project> prod --explain` describes each name. Values never enter the chat.",
        ]
        dest.write_text("\n".join(header + [f"{n}=" for n in names]) + "\n", encoding="utf-8")
    elif missing:
        text = dest.read_text(encoding="utf-8")
        prefix = "" if text.endswith("\n") or not text else "\n"
        dest.write_text(text + prefix + "".join(f"{n}=\n" for n in missing), encoding="utf-8")
    try:
        os.chmod(dest, 0o600)
    except OSError:
        pass
    return dest


# ----------------------------------------------------------------------------- readiness


def _compose_text(project_root: Path, name: str) -> str:
    path = project_root / "docker" / name
    return path.read_text(encoding="utf-8", errors="ignore") if path.is_file() else ""


def _service_blocks(text: str) -> Dict[str, str]:
    """Very small YAML slicer: top-level `services:` children → their indented block."""
    blocks: Dict[str, str] = {}
    in_services = False
    current = None
    buf: List[str] = []
    for line in text.splitlines():
        if re.match(r"^services:\s*$", line):
            in_services = True
            continue
        if in_services and re.match(r"^\S", line):
            if current:
                blocks[current] = "\n".join(buf)
            in_services = False
            current = None
            buf = []
            continue
        if in_services:
            m = re.match(r"^  (\w[\w-]*):\s*$", line)
            if m:
                if current:
                    blocks[current] = "\n".join(buf)
                current = m.group(1)
                buf = []
            elif current:
                buf.append(line)
    if current:
        blocks[current] = "\n".join(buf)
    return blocks


def readiness_findings(project_root: Path) -> List[Tuple[str, str]]:
    """(PASS|FAIL, line) pairs. Any FAIL blocks `ship --to main`."""
    out: List[Tuple[str, str]] = []
    base = _compose_text(project_root, "docker-compose.yml")
    prod = _compose_text(project_root, "compose.prod.yml")

    def row(ok: bool, text: str) -> None:
        out.append(("PASS" if ok else "FAIL", text))

    row(bool(base), "docker/docker-compose.yml exists")
    row(bool(prod), "docker/compose.prod.yml exists (./studio env <p> init copies it)")
    if not prod:
        return out
    prod_blocks = _service_blocks(prod)
    base_blocks = _service_blocks(base)
    for name, block in base_blocks.items():
        if not _DATA_SERVICE.match(name):
            continue
        publishes = bool(re.search(r"^\s*ports:\s*\n\s*-\s", block, re.M))
        reset = "ports: !reset" in prod_blocks.get(name, "") or "ports: []" in prod_blocks.get(name, "")
        row(not publishes or reset, f"{name}: no data port published in production")
    for name, block in prod_blocks.items():
        row("restart:" in block, f"{name}: restart policy set")
        row("logging" in block, f"{name}: bounded logging")
    app = prod_blocks.get("app", "")
    if app or "app" in base_blocks:
        row("npm run dev" not in app and "build:" in app or "image:" in app, "app: built image, not a dev server")
        row("NODE_ENV: production" in app, "app: NODE_ENV=production")
        row("migrate" in app, "app: migrate runs before start")
        row("healthcheck" in app, "app: healthcheck declared")
        dockerfile = project_root / "apps" / "web" / "Dockerfile"
        row(dockerfile.is_file(), "apps/web/Dockerfile exists")
    row((project_root / "docs" / "ops" / "incident-runbook.md").is_file(), "docs/ops/incident-runbook.md exists (PE-007)")
    row((project_root / "env.schema.json").is_file() or True, "env.schema.json names (product file optional)")
    return out


def readiness_blockers(project_root: Path) -> List[str]:
    return [f"readiness FAIL: {line}" for state, line in readiness_findings(project_root) if state == "FAIL"]


def readiness_report(project: str, project_root: Path) -> str:
    rows = readiness_findings(project_root)
    fails = sum(1 for s, _ in rows if s == "FAIL")
    lines = [f"Production readiness — {project}", ""]
    lines += [f"  {state:<4} {text}" for state, text in rows]
    lines += ["", f"  {len(rows) - fails} PASS / {fails} FAIL", ""]
    lines.append("  ship --to main: " + ("allowed" if not fails else "refused until every FAIL is fixed"))
    return "\n".join(lines)


# ----------------------------------------------------------------------------- runners


def ops_log_path(project_root: Path) -> Path:
    return project_root / "docs" / "ops" / "ops-log.md"


def append_ops_log(project_root: Path, action: str, result: str, note: str = "") -> Path:
    path = ops_log_path(project_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.is_file():
        path.write_text("# Ops log\n\nOne line per `./studio ops` run. Values are never written here.\n\n", encoding="utf-8")
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    with path.open("a", encoding="utf-8") as fh:
        fh.write(f"- {stamp} `{action}` → {result}{(' — ' + note) if note else ''}\n")
    return path


def op_needs_approve(action: str, flags: Sequence[str]) -> bool:
    key = " ".join([action] + [f for f in flags if f in ("--prod", "--prune-volumes", "--reset", "--drop")])
    return key in HITL_OPS


def refuse_without_approve(project: str, action: str, flags: Sequence[str]) -> str:
    cmd = " ".join(["./studio ops", project, action] + list(flags) + ["--approve"])
    kind = "destructive" if any(f in flags for f in ("--prune-volumes", "--reset", "--drop")) else "production migration"
    return (
        f"  ❌ `{action} {' '.join(flags)}` is a {kind} step and waits for the human.\n"
        f"  Run: {cmd}\n"
        "  Everything else under `./studio ops` runs without a signature and is logged in docs/ops/ops-log.md."
    )


def _load_prod_env(project_root: Path) -> Dict[str, str]:
    path = project_root / PROD_ENV_FILE
    if not path.is_file():
        return {}
    return parse_env_assignments(path.read_text(encoding="utf-8"))


def _run(argv: Sequence[str], env: Dict[str, str], timeout: int = 600) -> Tuple[int, str]:
    full_env = dict(os.environ)
    full_env.update(env)
    try:
        proc = subprocess.run(list(argv), capture_output=True, text=True, env=full_env, timeout=timeout)
    except FileNotFoundError:
        return 127, f"{argv[0]} not found on this machine"
    except subprocess.TimeoutExpired:
        return 124, "timed out"
    return proc.returncode, redact_output((proc.stdout or "") + (proc.stderr or ""), secret_values_for_redaction(env))


def ssh_argv(env: Dict[str, str], remote: str) -> List[str]:
    """ssh command; key path and host come from env (names, resolved by the shell, not printed)."""
    return [
        "ssh",
        "-o", "BatchMode=yes",
        "-o", "StrictHostKeyChecking=accept-new",
        "-i", env["VPS_SSH_KEY_PATH"],
        f"{env['VPS_SSH_USER']}@{env['VPS_SSH_HOST']}",
        remote,
    ]


def coolify_argv(env: Dict[str, str], path: str, method: str = "GET") -> List[str]:
    return [
        "curl", "-sS", "-X", method,
        "-H", "Authorization: Bearer " + env["COOLIFY_TOKEN"],
        "-H", "Accept: application/json",
        env["COOLIFY_URL"].rstrip("/") + path,
    ]


OP_NEEDS: Dict[str, Tuple[str, ...]] = {
    "deploy": ("COOLIFY_URL", "COOLIFY_TOKEN", "COOLIFY_APP_UUID"),
    "logs": ("COOLIFY_URL", "COOLIFY_TOKEN", "COOLIFY_APP_UUID"),
    "status": ("VPS_SSH_HOST", "VPS_SSH_USER", "VPS_SSH_KEY_PATH", "VPS_COMPOSE_DIR"),
    "migrate": ("VPS_SSH_HOST", "VPS_SSH_USER", "VPS_SSH_KEY_PATH", "VPS_COMPOSE_DIR"),
    "db": ("VPS_SSH_HOST", "VPS_SSH_USER", "VPS_SSH_KEY_PATH", "VPS_COMPOSE_DIR"),
    "cleanup": ("VPS_SSH_HOST", "VPS_SSH_USER", "VPS_SSH_KEY_PATH"),
}


def run_op(project: str, project_root: Path, action: str, flags: Sequence[str], approve: bool = False, dry_run: bool = False) -> Tuple[bool, str]:
    """Returns (ok, text). text is already redacted. Logs the attempt."""
    flags = list(flags)
    if action == "readiness":
        report = readiness_report(project, project_root)
        fails = len(readiness_blockers(project_root))
        append_ops_log(project_root, "readiness", f"{'PASS' if not fails else f'{fails} FAIL'}")
        return fails == 0, report
    if action not in OP_NEEDS:
        return False, f"  unknown ops action `{action}`. Use readiness|deploy|logs|status|migrate|db|cleanup"
    if op_needs_approve(action, flags) and not approve:
        return False, refuse_without_approve(project, action, flags)
    missing = missing_prod_names(project_root, OP_NEEDS[action])
    if missing:
        ensure_prod_env_file(project, project_root)
        return False, (
            f"  ❌ {action} needs {', '.join(missing)} in projects/{project}/{PROD_ENV_FILE}.\n"
            f"  `./studio env {project} prod --explain` describes each name. The file was extended with empty lines."
        )
    env = _load_prod_env(project_root)
    compose = f"cd {shlex.quote(env.get('VPS_COMPOSE_DIR', '.'))} && docker compose -f docker-compose.yml -f compose.prod.yml"
    if action == "deploy":
        argv = coolify_argv(env, f"/api/v1/deploy?uuid={env['COOLIFY_APP_UUID']}&force=false")
    elif action == "logs":
        lines = next((f.split("=", 1)[1] for f in flags if f.startswith("--lines=")), "200")
        argv = coolify_argv(env, f"/api/v1/applications/{env['COOLIFY_APP_UUID']}/logs?lines={lines}")
    elif action == "status":
        argv = ssh_argv(env, f"{compose} ps && df -h / && free -m 2>/dev/null || true")
    elif action == "migrate":
        if "--prod" not in flags:
            return False, "  migrate here is production only: ./studio ops <p> migrate --prod --approve (local: ./studio env <p> migrate)"
        argv = ssh_argv(env, f"{compose} run --rm app npm run migrate")
    elif action == "db":
        if "--reset" in flags or "--drop" in flags:
            argv = ssh_argv(env, f"{compose} down -v db")
        else:
            sql = next((f.split("=", 1)[1] for f in flags if f.startswith("--sql=")), r"\dt")
            argv = ssh_argv(env, f"{compose} exec -T db psql -U \"$POSTGRES_USER\" \"$POSTGRES_DB\" -c {shlex.quote(sql)}")
    else:  # cleanup
        prune = "docker system prune -af" + (" --volumes" if "--prune-volumes" in flags else "")
        argv = ssh_argv(env, f"{prune} && docker image prune -af")
    label = " ".join([action] + flags)
    if dry_run:
        shown = redact_output(" ".join(argv), secret_values_for_redaction(env))
        append_ops_log(project_root, label, "dry-run")
        return True, f"  dry-run: {shown}"
    code, text = _run(argv, env)
    append_ops_log(project_root, label, "ok" if code == 0 else f"exit {code}", "approved" if approve else "")
    return code == 0, text.strip()
