#!/usr/bin/env python3
"""Queue skill training beside product execute — does not block IMPLEMENT."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from studio_hq_lock import hq_write_lock

QUINSY_STUDIO = Path(__file__).parent.parent
QUEUE_PATH = QUINSY_STUDIO / "knowledge-base" / "learnings" / "train-queue.json"
TEAMS_DIR = QUINSY_STUDIO / "teams"
BACKLOG_DONE = QUINSY_STUDIO / "backlog" / "done"
DEFAULT_OPEN_MAX = 12
BACKLOG_OPEN = QUINSY_STUDIO / "backlog" / "open"


def _norm_topic(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (text or "").lower())[:80]


def _topic_family(text: str) -> str:
    """Stable prefix so portability rewrites still match the original job."""
    return _norm_topic(text)[:32]


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
    with hq_write_lock("hq"):
        QUEUE_PATH.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return QUEUE_PATH


def open_jobs() -> List[Dict]:
    return [j for j in load_queue().get("jobs", []) if j.get("status") == "open"]


def train_open_max() -> int:
    try:
        from studio_settings import load_settings

        cost = (load_settings().get("cost") or {})
        return max(1, int(cost.get("train_open_max") or DEFAULT_OPEN_MAX))
    except Exception:
        return DEFAULT_OPEN_MAX


def infer_lo_id(topic: str) -> str:
    """Match a train topic to an LO filename/title when observation was omitted."""
    needle = _norm_topic(topic)
    if len(needle) < 12:
        return ""
    hits: List[str] = []
    for folder in (BACKLOG_OPEN, BACKLOG_DONE):
        if not folder.is_dir():
            continue
        for path in folder.glob("LO-*.md"):
            match = re.search(r"(LO-\d+)", path.name, re.I)
            if not match:
                continue
            slug = _norm_topic(path.stem)
            if needle[:40] in slug or slug[8:48] in needle:
                hits.append(match.group(1).upper())
    unique = list(dict.fromkeys(hits))
    return unique[0] if len(unique) == 1 else ""


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
    observation = (observation or "").strip()
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
    if not observation:
        observation = infer_lo_id(topic) or ""
    if (source or "").lower() == "lo" and not observation:
        raise ValueError("source=lo requires observation --lo LO-NNNN (empty observation is a bug)")
    with hq_write_lock("hq"):
        return _enqueue_train_locked(
            skill_id, topic, source=source, observation=observation
        )


def _enqueue_train_locked(
    skill_id: str,
    topic: str,
    *,
    source: str,
    observation: str,
) -> Dict:
    data = load_queue()
    family = (skill_id, _topic_family(topic))
    family_hit = None
    for existing in data.get("jobs", []):
        if existing.get("skill_id") != skill_id:
            continue
        existing_topic = str(existing.get("topic") or "")
        exact = _norm_topic(existing_topic) == _norm_topic(topic)
        related = _topic_family(existing_topic) == family[1]
        if not exact and not related:
            continue
        if observation and not (existing.get("observation") or "").strip():
            existing["observation"] = observation
            save_queue(data)
        if exact:
            return existing
        family_hit = existing
    if family_hit:
        return family_hit
    opened = [j for j in data.get("jobs", []) if j.get("status") == "open"]
    cap = train_open_max()
    if len(opened) >= cap:
        raise ValueError(
            f"train queue full ({len(opened)}/{cap} open). "
            f"./studio train --done TR-NNNN after infusion, or raise cost.train_open_max"
        )
    jid = f"TR-{len(data['jobs']) + 1:04d}"
    job = {
        "id": jid,
        "skill_id": skill_id,
        "topic": topic,
        "source": source,
        "observation": observation,
        "status": "open",
        "created": datetime.now().isoformat(timespec="seconds"),
        "instruction": (
            "Second agent: research (cited), derive portable principles, then "
            "./studio infusion-delta into the named playbook (no full-file rewrite). "
            f"Close with ./studio train --done {jid}. Product execute stays IMPLEMENT."
        ),
    }
    data["jobs"].append(job)
    save_queue(data)
    return job


def purge_empty_observations() -> List[str]:
    """Close open train jobs that were written without an LO observation."""
    data = load_queue()
    stamp = datetime.now().isoformat(timespec="seconds")
    closed: List[str] = []
    for job in data.get("jobs", []):
        if job.get("status") != "open":
            continue
        if (job.get("observation") or "").strip():
            continue
        job["status"] = "done"
        job["closed"] = stamp
        job["closed_reason"] = "empty-observation-invalid"
        closed.append(str(job.get("id")))
    if closed:
        save_queue(data)
    return closed


def close_job(job_id: str) -> Optional[Dict]:
    jid = (job_id or "").strip().upper()
    data = load_queue()
    found = None
    for job in data.get("jobs", []):
        if str(job.get("id") or "").upper() == jid:
            job["status"] = "done"
            job["closed"] = datetime.now().isoformat(timespec="seconds")
            found = job
            break
    if found:
        save_queue(data)
    return found


def close_jobs_for_lo(lo_id: str) -> List[Dict]:
    lid = (lo_id or "").strip().upper()
    if not lid:
        return []
    data = load_queue()
    closed: List[Dict] = []
    stamp = datetime.now().isoformat(timespec="seconds")
    for job in data.get("jobs", []):
        if job.get("status") != "open":
            continue
        obs = str(job.get("observation") or "")
        if lid in obs.upper() or lid in str(job.get("topic") or "").upper():
            job["status"] = "done"
            job["closed"] = stamp
            closed.append(job)
    if closed:
        save_queue(data)
    return closed


def backfill_observations() -> List[str]:
    """Fill empty observation from LO match; close opens that duplicate a done job."""
    data = load_queue()
    changed: List[str] = []
    stamp = datetime.now().isoformat(timespec="seconds")
    done_by_family = {}
    for job in data.get("jobs", []):
        if job.get("status") != "done":
            continue
        done_by_family[(job.get("skill_id"), _topic_family(str(job.get("topic") or "")))] = job
    for job in data.get("jobs", []):
        if job.get("status") != "open":
            continue
        topic = str(job.get("topic") or "")
        if not (job.get("observation") or "").strip():
            sibling = done_by_family.get((job.get("skill_id"), _topic_family(topic)))
            inferred = infer_lo_id(topic)
            filled = (sibling.get("observation") if sibling else "") or inferred
            if filled:
                job["observation"] = filled
                changed.append(str(job.get("id")))
        family = (job.get("skill_id"), _topic_family(topic))
        if family in done_by_family:
            job["status"] = "done"
            job["closed"] = stamp
            job["closed_reason"] = "duplicate-of-done"
            changed.append(str(job.get("id")))
    if changed:
        save_queue(data)
    return changed


def sync_train_with_done_los() -> List[str]:
    """Close TR jobs whose observation LO is already in backlog/done/."""
    backfill_observations()
    if not BACKLOG_DONE.is_dir():
        return []
    done_ids = set()
    for path in BACKLOG_DONE.glob("LO-*.md"):
        match = re.search(r"(LO-\d+)", path.name, re.I)
        if match:
            done_ids.add(match.group(1).upper())
    closed_ids: List[str] = []
    for lid in sorted(done_ids):
        for job in close_jobs_for_lo(lid):
            closed_ids.append(str(job.get("id")))
    return closed_ids


def sidecar_commands(limit: int = 4) -> List[Dict]:
    """Oldest open train jobs for the execute CARD TRAIN lines."""
    jobs = sorted(open_jobs(), key=lambda j: str(j.get("created") or ""))
    out: List[Dict] = []
    for job in jobs[: max(1, limit)]:
        skill = job.get("skill_id") or "SO-001"
        topic = str(job.get("topic") or "")[:80].replace('"', "")
        lo = str(job.get("observation") or "").strip()
        cmd = f'./studio train {skill} --from lo --topic "{topic}"'
        if lo:
            cmd += f" --lo {lo}"
        out.append(
            {
                "id": job.get("id"),
                "skill_id": skill,
                "topic": topic,
                "lo": lo,
                "command": cmd,
                "queued": f"./studio train --done {job.get('id')}",
            }
        )
    return out


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
