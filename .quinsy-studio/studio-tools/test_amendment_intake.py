#!/usr/bin/env python3
"""Tests for amendment intake scaffolding."""

import json
import sys
from pathlib import Path

TOOLS = Path(__file__).parent
sys.path.insert(0, str(TOOLS))

import amendment_intake as ai  # noqa: E402


SAMPLE_BRIEF = """# Amendment brief — Agency positioning

## 8. Team selection

- [x] **01 — Frontend Experience**
- [x] **10 — Product Design & Experience**

## 9. Skill selection

- [x] **FE-001** UI Component Design
- [x] **UX-001** Product design / user flows
"""


def test_parse_teams_and_skills():
    teams, skills = ai.parse_teams_and_skills(SAMPLE_BRIEF)
    assert any("01" in t for t in teams)
    assert "FE-001" in skills
    assert "UX-001" in skills


def test_next_amendment_id():
    reg = {"amendments": [{"id": "AM-001"}, {"id": "AM-003"}]}
    assert ai.next_amendment_id(reg) == "AM-004"


def test_validate_brief_rejects_milestones():
    bad = SAMPLE_BRIEF + "\nmilestone: M6\n"
    ok, errors, _warnings = ai.validate_brief(bad)
    assert not ok
    assert errors


def test_scaffold_amendment():
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        studio_root = Path(tmp)
        project = "testproj"
        projects = studio_root / "projects" / project
        projects.mkdir(parents=True)
        intake = studio_root / "intake" / "amendments" / project
        intake.mkdir(parents=True)
        brief = intake / "amendment_01.md"
        brief.write_text(SAMPLE_BRIEF, encoding="utf-8")

        old_root = ai.STUDIO_ROOT
        old_projects = ai.PROJECTS_DIR
        old_intake = ai.INTAKE_AMENDMENTS_DIR
        try:
            ai.STUDIO_ROOT = studio_root
            ai.PROJECTS_DIR = studio_root / "projects"
            ai.INTAKE_AMENDMENTS_DIR = studio_root / "intake" / "amendments"
            ok, folder, meta = ai.scaffold_amendment(project, brief)
        finally:
            ai.STUDIO_ROOT = old_root
            ai.PROJECTS_DIR = old_projects
            ai.INTAKE_AMENDMENTS_DIR = old_intake

        assert ok, folder
        assert meta is not None
        assert meta["id"] == "AM-001"
        am_dir = projects / "docs" / "amendments" / folder
        assert (am_dir / "source.md").exists()
        assert (am_dir / "03-milestone-roadmap.md").exists()
        reg = json.loads((projects / "docs" / "amendments" / "registry.json").read_text())
        assert len(reg["amendments"]) == 1


if __name__ == "__main__":
    test_parse_teams_and_skills()
    test_next_amendment_id()
    test_validate_brief_rejects_milestones()
    test_scaffold_amendment()
    print("ok")
