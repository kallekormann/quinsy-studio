# Quinsy Studio — Anti-Slop Policy

> AI-generated code has characteristic patterns that make it worse than manually written code.
> This policy defines the binding rules for avoiding AI slop.

## Core principle

```
No AI slop in production code.
The anti-slop audit must be green before a gate counts as passed.
```

---

## Registry of slop patterns

### Category 1: Code slop (severity: error)

| Rule | Pattern | Detection |
|------|---------|-----------|
| S1 | Unused imports | `import .* from` without evidence |
| S2 | Unused variables | declared but never referenced |
| S3 | Dead code | unreachable code after return/throw |
| S4 | Redundant functions | never called |
| S5 | Redundant conditions | `if (x === true)` instead of `if (x)` |
| S6 | Unused parameters | function parameters without use |
| S7 | Excessive nesting | >4 levels |

### Category 2: Comment slop (severity: warning)

| Rule | Pattern | Detection |
|------|---------|-----------|
| C1 | AI-typical comments | "This function does X", "Here we..." |
| C2 | TODO without owner/date | `// TODO` without `@name YYYY-MM-DD` |
| C3 | Commented-out code | `// ... (old code)` |
| C4 | Over-commented trivialities | comment for `const x = 1` |

### Category 3: Error-handling slop (severity: error)

| Rule | Pattern | Detection |
|------|---------|-----------|
| E1 | Catch-all | `catch (e) {}` or `catch (e) { console.log(e) }` |
| E2 | Missing error handling | async function without try/catch |
| E3 | Swallowed errors | catch without throw/logging |
| E4 | Generic messages | "An error occurred" without details |

### Category 4: Architectural slop (severity: warning)

| Rule | Pattern | Detection |
|------|---------|-----------|
| A1 | Missing abstraction | everything in one file |
| A2 | Circular dependencies | A → B → A |
| A3 | God functions | >100 lines |
| A4 | Missing typing | `any`/`unknown` without need |
| A5 | Inconsistent naming | camelCase and snake_case mixed |

---

## Audit mode

```bash
# Full audit
./studio gate <project> --anti-slop

# Only code slop
./studio gate <project> --anti-slop --category code

# Output as JSON
./studio gate <project> --anti-slop --json
```

---

## Prevention strategies

### For agents

1. **Specific instructions**
   ```
   ❌ "Write a function that does X"
   ✅ "Write a function that does X, with error handling for Y and Z"
   ```

2. **Demand a code review**
   ```
   ❌ "Write the code"
   ✅ "Write the code and then check it for AI slop patterns"
   ```

3. **Name best practices**
   ```
   ❌ (no constraints)
   ✅ "Use specific error messages, avoid catch-all"
   ```

### For humans

1. **PR review checklist**
   - [ ] Are all imports used?
   - [ ] Are all variables used?
   - [ ] Is there unreachable code?
   - [ ] Are errors handled specifically?
   - [ ] Are comments informative (not trivial)?

2. **Automation**
   - ESLint with custom rules
   - TypeScript strict mode
   - Pre-commit hooks

---

## Integration with gates

The anti-slop audit is a **mandatory part** of gate 5 (QA gate):

```bash
./studio gate <project> --level 5
# Runs the anti-slop audit automatically
```

**Rule:** a gate cannot be green if the anti-slop audit has error violations.

---

## Change policy

Anti-slop rules can be changed:
1. Create a learning item: `./studio learn "Rule X is too strict" --signal tooling-gap`
2. Discuss it in the meta-retro
3. Document the decision
4. Create a CHANGELOG entry

---

## References

- `.quinsy-studio/process/gates.md` — gate definitions
- `.quinsy-studio/process/learning-loop.md` — learning loop
- `.quinsy-studio/teams/07-ai-autonomous-systems/` — anti-slop team
