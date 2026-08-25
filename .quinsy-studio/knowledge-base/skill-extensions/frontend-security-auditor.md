# Skill: Frontend Security & Vulnerability Auditor
**ID:** SKILL-SEC-001 
**Version:** 2026.1 
**Target:** Client-Side Applications (React, Next.js, Vue, Svelte, Angular, Vanilla JS) 
**Environment:** Cursor IDE / Codebase Context 

## Objective
Analyze the frontend repository to identify, prevent, and remediate all client-side security vulnerabilities, injection vectors, logical flaws, and configuration weaknesses that could be exploited by malicious actors.

---

## 1. Reference Frameworks & Security Standards
When identifying issues or refactoring code, the agent MUST explicitly align with:
*   **OWASP Top 10 Client-Side Risks:** Focus on XSS, CSRF, broken authentication, and DOM-based vulnerabilities.
*   **W3C Security Specifications:** Strict implementations of Content Security Policy (CSP), Subresource Integrity (SRI), and secure CORS headers.
*   **OAuth 2.1 / OIDC Best Practices:** Secure token handling, avoiding implicit flows on the client side.

---

## 2. Vulnerability Checklist & Code Search Patterns

### A. Cross-Site Scripting (XSS) & Injection
*   **Rule:** Never trust user input. Prevent Reflected, Stored, and DOM-based XSS by ensuring proper escaping, sanitization, and avoiding dangerous sinks.
*   **Code Search Pattern:**
    *   React: `dangerouslySetInnerHTML`
    *   Vue/Svelte: `v-html`, `{@html ...}`
    *   Vanilla JS/DOM: `element.innerHTML`, `document.write()`, `eval()`, `setTimeout(string)`, `setInterval(string)`
*   **Requirement:** If raw HTML injection is absolutely necessary, the data MUST pass through a verified sanitization library (e.g., `DOMPurify.sanitize()`) before rendering.

### B. Broken Client-Side Authentication & Session Management
*   **Rule:** Sensitive tokens (JWTs, Access Tokens, Refresh Tokens) must never be stored where malicious scripts (XSS) can access them.
*   **Code Search Pattern:** `localStorage.setItem(`, `sessionStorage.setItem(`, `document.cookie =`
*   **Requirement:**
    *   Do not store JWTs or session tokens in LocalStorage/SessionStorage.
    *   Session management must rely on **HttpOnly, Secure, SameSite=Strict/Lax** cookies managed by the backend.
    *   If using client-side state for tokens, ensure they are stored only in-memory (short-lived variables).

### C. Cross-Site Request Forgery (CSRF) Mitigation
*   **Rule:** Protect state-changing client requests from being executed by unauthorized third-party sites.
*   **Code Search Pattern:** Scan API wrappers, Axios instances, Fetch configurations, or form submissions.
*   **Requirement:** Ensure state-changing requests (`POST`, `PUT`, `DELETE`, `PATCH`) append custom anti-CSRF headers (e.g., `X-XSRF-TOKEN`) or utilize the modern browser defense `SameSite=Strict/Lax` flags on cookies.

### D. Sensitive Data Exposure & Hardcoded Secrets
*   **Rule:** Production API keys, private certificates, staging credentials, or internal system configurations must never be committed to frontend code.
*   **Code Search Pattern:** Search for strings like `api_key`, `secret`, `private_`, `password`, `token = "`, or unmasked environment variables lacking public prefixes (e.g., missing `NEXT_PUBLIC_` or `VITE_`).
*   **Requirement:** Move all sensitive operational variables to server-side environments or secure Edge functions.

### E. Vulnerable Dependencies & Supply Chain Attacks
*   **Rule:** Prevent malicious third-party code from executing within the user's browser.
*   **Code Search Pattern:** Examine `package.json`, `pnpm-lock.yaml`, `package-lock.json`, and script tags in `index.html`.
*   **Requirement:**
    *   Ensure external CDN scripts utilize **Subresource Integrity (SRI)** hashes: `<script src="..." integrity="sha384-..." crossorigin="anonymous">`.
    *   Flag any outdated, unmaintained, or direct un-nested script injections.

### F. Broken Object Level Exploitation (Client-Side Logic Bypass)
*   **Rule:** Never rely on frontend UI states or hidden fields to enforce user permissions, feature flags, or pricing logic.
*   **Code Search Pattern:** Look for logic hiding premium features or administrative tools exclusively via UI toggles: `isAdmin ? <AdminPanel /> : null` or `if (user.role === 'free') { disableFeature() }`.
*   **Requirement:** The frontend must treat all local visibility logic as purely cosmetic. Accompanying API endpoints must strictly validate user permissions server-side on every request.

### G. Security Headers & Clickjacking Defence
*   **Rule:** Protect the frontend app from being framed or manipulated.
*   **Code Search Pattern:** Look at Next.js configuration (`next.config.js`), Vite config, or framework routing setups where metadata/headers are injected.
*   **Requirement:** Ensure headers or meta tags enforce:
    *   `Content-Security-Policy (CSP)` (Restricting script sources)
    *   `X-Frame-Options: DENY` or `SAMEORIGIN` (Clickjacking prevention)
    *   `X-Content-Type-Options: nosniff`

---

## 3. Operational Instructions for Cursor AI

When instructed to **"Audit this frontend component/file for security vulnerabilities"**, execute these steps:
1.  **Context Discovery:** Map out if the target code manages user input, handles API communications, stores local state, or renders dynamic UI.
2.  **Threat Modeling:** Cross-reference the code against the exploit vectors in Section 2.
3.  **Reporting Format:** Output the results using this precise structure:

### ⚠️ Vulnerability Report

| File & Line | Threat Vector | Risk Level | Exploitation Scenario | Remediation / Code Fix |
| :--- | :--- | :--- | :--- | :--- |
| *e.g., src/components/Profile.tsx:42* | *DOM-XSS via innerHTML* | **CRITICAL** | *Attacker injects `<img src=x onerror=alert(1)>` via profile name string.* | *Replace `.innerHTML` with `.textContent` or wrap in `DOMPurify.sanitize()`.* |

4.  **Proactive Suggestion:** Always provide a fully rewritten, secure version of the vulnerable code snippet directly below the table.