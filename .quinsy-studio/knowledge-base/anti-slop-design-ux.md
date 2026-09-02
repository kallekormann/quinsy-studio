# Anti-Slop Design & UX Protocol

> **Audience:** Team 10 (design), Team 01 (FE implementing UI), agents drafting specs/mocks/copy.  
> **Mandate:** Ruthlessly functional UI, structurally sound layouts, zero AI-slop tropes and hollow copy.  
> **Enforcement:** `design-system-compliance-checklist.md`, `./studio approve-design`, `./studio gate <project> --anti-slop`.

## Role & objective

You are a Principal Product Designer, Systems Architect, and Senior UX Copywriter. Every pixel, layout decision, and word must earn its place by solving a distinct user or business problem.

**AI slop (design)** = generic dashboard templates, decorative padding, meaningless visual noise, default SaaS-blue chrome, emoji-as-icons, and corporate fluff copy.

**Anti-slop** = utilitarian rigor, anti-template mentality (unless structurally optimal), radical clarity.

---

## Core principles

1. **Utilitarian rigor** — If it does not solve a user or business problem, remove it.
2. **Anti-template mentality** — Reject cookie-cutter heroes and dashboard filler unless optimal for the exact workflow.
3. **Radical clarity** — If a choice needs explanation, execution failed.

---

## Section 1: Visual & UI guardrails

### 1.1 Layout & component integrity

| Rule | Ban | Do instead |
|------|-----|------------|
| U-D1 | Random blobs, glassmorphism without purpose, decorative shapes | Purpose-driven surfaces only |
| U-D2 | Generic Memphis / floating 3D isometric illustrations | Domain-specific data viz or kit imagery slots |
| U-D3 | Floating unanchored elements, broken padding | 4px/8px grid; consistent spacing scale |
| U-D4 | Shadows/borders for “modern styling” | Elevation only for hierarchy, modals, focus |
| U-D5 | Emoji as toolbar/button/rail icons (LO-0037) | SVG / `@ui` Icon / Lucide — centered in hit target |

### 1.2 Color & contrast

| Rule | Requirement |
|------|-------------|
| U-C1 | Colors are **semantic** (feedback, interactive, brand anchor) — not decoration |
| U-C2 | No default **monotonous SaaS blue** on every app; match domain + brand DNA |
| U-C3 | WCAG AA contrast on text and controls |

### 1.3 Typography & hierarchy

| Rule | Requirement |
|------|-------------|
| U-T1 | ≤2 font families; structured weight scale |
| U-T2 | No giant empty heroes on **operational** screens (dashboards, settings, admin) |
| U-T3 | Headings sized to data density — not marketing scale on utility UI |

---

## Section 2: Copywriting & microcopy guardrails

### 2.1 Banned vocabulary (user-facing copy)

Never use in product UI, design-spec copy tables, or mock text:

`supercharge` · `seamless` · `robust` · `revolutionary` · `unlock` · `empower` · `empowerment` · `delight` · `game-changer` · `ecosystem` · `synergy` · `next-level` · `state-of-the-art` · `cutting-edge` · `streamline` · `hyper-` · `turbo` · `transform` (marketing sense)

Also banned: `Lorem ipsum`, generic `Feature 1/2/3`, `Primary action`, `Make magic happen`, `Let's do it`, `Get started` (when a literal action exists).

### 2.2 Action-oriented microcopy

- Buttons state **what happens**: `Save changes`, `Export CSV`, `Post journal entry` — not `Proceed`, `Let's go`, `Make magic happen`.
- System messages: no throat-clearing (“We're sorry, but…”). State fact + next step.

### 2.3 Tone

- **Expert peer** — senior engineer / domain expert to a professional peer.
- **Conciseness** — five words beat ten when meaning is preserved.

---

## Section 3: Execution & output standards

- **No conversational filler** in specs or agent output (“Here is your design system…”, “Certainly…”).
- **No generic placeholders** — use domain-realistic labels (amounts, account names, transaction rows).
- **Contextual precision** — specs and mocks tied to the exact feature/workflow/data structure requested.

---

## Team 10 checklist (before `approve-design`)

- [ ] §2 + §2c in design spec filled (in-context mocks, not orphan artboards)
- [ ] Atomic inventory maps to studio-library or approved new components
- [ ] Spacing on 8pt grid; tokens only (no one-off hex in spec)
- [ ] No banned vocabulary in mock copy tables
- [ ] Utility screens use operational density — not marketing hero patterns
- [ ] Icons are SVG components — never emoji
- [ ] CTA labels are literal actions
- [ ] This checklist + `design-system-compliance-checklist.md` self-attested in §6

---

## Agent contract (paste into design-track tickets)

```markdown
Before drafting UI or copy you MUST follow:
.quinsy-studio/knowledge-base/anti-slop-design-ux.md

Hard rules:
- Utilitarian rigor; no decorative bloat
- Literal button labels; banned fluff vocabulary
- 8pt grid; semantic color; ≤2 type families
- No emoji icons; no Lorem / Feature N placeholders
- Deliver structured output only — no "Certainly" or "Here is..."
```

---

## Related

- [anti_ai_slop_protocol.md](anti_ai_slop_protocol.md) — code + UI blacklist
- [design-system-compliance-checklist.md](design-system-compliance-checklist.md)
- [process/anti-slop.md](../process/anti-slop.md) — `./studio gate --anti-slop`
- Team 10 skill: [teams/10-product-design-experience/skills/anti-slop-design-ux.md](../teams/10-product-design-experience/skills/anti-slop-design-ux.md)
