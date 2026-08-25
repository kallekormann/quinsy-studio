# Design System Compliance Checklist

> **Skills:** UX-006 (Brand guardian), FE-001, FE-002, AI-002  
> **When:** Team 10 design spec review and `./studio approve-design` (human + agent pre-check).

## Rule

**No hallucinated UI.** Every element maps to studio-library or an approved new component in studio-library first.

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

### Anti-slop UI

- [ ] No generic violet/gradient blocks outside token system
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

Human runs `./studio approve-design <project> <TICKET>` after:

1. §2 Context & placement present
2. Atomic inventory complete
3. This checklist pass (self-attest in spec or approval notes)

Agent should **warn** (not block human) if spec references non-library patterns.

---

## Related

- [component-creation-playbook.md](component-creation-playbook.md)
- [brand-guardian-checklist.md](brand-guardian-checklist.md)
- [ui/docs/README.md](../studio-library/ui/docs/README.md)
