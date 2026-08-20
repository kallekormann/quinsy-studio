# Skill: Frontend Testing

> Unit tests, integration tests, E2E tests, visual regression, snapshot tests

## Metadata

```
skill_id: FE-006
name: Frontend Testing
team: 01-frontend-experience
lead_role: QA Specialist
support_roles: [Frontend Engineer]
phases: [4, 5]
activation_triggers:
  - Ticket contains "test", "testing", "coverage"
  - Phase 4: TDD during implementation
  - Phase 5: QA gate checks test coverage
  - Reuse review: component needs tests for the library
```

---

## Verhaltensregeln

### 1. Test pyramid

```markdown
        ╱╲
       ╱ E2E ╲           ← 10% (few, critical paths)
      ╱────────╲
     ╱ Integration ╲      ← 30% (component interplay)
    ╱────────────────╲
   ╱     Unit tests    ╲  ← 60% (fast, isolated)
  ╱────────────────────╲

Coverage minimum:
  - statements: > 80%
  - branches: > 75%
  - functions: > 80%
  - lines: > 80%
```

### 2. Unit tests (Vitest/Jest)

```markdown
What to test:
  - component rendering with different props
  - event handlers (onClick, onChange)
  - conditional rendering logic
  - utility functions
  - custom hooks

How to test:
  - render() with Testing Library
  - userEvent for interactions
  - screen.getBy* for element search
  - expect() for assertions

Naming:
  describe('ComponentName', () => {
    it('should render with default props', () => {})
    it('should handle click event', () => {})
    it('should be accessible', () => {})
  })
```

### 3. Integration tests

```markdown
What to test:
  - component interplay
  - form submission with validation
  - API integration (mocked)
  - navigation between pages
  - theme/context providers
```

### 4. E2E tests (Playwright)

```markdown
What to test:
  - critical user journeys
  - login/logout flow
  - checkout/conversion flow
  - form submission with backend
  - multi-step workflows

Only critical paths — not every button!
```

### 5. Visual regression

```markdown
Tools: Chromatic / Percy / Playwright snapshots

What to test:
  - components in all variants
  - responsive breakpoints
  - dark/light mode
  - hover/focus/active states
```

### 6. TDD workflow

```markdown
1. RED:    write a test that fails
2. GREEN:  write code that passes the test
3. REFACTOR: clean up code, tests stay green
```

---

## Anti-Patterns

### ❌ Forbidden

```markdown
- Tests that only check whether a component renders
- No test for error states
- Snapshot tests that are updated too often
- Tests that depend on external services
- No test for accessibility
- Mocks that hide too much
```

### ✅ Instead

```markdown
- Tests for all states (loading, error, success, empty)
- Test error states explicitly
- Integration tests instead of too many snapshots
- API mocks with MSW (Mock Service Worker)
- axe-core integration in tests
- Simple, understandable mocks
```

---

## References

- `.quinsy-studio/knowledge-base/frontend_playbook.md` — frontend rules
- `.quinsy-studio/process/ticket-workflow.md` — step 5 (self-check)
- `./studio gate <project> --tests` — check test coverage
