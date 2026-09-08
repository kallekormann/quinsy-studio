# Quinsy Studio — Learning Loop

> The studio learns from its mistakes. Every mistake is analyzed and turned into improvements.

## Core principle

```
Learning identified → classify → inbox + LO (same session) → train in parallel → CHANGELOG
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
5. **Infusion:** HQ playbooks/skills must not introduce project folder names outside provenance / `source:` lines (`./studio infusion` reports hits).

**HQ LO vs project log (examples):**

| Belongs in studio HQ | Stays in `projects/<p>/docs/studio-learnings-local.md` |
|----------------------|--------------------------------------------------------|
| Guard must not queue HITL “approved” / review approve | Do not sprint tickets AFFI-0007 until vendor X signs off |
| Close UI sprints (review → reuse → retro) when the last ticket is done | This sprint still had vendor ingest tickets with no publisher site |
| Shared CSS must be in the host stylesheet scan so chrome cannot ship unstyled | Keep magazine `@source` in this app’s public host DoD |
| Reuse harvest: generalize `packages/auth` | Copy this product’s first-brand token kit into the library |

A five-word incident is **not** a principle. Retro bullets that name a ticket, sprint, vendor, or surface go local. Rewrite into a rule that the *next* product would still need, or do not open an LO.

```
raw observation → generalize title → portable?
  ├─ no  → projects/<p>/docs/studio-learnings-local.md
  ├─ yes, playbook-only → LO (train_skills: [])
  └─ yes, skill gap → LO + ./studio train <skill-id> --topic "<principle>"
```

Each portable harvest:

1. **Classifies** into an infusion bucket (package, ui-component, design, ux, ia, layout, usability, frontend, backend, database, security, process, tooling)
2. **Appends** `.quinsy-studio/knowledge-base/learnings/inbox.md` (generic observation; `--source` is provenance only)
3. **Opens** a compact LO-* with `infusion_kind`, `infusion_path`, and `train_skills`

Then `./studio execute <project>` **continues product IMPLEMENT**. Open LOs with `train_skills` queue `./studio train` in parallel. `STUDIO_LO` only when the product loop is idle. HITL gate 0, UI sprint-review, and design-approve still win.

Do **not** copy project UI/tokens into `studio-library/`. Promote reusable assets via `./studio library promote` — learnings are principles/skills, not product dumps.

```bash
./studio learn "<portable principle>" --signal <signal> --source <project>
./studio execute <project>   # ACTION IMPLEMENT (train sidecar only if train_skills set)
./studio train BE-001 --from mistake --topic "<portable principle>"
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

Project sprint planning is **not** blocked by open LO-* tickets. Harvest is immediate; `./studio train` infuses in parallel while product execute continues IMPLEMENT.

```
Project work identifies a learning
    → harvest (inbox + classified LO) in the same session
    → ./studio execute  → ACTION IMPLEMENT  (TRAIN sidecar)
    → train agent infuses in .quinsy-studio/ (or STUDIO_LO when idle)
    → continue project tickets / next sprint
```

**Infusion targets** (generalize — never copy client project names into studio docs):

| Kind | Infuse into |
|------|-------------|
| `ui-component` | `studio-library/ui/components/` + atomic-design playbook (LO, not project copy) |
| `package` | `studio-library/packages/` |
| `design` / `layout` | `knowledge-base/design_playbook.md` |
| `ux` / `usability` | `knowledge-base/design-science-playbook.md` |
| `ia` | `knowledge-base/contextual-ia-playbook.md` |
| `frontend` / `backend` / `database` / `security` | matching playbooks / PE–BE skills |
| `process` | `process/` |
| `tooling` / `gate-fail` | `studio-tools/` |

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
| Before coding | `./studio library pull <project> auth billing …` |
| Gate 2 (design) | `./studio approve --gate 2` → `promote-library` |
| After ticket (generic code) | `./studio library promote <project> <path> --ticket <id>` |

Registry: [../studio-library/library_registry.md](../studio-library/library_registry.md)

Process/skill improvements still use **LO-*** items and `./studio learn`.

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
