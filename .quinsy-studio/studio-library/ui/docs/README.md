# Studio UI Reference

> In-repo companion to [Tailwind CSS](https://tailwindcss.com/docs/) and [Headless UI](https://headlessui.com).  
> **All UI / frontend tickets must use Tailwind utilities + studio-library components** — no hand-rolled modals, raw unstyled form controls, or one-off CSS.

## Getting started

| Doc | Purpose |
|-----|---------|
| [Installation](./getting-started/installation.md) | Tailwind v4 + `@headlessui/react` in projects |
| [Atomic layout](./getting-started/atomic-design.md) | How library maps to Brad Frost levels |
| [Library-first](./getting-started/library-first.md) | `./studio library pull` before new UI |

## Primitives (Headless UI — behavior + a11y)

Unstyled re-exports. Style with Tailwind + project tokens.

| Primitive | Doc |
|-----------|-----|
| Dialog | [dialog](../../primitives/headless/dialog/README.md) |
| Menu | [menu](../../primitives/headless/menu/README.md) |
| Popover | [popover](../../primitives/headless/popover/README.md) |
| Listbox | [listbox](../../primitives/headless/listbox/README.md) |
| Combobox | [combobox](../../primitives/headless/combobox/README.md) |
| Disclosure | [disclosure](../../primitives/headless/disclosure/README.md) |
| Tabs | [tabs](../../primitives/headless/tabs/README.md) |
| Button | [button](../../primitives/headless/button/README.md) |
| Checkbox | [checkbox](../../primitives/headless/checkbox/README.md) |
| Switch | [switch](../../primitives/headless/switch/README.md) |
| RadioGroup | [radio-group](../../primitives/headless/radio-group/README.md) |
| Field / Fieldset | [field](../../primitives/headless/field/README.md) |
| Input | [input](../../primitives/headless/input/README.md) |
| Textarea | [textarea](../../primitives/headless/textarea/README.md) |
| Select | [select](../../primitives/headless/select/README.md) |
| Transition | [transition](../../primitives/headless/transition/README.md) |
| CloseButton | [close-button](../../primitives/headless/close-button/README.md) |

## Atoms (token-styled)

| Component | Variants / notes | Doc |
|-----------|------------------|-----|
| Button | primary, secondary, outline, ghost, **link**, destructive | [button](../../components/button/README.md) |
| Input | text fields | [input](../../components/input/README.md) |
| Textarea | multiline | [textarea](../../components/textarea/README.md) |
| Select | native select | [select](../../components/select/README.md) |
| Checkbox | boolean | [checkbox](../../components/checkbox/README.md) |
| Switch | toggle | [switch](../../components/switch/README.md) |
| Badge | status chips | [badge](../../components/badge/) |
| Icon | SVG icons | [icon](../../components/icon/) |
| Card | surface container | [card](../../components/card/README.md) |

## Molecules

| Component | Composes | Doc |
|-----------|----------|-----|
| DropdownMenu | Menu + Button | [dropdown-menu](../../components/dropdown-menu/README.md) |
| RadioGroup | RadioGroup primitive | [radio-group](../../components/radio-group/README.md) |
| SearchCommand | Dialog + Combobox | [search-command](../../components/search-command/README.md) |
| InlineForm | Input + Button | [inline-form](../../components/inline-form/) |
| ChecklistItem | toggle row | [checklist-item](../../components/checklist-item/) |

## Organisms

| Component | Doc |
|-----------|-----|
| PageShell | [pageshell](../../components/pageshell/) |

## Tokens

| Resource | Doc |
|----------|-----|
| Design tokens | [tokens](../../tokens/README.md) |
| Tailwind preset | `ui/tokens/tailwind.preset.ts` |

## Patterns

| Pattern | Doc |
|---------|-----|
| Transitions | [patterns/transitions.md](./patterns/transitions.md) |
| Forms | [patterns/forms.md](./patterns/forms.md) |
| Upgrade soft-path | [patterns/upgrade-soft-path.md](./patterns/upgrade-soft-path.md) |
| Dark mode | [patterns/dark-mode.md](./patterns/dark-mode.md) |

## Enforcement (tickets)

- **Team 01** FE-001 / FE-002: load this index before implement
- **No custom overlay** without Dialog primitive
- **No raw `<select>` styling** without `select` atom or Listbox primitive
- External reference: [Tailwind docs](https://tailwindcss.com/docs/) for utility classes
