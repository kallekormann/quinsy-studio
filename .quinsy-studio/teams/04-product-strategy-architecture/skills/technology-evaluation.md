# Skill: Technology Evaluation

> Framework/library evaluation, PoC creation, migration planning

## Metadata

```
skill_id: PS-003
name: Technology Evaluation
team: 04-product-strategy-architecture
lead_role: Systems Architect
support_roles: [Backend Architect, Frontend Architect]
phases: [1, 2]
activation_triggers:
  - Ticket contains "evaluation", "framework", "library", "migration"
  - Phase 1: technologies are assessed
  - Phase 2: tech stack is finalized
  - A new dependency should be introduced
```

---

## Behavior rules

### 1. Evaluation process

```markdown
Step 1: define requirements
  - Functional requirements
  - Non-functional (performance, scalability)
  - Team competence
  - Budget

Step 2: identify options
  - 3-5 realistic options
  - No exotic choices (only if compelling)

Step 3: weight criteria
  - Performance (25%)
  - Community & support (20%)
  - Learning curve (20%)
  - Long-term maintenance (20%)
  - Costs (15%)

Step 4: PoC (for critical decisions)
  - Max. 2 days
  - Realistic scenario
  - Benchmark against criteria

Step 5: recommendation with an ADR
```

### 2. PoC rules

```markdown
PoC goal:
  - Prove technical feasibility
  - Measure performance
  - Estimate the learning curve
  - Understand the integration effort

PoC scope:
  - Max. 2 days
  - Max. 500 lines of code
  - Realistic scenario (no to-do app)

Documentation:
  - ADR with recommendation
  - Benchmark results
  - Experience (positive/negative)
```

### 3. Migration

```markdown
When to migrate:
  - Technology is EOL (end of life)
  - Drastically better alternative
  - Security vulnerabilities
  - Performance problems

Migration strategy:
  1. Strangler fig pattern (incremental)
  2. Feature flag for the new implementation
  3. Parallel operation
  4. A/B test
  5. Full switch
  6. Remove the old technology
```

---

## Anti-patterns

### ❌ Forbidden

```markdown
- "Because it's cool" as justification
- No PoC for critical decisions
- Big bang migration
- No rollback plan
- Evaluation without criteria
```

### ✅ Instead

```markdown
- Structured evaluation with weighting
- PoC for everything with >3 months impact
- Incremental migration (strangler fig)
- Rollback plan for every migration
- ADR for every decision
```

---

## References

- `.quinsy-studio/process/adr-policy.md` — ADR rulebook
- `.quinsy-studio/process/project-archetypes.md` — stack recommendations
