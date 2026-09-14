# Agentic loop playbook

> A dashboard of signals is not learning. Learning exists only when **guidance is stored, versioned, and read back into the next generation**.

## Loop shape

```
signal → cluster → proposed delta → human confirm → deterministic merge → prompt injection
                                                                      ↓
                                                            provenance: versions used
```

Each step has one owner. The LLM does **not** own merge.

## Store, not a vibe

Learned guidance lives in a **write target** the next run can read:

- Versioned playbook (or equivalent) entries
- Each entry cites **evidence** (ticket, log, eval, human edit)
- A human can **retire** an entry
- Displayed rates carry a **sample size**, or the UI says “not enough data”

If nothing writes into that store, you have telemetry, not a loop.

## Delta operations only (ACE)

Playbooks evolve by **ADD / UPDATE / REMOVE** applied by a **deterministic, non-LLM merge**. Full model rewrites cause brevity bias and context collapse (ACE, ICLR 2026).

| Role | Who | Allowed |
|------|------|---------|
| Generator | LLM | Produce candidate output using current playbook versions |
| Reflector | LLM | Propose a **delta** (what to add/change/remove, with evidence) |
| Curator | Human + code | Confirm; merge is **code**, never “rewrite the whole file” |

Treat procedural memory as **code**: versioned, diffable, human-gated promotion. Never auto-write memory from a model pass.

## Anti-patterns

| Don’t | Do |
|-------|----|
| Model rewrites the playbook each cycle | Apply a confirmed delta |
| Auto-confirm every reflection | Human gate before merge |
| Signals with no consumer | Name the store and the injection site |
| Rate without n | Show sample size or withhold the rate |

## Studio HQ (this repo)

Team **07** owns loop integrity; Team 09 owns harvest process.

```
./studio learn "…" --signal … --source <project>
  → portable? LO + inbox : docs/studio-learnings-local.md
./studio train <skill> --topic "…" --lo LO-NNNN   # sidecar; observation required for --from lo
./studio infusion-delta --path knowledge-base/….md --op add --section Deltas --body "…"
./studio train --done TR-NNNN           # or --lo LO-NNNN; auto-sync when LO is in backlog/done/
./studio cite knowledge-base/….md --helpful PB-YYYYMMDD-001 [--harmful PB-…]
Receipt ## Playbook citations (helpful/harmful) bump ACE counters on MOVE_DONE.
CARD injects ≤6 ranked playbooks. Do not Read learnings/inbox.md on IMPLEMENT.
```

`STUDIO_LO` only when the product loop is idle. Open LOs never block `./studio sprint`. See `process/learning-loop.md`.
