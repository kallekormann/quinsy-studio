---
id: LO-0133
title: Gate smoke SEGV’d in the Cursor sandbox (Playwright Chromium); needed unrestrict
type: studio-evolution
status: open
phase: 6
priority: P1
estimate: S
assignee_role: Studio Automation Engineer (Director)
team: 09-studio-operations-evolution
skills: [SO-001]
dependencies: []
files: [.quinsy-studio/studio-tools/, .quinsy-studio/CHANGELOG.md]
signal: tooling-gap
source: moody
infusion_kind: tooling
infusion_path: studio-tools/
train_skills: [SO-001]
created: 2026-09-08
---

## Target
General rule lives in `studio-tools/` so the next project cannot repeat this. No client / product names in studio HQ titles or infused body (provenance `--source` / CHANGELOG only).

## Scope
Kind `tooling`. Promote or author in `studio-tools/` using `process/gates.md`. Principle title must stay product-agnostic. Train skills: ['SO-001']. Observation (provenance): Gate smoke SEGV’d in the Cursor sandbox (Playwright Chromium); needed unrestricted env — burned retries on MOOD-0640

## AC
- Inbox item LO-0133 generalized into `studio-tools/` (or matching playbook/skill/package)
- Infused text passes portability gate (no project folder names outside provenance)
- CHANGELOG.md updated
- LO moved to backlog/done/
