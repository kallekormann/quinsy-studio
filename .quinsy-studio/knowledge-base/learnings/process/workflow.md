# process / workflow

Portable studio principles (not project incidents).
Matching playbook/skill: `process/learning-loop.md`.

## Principles

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
