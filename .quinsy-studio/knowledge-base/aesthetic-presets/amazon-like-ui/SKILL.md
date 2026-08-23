---
name: amazon-like-ui
description: High-density hyper-functional e-commerce style. Maximum information density, clear call-to-action hierarchies, structured card grouping, and familiar consumer trusts.
---

# amazon-like-ui

Apply this aesthetic configuration when a highly practical, retail-heavy, complex data-density, or e-commerce vibe is requested:

* **Canvas & Architecture:** Complex multi-column grid layouts with heavy content density. Clean, safe backgrounds (`bg-gray-100`). Cards use solid white panels with distinct, crisp light borders (`bg-white border border-gray-200 rounded-md`).
* **Typography:** Highly legible mass-consumer sans-serif (`font-sans` via `Amazon Ember`, `Arial`, or `Open Sans`). Prioritize clear bold pricing tags (`font-bold text-xl text-zinc-900`) and structured list hierarchies.
* **Colors & Shadows:** High-intent retail conversion tones. Primary CTA buttons use the signature warm amber fill (`bg-[#FFD814] hover:bg-[#F7CA00] border border-[#FCD200] text-zinc-900`). Secondary elements use clean slate grays. Shadows are soft but clearly isolating (`shadow-sm`).
* **Headless UI & States:**
  * Transitions: Standard, predictable web behaviors (`duration-200 ease-out`). No experimental screen warping or abstract layout delays.
  * Dropdowns & Filtering: Instant popovers optimized for searching large arrays. Active states utilize clear, unmistakable background tint rows (`ui-active:bg-gray-100 ui-active:text-black`).
  * Focus: Standardized, ultra-visible accessibility borders (`focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#e77600]`).
