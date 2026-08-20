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


if __name__ == "__main__":
    test_find_similar_feedback()
    print("ok")
