# Studio Library — Sticker Sheet Catalog

Updated: 2026-08-23  
**UI reference:** [ui/docs/README.md](../docs/README.md)

## Primitives (Headless UI — full v2 coverage)

Peer dependency: `@headlessui/react`

**Overlays & navigation:** `dialog`, `menu`, `popover`, `disclosure`, `tabs`  
**Selection:** `listbox`, `combobox`, `radio-group`, `select`  
**Forms:** `field`, `checkbox`, `switch`, `input`, `textarea`, `button`  
**Motion:** `transition`, `close-button`

> Pull styled atoms (`button`, `input`, …) for token-styled controls. Primitives live at `ui/primitives/headless/<name>/`.

## Atoms

- `badge`
- `button` — primary, secondary, outline, ghost, **link**, destructive
- `card`
- `checkbox`
- `icon`
- `input`
- `select`
- `switch`
- `textarea`

## Molecules

- **SegmentedToggle** — `ui/components/segmented-toggle/` (labeled A|B exclusive; not Switch)
- **Tooltip** — `ui/components/tooltip/` (position-aware label / compact popover for icon buttons)

- `checklist-item`
- `dropdown-menu`
- `inline-form`
- `palette-strip`
- `radio-group`
- `search-command` (Dialog + Combobox)
- `item-inspector`
- `auth-login`

## Organisms

- `pageshell`

## Packages

- `color-extraction` — dominant-color palette from images
- `qa-smoke` — Playwright smoke-routes runner
- `item-tags` — tag parse/normalize
- `item-search` — metadata search (CMD-K)
- `canvas-export` — Konva PNG/PDF export
