#!/usr/bin/env python3
"""Ideation desk. Files live in gitignored ideation/. The CLI does not search the web."""

from __future__ import annotations

import json
import re
import shutil
import sqlite3
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse

DIMENSIONS: List[Tuple[str, int]] = [
    ("willingness_to_pay", 3),
    ("demand_volume", 2),
    ("frequency_urgency", 2),
    ("reachability", 3),
    ("time_to_mvp", 1),
    ("monetization", 1),
    ("platform_risk", 2),
    ("trend", 1),
    ("competitor_weakness", 2),
    ("fit", 1),
]
DIM_NAMES = [name for name, _weight in DIMENSIONS]
DIM_WEIGHT = {name: weight for name, weight in DIMENSIONS}
PROMOTE_MIN = 58
MAX_SCORE = 90
PARAPHRASE_MAX = 200
COMPETE_FRACTION = 1 / 3
CROWDED = {"crowded", "saturated"}
# Builder time is not a ceiling. One chunk is about two months: a full web app
# for one solo builder plus AI agents for coding and design. The first chunk is
# the MVP. Later chunks stay in the idea. Medicine is a knock-out, not a slow build.
FEASIBILITY_BAR = (
    "Builder time is not a ceiling. One solo builder, with AI agents for coding and design, "
    "ships in chunks of about two months. Each chunk is a full web app, big enough for that "
    "builder and those agents. The first chunk is the MVP. Later chunks stay in the idea. "
    "Medicine and clinical care are out of reach. Other trades stay in reach "
    "when the activity is allowed and the job is software."
)
CLINICAL_DOMAINS = {"clinical", "medicine"}
IDEA_DOMAINS = {"trade", "life", "clinical"}
SECTIONS = ("brief", "signals", "cluster", "ideas", "compete", "shape", "score", "present", "learn")
SHAPE_HEADINGS = (
    "### Problem",
    "### Solution",
    "### Architecture",
    "### Experience",
    "### Steps",
    "### First chunk",
    "### Later chunks",
)
BUILD_HEADINGS = ("User tasks", "System tasks", "Backend", "Infrastructure", "Modules")
BUILD_VERBS = re.compile(
    r"(?i)\b(implement|deploy|refactor|product code|build(?!\s+(?:upon|on)\b))\b"
)
IDEATE_RE = re.compile(r"(?i)(\bideate\b|\bincubate\b|\bideation\b|\./studio ideate\b)")
CONTINUATION_RE = re.compile(
    r"(?i)^("
    r"signals|cluster|ideas|compete|shape|score|present|learn|dimension|"
    r"willingness(?: to pay)?|demand(?: volume)?|frequency(?: and urgency)?|"
    r"reach(?:ability)?|time to mvp|monetization|platform(?: risk)?|trend|"
    r"competitor weakness|fit|"
    r"where can i read the idea\??|show the idea|show"
    r")$"
)
MARKET_FITS = {"applies", "outside", "global"}

SKILL_REL = (
    ".quinsy-studio/teams/09-studio-operations-evolution/skills/ideation-desk.md"
)


class DeskError(Exception):
    pass


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def template_dir() -> Path:
    return repo_root() / ".quinsy-studio" / "studio-templates" / "ideation"


def is_ideate_request(text: str) -> bool:
    """True when the bubble is the ideation desk and not a product-build request."""
    raw = text or ""
    if not IDEATE_RE.search(raw):
        return False
    if BUILD_VERBS.search(raw):
        return False
    return True


def is_desk_continuation(text: str, session_open: bool) -> bool:
    """True when an open session is still the desk, and the bubble is only the next section or dimension."""
    if not session_open or BUILD_VERBS.search(text or ""):
        return False
    return bool(CONTINUATION_RE.match((text or "").strip()))


def session_is_open(root: Optional[Path] = None) -> bool:
    folder = (root or repo_root()) / "ideation" / "sessions"
    if not folder.is_dir():
        return False
    for path in sorted(folder.glob("*.md"), reverse=True):
        meta, _body = _split_front(path.read_text(encoding="utf-8"))
        if meta.get("status") == "open":
            return True
    return False


def _two_sentences(text: str) -> bool:
    parts = [part.strip() for part in re.split(r"[.!?]+", text or "") if part.strip()]
    return len(parts) >= 2


def _today(day: Optional[date]) -> date:
    return day or date.today()


def _parse_day(value: str) -> Optional[date]:
    try:
        return datetime.strptime((value or "").strip()[:10], "%Y-%m-%d").date()
    except ValueError:
        return None


def _domain(url: str) -> str:
    host = urlparse(url or "").netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    return host


def _slug(text: str) -> str:
    text = (text or "").lower()
    text = re.sub(r"[äöüß]", lambda m: {"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss"}[m.group()], text)
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")[:50] or "idea"


def _split_front(text: str) -> Tuple[Dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}, text
    meta: Dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ": " not in line:
            continue
        key, value = line.split(": ", 1)
        meta[key.strip()] = value
    return meta, text[end + 5 :]


def _dump_front(meta: Dict[str, str], body: str) -> str:
    lines = ["---"]
    for key, value in meta.items():
        clean = str(value).replace("\n", " ").strip()
        lines.append(f"{key}: {clean}")
    lines.append("---")
    text = "\n".join(lines) + "\n"
    if body:
        if not body.startswith("\n"):
            text += "\n"
        text += body if body.endswith("\n") else body + "\n"
    return text


def _keywords(value: str) -> List[str]:
    parts = re.split(r"[,;]", value or "")
    return [p.strip().lower() for p in parts if p.strip()]


def _load_yaml_budgets(path: Path) -> dict:
    data: dict = {}
    current = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        if not line.startswith(" ") and line.endswith(":"):
            current = line[:-1].strip()
            data[current] = {}
            continue
        if ":" not in line:
            continue
        key, value = line.strip().split(":", 1)
        key = key.strip()
        value = value.strip()
        try:
            parsed: object = int(value)
        except ValueError:
            parsed = value
        if current and line.startswith(" "):
            data[current][key] = parsed
        else:
            current = None
            data[key] = parsed
    return data


class Desk:
    def __init__(self, root: Path, templates: Path, today: Optional[date] = None, now: Optional[datetime] = None):
        self.root = Path(root)
        self.templates = Path(templates)
        self.today = _today(today)
        self.now = now or datetime.combine(self.today, datetime.min.time())
        self.ideation = self.root / "ideation"
        self.intake = self.root / "intake"

    def seed(self) -> str:
        self.ideation.mkdir(parents=True, exist_ok=True)
        for name in (
            "problems",
            "ideas",
            "competitors",
            "sessions",
            "shortlist",
            "scratch",
        ):
            (self.ideation / name).mkdir(parents=True, exist_ok=True)
        copied = []
        for src in self.templates.iterdir():
            if not src.is_file():
                continue
            dest = self.ideation / src.name
            if dest.exists():
                continue
            shutil.copyfile(src, dest)
            copied.append(src.name)
        self._rebuild_index()
        if copied:
            return "Seeded " + ", ".join(sorted(copied))
        return "Store already seeded"

    def budgets(self) -> dict:
        path = self.ideation / "budgets.yaml"
        if not path.exists():
            self.seed()
        return _load_yaml_budgets(path)

    def resolve_budget(self, tier: str, overrides: Dict[str, str]) -> Dict[str, int]:
        data = self.budgets()
        if tier not in data or not isinstance(data[tier], dict):
            raise DeskError(f"Unknown budget tier '{tier}'. Use small, normal, or large.")
        base = dict(data[tier])
        mapping = {
            "max-searches": "searches",
            "max-fetches": "fetches",
            "max-minutes": "minutes",
            "max-reclusters": "reclusters",
        }
        for flag, key in mapping.items():
            if flag in overrides and overrides[flag] != "yes":
                base[key] = int(overrides[flag])
        for key in (
            "searches",
            "fetches",
            "iterations_per_dimension",
            "reclusters",
            "minutes",
            "session_log_bytes",
            "shortlist_n",
            "near_misses",
            "competitor_profiles",
            "neighboring_listings",
        ):
            if key not in base:
                raise DeskError(f"Budget tier '{tier}' is missing {key}")
        return {key: int(base[key]) for key in base}

    def _cap(self, kind: str) -> int:
        data = self.budgets()
        key = f"{kind}_file_bytes"
        value = data.get(key)
        if not isinstance(value, int):
            raise DeskError(f"budgets.yaml is missing {key}")
        return value

    def _write(self, path: Path, meta: Dict[str, str], body: str, cap: int) -> None:
        text = _dump_front(meta, body)
        size = len(text.encode("utf-8"))
        if size > cap:
            raise DeskError(
                f"Refusing to write {path.relative_to(self.root)}: {size} bytes exceeds the {cap} byte cap. Nothing was truncated."
            )
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def _read(self, path: Path) -> Tuple[Dict[str, str], str]:
        return _split_front(path.read_text(encoding="utf-8"))

    def _files(self, kind: str) -> List[Path]:
        folder = self.ideation / kind
        if not folder.exists():
            return []
        return sorted(folder.glob("*.md"))

    def _next_id(self, kind: str, prefix: str) -> str:
        highest = 0
        for path in self._files(kind):
            match = re.fullmatch(rf"{prefix}-(\d+)", path.stem)
            if match:
                highest = max(highest, int(match.group(1)))
        return f"{prefix}-{highest + 1:03d}"

    def _rebuild_index(self) -> None:
        problems = []
        by_category: Dict[str, List[str]] = {}
        for path in self._files("problems"):
            meta, _body = self._read(path)
            row = " | ".join(
                [
                    meta.get("id", path.stem),
                    meta.get("sentence", ""),
                    meta.get("segment", ""),
                    meta.get("keywords", ""),
                    meta.get("status", "new"),
                    meta.get("score", "-"),
                    meta.get("date", ""),
                    meta.get("discard_reason", ""),
                ]
            )
            category = meta.get("category") or "uncategorized"
            by_category.setdefault(category, []).append(row)
            problems.append(row)
        lines = ["# Index", "", "Duplicate checks use these rows. Do not open every file to decide a match.", ""]
        lines.append("## Problems")
        lines.append("")
        if any(len(rows) > 40 for rows in by_category.values()):
            for category, rows in sorted(by_category.items()):
                lines.append(f"### {category}")
                lines.append("")
                lines.extend(rows)
                lines.append("")
        else:
            lines.extend(problems)
            lines.append("")
        lines.append("## Ideas")
        lines.append("")
        for path in self._files("ideas"):
            meta, _body = self._read(path)
            lines.append(
                " | ".join(
                    [
                        meta.get("id", path.stem),
                        meta.get("title", ""),
                        meta.get("problems", ""),
                        meta.get("shape", ""),
                        meta.get("status", "draft"),
                        meta.get("score_total", "-"),
                        meta.get("date", ""),
                        meta.get("discard_reason", ""),
                    ]
                )
            )
        lines.append("")
        lines.append("## Competitors")
        lines.append("")
        for path in self._files("competitors"):
            meta, _body = self._read(path)
            lines.append(
                " | ".join(
                    [
                        meta.get("id", path.stem),
                        meta.get("name", ""),
                        meta.get("category", ""),
                        meta.get("tier", "unknown"),
                        meta.get("last_checked", ""),
                    ]
                )
            )
        lines.append("")
        (self.ideation / "INDEX.md").write_text("\n".join(lines), encoding="utf-8")

    def index_problem_rows(self) -> List[Dict[str, str]]:
        rows = []
        for path in self._files("problems"):
            meta, _body = self._read(path)
            rows.append(meta)
        return rows

    def find_duplicate(self, sentence: str, keywords: str) -> Optional[Dict[str, str]]:
        incoming = set(_keywords(keywords))
        norm = re.sub(r"\s+", " ", (sentence or "").strip().lower())
        for meta in self.index_problem_rows():
            existing = re.sub(r"\s+", " ", (meta.get("sentence") or "").strip().lower())
            if norm and existing == norm:
                return meta
            overlap = incoming & set(_keywords(meta.get("keywords", "")))
            if len(overlap) >= 2:
                return meta
        return None

    def _open_session(self) -> Optional[Path]:
        for path in sorted((self.ideation / "sessions").glob("*.md"), reverse=True):
            meta, _body = self._read(path)
            if meta.get("status") == "open":
                return path
        return None

    def _session_or_raise(self) -> Path:
        path = self._open_session()
        if path is None:
            raise DeskError("No open session. Start one with ./studio ideate [focus].")
        return path

    def _touch_clock(self, meta: Dict[str, str], *, allow_hard: bool = False) -> str:
        """Return '' or 'wrap-up' or 'hard'. Hard writes the incomplete shortlist once."""
        started = datetime.fromisoformat(meta["started_at"])
        elapsed = (self.now - started).total_seconds() / 60
        limit = int(meta["limit_minutes"])
        if elapsed >= limit or self._over_hard(meta):
            if meta.get("hard_stopped") != "yes":
                meta["hard_stopped"] = "yes"
                meta["status"] = "closed"
                meta["section"] = "present"
            if not allow_hard:
                raise DeskError("BUDGET hard limit reached. The shortlist is marked incomplete. Collection has stopped.")
            return "hard"
        if elapsed >= 0.8 * limit or self._over_soft(meta):
            return "wrap-up"
        return ""

    def _over_hard(self, meta: Dict[str, str]) -> bool:
        for key in ("searches", "fetches", "reclusters"):
            if int(meta.get(f"spent_{key}", "0")) >= int(meta[f"limit_{key}"]):
                return True
        return False

    def _over_soft(self, meta: Dict[str, str]) -> bool:
        for key in ("searches", "fetches", "reclusters"):
            limit = int(meta[f"limit_{key}"])
            spent = int(meta.get(f"spent_{key}", "0"))
            if limit and spent / limit >= 0.8:
                return True
        return False

    def _load_session(self, path: Path) -> Tuple[Dict[str, str], str]:
        meta, body = self._read(path)
        mode = ""
        try:
            mode = self._touch_clock(meta, allow_hard=True)
        except DeskError:
            mode = "hard"
        if mode == "hard" and meta.get("shortlist_written") != "yes":
            self._write_shortlist(meta, incomplete=True)
            meta["shortlist_written"] = "yes"
            meta["status"] = "closed"
            body += "\n## Checkpoint\n\nHard budget stop. Shortlist marked incomplete.\n"
            self._write(path, meta, body, int(meta["limit_session_log_bytes"]))
        elif mode == "wrap-up" and "BUDGET wrap-up" not in body:
            body += "\n## Checkpoint\n\nBUDGET wrap-up at 80 percent. No new collection. Score and present from what is stored.\n"
            self._write(path, meta, body, int(meta["limit_session_log_bytes"]))
        return meta, body

    def start(self, focus: str, tier: str, overrides: Dict[str, str], force_new: bool) -> str:
        self.seed()
        focus_text = (focus or "").strip()
        market = (overrides.get("market") or "").strip()
        if not force_new:
            existing = self._open_session()
            if existing:
                meta, body = self._load_session(existing)
                if meta.get("section") == "brief" and focus_text:
                    meta["focus"] = focus_text
                    meta["section"] = "signals"
                    if market:
                        meta["hitl_market"] = market
                    body += f"\n## Brief\n\n{focus_text}\n"
                    stated = (meta.get("hitl_market") or "").strip()
                    if stated:
                        body += f"\nMarket to check at qualification: {stated}. Research is not limited to it.\n"
                    else:
                        body += "\nNo market was stated. Judge globally at qualification.\n"
                    self._write(existing, meta, body, int(meta["limit_session_log_bytes"]))
                    return self._section_banner(existing, meta, resumed=True)
                return self._section_banner(existing, meta, resumed=True)
        limits = self.resolve_budget(tier, overrides)
        awaiting = not focus_text
        focus_label = focus_text or "awaiting brief"
        focus_slug = _slug(focus_label)
        name = f"{self.today.isoformat()}-{focus_slug}.md"
        path = self.ideation / "sessions" / name
        if path.exists():
            stamp = self.now.strftime("%H%M%S")
            path = self.ideation / "sessions" / f"{self.today.isoformat()}-{focus_slug}-{stamp}.md"
            suffix = 2
            while path.exists():
                path = self.ideation / "sessions" / f"{self.today.isoformat()}-{focus_slug}-{stamp}-{suffix}.md"
                suffix += 1
        meta = {
            "status": "open",
            "section": "brief" if awaiting else "signals",
            "focus": focus_label,
            "hitl_market": market,
            "budget": tier,
            "started_at": self.now.isoformat(timespec="seconds"),
            "shortlist_written": "no",
            "hard_stopped": "no",
            "spent_searches": "0",
            "spent_fetches": "0",
            "spent_reclusters": "0",
            "spent_compete_searches": "0",
            "spent_compete_fetches": "0",
            "passes_json": "{}",
            "empty_json": "{}",
            "closed_sources": "",
        }
        for key, value in limits.items():
            meta[f"limit_{key}"] = str(value)
        market_line = (
            f"Market to check at qualification: {market}. Research is not limited to it.\n"
            if market
            else "No market was stated. Judge globally at qualification.\n"
        )
        brief_line = (
            "\n## Brief\n\nWaiting for the human. Do not search yet.\n"
            if awaiting
            else f"\n## Brief\n\n{focus_text}\n"
        )
        body = (
            f"# Session {meta['focus']}\n\n"
            "Official APIs first. An unofficial endpoint is never the only source, and it is marked fragile in sources.md.\n\n"
            + market_line
            + brief_line
            + "\n## Budget\n\n"
            + "\n".join(f"- {key}: {value}" for key, value in limits.items())
            + "\n\n## Catalog\n\nMark each source row searched or skipped.\n"
        )
        self._write(path, meta, body, limits["session_log_bytes"])
        self._clear_scratch()
        return self._section_banner(path, meta, resumed=False)

    def _gap_label(self) -> str:
        rows = self.index_problem_rows()
        if not rows:
            return "no problems yet"
        counts: Dict[str, int] = {}
        for meta in rows:
            key = meta.get("region") or meta.get("category") or meta.get("life_situation") or "unspecified"
            counts[key] = counts.get(key, 0) + 1
        return min(counts, key=counts.get)

    def _section_banner(self, path: Path, meta: Dict[str, str], resumed: bool) -> str:
        section = meta.get("section") or "signals"
        rel = path.relative_to(self.root)
        stated = (meta.get("hitl_market") or "").strip() or "none"
        if section == "brief":
            next_step = (
                "No brief yet. Ask the human what to look into. A market is optional. "
                "Do not search until they answer."
            )
        else:
            next_step = (
                f"Market to check at qualification: {stated}. Research wherever the sources are. "
                "Run signals, cluster, ideas, compete, shape, score, and present in this turn. "
                "Do not ask the human to continue. "
                "Search the web, then record each search with ./studio ideate search and each fetch with ./studio ideate fetch. "
                "The CLI does not search. "
                "Qualify each idea against the stated market, or as global when none was stated."
            )
        return (
            f"ACTION: IDEATE\n"
            f"SECTION: {section}\n"
            f"SKILL: {SKILL_REL}\n"
            f"HEADING: ## {section}\n"
            f"SESSION: {rel}\n"
            f"BUDGET: {meta.get('budget')} searches {meta.get('spent_searches')}/{meta.get('limit_searches')} "
            f"fetches {meta.get('spent_fetches')}/{meta.get('limit_fetches')}\n"
            f"MARKET: {stated}\n"
            f"GAP: {meta.get('focus')}\n"
            f"{'Resumed the open session.' if resumed else 'Opened a session.'} {next_step}\n"
            "Do not run approve, reject, park, or promote unless the human asked in this conversation."
        )

    def status(self) -> str:
        self.seed()
        index = (self.ideation / "INDEX.md").read_text(encoding="utf-8")
        lines = [index.rstrip(), "", "## Budget"]
        sessions = sorted((self.ideation / "sessions").glob("*.md"))[-5:]
        if not sessions:
            lines.append("No sessions yet.")
        for path in sessions:
            meta, _body = self._read(path)
            lines.append(
                f"- {path.name}: {meta.get('status')} {meta.get('budget')} "
                f"searches {meta.get('spent_searches')}/{meta.get('limit_searches')} "
                f"fetches {meta.get('spent_fetches')}/{meta.get('limit_fetches')} "
                f"minutes limit {meta.get('limit_minutes')}"
            )
        return "\n".join(lines)

    def _guard_collection(self, meta: Dict[str, str]) -> None:
        if meta.get("status") != "open":
            raise DeskError("This session is closed.")
        if meta.get("section") == "brief":
            raise DeskError("Ask for a brief before searching.")
        mode = self._touch_clock(meta, allow_hard=False)
        if mode == "wrap-up":
            raise DeskError("BUDGET wrap-up. No new collection. Write a checkpoint and present the shortlist from stored evidence.")

    def search(self, source: str, outcome: str) -> str:
        path = self._session_or_raise()
        meta, body = self._load_session(path)
        if meta.get("section") == "brief":
            raise DeskError("Ask for a brief before searching.")
        self._guard_collection(meta)
        source = (source or "").strip().lower()
        if not source:
            raise DeskError("search needs --source.")
        closed = {s for s in meta.get("closed_sources", "").split(",") if s}
        if source in closed:
            raise DeskError(f"Source '{source}' is closed after two searches with no new evidence.")
        outcome = (outcome or "").strip().lower()
        if outcome not in {"new", "empty"}:
            raise DeskError("search --outcome must be new or empty.")
        section = meta.get("section") or "signals"
        if section == "compete":
            cap = max(1, int(int(meta["limit_searches"]) * COMPETE_FRACTION))
            spent_c = int(meta.get("spent_compete_searches", "0"))
            if spent_c + 1 > cap:
                raise DeskError(f"Competition pass has used its search share ({cap}).")
            meta["spent_compete_searches"] = str(spent_c + 1)
        spent = int(meta.get("spent_searches", "0")) + 1
        if spent > int(meta["limit_searches"]):
            raise DeskError("Search would pass the hard search cap.")
        meta["spent_searches"] = str(spent)
        empty = json.loads(meta.get("empty_json") or "{}")
        if outcome == "empty":
            empty[source] = int(empty.get(source, 0)) + 1
            if empty[source] >= 2:
                closed.add(source)
                meta["closed_sources"] = ",".join(sorted(closed))
        else:
            empty[source] = 0
        meta["empty_json"] = json.dumps(empty)
        body += f"\n- search {source}: {outcome}\n"
        at_hard = spent >= int(meta["limit_searches"])
        if at_hard:
            meta["hard_stopped"] = "yes"
            meta["status"] = "closed"
            meta["shortlist_written"] = "yes"
            body += "\n## Checkpoint\n\nHard budget stop. Shortlist marked incomplete.\n"
        self._write(path, meta, body, int(meta["limit_session_log_bytes"]))
        if at_hard:
            self._write_shortlist(meta, incomplete=True)
            self._clear_scratch()
            return f"Recorded search {source} {outcome}. Hard budget reached. Shortlist marked incomplete."
        self._load_session(path)
        return f"Recorded search {source} {outcome}. Spent {meta['spent_searches']}/{meta['limit_searches']}."

    def fetch(self) -> str:
        path = self._session_or_raise()
        meta, body = self._load_session(path)
        self._guard_collection(meta)
        section = meta.get("section") or "signals"
        if section == "compete":
            cap = max(1, int(int(meta["limit_fetches"]) * COMPETE_FRACTION))
            spent_c = int(meta.get("spent_compete_fetches", "0"))
            if spent_c + 1 > cap:
                raise DeskError(f"Competition pass has used its fetch share ({cap}).")
            meta["spent_compete_fetches"] = str(spent_c + 1)
        spent = int(meta.get("spent_fetches", "0")) + 1
        if spent > int(meta["limit_fetches"]):
            raise DeskError("Fetch would pass the hard fetch cap.")
        meta["spent_fetches"] = str(spent)
        body += "\n- fetch recorded (raw page not stored)\n"
        self._write(path, meta, body, int(meta["limit_session_log_bytes"]))
        return f"Recorded fetch. Spent {meta['spent_fetches']}/{meta['limit_fetches']}. Store a paraphrase, not the page."

    def checkpoint(self, step: str) -> str:
        path = self._session_or_raise()
        meta, body = self._load_session(path)
        if meta.get("hard_stopped") == "yes":
            raise DeskError("Session already stopped on the hard budget.")
        if step not in SECTIONS:
            raise DeskError("checkpoint --step must be one of " + ", ".join(SECTIONS))
        meta["section"] = step
        body += f"\n## Checkpoint\n\nStep {step} at {self.now.isoformat(timespec='seconds')}.\n"
        self._write(path, meta, body, int(meta["limit_session_log_bytes"]))
        return self._section_banner(path, meta, resumed=True)

    def recluster(self) -> str:
        path = self._session_or_raise()
        meta, body = self._load_session(path)
        self._guard_collection(meta)
        spent = int(meta.get("spent_reclusters", "0")) + 1
        if spent > int(meta["limit_reclusters"]):
            raise DeskError("Re-cluster would pass the session cap.")
        meta["spent_reclusters"] = str(spent)
        body += "\n- recluster\n"
        self._write(path, meta, body, int(meta["limit_session_log_bytes"]))
        return f"Re-cluster {spent}/{meta['limit_reclusters']}."

    def add_problem(self, flags: Dict[str, str]) -> str:
        self.seed()
        sentence = flags.get("sentence", "").strip()
        keywords = flags.get("keywords", "").strip()
        if "|" in sentence or "|" in keywords:
            raise DeskError("Sentence and keywords cannot contain '|'.")
        words = _keywords(keywords)
        if not sentence or not (3 <= len(words) <= 5):
            raise DeskError("problem needs --sentence and 3 to 5 --keywords.")
        dup = self.find_duplicate(sentence, keywords)
        if dup:
            reason = dup.get("discard_reason") or "already stored"
            raise DeskError(
                f"Refusing a new problem. {dup.get('id')} already matches ({dup.get('status')}): {reason}"
            )
        pid = self._next_id("problems", "P")
        meta = {
            "id": pid,
            "status": "new",
            "sentence": sentence,
            "segment": flags.get("segment", ""),
            "keywords": ", ".join(words),
            "region": flags.get("region", ""),
            "language": flags.get("language", ""),
            "category": flags.get("category", ""),
            "life_situation": flags.get("life-situation", ""),
            "score": "-",
            "date": self.today.isoformat(),
            "discard_reason": "",
        }
        self._write(self.ideation / "problems" / f"{pid}.md", meta, "## Evidence\n", self._cap("problem"))
        self._note_session_ids("session_problems", pid)
        self._rebuild_index()
        return f"Created {pid}. Match later signals to this row before opening another problem."

    def discard(self, entity_id: str, reason: str) -> str:
        path, kind = self._entity_path(entity_id)
        if not reason.strip():
            raise DeskError("discard needs a one-line reason.")
        meta, body = self._read(path)
        meta["status"] = "discarded"
        meta["discard_reason"] = reason.strip()
        cap = self._cap("problem" if kind == "problems" else "idea" if kind == "ideas" else "competitor")
        self._write(path, meta, body, cap)
        self._rebuild_index()
        return f"Discarded {entity_id}: {reason.strip()}"

    def _entity_path(self, entity_id: str) -> Tuple[Path, str]:
        prefix = entity_id.split("-", 1)[0]
        kind = {"P": "problems", "I": "ideas", "C": "competitors"}.get(prefix)
        if not kind:
            raise DeskError(f"Unknown id {entity_id}. Use P-###, I-###, or C-###.")
        path = self.ideation / kind / f"{entity_id}.md"
        if not path.exists():
            raise DeskError(f"{entity_id} does not exist.")
        return path, kind

    def add_evidence(self, entity_id: str, flags: Dict[str, str]) -> str:
        path, kind = self._entity_path(entity_id)
        if kind == "competitors":
            return self._competitor_field(path, flags)
        paraphrase = (flags.get("paraphrase") or "").strip()
        if len(paraphrase) > PARAPHRASE_MAX:
            raise DeskError(f"Paraphrase is {len(paraphrase)} characters. The cap is {PARAPHRASE_MAX}. Nothing was stored.")
        url = (flags.get("url") or "").strip()
        day = (flags.get("date") or "").strip()
        source = (flags.get("source") or "").strip()
        author = (flags.get("author") or "").strip()
        thread = (flags.get("thread") or "").strip()
        count = (flags.get("count") or "1").strip()
        in_force = flags.get("in-force") == "yes"
        verified = "yes" if url and day and _parse_day(day) else "no"
        if verified == "yes" and not in_force:
            parsed = _parse_day(day)
            if parsed and parsed < self.today - timedelta(days=730):
                verified = "no"
        line = " | ".join([source or "-", url or "-", day or "-", count, paraphrase or "-", author or "-", thread or "-", verified, "in-force" if in_force else "-"])
        meta, body = self._read(path)
        if "## Evidence" not in body:
            body += "\n## Evidence\n"
        body += f"- {line}\n"
        cap = self._cap("problem" if kind == "problems" else "idea")
        self._write(path, meta, body, cap)
        return f"Appended evidence to {entity_id} ({'counts' if verified == 'yes' and author else 'unverified, does not count'})."

    def evidence_lines(self, meta_body: str) -> List[Dict[str, str]]:
        lines = []
        for raw in meta_body.splitlines():
            if not raw.startswith("- "):
                continue
            parts = [p.strip() for p in raw[2:].split("|")]
            if len(parts) < 9:
                continue
            lines.append(
                {
                    "source": parts[0],
                    "url": parts[1],
                    "date": parts[2],
                    "count": parts[3],
                    "paraphrase": parts[4],
                    "author": parts[5],
                    "thread": parts[6],
                    "verified": parts[7],
                    "in_force": parts[8],
                }
            )
        return lines

    def independent_count(self, body: str) -> int:
        counted: List[Tuple[str, str, str]] = []
        for line in self.evidence_lines(body):
            if line["verified"] != "yes" or line["author"] in {"", "-"} or line["url"] in {"", "-"}:
                continue
            domain = _domain(line["url"])
            author = line["author"].lower()
            thread = line["thread"] if line["thread"] not in {"", "-"} else line["url"]
            if not domain:
                continue
            clash = False
            for prev_domain, prev_author, prev_thread in counted:
                if domain == prev_domain or author == prev_author or thread == prev_thread:
                    clash = True
                    break
            if clash:
                continue
            counted.append((domain, author, thread))
        return len(counted)

    def add_idea(self, flags: Dict[str, str]) -> str:
        self.seed()
        title = flags.get("title", "").strip()
        problems = flags.get("problems", "").strip()
        shape = flags.get("shape", "").strip()
        if not title or not problems or not shape:
            raise DeskError("idea needs --title, --problems, and --shape.")
        blues = flags.get("blue") or []
        if isinstance(blues, str):
            blues = [blues]
        blues = [b.strip() for b in blues if b.strip()]
        if len(blues) > 4:
            raise DeskError("Blue Ocean is at most 4 lines.")
        iid = self._next_id("ideas", "I")
        scores = "\n".join(f"{name}: empty" for name in DIM_NAMES)
        meta = {
            "id": iid,
            "title": title,
            "status": "draft",
            "problems": problems,
            "shape": shape,
            "host": flags.get("host", ""),
            "pitch": flags.get("pitch", ""),
            "competitors": flags.get("competitors", ""),
            "crowdedness": flags.get("crowdedness", "unknown"),
            "wedge": flags.get("wedge", ""),
            "wedge_price_only": flags.get("wedge-price-only", "no"),
            "wedge_cost_evidence": flags.get("wedge-cost-evidence", "no"),
            "bundling_risk": flags.get("bundling-risk", ""),
            "legal_duty": "yes" if flags.get("legal-duty") == "yes" else "no",
            "domain": self._domain(flags.get("domain", "")),
            "knockout": "",
            "rank": "",
            "intake": "",
            "closest_product": flags.get("closest-product", ""),
            "closest_price": flags.get("closest-price", ""),
            "biggest_risk": flags.get("biggest-risk", ""),
            "unverified": flags.get("unverified", ""),
            "score_total": "",
            "date": self.today.isoformat(),
            "discard_reason": "",
        }
        body = "## Blue Ocean\n\n" + "\n".join(blues) + "\n\n## Scores\n\n" + scores + "\n\n## Matrix\n\n## Pricing\n\n## Evidence\n"
        if meta["domain"] == "clinical":
            meta["knockout"] = "medicine-out-of-reach"
            meta["status"] = "needs review"
        self._write(self.ideation / "ideas" / f"{iid}.md", meta, body, self._cap("idea"))
        self._note_session_ids("session_ideas", iid)
        self._rebuild_index()
        return (
            f"Created {iid}. Trace it to {problems}. "
            "One idea per problem. Score every dimension in this turn, one CLI call per dimension."
        )

    def score(self, idea_id: str, dimension: str, value: str, source_note: str) -> str:
        path, kind = self._entity_path(idea_id)
        if kind != "ideas":
            raise DeskError("score applies to an idea id.")
        if dimension not in DIM_WEIGHT:
            raise DeskError("Unknown dimension. Use one of " + ", ".join(DIM_NAMES))
        if value == "" or value == "empty":
            number = None
        else:
            if not re.fullmatch(r"[0-5]", value or ""):
                raise DeskError("A score is an integer 0-5, or omit it to leave the dimension empty.")
            number = int(value)
        meta, body = self._read(path)
        session = self._open_session()
        if session:
            meta_s, body_s = self._load_session(session)
            if meta_s.get("hard_stopped") == "yes" or meta_s.get("status") != "open":
                raise DeskError("Session is closed. No further scoring.")
            if number is not None:
                passes = json.loads(meta_s.get("passes_json") or "{}")
                key = f"{idea_id}:{dimension}"
                current = self._score_map(body).get(dimension)
                used = 0 if current is None else int(passes.get(key, 0))
                cap = int(meta_s["limit_iterations_per_dimension"])
                if used + 1 > cap:
                    raise DeskError(f"Dimension pass cap reached for {dimension} ({cap}).")
                passes[key] = used + 1
                meta_s["passes_json"] = json.dumps(passes)
                self._write(session, meta_s, body_s, int(meta_s["limit_session_log_bytes"]))
        if dimension == "competitor_weakness" and number is not None and number > 2:
            self._enforce_wedge(meta)
        if dimension == "competitor_weakness" and number is not None and not meta.get("competitors"):
            raise DeskError("Competitor weakness stays empty until the idea links to competitor files.")
        if number is not None and not (source_note or "").strip():
            raise DeskError("A filled dimension needs --sources. Leave it empty instead of guessing.")
        body = self._replace_score_line(body, dimension, "empty" if number is None else str(number))
        if source_note:
            body = self._write_evidence(body, dimension, source_note)
        knockout = self._knockout_for(meta, dimension, number)
        if knockout:
            meta["knockout"] = knockout
        elif meta.get("knockout") and number not in {0, None}:
            if meta["knockout"] == self._knockout_for(meta, dimension, 0):
                meta["knockout"] = ""
        sticky = self._reach_knockout(meta)
        if sticky:
            meta["knockout"] = sticky
        total, status = self._refresh_status(meta, body)
        meta["score_total"] = "" if total is None else str(total)
        meta["status"] = status
        self._write(path, meta, body, self._cap("idea"))
        self._rebuild_index()
        shown = "empty" if number is None else str(number)
        rel = path.relative_to(self.root)
        return f"{rel} {idea_id} {dimension}={shown} status={status} total={meta['score_total'] or '-'}."

    def _enforce_wedge(self, meta: Dict[str, str]) -> None:
        if meta.get("crowdedness") not in CROWDED:
            return
        wedge = (meta.get("wedge") or "").strip()
        if not wedge:
            raise DeskError("Crowded or saturated space: competitor weakness cannot score above 2 without a wedge.")
        if meta.get("wedge_price_only") == "yes" and meta.get("wedge_cost_evidence") != "yes":
            raise DeskError("A price-only wedge needs sourced evidence that the cost structure can stay lower. Otherwise the score stays at 2 or below.")

    def _knockout_for(self, meta: Dict[str, str], dimension: str, number: Optional[int]) -> str:
        if number != 0:
            return ""
        if dimension == "willingness_to_pay":
            return "nobody-paying"
        if dimension == "reachability":
            return "no-channel"
        if dimension == "competitor_weakness":
            return "incumbent-no-weakness"
        if dimension == "platform_risk":
            return "platform-or-legal-block"
        if dimension == "trend" and meta.get("legal_duty") != "yes":
            return "trend-shrinking"
        if dimension == "fit":
            return "out-of-reach"
        return ""

    def _domain(self, raw: str) -> str:
        domain = (raw or "").strip().lower()
        if domain == "medicine":
            domain = "clinical"
        if domain and domain not in IDEA_DOMAINS:
            raise DeskError("idea --domain is trade, life, or clinical.")
        return domain

    def _reach_knockout(self, meta: Dict[str, str]) -> str:
        if (meta.get("domain") or "") in CLINICAL_DOMAINS:
            return "medicine-out-of-reach"
        return ""

    def _replace_score_line(self, body: str, dimension: str, shown: str) -> str:
        pattern = re.compile(rf"^{re.escape(dimension)}: .*$", re.M)
        if pattern.search(body):
            return pattern.sub(f"{dimension}: {shown}", body, count=1)
        return body + f"\n{dimension}: {shown}\n"

    def _score_map(self, body: str) -> Dict[str, Optional[int]]:
        found: Dict[str, Optional[int]] = {}
        for name in DIM_NAMES:
            match = re.search(rf"^{re.escape(name)}: (.+)$", body, re.M)
            raw = match.group(1).strip() if match else "empty"
            if raw == "empty":
                found[name] = None
            elif re.fullmatch(r"[0-5]", raw):
                found[name] = int(raw)
            else:
                found[name] = None
        return found

    def _refresh_status(self, meta: Dict[str, str], body: str) -> Tuple[Optional[int], str]:
        if meta.get("status") in {"approved", "rejected", "parked", "promoted", "discarded"}:
            scores = self._score_map(body)
            total = self._total(scores)
            return total, meta["status"]
        scores = self._score_map(body)
        sticky = self._reach_knockout(meta)
        if sticky:
            meta["knockout"] = sticky
            return self._total(scores), "needs review"
        if any(value is None for value in scores.values()):
            if all(value is None for value in scores.values()):
                return None, "draft"
            return None, "needs review"
        if meta.get("knockout"):
            return self._total(scores), "needs review"
        linked = [p.strip() for p in meta.get("problems", "").split(",") if p.strip()]
        if not linked:
            meta["knockout"] = meta.get("knockout") or "no-linked-problem"
            return self._total(scores), "needs review"
        for pid in linked:
            ppath = self.ideation / "problems" / f"{pid}.md"
            if not ppath.exists():
                meta["knockout"] = "no-linked-problem"
                return self._total(scores), "needs review"
            _pmeta, pbody = self._read(ppath)
            if self.independent_count(pbody) < 3:
                meta["knockout"] = "fewer-than-3-sources"
                return self._total(scores), "needs review"
        meta["knockout"] = ""
        return self._total(scores), "validated"

    def _total(self, scores: Dict[str, Optional[int]]) -> Optional[int]:
        if any(value is None for value in scores.values()):
            return None
        return sum(int(scores[name]) * DIM_WEIGHT[name] for name in DIM_NAMES)

    def add_competitor(self, flags: Dict[str, str]) -> str:
        self.seed()
        name = flags.get("name", "").strip()
        if not name:
            raise DeskError("competitor needs --name.")
        for meta in (self._read(path)[0] for path in self._files("competitors")):
            if meta.get("name", "").strip().lower() == name.lower():
                raise DeskError(f"{meta.get('id')} already stores {name}. Link the idea to that id.")
        cid = self._next_id("competitors", "C")
        meta = {
            "id": cid,
            "name": name,
            "url": flags.get("url", ""),
            "category": flags.get("category", ""),
            "tier": flags.get("tier", "unknown"),
            "last_checked": self.today.isoformat(),
        }
        fields = [
            "positioning",
            "segments",
            "offering",
            "pricing",
            "technology",
            "distribution",
            "penetration",
            "reviews",
            "funding",
            "age",
            "activity",
            "weaknesses",
        ]
        body = ""
        for field in fields:
            body += f"## {field}\n\ntag: unknown\nvalue: \nsource_url: \nsource_date: \n\n"
        self._write(self.ideation / "competitors" / f"{cid}.md", meta, body, self._cap("competitor"))
        self._rebuild_index()
        return f"Created {cid}. Fill fields with ./studio ideate field. Unknown stays unknown."

    def _competitor_field(self, path: Path, flags: Dict[str, str]) -> str:
        field = flags.get("field", "").strip()
        tag = flags.get("tag", "").strip()
        if tag not in {"verified", "inferred", "unknown"}:
            raise DeskError("field --tag must be verified, inferred, or unknown.")
        if tag != "unknown" and (not flags.get("url") or not flags.get("date")):
            raise DeskError("verified and inferred fields need --url and --date. Do not guess a fill.")
        meta, body = self._read(path)
        block = (
            f"## {field}\n\n"
            f"tag: {tag}\n"
            f"value: {(flags.get('value') or '').strip()}\n"
            f"source_url: {(flags.get('url') or '').strip()}\n"
            f"source_date: {(flags.get('date') or '').strip()}\n\n"
        )
        pattern = re.compile(rf"## {re.escape(field)}\n.*?(?=\n## |\Z)", re.S)
        if pattern.search(body):
            body = pattern.sub(block.rstrip() + "\n", body, count=1)
        else:
            body += "\n" + block
        if field == "penetration" and flags.get("tier"):
            meta["tier"] = flags["tier"]
        meta["last_checked"] = self.today.isoformat()
        self._write(path, meta, body, self._cap("competitor"))
        self._rebuild_index()
        return f"Updated {meta.get('id')} {field} as {tag}."

    def matrix(self, idea_id: str, feature: str, competitor: str, mark: str) -> str:
        path, kind = self._entity_path(idea_id)
        if kind != "ideas":
            raise DeskError("matrix applies to an idea.")
        if mark not in {"table stakes", "differentiator", "gap nobody covers"}:
            raise DeskError("matrix --mark must be 'table stakes', differentiator, or 'gap nobody covers'.")
        meta, body = self._read(path)
        line = f"- {feature} | {competitor} | {mark}\n"
        if "## Matrix" not in body:
            body += "\n## Matrix\n"
        body = body.replace("## Matrix\n", "## Matrix\n" + line, 1)
        self._write(path, meta, body, self._cap("idea"))
        return f"Matrix row added on {idea_id}."

    def _write_evidence(self, body: str, dimension: str, note: str) -> str:
        block = f"### {dimension}\n\n{note.strip()}\n"
        pattern = re.compile(rf"### {re.escape(dimension)}\n.*?(?=\n### |\n## |\Z)", re.S)
        shape_at = body.find("\n## Shape")
        head = body if shape_at < 0 else body[:shape_at]
        tail = "" if shape_at < 0 else body[shape_at:]
        if pattern.search(head):
            head = pattern.sub(block.rstrip() + "\n", head, count=1)
        else:
            if "## Evidence" not in head:
                head = head.rstrip() + "\n\n## Evidence\n"
            head = head.rstrip() + "\n\n" + block
        tail = pattern.sub("", tail)
        return head.rstrip() + "\n" + tail.lstrip("\n")

    def shape_missing(self, body: str) -> bool:
        return not all(heading in body for heading in ("## Shape",) + SHAPE_HEADINGS)

    def shape(self, idea_id: str, flags: Dict[str, str]) -> str:
        path, kind = self._entity_path(idea_id)
        if kind != "ideas":
            raise DeskError("shape applies to an idea.")
        parts: Dict[str, str] = {}
        for key in ("problem", "solution", "architecture", "experience", "steps", "mvp", "later"):
            value = flags.get(key) or ""
            if isinstance(value, list):
                value = " ".join(str(item) for item in value)
            value = str(value).strip()
            if not value:
                raise DeskError(f"shape needs --{key}.")
            parts[key] = value
        meta, body = self._read(path)
        block = (
            "## Shape\n\n"
            f"### Problem\n\n{parts['problem']}\n\n"
            f"### Solution\n\n{parts['solution']}\n\n"
            f"### Architecture\n\n{parts['architecture']}\n\n"
            f"### Experience\n\n{parts['experience']}\n\n"
            f"### Steps\n\n{parts['steps']}\n\n"
            f"### First chunk\n\n{parts['mvp']}\n\n"
            f"### Later chunks\n\n{parts['later']}\n"
        )
        blues = flags.get("blue")
        if isinstance(blues, str):
            blues = [blues]
        if isinstance(blues, list) and blues:
            body = re.sub(
                r"## Blue Ocean\n.*?(?=\n## |\Z)",
                "## Blue Ocean\n\n" + "\n".join(str(line) for line in blues) + "\n",
                body,
                count=1,
                flags=re.S,
            )
        pattern = re.compile(r"## Shape\n.*?(?=\n## |\Z)", re.S)
        if pattern.search(body):
            body = pattern.sub(block.rstrip() + "\n", body, count=1)
        else:
            body = body.rstrip() + "\n\n" + block
        if flags.get("closest"):
            meta["closest_product"] = str(flags["closest"]).strip()
        if flags.get("closest-price"):
            meta["closest_price"] = str(flags["closest-price"]).strip()
        if flags.get("title"):
            meta["title"] = str(flags["title"]).strip()
        if flags.get("pitch"):
            meta["pitch"] = str(flags["pitch"]).strip()
        self._write(path, meta, body, self._cap("idea"))
        self._note_session_ids("session_ideas", meta["id"])
        return f"Shape stored on {meta['id']}."

    def pricing(self, idea_id: str, unit: str, competitor: str, price: str) -> str:
        path, kind = self._entity_path(idea_id)
        if kind != "ideas":
            raise DeskError("pricing applies to an idea.")
        meta, body = self._read(path)
        line = f"- {unit} | {competitor} | {price}\n"
        if "## Pricing" not in body:
            body += "\n## Pricing\n"
        body = body.replace("## Pricing\n", "## Pricing\n" + line, 1)
        self._write(path, meta, body, self._cap("idea"))
        return f"Pricing row added on {idea_id}."

    def set_crowd(self, idea_id: str, flags: Dict[str, str]) -> str:
        path, kind = self._entity_path(idea_id)
        if kind != "ideas":
            raise DeskError("crowd applies to an idea.")
        meta, body = self._read(path)
        crowdedness = flags.get("class", "")
        if crowdedness not in {"open", "contested", "crowded", "saturated"}:
            raise DeskError("crowd --class must be open, contested, crowded, or saturated.")
        meta["crowdedness"] = crowdedness
        if "wedge" in flags:
            meta["wedge"] = flags["wedge"]
        if "wedge-price-only" in flags:
            meta["wedge_price_only"] = flags["wedge-price-only"]
        if "wedge-cost-evidence" in flags:
            meta["wedge_cost_evidence"] = flags["wedge-cost-evidence"]
        if "bundling-risk" in flags:
            meta["bundling_risk"] = flags["bundling-risk"]
        if "competitors" in flags:
            meta["competitors"] = flags["competitors"]
        self._write(path, meta, body, self._cap("idea"))
        self._rebuild_index()
        return f"{idea_id} crowdedness={crowdedness}."

    def _note_session_ids(self, key: str, entity_id: str) -> None:
        path = self._open_session()
        if path is None:
            return
        meta, body = self._read(path)
        current = [item.strip() for item in meta.get(key, "").split(",") if item.strip()]
        if entity_id not in current:
            current.append(entity_id)
        meta[key] = ",".join(current)
        cap = int(meta.get("limit_session_log_bytes") or "30720")
        self._write(path, meta, body, cap)

    def _ready_ideas(self, only_ids: Optional[List[str]] = None) -> List[str]:
        """One idea per problem, with three sourced lines, a competitor, and a two-sentence pitch."""
        allowed = set(only_ids or [])
        seen = set()
        ready: List[str] = []
        for path in self._files("ideas"):
            meta, _body = self._read(path)
            if allowed and meta.get("id") not in allowed:
                continue
            if meta.get("status") == "discarded":
                continue
            if not _two_sentences(meta.get("pitch", "")):
                continue
            if not [item for item in meta.get("competitors", "").split(",") if item.strip()]:
                continue
            pids = [item.strip() for item in meta.get("problems", "").split(",") if item.strip()]
            if not pids or pids[0] in seen:
                continue
            problem = self.ideation / "problems" / f"{pids[0]}.md"
            if not problem.exists():
                continue
            _pm, pbody = self._read(problem)
            if self.independent_count(pbody) < 3:
                continue
            seen.add(pids[0])
            ready.append(meta["id"])
        return ready

    def show(self, idea_id: str) -> str:
        path, kind = self._entity_path(idea_id)
        if kind != "ideas":
            raise DeskError("show applies to an idea id.")
        meta, body = self._read(path)
        rel = path.relative_to(self.root)
        return f"{rel}\n\n{meta.get('title')}\n{meta.get('pitch') or ''}\n\n{body}".rstrip() + "\n"

    def stop(self, reason: str) -> str:
        path = self._session_or_raise()
        meta, body = self._read(path)
        if meta.get("status") != "open":
            raise DeskError("This session is already closed.")
        meta["status"] = "stopped"
        note = (reason or "").strip() or "Stopped without a shortlist."
        body += f"\n## Checkpoint\n\nStopped without a shortlist. {note}\n"
        cap = int(meta.get("limit_session_log_bytes") or "30720")
        self._write(path, meta, body, cap)
        return f"Stopped {path.name}. No shortlist."

    def qualify(self, idea_id: str, fit: str, note: str) -> str:
        path = self._session_or_raise()
        session, _body = self._read(path)
        if session.get("status") != "open":
            raise DeskError("This session is closed.")
        stated = (session.get("hitl_market") or "").strip()
        choice = (fit or "").strip().lower()
        if choice not in MARKET_FITS:
            raise DeskError("qualify --fit must be applies, outside, or global.")
        if stated and choice == "global":
            raise DeskError("A market was stated. Use applies or outside.")
        if not stated and choice != "global":
            raise DeskError("No market was stated. Use global.")
        ipath, kind = self._entity_path(idea_id)
        if kind != "ideas":
            raise DeskError("qualify applies to an idea id.")
        meta, body = self._read(ipath)
        meta["market_fit"] = choice
        meta["market_note"] = (note or "").strip()
        self._write(ipath, meta, body, self._cap("idea"))
        return f"{meta['id']} market {choice}."

    def present(self) -> str:
        path = self._session_or_raise()
        meta, body = self._read(path)
        started = datetime.fromisoformat(meta["started_at"])
        elapsed = (self.now - started).total_seconds() / 60
        notes: List[str] = []
        incomplete = meta.get("hard_stopped") == "yes" or self._over_hard(meta) or elapsed >= int(meta["limit_minutes"])
        if incomplete:
            notes.append("budget reached")
        if int(meta.get("spent_searches") or "0") < 1:
            notes.append("no searches recorded")
            incomplete = True
        session_ideas = [item.strip() for item in meta.get("session_ideas", "").split(",") if item.strip()]
        stated = (meta.get("hitl_market") or "").strip()
        if stated:
            missing = []
            for iid in session_ideas:
                ipath = self.ideation / "ideas" / f"{iid}.md"
                if not ipath.exists():
                    missing.append(iid)
                    continue
                imeta, _ibody = self._read(ipath)
                if imeta.get("market_fit") not in {"applies", "outside"}:
                    missing.append(iid)
            if missing:
                notes.append("market not checked: " + ", ".join(missing))
                incomplete = True
        missing_shape = []
        for iid in session_ideas:
            ipath = self.ideation / "ideas" / f"{iid}.md"
            if not ipath.exists():
                continue
            imeta, ibody = self._read(ipath)
            if imeta.get("status") == "discarded":
                continue
            if self.shape_missing(ibody):
                missing_shape.append(iid)
        if missing_shape:
            notes.append("shape missing: " + ", ".join(missing_shape))
            incomplete = True
        self._write_shortlist(meta, incomplete=incomplete, notes=notes if incomplete else None)
        meta["shortlist_written"] = "yes"
        meta["status"] = "closed"
        meta["section"] = "present"
        body += "\n## Checkpoint\n\nShortlist written. Session stopped. Do not write a PRD.\n"
        self._write(path, meta, body, int(meta["limit_session_log_bytes"]))
        self._clear_scratch()
        name = f"{self.today.isoformat()}.md"
        if incomplete:
            return (
                f"Shortlist: ideation/shortlist/{name}. Incomplete ({'; '.join(notes)}). "
                "Session stopped. Waiting for approve, reject, or park."
            )
        return f"Shortlist: ideation/shortlist/{name}. Session stopped. Waiting for approve, reject, or park."

    def _write_shortlist(self, session_meta: Dict[str, str], incomplete: bool, notes: Optional[List[str]] = None) -> None:
        n = int(session_meta.get("limit_shortlist_n", "5"))
        misses_n = int(session_meta.get("limit_near_misses", "3"))
        ranked = []
        near = []
        only = [item.strip() for item in session_meta.get("session_ideas", "").split(",") if item.strip()]
        allowed = set(only)
        for path in self._files("ideas"):
            meta, body = self._read(path)
            if allowed and meta.get("id") not in allowed:
                continue
            if meta.get("status") == "discarded":
                continue
            total, status = self._refresh_status(meta, body)
            meta["status"] = status if meta.get("status") not in {"approved", "rejected", "parked", "promoted"} else meta["status"]
            if total is not None:
                meta["score_total"] = str(total)
            eligible = (
                status == "validated"
                and total is not None
                and total >= PROMOTE_MIN
                and meta.get("market_fit") != "outside"
            )
            record = (total if total is not None else -1, meta, body, status)
            if eligible:
                ranked.append(record)
            else:
                near.append(record)
        ranked.sort(key=lambda item: item[0], reverse=True)
        top = ranked[:n]
        overflow = ranked[n:]
        near.extend(overflow)
        near.sort(key=lambda item: item[0], reverse=True)
        chosen_misses = near[:misses_n]
        for _total, meta, body, status in top:
            if status == "validated":
                meta["status"] = "presented"
                self._write(self.ideation / "ideas" / f"{meta['id']}.md", meta, body, self._cap("idea"))
        lines = [f"# Shortlist {self.today.isoformat()}", ""]
        stated = (session_meta.get("hitl_market") or "").strip()
        if stated:
            lines.append(f"Stated market: {stated}. An idea qualifies only when sourced evidence shows the problem there.")
        else:
            lines.append("No market was stated. Ideas are judged globally.")
        lines.append("")
        if incomplete:
            lines.append("incomplete: " + "; ".join(notes or ["budget reached"]))
            lines.append("")
            lines.append("Not covered: any catalog row not marked searched in the session log.")
            lines.append("")
        lines.append(f"Top {n} need a validated total of at least {PROMOTE_MIN} (max {MAX_SCORE}).")
        lines.append("")
        if not top:
            lines.append("No idea is eligible.")
            lines.append("")
        for sort_total, meta, body, _status in top:
            lines.extend(self._short_block(meta, body, sort_total if sort_total >= 0 else None, miss=""))
        lines.append("## Near-misses")
        lines.append("")
        for sort_total, meta, body, status in chosen_misses:
            shown = sort_total if sort_total >= 0 else None
            if meta.get("market_fit") == "outside":
                reason = "does not apply to the stated market"
            else:
                reason = meta.get("knockout") or ("missing dimension" if status == "needs review" else f"total {shown if shown is not None else '-'} below {PROMOTE_MIN} or not validated")
                if status == "needs review" and not meta.get("knockout"):
                    empty = [name for name, value in self._score_map(body).items() if value is None]
                    reason = "missing dimension: " + ", ".join(empty) if empty else reason
            lines.extend(self._short_block(meta, body, shown, miss=reason))
        text = "\n".join(lines)
        dest = self.ideation / "shortlist" / f"{self.today.isoformat()}.md"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text, encoding="utf-8")
        self._rebuild_index()

    def _short_block(self, meta: Dict[str, str], body: str, total: Optional[int], miss: str) -> List[str]:
        scores = self._score_map(body)
        breakdown = ", ".join(
            f"{name}={'empty' if scores[name] is None else scores[name]}x{DIM_WEIGHT[name]}" for name in DIM_NAMES
        )
        problems = [p.strip() for p in meta.get("problems", "").split(",") if p.strip()]
        evidence = []
        for pid in problems:
            ppath = self.ideation / "problems" / f"{pid}.md"
            count = 0
            if ppath.exists():
                _pm, pbody = self._read(ppath)
                count = self.independent_count(pbody)
            evidence.append(f"{pid} ({count} independent)")
        comps = []
        for cid in [c.strip() for c in meta.get("competitors", "").split(",") if c.strip()][:3]:
            cpath = self.ideation / "competitors" / f"{cid}.md"
            if cpath.exists():
                cm, _cb = self._read(cpath)
                comps.append(f"{cm.get('name')} tier {cm.get('tier')} price see file")
            else:
                comps.append(cid)
        lines = [
            f"### {meta.get('title')} ({meta.get('id')})",
            "",
            f"- Shape: {meta.get('shape')} host: {meta.get('host') or '-'}",
            f"- Pitch: {meta.get('pitch') or '-'}",
            f"- Market: {meta.get('market_fit') or 'global'}"
            + (f" ({meta.get('market_note')})" if meta.get("market_note") else ""),
            f"- Problems: {', '.join(evidence) or '-'}",
            f"- Score: {total if total is not None else '-'} / {MAX_SCORE}",
            f"- Dimensions: {breakdown}",
            f"- Risk: {meta.get('biggest_risk') or '-'} Unverified: {meta.get('unverified') or '-'}",
            f"- Closest: {meta.get('closest_product') or '-'} at {meta.get('closest_price') or '-'}",
            f"- Crowdedness: {meta.get('crowdedness')} wedge: {meta.get('wedge') or '-'} bundling: {meta.get('bundling_risk') or '-'}",
            f"- Competitors: {', '.join(comps) or '-'}",
        ]
        if miss:
            lines.append(f"- Missed: {miss}")
        lines.append("")
        return lines

    def _clear_scratch(self) -> None:
        scratch = self.ideation / "scratch"
        if not scratch.exists():
            return
        for child in scratch.iterdir():
            if child.is_file():
                child.unlink()
            elif child.is_dir():
                shutil.rmtree(child)

    def approve(self, ids: List[str]) -> str:
        if not ids:
            raise DeskError("approve needs at least one idea id, in priority order.")
        day = self.today.isoformat()
        lines = [f"## {day}", ""]
        for rank, iid in enumerate(ids, start=1):
            path, kind = self._entity_path(iid)
            if kind != "ideas":
                raise DeskError("approve takes idea ids.")
            meta, body = self._read(path)
            _total, status = self._refresh_status(meta, body)
            if status not in {"validated", "presented"} and meta.get("status") not in {"validated", "presented"}:
                raise DeskError(f"{iid} is {meta.get('status') or status}, not validated or presented.")
            meta["status"] = "approved"
            meta["rank"] = str(rank)
            self._write(path, meta, body, self._cap("idea"))
            lines.append(f"{rank}. {iid}")
        lines.append("")
        approvals = self.ideation / "approvals.md"
        previous = approvals.read_text(encoding="utf-8") if approvals.exists() else "# Approvals\n\n"
        approvals.write_text(previous.rstrip() + "\n\n" + "\n".join(lines), encoding="utf-8")
        self._rebuild_index()
        return "Approved " + ", ".join(ids) + " in that rank order."

    def reject(self, idea_id: str, reason: str) -> str:
        return self._decide(idea_id, "rejected", reason, "reject")

    def park(self, idea_id: str, note: str) -> str:
        return self._decide(idea_id, "parked", note, "park")

    def _decide(self, idea_id: str, status: str, reason: str, label: str) -> str:
        if not reason.strip():
            raise DeskError(f"{label} needs a reason.")
        path, kind = self._entity_path(idea_id)
        if kind != "ideas":
            raise DeskError(f"{label} takes an idea id.")
        meta, body = self._read(path)
        meta["status"] = status
        meta["discard_reason"] = reason.strip()
        self._write(path, meta, body, self._cap("idea"))
        approvals = self.ideation / "approvals.md"
        previous = approvals.read_text(encoding="utf-8") if approvals.exists() else "# Approvals\n"
        approvals.write_text(previous.rstrip() + f"\n\n- {self.today.isoformat()} {status} {idea_id}: {reason.strip()}\n", encoding="utf-8")
        self._rebuild_index()
        return f"{idea_id} {status}: {reason.strip()}"

    def promote(self) -> str:
        approved = []
        for path in self._files("ideas"):
            meta, body = self._read(path)
            if meta.get("status") == "approved":
                approved.append((int(meta.get("rank") or "999"), path, meta, body))
        if not approved:
            raise DeskError("Nothing is approved. Promote refuses ideas that are not approved.")
        approved.sort(key=lambda item: item[0])
        written = []
        for _rank, path, meta, body in approved:
            total, status = self._refresh_status(dict(meta), body)
            if meta.get("knockout") or status != "validated" and meta.get("status") != "approved":
                pass
            scores = self._score_map(body)
            if any(value is None for value in scores.values()):
                raise DeskError(f"{meta['id']} still has an empty dimension. Promote refused.")
            if meta.get("knockout"):
                raise DeskError(f"{meta['id']} has knock-out {meta['knockout']}. Promote refused.")
            linked = [p.strip() for p in meta.get("problems", "").split(",") if p.strip()]
            if not linked:
                raise DeskError(f"{meta['id']} has no linked problem. Promote refused.")
            for pid in linked:
                ppath = self.ideation / "problems" / f"{pid}.md"
                if not ppath.exists():
                    raise DeskError(f"{meta['id']} links missing {pid}. Promote refused.")
                _pm, pbody = self._read(ppath)
                if self.independent_count(pbody) < 3:
                    raise DeskError(f"{pid} has fewer than 3 independent sourced lines. Promote refused.")
            if total is None or total < PROMOTE_MIN:
                raise DeskError(f"{meta['id']} total {total} is below {PROMOTE_MIN}. Promote refused.")
            gaps = self.prd_gaps(body)
            if gaps:
                raise DeskError(
                    f"{meta['id']} PRD is missing: {', '.join(gaps)}. "
                    "Write the full solution before promote."
                )
            slug = _slug(meta.get("title", meta["id"]))
            dest = self.intake / f"{slug}.md"
            if dest.exists():
                dest = self.intake / f"{slug}-{meta['id'].lower()}.md"
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(self._prd(meta, body), encoding="utf-8")
            meta["status"] = "promoted"
            meta["intake"] = str(dest.relative_to(self.root))
            self._write(path, meta, body, self._cap("idea"))
            written.append(f"{meta['id']} -> {meta['intake']}")
        self._rebuild_index()
        return "Promoted\n" + "\n".join(written) + "\nBootstrap is still a separate command."

    def _h3(self, body: str, title: str) -> str:
        match = re.search(rf"### {re.escape(title)}\n+(.*?)(?=\n### |\n## |\Z)", body, re.S)
        return match.group(1).strip() if match else ""

    def prd_gaps(self, body: str) -> List[str]:
        missing = []
        for title in ("Problem", "Steps", "First chunk", "Later chunks", *BUILD_HEADINGS):
            if len(self._h3(body, title)) < 80:
                missing.append(title)
        modules = self._h3(body, "Modules")
        if "Bootstrap focuses on" not in modules:
            missing.append("Modules: name the module bootstrap focuses on")
        if "Not in this module" not in modules:
            missing.append("Modules: say what is not in each module")
        return missing

    def build(self, idea_id: str, flags: Dict[str, object]) -> str:
        path, kind = self._entity_path(idea_id)
        if kind != "ideas":
            raise DeskError("build applies to an idea.")
        parts: Dict[str, str] = {}
        for key, title in (
            ("user", "User tasks"),
            ("system", "System tasks"),
            ("backend", "Backend"),
            ("infrastructure", "Infrastructure"),
            ("modules", "Modules"),
        ):
            value = flags.get(key) or ""
            if isinstance(value, list):
                value = " ".join(str(item) for item in value)
            value = str(value).strip()
            if len(value) < 80:
                raise DeskError(f"build --{key} must describe the full solution.")
            parts[title] = value
        modules = parts["Modules"]
        if "Bootstrap focuses on" not in modules or "Not in this module" not in modules:
            raise DeskError("build --modules must name the bootstrap module and what is not in each module.")
        meta, body = self._read(path)
        if "## Shape" not in body:
            raise DeskError("Shape the idea before writing the build.")
        block = "".join(f"\n### {title}\n\n{text}\n" for title, text in parts.items())
        for title in parts:
            body = re.sub(rf"### {re.escape(title)}\n.*?(?=\n### |\n## |\Z)", "", body, count=1, flags=re.S)
        body = body.rstrip() + "\n" + block
        self._write(path, meta, body, self._cap("idea"))
        return f"Build stored on {meta['id']}."

    def write_prd(self, idea_id: str) -> str:
        path, kind = self._entity_path(idea_id)
        if kind != "ideas":
            raise DeskError("prd applies to an idea.")
        meta, body = self._read(path)
        if meta.get("status") not in {"approved", "promoted"}:
            raise DeskError(f"{idea_id} is {meta.get('status')}. Approve it before writing the PRD.")
        gaps = self.prd_gaps(body)
        if gaps:
            raise DeskError(f"{idea_id} PRD is missing: {', '.join(gaps)}.")
        slug = _slug(meta.get("title", meta["id"]))
        dest = self.intake / f"{slug}.md"
        if meta.get("intake"):
            dest = self.root / meta["intake"]
        elif dest.exists():
            dest = self.intake / f"{slug}-{meta['id'].lower()}.md"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(self._prd(meta, body), encoding="utf-8")
        meta["intake"] = str(dest.relative_to(self.root))
        if meta.get("status") == "approved":
            meta["status"] = "promoted"
        self._write(path, meta, body, self._cap("idea"))
        self._rebuild_index()
        return f"{meta['id']} -> {meta['intake']}"

    def _prd(self, meta: Dict[str, str], body: str) -> str:
        shape = meta.get("shape") or "other"
        archetype = {
            "marketplace listing": "marketplace",
            "SaaS": "saas-application",
            "extension": "prototype",
            "mini web app": "prototype",
        }.get(shape, "prototype")
        problems = []
        evidence_bits = []
        for pid in [p.strip() for p in meta.get("problems", "").split(",") if p.strip()]:
            ppath = self.ideation / "problems" / f"{pid}.md"
            if not ppath.exists():
                continue
            pmeta, pbody = self._read(ppath)
            problems.append(pmeta.get("sentence") or pid)
            for line in self.evidence_lines(pbody):
                if line["verified"] == "yes":
                    evidence_bits.append(f"{line['source']} {line['url']} ({line['date']}): {line['paraphrase']}")
        pitch = meta.get("pitch") or meta.get("title")
        evidence = "\n".join("- " + bit for bit in evidence_bits) or "- No verified line."
        competitors = meta.get("competitors") or "none"
        closest = meta.get("closest_product") or "none"
        price = meta.get("closest_price") or "not recorded"
        sections = {title: self._h3(body, title) for title in (
            "Problem", "Solution", "Architecture", "Experience", "Steps",
            "First chunk", "Later chunks", *BUILD_HEADINGS,
        )}
        joined = " ".join(problems)
        def bullets(text: str) -> str:
            parts = [part.strip() for part in re.split(r"(?<=[.])\s+", text) if part.strip()]
            return "\n".join(f"  * {part}" for part in parts)
        user_bullets = bullets(sections["User tasks"])
        system_bullets = bullets(sections["System tasks"])
        arch = sections["Architecture"].strip()
        not_in_product = arch.split(". ")[0].rstrip(".") if arch else "Named in Architecture"
        if not_in_product.lower().startswith("do not "):
            not_in_product = not_in_product[7:]
        not_in_product = not_in_product[:1].upper() + not_in_product[1:] + "."
        bundling = (meta.get("bundling_risk") or "not recorded").rstrip(".")
        return f"""# PRD — {meta.get('title')}

> **Archetype & Complexity**
> * **Archetype:** {archetype}
> * **Complexity:** P0 is the first scope module. The full product is every module below.

---

## Title / Overview

{pitch}

The final goal is every module in Scope modules. Bootstrap builds the module that says bootstrap focuses on it, and does not start a later module until that module is done.

---

## Problem

{joined}

{sections['Problem']}

Linked idea file: ideation/ideas/{meta.get('id')}.md.

Evidence:

{evidence}

---

## Target Audience & Users

* **Primary audience:** {joined}
* **Jobs-to-be-done:**
{user_bullets}

---

## Goals & Success Criteria

* **North Star Metric:** {pitch}
* **KPIs:**
  * The first module is done when the user tasks named in that module are true.
  * A later module adds only what that module names.
  * The full product is done when every module is done.

---

## Scope

* **First build:** the module this PRD says bootstrap focuses on.
* **Rest of the product:** every later module in Scope modules. These are part of the product. They are not discarded.
* **Not in the product:** {not_in_product}

---

## Scope modules

{sections['Modules']}

---

## Requirements

### Functional Requirements

{sections['Steps']}

### User tasks

{user_bullets}

### System tasks

{system_bullets}

### Non-functional Requirements

* **Performance:** Work the system does in the background does not block the screen the person is using.
* **Usability:** The person does the user tasks. The system does the system tasks. The person can see which step is next.
* **Platforms:** Web app. Shape: {shape}.
* **Security:** The person signs in. Credentials and uploaded files are not public. Data leaves the system only on a step the person enabled.

---

## Backend

{sections['Backend']}

---

## Infrastructure

{sections['Infrastructure']}

---

## Monetization

* **Model:** The charge named on the idea. Neighboring price: {closest} at {price}.
* **Free tier:** Only if a module says so.
* **Pro tier:** The product described in the modules.

---

## Compliance & Legal

* **GDPR:** Personal data the product stores is named in Backend. A step that sends data to another party is named in the module that sends it.
* **Other:** Bundling risk: {bundling}. Platform risk stays on the idea file.

---

## Technology

* **Frontend:** Web app for the user tasks.
* **Backend:** Specified under Backend. Do not add a second backend in a later module.
* **Infrastructure:** Specified under Infrastructure. A later module adds only the piece that module names.
* **Deployment:** One web app the operator runs. Credentials stay on the server.

---

## Experience

{sections['Experience']}

{sections['Architecture']}

---

## Risks & Open Questions

* **Risk:** Starting a later module before the first module is done.
* **Risk:** {meta.get('biggest_risk') or 'A closer product may already ship a later module.'}
* **Open question:** {meta.get('unverified') or 'A vendor named inside a module is fixed. A vendor the module does not name is not chosen.'}

---

## Existing products

{sections['Solution']}

---

## References

* Idea {meta.get('id')} competitors {competitors}
* Closest existing product: {closest} at {price}
* Crowdedness: {meta.get('crowdedness')}
* Wedge: {meta.get('wedge') or 'not recorded'}
"""

    def propose(self, text: str) -> str:
        self.seed()
        if not text.strip():
            raise DeskError("propose needs the proposal text.")
        path = self.ideation / "rubric-proposals.md"
        previous = path.read_text(encoding="utf-8")
        path.write_text(previous.rstrip() + f"\n\n## {self.today.isoformat()}\n\n{text.strip()}\n", encoding="utf-8")
        return "Proposal appended. rubric.md was not changed."

    def apply_rubric(self, note: str) -> str:
        if not note.strip():
            raise DeskError("apply-rubric needs the approved change in --note.")
        path = self.ideation / "rubric.md"
        if not path.exists():
            self.seed()
        text = path.read_text(encoding="utf-8")
        text += f"\n\n## Changelog\n\n- {self.today.isoformat()}: {note.strip()}\n"
        path.write_text(text, encoding="utf-8")
        return "rubric.md changelog updated from an approved proposal."

    def import_incubator(self, db_path: Path) -> str:
        self.seed()
        if not db_path.exists():
            raise DeskError(f"Incubator database not found at {db_path}. Nothing imported.")
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        conn.row_factory = sqlite3.Row
        pains = conn.execute(
            "SELECT id, description, frequency, source_ids, created_at FROM pain_points"
        ).fetchall()
        created = 0
        skipped = 0
        for pain in pains:
            sourced = self._incubator_sources(conn, pain)
            if not sourced:
                skipped += 1
                continue
            sentence = re.sub(r"\s+", " ", (pain["description"] or "")).strip()[:180]
            words = [w.lower() for w in re.findall(r"[a-zA-Z]{4,}", sentence)][:5]
            while len(words) < 3:
                words.append("imported")
            if self.find_duplicate(sentence, ", ".join(words[:5])):
                skipped += 1
                continue
            message = self.add_problem(
                {
                    "sentence": sentence.replace("|", "/"),
                    "keywords": ", ".join(words[:5]),
                    "segment": "imported",
                    "category": "incubator",
                    "region": "",
                    "language": "",
                }
            )
            pid = message.split()[1].rstrip(".")
            for row in sourced:
                self.add_evidence(
                    pid,
                    {
                        "source": row["source"],
                        "url": row["url"],
                        "date": row["date"],
                        "count": str(pain["frequency"] or 1),
                        "paraphrase": sentence[:PARAPHRASE_MAX],
                        "author": row["author"],
                        "thread": row["thread"],
                    },
                )
            created += 1
        conn.close()
        return f"Imported {created} sourced pains. Skipped {skipped} unsourced or duplicate rows."

    def _incubator_sources(self, conn: sqlite3.Connection, pain: sqlite3.Row) -> List[Dict[str, str]]:
        raw = (pain["source_ids"] or "").strip()
        refs: List[Tuple[str, str]] = []
        if raw.startswith("http"):
            refs.append(("url", raw))
        else:
            try:
                parsed = json.loads(raw or "[]")
            except json.JSONDecodeError:
                parsed = []
            if isinstance(parsed, list):
                refs.extend(("id", str(item)) for item in parsed)
        found = []
        for kind, value in refs:
            if kind == "id":
                row = conn.execute(
                    "SELECT source_url, date_posted, scraped_at, author, source_type, title FROM raw_signals WHERE id = ?",
                    (value,),
                ).fetchone()
            else:
                row = conn.execute(
                    "SELECT source_url, date_posted, scraped_at, author, source_type, title FROM raw_signals WHERE source_url = ?",
                    (value,),
                ).fetchone()
            url = ""
            date = ""
            author = ""
            source = "incubator"
            thread = value
            if row:
                url = (row["source_url"] or value or "").strip()
                date = ((row["date_posted"] or row["scraped_at"] or "")[:10])
                author = (row["author"] or "").strip()
                source = row["source_type"] or source
                thread = row["title"] or url
            elif kind == "url":
                url = value
            if not date:
                date = (pain["created_at"] or "")[:10]
            if not url.startswith("http") or not _parse_day(date):
                continue
            found.append(
                {
                    "url": url,
                    "date": date,
                    "author": author,
                    "source": source,
                    "thread": thread or url,
                }
            )
        return found


def _multi_flags(args: List[str]) -> Tuple[List[str], Dict[str, object]]:
    positional: List[str] = []
    flags: Dict[str, object] = {}
    multi = {"blue"}
    i = 0
    while i < len(args):
        arg = args[i]
        if arg.startswith("--"):
            key = arg[2:]
            if i + 1 < len(args) and not args[i + 1].startswith("--"):
                value: object = args[i + 1]
                i += 2
            else:
                value = "yes"
                i += 1
            if key in multi:
                current = flags.get(key, [])
                if not isinstance(current, list):
                    current = [current]
                current.append(value)
                flags[key] = current
            else:
                flags[key] = value
        else:
            positional.append(arg)
            i += 1
    return positional, flags


def dispatch(argv: List[str], root: Optional[Path] = None, templates: Optional[Path] = None, today: Optional[date] = None, now: Optional[datetime] = None) -> Tuple[int, str]:
    desk = Desk(root or repo_root(), templates or template_dir(), today=today, now=now)
    if argv and argv[0] in {"-h", "--help", "help"}:
        return 0, (
            "Usage:\n"
            "  ./studio ideate [focus] --budget small|normal|large\n"
            "  ./studio ideate status\n"
            "  ./studio ideate search --source <row> --outcome new|empty\n"
            "  ./studio ideate fetch\n"
            "  ./studio ideate checkpoint --step signals|cluster|ideas|compete|shape|score|present|learn\n"
            "  ./studio ideate problem --sentence \"...\" --keywords \"a, b, c\"\n"
            "  ./studio ideate deepen <P-id|I-id> --source --url --date --paraphrase --author [--thread]\n"
            "  ./studio ideate idea --title \"...\" --problems P-001 --shape extension --domain trade|life|clinical\n"
            "  ./studio ideate competitor --name \"...\"\n"
            "  ./studio ideate field <C-id> --field pricing --tag verified|inferred|unknown --value \"...\"\n"
            "  ./studio ideate shape <I-id> --problem \"...\" --solution \"...\" --architecture \"...\" --experience \"...\" --steps \"...\" --mvp \"...\" --later \"...\"\n"
            "  ./studio ideate score <I-id> --dimension willingness_to_pay --value 0-5 --sources \"...\"\n"
            "  ./studio ideate qualify <I-id> --fit applies|outside|global --note \"...\"\n"
            "  ./studio ideate show <I-id>\n"
            "  ./studio ideate stop --reason \"...\"\n"
            "  ./studio ideate present\n"
            "  ./studio ideate approve <I-id> [<I-id> ...]\n"
            "  ./studio ideate reject <I-id> --reason \"...\"\n"
            "  ./studio ideate park <I-id> --note \"...\"\n"
            "  ./studio ideate build <I-id> --user \"...\" --system \"...\" --backend \"...\" --infrastructure \"...\" --modules \"...\"\n"
            "  ./studio ideate prd <I-id>\n"
            "  ./studio ideate promote\n"
            "  ./studio ideate import-incubator [--db path]\n"
        )
    positional, flags = _multi_flags(argv)
    command = positional[0] if positional else "start"
    rest = positional[1:]
    try:
        if command == "start" or command not in {
            "status",
            "search",
            "fetch",
            "checkpoint",
            "recluster",
            "problem",
            "deepen",
            "idea",
            "competitor",
            "field",
            "score",
            "qualify",
            "show",
            "stop",
            "matrix",
            "pricing",
            "shape",
            "crowd",
            "present",
            "approve",
            "reject",
            "park",
            "build",
            "prd",
            "promote",
            "discard",
            "propose",
            "apply-rubric",
            "import-incubator",
        }:
            focus_parts = positional
            if command == "start":
                focus_parts = rest
            focus = " ".join(focus_parts)
            tier = str(flags.get("budget") or "normal")
            message = desk.start(focus, tier, {k: str(v) for k, v in flags.items() if not isinstance(v, list)}, flags.get("new") == "yes")
        elif command == "status":
            message = desk.status()
        elif command == "search":
            message = desk.search(str(flags.get("source") or ""), str(flags.get("outcome") or ""))
        elif command == "fetch":
            message = desk.fetch()
        elif command == "checkpoint":
            message = desk.checkpoint(str(flags.get("step") or ""))
        elif command == "recluster":
            message = desk.recluster()
        elif command == "problem":
            message = desk.add_problem({k: str(v) for k, v in flags.items()})
        elif command == "deepen":
            if not rest:
                raise DeskError("deepen needs an id.")
            message = desk.add_evidence(rest[0], {k: str(v) for k, v in flags.items()})
        elif command == "idea":
            message = desk.add_idea(flags)
        elif command == "competitor":
            message = desk.add_competitor({k: str(v) for k, v in flags.items()})
        elif command == "field":
            if not rest:
                raise DeskError("field needs a competitor id.")
            path, _kind = desk._entity_path(rest[0])
            message = desk._competitor_field(path, {k: str(v) for k, v in flags.items()})
        elif command == "score":
            if not rest:
                raise DeskError("score needs an idea id.")
            message = desk.score(rest[0], str(flags.get("dimension") or ""), str(flags.get("value") or ""), str(flags.get("sources") or ""))
        elif command == "qualify":
            if not rest:
                raise DeskError("qualify needs an idea id.")
            message = desk.qualify(rest[0], str(flags.get("fit") or ""), str(flags.get("note") or ""))
        elif command == "show":
            if not rest:
                raise DeskError("show needs an idea id.")
            message = desk.show(rest[0])
        elif command == "stop":
            message = desk.stop(str(flags.get("reason") or ""))
        elif command == "matrix":
            message = desk.matrix(str(flags.get("idea") or (rest[0] if rest else "")), str(flags.get("feature") or ""), str(flags.get("competitor") or ""), str(flags.get("mark") or ""))
        elif command == "pricing":
            message = desk.pricing(str(flags.get("idea") or (rest[0] if rest else "")), str(flags.get("unit") or ""), str(flags.get("competitor") or ""), str(flags.get("price") or ""))
        elif command == "shape":
            if not rest:
                raise DeskError("shape needs an idea id.")
            message = desk.shape(rest[0], flags)
        elif command == "crowd":
            if not rest:
                raise DeskError("crowd needs an idea id.")
            message = desk.set_crowd(rest[0], {k: str(v) for k, v in flags.items()})
        elif command == "present":
            message = desk.present()
        elif command == "approve":
            message = desk.approve(rest)
        elif command == "reject":
            if not rest:
                raise DeskError("reject needs an idea id.")
            message = desk.reject(rest[0], str(flags.get("reason") or ""))
        elif command == "park":
            if not rest:
                raise DeskError("park needs an idea id.")
            message = desk.park(rest[0], str(flags.get("note") or ""))
        elif command == "build":
            if not rest:
                raise DeskError("build needs an idea id.")
            message = desk.build(rest[0], flags)
        elif command == "prd":
            if not rest:
                raise DeskError("prd needs an idea id.")
            message = desk.write_prd(rest[0])
        elif command == "promote":
            message = desk.promote()
        elif command == "discard":
            if not rest:
                raise DeskError("discard needs an id.")
            message = desk.discard(rest[0], str(flags.get("reason") or ""))
        elif command == "propose":
            message = desk.propose(str(flags.get("text") or ""))
        elif command == "apply-rubric":
            message = desk.apply_rubric(str(flags.get("note") or ""))
        elif command == "import-incubator":
            db = Path(str(flags.get("db") or "/Users/kalle/Documents/Projects/incubator/incubator.db"))
            message = desk.import_incubator(db)
        else:
            message = "Unknown ideate command."
            return 2, message
        return 0, message
    except DeskError as exc:
        return 2, str(exc)
    except Exception as exc:
        return 2, f"{type(exc).__name__}: {exc}"
