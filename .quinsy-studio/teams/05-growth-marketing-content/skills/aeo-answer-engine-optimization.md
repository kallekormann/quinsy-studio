# Skill: AEO (Answer Engine Optimization)

> Optimization for AI search engines, structured data, citable content

## Metadata

```
skill_id: GM-002
name: Answer Engine Optimization (AEO)
team: 05-growth-marketing-content
lead_role: SEO Specialist
support_roles: [Content Strategist, Frontend Engineer]
phases: [3, 5, 7]
activation_triggers:
  - Ticket contains "AEO", "AI search", "ChatGPT", "Perplexity"
  - Phase 3: content is optimized for AEO
  - Phase 5: AEO audit
  - Phase 7: AEO optimization
  - Ticket words: ai crawler policy, llms.txt, robots.txt GPTBot, citation audit
pairs_with: [GM-001, BE-007, FE-003, CL-003]
```

---

## Behavior rules

### 1. Structured data for LLMs

```markdown
LLMs extract:
  - Tables (markdown/HTML)
  - Lists (numbered and unnumbered)
  - Definitions (clear terms)
  - Comparisons (side-by-side)
  - FAQ sections

Formatting:
  - Clear headings (H2, H3)
  - Bullet points for enumerations
  - Tables for comparisons
  - Code blocks for technical content
```

### 2. Citable answers

```markdown
Every main claim:
  1. Direct answer (1-2 sentences)
  2. Detailed explanation
  3. Source / reference
  4. Example

Structure:
  "Yes/No/Fact. [Detailed explanation].
   According to [source], [specific value/fact]."
```

### 3. FAQ optimization

```markdown
For pages where users really ask questions:
  - The questions users ask (support inbox, search queries, "People Also Ask")
  - Clear, direct answers, visible on the page
  - FAQPage markup is optional: it can help machines read Q&A pairs, but
    Google shows FAQ rich results only for authoritative government and
    health sites since August 2023. No snippet promise (see GM-001 §4).
```

### 4. Comparison tables

```markdown
For product/feature comparisons:
  - Markdown tables
  - Clear column headings
  - Feature vs. feature
  - Price vs. price

Example:
  | Feature | Free | Pro | Enterprise |
  |---------|------|-----|------------|
  | Users   | 1    | 10  | Unlimited  |
  | Storage | 1GB  | 10GB| 100GB      |
```

### 5. Authority signals

```markdown
For LLM rankings:
  - Author bio with expertise
  - Citations and references
  - Freshness (update the date)
  - Build domain authority
  - Brand mentions
  - Consistent entity: same brand and product names everywhere;
    Organization schema with sameAs links to official profiles
```

### 6. AI crawler policy (a recorded decision, not a default)

Foundations come before citation work. An old robots.txt that blocks every
AI crawler by accident is the most common failure; blocking on purpose is a
valid business choice. Present the options, let the human decide, record it.

```markdown
Decision record: `docs/growth/ai-crawler-policy.md`
  - One row per user agent: allow / disallow, purpose, reason, date, decided by
  - Separate training crawlers from search and user-fetch agents
  - Re-check operator docs at least each quarter; agents change

Known agents (verify on each operator's docs page when writing the record):
  | Operator   | Training      | Search index        | User-triggered fetch |
  |------------|---------------|---------------------|----------------------|
  | OpenAI     | GPTBot        | OAI-SearchBot       | ChatGPT-User         |
  | Anthropic  | ClaudeBot     | Claude-SearchBot    | Claude-User          |
  | Perplexity | —             | PerplexityBot       | Perplexity-User      |
  | Google     | Google-Extended (product token, Gemini) | Googlebot (also AI Overviews) | — |
  | Apple      | Applebot-Extended (token) | Applebot  | —                    |
  | Common Crawl | CCBot       | —                   | —                    |

Rules:
  - Blocking Google-Extended does not remove the site from Google Search or
    AI Overviews; only blocking Googlebot does that (and kills SEO).
  - User-triggered fetchers may not follow robots.txt; operators say so.
    robots.txt is a request, not access control. Hard blocks need the WAF
    (Cloudflare) and are a separate decision.
  - Text-and-data-mining reservation (§ 44b(3) UrhG) must be machine-readable
    for online content. If the business reserves TDM rights, state it in
    robots.txt (disallow training agents) and in the terms (CL-003).
  - One source of truth: Next.js `app/robots.ts` builds the rules from the
    decision record (or a Payload global holding it). No hand-edited
    `public/robots.txt` alongside it.
  - Check: fetch `/robots.txt` on production and diff against the record.
```

### 7. llms.txt generated from Payload

`llms.txt` is a community proposal (llmstxt.org), not a standard. There is
no public evidence that major answer engines rank by it. Build it because it
is cheap when generated, never hand-maintained.

```markdown
Route: `app/llms.txt/route.ts` (and optional `app/llms-full.txt/route.ts`)
Format (per llmstxt.org):
  # <Site name>
  > <one-line summary: what it is, for whom>
  ## <Section, e.g. Product, Docs, Pricing, Guides>
  - [Title](absolute URL): one-line description

Content:
  - Query Payload's Local API for published documents only:
    `draft: false`, `overrideAccess: false`, no user (public access rules apply)
  - Skip documents marked noindex, private, gated or with a fallback locale
  - Title and description come from the SEO field group
  - Sections follow the site's information architecture (keyword map roles)

Freshness:
  - `afterChange` / `afterDelete` hooks on public collections call
    `revalidatePath('/llms.txt')`; no stale links after a publish
  - Optional: `.md` route per page from the same content for clean ingestion

Check: a test asserts every URL in llms.txt returns 200 and is indexable,
and that no draft or private document appears.
```

### 8. Citation audit routine

AI answers are non-deterministic. Say "improve citation likelihood", never
"get cited". Measure before and after.

```markdown
1. Prompt set: buyer-language prompts in `docs/growth/citation-audit/prompts.md`,
   grouped by intent: recommendation ("best X for Y"), comparison ("X vs Y"),
   how-to, definition. Include German prompts for German markets.
2. Baseline run: each prompt on ChatGPT, Claude, Gemini, Perplexity and
   Google AI Overviews. Logged-out or fresh session; record date, model,
   language. Run each prompt more than once; record every result.
3. Record per answer: are we mentioned, which URL is cited, which
   competitors are cited and with which page.
4. Lost prompts: table of prompts where competitors are cited and we are
   not, with the page type that wins (comparison page, FAQ, docs, review).
5. Fix pack: missing pages or sections, entity consistency, crawler access
   (section 6), structure (sections 1–4). Each fix becomes a ticket.
6. Recheck: same prompts after the fixes are live and recrawled; compare
   with the baseline file. Report counts, not invented percentages.
Store each run as `docs/growth/citation-audit/YYYY-MM-DD.md`.
```

---

## Anti-patterns

### ❌ Forbidden

```markdown
- Only continuous prose without structure
- No sources for claims
- No tables for comparisons
- Outdated content
- Legacy robots.txt blocking AI agents nobody decided to block
- Hand-maintained llms.txt pointing to dead or draft pages
- Promising citations or FAQ snippets
- Single-platform, single-run citation "audits"
```

### ✅ Instead

```markdown
- Structured content with lists/tables
- Sources for every claim
- Comparison tables for features
- Regular updates
- Visible FAQ answers; FAQPage markup as an optional extra
- Crawler policy recorded per agent and rendered by `app/robots.ts`
- llms.txt generated from published Payload content
- Baseline and recheck runs stored with date and model
```

---

## Done evidence (receipt)

- `docs/growth/ai-crawler-policy.md` exists; production `/robots.txt` matches it (diff output).
- `/llms.txt` returns 200; test proves every listed URL is published and indexable.
- Citation audit tickets: baseline file and recheck file paths, lost-prompt table.

---

## External skill support

> Before implementation load the imported best-in-class skills (`./studio update-skills`):

- **`marketing_aeo/skills/ai-seo`** (coreyhaines31/marketingskills) — complete AEO workflow: being cited in AI search results and LLM answers. **Primary source for this skill.**
- **`marketing_aeo/skills/schema`** — structured data / JSON-LD / schema.org markup for AI visibility
- **`marketing_aeo/skills/competitors`** — comparison/alternative pages (`/alternatives-to/`)

Flow: read `ai-seo` → apply the audit points → add schema markup → check llms.txt.

## References

- `.quinsy-studio/knowledge-base/design_playbook.md` — content structure
- `.quinsy-studio/knowledge-base/frontend_playbook.md` — schema.org
- llmstxt.org (proposal by Jeremy Howard, 2024); operator crawler docs (OpenAI, Anthropic, Perplexity, Google, Apple)
- § 44b UrhG (text and data mining reservation)
- Source for sections 6–8: agency-agents `marketing/marketing-aeo-foundations.md`, `marketing/marketing-ai-citation-strategist.md` (MIT), invented scores and targets removed
