---
id: LO-0336
title: Distill postgres and API catalog into backend playbook; add thin BE-006 jobs and delivery
type: studio-evolution
status: done
phase: 6
priority: P1
estimate: L
assignee_role: Backend Architect (Director)
team: 02-backend-systems
skills: [BE-001, BE-002, BE-005, SO-001]
dependencies: [LO-0331]
files: [.quinsy-studio/knowledge-base/backend_playbook.md, .quinsy-studio/teams/02-backend-systems/, .quinsy-studio/teams/skill-registry.md]
sprint: HQ-SKILL-04
epic: HQ-SKILL
signal: process-gap
source: studio-hq
infusion_kind: playbook
infusion_path: knowledge-base/backend_playbook.md
train_skills: [BE-001, BE-002]
created: 2026-09-24
---

## Target
Catalog `postgres-schema-design`, `supabase-postgres-best-practices`, `api-design-principles` distill into the backend spine. New **BE-006 Jobs & delivery** covers queues, outbox, partner sync (Data Engineer role had no skill).

## Scope
Thin `skills/jobs-and-delivery.md`. Registry triggers: queue, job, worker, outbox, sync, webhook retry. Keep migrate `--approve` / names-only secrets. Epic: process/hq-skill-advancement-sprints.md.

## AC
- BE-006 file + Team 02 README + registry
- backend_playbook spine sections: indexes/FKs, idempotency, jobs
- CHANGELOG

## Out of scope
Product migrations. GraphQL as a new skill ID.
