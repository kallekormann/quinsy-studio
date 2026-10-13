#!/usr/bin/env python3
"""Loop metrics for the sprint retro (agency integration L14).

Read from `sprints/SPRINT-NN/execution-log.json` and the escalation packets,
never from memory: first-pass gate rate (overall and per failing check),
average retries, QA fails, finish-gate holds, blocked tickets.
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any, Dict, List

GATE_EVENTS = ("gate-pass", "gate-fail")
FAIL_EVENTS = ("gate-fail", "qa-fail")


def _checks(note: str) -> List[str]:
    if not note.startswith("gate red:"):
        return []
    return [c.strip() for c in note.split(":", 1)[1].split(",") if c.strip()]


def loop_metrics(log: Dict[str, Any], sprint_dir: Path) -> Dict[str, Any]:
    first_gate: Dict[str, Dict[str, Any]] = {}
    fails: Counter = Counter()
    qa_fails = holds = 0
    for entry in log.get("entries", []):
        tid = entry.get("ticket")
        event = entry.get("event")
        note = str(entry.get("note") or "")
        if not tid:
            continue
        if event in GATE_EVENTS and tid not in first_gate:
            first_gate[tid] = entry
        if event in FAIL_EVENTS:
            fails[tid] += 1
        if event == "qa-fail":
            if note.startswith("finish hold"):
                holds += 1
            else:
                qa_fails += 1

    gated = len(first_gate)
    first_pass = sum(1 for e in first_gate.values() if e.get("event") == "gate-pass")
    per_check: Counter = Counter()
    for entry in first_gate.values():
        if entry.get("event") == "gate-fail":
            per_check.update(set(_checks(str(entry.get("note") or ""))))

    esc_dir = sprint_dir / "escalations"
    blocked = sorted(p.stem for p in esc_dir.glob("*.md")) if esc_dir.is_dir() else []
    return {
        "gated": gated,
        "first_pass": first_pass,
        "per_check": dict(per_check),
        "avg_retries": (sum(fails[t] for t in first_gate) / gated) if gated else 0.0,
        "qa_fails": qa_fails,
        "finish_holds": holds,
        "blocked": blocked,
    }


def metrics_lines(metrics: Dict[str, Any]) -> List[str]:
    gated = metrics["gated"]
    if not gated:
        return ["- Loop: no ticket reached the gate this sprint (execution-log.json is empty)"]
    pct = round(100 * metrics["first_pass"] / gated)
    lines = [
        f"- First-pass gate: {metrics['first_pass']}/{gated} tickets ({pct}%)",
        f"- Average retries per gated ticket: {metrics['avg_retries']:.1f} (red gates + QA fails)",
        f"- QA fails: {metrics['qa_fails']} · finish-gate holds: {metrics['finish_holds']}",
        f"- Blocked after escalation: {len(metrics['blocked'])}"
        + (f" ({', '.join(metrics['blocked'])})" if metrics["blocked"] else ""),
    ]
    if metrics["per_check"]:
        lines.append("- First-pass rate per failing check:")
        for check, n in sorted(metrics["per_check"].items(), key=lambda kv: (-kv[1], kv[0])):
            lines.append(f"  - {check}: {gated - n}/{gated} ({round(100 * (gated - n) / gated)}%)")
    return lines
