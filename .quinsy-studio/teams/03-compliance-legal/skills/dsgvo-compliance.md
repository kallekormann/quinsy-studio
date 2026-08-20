# Skill: GDPR Compliance

> General Data Protection Regulation, records of processing, data subject rights, privacy policy

## Metadata

```
skill_id: CL-001
name: GDPR Compliance
team: 03-compliance-legal
lead_role: Legal & Privacy Officer
support_roles: [Backend Security Engineer]
phases: [0, 1, 2, 3, 4, 5, 6]
activation_triggers:
  - Ticket contains "GDPR", "data protection", "privacy"
  - Every project (mandatory check in phase 1)
  - Phase 5: GDPR audit
  - External service providers are integrated
```

---

## Behavior rules

### 1. Records of processing (Art. 30 GDPR)

```markdown
Mandatory entries per processing activity:
  1. Name of the controller
  2. Purpose of the processing
  3. Category of data subjects
  4. Category of personal data
  5. Category of recipients
  6. Third-country transfer (yes/no + safeguards)
  7. Deletion periods
  8. Technical and organizational measures
```

### 2. Privacy policy

```markdown
Mandatory content:
  1. Controller (name, address, email)
  2. Data protection officer (if any)
  3. Types of data collected
  4. Purposes of processing
  5. Legal bases (Art. 6 GDPR)
  6. Retention / deletion periods
  7. Data subject rights (access, erasure, rectification)
  8. Right to complain (supervisory authority)
  9. Server location
  10. Contact details

Update: at least annually or on changes
```

### 3. Cookie banner

```markdown
Categories:
  - Necessary (always active, no consent needed)
  - Analytics (opt-in!)
  - Marketing (opt-in!)

Rules:
  - Opt-in (not opt-out!)
  - Granular selection per category
  - "Accept all" AND "Save selection"
  - Withdrawal possible at any time (link in the footer)
  - No trick cookies ("continue = accept")
  - Cookie duration documented
  - Third-party list current
```

### 4. Legal bases

```markdown
Art. 6(1) GDPR:
  a) Consent              → cookie banner, newsletter
  b) Contract performance → account creation, order
  c) Legal obligation     → tax retention
  d) Vital interests      → emergencies
  e) Public interest      → (rare)
  f) Legitimate interest  → analytics (with balancing test!)

Every data field must have a documented legal basis!
```

### 5. Data subject rights

```markdown
User rights:
  - Access (Art. 15): which data do we have?
  - Rectification (Art. 16): correct data
  - Erasure (Art. 17): "right to be forgotten"
  - Restriction (Art. 18): restrict processing
  - Data portability (Art. 20): data as export
  - Objection (Art. 21): object to processing
  - Automated decisions (Art. 22): none without consent

Implementation:
  - Self-service portal for access/export/erasure
  - Response time: 30 days (max.)
```

### 6. Third-country transfer

```markdown
When data is processed outside the EU:
  1. Check whether an adequacy decision exists
  2. If not: standard contractual clauses (SCC)
  3. Document TOMs (technical and organizational measures)
  4. Inform the user

Priority: EU servers! Third country only for compelling reasons.
```

---

## Anti-patterns

### ❌ Forbidden

```markdown
- Tracking without consent
- No cookie banner
- Opt-out instead of opt-in
- No records of processing
- Third-country transfer without SCC
- Storing data longer than necessary
- No self-service portal for data subject rights
```

### ✅ Instead

```markdown
- Track only with consent
- Granular cookie banner
- Opt-in as standard
- Complete records of processing
- Prefer EU servers
- Define and implement retention periods
- Self-service for access/export/erasure
```

---

## References

- `.quinsy-studio/knowledge-base/compliance_playbook.md` — compliance rules
- `.quinsy-studio/process/gates.md` — GDPR in gate 5
- `./studio gate <project> --gdpr` — GDPR check
