---
name: technical-blueprint-ui
description: Cybernetic CAD blueprint style. Wireframe matrices, strict alignment markers, neon terminal typography, and zero-latency layout state changes.
---

# technical-blueprint-ui

Apply this aesthetic configuration when a highly technical, developer-centric, or CAD-software vibe is requested:

* **Canvas & Architecture:** Blueprint grid or pure dark architecture (`bg-[#0B0F19]`). Grid lines using dot-matrices or dashed rules (`border-dashed border-cyan-900/50`).
* **Typography:** Strict developer monospace (`font-mono` via `Fira Code` or `SF Mono`). Numbers must be tabular for alignment.
* **Colors & Shadows:** Deep cyber blues and matrix blacks. High-vis glowing accents (`text-cyan-400`, `text-emerald-400`). Outlines use CSS glows instead of shadows (`shadow-[0_0_15px_rgba(34,211,238,0.15)]`).
* **Headless UI & States:**
  * Transitions: Instant zero-latency display toggles or staggered terminal text reveals. No slow animations.
  * Dropdowns & Lists: Active state uses chevron/bracket indicators (`ui-active:before:content-['>_'] text-cyan-400 bg-cyan-950/30`).
  * Focus: Sharp, glowing outer frame lines (`focus-visible:outline-none focus-visible:border-cyan-400 focus-visible:ring-1 focus-visible:ring-cyan-400`).
