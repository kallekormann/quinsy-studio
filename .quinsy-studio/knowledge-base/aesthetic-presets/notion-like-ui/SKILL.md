---
name: notion-like-ui
description: Tactile document and workspace minimal-creative aesthetic. Off-white and soft paper canvas, hand-drawn utility details, inline-focused metadata layouts, and completely flat structural panels.
---

# notion-like-ui

Apply this aesthetic configuration when a personal productivity, note-taking, docs-heavy, or collaborative knowledge-base vibe is selected:

* **Canvas & Architecture:** Utterly flat, document-first canvas layouts. Backgrounds are clean soft whites (`bg-white`) or paper tints (`bg-[#FBFBFA]`). Cards use zero drop shadows, relying on very light gray borders (`border border-neutral-200`). Radiuses are standard consumer-friendly boundaries (`rounded-md`).
* **Typography:** Clean, approachable grotesque or simple system sans-serif (`font-sans` via `Inter`, `Segoe UI`, or `SF Pro`). Code snippets use strict monospace blocks. High reliance on large, bold, clean page title treatments.
* **Colors & Shadows:** Muted, desaturated pastel tints for tags and highlights (soft yellow, faded green, light gray-blue background tokens). Exclude heavy gradients and rich volumetric shadows completely (`shadow-none`).
* **Headless UI & States:**
  * Transitions: Low-key, transparent fades for menus and selection boxes (`duration-150 ease-out`).
  * Active States: Hovering over nested structures or menus applies a universal, subtle tint background sweep (`ui-active:bg-neutral-100/80 ui-active:text-neutral-900`). List options look like native operating system text blocks.
  * Focus: Discrete, non-disruptive focus indicators (`focus-visible:outline-none focus-visible:bg-neutral-100`).
