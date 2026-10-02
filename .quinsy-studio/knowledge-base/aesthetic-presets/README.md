# Aesthetic presets (Team 10 repertoire)

Studio-owned visual direction skills for **UX-005** (Visual UI Design) and **UX-006** (Brand Guardian).  
Load one preset per product as the **craft substrate** (type, elevation, motion, density). It is not the product identity. `design/DESIGN.md` must name the slug and a product delta. Combine with project tokens; never override a signed brand.

Path: `.quinsy-studio/knowledge-base/aesthetic-presets/<slug>/SKILL.md`

## When to use

| Situation | Preset category |
|-----------|-----------------|
| Gate 2a / 2b | Required substrate after the human interview. Uniqueness section states the delta. |
| UI design spec (`ticket_type: ui-*`) | **Optional** section: Aesthetic preset |
| Marketing / landing (UX-007) | Preset + narrative storyboard (still optional vs project DNA) |
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

- **Preset:** `academic-editorial-ui` (one slug from the catalog — craft substrate, not the identity)
- **Delta:** audience job, density, posture, and what this product is not
- **Token overrides:** None | list project token mappings
- **Headless UI notes:** focus rings and active states from the preset SKILL.md. Motion timing stays on `--motion-*` unless the signed direction names a delta.
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

