# Component creation playbook

> New UI in projects starts in **studio-library**, not as one-offs in `projects/<name>/`.

## When this applies

- Design spec marks an atomic inventory row as **New? yes**
- `./studio library suggest` finds no matching primitive or styled component
- Ticket type: `ui-new-component` or `ui-composition` with new molecule

## Flow

1. **Team 10** completes design spec with Atomic Inventory (`knowledge-base/design-spec-template.md`)
2. Human: `./studio approve-design <project> <ticket-id>`
3. **Studio library first** — add primitive or styled component under `.quinsy-studio/studio-library/`
4. Register in `manifest.json` + `ui/sticker-sheet/catalog.md` (grouped by atomic level)
5. **Team 01** pulls: `./studio library pull <project> <name>`
6. Adapt project tokens in `ui/tokens/` — never merge project brand into studio-library

## Layer rules

| Level | Path | Notes |
|-------|------|-------|
| Primitive | `ui/primitives/headless/<slug>/` | Thin `@headlessui/react` re-export; unstyled |
| Atom | `ui/components/<slug>/` kind `ui-atom` | Single-purpose, token-styled |
| Molecule | `ui/components/<slug>/` kind `ui-molecule` | Composes atoms |
| Organism | `ui/components/<slug>/` kind `ui-organism` | App chrome sections |

## Checklist before promote

- [ ] README with pull instructions + a11y notes
- [ ] `index.ts` barrel export
- [ ] Sticker-sheet entry at correct atomic level
- [ ] No project-specific copy or brand colors hardcoded
- [ ] FE-004 contrast check on token pairs used

## Related

- `atomic-design-playbook.md`
- `headless-ui-playbook.md`
- `brand-guardian-checklist.md`
