---
id: LO-0061
title: Factory loop — HITL contraction, inform/veto, parallel train, human inbox, honest stubs
type: studio-evolution
status: done
phase: 6
priority: P1
estimate: L
assignee_role: Studio Automation Engineer (Director)
team: 09-studio-operations-evolution
skills: [SO-001, SO-002, SO-003]
dependencies: [LO-0053, LO-0055]
files: [.quinsy-studio/studio-tools/studio_execute.py, .quinsy-studio/process/human-in-the-loop.md, AGENTS.md]
signal: process-gap
source: studio-meta
infusion_kind: process
infusion_path: process/human-in-the-loop.md
created: 2026-09-07
---

## Target
Product execute runs until design HITL, UI sprint review, or rare tech-veto. Architecture/reuse/scope are inform. Open LOs train in parallel instead of blocking IMPLEMENT. Human chat queues; only abort preempts.

## Scope
`.quinsy-studio/` only. No Moody product tickets. Library stubs stay in HQ but are not pullable.

## AC
- Mandatory HITL: gate 0, **gate 1 architecture**, **gate 2 design track**, design-track `approve-design`, UI sprint review, tech-veto, abort, 3× QA fail
- After PRD, execute produces the blueprint then HITL gate 1; then design (direction / system / mocks or prototype) then HITL gate 2
- Reuse and sprint scope/groom are agent-owned (human may override); reuse `--approve` is not a blocker
- CARD lists skill IDs + playbook paths
- `./studio note` ACK-queues; drain after MOVE_DONE; abort is the only preempt
- `./studio train` queues beside product work; execute IMPLEMENT is not replaced by STUDIO_LO mid-sprint
- `billing` and `feature-gating` pulls are refused as stubs
