# Headless UI playbook

Studio-library primitives wrap [@headlessui/react](https://headlessui.com) v2 for accessible behavior. Style with [Tailwind CSS](https://tailwindcss.com/docs/) utilities and project tokens.

**Full catalog:** [ui/docs/README.md](../studio-library/ui/docs/README.md)

## Peer dependency

```bash
npm install @headlessui/react tailwindcss
```

## Complete primitive map (v2)

| Need | Primitive | Styled atom/molecule |
|------|-----------|----------------------|
| Modal, confirm, CMD-K | `dialog` | `search-command` |
| Dropdown, account menu | `menu` | `dropdown-menu` |
| Contextual panel | `popover` | — |
| Single custom select | `listbox` | — |
| Searchable select | `combobox` | `search-command` |
| Accordion | `disclosure` | — |
| Settings tabs | `tabs` | — |
| Primary actions | `button` (primitive) | `button` (atom) |
| Boolean | `checkbox` | `checkbox` |
| Toggle | `switch` | `switch` |
| Radio set | `radio-group` | `radio-group` |
| Form structure | `field` | use with atoms |
| Text field | `input` | `input` |
| Multiline | `textarea` | `textarea` |
| Native select | `select` | `select` |
| Enter/leave motion | `transition` | — |
| Dialog close | `close-button` | — |

## Rules

1. **No hand-rolled modals** — use `dialog` or `search-command`
2. **Projects pull styled atoms first** — primitives for custom compositions only
3. **Tailwind for all styling** — no inline styles except dynamic values
4. New generics → [component-creation-playbook.md](./component-creation-playbook.md)

Path: `.quinsy-studio/studio-library/ui/primitives/headless/`
