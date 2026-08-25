---
id: LO-0007
title: Studio HQ project-agnostic abstraction audit and verify-abstraction command
type: studio-evolution
status: done
phase: 6
priority: P1
estimate: M
assignee_role: Process Guard (Director)
team: 09-studio-operations-evolution
skills: ['SO-002']
dependencies: []
created: 2026-08-25
completed: 2026-08-25
---

# LO-0007 — Studio HQ abstraction

## Done

- [x] `process/studio-abstraction.md` policy
- [x] `./studio verify-abstraction` CLI
- [x] Amendment docs: generic `acme-app` example in `studio-templates/amendment_01.example.md`
- [x] `amendment-intake.md`, `GETTING_STARTED.md`, `amendment_template.md` — no moody paths
- [x] `ticket-team-allocation.md`, `worlds.md`, `studio.py`, `sprint_reuse_review.py` — generic examples
- [x] `studio-library/packages/auth` README + mailpit message — `<project>` placeholder
- [x] Deleted `.quinsy-studio/tmp/generate_moody_backlog.py`

## Allowed exceptions

- `backlog/` LO tickets may cite `--source <project>`
- `retros/` may name project for sprint attribution
- `manifest.json` `source_project` promotion provenance

## Verify

```bash
./studio verify-abstraction
```
