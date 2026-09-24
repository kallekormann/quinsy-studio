---
id: LO-0332
title: Distill selected design catalog into Team 10 playbooks; Figma handoff as extension; no UX-009
type: studio-evolution
status: done
phase: 6
priority: P1
estimate: L
assignee_role: Product Designer (Director)
team: 10-product-design-experience
skills: [UX-001, UX-002, UX-004, UX-005, UX-006, UX-007, UX-008, SO-003]
dependencies: [LO-0331]
files: [.quinsy-studio/knowledge-base/product-ux-playbook.md, .quinsy-studio/knowledge-base/interaction-ux-playbook.md, .quinsy-studio/knowledge-base/ux-research-playbook.md, .quinsy-studio/knowledge-base/design-science-playbook.md, .quinsy-studio/knowledge-base/anti-slop-design-ux.md, .quinsy-studio/knowledge-base/aesthetic-presets.md, .quinsy-studio/knowledge-base/skill-extensions/]
sprint: HQ-SKILL-02
epic: HQ-SKILL
signal: design-gap
source: studio-hq
infusion_kind: playbook
infusion_path: knowledge-base/interaction-ux-playbook.md
train_skills: [UX-002, UX-005, UX-007]
created: 2026-09-24
---

## Target
Selected catalog design skills (`frontend-design`, `ui-design-system`, `ux-researcher-designer`, `avoid-ai-writing`, `figma-implement-design`, **`scroll-experience`**, **`theme-factory`**) become **Do/Don’t/spec-fail** in existing Team 10 playbooks. No UX-009 Delight. Figma is a skill-extension under UX-002/005. Scroll narrative loads from UX-002/UX-007 + delight (not a new ID). Theme-factory is the **HITL pick + cohesive apply** ritual: product UI maps to aesthetic presets/tokens; slides/PDF may use factory packs after human choice.

## Scope
Infusion-delta only (no full-file rewrite). Point thin skills at new bullets. `figma-token-handoff.md` extension. Skip **shadcn palettes** (not the kit). Distill `creative-design/scroll-experience`: enhance scroll, never hijack; mobile + `prefers-reduced-motion`; content readable without animation. Distill `creative-design/theme-factory`: show repertoire → wait for HITL → apply one palette+type pair; **do not** replace the 17 aesthetic presets or paste catalog hex into product CSS. Epic: process/hq-skill-advancement-sprints.md.

## AC
- Playbooks cite catalog as source, distill operational rules
- `interaction-ux-playbook.md` and `delight-playbook.md` (and/or `visual-storytelling-playbook.md`) include scroll-experience Do/Don’t/spec-fail
- `aesthetic-presets.md` / `design-science-playbook.md` / Brand Guardian: theme-factory HITL picker + token mapping
- `skill-extensions/README.md` lists figma-token-handoff
- UX-008 / anti-slop-design points at avoid-ai-writing ideas without pasting the catalog
- CHANGELOG; no new UX skill ID

## Out of scope
Replacing aesthetic presets with “Ocean Depths” etc. as product tokens. New Team 10 skill IDs. Product mocks. GSAP as a studio-library default.
