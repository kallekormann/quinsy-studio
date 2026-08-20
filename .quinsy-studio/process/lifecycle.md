# Quinsy Studio — 7-Phase Lifecycle

> The binding flow from intake to deployment. The agent works autonomously — **only** at the human gates does it stop and wait for approval.

## Architecture principle

```
Studio (meta level)        ──▶  exists autonomously, improves itself
Project (execution level)  ──▶  executed by the studio, local loop
```

---

## Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        7-PHASE LIFECYCLE                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Phase 1: Intake & PRD Processing                                       │
│     └─▶ read PRD, milestones/tickets, repo/docker init                 │
│                                                                         │
│  Phase 2: Architecture & Design Blueprinting                           │
│     └─▶ ADRs, UI specs based on playbooks                              │
│                                                                         │
│  ═══════════════ HUMAN PHASE GATE 1 ═══════════════                    │
│     └─▶ ./studio approve <project> --gate 1                            │
│                                                                         │
│  Phase 3: Sprint Setup & Backlog Grooming                              │
│     └─▶ move tickets into sprint folders                               │
│                                                                         │
│  Phase 4: Autonomous Sprint Execution                                  │
│     └─▶ write code, test locally in the docker container               │
│                                                                         │
│  Phase 5: Comprehensive QA & Compliance Gate                           │
│     └─▶ validate_anti_slop.py + run_qa_gate.py                         │
│                                                                         │
│  Phase 6: Dual-Loop Knowledge Harvesting                               │
│     └─▶ retro: local learnings (project) + global evolution (studio)   │
│                                                                         │
│  Phase 7: Deployment & Iteration                                       │
│     └─▶ zero-downtime deployment, monitoring                           │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Intake & PRD Processing

**Goal:** understand the PRD, set up the project structure, generate tickets.

| Aspect | Description |
|--------|-------------|
| **Input** | PRD (`projects/[name]/docs/prd.md`) |
| **Output** | validated PRD, generated tickets, repo + docker init |
| **Roles (lead)** | Product Manager, Systems Architect |
| **Roles (support)** | Legal/Privacy Officer (early check) |
| **Human gate** | No — agent works autonomously |

### Flow

1. Read the PRD and check completeness
2. Fill `docs/definitions/` (00-index to 11-assumptions)
3. Determine the archetype and fill out the archetype checklist
4. `./studio init <project> --archetype <type>`
5. `./studio env <project> init` — docker-compose + git
6. `./studio repo <project> create` — GitHub repo (only with approval)
7. Generate tickets: `generate_ticket_manifest.py`
8. Create initial ADRs for fundamental decisions
9. Initialize `status.json`
10. Check gate 0

### Gate 0 (internal)

- [ ] PRD validated and complete
- [ ] Definitions documents filled
- [ ] Archetype determined
- [ ] At least 1 ADR present
- [ ] Repo + docker initialized

---

## ═══════════════ HUMAN GATE 0 — Intake ═══════════════

> After Phase 1: user approves PRD + `docs/definitions/`.
> CLI: `./studio approve <project> --gate 0`

---

## Phase 2: Architecture Blueprinting

**Goal:** system architecture, data model, ADRs — **no UI mocks yet**.

| Output | Path |
|--------|------|
| Blueprint | `docs/architecture/BLUEPRINT.md` |
| Data model | `docs/architecture/data-model.md` |
| ADRs | `docs/adr/ADR-*.md` |

CLI: `./studio blueprint <project>`

## ═══════════════ HUMAN GATE 1 — Architecture ═══════════════

> User approves tech stack, data model, ADRs.
> CLI: `./studio approve <project> --gate 1`
> Iteration: `./studio revise <project> --gate 1 --feedback "..."`

---

## Phase 3: Design (prototype)

**Goal:** design tokens, atomic components, Next.js mocks, sticker sheet.

| Output | Path |
|--------|------|
| Design spec | `design/DESIGN.md` |
| Mock scope | `design/DESIGN-SCOPE.md` (`journey` \| `core-views`) |
| Prototype | `design/prototype/` (Next.js) |
| Tokens | `ui/tokens/design-tokens.json` |
| Components | `ui/components/atoms|molecules|organisms/` |
| Sticker sheet | `design/prototype/app/sticker-sheet/` |

CLI: `./studio design <project> --scope journey|core-views`

## ═══════════════ HUMAN GATE 2 — Design ═══════════════

> User approves visual direction + mocks. **Tickets are generated here.**
> CLI: `./studio approve <project> --gate 2`
> Iteration: `./studio revise <project> --gate 2 --feedback "..."`

---

## Phase 4: Sprint Setup & Backlog Grooming

**Goal:** organize tickets into sprints, plan capacity.

| Aspect | Description |
|--------|-------------|
| **Input** | approved architecture blueprint |
| **Output** | first sprint with assigned tickets |
| **Roles (lead)** | Product Manager, Backlog Owner |
| **Roles (support)** | Systems Architect |
| **Human gate** | No — agent works autonomously |

### Flow

1. `./studio sprint <project>` — create a sprint + **backlog validation** report
2. `./studio groom <project>` — human reviews validation + plan.md
3. `./studio groom <project> --approve` — **required** before `./studio move … implement`
4. Prioritize tickets (RICE, MoSCoW) — move deferrals out of sprint in plan.md
5. Identify dependencies
6. Estimate capacity
7. Assign tickets to the sprint
8. Fill out `plan.md`
9. Run a blocked review
10. Write the grooming protocol

---

## Phase 4: Autonomous Sprint Execution

**Goal:** write code, test locally, deliver iteratively.

| Aspect | Description |
|--------|-------------|
| **Input** | sprint with assigned tickets |
| **Output** | implemented code with local tests |
| **Roles (lead)** | Frontend Engineer, Backend Engineer |
| **Roles (support)** | Database Specialist, QA Specialist |
| **Human gate** | No — agent works autonomously |

### Flow per ticket (9 steps)

1. Intake & understanding
2. Decomposition & dependencies
3. Conception/design
4. Implementation (clean code, TDD)
5. Self-check (tests, lint, review)
6. QA gate (`./studio gate <project>`)
7. Docs & ADR sync
8. Reuse review (`./studio promote`)
9. Completion → status `done`

### Rules

- **No code without a ticket**
- **Test-first (TDD)**
- **Clean code / SOLID**
- **Follow anti-slop**
- **Docker container for local testing**

---

## Phase 5: Comprehensive QA & Compliance Gate

**Goal:** formal QA, security audit, anti-slop audit, GDPR check.

| Aspect | Description |
|--------|-------------|
| **Input** | implemented code |
| **Output** | QA report, security audit, anti-slop report |
| **Roles (lead)** | QA Specialist, Security Engineer, Legal/Privacy Officer |
| **Roles (support)** | AI-Autonomous Systems (anti-slop) |
| **Human gate** | No — agent works autonomously |

### Flow

1. Run `validate_anti_slop.py`
2. Run `run_qa_gate.py`
3. Security scan (OWASP, dependencies)
4. GDPR compliance check
5. Performance tests (core web vitals)
6. Accessibility check (a11y)
7. Anti-slop audit: 0 error violations
8. Gate 5 must be green
9. Generate the QA report

---

## Phase 6: Dual-Loop Knowledge Harvesting

**Goal:** learn from the sprint — strict separation local vs. global.

| Aspect | Description |
|--------|-------------|
| **Input** | sprint experience, QA results |
| **Output** | local learnings + global studio evolution |
| **Roles (lead)** | Process Guard, Platform Architect |
| **Roles (support)** | Documentation Writer, Agile Coach |
| **Human gate** | No — agent works autonomously |

### Flow

1. Run the sprint retrospective
2. Collect learning items (`./studio learn`)
3. **Local loop:** project-specific learnings → `projects/[name]/docs/local_learnings.md`
4. **Global loop:** universal improvements → `.quinsy-studio/knowledge-base/`
5. Update playbooks (global loop)
6. Optimize python tools (global loop)
7. Update CHANGELOG
8. `./studio retro <project>`

---

## Phase 7: Deployment & Iteration

**Goal:** deploy the production environment, monitor, plan the next iteration.

| Aspect | Description |
|--------|-------------|
| **Input** | QA-checked code |
| **Output** | live system, monitoring, next sprint planning |
| **Roles (lead)** | Platform Architect, Backend Security & Infrastructure |
| **Roles (support)** | Growth Manager, Data Analyst |
| **Human gate** | No — but a deployment approval is recommended |

### Flow

1. Staging deployment
2. Smoke tests
3. Production deployment (zero-downtime)
4. Set up monitoring & alerting
5. Release notes
6. Plan the next sprint
7. Back to phase 3/4 (iterative)

---

## Gate definitions

| Gate | Phase | Checkpoints |
|------|-------|-------------|
| **Gate 0** | Phase 1→2 | PRD + definitions — **user approval** |
| **Gate 1** | Phase 2→3 | architecture blueprint — **user approval** |
| **Gate 2** | Phase 3→4 | design + mocks — **user approval** (tickets generated) |
| **Gate 3** | Phase 4 (internal) | sprint planned, tickets assigned |
| **Gate 5** | Phase 5 (internal) | QA, security, anti-slop, GDPR — all green |

---

## Dual-loop integration

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     DUAL-LOOP INTEGRATION                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  LOCAL LOOP (project world)            GLOBAL LOOP (studio world)      │
│  ─────────────────────────            ──────────────────────────        │
│  • Project-specific bugs               • Universal playbooks            │
│  • Niche insights                      • Python tooling updates         │
│  • Workarounds                         • Anti-slop rule updates         │
│  • Storage: projects/[name]/           • Storage: .quinsy-studio/       │
│    docs/local_learnings.md              knowledge-base/                  │
│                                                                         │
│  ⚠️ Does NOT affect other             ✅ Applies to ALL future          │
│     projects                              projects                       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## References

- `.quinsy-studio/process/gates.md` — gate definitions in detail
- `.quinsy-studio/process/learning-loop.md` — dual-loop learning
- `.quinsy-studio/process/ticket-workflow.md` — 9-step ticket workflow
- `.quinsy-studio/knowledge-base/` — playbooks & protocols
- `studio-tools/` — python automation
