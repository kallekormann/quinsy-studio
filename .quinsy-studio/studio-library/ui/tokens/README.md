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

## Motion

The same CSS file defines the motion scale: `--motion-duration-*`, `--motion-ease-*`, `--motion-scale-*`, plus distance and blur. `prefers-reduced-motion` sets the durations to `0ms`. HITL `motion: off` does that in the project token file.

Overlays set `--tw-enter-scale` and `--tw-exit-scale` from the scale tokens so a centered dialog keeps its translate. Pattern: [../docs/patterns/transitions.md](../docs/patterns/transitions.md). Skill: [../../../knowledge-base/skill-extensions/motion-transitions.md](../../../knowledge-base/skill-extensions/motion-transitions.md).
