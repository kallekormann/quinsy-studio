# Launch playbook

How a milestone that ends in a public release gets launched: which tickets exist, in which studio phase they run, and what has to be true on launch day. Channel rules, disclosure and the launch-day checklist live in GM-005 (`teams/05-growth-marketing-content/skills/launch-community.md`). Claims and partner posts follow `skill-extensions/marketing-law.md`.

## 1. When a launch exists

A milestone whose last ticket is the first `ship --to main` of a product, or a release the PRD names as public, is a launch milestone. The PM (PM-004) adds the launch ticket pack when the milestone is planned, not after the build. A launch without a metric in the gate 0 frame starts with `unknown` and says how it will be learned.

## 2. Ticket pack

Copy the drafts in `studio-templates/growth/launch-ticket-pack.md` with `./studio ticket <p> "<title>"`, then paste the Target, Scope, AC and Staffing into each ticket. Drop a ticket only with a reason in the milestone plan (for example "no mailing list yet: L5 dropped").

| # | Ticket | Phase | Owner skill |
|---|--------|-------|-------------|
| L1 | Launch plan and channel drafts | architecture (plan), implementation (drafts) | GM-005 |
| L2 | Launch landing page and pricing | design, then implementation | UX-007 + GD-002 |
| L3 | Press kit, launch post and changelog in Payload | implementation | GM-003 |
| L4 | Cookieless analytics and UTM register | implementation | GM-005 |
| L5 | Welcome flow and launch mailing | implementation | GM-006 |
| L6 | Legal pages: Impressum, privacy, terms | implementation | CL-003 |
| L7 | Production readiness: monitoring, runbook, rollback | implementation | PE-007 |
| L8 | Launch day and T+7 results | after `ship --to main` | GM-005 |

L2 runs in the design phase with real-UI mocks, the five-second test and the GD-003 walkthrough. L6 and L7 block L8. L8 starts only after the human approves `./studio ship <p> --to main --approve`.

## 3. Timeline

| When | What |
|------|------|
| T-21 | L1 launch plan written; channels in and out of scope; rules pages read and dated |
| T-14 | L2 signed in the design phase; L6 and L7 in the implementation phase |
| T-7 | L3, L4, L5 done; UTM test visits visible; mail flow tested end to end |
| T-2 | Reality check (SO-005) on dev is READY; channel drafts handed to the human |
| T-0 | `ship --to main --approve`; launch-day checklist (GM-005) on the receipt; human posts |
| T+1 to T+7 | Agent drafts replies; human answers; bugs filed as tickets, not hot-fixed in chat |
| T+7 | L8 writes `## Results` in the launch plan; the retro reads it |

## 4. What the studio enforces

- Every ticket in the pack passes `./studio groom` staffing (security, privacy, consent, email and accessibility companions are already on the drafts).
- The gate and receipt rules apply as for any ticket: PASS / FAIL / NOT TESTED with paths, QA review, finish gate on L2.
- `ship --to main` refuses without `docs/ops/incident-runbook.md`, a complete secrets inventory and data ports bound to `127.0.0.1` (L7 covers these).
- Marketing copy goes through the anti-slop gate, including the must-fail microcopy.

## 5. Never

- The agent registers accounts, logs in to social platforms or posts for the human.
- Upvote requests, vote rings, sock puppets, undisclosed staff or friend reviews.
- A launch metric copied from someone else's blog.
- Tracking that sets cookies before consent.
- A launch date that skips the reality check.
