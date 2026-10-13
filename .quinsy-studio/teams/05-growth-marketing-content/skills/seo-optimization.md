# Skill: SEO Optimization

> Technical SEO, content SEO, schema.org, core web vitals, link building

## Metadata

```
skill_id: GM-001
name: SEO Optimization
team: 05-growth-marketing-content
lead_role: SEO Specialist
support_roles: [Frontend Architect, Content Strategist]
phases: [2, 3, 5, 7]
activation_triggers:
  - Ticket contains "SEO", "visibility", "ranking", "Google"
  - Phase 2: URL structure is defined
  - Phase 3: content architecture
  - Phase 5: SEO audit
  - Phase 7: SEO optimization
  - Ticket words: keyword cannibalization, hreflang, keyword map, title tag
pairs_with: [GM-002, FE-008, FE-003, BE-007]
```

---

## Behavior rules

### 1. Technical SEO

```markdown
Core web vitals (required):
  - LCP < 2.5s
  - INP < 200ms
  - CLS < 0.1

Indexing:
  - robots.txt correct (no important pages blocked!)
  - XML sitemap generated and submitted to Google
  - Self-referencing canonical on every indexable page; cross-canonical only for true duplicates
  - hreflang for multilingual pages (rules in section 7)
  - No noindex on important pages
  - Rendered on the server: core content visible with JavaScript disabled

URL structure:
  - Short and descriptive
  - Keywords in the slug
  - No parameters in URLs
  - Hyphens instead of underscores
```

### 2. On-page SEO

```markdown
Per page:
  - Title tag: unique, primary keyword early, short enough not to be cut
    in the search result preview (Google truncates by pixel width, not a fixed count)
  - Meta description: unique, says what the page answers, ends with the next step
  - H1: once per page, contains the page's primary keyword (from the keyword map)
  - H2-H6: hierarchical headings
  - Alt texts: descriptive for all content images; empty alt for decoration
  - Internal linking: contextual links between pillar and cluster pages; no orphan pages
  - Schema.org: structured data that matches visible content (section 4)

In Payload: title, description, canonical and primary keyword live in the SEO
field group of each collection. Next.js `generateMetadata` reads them; no
hard-coded meta in components.
```

### 3. Content SEO

```markdown
Content strategy:
  - Pillar pages (main topics, full coverage of the intent)
  - Cluster content (one sub-topic and one primary keyword per page)
  - Hub & spoke model
  - Length follows the intent and the pages that rank now, not a word target
  - Internal linking between pillar and cluster

Keyword research:
  - Long-tail keywords for new domains
  - Understand search intent (informational, transactional)
  - Consider keyword difficulty
  - Volume + difficulty = priority
```

### 4. Schema.org

```markdown
Required markups:
  - Organization (company: name, logo, url, sameAs)
  - WebSite (name, url; no SearchAction — Google retired the sitelinks
    search box in November 2024)
  - BreadcrumbList
  - Product with Offer (e-commerce; price matches the visible PAngV total price)
  - Article (blog: author, datePublished, dateModified)

Optional, no snippet promise:
  - FAQPage on real FAQ sections. Since August 2023 Google shows FAQ rich
    results only for well-known, authoritative government and health sites.
    The markup may still help machines read Q&A pairs (GM-002). Never promise
    a client FAQ snippets.
  - HowTo: Google no longer shows HowTo rich results (2023). Use only if
    another consumer needs it.

Rules:
  - Markup describes content visible on the page; nothing hidden
  - JSON-LD generated from Payload fields, not typed by hand

Validation:
  - Google Rich Results Test (for types Google still supports)
  - Schema.org validator
```

### 5. Link building

```markdown
Strategies:
  - Linkable assets (original data, tools, reference guides)
  - Digital PR and expert commentary (GM-005 press rules)
  - Broken link reclamation and unlinked brand mentions
  - Partnerships with relevant sites

Rules:
  - Only natural links
  - No link buying, no link exchanges at scale, no paid guest posts without
    rel="sponsored" (Google spam policies; paid links are also advertising
    that must be labelled under § 5a(4) UWG)
  - Diversify anchor text
  - Relevance > authority
```

### 6. Keyword cannibalization protocol

Two of our pages competing for the same query split clicks and confuse
ranking. Run this before any title, H1, meta or content change on an
existing page, and before a new page targets a keyword.

```markdown
1. Keyword map first
   - `docs/growth/keyword-map.md`: one row per URL — primary keyword,
     intent, role (pillar / cluster / product / landing), owner page for
     secondary terms.
   - One primary keyword belongs to one URL. A title or H1 never uses a
     primary keyword owned by another URL.
   - Checkable: the Payload SEO group has a `primaryKeyword` field with a
     validation hook that refuses a value already used by another
     published document (any collection, same locale).

2. Cross-page query check (with Search Console)
   - Performance report, dimensions page + query, filtered on the target
     keywords, last 3 months.
   - Conflict = two or more of our URLs get impressions for the same query
     and both rank in the top 20 with split clicks.

3. Fallback without Search Console (new site, no access yet)
   - List every URL from sitemap.xml whose title, H1 or body targets the
     keyword. Two URLs with the same primary keyword in title + H1 = conflict.
   - The homepage is the usual hidden cannibal: give it its own keyword and
     let it link out to the dedicated page.

4. Resolve, one owner per query
   - Owner = the URL with the closest intent match; tie → most clicks.
   - Merge thin duplicates into the owner and 301-redirect the old URL
     (Payload redirects collection or next.config redirects).
   - Or rewrite the non-owner's title/H1 to a distinct long-tail angle.
   - Add a contextual link from the non-owner to the owner.
   - Canonical stays self-referencing unless the pages are true duplicates.

5. Record
   - Update the keyword map; note the conflict and the fix in the ticket receipt.
```

### 7. hreflang rules (pair with FE-008 i18n)

```markdown
- One URL per language version. Never serve two languages on one URL by
  cookie or Accept-Language.
- Every language version lists all versions, including itself.
  Annotations must be reciprocal; Google ignores a one-way pair.
- Codes: ISO 639-1 language, optional ISO 3166-1 alpha-2 region
  (`de`, `de-AT`, `de-CH`, `en`). Region alone is invalid.
- Add `x-default` pointing to the language picker or the default locale.
- Canonical points to the same-language URL. Never canonicalise a German
  page to the English one.
- `<html lang>` matches the page's locale (set per locale layout).
- Only list locales that have published, translated content. A Payload
  locale that falls back to the default language is not a translation:
  no hreflang entry, and no sitemap entry, for that locale.
- Generate from data: Next.js `generateMetadata` → `alternates.languages`
  built from the Payload document's published locales, or sitemap
  `xhtml:link` alternates. No hand-typed hreflang tags.
- Check: crawl one URL per locale and confirm each lists the same set.
```

---

## Anti-patterns

### ❌ Forbidden

```markdown
- Keyword stuffing
- Cloaking (different content for Google)
- Link buying
- Duplicate content without canonical
- No sitemap
- robots.txt blocks important pages
- Promising FAQ or HowTo rich snippets
- Two pages with the same primary keyword in title and H1
- hreflang to an untranslated fallback locale; one-way hreflang
- Cross-language canonicals
```

### ✅ Instead

```markdown
- Natural keyword integration
- Same content for everyone
- Organic link building
- Canonical for duplicates
- Generate an XML sitemap
- Correct robots.txt
- FAQ markup as machine-readable extra, no snippet promise
- Keyword map with one owner per primary keyword
- Reciprocal hreflang generated from published Payload locales
```

---

## Done evidence (receipt)

- Keyword map row for every page the ticket touched; cannibalization check
  result (GSC export or sitemap fallback) with "no conflict" or the fix.
- Rich Results Test or schema validator output for each JSON-LD type added.
- Multilingual tickets: crawl output showing reciprocal hreflang and matching
  `lang` for each locale.

---

## External skill support

> Before implementation load the imported best-in-class skills (`./studio update-skills`):

- **`marketing_aeo/skills/seo-audit`** (coreyhaines31/marketingskills) — complete SEO audit workflow. **Primary source for audits.**
- **`marketing_aeo/skills/schema`** — structured data / schema.org markup
- **`marketing_aeo/skills/programmatic-seo`** — pSEO architecture (programmatic pages, templates)
- **`marketing_aeo/skills/site-architecture`** — URL/site architecture, internal linking
- **`marketing_aeo/skills/customer-research`** — keyword matrices, search intent, audience research

Flow: read `seo-audit` → check the pSEO architecture → add schema → apply link-rot prevention.

## References

- `.quinsy-studio/knowledge-base/frontend_playbook.md` — core web vitals
- `.quinsy-studio/knowledge-base/design_playbook.md` — UX for SEO
- Google Search Central: structured data gallery; "Changes to HowTo and FAQ rich results" (August 2023); hreflang documentation; spam policies
- Source for sections 6–7: agency-agents `marketing/marketing-seo-specialist.md` (MIT)

---

## Studio skill extension (affiliate / commercial links)

**Load for affiliate sites and commercial outbound links:**  
[knowledge-base/skill-extensions/affiliate-compliance.md](../../../knowledge-base/skill-extensions/affiliate-compliance.md)

**Adds to GM-001:**
- `rel="noopener noreferrer sponsored"` on commercial outbound links
- Visible affiliate disclosure above the fold
- Internal redirect routes use HTTP 302 (not 301)
- Optional cookieless analytics when avoiding CMP friction
