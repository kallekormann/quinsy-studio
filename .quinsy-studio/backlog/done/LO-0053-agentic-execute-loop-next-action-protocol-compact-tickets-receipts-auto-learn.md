---
id: LO-0053
title: Agentic execute loop — next-action protocol, compact tickets, receipts, auto-learn
type: studio-evolution
status: done
phase: 6
priority: P1
estimate: L
assignee_role: Studio Automation Engineer (Director)
team: 09-studio-operations-evolution
skills: [SO-001, SO-002, SO-003]
dependencies: []
files: [.quinsy-studio/studio-tools/studio_execute.py, .quinsy-studio/studio-tools/ticket_helpers.py, AGENTS.md]
signal: tooling-gap
source: studio-meta
created: 2026-09-07
---

## Target
Studio HQ has a closed execute loop: one next action until HITL, compact ticket cards, receipts before done, bounded gate-fail debug, auto-learn.

## Scope
`.quinsy-studio/` only. Markdown stays ticket source of truth (no SQL).

## AC
- `./studio execute <project>` emits IMPLEMENT / GATE / VERIFY / MOVE_DONE / DEBUG / STUDIO_LO / HITL
- Session start loops execute until HITL; does not ask to continue
- New tickets are compact (no boilerplate DoD, no filler BDD)
- `move … done` requires receipt (Plan, AC coverage, default flow) plus gate 5
- Gate fail writes debug file; 3rd fail auto-drafts LO with signal gate-fail
- `./studio health` reports open LOs, missing receipts, unmet deps
