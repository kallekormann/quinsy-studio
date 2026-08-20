# Frontend Playbook

> Component composition, IndexedDB local-first, SSR/ISR — the global frontend standards.

## Core principle

```
Fast. Offline-capable. Accessible.
No compromise on performance.
```

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

## References

- `.quinsy-studio/knowledge-base/design_playbook.md` — design standards
- `.quinsy-studio/knowledge-base/anti_ai_slop_protocol.md` — frontend slop rules
- `.quinsy-studio/studio-library/ui/` — UI assets
- `.quinsy-studio/teams/01-frontend-experience/` — frontend team
