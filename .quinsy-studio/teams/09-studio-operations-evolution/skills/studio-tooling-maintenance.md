# Skill: Studio Tooling Maintenance

> Maintenance, refactoring and improvement of the Python tools in the Studio HQ

## Metadata

```
skill_id: SO-001
name: Studio Tooling Maintenance
team: 09-studio-operations-evolution
lead_role: Studio Automation Engineer
support_roles: [Platform Architect]
phases: [6, 7]
activation_triggers:
  - Ticket contains "Studio Tools", "Python", "Tooling", "Maintenance"
  - /studio-evolution command
  - Phase 6: Learning Loop identifies tooling improvements
  - Performance problems with studio tools
```

---

## Behavioral Rules

### 1. Maintain Python Tools

```markdown
Files in .quinsy-studio/studio-tools/:
  - validate_anti_slop.py    → Anti-slop detection
  - run_qa_gate.py           → QA gate orchestration
  - generate_ticket_manifest.py → Ticket generation
  - sync_global_assets.py    → Asset promotion
  - init_project_env.py      → Project initialization
  - requirements.txt         → Dependencies

Regular maintenance:
  - Update dependencies (weekly)
  - Security scans
  - Performance benchmarks
  - Write/update unit tests
```

### 2. Refactoring Rules

```markdown
When refactoring:
  - Keep API backward-compatible
  - Update CHANGELOG.md
  - Update README.md
  - Update tests
  - No breaking changes without version bump
```

### 3. Monitoring

```markdown
What to track:
  - Execution time per tool
  - Success rate
  - Usage frequency
  - Error logs
```

---

## Anti-Patterns

### ❌ Prohibited

```markdown
- Breaking changes without versioning
  - No tests for changed tools
  - Not updating dependencies
  - Debug code in production
```

### ✅ Instead

```markdown
- Semantic versioning
  - Tests before every deploy
  - Regular dependency updates
  - Clean production code
```

---

## References

- `.quinsy-studio/studio-tools/` — Python automation
- `.quinsy-studio/process/learning-loop.md` — Learning Loop
