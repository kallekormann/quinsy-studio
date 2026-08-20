# Skill: Accessibility

> WCAG 2.1 AA, screen readers, keyboard navigation, ARIA, focus management

## Metadata

```
skill_id: FE-004
name: Accessibility (a11y)
team: 01-frontend-experience
lead_role: QA Specialist
support_roles: [Frontend Engineer, UI/Interaction Designer]
phases: [3, 4, 5]
activation_triggers:
  - Ticket contains "a11y", "accessibility"
  - Phase 5 QA gate checks accessibility
  - New component is being created
  - User complains about usability
```

---

## Verhaltensregeln

### 1. WCAG 2.1 AA compliance

```markdown
Required level (AA):
1. Perceivable: alt texts, contrasts, scalable
2. Operable: keyboard navigation, no time limits
3. Understandable: clear labels, error messages
4. Robust: semantic HTML, correct ARIA

Metrics:
  - color contrast: min. 4.5:1 (text), 3:1 (large text)
  - text scalable to 200% without horizontal scroll
  - all interactive elements reachable by keyboard
  - focus indicator always visible
```

### 2. Semantic HTML

```markdown
Always use:
  - <nav> for navigation
  - <main> for main content
  - <section> for content areas
  - <article> for standalone content
  - <header>, <footer> for page areas
  - <button> for actions (not <div onClick>)
  - <a> for links (not <span onClick>)
  - <h1>-<h6> for hierarchy (don't skip!)
  - <ul>/<ol> for lists
  - <table> for tables with <th>, <caption>
```

### 3. ARIA labels

```markdown
When ARIA is needed:
  - Icon-only buttons: aria-label="Save"
  - Complex widgets: aria-expanded, aria-selected
  - Live regions: aria-live="polite" for dynamic content
  - Form errors: aria-describedby for error messages

Never:
  - role="button" on <div> (use <button> instead)
  - aria-label on non-interactive elements
  - ARIA for things semantic HTML already solves
```

### 4. Keyboard navigation

```markdown
Keyboard shortcuts:
  - Tab: to the next interactive element
  - Shift+Tab: to the previous element
  - Enter/Space: activate buttons/links
  - Escape: close modal, close dropdown
  - Arrow keys: navigation in lists/menus

Focus management:
  - focus indicator: visible (min. 2px, high contrast)
  - focus trap in modals
  - skip links for long pages
  - focus reset after navigation
```

### 5. Screen reader support

```markdown
Checkpoints:
  - All images have alt text (or alt="" for decorative)
  - Forms have associated labels
  - Error messages are audible via screen reader
  - Dynamic content uses aria-live
  - Tables have caption and th
  - Links have meaningful text (not "click here")
  - DOM order matches the visual order
```

### 6. Testing

```markdown
Tools:
  - axe-core (automated)
  - Lighthouse accessibility audit
  - screen reader testing (VoiceOver/NVDA)
  - keyboard-only navigation test
  - color contrast analyser

Manual checks:
  - keyboard only: are all functions usable?
  - screen reader: is all content understandable?
  - zoom 200%: does the layout work?
  - high contrast mode: is everything visible?
```

---

## Anti-Patterns

### ❌ Forbidden

```markdown
- <div onClick> instead of <button onClick>
- Missing alt texts on images
- No aria-label on icon buttons
- Missing keyboard navigation
- Focus indicator not visible (outline: none without replacement)
- Color as the only source of information
- Time limits without the possibility to extend
- Flashing (more than 3x per second)
```

### ✅ Instead

```markdown
- Semantic HTML elements
- Meaningful alt texts
- ARIA labels where needed
- Complete keyboard support
- Visible focus indicator
- Color + icon/text as information
- Time limits with extension option
- No flashing animations
```

---

## References

- `.quinsy-studio/knowledge-base/frontend_playbook.md` — frontend rules
- `.quinsy-studio/knowledge-base/design_playbook.md` — design rules
- `.quinsy-studio/process/gates.md` — a11y in gate 5
