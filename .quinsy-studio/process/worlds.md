# Two Worlds — Studio HQ vs Project

Quinsy Studio enforces **strict separation** between meta-studio and client projects.

## World A — Studio HQ (this git repo)

| Path | Committed? |
|------|------------|
| `.quinsy-studio/` | Yes |
| `studio`, `AGENTS.md`, `README.md` | Yes |
| `projects/` | **Never** |
| `intake/` | **Never** |

Studio improvements use **LO-*** tickets in `.quinsy-studio/backlog/`.

## World B — Project (own git repo)

Each project under `projects/<name>/` has:

- Its own `git init` on `./studio init`
- Its own remote (via `./studio repo <name> create` — human approval)
- Code, tickets, design, docker — all local to the project

## Verification

```bash
./studio verify-worlds
./studio verify-abstraction
```

Fails if:

- Studio git tracks anything under `projects/` or `intake/`
- A project folder exists without `.git/`

## Git remotes (two repos)

| Location | `origin` should be |
|----------|-------------------|
| Quinsy Studio root (`quinsy-studio/`) | `https://github.com/kallekormann/quinsy-studio.git` |
| Project (`projects/<name>/`) | That project's own remote (e.g. `acme-app.git`) |

Studio HQ commits: `.quinsy-studio/`, `studio`, `AGENTS.md` only.  
Project commits: everything under `projects/<name>/` from **inside** that folder.

```bash
# Studio root
git remote -v   # → quinsy-studio

# Project
cd projects/<name> && git remote -v   # → project repo
```

## Agent rules

1. **Never** `git add projects/` from the studio repo root
2. **Never** commit project code into quinsy-studio
3. Project git operations run **inside** `projects/<name>/` (`git -C projects/<name> …`). The git toplevel must be that folder — never the studio root, never a sibling project
4. **Never** Read, copy, merge, or commit another `projects/<sibling>/` tree into the active project
5. Studio tooling changes live in `.quinsy-studio/` only
6. Studio docs/tools use `<project>` placeholders — see [studio-abstraction.md](studio-abstraction.md)

`./studio focus <project>` (and `./studio isolate <project>`) rewrites a local `.cursorignore` block so sibling project folders are hidden from the IDE agent, and installs a project `pre-commit` hook that refuses escaped paths / symlinks into `projects/`. Those files are gitignored in Studio HQ.

## .gitignore (studio root)

`projects/` and `intake/` are gitignored. If they were committed before the rule, remove from index:

```bash
git rm -r --cached projects/ intake/ 2>/dev/null || true
```
