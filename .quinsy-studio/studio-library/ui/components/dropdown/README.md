# Dropdown

Single-value **Listbox** dropdown for product surfaces. **Not** native OS `<select>` chrome.

Paint comes from **kit CSS variables** (any brand kit, not product class names):

| Role | Variable (fallback) |
|------|---------------------|
| Border | `--color-border` |
| Surface | `--color-background` → `--color-surface` |
| Text | `--color-foreground` → `--color-text` |
| Muted | `--color-muted` → `--color-text-muted` |
| Accent / selected | `--color-accent` → `--color-primary-500` |
| Type | `--font-ui` → `--font-sans` |

## Pull

```bash
./studio library pull <project> dropdown listbox
```

## Usage

```tsx
<Dropdown
  label="Sortierung"
  value={sort}
  onChange={setSort}
  options={[
    { value: 'opened', label: 'Meist geöffnet' },
    { value: 'newest', label: 'Neu hinzugefügt' },
  ]}
/>
```

## A11y

- Headless UI Listbox: arrows, Esc, focus management
- Provide `label` (wired to `aria-labelledby`) or `aria-label`
