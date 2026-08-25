# Skill: Comprehensive Global Compliance & Tracking Engine
**ID:** SKILL-LEG-ALL-001 
**Version:** 2026.3 
**Target:** Frontend Consent UIs, Server-side Tracking, Affiliate Link Routing, Privacy/ToS Architectures, Analytics Integration 
**Environment:** Cursor IDE / Codebase Context + Web Search 

## Objective
Act as a hybrid Legal-Tech engineer to analyze, draft, and audit application code. This skill ensures strict alignment with global data privacy (GDPR, CCPA/CPRA), ePrivacy cookie laws, advertising disclosure mandates (FTC, UWG), and search engine compliance frameworks by leveraging live web research against authoritative sources.

---

## 1. Dynamic Knowledge & Research Anchors (Live Web Verification)
When instructed to "verify compliance", "audit tracking logic", or "research legal updates", the agent MUST actively utilize its web search tools to cross-reference the codebase against the following authoritative URLs:

### A. Data Privacy & Consent Rules (GDPR & ePrivacy)
*   **Source:** [gdpr-info.eu](https://gdpr-info.eu)
    *   *Application:* Cross-reference Article 4 (Consent definition), Article 7 (Conditions for consent), and Article 17 (Right to be Forgotten / Erasure).
*   **Source:** [edpb.europa.eu - Guidelines on Consent](https://europa.eu)
    *   *Application:* Check for recent EDPB updates regarding Cookie Banner design, Cookie Walls, and Dark Patterns (Deceptive UI design).
*   **Source:** [cppa.ca.gov - CCPA/CPRA Regulations](https://ca.gov)
    *   *Application:* Audit mandatory requirements for "Do Not Sell/Share My Personal Information" triggers and Global Privacy Control (GPC) support.

### B. Affiliate, Marketing & Disclosures (FTC & UWG)
*   **Source:** [ftc.gov - Endorsement Guides](https://ftc.gov)
    *   *Application:* Verify that affiliate disclosures meet the updated "clear and conspicuous" layout standards (placement, proximity, and visibility).
*   **Source:** [gesetze-im-internet.de - § 5a UWG](https://gesetze-im-internet.de)
    *   *Application:* Ensure commercial intents of affiliate tracking links are cleanly disclosed to DACH consumers to avoid legal warnings (Abmahnungen).

### C. Search Engine Validation & Browser Storage
*   **Source:** [://google.com - Link Fundamentals](https://://google.com/search/docs/fundamentals/creators-links)
    *   *Application:* Verify exact syntax and rules for `rel="sponsored"`, `rel="nofollow"`, and dynamic link decoration to prevent SEO indexing penalties.
*   **Source:** [developer.mozilla.org - Web Privacy Guide](https://mozilla.org)
    *   *Application:* Monitor changes in browser storage sandboxing (e.g., partitioned storage, client-side tracking cookie restrictions).

---

## 2. Integrated Code Review & Verification Protocols

### Protocol A: The Data & Cookie Ingestion Layer (Privacy & Cookies)
*   **Rule:** Non-essential tracking scripts (Google Analytics, Meta Pixel, PostHog, Mixpanel) must remain completely un-hydrated in memory and blocked from setting cookies until the global state validates an explicit user opt-in.
*   **Code Search Focus:** Root layouts, HTML templates (`index.html`, `_document.tsx`), or telemetry initialization modules.
*   **Requirement:** Enforce state-locked conditional mounting. Reject any tracking script that auto-initializes on DOM load without an active user consent check.

### Protocol B: The Affiliate & Link Redirection Layer (Affiliate Tracking)
*   **Rule:** Outbound commercial tracking must be transparent to search crawlers and secure for user experience without triggering malicious-redirect or ad-blocking flags.
*   **Code Search Focus:** Outbound links, anchor tag wrappers (`<a>`), dynamic markdown renderers, and server-side redirect APIs (`/go/*`, `/out/*`).
*   **Requirement:**
    *   All external commercial URLs must enforce `target="_blank" rel="noopener noreferrer sponsored"`.
    *   Internal redirection APIs handling affiliate jumps must serve an HTTP `302 Found` (temporary) status code to prevent permanent browser caching of tracking tokens.

### Protocol C: UI Visual Equity & Messaging (UX Delight vs. Dark Patterns)
*   **Rule:** Privacy interfaces and affiliate disclosures must maintain high readability and avoid deceptive design tactics.
*   **Code Search Focus:** Cookie consent banners, modal configuration settings, sign-up forms.
*   **Requirement:**
    *   The "Decline All" or "Manage Preferences" action must match the "Accept All" button in typography, sizing, and visual prominence.
    *   Affiliate disclosure microcopy must be placed above the fold or immediately adjacent to the first commercial interaction point.

### Protocol D: Data Retention & Audit Trails (Backend Compliance)
*   **Rule:** Database architectures must log tracking consent configurations without leaking unencrypted Personal Identifiable Information (PII).
*   **Code Search Focus:** Database migration tables, user/workspace schemas (Prisma, Mongoose, SQL).
*   **Requirement:** Ensure registration handlers log verifiable, time-stamped contract metadata containing: `consent_timestamp`, `tos_version_accepted`, `privacy_version_accepted`, and granular sub-flags (`analytics_allowed: boolean`, `marketing_allowed: boolean`).

---

## 3. Operational Workflow & Execution Instructions for Cursor

When instructed to **"Run a full structural compliance audit on this route/component"**, execute these steps:

1.  **Live Research (Optional but Recommended):** Use web search tools on the URLs in Section 1 to check for any critical updates to tracking compliance.
2.  **Code Sweep:** Map out how the targeted files handle user interfaces, client-side cookies, outbound link routing, and analytics injection.
3.  **Reporting Interface:** Generate the diagnostic matrix using this strict format:

### 🚨 Comprehensive Legal & Tracking Diagnostic

| Component / File | Risk Vector | Status Level | Concrete Legal/UX Threat | Algorithmic / Code Remediation |
| :--- | :--- | :--- | :--- | :--- |
| *e.g., components/ProductCard.tsx* | *Affiliate & SEO Linkage* | **CRITICAL** | *Outbound store links lack `sponsored` attribute. Triggers high risk of Google indexing penalty.* | *Update link attributes to include `rel="noopener noreferrer sponsored"`.* |
| *e.g., layouts/BaseLayout.tsx* | *Cookie & Script Hydration* | **WARNING** | *Google Analytics initializes instantly; violates GDPR prior-consent mandates.* | *Migrate the initialization logic into an asynchronous dynamic loader function linked to consent state.* |

4.  **Compliant Code Synthesis:** Immediately below the matrix, provide the production-grade, secure, and optimized code refactor that completely resolves the identified flaws.

### Protocol D: Data Retention & Audit Trails (Backend Compliance)
*   **Rule:** Database architectures must log tracking consent configurations without leaking unencrypted Personal Identifiable Information (PII) and provide strict temporal proof of consent.
*   **Code Search Focus:** Database migration tables, user/workspace schemas (Prisma, Mongoose, SQL).
*   **Requirement:** Ensure registration and update handlers log verifiable, time-stamped contract metadata matching the explicit compliance schema matrix below.

#### 📊 Consent Audit Schema Matrix
The agent must verify that the User or Consent database model contains the following fields with these precise specifications:

| Field Name | Type | Nullable | Encryption / Security | Legal Purpose |
| :--- | :--- | :--- | :--- | :--- |
| `consent_timestamp` | `DateTime` | No | None (Index optimized) | Proves *when* the agreement occurred (GDPR Art. 7.1). |
| `tos_version_accepted` | `String` | No | None (SemVer standard) | Identifies the exact Terms of Service contract version. |
| `privacy_version_accepted`| `String` | No | None (SemVer standard) | Identifies the exact Privacy Policy document version. |
| `analytics_allowed` | `Boolean`| No | Default: `false` | Controls conditional client-side load of trackers (GA4/PostHog). |
| `marketing_allowed` | `Boolean`| No | Default: `false` | Controls conditional load of retargeting pixels (Meta Pixel). |
| `consent_ip_hash` | `String` | Yes | SHA-256 Hashed + Salted | Proof of origin without storing raw PII (Data Minimization). |
