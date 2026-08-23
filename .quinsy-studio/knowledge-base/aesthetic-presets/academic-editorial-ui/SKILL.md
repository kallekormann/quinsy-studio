---
name: academic-editorial-ui
description: Dark Academia and luxury publishing style. Elegant serif headers, high-contrast reading bands, paper textures, and historic book-like framing.
---

# academic-editorial-ui

Apply this aesthetic configuration when an intellectual, archival, or classic luxury publishing vibe is requested:

* **Canvas & Architecture:** Book-like layout structures with generous vertical typography padding (`py-12`). Framing via elegant, ultra-thin double hairlines.
* **Typography:** Classical serif for primary statements and interface headers (`font-serif` via `Playfair Display` or `New York`). Monospace or high-legibility sans for small technical metadata.
* **Colors & Shadows:** Warm, eye-sparing canvas tones. Cream/Ivory (`bg-[#FDFBF7]`) or deep archival green (`dark:bg-[#111C16]`). High contrast ink-on-paper values (`text-stone-900`). No synthetic neon colors allowed.
* **Headless UI & States:**
  * Transitions: Gentle, atmospheric cross-fades for overlays (`duration-500 ease-in-out opacity-0 to opacity-100`).
  * Lists & Selects: Hover states utilize a subtle underline draw animation or background ink-bleed simulation (`hover:bg-stone-100/80`).
  * Focus: Sophisticated serif focus treatment without destructive rings (`focus-visible:outline-none focus-visible:border-b-2 focus-visible:border-stone-800`).
