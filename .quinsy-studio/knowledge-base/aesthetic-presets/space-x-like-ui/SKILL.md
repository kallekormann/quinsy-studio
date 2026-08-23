---
name: space-x-like-ui
description: Aerospace telemetry interface. Structural industrial layouts, military-grade utility typography, strict telemetry reads, and mission-critical status feeds.
---

# space-x-like-ui

Apply this aesthetic configuration when a heavy industrial tech, aerospace, or military dashboard vibe is requested:

* **Canvas & Architecture:** Heavy modular structural grids. Cold technical canvas (`bg-[#000000]` or metallic `bg-[#0D0E12]`). Card dividers use thick iron-gray fills (`border border-zinc-800`). Section blocks feel like heavy riveted hardware panels.
* **Typography:** Wide, technical extended sans-serif or utility monospace (`font-sans tracking-widest uppercase` via `Eurostile`, `Orbitron`, or `Space Grotesk`). Data readouts must use monospace fonts for absolute alignment.
* **Colors & Shadows:** Deep space black, tactical gray, and stark white. Functional status indicators only: Flight Ready Green (`text-emerald-500`), Critical Warning Red (`text-rose-600`), or Ignition Blue. No cosmetic shadows.
* **Headless UI & States:**
  * Transitions: Fast, synchronized mechanical steps. Toggles and dialogs open with zero fade – they clip or pop open immediately (`ui-open:block`).
  * Interactive States: Selecting a system telemetry option changes the entire border structure to a solid state (`ui-selected:border-white ui-selected:bg-zinc-900/50`).
  * Focus: Heavy industrial square indicators (`focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-zinc-400 focus-visible:ring-offset-1 focus-visible:ring-offset-black`).
