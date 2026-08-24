---
id: LO-0002
title: Mature feedback tickets need explicit Scope line in ticket body
type: studio-evolution
status: open
phase: 6
priority: P2
estimate: M
assignee_role: Process Guard (Director)
team: 09-studio-operations-evolution
skills: ['SO-002']
dependencies: []
created: 2026-08-24
---

# LO-0002 — Mature feedback tickets need explicit Scope line in ticket body

## 1. Context & Value
- **Current state:** Observation: Mature feedback tickets need explicit Scope line in ticket body (signal: process-gap, source: moody)
- **Target state:** The studio is improved so this signal does not recur.
- **Value:** The studio learns from projects (dual loop) and improves process, skills, or tooling.

## 2. Technical Constraints
- **Modification scope:** .quinsy-studio/process/, .quinsy-studio/studio-tools/, .quinsy-studio/teams/
- **Rule:** No changes to client projects (studio HQ only)
- **Rule:** Every change → CHANGELOG.md entry
- **Rule:** After implementation: skill-matching test + QA gate green
- **Rule:** Signal: process-gap — Source: moody
- **Playbook:** `process/learning-loop.md` (mandatory)
- **Anti-slop:** No AI clichés, no unnecessary external packages without an ADR

## 3. Acceptance Criteria (BDD)
**Scenario 1:** Studio improvement works
- **Given:** The learning signal (process-gap) occurs again
- **When:** The improved process/skill/tool is applied
- **Then:** The signal no longer occurs or is handled correctly

## Proposal
- Document in `human-in-the-loop.md`: feedback tickets need `**Scope:**` in body when from `--from-feedback`.
- Fix `assess_ticket_maturity` to read `phase` from frontmatter (not body).

## Status
- [x] Discussed in the meta-retro (2026-08-24)
- [x] Partial: `sprint_planning.py` + `human-in-the-loop.md` updated
- [ ] Ticket template / `./studio ticket` auto-injects `**Scope:**` from clarify draft
- [ ] CHANGELOG.md entry on full close

## Skills
- SO-002