#!/usr/bin/env python3
"""Design push-back loop (LO-0405, LO-0406, LO-0408)."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import design_feedback as df
from design_ticket_helpers import design_spec_catalog_error


class ReasonTests(unittest.TestCase):
    def test_codes_and_validation(self):
        self.assertIn("hierarchy", df.reason_codes())
        self.assertIsNone(df.validate_reason("Motion"))
        self.assertIn("--reason must be one of", df.validate_reason("vibes") or "")

    def test_finish_hold_code(self):
        self.assertEqual(df.finish_hold_code("Decision: HOLD\nReason: density\n"), "density")
        self.assertEqual(df.finish_hold_code("Decision: HOLD\n"), "uniqueness")

    def test_set_design_rejected(self):
        self.assertIn("design_status: pending", df.set_design_rejected("---\ndesign_status: approved\n---\n"))


class LogTests(unittest.TestCase):
    def test_append_read_counts_and_retro(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            df.append_pushback(root, "T-1", "hierarchy", "primary action sits below the fold", "reject")
            df.append_pushback(root, "T-1", "hierarchy", "", "finish-hold")
            df.append_pushback(root, "T-2", "copy", "CTA says Submit", "feedback")
            entries = df.read_pushback(root)
            self.assertEqual(len(entries), 3)
            self.assertEqual(df.code_counts(entries), {"hierarchy": 2, "copy": 1})
            self.assertEqual(len(df.pushback_for(root, ["T-2"])), 1)
            block = df.retro_design_section(root, ["T-1", "T-2"])
            self.assertIn("| hierarchy | 2 |", block)
            self.assertIn("Carry forward", block)
            self.assertIn("`hierarchy` lines", block)
            self.assertIn("No design push-back", df.retro_design_section(root, ["T-9"]))

    def test_record_pushback_survives_harvest_error(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            with patch("design_feedback.harvest_pushback", side_effect=RuntimeError("boom")):
                result = df.record_pushback("demo", root, "T-1", "brand", "off palette", "reject")
            self.assertTrue(Path(str(result["log"])).is_file())
            self.assertFalse(result["created"])

    def test_record_pushback_calls_harvest_with_design_gap(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            with patch("studio_harvest.harvest_identified_learning", return_value={"created": True, "lo_id": "LO-9999"}) as fake:
                result = df.record_pushback("demo", root, "T-1", "motion", "menu pops without easing", "reject")
            self.assertEqual(result["lo_id"], "LO-9999")
            kwargs = fake.call_args.kwargs
            self.assertEqual(kwargs["signal"], "design-gap")
            self.assertEqual(kwargs["kind"], "ux")


class CatalogAppliedTests(unittest.TestCase):
    def test_missing_section(self):
        self.assertIn("7b", design_spec_catalog_error("## 7. Design system compliance\nok\n") or "")

    def test_no_ids(self):
        err = design_spec_catalog_error("## 7b. Catalog applied\n- read things\n\n## 8. Handoff\n")
        self.assertIn("names no PB- id", err or "")

    def test_ids_pass(self):
        self.assertIsNone(design_spec_catalog_error("## 7b. Catalog applied\n- PB-20260916-004 — applied in §4\n\n## 8. Handoff\n"))
        lo_only = design_spec_catalog_error("## 7b. Catalog applied (required)\n- LO-0172 — scrollbar gutter in §4\n")
        self.assertIn("only LO- ids", lo_only or "")

    def test_none_with_reason_passes(self):
        self.assertIsNone(design_spec_catalog_error("## 7b. Catalog applied\ncatalog: none — no entry in the design catalog covers a first-run tour surface yet.\n"))
        self.assertIsNotNone(design_spec_catalog_error("## 7b. Catalog applied\ncatalog: none\n"))


if __name__ == "__main__":
    unittest.main()
