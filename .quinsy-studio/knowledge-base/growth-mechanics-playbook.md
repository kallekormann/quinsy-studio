# Growth mechanics playbook (Teams 10 + 11)

Operational rules for **commercial surfaces**: landing, pricing page/table, checkout, cart, product listing (PLP), product detail (PDP). Team 10 designs the control. Team 11 owns hypothesis and variant intent. Team 05 does SEO/AEO on public URLs only.

Sources (distilled, not reprinted): Nielsen heuristics; Krug; Wroblewski forms; NN/g ecommerce/landing; Baymard checkout and product-list research; *Good Services* (clear offering, no hidden terms). Studio anti-slop still wins over “clever” CRO copy.

## Always (every commercial surface)

**Do**

- One primary job per view (choose a plan, pay, pick a product, understand the offer).
- One primary CTA. Secondary actions are visually quieter.
- Offer, price (or “free”), and next step visible without hunting.
- Proof next to the claim it supports (not a logo row in the footer only).
- Spec **Growth intent** (§6): job, claim, metric or how we would know, what we are *not* testing.
- **Peak–end** after pay/submit: artifact + next step ([delight-playbook.md](delight-playbook.md)). Not confetti over a pending charge.

**Don’t**

- Three competing heroes, three equal CTAs, or a pricing grid that cannot be compared column-to-column.
- A/B instead of fixing a broken flow (wrong surface, broken form, missing default).
- Fake scarcity, hidden renewals, disguised ads, pre-ticked paid add-ons.

**Spec / mock fail**

- No Growth intent on a commercial ticket.
- Price or total appears only after a dead-end click.
- Success/thanks state with no receipt, total, or next step (peak–end missing).

## Landing page

**Do:** Information scent in the first screen (who it is for, what you get, what to do). Scan path: claim → proof → CTA. Literal microcopy.

**Don’t:** Metaphor headlines, overlapping badges, auto-playing noise, nav that competes with the only job.

**Fail:** Hero with no next step; proof unrelated to the claim; Team 11 variants that change five things at once.

## Pricing page / table

**Do:** Comparable columns (same rows). One recommended plan (honest default). Annual/monthly toggle does not hide the other price. Limits and “who this is for” in the cell, not a footnote novel.

**Don’t:** Decoy plan that exists only to confuse. Different feature names per column. CTA that says “Learn more” as the only paid action.

**Fail:** Cannot tell which plan is default; price missing on the recommended card; recommended badge with no reason in §8.

## Checkout / cart

**Do:** Progress or a single short page. Guest path if the product does not require an account to pay. Line items, tax/shipping, and **total** before pay. Errors on the field. Back without wiping the cart.

**Don’t:** Forced account before seeing total. Surprise fees on the last button. Payment as the only error state with no field-level recovery (Wroblewski).

**Fail:** Total not in the mock; no guest/login choice when both exist; no error state.

## PLP (listing / catalog)

**Do:** Filters that match how people shop (not the warehouse taxonomy). One clear product job per card (image, name, price, one action). Selected filters stay visible.

**Don’t:** Infinite identical cards with no price. Filters that reset the scroll with no count. SEO category chrome that hides the list.

**Fail:** Card with no price; no empty-filter state; Team 05 metadata instead of a usable grid.

## PDP (product detail)

**Do:** Title, price, variant, primary add-to-cart above the fold on the default viewport. Variants do not hide availability. Related items after the job is done.

**Don’t:** Carousel-only critical info. “Add” that does nothing when a variant is required (no inline error). Fake reviews.

**Fail:** Add-to-cart with unspecified variant; price missing; no sold-out state.

## Experiments (Team 11)

| Field | Required |
|-------|----------|
| Job | What the person is trying to finish |
| Claim | One sentence, falsifiable |
| Change | **One** primary difference vs control |
| Metric | Named event or, if no analytics yet, what we would count |
| Stop | What would kill the variant |

If there is no analytics yet, still write the claim. Do not invent three layouts “to see what feels better.”

## Dark patterns (never “growth”)

Hidden costs, obstruction, forced continuity, fake urgency, sneak into basket. Legal/HITL. Team 11 does not ship these as variants.
