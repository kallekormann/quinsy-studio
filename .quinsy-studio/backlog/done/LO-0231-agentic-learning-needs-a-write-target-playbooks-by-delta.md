---
id: LO-0231
title: Agentic learning needs a write target — versioned playbooks evolved by delta, never by model rewrite
type: studio-evolution
status: done
phase: 6
priority: P0
estimate: M
assignee_role: Autonomous Systems Director
team: 07-ai-autonomous-systems
skills: [AI-003, SO-002]
dependencies: []
files: [.quinsy-studio/knowledge-base/agentic-loop-playbook.md, .quinsy-studio/CHANGELOG.md]
signal: architecture-gap
source: affiliate-platform
infusion_kind: process
infusion_path: knowledge-base/agentic-loop-playbook.md
train_skills: [AI-003]
created: 2026-09-12
---

## Target
A studio playbook for designing agentic/learning loops in any product. Core rules: (1) signals feeding dashboards is not learning — learned guidance must live in a store that is read back into generation (versioned playbook entries, each citing evidence, retirable by a human); (2) playbooks evolve only by delta operations (ADD/UPDATE/REMOVE) applied by a deterministic non-LLM merge — full model rewrites cause brevity bias and context collapse (ACE, ICLR 2026); (3) procedural memory is treated as code: versioned, diffable, human-gated promotion, never auto-written; (4) every displayed rate carries a sample size or says "not enough data".

## Scope
Kind `process`. Author `knowledge-base/agentic-loop-playbook.md`: the loop shape (signal → cluster → proposed delta → human confirm → deterministic merge → prompt injection → provenance records versions used), the ACE roles (Generator/Reflector/Curator with LLM only in reflection, never in merge), and the anti-patterns (model rewrites memory; auto-confirmed learning; signals without a consumer). This also applies to the studio's own LO/train loop: LO infusion is a delta into a playbook, not a rewrite of one.

## AC
- Playbook exists; the "loop closes on a store" principle stated product-agnostically
- Studio LO process doc cross-references it (LO infusion = confirmed delta)
- Portability gate passes; CHANGELOG updated; LO moved to done

## Status Change
- **From:** open
- **To:** done
- **Date:** 2026-09-12 23:52
- **Reason:** Infused agentic-loop-playbook.md; learning-loop.md delta cross-ref
