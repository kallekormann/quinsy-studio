# Local-first sync playbook

> **Signal:** process-gap from local-first canvas projects  
> **When:** Gate 1 architecture + any project using IndexedDB/Dexie as source of truth with cloud backup

## Principle

**Local-first ≠ migrate once.** Boards and items need **continuous** cloud sync (or explicit sync engine), not a one-time import on first login.

## Anti-pattern

| Wrong | Right |
|-------|-------|
| One-time `migrateLocalBoardsToCloud()` on auth | Ongoing push/pull per board |
| Cloud only as cold backup | Cloud reflects latest local ops within SLA |
| Agent assumes REST CRUD replaces sync | Document sync model in ADR |

## Architecture checklist (gate 1)

- [ ] Local store is source of truth (Dexie, OPFS, Yjs, …)
- [ ] Sync direction documented: LWW, CRDT, or hybrid
- [ ] Conflict resolution defined
- [ ] Offline queue + replay on reconnect
- [ ] `docs/architecture/sync.md` or ADR references this playbook

## Idempotent local writes (LO-0024)

Guest→auth and plugin OAuth handoffs often re-write the same board/item keys.

| Wrong | Right |
|-------|-------|
| `table.add(row)` on migrate | `table.put(row)` / upsert |
| Surface `ConstraintError: Key already exists` as “Sync issue” | Swallow duplicate as success or merge; never scare PLG/plugin login |
| Mark plugin login done when boards list loads | Also smoke: no IndexedDB error banner on `/login` → connected |

## Ticket guidance

Backlog tickets for sync must state **continuous** vs **one-time** explicitly in scope.

## Studio library

Generic sync helpers belong in `studio-library/packages/` after promotion — not project-only scripts in `.quinsy-studio/`.

## Related

- [backend_playbook.md](backend_playbook.md)
- [project-archetypes.md](../process/project-archetypes.md)

## Deltas

- **PB-20260922-001** helpful=0 harmful=0 :: Adding a canvas item type ships the CRDT/Yjs allowlist and the persistence enum in the same change. A UI type the sync layer rejects is not done.
