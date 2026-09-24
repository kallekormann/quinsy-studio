# Skill: Jobs and Delivery (BE-006)

```
skill_id: BE-006
team: 02-backend-systems
lead_role: Backend Architect
support_roles: [Backend Engineer]
```

Queues, workers, outbox, and **at-least-once** delivery. Not GitHub Actions (PE-002). Not durable **agent** orchestration (AI-003).

**Playbook:** [backend_playbook.md](../../../knowledge-base/backend_playbook.md)

## Do

- Idempotency keys on mutating jobs; outbox when a write must fan out.
- Bound retries + dead-letter; timeouts on every vendor call.
- Worker `--queue` lists every topology the dispatcher uses.
- Secrets as **names** in `env.schema.json`; inject via `./studio env … --approve`.

## Don’t

- Side effects in the orchestrator if this is a workflow (that is AI-003).
- GraphQL as a default (ADR only).
- Ask the human to migrate — run migrate when the DB is reachable.

## Implement-fail

- Job that cannot be retried safely (no idempotency).
- Queue name missing from the worker command (jobs sit forever).

**Triggers:** queue, worker, outbox, bullmq, background job, sync worker.
