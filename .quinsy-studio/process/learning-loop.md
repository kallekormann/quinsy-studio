# Quinsy Studio — Learning Loop

> The studio learns from its mistakes. Every mistake is analyzed and turned into improvements.

**Loop closes on the file (LO-0231):** infusion is a confirmed **delta** into the named target (`infusion_path`), merged without an LLM rewrite. See [agentic-loop-playbook.md](../knowledge-base/agentic-loop-playbook.md).

## Core principle

```
deviation seen → candidate LO → verdict: project or studio → (studio) next + target → TRAIN_DUE
    → training chat: ## Impact → low: infuse / high: human --approve or --defer
    → infusion-delta --lo writes the PB- bullet into the real file → CHANGELOG → train --done
```

A lesson is finished when **the file the next project follows has changed**. There is no catalog. The LO ticket is a local work order (gitignored); the committed result is one `PB-YYYYMMDD-NNN` bullet in a playbook under `knowledge-base/`, a `process/` file, a skill under `teams/`, a template, or a tool.

Do **not** wait for a human prompt or the next project sprint. The product agent captures, judges, and informs; the training chat applies.

---

## 1. Capture — every deviation becomes a candidate

| Trigger | What happens |
|---------|----------------|
| `./studio approve <p> --gate N` after **≥2** `## Gate N` entries in `docs/phases/revisions.md` | A candidate LO opens before the signature, quoting each round's feedback. The question it carries: did the packet change because of this product, or because the studio default was wrong? |
| `./studio retro <p> --complete` | Every filled "went badly" / "improve" bullet becomes a candidate (once per sprint) |
| `./studio approve-design --reject --reason <code>`, finish-gate HOLD, design feedback | Candidate with `assumed` = the rule stem, `signed` = the human's note |
| `./studio reuse` | Unpromoted `packages/` / `ui/components/` → candidates |
| 3rd gate fail | Candidate with `signal: gate-fail` (kind: tooling) |
| `./studio learn "<rule>"` | Manual candidate |

The portability gate still runs first (product nouns, incident shape, rule cue). What fails it goes to `projects/<p>/docs/studio-learnings-local.md` and never opens an LO.

Every LO carries a `## Lesson` block:

```markdown
## Lesson

- **assumed:** what the studio process, template, or default said
- **signed:** what the human finally accepted
- **verdict:** project | studio — one sentence why
- **next:** the rule, written as the bullet that goes into the studio file
- **target:** `process/… | knowledge-base/….md | teams/…/skills/….md | studio-templates/… | studio-tools/…`
```

A candidate has `needs_verdict: true` and placeholders. **`retro --complete` refuses while any candidate has no verdict.** The product agent answers:

```bash
./studio learn LO-NNNN --verdict studio  --reason "…" --assumed "…" --signed "…" --next "<rule>" [--target <file>]
./studio learn LO-NNNN --verdict project --reason "…" --assumed "…" --signed "…"
```

- `verdict: project` → the line goes to `projects/<p>/docs/studio-learnings-local.md` with its reason; the LO is removed. The human can overrule from the TRAIN_DUE list (`./studio train --promote <p> --topic "<title>"`).
- `verdict: studio` → `next` must pass the portability gate; `target` must be a real file under `.quinsy-studio/` and never under `knowledge-base/learnings/`. The default target comes from the kind (`KIND_MAP` playbook: design → `design_playbook.md`, tooling → `process/gates.md`, process → `process/learning-loop.md`, …).

## 2. Inform — the product agent tells the human a training session is due

`retro --complete` ends with a **TRAIN_DUE** block; the execute CARD (`INFORM:` line, also on HITL cards), `./studio status <p>`, `./studio settings`, `./studio learn-list`, and `./studio infusion` print it:

```
TRAIN_DUE — 2 studio lesson(s) wait for a training chat. Say "run training" in a studio chat.
  Deferred (you said wait): …                 ← first, with --reopen
  Ready for training: LO-NNNN [high] next → target
  Need a verdict: LO-NNNN …                   ← product agent still owes the answer
  Judged project-specific (overrule with ./studio train --promote …): title — reason
```

`run training` in a chat is `STUDIO_META` for the guard: it never lands on a product sprint inbox. `STUDIO_LO` on the execute card appears only when the product loop is idle. The product chat never edits playbooks.

## 3. Impact — the training chat decides how much the studio moves

```bash
./studio train LO-NNNN
```

1. Refuses without a verdict.
2. Writes a `## Impact` block into the LO on first run; the agent fills it: **files** (and which gates/commands read them), **in-flight** (would a running sprint behave differently on the next execute), **compliance** (do signed packets, templates, or library assets become non-compliant), **pro**, **contra**, **severity**.
3. The **severity floor** comes from the target path: `process/`, `studio-tools/`, `studio-templates/`, `teams/**/skills/` → **high**; a `knowledge-base/*.md` playbook → **low**. The agent may raise, never lower.
4. **Low** → infuse now (INFORM). **High** → the card prints pro/contra and stops: `./studio train LO-NNNN --approve` or `./studio train LO-NNNN --defer --reason "…"`. Deferred LOs move to `backlog/deferred/`, stay first in every TRAIN_DUE list, and come back with `--reopen`.

## 4. Close — the lesson is in the file or the LO stays open

```bash
./studio infusion-delta --lo LO-NNNN --path <target> --op add --body "assumed: … signed: … next: …"
# CHANGELOG.md line naming the PB- id
./studio verify-abstraction
./studio train --done LO-NNNN
```

- `infusion-delta --lo` refuses a body without `assumed:` / `signed:` / `next:`, a path that differs from the LO target, and a high-impact LO that is not approved. It records the PB- id on the LO.
- `train --done LO-NNNN` refuses unless the target file contains that PB- id, `CHANGELOG.md` names it, and `verify-abstraction` is clean. Only then does the LO move to `backlog/done/`.
- Find infused rules later: `./studio learn-find "<topic>"` searches PB- bullets in `knowledge-base/*.md`, `process/*.md`, `teams/**/skills/*.md`. Design specs and milestone reviews cite those PB- ids in `## Catalog applied`; LO- ids do not count.

**Not in git:** `backlog/`, `retros/`, `sprints/`, `.train-queue.json`, and the retired `knowledge-base/learnings/` folder. The HQ pre-commit hook refuses them.

Do **not** copy project UI/tokens into `studio-library/`. Promote reusable assets via `./studio library promote` — lessons are rules, not product dumps.

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

### Studio Infusion Gate

Project sprint planning is **not** blocked by open LO-* tickets. `./studio infusion` lists them with the TRAIN_DUE block; `./studio learn-list` shows which still need a verdict.

**Infusion targets** (generalize — never copy client project names into studio docs):

| Kind | Default target | Severity floor |
|------|----------------|----------------|
| `ui-component` | `knowledge-base/atomic-design-playbook.md` | low |
| `package` | `studio-library/library_registry.md` | low |
| `design` / `layout` | `knowledge-base/design_playbook.md` | low |
| `ux` / `usability` | `knowledge-base/design-science-playbook.md` | low |
| `ia` | `knowledge-base/contextual-ia-playbook.md` | low |
| `frontend` / `backend` / `database` | matching playbook | low |
| `security` | `knowledge-base/skill-extensions/frontend-security-auditor.md` | low |
| `process` | `process/learning-loop.md` | high |
| `tooling` | `process/gates.md` | high |

The agent may name another target (a skill file, a template, a tool); the floor follows the path.

See [studio-abstraction.md](studio-abstraction.md) — LOs cite `--source <project>`; bullets use `<project>` placeholders.

**LO titles & `next` (LO-0040):** write the **general rule** (reuse ladder, pattern name, archetype option). The originating sprint is `--source` / Scope context — never the title or the rule.

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

```
┌──────────────────────────────────────────────────────────────┐
│                      LEARNING LOOP                           │
├──────────────────────────────────────────────────────────────┤
│  product chat                                                │
│  1. deviation: gate round ≥2, retro line, reject, gate fail  │
│  2. candidate LO (## Lesson placeholders)                    │
│  3. verdict: project (local log) | studio (next + target)    │
│  4. TRAIN_DUE on retro / card / status / settings            │
│                                                              │
│  training chat ("run training")                              │
│  5. ./studio train LO → ## Impact → low | high (HITL)        │
│  6. infusion-delta --lo → PB- bullet in the real file        │
│  7. CHANGELOG line → verify-abstraction → train --done       │
└──────────────────────────────────────────────────────────────┘
```

---

## References

- `.quinsy-studio/process/iterative-delivery.md` — sprint/retro
- `.quinsy-studio/process/gates.md` — gate definitions
- `CHANGELOG.md` — change history
