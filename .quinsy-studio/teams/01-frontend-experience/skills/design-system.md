# Skill: Design System

> Design tokens, typography, color palette, spacing system, theme management

## Metadata

```
skill_id: FE-002
name: Design System Management
team: 01-frontend-experience
lead_role: UI/Interaction Designer
support_roles: [Frontend Architect, Frontend Engineer]
phases: [2, 3]
activation_triggers:
  - New project is initialized (phase 2/3)
  - Design tokens must be defined/updated
  - Color palette or typography is changed
  - Dark/light mode must be implemented
  - An asset is promoted to the studio library
```

---

## Tailwind + tokens (mandatory)

- Install Tailwind v4 per [installation guide](../../../../studio-library/ui/docs/getting-started/installation.md)
- Pull `tokens` + `tailwind.preset.ts` from studio-library
- Semantic classes: `primary-*`, `neutral-*`, `surface`, `error-*`
- Dark mode: `dark:` variants on every chrome surface (see [dark-mode pattern](../../../../studio-library/ui/docs/patterns/dark-mode.md))

External reference: [Tailwind CSS documentation](https://tailwindcss.com/docs/) — utility vocabulary for all FE tickets.

## Behavior rules

### 1. Design token hierarchy

```markdown
Global tokens (studio HQ):
  → studio-library/ui/tokens/design-tokens.json
  → apply to ALL projects

Local tokens (project):
  → projects/[name]/ui/tokens/
  → can override globals (project-specific)
```

### 2. Token structure

```markdown
Every token has:
- Category: color, typography, spacing, shadow, border, breakpoint
- Name: consistent naming (color-primary-500)
- Value: JSON-compatible
- Dark mode: own value or alias
- Description: what the token represents
```

### 3. Typography scale

```markdown
Standard scale (rem-based):

Display:    3rem / 48px  — hero headline
H1:         2.25rem / 36px
H2:         1.875rem / 30px
H3:         1.5rem / 24px
H4:         1.25rem / 20px
Body-LG:    1.125rem / 18px
Body:       1rem / 16px      ← base
Body-SM:    0.875rem / 14px
Caption:    0.75rem / 12px

Line heights:
  Tight:   1.25 (headlines)
  Normal:  1.5  (body)
  Relaxed: 1.75 (long-form)
```

### 4. Color palette

```markdown
Structure per color:
  - 50:  background (lightest)
  - 100: light
  - 200: light
  - 300: medium-light
  - 400: medium
  - 500: primary (standard)
  - 600: medium-dark
  - 700: dark
  - 800: dark
  - 900: darkest
  - A100-A700: accent

Base colors:
  - primary: brand color
  - neutral: gray tones
  - success: success
  - warning: warning
  - error: error
  - info: information
```

### 5. Spacing system

```markdown
8px grid as base:

space-0:   0px
space-1:   4px     (0.25rem)
space-2:   8px     (0.5rem)    ← base unit
space-3:   12px    (0.75rem)
space-4:   16px    (1rem)
space-5:   20px    (1.25rem)
space-6:   24px    (1.5rem)
space-8:   32px    (2rem)
space-10:  40px    (2.5rem)
space-12:  48px    (3rem)
space-16:  64px    (4rem)
space-20:  80px    (5rem)
space-24:  96px    (6rem)
```

### 6. Promotion to the studio library

```markdown
When to promote?
- Component is identical in 2+ projects
- Design decision is universal
- Token is project-agnostic

How to promote?
1. Copy code into studio-library/
2. Add README.md with documentation
3. Update manifest.json
4. Add a CHANGELOG.md entry
```

---

## Anti-patterns

### ❌ Forbidden

```markdown
- Hardcoded colors in components (instead of tokens)
- Pixel values instead of rem/em
- Loading single fonts (instead of a font family)
- No dark mode (if the project needs it)
- Tokens directly in CSS (instead of JSON as source of truth)
- No consistency between projects
```

### ✅ Instead

```markdown
- Always use design tokens
- rem/em for everything
- Font family with fallbacks
- Dark mode via CSS custom properties
- Tokens as JSON + generated CSS custom properties
- Global tokens from studio HQ, local overrides
```

---

## External skill support

> Before implementation load the imported best-in-class skills (`./studio update-skills`):

- **`design/skills/`** (Nutlope/hallmark) — anti-AI-slop design: macrostructure selection, 57 slop test gates, themes. **Mandatory before every new UI draft.**
- **`design_awesome/skills/<style>/SKILL.md`** (bergside/awesome-design-skills) — 67 design system styles (corporate, minimal, glassmorphism, ...) with SKILL.md + DESIGN.md

Flow: choose a style from `design_awesome` → run the `design` (hallmark) slop test → define tokens → check promotion.

## References

- `.quinsy-studio/studio-library/ui/tokens/` — token files
- `.quinsy-studio/studio-library/manifest.json` — registration
- `.quinsy-studio/knowledge-base/design_playbook.md` — design rules
