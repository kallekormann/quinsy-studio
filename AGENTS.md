# Quinsy Studio — AI Agent Contract

You operate **Quinsy Studio** in the IDE. Stay in context. Separate worlds. **Library-first.**

## Every turn (before session start or the user's ask)

A new chat bubble is **not** a new assignment while work is in flight.

```bash
./studio guard <p> "<verbatim user message>"
```

On `INBOX_ACK`: the note is already queued — one-line ACK, resume the same ACTION. Do not implement the note until after `MOVE_DONE` + drain. Only abort preempts. **Exception:** `STUDIO_META` (`HQ-T*`, `LO-NNNN`, `.quinsy-studio`, “quinsy-studio process”) is studio HQ — do not queue it on the product sprint inbox. **Exception:** `IDEATE` (`ideate`, `incubate`, `ideation`, or a section or dimension name while a session is open) is the research desk — if the session is waiting for a brief, ask once and do not search; after a brief, run `./studio ideate` through present in that turn, including shape (problem space, solution space, architecture, and experience), and do not call `execute`. Do not ask the human to continue between sections. Do not run `approve`, `reject`, `park`, or `promote` unless the human asked in this conversation. Builder time is not a ceiling: one solo builder, with AI agents for coding and design, ships in chunks of about two months. The first chunk is the MVP. Later chunks stay in the idea. Medicine and clinical care are out of reach (`--domain clinical` cannot validate). Other trades stay in reach. HITL replies when execute already says `STOP` (gates, **`approve-design` / `approve-arch`**, cadence review, “back on track”). Mid-sprint “looks good” on a **non-design** ticket is **not** HITL.

This is **studio-core** (`./studio guard`), not a project-local convention.

## Session start (mandatory)

```bash
./studio install                  # once after git clone (skip if node_modules exists)
./studio verify-worlds
./studio settings                 # HQ train ledger
./studio settings <project>     # product execute ledger (raise named keys on INFORM cost-cap)
./studio focus <project>          # or: ./studio adopt <p> --from <url-or-path> when the tree already has source
./studio execute <project>        # do NEXT; loop until ACTION is HITL — do not ask to continue
```

**Docker is required** (install Desktop if missing). Do **not** Read `.env` **values** — names only (`env.schema.json` and `*.env.example`). Desktop values live in gitignored `projects/<p>/.env`. Production values live in Coolify. `./studio env <p> up|migrate|dev --approve` injects the project file into Compose. One chat / IDE window per product (`parallel.max_projects`, default 5). HQ train/infusion is a **separate** session: product execute **INFORM**s open LO counts and must not steal the chat for `STUDIO_LO` mid-project. Plan: [.quinsy-studio/process/hq-isolation-sprints.md](.quinsy-studio/process/hq-isolation-sprints.md).

`./studio resume <project>` still prints a checklist. Prefer **execute**: one machine-readable step (`IMPLEMENT` / `GATE` / `VERIFY` / `MOVE_DONE` / `INFORM` / `STUDIO_LO` / `HITL`). Read the compact CARD (including **skills + playbooks**), and the full ticket `.md` only when the action is `IMPLEMENT`. Never dump the backlog into context.

On `HITL`: stop and wait — **gate 0**, **gate 1 architecture**, **gate 2a direction**, **gate 2b project kit** (sequential; `--gate 2` is refused), the batch **`approve-design --phase` / `approve-arch --phase`** after every packet in that phase is written, **`./studio env … --approve`**, **cadence review** (every N implementation phases), **tech-veto**, abort, or 3× QA fail. After gate 2b, `./studio sprint` opens the next phase: design, then architecture, then implementation. An empty phase is skipped in the same turn. Implementation only scopes tickets whose design and architecture are `approved` or `n/a`. One unsigned ticket does not freeze a ready sibling. Do **not** wait for a ticket ACK on feature work — receipt skill QA is the done bar. On `MOVE_DONE`, commit the **product** repo (`git -C projects/<p>`). Before cadence review, `./studio ship <p> --to dev`. **Never** auto-push `main` / production — HITL `./studio ship <p> --to main --approve`. Do not implement cadence-review **design** feedback. Reuse and sprint scope are **inform**.

**Sibling projects:** `./studio focus <p>` hides other `projects/*` from the agent. Never Read, copy, merge, or `git add` a sibling tree into the active project git. `CROSS_PROJECT` from guard means switch focus — do not pull the other product in.

**Existing codebase:** `./studio adopt <p> --from <url-or-path>` overlays studio docs without wiping source. Execute fills `docs/as-built/` (cite paths), then HITL gate 0. Do not `init`/`bootstrap` an empty scaffold over a live tree. See [brownfield-adopt.md](.quinsy-studio/process/brownfield-adopt.md).

On `INFORM`: do NEXT (inbox drain, reuse brief), then execute again — do not wait for a signature. **Exception:** `INFORM cost-cap` — stop stuffing files; raise the **named** key in `projects/<p>/docs/studio.settings.local.yaml` (product execute) or `.quinsy-studio/studio.settings.local.yaml` (train / STUDIO_LO).

On `STUDIO_LO`: only when the product loop is **idle**. Mid-sprint, harvest immediately and spawn `./studio train` in a **HQ session**; keep `IMPLEMENT` here. Infuse with `./studio infusion-delta` (no full-file rewrite), then `./studio train --done TR-NNNN`. Cite playbook bullets on the receipt (`./studio cite` / MOVE_DONE counters). Always pass `--lo LO-NNNN` when queueing train. Move LO to `backlog/done/`. Infusion-delta and HQ commits abort if a real project folder name appears outside provenance.

`./studio focus` will not rewrite isolation while another product holds an execute lease, unless `--force`. `./studio execute <p> --release` frees a slot. `./studio env <p> up|migrate|dev --approve` injects named vars; without `--approve` it exits. `./studio approve --gate N` refuses unless gate N-1 is approved.

Read: [agent-context.md](.quinsy-studio/process/agent-context.md) | [ticket-team-allocation.md](.quinsy-studio/process/ticket-team-allocation.md) | [library_registry.md](.quinsy-studio/studio-library/library_registry.md)

## Library-first (UI + code)

**Before writing new UI or package code:**

```bash
./studio library list
./studio library suggest <project> "auth button"
./studio library pull <project> auth tokens button
```

Use library artifacts as **boilerplate** — adapt tokens, config, business rules in the project. **Stubs** (`billing`, `feature-gating`) are **not pullable** — build in-project, then promote a working generic.
After the ticket is done, promote **only if the generic asset improved** (no client UI/tokens):

```bash
./studio library promote <project> packages/billing --ticket <ID> [--force]
```

On `./studio move <project> <ID> implement` you get a library hint.
**UI tickets:** design-track (new component, composition, marketing, workflow, IA) belong in a **design phase**. Team 10 writes every spec and in-context, project-token, all-state mock in that phase, then the human signs once with `./studio approve-design <p> --phase`. Each design ticket states `architecture delta: none` or names the architecture ticket. Commercial surfaces (landing, pricing, checkout, PLP, PDP) also load **Team 11** (`GD-001`/`GD-002`) and spec Growth intent. Do not HITL approve-design until those files exist. **All other UI/FE tickets** stay on the gate-2b design system (tokens + library) — no ticket ACK. If a primitive is missing, file a design-track ticket for the next design phase. Tailwind + studio-library — no hand-rolled modals.

**Project UI kit (setup, not later):** every product app that uses studio-library must have `radix-ui`, `class-variance-authority`, `clsx`, `tailwind-merge`, and `lucide-react` (plus `@headlessui/react` for Headless primitives). `./studio init` / `design` / `adopt` write `docs/setup/ui-kit.md`; the design prototype `package.json` includes them. Merge on `library pull`. Do not wait for a missing-module crash.

**Database migrations:** if you can reach the database (Compose via `./studio env <p> migrate --approve`, documented VPS), **you run** the project migrate command as sprint work. Inform the human that it ran. Do **not** Read `.env` **values**. Destructive reset is HITL. See [backend_playbook.md](.quinsy-studio/knowledge-base/backend_playbook.md).

On `./studio move … done` → warns if registry paths changed without promotion; **requires `./studio gate <project> --level 5` green** and a filled **execution receipt** (`./studio receipt`) with Plan, AC coverage, default-flow (LO-0051), and Skill QA / Design skill / Architecture skill. Level 2 lint-only is not enough.

**Studio library is studio-owned:** project tokens/UI are never merged into `.quinsy-studio/studio-library/` on gate 2b. Pull Headless primitives → adapt brand locally. **New behavior primitives** go in studio-library first ([component-creation-playbook.md](.quinsy-studio/knowledge-base/component-creation-playbook.md)); Headless UI primitives live under `ui/primitives/headless/`.

**Sprint HITL:** Never ticket cadence-review **design** ideas directly. Use `./studio feedback` → `clarify` → `ticket --from-feedback`. Those tickets wait for the next design or architecture phase. **After a phase starts:** no per-ticket ACK. **Human stops:** `approve-design --phase` / `approve-arch --phase`, then **cadence review** every N implementation phases. An infeasible design returns with `./studio approve-arch <p> <TICKET> --reject`. Backend-only and off-cadence batches inform and continue to retro. Hygiene: `./studio sprint --kind hygiene` (outside the train; it does not count toward cadence). **During review:** capture feedback only. **Sprint planning:** `./studio sprint` opens the next phase and skips an empty one → `--approve-scope` → groom → execute.

## Two worlds — never mix

| World | Path | Git |
|-------|------|-----|
| Studio HQ | `.quinsy-studio/` | quinsy-studio root |
| Project | `projects/<name>/` | **separate repo** |
| Siblings | other `projects/*` | **opaque** after `./studio focus` |

`./studio verify-worlds` — must pass before project work. `./studio focus <p>` hides sibling trees from the agent. Never Read, copy, or commit another product into the active git. Switch products with a new `./studio focus`.

## Pre-implementation gates

| Gate | Approves | Tickets? |
|------|----------|----------|
| 0 | PRD + definitions (HITL) | No |
| 1 | Architecture after PRD (HITL) | No — design track starts after this |
| 2a | Design direction: human interview + signed DESIGN.md (HITL). Blocks prototype. | No |
| 2b | Project kit: CSS tokens, coded A/M/O, sticker all-states (HITL). Look stays in the project. | After approve: tickets / sprints |
| Milestones | Version plan (`docs/phases/`) | Inform; don’t hard-block backend **after** gates 0–2b |
| Milestone review | Version complete (M0, M1, …) | Yes — before next milestone backlog |

```bash
./studio approve <p> --gate 2a   # discovery + DESIGN.md (no indigo stub, uniqueness required)
./studio approve <p> --gate 2b   # project kit; does not promote look into studio-library
# ./studio approve <p> --gate 2  # refused — use 2a then 2b
./studio approve-design <p> <TICKET>   # HITL after spec + all-state mocks exist
./studio ia-audit <p> <TICKET>         # IA nav counts before approve-design (ia-navigation)
./studio approve-arch <p> <TICKET>     # HITL after docs/architecture/<TICKET>.md exists
./studio train --purge-empty            # close blank-observation train jobs
./studio sprint <p> --kind hygiene      # lint/debt batch (does not count toward cadence)
./studio approve <p> --milestones   # approve milestone roadmap (after docs/phases/ drafted)
./studio library promote-design <p> [--force]
```

After `--milestones`, agent writes tickets for the active milestone only, then sprint planning begins.

## Context & drift

```bash
./studio guard <project> "user request"
./studio focus <project> && ./studio resume <project>   # drift recovery
```

## Sprint HITL (after gate 2b)

**Mid-sprint:** agent implements autonomously — human does not approve ticket-by-ticket. Do not wait for “looks good” after `MOVE_DONE`.

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

## Amendment intake (strategic direction, post gate 2b)

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
