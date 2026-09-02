#!/usr/bin/env python3
"""Tests for design_ticket_helpers placement gate."""

from design_ticket_helpers import (
    design_spec_has_in_context_mocks_section,
    design_spec_has_placement_section,
    infer_ticket_type,
)


def test_infer_ia_feature_placement():
    assert infer_ticket_type("Move presentation link to presentation builder") == "ia-feature-placement"
    assert infer_ticket_type("Fix export button alignment") == "feature"


def test_infer_design_brief_title_and_scope():
    assert (
        infer_ticket_type("Design: board multiselect floating bar (extension Capture Mode style)")
        == "ui-composition"
    )
    assert (
        infer_ticket_type(
            "Team 10 design spec + in-context mock for board canvas multiselect floating pill"
        )
        == "ui-composition"
    )


def test_placement_section_detected():
    spec = """
## 1. Summary
Problem.

## 2. Context & placement

### User intent & surface

| Field | Value |
| **Primary intent** | Ship client narrative |
| **Home surface** | Presentation builder aside |
| **Why not elsewhere** | Share is for collaborators |

## 3. Atomic inventory
"""
    assert design_spec_has_placement_section(spec)


def test_placement_section_missing():
    assert not design_spec_has_placement_section("## 1. Summary\nOnly summary.\n")


def test_in_context_mocks_detected():
    spec = """
## 2c. Experienceable in-context mocks

| Field | Value |
|-------|-------|
| **Shell / surface** | Board canvas chrome + Inbox rail |
| **Mock assets** | docs/design-specs/mocks/MOOD-0190/dialog-in-board.png |
| **States shown** | empty, open, error |
| **Anti-orphan check** | Board header and canvas edge visible in frame |

## 3. Atomic inventory
"""
    assert design_spec_has_in_context_mocks_section(spec)


def test_in_context_mocks_missing():
    assert not design_spec_has_in_context_mocks_section(
        "## 1. Summary\nNo mocks section.\n## 2. Context & placement\nDone.\n"
    )


def test_emoji_icon_warning_none_without_mocks(tmp_path):
    from design_ticket_helpers import design_mocks_emoji_icon_warning
    assert design_mocks_emoji_icon_warning(tmp_path, "T-1") is None


def test_emoji_icon_warning_flags_btn_emoji(tmp_path):
    from design_ticket_helpers import design_mocks_emoji_icon_warning
    d = tmp_path / "docs" / "design-specs" / "mocks" / "T-1"
    d.mkdir(parents=True)
    (d / "x.html").write_text('<button class="btn icon">🎨</button>', encoding="utf-8")
    warn = design_mocks_emoji_icon_warning(tmp_path, "T-1")
    assert warn and "LO-0037" in warn
