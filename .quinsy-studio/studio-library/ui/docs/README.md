# Studio UI Reference

> In-repo companion to [Tailwind CSS](https://tailwindcss.com/docs/), [Headless UI](https://headlessui.com), and a **shadcn-style** themable kit.  
> **All UI / frontend tickets must use Tailwind utilities + studio-library components** — no hand-rolled modals, raw unstyled form controls, or one-off CSS.

**Coverage vs shadcn / Command Center:** [shadcn-coverage.md](./shadcn-coverage.md)

## Getting started

| Doc | Purpose |
|-----|---------|
| [Installation](./getting-started/installation.md) | Tailwind v4 + Headless UI + Radix kit peers |
| [Atomic layout](./getting-started/atomic-design.md) | How library maps to Brad Frost levels |
| [Library-first](./getting-started/library-first.md) | `./studio library pull` before new UI |
| [shadcn coverage](./shadcn-coverage.md) | What we have, what we skipped, what won |

## Primitives (Headless UI — behavior + a11y)

Unstyled re-exports. Style with Tailwind + project tokens, **or** use the styled kit below (Radix).

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

## Styled kit (shadcn / tokens)

CVA + CSS variables (`--primary`, `--background`, `--muted-foreground`, …). Pull the slug you need. Full list: [shadcn-coverage.md](./shadcn-coverage.md).

### Atoms

Button, Input, Textarea, Label, Badge, Checkbox, Switch, Separator, Skeleton, Kbd, Spinner, Avatar, Progress, Slider, Toggle, Native Select, Aspect Ratio, Icon.

### Molecules

Alert, Alert Dialog, Card, Field, Input Group, Input OTP, Tooltip, Popover, Hover Card, Accordion, Collapsible, Tabs, Radio Group, Dropdown Menu, Select, Dialog, Sheet, Drawer, Pagination, Breadcrumb, Button Group, Toggle Group, Empty, Item, Combobox, Sonner, Attachment, Bubble, Message, Marker.

Headless compositions still available: DialogShell, Dropdown (Listbox), SegmentedToggle, SearchCommand, InlineForm, ChecklistItem.

### Organisms

Table, Command, Menubar, Navigation Menu, Context Menu, Sidebar, Calendar, Carousel, Chart, Resizable, Scroll Area, PageShell, StudioRail.

## Tokens

| Resource | Doc |
|----------|-----|
| Design tokens + shadcn aliases | [tokens](../../tokens/README.md) |
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
- **No custom overlay** without Dialog primitive **or** `dialog` / `sheet` kit
- **No raw `<select>` styling** — use `select` kit or Listbox / `native-select`
- External reference: [Tailwind docs](https://tailwindcss.com/docs/) for utility classes
