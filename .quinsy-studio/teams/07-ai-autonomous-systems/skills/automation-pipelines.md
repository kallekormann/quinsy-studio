# Skill: Automation Pipelines (AI-003)

> Durable **agent / product jobs** (checkpoints, idempotency, backoff).  
> GitHub Actions belongs to **PE-002**. Queues/outbox/workers belong to **BE-006**.

## Metadata

```
skill_id: AI-003
name: Automation Pipelines
team: 07-ai-autonomous-systems
lead_role: Studio Automation Engineer
support_roles: [Platform Architect, Backend Engineer]
phases: [3, 4, 5, 6, 7]
activation_triggers:
  - Durable workflow, orchestrator, Inngest, Temporal, n8n (ADR), train/infusion
  - Product agent jobs that must survive process restart
```

---

## Behavior rules

### 1. Studio loop (HQ)

```markdown
Studio automation is ./studio execute until HITL, then train / infusion-delta.
Do not import executing-plans (batch then wait) — it fights the execute loop.
```

### 2. Durable product / studio jobs

Distilled from catalog `workflow-automation` (not n8n-as-default).

**Do**

- Idempotency keys on every activity that has a side effect.
- Checkpointed steps; resume after crash.
- Activity timeouts + exponential backoff; no unbounded retry.
- Keep workflow **state small** — store blobs in object/DB, pass ids.
- No side effects in the orchestrator; only in activities/workers (BE-006).

**Don’t**

- Treat GitHub Actions as this skill (PE-002).
- Pick n8n / Temporal / Inngest / in-app workers without an **ADR**.
- Put huge payloads in workflow history.

**Implement-fail:** fire-and-forget LLM call that cannot resume; secrets in workflow state.

### 3. Platform choice (ADR)

| Option | When |
|--------|------|
| In-app workers + BE-006 | Default if the product already has queues |
| Inngest / Trigger.dev | Event-driven product jobs, HITL ADR |
| Temporal | Long-running, strongly consistent sagas, HITL ADR |
| n8n | Operator glue only after ADR — not agent CARD default |

### 4. Observability

Log step name, idempotency key, duration. Alerts on poison messages. Prompt-injection defenses: PE-003 (defensive).

## Related

- [ai_automation_playbook.md](../../../knowledge-base/ai_automation_playbook.md)
- BE-006 jobs-and-delivery
- PE-002 ci-cd-pipelines
- AI-004 eval-and-context
