---
id: LO-0040
title: Component reuse ladder — project component then studio-library; right-rail dock as SaaS UX pattern
type: studio-evolution
status: done
phase: 6
priority: P2
estimate: M
assignee_role: Process Guard (Director)
team: 09-studio-operations-evolution
skills: ['SO-002']
dependencies: []
created: 2026-09-01
updated: 2026-09-01
signal: process-gap
source: moody
---

# LO-0040 — Component reuse ladder — project component then studio-library; right-rail dock as SaaS UX pattern

## Observation

A sprint “fixed” inspector chrome by re-skinning a panel shell with ad-hoc titles/trailing controls instead of **reusing the existing docked rail composition**. The learning was captured too narrowly (one product surface + one eyebrow string) instead of the general rule.

## Impact

- Duplicate / divergent chrome across surfaces that should share one organism
- Rework loops at sprint review
- Studio LO infusions that overfit to a single project ticket wording (violates `studio-abstraction.md` / learning-loop “generalize”)

## Proposal

### 1. Component reuse ladder (always)

1. **Reuse** an existing project or studio-library component when the interaction already exists.
2. If the UI is not yet a component, **extract a project-scoped reusable component** (same app / multiple surfaces) before shipping one-off markup.
3. If the component is **cross-project generic**, promote or author it in **studio-library** (`./studio library promote` / component-creation playbook).

### 2. Right-rail dock pattern (library organism)

**Icon rail navigation + detail panel that opens for the active peer** (`StudioRail` + `StudioPanel` / `StudioDock`) is a reusable chrome organism. Surfaces that need “inspect / tools beside the stage” must mount that composition — not a lookalike card with copied classes or a second hand-rolled header.

### 3. Design / archetype learning (SaaS)

When defining UX/UI for **saas-application** (and similar dense knowledge-work apps), treat **right-rail navigation with detail-rails** as a first-class layout option alongside left nav / top chrome — call it out in gate 2 / design review when the product has inspectable objects, queues, or tool peers.

### Infusion targets

- `knowledge-base/component-creation-playbook.md` — reuse ladder
- `knowledge-base/frontend_playbook.md` — dock + reuse (replace surface-specific inspector recipe)
- `process/human-in-the-loop.md` — generalized DoD
- `process/project-archetypes.md` — saas UX option
- `process/learning-loop.md` — reinforce generalized LO titles
- `studio-library/ui/components/studio-rail/README.md` — pattern framing

## Definition of Done

- [x] Discussed in meta retro
- [x] Implemented (CHANGELOG.md entry)
- [x] Generalized (no project-surface-only rule as the primary learning)
- [x] Skill-matching / QA gate green

## Skills

- SO-002
