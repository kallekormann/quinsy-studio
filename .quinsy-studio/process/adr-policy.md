# Quinsy Studio — ADR Rulebook

> Every architectural decision is documented as an Architecture Decision Record (ADR).
> ADRs are the project's memory — they explain the "why" behind the "what".

## Core principle

```
No decision without documentation.
No documentation without rationale.
No rationale without an alternative.
```

---

## When is an ADR created?

| Situation | ADR required? |
|-----------|---------------|
| Technology change (e.g. framework, DB) | **Yes** |
| Architecture pattern (e.g. monolith → microservices) | **Yes** |
| API design decision | **Yes** |
| UI/UX fundamental decision | **Yes** |
| Security architecture | **Yes** |
| Deployment strategy | **Yes** |
| Code convention (new rule) | Recommended |
| Bugfix with architectural impact | Recommended |
| Small bugfix without impact | No |

---

## ADR template

Every ADR follows this template:

```markdown
# ADR-XXXX: [Title of the decision]

**Status:** proposed | accepted | deprecated | superseded
**Date:** YYYY-MM-DD
**Decision-maker:** [Role / Name]
**Affected phases:** [Phase(s)]

## Context
What is the situation? Which problem needs to be solved?

## Decision
What was decided?

## Rationale
Why was this decision made?

## Alternatives
Which alternatives were considered?

### Alternative A: [Name]
- Pros: ...
- Cons: ...

### Alternative B: [Name]
- Pros: ...
- Cons: ...

## Consequences
What does this decision mean for the project?

### Positive
- ...

### Negative
- ...

### Risks
- ...

## Metrics
How is the success of this decision measured?

## Follow-up
Which next steps arise from this?
```

---

## ADR numbering

```
ADR-0001, ADR-0002, ADR-0003, ...
```

- sequential
- never recycled
- superseded ADRs keep their number

---

## ADR status

| Status | Meaning |
|--------|---------|
| `proposed` | suggested, not yet decided |
| `accepted` | accepted, binding |
| `deprecated` | no longer valid (replaced by a new ADR) |
| `superseded` | replaced by ADR-XXXX |

---

## Storage location

```
<project>/docs/adr/
├── README.md              # overview of all ADRs
├── ADR-0001-...
├── ADR-0002-...
└── ...
```

### ADR README.md

```markdown
# Architecture Decision Records

| ADR | Title | Status | Date |
|-----|-------|--------|------|
| ADR-0001 | [Title] | accepted | YYYY-MM-DD |
| ADR-0002 | [Title] | proposed | YYYY-MM-DD |

## Legend
- **accepted:** binding decision
- **proposed:** still in discussion
- **deprecated:** no longer valid
- **superseded:** replaced by a newer ADR
```

---

## ADR workflow

```bash
# Create a new ADR
./studio adr <project> "<title>"

# The ADR file is created with:
# - template
# - next free number
# - status: proposed

# Edit an ADR
# 1. fill out the file manually
# 2. set status to "accepted"
# 3. commit with ADR reference
```

---

## ADR review

Every ADR is reviewed at least once:

1. **Creation:** the Project Manager creates the ADR
2. **Review:** affected roles review it
3. **Decision:** human or Project Manager (depending on weight)
4. **Archiving:** the ADR is committed

---

## ADR obligations per phase

| Phase | ADR obligation |
|-------|----------------|
| Phase 0 | archetype, complexity level |
| Phase 1 | go/no-go, technology stack |
| Phase 2 | all architecture decisions |
| Phase 3 | design system principle |
| Phase 4 | on deviation from phase-2 ADRs |
| Phase 5 | — |
| Phase 6 | deployment strategy |
| Phase 7 | optimization decisions |

---

## Anti-patterns

### ❌ No ADR for an architect decision
```bash
# Bad:
"We now use PostgreSQL instead of MySQL"
# (no documentation why)

# Good:
# ADR-0003: Switch to PostgreSQL
# Status: accepted
# Rationale: JSONb support, better full-text search, ...
```

### ❌ ADR without alternatives
```markdown
# Bad:
## Decision: We use Next.js
## Rationale: Because it is good

# Good:
## Alternatives
### A: Next.js + Payload - Pros: SSR, one server for content and auth, Coolify deploy
### B: Remix - Pros: web standards, simple loader model
### C: Astro - Pros: island architecture, performance
## Decision: Next.js (because of SSR + large-scale features)
```

### ❌ Outdated ADR not marked
```markdown
# Bad:
ADR-0001: "We use jQuery" (never updated)

# Good:
ADR-0001: "We use jQuery"
Status: superseded (by ADR-0015: React migration)
```

---

## References

- `docs/adr/README.md` — ADR overview in the project
- `.quinsy-studio/process/lifecycle.md` — phases in which ADRs arise
- `./studio adr <project> "<title>"` — create an ADR
