# Quinsy Studio — Learning Loop

> The studio learns from its mistakes. Every mistake is analyzed and turned into improvements.

**Loop closes on a store (LO-0231):** infusion is a confirmed **delta** into a named playbook (`infusion_path`), merged without an LLM rewrite. See [agentic-loop-playbook.md](../knowledge-base/agentic-loop-playbook.md).

## Core principle

```
Learning identified → classify → inbox + LO (same session) → INFORM product chat + `./studio train` in a HQ session → CHANGELOG
```

Do **not** wait for a human `./studio learn` prompt, retro close, or the next project sprint. If learnings pile up, the originating context is gone and the next project repeats the mistake.

---

## Immediate harvest

The moment a learning is identified, studio HQ captures it **only if portable**:

| Trigger | What happens |
|---------|----------------|
| `./studio learn "..."` | Portability gate → classify → inbox + LO (or project-local log) |
| `./studio retro --complete` | Auto-harvest “went badly” / “improve” bullets through the same gate |
| `./studio reuse` | Unpromoted `packages/` / `ui/components/` → classified LOs |
| 3rd gate fail | Auto-harvest `signal: gate-fail` (kind: tooling) |

### Portability gate (required)

Before an LO or train job is created:

1. **Rewrite** product brands / project folder names out of the title (e.g. stock-media provider, not a single product’s tab name).
2. **Portability test:** would another product still benefit from the *principle* alone? If the title still needs project nouns, or is incident-shaped → **do not** open an LO.
3. **Project-local log:** dropped items go to `projects/<p>/docs/studio-learnings-local.md` (provenance only).
4. **Train only on skill gaps:** LO frontmatter `train_skills: [...]`. Empty → playbook/process infusion only (no train queue).
5. **Infusion:** HQ playbooks/skills must not contain product folder names or product ticket IDs, provenance lines included (`./studio verify-abstraction` reports hits).

**HQ LO vs project log (examples):**

| Belongs in studio HQ | Stays in `projects/<p>/docs/studio-learnings-local.md` |
|----------------------|--------------------------------------------------------|
| Guard must not queue HITL “approved” / review approve | Do not sprint ticket <ticket> until vendor X signs off |
| Close UI sprints (review → reuse → retro) when the last ticket is done | This sprint still had vendor ingest tickets with no publisher site |
| Shared CSS must be in the host stylesheet scan so chrome cannot ship unstyled | Keep magazine `@source` in this app’s public host DoD |
| Public chrome must not list destinations that 404 (portable nav DoD) | Named section labels that 404 in this brand’s masthead |
| Public document route must serve operator Save; no silent fixture when a live id exists | This brand’s article still shows fixture copy after Save |
| Reuse harvest: generalize `packages/auth` | Copy this product’s first-brand token kit into the library |

A five-word incident is **not** a principle. Retro bullets that name a ticket, sprint, vendor, host, or surface go local. `when` / `before` / `after` / `chrome` / `inbox` alone are **not** enough to enter HQ. Rewrite into a must/should/never/prefer rule that the *next* product would still need, or do not open an LO.

```
raw observation → generalize title → portable?
  ├─ no  → projects/<p>/docs/studio-learnings-local.md
  ├─ yes, playbook-only → LO (train_skills: [])
  └─ yes, skill gap → LO + ./studio train <skill-id> --from lo --topic "<principle>" --lo LO-NNNN
```

Each portable harvest:

1. **Classifies** into a domain/topic (`knowledge-base/learnings/<domain>/<topic>.md`) plus the matching playbook/skill
2. **Appends** the **open** queue `.quinsy-studio/knowledge-base/learnings/inbox.md` (generic observation; the `--source` product stays in the local LO, never in inbox.md)
3. **Writes** the principle into the topic file and refreshes `learnings/index.md`
4. **Opens** a compact LO-* with `infusion_kind`, `infusion_path` (topic file), and `train_skills`

`inbox.md` is not the long-term store. Infused/stale rows are archived to `learnings/archive/inbox-YYYY-MM.md`. Find rules with `./studio learn-find "<topic>"` or the CARD's domain README. IMPLEMENT must not Read `inbox.md`.

Then `./studio execute <project>` **continues the current phase**. Open LOs with `train_skills` queue `./studio train` in a **HQ session**. **INFORM** the open HQ LO count on the execute CARD; do **not** infuse playbooks from the product chat. `STUDIO_LO` only when the product loop is idle (`implementation_in_flight` is false). HITL gate 0, the batch `approve-design --phase` / `approve-arch --phase`, and cadence review still win. `./studio train --purge-empty` closes jobs written without an LO observation.

Do **not** copy project UI/tokens into `studio-library/`. Promote reusable assets via `./studio library promote` — learnings are principles/skills, not product dumps.

```bash
./studio learn "<portable principle>" --signal <signal> --source <project>
./studio execute <project>   # ACTION IMPLEMENT (train sidecar only if train_skills set)
./studio train BE-001 --from lo --topic "<portable principle>" --lo LO-NNNN
```

### Signals

| Signal | Description | Action |
|--------|-------------|--------|
| `gate-fail` | gate check failed | review gate criteria |
| `rework` | work had to be redone | analyze the process step |
| `tooling-gap` | tooling was missing or insufficient | extend CLI/tooling |
| `design-gap` | design specification was insufficient | improve the design process |
| `process-gap` | process step was unclear | update process docs |
| `knowledge-gap` | knowledge was missing | extend the team skill |
| `sloppy-code` | AI slop detected | tighten anti-slop rules |
| `slow-gate` | gate check took too long | optimize the gate |

### Learning item format

```markdown
---
id: LO-NNNN
title: <title>
status: open | in-progress | done
signal: <signal>
source: <source>
infusion_kind: layout | ui-component | package | process | tooling | …
infusion_path: knowledge-base/design_playbook.md
train_skills: [UX-003, FE-002]   # empty [] = playbook-only, no train queue
priority: P0-P3
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# LO-NNNN — <title>

## Observation
What happened / what is missing?

## Impact
What was the consequence (rework, uncertainty, quality risk)?

## Proposal
How should process / skill / tooling be improved?

## Status
- [ ] Discussed in the meta-retro
- [ ] Implemented (CHANGELOG.md entry, version updated)
```

---

## List learning items

```bash
./studio learn-list
```

Shows all open learning items.

---

## Meta-retrospective

```bash
./studio retro <project>              # scaffold project retro (status: pending)
./studio retro <project> --complete   # validate filled retro → status: done
./studio infusion                     # verify open LO-* tickets before next project ticket
```

### Studio Infusion Gate (mandatory)

Project sprint planning is **not** blocked by open LO-* tickets. Harvest is immediate; `./studio train` infuses in a HQ session while product execute continues IMPLEMENT.

```
Project work identifies a learning
    → harvest (inbox + classified LO) in the same session
    → ./studio execute  → ACTION IMPLEMENT  (TRAIN sidecar)
    → ./studio infusion-delta --op add …   (never rewrite the whole playbook)
    → ./studio train --done TR-NNNN
    → continue project tickets / next sprint
```

**Infusion targets** (generalize — never copy client project names into studio docs):

| Kind | Durable store | Also infuse |
|------|----------------|-------------|
| `ui-component` / `package` | `knowledge-base/learnings/library/` | studio-library + atomic-design / registry |
| `design` / `layout` / `ux` / `ia` | `knowledge-base/learnings/design/` | matching design playbooks / UX skills |
| `frontend` / `backend` / `database` / `security` | `knowledge-base/learnings/frontend/` or `backend/` | matching playbooks / PE–BE skills |
| `process` / `tooling` | `knowledge-base/learnings/process/` | `process/` + studio-tools / SO skills |

Signals still map to these kinds (`design-gap` → design, `library-gap` → package or ui-component, `gate-fail` → tooling).

Signals still map to these kinds (`design-gap` → design, `library-gap` → package or ui-component, `gate-fail` → tooling).

See [studio-abstraction.md](studio-abstraction.md) — learnings cite `--source <project>`; fixes use `<project>` placeholders.

**LO titles & proposals (LO-0040):** Write the **general rule** (reuse ladder, pattern name, archetype option). Use the originating sprint only as `--source` / Observation context — not as the ticket title or the primary DoD (“fix surface A to match surface B”).

### Flow

1. **Harvest immediately** (not a later Phase 6 batch)
   - Inbox: `knowledge-base/learnings/inbox.md`
   - Open LOs from `./studio learn-list`
   - Retro `--complete`, reuse scan, 3rd gate fail
   - **Route kinds:** design / ux / ia / layout / package / tooling → matching infusion path **in this session**

2. **Skill review**
   - Every team skill is reviewed
   - Collect quality signals
   - Identify improvements

3. **Decisions**
   - What will be changed?
   - What will be kept?
   - Prioritization

4. **Action items**
   - Concrete changes
   - Assign owner
   - Set deadline

5. **CHANGELOG**
   - Every change is documented
   - Update the version

### Retro template

```markdown
# Meta-Retro — YYYY-MM-DD

## Incoming learning items
- LO-0000: ...

## Skill review
| Skill | Quality signal | Action |
|-------|----------------|--------|
| ... | ... | ... |

## Decisions
- ... (every change → CHANGELOG.md entry)

## Action items
- [ ] ... (owner: ...)
- [ ] ... (owner: ...)
```

---

## Global loop: studio library

Reusable **UI and code** flow from projects into `.quinsy-studio/studio-library/`:

| When | Command |
|------|---------|
| Before coding | `./studio library pull <project> tokens button …` (not stubs). Kit peers in the app first. |
| Gate 2b (project kit) | `./studio approve --gate 2b` — look stays in the project; no `promote-library` |
| After ticket (generic code) | `./studio library promote <project> <path> --ticket <id>` |

Registry: [../studio-library/library_registry.md](../studio-library/library_registry.md)

Process/skill improvements still use **LO-*** items and `./studio learn`.

**Harvest is part of done.** A ticket that builds a capability another product can use must leave one of these on the receipt:

- `./studio library promote` for generic code. Strip the project's color, type, and copy. Auth screens promote the structure and the variants (sign in, invite-only account, password). The brand stays in the project.
- `./studio learn` when the lesson is a principle and there is no module yet.

Capabilities that always take this path: realtime, collaboration, object storage, and authentication. Skipping both needs a receipt line that says why the work cannot leave the product. Product look is never promoted. Infusion of the learning happens in an HQ session, not by pausing the product sprint.

---

## Maintain the CHANGELOG

Every change to the studio is documented in the CHANGELOG:

```markdown
## [1.1.0] — 2026-08-21

### Changed
- Gate check optimized (30% faster)
- Anti-slop rules tightened (new rule: C5)

### Added
- New command: `./studio audit <project>`
- Team skill 07: anti-slop section extended

### Fixed
- Gate history bug fixed
```

---

## Integration

The learning loop is a **continuous process**:

```
┌─────────────────────────────────────────────────────────┐
│                 LEARNING LOOP                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. Work                                                │
│     └─▶ mistakes happen                                 │
│                                                         │
│  2. Create a learning item                              │
│     └─▶ `./studio learn "..." --signal ...`            │
│                                                         │
│  3. Meta-retro                                          │
│     └─▶ `./studio retro <project>`                     │
│                                                         │
│  4. Implement the improvement                           │
│     └─▶ adjust process/tool/skill                      │
│                                                         │
│  5. Update the CHANGELOG                                │
│     └─▶ version bump                                    │
│                                                         │
│  6. Back to 1                                           │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## References

- `.quinsy-studio/process/iterative-delivery.md` — sprint/retro
- `.quinsy-studio/process/gates.md` — gate definitions
- `CHANGELOG.md` — change history
