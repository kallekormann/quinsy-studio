#!/usr/bin/env python3
"""Security gate checks (agency integration L4, L12).

Static scans of a product tree. They catch the mistakes AI-written Payload and
Next code makes most often (AI-005, PE-003, PE-006):

level 2, hard   secret_scan, client_env_leak, insecure_env_fallback, docker_secret_leak
level 5, hard   payload_access, local_api_override, webhook_signature
warnings        llm_sink, sensitive_log, security_headers

A finding is waived only by a row in `docs/security/exceptions.md`:

    | check | path | reason | expires |
    | local_api_override | src/app/(app)/page.tsx | public marketing list | 2026-12-31 |

An expired row no longer waives anything, and `ship --to main` refuses it.
`.env` files are never opened; only `.env.example` is scanned.
"""

from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Optional, Tuple

SKIP_DIRS = {
    "node_modules", ".next", ".git", "dist", "build", "coverage", "vendor",
    "__pycache__", ".turbo", ".cache", "playwright-report", "test-results",
}
CODE_SUFFIXES = {".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs"}
TEXT_SUFFIXES = CODE_SUFFIXES | {".json", ".yml", ".yaml", ".md", ".py", ".sh", ".toml", ".example", ".txt"}
SKIP_FILES = {"package-lock.json", "pnpm-lock.yaml", "yarn.lock", "payload-types.ts", "importMap.js"}

HARD_LEVEL_2 = ("secret_scan", "client_env_leak", "insecure_env_fallback", "docker_secret_leak")
HARD_LEVEL_5 = ("payload_access", "local_api_override", "webhook_signature")
WARN_CHECKS = ("llm_sink", "sensitive_log", "security_headers")

SECRET_NAME = r"[A-Z0-9_]*(?:SECRET|PASSWORD|TOKEN|API_KEY|PRIVATE_KEY|ACCESS_KEY|SERVICE_ROLE|DATABASE_URL)[A-Z0-9_]*"

TOKEN_PATTERNS: Tuple[Tuple[str, re.Pattern], ...] = (
    ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("Stripe live key", re.compile(r"\b(?:sk|rk)_live_[0-9A-Za-z]{16,}")),
    ("Stripe webhook secret", re.compile(r"\bwhsec_[0-9A-Za-z]{20,}")),
    ("LLM API key", re.compile(r"\bsk-(?:ant-|proj-)?[A-Za-z0-9_-]{24,}")),
    ("GitHub token", re.compile(r"\b(?:ghp_[A-Za-z0-9]{36}|github_pat_[A-Za-z0-9_]{40,})")),
    ("Slack token", re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}")),
    ("Resend key", re.compile(r"\bre_[A-Za-z0-9]{24,}\b")),
    ("private key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
)


# --------------------------------------------------------------------------
# files
# --------------------------------------------------------------------------

def _is_env_file(path: Path) -> bool:
    name = path.name
    return name == ".env" or (name.startswith(".env") and not name.endswith(".example"))


def iter_files(root: Path, suffixes: Optional[Iterable[str]] = None) -> List[Path]:
    wanted = set(suffixes) if suffixes else None
    out: List[Path] = []
    if not root.is_dir():
        return out
    for path in root.rglob("*"):
        if not path.is_file() or any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.name in SKIP_FILES or _is_env_file(path):
            continue
        if wanted is not None:
            suffix = path.suffix.lower() or path.name.lower()
            if suffix not in wanted and not (path.name.startswith("Dockerfile") and "Dockerfile" in wanted):
                continue
        out.append(path)
    return out


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def _rel(root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def _line_of(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def _app_roots(root: Path) -> List[Path]:
    web = root / "apps" / "web"
    return [web] if (web / "package.json").exists() else [root]


# --------------------------------------------------------------------------
# level 2
# --------------------------------------------------------------------------

def secret_scan(root: Path) -> List[str]:
    findings: List[str] = []
    for path in iter_files(root, TEXT_SUFFIXES | {"Dockerfile"}):
        text = _read(path)
        for label, pattern in TOKEN_PATTERNS:
            for match in pattern.finditer(text):
                findings.append(f"{_rel(root, path)}:{_line_of(text, match.start())}: {label} committed in source")
    return findings


_PUBLIC_SECRET = re.compile(rf"\bNEXT_PUBLIC_(?!\w*PUBLISHABLE)(?!\w*SITE_KEY){SECRET_NAME}\b")
_SERVER_ENV = re.compile(r"process\.env\.(?!NEXT_PUBLIC_|NODE_ENV\b)([A-Z][A-Z0-9_]*)")
_USE_CLIENT = re.compile(r"^\s*['\"]use client['\"]", re.M)


def client_env_leak(root: Path) -> List[str]:
    findings: List[str] = []
    for path in iter_files(root, TEXT_SUFFIXES):
        text = _read(path)
        for match in _PUBLIC_SECRET.finditer(text):
            findings.append(
                f"{_rel(root, path)}:{_line_of(text, match.start())}: {match.group(0)} — NEXT_PUBLIC_ ships to every browser"
            )
        if path.suffix in CODE_SUFFIXES and _USE_CLIENT.search(text[:400]):
            for match in _SERVER_ENV.finditer(text):
                findings.append(
                    f"{_rel(root, path)}:{_line_of(text, match.start())}: process.env.{match.group(1)} in a client component"
                )
    return findings


_FALLBACK = re.compile(
    rf"process\.env(?:\.({SECRET_NAME})|\[\s*['\"]({SECRET_NAME})['\"]\s*\])\s*(?:\|\||\?\?)\s*['\"`]"
)


def insecure_env_fallback(root: Path) -> List[str]:
    findings: List[str] = []
    for path in iter_files(root, CODE_SUFFIXES):
        text = _read(path)
        for match in _FALLBACK.finditer(text):
            name = match.group(1) or match.group(2)
            findings.append(
                f"{_rel(root, path)}:{_line_of(text, match.start())}: {name} falls back to a literal; fail fast instead"
            )
    return findings


_DOCKER_SECRET = re.compile(rf"^\s*(ARG|ENV)\s+({SECRET_NAME})\b", re.M)
_COPY_ENV = re.compile(r"^\s*(?:COPY|ADD)\s+[^\n]*\.env(?!\.example)\b", re.M)
_COPY_ALL = re.compile(r"^\s*COPY\s+\.\s+\.", re.M)
_COMPOSE_LITERAL = re.compile(rf"^\s*-?\s*({SECRET_NAME})\s*[:=]\s*['\"]?([^\s'\"#]{{4,}})", re.M)


def _dockerignore_covers_env(folder: Path) -> bool:
    ignore = folder / ".dockerignore"
    if not ignore.exists():
        return False
    lines = {ln.strip() for ln in _read(ignore).splitlines()}
    return bool(lines & {".env", ".env*", "*.env", ".env.*", "**/.env", "**/.env*"})


def docker_secret_leak(root: Path) -> List[str]:
    findings: List[str] = []
    for path in iter_files(root, {"Dockerfile"}):
        if not path.name.startswith("Dockerfile"):
            continue
        text = _read(path)
        rel = _rel(root, path)
        for match in _DOCKER_SECRET.finditer(text):
            findings.append(f"{rel}:{_line_of(text, match.start())}: {match.group(1)} {match.group(2)} bakes a secret into the image")
        for match in _COPY_ENV.finditer(text):
            findings.append(f"{rel}:{_line_of(text, match.start())}: copies an .env file into the image")
        match = _COPY_ALL.search(text)
        if match and not _dockerignore_covers_env(path.parent):
            findings.append(f"{rel}:{_line_of(text, match.start())}: `COPY . .` without a .dockerignore that excludes .env")
    for path in iter_files(root, {".yml", ".yaml"}):
        if "compose" not in path.name:
            continue
        text = _read(path)
        for match in _COMPOSE_LITERAL.finditer(text):
            if "${" in match.group(2):
                continue
            findings.append(
                f"{_rel(root, path)}:{_line_of(text, match.start())}: {match.group(1)} has a literal value; use ${{{match.group(1)}}}"
            )
    return findings


# --------------------------------------------------------------------------
# level 5
# --------------------------------------------------------------------------

_COLLECTION = re.compile(r":\s*CollectionConfig\s*=\s*\{|\bCollectionConfig\b[^\n]*=\s*\{")
_ACCESS_BLOCK = re.compile(r"\baccess\s*:\s*\{")
_OPEN_OP = re.compile(r"\b(create|update|delete)\s*:\s*\(\s*\)\s*=>\s*true\b")


def payload_access(root: Path) -> List[str]:
    findings: List[str] = []
    for base in _app_roots(root):
        for path in iter_files(base, {".ts", ".tsx"}):
            text = _read(path)
            if not _COLLECTION.search(text):
                continue
            rel = _rel(root, path)
            if not _ACCESS_BLOCK.search(text):
                findings.append(f"{rel}: collection has no `access` block (Payload default lets any logged-in user write)")
                continue
            is_auth = bool(re.search(r"^\s*auth\s*:", text, re.M))
            for match in _OPEN_OP.finditer(text):
                op = match.group(1)
                if op == "create" and is_auth:
                    continue
                findings.append(f"{rel}:{_line_of(text, match.start())}: `{op}: () => true` lets anyone {op}")
    return findings


_LOCAL_API = re.compile(r"\bpayload\.(find|findByID|findGlobal|create|update|delete|count|updateGlobal)\s*\(\s*\{")


def _call_args(text: str, start: int) -> str:
    depth, i = 0, start
    while i < len(text):
        ch = text[i]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return text[start: i + 1]
        i += 1
    return text[start:]


def local_api_override(root: Path) -> List[str]:
    """Local API skips access rules unless told otherwise; app code must decide out loud."""
    findings: List[str] = []
    for base in _app_roots(root):
        app = base / "src" / "app"
        for path in iter_files(app, CODE_SUFFIXES):
            if "(payload)" in path.parts:
                continue
            text = _read(path)
            for match in _LOCAL_API.finditer(text):
                args = _call_args(text, match.end() - 1)
                if "overrideAccess" not in args:
                    findings.append(
                        f"{_rel(root, path)}:{_line_of(text, match.start())}: payload.{match.group(1)} without "
                        "`overrideAccess` — pass `user` with `overrideAccess: false`, or `overrideAccess: true` for public data"
                    )
    return findings


_VERIFY = re.compile(r"handleWebhook|constructEvent|timingSafeEqual|verifySignature|webhooks\.verify|\.verify\(")


def webhook_signature(root: Path) -> List[str]:
    findings: List[str] = []
    for base in _app_roots(root):
        for path in iter_files(base / "src", CODE_SUFFIXES):
            if "webhook" not in "/".join(path.parts).lower():
                continue
            if path.stem != "route" and "webhook" not in path.stem.lower():
                continue
            text = _read(path)
            rel = _rel(root, path)
            if not _VERIFY.search(text):
                findings.append(f"{rel}: webhook handler never verifies the signature")
            elif re.search(r"\breq(?:uest)?\.json\(\)", text) and not re.search(r"\.text\(\)", text):
                findings.append(f"{rel}: webhook parses JSON before verifying; read `await req.text()` and verify the raw body")
    return findings


# --------------------------------------------------------------------------
# warnings
# --------------------------------------------------------------------------

_LLM_IMPORT = re.compile(r"from\s+['\"](?:ai|@ai-sdk/[\w-]+|openai|@anthropic-ai/sdk|@google/genai)['\"]")
_SINK = re.compile(r"dangerouslySetInnerHTML|\beval\s*\(|new Function\s*\(|\$queryRawUnsafe|\bsql\.raw\s*\(")


def llm_sink(root: Path) -> List[str]:
    findings: List[str] = []
    for path in iter_files(root, CODE_SUFFIXES):
        text = _read(path)
        if not _LLM_IMPORT.search(text):
            continue
        for match in _SINK.finditer(text):
            findings.append(f"{_rel(root, path)}:{_line_of(text, match.start())}: LLM output may reach `{match.group(0).strip()}` (AI-005)")
    return findings


_LOG_SECRET = re.compile(
    r"\b(?:console\.(?:log|info|warn|error|debug)|logger\.\w+|req\.payload\.logger\.\w+)\s*\([^)\n]*\b(password|token|secret|authorization|cookie|apiKey|api_key)\b",
    re.I,
)


def sensitive_log(root: Path) -> List[str]:
    findings: List[str] = []
    for path in iter_files(root, CODE_SUFFIXES):
        if ".test." in path.name or ".spec." in path.name:
            continue
        text = _read(path)
        for match in _LOG_SECRET.finditer(text):
            findings.append(f"{_rel(root, path)}:{_line_of(text, match.start())}: logs `{match.group(1)}`")
    return findings


REQUIRED_HEADERS = ("Content-Security-Policy", "Strict-Transport-Security", "X-Content-Type-Options", "Referrer-Policy")


def security_headers(root: Path) -> List[str]:
    configs = [p for base in _app_roots(root) for p in base.glob("next.config.*")]
    if not configs:
        return []
    blob = "\n".join(_read(p) for p in configs)
    middleware = "\n".join(_read(p) for base in _app_roots(root) for p in (base / "src").glob("middleware.*"))
    missing = [h for h in REQUIRED_HEADERS if h not in blob and h not in middleware]
    if missing:
        return [f"{_rel(root, configs[0])}: no {', '.join(missing)} header (PE-003)"]
    return []


CHECKS: Dict[str, Callable[[Path], List[str]]] = {
    "secret_scan": secret_scan,
    "client_env_leak": client_env_leak,
    "insecure_env_fallback": insecure_env_fallback,
    "docker_secret_leak": docker_secret_leak,
    "payload_access": payload_access,
    "local_api_override": local_api_override,
    "webhook_signature": webhook_signature,
    "llm_sink": llm_sink,
    "sensitive_log": sensitive_log,
    "security_headers": security_headers,
}


# --------------------------------------------------------------------------
# exceptions
# --------------------------------------------------------------------------

def load_exceptions(root: Path) -> List[Dict[str, str]]:
    path = root / "docs" / "security" / "exceptions.md"
    rows: List[Dict[str, str]] = []
    for line in _read(path).splitlines():
        cells = [c.strip().strip("`") for c in line.strip().strip("|").split("|")]
        if len(cells) < 4 or cells[0].lower() in ("check", "") or set(cells[0]) <= {"-", ":"}:
            continue
        rows.append({"check": cells[0], "path": cells[1], "reason": cells[2], "expires": cells[3]})
    return rows


def _expired(row: Dict[str, str], today: Optional[date] = None) -> bool:
    try:
        return date.fromisoformat(row["expires"]) < (today or date.today())
    except ValueError:
        return True


def expired_exceptions(root: Path, today: Optional[date] = None) -> List[str]:
    return [
        f"{r['check']} {r['path']} expired {r['expires']} ({r['reason']})"
        for r in load_exceptions(root)
        if _expired(r, today)
    ]


def run_check(name: str, root: Path, today: Optional[date] = None) -> List[str]:
    findings = CHECKS[name](root)
    waivers = [r for r in load_exceptions(root) if r["check"] == name and not _expired(r, today)]
    if not waivers:
        return findings
    return [f for f in findings if not any(f.startswith(w["path"]) for w in waivers)]


def main(argv: Optional[List[str]] = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if len(args) < 2 or args[1] not in CHECKS:
        print("Usage: security_checks.py <project_dir> <" + "|".join(CHECKS) + ">")
        return 2
    findings = run_check(args[1], Path(args[0]))
    for line in findings[:40]:
        print(line)
    if len(findings) > 40:
        print(f"… {len(findings) - 40} more")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
