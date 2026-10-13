#!/usr/bin/env python3
"""Must-fail and must-pass microcopy fixtures for the anti-slop gate."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from validate_anti_slop import copy_findings, scan_file

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "anti-slop"


def _lines(name: str):
    return [ln for ln in (FIXTURES / name).read_text(encoding="utf-8").splitlines() if ln.strip()]


class MicrocopyFixtureTests(unittest.TestCase):
    def test_every_must_fail_line_is_an_error(self):
        for line in _lines("microcopy-must-fail.txt"):
            with self.subTest(line=line):
                self.assertTrue(any(sev == "error" for _, _, sev in copy_findings(line)))

    def test_every_must_pass_line_is_clean(self):
        for line in _lines("microcopy-must-pass.txt"):
            with self.subTest(line=line):
                self.assertEqual(copy_findings(line), [])

    def test_spec_quoting_a_bad_example_is_not_flagged(self):
        line = "- Fail: a code alone (`Something went wrong`). Never write `Oops!`."
        self.assertEqual([f for f in copy_findings(line, ".md") if f[2] == "error"], [])
        self.assertTrue(copy_findings(line, ".tsx"))

    def test_scan_file_fails_shipped_copy(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "apps" / "web" / "src" / "app" / "error.tsx"
            path.parent.mkdir(parents=True)
            path.write_text("export default () => <p>Oops! Something went wrong.</p>\n", encoding="utf-8")
            errors = [v for v in scan_file(path, root) if v.severity == "error"]
            self.assertTrue(errors)
            self.assertEqual(errors[0].pattern_name, "microcopy")


class ProjectIgnoreTests(unittest.TestCase):
    def test_project_lists_its_own_vendored_folders(self):
        import tempfile

        from validate_anti_slop import project_ignore_patterns, should_ignore

        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            (root / "docs").mkdir()
            (root / "docs" / "anti-slop-ignore.txt").write_text("# vendored\napps/admin-shell\n", encoding="utf-8")
            extra = project_ignore_patterns(root)
        self.assertEqual(extra, ["apps/admin-shell"])
        self.assertTrue(should_ignore("projects/demo/apps/admin-shell/page.tsx", extra))
        self.assertFalse(should_ignore("projects/demo/apps/web/page.tsx", extra))


if __name__ == "__main__":
    unittest.main()
