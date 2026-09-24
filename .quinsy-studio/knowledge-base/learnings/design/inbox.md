# design / inbox

Portable studio principles (not project incidents).
Matching playbook/skill: `knowledge-base/design_playbook.md`.

## Principles

- **PB-20260923-001** helpful=0 harmful=0 :: Operator preview links use the configured magazine origin (loopback plus port on local stacks). Tenant chrome is a host query param, not the public hostname in the URL — that name often does not resolve locally.
- **LO-0327** 2026-09-23 :: Inbox preview URLs must use MAGAZINE_URL origin (localhost:13000 on Compose). Property chrome is host= query, not {prope
  - Inbox preview URLs must use MAGAZINE_URL origin (localhost:13000 on Compose). Property chrome is host= query, not {property.host}:port — that hostname does not resolve locally.
