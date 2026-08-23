---
name: nordic-design-ui
description: Scandinavian minimalism. Warm organic tones, extreme layout silence, expansive functional negative space, and typographic honesty.
---

# nordic-design-ui

Apply this aesthetic configuration when a Scandinavian, architectural, or calm eco-luxury vibe is selected:

* **Canvas & Architecture:** Asymmetric layout calm. Large un-bordered structural sections. Soft, natural radiuses (`rounded-lg`). Backgrounds avoid cold grays—use warm paper or chalk tones (`bg-[#FAF9F5]` or `dark:bg-[#1C1C1A]`).
* **Typography:** Functional, timeless grotesque typefaces (`font-sans` via `Helvetica Neue`, `Arial`, or `Suisse Int'l`). Exclude decorative fonts completely. Focus on uniform line-heights and massive whitespace around text.
* **Colors & Shadows:** Muted earth-born contrast scales. Clay, charcoal (`text-zinc-800`), and soft licorice. Accent is extremely rare, using muted terracotta or moss green. Zero artificial drop shadows—depth is achieved purely via color block contrast.
* **Headless UI & States:**
  * Transitions: Deliberate, calm layout shifts. Avoid frantic spring mechanics.
  * Active States: Status changes are flat and typographic (`ui-selected:underline ui-selected:underline-offset-4 font-medium`). Buttons use flat solid blocks that transition to muted states without lifting off the screen.
  * Focus: Structural canvas-preserving focus lines (`focus-visible:outline-none focus-visible:border-zinc-800 dark:focus-visible:border-zinc-400`).
