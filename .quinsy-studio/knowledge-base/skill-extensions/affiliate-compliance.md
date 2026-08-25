# Skill: Affiliate Compliance & Conversion Architecture
**ID:** SKILL-AFF-001 
**Version:** 2026.1 
**Target:** Affiliate Links, Link Redirectors, Analytics Integration, Disclaimer Disclosures, SEO Link Attributes 
**Environment:** Cursor IDE / Codebase Context 

## Objective
Audit and optimize the affiliate website's codebase to ensure transparent legal compliance, maximize link-click conversions, prevent AdBlocker interference, and guarantee perfect search engine (SEO) indexing structures without degrading user experience.

---

## 1. Compliance & UX Rules for Affiliate Operations

### A. Link Attribution & SEO Safety
*   **Rule:** Every outgoing commercial/affiliate link MUST utilize specific attributes to prevent search engine indexing penalties.
*   **Required HTML Structure:** `rel="nofollow sponsored"` or `rel="sponsored"`.
*   **Targeting:** Explicitly open external store targets in a new tab (`target="_blank" rel="noopener noreferrer sponsored"`).

### B. Disclosure Transparency (The Financial Hook)
*   **Rule:** Commercial intent must not be hidden.
*   **Requirement:** Pages rendering affiliate tracking components or outbound masked routers must display a visible, clear disclosure notice prior to or immediately adjacent to the links.

### C. Zero-Cookie Banner Enforcement (If applicable)
*   **Rule:** If the project goal is "No Cookie Banner for UX Maximization", prevent the introduction of client-side tracking containers (GTM, GA4, Meta Pixel).
*   **Alternative:** Enforce server-side or cookieless analytical endpoints (e.g., Plausible, Fathom, or custom edge logs).

---

## 2. Code Review & Pattern Matching

### A. Outbound Link Audit
*   **Code Search Pattern:** Scan components rendering markdown or static product links (`<a>` tags, button elements linking to stores).
*   **Requirement:** Flag any outbound commercial connection missing the `sponsored` flag or `target="_blank"`.

### B. Link Masking & Redirection Setup
*   **Code Search Pattern:** Scan directory configurations (`/pages/go/*`, `/api/redirect/*`, or Next.js `next.config.js` redirects).
*   **Requirement:** Ensure internal masking endpoints pass correct HTTP `302 Found` (temporary) status codes instead of `301 Moved Permanently`, as affiliate endpoints can change parameters dynamically.

---

## 3. Operational Instructions for Cursor AI

When instructed to **"Audit this affiliate page for compliance and conversion structural health"**, execute these steps:
1.  **Link Vector Sweep:** Scan all anchor tags and buttons pointing to external domains or internal redirectors.
2.  **Disclosure Evaluation:** Check for the presence of the legally required financial sponsor disclosures in the UI layout.
3.  **Output Template:** Deliver results instantly in this structure:

### 📈 Affiliate Tracking & UX Diagnostic

| File / Component | Link Type | Attributes Found | Compliance / SEO Risk | Required Refactor |
| :--- | :--- | :--- | :--- | :--- |
| *e.g., components/ProductCard.tsx* | *Direct Amazon Link* | `target="_blank"` | **HIGH RISK** (Missing `sponsored` attribute; Google SEO penalty risk) | *Update to `rel="noopener noreferrer sponsored"`.* |
| *e.g., templates/PostLayout.tsx* | *Content Page* | *None* | **WARNING** (No clear affiliate disclaimer visible above the fold) | *Inject a clean, accessible disclosure banner template below the main title.* |

4.  **Optimized Snippet:** Provide the completely secure and optimized component rewrite directly under the table.