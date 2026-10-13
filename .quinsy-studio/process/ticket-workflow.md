# Quinsy Studio — Ticket Workflow

> **Sprint HITL (after milestone roadmap):** use the [product backlog model](backlog-model.md) and [milestone planning](milestone-planning.md).
> The 9-step workflow below describes **quality gates inside a ticket**, not folder moves.

## Sprint ticket folders (canonical)

| Folder | When |
|--------|------|
| `backlog/*.md` | Product backlog (unscheduled) or sprint-planned (has `sprint:` tag) |
| `backlog/implement/` | Active sprint work |
| `backlog/done/` | Completed |

Create tickets:

```bash
./studio ticket <project> "<title>"   # → backlog/TICKET-NNN.md (status: backlog)
./studio ticket-card <project> <ID>   # compact card for the implementer (not the whole file)
```

New tickets are **compact**: frontmatter is the machine record; body is Target, Scope, AC only. Boilerplate DoD (gate 5, anti-slop) lives in process docs — do not paste it on every ticket.

**Groom for execution:** tickets a small/fast model will implement must expand to the contract in [ticket-authoring-playbook.md](../knowledge-base/ticket-authoring-playbook.md) (verbatim artifacts, literal Verify, Do not touch, Stop and ask if). Frontmatter `executable_by: composer|opus|human`. Never groom **XL** into a sprint.

**Rule (LO-0204):** `./studio ticket … --from-feedback` must use the clarify **draft_acceptance** lines as AC. Do not emit a generic “A user in project … uses the feature … works as described” Given/When/Then. If the draft has scope/out-of-scope, those become the ticket Scope — rewrite leftover filler before `./studio sprint`.

Move during sprint:

```bash
./studio move <project> TICKET-NNN implement
./studio move <project> TICKET-NNN done
```

**Rule (LO-0333 / LO-0338):** `ia-navigation` specs document `ia_nav: { top, depth }` and pass `./studio ia-audit`. Gate 5 soft-warns token hex and native `<select>`. AI-001 / AI-004 receipts need a filled `## Eval` or `move … done` refuses.

**Rule (LO-0294):** When `needs_architecture` is true, write `docs/architecture/<TICKET>.md` and keep the ticket on the production stream until `architecture_status` is approved. `./studio execute` must not offer `IMPLEMENT` while the architecture packet is pending (`PB-20260916-003` ticket-workflow, `PB-20260916-004` HITL).

**Rule (LO-0292):** `move … done` may print “sprint complete” only when every sprint ticket is `done` or `cancelled`. If others remain, print remaining count and `./studio execute` — do not send the agent to retro mid-sprint.

**Rule (LO-0175):** When a ticket is **superseded** or **cancelled**, in the **same turn** either clear `sprint:` (and set `sprint_deferred: true` if it stays in backlog) **or** `./studio move … cancelled` so it is not in `implement/` / sprint plan. Do not leave a ghost that `review` / `execute` can still pick. Pair with LO-0060 when the sprint goal itself changes.

**Rule (LO-0383):** Test helpers that stand in for primary keys must match the column type (UUID when the schema is UUID). Design-track and parked tickets stay out of an implementation sprint until that phase is open.

---

## Legacy: 9-step workflow (quality gates, not folders)

```
┌─────────────────────────────────────────────────────────────────┐
│                    9-STEP TICKET WORKFLOW                       │
└─────────────────────────────────────────────────────────────────┘

 1. INTAKE          ──▶  ticket is created
       │
 2. ANALYSIS        ──▶  requirements are analyzed
       │
 3. PLANNING        ──▶  implementation is planned
       │
 4. DESIGN          ──▶  design/architecture is defined
       │
 5. IMPLEMENTATION  ──▶  code is written
       │
 6. QA GATE         ──▶  quality is checked
       │
 7. REVIEW          ──▶  code review is performed
       │
 8. REUSE REVIEW    ──▶  reusability is checked
       │
 9. DONE            ──▶  ticket is completed
```

---

## The 9 steps (mandatory)

| # | Step | Description |
|---|------|-------------|
| 1 | **Intake & understanding** | read ticket, understand context, clarify questions |
| 2 | **Decomposition & dependencies** | split into sub-tasks, identify dependencies |
| 3 | **Conception/design** | define solution approach, architecture decisions |
| 4 | **Implementation (clean code, TDD)** | write code, write tests, tests green |
| 5 | **Self-check (tests, lint, review)** | independent quality check |
| 6 | **QA gate** | `./studio gate <project>` must be green |
| 7 | **Docs & ADR sync** | update documentation, create/update ADRs |
| 8 | **Reuse review** | reusable? → `./studio promote` + docs |
| 9 | **Completion** | `./studio move … done` (receipt + gate 5). Product git: **one commit per ticket**. Push `origin/dev` only before cadence review. `main` is HITL. |

**Rule:** no step is skipped. Every step is documented.

---

## Detailed steps

### Step 1: Intake & understanding

```bash
./studio ticket <project> "<title>" --phase <N> --priority <P> --estimate <E>
```

| Aspect | Description |
|--------|-------------|
| **Action** | create ticket with all metadata |
| **Output** | `<project>/backlog/TICKET-NNN-<slug>.md` |
| **Responsible** | Project Manager |

**Ticket template:**
```markdown
---
id: TICKET-NNN
title: <title>
status: open
phase: <N>
priority: <P0-P3>
estimate: <S/M/L/XL>
created: YYYY-MM-DD
assignee: <role>
---

# TICKET-NNN — <title>

## Acceptance criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Technical requirements
...

## Dependencies
- ...

## Rationale
Why is this ticket important?
```

---

### Step 2: Decomposition & dependencies

```bash
./studio move <project> TICKET-NNN analyze --reason "Decomposition done"
```

| Aspect | Description |
|--------|-------------|
| **Action** | split into sub-tasks, identify dependencies |
| **Output** | ticket with sub-tasks and dependencies |
| **Responsible** | Project Manager + Tech Lead |

**Checklist:**
- [ ] Ticket decomposed into sub-tasks
- [ ] Dependencies on other tickets documented
- [ ] Blockers identified
- [ ] Estimates for sub-tasks

---

### Step 3: Conception/design

```bash
./studio move <project> TICKET-NNN design --reason "Conception complete"
```

| Aspect | Description |
|--------|-------------|
| **Action** | define solution approach, architecture decisions |
| **Output** | design specification, possibly ADR |
| **Responsible** | relevant expert roles |

**Checklist:**
- [ ] Solution approach documented
- [ ] Architecture decisions as ADR (if needed)
- [ ] UI components defined (if frontend)
- [ ] Data model defined (if backend)
- [ ] API design defined (if API)

---

### Step 4: Implementation (clean code, TDD)

```bash
./studio move <project> TICKET-NNN implement --reason "Implementation started"
```

| Aspect | Description |
|--------|-------------|
| **Action** | write code (test-first!) |
| **Output** | working code with tests |
| **Responsible** | Backend Systems / Frontend Experience |

**Rules:**
- ✅ Test-first (TDD)
- ✅ Clean code / SOLID
- ✅ Specific error handling
- ✅ No AI slop
- ✅ Documentation
- ✅ UI kit peers already in the product app (`docs/setup/ui-kit.md`) before composing kit components
- ✅ Schema: agent runs migrate when the DB is reachable; INFORM. Do not ask the human.
- ❌ No code without a ticket
- ❌ No commit without green tests
- ❌ Do not dump migrate commands for the operator to run instead of you

---

### Step 5: Self-check (tests, lint, review)

```bash
# run tests
pnpm test
# linting
pnpm lint
# build
pnpm build
```

| Aspect | Description |
|--------|-------------|
| **Action** | independent quality check |
| **Output** | all checks green |
| **Responsible** | implementing agent |

**Checklist:**
- [ ] All tests green
- [ ] No linting errors
- [ ] Build successful
- [ ] Code review (self or peer)
- [ ] No AI slop (anti-slop check)

---

### Step 6: QA gate

```bash
./studio gate <project> --level 5
```

| Aspect | Description |
|--------|-------------|
| **Action** | run the formal QA gate |
| **Output** | gate status (green/red) |
| **Responsible** | QA Specialist, Anti-Slop Auditor |

**Rule:** `./studio gate <project> --level 5` must be green before a ticket is marked done. Level 2 (lint only) is **not** sufficient — it cannot catch runtime client crashes.

**Enforced in CLI:** `./studio move … done` rejects unless `status.json` shows gate level ≥ 5 and `gate_status: passed`.

**On failure:** the ticket goes back to step 4 (implementation) with `sprints/SPRINT-NN/debug/<TICKET>.md` in Issue / Expected / Actual / Evidence / Fix / Files form. Fix only the listed issues.

Level 2 also runs the security checks (`secret_scan`, `client_env_leak`, `insecure_env_fallback`, `docker_secret_leak`). Level 5 adds `payload_access`, `local_api_override`, `webhook_signature`, `npm_audit_policy`, `a11y_axe`, `e2e_hygiene` and `api_contract`. A check that could not run (no smoke config, registry offline) is NOT TESTED, never a pass. Waive a finding only with a row in `docs/security/exceptions.md` that has an expiry date.

---

### Step 6b: Independent QA review (`QA_REVIEW`)

```bash
./studio qa <project> <TICKET>                    # writes sprints/SPRINT-NN/qa/<TICKET>.md + reviewer brief
./studio qa <project> <TICKET> --verdict PASS|FAIL
```

| Aspect | Description |
|--------|-------------|
| **Action** | a fresh-context subagent judges the ticket against its AC |
| **Input** | the card, the diff, the receipt and the evidence only, not the implementer's chat |
| **Output** | `qa/<TICKET>.md`: `Verdict:`, a PASS / FAIL / NOT TESTED line per AC, `## Findings` on FAIL |
| **Responsible** | QA Specialist (reviewer subagent); the implementer never writes its own verdict |

The reviewer defaults to FAIL when proof is missing. PASS is refused while any AC is FAIL or NOT TESTED. A FAIL returns the ticket to step 4 and counts toward the same 3 attempts as a red gate. A new green gate resets the verdict.

**UI finish gate (UX-009).** When `docs/design-specs/mocks/<TICKET>/` holds signed screenshots, run `./studio qa <project> <TICKET> --finish` after the QA PASS. Capture the shipped route in every mock state at 1440 and 390 into `qa/<TICKET>-finish/`, compare them in `qa/<TICKET>-finish-gate.md` with a Keep list, then record `--finish PASS` or `--finish HOLD`. HOLD is a QA fail, not a human stop.

**Escalation.** At 3 failures, or two identical ones, execute writes `sprints/SPRINT-NN/escalations/<TICKET>.md` and moves the ticket to `blocked`. Independent tickets continue. The human is asked only when every remaining ticket is blocked.

**Enforced in CLI:** `./studio move … done` refuses without a QA PASS after the last green gate, and without a finish-gate PASS when the ticket has signed mock shots.

---

### Step 7: Docs & ADR sync

```bash
# if needed:
./studio adr <project> "<title>"
```

| Aspect | Description |
|--------|-------------|
| **Action** | update documentation, create/update ADRs |
| **Output** | updated docs, possibly new ADRs |
| **Responsible** | implementing agent |

**Checklist:**
- [ ] Affected definition files updated
- [ ] READMEs current
- [ ] ADRs created (if architecture decision)
- [ ] Decision records updated (if HITL)

---

### Step 8: Reuse review (library-first)

```bash
./studio library suggest <project> "<ticket topic>"
./studio library pull <project> billing button auth-login    # before implement. Do not pull packages/auth.
# after ticket — if generic:
./studio library promote <project> packages/billing --ticket <ID> [--force]
```

| Aspect | Description |
|--------|-------------|
| **Action** | Pull library boilerplate first; promote mutations if generic |
| **Output** | `docs/library-usage.json`, `docs/library-promotions.json` |
| **Responsible** | Implementing engineer + agent |

**Checklist:**
- [ ] Checked `./studio library list` / `suggest` before coding
- [ ] Product app has UI kit peers (`docs/setup/ui-kit.md`) before pulling styled components
- [ ] Pulled relevant library assets (not the `feature-gating` stub)
- [ ] If this ticket needs schema and the DB is reachable: agent ran migrate and INFORM’d — did not ask the human
- [ ] Is the **final** solution useful for other projects?
- [ ] Promoted with `--ticket` if yes; documented in ticket if no

**On promotion:**
```bash
./studio library promote demo packages/billing --ticket DEMO-0004
./studio library promote demo ui/components/atoms/Badge.tsx --ticket DEMO-0002
```

Moving to `done` without promotion logs **warns** if `packages/` or `ui/components/` changed.

---

### Step 9: Completion → status `done`

```bash
./studio move <project> TICKET-NNN done --reason "All 9 steps complete"
```

| Aspect | Description |
|--------|-------------|
| **Action** | close the ticket, update status |
| **Output** | ticket moved to `backlog/done/`, status.json updated |
| **Responsible** | Project Manager |

**Completion checklist:**
- [ ] All 9 steps documented
- [ ] All acceptance criteria met
- [ ] QA gate green
- [ ] Docs current
- [ ] status.json updated
- [ ] Commit done

---

## Ticket statuses

```
open ──▶ analyze ──▶ plan ──▶ design ──▶ implement ──▶ qa ──▶ review ──▶ reuse ──▶ done
                                                                      
         blocked ◀── (on problems) ──▶ (back to previous step)
```

| Status | Meaning |
|--------|---------|
| `open` | ticket created, waiting for analysis |
| `analyze` | being analyzed |
| `plan` | implementation being planned |
| `design` | design/architecture being defined |
| `implement` | code being written |
| `qa` | quality being checked |
| `review` | code review |
| `reuse` | reuse review |
| `done` | completed |
| `blocked` | blocked (waiting for decision/input) |

---

## Blocked tickets

When a ticket is blocked:

```bash
./studio move <project> TICKET-NNN blocked --reason "Waiting for ADR decision"
```

- The blocking reason is documented
- The ticket is discussed at grooming
- At grooming it is checked whether the blocker can be resolved

---

## References

- `.quinsy-studio/process/lifecycle.md` — phases
- `.quinsy-studio/process/gates.md` — QA gate in detail
- `.quinsy-studio/process/anti-slop.md` — anti-slop audit
- `.quinsy-studio/process/iterative-delivery.md` — sprint/board/grooming
- `./studio ticket <project> "<title>"` — create a ticket
- `./studio move <project> <id> <status>` — change status

## Composer-executable contract is mandatory (LO-0238)

- **PB-20260914-001** helpful=0 harmful=0 :: Every ticket must satisfy the composer-executable contract **before entering a sprint** — sprint scope approval is the enforcement point, not implement time. Required fields (see `knowledge-base/ticket-authoring-playbook.md`): verbatim target artifacts (`files:`), a literal runnable **Verify** block, **Do not touch**, and **Stop and ask if**; frontmatter `executable_by: composer|opus|human`. A ticket that cannot be executed by a small model without further conversation is not groomed — expand it or split it. Never groom XL into a sprint.

## Done means deployed for review (LO-0239, LO-0240)

- **PB-20260914-002** helpful=0 harmful=0 :: A UI ticket is not `done` until its work is **committed and pushed to the deploy-tracked branch** the human will review against. If the hosting platform auto-deploys from the main branch, push main when the ticket is done — otherwise sprint review sees stale production and feedback lands on the wrong version. Verify the review URL actually shows the ticket's change before requesting sprint review.

## Externally rendered output needs a manual pass (LO-0241)

- **PB-20260914-003** helpful=0 harmful=0 :: When a ticket's output renders in an external tool the QA gate cannot see (design-tool plugins, third-party canvases, emails, PDFs), automated checks are insufficient: a **manual pass in the target tool** is part of the ticket's Verify, and the receipt must record it. Do not mark such tickets done on gate-green alone.

## Shared model before parallel consumers (LO-0242)

- **PB-20260914-004** helpful=0 harmful=0 :: When two consumers render the same domain object (e.g. an HTML export and an external placer/plugin), extract the **shared model first** — one source of truth for structure and naming — before implementing either consumer. Duplicated ad-hoc models drift immediately and double every subsequent change.

## Refactors sweep their assertions; verify blocks are literal (LO-0249, LO-0250)

- **PB-20260914-005** helpful=0 harmful=0 :: When a refactor changes class names, tokens, or user-facing copy, sweep **test assertions in the same ticket** — stale assertions silently break the suite for the next ticket. Rename tickets are only done when the ticket's literal Verify command (e.g. `rg -c "<old names>"`) actually returns CLEAN; run the Verify block verbatim before claiming completion — partial renames (models done, services/jobs/tests not) are the common failure.

## Scope JSON is the approve source (LO-0251)

- **PB-20260914-006** helpful=0 harmful=0 :: `--approve-scope` tags tickets from `sprints/<sprint>/scope-proposal.json`, not the markdown proposal. After splitting an epic or editing the intended sprint list, re-run `./studio sprint` (or rewrite the JSON to match) **before** approve-scope. Approving a stale JSON recreates the parent epic as the sprint.

## Park parent epics before the first proposal (LO-0252)

- **PB-20260914-007** helpful=0 harmful=0 :: Set `sprint_deferred: true` on parent epics (XL / `ticket_type: epic`) **before** the first `./studio sprint` of a cycle. Children that are S/M and composer-executable are what get proposed. An un-deferred epic is a P0 magnet.

## Deltas

- **PB-20261012-001** helpful=0 harmful=0 :: **PB-20261012-002** helpful=0 harmful=0 :: MOVE_DONE flags newly added `[Nrem]` / `[Npx]` classNames. Moving a line counts as added. Use a scale utility or keep the original className line unchanged.
- **PB-20261008-001** helpful=0 harmful=0 :: Test helpers that stand in for primary keys must match the column type (UUID when the schema is UUID). Design-track and parked tickets stay out of an implementation sprint until that phase is open.
- **PB-20260916-007** helpful=0 harmful=0 :: After the core entity rename, new tables that store domain_id must foreign-key properties, not the domains view. Constraining domains fails because it is no longer a table.
- **PB-20260916-006** helpful=0 harmful=0 :: A light presentation island inside a dark (or mixed) theme must pin --ink (and related text tokens) on that island so inherited theme text-ink cannot flip the island pale. Do not rely on a parent html.dark token for type on a forced-light surface.
- **PB-20260916-005** helpful=0 harmful=0 :: Canvas (non-DOM) paint must follow html.dark the same way HTML chrome does. Resolve theme colors to hex from computed styles before stroke, fill, or title text. CSS variables never reach a canvas 2D API.
- **PB-20260916-003** helpful=0 harmful=0 :: needs_architecture tickets stay on the production stream until the architecture packet exists and architecture_status is approved. Execute must not offer IMPLEMENT on a pending architecture packet.
- **PB-20260916-002** helpful=0 harmful=0 :: infer_ticket_type treats fixture or identity swaps as feature, not design-pending ui-composition, even when the raw text also mentions a menu.
- **PB-20260916-001** helpful=0 harmful=0 :: When proposing sprint scope, sort --from-feedback tickets by newer ticket number first at the same priority. Older leftover P0 restyle work must not beat the feedback just captured this session.
- **PB-20260915-001** helpful=0 harmful=0 :: Ticket --from-feedback must put each Given/When/Then on its own AC bullet. Two clauses in one dash fail the sprint maturity check (needs at least two specific AC items) and gold-path work looks immature.
