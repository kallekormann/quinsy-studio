# Skill: Performance Optimization

> Core web vitals, bundle analysis, code splitting, lazy loading, caching

## Metadata

```
skill_id: FE-003
name: Performance Optimization
team: 01-frontend-experience
lead_role: Frontend Architect
support_roles: [Frontend Engineer, Platform Architect]
phases: [3, 4, 5, 7]
activation_triggers:
  - Ticket contains "performance", "load time", "speed", "bundle"
  - Core web vitals are under budget
  - Lighthouse score < 90
  - Phase 5 QA gate checks performance
```

---

## Behavior rules

### 1. Performance budget

```markdown
Core web vitals:
  LCP (Largest Contentful Paint):  < 2.5s
  INP (Interaction to Next Paint): < 200ms
  CLS (Cumulative Layout Shift):   < 0.1

Lighthouse scores:
  Performance:     > 90
  Accessibility:   > 90
  Best practices:  > 90
  SEO:             > 90

Bundle budget:
  Total:           < 250KB (gzipped)
  First load JS:   < 100KB (gzipped)
  CSS:             < 50KB (gzipped)
```

### 2. Code-splitting strategy

```markdown
Splitting points:
1. Route-based (Next.js: automatic via dynamic imports)
2. Component-based (for large components)
3. Library-based (for large dependencies)

dynamic import for:
  - modal components
  - chart libraries
  - editor components
  - anything > 20KB that is not immediately visible
```

### 3. Lazy loading

```markdown
Images:
  - loading="lazy" for below-the-fold images
  - srcset for responsive images
  - WebP/AVIF format
  - Blur placeholder for LCP images

Components:
  - React.lazy() + Suspense
  - Intersection observer for infinite lists
  - Prefetching for likely next routes

Data:
  - SWR/React Query for client fetching
  - ISR (Incremental Static Regeneration) for static pages
  - Streaming SSR for complex pages
```

### 4. Caching strategy

```markdown
HTTP caching:
  - Static assets: immutable, long cache (1 year)
  - API responses: stale-while-revalidate
  - HTML: short cache + revalidation

Service worker (PWA):
  - Cache-first for static assets
  - Network-first for API calls
  - Offline fallback for critical pages
```

### 5. Image optimization

```markdown
Formats:
  - WebP as standard
  - AVIF as modern fallback
  - PNG only for transparency
  - SVG for icons

Techniques:
  - Responsive images (srcset, sizes)
  - Lazy loading (loading="lazy")
  - Blur placeholder
  - CDN for image resizing
```

### 6. Monitoring

```markdown
Tools:
  - Lighthouse CI (in pipeline)
  - Web vitals library (in code)
  - Sentry performance monitoring
  - Custom performance marks

Track metrics:
  - FCP (First Contentful Paint)
  - LCP (Largest Contentful Paint)
  - INP (Interaction to Next Paint)
  - CLS (Cumulative Layout Shift)
  - TTFB (Time to First Byte)
```

---

## Anti-patterns

### ❌ Forbidden

```markdown
- Large bundle without code splitting
- All images without lazy loading
- CSS/JS without minification
- No preloading/prefetching strategy
- Checking performance only in phase 5
- No performance budget
- Inline SVGs for complex icons (instead of sprite/component)
```

### ✅ Instead

```markdown
- Dynamic imports for everything > 20KB
- Lazy loading for below-the-fold
- Minification + tree shaking
- Prefetching for likely next routes
- Performance check in phase 3 (early!)
- Lighthouse CI in pipeline
- SVG sprite or icon component
```

---

## References

- `.quinsy-studio/knowledge-base/frontend_playbook.md` — frontend rules
- `.quinsy-studio/process/gates.md` — performance in gate 5
- `./studio gate <project> --performance` — performance check
