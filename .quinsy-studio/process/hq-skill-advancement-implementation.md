# HQ-SKILL — implementation plan

> Binding ticket list: [hq-skill-advancement-sprints.md](hq-skill-advancement-sprints.md) (`LO-0331`–`LO-0339`).  
> **HQ session only.** `./studio guard` must return `STUDIO_META`. Do not `./studio execute` a product.  
> Infusion: `./studio infusion-delta` (no full-file rewrite). After each LO: tests if tools changed, `.quinsy-studio/CHANGELOG.md`, move LO to `backlog/done/`.

**Chat ritual**

```bash
./studio verify-worlds
# This chat: HQ only. Implement one LO, then the next.
```

**Catalog read rule:** when a LO lists a catalog skill, **open that `SKILL.md`** (clone under `external-skills/` after 0331, or raw GitHub) and distill 3–8 Do/Don’t/fail lines. Do not paste the catalog.

---

## Global order (do not skip)

| Step | LO | Sprint | Depends on |
|------|-----|--------|------------|
| 1 | **0331** Subscribe | HQ-SKILL-01 | — |
| 2 | **0332** Team 10 distill (**`scroll-experience`** + **`theme-factory`**) | HQ-SKILL-02 | 0331 |
| 3 | **0333** IA CLI | HQ-SKILL-02 | — (can parallel 0332 after 0331) |
| 4 | **0334** Token warn / shadcn | HQ-SKILL-03 | 0332 |
| 5 | **0335** FE distill + FE-007 | HQ-SKILL-03 | 0331 |
| 6 | **0336** BE distill + BE-006 | HQ-SKILL-04 | 0331 |
| 7 | **0337** AI-004 + AI-003 durable workflows (`workflow-automation`) | HQ-SKILL-05 | 0331 |
| 8 | **0338** Python scans + AI eval receipt | HQ-SKILL-06 | 0334, 0335, 0337 |
| 9 | **0339** Registry + GETTING_STARTED | HQ-SKILL-06 | 0331, 0335, 0336, 0337 |

0333 may start as soon as 0331 is done (or in parallel with 0332). 0334 waits for 0332 playbook language. 0338 waits for IDs FE-007 / AI-004 to exist.

---

## LO-0331 — Subscribe (no blob)

**Read:** `skill-dependencies.json`, `update-skills` in `studio.py`, `external_skills_conflict_matrix.md`.

**Do**

1. Add two entries to `skill-dependencies.json`:
   - `superpowers` → `github:obra/superpowers@main` — team 09 — usage: debugging/review/avoid-ai-writing. **Not** `executing-plans`.
   - `anthropic_docs` → `github:anthropics/skills@main` — team 09/10 — pdf/pptx/xlsx/docx.
2. Conflict matrix: new columns; mark `executing-plans` ❌; aitmpl `npx claude-code-templates` without a named path ❌; Bright Data scrape default ❌.
3. `./studio update-skills superpowers` and `./studio update-skills anthropic_docs` (or whatever keys you used). Confirm `.quinsy-studio/external-skills/INDEX.md`.
4. Registry: one row each under External Skills.
5. CHANGELOG.

**Done when:** clones exist, matrix forbids the blob, INDEX lists them.

---

## LO-0332 — Team 10 distill + `scroll-experience` + `theme-factory`

**Read first (catalog):**  
`creative-design/scroll-experience/SKILL.md` (Apache, vibeship-spawner).  
`creative-design/theme-factory/SKILL.md` (10 packs + custom; wait for human pick).  
Then: `frontend-design`, `ui-design-system`, `ux-researcher-designer`, `figma-implement-design`, `mobile-design`, `web-design-guidelines`, `mermaid-diagrams`, `c4-architecture`, `canvas-design`.  
**Anti-pattern only:** `ui-ux-pro-max` (do not copy palettes). **shadcn** is still not the kit (LO-0334).

**`scroll-experience` distill (required)**

| Playbook | Distill |
|----------|---------|
| `interaction-ux-playbook.md` | Scroll is navigation, not a movie controller. **Don’t:** scroll hijack, replace wheel, break back/history. **Do:** scrub/enhance; sticky/pin only when the job needs it; story beats (hook → context → journey → climax → CTA) on **commercial-web / marketing-page** only. |
| `delight-playbook.md` | Visceral motion on scroll is **surface delight**. Rule zero still wins. **Don’t:** animation overload; hide critical copy until a tween finishes. |
| `visual-storytelling-playbook.md` | Beats + sticky walkthroughs for UX-007. Horizontal pin = optional, must degrade on small screens. |
| `anti-slop-design-ux.md` | Cinematic clichés (“immersive journey”, “thumb movie”) are slop unless the spec names one beat and one motion. |
| `growth-mechanics-playbook.md` | Team 11: scroll stories on landing only if GD-001 has a claim; no fake progress. |
| `frontend_playbook.md` (pointer; full FE in 0335) | Prefer CSS `scroll-timeline` / `position: sticky` before GSAP/Lenis. **Don’t** add GSAP to studio-library by default. |
| FE-004 pointer | `prefers-reduced-motion: reduce` → static layout, same content. |

**Spec-fail (approve-design / Team 10):** marketing-page with parallax and no reduced-motion note; content only visible after animation; desktop-only scroll story.

**`theme-factory` distill (required)**

Catalog is a **picker + apply** toolkit (showcase → HITL confirmation → cohesive color+type). Studio already has 17 aesthetic presets.

| Playbook / skill | Distill |
|------------------|---------|
| `aesthetic-presets.md` / UX-005 | **Show repertoire, wait for pick, then apply.** Product screens: map the choice to **one** studio preset slug or `project-brand-only`. Then tokens. Never ship “Ocean Depths” hex in app CSS. |
| `design-science-playbook.md` | Palette + type **together**. Contrast via `design_math` before approve-design. |
| Brand Guardian / UX-006 | Same ritual as logo: no surprise restyle. Custom “generate a theme” is HITL, then token translation. |
| UX-007 artifacts (slides, PDF, reports) | Factory’s 10 packs **may** apply to those artifacts after HITL. Product chrome still uses project tokens. |
| FE-002 pointer | Second palette on a live product = implement-fail (LO-0334). |

**Spec-fail:** design spec names a catalog theme name as the product palette without a preset slug / token map.

**Also in this LO**

- Infusion-delta into `product-ux-playbook.md`, `ux-research-playbook.md`, `design-science-playbook.md`.
- New `knowledge-base/skill-extensions/figma-token-handoff.md` + README row.
- Thin skills UX-002 / UX-005 / UX-007: one line each for scroll-experience and theme-factory.
- **No UX-009.**

**Done when:** playbooks have Do/Don’t/fail for scroll **and** theme picker; figma extension exists; CHANGELOG; still 8 UX IDs.

---

## LO-0333 — IA audit CLI

**Read:** `design_math.py` (`ia_nav_audit`), `design_ticket_helpers.py` (approve-design), UX-003 skill.

**Do**

1. Add `studio_ia_audit.py` (or functions in `design_ticket_helpers`) that parse spec for top-level count + max depth (document the heading/field, e.g. `ia_nav: { top: N, depth: M }` or a table in §2).
2. CLI: `./studio ia-audit <project> <TICKET>` prints findings (empty list = pass).
3. `approve-design` for `ticket_type: ia-navigation`: fail if counts missing **or** `ia_nav_audit` non-empty (≤7 top, depth ≤3).
4. Tests in `test_design_math.py` / `test_design_ticket_helpers.py`.
5. UX-003 skill: “run `./studio ia-audit`”.

**Done when:** unit tests green; approve-design refuses a fixture spec with 9 top-level items.

---

## LO-0334 — Design system application

**Read:** FE-002 skill, `frontend_playbook.md`, `run_qa_gate.py`.

**Do**

1. Playbook Don’t: second palette; **shadcn is not the kit** (Radix + studio-library).
2. Gate 5 **warn** on `#` hex / `rgb(` in product `app/` or `src/` UI files. Allowlist: generated canvas, `tokens.css`, tests, `node_modules` (never scan).
3. Conflict matrix / registry note: shadcn not pullable as kit.
4. Tests with a tiny fixture file containing `#ff00aa`.

**Done when:** warn appears in gate 5 output; documented allowlist; CHANGELOG.

---

## LO-0335 — Frontend + FE-007

**Read catalog:** second-pass FE list in the epic (`react-state-management`, `tanstack-query-expert`, `zustand-store-ts`, `i18n-localization`, `core-web-vitals`, Playwright cluster, `nextjs-best-practices`, …).

**Do**

1. Infusion-delta `frontend_playbook.md` + `qa-gate-playbook.md`.
2. New `teams/01-frontend-experience/skills/client-security.md` (`FE-007`). CARD: XSS/CSP/tokens; pointer to `frontend-security-auditor.md`.
3. Team 01 README + `skill-registry.md` + `ticket-team-allocation.md`: UI implement includes FE-007.
4. FE-006: role-based Playwright locators (from catalog), not a second QA team.
5. FE-005: point `progressive-web-app` catalog only when ticket says PWA.

**Done when:** FE-007 exists; allocation lists it; playbook has App Router / query / i18n Don’ts.

---

## LO-0336 — Backend + BE-006

**Read catalog:** postgres/optimizer, `bullmq-specialist`, `laravel-expert`, `saas-multi-tenant`, `openapi-to-typescript`, `stripe-integration`, `backend-to-frontend-handoff-docs`.

**Do**

1. Infusion-delta `backend_playbook.md` (indexes/FKs, idempotency, jobs, handoff). Cross-pointer: durable **agent** workflows are AI-003 (`workflow-automation`); BE-006 is queues/outbox/workers.
2. New `teams/02-backend-systems/skills/jobs-and-delivery.md` (`BE-006`). Triggers: queue, job, worker, outbox, sync.
3. Registry + Team 02 README.
4. Keep migrate `./studio env … migrate --approve`; names-only secrets.

**Done when:** BE-006 on CARD for job tickets; spine sections exist.

---

## LO-0337 — AI-004 + retarget AI-003 + `workflow-automation`

**Read catalog:** `workflow-automation/workflow-automation/SKILL.md` (required). Then `llm-evaluation`, `rag-implementation`, `llm-app-patterns`, `prompt-engineering-patterns`, `prompt-caching`, `context-window-management`, `agent-evaluation`. Optional siblings: `inngest`, `n8n`, `n8n-workflow-patterns`, `trigger-dev`.

**Do**

1. Infusion-delta `ai_automation_playbook.md` — durable execution Do/Don’t (idempotency keys, checkpointed steps, activity timeouts, no side effects in orchestrator, exponential backoff, no huge payloads in workflow state).
2. New `teams/07-ai-autonomous-systems/skills/eval-and-context.md` (`AI-004`).
3. Rewrite AI-001 provider laundry list → adapter + eval + user-visible surface (LO-0017).
4. AI-003: **not** GitHub Actions (PE-002). **Is** studio train/infusion **plus** product/studio durable agent jobs. Point at BE-006 for queues. Platform (n8n vs Temporal vs Inngest vs in-app workers) is an **ADR**, not a studio default.
5. Registry triggers: RAG, eval, context window, durable workflow, orchestrator, Inngest, Temporal (not “CI/CD”).
6. Prompt-injection: one bullet pointing at PE-003 (defensive).

**Done when:** AI-004 exists; AI-003 owns durable workflows not CI; playbook has the catalog anti-patterns distilled.

---

## LO-0338 — Python checks

**Depends on:** FE-007 and AI-004 files existing.

**Do**

1. `studio_skill_checks.py`:
   - token hex warn (share allowlist with 0334)
   - native `<select>` warn in product UI (not library primitives)
   - AI receipt: if ticket skills include AI-001 or AI-004, require an `Eval` heading (same style as Default flow / LO-0051)
2. Wire warn into `run_qa_gate.py` level 5.
3. `move … done`: start as **warn**, then **refuse** AI receipts missing Eval if tests are stable.
4. `test_studio_skill_checks.py`.

**Done when:** tests cover hex, select, eval heading; CHANGELOG.

---

## LO-0339 — Docs + CARD lists

**Do**

1. `skill-registry.md`: counts (FE 7, BE 6, AI 4), mappings for new IDs, epic link (already started), catalog rows including `scroll-experience` → UX-002/007 and `theme-factory` → UX-005/006/007.
2. `ticket-team-allocation.md` implement column.
3. GETTING_STARTED: epic + `./studio ia-audit` + new IDs.
4. AGENTS.md one line if CARD constitution needs FE-007/AI-004 (only if execute CARD is generated from registry — then update that generator).
5. CHANGELOG.

**Done when:** an agent reading GETTING_STARTED can find HQ-SKILL and the three new IDs.

---

## `scroll-experience` — implement notes (so 0332 is not vague)

Catalog anti-patterns we **keep:** no scroll hijack; no animation overload; no desktop-only parallax.

Catalog patterns we **adapt, not copy:** GSAP/Lenis/Locomotive are **project choices** via ADR, not studio-library defaults. Spec may name CSS `animation-timeline: view()` first.

**CARD load:** `marketing-page`, `workflow-explainer` (long scrolly), commercial-web class. **Not** settings/operator tables (`product-app`).

**Team split:** Team 10 writes beats + reduced-motion + content-first. Team 01 implements without hijack and without CLS. Team 11 only if the page is a funnel (GD-001).

---

## `theme-factory` — implement notes (so 0332 is not vague)

Catalog value: **explicit HITL choice**, cohesive **color + type pairing**, optional packs for **slides/docs**.

**Do not:** replace `knowledge-base/aesthetic-presets/` with Ocean Depths / Sunset Boulevard as product tokens. **Do not** auto-generate a palette and apply it without `approve-design` / brand HITL.

**Do:** spec § visual names a **preset slug** (or `project-brand-only`) after the human picks. Artifact-only work (pitch deck, PDF) may use a factory pack after confirmation. Custom theme → review → map into tokens.

**CARD load:** gate 2 / UX-005 / UX-007 artifact tickets. Operator `product-app` screens stay on existing project tokens unless the ticket is a rebrand (HITL).

---

## Tests to run per LO

| LO | Command |
|----|---------|
| 0331 | `./studio update-skills` for the two keys; no product name in new files (`./studio verify-abstraction`) |
| 0332 | `./studio verify-abstraction`; no product nouns outside provenance |
| 0333 | `python3 -m unittest test_design_math.py test_design_ticket_helpers.py` (from `studio-tools/`) |
| 0334–0338 | unittest for the new/changed modules + `test_studio_execute.py` if CARD lists change |
| 0339 | docs only + verify-abstraction |

---

## Out of scope (same as epic)

No `projects/` code. No aitmpl blob install. No UX-009. No GSAP in studio-library. No offensive security skills. No product execute in this chat.
