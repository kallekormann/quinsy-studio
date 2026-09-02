# Tooltip

Position-aware label tip / compact popover for icon buttons and dense chrome (MOOD-0425).

## When to use

| Need | Use |
|------|-----|
| Icon-only control needs a name (Library, Inbox, Search) | `variant="tooltip"` + `label` |
| Short help with a bit more copy | `variant="popover"` + `content` |
| Click menus / action lists | `DropdownMenu` — not this |

## Placement

`placement`: `top` | `right` | `bottom` | `left` (preferred). Always flips, then shifts into the viewport.

## Example

```tsx
import { Tooltip } from '@ui/components/tooltip';

<Tooltip label="Library" placement="bottom">
  <button type="button" aria-label="Library">…</button>
</Tooltip>
```

## A11y

Keep `aria-label` on the control. Tip sets `role="tooltip"` + `aria-describedby` while open.
