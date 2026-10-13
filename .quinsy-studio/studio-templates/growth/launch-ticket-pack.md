# Launch ticket pack

Drafts for a launch milestone (`knowledge-base/launch-playbook.md`). Create each with `./studio ticket <p> "<title>"`, then paste the sections. Replace `<release>` and `<p>`. `test_launch_pack.py` checks that every draft passes PM-004 staffing.

---

### L1 — Launch plan and channel drafts

## Target
`docs/growth/launch-plan.md` for <release> and one draft per channel in scope, ready for the human to post.

## Scope
- Launch plan from `studio-templates/growth/launch-plan.md`: goal, audience, three messages with proof, channels in and out of scope with rules URL and date read, timeline, measurement, risks, disclosure line.
- `docs/growth/launch/<channel>.md` per channel with its disclosure line and UTM link.
- Claims list with evidence for every sole-position or numeric claim (marketing-law).

## AC
- [ ] Launch plan has every heading; no invented numbers
- [ ] Every draft has a disclosure line and a UTM link listed in `docs/growth/utm-register.md`
- [ ] No draft asks for upvotes or likes

## Staffing
- GM-005 (owner): launch plan, channel rules, disclosure
- GM-003: messages and proof
- GD-001: each message is a falsifiable claim with a stand-in metric

---

### L2 — Launch landing page and pricing

## Target
A public landing page and pricing page for <release> that a PRD persona understands in five seconds and can act on.

## Scope
- Design phase: spec, real-UI mocks of the landing and pricing pages at 1440 and 390, five-second test, persona walkthrough, imagery briefs.
- Implementation: Payload-managed sections, prices with VAT per PAngV, public metadata, schema and llms.txt entry.

## AC
- [ ] Signed mocks; UX-009 finish gate PASS
- [ ] Prices show the total including VAT
- [ ] axe test green on both pages; keyboard path to the primary action

## Staffing
- UX-007 (owner): story and imagery
- GM-007: core message and problem-first order from docs/definitions/12-positioning.md
- GD-002: commercial-surface mechanics and PAngV
- GD-001: growth intent claim
- GD-003: five-second test and walkthrough
- GM-001: public page SEO; schema and llms.txt entries follow the SEO foundation pack (GM-002 owns that pack)
- FE-004: accessibility
- FE-006: tests

---

### L3 — Press kit, launch post and changelog in Payload

## Target
The launch post, changelog entry and press kit page are Payload documents published through the normal flow.

## Scope
- Payload collections or globals for posts, changelog and press kit if they do not exist.
- Press kit page: boilerplate, logo files, screenshots captured from the app, founder photo with release, contact address.

## AC
- [ ] All three pages render from Payload; no hand-edited HTML
- [ ] Screenshots are captures of the running app
- [ ] Each page has metadata and appears in the sitemap

## Staffing
- GM-003 (owner): launch copy
- BE-007: Payload collections and access
- UX-007: screenshots and imagery
- GM-001: metadata and sitemap
- CL-001: founder photo and contact address are personal data
- FE-004: accessibility
- FE-006: tests

---

### L4 — Cookieless analytics and UTM register

## Target
Visits and signups per launch channel are countable without cookies or device storage.

## Scope
- Self-hosted cookieless analytics on Coolify (for example Umami or Plausible), or an ADR for another tool.
- `docs/growth/utm-register.md`; one test visit per UTM source.
- Processor list and privacy policy updated.

## AC
- [ ] The tool stores nothing on the device; if it does, the consent banner gates it
- [ ] One test visit per UTM source visible in analytics (screenshot path)
- [ ] No personal data in UTM parameters

## Staffing
- GM-005 (owner): measurement plan
- CL-002: consent and § 25 TDDDG
- CL-001: processor list and privacy policy
- PE-001: deploy on Coolify
- PE-006: analytics credentials

---

### L5 — Welcome flow and launch mailing

## Target
New signups get a confirmation and welcome mail, and the launch mailing reaches confirmed subscribers only.

## Scope
- Double opt-in for the newsletter; transactional mails separate from marketing mails.
- Welcome flow and one launch mailing with unsubscribe in one click.

## AC
- [ ] Double opt-in recorded with timestamp
- [ ] Launch mailing goes only to confirmed subscribers
- [ ] Unsubscribe works in one click and is honoured at once

## Staffing
- GM-006 (owner): lifecycle email and consent
- CL-001: personal data and consent records
- PE-006: SMTP credentials
- FE-006: tests

---

### L6 — Legal pages: Impressum, privacy, terms

## Target
Impressum, privacy policy and terms are reachable from every page footer before launch.

## Scope
- Impressum per § 5 DDG, privacy policy listing every processor, terms with withdrawal rules if the product takes money.

## AC
- [ ] All three pages linked in every footer
- [ ] Every processor from L4 and L5 is listed
- [ ] Withdrawal terms present when there is a paid plan

## Staffing
- CL-003 (owner): Impressum and terms
- CL-001: privacy policy and processors
- FE-004: accessibility
- FE-006: tests

---

### L7 — Production readiness: monitoring, runbook, rollback

## Target
Production can be watched, rolled back and recovered on launch day.

## Scope
- Error monitoring and uptime alert; `docs/ops/incident-runbook.md`; rollback commit named for Coolify.
- Secrets inventory complete; data ports bound to `127.0.0.1`; restore drill passed.

## AC
- [ ] `./studio ship <p> --to main` pre-checks pass (runbook, inventory, ports, exceptions)
- [ ] An alert reaches the human in a test
- [ ] Restore drill time recorded

## Staffing
- PE-007 (owner): incident runbook and breach response
- PE-001: monitoring, backups, Coolify
- PE-006: secrets inventory
- SO-005: release reality check

---

### L8 — Launch day and T+7 results

## Target
The launch runs from the plan, and the launch plan records what happened.

## Scope
- After `./studio ship <p> --to main --approve`: launch-day checklist from GM-005 on the receipt; human posts; agent drafts replies.
- T+7: `## Results` in the launch plan; bugs from launch week filed as tickets.

## AC
- [ ] Launch-day checklist copied to the receipt with PASS / FAIL / NOT TESTED per line
- [ ] `## Results` filled with visits and signups per UTM source
- [ ] Launch-week bugs are tickets, not chat fixes

## Staffing
- GM-005 (owner): launch day and results
- SO-005: reality check on production
- PE-007: on watch for the first hours
