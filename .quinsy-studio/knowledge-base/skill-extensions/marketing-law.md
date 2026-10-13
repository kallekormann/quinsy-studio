# Skill extension: Marketing Law (Germany / EU)
**Owner:** Team 03 Compliance & Legal
**Extends:** CL-001, CL-003, GM-001, GM-003, GM-005, GM-006, GD-001, GD-002 (not a skill ID)
**Target:** Landing and pricing pages, ads, launch posts, newsletters, review requests, referral flows, partner and influencer content, comparison pages
**Environment:** Payload CMS on Next.js; product repo `docs/` and Payload content

## Objective
Check marketing copy, flows and code against German unfair-competition, price and device-access law before they ship. Each line below is a yes/no check. A "no" blocks the ticket until fixed or until the human signs a written exception. This is a checklist, not legal advice. Novel or high-stakes cases go to a lawyer.

---

## 1. Misleading claims (§ 5 UWG)
- [ ] Every factual claim is true and we hold proof. The proof path sits next to the draft (`docs/growth/claims.md`).
- [ ] Sole-position claims ("the only", "first", "leading", "Germany's No. 1") have evidence that we lead by a clear margin, and the evidence is current.
- [ ] Numbers ("10,000 users", "saves 5 hours a week") come from our own measured data, with date and method.
- [ ] "Free" means free. If a paid plan is needed later, the limit is stated next to the word.
- [ ] Prices, availability and delivery times match what the checkout delivers.
- [ ] Test marks, seals and awards are real, current, and link to the criteria.
- [ ] Environmental claims ("klimaneutral", "nachhaltig") are explained in the ad itself (BGH I ZR 98/23). Generic environmental claims and offset-based neutrality claims are banned under Directive (EU) 2024/825 from 27 September 2026; check the amended UWG annex before using any.
- [ ] Fake scarcity or urgency is absent: countdowns end for real, "only 3 left" reflects stock.

## 2. Material information and hidden advertising (§ 5a, § 5b UWG)
- [ ] The commercial purpose of every post, article or video is clear from content or layout (§ 5a(4)). Paid editorial content is labelled (Annex no. 11).
- [ ] Founders, staff and contractors posting about the product say so. Nobody poses as a neutral consumer (Annex no. 23).
- [ ] Offers to consumers show the material information of § 5b(1): main features, identity and address of the trader, total price, payment and delivery terms, withdrawal right where it exists.
- [ ] Search results or rankings on our site disclose paid placement and the main ranking parameters (§ 5b(2)).

## 3. Reviews
- [ ] We never write, buy or commission fake reviews or likes, and never instruct others to (Annex no. 23c).
- [ ] If we show reviews, the page says whether and how we check they come from real customers (§ 5b(3)). Without checks we do not claim "verified" (Annex no. 23b).
- [ ] No review gating: the review request goes to every customer in the cohort, not only to those who rated us well in a pre-survey. Selective asking misleads (§ 5) and breaks Google and Trustpilot policies.
- [ ] Incentives for reviews (discounts, raffles) are disclosed on the review and do not depend on a positive rating.
- [ ] Negative reviews are not suppressed or delayed differently from positive ones.
- [ ] A review request by email is advertising: it needs consent or the § 7(3) conditions (see section 6).

## 4. Influencer and partner content
- [ ] Paid or gifted partner content is labelled "Werbung" or "Anzeige" at the start of the post, visible without expanding. Not hidden in a hashtag block at the end. "#ad", "sponsored" or "in Kooperation mit" alone are risky in German case law.
- [ ] The contract with the partner requires the label and lets us remove unlabelled content.
- [ ] Affiliate links carry `rel="sponsored"` and a visible disclosure near the link (see `affiliate-compliance.md`).
- [ ] We give partners only claims that pass section 1.

## 5. Comparative advertising (§ 6 UWG)
A comparison that names or identifies a competitor is allowed only if all checks pass:
- [ ] It compares goods or services for the same need or purpose.
- [ ] It compares material, relevant, verifiable and typical features, or price, objectively.
- [ ] It causes no confusion between us and the competitor or their marks.
- [ ] It does not exploit or harm the competitor's reputation, and does not disparage.
- [ ] It does not present our product as an imitation of a protected product.
- [ ] Competitor prices and features carry the date checked and a source; the page is reviewed on a schedule.

## 6. Unsolicited contact (§ 7 UWG)
- [ ] Marketing email, SMS and messenger messages go only to people with prior express consent, proven by double opt-in and a consent log (GM-006).
- [ ] The existing-customer route (§ 7(3)) is used only when all four conditions hold: address from a sale, own similar products, no objection, objection notice at collection and in every mail.
- [ ] Cold calls to consumers only with prior express consent, documented and kept (§ 7a UWG). Cold calls to businesses only with at least presumed consent.
- [ ] Every marketing message names the sender and has a working unsubscribe.
- [ ] No disguised sender identity.

## 7. Tell-a-friend and referral invites
- [ ] Our system does not send invitation emails to addresses a user typed in. The BGH treats such mails as advertising by the company without the recipient's consent (BGH I ZR 208/12).
- [ ] Referral uses share links: the user copies a link or uses the device share sheet and sends it from their own account.
- [ ] Referral rewards are disclosed in the shared text if the user gets paid for sharing.
- [ ] Imported address books are not stored or mailed.

## 8. Device access and tracking (§ 25 TDDDG)
- [ ] Nothing non-essential is stored on or read from the user's device (cookies, localStorage, fingerprinting, pixels) before consent. CL-002 banner gates it.
- [ ] Strictly necessary exceptions (session, cart, consent state, security) are listed by name.
- [ ] Marketing pixels (Meta, LinkedIn, Google Ads) and A/B-test assignment cookies load only after consent.
- [ ] Email open pixels and per-recipient click tracking have their own consent (GM-006).
- [ ] Fonts, maps and videos are self-hosted or click-to-load (LG München I, 3 O 17493/20 on Google Fonts).

## 9. Price display (PAngV)
- [ ] Consumer prices are total prices including VAT and all unavoidable components (§ 3). Shipping costs are stated (§ 6).
- [ ] Goods sold by weight, volume, length or area show a unit price per kg, l, m or m² near the total price (§ 4).
- [ ] A price reduction states the lowest total price of the last 30 days before the reduction (§ 11). The percentage or strike-through refers to that price (ECJ C-330/23).
- [ ] Subscription prices state the billing period and the price after any trial or intro period.
- [ ] B2B-only net prices appear only where the offer is clearly limited to businesses.
- [ ] Detail rules for surfaces: GD-002.

---

## Operational instructions

When asked to "check this page, post, flow or campaign for marketing law":
1. **Collect:** the Payload documents, components and mail templates involved; `docs/growth/claims.md`; the consent log schema.
2. **Run sections 1–9.** Mark each line PASS, FAIL or N/A with a reason for N/A.
3. **Report** in this table, then fix FAIL lines in the same ticket or file follow-up tickets:

| Item | Section | Result | Evidence or problem | Fix |
| :--- | :--- | :--- | :--- | :--- |
| *e.g. pricing page hero* | 9 PAngV § 11 | FAIL | *Strike-through shows last month's list price, not the 30-day low* | *Store price history in Payload; render the 30-day minimum* |
| *e.g. referral modal* | 7 Tell-a-friend | FAIL | *Form sends invite mails to typed-in addresses* | *Replace with copy-link and Web Share API* |

4. **Receipt:** paste the table under `## Marketing law` in the ticket receipt.

## References
- UWG §§ 3, 5, 5a, 5b, 6, 7, 7a and Annex nos. 11, 23, 23b, 23c.
- TDDDG § 25; PAngV §§ 3, 4, 6, 11; DSGVO Art. 6, 7, 21; DDG § 5.
- BGH I ZR 208/12 (tell-a-friend); BGH I ZR 164/09 (double opt-in proof); BGH I ZR 98/23 (klimaneutral); ECJ C-330/23 (price reduction reference); LG München I 3 O 17493/20 (Google Fonts).
- Directive (EU) 2024/825 (empowering consumers for the green transition).
