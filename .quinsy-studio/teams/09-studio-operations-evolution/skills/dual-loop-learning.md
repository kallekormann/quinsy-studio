# Skill: Dual-Loop Learning

> Local Loop (Project) vs Global Loop (Studio), Learning Harvesting, Knowledge Promotion

## Metadata

```
skill_id: SO-003
name: Dual-Loop Learning
team: 09-studio-operations-evolution
lead_role: Process Guard
support_roles: [Agile Coach, Documentation Writer]
phases: [6]
activation_triggers:
  - Ticket contains "Learning", "Retro", "Knowledge", "Promotion"
  - Phase 6: Knowledge Harvesting (mandatory)
  - /studio learn command
  - /studio promote command
```

---

## Behavioral Rules

### 1. Local Loop (Project World)

```markdown
What belongs here:
  - Project-specific bugs and workarounds
  - Niche insights from A/B tests
  - Client-specific requirements
  - Project-specific config details

Storage location:
  projects/[name]/docs/studio-learnings-local.md

Format:
  ## Learning LL-{NNN}
  - **Date:** YYYY-MM-DD
  - **Context:** What happened?
  - **Insight:** What did we learn?
  - **Action:** What was changed?
  - **Applies to:** This project only
```

### 2. Global Loop (Studio World)

```markdown
What belongs here:
  - Universally applicable solutions
  - Better playbooks
  - New anti-slop rules
  - Improved Python tools
  - Reusable components

Storage location:
  .quinsy-studio/knowledge-base/*.md, process/*.md, teams/*/skills/*.md → PB- bullets (learn-find)
  .quinsy-studio/backlog/open/LO-*.md                        → local work orders with the ## Lesson block
  .quinsy-studio/backlog/deferred/LO-*.md                    → high-impact lessons the human said wait on
  .quinsy-studio/knowledge-base/  → Playbooks (ACE deltas on train)
  .quinsy-studio/teams/*/skills/ → Skill deltas
  .quinsy-studio/studio-tools/    → Python Scripts
  .quinsy-studio/studio-templates/ → Templates
  studio-library/                 → UI/Packages

Promotion via:
  ./studio promote <project> <asset-path>
```

### 3. Immediate harvest (do not batch until next sprint)

```markdown
When a deviation is identified (gate signed after ≥2 rounds, retro bullet, design reject, 3rd gate fail, reuse path, explicit learn):
  1. Portability gate (must/should/never/prefer — not host/ticket incidents)
  2. Classify kind → default target (the real playbook / process file / skill)
  3. Open LO-* candidate with a ## Lesson block (assumed / signed / verdict / next / target)
  4. Verdict (product agent, before retro --complete can close):
       project → projects/[name]/docs/studio-learnings-local.md with reason, LO removed
       studio  → next rule + target; TRAIN_DUE on retro, execute card, status, settings
  5. Training chat: ./studio train <LO> → ## Impact (files, in-flight, compliance, pro, contra, severity)
       floor by target path: process/ studio-tools/ studio-templates/ teams/**/skills/ = high; playbook = low
       low → infuse (INFORM); high → human --approve or --defer --reason (backlog/deferred/, --reopen)
  6. ./studio infusion-delta --lo <LO> --path <target> --op add --body "assumed: … signed: … next: …"
  7. CHANGELOG line names the PB- id; ./studio verify-abstraction; ./studio train --done <LO>
       (refuses until the bullet is in the target and the CHANGELOG names it)
No catalog folder: the bullet in the file is the record; ./studio learn-find searches it.
Do not copy project UI/tokens into studio-library.
```

### 4. Promotion Workflow

```markdown
When to promote:
  - Solution is useful in 2+ projects
  - Code/design is generic
  - Solution is proven (tested)

How to promote:
  1. ./studio promote <project> <asset-path>
  2. Asset is copied to Studio Library
  3. README.md is created/updated
  4. manifest.json is updated
  5. CHANGELOG.md is updated
  6. Skill registry is updated (if new skill)
```

---

## Anti-Patterns

### ❌ Prohibited

```markdown
- Letting LOs pile until the next sprint (context is gone; next project cannot use the learning)
- Copying project-specific solutions to Studio HQ
- Waiting for a human learn prompt or Phase 6 batch before capturing
- Promotions without documentation
- Local learnings sold as global
```

### ✅ Instead

```markdown
- Immediate harvest when identified (inbox + LO) then `./studio train` in a HQ session
  - Strict separation Local/Global
  - Promotion with complete documentation
  - Only universally applicable solutions in Studio HQ
```

---

## References

- `.quinsy-studio/process/learning-loop.md` — Dual-Loop Learning
- `.quinsy-studio/process/lifecycle.md` — Phase 6
- `./studio promote` — Promotion command
- `./studio learn` — Learning interface
