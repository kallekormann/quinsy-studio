# Quinsy Studio

You name a direction. The studio researches it, writes the product down, and builds it. You stop at named gates. Between those gates the agent keeps going.

The reference is the [manual](.quinsy-studio/docs/README.md). Start with [the concept](.quinsy-studio/docs/07-concept.md), then [the three loops](.quinsy-studio/docs/02-three-loops.md).

## What is in this repo

Studio git holds the method: process, teams, skills, the learnings catalog, the library, and the templates. A clone does not contain your products, your research notes, or the tickets that produced a lesson.

| Layer | Path | In studio git? |
|-------|------|----------------|
| Studio HQ | `.quinsy-studio/`, `studio`, `AGENTS.md` | Yes |
| This manual | `.quinsy-studio/docs/` | Yes |
| Learnings catalog | `knowledge-base/learnings/<domain>/` | Yes — the principle |
| Ideation notes | `ideation/` | No |
| Products | `projects/<name>/` | No — each product has its own git repo |
| Product definition before bootstrap | `intake/` | No |
| Tickets, retros, train queue | `.quinsy-studio/backlog/`, `retros/`, `sprints/`, `learnings/` | No |

## After you clone

```bash
./studio install
./studio verify-worlds
./studio verify-abstraction
```

Node.js 20 or newer. Docker Desktop is required to boot, migrate, and pass a gate. Open this repo at the root. You talk. The agent runs `./studio`.

| You have | You say | Read |
|----------|---------|------|
| A direction, no product | *"Look into …"* | [The path](.quinsy-studio/docs/04-the-path.md) |
| A definition in `intake/` | *"Bootstrap `<project>` and walk me through gate 0."* | [The product loop](.quinsy-studio/docs/08-product-loop.md) |
| Code that already runs | *"Adopt `<project>` from this folder."* | [The product loop](.quinsy-studio/docs/08-product-loop.md) |

## The manual

| Topic | Chapter |
|-------|---------|
| Setup | [01-setup.md](.quinsy-studio/docs/01-setup.md) |
| Concept and rules | [07-concept.md](.quinsy-studio/docs/07-concept.md) |
| The three loops | [02-three-loops.md](.quinsy-studio/docs/02-three-loops.md) |
| The path | [04-the-path.md](.quinsy-studio/docs/04-the-path.md) |
| What you say | [15-what-you-say.md](.quinsy-studio/docs/15-what-you-say.md) |
| Gates and how you work the build | [08-product-loop.md](.quinsy-studio/docs/08-product-loop.md) |
| Several products in one window | [03-several-products.md](.quinsy-studio/docs/03-several-products.md) |
| Payload, secrets, production | [13-foundation.md](.quinsy-studio/docs/13-foundation.md) |
| Library | [12-library.md](.quinsy-studio/docs/12-library.md) |
| Why training sessions exist | [09-hq-learning.md](.quinsy-studio/docs/09-hq-learning.md) |
| Teams and skills | [10-teams.md](.quinsy-studio/docs/10-teams.md) · [11-skills.md](.quinsy-studio/docs/11-skills.md) |
| Commands | [05-commands.md](.quinsy-studio/docs/05-commands.md) |
| When you are stuck | [06-when-you-are-stuck.md](.quinsy-studio/docs/06-when-you-are-stuck.md) |

The agent contract is [AGENTS.md](AGENTS.md). Other hosts: [Claude Code](CLAUDE.md) · [Gemini CLI](GEMINI.md) · [Hosts](.quinsy-studio/docs/16-hosts.md).
