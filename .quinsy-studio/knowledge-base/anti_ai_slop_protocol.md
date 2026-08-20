# Anti-AI-Slop Protocol

> Absolute blacklist for AI-generated code. No violation is acceptable.

## Core principle

```
AI slop = code that works but is bad.
Anti-slop = code that works AND is good.
```

---

## ABSOLUTE BLACKLIST (immediate rejection)

### Text clichés (comments, variables, functions)

| # | Forbidden | Reason |
|---|-----------|-------|
| T1 | "This function does X" | trivial, not informative |
| T2 | "Here we..." | conversational, unprofessional |
| T3 | "Let's..." / "Let me..." | AI-typical |
| T4 | "Note that..." | redundant |
| T5 | "It's important to..." | obvious |
| T6 | "Basically..." / "Simply..." | condescending |
| T7 | "In this case..." | redundant |
| T8 | "As we can see..." | AI-typical |
| T9 | "This is a..." | AI-typical |
| T10 | "We need to..." | imperative AI |

### Code patterns

| # | Forbidden | Reason |
|---|-----------|-------|
| C1 | `catch (e) {}` | swallowed error |
| C2 | `catch (e) { console.log(e) }` | debug code |
| C3 | `if (x === true)` | redundant |
| C4 | `const result = await fn(); return result;` | superfluous |
| C5 | `// Initialize` / `// Setup` | trivial comments |
| C6 | function >100 lines | god function |
| C7 | >4 levels of nesting | cognitive overload |
| C8 | `any` / `unknown` without need | missing typing |
| C9 | unused imports/variables | dead code |
| C10 | duplicated logic | redundancy |

---

## FORBIDDEN UI PATTERNS

### Free LLM styling

| # | Forbidden | Instead |
|---|-----------|---------|
| U1 | inline styles | design tokens / Tailwind |
| U2 | hardcoded colors | CSS custom properties |
| U3 | free font choices | defined typography scale |
| U4 | arbitrary border radii | token-based radii |
| U5 | free shadows | defined shadow scale |

### Structure

| # | Forbidden | Instead |
|---|-----------|---------|
| U6 | `div` instead of semantic elements | `<button>`, `<nav>`, `<article>` |
| U7 | missing `alt` texts | descriptive alternative texts |
| U8 | missing keyboard navigation | complete tab order |
| U9 | missing ARIA labels | specific labels |
| U10 | colors without contrast check | WCAG AA minimum |

---

## FORBIDDEN BACKEND PATTERNS

| # | Forbidden | Instead |
|---|-----------|---------|
| B1 | secrets in code | environment variables |
| B2 | SQL injection (string concat) | prepared statements / ORM |
| B3 | missing input validation | Zod / Joi / class-validator |
| B4 | catch-all error handling | specific error types |
| B5 | sync code in async | complete async chain |
| B6 | missing rate limiting | express-rate-limit / middleware |
| B7 | no CORS setup | explicit origin whitelist |
| B8 | missing security headers | Helmet / custom headers |

---

## ENFORCEMENT

### During development

```bash
# Anti-slop check before every commit
python3 .quinsy-studio/studio-tools/validate_anti_slop.py .

# On violation: the commit is aborted
```

### In the QA gate

```bash
# Anti-slop audit as part of the gate
./studio gate <project> --anti-slop

# The gate cannot be green with error violations
```

### In code review

```markdown
## Anti-slop checklist

- [ ] No text clichés (T1-T10)
- [ ] No code patterns (C1-C10)
- [ ] No UI patterns (U1-U10)
- [ ] No backend patterns (B1-B8)
```

---

## EXCEPTIONS (only with an ADR)

Sometimes AI slop is unavoidable:
- an explicit ADR documents the exception
- risk assessment done
- tech-debt ticket created
- time frame for cleanup defined

---

## References

- `.quinsy-studio/process/anti-slop.md` — audit tool
- `.quinsy-studio/process/anti-slop-policy.md` — binding rules
- `.quinsy-studio/teams/07-ai-autonomous-systems/` — anti-slop team
