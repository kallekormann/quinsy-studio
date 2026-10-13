# HQ epic — session-scoped binding (one window, many products)

> Studio-meta plan. Tickets `LO-0419` to `LO-0424` in `backlog/open/`. Nothing here writes into `projects/`.
> Until this epic is done, isolation stays **workspace-global**: one `.cursorignore`, one generated rule, one `.active-project.json`. Several chats in one Cursor window will keep overwriting each other. Workaround: one window (or git worktree) per product, or one `./studio execute` at a time.

## 1. Finding

Product git is already separate (`git -C projects/<name>`). Studio HQ git never stages `projects/`. What is shared is the **IDE enforcement surface**:

| Artifact | Today |
|----------|--------|
| `.cursorignore` QUINSY-ISOLATION block | Hides every sibling of the last focused product |
| `.cursor/rules/quinsy-project-isolation.mdc` | `alwaysApply: true`, names one active product |
| `.quinsy-studio/.active-project.json` | One active product for the whole workspace |
| `./studio execute <p>` | Acquires a **project** lease, then `apply_project_isolation(p)` and rewrites the row above |

`parallel.max_projects` (default 5) only caps leases. `./studio focus` refuses to clobber a live lease unless `--force`. Neither gives each Composer chat its own tree. Shipped in [hq-isolation-sprints.md](hq-isolation-sprints.md) (`LO-0324`–`LO-0326`).

## 2. Decision

**Cursor only.** The switch is the existing HQ key `runtime` in `.quinsy-studio/studio.settings.yaml` (already `cursor`). No second flag.

| `runtime` | Multi-project behavior |
|-----------|------------------------|
| `cursor` | Session bind, session leases, Cursor hooks. `execute` / `focus` do not rewrite the sibling block. |
| any other value (`claude`, `cli`, …) | Today's workspace isolation. `./studio bind` refuses. Hook scripts, if present on disk, allow the call and do not deny. `execute` still calls `apply_project_isolation`. A missing key already defaults to `cursor` in the settings loader, so the off switch is an explicit other value. |

Claude Code reads `CLAUDE.md` and does not run `.cursor/hooks`. A terminal CLI does not either. Both call the same `./studio` Python. The encapsulation is in that Python and in the first line of every hook: if HQ `runtime` is not `cursor`, leave behavior unchanged. Product `docs/studio.settings.yaml` does not turn this on — the workspace file does, because the window is one studio root.

**Same Cursor window, one chat per product, enforced per conversation — not per workspace.** Only when `runtime` is `cursor`.

1. Each agent session binds to exactly one product with `./studio bind <project>`.
2. Binding lives under `.quinsy-studio/.cache/agent-sessions/<sessionId>.json` (gitignored cache). It is not `.active-project.json`.
3. Execute leases are `(sessionId, project)`. A second session may execute a different product at the same time, up to `parallel.max_projects`.
4. `./studio execute` and `./studio focus` **stop rewriting** sibling isolation while session binding is on. The secrets block in `.cursorignore` stays (names, never values).
5. Cursor hooks (`beforeReadFile`, `beforeShellExecution`, `sessionStart`) deny reads and shell paths under `projects/<other>/` and deny `git` whose toplevel is not `projects/<bound>/` or the studio root for HQ paths.
6. If the hook payload has **no stable session id**, multi-project mode stays **off**. Global isolation remains the safe default. Do not ship a gate that cannot tell chats apart.

Human stops do not change. This epic does not pause product execute. Implement it in an **HQ session** (`STUDIO_META`).

## Session id

Cursor documents a stable per-chat id. `conversation_id` is on every tool hook (`beforeReadFile`, `beforeShellExecution`, `preToolUse`) and stays the same across turns. `sessionStart` sends `session_id` and documents it as the same value. `generation_id` changes every user message, so it is not the bind key.

`multi_project_mode: on` when HQ `runtime` is `cursor`. The hook script and `./studio bind` no-op or refuse for any other runtime. Hooks stay in git so Cursor can load them; they allow the call when runtime is not `cursor`.

Field path: `conversation_id` (fallback `session_id`).

## 3. Waves

| Wave | LO | Scope |
|------|----|--------|
| **W0 Identity** | LO-0419 | Record hook stdin for `sessionStart`, `beforeReadFile`, `beforeShellExecution`. Name the session-id field, or record that it is missing and keep multi-project mode off |
| **W1 Bind** | LO-0420 | `studio_agent_sessions.py`; `./studio bind <project>`, `--show`, `--clear`; cache file per session; unit tests with a fixture id |
| **W2 Leases** | LO-0421 | Lease key is session + project; `execute` / `focus` do not call `apply_project_isolation` when the session is bound; `.active-project.json` is the human/CLI default only |
| **W3 Hooks** | LO-0422 | `.cursor/hooks.json` + scripts: deny sibling reads, deny wrong-repo git, inject “this session is bound to `<project>`” on start. `failClosed` on the deny hooks. No product names in HQ |
| **W4 Contract** | LO-0423 | `guard` warns when the named project ≠ the session binding; isolation rule text becomes session-scoped; AGENTS, GETTING_STARTED, agent-context, README, CHANGELOG |
| **W5 Proof** | LO-0424 | Unit tests, `verify-worlds` asserts hooks exist when binding is on, two-session dry run on a throwaway tree (deleted after) |

## 4. Done when

- Two fixture session ids can `bind` and `execute` two different projects without either call rewriting `.cursorignore` sibling lines.
- A hook fixture that reads `projects/<other>/…` is denied; a read under the bound project and under `.quinsy-studio/` is allowed.
- A hook fixture whose shell command is `git -C projects/<other>` is denied; `git -C projects/<bound>` is allowed.
- `./studio verify-worlds` and `./studio verify-abstraction` stay green (zero product nouns).
- If LO-0419 finds no session id, LO-0422 and LO-0424 record the mode as **off** and the epic stops there instead of pretending chats are isolated.

## 5. Out of scope

- Per-chat `.cursorignore` (Cursor does not offer it). Hooks are the enforcement.
- Moving the IDE into Docker.
- Changing product git layout.
- Raising `parallel.max_projects`.
