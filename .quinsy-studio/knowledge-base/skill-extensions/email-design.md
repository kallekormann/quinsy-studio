# Skill: Conversion-Driven Email UI/UX & Copywriting Auditor
**ID:** SKILL-UIX-002 
**Version:** 2026.2 
**Target:** HTML Email Templates, Transactional Emails, Newsletter Copy & Layouts, Sales Funnels, Microcopy, Typography Hierarchies 
**Environment:** Cursor IDE / Codebase Context 

## Objective
Analyze, audit, and optimize email code, visual layouts, and copywriting structure. This skill guarantees bulletproof HTML compatibility across chaotic clients (Outlook, Gmail) while explicitly engineering the copy and UX layout for high information value, readability, and maximum click-through rate (CTR) conversions.

---

## 1. Authoritative Email Rendering & UX Laws
When auditing or generating email components, the agent MUST enforce these technical and behavioral rules:
*   **The Inverted Pyramid Rule:** Layouts must visually funnel the user's eyes from a high-impact headline/hook, down through supporting context, directly into a single, high-contrast action point (CTA).
*   **The Outlook/Word Constraint:** Outlook (Desktop) uses the MS Word engine. It ignores Flexbox, Grid, max-width, margins, and border-radius. Layouts must rely on nested HTML tables (`<table>`, `<tr>`, `<td>`).
*   **The 3-Second Copy Scan Mandate:** Busy users scan, they do not read. Paragraphs must never exceed 3 lines. Key benefits must rely on bullet points with bold structural anchors.
*   **Dark Mode Contrast Adaptability:** Clients invert backgrounds automatically. Typography (contrast ratio minimum 4.5:1) and graphics must remain perfectly eligible against hex `#FFFFFF` and `#121212`.

---

## 2. Integrated Layout, Copy & UX Checklist

### A. Inbox First-Impression (Subject & Preheader Teamwork)
*   **Rule:** The Subject Line and Hidden Preheader must read as a continuous, compelling story to maximize Open Rates, never leaking system placeholders.
*   **Requirement:** Enforce a hidden preheader div right below `<body>` with standard zero-size styling.
*   **Copywriting Standard:** The preheader MUST supplement, not repeat, the subject line. (e.g., Subject: *Your SaaS report is ready* | Preheader: *See which 3 marketing funnels generated 80% of your growth this week*).

### B. High-Conversion Typographic Hierarchy
*   **Rule:** Ensure copy looks informative, organized, and accessible even with images disabled.
*   **Code Search Focus:** Font sizes, line heights, and padding parameters inside `<td>` or `<span>` blocks.
*   **Standards:**
    *   **Main Headlines (H1):** 24px - 32px, `line-height` at 130%. Must instantly state the primary value proposition.
    *   **Body Copy:** 16px minimum for mobile legibility, `line-height` at 150% - 160% to prevent visual crowding.
    *   **Scannable Breakouts:** Utilize `<strong>` tags on the first 2-3 words of bullet points to anchor the reader's eyes during rapid vertical scrolling.

### C. Psychological CTA Architecture
*   **Rule:** Links must be "bulletproof" HTML table-cells, utilizing urgent, action-oriented, low-friction microcopy.
*   **UX Requirement:** Minimum tap target size of 44px x 44px. Margins around the CTA must provide breathing room (minimum 24px vertical padding) to prevent accidental clicks on surrounding elements.
*   **Copywriting Requirement:** Avoid lazy, generic command phrases like *"Click Here"* or *"Submit"*. Replace them with value-focused, friction-free alternatives like *"Get My Free Dashboard"* or *"Unlock Strategy Blueprint"*.

### D. Multi-Device Image & Value Safeguards
*   **Rule:** Emails must remain fully informative and capable of converting even when the recipient's client blocks image loading by default.
*   **Code Search Focus:** `<img>` tags and image ratio layouts.
*   **Requirement:**
    *   Every image must feature styling-optimized `alt="..."` text (colored and sized via inline CSS to look like regular headlines if the image fails to load).
    *   The total image-to-text layout ratio must not exceed 40:60 to avoid triggering automatic ISP spam-filtering matrices.

---

## 3. Operational Instructions for Cursor AI

When instructed to **"Audit this email template / copy slice"**, execute these sequential tasks:
1.  **Hierarchy Assessment:** Analyze if the layout forms a clear visual pyramid leading to the conversion goal.
2.  **Copywriting Friction Check:** Evaluate if sentences are too long, vocabulary is passive, or the value proposition is buried.
3.  **Technical Compatibility Scan:** Check for illegal web layout styles (Flex/Grid) and ensure Dark Mode safety.
4.  **Reporting Interface:** Present data utilizing this multi-layered diagnostic model:

### ✉️ Email UI/UX, Copy & Rendering Diagnostic

| Section / File | Vulnerability Layer | Risk Level | Behavioral or Rendering Threat | Conversion & Structural Fix |
| :--- | :--- | :--- | :--- | :--- |
| *e.g., templates/Promo.html* | **Copywriting / CTA** | **HIGH RISK** | *CTA button copy says "Click Here". Passive phrasing dramatically lowers user intent and CTR.* | *Change text to value-driven action: "Start Scaling For Free".* |
| *e.g., templates/Welcome.html* | **UX Hierarchy** | **WARNING** | *Body paragraph is 7 lines long without structural bolding. Users will skip reading entirely.* | *Break into 2 short paragraphs and convert core perks into a bulleted list.* |
| *e.g., components/Hero.tsx* | **Technical Rendering** | **CRITICAL** | *Uses `display:flex` for a 2-column layout. Will collapse into a jumbled mess in Outlook Desktop.* | *Refactor columns into nested HTML `<td>` containers wrapped in Mso ghost comments.* |

5.  **Refactored Synthesis:** Directly below the table, output the fully optimized, beautifully written, inline-styled, and conversion-tested HTML snippet ready to replace the audited section.