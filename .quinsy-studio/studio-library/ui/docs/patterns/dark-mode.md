# Dark mode

1. Pull tokens: `./studio library pull <project> tokens`
2. Map `--color-surface` / `--color-surface-dark` in project `design-tokens.css`
3. Use `dark:` Tailwind variants on all chrome (see existing atoms for patterns)

Acceptance: UI tickets must verify light **and** dark when surface appears in app chrome or canvas.

Reference: [Tailwind dark mode](https://tailwindcss.com/docs/dark-mode).
