# Milestone coverage checklist

> Used by PM-002 when drafting `docs/phases/`, and by `./studio approve <p> --milestones`, which refuses a roadmap that leaves out an area the PRD needs. Code mirror: `studio_milestones.COVERAGE_AREAS`.

The roadmap covers the **finished product**, not the MVP. M0 is the first two-month chunk. Every later area still gets a milestone row, even if it is M4. A roadmap that stops at "MVP + polish" is refused.

## Areas

Each row names the area, when it is required, and the words `approve --milestones` looks for in `docs/phases/M*.md`. Write the area in plain words; the keyword is only how the check finds it.

| Area | Required when | Found by | Owner skills |
|------|---------------|----------|--------------|
| Scaffolding and repo shape | always | scaffold, boilerplate, repo layout, separation of concerns | PS-002, FE-001, BE-001 |
| Data model and database | always | database, schema, migration, postgres | BE-002 |
| API and services | always | api, service layer, endpoint | BE-001, BE-004 |
| Background jobs and workers | PRD names jobs, email, imports, exports, AI calls, scheduled work | worker, queue, job, outbox | BE-006 |
| Cache and realtime | PRD names cache, realtime, presence, rate limits | redis, cache, realtime, websocket | BE-004, BE-006 |
| Authentication and access | always | auth, login, session, access control, roles | BE-003, PE-003 |
| Security hardening | always | security, threat model, hardening, csp | PE-003, PE-005, AI-005 |
| Privacy and legal | always | privacy, dsgvo, gdpr, consent, impressum | CL-001, CL-002, CL-003, CL-004 |
| Performance | always | performance, core web vitals, budget, caching | FE-003, BE-004 |
| Frontend boilerplate and app shell | always | app shell, layout, routing, frontend boilerplate | FE-001, FE-002 |
| UX flows and interaction | always | user flow, interaction, usability, onboarding | UX-001, UX-002, UX-003 |
| Motion and delight | always | motion, animation, transition, aha, delight | UX-002, FE-001 |
| Billing | PRD names price, plan, subscription, checkout, invoice | billing, payment, subscription, checkout | BE-008, CL-003 |
| Internationalisation | PRD names more than one language or market | i18n, localisation, localization, language | FE-008, BE-007 |
| Operations and production | always | ops, deploy, coolify, backup, incident, readiness | PE-001, PE-006, PE-007 |
| Testing and quality | always | test, e2e, accessibility, a11y, qa | FE-004, FE-006 |
| Positioning and messaging | public web product | positioning, message, persona page, storytelling | GM-007, UX-007 |
| SEO and AEO foundation | public web product | seo, aeo, sitemap, schema.org, llms.txt | GM-001, GM-002 |
| Growth loops | public web product with accounts | growth loop, invite, referral, activation, upsell | GD-004, UX-002 |
| Content engine | public web product that wants organic traffic | blog, posts, content engine, editorial | GM-003, BE-007 |
| Launch | public web product | launch, waitlist, lifecycle email, community | GM-005, GM-006 |

"Public web product" means the PRD or the archetype names a marketing site, landing page, signup, or organic acquisition. "Always" rows apply to every project archetype that ships software.

## How to use it

1. Read the PRD and `docs/definitions/`. Mark each row required or not, with the sentence in the PRD that decides it.
2. Place every required row in a milestone. One row can span two milestones (foundation in M0, hardening in M2); name both.
3. Order milestones so each one ships something a person can use. Foundation rows (scaffolding, data model, auth, app shell) belong to M0.
4. Write each `M<n>-*.md` from `studio-templates/phases/milestone.md`. The `## Coverage` table names the rows that milestone carries.
5. `./studio approve <p> --milestones`. The CLI lists missing required areas and refuses until each has a home.

## Anti-patterns

- A roadmap of "MVP, Beta, Launch" with no area rows. Those are dates, not scope.
- Security, privacy and operations left to "later". They are M0 foundation plus a hardening row before the first `ship --to main`.
- Growth and SEO rows deferred without a reason written in the PRD.
- Tickets written for M1 while M0 is open. Tickets exist for the active milestone only.
