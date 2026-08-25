# Quinsy Studio CHANGELOG

## 2026-08-25 — STUDIO-SPRINT-01 (design discipline & abstraction)

### Added

- Contextual IA, workflow definition, and design-system compliance playbooks
- Design spec template v2 with mandatory §2 Context & placement
- `ticket_type: ia-feature-placement` and UX-003 expansion
- `./studio verify-abstraction` — scan studio HQ for project-name leaks
- `process/studio-abstraction.md` policy
- `studio-templates/amendment_01.example.md` (generic `acme-app` example)

### Changed

- `approve-design` warns when design spec lacks placement section
- `guard` suggests placement spec for multi-surface UI requests
- Amendment intake docs use `<project>` placeholders throughout
- `README.md`, `GETTING_STARTED.md`, `.quinsy-studio/README.md` — design discipline, `verify-abstraction`, amendment template paths
- **Studio Infusion Gate** — `./studio infusion`; open LO-* block `./studio sprint`; retro requires `--complete`
- Retro flow: scaffold → fill → `--complete` (no auto-done on empty template)

### Added (infusion sprint)

- `studio_learning_gate.py`, `./studio infusion`
- `local-first-sync-playbook.md`
- Supabase local migrate guidance (docker README, backend playbook)
- PRD NFR heading fix (`test_process_intake_nfr.py`)
- Feedback ticket `## Scope` injection (LO-0002)
- Closed LO-0000, LO-0002–0005, LO-0010

### Removed

- `.quinsy-studio/tmp/generate_moody_backlog.py` (project-specific script in studio HQ)
