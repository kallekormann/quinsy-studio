#!/usr/bin/env python3
"""Tests for PRD intake NFR section routing (LO-0000)."""

from process_intake import map_heading_to_section


def test_non_functional_headings():
    assert map_heading_to_section("Non-Functional Requirements") == "requirements_non_functional"
    assert map_heading_to_section("non functional requirements") == "requirements_non_functional"
    assert map_heading_to_section("NFR") == "requirements_non_functional"


def test_functional_not_from_non_functional():
    assert map_heading_to_section("functional requirements") == "requirements_functional"
    assert map_heading_to_section("Functional Requirements") == "requirements_functional"
