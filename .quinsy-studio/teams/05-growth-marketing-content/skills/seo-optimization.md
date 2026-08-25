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
  - Canonical tags for duplicate content
  - hreflang for multilingual pages
  - No noindex on important pages

URL structure:
  - Short and descriptive
  - Keywords in the slug
  - No parameters in URLs
  - Hyphens instead of underscores
```

### 2. On-page SEO

```markdown
Per page:
  - Title tag: 50-60 characters, main keyword first
  - Meta description: 150-160 characters, call to action
  - H1: once per page, contains the main keyword
  - H2-H6: hierarchical headings
  - Alt texts: descriptive for all images
  - Internal linking: 3-5 internal links per page
  - Schema.org: structured data for rich snippets
```

### 3. Content SEO

```markdown
Content strategy:
  - Pillar pages (main topics, >2000 words)
  - Cluster content (sub-topics, >800 words)
  - Hub & spoke model
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
  - Organization (company)
  - WebSite (with SearchAction)
  - BreadcrumbList
  - FAQPage (for FAQ sections)
  - Product (for e-commerce)
  - Article (for blog)

Validation:
  - Google rich results test
  - Schema.org validator
```

### 5. Link building

```markdown
Strategies:
  - Content marketing (viral content)
  - Guest posting (authoritative blogs)
  - Broken link building
  - HARO (Help A Reporter Out)
  - Partnerships / cross-linking

Rules:
  - Only natural links
  - No link buying
  - Diversify anchor text
  - Relevance > authority
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
```

### ✅ Instead

```markdown
- Natural keyword integration
- Same content for everyone
- Organic link building
- Canonical for duplicates
- Generate an XML sitemap
- Correct robots.txt
```

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

---

## Studio skill extension (affiliate / commercial links)

**Load for affiliate sites and commercial outbound links:**  
[knowledge-base/skill-extensions/affiliate-compliance.md](../../../knowledge-base/skill-extensions/affiliate-compliance.md)

**Adds to GM-001:**
- `rel="noopener noreferrer sponsored"` on commercial outbound links
- Visible affiliate disclosure above the fold
- Internal redirect routes use HTTP 302 (not 301)
- Optional cookieless analytics when avoiding CMP friction
