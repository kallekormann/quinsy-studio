# Skill: Anti-Slop Audit

> AI code detection, code quality checks, anti-pattern detection

## Metadata

```
skill_id: AI-002
name: Anti-Slop Audit
team: 07-ai-autonomous-systems
lead_role: Process Guard
support_roles: [AI Architect, QA Specialist]
phases: [4, 5]
activation_triggers:
  - Ticket contains "anti-slop", "slop", "AI code", "quality"
  - Phase 5: QA gate checks anti-slop
  - Reuse review: code is promoted to the library
  - Suspicion of AI-generated code
```

---

## Behavior rules

### 1. Anti-slop checklist

```markdown
Code pattern detection:
  - Excessive comments (every line commented)
  - Redundant variables
  - Unnecessary imports
  - Excessive error-handling blocks
  - TODO comments without context
  - Excessive log calls
  - Unnecessary delays/fake data
  - Redundant validation
```

### 2. Text patterns (AI clichés)

```markdown
Blacklist:
  - "In today's digital landscape"
  - "Revolutionize" / "Revolutionary"
  - "Seamless" / "Seamlessly"
  - "Empower" / "Empowering"
  - "Leverage" / "Leveraging"
  - "Cutting-edge" / "State-of-the-art"
  - "Furthermore" / "Moreover"
  - "It's worth noting that"
  - "Delve" / "Delving"
  - "Tapestry" / "Multifaceted"
  - "Game-changer"
  - "Unlock the potential"
```

### 3. Quality check

```markdown
For every code file:
  - Complex functions (>50 lines)?
  - Maximum nesting (>3 levels)?
  - Too many parameters (>5)?
  - Missing typing?
  - Dead code?
  - Performance issues (N+1, missing indexes)?
```

### 4. Audit workflow

```markdown
Step 1: static check
  - Linting (ESLint, Prettier)
  - Type check (TypeScript)
  - Complexity analysis

Step 2: pattern matching
  - AI clichés in comments/strings
  - Excessive log calls
  - Redundant code

Step 3: review
  - Check code sensibility
  - Check performance
  - Check security

Step 4: report
  - Errors (must be fixed)
  - Warnings (should be fixed)
  - Suggestions (could be improved)
```

### 5. Integration into the QA gate

```markdown
./studio gate <project> --anti-slop

Output:
  ✅ Anti-slop: 0 errors, 3 warnings
  ❌ Anti-slop: 5 errors (must be fixed)

Rule: 0 anti-slop errors for a gate pass
```

---

## Anti-patterns

### ❌ Forbidden

```markdown
- AI-generated code without review
- Excessive TODO comments
- Redundant code not cleaned up
- Anti-slop check only optional
- No anti-slop in the QA gate
```

### ✅ Instead

```markdown
- Every code is reviewed
- Clear, useful comments
- Redundant code is removed
- Anti-slop as a mandatory check in the QA gate
- Pattern detection in CI/CD
```

---

## References

- `.quinsy-studio/knowledge-base/anti_ai_slop_protocol.md` — anti-slop rules
- `.quinsy-studio/process/gates.md` — anti-slop in gate 5
- `studio-tools/validate_anti_slop.py` — automated check
