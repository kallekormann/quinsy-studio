#!/usr/bin/env python3
"""Tests for ticket_ids.scan_max_ticket_number / allocate_ticket_id."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))

import ticket_ids  # noqa: E402


@pytest.fixture()
def project_backlog(tmp_path, monkeypatch):
    projects = tmp_path / "projects"
    proj = projects / "acme"
    backlog = proj / "backlog"
    backlog.mkdir(parents=True)
    (backlog / "done").mkdir()
    (backlog / "open").mkdir()
    monkeypatch.setattr(ticket_ids, "PROJECTS_DIR", projects)
    return proj, backlog


def test_scan_includes_root_level_tickets(project_backlog):
    proj, backlog = project_backlog
    (backlog / "done" / "ACME-0007-done.md").write_text("# done\n")
    (backlog / "ACME-0519-root.md").write_text("# root\n")  # amendment-style
    assert ticket_ids.scan_max_ticket_number("acme") == 519


def test_allocate_after_root_level_does_not_collide(project_backlog):
    proj, backlog = project_backlog
    (backlog / "ACME-0508-freeze.md").write_text("# a\n")
    (backlog / "ACME-0520-feedback.md").write_text("# b\n")
    tid = ticket_ids.allocate_ticket_id("acme")
    assert tid == "ACME-0521"
    assert (proj / ".ticket_counter").read_text().strip() == "521"


def test_status_dirs_still_counted(project_backlog):
    _, backlog = project_backlog
    (backlog / "open" / "ACME-0042-open.md").write_text("# o\n")
    (backlog / "done" / "ACME-0099-done.md").write_text("# d\n")
    assert ticket_ids.scan_max_ticket_number("acme") == 99
