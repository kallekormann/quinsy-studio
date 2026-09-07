# Quinsy Studio — Learning Loop

> The studio learns from its mistakes. Every mistake is analyzed and turned into improvements.

## Core principle

```
Learning identified → classify → inbox + LO (same session) → execute STUDIO_LO → CHANGELOG
```

Do **not** wait for a human `./studio learn` prompt, retro close, or the next project sprint. If learnings pile up, the originating context is gone and the next project repeats the mistake.

---

## Immediate harvest

The moment a learning is identified, studio HQ captures it:

| Trigger | What happens |
|---------|----------------|
| `./studio learn "..."` | Classify → inbox + LO |
| `./studio retro --complete` | Auto-harvest “went badly” / “improve” bullets (no learn prompts to run later) |
| `./studio reuse` | Unpromoted `packages/` / `ui/components/` → classified LOs |
| 3rd gate fail | Auto-harvest `signal: gate-fail` (kind: tooling) |

Each harvest:

1. **Classifies** into an infusion bucket (package, ui-component, design, ux, ia, layout, usability, frontend, backend, database, security, process, tooling)
2. **Appends** `.quinsy-studio/knowledge-base/learnings/inbox.md` (generic observation, no client product names)
3. **Opens** a compact LO-* with `infusion_kind` + `infusion_path`

Then `./studio execute <project>` returns **`STUDIO_LO` before the next project `IMPLEMENT`** (in-progress tickets still finish VERIFY/GATE/DEBUG/MOVE_DONE). HITL gates 0–2, sprint-review, and design-approve still win.

Do **not** copy project UI/tokens into `studio-library/`. The inbox + LO is the capture; the agent **generalizes** the rule or extracts a library asset on `STUDIO_LO`.

```bash
./studio learn "<title>" --signal <signal> --source <source>
./studio execute <project>   # ACTION STUDIO_LO — infuse now
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

Project sprint planning (`./studio sprint <project>`) **and the next project IMPLEMENT** are blocked while open **LO-*** tickets exist. Harvest is immediate; execute returns `STUDIO_LO` while the originating context is still in session.

```
Project work identifies a learning
    → harvest (inbox + classified LO) in the same session
    → ./studio execute  → ACTION STUDIO_LO  (implement in .quinsy-studio/)
    → ./studio infusion (gate clear)
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
