# Extension: Figma token handoff (UX-002 / UX-005)

> Not a ticket skill ID. Load when a ticket cites a Figma file. Distilled from catalog `figma-implement-design` — **handoff only**.

## Do

- Map Figma color/type/spacing to **project `ui/tokens`** before implement.
- Record the file URL and node ids in the design spec §2c; mocks stay HTML in-product.
- If tokens disagree with gate-2: HITL (`approve-design`), do not invent a second palette.

## Don’t

- Treat Figma as the runtime kit (studio-library + Radix / Headless win).
- Screenshot-only “implementation” without token names.
- Auto-apply a Figma theme pack as product CSS (see theme-factory ritual in `aesthetic-presets.md`).

## Spec-fail

- Figma link with no token mapping table.
- Implement ticket that copies Figma hex into `app/` instead of tokens (`studio_skill_checks` warn).
