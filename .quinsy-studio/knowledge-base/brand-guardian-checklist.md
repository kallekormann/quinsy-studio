# Brand Guardian checklist (UX-006)

Run at design spec review and before `./studio move … done` on UI tickets. Visual numbers: [design-science-playbook.md](design-science-playbook.md). Voice: [anti-slop-design-ux.md](anti-slop-design-ux.md). Original logo **mark** is human HITL.

## Always

**Do:** Project tokens, declared aesthetic preset (or `project-brand-only`), one voice table for UI chrome.

**Don’t:** Parallel palette in mocks. Preset hex overriding brand tokens with no mapping. Motivational UI copy.

**Fail:** Contrast table skipped. Two CTA verbs for the same action. Logo lockup invented in a ticket.

## Tokens

- [ ] Colors from `projects/<p>/ui/tokens/design-tokens.css` (not hardcoded hex in components)
- [ ] Light + dark mode pairs documented
- [ ] Contrast table passes WCAG AA

## Typography

- [ ] Font families match project definitions
- [ ] Scale from design spec (φ or modular)

## Voice & tone

- [ ] Microcopy matches project brand (no generic AI phrases — anti-slop)
- [ ] CTA labels consistent across page

## Visual consistency

- [ ] Atomic inventory uses library components where possible
- [ ] **Aesthetic preset** declared in design spec (`knowledge-base/aesthetic-presets/<slug>/`)
- [ ] Preset motion/focus/active states applied via Tailwind + Headless UI (not one-off CSS)
- [ ] Preset does not override project brand tokens without documented mapping

## Platform

- [ ] Layout matches target (desktop / mobile / webapp / extension)

Agent: `teams/10-product-design-experience/agents/design-brand-guardian.md`
