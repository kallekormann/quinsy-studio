# Quinsy Studio CHANGELOG

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

