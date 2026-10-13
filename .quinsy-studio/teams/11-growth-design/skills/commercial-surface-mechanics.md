# Skill: Commercial surface mechanics (GD-002)

```
skill_id: GD-002
team: 11-growth-design
lead_role: Growth Designer
```

Growth mechanics as **design constraints** on money surfaces: landing, pricing table/page, checkout/cart, PLP, PDP. Team 10 still draws the UI; this skill forbids pretty grids that fail comparison, hidden totals, and scentless heroes.

**Playbook:** [growth-mechanics-playbook.md](../../../knowledge-base/growth-mechanics-playbook.md)

**Ticket types:** `marketing-page`; `ui-composition` when the title is checkout, cart, catalog, PDP, or product listing.

**Fail lines:** see playbook per surface, plus the two sections below.

## Price display (PAngV, consumer-facing surfaces)

Applies wherever a consumer sees a price: landing, pricing table, PLP, PDP, cart, checkout, ads, newsletters.

**Do**

- Show the **total price** including VAT and all unavoidable components (§ 3 PAngV). Net prices only on surfaces clearly limited to businesses.
- State shipping and delivery costs, or where they are shown, next to the price (§ 6).
- Goods sold by weight, volume, length or area: show the **unit price** per 1 kg, 1 l, 1 m or 1 m² close to the total price, equally legible (§ 4).
- Subscriptions: billing period next to the price ("€ 12 / Monat"), and the price after any trial or intro period on the same view.
- Annual/monthly toggle: both prices stay findable; the "per month" figure of an annual plan also shows the amount charged per year.
- **Price reductions** (§ 11): a strike-through, "−20 %" or "was € X" refers to the **lowest total price of the last 30 days** before the reduction. The percentage is calculated from that price (ECJ C-330/23). Store price history in Payload (price + valid-from per product or plan) and render the 30-day minimum from data, never from a hand-typed "old price" field.
- Total in the cart and on the checkout button matches the final charge. No price component appears for the first time after the last click.

**Fail**

- Price shown without VAT on a consumer surface, or VAT "plus" in small print.
- Strike-through price that is a list price ("UVP" without saying so) or last month's higher price, not the 30-day low.
- Unit price missing for goods sold by quantity.
- Intro price with the renewal price only in the terms.
- Fake countdowns or "only today" reductions that renew.

Wider claims, review and urgency rules: [marketing-law.md](../../../knowledge-base/skill-extensions/marketing-law.md).

## Fonts and third-party assets

- **Self-host fonts.** Serve font files from the app (`next/font/local`, or `next/font/google`, which downloads at build time and serves from our domain). No `<link>` to `fonts.googleapis.com` or other font CDNs at runtime. Loading Google Fonts from Google transfers the visitor's IP without consent (LG München I, 20 Jan 2022, 3 O 17493/20).
- Same rule for icon fonts, maps, video embeds and chat widgets on commercial surfaces: self-host, or click-to-load after consent (CL-002).
- Check: the built page makes no request to a third-party font or asset host before consent (browser network panel or a Playwright request filter in the receipt).

**Done evidence (receipt):** screenshot of each price state (regular, reduced with 30-day reference, subscription with period); network log showing no third-party font requests.
