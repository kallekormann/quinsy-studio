# Sprint planning playbook

Rules for scoping a sprint. Product-agnostic; provenance lives in `CHANGELOG.md`.

## Proof surface (LO-0235)

No sprint is purely internal. Every sprint — including infrastructure sprints — ships an **observable artifact**: a smoke test that defines "the product works", a receipt, or a minimal honest view, so progress is verifiable rather than asserted. The loop-closure smoke test pattern (perform the action, then assert the **full chain of effects**) doubles as the product's definition of working.

## Truth before polish (LO-0235)

Where an existing surface displays invented or placeholder data, the honest (often emptier) version ships **before** any refinement. Tell the human in advance that it will look like a regression, and ship designed empty states so honesty reads as intentional.

## Disjoint file lists (LO-0235)

Two tickets running in parallel within one sprint must have **disjoint `files:` lists**. Overlapping files serialize the work or produce merge damage; split or sequence the tickets instead.
