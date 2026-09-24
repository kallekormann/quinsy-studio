---
id: LO-0331
title: Subscribe superpowers and Anthropic document skills; conflict-matrix those sources; refuse aitmpl blob install
type: studio-evolution
status: done
phase: 6
priority: P1
estimate: M
assignee_role: Studio Automation Engineer (Director)
team: 09-studio-operations-evolution
skills: [SO-001, SO-003]
dependencies: []
files: [.quinsy-studio/skill-dependencies.json, .quinsy-studio/knowledge-base/external_skills_conflict_matrix.md, .quinsy-studio/teams/skill-registry.md]
sprint: HQ-SKILL-01
epic: HQ-SKILL
signal: tooling-gap
source: studio-hq
infusion_kind: process
infusion_path: process/hq-skill-advancement-sprints.md
train_skills: [SO-001]
created: 2026-09-24
---

## Target
Studio imports **named** skill repos (`obra/superpowers`, `anthropics/skills`) via `skill-dependencies.json` + `./studio update-skills`. The aitmpl marketplace is a **catalog to read**, not an install target.

## Scope
Add two dependency entries (team 09 / 10 as documented in the epic). Conflict matrix rows: executing-plans blocked; document skills optional; anti-slop overrides. INDEX.md after import. Sprint `HQ-SKILL-01`. Epic: process/hq-skill-advancement-sprints.md.

## AC
- `skill-dependencies.json` lists superpowers and anthropics/skills with why + team
- conflict matrix forbids `executing-plans` and wholesale `npx claude-code-templates`
- `./studio update-skills` clone path documented; CHANGELOG

## Out of scope
Installing 910 catalog skills. Bright Data MCP. Product trees.
