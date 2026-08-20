# Skill: Documentation Governance

> Strict separation of Studio/Project, CHANGELOG maintenance, README currency, Knowledge Transfer

## Metadata

```
skill_id: SO-004
name: Documentation Governance
team: 09-studio-operations-evolution
lead_role: Documentation Writer
support_roles: [Process Guard]
phases: [6, 7]
activation_triggers:
  - Ticket contains "Docs", "Documentation", "README", "CHANGELOG"
  - Phase 6: Documentation is being updated
  - Phase 7: Release documentation
  - /studio evolve command
```

---

## Behavioral Rules

### 1. Strict Separation of Studio/Project

```markdown
Studio HQ (.quinsy-studio/):
  - Contains ONLY universally applicable content
  - No project-specific details
  - Playbooks, tools, templates, skills

Project (projects/[name]/):
  - Contains ONLY project-specific content
  - Local learnings
  - Project-specific documentation
  - Status, tickets, sprints

Rule:
  - Studio files must NOT contain project references
  - Project files may REFERENCE studio content (not copy it)
```

### 2. CHANGELOG Maintenance

```markdown
Format (Keep a Changelog):
  ## [Version] - YYYY-MM-DD
  ### Added
  - New feature
  ### Changed
  - Changed feature
  ### Fixed
  - Bug fix
  ### Removed
  - Removed feature

When to update:
  - On every promotion
  - On every tool change
  - On every process change
  - On every release
```

### 3. README Maintenance

```markdown
For each component:
  - Brief description
  - Installation/setup
  - Usage
  - References
  - Currency: On every change

Standard READMEs:
  - .quinsy-studio/README.md (Studio HQ)
  - Each team README.md
  - Each skill README.md (in the skill itself)
```

### 4. Knowledge Transfer

```markdown
Ensure:
  - New team members find all information
  - Decisions are documented (ADRs)
  - Learnings are accessible
  - Processes are described

Tools:
  - ADRs for architecture decisions
  - Learning logs for insights
  - Decision records for HITL decisions
```

---

## Anti-Patterns

### ❌ Prohibited

```markdown
- Studio files with project references
  - Outdated READMEs
  - No CHANGELOG
  - Documentation treated as optional
```

### ✅ Instead

```markdown
- Strict separation Studio/Project
  - Regular README updates
  - CHANGELOG on every change
  - Documentation as mandatory
```

---

## References

- `.quinsy-studio/process/learning-loop.md` — Dual-Loop Learning
- `CHANGELOG.md` — Studio Changelog
- `README.md` — Studio README
