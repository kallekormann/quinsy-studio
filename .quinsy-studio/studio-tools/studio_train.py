#!/usr/bin/env python3
"""Queue skill training beside product execute — does not block IMPLEMENT."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

QUINSY_STUDIO = Path(__file__).parent.parent
QUEUE_PATH = QUINSY_STUDIO / "knowledge-base" / "learnings" / "train-queue.json"
TEAMS_DIR = QUINSY_STUDIO / "teams"


def load_queue() -> Dict:
    if not QUEUE_PATH.exists():
        return {"jobs": []}
    try:
        data = json.loads(QUEUE_PATH.read_text(encoding="utf-8"))
        data.setdefault("jobs", [])
        return data
    except json.JSONDecodeError:
        return {"jobs": []}


def save_queue(data: Dict) -> Path:
    QUEUE_PATH.parent.mkdir(parents=True, exist_ok=True)
    QUEUE_PATH.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return QUEUE_PATH


def open_jobs() -> List[Dict]:
    return [j for j in load_queue().get("jobs", []) if j.get("status") == "open"]


def enqueue_train(
    skill_id: str,
    topic: str,
    *,
    source: str = "mistake",
    observation: str = "",
) -> Dict:
    skill_id = (skill_id or "").strip()
    topic = (topic or "").strip()
    if not skill_id or not topic:
        raise ValueError("skill-id and topic are required")
    try:
        from studio_portability import portability_verdict

        verdict = portability_verdict(topic)
        if not verdict["portable"]:
            raise ValueError(
                f"train topic not portable: {verdict.get('reason') or 'rewrite to a reusable principle'}"
            )
        topic = str(verdict["title"])
    except ImportError:
        pass
    data = load_queue()
    for existing in data.get("jobs", []):
        if existing.get("status") == "open" and existing.get("topic") == topic and existing.get("skill_id") == skill_id:
            return existing
    job = {
        "id": f"TR-{len(data['jobs']) + 1:04d}",
        "skill_id": skill_id,
        "topic": topic,
        "source": source,
        "observation": observation,
        "status": "open",
        "created": datetime.now().isoformat(timespec="seconds"),
        "instruction": (
            "Second agent: research (web or cited source), derive portable principles "
            "(no project/product names in HQ docs; provenance only), append to the skill "
            "toolbox and a playbook. Product execute continues IMPLEMENT in parallel."
        ),
    }
    data["jobs"].append(job)
    save_queue(data)
    return job


def skill_file_hint(skill_id: str) -> Optional[str]:
    sid = skill_id.upper()
    for path in TEAMS_DIR.glob("*/skills/*.md"):
        try:
            head = path.read_text(encoding="utf-8", errors="ignore")[:400]
        except OSError:
            continue
        if f"id: {sid}" in head or f"**ID:** {sid}" in head or path.stem.replace("-", "").upper().endswith(sid.replace("-", "")):
            return str(path.relative_to(QUINSY_STUDIO))
    return None
