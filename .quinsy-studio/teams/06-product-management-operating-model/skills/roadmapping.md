# Skill: Roadmapping

> Now/next/later, RICE/MoSCoW, dependencies, stakeholder alignment

## Metadata

```
skill_id: PM-002
name: Roadmapping
team: 06-product-management-operating-model
lead_role: Product Manager
support_roles: [Product Strategist, Systems Architect]
phases: [1, 3, 7]
activation_triggers:
  - Ticket contains "roadmap", "prioritization", "planning"
  - Phase 1: first roadmap is created
  - Phase 3: sprint roadmap
  - Phase 7: next iteration
```

---

## Behavior rules

### 1. Roadmap format

```markdown
Now (0-3 months):
  - Critical features for launch
  - Quick wins (high impact, low effort)
  - Bug fixes that bother users

Next (3-6 months):
  - Growth features
  - Monetization
  - Performance optimization

Later (6-12 months):
  - Enterprise features
  - Internationalization
  - Advanced analytics
```

### 2. Prioritization

```markdown
RICE score:
  Reach × Impact × Confidence / Effort

  Reach:     how many users does it affect? (per quarter)
  Impact:    how strong is the impact? (0.25, 0.5, 1, 2, 3)
  Confidence: how sure are we? (100%, 80%, 50%)
  Effort:    effort in person-months

MoSCoW:
  Must:     without it no MVP
  Should:   important but deferrable
  Could:    nice-to-have
  Won't:    not in this release
```

### 3. Dependencies

```markdown
For every epic/feature:
  - Upstream dependencies (what must come first?)
  - Downstream dependencies (what does the feature need?)
  - Cross-team dependencies
  - External dependencies (APIs, services)

Visualization:
  - Dependency map
  - Identify the critical path
  - Detect blockers early
```

### 4. Stakeholder alignment

```markdown
Regular update:
  - What was delivered?
  - What is next?
  - What are the risks?
  - Do we need decisions?

Format:
  - Executive summary (1 page)
  - Feature status (table)
  - Risks and blockers
  - Next steps
```

---

## Anti-patterns

### ❌ Forbidden

```markdown
- Everything is "priority 1"
- No dependencies documented
- Roadmap without time windows
- No stakeholder update
- Feature factory (outputs instead of outcomes)
```

### ✅ Instead

```markdown
- Clear prioritization (RICE/MoSCoW)
- Dependencies documented
- Now/next/later with time windows
- Regular stakeholder updates
- Outcome-based roadmap
```

---

## References

- `.quinsy-studio/process/iterative-delivery.md` — sprint/grooming
- `.quinsy-studio/process/lifecycle.md` — phases
