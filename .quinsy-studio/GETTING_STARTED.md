# Quinsy Studio — Getting Started

> Canonical workflow: intake → architecture → design → implementation.  
> Root overview: [`README.md`](../README.md) · Agent: [`AGENTS.md`](../AGENTS.md)

## Session ritual (IDE + agent)

```bash
./studio verify-worlds
./studio focus <project>
./studio resume <project>
```

## Three human gates (before coding)

| Gate | You approve | CLI |
|------|-------------|-----|
| **0** | PRD + definitions | `./studio approve <p> --gate 0` |
| **1** | Architecture blueprint + ADRs | `./studio approve <p> --gate 1` |
| **2** | Design + Next.js mocks + sticker sheet | `./studio approve <p> --gate 2` |

Tickets are created **only after gate 2**. Gate 2 also promotes design artifacts to [studio-library](studio-library/library_registry.md).

## AI-driven bootstrap

1. Drop PRD in [`intake/`](../intake/) (gitignored — local only)
2. Tell the agent: **"Bootstrap &lt;project&gt;"**
3. Approve each gate when artifacts are ready
4. At design: choose `--scope journey` (full flow) or `--scope core-views` (key screens)

```bash
./studio bootstrap my-project
./studio approve my-project --gate 0
./studio blueprint my-project && ./studio approve my-project --gate 1
./studio design my-project --scope core-views
./studio approve my-project --gate 2
./studio sprint my-project
./studio move my-project MY-0001 implement
```

## Iteration at any gate

```bash
./studio revise my-project --gate 1 --feedback "Use IndexedDB only, defer Supabase"
```

Logged in `projects/<p>/docs/phases/revisions.md`.

## Library-first (UI + code)

| Step | Command |
|------|---------|
| Discover | `./studio library list` |
| Before coding | `./studio library suggest <p> "billing auth button"` |
| Pull boilerplate | `./studio library pull <p> auth billing button tokens` |
| Promote code | `./studio library promote <p> packages/billing [--force] [--ticket ID]` |
| Promote design | `./studio promote-library <p> [--force]` |

On `./studio move <p> <ID> implement` → library hint.  
On `./studio move … done` → warns if registry paths changed without promotion.

## Project artifacts (all under `projects/<p>/`)

| Artifact | Path |
|----------|------|
| PRD | `docs/intake/prd.md` |
| Definitions | `docs/definitions/` |
| Architecture | `docs/architecture/` |
| ADRs | `docs/adr/` |
| Design spec | `design/DESIGN.md` |
| Mock scope | `design/DESIGN-SCOPE.md` |
| Design prototype (Next.js) | `design/prototype/` |
| Tokens | `ui/tokens/design-tokens.json` |
| Atomic UI | `ui/components/atoms\|molecules\|organisms/` |
| Sticker sheet | `design/prototype/app/sticker-sheet/` |
| Packages | `packages/auth/`, `packages/billing/`, … |
| Tickets | `backlog/open/` (after gate 2) |
| Library pull log | `docs/library-usage.json` |
| Library promote log | `docs/library-promotions.json` |

Run prototype: `cd projects/<p>/design/prototype && npm install && npm run dev`

## Agent hardening

| Concern | Doc / command |
|---------|----------------|
| Scope & drift | [process/agent-context.md](process/agent-context.md) |
| Two git worlds | [process/worlds.md](process/worlds.md) · `./studio verify-worlds` |
| Off-sprint work | `./studio guard <p> "request"` |
| Ticket workflow | [process/ticket-workflow.md](process/ticket-workflow.md) |

## Studio-only improvements

Use **LO-*** tickets in `.quinsy-studio/backlog/` — not project code.

```bash
./studio learn "..." --signal tooling-gap
./studio learn-list
```
