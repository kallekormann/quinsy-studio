# Skill: Architecture Decisions

> ADRs, tech stack selection, build vs buy, monolith vs microservices

## Metadata

```
skill_id: PS-002
name: Architecture Decisions
team: 04-product-strategy-architecture
lead_role: Systems Architect
support_roles: [Backend Architect, Frontend Architect, Platform Architect]
phases: [2, 3]
activation_triggers:
  - Ticket contains "ADR", "architecture", "tech stack", "build vs buy"
  - Phase 2: overall architecture is defined
  - Phase 3: technology decisions
  - Fundamental architecture change
```

---

## Behavior rules

### 1. ADR format

```markdown
# ADR-{NNN}: {Title}

## Status
  proposed | accepted | deprecated | superseded

## Context
  Which problem is being solved?

## Decision
  What was decided?

## Rationale
  Why was it decided this way?

## Alternatives
  What was rejected and why?

## Consequences
  Positive and negative impacts

## Risks
  What could go wrong?
```

### 2. Tech-stack decision

```markdown
Framework:
  - Next.js (React SSR/ISR) → standard for web
  - Laravel (PHP) → for enterprise/PHP legacy
  - Supabase → as database/backend (fast)

Database:
  - PostgreSQL (Supabase) → standard
  - Redis → cache, queues, sessions
  - SQLite → embedded, testing

Deployment:
  - Vercel → standard for Next.js
  - Docker → for complex setups
  - Railway / Fly.io → for backends

Decision criteria:
  1. Team competence
  2. Community & ecosystem
  3. Long-term maintenance
  4. Performance
  5. Costs
```

### 3. Build vs buy

```markdown
Build when:
  - Core competence (differentiation)
  - Full control needed
  - No good alternative exists
  - Cheaper in the long run

Buy when:
  - Non-core competence
  - Time-to-market critical
  - Best practice exists
  - Support & maintenance needed

Examples:
  ✅ Buy: auth (Supabase Auth), payment (Stripe), email (Resend)
  ✅ Build: core features, UI, business logic
```

### 4. Monolith vs microservices

```markdown
Standard: modular monolith
  - One deployment
  - Clear module boundaries
  - Internal APIs (not HTTP)
  - Split into microservices later if needed

Microservices when:
  - Different teams
  - Different scaling needs
  - Different tech stacks needed
  - >50 developers
```

---

## Anti-patterns

### ❌ Forbidden

```markdown
- No ADR for fundamental decisions
- Tech choice based on "hype"
- Microservices without clear boundaries
- Build when buy exists (NIH syndrome)
- No ADR for rejected alternatives
```

### ✅ Instead

```markdown
- ADR for every fundamental decision
- Tech choice based on criteria
- Modular monolith as standard
- Build only when it is a core competence
- Complete ADRs with alternatives
```

---

## References

- `.quinsy-studio/process/adr-policy.md` — ADR rulebook
- `.quinsy-studio/process/project-archetypes.md` — stack recommendations
- `projects/[name]/docs/adr/` — ADR storage
