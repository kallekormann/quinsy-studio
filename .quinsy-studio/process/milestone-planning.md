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
Gate 0 — PRD + definitions
Gate 1 — Architecture + ADRs
Gate 2 — Design + mocks + library promotion
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
Milestone kickoff (agent)
  • Write tickets for **active milestone only** → product backlog
  • Tag tickets: milestone: M0
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
├── README.md           # Index: all milestones, status, current milestone
├── revisions.md        # Gate iteration feedback (pre-implementation)
├── M0-mvp-launch.md    # First shippable version — outline
├── M1-pro.md           # Next version — outline
└── M2-*.md             # Optional later versions
```

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
| **Milestone kickoff** | Before first sprint of a milestone | Confirm milestone scope + ticket list for active milestone | Milestone tickets in product backlog |
| **Milestone review** | All milestone tickets `done` | Try the build; approve milestone complete or reject with notes | Milestone marked `complete` |
| **Next milestone planning** | After milestone review | Approve next milestone outline + new tickets before sprint | Next milestone `scope-approved` |

Sprint-level HITL (scope proposal, groom, sprint review) is unchanged — see [human-in-the-loop.md](human-in-the-loop.md).

### Proposed CLI (ceremony)

Document-first; wire into `./studio` incrementally:

```bash
# After gate 2 — agent drafts roadmap (files in docs/phases/)
./studio milestones <project>              # validate / summarize roadmap status

# Human approves milestone roadmap
./studio approve <project> --milestones

# Agent writes tickets for active milestone → product backlog
./studio milestone <project> plan

# When all milestone tickets are done
./studio milestone <project> review
./studio milestone <project> --approve --notes "..."

# Plan next milestone (agent populates backlog)
./studio milestone <project> plan --next
```

Until CLI is wired, follow the same steps manually via files + `./studio resume`.

---

## Ticket rules

### When tickets are created

| Stage | Tickets |
|-------|---------|
| Gate 2 | **No full product backlog** — design approval + library promotion only |
| Milestone kickoff | Tickets for **active milestone only** → `backlog/*.md` |
| Sprint review feedback | `./studio feedback` → clarify → ticket (may tag current or next milestone) |
| Next milestone planning | New milestone tickets + carry-over blocked items |

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
| P2 growth / viral | M2 — Share & retention |

One PRD tier may span two milestones (e.g. P0 MVP + P0 ship-readiness as M0a/M0b) when the human prefers smaller releases.

---

## Agent obligations

After gate 2:

1. Draft `docs/phases/README.md` and at least **M0** + **M1 outline** (M1 may stay `planned`).
2. Stop at roadmap approval — do not populate the full backlog or start sprints.
3. After roadmap approval, write **M0 tickets only** with acceptance criteria.
4. During sprints, only pull tickets for the **current milestone**.
5. When milestone tickets are all `done`, surface **milestone review pending** — do not start next milestone tickets without human approval.
6. Log scope changes in `docs/phases/revisions.md` or the active milestone doc.

---

## References

- [lifecycle.md](lifecycle.md) — where execution planning sits
- [backlog-model.md](backlog-model.md) — product backlog + sprint flow
- [human-in-the-loop.md](human-in-the-loop.md) — sprint + milestone HITL
- [iterative-delivery.md](iterative-delivery.md) — sprint cycle within a milestone
