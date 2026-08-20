# Quinsy Studio — Ticket Workflow

> **Sprint HITL (after gate 2):** use the [product backlog model](backlog-model.md) — `backlog/` → `implement/` → `done/`.
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
```

Move during sprint:

```bash
./studio move <project> TICKET-NNN implement
./studio move <project> TICKET-NNN done
```

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
| 9 | **Completion** | status `done`, update status.json |

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
- ❌ No code without a ticket
- ❌ No commit without green tests

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

**Rule:** `./studio gate <project>` must be green before a ticket is marked done.

**On failure:** the ticket goes back to step 4 (implementation)

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
./studio library pull <project> auth billing button    # before implement
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
- [ ] Pulled relevant stubs (auth, billing, UI atoms)
- [ ] Is the **final** solution useful for other projects?
- [ ] Promoted with `--ticket` if yes; documented in ticket if no

**On promotion:**
```bash
./studio library promote nudge packages/billing --ticket NUDG-0004
./studio library promote nudge ui/components/atoms/Badge.tsx --ticket NUDG-0002
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
