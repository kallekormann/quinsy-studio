# Quinsy Studio CHANGELOG

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

