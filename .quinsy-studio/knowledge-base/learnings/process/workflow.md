# process / workflow

Portable studio principles (not project incidents).
Matching playbook/skill: `process/learning-loop.md`.

## Principles

- **LO-0361** 2026-09-29 :: When `docs/i18n.md` exists, ticket type must stay explicit (`feature`) so catalog AC does not infer a design-track ticket.
  - When a project has `docs/i18n.md`, every ticket gets catalog AC. That AC mentions "UI string" and must not flip `infer_ticket_type` to `ui-composition`. Set `ticket_type: feature` (or the real design type) explicitly. Classifier: strip catalog AC before matching the word `ui`.
- **PB-20260927-003** helpful=0 harmful=0 :: Gate feedback must be a gate revision and must not be queued as a sprint inbox note while execute is waiting on a human gate.
- **PB-20260927-002** helpful=1 harmful=0 :: A stack and host named in the PRD must win over the archetype default, and that delta must be an ADR.
- **PB-20260927-001** helpful=0 harmful=0 :: A PRD rewrite must keep the original specification unchanged and must not drop normative details to fit a length cap.
- **LO-0359** 2026-09-26 :: Gate feedback must be a gate revision and must not be queued as a sprint inbox note while execute is waiting on a human gate.
  - Gate feedback must be a gate revision and must not be queued as a sprint inbox note while execute is waiting on a human gate.
- **LO-0357** 2026-09-26 :: A stack and host named in the PRD must win over the archetype default, and that delta must be an ADR.
  - A stack and host named in the PRD must win over the archetype default, and that delta must be an ADR.
- **LO-0353** 2026-09-26 :: A PRD rewrite must keep the original specification unchanged and must not drop normative details to fit a length cap.
  - A PRD rewrite must keep the original specification unchanged and must not drop normative details to fit a length cap.
- **PB-20260926-005** helpful=0 harmful=0 :: When collapsing stacked mocks into one composition, keep the feature inventory section. A single narrative frame is not permission to delete the inventory.
- **LO-0350** 2026-09-26 :: Keep the feature inventory when replacing stacked mocks
  - See **PB-20260926-005**. When collapsing stacked mocks into one composition, keep the feature inventory section. A single narrative frame is not permission to delete the inventory.
- **PB-20260926-004** helpful=0 harmful=0 :: Do not `--approve-scope` tickets that are blocked (unmet dependencies or not ready). Drop them from `proposed` before approve.
- **LO-0349** 2026-09-26 :: Do not `--approve-scope` blocked tickets
  - See **PB-20260926-004**. Do not `--approve-scope` tickets that are blocked (unmet dependencies or not ready). Drop them from `proposed` before approve.
- **PB-20260926-003** helpful=0 harmful=0 :: Keep public host routing on the original Host header without a path-prefix rewrite. Do not restyle a live public site from a docs-only ticket.
- **LO-0348** 2026-09-26 :: Keep public host routing on the original Host header
  - See **PB-20260926-003**. Keep public host routing on the original Host header without a path-prefix rewrite. Do not restyle a live public site from a docs-only ticket.
- **PB-20260926-002** helpful=0 harmful=0 :: Do not groom a control-specific ticket onto a surface that does not already show that control. File a design-track ticket and get the packet signed before the control is in grooming.
- **PB-20260926-001** helpful=0 harmful=0 :: A sprint field of none/empty is unscheduled. Planning must treat it as no sprint tag, not as already assigned.
- **LO-0345** 2026-09-26 :: Do not groom a control onto a surface that lacks that control
  - See **PB-20260926-002**. Do not groom a control-specific ticket onto a surface that does not already show that control. A design packet must add the control first.
- **LO-0343** 2026-09-25 :: A shell ticket must not depend on the full feature inventory
  - Ship the shared surface first. Inventory work is its own later ticket. A shell ticket depends only on the shell it renders.
- **PB-20260925-002** helpful=0 harmful=0 :: Layout and composition sprints must not restyle a tenant's public magazine, generate articles, merge properties, or auto-publish. Those actions need their own operator tickets.
- **LO-0342** 2026-09-25 :: Layout sprints must not restyle public magazine chrome or auto-publish
  - See **PB-20260925-002**. Layout and composition sprints must not restyle a tenant's public magazine, generate articles, merge properties, or auto-publish.
- **PB-20260925-001** helpful=0 harmful=0 :: An IDE command palette that steals the browser automation tab is a known live-proof gap. Do not block MOVE_DONE when unit contracts cover the AC. Record the intercept and cite HTTP/API tests; do not treat a hung tab as failed receipt proof.
- **LO-0340** 2026-09-25 :: Command palette intercept is a live-proof gap, not a MOVE_DONE blocker
  - See **PB-20260925-001**. An IDE command palette that steals the automation tab does not fail the receipt when unit contracts cover the AC.
- **LO-0330** helpful=0 harmful=0 :: Link a first-party catalog row to a network SKU only on a unique identity match (GTIN/EAN, then part number plus brand, then normalized name plus brand). Missing or ambiguous matches stay unmatched until the operator picks the SKU. Never invent a destination.
- **PB-20260923-001** helpful=0 harmful=0 :: Folder filters that join work rows to pages by page_id must also resolve the page via the linked brief, or persist page_id as soon as the page exists.
- **LO-0329** 2026-09-23 :: Folder filters that key off `page_id` must also resolve `pages.brief_id = linked
  - Folder filters that key off `page_id` must also resolve `pages.brief_id = linked_brief_id`, or persist `page_id` as soon as the page exists.
- **LO-0328** 2026-09-23 :: Local preview origin must stay `MAGAZINE_URL` (loopback + port). Property identi
  - Local preview origin must stay `MAGAZINE_URL` (loopback + port). Property identity belongs in `host=`, not in the DNS host of the URL.
- **LO-0313** 2026-09-22 :: Default legal templates use the property's public identity, never a hard-coded first-tenant brand string.
  - Seeded legal sentences (imprint, privacy, disclosures) take the property masthead/host. A second property must not inherit another tenant's legal copy.
- **PB-20260922-003** 2026-09-22 :: Sprint `--approve-scope` reads `scope-proposal.json` against `backlog/*.md` only.
  - Tickets already in `backlog/done/` must be dropped from `proposed` before approve. Editing the markdown proposal alone does not update the JSON.
- **LO-0307** 2026-09-16 :: A font placed in a zone should be used as Primary until the opera
  - A font placed in a zone should be used as Primary until the opera
