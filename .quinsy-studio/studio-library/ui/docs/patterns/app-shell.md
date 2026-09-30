# App shell

One persistent shell. The content region changes. The shell does not remount as a new page.

- A view transition may morph the content region.
- Focus moves to the new heading.
- `prefers-reduced-motion` cuts the morph and leaves the content change.
- Do not add GSAP.

Overlays inside the shell follow the behavior contract in `knowledge-base/component-creation-playbook.md`: Escape, focus return, flip then shift inside the viewport, and tokens only.
