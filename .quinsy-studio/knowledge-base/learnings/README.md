# Studio learnings

Durable, portable principles gathered while implementing products — **not** the harvest dump.

| Layer | Path | IMPLEMENT? |
|-------|------|------------|
| Catalog | [index.md](index.md) | Yes — find a topic |
| Domain | `<domain>/README.md` | Yes — CARD lists this |
| Topic | `<domain>/<topic>.md` | Yes — the rules |
| Open queue | [inbox.md](inbox.md) | **No** |
| History | [archive/](archive/) | **No** |
| Project-only | `projects/<p>/docs/studio-learnings-local.md` | That product only |

```
./studio learn-find "queue"
./studio learn-compact    # archive infused inbox rows
```

On train, also delta the matching playbook or skill (`./studio infusion-delta`). Inbox is never the long-term store.
