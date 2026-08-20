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
| **Feature** | new features (incremental) | No |
| **Bugfix** | fixing bugs | No |
| **Docs** | documentation | No |

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
