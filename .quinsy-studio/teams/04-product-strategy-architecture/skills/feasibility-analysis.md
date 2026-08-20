# Skill: Feasibility Analysis

> Feasibility check, risk analysis, capacity planning, scope definition

## Metadata

```
skill_id: PS-004
name: Feasibility Analysis
team: 04-product-strategy-architecture
lead_role: Systems Architect
support_roles: [Product Manager, Backend Architect]
phases: [0, 1]
activation_triggers:
  - Ticket contains "feasibility", "risk", "scope"
  - Phase 0: new project is evaluated
  - Phase 1: scope is defined
  - Complex feature request
```

---

## Behavior rules

### 1. Feasibility check

```markdown
Dimensions:
  - Technical: is it feasible?
  - Economic: is the effort worth it?
  - Temporal: is the schedule realistic?
  - Resources: do we have the skills?
  - Legal: is it legally allowed?

For every dimension:
  - Status: ✅ feasible / ⚠️ risky / ❌ not feasible
  - Rationale
  - Risks
  - Recommendation
```

### 2. Risk analysis

```markdown
Per risk:
  - Description
  - Probability of occurrence (1-5)
  - Impact (1-5)
  - Risk score (P × I)
  - Countermeasure
  - Responsible person

Risk matrix:
  5×5 = 25 (critical)
  4×4 = 16 (high)
  3×3 = 9 (medium)
  2×2 = 4 (low)
  1×1 = 1 (minimal)
```

### 3. Scope definition

```markdown
MoSCoW prioritization:
  Must:     without these features no MVP
  Should:   important but deferrable
  Could:    nice-to-have
  Won't:    not in this release

Scope checks:
  - Does it fit the time budget?
  - Are the dependencies clarified?
  - Are there quick wins?
  - What can be omitted without losing value?
```

### 4. Capacity planning

```markdown
For every phase:
  - Required roles
  - Estimated hours
  - Dependencies
  - Risk buffer (20-30%)

Team availability:
  - Who is available when?
  - Are there dependencies on other projects?
  - Vacation / holidays
```

---

## Anti-patterns

### ❌ Forbidden

```markdown
- "We'll manage" without analysis
- No risk plan
- Unrealistic schedules
- Scope creep without prioritization
- No rollback plan
```

### ✅ Instead

```markdown
- Structured feasibility check
- Risk matrix with countermeasures
- Realistic schedules with buffer
- MoSCoW prioritization
- Rollback plan for every phase
```

---

## References

- `.quinsy-studio/process/lifecycle.md` — phases
- `.quinsy-studio/process/project-archetypes.md` — archetypes
