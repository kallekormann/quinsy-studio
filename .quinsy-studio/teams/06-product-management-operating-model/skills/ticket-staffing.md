# Skill: Ticket Staffing

> The Product Manager staffs every ticket: which teams and skills own it, and why. A ticket is not staffed by the keywords in its title. Staffing decides which skill files the implementer reads and which Done evidence the receipt must show. A missing security, privacy, accessibility or testing skill means that check never happens.

## Metadata

```
skill_id: PM-004
name: Ticket Staffing
team: 06-product-management-operating-model
lead_role: Product Manager (Director)
support_roles: [Process Guard (Director), Systems Architect (Director)]
phases: [3, 4]
activation_triggers:
  - Writing tickets for a milestone, an amendment, or sprint feedback
  - ./studio groom (every sprint)
  - groom finding SKILLS_MISSING, SKILL_UNKNOWN or STAFFING_GAP
  - execute CARD line "staffed by PM-004"
pairs_with: [PM-002, SO-002]
```

## When to load

- Every time tickets are written: milestone breakdown after `./studio approve --milestones`, amendment ticket drafts, `./studio ticket … --from-feedback`.
- Every `./studio groom`. Grooming is where staffing is checked and fixed.
- When the execute CARD says a skill was staffed because the ticket lacked it.

## Rules

### 1. Staff from the work, not the title

Read Target, Scope and AC. Ask what the change touches, not what the title says. A ticket called "Leadmarkt UI parity" collects personal data, so it needs CL-001. A ticket called "Site config cache and host resolution" decides which tenant a request belongs to, so it needs PE-003 and PE-005.

### 2. One owner, then companions

- **Owner:** the skill of the team that does most of the work. It sets `team:` and `assignee_role:`. Put it first in `skills:`.
- **Companions:** skills from other teams whose rules must hold for this change. They do not own the ticket; their Done evidence still goes on the receipt.

### 3. Required companions

`./studio groom` refuses the sprint (`STAFFING_GAP`, error) when one of these signals is present and the skill is missing:

| Signal in Target / Scope / AC | Required skill |
|---|---|
| Auth, login, registration, sessions, roles, permissions, tenants, uploads, webhooks, API keys | PE-003 Security audit, AI-005 AI-code security audit |
| LLM calls, prompts, embeddings | AI-005 |
| Personal data: leads, contact forms, sign-up, profiles, newsletters, tracking | CL-001 GDPR |
| Tracking, analytics, pixels, cookies | CL-002 Cookie banner |
| Secrets, credentials, env vars, SMTP | PE-006 Secrets hygiene |
| Payments, checkout, subscriptions, refunds | BE-008 Payments and billing |
| Checkout, subscriptions, paid plans | CL-003 Imprint and terms |
| Marketing email: newsletter, sequences, onboarding mail | GM-006 Lifecycle email |
| Any user-facing UI | FE-004 Accessibility, FE-006 Frontend testing |

The design phase of a design-track ticket skips FE-006 and UX-009; they apply when the ticket is built.

### 4. Suggested companions

Groom prints these as `STAFFING_SUGGEST` (info). Add them when they apply:

| Signal | Skill |
|---|---|
| New or changed trust boundary (auth, tenant, upload, webhook, payment, third party) | PE-005 Threat modeling (threat delta in the architecture phase) |
| Built UI that has a signed mock | UX-009 UI finish gate |
| Documents, PDFs, invoices | BE-009 Document generation |
| More than one language | FE-008 i18n |
| Public page that should be found | GM-001 SEO |
| Deployment or infrastructure change | PE-001 Infrastructure |
| Backups, restore, incidents | PE-007 Incident response |
| Landing, pricing, checkout, PLP, PDP | GD-002 (plus GD-001 / GD-003 in the design phase) |

### 5. Waive with a reason, never silently

If a required companion does not apply, add it to `staffing_waive:` in the frontmatter and give the reason under `## Staffing`:

```yaml
skills: [FE-001, FE-002, FE-004, FE-006]
staffing_waive: [CL-001]
```

```markdown
## Staffing
- CL-001 waived: the form only filters the public catalog; nothing is stored or sent.
```

### 6. Eight skills at most; split instead of overloading

A card loads at most eight skills. When a ticket needs more, it is doing too much. Split it along the team seam, for example "checkout UI" and "payment webhook". Do not drop a required companion to make room.

### 7. Phase staffing

| Phase | Owner | Typical companions |
|---|---|---|
| Design | Team 10 (UX-*) | GD-* on commercial surfaces, FE-004, CL-001 when the flow collects data |
| Architecture | Team 04 (PS-002) or the building team | PE-005 threat delta, BE-002 for schema, CL-004 data map |
| Implementation | Team 01 / 02 / 07 | The required companions above, UX-009 for UI with a signed mock |

After `approve-design` the owner moves from Team 10 to Team 01; keep UX-006 and add UX-009.

### 8. Cover every team over a milestone

At milestone planning, list the teams the milestone needs. A web product milestone that never touches Team 03 (legal), Team 08 (platform) or FE-004/FE-006 is a staffing gap, not a lucky milestone. Add the tickets: imprint and privacy pages, consent, deployment, backups, accessibility pass.

## Workflow

1. Draft the ticket (Target, Scope, AC). `./studio ticket` pre-fills skills and writes `## Staffing` with the reason for each companion it added.
2. Read the ticket as the implementer would. Set the owner first. Add or remove companions with rules 3 and 4.
3. Run `./studio groom <p>`. Fix every `SKILLS_MISSING`, `SKILL_UNKNOWN` and `STAFFING_GAP`. Decide each `STAFFING_SUGGEST`.
4. `./studio groom <p> --approve` only when the validation has no errors.
5. During execute, if the CARD says `staffed by PM-004`, add those skills to the ticket (or waive them) in the same commit.
6. At retro, list the teams that were never staffed in the sprint and whether that was right.

## Deliverables

- `skills:` with the owner first, companions after, at most eight.
- `team:` and `assignee_role:` that match the owner.
- `## Staffing` with one line per companion and each waiver reason.
- `staffing_waive:` when a required companion does not apply.

## Done evidence (receipt)

Staffing is checked at groom, not on the receipt. The receipt shows the result: each staffed skill's own Done evidence (for example `## Security` for PE-003, `## A11y` for FE-004, the access rule for BE-007).

## Anti-patterns

- Staffing from the title only, or accepting `./studio ticket` output without reading it.
- `skills: []`, or one skill on a ticket that clearly crosses teams.
- Leaving out the security or privacy skill because "it is only a UI ticket".
- Waiving without a reason, or waiving to fit the eight-skill limit.
- Adding every skill "to be safe". Each skill adds files to read and evidence to produce.

## Handoff

- To the owner team: the ticket with its skills; the CARD lists the skill files to read.
- To Team 09 (SO-002): sprints with repeated `STAFFING_GAP` findings become a process LO.
- To Team 04 (PS-002): tickets that need PE-005 get a threat delta in the architecture phase.

## References

- `studio-tools/skill_matcher.py` — `STAFFING_RULES`, `staff_skills`
- `studio-tools/sprint_backlog_validate.py` — `staffing_findings`
- `process/ticket-team-allocation.md` — owner by ticket kind
- `teams/skill-registry.md` — all skill IDs
