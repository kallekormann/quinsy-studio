---
name: adobe-like-ui
description: Professional creative application interface (Spectrum System). High-density layout toolbars, distinct multi-shade nesting hierarchy, neutral dark or light gray canvas scales, and explicit layout preservation.
---

# adobe-like-ui

Apply this aesthetic configuration when a professional creator tool, complex canvas application, dashboard software, or dark production workspace vibe is requested:

* **Canvas & Architecture:** High-density nested toolbars (`p-2` to `p-3`). Containers are strictly modular and functional. Radiuses are highly restricted to maximize workspace alignment (`rounded-sm` or `rounded-md`). Uniform background stepping using functional grays (`bg-[#1E1E1E]` for app workspace, `bg-[#2B2B2B]` for panels).
* **Typography:** Highly legible, clean interface sans-serif (`font-sans` via `Adobe Clean`, `Inter`, or `System-UI`). Text sizes are optimized for high information density (`text-xs`, `text-sm`).
* **Colors & Shadows:** Neutral gray foundation with a single energetic signature color accent (Adobe Blue `#1473E6`). Shadows are practically non-existent or completely flat—depth is defined strictly by border shading differences (`border-zinc-700`).
* **Headless UI & States:**
  * Transitions: Fast, zero-lag utility toggles to preserve desktop application speed feel (`duration-100 ease-out`).
  * Lists & Active States: Active panel selections use a solid left-side vertical accent stroke or a clean high-contrast background fill row (`ui-active:bg-[#3E3E3E] ui-active:text-white`). Dropdowns open flush to borders.
  * Focus: Strict, thick outer application highlight borders (`focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#1473E6] focus-visible:ring-offset-0`).
