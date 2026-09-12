# Studio Library — Design Tokens

**Scope:** Generic Tailwind-default scale. **Studio-owned** — not updated from project gate 2.

| File | Purpose |
|------|---------|
| `design-tokens.json` | Canonical token schema (primary/neutral/semantic) |
| `design-tokens.css` | CSS custom properties + light/dark surfaces |
| `tailwind.preset.ts` | Tailwind `theme.extend` → `var(--…)` |

## Project usage

1. **Pull** boilerplate: `./studio library pull <project> tokens button input`
2. **Keep project brand** in `projects/<name>/ui/tokens/design-tokens.json` + `.css` — local overrides only
3. **Never** promote project tokens back to this folder

Styled kit components also use shadcn names (`bg-primary`, `text-muted-foreground`, `border-input`). Those map through `--primary`, `--background`, `--muted-foreground`, etc., aliased from the studio scale in `design-tokens.css`. Remap either the scale or the aliases — not hardcoded hex.
