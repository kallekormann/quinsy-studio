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
For every important page:
  - 3-5 frequent questions
  - Clear, direct answers
  - FAQPage schema.org markup
  - Derive questions from "People Also Ask"
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
```

---

## Anti-patterns

### ❌ Forbidden

```markdown
- Only continuous prose without structure
- No sources for claims
- No tables for comparisons
- Outdated content
- No FAQ sections
```

### ✅ Instead

```markdown
- Structured content with lists/tables
- Sources for every claim
- Comparison tables for features
- Regular updates
- FAQ with schema.org markup
```

---

## External skill support

> Before implementation load the imported best-in-class skills (`./studio update-skills`):

- **`marketing_aeo/skills/ai-seo`** (coreyhaines31/marketingskills) — complete AEO workflow: being cited in AI search results and LLM answers. **Primary source for this skill.**
- **`marketing_aeo/skills/schema`** — structured data / JSON-LD / schema.org markup for AI visibility
- **`geo_visibility/SKILL.md`** (bloomprotocol) — AI visibility audit, llms.txt, comparison page generator
- **`marketing_aeo/skills/competitors`** — comparison/alternative pages (`/alternatives-to/`)

Flow: read `ai-seo` → apply the audit points → add schema markup → check llms.txt.

## References

- `.quinsy-studio/knowledge-base/design_playbook.md` — content structure
- `.quinsy-studio/knowledge-base/frontend_playbook.md` — schema.org
