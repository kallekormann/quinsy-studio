# Milestone Execution Planning

> After design (gate 2), define **product milestones** (versions) before sprints begin.
> Milestones give humans a durable map of maturity; sprints deliver increments **within** the active milestone.

## Why this exists

Gate 2 proves **how** the product looks and behaves in mocks. It does not answer:

- Which **versions** ship in what order (M0 free MVP → M1 Pro → …)
- When the project is **mature enough to release**
- What tickets belong to **this milestone** vs a later one

Without milestone planning, an empty product backlog looks like “the project is done” when only one sprint tranche finished.

## Concepts

| Term | Meaning | Horizon |
|------|---------|---------|
| **Milestone** | Product version tranche (M0, M1, …) | Weeks to months, multiple sprints |
| **Sprint** | Tactical delivery batch | Days to ~2 weeks |
| **Product backlog** | Unscheduled tickets (`backlog/*.md`) | Feeds sprint planning |
| **Sprint review** | Human approves **shipped sprint** | End of each sprint |
| **Milestone review** | Human approves **completed milestone** | When all milestone tickets are `done` |

Milestones are documented under `projects/<p>/docs/phases/`.

---

## Placement in the lifecycle

```
Gate 0 — PRD + definitions  (adopt: as-built truth + synthesized PRD)
Gate 1 — Architecture + ADRs  (adopt: as-is, no stack swap)
Gate 2 — Design + mocks + library promotion  (adopt: design of what exists; no fake prototype)
    │
    ▼
Execution planning (agent)
  • docs/phases/README.md — milestone index + status
  • docs/phases/M0-*.md, M1-*.md — outline per version
    │
    ▼
HITL — Approve milestone roadmap (human)
    │
    ▼
Milestone kickoff (agent as Product Manager)
  • Write tickets for **active milestone only** → product backlog
  • Tag tickets: milestone: M0
  • Staff every ticket (PM-004): owner skill first, required companions, `## Staffing`
  • List the teams the milestone needs; add the missing tickets (legal pages,
    consent, deploy, backups, a11y pass) instead of leaving a team unstaffed
    │
    ▼
┌─── Sprint loop (within milestone) ───────────────────────────┐
│  ./studio sprint → --approve-scope → groom → implement       │
│  ./studio review --approve → retro → next sprint             │
└──────────────────────────────────────────────────────────────┘
    │
    ▼ (all milestone tickets done + milestone DoD met)
HITL — Milestone review (human)
    │
    ▼
Next milestone planning (agent)
  • Update docs/phases/ for M1
  • Write M1 tickets → product backlog
  • Carry over blocked / feedback tickets (re-tag milestone if needed)
    │
    ▼
Back to sprint loop for M1
```

---

## docs/phases/ layout

```
projects/<p>/docs/phases/
├── README.md           # Index: every milestone, status, current milestone
├── revisions.md        # Gate iteration feedback (pre-implementation)
├── M0-*.md             # First version
├── M1-*.md             # Next version
└── M2-*.md … Mn-*.md   # As many later versions as the PRD needs
```

There is no cap of three or four. A large PRD, or a PRD with many source files, gets one milestone per version required to deliver that material.

### Milestone doc template

Each `M*.md` file includes:

| Section | Purpose |
|---------|---------|
| **Goal** | One sentence — why this version exists |
| **In scope** | Features / outcomes included |
| **Out of scope** | Explicit deferrals to later milestones |
| **Success criteria** | Measurable “done” for the milestone |
| **HITL decisions** | Choices human must make before or during (hosting, pricing, legal entity, …) |
| **Status** | `planned` → `scope-approved` → `in-progress` → `complete` |
| **Tickets** | Links or IDs once backlog is populated |

### README.md index (required)

The index must show at a glance:

- Current milestone (`M0`, `M1`, …)
- Status per milestone
- Link to each milestone doc
- Relationship to PRD P0 / P1 / P2 (if used)

---

## Human gates (HITL)

| Gate | When | Human action | Agent may proceed when |
|------|------|--------------|------------------------|
| **Roadmap approval** | After gate 2, roadmap drafted | Review `docs/phases/README.md` + milestone outlines; approve | Roadmap marked `scope-approved` |
| **Milestone review** | All milestone tickets `done` | Try the build; approve milestone complete or reject with notes | Milestone marked `complete` |
| **Next milestone planning** | After milestone review | Covered by `--approve`; the agent runs `plan --next` and `plan` | Tickets stamped with the next milestone |

Sprint-level HITL (scope proposal, groom, sprint review) is unchanged — see [human-in-the-loop.md](human-in-the-loop.md).

### CLI (wired)

```bash
./studio milestone <project>                       # roadmap table, active milestone, coverage gaps
./studio approve <project> --milestones            # HITL — refuses an uncovered required area
./studio milestone <project> plan                  # tickets from `## Tickets` lines, staffed, stamped milestone: M<n>
./studio milestone <project> review                # when every M<n> ticket is done: state + recommendations
./studio milestone <project> --approve --notes ".."# HITL — product decision
./studio milestone <project> plan --next           # activate the next milestone
```

Execute drives this: after gate 2b the next step is the roadmap (IMPLEMENT until coverage passes, then HITL); between sprints a finished milestone routes to `review` and then to the `--approve` HITL. `./studio sprint` refuses without an approved roadmap and an active milestone (hygiene sprints excepted). Coverage: [milestone-coverage-checklist.md](../knowledge-base/milestone-coverage-checklist.md). Template: `studio-templates/phases/milestone.md`.

---

## Ticket rules

### When tickets are created

| Stage | Tickets |
|-------|---------|
| Gate 2 | **No full product backlog** — design approval + library promotion only |
| Milestone kickoff | Tickets for **active milestone only** → `backlog/*.md` |
| Sprint review feedback | `./studio feedback` → clarify → ticket (may tag current or next milestone) |
| Next milestone planning | New milestone tickets + carry-over blocked items |

Every ticket is staffed by the Product Manager with PM-004 ([ticket-staffing.md](../teams/06-product-management-operating-model/skills/ticket-staffing.md)). `./studio groom` refuses a sprint with an unstaffed ticket or a missing required companion.

Gate 2 may still produce a **ticket manifest sketch** (`docs/ticket-manifest.json`) as input to milestone planning — not the execution backlog.

### Ticket metadata

```yaml
---
id: PROJ-0012
title: Task edit and delete
status: backlog
milestone: M0
priority: P0
---
```

Sprint planning (`./studio sprint`) draws from product backlog tickets tagged with the **current milestone**, plus any blocked or human-added tickets the groom approves.

### Milestone completion

A milestone is complete when:

1. Every ticket with `milestone: M0` is in `backlog/done/` (or explicitly deferred with human approval)
2. Milestone success criteria in `docs/phases/M0-*.md` are met
3. Human runs **milestone review** (distinct from sprint review)

Optional: final sprint of a milestone includes deploy / release notes if the milestone goal is “ship to production”.

---

## Relationship to PRD P0 / P1 / P2

PRD scope tiers are **input** to milestone outlines — not identical to milestones.

Example mapping:

| PRD tier | Typical milestone |
|----------|-------------------|
| P0 core loop | M0 — MVP launch |
| P1 Pro / monetization | M1 — Pro pass |
| P2 growth / viral | a later milestone |

One PRD tier may span many milestones. The count comes from the PRD and `docs/intake/sources/`, not from a fixed list.

---

## Agent obligations

After gate 2:

1. Draft `docs/phases/README.md` and one outline per version the PRD needs. M0 is the first. Continue through M1, M2, M3, and further until the PRD and its source files are covered. Do not stop at three or four.
2. Stop at roadmap approval — do not populate the full backlog or start sprints.
3. After roadmap approval, write **M0 tickets only** with acceptance criteria.
4. During sprints, only pull tickets for the **current milestone**.
5. When milestone tickets are all `done`, execute routes to `./studio milestone <p> review`; the human signs with `--approve` before `plan --next`.
6. Log scope changes in `docs/phases/revisions.md` or the active milestone doc.
7. **Post-launch direction** that is conceptual (not sprint-sized): use [amendment intake](amendment-intake.md) — not `./studio feedback` alone.

---

## References

- [lifecycle.md](lifecycle.md) — where execution planning sits
- [backlog-model.md](backlog-model.md) — product backlog + sprint flow
- [human-in-the-loop.md](human-in-the-loop.md) — sprint + milestone HITL
- [iterative-delivery.md](iterative-delivery.md) — sprint cycle within a milestone
- [amendment-intake.md](amendment-intake.md) — conceptual direction → milestones + tickets
