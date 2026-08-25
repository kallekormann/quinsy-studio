# Skill: Product Strategy

> Vision, roadmap, competitive analysis, monetization, go-to-market

## Metadata

```
skill_id: PS-001
name: Product Strategy
team: 04-product-strategy-architecture
lead_role: Product Strategist
support_roles: [Product Manager, Growth Manager]
phases: [0, 1, 2, 7]
activation_triggers:
  - Ticket contains "strategy", "vision", "roadmap", "monetization"
  - Phase 0: new project is evaluated
  - Phase 1: validation and strategy
  - Phase 7: next iteration is planned
```

---

## Behavior rules

### 1. Vision & mission

```markdown
For every project:
  - Vision: which future do we create?
  - Mission: how do we get there?
  - North Star metric: what IS the metric?
  - USPs: what makes us unique?
```

### 2. Competitive analysis

```markdown
Structure:
  - Direct competitors (same solution)
  - Indirect competitors (same solution for a different problem)
  - Substitutes (alternative solution approaches)

Per competitor:
  - Features (what do they offer?)
  - Price (how do they monetize?)
  - Target audience (whom do they serve?)
  - USP (what is their differentiator?)
  - Weaknesses (where can we win?)
```

### 3. Monetization

```markdown
Models:
  - Freemium: base free, premium paid
  - Subscription: monthly/yearly
  - Transaction-based: per use
  - Licensing: enterprise licenses
  - Hybrid: combination

Pricing:
  - Value-based pricing (not cost-plus)
  - Competitive comparison
  - Test price elasticity
  - Tier structure (3 levels)
```

### 4. Go-to-market

```markdown
Phases:
  1. Pre-launch: waitlist, beta, feedback
  2. Launch: PR, social, outreach
  3. Post-launch: growth, retention, optimization

Channels:
  - Organic: SEO, content, social
  - Paid: ads, influencers
  - Partnership: integrations, affiliates
  - Community: Discord, forum
```

### 5. Roadmap

```markdown
Format: now / next / later

Now (0-3 months):
  - Critical features
  - Quick wins
  - Must-haves for launch

Next (3-6 months):
  - Growth features
  - Monetization
  - Optimization

Later (6-12 months):
  - Enterprise features
  - Internationalization
  - Advanced analytics
```

---

## Anti-patterns

### ❌ Forbidden

```markdown
- No differentiator vs. the competition
- Feature parity as a goal (instead of differentiation)
- No North Star metric
- Roadmap without prioritization
- Price based only on cost
```

### ✅ Instead

```markdown
- Define clear USPs
- Differentiation through focus
- Define and track the North Star metric
- Prioritized roadmap with now/next/later
- Value-based pricing with tiering
```

---

## References

- `.quinsy-studio/process/project-archetypes.md` — archetypes
- `.quinsy-studio/teams/05-growth-marketing-content/` — growth team

---

## Studio skill extension (PLG)

**Load when strategy touches self-serve distribution, activation, or usage monetization:**  
[knowledge-base/skill-extensions/product-led-growth.md](../../../knowledge-base/skill-extensions/product-led-growth.md)

**Adds to PS-001:**
- Inherent loop (watermarked exports / shared surfaces)
- Collaborative loop (invite-before-pay seat expansion)
- Monetization loop (contextual usage thresholds, not hard errors)
- Time-to-value: defer profiling until after aha-moment
