# Frontend Playbook

> Component-Composition, IndexedDB Local-First, SSR/ISR — die globalen Frontend-Standards.

## Grundprinzip

```
Schnell. Offline-fähig. Barrierefrei.
Kein Kompromiss bei Performance.
```

---

## Architektur

### Monorepo-Struktur

```
project/
├── apps/
│   └── web/              # Next.js App
├── packages/
│   ├── ui/               # Shared Components
│   ├── config/           # ESLint, Prettier
│   └── tsconfig/         # TypeScript Configs
├── turbo.json
├── pnpm-workspace.yaml
└── package.json
```

### Component Composition

```
Atoms → Molecules → Organisms → Templates → Pages

Button, Input     Card, Form       Header, Footer    Page-Layout    Home, About
Badge, Icon       Modal, Dropdown  Sidebar, Nav
```

**Regel:** Komponenten sind generisch, konfigurierbar, wiederverwendbar.

---

## Next.js App Router

### Grundstruktur

```typescript
// app/layout.tsx
export default function RootLayout({ children }) {
  return (
    <html lang="de">
      <body>{children}</body>
    </html>
  );
}

// app/page.tsx
export default function Home() {
  return <main>...</main>;
}
```

### Server Components (Standard)

```typescript
// Server Component (kein "use client")
async function UserData({ userId }) {
  const user = await db.user.findUnique({ where: { id: userId } });
  return <div>{user.name}</div>;
}
```

### Client Components (nur bei Bedarf)

```typescript
"use client";

import { useState } from 'react';

function InteractiveComponent() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}
```

**Regel:** Server Components als Default, Client Components nur wenn nötig (Interaktivität, Browser APIs).

---

## IndexedDB Local-First

### Architektur

```
┌─────────────────────────────────────────────────────────┐
│                    LOCAL-FIRST ARCHITECTURE              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────┐     ┌─────────────┐                   │
│  │   UI Layer  │────▶│  Local DB   │                   │
│  │  (React)    │     │ (IndexedDB) │                   │
│  └─────────────┘     └──────┬──────┘                   │
│                             │                           │
│                      ┌──────▼──────┐                   │
│                      │   Sync Layer│                   │
│                      │  (Optional) │                   │
│                      └──────┬──────┘                   │
│                             │                           │
│                      ┌──────▼──────┐                   │
│                      │  Cloud DB   │                   │
│                      │ (Supabase)  │                   │
│                      └─────────────┘                   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Implementierung (idb Library)

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

### Offline-First Strategie

```typescript
// Service Worker für Offline
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

### Core Web Vitals Budget

| Metric | Target | Measurement |
|--------|--------|-------------|
| LCP | < 2.5s | Largest Contentful Paint |
| FID | < 100ms | First Input Delay |
| CLS | < 0.1 | Cumulative Layout Shift |
| INP | < 200ms | Interaction to Next Paint |

### Optimierungen

```typescript
// 1. Lazy Loading
const HeavyComponent = dynamic(() => import('./HeavyComponent'), { loading: () => <Spinner /> });

// 2. Image Optimization
import Image from 'next/image';
<Image src="/photo.jpg" width={500} height={300} alt="Description" priority={false} />

// 3. Font Optimization
import { Inter } from 'next/font/google';
const inter = Inter({ subsets: ['latin'] });

// 4. Script Optimization
import Script from 'next/script';
<Script src="/analytics.js" strategy="lazyOnload" />
```

### Bundle-Analyse

```bash
# Build mit Analyse
ANALYZE=true pnpm build

# Lighthouse
npx lighthouse http://localhost:3000 --output=html
```

---

## State Management

### Einfach: React State

```typescript
// Für lokale State
const [count, setCount] = useState(0);

// Für abgeleiteten State
const doubleCount = useMemo(() => count * 2, [count]);
```

### Mittel: Context

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

### Komplex: Zustand / Jotai

```typescript
import { create } from 'zustand';

const useStore = create((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
}));
```

**Regel:** Einfach → Mittel → Komplex. Nicht übervieren.

---

## Testing

### Unit Tests (Vitest)

```typescript
import { render, screen } from '@testing-library/react';
import { Button } from './Button';

test('renders correctly', () => {
  render(<Button>Click me</Button>);
  expect(screen.getByText('Click me')).toBeInTheDocument();
});
```

### E2E Tests (Playwright)

```typescript
import { test, expect } from '@playwright/test';

test('homepage loads', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveTitle(/My App/);
});
```

---

## Referenzen

- `.quinsy-studio/knowledge-base/design_playbook.md` — Design-Standards
- `.quinsy-studio/knowledge-base/anti_ai_slop_protocol.md` — Frontend-Slop-Regeln
- `.quinsy-studio/studio-library/ui/` — UI-Assets
- `.quinsy-studio/teams/01-frontend-experience/` — Frontend-Team
