# Meta-retro — 2026-08-27 (post SPRINT-51 / LO-0024)

**Source:** moody SPRINT-51 — Figma Login showed IndexedDB ConstraintError Sync issue; boards names-only.

## Signal
Guest→auth migration used non-idempotent IndexedDB `add`, surfacing ConstraintError during plugin OAuth handoff.

## Infusion
- LO-0024 → HITL + local-first-sync-playbook (put/upsert; no Sync scare on plugin login)

## Follow-up
Next Moody sprint: MOOD-0232–0235 (Figma login polish + board actions); MOOD-0236 screen-by-screen UX session.
