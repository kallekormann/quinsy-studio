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
Legal basis: § 5 DDG (Digitale-Dienste-Gesetz, replaced § 5 TMG in May 2024).
For all commercial websites/services:
  1. Name/company of the operator; for companies the legal form and
     authorised representatives (e.g. Geschäftsführer)
  2. Address for service (ladungsfähige Anschrift; no P.O. box)
  3. Fast electronic contact: email address plus a second direct way
     (phone or a contact form that gets answered)
  4. Register court and number (Handelsregister, Vereinsregister, …), if registered
  5. VAT ID (§ 27a UStG) or business ID number, if one exists
  6. Supervisory authority, if the activity needs a licence
  7. Regulated professions: chamber, professional title, state that
     granted it, link to professional rules
  8. Journalistic-editorial content (blog, magazine, newsletter with
     editorial content): responsible person with name and address
     (§ 18(2) MStV, replaced § 55(2) RStV in November 2020)
  9. Consumer dispute resolution (§ 36 VSBG, applies to traders with a
     website or ToS): state whether we are willing or obliged to take part
     in proceedings before a consumer arbitration board. Traders with 10 or
     fewer employees on 31 December of the previous year are exempt from
     this statement. If we do commit to a board, name it with address and
     website regardless of size.
 10. Do NOT link the EU ODR platform: Regulation (EU) 2024/3228 repealed
     the ODR Regulation and the platform closed on 20 July 2025. Remove old
     ODR links and ODR wording from imprint and ToS.

Placement (§ 5(1) DDG: easily recognisable, directly reachable, always available):
  - Directly reachable (1 click from the footer, label "Impressum")
  - No login required
  - Not hidden in the ToS
  - Rendered from a Payload global, so address changes are one edit
```

Outdated citations to replace on sight (in imprint, privacy policy, ToS, cookie text):

| Old | Current |
|---|---|
| § 5 TMG, "Telemediengesetz" | § 5 DDG |
| § 55(2) RStV | § 18(2) MStV |
| § 25 TTDSG, "TTDSG" | § 25 TDDDG (renamed May 2024) |
| § 7, § 10 TMG (host liability) | Art. 4–6 DSA (Regulation (EU) 2022/2065) |
| "Online-Streitbeilegung … ec.europa.eu/consumers/odr" | remove (platform closed 20 July 2025) |
| Art. 14(1) ODR Regulation | remove |

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

Consumer subscriptions (B2C, concluded online):
  - Cancellation button (§ 312k BGB): a "Verträge hier kündigen" button,
    always reachable, leading to a confirmation page with a
    "jetzt kündigen" button; confirmation sent in text form
  - After the minimum term, consumer contracts may renew only into
    open-ended contracts cancellable with one month's notice (§ 309 Nr. 9 BGB)
```

### 3. Withdrawal right

```markdown
For consumers (B2C):
  - 14 days withdrawal right
  - No reason needed
  - Form: text (email, letter, form)
  - Start of period: receipt of goods; for services and digital content,
    conclusion of the contract
  - Exceptions: perishable goods; digital content only expires early if the
    consumer expressly agreed to start before the period ends, acknowledged
    losing the right, and got a confirmation (§ 356(5) BGB)
  - Withdrawal function: Directive (EU) 2023/2673 requires an online
    withdrawal button for contracts concluded online, applying from
    19 June 2026. Implement it next to the cancellation button and check the
    German implementing provision in the BGB before shipping.

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
- Citing TMG, RStV or TTDSG
- Linking the closed EU ODR platform
- Missing § 36 VSBG statement (when not exempt)
- No withdrawal right (B2C); no cancellation button on consumer subscriptions
- Disclaimer too broad
- Imprint only as PDF (instead of an HTML page)
```

### ✅ Instead

```markdown
- Directly linked in the footer
- All § 5 DDG information present; § 18(2) MStV person named if editorial
- § 36 VSBG statement or documented exemption
- 14 days withdrawal right correctly implemented
- Disclaimer legally reviewed
- As its own HTML page
```

---

## References

- `.quinsy-studio/knowledge-base/compliance_playbook.md` — compliance rules
- `.quinsy-studio/process/gates.md` — legal check in gate 5
- § 5 DDG; § 18(2) MStV; § 36 VSBG; §§ 312k, 356, 309 BGB; Regulation (EU) 2024/3228; Directive (EU) 2023/2673
- Check: `rg -n "TMG|RStV|TTDSG|ec.europa.eu/consumers/odr"` over product content and Payload seed data returns nothing
- Marketing claims on legal pages and checkout: [marketing-law.md](../../../knowledge-base/skill-extensions/marketing-law.md)

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
