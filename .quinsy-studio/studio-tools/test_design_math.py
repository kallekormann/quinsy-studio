#!/usr/bin/env python3
"""Tests for design_math.py"""

from design_math import (
    contrast_ratio,
    golden_scale,
    ia_nav_audit,
    palette_60_30_10,
    wcag_aa_pass,
)


def test_contrast_black_on_white():
    ratio = contrast_ratio("#000000", "#ffffff")
    assert ratio == 21.0


def test_wcag_aa():
    assert wcag_aa_pass(4.5)
    assert not wcag_aa_pass(3.0)
    assert wcag_aa_pass(3.0, large_text=True)


def test_golden_scale():
    sizes = golden_scale(16, steps=4)
    assert sizes[0] == 16
    assert sizes[1] > 16


def test_palette_split():
    p = palette_60_30_10("#3366cc", "#f5f5f5", "#ff6600")
    assert p["dominant_60"] == "#f5f5f5"


def test_ia_nav_audit():
    assert ia_nav_audit(5, 2) == []
    assert len(ia_nav_audit(9, 4)) == 2


def test_parse_ia_nav_inline():
    from studio_ia_audit import parse_ia_nav_counts, ia_nav_findings

    assert parse_ia_nav_counts("ia_nav: { top: 5, depth: 2 }") == (5, 2)
    assert ia_nav_findings("ia_nav: { top: 9, depth: 1 }")
    assert ia_nav_findings("")  # missing
    assert ia_nav_findings("ia_nav: { top: 4, depth: 2 }") == []


if __name__ == "__main__":
    test_contrast_black_on_white()
    test_wcag_aa()
    test_golden_scale()
    test_palette_split()
    test_ia_nav_audit()
    test_parse_ia_nav_inline()
    print("design_math tests OK")
