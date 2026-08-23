---
name: apple-like-ui
description: Premium Cupertino hardware aesthetic. High-fidelity glassmorphism, strict human interface guidelines, ultra-crisp typography, and organic fluid depth.
---

# apple-like-ui

Apply this aesthetic configuration when a premium, clean, or Cupertino-hardware vibe is selected:

* **Canvas & Architecture:** Perfect symmetry. Soft architectural geometry (`rounded-xl` for standard cards, `rounded-2xl` or `rounded-3xl` for large dialogs). Layered sheets using pure glassmorphism (`bg-white/70 dark:bg-zinc-900/70 backdrop-blur-xl border border-white/20 dark:border-zinc-800/30`).
* **Typography:** System-centric sans-serif (`font-sans` via `SF Pro`, `Inter`, or `Geist`). Strict semantic hierarchy with high tracking-tight on large headers (`tracking-tight font-semibold`).
* **Colors & Shadows:** Pure neutral tones (`bg-zinc-50` or `bg-black`). Accents via system colors (`text-blue-500` or neutral monochrome text). Volumetric, photorealistic shadows that mimic physical light refraction (`shadow-[0_4px_30px_rgba(0,0,0,0.03)]` up to `shadow-[0_20px_40px_rgba(0,0,0,0.12)]`).
* **Headless UI & States:**
  * Transitions: Fluid, organic ease-in-out curve resembling native iOS/macOS (`transition-all duration-300 cubic-bezier(0.25, 1, 0.5, 1)`).
  * Interactive States: Subtle dimming on active clicks (`active:opacity-70 transition-opacity`). Active dropdown items use solid system fills (`ui-active:bg-blue-600 ui-active:text-white`).
  * Focus: Perfectly rounded, non-destructive focus rings (`focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500/50 focus-visible:ring-offset-2`).
