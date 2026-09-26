# design / inbox

Portable studio principles (not project incidents).
Matching playbook/skill: `knowledge-base/design_playbook.md`.

## Principles

- **PB-20260926-002** helpful=0 harmful=0 :: Keep operator nav and inbox work on the shipped chrome. Do not invent a second shell or an in-thread preview frame.
- **LO-0347** 2026-09-26 :: Keep operator nav and inbox work on the shipped chrome
  - See **PB-20260926-002**. Keep operator nav and inbox work on the shipped chrome. Do not invent a second shell or an in-thread preview frame.
- **PB-20260926-001** helpful=0 harmful=0 :: Keep layout and composition work on the live layout-picker cards. Do not invent a second block-list editor, a second intake inbox, or a one-off product-detail workbench.
- **LO-0346** 2026-09-26 :: Keep composition work on the live layout-picker cards
  - See **PB-20260926-001**. Keep layout and composition work on the live layout-picker cards. Do not invent a second block-list editor, a second intake inbox, or a one-off product-detail workbench.
- **PB-20260923-001** helpful=0 harmful=0 :: Operator preview links use the configured magazine origin (loopback plus port on local stacks). Tenant chrome is a host query param, not the public hostname in the URL — that name often does not resolve locally.
- **LO-0327** 2026-09-23 :: Inbox preview URLs must use MAGAZINE_URL origin (localhost:13000 on Compose). Property chrome is host= query, not {prope
  - Inbox preview URLs must use MAGAZINE_URL origin (localhost:13000 on Compose). Property chrome is host= query, not {property.host}:port — that hostname does not resolve locally.
