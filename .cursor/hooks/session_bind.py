#!/usr/bin/env python3
"""Cursor hook: per-chat product binding. No-op unless HQ runtime is cursor."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".quinsy-studio" / "studio-tools"))

from studio_session_hooks import hook_response, loads_hook_payload  # noqa: E402


def main() -> int:
    try:
        payload = loads_hook_payload(sys.stdin.read())
    except json.JSONDecodeError:
        print(json.dumps({"permission": "allow"}))
        return 0
    result = hook_response(payload, studio_root=ROOT)
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
