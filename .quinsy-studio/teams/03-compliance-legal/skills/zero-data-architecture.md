# Skill: Zero-Data Architecture

> Data minimization, deletion concepts, data processing agreements, pseudonymization

## Metadata

```
skill_id: CL-004
name: Zero-Data Architecture
team: 03-compliance-legal
lead_role: Legal & Privacy Officer
support_roles: [Backend Architect, Systems Architect]
phases: [2, 3, 4]
activation_triggers:
  - Ticket contains "zero-data", "data minimization", "deletion concept"
  - Phase 2: data architecture is defined
  - External service providers are integrated
  - Feature requires personal data
  - Ticket words: data map, erase everywhere, right to erasure, retention period
pairs_with: [CL-001, PE-005, PE-007, BE-002, BE-006, BE-007]
```

---

## Behavior rules

### 1. Data minimization (Art. 5 GDPR)

```markdown
Principle: as little data as possible, as much as necessary

Checklist for every data field:
  - Do we really need this field?
  - Can it be pseudonymized?
  - Can it be aggregated?
  - Can it be deleted after use?
  - Is there a less invasive alternative?

Examples:
  ❌ store date of birth → ✅ only "over 18" boolean
  ❌ full IP address → ✅ pseudonymized IP
  ❌ name + email + phone → ✅ only email (communication)
```

### 2. Deletion concept

```markdown
Per data category:
  - Define the retention period (max.!)
  - Implement automatic deletion
  - Deletion must be verifiable
  - Consider backup deletion

Deletion strategies:
  - Soft delete → hard delete after the period
  - Anonymization (instead of deletion when aggregates are needed)
  - Pseudonymization (deletion of the mapping)
```

### 3. Data processing agreements (DPA)

```markdown
Mandatory for every external provider that processes personal data:

Content:
  1. Type and purpose of the processing
  2. Duration
  3. Type of personal data
  4. Category of data subjects
  5. Obligations of the processor
  6. Technical and organizational measures
  7. Sub-processors
  8. Third-country transfer (if any)

Examples of DPA obligations:
  - Hosting (Coolify on a VPS, Cloudflare R2)
  - Analytics (Plausible, PostHog)
  - Email (Resend)
  - Payment (Stripe, Lemon Squeezy)
  - Support (Crisp, Intercom)
```

### 4. Pseudonymization

```markdown
Techniques:
  - Hashing for user IDs in logs
  - Tokenization for payment data
  - Aggregation for analytics
  - K-anonymity for requests

Benefits:
  - Data protection despite analysis capability
  - Reduced risk in case of a data breach
  - Easier GDPR compliance
```

### 5. Privacy by design

```markdown
Architecture principles:
  1. Collect only necessary data
  2. Store data only as long as necessary
  3. Private by default (privacy-first)
  4. End-to-end encryption where possible
  5. Prefer client-side processing
  6. No third-party tracking without consent
```

### 6. Data map (deliverable)

You cannot minimise, protect or delete data you have not found. The data map
is the source of truth for CL-001 (record of processing, DPIA), PE-005
(threat model access paths) and PE-007 (breach scope). PE-005's
`## Data map` section links here instead of keeping a second copy.

```markdown
File: `docs/security/data-map.md` — written at gate 1, updated in the same
ticket that adds, changes or removes a field, store or processor.

One row per data category:
| Data category | Fields | Purpose | Legal basis | Where stored | Retention | Processor | Delete path |
|---|---|---|---|---|---|---|---|
| Account | email, name, password hash | Login, contract | Art. 6(1)(b) | Postgres `users` (+ `_users_v` versions) | Account life + 30 days | Coolify VPS host | `users` afterDelete hook |
| Newsletter consent | email, consent version, timestamps | Proof of consent | Art. 6(1)(c)/(f) | Postgres `subscribers` | Until withdrawal + proof period | Email provider | Job `erase-subscriber` |
| Uploads | user files | Feature X | Art. 6(1)(b) | S3/R2 bucket `media` | With owning document | R2 | Payload upload delete |
(example rows; fill with the project's real values)

Rules:
  - Every column filled; "unknown" is a FAIL, not a value
  - Search all stores, including the ones nobody thinks of: Payload version
    tables, job queue inputs, logs, error tracker, analytics, email
    provider, search index, caches, backups
  - Classes per row: public / internal / personal / special-category
    (Art. 9) / secret — secrets go to PE-006, not here
  - Retention is a period or an event, enforced by a job (BE-006),
    not by memory
  - A field not on the map must not be collected
  - "Anonymised" only if re-identification has been tested; removing
    names is pseudonymisation, still personal data
```

### 7. Erase everywhere

A deletion that clears one table is a false promise. Erasure (Art. 17)
reaches every store on the data map and leaves an audit record.

```markdown
Fan-out per erasure request, one idempotent BE-006 job per store,
tracked to completion:

  [ ] Postgres: the document AND its Payload versions/drafts
      (`_<slug>_v` tables keep old copies) and related documents
      (afterDelete hook or explicit cascade; check relationship fields)
  [ ] S3/R2 uploads: deleting the Payload upload doc deletes the file;
      also remove derived image sizes and orphaned files from failed jobs
  [ ] Payload jobs queue: pending or failed jobs whose input holds the
      person's data
  [ ] Email provider: delete the contact; keep only a hashed suppression
      entry so we never mail them again (Art. 21 objection)
  [ ] Analytics: cookieless/aggregate tools hold nothing to delete
      (verify); tools with person profiles → call their deletion API
  [ ] Error tracker and logs: no personal data in logs by design
      (hash user IDs); log retention short and stated in the data map
  [ ] Payment provider: customer record deleted or restricted, except
      data we must keep under tax law (§ 147 AO, § 257 HGB) — mark it
      "restricted, retention until <date>", do not delete early
  [ ] Search index and caches: purge entries; revalidate cached pages
  [ ] Backups: cannot be edited. Policy: backups expire after a fixed
      period (stated in the data map). Keep a deletion log of erased
      user IDs; after any restore, re-apply it before the app goes live
  [ ] Third parties (Art. 19): tell each recipient listed on the map

Verify: re-query each store by the person's identifiers; nothing returns.

Audit record (keep, contains no personal data beyond a hash):
  request id, hashed user id, received at, done at, per-store result,
  data kept and the legal reason.

Deadline: one month from receipt (Art. 12(3)).
```

---

## Anti-patterns

### ❌ Forbidden

```markdown
- Store everything "in case it's needed"
- No deletion periods defined
- No DPA with providers
- Store IP addresses unencrypted
- User tracking without consent
- Personal data in logs
- Deleting the user row but leaving Payload versions, uploads or job inputs
- A data map with "unknown" cells or no processor column
- Promising erasure from backups that are never expired
- Calling name-stripped data "anonymised"
```

### ✅ Instead

```markdown
- Collect only necessary data
- Clear deletion periods + automatic deletion
- DPA with all providers
- Pseudonymization where possible
- Tracking only with consent
- Anonymized logs
- One data map, every cell filled, updated in the same ticket
- Erasure job that fans out to every store and writes an audit record
```

---

## Done evidence (receipt)

- `docs/security/data-map.md` exists; every row has all eight columns filled; the ticket's new fields or stores appear in it (diff).
- Erasure tickets: an integration test creates a user with an upload, a version, a queued job and a subscriber entry, runs the erasure, and asserts each store returns nothing; audit record path.
- Backup expiry period and restore re-apply step written in the data map or runbook.

---

## References

- `.quinsy-studio/knowledge-base/compliance_playbook.md` — compliance rules
- `.quinsy-studio/knowledge-base/backend_playbook.md` — database design
- `teams/08-platform-enterprise-engineering/skills/threat-modeling.md` (PE-005) — access paths per data class
- GDPR Art. 5, 12(3), 17, 19, 30; § 147 AO; § 257 HGB
- Source for sections 6–7: agency-agents `engineering/engineering-privacy-engineer.md` (MIT), rewritten for Payload, S3/R2 and Coolify
