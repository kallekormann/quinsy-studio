# Design direction playbook (gate 2a)

Garrett’s order: **strategy → structure → skeleton → surface**. Gate 2a is strategy + visual DNA. Prototype and sticker sheet are **2b**, after the human signs this packet.

Skills on the CARD: **UX-001, UX-004, UX-006, UX-008**. Not UX-005 pixels yet.

Interview idea distilled from a design-agent ritual: ask only what the PRD did not already answer. Do not vendor a 40-question survey.

## Always

**Do**

- Read PRD + definitions first. Write **unanswered** questions to `docs/design/discovery.md` (`Q:` / `A:`).
- Stop for HITL until the human fills `A:` lines. Do not invent brand, hex, or “Stripe-like”.
- Then fill `design/DESIGN.md`: goals, posture, visual DNA, uniqueness / what we are not, type, **color roles** (token **names**), voice, motion, anti-patterns.
- Aesthetic presets are an **optional footnote**, mapped onto those tokens. Uniqueness beats the catalog.

**Don’t**

- Scaffold `design/prototype` or paste `#6366f1` / `bg-indigo-600` before `./studio approve --gate 2a`.
- Fill discovery answers yourself.
- Treat “Ocean Depths” or a preset slug as the signed bible.

**Fail lines (2a validator)**

- Missing or unanswered `docs/design/discovery.md` (`_unanswered_`, fewer than four `A:`).
- `DESIGN.md` still says “Describe look & feel from PRD” or is shorter than a real direction packet.
- Default indigo / SaaS blue in DESIGN.md.
- No Uniqueness / Visual DNA / What we are not section — or a clone name (“Linear-like”) with no product constraints.
- Mood adjective only (no type, color roles, posture, or voice).

## Interview order (unanswered only)

1. Job done in one sitting; sovereign vs transient; density.
2. What this product must **not** look like (references the human hates).
3. Voice in chrome; a phrase we would never say.
4. Light / dark default; type we already own or must avoid.
5. Color **roles** the human states (names, not a dumped palette).
6. Screens they *want* us near — what specifically (layout, type), not “vibe”.

Adopt / brownfield: 2a is **keep vs evolve** the existing UI (`docs/ia/surface-map.md`). Still no fake greenfield prototype.

## After 2a

`./studio design --scope journey|core-views` (or as-built token-map). Iterate with `./studio revise --gate 2b` until `./studio approve --gate 2b`. Look stays in the **project**. Studio-library stays Headless primitives.

See [ux-research-playbook.md](ux-research-playbook.md) (human interview, not invented personas) and [anti-slop-design-ux.md](anti-slop-design-ux.md) U-C2.
