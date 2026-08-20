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
  projects/[name]/docs/local_learnings.md

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
  .quinsy-studio/knowledge-base/  → Playbooks
  .quinsy-studio/studio-tools/    → Python Scripts
  .quinsy-studio/studio-templates/ → Templates
  studio-library/                 → UI/Packages

Promotion via:
  ./studio promote <project> <asset-path>
```

### 3. Learning Harvesting (Phase 6)

```markdown
Workflow:
  1. Run sprint retrospective
  2. Collect learning items
  3. For each learning:
     a. Is it project-specific? → Local Loop
     b. Is it universal? → Global Loop
  4. Local Learnings → projects/[name]/docs/local_learnings.md
  5. Global Learnings → .quinsy-studio/knowledge-base/ or studio-tools/
  6. Update CHANGELOG
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
- Copying project-specific solutions to Studio HQ
  - No learning harvesting after sprint
  - Promotions without documentation
  - Local learnings sold as global
```

### ✅ Instead

```markdown
- Strict separation Local/Global
  - Mandatory learning harvesting in Phase 6
  - Promotion with complete documentation
  - Only universally applicable solutions in Studio HQ
```

---

## References

- `.quinsy-studio/process/learning-loop.md` — Dual-Loop Learning
- `.quinsy-studio/process/lifecycle.md` — Phase 6
- `./studio promote` — Promotion command
- `./studio learn` — Learning interface
