# Skill: Release Reality Check

> The last check before the human sees a sprint. After `./studio ship <p> --to dev`, walk one real journey end to end on the dev deployment, re-run every done ticket's default-flow claim there, and write one verdict: READY, NEEDS WORK or FAILED. Per-ticket QA proves a ticket in isolation. This check proves the tickets work together on a deployed build. FAILED files debug tickets and keeps the cadence review closed; the human is never asked to sign a broken build.

## Metadata

```
skill_id: SO-005
name: Release Reality Check
team: 09-studio-operations-evolution
lead_role: Release Verifier
support_roles: [QA Specialist, Process Guard]
phases: [5, 7]
activation_triggers:
  - "./studio ship <p> --to dev" finished and a cadence review is due
  - Review packet (sprints/SPRINT-NN/review.md) is being prepared
  - Phrases: "reality check", "release reality check", "ready for review", "integration check"
pairs_with: [FE-006, FE-004, FE-003, UX-009, SO-002, PE-002]
```

Default verdict: NEEDS WORK until evidence from the dev deployment exists.

## When to load

- After `ship --to dev` and before `./studio review` opens the cadence HITL.
- Again after the fixes from a FAILED verdict ship to dev.
- Not per ticket. Per-ticket proof is the receipt, gate level 5 and QA_REVIEW.
- Not for backend-only sprints that end in an INFORM. Run it on the next cadence review that includes them.

## Rules

### 1. Test the dev deployment, not the laptop

Use the dev URL from the project runbook. A local `next dev` run is not evidence for this check. If dev is not reachable, the verdict is NEEDS WORK with the reason "dev not reachable". Do not fall back to localhost and call it READY.

### 2. One end-to-end journey, chosen from the PRD

Pick the journey the sprint moved the most, from `docs/workflows/REGISTRY.md` when it exists, else from the PRD default flow. Walk it start to finish as a new user: entry route, sign-up or sign-in through Payload auth, the core job, the result. Cross every ticket boundary the sprint touched. Run it at 1440 and at 390.

### 3. Re-check every done ticket's default-flow claim

For each ticket that reached `done` since the last cadence review, open its receipt `## Default flow` and repeat that path on dev. Record PASS, FAIL or NOT TESTED per ticket. A claim that only worked on localhost is a FAIL here.

### 4. Evidence is a file, a status or a log line

Screenshots go in `sprints/SPRINT-NN/reality-check/` and must exist on disk. Behavior needs more than a screenshot: a URL change, a persisted record you can reload, a network status, a Playwright assertion. A screenshot of a filled form does not prove it was saved.

### 5. Automatic-fail triggers

Any one of these makes the verdict FAILED:

- A journey step cannot be completed on dev.
- A done ticket's default-flow claim fails on dev.
- A receipt names an evidence path that does not exist.
- A 5xx response, an unhandled client error or a blank screen on the journey.
- A private or authenticated page is served from a shared cache, or one user sees another user's data.
- An axe violation of impact `critical` or `serious` on a journey route (FE-004).
- The 390 layout hides the primary action or the job's key object.
- A pending migration on dev, or a schema error caused by one.
- A UI ticket shipped with an open UX-009 HOLD.

A soft `perf_budget` warning is not an automatic fail. List it under findings.

### 6. Verdict rules

- **READY**: the journey passes at both widths, every ticket row is PASS, and no trigger fired.
- **NEEDS WORK**: no trigger fired, but at least one row is NOT TESTED, or findings remain that the human should weigh.
- **FAILED**: at least one automatic-fail trigger fired.

A NOT TESTED row never becomes PASS by argument.

### 7. Do not invent issues

Report only reproducible gaps against the PRD, the signed specs or the ticket AC. Zero findings is a valid result for the tested scope; list what was not tested next to it. Do not add requirements that no spec states. Do not grade style with a score.

### 8. FAILED files debug tickets, not a sign-off request

On FAILED, write one bug ticket per trigger with `./studio ticket <p> "..."` in Issue / Expected / Actual / Evidence / Fix / Files form. Do not open the cadence review. Fix in the next implementation work, ship to dev again, then rerun this check. Execute continues; this is not a new human stop.

### 9. Stay independent

Run the check with a fresh context when possible: the dev URL, the receipts, `review.md` and the specs only. Do not reuse the implementing session's conclusions. Treat "all green" claims in receipts as claims to verify.

## Workflow

1. Confirm `ship --to dev` finished and note the deployed commit SHA.
2. Read the runbook for the dev URL. Read `sprints/SPRINT-NN/review.md` for the done-ticket list.
3. Choose the journey (rule 2). Write its steps before walking it.
4. Walk the journey at 1440, then at 390, with Playwright against the dev URL. Save a screenshot per step and keep the trace.
5. Run the axe scan on each journey route (FE-004).
6. Re-run each done ticket's default flow (rule 3). Fill the ticket table.
7. Check the triggers (rule 5). Pick the verdict (rule 6).
8. Write `sprints/SPRINT-NN/reality-check.md`. Link it from `review.md`.
9. FAILED: file the bug tickets and keep the review closed. READY or NEEDS WORK: continue to `./studio review`.

## Deliverables

`sprints/SPRINT-NN/reality-check.md`:

```markdown
# Reality check — SPRINT-NN

Verdict: READY | NEEDS WORK | FAILED
Dev URL: <url>  ·  Commit: <sha>  ·  Date: YYYY-MM-DD

## Journey
Name: <journey from REGISTRY or PRD>
| # | Step | 1440 | 390 | Evidence |
|---|------|------|-----|----------|
| 1 | Open /, click "Start" | PASS | PASS | reality-check/j1-1440.png, j1-390.png |

## Done tickets
| Ticket | Default-flow claim | Result | Evidence |
|--------|--------------------|--------|----------|
| T-012 | /settings → save name → reload shows name | PASS | reality-check/T-012.png, PATCH 200 |

## Automatic-fail triggers
- none fired | <trigger> → <ticket filed>

## Findings (not triggers)
- <reproducible gap, where, evidence>

## Not tested
- <scope, reason>
```

## Done evidence (receipt)

This check has no ticket receipt. The review packet is its receipt:

- `reality-check.md` exists with a verdict line, the dev URL and the commit SHA.
- Every screenshot path in it exists on disk.
- Every done ticket of the sprint has a row with PASS, FAIL or NOT TESTED.
- A FAILED verdict lists one filed ticket ID per trigger.

## Anti-patterns

- Running the journey on localhost because dev is slow to deploy.
- Copying receipt results into the table without repeating the path.
- READY with NOT TESTED rows.
- A quality score or grade in place of a verdict.
- Inventing findings so the report does not look empty.
- Asking the human to sign a FAILED build "with known issues".
- Fixing code inside this check. It files tickets; implementation fixes them.

## Handoff

- **To the human (cadence review):** READY or NEEDS WORK, with `reality-check.md` linked at the top of `review.md`.
- **To implementation:** FAILED bug tickets in the product backlog, tagged into the current sprint.
- **To SO-002:** recurring trigger types for the retro.
- **To SO-003:** a rule that failed twice across sprints becomes an LO candidate in a HQ session.

## References

- [human-in-the-loop.md](../../../process/human-in-the-loop.md) — cadence review and `ship --to dev`
- [qa-gate-playbook.md](../../../knowledge-base/qa-gate-playbook.md) — default-flow proof
- [hq-agency-agents-integration.md](../../../process/hq-agency-agents-integration.md) — L1, L2, L11
- FE-006 Frontend testing · FE-004 Accessibility · UX-009 UI finish gate
- Source: msitarzewski/agency-agents `testing/testing-reality-checker.md`, `specialized/agents-orchestrator.md` (MIT), rewritten for the studio loop
