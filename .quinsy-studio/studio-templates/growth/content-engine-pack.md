# Content engine pack — <product>

Skills GM-003 (content strategy), GM-007 (message spine), GM-001 / GM-002 (findability), BE-007 (Payload), AI-001 (LLM calls). Copy to `projects/<p>/docs/growth/content-engine.md`. Milestone coverage area `content`. The engine produces drafts; a named reviewer publishes.

## Spine

- **Core message** (from `docs/definitions/12-positioning.md`): every piece supports it.
- **Pillars** (3–5): one per persona problem; each pillar has a category in Payload.
- **Cadence**: <n> posts / week; what is generated, what is human-written.

| Pillar | Persona | Problem it serves | Category slug | Formats |
|--------|---------|-------------------|---------------|---------|
| <pillar> | <persona> | <problem line> | <slug> | how-to, comparison, answer page |

## Pipeline (Payload `posts`, `source` field)

1. **Topic queue** — a Payload collection or a `topics` field group: question, persona, pillar, target query, status. Fed by: support questions, search console queries, the push-back log for the persona page, competitor gaps.
2. **Draft** — a Payload job calls the LLM (AI-001; model name from `env.schema.json`, value from `.env`) with the message spine, the persona block, the pillar, and the answer-block rule. Writes `posts` with `status: draft`, `source: generated`.
3. **Review** — the content strategist (human or agent in a review context) checks: on-message, provable claims, marketing law, no banned vocabulary (UX-008 list), answer block ≤ 60 words, author set. Flip `source` to `assisted` after edits.
4. **Publish** — `status: published` revalidates the post, category, persona page, sitemap, and feed.
5. **Measure** — impressions and clicks per post (Search Console API) and AEO citations (manual sample) into `docs/growth/content-metrics.md` monthly; PM-002 reads it at the milestone review.

## Rules

- Generated text never publishes without the review step; the job cannot set `status: published`.
- Every post names a real author (E-E-A-T) and carries the persona and pillar.
- Comparison posts follow `skill-extensions/marketing-law.md` (UWG § 6).
- Internal links: each post links its persona page and one sibling post; persona pages list their posts.
- No scraped or reprinted third-party text; sources are cited.
- Notification of new posts (newsletter) goes through GM-006 with opt-in.

## Receipt lines

```markdown
## Growth
- GM-003: pillars + cadence — docs/growth/content-engine.md
- BE-007: posts/categories collections with access rules — apps/web/src/collections/Posts.ts
- AI-001: draft job writes status=draft only — <job file path>; test <path>
- GM-002: answer group rendered as FAQPage — <component path>
```

## Anti-patterns

- An LLM job that publishes directly.
- Posts without persona or pillar ("general").
- A blog that does not link back to the persona page or product.
- Topic choice by keyword volume alone, ignoring the persona problem.
