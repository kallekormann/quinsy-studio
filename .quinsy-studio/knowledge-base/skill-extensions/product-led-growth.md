
Kalle Kormann-Philipson <kallekormann@gmail.com>
So., 23. Aug., 14:15 (vor 2 Tagen)
an mich

# Skill: Product-Led Growth (PLG) & Growth Loop Engineer
**ID:** SKILL-PLG-001 
**Version:** 2026.1 
**Target:** Application Workflows, Referral Modules, Pricing Pages, Onboarding Funnels, Product Analytics Instrumentation 
**Environment:** Cursor IDE / Codebase Context 

## Objective
Analyze, design, and audit the web application's codebase to inject autonomous self-distribution (viral loops), accelerate time-to-value (activation), and engineer friction-free, usage-based monetization touchpoints.

---

## 1. Core PLG Mechanics to Enforce
When building features or refactoring workflows, the agent MUST optimize for these three loops:
*   **The Inherent Loop (Watermark):** Every transactional output (shared link, exported PDF, embedded widget) must expose the brand and act as an acquisition funnel for non-users.
*   **The Collaborative Loop (Seat Expansion):** Multi-user workflows must prompt seamless team invitations without forcing payment barriers upfront (expand first, monetize later).
*   **The Monetization Loop (Usage Triggers):** Paywalls must be dynamic, contextual, and triggered by usage thresholds (value metrics) rather than hard roadblocks.

---

## 2. Code Review & Search Patterns

### A. Time-to-Value & Onboarding Optimization
*   **Rule:** Remove micro-frictions. Postpone profiling questions (e.g., "What is your company size?") until *after* the user experiences the initial "Aha-Moment".
*   **Code Search Pattern:** Scan onboarding flows, setup wizards, and onboarding form actions.
*   **Requirement:** Identify any blocking configuration setup or third-party validation that can be moved to background tasks or skipped entirely on first sign-up.

### B. Viral & Collaborative Loops Implementation
*   **Rule:** Sharing features must double as an organic user acquisition channel.
*   **Code Search Pattern:** Check share buttons, link generation functions, email notification dispatchers, or canvas export components.
*   **Requirement:** Gated/shared pages designed for external clients/collaborators must feature an intuitive, non-intrusive registration call-to-action (e.g., *"Built with [SaaS Name] — Create your own free workspace"*).

### C. In-App Monetization & Usage-Based Triggers
*   **Rule:** Never wait for a user to hit an error code to show a pricing table. Surface expansion prompts contextually when usage thresholds near capacity.
*   **Code Search Pattern:** Scan application states handling limits (e.g., `user.project_count`, `workspace.storage_used`).
*   **Requirement:** Ensure frontend components render predictive warnings and inline, one-click upgrade actions when the user hits 80% and 90% of their plan limits.

### D. Explicit UX DoD for PLG + paywall tickets (LO-0021)
When implementing Try/PLG entry or UpgradeModal / export paywalls, acceptance **must** name:
1. **Landing surface** (exact route or dialog) — latency goals must not skip a required naming/consent screen.
2. **Blocking vs soft** — “paywall at export” means the UpgradeModal (or equivalent) **opens** at that moment for free tier; a footer link alone fails review.
3. **What still works free** — e.g. password share stays free while raster branding is monetized.

### E. Soft-path to Account / plan (LO-0142 / LO-0143)
When marketing or paywall soft-paths defer checkout to Settings Account (or plan tab):
1. **URL alone is not done** — Free users must see Free plan + Upgrade CTA in the first Account viewport, **or** the upgrade dialog must auto-open (`?upgrade=1`).
2. **Click-to-open only fails soft-path intent** — if the journey was “upgrade now,” do not require hunting an unmarked control.
3. **Assert before `move … done`** — free-tier unit/UI/smoke (see `process/gates.md` LO-0143). Pattern: `studio-library/ui/docs/patterns/upgrade-soft-path.md`.

---
*   **Code Structure Example:**
    ```typescript
    if (usageRatio >= 0.8 && usageRatio < 1.0) {
       renderContextualBanner("You're approaching your limit. Upgrade seamlessly to keep scaling.");
    }
    ```

### D. Analytics & PQL (Product Qualified Lead) Instrumentation
*   **Rule:** Core activation events must be meticulously tracked to inform growth workflows.
*   **Code Search Pattern:** Look for event trackers (Mixpanel, Amplitude, PostHog, Segment SDKs).
*   **Requirement:** Ensure key milestone handlers (e.g., `onFirstIntegrationSuccess`, `onDashboardShared`) trigger analytics payloads that contain the user's role and workspace state, allowing backend engines to compute the active PQL score.

---

## 3. Operational Instructions for Cursor AI

When instructed to **"Audit this workflow/component for PLG capabilities"**, follow this layout:
1.  **Loop Classification:** Identify if the targeted area belongs to Onboarding/Activation, Collaboration/Virality, or Upgrades/Monetization.
2.  **Friction Analysis:** Locate code bottlenecks, forced manual steps, hidden upgrade paths, or missed sharing opportunities.
3.  **Reporting Structure:** Format recommendations using this explicit structure:

### 🚀 PLG Growth Engine Optimization

| File / Route | Current Implementation | Proposed Growth Mechanism | Code/UX Change Required | Growth Impact Spec |
| :--- | :--- | :--- | :--- | :--- |
| *e.g., routes/share.ts* | *Generates raw JSON payload for external viewers.* | *Watermark / Content Loop* | *Wrap payload in a clean public-facing Next.js reader layout with a "Claim your free account" button in the navigation header.* | *Drives secondary organic traffic and lowers blending CAC via public shares.* |

4.  **Refactored Code Block:** Provide a production-ready, clean code update that implements the viral hook or context-aware paywall element directly beneath the diagnostic table.