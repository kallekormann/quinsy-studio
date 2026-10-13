# Skill: Incident, Reliability and Breach Response

> Gets a broken or breached production app back to safe service, and meets the legal clock when personal data is involved. Produces the incident runbook before the first `ship --to main`, a breach log, a tested restore, and a blameless postmortem after every SEV1 or SEV2. The agent drafts; the human (the controller) decides and sends any notification.

## Metadata

```
skill_id: PE-007
name: Incident, Reliability and Breach Response
team: 08-platform-enterprise-engineering
lead_role: Platform Architect
support_roles: [DevOps Engineer, Backend Engineer, Data Protection Lead]
phases: [5, 7]
activation_triggers:
  - Before the first ./studio ship <p> --to main (runbook, backups, restore drill)
  - Production outage, data loss, failed deploy or failed migration
  - Suspected personal-data breach, leaked credential that was used, unauthorized access
  - Ticket words: incident, outage, postmortem, restore drill, backup, data breach, Datenpanne
pairs_with: [PE-001, PE-002, PE-004, PE-006, CL-001, CL-004]
```

## When to load

- Ops readiness: before the first production ship, and when the deploy target, database or backup setup changes.
- Live incident: immediately. Mitigation comes before root cause.
- After an incident: postmortem within a few working days, while the timeline is fresh.

## Rules

### 1. Severity is defined by user impact

| Level | Definition | Breach check |
|---|---|---|
| SEV1 | Core journey unusable for all or most users, data loss, or personal data possibly exposed | Start the breach assessment (rule 5) now |
| SEV2 | Core journey broken for some users, or a paid feature down with no workaround | Only if data exposure is possible |
| SEV3 | Non-core feature broken, a workaround exists | No |
| SEV4 | Cosmetic, no user impact | No |

Any doubt about data integrity or confidentiality raises the level to SEV1 until ruled out. Response targets per level are set in the runbook by the human; the skill does not invent them.

### 2. Mitigate first, then diagnose

Order: stop the harm, restore service, then find the cause. Mitigation options, in order of preference:

1. Redeploy the previous image in Coolify (app-only regressions).
2. Turn the feature off (flag, env toggle, or route returning 503 with a clear message).
3. Forward-fix migration (rule 7).
4. Restore from backup (data loss or corruption only; this loses writes since the backup).

Timebox each hypothesis. Write every action with a UTC timestamp in `docs/ops/incidents/INC-NNN.md` as you go.

### 3. Preserve evidence before you change things

Before restarting or redeploying a suspected breached system: export Coolify and app logs for the window, record the running image tag, take a database dump to off-host storage. Do not delete accounts, logs or files an attacker touched; disable them instead.

### 4. Contain credentials

On suspected compromise: rotate every secret the affected container could read (PE-006 leak order), invalidate sessions (rotate `PAYLOAD_SECRET` to force re-login; API keys stored with `useAPIKey` depend on it and must be reissued), and lock admin accounts that show unknown activity.

### 5. Personal-data breach: DSGVO Art. 33 and 34

A breach is any security failure that leads to destruction, loss, change, unauthorized disclosure of, or access to personal data (Art. 4(12)). Availability loss counts too.

- **Clock:** the controller must notify the competent supervisory authority without undue delay and, where feasible, within 72 hours after becoming aware (Art. 33(1)). "Aware" is when there is reasonable certainty a breach happened. Record that timestamp.
- **When not required:** only if the breach is unlikely to result in a risk to people's rights and freedoms. Write down why.
- **Authority:** in Germany usually the state data protection authority (Landesdatenschutzbeauftragte) where the controller is established. Name it in the runbook before launch.
- **Content (Art. 33(3)):** nature of the breach, categories and approximate number of people and records, contact point, likely consequences, measures taken or planned. Information may be sent in phases (Art. 33(4)).
- **Data subjects (Art. 34):** inform affected people without undue delay when the breach is likely to result in a high risk. Not required if the data was encrypted and unreadable, if later measures removed the high risk, or if individual notice is disproportionate (then a public notice).
- **Processors:** a processor tells the controller without undue delay (Art. 33(2)). Check each vendor DPA for how they notify you.
- The agent drafts the assessment and the notification text. The human decides and submits. The agent never contacts an authority or users on its own.

### 6. Keep a breach log

Every breach goes in `docs/ops/breach-log.md`, notified or not (Art. 33(5)): ID, aware-at (UTC), facts, data categories, people affected (approx.), risk assessment, notified authority yes/no + why, notified people yes/no + why, measures, link to INC-NNN.

### 7. Forward-fix over rollback for migrations

- Do not run `payload migrate:down` in production as an incident step; down migrations drop data written since the up.
- Redeploying the previous image is safe only if the schema is still compatible with it. That is why migrations are expand/contract (PE-002).
- If a migration broke production: ship a new forward migration that repairs the schema or data, tested on a restored copy first.
- A destructive reset or a restore that drops writes is HITL (`./studio ops <p> db --reset --approve`).
- The forward migration itself runs from the agent seat after the human signs: `./studio ops <p> migrate --prod --approve`. Read the diagnosis from `./studio ops <p> logs` and `status` first; both are agent-run and logged in `docs/ops/ops-log.md`.

### 8. Backups exist only if a restore works

- Coolify scheduled backups of the production Postgres to S3-compatible storage outside the VPS and its provider account (another provider or another EU region).
- Uploads in R2: versioning or a second copy, so a deleted bucket object can come back.
- Restore drill before the first main ship and then on a schedule the human sets: restore the latest dump into a scratch Postgres container, point a local app at it, run `payload migrate:status` and a smoke query set. Record date, dump age (recovery point) and time taken (recovery time) in the runbook.
- Retention of backups follows the deletion concept (CL-004): erased users must not live forever in backups.

### 9. Postmortems are blameless and short

Write about the system, not people: what allowed this failure. At most five action items, each with an owner and a ticket. A repeat cause means an earlier action item was not done; say so.

## Workflow

1. **Readiness:** write `docs/ops/incident-runbook.md` (template below), set up backups, run the restore drill.
2. **Detect:** alert from PE-004 monitoring, user report, or provider notice. Open `INC-NNN.md`, set severity.
3. **Mitigate:** rule 2 in order. Verify recovery with real requests, not "looks fine".
4. **Breach check:** if personal data may be involved, run rule 5 now and start the breach log entry.
5. **Resolve:** confirm health checks, error rate back to normal, core journey works.
6. **Postmortem:** template below; action items become tickets.

## Deliverables

`docs/ops/incident-runbook.md` contains:

- Contacts: owner, hosting provider, DNS, email provider, payment provider, supervisory authority (name and URL).
- Where to look: Coolify app and logs, monitoring dashboard, provider status pages.
- Mitigation steps: previous-image redeploy in Coolify, feature off-switch, forward-fix migration path.
- Backup location, restore steps, last drill date with recovery point and recovery time.
- Severity table (rule 1) and breach steps (rule 5).

`docs/ops/incidents/INC-NNN.md` postmortem template:

```
# INC-NNN: <title>
Severity: SEV<n> | Start / end (UTC): | Breach: yes / no / assessed-not-required
## Summary (3 sentences: what, who was affected, how it was fixed)
## Impact (users, data, duration)
## Timeline (UTC)
## Causes (trigger, why it was possible, what was missing)
## What worked / what did not
## Action items (max 5: action, owner, ticket)
```

`docs/ops/breach-log.md` (rule 6).

## Done evidence (receipt)

- Readiness ticket: receipt `## Risk & rollback` names the runbook path, backup target (provider and region, no credentials), and the restore drill result: date, dump age, restore duration, smoke result PASS / FAIL.
- Incident ticket: receipt links `INC-NNN.md`; `## Risk & rollback` states the mitigation used; breach line says `breach: yes (log entry B-NNN)`, `no (reason)` or `assessed — not notifiable (reason)`.

## Anti-patterns

- Running `migrate:down` against production data.
- "We have backups" with no restore ever done.
- Backups stored on the same VPS or provider account as the database.
- Waiting for full root cause before notifying when the 72-hour clock runs.
- Not logging a breach because it was judged not notifiable.
- Postmortems that name a person as the cause.
- The agent emailing users or the authority without the human.

## Handoff

- To PE-002: forward-fix migration and the previous-image redeploy.
- To PE-006: credential rotation after compromise.
- To CL-001: breach assessment for the record of processing and the privacy notice.
- To the ticket writer: postmortem action items as tickets for the next phase.
- To the human: notification drafts and the decision to send.

## References

- DSGVO Art. 4(12), 33, 34; EDPB Guidelines 9/2022 on personal data breach notification.
- NIST SP 800-61 (incident handling).
- Coolify docs: scheduled database backups, deployment rollback.
- Payload docs: migrations (`migrate`, `migrate:status`).
- Source: agency-agents `security/security-incident-responder.md`, `engineering/engineering-incident-response-commander.md`, `engineering/engineering-sre.md`, `engineering/engineering-database-reliability-engineer.md`, `specialized/data-privacy-officer.md` (MIT), rewritten for Coolify, Postgres and German law.
