# Quinsy Studio — AI Agent Contract

You operate **Quinsy Studio** in the IDE. Stay in context. Separate worlds. **Library-first.**

## Session start (mandatory)

```bash
./studio install                  # once after git clone (skip if node_modules exists)
./studio verify-worlds
./studio focus <project>          # or: ./studio adopt <p> --from <url-or-path> when the tree already has source
./studio execute <project>        # do NEXT; loop until ACTION is HITL — do not ask to continue
```

`./studio resume <project>` still prints a checklist. Prefer **execute**: one machine-readable step (`IMPLEMENT` / `GATE` / `VERIFY` / `MOVE_DONE` / `STUDIO_LO` / `HITL`). Read the compact CARD, and the full ticket `.md` only when the action is `IMPLEMENT`. Never dump the backlog into context.

On `HITL`: stop and wait (gates 0–2 including **as-built** on adopted repos, design-approve, sprint scope, sprint review, next-sprint). Do not implement sprint-review feedback.

**Existing codebase:** `./studio adopt <p> --from <url-or-path>` overlays studio docs without wiping source. Execute fills `docs/as-built/` (cite paths), then HITL gate 0. Do not `init`/`bootstrap` an empty scaffold over a live tree. See [brownfield-adopt.md](.quinsy-studio/process/brownfield-adopt.md).

On `STUDIO_LO`: implement in `.quinsy-studio/` only, CHANGELOG, move LO to `backlog/done/`, then `./studio execute` again. Learnings are harvested **when identified** (learn / retro `--complete` / reuse / 3rd gate fail) — execute returns `STUDIO_LO` **before the next project ticket**, including mid-sprint. Do not leave LOs piled for a later human trigger.

Read: [agent-context.md](.quinsy-studio/process/agent-context.md) | [ticket-team-allocation.md](.quinsy-studio/process/ticket-team-allocation.md) | [library_registry.md](.quinsy-studio/studio-library/library_registry.md)

## Library-first (UI + code)

**Before writing new UI or package code:**

```bash
./studio library list
./studio library suggest <project> "auth billing button"
./studio library pull <project> auth billing tokens button
```

Use library artifacts as **boilerplate** — adapt tokens, config, business rules in the project.  
After the ticket is done, if changes are generic:

```bash
./studio library promote <project> packages/billing --ticket <ID> [--force]
```

On `./studio move <project> <ID> implement` you get a library hint.  
**UI tickets:** design-track types require Team 10 design spec + human `./studio approve-design <p> <ID>` before implement. **All UI/FE tickets:** Tailwind CSS + studio-library ([ui/docs/README.md](.quinsy-studio/studio-library/ui/docs/README.md)) — no hand-rolled modals or unstyled form controls.
On `./studio move … done` → warns if registry paths changed without promotion; **requires `./studio gate <project> --level 5` green** and a filled **execution receipt** (`./studio receipt`) with Plan, AC coverage, and default-flow (LO-0051). Level 2 lint-only is not enough.

**Studio library is studio-owned:** project tokens/UI are never merged into `.quinsy-studio/studio-library/` on gate 2. Pull library → adapt brand locally. **New components** go in studio-library first ([component-creation-playbook.md](.quinsy-studio/knowledge-base/component-creation-playbook.md)); Headless UI primitives live under `ui/primitives/headless/`.

**Sprint HITL:** Never ticket sprint-review ideas directly. Use `./studio feedback` → `clarify` → `ticket --from-feedback`. **Autonomous mid-sprint:** agent implements all groomed sprint tickets without human checkpoints. **Human joins at sprint review** when all sprint tickets are `done`. **During review:** capture feedback only — never implement in project code until the next sprint. **Milestones:** after gate 2, agent drafts `docs/phases/` roadmap → human approves → tickets for active milestone only → sprints. **Milestone review** when all milestone tickets are done, before next milestone backlog. **Product backlog** lives in `projects/<p>/backlog/*.md` (not `open/`). **Sprint planning:** `./studio sprint` proposes scope → human `./studio sprint --approve-scope` → `./studio groom --approve`.

## Two worlds — never mix

| World | Path | Git |
|-------|------|-----|
| Studio HQ | `.quinsy-studio/` | quinsy-studio root |
| Project | `projects/<name>/` | **separate repo** |

`./studio verify-worlds` — must pass before project work.

## Pre-implementation gates

| Gate | Approves | Tickets? |
|------|----------|----------|
| 0 | PRD + definitions | No |
| 1 | Architecture | No |
| 2 | Design + mocks | No — **milestone roadmap** next |
| Milestones | Version plan (`docs/phases/`) | Yes — before sprints |
| Milestone review | Version complete (M0, M1, …) | Yes — before next milestone backlog |

```bash
./studio approve <p> --gate 2    # validates design + refreshes library catalog (no project → library merge)
./studio approve-design <p> <TICKET>   # HITL after Team 10 design spec (UI tickets)
./studio approve <p> --milestones   # approve milestone roadmap (after docs/phases/ drafted)
./studio library promote-design <p> [--force]
```

After `--milestones`, agent writes tickets for the active milestone only, then sprint planning begins.

## Context & drift

```bash
./studio guard <project> "user request"
./studio focus <project> && ./studio resume <project>   # drift recovery
```

## Sprint HITL (after gate 2)

**Mid-sprint:** agent implements autonomously — human does not approve ticket-by-ticket.

**Sprint review:** when all sprint tickets are `done`, human reviews shipped work; feedback becomes tickets only after clarification.

```bash
./studio review <project>                          # status brief for human
./studio feedback <project> "idea"                 # raw — not a ticket
./studio clarify <project> FB-001 ... --approve    # executable draft
./studio ticket <project> "..." --from-feedback FB-001
./studio review <project> --approve
./studio reuse <project> && ./studio reuse <project> --approve   # mandatory library review
./studio groom <project> && ./studio retro <project> && ./studio sprint <project>
```

See [human-in-the-loop.md](.quinsy-studio/process/human-in-the-loop.md#sprint-cadence-hitl-after-gate-2).

## Amendment intake (strategic direction, post gate 2)

**Sprint feedback** = small, concrete ideas. **Amendments** = conceptual direction → milestone + ticket breakdown.

```bash
# Human drops brief: intake/amendments/<project>/amendment_01.md
./studio amend <project> intake/amendments/<project>/amendment_01.md
./studio amendments <project>
./studio approve <project> --amendment AM-001
./studio approve <project> --milestones   # if roadmap changed
```

Agent produces `projects/<p>/docs/amendments/AM-NNN-*/` (vision, requirements, UX/FE/BE arch, milestone roadmap, ticket drafts). No implementation until approved. See [amendment-intake.md](.quinsy-studio/process/amendment-intake.md).

## Reference

- [GETTING_STARTED.md](.quinsy-studio/GETTING_STARTED.md)
- `projects/<p>/docs/library-usage.json` — what was pulled
- `projects/<p>/docs/library-promotions.json` — what was promoted
