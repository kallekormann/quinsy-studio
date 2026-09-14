# Compliance Playbook

> Zero-data architecture, GDPR, cookie consent — the global compliance standards.

## Core principle

```
Compliance is not a feature — it is an obligation.
Data minimization is the default.
```

---

## Zero-data architecture

### Principle

```
Collect only what you need.
Delete what you no longer need.
Protect what you must keep.
```

### Implementation

| Principle | Measure |
|-----------|---------|
| **Data minimization** | collect only essential data |
| **Purpose limitation** | use data only for the defined purpose |
| **Storage limitation** | automatic deletion periods |
| **Pseudonymization** | IDs instead of real names |
| **Encryption** | at rest and in transit |

### Technical measures

```typescript
// 1. Pseudonymization
const pseudonym = crypto.createHash('sha256').update(userId).digest('hex');

// 2. Automatic deletion
await db.query(`
  DELETE FROM analytics 
  WHERE created_at < NOW() - INTERVAL '90 days'
`);

// 3. Encryption
const encrypted = crypto.createCipheriv('aes-256-gcm', key, iv);
```

---

## GDPR

### Data subject rights

| Right | Description | Implementation |
|-------|-------------|----------------|
| **Access** | which data is stored? | API endpoint: `GET /me/data` |
| **Rectification** | correct data | API endpoint: `PATCH /me` |
| **Erasure** | delete data ("right to be forgotten") | API endpoint: `DELETE /me` |
| **Data portability** | data as export | API endpoint: `GET /me/export` |
| **Objection** | against processing | checkbox in settings |
| **Consent** | opt-in for tracking | cookie banner |

### Records of processing

```markdown
# Records of processing

| Processing | Purpose | Legal basis | Retention |
|------------|---------|-------------|-----------|
| User account | service delivery | Art. 6(1)(b) GDPR | until deletion |
| Analytics | product improvement | Art. 6(1)(a) GDPR | 90 days |
| Newsletter | marketing | Art. 6(1)(a) GDPR | until unsubscribe |
```

---

## Cookie banner

### Requirements

1. **Opt-in** (not opt-out!)
2. **Granular selection** (necessary, analytics, marketing)
3. **Withdrawal** possible at any time
4. **No tricks** (e.g. "continue = accept")
5. **Cookie duration** documented
6. **Third-party list** current

### Implementation

```typescript
// cookie categories
const cookieCategories = {
  necessary: {
    name: 'Necessary',
    description: 'Essential for using the site',
    required: true, // cannot be disabled
  },
  analytics: {
    name: 'Analytics',
    description: 'Help us improve the site',
    required: false,
  },
  marketing: {
    name: 'Marketing',
    description: 'Personalized advertising',
    required: false,
  },
};

// consent management
function setConsent(category: keyof typeof cookieCategories, value: boolean) {
  localStorage.setItem(`consent_${category}`, String(value));
}

function hasConsent(category: keyof typeof cookieCategories): boolean {
  if (cookieCategories[category].required) return true;
  return localStorage.getItem(`consent_${category}`) === 'true';
}
```

---

## Imprint

### Mandatory information

```markdown
# Imprint

## Responsible for the content
[Name/Company]
[Street, number]
[Postal code, city]
[Email]
[Phone] (optional)

## VAT ID (if available)
[Tax number or VAT ID]

## Dispute resolution
The European Commission provides a platform for online dispute resolution (OS): https://ec.europa.eu/consumers/odr/

We are not willing or obliged to participate in dispute resolution proceedings before a consumer arbitration board.

## Disclaimer
[Content- and legally]
```

---

## Privacy policy

### Structure

```markdown
# Privacy Policy

## 1. Controller
[Name, address, email]

## 2. Data protection officer (if any)
[Name, email]

## 3. Types of data collected
- Account data (email, name)
- Usage behavior (analytics)
- Technical data (IP, browser)

## 4. Purposes of processing
- Service delivery
- Product improvement
- Marketing (with consent)

## 5. Legal bases
- Art. 6(1)(a) GDPR: consent
- Art. 6(1)(b) GDPR: contract initiation
- Art. 6(1)(f) GDPR: legitimate interest

## 6. Retention periods
- Account data: until deletion
- Analytics: 90 days
- Logs: 30 days

## 7. Data subject rights
- Access (Art. 15 GDPR)
- Rectification (Art. 16 GDPR)
- Erasure (Art. 17 GDPR)
- Data portability (Art. 20 GDPR)
- Objection (Art. 21 GDPR)

## 8. Right to complain
[Supervisory authority]

## 9. Server location
[EU/indication]

## 10. Cookies
[cookie list]
```

---

## AVV / DPA

### Checklist for service providers

- [ ] Data processing agreement (DPA) present
- [ ] Server location in the EU
- [ ] Encryption at rest and in transit
- [ ] Sub-processors documented
- [ ] Deletion concept defined
- [ ] Security measures documented

---

## Gate integration

```bash
# GDPR check
./studio gate <project> --gdpr

# cookie banner check
./studio gate <project> --cookies

# imprint check
./studio gate <project> --imprint
```

---

## Spec-fail (public surfaces)

| Fail | Why |
|------|------|
| Public site ships without imprint / privacy links in chrome | Legal HITL is not optional on public URLs (CL-003) |
| Non-essential cookies or pixels before consent | Cookie banner is a gate, not a footer note (CL-002) |
| Collecting account data with no purpose + retention | GDPR minimization (CL-001) |
| Dark-pattern “accept all” only | Must be able to reject non-essential |

Contracts, GDPR exceptions, and production personal-data deletes stay **HITL**. Do not invent a Team 10-style book stack here.

---

## References

- `.quinsy-studio/teams/03-compliance-legal/` — compliance team
- `.quinsy-studio/process/human-in-the-loop.md` — HITL for compliance decisions
- `.quinsy-studio/process/gates.md` — gate definitions
