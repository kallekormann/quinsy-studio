---
name: linear-like-ui
description: Professional high-end SaaS productivity aesthetic. Masterclass dark-mode dominance, hairline borders, ultra-subtle gradients, and keyboard-first interactive feedback.
---

# linear-like-ui

Apply this aesthetic configuration when a high-end software tool, dark SaaS dashboard, or premium productivity vibe is requested:

* **Canvas & Architecture:** Compact, dense layouts built for efficiency (`p-4` to `p-6`). Micro-radiuses (`rounded-md` or `rounded-lg`). Absolute precision dark theme (`bg-[#12111a]` or `bg-[#0c0b10]`). Containers use fine dark hairlines (`border border-white/[0.08]`).
* **Typography:** Clean, sharp utility sans-serif (`font-sans` via `Geist Sans`, `Inter`, or `SF Pro`). Small font sizes (`text-sm`, `text-xs`) with precise tracking.
* **Colors & Shadows:** Monochromatic dark core with rich, single-pixel top borders acting as highlights (`shadow-[inset_0_1px_0_0_rgba(255,255,255,0.05)]`). Sophisticated neon-purple or metallic silver accents used sparingly.
* **Headless UI & States:**
  * Transitions: Snap-to-target ultra-fast execution (`duration-150 ease-out`). Popovers and menus translate slightly upward on open (`data-[state=open]:animate-in data-[state=open]:fade-in-0 data-[state=open]:zoom-in-95`).
  * Lists & Command Menus: Keyboard selection is primary. Active states must look perfectly integrated (`ui-active:bg-white/[0.05] ui-active:text-zinc-100`). Include visible shortcut badges (`kbd`).
  * Focus: Sharp accent border overrides (`focus-visible:outline-none focus-visible:border-purple-500/50 focus-visible:ring-1 focus-visible:ring-purple-500/30`).
