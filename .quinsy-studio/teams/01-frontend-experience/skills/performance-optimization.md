# Skill: Performance (FE-003)

> Fast pages on a real phone, measured against the published Core Web Vitals, without ever serving one user's page to another. Next.js App Router on Payload: Server Components by default, sized images, self-hosted fonts, bounded lists. Measure the ticket's primary view before and after. The gate budget is soft; the private-page rule is not.

## Metadata

```
skill_id: FE-003
name: Performance
team: 01-frontend-experience
lead_role: Frontend Architect
support_roles: [QA Specialist, Backend Engineer]
phases: [4, 5]
activation_triggers:
  - Ticket contains "Performance", "Load Time", "Speed", "Bundle", "Core Web Vitals", "LCP", "INP", "CLS"
  - Ticket adds images, fonts, third-party scripts, caching or a long list
  - Soft perf_budget warning from gate 5
pairs_with: [FE-006, BE-002, BE-007, CL-002, PE-001]
```

## When to load

- A ticket that changes a public page, a list, an image pipeline, fonts, caching or third-party scripts.
- A soft `perf_budget` warning on gate 5.
- Before a launch, on the landing and the core job routes.

## Rules

### 1. Use the published thresholds only

Core Web Vitals, "good" at the 75th percentile of page loads (web.dev):

| Metric | Good | Measures |
|--------|------|----------|
| LCP | ≤ 2.5 s | Largest Contentful Paint |
| INP | ≤ 200 ms | Interaction to Next Paint |
| CLS | ≤ 0.1 | Cumulative Layout Shift |

INP replaced FID in March 2024. Ignore FID rows in older docs. Do not invent other thresholds. Lab numbers (Lighthouse, mobile preset) are a proxy before launch. Field data at p75 is the verdict after launch.

### 2. Measure a production build

Measure with `next build` and `next start` in Compose, not `next dev`. Use the Lighthouse mobile preset on the ticket's primary view. Record before and after. A change with no before number is not an optimisation.

### 3. Never cache a private page

A page or response that depends on the signed-in user, a cookie, a cart or an account is never stored in a shared cache.

- Authenticated routes read the session (`cookies()`, Payload `auth`), so they render dynamically. Do not force them static with `export const dynamic = 'force-static'` or `revalidate`.
- Do not wrap user-specific Payload queries in `unstable_cache`, `'use cache'` or a `fetch` with `cache: 'force-cache'` or `next: { revalidate }`.
- Authenticated HTML and `/api/*` responses carry `Cache-Control: private, no-store` (or Next's dynamic default). Check with `curl -I` and a session cookie on dev.
- `/admin`, `/api`, cart, checkout and account routes are excluded from any proxy or CDN cache in Coolify.

One user seeing another user's data is a breach (CL-001), not a speedup. This is an automatic fail in SO-005.

### 4. Cache public content on purpose

Public Payload pages may use static rendering or time-based revalidation. After a write, revalidate from a Payload `afterChange` hook on the server with `revalidatePath` or `revalidateTag`. Never call a revalidation secret from a `'use client'` module.

### 5. Images

- Use `next/image` with `width` and `height`, or `fill` with `sizes`. No dimensionless images.
- Serve Payload upload `imageSizes`, not the original file.
- Mark the LCP image as priority (the `priority` prop; check the prop name for the project's Next version). Never lazy-load it. Everything below the fold stays lazy.
- AVIF or WebP through the Next image optimizer.

### 6. Fonts

- Self-host with `next/font/local`. No `next/font/google` and no `fonts.googleapis.com` link on pre-auth pages. Loading Google Fonts from Google's servers sends the visitor's IP address to Google (LG München I, 20 Jan 2022, 3 O 17493/20).
- Limit families and weights to what `design/DESIGN.md` names. Subset when the font allows it.
- `display: 'swap'`. `next/font` adjusts fallback metrics, which keeps CLS low.

### 7. JavaScript

- Server Components by default. Put `'use client'` on the smallest leaf that needs state or events.
- Load heavy client widgets (editors, charts, maps) with `next/dynamic`.
- Third-party scripts use `next/script` with `lazyOnload` or `afterInteractive`, and only after consent where CL-002 requires it.
- Keep event handlers short. Move heavy updates into `useTransition`. A long task on click is an INP problem.
- Check the bundle with `@next/bundle-analyzer` when a ticket adds a dependency.

### 8. Bounded data

- No unbounded client lists. Paginate with Payload `limit` and `page`, or virtualise long lists.
- Set Payload `depth` to what the view renders and use `select` for wide collections.
- Query indexes belong to BE-002.

### 9. Layout stability

Reserve space for images, embeds, ads and async banners. A skeleton has the size of the content it replaces. The cookie banner overlays the page; it does not push content down.

### 10. Soft budget: `perf_budget`

The planned gate check runs a lab measure on the smoke routes and warns when LCP, CLS or the total blocking time gets worse. It does not block `MOVE_DONE`. Record the numbers and the reason when you accept a warning.

## Workflow

1. Name the primary view and its LCP element.
2. Measure the production build before the change (Lighthouse mobile).
3. Apply the rules that the change touches.
4. Check the cache headers of every authenticated route the ticket touches.
5. Measure again. Compare. Rerun the default-flow test (FE-006). A faster page with a broken menu is a regression.
6. Fill the receipt `## Evidence`.

## Deliverables

- Before and after numbers for the primary view.
- Cache-header proof for authenticated routes.
- Image and font config in `next.config.mjs` and the root layout.

## Done evidence (receipt)

```markdown
## Evidence
- Performance (lab, Lighthouse mobile, production build) /pricing: LCP 3.1 s → 2.2 s · CLS 0.18 → 0.02 · PASS
- LCP element: hero image, priority, Payload size "hero"
- Private-page cache: /account `Cache-Control: private, no-cache, no-store` with session · PASS
- Fonts: next/font/local only, no googleapis requests · PASS
- perf_budget: no warning | warning accepted (reason)
```

Results are PASS, FAIL or NOT TESTED.

## Anti-patterns

- Measuring `next dev` on a fast laptop and calling it done.
- `revalidate` on a page that reads the session.
- A CDN rule that caches all HTML.
- `loading="lazy"` on the hero image.
- Google Fonts from Google's CDN.
- `'use client'` at the top of a page "to make it work".
- Fetching a whole collection to show ten rows.
- Unsourced claims such as "every second costs 7 % conversion".

## Handoff

- **To BE-002:** slow queries and missing indexes.
- **To PE-001:** proxy and CDN cache rules in Coolify.
- **To SO-005:** the private-page cache check runs on dev.
- **To CL-002:** third-party scripts that need consent.

## References

- [Core Web Vitals thresholds](https://web.dev/articles/vitals) · [INP](https://web.dev/articles/inp)
- [Next.js caching](https://nextjs.org/docs/app/building-your-application/caching) · [next/image](https://nextjs.org/docs/app/api-reference/components/image) · [next/font](https://nextjs.org/docs/app/api-reference/components/font)
- [frontend_playbook.md](../../../knowledge-base/frontend_playbook.md) — Performance, pre-auth fonts (LO-0134)
- [payload-playbook.md](../../../knowledge-base/payload-playbook.md)
- Source: msitarzewski/agency-agents `testing/testing-performance-benchmarker.md`, `engineering/engineering-wordpress-performance.md` (MIT), rules only
