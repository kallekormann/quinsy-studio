# Skill: SaaS Legal & Privacy Compliance Auditor (Global Markets)
**ID:** SKILL-LEG-001 
**Version:** 2026.1 
**Target:** Global B2B/B2C SaaS (GDPR, CCPA/CPRA, FTC Section 5, EU AI Act) 
**Environment:** Cursor IDE / Codebase Context 

## Objective
Analyze the repository's Frontend code, UI layouts, Backend logic, Database schemas, and Legal documents to ensure strict adherence to global privacy laws and contract formation standards.

---

## 1. Reference Authorities & Live Frameworks
When validating compliance or generating fixes, the agent MUST cross-reference and align with these global standards:
*   **GDPR (EU/Global):** [gdpr-info.eu](https://gdpr-info.eu) (Strict opt-in, Data Minimization, Right to be Forgotten).
*   **US State Laws (CCPA/CPRA):** [cppa.ca.gov](https://ca.gov) (Opt-out mechanisms, "Do Not Sell/Share My Info", B2B exceptions management).
*   **FTC Act Section 5 (US):** [ftc.gov](https://ftc.gov) (Deceptive practices prevention; engineering reality must match legal policy promises).
*   **EU AI Act (Global Impact):** [artificialintelligenceact.eu](https://artificialintelligenceact.eu) (Transparency tags if the SaaS processes data using LLMs/Machine Learning).

---

## 2. Frontend Execution Rules (UI/UX & Client-Side)
The agent will scan Frontend components (React, Vue, Next.js, HTML, etc.) for the following patterns:

### A. Contract Formation & Assent (Click-wrap)
*   **Rule:** Browse-wrap (implicit consent via usage) is forbidden. Sign-up and checkout forms must require explicit assent.
*   **Code Search Pattern:** Look for `<form>` components handling `signup`, `register`, or `checkout`.
*   **Requirement:** Ensure a mandatory checkbox exists. The "Submit" button must be disabled until checked, OR the submission function must validate the checkbox state.
*   **Text Standard:** *"I agree to the [Terms of Service](url) and [Privacy Policy](url)."*

### B. Cookie & Tracking Consent
*   **Rule:** Zero-cookie loading prior to consent for EU/UK users.
*   **Code Search Pattern:** Check `index.html`, `_document.js`, or root layouts for tracking pixels (Google Analytics, Meta Pixel, PostHog, Mixpanel).
*   **Requirement:** These scripts must be wrapped in a conditional block controlled by a consent management state (e.g., `if (cookiesAccepted)`). Pre-ticked consent checkboxes are critical failures.

### C. Public Disclosures & Footers
*   **Rule:** Ubiquitous link presence.
*   **Code Search Pattern:** Scan layout/footer components.
*   **Requirement:** Links to `Privacy Policy`, `Terms of Service`, and a `"Do Not Sell/Share My Personal Information"` toggle (or unified Cookie Settings button) must be visible globally.

---

## 3. Backend & API Execution Rules (Server-Side)
The agent will scan Backend routes, controllers, schemas, and config files for the following patterns:

### A. Consent Logging & Auditing
*   **Rule:** Legal teams must be able to prove *who* agreed to *what* version, and *when*.
*   **Code Search Pattern:** Scan `User` database schemas, Prisma schemas, Mongoose models, or SQL migrations.
*   **Requirement:** The user table/collection MUST contain fields for:
    *   `tos_accepted_at`: Timestamp
    *   `tos_version_accepted`: String/SemVer
    *   `privacy_policy_version_accepted`: String/SemVer
    *   `consent_ip_address`: String (masked/hashed where appropriate for privacy minimization)

### B. Data Minimization & PII Handling
*   **Rule:** Storage of unencrypted PII (Personally Identifiable Information) or unnecessary business data is forbidden.
*   **Code Search Pattern:** Check API endpoints handling data ingestion (`/api/v1/profiles`, `/api/v1/organizations`).
*   **Requirement:** Validate that data is encrypted at rest. Look for encryption utilities (e.g., AES-256 wrappers) on sensitive fields like phone numbers, billing addresses, or company tax IDs.

### C. Right to be Forgotten (Data Deletion)
*   **Rule:** Users must have a clean automated or triaged path to delete all data across both consumer and business accounts.
*   **Code Search Pattern:** Scan delete user endpoints (`DELETE /api/v1/user` or `/api/v1/organization`).
*   **Requirement:** Check if deletion cascades to sub-tables (logs, third-party syncs) or securely anonymizes the records. Soft deletes must completely hide data from operational access and have a hard-delete TTL (Time-To-Live).

### D. Third-Party Data Exfiltration
*   **Rule:** Webhooks and external APIs must not leak PII without logging.
*   **Code Search Pattern:** Search for `fetch(`, `axios.`, or external SDK triggers sending payload data to third parties.
*   **Requirement:** Ensure no raw user or business emails/names are appended to tracking URLs or sent to unauthorized analytical endpoints.

---

## 4. Operational Instructions for Cursor AI

When I ask you to **"Audit this feature/code for compliance"**, follow this exact workflow:
1.  **Identify Scope:** Determine if the code touches Frontend (UI/Consent), Backend (Processing/Storage), or Legal Docs.
2.  **Run Pattern Matching:** Use the rules in Sections 2 & 3 to find discrepancies.
3.  **Output Format:** Present findings in a structured table:
    *   **File/Component:** Location of code
    *   **Risk Level:** [CRITICAL / WARNING / COMPLIANT]
    *   **Violation:** Specific global rule violated
    *   **Remediation:** Exact code fix required to achieve compliance.