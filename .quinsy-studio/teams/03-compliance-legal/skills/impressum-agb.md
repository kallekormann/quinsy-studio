# Skill: Imprint & ToS

> Imprint, terms of service, disclaimers, EU dispute resolution

## Metadata

```
skill_id: CL-003
name: Imprint & ToS
team: 03-compliance-legal
lead_role: Legal & Privacy Officer
support_roles: []
phases: [3, 4, 5]
activation_triggers:
  - Ticket contains "imprint", "terms of service", "ToS"
  - Phase 3: legal pages are planned
  - Phase 4: legal pages are implemented
  - Phase 5: legal check in the QA gate
```

---

## Behavior rules

### 1. Imprint (mandatory information)

```markdown
For all websites/services:
  1. Name/company of the operator
  2. Full address
  3. Email contact
  4. Phone (if available)
  5. VAT ID (if available)
  6. Responsible for content (§ 55(2) RStV)
  7. EU dispute resolution (link to the ODR platform)

Placement:
  - Directly reachable (1 click from the footer)
  - No login required
  - Not hidden in the ToS
```

### 2. ToS (terms of service)

```markdown
Mandatory content:
  1. Scope of application
  2. Subject of the contract
  3. Registration / account
  4. Prices and payment
  5. Withdrawal right (14 days for consumers)
  6. Warranty
  7. Disclaimer
  8. Severability clause
  9. Place of jurisdiction
  10. Applicable law (DE or AT)

For SaaS:
  - Notice periods
  - SLA (service level agreement)
  - Data export on termination
  - Features and changes
```

### 3. Withdrawal right

```markdown
For consumers (B2C):
  - 14 days withdrawal right
  - No reason needed
  - Form: text (email, letter, form)
  - Start of period: receipt of goods/service
  - Exceptions: perishable goods, digital content (after download)

For B2B:
  - No statutory withdrawal right
  - Can be freely agreed in the ToS
```

### 4. Disclaimer

```markdown
Typical wording:
  "We assume no liability for the content of external links.
   Only the operators of the linked pages are responsible
   for their content."

For SaaS:
  - Limit liability to intent and gross negligence
  - Define a liability cap
  - Exclude indirect damages
```

---

## Anti-patterns

### ❌ Forbidden

```markdown
- Imprint not reachable
- Incomplete mandatory information
- Missing EU dispute resolution
- No withdrawal right (B2C)
- Disclaimer too broad
- Imprint only as PDF (instead of an HTML page)
```

### ✅ Instead

```markdown
- Directly linked in the footer
- All mandatory information present
- EU dispute resolution link correct
- 14 days withdrawal right correctly implemented
- Disclaimer legally reviewed
- As its own HTML page
```

---

## References

- `.quinsy-studio/knowledge-base/compliance_playbook.md` — compliance rules
- `.quinsy-studio/process/gates.md` — legal check in gate 5

---

## Studio skill extension

**Load when drafting or auditing ToS/EULA/subscription terms from the codebase:**  
[knowledge-base/skill-extensions/tos-architect.md](../../../knowledge-base/skill-extensions/tos-architect.md)

**Adds to CL-003:**
- Map billing webhooks and tier config → payment/renewal clauses
- Map `package.json` / sub-processors → SLA and force majeure
- Map LLM integrations → AI acceptable-use and output IP clauses
- Map file-upload flows → user content license grant
- EU consumer law + US disclaimer/limitation templates
