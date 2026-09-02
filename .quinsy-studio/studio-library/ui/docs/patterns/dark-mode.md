# Dark mode

1. Pull tokens: `./studio library pull <project> tokens`
2. Map `--color-surface` / `--color-surface-dark` in project `design-tokens.css`
3. Use `dark:` Tailwind variants on all chrome (see existing atoms for patterns)

## Shared panel / dialog surface

Light mode: cards and dialogs use **white** (`bg-white` / `bg-surface`).

Dark mode: **one** elevated surface for dialogs, share shells, and floating inspectors — `dark:bg-surface-dark` (same token as ItemInspector / Card). Do **not** mix `dark:bg-neutral-900` on DialogShell while panels use `surface-dark`.

Hand-rolled modals (e.g. Share) must match DialogShell: `bg-white` + `dark:bg-surface-dark`.

## Selected controls (radio / checkbox)

Selected fill must use a **defined brand token** in the project (`primary-*` or `accent-*`). Never ship `primary-*` classes if the project only maps `accent-*` — the control looks empty and teams invent border-only selection chrome.

Acceptance: UI tickets must verify light **and** dark when surface appears in app chrome or canvas.

Reference: [Tailwind dark mode](https://tailwindcss.com/docs/dark-mode).
