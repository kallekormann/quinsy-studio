#!/usr/bin/env python3
"""Tests for studio_skill_checks.py (LO-0334 / LO-0338)."""

import tempfile
from pathlib import Path

from studio_skill_checks import (
    ai_eval_receipt_issues,
    native_select_warnings,
    token_literal_warnings,
)


def test_hex_in_app_warns():
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        f = root / "app" / "page.tsx"
        f.parent.mkdir(parents=True)
        f.write_text('export const c = "#ff00aa";\n', encoding="utf-8")
        warns = token_literal_warnings(root)
        assert any("token-literal" in w and "page.tsx" in w for w in warns)


def test_hex_in_tokens_allowlisted():
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        f = root / "src" / "ui" / "tokens" / "tokens.css"
        f.parent.mkdir(parents=True)
        f.write_text(":root { --accent: #ff00aa; }\n", encoding="utf-8")
        assert token_literal_warnings(root) == []


def test_native_select_warns():
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        f = root / "src" / "Form.tsx"
        f.parent.mkdir(parents=True)
        f.write_text("<select><option>A</option></select>\n", encoding="utf-8")
        warns = native_select_warnings(root)
        assert any("native-select" in w for w in warns)


def test_ai_eval_required():
    ticket = "skills: [AI-004, FE-001]\n"
    assert ai_eval_receipt_issues("## Plan\nok\n", ticket)
    filled = "## Plan\nok\n## Eval\n- golden set 12 prompts, 10 pass\n"
    assert ai_eval_receipt_issues(filled, ticket) == []
    assert ai_eval_receipt_issues("## Plan\nok\n", "skills: [FE-001]\n") == []


if __name__ == "__main__":
    test_hex_in_app_warns()
    test_hex_in_tokens_allowlisted()
    test_native_select_warns()
    test_ai_eval_required()
    print("studio_skill_checks tests OK")
