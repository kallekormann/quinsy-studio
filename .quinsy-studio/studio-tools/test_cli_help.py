#!/usr/bin/env python3
"""SO-001 CLI rule: every `./studio` command has a help line in both help blocks."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

SOURCE = (Path(__file__).resolve().parent / "studio.py").read_text(encoding="utf-8")
HELP_LINE = re.compile(r"^\s+\./studio ([a-z0-9-]+)", re.M)


def _commands():
    found = set(re.findall(r'(?<![\w])command == "([a-z0-9-]+)"', SOURCE))
    for group in re.findall(r'(?<![\w])command in \(([^)]*)\)', SOURCE):
        found |= set(re.findall(r'"([a-z0-9-]+)"', group))
    return found


def _blocks():
    first = SOURCE.index('"""')
    second = SOURCE.index('"""', first + 3)
    return SOURCE[first:second], SOURCE[second:]


class CliHelpTests(unittest.TestCase):
    def test_every_command_is_in_the_module_help(self):
        doc, _ = _blocks()
        self.assertEqual(sorted(_commands() - set(HELP_LINE.findall(doc))), [])

    def test_every_command_is_in_the_printed_help(self):
        _, rest = _blocks()
        self.assertEqual(sorted(_commands() - set(HELP_LINE.findall(rest))), [])

    def test_no_help_line_without_a_handler(self):
        doc, rest = _blocks()
        documented = set(HELP_LINE.findall(doc)) | set(HELP_LINE.findall(rest))
        self.assertEqual(sorted(documented - _commands()), [])


if __name__ == "__main__":
    unittest.main()
