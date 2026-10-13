# Persona page set — <product>

Skills GM-007 (message), GD-002 (commercial surface), UX-007 (story), GD-003 (walkthrough). Copy to `projects/<p>/docs/growth/persona-pages.md`. One page per persona from `docs/definitions/02-personas.md`; the generic home page points to them. A feature grid above the fold fails (UX-008 rule 7).

## Set

| Persona | Route | Problem line (their words) | Mechanism line | Proof line | Ask |
|---------|-------|----------------------------|----------------|------------|-----|
| <persona 1> | /for/<slug> | <from 12-positioning.md> | <how the product removes the problem> | <number / quote / demo> | <one CTA> |
| <persona 2> | /for/<slug> | | | | |

## Page structure (every persona page)

1. **Problem** — the first screen states the problem in the persona's words; no product name needed to understand it. Five-second test (GD-003) at 1440 and 390.
2. **Today** — the alternative they use and what it costs them.
3. **Mechanism** — how the product works for this persona, shown in the real UI (mock route or product screenshots), two or three steps.
4. **Proof** — numbers, quotes with permission, or a live demo; each next to the claim it supports.
5. **Articles** — posts from the content engine filtered by `persona` (Payload `posts.persona`).
6. **Ask** — one primary CTA from the message hierarchy; secondary quieter.

## Shared

- Meta title, description, OG text, and the AEO answer block come from the GM-007 hierarchy (same vocabulary as the hero).
- JSON-LD: `WebPage` + `FAQPage` when the answer block is present (GM-002).
- Internal links: home → each persona page; each persona page → pricing (if any) and the two most relevant posts.
- Marketing law (`skill-extensions/marketing-law.md`): comparative claims provable; no invented testimonials.

## Design spec requirements

The design ticket for each page carries §5 Story, §6 Growth intent, the five-second table, the persona walkthrough appendix, and §7b Catalog applied.
