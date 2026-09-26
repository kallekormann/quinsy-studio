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

1. **Optional.** Uniqueness in `design/DESIGN.md` beats a catalog clone. A spec may omit this section.
2. If used: **one primary preset** (optional secondary for marketing hero only), mapped to **project tokens**.
3. If project `design/DESIGN.md` names a direction → preset must align or spec explains deviation.
4. Preset defines **layout, elevation, motion, Headless UI state styling** — not business logic.
5. `project-brand-only` — valid when gate-2b tokens already define full visual language.

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

## Theme-factory ritual (HITL — not a CSS kit)

Catalog `theme-factory` is a **picker**: show repertoire → wait for human pick → apply **one** cohesive color+type pair.

- Product UI: map the pick onto **one aesthetic preset** or `project-brand-only`, then **tokens**. Do not paste pack names (“Ocean Depths”) into `app/` CSS.
- Artifacts (slides/PDF, UX-007): packs are allowed; still check WCAG on hex (`design_math.py`).
- Never auto-generate and apply a palette without `approve-design` / brand HITL (UX-006).

