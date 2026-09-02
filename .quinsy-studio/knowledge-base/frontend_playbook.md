# Frontend Playbook

> Component composition, IndexedDB local-first, SSR/ISR — the global frontend standards.

## Core principle

```
Fast. Offline-capable. Accessible.
No compromise on performance.
```

---

## Canvas shell vs document routes (LO-0035)

Infinite-canvas apps often lock the board shell with `h-dvh overflow-hidden`. That is correct for Konva/canvas, but **document UIs** under the same segment (`/board/[id]/brand-guide`, `/presentation`, etc.) will not scroll on `body`.

**Do:** Add a nested `layout.tsx` with `h-dvh overflow-y-auto` (or make the document `main` the scrollport).  
**Do:** Dialog shells with tall content use `max-h-[min(90dvh,…)]` + `overflow-y-auto` on the body region; keep header/footer `shrink-0`.  
**Don't:** Assume page scroll works under the canvas shell without a dedicated scroll container.

---

## Docked chrome reuse (LO-0039)

When reusing **Studio rail / panel** chrome (`StudioPanel`, `StudioRail`, `StudioDock`, floating right rails) across surfaces (canvas, Library, hubs):

**Do:** Mount the **component** (`StudioPanel` / `StudioDock`), not only copy `studioPanelClass` onto an aside.  
**Do:** Assert **flush to the intended edge** (no content-inset / `chromePageBody` gutter beside the panel).  
**Do:** Assert **full height** of the stage under app chrome (top→bottom) — not a mid-page sticky card.  
**Don't:** Mark done because class names match canvas while live layout still looks like a floating card.

See also: `process/human-in-the-loop.md` (LO-0039 sprint DoD rule).

### Component reuse ladder (LO-0040)

Before shipping new chrome or a lookalike panel:

1. **Reuse** — mount the existing component (`StudioDock` / `StudioPanel` / shared inspector shell, etc.).
2. **Project component** — if the pattern exists in markup only, extract a reusable component under the project `ui/` (or `src/components/`) used by every surface that needs it.
3. **Studio library** — if the pattern is generic across products, author or promote under `.quinsy-studio/studio-library/` (see `component-creation-playbook.md`).

**Right-rail dock:** icon rail + peer detail panel (`studio-rail` / `StudioDock`) is the canonical organism for “tools beside the stage.” Do not fake it with padded cards or duplicate headers that diverge from the docked composition.

See also: `process/human-in-the-loop.md` (LO-0040); SaaS archetype UX option in `process/project-archetypes.md`.

---

## Architecture

### Monorepo structure

```
project/
├── apps/
│   └── web/              # Next.js app
├── packages/
│   ├── ui/               # shared components
│   ├── config/           # ESLint, Prettier
│   └── tsconfig/         # TypeScript configs
├── turbo.json
├── pnpm-workspace.yaml
└── package.json
```

### Component composition

```
Atoms → Molecules → Organisms → Templates → Pages

Button, Input     Card, Form       Header, Footer    Page layout    Home, About
Badge, Icon       Modal, Dropdown  Sidebar, Nav
```

**Rule:** components are generic, configurable, reusable.

### Selects / dropdowns (anti-OS-chrome)

**Do not use native `<select>`** on product surfaces (board, dialogs, settings, presentation). OS chrome mixes with brand UI.

Use a **Headless UI Listbox/Menu** molecule (studio-library `dropdown` / project Dropdown) styled like other popovers (e.g. user menu). Keyboard Esc + outside click must dismiss.

**Binary labeled choices** (Selected | Whole board, View | Edit): use studio-library **`SegmentedToggle`** — not a pair of ad-hoc buttons, and not `Switch` (Switch is boolean on/off only). Pull: `./studio library pull <project> segmented-toggle`.

**Dialog / panel dark surfaces:** light = white; dark = one shared elevated token (`dark:bg-surface-dark`) for DialogShell, share modals, and item details — never mix `neutral-900` with `surface-dark`. See [dark-mode.md](../studio-library/ui/docs/patterns/dark-mode.md).

**Radio / checkbox selected chrome:** use a brand token the project actually defines (`primary-*` or `accent-*`). Empty radio dots + accent borders usually mean undefined `primary-*`.

**Browser extensions (MV3 + Vite):** see [chrome-mv3-vite-content-scripts.md](./chrome-mv3-vite-content-scripts.md) — content entries must be IIFE or `content_scripts.type: "module"`; classic scripts with `import` fail silently.

---

## Next.js App Router

### Basic structure

```typescript
// app/layout.tsx
export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}

// app/page.tsx
export default function Home() {
  return <main>...</main>;
}
```

### Server components (default)

```typescript
// server component (no "use client")
async function UserData({ userId }) {
  const user = await db.user.findUnique({ where: { id: userId } });
  return <div>{user.name}</div>;
}
```

### Client components (only when needed)

```typescript
"use client";

import { useState } from 'react';

function InteractiveComponent() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}
```

**Rule:** server components by default, client components only when necessary (interactivity, browser APIs).

---

## IndexedDB local-first

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    LOCAL-FIRST ARCHITECTURE              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────┐     ┌─────────────┐                   │
│  │   UI layer  │────▶│  Local DB   │                   │
│  │  (React)    │     │ (IndexedDB) │                   │
│  └─────────────┘     └──────┬──────┘                   │
│                             │                           │
│                      ┌──────▼──────┐                   │
│                      │   sync layer│                   │
│                      │  (optional) │                   │
│                      └──────┬──────┘                   │
│                             │                           │
│                      ┌──────▼──────┐                   │
│                      │  cloud DB   │                   │
│                      │ (Supabase)  │                   │
│                      └─────────────┘                   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Implementation (idb library)

```typescript
import { openDB } from 'idb';

const dbPromise = openDB('myapp', 1, {
  upgrade(db) {
    const store = db.createObjectStore('tasks', { keyPath: 'id' });
    store.createIndex('by-date', 'createdAt');
  },
});

// Read
const tasks = await (await dbPromise).getAll('tasks');

// Write
await (await dbPromise).put('tasks', { id: '1', title: 'Buy milk' });

// Sync (optional)
async function syncToCloud() {
  const local = await (await dbPromise).getAll('tasks');
  await fetch('/api/sync', { method: 'POST', body: JSON.stringify(local) });
}
```

### Offline-first strategy

```typescript
// service worker for offline
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request);
    })
  );
});
```

---

## Performance

### Core web vitals budget

| Metric | Target | Measurement |
|--------|--------|-------------|
| LCP | < 2.5s | Largest Contentful Paint |
| FID | < 100ms | First Input Delay |
| CLS | < 0.1 | Cumulative Layout Shift |
| INP | < 200ms | Interaction to Next Paint |

### Optimizations

```typescript
// 1. Lazy loading
const HeavyComponent = dynamic(() => import('./HeavyComponent'), { loading: () => <Spinner /> });

// 2. Image optimization
import Image from 'next/image';
<Image src="/photo.jpg" width={500} height={300} alt="Description" priority={false} />

// 3. Font optimization
import { Inter } from 'next/font/google';
const inter = Inter({ subsets: ['latin'] });

// 4. Script optimization
import Script from 'next/script';
<Script src="/analytics.js" strategy="lazyOnload" />
```

### Bundle analysis

```bash
# build with analysis
ANALYZE=true pnpm build

# lighthouse
npx lighthouse http://localhost:3000 --output=html
```

---

## State management

### Simple: React state

```typescript
// for local state
const [count, setCount] = useState(0);

// for derived state
const doubleCount = useMemo(() => count * 2, [count]);
```

### Medium: Context

```typescript
const ThemeContext = createContext('light');

function App() {
  return (
    <ThemeContext.Provider value="dark">
      <Child />
    </ThemeContext.Provider>
  );
}
```

### Complex: Zustand / Jotai

```typescript
import { create } from 'zustand';

const useStore = create((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
}));
```

**Rule:** simple → medium → complex. Don't over-engineer.

---

## Testing

### Unit tests (Vitest)

```typescript
import { render, screen } from '@testing-library/react';
import { Button } from './Button';

test('renders correctly', () => {
  render(<Button>Click me</Button>);
  expect(screen.getByText('Click me')).toBeInTheDocument();
});
```

### E2E tests (Playwright)

```typescript
import { test, expect } from '@playwright/test';

test('homepage loads', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveTitle(/My App/);
});
```

---

## Tailwind content scan (shared class constants)

**Signal (LO-0027 / moody):** Shared layout class strings living only in `src/lib/**` (or any path **outside** `tailwind.config` `content`) and applied as `className={SOME_CONST}` are **purged**. The DOM still has the class names, but CSS never emits utilities like `right-3` → absolute panels fall to the **left**. Hard refresh cannot fix missing CSS.

### Rules

1. **Every path that defines Tailwind class strings must be in `content`** — including `src/lib/**` if motion/layout helpers export class constants.
2. **Prefer literal `className="…"` in scanned TSX** (components under `src/components`, `src/app`, `ui/components`) for layout-critical utilities (`absolute`, `right-*`, `left-*`, `top-*`, `bottom-*`, width).
3. **Do not treat variable `className={CONST}` as Tailwind-visible** unless the constant’s file is scanned **or** the full string also appears as a literal somewhere in `content`.
4. **DoD for dock/position tickets:** DevTools Computed shows non-auto `right`/`left`, **or** confirm the utility exists in built CSS — not only that the TSX constant looks correct.
5. **Belt:** optional `style={{ right: N, width: N }}` for critical floating rails so purge mistakes cannot silent-regress.

### Anti-pattern

```ts
// src/lib/motion/app-motion.ts  ← NOT in content
export const FLOATING_RIGHT_RAIL_CLASS = 'absolute right-3 ...';

// drawer (scanned) — Tailwind never sees the string
className={FLOATING_RIGHT_RAIL_CLASS}
```

### Pattern

```tsx
// Literal in a content-scanned component (same idea as InspectorPanelShell)
className="absolute bottom-20 right-3 top-14 z-30 flex w-[280px] ..."
```

---

## PDF export DoD (Playwright + watermark)

**Signal (LO-0028 / moody):** Brand-guide PDF via Playwright can 503 when Chromium is missing; free Export PDF can die in `applyWatermark` (`Failed to load export image for watermark`) with no file. Both look “done” in unit tests.

### Rules

1. **Smoke downloads a PDF** for brand-guide Download PDF and Export → PDF (free path) before marking done.
2. **File size > 0** — record downloaded PNG/PDF byte length in the smoke note; empty files and silent “success” without a download are not done (LO-0028 follow-up / moody S65).
3. **Playwright Chromium** must be installed for local/dev when the brand-guide PDF API uses `chromium.launch` — document in project setup / RUNBOOK, or provide a non-headless fallback.
4. **Watermark must not hard-block download** — on decode failure, skip watermark and still save PDF (or fix decode); never leave the user with only an error toast.
5. **Anti-slop on export paths (LO-0029)** — no bare `100`/`1000`/`86400`; no consecutive `await`/`await` lines. Use named constants and await chaining / helpers before gate 5.
6. Review briefs for PDF tickets: numbered steps that click Download PDF / Export PDF and confirm a **non-empty** file appears.
7. **WYSIWYG type stack (LO-0032)** — if the ticket touches an on-screen brand guide / print preview **and** a PDF (or printable HTML) of the same surface, DoD must assert **the same font-family stack** for hero/title and body on screen and in PDF. Shared CSS/tokens preferred over divergent React vs PDF HTML. Serif on screen + sans in PDF (or the reverse) is not done.

---

## References

- `.quinsy-studio/knowledge-base/design_playbook.md` — design standards
- `.quinsy-studio/knowledge-base/anti_ai_slop_protocol.md` — frontend slop rules
- `.quinsy-studio/studio-library/ui/` — UI assets
- `.quinsy-studio/teams/01-frontend-experience/` — frontend team
