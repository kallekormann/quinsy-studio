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
  → portable? LO + open inbox + learnings/<domain>/<topic>.md : docs/studio-learnings-local.md
./studio learn-find "queue"           # catalog search — not inbox.md
./studio train <skill> --topic "…" --lo LO-NNNN   # sidecar; observation required for --from lo
./studio infusion-delta --path knowledge-base/….md --op add --section Deltas --body "…"
./studio train --done TR-NNNN           # or --lo LO-NNNN; auto-sync when LO is in backlog/done/
./studio cite knowledge-base/….md --helpful PB-YYYYMMDD-001 [--harmful PB-…]
Receipt ## Playbook citations (helpful/harmful) bump ACE counters on MOVE_DONE.
CARD injects ≤6 ranked playbooks plus the domain learnings README. Do not Read learnings/inbox.md on IMPLEMENT.
```

`STUDIO_LO` only when the product loop is idle. Open LOs never block `./studio sprint`. See `process/learning-loop.md`.

## T0 edit-diff capture

- **PB-20260914-001** helpful=0 harmful=0 :: Approve/reject carries one bit per review; the human's **edit of an agent draft** carries hundreds — dense, specific, zero external traffic. For any agentic product (and studio HQ artifacts the human corrects: design specs, tickets, receipts):

1. **Immutable/versioned output** — every agent draft is stored as a version so before/after is stable.
2. **Automatic diff capture** — every human-edited acceptance records the diff; no manual step.
3. **Normalised edit distance is the headline "is it learning?" metric** — reference-free, free to compute, should trend down over time.
4. **Pair with rejection rate** — falling edit distance with rising rejections signals review fatigue, not improvement.

Research anchors: coactive learning / PRELUDE-CIPHER. Prefer preference learning over imitation — a partially fixed accepted draft is not gold.

## Quality ratchet

- **PB-20260914-002** helpful=0 harmful=0 :: Error analysis comes **before** evals; judges advise, never gate.

**Order of work (eval-driven development is an anti-pattern — failure modes are not predictable in advance):**
1. Read ≥100 real traces.
2. Label the earliest meaningful failure per trace.
3. Cluster and count.
4. Fix the trivially fixable first.
5. Write evaluators only for persistent, recurring failures.
6. Every fixed failure gets a test — deterministic assertion where possible.

**Evaluator cost hierarchy:** a new LLM judge costs 100+ labelled examples plus weekly maintenance; a deterministic check costs one assertion. Buy the assertion first.

**Judge discipline:** LLM-as-judge verdicts flip ~13.6% on repeated identical evaluation, with severe position and rubric-interference bias. Therefore: deterministic checks **gate**, judges **annotate**; one criterion per judge call; randomise order; never gate an irreversible action on a single-trial judge; calibrate judges against subsequent human decisions as a correctness requirement.

Applies to studio gate design too: derive new gate checks from observed failure traces, not imagination.
