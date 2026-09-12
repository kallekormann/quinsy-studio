# Design canon ledger (Teams 10 / 11 / 05)

How design knowledge enters Quinsy: **cite a source → distill into Do / Don’t / spec-fail** in a playbook → **CARD-load** the matching skill. Do not paste book chapters into git. Desk copies the human owns, public guidelines, and professional practice are all valid input.

## Three craft teams

| Team | Owns | Does not own |
|------|------|----------------|
| **10 Product Design & Experience** | What it is and why: IA, flow, interaction, visual, brand, atomic, UI writing. On commercial surfaces, **growth mechanics as design constraints**. | Experiment backlog; SEO crawl plan; random hero variants |
| **11 Growth Design** | Hypothesis, primary metric (or falsifiable claim), experiment design, variant *intent*, commercial-pattern mechanics (pricing, checkout, catalog, PDP) | Visual system, new atoms, IA home surface |
| **05 Growth, Marketing & Content** | SEO, AEO, editorial/marketing copy at volume | Pixel layout of a pricing table; inventing checkout |

**Lead on a design-track ticket stays Team 10.** Team 11 skills are **appended** on commercial surfaces so `team_for_skills` does not steal the ticket.

**Pairing:** if the surface is a funnel (landing, pricing, checkout, PLP, PDP), Team 10 loads [growth-mechanics-playbook.md](growth-mechanics-playbook.md). Team 11 fills **spec Growth intent** (§6). Team 05 only if the URL is public (SEO/AEO). Do not A/B a broken IA — that is UX-003.

**When the situation needs it:** conversion complaint, new money surface, or “we should test this” → Team 11 writes 1–3 claims **with** the spec. No variant without a claim. Dark patterns (fake scarcity, hidden total) are HITL / legal, not growth.

## Topic → owner

| Cluster | 10 | 11 | 05 |
|---------|-----|----|-----|
| Vision, concept, prototyping | Gate 2 + spec §1 | — | — |
| IA, user-flow, workflow, service | UX-001/002/003 | Marks funnel steps | Crawl URLs |
| Interaction, usability, forms | UX-002 | Checkout/form as conversion | — |
| Visual, layout, color, atomic, brand | UX-005/006 | CTA hierarchy, not a new palette | — |
| UI writing | UX-002/006 | CTA / offer framing | Campaign copy |
| Landing / pricing / checkout / PLP / PDP | UX-007 + growth playbook | **Growth intent §6 + GD-001/002** | Public URL SEO/AEO |
| SEO / AEO | Voice from UX-006 | Message tests | **Lead** |
| A/B | Ships the control on-system | Hypothesis, metric, stop rules | Analytics after |
| Original logo mark | Human HITL | — | — |
| **Delight** | Infused UX-001/002/003/005/007 — [delight-playbook.md](delight-playbook.md) | Peak–end on buy; no dark-pattern “excitement” | — |

## Surface class (CARD)

| Class | Examples | Load |
|-------|----------|------|
| `product-app` | Settings, canvas, operator table | Team 10 only |
| `commercial-web` | Landing, pricing page/table, checkout, cart, PLP, PDP | Team 10 + GD-001 + GD-002 + growth playbook |

## Canon (distill, cite, do not reprint)

**Team 10 — product / UX / visual**

| Source | Feeds |
|--------|--------|
| Nielsen 10 usability heuristics (NN/g; credit Nielsen) | UX-002, `design-science-playbook` |
| Garrett *Elements of UX* | Gate 2 + UX-001 (strategy before surface) |
| Cooper *About Face* | UX-001/002 (states, posture, errors) |
| Indi Young *Mental Models* | UX-004 |
| Wroblewski *Web Form Design* | UX-002 |
| Rosenfeld / Morville IA | UX-003 |
| Krug *Don't Make Me Think* | UX-002, UX-007 |
| Brad Frost atomic design | `atomic-design-playbook` |
| WCAG / W3C POUR | UX-005 + FE-004 |
| Apple HIG + Material 3 *foundations* (grammar, not clone) | UX-002/005 |
| Laws of UX (Yablonski) as psychology index | UX-002/005 |
| Stickdorn / Lou Downe *Good Services* | UX-001 when the product is a multi-touch service |

**Teams 10+11 — commercial mechanics** (see growth playbook)

NN/g landing & ecommerce; Baymard checkout/list/PDP principles; ethics-bounded persuasion (clear offer, proof beside claim, one primary action, honest recommended plan, total cost before pay). Team 11: one change, one metric (or falsifiable claim), kill criteria.

**Team 05** — existing GM-001–003 + subscribed marketing/AEO packs. Not a substitute for Team 11.

## Infusion rule

1. Add or patch a **playbook section** (operational).
2. Point the **thin skill** at it.
3. Wire `ticket_type` / commercial triggers so the CARD lists the playbook.
4. Prefer a **spec-fail line** over a new skill ID. **Do not** add UX-009 Delight — it would only run when tagged; delight must ride on every design CARD via UX-002.

## Team 10 playbooks (Do / Don’t / fail)

| Skill | Playbook |
|-------|----------|
| UX-001 | [product-ux-playbook.md](product-ux-playbook.md) |
| UX-002 | [interaction-ux-playbook.md](interaction-ux-playbook.md) |
| UX-003 | [contextual-ia-playbook.md](contextual-ia-playbook.md) |
| UX-004 | [ux-research-playbook.md](ux-research-playbook.md) |
| UX-005 | [design-science-playbook.md](design-science-playbook.md) |
| UX-006 | [brand-guardian-checklist.md](brand-guardian-checklist.md) |
| UX-007 | [visual-storytelling-playbook.md](visual-storytelling-playbook.md) |
| Atomic | [atomic-design-playbook.md](atomic-design-playbook.md) |
| **All 10 + 11** | [delight-playbook.md](delight-playbook.md) — **not** a separate skill ID |

CARD loads these via `playbooks_for_skills`. Infuse LOs into these files, not new skill IDs.
