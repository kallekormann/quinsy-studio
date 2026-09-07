---
id: LO-0071
title: Agent sandbox cannot run Chromium smoke (SIGSEGV) — gates used QUINSY_SKIP_SMOKE
type: studio-evolution
status: done
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
created: 2026-09-07
---

## Target
General rule lives in `studio-tools/` so the next project cannot repeat this. No client names in studio HQ.

## Scope
Kind `tooling`. Promote or author in `studio-tools/` using `process/gates.md`. Observation: Agent sandbox cannot run Chromium smoke (SIGSEGV) — gates used QUINSY_SKIP_SMOKE

## AC
- Inbox item LO-0071 generalized into `studio-tools/` (or matching playbook/skill/package)
- CHANGELOG.md updated
- LO moved to backlog/done/
