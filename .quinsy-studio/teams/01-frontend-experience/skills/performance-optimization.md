# Skill: Performance Optimization

> Core Web Vitals, Bundle-Analyse, Code-Splitting, Lazy Loading, Caching

## Metadata

```
skill_id: FE-003
name: Performance Optimization
team: 01-frontend-experience
lead_role: Frontend Architect
support_roles: [Frontend Engineer, Platform Architect]
phases: [3, 4, 5, 7]
activation_triggers:
  - Ticket enthält "Performance", "Ladezeit", "Speed", "Bundle"
  - Core Web Vitals sind unter Budget
  - Lighthouse-Score < 90
  - Phase 5 QA-Gate prüft Performance
```

---

## Verhaltensregeln

### 1. Performance Budget

```markdown
Core Web Vitals:
  LCP (Largest Contentful Paint):  < 2.5s
  INP (Interaction to Next Paint): < 200ms
  CLS (Cumulative Layout Shift):   < 0.1

Lighthouse Scores:
  Performance:     > 90
  Accessibility:   > 90
  Best Practices:  > 90
  SEO:             > 90

Bundle Budget:
  Total:           < 250KB (gzipped)
  First Load JS:   < 100KB (gzipped)
  CSS:             < 50KB (gzipped)
```

### 2. Code-Splitting Strategie

```markdown
Splitting-Punkte:
1. Route-basiert (Next.js: automatisch via dynamic imports)
2. Komponenten-basiert (bei large Komponenten)
3. Library-basiert (bei großen Dependencies)

dynamic import für:
  - Modal-Komponenten
  - Chart-Libraries
  - Editor-Komponenten
  - Anything > 20KB das nicht sofort sichtbar ist
```

### 3. Lazy Loading

```markdown
Bilder:
  - loading="lazy" für below-the-fold Bilder
  - srcset für responsive Bilder
  - WebP/AVIF Format
  - Blur-Placeholder für LCP-Bilder

Komponenten:
  - React.lazy() + Suspense
  - Intersection Observer für无限列表
  - Prefetching für wahrscheinliche nächste Routes

Daten:
  - SWR/React Query für Client-fetching
  - ISR (Incremental Static Regeneration) für statische Seiten
  - Streaming SSR für komplexe Seiten
```

### 4. Caching-Strategie

```markdown
HTTP Caching:
  - Static Assets: immutable, long-cache (1 year)
  - API Responses: stale-while-revalidate
  - HTML: short-cache + revalidation

Service Worker (PWA):
  - Cache-First für statische Assets
  - Network-First für API Calls
  - Offline-Fallback für kritische Seiten
```

### 5. Image-Optimierung

```markdown
Formate:
  - WebP als Standard
  - AVIF als Modern-Fallback
  - PNG nur für Transparenz
  - SVG für Icons

Techniken:
  - Responsive Images (srcset, sizes)
  - Lazy Loading (loading="lazy")
  - Blur-Placeholder
  - CDN für Image-Resizing
```

### 6. Monitoring

```markdown
Tools:
  - Lighthouse CI (in Pipeline)
  - Web Vitals Library (im Code)
  - Sentry Performance Monitoring
  - Custom Performance Marks

Metriken tracken:
  - FCP (First Contentful Paint)
  - LCP (Largest Contentful Paint)
  - INP (Interaction to Next Paint)
  - CLS (Cumulative Layout Shift)
  - TTFB (Time to First Byte)
```

---

## Anti-Patterns

### ❌ Verboten

```markdown
- Große Bundle ohne Code-Splitting
- Alle Bilder ohne Lazy Loading
- CSS/JS ohne Minification
- Keine Preloading-Prefetching Strategie
- Performance erst in Phase 5 prüfen
- Kein Performance Budget
- Inline-SVGs für komplexe Icons (statt Sprite/Component)
```

### ✅ Stattdessen

```markdown
- Dynamische Imports für alles > 20KB
- Lazy Loading für below-the-fold
- Minification + Tree-Shaking
- Prefetching für wahrscheinliche nächste Routes
- Performance-Check in Phase 3 (früh!)
- Lighthouse CI in Pipeline
- SVG-Sprite oder Icon-Component
```

---

## Referenzen

- `.quinsy-studio/knowledge-base/frontend_playbook.md` — Frontend-Regeln
- `.quinsy-studio/process/gates.md` — Performance im Gate 5
- `./studio gate <project> --performance` — Performance-Check
