# Design System Compliance Checklist

> **Skills:** UX-006 (Brand guardian), FE-001, FE-002, AI-002  
> **When:** Team 10 design spec review and `./studio approve-design` (human + agent pre-check).

## Rule

**No hallucinated UI.** Every element maps to studio-library or an approved new component in studio-library first. Feature tickets **stay inside** the gate-2b project kit (project tokens + pulled components). If a component, token, or pattern is **missing**, stop the feature ticket and open a design-track ticket for the next **design phase** (`./studio approve-design <p> --phase`) — do not invent the primitive to unblock implement.

---

## Spec review (Team 10)

### Primitives & components

- [ ] Atomic inventory lists **library pull** vs **new studio-library** (not project-only one-offs)
- [ ] Dialogs, menus, tabs use Headless UI primitives from `ui/primitives/headless/`
- [ ] Buttons, inputs, fields use `@ui/components/atoms/*` or documented molecules
- [ ] No raw `<div role="dialog">` unless ADR exception

### Tokens & brand

- [ ] Colors reference **project tokens** or presentation/canvas token sets — no one-off hex in spec
- [ ] Aesthetic preset declared (§3b in design spec)
- [ ] Typography/spacing on 8pt grid (`design_playbook.md`)
- [ ] Dark mode surfaces listed if applicable

### Anti-slop UI & copy

Canonical: [anti-slop-design-ux.md](anti-slop-design-ux.md) · Team 10 skill UX-008

- [ ] No generic violet/gradient blocks outside token system
- [ ] **No emoji as icons** in mocks or product chrome — SVG / `@ui` Icon components only; icons optically centered in hit targets (LO-0037)
- [ ] No decorative blobs, glassmorphism, or template-dashboard filler without purpose (U-D1)
- [ ] 8pt grid; semantic color; ≤2 type families; operational screens ≠ marketing hero scale
- [ ] Mock copy uses **literal CTAs** — no banned fluff vocabulary (§2.1) or placeholders (`Lorem`, `Feature 1`, `Primary action`)
- [ ] **Spec file exists and is filled** — not a missing path, not a stub. Do not ask for `approve-design` until `projects/<p>/docs/design-specs/<TICKET>.md` is on disk.
- [ ] **§2 + §2c filled** — mocks alone do not pass `approve-design` (LO-0038)
- [ ] **Real UI** — mocks are `(design-mocks)` routes in the product app that render its own views and components; no standalone HTML, inline styles, or hex colours
- [ ] **Interactive** — one ticket-root `page.tsx` plus `mock-scenario-panel` (no `<state>/` folders); wired handlers; `?state=` covering §2c and screenshot stems; §2d transitions moving; §2e walkthrough written; `./studio mock <p> <T>` green
- [ ] **Mocks use project CSS tokens** (`ui/tokens`, `var(--…)`) — not a parallel hex palette
- [ ] **In-context** — component shown in the product view it ships in (chrome/nav/neighbors visible)
- [ ] **All states mocked** — rest/hover/pressed/disabled/focus; open/closed for menus; empty/loading/error for surfaces
- [ ] No duplicate controls for the same action on one surface
- [ ] Progressive disclosure for advanced options — not one scrolling wall

---

## Implement review (Team 01)

```bash
./studio library list
./studio library suggest <project> "<feature>"
./studio library pull <project> dialog button tabs field
```

- [ ] Pulled artifacts recorded in `docs/library-usage.json`
- [ ] New generic components promoted after ticket done (`./studio library promote`)

---

## Approve-design gate

Human runs `./studio approve-design <project> <TICKET>` only after:

1. Spec markdown **exists and is filled** (CLI **fails** if the file is missing or still a stub)
2. §2 Context & placement present
3. §2c in-context mocks: HTML under `docs/design-specs/mocks/<TICKET>/`, **project tokens**, **all states**
4. Atomic inventory complete
5. This checklist pass (self-attest in spec or approval notes)

The CLI **blocks** approval when spec/mocks/tokens/states are incomplete. The agent must **write** those files first — execute returns IMPLEMENT (write spec), not HITL, until they exist.

---

## Related

- [anti-slop-design-ux.md](anti-slop-design-ux.md)
- [component-creation-playbook.md](component-creation-playbook.md)
- [brand-guardian-checklist.md](brand-guardian-checklist.md)
- [ui/docs/README.md](../studio-library/ui/docs/README.md)
