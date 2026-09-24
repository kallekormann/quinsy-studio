# Aesthetic presets (Team 10 repertoire)

Studio-owned visual direction skills for **UX-005** (Visual UI Design) and **UX-006** (Brand Guardian).  
Load one preset per surface in the design spec — combine with project tokens, never override brand without human approval.

Path: `.quinsy-studio/knowledge-base/aesthetic-presets/<slug>/SKILL.md`

## When to use

| Situation | Preset category |
|-----------|-----------------|
| Gate 2 / sticker sheet direction | Pick 1–2 candidates; human approves at gate 2 |
| UI design spec (`ticket_type: ui-*`) | **Required** section: Aesthetic preset |
| Marketing / landing (UX-007) | Preset + narrative storyboard |
| Project already has brand tokens | Preset adapts *layout, motion, elevation* — tokens stay in `ui/tokens/` |

## Catalog

### Foundation (from Design Agent)

| Slug | Vibe | Best for |
|------|------|----------|
| [soft-ui](soft-ui/SKILL.md) | Warm consumer premium, glass, bounce | Onboarding, consumer SaaS |
| [minimalist-ui](minimalist-ui/SKILL.md) | Restrained, whitespace, monochrome | Productivity, docs |
| [brutalist-ui](brutalist-ui/SKILL.md) | Raw, high-contrast, editorial | Campaigns, bold marketing |

### Industry references

| Slug | Vibe | Best for |
|------|------|----------|
| [apple-like-ui](apple-like-ui/SKILL.md) | Cupertino glass, system hierarchy | Desktop/web premium tools |
| [stripe-like-ui](stripe-like-ui/SKILL.md) | FinTech precision, gradients | Billing, dashboards, B2B |
| [linear-like-ui](linear-like-ui/SKILL.md) | Dark productivity, keyboard-first | Dev tools, issue trackers |
| [notion-like-ui](notion-like-ui/SKILL.md) | Calm workspace, blocks | Wikis, knowledge apps |
| [adobe-like-ui](adobe-like-ui/SKILL.md) | Pro creative chrome, dense panels | Canvas, media editors |
| [paypal-like-ui](paypal-like-ui/SKILL.md) | Trust, commerce clarity | Payments, checkout |
| [amazon-like-ui](amazon-like-ui/SKILL.md) | Commerce density, scanability | Catalog, retail |
| [nike-like-ui](nike-like-ui/SKILL.md) | Bold athletic, hero imagery | Lifestyle, campaigns |
| [space-x-like-ui](space-x-like-ui/SKILL.md) | Industrial sci-fi, mission control | Data-heavy, status UIs |

### Atmosphere / specialty

| Slug | Vibe | Best for |
|------|------|----------|
| [nordic-design-ui](nordic-design-ui/SKILL.md) | Light, calm, Scandinavian | Wellness, calm productivity |
| [cosmic-void-ui](cosmic-void-ui/SKILL.md) | Deep space, luminous accents | Immersive, creative |
| [technical-blueprint-ui](technical-blueprint-ui/SKILL.md) | CAD / terminal blueprint | Dev portals, technical docs |
| [technical-ui](technical-ui/SKILL.md) | Engineering UI, monospace accents | APIs, admin, status |
| [academic-editorial-ui](academic-editorial-ui/SKILL.md) | Scholarly, serif + structure | Long-form, research |

## Design spec requirement

In every Team 10 design spec, add:

```markdown
## Aesthetic preset

- **Preset:** `stripe-like-ui` (or `project-brand-only`)
- **Rationale:** Why this preset fits the job + audience
- **Token overrides:** None | list project token mappings
- **Headless UI notes:** transitions, focus rings, active states from preset SKILL.md
```

## Agents & skills

| Load | When |
|------|------|
| UX-005 + preset SKILL.md | Visual layout, type, color application |
| UX-006 | Preset must not break project brand voice/tokens |
| UX-007 | Marketing surfaces — preset + storyboard |
| `taste-skill` (external) | Anti-slop quality bar |

See [teams/10-product-design-experience/skills/aesthetic-presets.md](../../teams/10-product-design-experience/skills/aesthetic-presets.md).

**Theme-factory:** HITL pick only. Product CSS stays presets + tokens (LO-0332).

