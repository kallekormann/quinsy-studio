#!/usr/bin/env python3
"""Tests for product backlog layout."""

import tempfile
from pathlib import Path

from backlog_paths import (
    QUEUE_STATUS,
    list_unscheduled_backlog,
    migrate_legacy_backlog,
    queue_ticket_paths,
)


def test_migrate_open_to_backlog_root():
    with tempfile.TemporaryDirectory() as tmp:
        project = "testproj"
        root = Path(tmp) / "projects" / project / "backlog"
        open_dir = root / "open"
        open_dir.mkdir(parents=True)
        ticket = open_dir / "TEST-0001-sample.md"
        ticket.write_text(
            "---\nid: TEST-0001\nstatus: open\ntitle: Sample\ncreated: 2026-01-01\n---\n",
            encoding="utf-8",
        )

        import backlog_paths as bp

        old_projects = bp.PROJECTS_DIR
        bp.PROJECTS_DIR = Path(tmp) / "projects"
        try:
            actions = migrate_legacy_backlog(project)
            assert any("open/" in a for a in actions)
            assert (root / "TEST-0001-sample.md").exists()
            assert not open_dir.exists() or not list(open_dir.glob("*.md"))
        finally:
            bp.PROJECTS_DIR = old_projects
