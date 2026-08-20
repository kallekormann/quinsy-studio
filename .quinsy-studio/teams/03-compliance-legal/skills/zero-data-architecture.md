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
  - Hosting (Vercel, AWS, Supabase)
  - Analytics (Plausible, PostHog)
  - Email (SendGrid, Resend)
  - Payment (Stripe)
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
```

### ✅ Instead

```markdown
- Collect only necessary data
- Clear deletion periods + automatic deletion
- DPA with all providers
- Pseudonymization where possible
- Tracking only with consent
- Anonymized logs
```

---

## References

- `.quinsy-studio/knowledge-base/compliance_playbook.md` — compliance rules
- `.quinsy-studio/knowledge-base/backend_playbook.md` — database design
