# Quinsy Studio — Iterative Delivery

> From phase 3 on, work is iterative. Sprints, grooming and the backlog board are the engines.

## Core principle

```
Iterative = plan → build → check → learn → repeat
```

No sprint is identical; every sprint learns from the previous one.

---

## Sprint cycle

```
┌─────────────────────────────────────────────────────────┐
│                    SPRINT CYCLE                         │
└─────────────────────────────────────────────────────────┘

 ┌──────────────┐
 │   SPRINT     │ ◀──────────────────────────────┐
 │   START      │                                │
 └──────┬───────┘                                │
        │                                        │
        ▼                                        │
 ┌──────────────┐                                │
 │   GROOMING   │                                │
 │   (Board)    │                                │
 └──────┬───────┘                                │
        │                                        │
        ▼                                        │
 ┌──────────────┐                                │
 │   TICKETS    │                                │
 │   WORK ON    │                                │
 └──────┬───────┘                                │
        │                                        │
        ▼                                        │
 ┌──────────────┐                                │
 │   QA GATE    │                                │
 └──────┬───────┘                                │
        │                                        │
        ▼                                        │
 ┌──────────────┐                                │
 │   RETRO      │ ──── learning items ──────────┘
 │   + REVIEW   │
 └──────────────┘
```

---

## Sprint structure

Every sprint has:
- **Name:** `SPRINT-01`, `SPRINT-02`, ...
- **Duration:** variable (depending on the project)
- **Focus:** one or more features
- **Goal:** clear definition of done

### Sprint directory

```
<project>/sprints/
├── SPRINT-01/
│   ├── plan.md          # sprint planning
│   ├── summary.md       # sprint summary
│   ├── grooming.md      # grooming protocol
│   └── retro.md         # retrospective
├── SPRINT-02/
│   └── ...
```

---

## Sprint planning

```bash
./studio sprint <project>
```

Creates `sprints/SPRINT-NN/plan.md` with template:

```markdown
# Sprint Planning — SPRINT-NN

**Goal:** <what should be achieved in this sprint?>
**Start:** YYYY-MM-DD
**End:** YYYY-MM-DD
**Capacity:** <realistic estimate>

## Tickets in this sprint

| Ticket | Title | Phase | Priority | Estimate |
|--------|-------|-------|----------|----------|
| TICKET-NNN | ... | 4 | P1 | M |

## Dependencies
- ...

## Risks
- ...

## Definition of Done
- [ ] All tickets in status "done"
- [ ] QA test green
- [ ] Anti-slop audit: 0 errors
- [ ] Retrospective done
- [ ] Summary written
```

---

## Grooming

```bash
./studio groom <project>
```

Grooming is the weekly board meeting:

### Grooming agenda

1. **Check blocked tickets**
   - Can the blocker be resolved?
   - Should the ticket be closed?

2. **Prioritization**
   - Are the priorities still current?
   - Should tickets be reordered?

3. **Dependencies**
   - Are there new dependencies?
   - Are dependencies resolved?

4. **Capacity**
   - Is the sprint planned realistically?
   - Should tickets be moved?

5. **New tickets**
   - Are there new requirements?
   - Should they be created as tickets?

### Grooming protocol

```markdown
# Grooming Protocol — SPRINT-NN

**Date:** YYYY-MM-DD
**Participants:** Project Manager, ...

## Blocked tickets
| Ticket | Reason | Action |
|--------|--------|--------|
| ... | ... | ... |

## Prioritization changes
| Ticket | New priority | Reason |
|--------|--------------|--------|
| ... | ... | ... |

## New tickets
| Ticket | Title | Priority |
|--------|-------|----------|
| ... | ... | ... |

## Capacity adjustments
- ...

## Next steps
- ...
```

---

## Backlog board

The board shows all tickets by their current status:

```bash
./studio board <project>
```

### Board view

```
┌─────────────┬─────────────┬─────────────┬─────────────┬─────────────┐
│    OPEN     │  IN PROGRESS│    QA       │   REVIEW    │    DONE     │
├─────────────┼─────────────┼─────────────┼─────────────┼─────────────┤
│ TICKET-008  │ TICKET-007  │ TICKET-006  │ TICKET-005  │ TICKET-001  │
│ TICKET-009  │             │             │             │ TICKET-002  │
│ TICKET-010  │             │             │             │ TICKET-003  │
│ TICKET-011  │             │             │             │ TICKET-004  │
└─────────────┴─────────────┴─────────────┴─────────────┴─────────────┘
```

### Board filters

```bash
./studio board <project> --phase 4
./studio board <project> --priority P0
./studio board <project> --assignee "frontend"
```

---

## Ticket movement

```bash
# move a ticket to the next status
./studio move <project> TICKET-NNN <status> [--reason "Reason"]

# examples
./studio move nudge TICKET-007 implement --reason "Implementation started"
./studio move nudge TICKET-007 qa --reason "QA started"
./studio move nudge TICKET-007 done --reason "All criteria met"
```

**Rule:** every movement is documented (status change + reason).

---

## Sprint review

At the end of each sprint:

```markdown
# Sprint Review — SPRINT-NN

## Achieved
- [x] TICKET-001: ...
- [x] TICKET-002: ...

## Not achieved (moved)
- [ ] TICKET-003: ... (reason: ...)

## Metrics
- Planned: 5 tickets
- Completed: 3 tickets
- Rate: 60%
- Average duration: 2 days/ticket

## Velocity
- SPRINT-01: 3 tickets
- SPRINT-02: 4 tickets (+1)
- Trend: 📈
```

---

## Retrospective

After each sprint:

```bash
./studio retro <project>
```

### Retro template

```markdown
# Retrospective — SPRINT-NN

## What went well? 🟢
- ...

## What went badly? 🔴
- ...

## What can we improve? 🟡
- ...

## Learning items
| Item | Signal | Source | Action |
|------|--------|--------|--------|
| ... | ... | ... | ... |

## Action items
- [ ] ... (owner: ...)
- [ ] ... (owner: ...)
```

---

## Learning items

```bash
./studio learn "<title>" --signal <signal> --source <source>
```

### Learning signals

| Signal | Meaning |
|--------|---------|
| `gate-fail` | gate check failed |
| `rework` | work had to be redone |
| `tooling-gap` | tooling was missing or insufficient |
| `design-gap` | design specification was insufficient |
| `process-gap` | process step was unclear |
| `knowledge-gap` | knowledge was missing |

### Learning item template

```markdown
---
id: LO-NNNN
title: <title>
status: open | in-progress | done
signal: <signal>
source: <source>
priority: P0-P3
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# LO-NNNN — <title>

## Observation
What happened / what is missing?

## Impact
What was the consequence (rework, uncertainty, quality risk)?

## Proposal
How should process / skill / tooling be improved?

## Status
- [ ] Discussed in the meta-retro
- [ ] Implemented (CHANGELOG.md entry, version updated)
```

---

## Status file

Every project has a `status.json`:

```json
{
  "name": "nudge",
  "phase": "5",
  "gate": "4",
  "gate_status": "passed",
  "created": "2026-08-19",
  "last_update": "2026-08-19",
  "archetype": "saas-application",
  "current_sprint": "SPRINT-01",
  "active_ticket": "TICKET-007",
  "velocity": {
    "SPRINT-01": 3,
    "SPRINT-02": 4
  },
  "gate_history": [
    {
      "gate": 0,
      "status": "green",
      "passed_at": "2026-08-19T10:00:00Z"
    }
  ]
}
```

---

## References

- `.quinsy-studio/process/ticket-workflow.md` — 9-step ticket workflow
- `.quinsy-studio/process/gates.md` — gate definitions
- `.quinsy-studio/process/lifecycle.md` — phase overview
- `./studio sprint <project>` — create a sprint
- `./studio groom <project>` — run grooming
- `./studio board <project>` — show the board
- `./studio move <project> <id> <status>` — move a ticket
- `./studio learn "<title>"` — create a learning item
- `./studio retro <project>` — start a retrospective
