#!/usr/bin/env python3
"""Tests for sprint feedback deduplication."""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from sprint_hitl import (  # noqa: E402
    add_feedback,
    find_similar_feedback,
    load_feedback_queue,
    save_feedback_queue,
)


def test_find_similar_feedback():
    with tempfile.TemporaryDirectory() as tmp:
        project = "testproj"
        sprint = "SPRINT-01"
        import sprint_hitl as sh

        sh.PROJECTS_DIR = Path(tmp) / "projects"
        sh.save_feedback_queue(
            project,
            sprint,
            [
                {
                    "id": "FB-001",
                    "status": "raw",
                    "raw": "Confetti animation on task complete; better add remove motion",
                },
            ],
        )
        dup = find_similar_feedback(
            project,
            sprint,
            "Sprint review: burst needs confetti; add remove task transformation animation",
        )
        assert dup is not None
        assert dup["id"] == "FB-001"


def test_drain_note_becomes_fb():
    with tempfile.TemporaryDirectory() as tmp:
        import sprint_hitl as sh
        import ticket_ids
        import backlog_paths
        from studio_human_inbox import append_note
        from studio_feedback_loop import process_feedback_queue

        root = Path(tmp) / "projects"
        sh.PROJECTS_DIR = root
        ticket_ids.PROJECTS_DIR = root
        backlog_paths.PROJECTS_DIR = root
        (root / "testproj" / "sprints" / "SPRINT-01").mkdir(parents=True)
        append_note(
            "testproj",
            "SPRINT-01",
            "Empty state on /commands when there are no jobs: show a Create job CTA.",
        )
        result = process_feedback_queue("testproj", "SPRINT-01")
        ids = {i["id"] for i in load_feedback_queue("testproj", "SPRINT-01")}
        assert ids
        assert result["action"] in ("hitl", "ticketed")


if __name__ == "__main__":
    test_find_similar_feedback()
    test_drain_note_becomes_fb()
    print("ok")
