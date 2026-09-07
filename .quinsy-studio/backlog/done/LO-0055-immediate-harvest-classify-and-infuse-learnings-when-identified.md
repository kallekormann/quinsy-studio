---
id: LO-0055
title: Immediate harvest — classify and infuse learnings when identified, not on human trigger
type: studio-evolution
status: done
phase: 6
priority: P1
estimate: M
assignee_role: Studio Automation Engineer (Director)
team: 09-studio-operations-evolution
skills: [SO-001, SO-002, SO-003]
dependencies: []
files: [.quinsy-studio/studio-tools/studio_harvest.py, .quinsy-studio/studio-tools/studio_execute.py, .quinsy-studio/process/learning-loop.md]
signal: process-gap
source: studio-meta
infusion_kind: process
infusion_path: process/learning-loop.md
created: 2026-09-07
---

## Target
A learning is classified and written into studio HQ in the same session it is identified. Execute returns STUDIO_LO before the next project ticket so the originating context is not lost.

## Scope
`.quinsy-studio/` only. No SQL. No auto-copy of project UI/tokens into studio-library.

## AC
- Harvest on `./studio learn`, retro `--complete`, reuse, and 3rd gate fail (inbox + classified LO)
- Execute prefers STUDIO_LO over the next IMPLEMENT (in-progress VERIFY/GATE still finishes; HITL sprint-review still wins)
- Infusion buckets: package, ui-component, design/ux/ia/layout/usability, frontend/backend/database/security, process, tooling
- Exact-title dedupe so reuse paths do not collide
