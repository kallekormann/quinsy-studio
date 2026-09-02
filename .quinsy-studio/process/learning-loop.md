# Quinsy Studio — Learning Loop

> The studio learns from its mistakes. Every mistake is analyzed and turned into improvements.

## Core principle

```
Mistake → Learning item → Meta-retro → Improvement → CHANGELOG
```

---

## Capture learning items

```bash
./studio learn "<title>" --signal <signal> --source <source>
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
./studio infusion                     # verify open LO-* tickets before next project sprint
```

### Studio Infusion Gate (mandatory)

Project sprint planning (`./studio sprint <project>`) is **blocked** while open **LO-*** tickets exist in `.quinsy-studio/backlog/open/`.

```
Project sprint review
    → ./studio learn (capture signals)
    → ./studio retro --complete (filled retro)
    → Implement LO-* in studio HQ (process / skills / tools / library)
    → ./studio infusion (gate clear)
    → ./studio sprint <project> (next project sprint)
```

**Infusion targets** (generalize — never copy client project names into studio docs):

| Signal | Infuse into |
|--------|-------------|
| `design-gap` | knowledge-base/, teams/10/skills/, design-spec-template |
| `process-gap` | process/, human-in-the-loop.md |
| `tooling-gap` | studio-tools/, CLI |
| `knowledge-gap` | playbooks, skill-registry |
| `library-gap` | studio-library/ + promote from project |

See [studio-abstraction.md](studio-abstraction.md) — learnings cite `--source <project>`; fixes use `<project>` placeholders.

**LO titles & proposals (LO-0040):** Write the **general rule** (reuse ladder, pattern name, archetype option). Use the originating sprint only as `--source` / Observation context — not as the ticket title or the primary DoD (“fix surface A to match surface B”).

### Flow

1. **Collect learning items**
   - Open LOs from `./studio learn-list`
   - Feedback from sprint retros
   - Gate error analysis
   - **Route signals:** `design-gap` / `process-gap` / `tooling-gap` from project retros → open or update LO ticket before next project sprint

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
