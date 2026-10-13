# SEO + AEO foundation pack — <product>

Skills GM-001 (SEO), GM-002 (AEO), BE-007 (Payload). Copy to `projects/<p>/docs/growth/seo-foundation.md`. This is the milestone coverage area `seo` — one ticket pack, shipped before the first public page is announced.

## Checklist

| Item | Where | Owner | Done |
|------|-------|-------|------|
| Canonical URLs, trailing-slash policy, `www` redirect | Next config + Coolify proxy | GM-001 / PE-001 | |
| `robots.txt` with sitemap line; staging disallowed | `app/robots.ts` | GM-001 | |
| `sitemap.xml` from Payload collections (pages, posts, categories, persona pages) | `app/sitemap.ts` | GM-001 / BE-007 | |
| Meta title + description per page from `seo` group (`@payloadcms/plugin-seo`) | Payload config | GM-001 | |
| Open Graph + Twitter cards, generated OG image route | `app/og/route.tsx` | GM-001 / UX-005 | |
| JSON-LD: `Organization`, `WebSite`, `Article`, `FAQPage`, `Product`/`Offer` where priced | layout + page components | GM-001 / GM-002 | |
| `llms.txt` and `llms-full.txt` describing the product and linking the answer pages | `public/llms.txt` | GM-002 | |
| Answer blocks: question + ≤60-word answer on persona pages and posts (`posts.answer`) | Payload `answer` group | GM-002 / GM-007 | |
| RSS / Atom feed for posts | `app/feed.xml/route.ts` | GM-003 | |
| Redirects collection so slug changes never 404 | `@payloadcms/plugin-redirects` | BE-007 | |
| Core Web Vitals budget: LCP < 2.5 s, INP < 200 ms, CLS < 0.1 on persona pages at 390 | Lighthouse / web-perf run | FE-003 | |
| Image pipeline: sized, lazy, `alt` from Payload | upload collection | FE-003 / FE-004 | |
| Analytics with consent (CL-002); no tracking before consent | consent component | CL-002 | |
| Search Console + Bing Webmaster verified; sitemap submitted | ops log | GM-001 | |

## Receipt lines

```markdown
## Growth
- GM-001: sitemap.xml lists <n> URLs — curl https://<domain>/sitemap.xml
- GM-001: JSON-LD valid — <validator output path>
- GM-002: llms.txt present — https://<domain>/llms.txt
- GM-002: answer block on /for/<persona> — docs/design-specs/<TICKET>.md
- FE-003: CWV at 390 within budget — <lighthouse report path>
```

## Anti-patterns

- Keyword-stuffed titles that differ from the hero message (GM-007 says the same thing everywhere).
- A sitemap that lists drafts or staging URLs.
- AEO answers copied from the meta description.
- Tracking scripts before consent.
