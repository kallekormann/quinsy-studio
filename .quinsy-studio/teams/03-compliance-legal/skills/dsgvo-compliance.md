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
  - Ticket words: DPIA, data protection impact assessment, data breach, Art. 33
pairs_with: [CL-002, CL-004, PE-005, PE-007]
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

Legal basis: § 25 TDDDG for any storage on or reading from the device
(cookies, localStorage, pixels, fingerprinting); DSGVO for the processing
that follows. Details: CL-002.

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
  - Objection (Art. 21): object to processing; absolute for direct marketing
  - Automated decisions (Art. 22): decisions with legal or similarly
    significant effect based solely on automated processing only if
    necessary for a contract, allowed by law, or with explicit consent;
    then a human review on request

Implementation:
  - Self-service portal for access/export/erasure
  - Response time: one month from receipt (Art. 12(3)); extendable by two
    further months for complex or many requests, with notice and reasons
    within the first month
  - Erasure reaches every store: see CL-004 "erase everywhere"
```

### 6. Third-country transfer

```markdown
When data is processed outside the EU:
  1. Check whether an adequacy decision exists
  2. If not: standard contractual clauses (SCC)
  3. Document TOMs (technical and organizational measures)
  4. Inform the user

Priority: EU servers! Third country only for compelling reasons.
US processors: check whether the recipient is certified under the
EU-US Data Privacy Framework (adequacy decision of 10 July 2023);
otherwise SCC + transfer impact assessment.
```

### 7. DPIA triggers (Art. 35 GDPR)

A data protection impact assessment is required **before** processing that
is likely to result in a high risk. Check at gate 1 and in every
architecture-phase ticket that adds a data class or purpose.

```markdown
Always required (Art. 35(3)):
  a) Systematic, extensive evaluation of personal aspects by automated
     processing (incl. profiling) that leads to decisions with legal or
     similarly significant effect
  b) Large-scale processing of special categories (Art. 9: health,
     biometric, genetic, religion, ethnicity, sexual orientation, …) or
     criminal-offence data (Art. 10)
  c) Systematic large-scale monitoring of publicly accessible areas

Also check the German list: the DSK "Muss-Liste" of processing
operations that require a DPIA (published by the Datenschutzkonferenz),
e.g. scoring, tracking of location or behaviour across sites or devices,
large-scale employee monitoring.

Screening criteria (EDPB-endorsed WP248 rev.01, nine criteria):
  1. Evaluation or scoring (incl. profiling, prediction)
  2. Automated decision with legal or similar significant effect
  3. Systematic monitoring
  4. Sensitive or highly personal data
  5. Large scale
  6. Matching or combining datasets beyond users' expectations
  7. Vulnerable data subjects (children, employees, patients)
  8. Innovative use of technology (e.g. new AI features on personal data)
  9. Processing that blocks a right or access to a service or contract
  Two or more criteria met → do a DPIA, or record why not.

Output: `docs/security/dpia-<topic>.md`
  - Description of processing and purposes (link data map rows, CL-004)
  - Necessity and proportionality
  - Risks to data subjects (described, not invented scores)
  - Measures: technical, organisational, contractual
  - Residual risk and sign-off by the human
  - If high residual risk remains: prior consultation of the supervisory
    authority (Art. 36) before launch — HITL stop

Screening result (DPIA required / not required + criteria counted) goes
into the architecture doc of the ticket.
```

### 8. Personal data breach: scoring and the Art. 33/34 decision

Operational response (contain, preserve evidence, timeline, comms) lives in
PE-007 [incident-response.md](../../08-platform-enterprise-engineering/skills/incident-response.md).
This section owns the legal decision.

```markdown
Clock: 72 hours from becoming aware of a personal data breach
(Art. 33(1)). Awareness = reasonable certainty that a security incident
compromised personal data. A processor tells us without undue delay
(Art. 33(2)); our DPAs require it.

Breach types: confidentiality (disclosed or accessed), integrity
(altered), availability (lost or unreachable, incl. ransomware).

Severity scoring (ENISA methodology, 2013):
  Severity = DPC × EI + CB
  - DPC (data processing context): base score by data type —
    simple 1, behavioural 2, financial 3, sensitive 4 — then adjusted
    up or down for context as the method describes
  - EI (ease of identification): 0.25 negligible, 0.5 limited,
    0.75 significant, 1 maximum
  - CB (circumstances of breach): add up to +0.5 each for loss of
    confidentiality, integrity and availability, +0.5 for malicious intent
  Result: < 2 low · 2 to < 3 medium · 3 to < 4 high · ≥ 4 very high
  Record each input with its reason in the breach record.

Decision:
  1. Unlikely to result in a risk to rights and freedoms
     → no notification; document internally (Art. 33(5)).
  2. Risk (anything not clearly "unlikely")
     → notify the competent supervisory authority within 72 hours
       (Art. 33(1)). Late notice states the reasons for the delay.
       Content (Art. 33(3)): nature, categories and approximate numbers
       of people and records, contact point, likely consequences,
       measures taken or proposed. Phased notice is allowed (Art. 33(4)).
  3. High risk (ENISA high or very high, or special categories,
     credentials, financial data in the clear)
     → also inform affected people without undue delay in plain language
       (Art. 34), unless: data was encrypted and the key is safe; later
       measures removed the high risk; or individual notice would take
       disproportionate effort → public communication instead (Art. 34(3)).
  Human decides at each step (HITL); the agent drafts the record and notices.

Breach record (always, Art. 33(5)): `docs/security/breaches/<YYYY-MM-DD>-<slug>.md`
  facts, timeline (aware at …), affected data and people, score inputs,
  decision and reason, notices sent with timestamps, remediation tickets.
Guidance: EDPB Guidelines 9/2022 (notification) and 01/2021 (examples).
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
- Launching a high-risk feature and doing the DPIA afterwards
- "We'll decide on notification after we know everything" past 72 hours
- Breach risk scores without recorded inputs
- Citing TTDSG instead of TDDDG
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
- DPIA screening recorded per architecture ticket
- Breach record for every breach, notified or not
```

---

## Done evidence (receipt)

- Gate 1 / architecture tickets: DPIA screening line (criteria counted, result) in the architecture doc; `docs/security/dpia-<topic>.md` when required.
- Breach tickets: breach record path with score inputs, decision, and timestamps for awareness and each notice.
- Privacy-policy tickets: `rg -n "TTDSG|TMG"` over the policy returns nothing.

---

## References

- `.quinsy-studio/knowledge-base/compliance_playbook.md` — compliance rules
- `.quinsy-studio/process/gates.md` — GDPR in gate 5
- `./studio gate <project> --gdpr` — GDPR check
- GDPR Art. 12, 21, 22, 33–36; TDDDG § 25; WP248 rev.01; DSK DPIA Muss-Liste; ENISA "Recommendations for a methodology of the assessment of severity of personal data breaches" (2013); EDPB Guidelines 9/2022 and 01/2021
- Source for sections 7–8: agency-agents `specialized/data-privacy-officer.md` (MIT), US frames and invented volume thresholds removed

---

## Studio skill extension

**Load for codebase audits and global privacy (GDPR, CCPA/CPRA, FTC, EU AI Act):**  
[knowledge-base/skill-extensions/privacy-legal-compliance.md](../../../knowledge-base/skill-extensions/privacy-legal-compliance.md)

**Adds to CL-001:**
- Click-wrap / explicit assent on signup and checkout (no browse-wrap)
- Consent audit fields on user schema (`tos_accepted_at`, version strings, hashed IP)
- Right-to-erasure cascade checks on delete endpoints
- Third-party exfiltration scan (`fetch`/`axios` to analytics without consent)
- Footer disclosure requirements (Privacy, ToS, Do Not Sell)

**Marketing, newsletters, reviews, referral, price display:** [marketing-law.md](../../../knowledge-base/skill-extensions/marketing-law.md) (UWG §§ 5, 5a, 6, 7; § 25 TDDDG; PAngV § 11).

**Full multi-topic audit:** use [compliance-orchestrator.md](../../../knowledge-base/skill-extensions/compliance-orchestrator.md) (routes to CL-001/002/003 — not a separate skill ID).
