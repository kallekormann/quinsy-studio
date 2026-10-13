# Skill: SaaS Terms of Service (ToS) Architect & Writer
**ID:** SKILL-LEG-002 
**Version:** 2026.1 
**Target:** Terms of Service, EULA, Subscription Agreements, Billing Logic, 3rd Party Sub-processor Mapping 
**Environment:** Cursor IDE / Codebase Context 

## Objective
Analyze the SaaS infrastructure, third-party integrations, and pricing structures within the codebase to draft, review, and maintain legally resilient, binding Terms of Service (ToS) aligned with global B2B/B2C regulations.

---

## 1. Required Legal Frameworks & Reference Anchors
When drafting or auditing clauses, the agent MUST strictly enforce compliance with:
*   **EU Digital Services & Consumer Law:** Directive (EU) 2019/770 (SaaS updates, conformity, and termination rights).
*   **US Commercial Law Standards:** Strict enforcement of "Disclaimer of Warranties" and "Limitation of Liability" templates utilizing standard conspicuous drafting (ALL-CAPS constraints).
*   **German AGB-Recht (§§ 305-310 BGB):** Strict prohibition of unfair surprise clauses, governing automated renewals, and rigid boundaries on liability limitations for B2B/B2C hybrid SaaS.

---

## 2. Context-Driven Drafting Requirements

The agent will map the dynamic properties of the codebase directly into the legal text across these pillars:

### A. Monetization, Tiers & Billing Mechanics
*   **Rule:** The legal payment terms must precisely reflect the technical billing implementation.
*   **Code Discovery Path:** Scan billing routers (`/api/v1/billing/*`), Stripe webhook handlers, subscription schemas, and pricing tier configurations.
*   **Drafting Directive:**
    *   For **Usage-Based Pricing**: Define exact metering definitions, calculation points, and consequences of late payments or card failures (suspension workflows).
    *   For **Seat/Tier Models**: Define the rules for "Pro-Rata" calculations during mid-cycle upgrades/downgrades and explicit non-refundability rules.

### B. Third-Party Platforms & Service Availability (SLA)
*   **Rule:** The SaaS cannot promise higher availability or lower liability than its underlying critical infrastructure.
*   **Code Discovery Path:** Scan `package.json`, environment names in `env.schema.json`, and API clients connecting to external platforms (Coolify, Payload, Cloudflare R2, Stripe, Lemon Squeezy, Resend, OpenAI).
*   **Drafting Directive:** Build robust *Service Availability* and *Force Majeure* clauses. Explicitly disclaim direct liability for data loss or service degradation originating from upstream infrastructure dependencies found in the code.

### C. Artificial Intelligence & Data Processing Governance (If applicable)
*   **Rule:** If the codebase sends data to LLM APIs, input/output ownership and IP indemnity must be explicitly allocated.
*   **Code Discovery Path:** Scan for OpenAI, Anthropic, LangChain, or custom vector database connections.
*   **Drafting Directive:** Inject precise *Acceptable Use Policy (AUP)* restrictions preventing prompt injection manipulation, clarify that the User owns the generated "Output" but holds the SaaS harmless against intellectual property claims stemming from AI generations.

### D. User Content & Intellectual Property (IP) License
*   **Rule:** The SaaS requires a limited, non-exclusive license to host, process, and display user data solely to provide the service.
*   **Code Discovery Path:** Scan file-upload components (S3 storage integrations, multi-tenant databases).
*   **Drafting Directive:** Draft a strict IP clause stating the platform retains all rights to the software, schemas, and UI, while the user retains rights to their uploaded data but grants the platform a necessary operational license.

---

## 3. Operational Instructions for Cursor AI

When instructed to **"Draft or review the Terms of Service based on this codebase"**, execute these steps:
1.  **Architecture Scan:** Run a sweep of dependencies (`package.json`), payment webhooks, and routing configurations to determine the exact technical profile.
2.  **Gap Analysis:** Compare existing legal text against the discovered technical reality.
3.  **Reporting & Execution Output:** Structure the delivery in two parts:

### 📑 Tech-to-Legal Alignment Map

| Code Asset / Pattern Found | Legal Risk Area | Required ToS Clause | Discrepancy / Action |
| :--- | :--- | :--- | :--- |
| *e.g., Stripe tiered webhook* | *Payment & Termination* | *Subscription Billing & Upgrades* | *Draft clause covering automatic renewal and pro-rata tier adjustments.* |
| *e.g., @openai/api client* | *IP & Liability* | *AI Sub-Processor & Output Disclaimer* | *Generate an AI-specific Acceptable Use Policy clause.* |

4.  **Text Generation:** Output the fully drafted, production-ready section of the Terms of Service using clear, professional legal English (or German, based on instruction), complete with placeholders for variables like `[Company Name]` and `[Jurisdiction]`.
