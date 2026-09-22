#!/usr/bin/env python3
"""LO-0314: env schema is names-only."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

SCHEMA = (
    Path(__file__).resolve().parent.parent / "studio-templates" / "env.schema.json"
)
EXAMPLE = Path(__file__).resolve().parent.parent / "studio-templates" / "env.example"

# Live-looking blobs that must never appear in the committed schema/example.
_VALUE_SHAPE = re.compile(
    r"(?i)(sk-[a-z0-9]{8,}|eyj[a-z0-9_-]{20,}|-----begin |"
    r"postgres://[^:]+:[^@]+@|postgresql://[^:]+:[^@]+@|"
    r"password=[^\s#]{3,})",
)


class EnvSchemaTests(unittest.TestCase):
    def test_schema_has_keys_and_no_secret_values(self):
        data = json.loads(SCHEMA.read_text(encoding="utf-8"))
        self.assertIn("variables", data)
        names = []
        for item in data["variables"]:
            self.assertIn("name", item)
            self.assertIn("purpose", item)
            self.assertNotIn("value", item)
            self.assertNotIn("default", item)
            name = item["name"]
            self.assertRegex(name, r"^[A-Z][A-Z0-9_]+$")
            blob = f"{name} {item['purpose']}"
            self.assertIsNone(_VALUE_SHAPE.search(blob), blob)
            names.append(name)
        self.assertIn("DATABASE_URL", names)
        self.assertIn("POSTGRES_PASSWORD", names)
        self.assertGreaterEqual(len(names), 8)

    def test_example_is_names_without_passwords(self):
        text = EXAMPLE.read_text(encoding="utf-8")
        self.assertIn("POSTGRES_PASSWORD=", text)
        self.assertNotIn("POSTGRES_PASSWORD=postgres", text)
        self.assertIsNone(_VALUE_SHAPE.search(text), text)
        docker_ex = SCHEMA.parent / "docker" / ".env.example"
        docker = docker_ex.read_text(encoding="utf-8")
        self.assertNotIn("POSTGRES_PASSWORD=postgres", docker)
        self.assertIsNone(
            re.search(r"postgresql://postgres:postgres@", docker), docker
        )


if __name__ == "__main__":
    unittest.main()
