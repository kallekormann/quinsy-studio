---
id: LO-0233
title: Error analysis before evals; deterministic checks decide and LLM judges only advise
type: studio-evolution
status: open
phase: 6
priority: P1
estimate: S
assignee_role: Autonomous Systems Director
team: 07-ai-autonomous-systems
skills: [AI-003, SO-002]
dependencies: [LO-0231]
files: [.quinsy-studio/knowledge-base/agentic-loop-playbook.md, .quinsy-studio/CHANGELOG.md]
signal: process-gap
source: affiliate-platform
infusion_kind: process
infusion_path: knowledge-base/agentic-loop-playbook.md
train_skills: [AI-003, SO-002]
created: 2026-09-12
---

## Target
Two quality rules for any agentic pipeline and for studio QA gates. (1) Eval-driven development is an anti-pattern: failure modes are not predictable in advance. Order: read ≥100 real traces → label the earliest meaningful failure → cluster and count → fix the trivially fixable → write evaluators only for persistent recurring failures → every fixed failure gets a test (assertion where possible). (2) LLM-as-judge verdicts flip ~13.6% on repeated identical evaluation with severe position and rubric-interference bias; therefore deterministic checks gate, judges annotate; one criterion per judge call; randomised order; never gate an irreversible action on a single-trial judge; calibrate judges against subsequent human decisions as a correctness requirement.

## Scope
Kind `process`. Add "quality ratchet" section to `knowledge-base/agentic-loop-playbook.md`: error-analysis-first loop, evaluator cost hierarchy (a judge costs 100+ labelled examples plus weekly maintenance), and the judge-discipline rules. Applies equally to studio gate design: derive new gate checks from observed failure traces, not imagination.

## AC
- Section added; the ordering rule and judge rules stated product-agnostically
- Portability gate passes; CHANGELOG updated; LO moved to done
