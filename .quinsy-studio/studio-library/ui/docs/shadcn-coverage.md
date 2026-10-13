# shadcn coverage vs studio-library

Inventory date: 2026-09-12.

**Rule used:** keep the more **generic + CSS-variable themable** implementation. Brand-hardcoded chrome loses to shadcn semantic tokens (`bg-primary`, `--background`, `--ring`, …).

**Stacks (do not mix in one component):**

| Layer | Path | Behavior |
|-------|--------|----------|
| Primitive | `ui/primitives/headless/<slug>/` | Headless UI — unstyled a11y |
| Styled kit | `ui/components/<slug>/` | shadcn/Radix + CVA + tokens |
| Pattern chrome | `studio-rail`, `item-inspector`, … | Keep local to that pattern — not shadcn |

## Verdict on overlaps (library vs shadcn)

A near-complete shadcn kit was compared with the existing studio **styled** atoms (Button, Input, Badge, Checkbox, …). The atoms hard-coded one brand (`#ef7d62`, `--line`, `text-ink`), so they were **less** generic. **Adopted shadcn** for the overlap.

Headless primitives stay. `dialog-shell`, `dropdown` (Listbox), `segmented-toggle`, `search-command` stay as Headless compositions for projects that do not take Radix.

`atoms/Button` and `atoms/Badge` are **legacy wrappers** mapping old prop names onto the kit.

## Official shadcn catalog

| shadcn component | Studio library | Source / notes |
|-----------------|----------------|----------------|
| Accordion | `ui/components/accordion/` | Added (shadcn) |
| Alert | `ui/components/alert/` | Added (shadcn) |
| Alert Dialog | `ui/components/alert-dialog/` | Added (shadcn) |
| Aspect Ratio | `ui/components/aspect-ratio/` | Added (shadcn) |
| Attachment | `ui/components/attachment/` | Added (shadcn) — generic file chip |
| Avatar | `ui/components/avatar/` | Added (shadcn). `avatar-stack` remains a separate molecule |
| Badge | `ui/components/badge/` | **Replaced** brand-styled atom |
| Breadcrumb | `ui/components/breadcrumb/` | Added (shadcn) |
| Bubble | `ui/components/bubble/` | Added (shadcn) |
| Button | `ui/components/button/` | **Replaced** brand-styled atom |
| Button Group | `ui/components/button-group/` | Added (shadcn) |
| Calendar | `ui/components/calendar/` | Added (shadcn). Peer: `react-day-picker` |
| Card | `ui/components/card/` | **Replaced** with shadcn compound card |
| Carousel | `ui/components/carousel/` | Added. Peer: `embla-carousel-react` |
| Chart | `ui/components/chart/` | Added. Peer: `recharts` |
| Checkbox | `ui/components/checkbox/` | **Replaced** brand/Headless-styled |
| Collapsible | `ui/components/collapsible/` | Added (shadcn) |
| Combobox | `ui/components/combobox/` | Added (shadcn). Peer: `@base-ui/react`. Headless combobox primitive kept |
| Command | `ui/components/command/` | Added. Peer: `cmdk`. `search-command` Headless molecule kept |
| Context Menu | `ui/components/context-menu/` | Added (shadcn) |
| Data Table | — | Use `table` + project TanStack Table. Not a single primitive |
| Date Picker | — | Compose `calendar` + `popover`. a date-range picker is app-level — not copied |
| Dialog | `ui/components/dialog/` | Added (shadcn). `dialog-shell` Headless molecule kept |
| Direction | `ui/components/direction/` | Added (shadcn) |
| Drawer | `ui/components/drawer/` | Added. Peer: `vaul` |
| Dropdown Menu | `ui/components/dropdown-menu/` | **Replaced** Headless Menu molecule |
| Empty | `ui/components/empty/` | Added (shadcn) |
| Field | `ui/components/field/` | Added (shadcn). Headless `field` primitive kept |
| Hover Card | `ui/components/hover-card/` | Added (shadcn) |
| Input | `ui/components/input/` | **Replaced** brand-styled atom |
| Input Group | `ui/components/input-group/` | Added (shadcn) |
| Input OTP | `ui/components/input-otp/` | Added. Peer: `input-otp` |
| Item | `ui/components/item/` | Added (shadcn) |
| Kbd | `ui/components/kbd/` | Added (shadcn) |
| Label | `ui/components/label/` | Added (shadcn) |
| Marker | `ui/components/marker/` | Added (shadcn) |
| Menubar | `ui/components/menubar/` | Added (shadcn) |
| Message | `ui/components/message/` | Added (shadcn) |
| Message Scroller | **not vendored** | Needs `@shadcn/react/message-scroller` |
| Native Select | `ui/components/native-select/` | Added (shadcn) |
| Navigation Menu | `ui/components/navigation-menu/` | Added (shadcn) |
| Pagination | `ui/components/pagination/` | Added (shadcn) |
| Popover | `ui/components/popover/` | Added (shadcn). Headless popover primitive kept |
| Progress | `ui/components/progress/` | **Replaced** |
| Questionnaire | **not vendored** | Needs `@shadcn/react/questionnaire` |
| Radio Group | `ui/components/radio-group/` | **Replaced** brand-styled |
| Resizable | `ui/components/resizable/` | Added. Peer: `react-resizable-panels` |
| Scroll Area | `ui/components/scroll-area/` | Added (shadcn) |
| Select | `ui/components/select/` | **Replaced** native select atom with Radix select |
| Separator | `ui/components/separator/` | **Replaced** |
| Sheet | `ui/components/sheet/` | Added (shadcn) |
| Sidebar | `ui/components/sidebar/` | Added (shadcn) |
| Skeleton | `ui/components/skeleton/` | Added (shadcn). `atoms/Skeleton` size presets kept |
| Slider | `ui/components/slider/` | Added (shadcn) |
| Spinner | `ui/components/spinner/` | Added (shadcn) |
| Switch | `ui/components/switch/` | **Replaced** |
| Table | `ui/components/table/` | Added (shadcn) |
| Tabs | `ui/components/tabs/` | Added (shadcn). Headless tabs primitive kept |
| Textarea | `ui/components/textarea/` | **Replaced** |
| Toast | `toast` (existing) + `sonner` | Sonner is the themable toaster. Legacy `Toast` kept |
| Toggle | `ui/components/toggle/` | Added (shadcn) |
| Toggle Group | `ui/components/toggle-group/` | Added (shadcn). `segmented-toggle` Headless kept for A\|B |
| Tooltip | `ui/components/tooltip/` | **Replaced** |
| Typography | CSS / tokens | Not a component |

## Not promoted (product or app composition)

Product-specific providers, inspectors, host icons, and app compositions such as a date-range picker or calendar event views stay in the product. Build a date-range picker from `calendar` + `popover`.

## Studio-only (keep — not shadcn)

`icon`, `pageshell`, `studio-rail`, `auth-login`, `item-inspector`, `search-command`, `inline-form`, `checklist-item`, `dialog-shell`, `dropdown` (Listbox), `segmented-toggle`, `soft-card`, `palette-strip`, `avatar-stack`.

These are patterns or domain chrome. Do not replace with shadcn unless they become generic token-only.

`button` / `dialog` / `input` (etc.) **pull the styled kit**. Headless copies are registered as `headless-dialog`, `headless-input`, …

Projects remap **one** of:

- `--color-primary-*` / `--color-bg` / `--color-surface` (studio scale)
- shadcn aliases `--primary`, `--background`, `--foreground`, `--muted`, `--ring`, `--radius`, `--sidebar-*`

Tailwind v4: `@theme inline` at the bottom of `design-tokens.css`. v3: `tailwind.preset.ts`.

## Peers (install in the **project**, not required on every ticket)

Always for the styled kit: `radix-ui`, `class-variance-authority`, `clsx`, `tailwind-merge`, `lucide-react`.

Optional by component: `cmdk`, `vaul`, `@base-ui/react`, `input-otp`, `react-day-picker`, `recharts`, `embla-carousel-react`, `react-resizable-panels`, `sonner`.
