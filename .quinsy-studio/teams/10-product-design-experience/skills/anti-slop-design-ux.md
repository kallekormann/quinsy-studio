# Skill: Anti-Slop Design & UX (UX-006 extension)

> Mandatory before Team 10 drafts specs, mocks, or microcopy. Blocks AI-slop in product UI.

## Metadata

```
skill_id: UX-008
name: Anti-Slop Design & UX
team: 10-product-design-experience
lead_role: Brand Guardian / UI Designer
phases: [2, 4]
activation_triggers:
  - Any design-track ticket (ui-new-component, ui-composition, marketing-page)
  - Brand kit, sticker sheet, Figma kit, HTML catalog (MOOD-0472 class)
  - ./studio approve-design pre-check
  - User feedback mentioning "AI slop", generic UI, fluff copy
```

## Canonical reference

Read and apply: [anti-slop-design-ux.md](../../../knowledge-base/anti-slop-design-ux.md)

## Behavior rules

1. **Layout** — 8pt grid; no decorative blobs; elevation only for hierarchy.
2. **Color** — semantic roles from brand DNA; no default SaaS-blue template.
3. **Type** — ≤2 families; operational screens ≠ marketing hero scale.
4. **Copy** — banned vocabulary list; literal CTAs; expert-peer tone.
5. **Icons** — SVG only (LO-0037); never emoji as chrome.
6. **Mocks** — in-context shell (§2c); domain-realistic data — no `Feature 1`, Lorem, `Primary action`.
7. **Output** — structured spec sections only; no conversational preamble.

## Gate

`./studio approve-design` expects §6 attestation against this skill + `design-system-compliance-checklist.md`.

Automated warnings: `./studio gate <project> --anti-slop` (copy + placeholder patterns in mocks and UI files).
