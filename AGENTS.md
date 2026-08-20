# Quinsy Studio — AI Agent Contract

You operate **Quinsy Studio** in the IDE. Stay in context. Separate worlds. **Library-first.**

## Session start (mandatory)

```bash
./studio verify-worlds
./studio focus <project>
./studio resume <project>
```

Read: [agent-context.md](.quinsy-studio/process/agent-context.md) | [library_registry.md](.quinsy-studio/studio-library/library_registry.md)

## Library-first (UI + code)

**Before writing new UI or package code:**

```bash
./studio library list
./studio library suggest <project> "auth billing button"
./studio library pull <project> auth billing tokens button
```

Use library artifacts as **boilerplate** — adapt tokens, config, business rules in the project.  
After the ticket is done, if changes are generic:

```bash
./studio library promote <project> packages/billing --ticket <ID> [--force]
```

On `./studio move <project> <ID> implement` you get a library hint.  
On `./studio move … done` unpromoted changes under `packages/`, `ui/components/`, etc. → **warning**.

## Two worlds — never mix

| World | Path | Git |
|-------|------|-----|
| Studio HQ | `.quinsy-studio/` | quinsy-studio root |
| Project | `projects/<name>/` | **separate repo** |

`./studio verify-worlds` — must pass before project work.

## Pre-implementation gates

| Gate | Approves | Tickets? |
|------|----------|----------|
| 0 | PRD + definitions | No |
| 1 | Architecture | No |
| 2 | Design + mocks | Yes + **design → library** |

```bash
./studio approve <p> --gate 2    # also runs promote-library
./studio library promote-design <p> [--force]
```

## Context & drift

```bash
./studio guard <project> "user request"
./studio focus <project> && ./studio resume <project>   # drift recovery
```

## Reference

- [GETTING_STARTED.md](.quinsy-studio/GETTING_STARTED.md)
- `projects/<p>/docs/library-usage.json` — what was pulled
- `projects/<p>/docs/library-promotions.json` — what was promoted
