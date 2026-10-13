# Skill: Threat Modeling

> Finds design-level security flaws before code exists. Produces one project threat model with a data map at gate 1, and a short threat delta per ticket in the architecture phase. Each threat ends in a testable requirement, not a recommendation. This skill designs the controls; PE-003 and AI-005 check the code.

## Metadata

```
skill_id: PE-005
name: Threat Modeling
team: 08-platform-enterprise-engineering
lead_role: Platform Architect
support_roles: [Backend Security Engineer, Backend Architect, Data Protection Lead]
phases: [1, 2, 4]
activation_triggers:
  - Gate 1 architecture packet (project threat model + data map)
  - Architecture-phase ticket that adds a collection, endpoint, webhook, upload, job, role, tenant or third-party call
  - Ticket words: threat model, trust boundary, attack surface, multi-tenant, tenant isolation, admin access
pairs_with: [PE-003, PE-006, AI-005, BE-003, BE-007, CL-004]
```

## When to load

- Gate 1: always, for every web product. The gate-1 packet is not complete without `docs/security/threat-model.md`.
- Architecture phase: on every ticket. Most tickets end with `threat delta: none`. The skill decides that, not the ticket author's guess.
- Implementation: only when the code departs from the signed architecture doc (new boundary found while coding). Stop and write the delta first.

## Rules

### 1. One project threat model, written at gate 1

`docs/security/threat-model.md` holds: system overview (stack, deploy target, external services), a link to the data map with access paths (rule 2), the trust-boundary table, STRIDE per boundary, and the requirement list. Keep it under three screens. It is a living file: each threat delta updates it in the same ticket.

### 2. The data map comes first

There is one data map: `docs/security/data-map.md`, owned by CL-004 (category, purpose, legal basis, where stored, retention, processor). Do not keep a second copy. The `## Data map` section of the threat model links to that file and adds what this skill owns: the class of each data category (`public`, `internal`, `personal`, `special-category` per DSGVO Art. 9, `secret` for credentials and tokens) and **who can read it through which path** (admin, REST/GraphQL, Local API, job, third party). If the file does not exist yet, write it with CL-004's columns in the same ticket. A field that is not on the map must not be collected.

### 3. Name the trust boundaries of our stack

Every Payload project has these boundaries. Mark each `in` or `n/a` in the table:

| Boundary | Typical threat | Control to name |
|---|---|---|
| Browser → Next.js routes `(app)`, `(marketing)` | IDOR, XSS, CSRF | Server-side session check, output encoding, Payload `csrf` allowlist |
| Browser → `/admin` | Privilege escalation, brute force | `access.admin`, `maxLoginAttempts`, admin role field-locked |
| Client → REST `/api/<slug>` and GraphQL `/api/graphql` | Broken object access, over-fetch via `depth`, GraphQL complexity | Collection `access` on every operation, `maxDepth`, GraphQL disabled or `maxComplexity` set |
| Server code → Local API | Access bypass (`overrideAccess` defaults to `true`) | `overrideAccess: false` + `user` on user-driven calls |
| Upload → S3 / R2 | Malicious file types, public private files | `upload.mimeTypes`, size limit, no `disablePayloadAccessControl` on private media |
| Hooks (`beforeChange`, `afterChange`) | Hidden writes without access checks, role self-assignment | Field-level access on role fields, `req` passed to nested calls |
| Jobs (Payload jobs, Python worker) | Job input trusted as system input | Validate job input, store the acting user id, re-check access |
| Inbound webhooks (Stripe, Lemon Squeezy, others) | Forged events, replay | Signature check on the raw body, idempotency key |
| App → third-party APIs and LLMs | Secret leak, SSRF, prompt injection | Server-only keys (PE-006), URL allowlist, AI-005 sink rules |
| App → Postgres | Injection, over-privileged DB user | Payload/Drizzle queries only, no string SQL, DB port not published |
| Tenant A → tenant B | Cross-tenant read or write | See rule 6 |

### 4. STRIDE per boundary, kept short

One row per real threat. Columns: Boundary, STRIDE letter, Scenario (one sentence), Control, Requirement ID. Skip letters that do not apply; do not pad. Rate risk `high` / `medium` / `low` by impact on users and data, not by a score you cannot defend.

### 5. Every threat ends in a testable requirement

Write `SR-nn: <check>` with how it is proven. Good: "SR-04: `PATCH /api/users/:id` with another user's id returns 403 (integration test `users.access.test.ts`)." Bad: "use proper access control." Requirements become acceptance criteria on the ticket that owns the boundary.

### 6. Multi-tenant isolation is a named decision

If the product has more than one customer organization, gate 1 states the model: row-level `tenant` field (Payload multi-tenant plugin or own field), separate schema, or separate database. For the row-level model:

- Every tenant-scoped collection's `read`, `update`, `delete` returns a `where` on `tenant`; `create` sets `tenant` server-side from the user, never from the request body.
- Local API calls in hooks and jobs filter by tenant explicitly.
- Uploads are tenant-scoped (prefix or field) and access-checked.
- One cross-tenant test per collection: user of tenant A gets 404 or 403 on tenant B's document via REST and Local API.

### 7. Threat delta per ticket

In the architecture phase, `docs/architecture/<TICKET>.md` contains either the line `threat delta: none` with a one-line reason, or a `## Threat delta` section: new or changed boundary, new STRIDE rows, new or changed SR-nn, and the data-map change. The same commit updates `docs/security/threat-model.md`. A ticket that adds a collection, endpoint, webhook, upload, job, role or tenant rule cannot say `none`.

### 8. Prefer removing the surface

Before adding a control, ask whether the surface is needed: disable GraphQL if no client uses it, keep media private unless it is marketing content, do not expose an endpoint that only the server calls.

## Workflow

1. Read the PRD, blueprint and `env.schema.json` (names only).
2. Write the data map (rule 2).
3. Fill the boundary table (rule 3); mark `n/a` rows with a reason.
4. Write STRIDE rows for `in` boundaries (rule 4).
5. Turn each row into an SR-nn requirement with its proof (rule 5).
6. State the tenant model if there is more than one customer org (rule 6).
7. Hand SR-nn list to the ticket writer; each SR maps to a ticket AC.
8. Per architecture-phase ticket: write the threat delta or `threat delta: none` (rule 7).

## Deliverables

- `docs/security/threat-model.md` with sections: `## System`, `## Data map`, `## Trust boundaries`, `## STRIDE`, `## Requirements`, `## Tenant model` (or `n/a`), `## Change log`.
- Per ticket: `## Threat delta` in `docs/architecture/<TICKET>.md`, or `threat delta: none — <reason>`.

## Done evidence (receipt)

- Gate 1: `docs/security/threat-model.md` exists, has all seven headings, and every `in` boundary has at least one STRIDE row or a stated reason for none.
- Architecture ticket: receipt section `## Threat delta` repeats the delta or `none — <reason>`, and names the threat-model commit.
- Implementation ticket owning an SR: receipt `## Security` lists each SR-nn as PASS / FAIL / N/A with the test file path that proves it.

## Anti-patterns

- A threat model copied from a template with Kubernetes, mTLS and API gateways the product does not have.
- "Mitigation: input validation" with no field, no boundary, no test.
- `threat delta: none` on a ticket that adds a webhook or a role.
- Trusting `tenant` or `role` from the request body.
- Invented risk scores (likelihood × impact numbers) with no basis.
- A threat model nobody updates after gate 1.

## Handoff

- To the ticket writer (PM-002 / execute): SR-nn list becomes acceptance criteria.
- To BE-007 and BE-003: access rules per collection and role fields to lock.
- To PE-006: every `secret` class on the data map becomes a row in `docs/security/secrets-inventory.md`.
- To CL-004 / CL-001: the data map for minimization, retention and the record of processing.
- To PE-003 and AI-005: the boundary table is their audit scope at phase 5.

## References

- OWASP Threat Modeling Cheat Sheet; OWASP ASVS 4.0 (V1 architecture, V4 access control).
- `teams/02-backend-systems/skills/payload/SKILL.md` and `reference/ACCESS-CONTROL.md`, `reference/QUERIES.md` (Local API access).
- `knowledge-base/payload-playbook.md`.
- Source: agency-agents `security/security-architect.md`, `security/security-appsec-engineer.md` (MIT), rewritten for Payload, Compose and Coolify.
