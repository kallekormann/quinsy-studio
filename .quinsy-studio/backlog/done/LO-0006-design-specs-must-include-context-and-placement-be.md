# LO-0006 — Design specs must include context-and-placement before layout polish

**Status:** done (STUDIO-SPRINT-01, 2026-08-25)  
**Signal:** design-gap · **Source:** moody (presentation link IA)

## Implemented

- [x] `knowledge-base/contextual-ia-playbook.md`
- [x] `knowledge-base/workflow-definition-playbook.md`
- [x] `knowledge-base/design-system-compliance-checklist.md`
- [x] `design-spec-template.md` v2 — mandatory §2 Context & placement
- [x] UX-003 skill expanded (nav + contextual placement)
- [x] `ticket-team-allocation.md` — `ia-feature-placement`, design gate updated
- [x] `design_ticket_helpers.py` — placement detection + `ia-feature-placement` type
- [x] `./studio approve-design` warns when §2 missing
- [x] `./studio guard` hints for multi-surface UI without placement spec
- [x] `test_design_ticket_helpers.py`

## Original observation

Layout-first tickets (e.g. "widen Share dialog") approved specs that kept capabilities on the wrong surface. Presentation link belonged in presentation builder, not Share. Required 2+ remediation sprints.

## Prevention

Placement before polish. Amendment and UI specs must answer *where* before *how wide*.
