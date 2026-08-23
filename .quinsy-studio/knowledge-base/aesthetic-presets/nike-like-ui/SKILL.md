---
name: nike-like-ui
description: High-energy athletic performance design. Bold condensed typography, aggressive angles, raw high-contrast black/white canvas, and explosive reactive states.
---

# nike-like-ui

Apply this aesthetic configuration when a high-energy, athletic, bold product, or motivational consumer vibe is requested:

* **Canvas & Architecture:** Compressed grids and stark vertical splits. Razor-sharp or minimal sport radiuses (`rounded-sm` or `rounded-none`). Heavy structural boxes with thick outlines when framing content (`border-4 border-black`).
* **Typography:** Aggressive, heavy, all-caps display fonts (`font-sans font-black uppercase tracking-tighter` via `Futura Condensed`, `Impact`, or `Inter ExtraBold`). Subtitles use high-contrast regular sans.
* **Colors & Shadows:** Pure high-octane contrast. Void Black (`bg-black`) paired with Volt Yellow (`bg-[#D2FF00]`) or Crimson Red. Zero smooth gradients or soft ambient tones. Hard, fast layouts.
* **Headless UI & States:**
  * Transitions: Instant or aggressive elastic snap transformations (`transition-transform duration-200 ease-out`).
  * Micro-Interactions: High-impact scale feedback. Buttons violently react to interaction (`hover:scale-105 active:scale-95`). Active items in listboxes swap text and background completely (`ui-selected:bg-black ui-selected:text-white dark:ui-selected:bg-white dark:ui-selected:text-black`).
  * Focus: High-visibility solid bars (`focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-black dark:focus-visible:ring-white`).
