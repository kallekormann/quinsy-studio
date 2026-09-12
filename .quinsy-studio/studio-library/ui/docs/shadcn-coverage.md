# shadcn coverage vs studio-library

Inventory date: 2026-09-12.

**Rule used:** keep the more **generic + CSS-variable themable** implementation. Brand-hardcoded coral/Bloom chrome loses to shadcn semantic tokens (`bg-primary`, `--background`, `--ring`, …).

**Stacks (do not mix in one component):**

| Layer | Path | Behavior |
|-------|--------|----------|
| Primitive | `ui/primitives/headless/<slug>/` | Headless UI — unstyled a11y |
| Styled kit | `ui/components/<slug>/` | shadcn/Radix + CVA + tokens |
| Product chrome | `studio-rail`, `item-inspector`, `emotion-strip`, … | Keep local to that pattern — not shadcn |

## Verdict on overlaps (library vs Command Center)

Command Center `apps/command-center/src/components/ui` is a near-complete shadcn kit. Existing studio **styled** atoms (Button, Input, Badge, Checkbox, …) were Moody Bloom (hardcoded `#ef7d62`, `--line`, `text-ink`). Those are **less** generic. **Adopted Command Center / shadcn** for the overlap.

Headless primitives stay. `dialog-shell`, `dropdown` (Listbox), `segmented-toggle`, `search-command` stay as Headless compositions for projects that do not take Radix.

`atoms/Button` and `atoms/Badge` are **legacy wrappers** mapping old prop names onto the kit.

## Official shadcn catalog

| shadcn component | Studio library | Source / notes |
|-----------------|----------------|----------------|
| Accordion | `ui/components/accordion/` | Added (CC) |
| Alert | `ui/components/alert/` | Added (CC) |
| Alert Dialog | `ui/components/alert-dialog/` | Added (CC) |
| Aspect Ratio | `ui/components/aspect-ratio/` | Added (CC) |
| Attachment | `ui/components/attachment/` | Added (CC) — generic file chip |
| Avatar | `ui/components/avatar/` | Added (CC). `avatar-stack` remains a separate molecule |
| Badge | `ui/components/badge/` | **Replaced** Bloom with CC |
| Breadcrumb | `ui/components/breadcrumb/` | Added (CC) |
| Bubble | `ui/components/bubble/` | Added (CC) |
| Button | `ui/components/button/` | **Replaced** Bloom |
| Button Group | `ui/components/button-group/` | Added (CC) |
| Calendar | `ui/components/calendar/` | Added (CC). Peer: `react-day-picker` |
| Card | `ui/components/card/` | **Replaced** with CC compound card |
| Carousel | `ui/components/carousel/` | Added. Peer: `embla-carousel-react` |
| Chart | `ui/components/chart/` | Added. Peer: `recharts` |
| Checkbox | `ui/components/checkbox/` | **Replaced** Bloom/Headless-styled |
| Collapsible | `ui/components/collapsible/` | Added (CC) |
| Combobox | `ui/components/combobox/` | Added (CC). Peer: `@base-ui/react`. Headless combobox primitive kept |
| Command | `ui/components/command/` | Added. Peer: `cmdk`. `search-command` Headless molecule kept |
| Context Menu | `ui/components/context-menu/` | Added (CC) |
| Data Table | — | Use `table` + project TanStack Table. Not a single primitive |
| Date Picker | — | Compose `calendar` + `popover`. CC `date-range-picker` is app-level — not copied |
| Dialog | `ui/components/dialog/` | Added (CC). `dialog-shell` Headless molecule kept |
| Direction | `ui/components/direction/` | Added (CC) |
| Drawer | `ui/components/drawer/` | Added. Peer: `vaul` |
| Dropdown Menu | `ui/components/dropdown-menu/` | **Replaced** Headless Menu molecule |
| Empty | `ui/components/empty/` | Added (CC) |
| Field | `ui/components/field/` | Added (CC). Headless `field` primitive kept |
| Hover Card | `ui/components/hover-card/` | Added (CC) |
| Input | `ui/components/input/` | **Replaced** Bloom |
| Input Group | `ui/components/input-group/` | Added (CC) |
| Input OTP | `ui/components/input-otp/` | Added. Peer: `input-otp` |
| Item | `ui/components/item/` | Added (CC) |
| Kbd | `ui/components/kbd/` | Added (CC) |
| Label | `ui/components/label/` | Added (CC) |
| Marker | `ui/components/marker/` | Added (CC) |
| Menubar | `ui/components/menubar/` | Added (CC) |
| Message | `ui/components/message/` | Added (CC) |
| Message Scroller | **not vendored** | Needs `@shadcn/react/message-scroller` |
| Native Select | `ui/components/native-select/` | Added (CC) |
| Navigation Menu | `ui/components/navigation-menu/` | Added (CC) |
| Pagination | `ui/components/pagination/` | Added (CC) |
| Popover | `ui/components/popover/` | Added (CC). Headless popover primitive kept |
| Progress | `ui/components/progress/` | **Replaced** |
| Questionnaire | **not vendored** | Needs `@shadcn/react/questionnaire` |
| Radio Group | `ui/components/radio-group/` | **Replaced** Bloom-styled |
| Resizable | `ui/components/resizable/` | Added. Peer: `react-resizable-panels` |
| Scroll Area | `ui/components/scroll-area/` | Added (CC) |
| Select | `ui/components/select/` | **Replaced** native select atom with Radix select |
| Separator | `ui/components/separator/` | **Replaced** |
| Sheet | `ui/components/sheet/` | Added (CC) |
| Sidebar | `ui/components/sidebar/` | Added (CC) |
| Skeleton | `ui/components/skeleton/` | Added (CC). `atoms/Skeleton` size presets kept |
| Slider | `ui/components/slider/` | Added (CC) |
| Spinner | `ui/components/spinner/` | Added (CC) |
| Switch | `ui/components/switch/` | **Replaced** |
| Table | `ui/components/table/` | Added (CC) |
| Tabs | `ui/components/tabs/` | Added (CC). Headless tabs primitive kept |
| Textarea | `ui/components/textarea/` | **Replaced** |
| Toast | `toast` (existing) + `sonner` | Sonner is the themable toaster. Legacy `Toast` kept |
| Toggle | `ui/components/toggle/` | Added (CC) |
| Toggle Group | `ui/components/toggle-group/` | Added (CC). `segmented-toggle` Headless kept for A\|B |
| Tooltip | `ui/components/tooltip/` | **Replaced** |
| Typography | CSS / tokens | Not a component |

## Command Center files not promoted (product or host)

| Path | Why |
|------|-----|
| `host-scope-provider.tsx` | Affiliate host scope |
| `inspector-sheet.tsx` | Product inspector |
| `date-range-picker.tsx` | App composition; build from calendar + popover |
| `calendar/event-calendar-views.tsx` | FullCalendar product view |
| `simple-icon.tsx` | Host icons |

## Studio-only (keep — not shadcn)

`icon`, `pageshell`, `studio-rail`, `auth-login`, `item-inspector`, `search-command`, `inline-form`, `checklist-item`, `dialog-shell`, `dropdown` (Listbox), `segmented-toggle`, `soft-card`, `emotion-strip`, `palette-strip`, `avatar-stack`.

These are patterns or domain chrome. Do not replace with shadcn unless they become generic token-only.

`button` / `dialog` / `input` (etc.) **pull the styled kit**. Headless copies are registered as `headless-dialog`, `headless-input`, …

Projects remap **one** of:

- `--color-primary-*` / `--color-bg` / `--color-surface` (studio scale)
- shadcn aliases `--primary`, `--background`, `--foreground`, `--muted`, `--ring`, `--radius`, `--sidebar-*`

Tailwind v4: `@theme inline` at the bottom of `design-tokens.css`. v3: `tailwind.preset.ts`.

## Peers (install in the **project**, not required on every ticket)

Always for the styled kit: `radix-ui`, `class-variance-authority`, `clsx`, `tailwind-merge`, `lucide-react`.

Optional by component: `cmdk`, `vaul`, `@base-ui/react`, `input-otp`, `react-day-picker`, `recharts`, `embla-carousel-react`, `react-resizable-panels`, `sonner`.
