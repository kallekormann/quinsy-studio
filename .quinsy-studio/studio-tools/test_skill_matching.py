#!/usr/bin/env python3
"""
Quinsy Studio — Skill-matching test

Validates skill_matcher.py against example tickets and external skill paths.
"""

import sys
from pathlib import Path

from skill_matcher import (
    INTERNAL_SKILLS,
    EXTERNAL_MAPPINGS,
    match_skills,
    external_skills_for,
)

STUDIO_ROOT = Path(__file__).parent.parent.parent
EXTERNAL = STUDIO_ROOT / ".quinsy-studio" / "external-skills"

TEST_TICKETS = [
    {
        "id": "NUDG-1001",
        "title": "Landing page with new design system and typography",
        "text": "Build landing page: design tokens, color palette, typography, dark mode. Components: button, card, modal. Check Hallmark design against AI slop.",
        "expect_internal": ["FE-002", "FE-001"],
        "expect_external": ["design/skills", "design_awesome"],
    },
    {
        "id": "NUDG-1002",
        "title": "SEO audit and AEO optimization for AI search",
        "text": "Run SEO audit: visibility, ranking, schema.org. AEO: ChatGPT and Perplexity citations, comparison pages. pSEO architecture.",
        "expect_internal": ["GM-001", "GM-002"],
        "expect_external": ["marketing_aeo/skills/ai-seo", "marketing_aeo/skills/seo-audit", "geo_visibility"],
    },
    {
        "id": "NUDG-1003",
        "title": "Cookie banner with GDPR compliance",
        "text": "Implement cookie banner: consent, tracking opt-in, GDPR, data protection. Withdrawal option.",
        "expect_internal": ["CL-002", "CL-001"],
        "expect_external": ["cookiecomply"],
    },
    {
        "id": "NUDG-1004",
        "title": "PostgreSQL schema and query optimization",
        "text": "Design database schema: migration, query, SQL, indexing for PostgreSQL.",
        "expect_internal": ["BE-002"],
        "expect_external": ["database-schema-design"],
    },
    {
        "id": "NUDG-1005",
        "title": "Security audit before release",
        "text": "Security audit: OWASP, penetration, vulnerability scan, dependency scanning.",
        "expect_internal": ["PE-003"],
        "expect_external": ["security-audit", "threat-modeling"],
    },
    {
        "id": "NUDG-1006",
        "title": "Godot 2D platformer with double jump",
        "text": "Build game: Godot 2D movement, platformer level, tilemap.",
        "expect_internal": ["GM-004"],
        "expect_external": ["gamedev"],
    },
    {
        "id": "NUDG-1007",
        "title": "Copywriting for pricing page",
        "text": "Copywriting: conversion copy for pricing, offer, newsletter sequence. Content strategy.",
        "expect_internal": ["GM-003"],
        "expect_external": ["marketing_aeo/skills/copywriting"],
    },
    {
        "id": "NUDG-1008",
        "title": "New settings modal component",
        "text": "Add new modal dialog for settings panel. UI component with dropdown menu.",
        "expect_internal": ["UX-002", "UX-005", "UX-006"],
        "expect_external": ["design-agent/ux-interaction-patterns"],
    },
    {
        "id": "NUDG-1009",
        "title": "Information architecture for main navigation",
        "text": "Redesign navigation structure and wayfinding. IA audit: top-level nav items.",
        "expect_internal": ["UX-003"],
        "expect_external": ["design-agent/ux-information-architecture"],
    },
    {
        "id": "NUDG-1010",
        "title": "Checkout flow conversion experiment",
        "text": "Design checkout: hypothesis for guest vs account, conversion CRO, one variant.",
        "expect_internal": ["GD-001", "GD-002"],
        "expect_external": ["marketing_aeo/skills/cro"],
    },
]


def verify_external_on_disk(ext_path: str) -> bool:
    if any(s in ext_path for s in ["skills (hallmark", "skills/<", "(Router:", "SKILL.md"]):
        domain = ext_path.split("/")[0].split()[0]
        return (EXTERNAL / domain).exists()

    parts = ext_path.split("/")
    domain = parts[0]
    rest = "/".join(parts[1:])
    base = EXTERNAL / domain
    if not base.exists():
        return False
    if not rest:
        return True
    current = base
    for part in rest.split("/"):
        candidates = [p for p in current.iterdir() if p.name.lower().startswith(part.lower())] if current.exists() else []
        if not candidates:
            return False
        current = candidates[0]
    return True


def main():
    print("=" * 62)
    print("  QUINSY STUDIO — SKILL-MATCHING-TEST")
    print(f"  Skills loaded: {len(INTERNAL_SKILLS)} internal, {len(EXTERNAL_MAPPINGS)} external maps")
    print("=" * 62)

    total = 0
    passed = 0
    ext_checked = 0
    ext_ok = 0

    for ticket in TEST_TICKETS:
        total += 1
        text = f"{ticket['title']} {ticket['text']}"
        internal_hits = match_skills(text)
        external_hits = external_skills_for(internal_hits)

        exp_in = set(ticket["expect_internal"])
        exp_ext = set(ticket["expect_external"])
        got_in = set(internal_hits)
        got_ext = set(external_hits)

        in_ok = exp_in.issubset(got_in)
        ext_ok_this = all(any(exp in e for e in got_ext) for exp in exp_ext)
        ok = in_ok and ext_ok_this

        print(f"\n  [{ticket['id']}] {ticket['title']}")
        print(f"    Internal: {'✓' if in_ok else '✗'} {sorted(got_in)} (expected {sorted(exp_in)})")
        print(f"    External: {'✓' if ext_ok_this else '✗'} {sorted(got_ext)} (expected {sorted(exp_ext)})")

        for e in sorted(got_ext):
            ext_checked += 1
            on_disk = verify_external_on_disk(e)
            if on_disk:
                ext_ok += 1
            print(f"    Disk:    {'✓' if on_disk else '✗'} {e}")

        if ok:
            passed += 1

    print("\n" + "=" * 62)
    print(f"  RESULT: {passed}/{total} tickets matched correctly")
    print(f"  External sources on disk: {ext_ok}/{ext_checked}")
    if passed == total:
        print("  ✅ ALL MATCH TESTS PASSED")
    else:
        print("  ❌ MATCH TESTS FAILED")
    if ext_ok < ext_checked and not EXTERNAL.exists():
        print("  ⚠️  Run `./studio update-skills` to import external skill packages")
    print("=" * 62)

    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
