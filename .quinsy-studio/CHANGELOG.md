# Quinsy Studio CHANGELOG

## 2026-09-12 — Open LO harvest (0206–0230), portability split

### Changed

- `studio-tools/sprint_reuse_review.py` — host `packages/ui` and scoped `@*/ui` are product-local; reuse does not demand promote (LO-0206).
- `process/human-in-the-loop.md` — scope-proposal md/json/execute counts match (LO-0208); human-smoke AC names compose/create path (LO-0223); operator filing stays structured-first (LO-0224).
- `process/ticket-team-allocation.md` — ticket-specific design spec + §2/§2c before sprint scope (LO-0213 / 0218 / 0220 / 0222).
- `knowledge-base/frontend_playbook.md` — shared card organism before a second copy; specimens use library/token styles; print CSS is the PDF source; HTML sticker `</style>` before body (LO-0210 / 0211 / 0212 / 0216 / 0217).
- `knowledge-base/design_playbook.md` — export chrome names filename/format only (LO-0226); list/detail titles truncate (LO-0229).
- `knowledge-base/backend_playbook.md` — pending migrations before treating API 500 as a product bug (LO-0227).
- `knowledge-base/host-port-allocation.md` — smoke on the project RUNBOOK compose URL, never a hardcoded studio port.

### Closed

- Infused: LO-0206, 0208, 0210–0213, 0216–0218, 0220, 0222–0224, 0226, 0227, 0229.
- Removed from HQ backlog (project-local only): LO-0207, 0209, 0214, 0215, 0219, 0221, 0225, 0228, 0230.

## 2026-09-11 — LO-0202–0205 (idle infusion + ticket generator)

### Changed

- `knowledge-base/backend_playbook.md` — LO-0202 closed as duplicate of LO-0200 (host-panel env aliases).
- `process/human-in-the-loop.md` — public `/` with published inventory is the default flow for chrome tickets (LO-0203, LO-0205).
- `knowledge-base/design_playbook.md` — smoke `/` on the RUNBOOK public host port, not only inner slugs (LO-0205).
- `process/ticket-workflow.md` + `studio-tools/ticket_helpers.py` / `studio.py` — `--from-feedback` uses draft AC; skip generic GWT (LO-0204).

### Closed

- LO-0202, LO-0203, LO-0204, LO-0205 infused.


## 2026-09-11 — LO-0200 / LO-0201 idle infusion

### Changed

- `knowledge-base/backend_playbook.md` — accept vendor env aliases in the server resolver; do not leave API secrets as `NEXT_PUBLIC_*` long-term (LO-0200).
- `knowledge-base/design_playbook.md` — selected palette id must drive presentation and PDF, not design-file-only fixes (LO-0201).

### Closed

- LO-0200, LO-0201 infused.


## 2026-09-11 — SPRINT-18 idle infusion (LO-0197–0199)

### Changed

- `process/ticket-team-allocation.md` — `files:` hitting `packages/ui` is not design-track by itself; split visitor-shortlist vs editorial comparison verbs before bulk-select (LO-0197, with LO-0184).
- `process/human-in-the-loop.md` — one listener per published host port: Compose XOR host `npm run dev` (LO-0198, LO-0199).

### Closed

- LO-0197, LO-0198, LO-0199 infused.


## 2026-09-11 — SPRINT-134 retro learnings (LO-0191–0196)

### Changed

- `knowledge-base/frontend_playbook.md` — print unlock for `overflow:hidden` / `h-dvh` shells; selected palette import never invents FALLBACK roles (LO-0191, LO-0192, LO-0194, LO-0196).
- `knowledge-base/design_playbook.md` — plugin HTML icon-only = outline/dimmed, not soft wash (LO-0193).
- `process/human-in-the-loop.md` — print overflow unlock in DoD; gitignored plugin `dist/` needs rebuild+reload for review smoke (LO-0192, LO-0194, LO-0195).

### Closed

- LO-0191, LO-0192, LO-0193, LO-0194, LO-0195, LO-0196 infused.


## 2026-09-11 — SPRINT-133 retro learnings (LO-0187–0190)

### Changed

- `process/human-in-the-loop.md` — print DoD: section wrappers + print-preview page count; plan-only green is not done (LO-0189 / LO-0181).
- `knowledge-base/frontend_playbook.md` — section=page print tree; selected-id bind for palette/kit import-export (LO-0188, LO-0189).
- `knowledge-base/design_playbook.md` + `studio-library/ui/components/button/README.md` — dimmed/outline icon chrome for light+dark (LO-0187, LO-0190).

### Closed

- LO-0187, LO-0188, LO-0189, LO-0190 infused.


## 2026-09-11 — SPRINT-131 retro learnings (LO-0181–0186)

### Changed

- `process/human-in-the-loop.md` — print/PDF receipts need page-count proof (LO-0181); prefer split sprints over 14-ticket polish dumps (LO-0183); bundle plugin shell chrome FBs (LO-0185).
- `process/ticket-team-allocation.md` — do not over-classify chrome polish as design-track (LO-0184).
- `knowledge-base/design_playbook.md` — plugin cold-open shows Login first (LO-0182); moving exports drops leftover helper cards (LO-0186).

### Closed

- LO-0181, LO-0182, LO-0183, LO-0184, LO-0185, LO-0186 infused.


## 2026-09-11 — Sprint-16 learnings (LO-0176–0180)

### Changed

- `process/gates.md` — after a claimed prod-infra fix, next tickets are research + instrumentation (LO-0176).
- `process/agent-context.md` — reuse vendored admin Kanban/table/Dialog/Empty; Add = Dialog, inspect = Sheet (LO-0177, LO-0178).
- `knowledge-base/design-science-playbook.md` — empty states name the previous step and link to it (LO-0179).
- `knowledge-base/backend_playbook.md` — persist native board column ids when wiring the job API (LO-0180).

### Closed

- LO-0176, LO-0177, LO-0178, LO-0179, LO-0180 infused.

## 2026-09-10 — Clear sprint on supersede/cancel (LO-0175)

### Changed

- `process/ticket-workflow.md` / `process/human-in-the-loop.md` — supersede or cancel must clear `sprint:` or `move … cancelled` in the same turn so execute/review cannot pick ghosts.

### Closed

- LO-0175 infused.

## 2026-09-10 — Anti-slop ignores vendored command-center shells

### Changed

- `studio-tools/validate_anti_slop.py` — ignore `apps/command-center` the same way as Filament public assets (vendored admin UI).

## 2026-09-10 — Residual UI needs a render-path ticket (LO-0174)

### Changed

- `process/gates.md` — leftover flicker after a status-only ticket requires a follow-up that changes the render path, not another flag flip.

### Closed

- LO-0174 infused.

## 2026-09-10 — Kit-token Dropdown (AFFI-0071)

### Changed

- `studio-library/ui/components/dropdown/` — Listbox paints from kit CSS variables (`--color-border`, `--color-background`, `--color-foreground`, `--color-muted`, `--color-accent`, `--font-ui`) instead of Moody class names.
- `studio-library/ui/tokens/design-tokens.css` — aliases those kit names onto the canonical surface/text/primary tokens.

## 2026-09-10 — Deployed review push; reuse inform-auto; gutter; pooler (LO-0167–0173)

### Changed

- `process/human-in-the-loop.md` / `process/agent-context.md` — git-deployed sprint review needs a product-repo push after MOVE_DONE (LO-0167, LO-0170); drop accidental `--help` feedback before retro (LO-0173).
- `studio-tools/studio.py` / `sprint_hitl.py` — reuse inform completes when paths are recorded; no `--approve` (LO-0169).
- `studio-library/library_registry.md` — `--record local` on brand UI when the ticket ships (LO-0171).
- `knowledge-base/design_playbook.md` — `scrollbar-gutter: stable` on public chrome (LO-0172).
- `knowledge-base/backend_playbook.md` — pooler tenant/SNI; apply DDL on the primary, not a bare pooler port (LO-0168).

### Closed

- LO-0167, LO-0168, LO-0169, LO-0170, LO-0171, LO-0172, LO-0173 infused.

## 2026-09-09 — Soft npm_audit label; warm Playwright cache (LO-0165, LO-0166)

### Changed

- `studio-tools/run_qa_gate.py` — `npm_audit` soft fails show ⚠️ and “does not fail RESULT” when hard checks pass (LO-0165).
- `process/gates.md` — warm `.quinsy-studio/.cache/playwright/<project>/` via `smoke:install` before smoke-heavy sprints (LO-0166); document npm_audit soft policy.

### Closed

- LO-0165, LO-0166 infused.

## 2026-09-09 — Dual-surface delete; reuse skip product packages; billing env (LO-0158–0164)

### Changed

- `knowledge-base/design_playbook.md` / `chrome-mv3-vite-content-scripts.md` — companion ↔ cloud delete must be bidirectional before “inbox ready” (LO-0158, LO-0160).
- `studio-tools/sprint_reuse_review.py` / `studio-library/library_registry.md` — skip figma-plugin/extension and `.DS_Store`/`dist` as promote noise (LO-0162, LO-0164).
- `knowledge-base/backend_playbook.md` — server-only secrets + host env contract in the same billing ticket (LO-0163).

### Closed

- LO-0158, LO-0160, LO-0162, LO-0163, LO-0164 infused.

## 2026-09-09 — Extension global-arm order; never silent focus switch (LO-0157, LO-0159, LO-0161)

### Changed

- `knowledge-base/chrome-mv3-vite-content-scripts.md` — global mode: fan-out + inject-on-miss before persisting armed storage (LO-0157, LO-0159).
- `process/agent-context.md` — do not `./studio focus` another product unless the human explicitly asks to switch; chat/execute topic mismatch stays on active project (LO-0161).

### Closed

- LO-0157, LO-0159, LO-0161 infused.

## 2026-09-09 — Operator click before job polish; recreate Compose workers (LO-0155, LO-0156)

### Changed

- `process/human-in-the-loop.md` / `process/agent-context.md` — a queued job is not the default flow until the operator control that enqueues it ships; implement that click before notify/revalidate polish when the human is waiting (LO-0155).
- `knowledge-base/backend_playbook.md` — recreate queue workers and the public app after Compose queue/env/volume edits; use the service hostname for container-to-container URLs (LO-0156).

### Closed

- LO-0155, LO-0156 infused.

## 2026-09-09 — Public document matches operator Save (LO-0154)

### Changed

- `process/human-in-the-loop.md` — published Save must be what the public document route serves; no silent fixture fallback when a live record id exists (LO-0154).

### Closed

- LO-0154 infused.

## 2026-09-09 — Public nav DoD + operator edit layout (LO-0151, LO-0152)

### Changed

- `process/human-in-the-loop.md` — public nav lists only published, non-empty destinations (LO-0151). Operator edit: tabs under header actions, ordered map first, one field per row (LO-0152).
- `process/learning-loop.md` — named 404s in a brand masthead stay in the project-local log; the portable rule is empty-destination chrome.

### Closed

- LO-0151, LO-0152 infused.
- LO-0153 closed as duplicate of LO-0150 (project public chrome stays local at reuse).

## 2026-09-09 — Warn that IDE focus is not a product sandbox

### Changed

- `README.md` and `GETTING_STARTED.md` — several products in one workspace can still be seen by the agent; users keep one chat/CLI process per product.

## 2026-09-09 — Ordered admin maps as lists (LO-0149)

### Changed

- `process/human-in-the-loop.md` — ordered named rows (section/nav maps) ship as a table/list, not a stacked card Repeater (LO-0149).

### Closed

- LO-0149 infused.

## 2026-09-09 — Project public chrome stays local (LO-0150)

### Changed

- `studio-library/library_registry.md` — project `packages/ui` masthead/nav/page renderers stay `local` at reuse; do not promote host face into HQ (LO-0150).

### Closed

- LO-0150 infused.

## 2026-09-09 — Sibling project isolation (focus / guard / git)

### Added

- `studio_isolation.py` — `./studio focus`, `./studio isolate`, and `./studio execute` hide other `projects/*` via `.cursorignore` + a generated Cursor rule. Guard returns `CROSS_PROJECT` if the request names a sibling. Execute CARD prints `ISOLATE`. Project `pre-commit` refuses a wrong git toplevel, escaped paths, and `projects/` symlinks.
- `verify-worlds` reapplies isolation for the active project and fails if that project's git toplevel is the wrong repo.

### Changed

- `.gitignore` — `.cursorignore` and `.cursor/rules/quinsy-project-isolation.mdc` are local (regenerated on focus).

## 2026-09-09 — Closed-library editor + visitor preview (LO-0148)

### Changed

- `process/human-in-the-loop.md` — operator editor matches the public block library and visitor template, not a Word/HTML page field (LO-0148).

### Closed

- LO-0148 infused.

## 2026-09-09 — Seeded corpus is not the next-wave backlog (LO-0147)

### Changed

- `knowledge-base/backend_playbook.md` — further corpus work uses the idea queue / admin briefs, not a silent rewrite of the seeded set (LO-0147).

### Closed

- LO-0147 infused.

## 2026-09-08 — Close sprint review when this sprint is done (LO-0144)

### Changed

- `process/human-in-the-loop.md` — do not keep sprint review open for later amendments, consoles, or unwritten skills that are still only feedback (LO-0144).
- `process/lifecycle.md` — Phase 7 review is for shipped sprint tickets (LO-0144).

### Closed

- LO-0144 infused.

## 2026-09-08 — Isolated test DB pin + operator idea queues (LO-0145 / LO-0146)

### Changed

- `process/gates.md` — `phpunit.xml` `force` is not enough inside Compose; TestCase must pin the isolated test database before schema refresh (LO-0145).
- `knowledge-base/backend_playbook.md` — same TestCase pin (LO-0145); operator idea queues belong in product admin, not IDE chat (LO-0146).
- `teams/02-backend-systems/skills/api-design.md` — toolbox: in-product idea queue (LO-0146).
- `teams/02-backend-systems/skills/error-handling.md` — toolbox: do not treat chat paste as the system of record (LO-0146).

### Closed

- LO-0145, LO-0146 infused.

## 2026-09-08 — Upgrade soft-path DoD (LO-0142 / LO-0143)

### Changed

- `studio-library/ui/docs/patterns/upgrade-soft-path.md` — soft-path must surface Free + Upgrade or auto-open upgrade dialog (LO-0142).
- `studio-library/ui/docs/README.md` — index link to upgrade soft-path pattern.
- `knowledge-base/frontend_playbook.md` — cross-link soft-path Account pattern (LO-0142).
- `knowledge-base/skill-extensions/product-led-growth.md` — soft-path Account DoD (LO-0142 / LO-0143).
- `process/gates.md` — free-tier Account assert before soft-path tickets are done (LO-0143).
- `teams/09-…/skills/studio-tooling-maintenance.md` — toolbox TR-0011 (LO-0142/0143).
- `teams/10-…/skills/visual-ui-design.md` — toolbox TR-0012 (LO-0142).
- `teams/01-…/skills/design-system.md` — toolbox TR-0013 (LO-0142).

### Closed

- LO-0142, LO-0143 infused.

## 2026-09-08 — Filament home is the resource list (LO-0141)

### Changed

- `knowledge-base/backend_playbook.md` — admin `homeUrl` to the primary resource index; header stats widgets must not stay lazy (LO-0141).

### Closed

- LO-0141 infused.

## 2026-09-08 — Legal disclosure needs network assert (LO-0139 / LO-0140)

### Changed

- `process/gates.md` — when Privacy forbids pre-auth / anonymous font CDNs, smoke must assert network on marketing **and** anonymous share/presentation surfaces in the same sprint (LO-0139 / LO-0140).

### Closed

- LO-0139, LO-0140 infused.


## 2026-09-08 — Gate uses project Prettier; first-brand chrome stays local (LO-0137–0138)

### Changed

- `studio-tools/run_qa_gate.py` — `npx --no-install` for Prettier, ESLint, `tsc`, and Vitest so QA cannot download a stray formatter (LO-0137).
- `process/gates.md` — document project-local Prettier for QA levels.
- `studio-library/library_registry.md` + `studio-library/packages/README.md` — first-brand public chrome stays in-project; reuse `--record … local` (LO-0138).

### Closed

- LO-0137, LO-0138 infused.

## 2026-09-08 — Gate smoke unrestricted + pre-auth font DoD (LO-0132–0136)

### Changed

- `process/gates.md` — before `move … done`, re-run Playwright smoke outside agent sandboxes; `QUINSY_SKIP_SMOKE` is last-resort only (LO-0132 / LO-0133 / LO-0136).
- `studio-tools/run_qa_gate.py` — skip message reminds agents to re-run smoke unrestricted.
- `knowledge-base/frontend_playbook.md` — pre-auth self-host font DoD covers layout, specimens/iframes, and `ensureGoogleFontLink` skips (LO-0134).
- `knowledge-base/component-creation-playbook.md` — project `ui/` cannot promote into studio-library; edit HQ library or open a studio LO (LO-0135).
- Portability: replaced project-folder names in chrome-mv3 / figma-plugin / frontend playbook provenance lines.

### Closed

- LO-0132–LO-0136 infused.


## 2026-09-08 — Portability gate drops project-incident LOs (LO-0129, LO-0131)

### Fixed

- Harvest no longer opens HQ LOs from long incident sentences, product ticket IDs, or vendor-sprint bullets. Those go to `projects/<p>/docs/studio-learnings-local.md`.
- Guard does not queue short HITL replies (`approved`, `looks good`) or review/amendment approve.

### Changed

- `process/learning-loop.md` — HQ vs project-local examples.
- `process/human-in-the-loop.md` — last ticket `done` → HITL sprint-review immediately.

### Closed

- LO-0129, LO-0131 infused. LO-0127, LO-0128, LO-0130, LO-0132 dropped (project-local, not studio HQ).

## 2026-09-08 — Polish-sprint capacity + motion smoke numbers (LO-0124–0126)

### Changed

- `process/human-in-the-loop.md` — intentional 2-ticket review-polish sprints OK under capacity warn (LO-0124).
- `knowledge-base/design-science-playbook.md` — prototype one sticky section before done (LO-0125).
- `knowledge-base/design_playbook.md` — put cover-range / throw-on numbers in the design spec (LO-0126).

### Closed

- LO-0124–LO-0126 infused.

## 2026-09-08 — Sticky blur timing + appear throw-on DoD (LO-0120–0123)

### Changed

- `process/human-in-the-loop.md` — sticky stages: current stays sharp; incoming blur-in; outgoing fade; throw-on over tilt-only (LO-0120–0122).
- `knowledge-base/design-science-playbook.md` — appear DoD requires start blur/opacity/scale + end tilt degrees (LO-0123).

### Closed

- LO-0120–LO-0123 infused.

## 2026-09-08 — Marketing scroll-story motion DoD (LO-0116–0119)

### Changed

- `process/human-in-the-loop.md` — lock scroll-story motion model in design spec before IMPLEMENT (LO-0116).
- `knowledge-base/design_playbook.md` — sticky stages: prefer blur crossfade over SoftCard chrome + scale-recess (LO-0117).
- `knowledge-base/design-science-playbook.md` — fixed illustration height, no page-wide enter cascades, native sticky scroll (LO-0118, LO-0119).
- Queued train TR-0009 (UX-002), TR-0010 (UX-003).

### Closed

- LO-0116–LO-0119 infused.

## 2026-09-08 — Tailwind v4 `@source` workspace UI; PHPUnit isolation (LO-0110–0115)

### Changed

- `frontend_playbook.md` — Tailwind v4 `@import` does not scan sibling UI packages; `@source` (or v3 `content`) before marking public chrome done (LO-0110, LO-0113).
- `backend_playbook.md` — do not `RefreshDatabase` / `migrate:fresh` the operator Compose Postgres from feature tests (LO-0112, LO-0115).

### Closed

- LO-0110, LO-0113 infused (scan). LO-0112, LO-0115 infused (test DB). LO-0111, LO-0114 closed as product-backlog (color swatch on initialize status), not HQ.

## 2026-09-07 — Reuse harvest skips token kits; Laravel serve --no-reload (LO-0100, LO-0101)

### Changed

- `studio_harvest.harvest_reuse_items` — auto-LO only registry generic packages; skip `theme-tokens` / `design-tokens` / `kit-*` and project `ui/`.
- `library_registry.md` reuse enforcement — record first-brand kits `local`.
- `backend_playbook.md` — `artisan serve --no-reload` (or `php -S`) so Compose env reaches HTTP.
- SO-001 toolbox: reuse harvest + Laravel serve notes.

### Closed

- LO-0100, LO-0101 infused. LO-0102–LO-0109 closed as duplicates or product-backlog items (not HQ).

## 2026-09-07 — Close reuse-harvest LOs for first-brand kits (LO-0083–0099)

### Closed

- LO-0083–LO-0099 → `backlog/done/` without promoting into `studio-library/`. Reuse harvest auto-opened package LOs for a project's first-brand token/UI tree; record `./studio reuse --record <path> local` instead of copying client kits into HQ.

## 2026-09-07 — Mid-execute chat is inbox ACK, not a new assignment

### Fixed

- `./studio guard` is studio-core: while any project has work in flight, a user message is `INBOX_ACK` (auto-queued) and the current ACTION continues. Sprint-review `FEEDBACK_ONLY` no longer preempts an in-flight ticket.
- Execute CARD prints `MID-CHAT:` on looping steps. Notes work before a sprint exists (`docs/human-inbox.json`).

## 2026-09-07 — Anti-slop ignores published admin kit assets (LO-0082)

### Changed

- `studio-tools/validate_anti_slop.py` — skip Composer `vendor/` and published Filament-style `public/js|css|fonts/filament` (same class as `node_modules`).
- SO-001 toolbox: extend `IGNORE_PATTERNS` for generated admin-kit trees; do not rewrite vendor files.

### Closed

- LO-0082 → `backlog/done/`.


## 2026-09-07 — Close duplicate retro harvest LOs (LO-0076–0081)

### Closed

- LO-0076–LO-0081 → `backlog/done/` as duplicates of LO-0067–0075 / existing playbook rules (portability gate still lets principle-shaped retro lines through; prefer stronger dedupe next).

## 2026-09-07 — Portability gate for harvest / train / infusion

### Added

- `studio-tools/studio_portability.py` — rewrite + portability test; project-local log; HQ noun scan.
- Harvest drops non-portable titles to `projects/<p>/docs/studio-learnings-local.md` (no LO).
- LO frontmatter `train_skills`; execute train sidecar only for skill gaps.
- `./studio train` rejects non-portable topics; `./studio infusion` reports project-name hits in HQ docs.

### Changed

- `process/learning-loop.md` — portability gate as required harvest step.
- Train topics must be reusable principles (not product/surface incident lines).

## 2026-09-07 — Studio LO infusion gate clear (LO-0067–LO-0075)

### Added

- `knowledge-base/backend_playbook.md` — licence adapter contract (LO-0067 / LO-0072); stock imagery provider priority — primary aggregator first, fallbacks last (LO-0075).
- `knowledge-base/design_playbook.md` — per-cell pixel budgets and resolution-aware bento placement (LO-0068 / LO-0070 / LO-0073).
- `teams/09-studio-operations-evolution/skills/studio-tooling-maintenance.md` — SO-001 toolbox: licence slugs, bento budgets, degraded Suggested UX, sandbox smoke skip (LO-0071), provider priority (LO-0075).

### Changed

- `knowledge-base/contextual-ia-playbook.md` — anti-pattern: selection-order mosaic placement (LO-0070).
- `process/human-in-the-loop.md` — degraded Suggested copy must separate HTTP outage vs filter-empty (LO-0069 / LO-0074).
- `process/gates.md` — LO-0071: explicit `QUINSY_SKIP_SMOKE` rule for agent sandboxes where Chromium SIGSEGVs.

### Closed

- LO-0067, LO-0068, LO-0069, LO-0070, LO-0071, LO-0072, LO-0073, LO-0074, LO-0075 → `backlog/done/`.

## 2026-09-07 — Probe host ports before Docker publish (LO-0066)

### Changed

- New [host-port-allocation.md](knowledge-base/host-port-allocation.md): agents probe `docker ps` before pinning Compose host ports; no new CLI.
- PE-001, backend playbook, agent-context, HITL, docker template: host ports via env (`POSTGRES_HOST_PORT`, `REDIS_HOST_PORT`); textbook 5432/6379/3000 are not a reservation.

## 2026-09-07 — Playwright arm64 host override when os.cpus() is empty

### Fixed

- `studio-tools/run_qa_gate.py` — on Darwin arm64, set `PLAYWRIGHT_HOST_PLATFORM_OVERRIDE` from `platform.machine()` so smoke finds durable arm64 browsers when Cursor sandboxes return empty `os.cpus()` (Playwright otherwise picks mac-x64).

## 2026-09-07 — Imagery Suggested smoke + presentation layout DoD (LO-0062–0065)

### Changed

- `process/human-in-the-loop.md` — Suggested/found imagery must smoke signed-in provider path; empty-after-alive-copy is not done (LO-0062/0064). Imagery selection epics need presentation placement + composition quality DoD, not rail-only (LO-0063/0065).
- `knowledge-base/contextual-ia-playbook.md` — anti-pattern: picker without presentation layout DoD.

## 2026-09-07 — Execute loop hygiene: tests, worlds, lean status.json

### Fixed

- `test_studio_learning_gate.py` is unittest (discoverable), not pytest-only.
- `./studio verify-worlds` allows committed `intake/amendments/**/amendment_*.example.md` and ignores leftover dirs (`--help`, `LO-0042`, `testproj`). Non-example amendment binaries are gitignored.
- File-hash snapshots move to `docs/ticket-file-snapshots.json`; `gate_history` is capped so execute does not parse an 8MB `status.json`.

## 2026-09-07 — Studio settings: per-step token policy + host adapters

### Added

- [studio.settings.yaml](studio.settings.yaml) — medium-project defaults; per-step `context` / `budget` (intake, architecture, design, implement, …).
- `./studio settings` — merged policy + estimated usage. Local override: `studio.settings.local.yaml` (gitignored; **no API keys**).
- Execute CARD shows `COST`; at 100% of a knob → `INFORM cost-cap` naming the yaml key. `economy` / `standard` / `premium` profiles.
- [CLAUDE.md](../CLAUDE.md) and [GEMINI.md](../GEMINI.md) — same `./studio` loop; keys stay in the host.

### Changed

- Estimates are `chars/4` of CARD + listed files, not host billing. `./studio focus` resets session usage.


### Changed

- **Gate 1 (architecture)** is mandatory HITL after gate 0. Execute writes the blueprint, then stops for `./studio approve --gate 1`. Iterate with `./studio revise --gate 1`.
- **Gate 2 (design track)** is mandatory HITL after architecture: design direction, design system, stills/mocks or clickable prototype. Execute runs `./studio design`, then stops for `./studio approve --gate 2`. Per-ticket `approve-design` still applies in sprints.
- `./studio inform --gate 1` no longer marks architecture informed — it points at `./studio approve`.
- Root `README.md`, [GETTING_STARTED.md](GETTING_STARTED.md), and this ops [README.md](README.md) match that loop (train in parallel, stubs not pullable, scope/reuse inform).


## 2026-09-07 — Factory loop: HITL contraction, parallel train, human inbox (LO-0061)

### Changed

- **Mandatory HITL** was contracted (reuse/scope inform, parallel train). **Same-day correction:** architecture (gate 1) and design track (gate 2) remain standing HITL after PRD — see entry above.
- Sprint scope/groom are **agent-owned** (human may override). Reuse is an **inform brief** — `--approve` no longer blocks retro or the next sprint.
- Harvest stays immediate. Open LOs spawn `./studio train` **beside** product work. Execute returns `STUDIO_LO` only when idle (no ready IMPLEMENT).
- CARD lists `skills` + playbook paths. `./studio note` queues mid-execute input (ACK; drain after MOVE_DONE). Only “stop this ticket” preempts.
- `billing` and `feature-gating` are marked `stub: true` and **not pullable**. Pull → adapt in the project; promote only when the generic asset improved.

### Added

- `./studio note` / `inform --gate 1` / `veto` / `train`
- `studio_human_inbox.py`, `studio_train.py`


## 2026-09-07 — Execute respects cross-sprint done deps

### Fixed

- `studio_execute.py` — `project_done_ids()` reads `backlog/done/` so sprint tickets whose dependencies finished in prior sprints are no longer falsely blocked.
- Execute picks the next ticket in **scope-proposal.json order** (then priority, then id), so approved sprint goals lead.

## 2026-09-07 — Live home surface + mid-sprint rewrite + marketing canvas fidelity (LO-0054, LO-0057–0060)

### Changed

- `process/human-in-the-loop.md` — confirm live product home before scoping UI from amendment IA (LO-0057/0059); same-turn `plan.md` + defer when feedback rewrites sprint goal (LO-0060); mature AC before implement on mid-sprint pulls (LO-0058); marketing canvas stills must mount real product canvas / shared fixtures (LO-0054).
- `process/amendment-intake.md` — agent obligation: live home-surface check before grooming amendment-placed UI.
- `process/backlog-model.md` — mid-sprint goal rewrite + maturity for feedback pulls.
- `knowledge-base/contextual-ia-playbook.md` — anti-patterns for amendment-over-live and immature mid-sprint pulls; live-vs-draft checklist.
- `knowledge-base/visual-storytelling-playbook.md` — product fidelity rule for canvas/stylescape marketing stills.

## 2026-09-07 — Brownfield adopt (LO-0056)

### Added

- `./studio adopt <project> --from <git-url-or-path> [--intent intake/<p>.md]` — overlay studio docs on an existing codebase. Keeps the project’s `.git`. Never wipes `src/` / `app/`.
- Process [brownfield-adopt.md](process/brownfield-adopt.md) + as-built templates (`docs/as-built/00`–`07`) and `studio-templates/adopt_intent.md`.
- Execute: `mode: adopt` fills as-built (`IMPLEMENT`) then synthesizes PRD (`VERIFY`) before HITL gate 0. Gate 2 is design-of-what-exists — no empty Next.js prototype.

### Changed

- `init` / `bootstrap` / `start` / `design` refuse or skip empty-scaffold on a live tree.
- Docs: GETTING_STARTED, root README, AGENTS — existing-project path vs greenfield PRD.

## 2026-09-07 — Immediate harvest + mid-sprint infusion (LO-0055)

### Added

- `studio_harvest.py` — classify a learning when it is identified (package, ui-component, design/ux/ia/layout/usability, frontend/backend/database/security, process, tooling), append `knowledge-base/learnings/inbox.md`, open a compact LO with `infusion_kind` / `infusion_path`.
- `./studio learn`, `./studio retro --complete`, `./studio reuse`, and 3rd gate fail all harvest immediately — no human learn prompt, no wait until next sprint.

### Changed

- `./studio execute` returns `STUDIO_LO` **before the next project IMPLEMENT**, including mid-sprint. In-progress tickets still finish VERIFY/GATE/DEBUG/MOVE_DONE. HITL (gates 0–2, sprint-review) still wins.
- Does not copy project UI/tokens into `studio-library/`; inbox + LO is the capture; the agent generalizes on `STUDIO_LO`.

## 2026-09-07 — Agentic execute loop (LO-0053)


### Added

- `./studio execute <project> [--json]` — one next action (`IMPLEMENT` / `GATE` / `VERIFY` / `MOVE_DONE` / `DEBUG` / `STUDIO_LO` / `HITL`). Agent loops until HITL; does not ask to continue.
- Compact ticket cards (`./studio ticket-card`) and execution receipts (`./studio receipt`) — Plan, AC coverage, default flow (LO-0051) required before `move … done`.
- `./studio health <project>` — sprint state-graph check (open LOs, missing receipts, unmet deps).
- Bounded gate-fail debug files (`sprints/SPRINT-NN/debug/<ticket>.md`, max 3 retries) and auto-draft LO on exhaustion (`signal: gate-fail`).
- Retro `--complete` harvests `./studio learn` prompts from went badly / improve.

### Changed

- `ticket_helpers.py` renders compact tickets (no duplicated skills/deps, no filler BDD, no per-ticket boilerplate DoD).
- Session start: `./studio execute` is the driver; `resume` remains a checklist.
- Docs: root `README.md`, `.quinsy-studio/README.md`, `GETTING_STARTED.md` — execute loop, compact tickets, receipts, health, `STUDIO_LO`.

### Notes

- Markdown remains ticket source of truth (no SQL). Tokens are saved by layered load (card vs full ticket), not storage format.


## 2026-09-05 — Durable Playwright browsers for gate smoke (LO-0052)

### Fixed

- `studio-tools/run_qa_gate.py` — smoke sets `PLAYWRIGHT_BROWSERS_PATH` to `.quinsy-studio/.cache/playwright/<project>/` and clears `PLAYWRIGHT_HOST_PLATFORM_OVERRIDE`, so gate smoke does not reinstall into ephemeral Cursor sandbox caches or hit mac-x64/arm64 mismatches.
- `process/gates.md` — documents durable cache + `QUINSY_SKIP_SMOKE` opt-out.
- `.gitignore` — ignores `.quinsy-studio/.cache/`.
- Provenance: moody SPRINT-111 review (process-gap).

## 2026-09-04 — Visible-outcome DoD: real end-to-end walkthrough required, not just green tests (LO-0051)

### Changed

- `process/iterative-delivery.md` — sprint plan Definition of Done requires that any ticket whose acceptance criteria is a **visible design/UX outcome** be verified by walking a real end-to-end scenario through the **default product flow**, with a before/after screenshot — not only green unit/QA tests.
- `process/human-in-the-loop.md` — Rule (LO-0051): a feature gated behind an unconfirmed or undiscoverable app state, or produced only by a code path the default flow never calls, counts as **not shipped** even with green gates. Sprint review means trying work through the same flow a real user reaches — not only reading `review.md`.
- Provenance: learning from a project sprint where gate-green tickets produced no visible change on the default path (`--source` on LO-0051).

## 2026-09-03 — Overlap check + mandatory scope-exclusions table in amendment intake (LO-0049, LO-0050)

### Changed

- `process/amendment-intake.md` — **Step 1.5 (overlap check)**: before drafting a new amendment, check `./studio amendments <project>` and existing `docs/amendments/*/01-vision-synthesis.md` for scope overlap; reconcile with a dormant approved amendment instead of drafting a parallel one.
- Mandatory **"Scope exclusions" table** in `02-requirements-addendum.md` (and surfaced in `10-approval-checklist.md`) for any requirement that freezes/excludes a system a reader would reasonably expect in scope.
- Provenance: LO-0049 / LO-0050 (`--source` on tickets).

## 2026-09-03 — Cross-surface acceptance + unread-field checks in amendment intake (LO-0048)

### Changed

- `process/amendment-intake.md` — agent obligations #8 and #9: before closing an amendment capability, re-check every promised **surface** (not only the last-tested one), and confirm newly authored frozen-type fields have at least one runtime reader before milestone review.
- Provenance: LO-0048.

## 2026-09-03 — Same-status ticket move must not unlink (LO-0047)

### Fixed

- `studio-tools/studio.py` `cmd_move` — when source and destination resolve to the same path (e.g. already `implement` → `implement`), update the ticket in place and **do not** `unlink()` after write (previously deleted the ticket)

## 2026-09-03 — Optional smoke skip for agent sandboxes (LO-0046)

### Changed

- `studio-tools/run_qa_gate.py` — `QUINSY_SKIP_SMOKE=1` skips Chromium smoke when the browser cannot launch (SIGSEGV / sandbox). Explicit opt-in only; local human runs leave unset.

## 2026-09-03 — Ticket ID allocation scans root backlog (LO-0045)

### Fixed

- `studio-tools/ticket_ids.py` — `scan_max_ticket_number` now includes root-level `backlog/{PREFIX}-*.md` (amendment-materialized / unscheduled tickets), not only `backlog/<status>/`
- Prevents `./studio ticket --from-feedback` from colliding with amendment-materialized IDs for any project prefix

### Added

- `studio-tools/test_ticket_ids.py` — root-level scan + allocate non-collision tests

## 2026-09-01 — Figma kit fidelity north-star DoD (LO-0044)

### Changed

- `knowledge-base/figma-plugin-host-networking.md` — kit fidelity DoD: north-star + screenshot; wireframe chrome fails
- `process/human-in-the-loop.md` — LO-0044 rule for professional / shadcn-class stickersheet tickets

## 2026-09-01 — Figma stickersheet inventory DoD (LO-0043)

### Changed

- `knowledge-base/figma-plugin-host-networking.md` — stickersheet DoD: section headlines alone are not done; assert inventory children on canvas
- `process/human-in-the-loop.md` — LO-0043 rule for kit / stickersheet placement tickets

## 2026-09-01 — Extension inbox sync port probe (LO-0042)

### Changed

- `knowledge-base/chrome-mv3-vite-content-scripts.md` — DoD: keep probing past plain-text wrong-app 404s until product JSON responds
- `process/human-in-the-loop.md` — LO-0042 rule for extension cloud-inbox multi-port sync

## 2026-09-01 — Figma localhost vs 127.0.0.1 prefs (LO-0041)

### Changed

- `knowledge-base/figma-plugin-host-networking.md` — localhost-only allowlist; `clientStorage` can override defaults with `127.0.0.1` and look like CSP failure
- `process/human-in-the-loop.md` — LO-0041 DoD: normalize API base to `localhost`; rebuild ≠ clear prefs

## 2026-09-01 — Component reuse ladder + right-rail dock pattern (LO-0040)

### Changed

- Rewrote LO-0040 as a **general** learning (was overfitted to one inspector surface)
- `process/learning-loop.md` — LO titles/proposals must state the general rule; `--source` is provenance only
- `knowledge-base/component-creation-playbook.md` — reuse ladder (reuse → project component → studio-library)
- `knowledge-base/frontend_playbook.md` — reuse ladder + right-rail dock organism
- `process/human-in-the-loop.md` — LO-0040 DoD generalized
- `process/project-archetypes.md` — saas-application UX option: right-rail nav + detail-rails
- `studio-library/ui/components/studio-rail/README.md` — pattern framing for cross-project reuse

## 2026-09-01 — Docked chrome DoD: edge + full height (LO-0039)

### Changed

- `process/human-in-the-loop.md` — LO-0039: reuse of `StudioPanel` / rails is not done on class-name reuse alone; require flush-edge + full-height live layout DoD
- `knowledge-base/frontend_playbook.md` — docked chrome reuse checklist (component + edge + height)

## 2026-08-31 — Design spec §2/§2c early + emoji mock scan (LO-0038, LO-0037)

### Changed

- `knowledge-base/design-spec-template.md` — LO-0038 callout: large mock packs still need §2 + §2c before approve-design
- `knowledge-base/design-system-compliance-checklist.md` — §2/§2c checklist item
- `studio-tools/design_ticket_helpers.py` — `design_mocks_emoji_icon_warning` (LO-0037)
- `studio-tools/studio.py` — `approve-design` warns on emoji-as-icon in mock HTML

## 2026-08-30 — No emoji-as-icons in mocks/UI (LO-0037)

### Changed

- `process/anti-slop.md` — Category 5b: emoji-as-icon banned in product UI and design-spec mocks; SVG / Icon components only
- `knowledge-base/design-system-compliance-checklist.md` — approve-design checklist item for no emoji + centered icons

## 2026-08-30 — Reuse: empty snapshot skip (LO-0036)

### Fixed

- `studio-tools/library_manager.py` — `check_reuse_before_done` returns clean when ticket has no implement snapshot (design-only done)
- `studio-tools/sprint_reuse_review.py` — skip empty snapshots so reuse review does not flag entire `packages/`

## 2026-08-29 — Canvas shell nested scroll (LO-0035)

### Changed

- `knowledge-base/frontend_playbook.md` — canvas `overflow-hidden` shells need nested scroll layouts for document routes; DialogShell tall-content pattern
- `process/human-in-the-loop.md` — LO-0035 rule

## 2026-08-29 — Review smoke surface match (LO-0034)

### Fixed

- `studio-tools/sprint_hitl.py` — Figma plugin smoke steps only for real plugin tickets; Brand kit / board tickets get webapp steps (not plugin OAuth defaults)
- `process/human-in-the-loop.md` — LO-0034 rule

## 2026-08-29 — Strategic feedback slicing (LO-0033)

### Changed

- `process/human-in-the-loop.md` — LO-0033: large review feedback → clarify + phase-aligned ticket slices (+ optional sprint roadmap) before next sprint; no mega-tickets

## 2026-08-29 — Brand-guide PDF WYSIWYG type DoD (LO-0032)

### Changed

- `knowledge-base/frontend_playbook.md` — PDF export DoD: screen and PDF must share the same type stack
- `process/human-in-the-loop.md` — LO-0032 rule for brand-guide / print WYSIWYG typography

## 2026-08-29 — Anti-slop dead-code regex (LO-0031)

### Fixed

- `studio-tools/validate_anti_slop.py` — “dead code after return” only matches same-indent statements (avoids nested JSX `return` false positives)

## 2026-08-29 — Feedback→ticket design brief infer (LO-0030)

### Changed

- `studio-tools/design_ticket_helpers.py` — `Design:` titles and Team 10 / in-context-mock scopes infer `ui-composition`
- `studio-tools/studio.py` — `--from-feedback` tickets infer type from title **plus** clarify scope/raw text

## 2026-08-29 — Sprint capacity 3–6

### Changed

- `process/human-in-the-loop.md` — sprints target **3–6** tickets; agents must not narrow proposals to 1–2 unless human asks for hotfix
- `studio-tools/sprint_backlog_validate.py` — `UNDER_CAPACITY` warning when sprint has fewer than 3 tickets

