#!/usr/bin/env python3
"""
ticket_ids.py — Unified ticket ID allocation for Quinsy Studio.
"""

import re
from pathlib import Path

STUDIO_ROOT = Path(__file__).parent.parent.parent
PROJECTS_DIR = STUDIO_ROOT / "projects"


def _project_prefix(project: str) -> str:
    return project[:4].upper()


def scan_max_ticket_number(project: str) -> int:
    """Return the highest ticket number in use for a project.

    Scans:
    - backlog/<status>/{PREFIX}-*.md  (open, done, implement, …)
    - backlog/{PREFIX}-*.md           (root-level / unscheduled / amendment materialize)
    - .ticket_counter                 (monotonic floor)
    """
    prefix = _project_prefix(project)
    max_num = 0
    backlog = PROJECTS_DIR / project / "backlog"
    if backlog.exists():
        # Root-level tickets (amendment materialize, unscheduled feedback tickets)
        for ticket_file in backlog.glob(f"{prefix}-*.md"):
            match = re.match(rf"{re.escape(prefix)}-(\d+)", ticket_file.name)
            if match:
                max_num = max(max_num, int(match.group(1)))
        # Status-folder tickets
        for status_dir in backlog.iterdir():
            if not status_dir.is_dir():
                continue
            for ticket_file in status_dir.glob(f"{prefix}-*.md"):
                match = re.match(rf"{re.escape(prefix)}-(\d+)", ticket_file.name)
                if match:
                    max_num = max(max_num, int(match.group(1)))
    counter_file = PROJECTS_DIR / project / ".ticket_counter"
    if counter_file.exists():
        try:
            max_num = max(max_num, int(counter_file.read_text().strip()))
        except ValueError:
            pass
    return max_num


def set_ticket_counter(project: str, count: int) -> None:
    counter_file = PROJECTS_DIR / project / ".ticket_counter"
    counter_file.parent.mkdir(parents=True, exist_ok=True)
    counter_file.write_text(str(count))


def get_ticket_counter(project: str) -> int:
    return scan_max_ticket_number(project)


def allocate_ticket_id(project: str) -> str:
    next_num = scan_max_ticket_number(project) + 1
    set_ticket_counter(project, next_num)
    return f"{_project_prefix(project)}-{next_num:04d}"


def assign_sequential_ids(tickets: list, project: str) -> list:
    prefix = _project_prefix(project)
    start = scan_max_ticket_number(project)
    id_map = {}
    counter = start
    for ticket in tickets:
        old_id = ticket["id"]
        counter += 1
        new_id = f"{prefix}-{counter:04d}"
        id_map[old_id] = new_id
        ticket["id"] = new_id
    for ticket in tickets:
        ticket["dependencies"] = [id_map.get(dep, dep) for dep in ticket.get("dependencies", [])]
    set_ticket_counter(project, counter)
    return tickets
