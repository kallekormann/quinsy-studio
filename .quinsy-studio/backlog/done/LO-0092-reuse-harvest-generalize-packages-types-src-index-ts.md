---
id: LO-0092
title: Reuse harvest: generalize `packages/types/src/index.ts`
type: studio-evolution
status: done
phase: 6
priority: P1
estimate: S
assignee_role: Studio Automation Engineer (Director)
team: 09-studio-operations-evolution
skills: [SO-001, BE-001]
dependencies: []
files: [.quinsy-studio/studio-library/packages/, .quinsy-studio/CHANGELOG.md]
signal: library-gap
source: affiliate-platform/SPRINT-01
infusion_kind: package
infusion_path: studio-library/packages/
train_skills: [SO-001, BE-001]
created: 2026-09-07
---

## Target
General rule lives in `studio-library/packages/` so the next project cannot repeat this. No client / product names in studio HQ titles or infused body (provenance `--source` / CHANGELOG only).

## Scope
Kind `package`. Promote or author in `studio-library/packages/` using `studio-library/library_registry.md`. Principle title must stay product-agnostic. Train skills: ['SO-001', 'BE-001']. Observation (provenance): Sprint ticket AFFI-0001 changed `packages/types/src/index.ts` without library promotion.

## AC
- Inbox item LO-0092 generalized into `studio-library/packages/` (or matching playbook/skill/package)
- Infused text passes portability gate (no project folder names outside provenance)
- CHANGELOG.md updated
- LO moved to backlog/done/

## Status Change
- **From:** open
- **To:** done
- **Date:** 2026-09-07
- **Reason:** Wont-promote. First-brand token/UI packages stay project-local; reuse harvest should record `local`, not auto-open HQ package LOs.
