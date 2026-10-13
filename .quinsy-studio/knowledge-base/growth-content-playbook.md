# Growth content playbook (Teams 05 + 11, with Team 10)

Operational rules for **how a product is explained and found**: positioning, persona pages, SEO and AEO foundation, and the content engine. Companion to `growth-mechanics-playbook.md` (commercial surfaces and in-product loops). Skills: GM-007, GM-001, GM-002, GM-003, GD-002, GD-003, GD-004, UX-007, UX-008.

Sources (distilled, not reprinted): April Dunford positioning; NN/g on landing pages and content; Google Search Essentials; schema.org; the studio anti-slop rules. Anti-slop wins over "clever" copy.

## 1. Positioning first (GM-007)

- `docs/definitions/12-positioning.md` is a gate-0 requirement. Audience, problem in their words, alternative today, category, the one difference, proof, core message, message hierarchy per persona.
- One core message, repeated verbatim across hero, meta, OG, store listing, first email, and AEO answer.
- A message change on a live surface is a GD-001 hypothesis with a GD-003 five-second test before and after.

## 2. Problem-first pages (GM-007 + GD-002 + UX-007)

Order on every public page: **problem → today's alternative → mechanism → proof → ask**. A feature grid above the fold fails (UX-008 rule 7).

- Multi-persona products get one page per persona (`studio-templates/growth/persona-page-set.md`); the home page routes to them.
- Mechanism is shown in the real UI (mock route or product screenshots), never stock illustration.
- Proof sits next to the claim it supports. Claims map to a proof list; marketing law applies (`skill-extensions/marketing-law.md`).
- Five-second test at 1440 and 390 on the first screen; persona walkthrough appendix on commercial packets.

## 3. SEO + AEO foundation (GM-001 + GM-002)

One pack, shipped before the first public page is announced: `studio-templates/growth/seo-foundation-pack.md`.

- Canonicals, robots, sitemap from Payload collections, meta from `plugin-seo`, OG images, JSON-LD per page type, `llms.txt`, RSS, redirects, CWV budget at 390, consent-gated analytics.
- AEO: a question and a ≤60-word answer on persona pages and posts (`posts.answer`), rendered as `FAQPage`; the answer is not the meta description.
- Titles and descriptions use the GM-007 vocabulary. Keyword stuffing that drifts from the core message fails review.

## 4. Content engine (GM-003 + BE-007 + AI-001)

`studio-templates/growth/content-engine-pack.md` and the Payload `posts` model in `payload-playbook.md`.

- Pillars map to persona problems; every post carries persona, pillar, author, and the answer block.
- Generated drafts stay `draft` until a reviewer publishes. The job cannot publish. Marketing law and the banned-vocabulary list apply to every published post.
- Measure impressions, clicks, and AEO citations monthly; PM-002 reads the numbers at the milestone review.

## 5. In-product loops (GD-004)

Live in `growth-mechanics-playbook.md § In-product loops` and `studio-templates/growth/growth-loop-map.md`. Content and pages feed the loop's receiver surface; the loop feeds content with real usage stories (with permission).

## 6. Milestone coverage

The coverage areas `positioning`, `seo`, `growth`, `content`, and `launch` in `milestone-coverage-checklist.md` map to sections 1–5 here plus `launch-playbook.md`. A public web product's roadmap names a milestone for each or states `none — reason`.

## Spec and receipt fail lines

- Public page without a GM-007 message block in §5 / §6.
- Hero that lists features.
- Claim without a proof line.
- Public page shipped before the SEO pack exists.
- Generated post published without a reviewer.
- Different taglines on site, listing, and first email.
