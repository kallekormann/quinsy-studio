#!/usr/bin/env python3
"""Tests for design_ticket_helpers placement gate."""

from design_ticket_helpers import (
    design_deliverables_status,
    design_implement_blocked_message,
    design_spec_completeness_error,
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


def test_infer_i18n_catalog_ac_stays_feature():
    blob = (
        "Authentication & Authorization\n"
        "Visible copy uses catalogs for de, en, es, fr, it, pt, pl. "
        "No UI string is hardcoded. See `docs/i18n.md`.\n"
        "A registered user logs in."
    )
    assert infer_ticket_type(blob) == "feature"
    from design_ticket_helpers import is_commercial_surface

    assert not is_commercial_surface(blob)


def test_infer_identity_fixture_stays_feature():
    assert (
        infer_ticket_type(
            "Command Center chrome drops kit demo identity. GitHub kit menus still show demo profiles."
        )
        == "feature"
    )


def test_feature_chrome_is_not_backend_only():
    from design_ticket_helpers import tickets_are_backend_only

    assert not tickets_are_backend_only(
        [{"ticket_type": "feature", "title": "Command Center chrome drops kit demo identity"}]
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


def test_missing_spec_file_is_completeness_error():
    import tempfile
    from pathlib import Path
    with tempfile.TemporaryDirectory() as raw:
        tmp_path = Path(raw)
        err = design_spec_completeness_error(
            tmp_path / "docs" / "design-specs" / "DEMO-0001.md",
            tmp_path,
            "DEMO-0001",
            "ui-composition",
        )
        assert err and "does not exist" in err


def test_stub_spec_is_write_not_approve():
    import tempfile
    from pathlib import Path
    with tempfile.TemporaryDirectory() as raw:
        tmp_path = Path(raw)
        spec = tmp_path / "docs" / "design-specs" / "DEMO-0001.md"
        spec.parent.mkdir(parents=True)
        spec.write_text("# Design spec — DEMO-0001\n\n**Status:** stub — fill me\n", encoding="utf-8")
        ticket = (
            "ticket_type: ui-composition\n"
            "design_status: pending\n"
            "design_spec: docs/design-specs/DEMO-0001.md\n"
        )
        status, msg = design_deliverables_status(tmp_path, "DEMO-0001", ticket)
        assert status == "write"
        assert msg and "approve-design" in msg
        assert "Do **not** run" in msg


def _filled_spec() -> str:
    return """
## 1. Summary
Ship the filter bar on the command list.

## 2. Context & placement

### User intent & surface

| Field | Value |
|-------|-------|
| **Primary intent** | Filter jobs on the command list |
| **Home surface** | /commands list inside app chrome |
| **Why not elsewhere** | Settings is the wrong context |

## 2c. Experienceable in-context mocks

| Field | Value |
|-------|-------|
| **Shell / surface** | Command list with app sidebar + top nav |
| **Mock assets** | docs/design-specs/mocks/DEMO-0001/list.html |
| **States shown** | rest/up, hover, pressed/down, disabled/inactive, focus, open, closed, empty, loading, error |
| **Anti-orphan check** | Sidebar and list header visible in the mock |
| **Project tokens** | ui/tokens/design-tokens.css |

## 2d. Motion

Filter menu opens in 250ms and closes in 150ms (`--motion-duration-fast` / `--motion-duration-quick`), ease smooth-out.
Reduced-motion: same menu, durations at 0ms.

## 3. Atomic inventory

| Level | Name | Library source | New? |
| atom | Button | pull: button | no |
| molecule | Dropdown | pull: dropdown-menu | no |
"""


def test_filled_spec_without_token_mocks_fails():
    import tempfile
    from pathlib import Path
    with tempfile.TemporaryDirectory() as raw:
        tmp_path = Path(raw)
        spec = tmp_path / "docs" / "design-specs" / "DEMO-0001.md"
        spec.parent.mkdir(parents=True)
        spec.write_text(_filled_spec(), encoding="utf-8")
        err = design_spec_completeness_error(spec, tmp_path, "DEMO-0001", "ui-composition")
        assert err and "mocks" in err.lower()


def test_filled_spec_with_token_all_state_mocks_passes():
    import tempfile
    from pathlib import Path
    with tempfile.TemporaryDirectory() as raw:
        tmp_path = Path(raw)
        spec = tmp_path / "docs" / "design-specs" / "DEMO-0001.md"
        spec.parent.mkdir(parents=True)
        spec.write_text(_filled_spec(), encoding="utf-8")
        mock = tmp_path / "docs" / "design-specs" / "mocks" / "DEMO-0001" / "list.html"
        mock.parent.mkdir(parents=True)
        mock.write_text(
            """<!doctype html>
<link rel="stylesheet" href="../../../../ui/tokens/design-tokens.css">
<!-- in-context: sidebar + command list -->
<button data-state="rest">Filter</button>
<button data-state="hover">Filter</button>
<button data-state="pressed">Filter</button>
<button disabled data-state="disabled">Filter</button>
<button data-state="focus">Filter</button>
<div data-state="closed">dropdown closed</div>
<div data-state="open">dropdown open</div>
<div data-state="empty">empty</div>
<div data-state="loading">loading</div>
<div data-state="error">error</div>
<div style="background: var(--background); color: var(--foreground)">shell</div>
""",
            encoding="utf-8",
        )
        err = design_spec_completeness_error(spec, tmp_path, "DEMO-0001", "ui-composition")
        assert err is None
        ticket = (
            "ticket_type: ui-composition\n"
            "design_status: pending\n"
            "design_spec: docs/design-specs/DEMO-0001.md\n"
        )
        status, msg = design_deliverables_status(tmp_path, "DEMO-0001", ticket)
        assert status == "approve"
        assert msg is None


def test_ia_navigation_missing_metrics_fails():
    import tempfile
    from pathlib import Path

    with tempfile.TemporaryDirectory() as raw:
        tmp_path = Path(raw)
        spec = tmp_path / "docs" / "design-specs" / "DEMO-IA.md"
        spec.parent.mkdir(parents=True)
        spec.write_text(_filled_spec(), encoding="utf-8")
        mock = tmp_path / "docs" / "design-specs" / "mocks" / "DEMO-IA" / "list.html"
        mock.parent.mkdir(parents=True)
        mock.write_text(
            """<!doctype html>
<link rel="stylesheet" href="../../../../ui/tokens/design-tokens.css">
<button data-state="rest">Nav</button>
<button data-state="hover">Nav</button>
<button data-state="pressed">Nav</button>
<button disabled data-state="disabled">Nav</button>
<button data-state="focus">Nav</button>
<div data-state="closed">closed</div>
<div data-state="open">open</div>
<div data-state="empty">empty</div>
<div data-state="loading">loading</div>
<div data-state="error">error</div>
<div style="background: var(--background); color: var(--foreground)">shell</div>
""",
            encoding="utf-8",
        )
        err = design_spec_completeness_error(spec, tmp_path, "DEMO-IA", "ia-navigation")
        assert err and "IA nav" in err


def test_ia_navigation_nine_top_level_fails():
    import tempfile
    from pathlib import Path

    with tempfile.TemporaryDirectory() as raw:
        tmp_path = Path(raw)
        spec = tmp_path / "docs" / "design-specs" / "DEMO-IA.md"
        spec.parent.mkdir(parents=True)
        spec.write_text(_filled_spec() + "\n\nia_nav: { top: 9, depth: 2 }\n", encoding="utf-8")
        mock = tmp_path / "docs" / "design-specs" / "mocks" / "DEMO-IA" / "list.html"
        mock.parent.mkdir(parents=True)
        mock.write_text(
            """<!doctype html>
<link rel="stylesheet" href="../../../../ui/tokens/design-tokens.css">
<button data-state="rest">Nav</button>
<button data-state="hover">Nav</button>
<button data-state="pressed">Nav</button>
<button disabled data-state="disabled">Nav</button>
<button data-state="focus">Nav</button>
<div data-state="closed">closed</div>
<div data-state="open">open</div>
<div data-state="empty">empty</div>
<div data-state="loading">loading</div>
<div data-state="error">error</div>
<div style="background: var(--background); color: var(--foreground)">shell</div>
""",
            encoding="utf-8",
        )
        err = design_spec_completeness_error(spec, tmp_path, "DEMO-IA", "ia-navigation")
        assert err and "9" in err


def test_ia_navigation_ok_counts_pass():
    import tempfile
    from pathlib import Path

    with tempfile.TemporaryDirectory() as raw:
        tmp_path = Path(raw)
        spec = tmp_path / "docs" / "design-specs" / "DEMO-IA.md"
        spec.parent.mkdir(parents=True)
        spec.write_text(_filled_spec() + "\n\nia_nav: { top: 5, depth: 2 }\n", encoding="utf-8")
        mock = tmp_path / "docs" / "design-specs" / "mocks" / "DEMO-IA" / "list.html"
        mock.parent.mkdir(parents=True)
        mock.write_text(
            """<!doctype html>
<link rel="stylesheet" href="../../../../ui/tokens/design-tokens.css">
<button data-state="rest">Nav</button>
<button data-state="hover">Nav</button>
<button data-state="pressed">Nav</button>
<button disabled data-state="disabled">Nav</button>
<button data-state="focus">Nav</button>
<div data-state="closed">closed</div>
<div data-state="open">open</div>
<div data-state="empty">empty</div>
<div data-state="loading">loading</div>
<div data-state="error">error</div>
<div style="background: var(--background); color: var(--foreground)">shell</div>
""",
            encoding="utf-8",
        )
        err = design_spec_completeness_error(spec, tmp_path, "DEMO-IA", "ia-navigation")
        assert err is None


def test_design_implement_blocks_pending_design_track():
    content = (
        "ticket_type: ui-composition\n"
        "design_status: pending\n"
        "design_spec: docs/design-specs/DEMO-0001.md\n"
    )
    msg = design_implement_blocked_message("DEMO-0001", content)
    assert msg and "approve-design" in msg


def test_design_implement_does_not_block_feature_tickets():
    content = "ticket_type: feature\ndesign_status: n/a\ntitle: API rate limit\n"
    assert design_implement_blocked_message("DEMO-0002", content) is None


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


def test_infer_checkout_is_composition_not_feature():
    from design_ticket_helpers import infer_ticket_type, is_commercial_surface, enrich_design_skills
    assert infer_ticket_type("Checkout guest vs account") == "ui-composition"
    assert is_commercial_surface("Checkout guest vs account")
    skills = enrich_design_skills(["UX-002"], "ui-composition", "Checkout guest vs account")
    assert "GD-001" in skills and "GD-002" in skills
    assert skills[0] != "GD-001"


def test_marketing_story_requires_arc_and_reduced_motion():
    from design_ticket_helpers import design_spec_story_error

    missing = design_spec_story_error("## 1. Summary\nHello", "marketing-page")
    assert missing and "Story" in missing
    template = """## 5. Story
- **Setup:** _fill_
- **Tension:** _fill_
- **CTA:** _fill_
- Reduced-motion path: _fill_
"""
    assert design_spec_story_error(template, "workflow-explainer")
    filled = """## 5. Story
- **Setup:** the operator opens the desk
- **Tension:** the queue is unsorted
- **Resolution:** one pass clears it
- **CTA:** Start the pass
- Reduced-motion path: the still frame, no scroll morph
## 6. Growth intent
"""
    assert design_spec_story_error(filled, "marketing-page") is None
    assert design_spec_story_error(filled, "ui-composition", "Checkout guest vs account") is None
    assert design_spec_story_error("## 1. Summary\nHello", "ui-composition", "Filter the command list") is None


def test_marketing_page_requires_growth_intent():
    from design_ticket_helpers import design_spec_growth_intent_error
    assert design_spec_growth_intent_error("## 1. Summary\nHello", "marketing-page")
    ok = design_spec_growth_intent_error(
        "## 6. Growth intent\nJob: choose a plan. Claim: annual default wins. Metric: plan_selected.",
        "marketing-page",
    )
    assert ok is None


def test_playbooks_include_growth_for_gd():
    from ticket_helpers import playbooks_for_skills
    paths = playbooks_for_skills(["UX-007", "GD-001"])
    assert any("growth-mechanics" in p for p in paths)
    assert any("visual-storytelling" in p for p in paths)
    assert any("delight-playbook" in p for p in paths)
    assert any("design-science" in p for p in paths)


def test_playbooks_include_interaction_for_ux002():
    from ticket_helpers import playbooks_for_skills
    paths = playbooks_for_skills(["UX-002", "UX-005"])
    assert any("interaction-ux-playbook" in p for p in paths)
    assert any("atomic-design-playbook" in p for p in paths)
    assert any("design-science" in p for p in paths)


def test_playbooks_fe001_not_team10_canon():
    from ticket_helpers import playbooks_for_skills
    paths = playbooks_for_skills(["FE-001"])
    blob = " ".join(paths)
    assert "frontend_playbook" in blob
    assert "motion-transitions" in blob
    assert "product-ux-playbook" not in blob
    assert "design-science-playbook" not in blob


def test_motion_section_required_unless_hitl_off():
    from design_ticket_helpers import design_spec_motion_error

    bare = "## 1. Summary\nA filter bar.\n"
    assert design_spec_motion_error(bare)
    assert design_spec_motion_error(bare, "motion: off") is None
    named = """
## 2d. Motion
Dropdown opens at duration fast and closes quicker. Ease smooth-out.
Reduced-motion keeps the same menu.
"""
    assert design_spec_motion_error(named) is None
    thin = "## 2d. Motion\nIt moves.\n"
    assert design_spec_motion_error(thin)
