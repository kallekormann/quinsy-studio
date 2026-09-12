# Visual storytelling playbook (UX-007)

For homepage, landing, pricing, and in-app workflow explainers. Scan/readability: Krug. Conversion mechanics: [growth-mechanics-playbook.md](growth-mechanics-playbook.md) + Team 11. First-success / peak–end: [delight-playbook.md](delight-playbook.md).

## Always

**Do:** First screen states who it is for, what you get, what to do next. One narrative arc. One primary CTA. Literal headlines (anti-slop). Numbered workflow steps ≤7.

**Don’t:** Metaphor heroes, overlapping badge clouds, autoplay noise, or a storyboard that doesn’t match the live product chrome (LO-0054).

**Fail:** Hero with no next step. Workflow explainer with unlabeled steps. Marketing still that fakes product UI.

## Narrative arc

1. **Setup** — user context, pain
2. **Tension** — what's broken today
3. **Resolution** — product as guide
4. **CTA** — single primary next step

## Marketing page sections (typical)

Hero → social proof → problem → solution → how it works → features → pricing/CTA → FAQ → footer.

Map each section to `ui/page-types/` or organisms from library.

## Workflow explainers

- Step diagram (numbered, ≤7 steps)
- Empty-state narrative when no data
- Onboarding storyboard (frame × frame)

## Product fidelity on marketing (LO-0054)

When a marketing still depicts **board / infinite-canvas / stylescape chrome**:

1. **Mount the real product canvas** (or shared marketing fixtures that feed that component) — do not invent parallel DOM frame chrome that only looks similar.
2. Use public-safe media URLs (`shareInlineUrl` / fixture assets) so marketing does not depend on private board auth.
3. Product CSS/tokens must auto-apply; inventing a second stylescape UI is a process failure.
4. Screenshot DoD: marketing still vs the live product surface it claims to show.

## Handoff

- Storyboard table in design spec
- Alt text strategy for visuals
- `prefers-reduced-motion` notes for any motion
- GM-003 for final copy; UX-006 for brand voice

Agent: `teams/10-product-design-experience/agents/design-visual-storyteller.md`
