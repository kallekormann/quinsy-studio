# Design direction playbook (gate 2a)

Garrett’s order: **strategy → structure → skeleton → surface**. Gate 2a is strategy + visual DNA. Prototype and sticker sheet are **2b**, after the human signs this packet.

Skills on the CARD: **UX-001, UX-004, UX-006, UX-008**. Not UX-005 pixels yet.

Interview idea distilled from a design-agent ritual: ask only what the PRD did not already answer. Do not vendor a 40-question survey.

## Always

**Do**

- Read PRD + definitions first. Write **unanswered** questions to `docs/design/discovery.md` (`Q:` / `A:`).
- Stop for HITL until the human fills `A:` lines. Do not invent brand, hex, or “Stripe-like”.
- Then fill `design/DESIGN.md`: goals, posture, visual DNA, uniqueness / what we are not, type, **color roles** (token **names**), voice, motion, anti-patterns.
- Aesthetic presets are a **craft substrate**, not the identity. Name one slug in `design/DESIGN.md` and a product delta (audience job, density, posture, what we are not). Uniqueness beats the catalog. A clone name with no delta still fails. Missing preset also fails.

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
- No aesthetic preset slug, or a preset named with no product delta.
- Missing `design/DIRECTION-CRITIQUE.md`, or any rubric line marked FAIL.

## Critique before HITL

After `DESIGN.md` is filled, UX-008 writes `design/DIRECTION-CRITIQUE.md` in a **second pass**. Each line is `PASS` or `FAIL`:

- Audience (from the PRD, not an invented persona)
- Preset (substrate plus product delta)
- Type (named families)
- Color (roles, not a dumped indigo palette)
- Density
- Banned patterns (blobs, glass, hero type on app chrome, emoji icons, default indigo unless the human wrote it in discovery)

`./studio approve --gate 2a` stays HITL, and only after every line is PASS. Execute stays on IMPLEMENT while the critique fails. Three distinct failing passes are logged in `docs/phases/revisions.md` and `design/critique-log.json`; the next failure stops for a human redirect.

## Interview order (unanswered only)

1. Job done in one sitting; sovereign vs transient; density.
2. What this product must **not** look like (references the human hates).
3. Voice in chrome; a phrase we would never say.
4. Light / dark default; type we already own or must avoid.
5. Color **roles** the human states (names, not a dumped palette).
6. Screens they *want* us near — what specifically (layout, type), not “vibe”.

Adopt / brownfield: 2a is **keep vs evolve** the existing UI (`docs/ia/surface-map.md`). Still no fake greenfield prototype.

## After 2a

`./studio design --scope journey|core-views` pulls the studio-library base kit (`button`, `input`, `popover`, `tooltip`, `dropdown-menu`, `dialog`, `sidebar`, `auth-login`, plus `studio-rail` on `saas-application`) and styles it with project tokens. The prototype also includes the shell around the PRD journey: marketing and legal for public products, sign-in, register, app shell, settings, and empty/loading/error. `internal-tool` skips marketing. `api-service` has no UI prototype.

On `./studio approve --gate 2b` the prototype mocks are copied into the product app. `design/prototype/` stays the visual baseline. Implementation wires data and may enhance UX, IA, structure, and infrastructure. A silent rewrite of a pulled control fails move-to-done unless the receipt has an `Enhancement:` line.

Iterate with `./studio revise --gate 2b` until `./studio approve --gate 2b`. Look stays in the **project**. Studio-library stays Headless primitives. Adopt / brownfield does not materialize a parallel app.

See [ux-research-playbook.md](ux-research-playbook.md) (human interview, not invented personas) and [anti-slop-design-ux.md](anti-slop-design-ux.md) U-C2.
