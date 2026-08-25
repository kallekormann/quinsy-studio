# Skill: Cookie Compliance, Consent Architecture & UX Optimizer
**ID:** SKILL-LEG-003 
**Version:** 2026.1 
**Target:** Cookie Banners, Consent Management Platforms (CMPs), Tracking Script Injectors, Client-side Analytics (GA4, PostHog, Mixpanel, Meta Pixel) 
**Environment:** Cursor IDE / Codebase Context 

## Objective
Audit and architect a legally bulletproof, GDPR/ePrivacy-compliant cookie consent system that guarantees fluid UI/UX, zero-interaction friction, and high opt-in conversion without resorting to illegal dark patterns.

---

## 1. Legal Foundations vs. Fluid UX Rules
When evaluating or writing code for the consent engine, the agent MUST enforce these dual-balancing principles:

### A. Legal Constraints (The Non-Negotiables)
*   **Prior Consent (Zero-Load):** No non-essential cookies (Analytics, Marketing) may be dropped or executed *before* explicit consent is given.
*   **Granular Opt-In:** Users must be able to accept "Analytics" but decline "Marketing" via distinct, un-checked toggles.
*   **Easy Withdrawal:** Revoking consent must be as easy as giving it (e.g., a persistent floating cookie icon in the lower-left corner).
*   **No Dark Patterns:** The "Decline All" button must have the exact same visual hierarchy, color contrast, and font size as the "Accept All" button.

### B. UX Optimization (The Delight Mechanics)
*   **Non-Blocking Layouts:** Where allowed, use elegant slide-in banners or corner cards instead of aggressive full-screen modal overlays to preserve immediate value-perception.
*   **Asynchronous Script Hydration:** Scripts must inject dynamically in memory *immediately* upon user click, preventing page reloads or layout shifts (CLS).
*   **State Persistence (Zero Flash):** Read the user's consent state from an encrypted cookie/localStorage synchronously during root layout rendering to prevent the banner from "flashing" on subsequent page views.

---

## 2. Code Review & Search Patterns

### A. Non-Essential Script Interception
*   **Rule:** Standard script tags (e.g., Google Analytics `<script>` snippets) directly embedded in HTML are critical compliance failures.
*   **Code Search Pattern:** Scan `index.html`, `_document.tsx`, `RootLayout.tsx`, or framework entry points for hardcoded `gtag`, `fbq`, `posthog`, or `mixpanel` initializations.
*   **Requirement:** Convert these hardcoded injections into dynamic, state-driven wrapper functions controlled by a central Consent Context.

### B. Conditional In-Memory Hydration
*   **Rule:** Tracking systems must dynamically mount only when permission is validated.
*   **Code Structure Standard (React/Next.js Example):**
    ```typescript
    const handleAcceptAll = () => {
      setConsentState({ analytics: true, marketing: true });
      // Dynamically load Google Analytics without page refresh
      if (typeof window !== 'undefined' && !window.gtag) {
        const script = document.createElement('script');
        script.src = `https://googletagmanager.com{process.env.NEXT_PUBLIC_GA_ID}`;
        script.async = true;
        document.head.appendChild(script);

        window.dataLayer = window.dataLayer || [];
        window.gtag = function() { dataLayer.push(arguments); };
        window.gtag('js', new Date());
        window.gtag('config', process.env.NEXT_PUBLIC_GA_ID);
      }
    };
    ```

### C. Granular Toggle Mechanics
*   **Rule:** The granular settings panel must offer clean, satisfying micro-interactions.
*   **Code Search Pattern:** Look for `ConsentModal.tsx` or `CookiePreferences.tsx` files.
*   **Requirement:** Ensure category toggles (Necessary, Performance, Marketing) use smooth 60fps spring transitions (e.g., Framer Motion) and clearly display which third-party tool (e.g., *Google Analytics*, *Stripe*, *PostHog*) falls under which bucket.

---

## 3. Operational Instructions for Cursor AI

When instructed to **"Audit or refactor our cookie banner and tracking logic"**, follow this setup:
1.  **Dependency Mapping:** Locate every client-side script that reads/writes cookies or local storage.
2.  **Compliance Testing:** Verify if scripts fire before interaction and evaluate button visual equity (Dark Pattern Check).
3.  **Reporting Matrix:** Present data utilizing this template:

### 🍪 Cookie & Consent Engine Audit

| Script / Component | Purpose | Current Compliance State | UX Friction Points | Required Refactor |
| :--- | :--- | :--- | :--- | :--- |
| *e.g., components/GA4.tsx* | *Google Analytics 4* | **CRITICAL FAILURE** (Loads instantly on root mount) | *None, but violates prior consent law.* | *Wrap in `useEffect` triggered exclusively by `consent.analytics === true` state.* |
| *e.g., components/CookieBanner.tsx* | *UI Consent Banner* | **WARNING** (Decline button is hidden inside sub-menus) | *High user frustration. Violates GDPR visual equity rules.* | *Move "Decline All" to the primary banner layout with matching visual prominence.* |

4.  **Production Code Block:** Generate a fully responsive, animated, and compliant Cookie Banner component accompanied by a global `ConsentProvider` wrapper file.
