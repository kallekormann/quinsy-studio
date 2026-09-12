# Skill: UI Component Design

> Atomic design, TypeScript, props API, Storybook documentation

## Metadata

```
skill_id: FE-001
name: UI Component Design
team: 01-frontend-experience
lead_role: Frontend Engineer
support_roles: [UI/Interaction Designer, QA Specialist]
phases: [3, 4, 5]
activation_triggers:
  - Ticket contains "component", "UI element"
  - New UI feature is being implemented
  - Design system is being extended
  - Reuse review identifies a reusable component
```

---

## Library-first + Tailwind (mandatory)

Before any new UI markup:

1. Read [ui/docs/README.md](../../../../studio-library/ui/docs/README.md)
2. `./studio library suggest <project> "<feature>"` → `./studio library pull`
3. Use **Tailwind utility classes** ([docs](https://tailwindcss.com/docs/)) — no ad-hoc CSS files for components
4. Use **Headless UI primitives** via studio-library — never hand-roll modals, menus, or focus traps
5. Confirm kit peers in the product `package.json`: `radix-ui`, `class-variance-authority`, `clsx`, `tailwind-merge`, `lucide-react` (`docs/setup/ui-kit.md`)
6. Styled controls: `button`, `input`, `card`, `dropdown-menu`, `checkbox`, `switch`, `select`, `textarea`


```markdown
Every component is assigned to the correct level:

ATOMS (smallest unit):
  - Button, Input, Badge, Icon, Avatar, Checkbox, Radio, Switch
  - Props: variant, size, disabled, loading, icon
  - No internal dependencies on other components

MOLECULES (combination of atoms):
  - Card, Form, Modal, Dropdown, SearchBar, FormField
  - Consist of 2+ atoms
  - Have a specific function

ORGANISMS (complex areas):
  - Header, Footer, Sidebar, Navigation, DataTable, Hero
  - Consist of molecules + atoms
  - Cover a whole view area

TEMPLATES (page layouts):
  - Page layouts without concrete content
  - Define the information architecture

PAGES (concrete implementations):
  - Templates filled with real data
```

### 2. Component specification

```markdown
Every component MUST have the following files:

src/components/{name}/
  ├── index.ts              # public API (named exports)
  ├── {name}.tsx            # implementation
  ├── {name}.test.tsx       # unit tests
  ├── {name}.stories.tsx    # Storybook documentation
  └── {name}.types.ts       # TypeScript types (if complex)
```

### 3. Props design

```markdown
Rules for props:

1. Consistent naming:
   - Boolean props: is{State} or has{Property} (isDisabled, hasIcon)
   - Event handlers: on{Event} (onClick, onChange)
   - Content props: children or specific (label, title)
   - Layout props: align, direction, gap

2. Sensible defaults:
   - All props except children have defaults
   - Defaults are visible in the documentation

3. TypeScript:
   - Props are explicitly typed (no any)
   - Union types for variants
   - Optional props marked with ?

4. Ref forwarding:
   - Components that access DOM elements forward refs
```

### 4. Styling rules

```markdown
1. Tailwind CSS as primary styling
2. CSS custom properties for theme variables
3. No inline styles (except dynamic values)
4. Responsive: mobile-first (sm:, md:, lg:, xl:)
5. Dark mode: via CSS custom properties / theme
6. Animations: only GPU-accelerated (transform, opacity)
```

### 5. Storybook rules

```markdown
Every component has:
- Default story
- All variants as separate stories
- Empty state story (if relevant)
- Disabled state story
- Loading state story
- Mobile viewport story
```

---

## Anti-patterns

### ❌ Forbidden

```markdown
- Inline styles instead of Tailwind
- div instead of semantic HTML elements (button, nav, main, section)
- Missing aria labels on interactive elements
- Hardcoded colors instead of design tokens
- Component with >20 props (too complex — split it!)
- No TypeScript types
- No default export (only named exports)
- CSS-in-JS without a compelling reason
- Any styles that are not responsive
```

### ✅ Instead

```markdown
- Tailwind + CSS custom properties
- Semantic HTML elements
- ARIA labels where needed
- Design tokens (.quinsy-studio/studio-library/ui/tokens/)
- Split props into sub-components
- Full TypeScript typing
- Named exports (barrel exports via index.ts)
- Tailwind for the fast path, CSS modules for complex animations
- Mobile-first responsive design
```

---

## Quality checklist

- [ ] Component is generic and configurable
- [ ] TypeScript types are complete
- [ ] Props have sensible defaults
- [ ] Storybook documentation present
- [ ] Unit tests present
- [ ] Accessibility checked (a11y)
- [ ] Responsive (mobile-first)
- [ ] Dark/light mode supported
- [ ] Performance within budget (no unnecessary re-rendering)
- [ ] No AI slop in the code
- [ ] Semantic HTML elements used
- [ ] Ref forwarding implemented (when needed)

---

## External skill support

> Before implementation load the imported best-in-class skills (`./studio update-skills`):

- **`design/skills/`** (Nutlope/hallmark) — run `hallmark audit` before UI review, `hallmark build` for new drafts (57 slop gates).
- **`design_awesome/skills/<style>/SKILL.md`** (bergside) — concrete style guides for components (corporate, minimal, ...)
- **`all_domains/design-and-ui-ux/frontend-design`** — generic frontend design workflow

Flow: build the component → run `hallmark audit` → fix slop violations → Storybook + tests.

## References

- `.quinsy-studio/studio-library/ui/tokens/` — design tokens
- `.quinsy-studio/studio-library/ui/components/` — existing components
- `.quinsy-studio/knowledge-base/design_playbook.md` — design rules
- `.quinsy-studio/knowledge-base/frontend_playbook.md` — frontend rules
- `.quinsy-studio/knowledge-base/anti_ai_slop_protocol.md` — anti-slop
