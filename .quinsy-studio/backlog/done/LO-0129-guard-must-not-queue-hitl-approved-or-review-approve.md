---
id: LO-0129
title: Guard must not queue HITL "approved" or review/amendment approve as inbox notes
type: studio-evolution
status: done
phase: 6
priority: P1
estimate: S
assignee_role: Studio Automation Engineer (Director)
team: 09-studio-operations-evolution
skills: [SO-001]
dependencies: []
files: [.quinsy-studio/studio-tools/studio_human_inbox.py, .quinsy-studio/CHANGELOG.md]
signal: tooling-gap
source: affiliate-platform
infusion_kind: tooling
infusion_path: studio-tools/
train_skills: [SO-001]
created: 2026-09-08
---

## Target
General rule lives in `studio-tools/` so the next project cannot repeat this.

## Scope
Kind `tooling`. `should_queue_as_note` treats short HITL replies (`approved`, `looks good`) and review/amendment approve phrases as not queueable.

## AC
- [x] Inbox item generalized into `studio_human_inbox.py`
- [x] CHANGELOG.md updated
- [x] LO moved to backlog/done/
