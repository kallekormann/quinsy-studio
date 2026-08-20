# Studio Library — Sticker Sheet

> **Combined token sheet + component inventory** (functional, neutral Tailwind).
> Updated when projects pass **human gate 2** (`./studio promote-library <project>`).

## Purpose

- Single catalog of all base UI primitives promoted from projects
- **Unstyled semantics, studio-default Tailwind** — projects override via `ui/tokens/`
- Grows as more projects complete design approval

## Files

| File | Role |
|------|------|
| `page.tsx` | Latest sticker-sheet page (from most recent promotion) |
| `catalog.md` | Index of all components in `ui/components/` |

## Promotion rules

1. Triggered on `./studio approve <project> --gate 2`
2. Manual re-sync: `./studio promote-library <project>`
3. Merges `design-tokens.json` (deep merge, newer keys win per section)
4. Copies `ui/components/atoms|molecules|organisms/*.tsx` → `ui/components/<slug>/`
5. Does **not** copy project branding — base Tailwind only

## Use in a new project

```bash
./studio sync <project>   # copies library assets into project ui/
```

Or copy individual components from `.quinsy-studio/studio-library/ui/components/`.
