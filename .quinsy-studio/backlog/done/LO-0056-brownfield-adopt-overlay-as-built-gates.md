---
id: LO-0056
title: Brownfield adopt — overlay studio docs on an existing codebase, reconstruct as-built, then join gates
type: studio-evolution
status: done
phase: 6
priority: P1
estimate: L
assignee_role: Studio Automation Engineer (Director)
team: 09-studio-operations-evolution
skills: [SO-001, SO-002, SO-003]
dependencies: []
files: [.quinsy-studio/process/brownfield-adopt.md, .quinsy-studio/studio-tools/studio_adopt.py, .quinsy-studio/studio-tools/studio.py, .quinsy-studio/studio-tools/studio_execute.py]
signal: process-gap
source: studio-meta
infusion_kind: process
infusion_path: process/brownfield-adopt.md
created: 2026-09-07
---

## Target
An existing repo can join Quinsy Studio without an empty scaffold. Overlay studio folders, reconstruct implementation state in depth, then plan further work through the same gates and execute loop.

## Scope
`.quinsy-studio/` only. Do not wipe application source. Do not `git init` over an existing `.git`. Do not copy project UI into `studio-library/`. No SQL.

## AC
- `./studio adopt <slug> --from <git-url|path>` copies/clones into `projects/<slug>/` and overlays `docs/` / `backlog/` / `status.json` `mode: adopt`
- As-built templates `docs/as-built/00`–`07` must be filled from code (cite paths; `_TODO_` is not done) before gate 0
- Execute: empty as-built → `IMPLEMENT`; ready + no PRD → `VERIFY`; then HITL gates. No fake Next.js prototype on adopt
- `init` / `bootstrap` refuse a live tree; gate 2 validation skips prototype when `mode: adopt`
