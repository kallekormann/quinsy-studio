# Skill: Lifecycle Email

> Builds marketing email that is lawful in Germany and lands in the inbox: double opt-in with a consent log, the § 7(3) UWG existing-customer route only when all four conditions hold, no per-recipient tracking without consent, an unsubscribe in every mail, and authenticated sending. Transactional and marketing mail stay apart. Mails go out from a background job, never from a request handler.

## Metadata

```
skill_id: GM-006
name: Lifecycle Email
team: 05-growth-marketing-content
lead_role: Growth Manager
support_roles: [Content Strategist, Backend Architect, Legal & Privacy Officer]
phases: [3, 4, 5, 7]
activation_triggers:
  - Ticket words: lifecycle email, double opt-in, newsletter signup, welcome sequence, win-back email, list-unsubscribe, drip campaign, email deliverability
  - Ticket that adds a newsletter form, a marketing mail or a sending domain
  - Any mail sent to a user that is not a direct reply to their own action
pairs_with: [BE-006, BE-005, GM-003, CL-001, CL-004, GM-005]
```

## When to load

- Before the first newsletter form or marketing mail exists. Consent and sending domain come first.
- For every new flow in the lifecycle map (welcome, activation, win-back, announcement).
- When a transactional mail is about to get "just one promo line" (rule 4 says no).
- With `knowledge-base/skill-extensions/email-design.md` for the HTML and copy of each mail, and `marketing-law.md` for claims.

## Rules

### 1. Marketing mail needs prior express consent (§ 7(2) UWG)

Without consent, advertising by email is an unreasonable nuisance. "Advertising" includes newsletters, product announcements, review requests and win-back mails. Consent is per purpose, not bundled with the terms or the signup, and never a pre-ticked box (Art. 7 DSGVO).

### 2. Double opt-in, with a consent log

The form stores the address as `pending`. A confirmation mail goes out with one link and no advertising. Only the click sets `confirmed`. Unconfirmed entries are deleted after a period stated in the data map (CL-004). The consent log is a Payload collection (admin-read only) with: email, `consent_text_version`, `source` (form and URL), `requested_at`, `confirmed_at`, `withdrawn_at`. Store IP or user agent only if the data map names the purpose (proof of consent) and a retention period. We must be able to prove consent per address (BGH I ZR 164/09).

### 3. Existing customers: § 7(3) UWG only when all four hold

Mail without separate consent is allowed only if: (1) we got the address in connection with a sale of goods or services to this customer; (2) we advertise our own similar goods or services; (3) the customer has not objected; (4) we told them clearly at collection and in every mail that they can object at any time at no cost beyond basic transmission rates. Free signups are not a sale. Missing the notice at collection kills the exception. If in doubt, ask for consent.

### 4. Transactional and marketing mail stay apart

Transactional: password reset, order and payment receipts, security notices, account changes. They contain no advertising; a promo block turns them into advertising that needs consent (BGH VI ZR 134/15). Send them from a separate stream or subdomain (for example `mail.` versus `news.`), so a marketing complaint spike does not block password resets.

### 5. Unsubscribe in every marketing mail

- A visible unsubscribe link in the body that works without login, in one step.
- Headers `List-Unsubscribe: <https://…>, <mailto:…>` and `List-Unsubscribe-Post: List-Unsubscribe=One-Click` (RFC 8058), both covered by the DKIM signature.
- The one-click endpoint is a POST without confirmation page, idempotent, and sets `withdrawn_at` at once. Gmail requires unsubscribes to be honoured within two days; we honour them immediately.
- Objection to direct marketing is absolute (Art. 21(2)–(3) DSGVO). Keep only a suppression entry (hashed address) so we never mail them again.

### 6. Tracking pixels and click tracking need consent

Open pixels and per-recipient click IDs read or link behaviour to a person. Treat them as needing consent under § 25 TDDDG and Art. 6(1)(a) DSGVO. Ask for it as a separate, unticked option in the signup form, or send untracked. Without that consent, measure only aggregate clicks on non-personalised links (UTM, see GM-005). Open rates are unreliable anyway since Apple Mail Privacy Protection; judge flows on clicks and conversions.

### 7. Authenticate the sending domain

Follow the published mailbox-provider rules (Google and Yahoo sender requirements from February 2024; Microsoft Outlook.com from May 2025):

- SPF and DKIM on the sending domain; DMARC published, at least `p=none` with a `rua` report address, and the From domain aligned with SPF or DKIM.
- Valid forward and reverse DNS (PTR) on sending IPs; TLS for transmission.
- Spam rate in Google Postmaster Tools below 0.3%, aiming below 0.1%.
- One-click unsubscribe (rule 5) for bulk senders (5,000 or more mails a day to Gmail).
- Move DMARC to `quarantine` or `reject` once reports show all legitimate sources pass.

### 8. Send from a job, with exit conditions

Sending runs as a BE-006 job (Payload jobs queue or the Python worker), never inline in a request. Each send is idempotent per `(subscriber, flow, step)`. Before each step the job re-checks: still `confirmed`, not withdrawn, not suppressed, not hard-bounced, exit condition not met. Hard bounces and complaints from the provider's webhook (BE-005, signature checked) suppress the address at once.

### 9. Content in Payload, design from the extension

Mail copy and flow steps are Payload documents (subject, preheader, body blocks, flow, step, delay). The HTML follows `knowledge-base/skill-extensions/email-design.md` (table layout, dark mode, alt text). Every mail names the sender and links to the Impressum (§ 5 DDG). The email provider is a processor: DPA signed and listed in the record of processing (CL-001, CL-004).

## Workflow

1. Write `docs/growth/lifecycle-map.md`: each flow with trigger, audience, steps, delays, exit conditions, legal basis (consent or § 7(3)), and the one metric it serves.
2. Set up the sending domain (rule 7). Record the DNS records and the date in the map.
3. Build the signup form, confirmation mail and consent log collection (rule 2).
4. Build the unsubscribe link, one-click endpoint and suppression (rule 5).
5. Build each flow as a BE-006 job with the re-check (rule 8). Start with welcome, then activation, then win-back.
6. Write mail content in Payload; render through the email-design rules.
7. Test: double opt-in end to end, unsubscribe by link and by `List-Unsubscribe-Post`, bounce webhook, rendering in Gmail, Outlook and Apple Mail.

### Lifecycle map (default flows)

| Flow | Trigger | Exit when | Basis |
|---|---|---|---|
| Welcome | Subscriber confirmed | Unsubscribed, bounced, all steps sent | Consent |
| Activation | Account created, core action not done | Core action done, unsubscribed | Consent or § 7(3) |
| Win-back | No core action for a period set in the map | Returned, unsubscribed, last step sent → suppress or ask to reconfirm | Consent or § 7(3) |
| Announcement | Release published in Payload | Single send | Consent or § 7(3) |

## Deliverables

- `docs/growth/lifecycle-map.md` (flows, bases, exit conditions, DNS records).
- Payload collections for subscribers/consent log and mail content.
- BE-006 jobs per flow; unsubscribe and webhook endpoints.
- Deliverability record: SPF, DKIM, DMARC values and Postmaster Tools set up.

## Done evidence (receipt)

- Test log: signup → confirmation mail (no advertising) → `confirmed_at` set; screenshot or test output path.
- One-click unsubscribe test: POST to the `List-Unsubscribe` URL sets `withdrawn_at`; next job run skips the address.
- Raw headers of a sent test mail showing `List-Unsubscribe`, `List-Unsubscribe-Post`, DKIM pass, SPF pass, DMARC pass.
- Each flow row in the lifecycle map names its legal basis; every § 7(3) flow shows where the objection notice appears at collection.
- Grep proof that transactional templates contain no promotional blocks.

## Anti-patterns

- Single opt-in, or a newsletter box ticked by default on signup.
- Importing a purchased or scraped list.
- "Recommended for you" blocks in the order confirmation.
- Unsubscribe behind login or a "are you sure?" page.
- Open pixels on everyone, then judging subject lines by open rate.
- Sending from the app server in the request cycle.
- Benchmark targets copied from a blog ("CTR above 3%") instead of our own baseline.
- CAN-SPAM checklists. US law is not our frame.

## Handoff

- To BE-006: job definitions, idempotency key, retry policy.
- To BE-005: provider webhook (bounces, complaints) with signature check.
- To CL-001 / CL-004: consent log, retention of pending and withdrawn entries, provider DPA, data-map rows.
- To GM-003: copy per step; to UX-007 / email-design extension: HTML.
- To GM-005: launch mailing goes only to confirmed subscribers.

## References

- UWG § 7(2), § 7(3); TDDDG § 25; DSGVO Art. 6, 7, 21; DDG § 5.
- BGH I ZR 164/09 (proof of consent, double opt-in); BGH VI ZR 134/15 (advertising in a transactional mail).
- RFC 8058 (one-click unsubscribe); RFC 7489 (DMARC).
- Google email sender guidelines (support.google.com/a/answer/81126); Yahoo sender requirements; Microsoft Outlook.com bulk sender requirements (2025).
- `knowledge-base/skill-extensions/email-design.md`, `marketing-law.md`; `teams/02-backend-systems/skills/jobs-and-delivery.md`.
- Source: agency-agents `marketing/marketing-email-strategist.md` (MIT), rewritten for UWG and DSGVO; benchmarks removed.
