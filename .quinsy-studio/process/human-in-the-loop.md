# Quinsy Studio — Human-in-the-Loop

> Some decisions are too important to leave to the agent alone.
> Human-in-the-loop ensures that irreversible actions receive human approval.

## Core principle

```
Agent: "I cannot decide this alone."
Human: "I decide."
Agent: "Implemented."
```

---

## When is HITL needed?

| Category | Actions | HITL? |
|----------|---------|-------|
| **Budget** | costs above X €/month | **Yes** |
| **Legal** | contracts, licenses, GDPR exceptions | **Yes** |
| **Irreversible** | deleting data, production deploy, DNS changes | **Yes** |
| **Security** | security exceptions, access rights | **Yes** |
| **Architecture** | large architecture changes | **Yes** |
| **Release** | production release | **Yes** |
| **Sprint review** | approve shipped sprint work | **Yes** |
| **Sprint feedback** | new ideas from review → backlog | **Yes** (clarify before ticket) |
| **Feature** | new features (incremental, in sprint) | No (if ticket exists) |
| **Bugfix** | fixing bugs | No |
| **Docs** | documentation | No |

---

## Sprint cadence HITL (after gate 2)

Pre-implementation uses gates 0–2 (`./studio approve`). **During sprints**, the agent executes autonomously; the human joins at **sprint review**, then helps plan the **next** sprint.

### Autonomous execution (mid-sprint)

While sprint tickets are not all `done`:

| Do | Don't |
|----|-------|
| Agent implements every groomed sprint ticket in order | Ask the human "should I continue?" between tickets |
| Agent moves tickets `implement` → `done` without pausing | Let the human change direction mid-sprint |
| Human may `./studio feedback` (queued for after review) | Turn feedback into tickets or code before sprint review |
| Agent captures feedback only during review | Agent implements feedback in project code during review |
| `./studio resume` points at the next ticket to implement | Block on a single ticket for human approval |

**Enforced by CLI:** `./studio move … implement` is blocked when sprint review is pending or the sprint is closed.

### Sprint ceremony flow

```
Groom sprint → autonomous implementation → ./studio review (human) → feedback → clarify → ticket → groom → retro → next sprint
```

| Step | Who | Command |
|------|-----|---------|
| **Sprint groom** | **Human** + agent | `./studio groom <p> --approve` before first `implement` |
| **Sprint work** | **Agent only** | `./studio move <p> <ID> implement` … `done` (all sprint tickets) |
| **Status brief** | Agent prepares | `./studio review <p>` → `sprints/SPRINT-NN/review.md` |
| **Sprint review** | **Human** tries shipped work | Read review.md, RUNBOOK, run the app |
| **Approve / reject** | **Human** | `./studio review <p> --approve` or `--reject --reason "..."` |
| **Raw feedback** | **Human** | `./studio feedback <p> "I want X"` — **not a ticket** |
| **Clarify** | Agent + **human** | `./studio clarify <p> FB-001 --title ... --acceptance ... --approve` |
| **Ticket** | Agent (after clarify) | `./studio ticket <p> "..." --from-feedback FB-001` |
| **Grooming** | **Human** + agent | `./studio groom <p>` — reprioritize backlog for next sprint |
| **Retro** | **Human** + agent | `./studio retro <p>` → `sprints/SPRINT-NN/retro.md` |
| **Next sprint** | **Human** + agent | `./studio sprint <p>` → `./studio groom <p> --approve` |

**Rule:** Ideas from sprint review never become tickets directly. Flow is always **feedback → clarify → ticket**.

**Rule:** During sprint review, the agent **never implements** feedback in project code — only `./studio feedback` → clarify → ticket for the **next** sprint.

**Rule:** `./studio sprint` is blocked until the current sprint is done, review is **approved**, and retro is complete.

When all sprint tickets reach `done`, `./studio resume` surfaces **sprint review pending** and blocks further implementation.

### Example

```bash
./studio review nudge
# human tries the app, then:
./studio feedback nudge "Habits should work offline"
./studio clarify nudge FB-001 \
  --title "Offline habit tracking" \
  --scope "Cache today's habits in IndexedDB" \
  --acceptance "Completing a habit works offline" \
  --approve
./studio ticket nudge "Offline habit tracking" --from-feedback FB-001
./studio review nudge --approve --notes "Sprint 1 shipped, offline next"
./studio groom nudge
./studio retro nudge
./studio sprint nudge
./studio groom nudge --approve
```

---

## Decision record template

```markdown
# Decision Record — DR-NNNN

**Status:** pending | approved | rejected
**Date:** YYYY-MM-DD
**Requested by:** <role/agent>
**Decision by:** <human>

## Decision
What needs to be decided?

## Context
Why is this decision necessary?

## Options

### Option A: <name>
- Pros: ...
- Cons: ...
- Costs: ...

### Option B: <name>
- Pros: ...
- Cons: ...
- Costs: ...

## Recommendation
Which option does the agent recommend and why?

## Risks
What can go wrong?

## Consequences
What does the decision mean for the project?
```

---

## HITL workflow

```
┌─────────────────────────────────────────────────────────┐
│               HUMAN-IN-THE-LOOP WORKFLOW                │
└─────────────────────────────────────────────────────────┘

 1. Agent recognizes a HITL situation
       │
 2. Create a decision record
       │
 3. Present the decision record
       │
 4. ┌─────────────────┐
    │  WAIT FOR      │
    │  DECISION      │
    └─────────────────┘
       │
 5. Human decides
       │
 6. Update the decision record
       │
 7. Implement the decision
```

---

## Commands

```bash
# Create a decision record
./studio decide <project> "<title>"

# Overview of all decision records
./studio decisions <project>

# Mark a decision record as approved
./studio decide <project> DR-NNNN --approve

# Mark a decision record as rejected
./studio decide <project> DR-NNNN --reject
```

---

## Decision record directory

```
<project>/docs/decisions/
├── README.md              # overview of all DRs
├── DR-0001-...
├── DR-0002-...
```

### README.md

```markdown
# Decision Records

| DR | Title | Status | Date | Decision-maker |
|----|-------|--------|------|----------------|
| DR-0001 | ... | approved | YYYY-MM-DD | ... |
| DR-0002 | ... | pending | YYYY-MM-DD | — |

## Legend
- **pending:** waiting for a decision
- **approved:** approved
- **rejected:** rejected
```

---

## HITL examples

### Example 1: Deployment costs

```markdown
# Decision Record — DR-0001

**Status:** pending
**Date:** 2026-08-20
**Requested by:** Platform Engineering

## Decision
Should the project use a managed Kubernetes cluster (€150/month) or a simpler docker host (€30/month)?

## Context
The project expects 10k users in the first year. Performance requirements are moderate.

## Options

### Option A: Managed Kubernetes
- Pros: auto-scaling, high availability
- Cons: complexity, costs
- Costs: €150/month

### Option B: Docker host
- Pros: simple, cheap
- Cons: manual scale-up
- Costs: €30/month

## Recommendation
Option B (docker host) — sufficient for the expected load, saves €1440/year.

## Risks
- On sudden traffic spikes: possible downtime
- Manual scaling required
```

---

### Example 2: License decision

```markdown
# Decision Record — DR-0002

**Status:** pending
**Date:** 2026-08-20
**Requested by:** Product Management

## Decision
Should a commercial UI license (€500/year) be purchased or should an open-source alternative be used?

## Context
The project needs an advanced data-grid component.

## Options

### Option A: Commercial license
- Pros: support, features
- Cons: costs, vendor lock-in
- Costs: €500/year

### Option B: Open source
- Pros: free, flexibility
- Cons: fewer features, no support
- Costs: €0

## Recommendation
Option B — the needed features are available in the open-source version.

## Risks
- If advanced features are needed: manual implementation required
```

---

## Automated HITL detection

The agent automatically recognizes HITL situations:

```yaml
# In the agent configuration
hitl_triggers:
  - pattern: "costs.*€[0-9]+"
    category: budget
  - pattern: "delete.*data"
    category: irreversible
  - pattern: "production.*deploy"
    category: release
  - pattern: "contract.*signature"
    category: legal
  - pattern: "gdpr.*exception"
    category: compliance
```

---

## HITL report

```markdown
# HITL Report — Monthly

## Decisions this month

| DR | Title | Status | Decision-maker | Date |
|----|-------|--------|----------------|------|
| DR-0001 | ... | approved | Max | 2026-08-15 |
| DR-0002 | ... | rejected | Max | 2026-08-18 |

## Pending decisions

| DR | Title | Requested by | Waiting since |
|----|-------|--------------|---------------|
| DR-0003 | ... | Agent | 2026-08-20 |

## Statistics
- Approved: 5
- Rejected: 1
- Pending: 1
- Average decision time: 2 days
```

---

## References

- `.quinsy-studio/process/lifecycle.md` — phases
- `.quinsy-studio/process/gates.md` — gates
- `./studio decide <project> "<title>"` — create a decision record
- `./studio decisions <project>` — show the overview
