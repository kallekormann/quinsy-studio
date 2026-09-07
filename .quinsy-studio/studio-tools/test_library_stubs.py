#!/usr/bin/env python3
"""Stubs are not pullable; suggest skips them."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from library_manager import asset_is_stub, pull_assets, suggest_assets


class StubLibraryTests(unittest.TestCase):
    def test_billing_and_gating_are_stubs(self):
        self.assertIsNotNone(asset_is_stub("billing"))
        self.assertIsNotNone(asset_is_stub("feature-gating"))
        self.assertIsNone(asset_is_stub("auth"))

    def test_pull_refuses_stubs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "demo").mkdir()
            with patch("library_manager.PROJECTS_DIR", root):
                result = pull_assets("demo", ["billing", "feature-gating"])
        statuses = {i.get("name"): i.get("status") for i in result.get("pulled", [])}
        self.assertEqual(statuses.get("billing"), "refused_stub")
        self.assertEqual(statuses.get("feature-gating"), "refused_stub")

    def test_suggest_skips_stubs(self):
        hits = suggest_assets("billing lemon subscription")
        names = {h.get("name") for h in hits}
        self.assertNotIn("billing", names)
        self.assertNotIn("feature-gating", names)


if __name__ == "__main__":
    unittest.main()
