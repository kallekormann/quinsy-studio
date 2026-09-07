"""Studio policy file: runtime hint + per-step estimated token budgets.

Tokens are chars/4 of what execute/CARD tells the agent to load — not host billing.
No API keys. Local yaml overlays committed defaults.
"""

from __future__ import annotations

import json
import re
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

TOOLS_DIR = Path(__file__).parent
QUINSY_STUDIO = TOOLS_DIR.parent
SETTINGS_PATH = QUINSY_STUDIO / "studio.settings.yaml"
LOCAL_SETTINGS_PATH = QUINSY_STUDIO / "studio.settings.local.yaml"
USAGE_PATH = QUINSY_STUDIO / ".session-usage.json"
EXAMPLE_LOCAL = QUINSY_STUDIO / "studio-templates" / "studio.settings.local.example.yaml"

STEP_NAMES = (
    "intake",
    "architecture",
    "design",
    "planning",
    "scoping",
    "implement",
    "review",
    "reuse",
    "learning",
    "retro",
)

STANDARD_STEPS = {
    "intake": {"context": 24000, "budget": 200000},
    "architecture": {"context": 32000, "budget": 250000},
    "design": {"context": 40000, "budget": 400000},
    "planning": {"context": 16000, "budget": 80000},
    "scoping": {"context": 12000, "budget": 60000},
    "implement": {"context": 16000, "budget": 400000},
    "review": {"context": 16000, "budget": 80000},
    "reuse": {"context": 12000, "budget": 40000},
    "learning": {"context": 12000, "budget": 60000},
    "retro": {"context": 12000, "budget": 40000},
}

PROFILE_MULTIPLIER = {"economy": 0.5, "standard": 1.0, "premium": 2.0}
DEFAULT_SESSION_BUDGET = 1_500_000
DEFAULT_WARN_PCT = 80

SECRET_KEY_RE = re.compile(
    r"(api[_-]?key|secret|password|anthropic_key|openai_key|gemini_api)",
    re.I,
)


def estimate_tokens(text: str) -> int:
    chars = len(text or "")
    if chars <= 0:
        return 0
    return max(1, chars // 4)


def parse_yaml_scalar(raw: str) -> Any:
    text = raw.strip()
    if not text or text in ("~", "null", "Null"):
        return None
    if text in ("true", "True", "yes"):
        return True
    if text in ("false", "False", "no"):
        return False
    if (text.startswith('"') and text.endswith('"')) or (text.startswith("'") and text.endswith("'")):
        return text[1:-1]
    try:
        if "." in text:
            return float(text)
        return int(text)
    except ValueError:
        return text


def parse_simple_yaml(text: str) -> Dict[str, Any]:
    """Indent-based map parser for studio.settings.yaml (no lists required)."""
    rows: List[Tuple[int, str]] = []
    for raw in text.splitlines():
        stripped = raw.split("#", 1)[0].rstrip()
        if not stripped.strip():
            continue
        indent = len(stripped) - len(stripped.lstrip(" "))
        rows.append((indent, stripped.strip()))

    def parse_block(index: int, min_indent: int) -> Tuple[Dict[str, Any], int]:
        result: Dict[str, Any] = {}
        block_indent: Optional[int] = None
        while index < len(rows):
            indent, content = rows[index]
            if indent < min_indent:
                break
            if block_indent is None:
                block_indent = indent
            if indent != block_indent:
                break
            if ":" not in content:
                index += 1
                continue
            key, _, rest = content.partition(":")
            key = key.strip()
            rest = rest.strip()
            if rest:
                result[key] = parse_yaml_scalar(rest)
                index += 1
            else:
                child, index = parse_block(index + 1, indent + 1)
                result[key] = child
        return result, index

    data, _ = parse_block(0, 0)
    return data


def _reject_secrets(node: Any, path: str = "") -> None:
    if isinstance(node, dict):
        for key, value in node.items():
            here = f"{path}.{key}" if path else str(key)
            if SECRET_KEY_RE.search(str(key)):
                raise ValueError(f"Refusing secret-like key '{here}' — keys stay in the host, not studio settings")
            if isinstance(value, str) and SECRET_KEY_RE.search(value) and len(value) > 20:
                raise ValueError(f"Refusing secret-like value at '{here}'")
            _reject_secrets(value, here)
    elif isinstance(node, list):
        for i, item in enumerate(node):
            _reject_secrets(item, f"{path}[{i}]")


def deep_merge(base: Dict[str, Any], overlay: Dict[str, Any]) -> Dict[str, Any]:
    out = deepcopy(base)
    for key, value in (overlay or {}).items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = deep_merge(out[key], value)
        else:
            out[key] = deepcopy(value)
    return out


def _scale_steps(steps: Dict[str, Dict[str, int]], multiplier: float) -> Dict[str, Dict[str, int]]:
    scaled: Dict[str, Dict[str, int]] = {}
    for name, pair in steps.items():
        scaled[name] = {
            "context": max(1, int(round(int(pair.get("context") or 0) * multiplier))),
            "budget": max(1, int(round(int(pair.get("budget") or 0) * multiplier))),
        }
    return scaled


def builtin_defaults() -> Dict[str, Any]:
    return {
        "runtime": "cursor",
        "cost": {
            "profile": "standard",
            "model_hint": "",
            "estimate": "chars_div_4",
            "warn_at_pct": DEFAULT_WARN_PCT,
            "session_token_budget": DEFAULT_SESSION_BUDGET,
            "max_files_open_on_implement": 12,
            "never_dump_backlog": True,
            "load_full_ticket_only_on": "IMPLEMENT",
            "max_qa_retries": 3,
            "train_parallel": True,
            "steps": deepcopy(STANDARD_STEPS),
        },
    }


def _load_yaml_file(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    data = parse_simple_yaml(path.read_text(encoding="utf-8"))
    _reject_secrets(data)
    return data if isinstance(data, dict) else {}


def load_settings(
    *,
    committed: Optional[Path] = None,
    local: Optional[Path] = None,
) -> Dict[str, Any]:
    """Merge builtin → committed yaml → profile scale → local yaml (explicit keys win)."""
    committed = committed or SETTINGS_PATH
    local = local or LOCAL_SETTINGS_PATH
    base = builtin_defaults()
    committed_data = _load_yaml_file(committed)
    merged = deep_merge(base, committed_data)
    local_data = _load_yaml_file(local)

    profile = str(
        ((local_data.get("cost") or {}).get("profile"))
        or ((merged.get("cost") or {}).get("profile"))
        or "standard"
    ).lower()
    if profile not in PROFILE_MULTIPLIER:
        profile = "standard"
    multiplier = PROFILE_MULTIPLIER[profile]
    cost = merged.setdefault("cost", {})
    cost["profile"] = profile
    if multiplier != 1.0:
        cost["steps"] = _scale_steps(cost.get("steps") or STANDARD_STEPS, multiplier)
        cost["session_token_budget"] = max(
            1, int(round(int(cost.get("session_token_budget") or DEFAULT_SESSION_BUDGET) * multiplier))
        )
        files = int(cost.get("max_files_open_on_implement") or 12)
        cost["max_files_open_on_implement"] = max(4, int(round(files * multiplier)))

    merged = deep_merge(merged, local_data)
    merged["cost"]["profile"] = profile
    steps = merged["cost"].setdefault("steps", {})
    for name in STEP_NAMES:
        if name not in steps:
            steps[name] = deepcopy(STANDARD_STEPS[name])
            if multiplier != 1.0 and name not in ((local_data.get("cost") or {}).get("steps") or {}):
                steps[name] = _scale_steps({name: STANDARD_STEPS[name]}, multiplier)[name]
    return merged


def step_limits(settings: Optional[Dict[str, Any]], step: str) -> Dict[str, int]:
    cost = (settings or load_settings()).get("cost") or {}
    name = step if step in STEP_NAMES else "implement"
    pair = (cost.get("steps") or {}).get(name) or STANDARD_STEPS["implement"]
    return {
        "context": int(pair.get("context") or STANDARD_STEPS["implement"]["context"]),
        "budget": int(pair.get("budget") or STANDARD_STEPS["implement"]["budget"]),
    }


def session_budget(settings: Optional[Dict[str, Any]] = None) -> int:
    cost = (settings or load_settings()).get("cost") or {}
    return int(cost.get("session_token_budget") or DEFAULT_SESSION_BUDGET)


def warn_at_pct(settings: Optional[Dict[str, Any]] = None) -> int:
    cost = (settings or load_settings()).get("cost") or {}
    try:
        return int(cost.get("warn_at_pct") or DEFAULT_WARN_PCT)
    except (TypeError, ValueError):
        return DEFAULT_WARN_PCT


def load_usage(path: Optional[Path] = None) -> Dict[str, Any]:
    target = path or USAGE_PATH
    if not target.exists():
        return {"project": "", "started_at": "", "session": 0, "steps": {}}
    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"project": "", "started_at": "", "session": 0, "steps": {}}
    data.setdefault("project", "")
    data.setdefault("session", 0)
    data.setdefault("steps", {})
    data.setdefault("started_at", "")
    return data


def save_usage(data: Dict[str, Any], path: Optional[Path] = None) -> None:
    target = path or USAGE_PATH
    target.write_text(json.dumps(data, indent=2), encoding="utf-8")


def reset_usage(project: str = "", path: Optional[Path] = None) -> Dict[str, Any]:
    data = {
        "project": project,
        "started_at": datetime.now().isoformat(timespec="seconds"),
        "session": 0,
        "steps": {},
    }
    save_usage(data, path)
    return data


def add_usage(step: str, tokens: int, project: str = "", path: Optional[Path] = None) -> Dict[str, Any]:
    data = load_usage(path)
    if project and data.get("project") and data.get("project") != project:
        data = reset_usage(project, path)
    elif project and not data.get("project"):
        data["project"] = project
        if not data.get("started_at"):
            data["started_at"] = datetime.now().isoformat(timespec="seconds")
    name = step if step in STEP_NAMES else "implement"
    add = max(0, int(tokens))
    data["session"] = int(data.get("session") or 0) + add
    steps = data.setdefault("steps", {})
    steps[name] = int(steps.get(name) or 0) + add
    save_usage(data, path)
    return data


def resolve_cost_step(kind: str, command: str = "", reason: str = "", read: str = "") -> str:
    blob = f"{kind} {command} {reason} {read}".lower()
    if kind == "STUDIO_LO" or "studio train" in blob or "idle infusion" in blob:
        return "learning"
    if "approve-design" in blob:
        return "implement"
    if "./studio design" in blob or "design track" in blob or "design of what exists" in blob or "stills/mocks" in blob:
        return "design"
    if "blueprint" in blob or "--gate 1" in blob:
        return "architecture"
    if "as-built" in blob or "--gate 0" in blob or "prd" in blob or "bootstrap" in blob:
        return "intake"
    if "approve-scope" in blob or "proposes scope" in blob or "./studio sprint" in blob:
        return "planning"
    if "groom" in blob:
        return "scoping"
    if "./studio review" in blob or "sprint review" in blob:
        return "review"
    if "./studio reuse" in blob or "reuse is inform" in blob:
        return "reuse"
    if "./studio retro" in blob or "fill project retro" in blob:
        return "retro"
    return "implement"


def estimate_turn_tokens(project: str, card: Optional[Dict[str, Any]], read: Optional[str]) -> int:
    chunks: List[str] = []
    if card:
        chunks.append(json.dumps(card, ensure_ascii=True))
        project_root = QUINSY_STUDIO.parent / "projects" / project
        for rel in (card.get("files") or [])[:12]:
            path = Path(rel)
            if not path.is_absolute():
                path = project_root / rel
            if path.is_file():
                try:
                    chunks.append(path.read_text(encoding="utf-8", errors="ignore")[:80_000])
                except OSError:
                    pass
    if read:
        path = Path(read)
        if not path.is_absolute():
            alt = QUINSY_STUDIO.parent / "projects" / project / read
            path = alt if alt.exists() else path
        if path.is_file():
            try:
                chunks.append(path.read_text(encoding="utf-8", errors="ignore")[:120_000])
            except OSError:
                pass
        elif path.is_dir():
            chunks.append("dir:" + str(path))
    total = estimate_tokens("\n".join(chunks))
    return total if total > 0 else 400


def _pct(used: int, limit: int) -> float:
    if limit <= 0:
        return 100.0
    return (used / limit) * 100.0


def cost_snapshot(
    *,
    step: str,
    turn: int,
    usage: Dict[str, Any],
    settings: Dict[str, Any],
) -> Dict[str, Any]:
    limits = step_limits(settings, step)
    session_used = int(usage.get("session") or 0)
    step_used = int((usage.get("steps") or {}).get(step) or 0)
    sess_lim = session_budget(settings)
    warn = warn_at_pct(settings)
    profile = str((settings.get("cost") or {}).get("profile") or "standard")
    hints = []
    if _pct(turn, limits["context"]) >= warn:
        hints.append(f"{step} context at {int(_pct(turn, limits['context']))}%")
    if _pct(step_used, limits["budget"]) >= warn:
        hints.append(f"{step} budget at {int(_pct(step_used, limits['budget']))}%")
    if _pct(session_used, sess_lim) >= warn:
        hints.append(f"session budget at {int(_pct(session_used, sess_lim))}%")
    return {
        "profile": profile,
        "step": step,
        "turn": turn,
        "context_limit": limits["context"],
        "step_used": step_used,
        "step_budget": limits["budget"],
        "session_used": session_used,
        "session_budget": sess_lim,
        "warn": bool(hints),
        "warn_detail": "; ".join(hints),
        "model_hint": (settings.get("cost") or {}).get("model_hint") or "",
        "runtime": settings.get("runtime") or "cursor",
    }


def format_cost_line(snap: Dict[str, Any]) -> str:
    def k(n: int) -> str:
        if n >= 1_000_000:
            return f"{n / 1_000_000:.1f}M"
        if n >= 1000:
            return f"{n / 1000:.1f}k"
        return str(n)

    line = (
        f"COST {snap.get('profile')}  step={snap.get('step')}  "
        f"turn≈{k(int(snap.get('turn') or 0))}/{k(int(snap.get('context_limit') or 0))}  "
        f"step≈{k(int(snap.get('step_used') or 0))}/{k(int(snap.get('step_budget') or 0))}  "
        f"session≈{k(int(snap.get('session_used') or 0))}/{k(int(snap.get('session_budget') or 0))}"
    )
    hint = snap.get("model_hint")
    if hint:
        line += f"  model_hint={hint}"
    return line


def cost_cap_hit(
    *,
    step: str,
    turn: int,
    usage: Dict[str, Any],
    settings: Dict[str, Any],
) -> Optional[Dict[str, Any]]:
    limits = step_limits(settings, step)
    session_used = int(usage.get("session") or 0)
    step_used = int((usage.get("steps") or {}).get(step) or 0)
    sess_lim = session_budget(settings)
    if turn > limits["context"]:
        return {
            "hit": f"cost.steps.{step}.context",
            "used": turn,
            "limit": limits["context"],
            "step": step,
        }
    if step_used + turn > limits["budget"]:
        return {
            "hit": f"cost.steps.{step}.budget",
            "used": step_used + turn,
            "limit": limits["budget"],
            "step": step,
        }
    if session_used + turn > sess_lim:
        return {
            "hit": "cost.session_token_budget",
            "used": session_used + turn,
            "limit": sess_lim,
            "step": step,
        }
    return None


def cost_cap_inform_message(hit: Dict[str, Any]) -> str:
    key = hit["hit"]
    used = hit["used"]
    limit = hit["limit"]
    example = EXAMPLE_LOCAL.relative_to(QUINSY_STUDIO.parent)
    local = LOCAL_SETTINGS_PATH.relative_to(QUINSY_STUDIO.parent)
    suggested = max(limit + 1, int(limit * 1.5))
    return (
        f"cost-cap: estimated {used} tokens > {limit} on {key}. "
        f"Copy {example} → {local} and raise {key} "
        f"(e.g. {limit} → {suggested}), then ./studio execute. "
        "Do not keep stuffing files."
    )


def apply_cost_policy(
    project: str,
    step: Any,
    *,
    settings: Optional[Dict[str, Any]] = None,
    usage_path: Optional[Path] = None,
) -> Any:
    """Attach COST to an ExecuteStep. INFORM (loop=False) when a named cap is hit."""
    settings = settings or load_settings()
    usage = load_usage(usage_path)
    cost_step = resolve_cost_step(step.kind, step.command or "", step.reason or "", step.read or "")
    turn = estimate_turn_tokens(project, step.card, step.read)

    if step.kind == "HITL":
        step.cost = cost_snapshot(step=cost_step, turn=0, usage=usage, settings=settings)
        step.cost["turn"] = 0
        return step

    hit = cost_cap_hit(step=cost_step, turn=turn, usage=usage, settings=settings)
    if hit:
        msg = cost_cap_inform_message(hit)
        snap = cost_snapshot(step=cost_step, turn=turn, usage=usage, settings=settings)
        snap["cap"] = hit
        step.kind = "INFORM"
        step.reason = msg
        step.command = f"./studio settings  # raise {hit['hit']}, then ./studio execute {project}"
        step.inform = msg
        step.loop = False
        step.cost = snap
        return step

    usage = add_usage(cost_step, turn, project=project, path=usage_path)
    step.cost = cost_snapshot(step=cost_step, turn=turn, usage=usage, settings=settings)
    return step


def format_settings_report(settings: Optional[Dict[str, Any]] = None, usage: Optional[Dict[str, Any]] = None) -> str:
    settings = settings or load_settings()
    usage = usage if usage is not None else load_usage()
    cost = settings.get("cost") or {}
    lines = [
        f"runtime:     {settings.get('runtime') or 'cursor'}",
        f"profile:     {cost.get('profile')}",
        f"model_hint:  {cost.get('model_hint') or '(host default)'}",
        f"estimate:    {cost.get('estimate')}  (not host billing)",
        f"warn_at:     {cost.get('warn_at_pct')}%",
        f"session:     {int(usage.get('session') or 0)} / {session_budget(settings)}"
        + (f"  project={usage.get('project')}" if usage.get("project") else ""),
        "",
        "steps:                context    budget     used",
    ]
    used_steps = usage.get("steps") or {}
    for name in STEP_NAMES:
        lim = step_limits(settings, name)
        used = int(used_steps.get(name) or 0)
        lines.append(
            f"  {name:<16} {lim['context']:>8}  {lim['budget']:>8}  {used:>8}"
        )
    lines.append("")
    lines.append("Override: copy studio-templates/studio.settings.local.example.yaml")
    lines.append("       →  .quinsy-studio/studio.settings.local.yaml  (no API keys)")
    lines.append("Hosts: Cursor (default), Claude Code (CLAUDE.md), Gemini CLI (GEMINI.md).")
    lines.append("Product LLM keys stay in the project .env — not this file.")
    return "\n".join(lines)
