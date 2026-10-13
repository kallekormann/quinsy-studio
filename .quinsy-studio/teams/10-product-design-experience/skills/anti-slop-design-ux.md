# Skill: Anti-Slop Design & UX (UX-008)

> Blocks AI-slop in product UI before Team 10 drafts specs, mocks, or microcopy, and critiques design direction at gate 2a. The bar: a surface a reader cannot attribute to a template, copy a domain expert would write, and mocks rendered by the real app.

## Metadata

```
skill_id: UX-008
name: Anti-Slop Design & UX
team: 10-product-design-experience
lead_role: Brand Guardian / UI Designer
support_roles: [UX Designer, Product Designer]
phases: [2, 4]
activation_triggers:
  - Any design-track ticket (ui-new-component, ui-composition, marketing-page)
  - Brand kit, sticker sheet, Figma kit, HTML catalog
  - ./studio approve-design pre-check; gate 2a direction critique
  - Feedback mentioning "AI slop", generic UI, fluff copy; push-back codes `uniqueness`, `copy`
pairs_with: [UX-006, UX-005, UX-002, GD-001]
```

Default verdict: generic until the spec names what makes this surface this product's.

## When to load

- Before any spec, mock, or copy is drafted on a design-track ticket.
- Gate 2a: critique the proposed direction for uniqueness.
- Reviewing a packet before `approve-design`; reading `uniqueness` / `copy` push-back.
- Not for: backend tickets.

## Rules

### 1. Layout

8pt grid; no decorative blobs or gradients; elevation only for hierarchy. Utilitarian layout for operational screens.

### 2. Colour

Semantic roles from the brand DNA in DESIGN.md; no default SaaS-blue template; no preset palette applied raw.

### 3. Type

≤2 families; operational screens do not use marketing hero scale.

### 4. Copy

Banned-vocabulary list from `knowledge-base/anti-slop-design-ux.md`; literal CTAs; expert-peer tone; no conversational preamble in deliverables. Distill `avoid-ai-writing` / `deslop` into these rules; they do not replace this file.

### 5. Icons and imagery

SVG from the kit only (LO-0037); never emoji as chrome. Imagery follows DESIGN.md and the pixel budgets.

### 6. Mocks

A real app route rendering the real shell, views, and components (§2c), never hand-drawn HTML; domain-realistic data — no `Feature 1`, Lorem, `Primary action`.

### 7. Feature-list pages are slop

A marketing or persona page that opens with a feature grid fails. Problem first, in the persona's words, then the mechanism, then proof (GD-001 / GM-007 / `growth-content-playbook.md`).

### 8. The catalog is read, not remembered

Spec §7b cites PB- ids and push-back codes applied. A `uniqueness` or `copy` rejection repeating on a surface means the rule above was not applied; fix the rule as a PB- bullet in `knowledge-base/anti-slop-design-ux.md` through the learning loop.

## Workflow

1. Read `knowledge-base/anti-slop-design-ux.md` (its PB- bullets) and the push-back log.
2. Paste the agent contract block into the ticket or spec header.
3. Walk the draft against rules 1–7; list every hit with the fix.
4. Run `./studio gate <p> --anti-slop` for copy and placeholder patterns.
5. Attest in spec §7; cite in §7b.

## Deliverables

- Agent contract block in the spec header.
- §7 attestation against this skill and `design-system-compliance-checklist.md`.
- Hit list with fixes when reviewing another team's packet.

## Done evidence

```markdown
## Design skill
- UX-008: §7 attestation — docs/design-specs/<TICKET>.md
- UX-008: ./studio gate <p> --anti-slop clean
- UX-008: §7b cites craft.md ids read
```

## Anti-patterns

- "Modern, clean, intuitive" as a direction.
- Feature grid above the fold.
- Emoji icons, Lorem, `Feature 1`.
- Hand-drawn HTML mocks.
- Fixing the string the human quoted and leaving the vocabulary rule unchanged.

## Handoff

- **To UX-005 / UX-006:** the hit list; they revise values and copy.
- **To GD-001 / GM-007:** page structure for commercial surfaces (problem-first).
- **To the human at gate 2a:** the uniqueness critique of the direction.

## Deltas

- Studio addition: rule 7 (feature-list pages) and rule 8 (catalog proof) come from the HQ autonomy program; the source lists stop at copy and layout.

## References

- [anti-slop-design-ux.md](../../../knowledge-base/anti-slop-design-ux.md) (canonical) · [design-system-compliance-checklist.md](../../../knowledge-base/design-system-compliance-checklist.md)
- [growth-content-playbook.md](../../../knowledge-base/growth-content-playbook.md)
