#!/usr/bin/env python3
"""Tests for UI kit peer merge on project scaffold."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from ui_kit_peers import (
    UI_KIT_PEER_DEPS,
    ensure_package_json_kit_peers,
    merge_kit_peers,
)


class UiKitPeersTests(unittest.TestCase):
    def test_merge_adds_all_kit_names(self):
        out = merge_kit_peers({})
        for name in UI_KIT_PEER_DEPS:
            self.assertIn(name, out)
        self.assertIn("@headlessui/react", out)

    def test_merge_does_not_overwrite_existing_range(self):
        out = merge_kit_peers({"radix-ui": "^1.0.0"})
        self.assertEqual(out["radix-ui"], "^1.0.0")

    def test_ensure_writes_package_json(self):
        with tempfile.TemporaryDirectory() as raw:
            pkg = Path(raw) / "package.json"
            pkg.write_text('{"name": "app", "dependencies": {"next": "14.0.0"}}\n')
            self.assertTrue(ensure_package_json_kit_peers(pkg))
            data = json.loads(pkg.read_text())
            self.assertIn("clsx", data["dependencies"])
            self.assertIn("next", data["dependencies"])
            self.assertFalse(ensure_package_json_kit_peers(pkg))


if __name__ == "__main__":
    unittest.main()
