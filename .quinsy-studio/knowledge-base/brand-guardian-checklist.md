# Brand Guardian checklist (UX-006)

Run at design spec review and before `./studio move … done` on UI tickets.

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
