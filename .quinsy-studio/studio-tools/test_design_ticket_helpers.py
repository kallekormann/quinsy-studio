#!/usr/bin/env python3
"""Tests for design_ticket_helpers placement gate."""

from design_ticket_helpers import (
    design_spec_has_placement_section,
    infer_ticket_type,
)


def test_infer_ia_feature_placement():
    assert infer_ticket_type("Move presentation link to presentation builder") == "ia-feature-placement"
    assert infer_ticket_type("Fix export button alignment") == "feature"


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
