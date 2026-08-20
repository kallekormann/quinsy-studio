# Skill: Process Optimization

> Sprint discipline, studio flows, metrics, anti-patterns in the process

## Metadata

```
skill_id: SO-002
name: Process Optimization
team: 09-studio-operations-evolution
lead_role: Process Guard
support_roles: [Agile Coach]
phases: [3, 5, 6, 7]
activation_triggers:
  - Ticket contains "Process", "Sprint Discipline", "Optimization"
  - Phase 3: Sprint setup is being reviewed
  - Phase 5: QA gate identifies process gaps
  - Phase 6: Retro identifies improvements
  - /studio-evolution command
```

---

## Behavioral Rules

### 1. Sprint Discipline

```markdown
What to check:
  - Are all 9 steps of the ticket workflow being followed?
  - Is TDD actually being applied?
  - Is anti-slop audit being run?
  - Are gates being passed?
  - Is documentation being maintained?

On violations:
  - Ticket goes back to the missing step
  - Learning is logged
  - Process gap is closed
```

### 2. Studio Metrics

```markdown
What to track:
  - Sprint velocity (story points per sprint)
  - Ticket cycle time (Intake → Done)
  - Gate pass rate (first time)
  - Anti-slop error rate
  - Learning items per sprint
  - Local vs. Global Learnings ratio

Goals:
  - Velocity stable or increasing
  - Cycle time decreasing
  - Gate pass rate > 80%
  - Anti-slop error rate < 5%
```

### 3. Process Anti-Patterns

```markdown
Detection:
  - Tickets stuck in "implement" (>3 days)
  - Steps being skipped
  - Gates not being passed
  - Missing documentation
  - No learning from errors

Countermeasures:
  - Automatic reminders
  - Stricter gate checks
  - Process improvements in Global Loop
```

---

## Anti-Patterns

### ❌ Prohibited

```markdown
- Process not being checked
  - Metrics not being tracked
  - Violations not being documented
  - No improvements from learnings
```

### ✅ Instead

```markdown
- Regular process checks
  - Metrics dashboard
  - Violation → Learning → Improvement
  - Iterative process optimization
```

---

## Quality Assurance: Skill Matching Test

The skill matching test verifies that tickets are correctly mapped to internal AND external skills
(`.quinsy-studio/studio-tools/test_skill_matching.py`):

```bash
python3 .quinsy-studio/studio-tools/test_skill_matching.py
```

**Run after:**
- New trigger words / skill added
- New external skill dependency
- Change to the skill registry

**Test cases (7):** Design System, SEO/AEO, Cookie Compliance, Database, Security, Game Dev, Copywriting.
Expectation: `7/7` tickets matched, `29/29` external sources on disk.

## References

- `.quinsy-studio/process/lifecycle.md` — Phases
- `.quinsy-studio/process/ticket-workflow.md` — 9-step workflow
- `.quinsy-studio/process/iterative-delivery.md` — Sprint/Grooming
