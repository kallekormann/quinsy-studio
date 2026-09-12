---
id: LO-0232
title: Capture human edit diffs on agent output — edit distance is the headline zero-traffic learning metric
type: studio-evolution
status: open
phase: 6
priority: P1
estimate: S
assignee_role: Autonomous Systems Director
team: 07-ai-autonomous-systems
skills: [AI-003]
dependencies: [LO-0231]
files: [.quinsy-studio/knowledge-base/agentic-loop-playbook.md, .quinsy-studio/CHANGELOG.md]
signal: architecture-gap
source: affiliate-platform
infusion_kind: process
infusion_path: knowledge-base/agentic-loop-playbook.md
train_skills: [AI-003]
created: 2026-09-12
---

## Target
Approve/reject captures one bit per review; the human's edit of an agent draft carries hundreds — dense, specific, available with zero external traffic. Any agentic product (and the studio itself, for design specs, tickets, and receipts the human corrects) should: (1) make output immutable/versioned so before/after is stable; (2) capture the diff automatically on every human-edited acceptance; (3) report normalised edit distance as the headline "is it learning?" metric — reference-free, free to compute, should trend down; (4) pair it with rejection rate to distinguish improvement from review fatigue. Named research pattern: coactive learning / PRELUDE-CIPHER; preference learning over imitation because partial fixes make the accepted version non-gold.

## Scope
Kind `process`. Add a "T0 edit-diff capture" section to `knowledge-base/agentic-loop-playbook.md` (created by LO-0231). Product-agnostic; provenance in CHANGELOG only.

## AC
- Section added with the four rules and the edit-distance metric definition
- Portability gate passes; CHANGELOG updated; LO moved to done
