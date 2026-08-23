# Skill: Aesthetic Presets (UX-005 adjunct)

```
skill_id: UX-005-PRESETS
team: 10-product-design-experience
lead_role: UI/Visual Designer
pairs_with: [UX-005, UX-006, UX-007]
```

Select and apply a studio aesthetic preset for visual direction. **Not a separate ticket skill ID** — loaded alongside UX-005 on design-track tickets.

## Load path

```
.quinsy-studio/knowledge-base/aesthetic-presets/<slug>/SKILL.md
```

Full catalog: [knowledge-base/aesthetic-presets/README.md](../../../knowledge-base/aesthetic-presets/README.md)

## Selection rules

1. **One primary preset** per design spec (optional secondary for marketing hero only).
2. If project `design/DESIGN.md` names a direction → preset must align or spec explains deviation.
3. Preset defines **layout, elevation, motion, Headless UI state styling** — not business logic.
4. Map preset colors to **project tokens** in the spec; run `design_math.py` contrast checks.
5. `project-brand-only` — valid when gate-2 tokens already define full visual language.

## Quick picker

| User says | Start with |
|-----------|------------|
| FinTech, billing, premium B2B | `stripe-like-ui` |
| Apple, macOS, glass | `apple-like-ui` |
| Linear, dev tool, dark | `linear-like-ui` |
| Notion, wiki, calm | `notion-like-ui` |
| Adobe, canvas, pro tool | `adobe-like-ui` |
| Playful, consumer | `soft-ui` |
| Minimal, Swiss | `minimalist-ui` |
| Bold, raw | `brutalist-ui` |
| Blueprint, terminal | `technical-blueprint-ui` |
| Editorial, research | `academic-editorial-ui` |

## Deliverable

Design spec section **Aesthetic preset** (see `design-spec-template.md`).
