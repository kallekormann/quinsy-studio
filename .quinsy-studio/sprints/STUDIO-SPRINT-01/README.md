# STUDIO-SPRINT-01 — Design discipline & studio abstraction

**Status:** in progress  
**Scope:** Studio HQ only (`.quinsy-studio/`) — no project code

## Goal

Prevent multi-sprint remediation from wrong-surface IA and project-specific coupling in studio docs/tools.

## Tickets

| ID | Title | Status |
|----|-------|--------|
| LO-0006 | Context & placement in design specs + playbooks | done |
| LO-0007 | Studio HQ de-Moody + `verify-abstraction` | done |
| LO-0008 | Amendment intake generic examples + surface map in UX concept | done |
| LO-0009 | `ia-feature-placement` ticket type + guard hints | done |
| LO-0010 | Meta-retro → LO routing policy | open (doc) |

## Shipped

- `knowledge-base/contextual-ia-playbook.md`
- `knowledge-base/workflow-definition-playbook.md`
- `knowledge-base/design-system-compliance-checklist.md`
- `knowledge-base/design-spec-template.md` v2 (§2 Context & placement)
- `process/studio-abstraction.md`
- `studio-templates/amendment_01.example.md` (acme-app)
- `process/amendment-intake.md` — generic paths, UX-003 in analysis
- `./studio verify-abstraction`
- `approve-design` placement warning
- UX-003 skill expanded
- Removed `.quinsy-studio/tmp/generate_moody_backlog.py`

## Verify

```bash
./studio verify-worlds
./studio verify-abstraction
cd .quinsy-studio/studio-tools && python -m pytest test_design_ticket_helpers.py -q
```

## Human approval

Studio sprint — no `./studio sprint --approve-scope` (LO backlog, not project sprint).
