# Quinsy Studio — Lifecycle

> The binding flow from intake to deployment. The agent works autonomously — **only** at the human gates does it stop and wait for approval.

**Human HITL is named by gate, not by “Phase N”.** Numbered phases below are execution slices. If a doc disagrees with this table, **this table wins**.

## Architecture principle

```
Studio (meta level)        ──▶  exists autonomously, improves itself
Project (execution level)  ──▶  executed by the studio, local loop
```

---

## Overview (gates first)

| HITL / slice | What | CLI |
|--------------|------|-----|
| **Gate 0** | PRD + definitions (as-built if adopt) | `./studio approve --gate 0` |
| **Gate 1** | Architecture (ADRs, stack, persistence) | `./studio approve --gate 1` (refuses if gate 0 pending) |
| **Gate 2a** | Design direction (interview + DESIGN.md) | `./studio approve --gate 2a` (refuses if gate 1 pending) |
| **Gate 2b** | Project kit (tokens, A/M/O, sticker) | `./studio approve --gate 2b` (refuses if 2a pending). Bare `--gate 2` is refused. |
| **Milestones** | Version plan `docs/phases/` | `./studio approve --milestones` |
| Sprint setup | Scope the current train phase, then groom. An empty phase is skipped | `./studio sprint` → `--approve-scope` → `groom` |
| Sprint execute | After gate 2b: design phase, then architecture phase, then implementation. Empty phases skip | `./studio sprint` then `./studio execute` |
| Design / arch packets | Written during that phase, then one batch signature | `./studio approve-design <p> --phase` / `approve-arch <p> --phase` |
| **QA level 5** | Lint/tests/build/smoke + receipt skill QA (not a human phase gate) | `./studio gate --level 5` before `move … done` |
| **Cadence review** | Every N implementation sprints (default 2) | `./studio review` → `--approve` |
| Hygiene | Lint/debt batch after implementation batches | `./studio sprint --kind hygiene` |
| Harvest | Portable LO + HQ train session; product execute INFORM the count | `docs/studio-learnings-local.md` vs HQ playbooks |
| Deploy | Staging → prod (release is HITL) | project RUNBOOK |

ASCII “Phase 1…8” in older notes is the same flow: intake → architecture → design → sprint → QA → harvest → deploy. **Do not invent Phase 8 as a ninth human gate.**

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
>
> **Existing codebase:** `./studio adopt` overlays studio docs; gate 0 is **as-built truth** + synthesized PRD. See [brownfield-adopt.md](brownfield-adopt.md).

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

## Phase 3: Design direction (2a) then project kit (2b)

**2a goal:** unique signed `design/DESIGN.md` from a human interview, then a UX-008 critique. Prototype is blocked until every critique line is PASS.

**2b goal:** pulled library kit styled with project tokens, shell routes plus the PRD journey, sticker sheet — **in the project**. Approving 2b copies that prototype into the product app and keeps `design/prototype/` as the baseline. No library promote of product look.

> **Adopted repo:** 2a is keep vs evolve; 2b is token-map of **what exists**. Do **not** scaffold a parallel Next.js prototype. See [brownfield-adopt.md](brownfield-adopt.md).

| Output | Path |
|--------|------|
| Discovery | `docs/design/discovery.md` |
| Design spec | `design/DESIGN.md` |
| Direction critique | `design/DIRECTION-CRITIQUE.md` (UX-008, before gate 2a HITL) |
| Mock scope | `design/DESIGN-SCOPE.md` (`journey` \| `core-views` plus required shell) |
| Prototype | `design/prototype/` (Next.js, after 2a). Remains the visual baseline after 2b. |
| Product app | `app/` — copy of the prototype mocks after `./studio approve --gate 2b` |
| Baseline note | `docs/design/baseline.md` |
| CSS tokens | `ui/tokens/design-tokens.css` |
| Components | pulled `ui/components/<slug>/` plus any project atoms/molecules/organisms |
| Sticker sheet | `design/prototype/app/sticker-sheet/` |

CLI: `./studio design <project> --discovery` then `--scope journey|core-views`

## ═══════════════ HUMAN GATE 2a — Direction ═══════════════

> User signs the identity after the critique passes. Prototype stays blocked.
> The human is not the first person to notice slop. Execute stays IMPLEMENT while `DIRECTION-CRITIQUE.md` has a FAIL.
> CLI: `./studio approve <project> --gate 2a`
> Iteration: `./studio revise <project> --gate 2a --feedback "..."`

## ═══════════════ HUMAN GATE 2b — Project kit ═══════════════

> User approves the live kit. Approval copies the prototype into the product app and leaves the prototype as the baseline. **Do not** merge product look into studio-library; execution backlog is **not** filled until milestone kickoff.
> CLI: `./studio approve <project> --gate 2b`
> Iteration: `./studio revise <project> --gate 2b --feedback "..."`

---

## Execution planning — Milestone roadmap (post gate 2)

**Goal:** outline product versions (milestones) so humans see maturity and scope beyond “backlog empty.”

| Aspect | Description |
|--------|-------------|
| **Input** | Approved PRD, blueprint, design, gate 2 artifacts |
| **Output** | `docs/phases/README.md` + `M0-*.md`, `M1-*.md`, …; tickets for **active milestone only** |
| **Roles (lead)** | Product Manager, Systems Architect |
| **Human gate** | **Yes** — approve milestone roadmap before sprints |

### Flow

1. Agent drafts milestone index + outlines from PRD P0/P1/P2 and blueprint boundaries
2. Human reviews goals, in/out scope, and HITL decision points per milestone
3. Human approves roadmap (`./studio approve <project> --milestones` — see [milestone-planning.md](milestone-planning.md))
4. Agent writes tickets for the **first active milestone** → product backlog (`milestone: M0`)
5. Human confirms milestone kickoff ticket list (may adjust before first `./studio sprint`)

### Milestone boundary (repeat)

When all tickets for the current milestone are `done` and milestone success criteria are met:

1. Human **milestone review** — approve version complete or send back
2. Agent plans **next milestone** — update `docs/phases/`, write new tickets to backlog
3. Carry over `backlog/blocked/` and feedback-sourced tickets; re-tag `milestone` if needed
4. Resume sprint loop (`./studio sprint` → `--approve-scope` → …)

See [milestone-planning.md](milestone-planning.md) for templates and ticket rules.

---

## Phase 4: Sprint Setup & Backlog Grooming

**Goal:** organize tickets into sprints, plan capacity.

| Aspect | Description |
|--------|-------------|
| **Input** | approved milestone roadmap + product backlog for current milestone |
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

## Phase 5: Autonomous Sprint Execution

**Goal:** write code, test locally, deliver iteratively.

| Aspect | Description |
|--------|-------------|
| **Input** | sprint with assigned tickets |
| **Output** | implemented code with local tests |
| **Roles (lead)** | Frontend Engineer, Backend Engineer |
| **Roles (support)** | Database Specialist, QA Specialist |
| **Human gate** | No mid-sprint ticket ACK on an implementation phase. Design and architecture phases sign once at the end. An unsigned ticket does not freeze a ready sibling. |

### Flow per ticket (9 steps)

1. Intake & understanding
2. Decomposition & dependencies
3. Conception/design — **design-track:** Team 10 spec; human `./studio approve-design`. **Else:** stay on gate-2 design system
4. Implementation (clean code, TDD) — blocked until `approve-design` for design-track types
5. Self-check (tests, lint, review)
6. QA gate (`./studio gate <project>`)
7. Docs & ADR sync
8. Reuse review (`./studio promote`)
9. Completion → status `done`

### Rules

- **No code without a ticket**
- **No human checkpoint between sprint tickets** — finish the sprint, then `./studio review`
- **`./studio move … implement` blocked** when sprint review is pending or sprint is closed
- **Test-first (TDD)**
- **Clean code / SOLID**
- **Follow anti-slop**
- **Docker container for local testing**
- **UI kit peers** in the product React `package.json` from scaffold (`docs/setup/ui-kit.md`)
- **Agent applies pending migrations** when the DB is reachable (local or VPS), then informs the human. Do not ask the operator to migrate. Destructive reset is HITL.

---

## Phase 6: Comprehensive QA & Compliance Gate

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
7. Gate 5 must be green
8. Generate the QA report

**Before `./studio move … done`:** run `./studio gate <project> --level 5` (build + runtime smoke + tests). Level 2 lint-only passes miss client runtime crashes.

---

## Phase 7: Dual-Loop Knowledge Harvesting

**Goal:** learn from the sprint — strict separation local vs. global.

| Aspect | Description |
|--------|-------------|
| **Input** | sprint experience, QA results |
| **Output** | local learnings + global studio evolution |
| **Roles (lead)** | Process Guard, Platform Architect |
| **Roles (support)** | Documentation Writer, Agile Coach |
| **Human gate** | **Cadence** — `./studio review --approve` every N implementation sprints; off-cadence batches go to retro |

### Flow

1. Human tries shipped work (`./studio review <project>`)
2. Approve or reject sprint (`./studio review --approve` / `--reject`) — do not linger for work that is still only feedback (LO-0144)
3. Capture feedback (`./studio feedback`) — not direct tickets
4. Clarify + ticket from feedback (`./studio clarify` → `./studio ticket --from-feedback`)
5. Run the sprint retrospective (`./studio retro <project>`)
6. Collect learning items (`./studio learn`)
7. **Local loop:** project-specific learnings → `projects/<name>/docs/studio-learnings-local.md`
8. **Global loop:** universal improvements → `.quinsy-studio/knowledge-base/`
9. Groom backlog (`./studio groom`) + plan next sprint (`./studio sprint <project>`)
10. If milestone tickets are all `done` → **milestone review** before next milestone planning (see [milestone-planning.md](milestone-planning.md))

---

## Phase 8: Deployment & Iteration (not a numbered human gate)

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
| **Gate 0** | After intake / as-built | PRD + definitions — **user approval** |
| **Gate 1** | After architecture | ADRs / stack — **user approval** |
| **Gate 2** | After design track | design + mocks — **user approval** (library promotion) |
| **Milestones** | Post gate 2 | milestone roadmap — **user approval** (`--milestones`) |
| **Milestone review** | End of M0, M1, … | version complete — **user approval** before next milestone backlog |
| **Gate 3** | Sprint setup (internal) | sprint planned, tickets assigned — **not** a human stop |
| **QA level 5** | Before `move … done` | QA, security, anti-slop, GDPR — all green (`./studio gate --level 5`) |

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
│    docs/studio-learnings-local.md        knowledge-base/                  │
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
- `.quinsy-studio/process/milestone-planning.md` — milestone roadmap + version gates
- `.quinsy-studio/knowledge-base/` — playbooks & protocols
- `studio-tools/` — python automation
