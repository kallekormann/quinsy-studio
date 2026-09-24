---
id: LO-0337
title: Distill eval and context catalog; add thin AI-004; retarget AI-003 away from PE-002 CI/CD
type: studio-evolution
status: done
phase: 6
priority: P1
estimate: L
assignee_role: Autonomous Systems Director
team: 07-ai-autonomous-systems
skills: [AI-001, AI-003, BE-006, PE-002, SO-001]
dependencies: [LO-0331]
files: [.quinsy-studio/knowledge-base/ai_automation_playbook.md, .quinsy-studio/teams/07-ai-autonomous-systems/, .quinsy-studio/teams/skill-registry.md]
sprint: HQ-SKILL-05
epic: HQ-SKILL
signal: process-gap
source: studio-hq
infusion_kind: playbook
infusion_path: knowledge-base/ai_automation_playbook.md
train_skills: [AI-001, AI-003]
created: 2026-09-24
---

## Target
Catalog `agent-evaluation`, `context-window-management`, `autonomous-agent-patterns`, and **`workflow-automation/workflow-automation`** distill into `ai_automation_playbook.md`. New **AI-004 Eval & context**. **AI-003** is studio train/infusion **and durable agent workflows** (checkpoints, idempotency, sequential/parallel/orchestrator-worker). GitHub Actions stays **PE-002**. Job queues stay **BE-006**.

## Scope
Thin `skills/eval-and-context.md`. Rewrite AI-001 generic provider list to adapter + eval + user-visible surface (existing LO-0017). Distill workflow-automation: no payment/side-effect without durable execution; no monolithic workflow; observability required. n8n/Temporal/Inngest = **ADR**, not a default install. Related catalog reads: `inngest`, `n8n`, `trigger-dev`. Epic: process/hq-skill-advancement-sprints.md.

## AC
- AI-004 file + Team 07 README + registry
- AI-003 skill no longer lists CI/CD as primary; PE-002 remains CI
- AI-003 / playbook include durable-execution Do/Don’t from `workflow-automation`
- playbook sections: eval harness, context budget, tool-exfil / prompt injection pointer to PE-003
- CHANGELOG

## Out of scope
Product LLM keys in chat. Eval receipt CLI (LO-0338). Shipping n8n as a studio HQ service.
