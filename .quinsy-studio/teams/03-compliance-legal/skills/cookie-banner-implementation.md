# Skill: Cookie Banner Implementation

> Cookie banner, consent management, categories, opt-in, withdrawal

## Metadata

```
skill_id: CL-002
name: Cookie Banner Implementation
team: 03-compliance-legal
lead_role: Legal & Privacy Officer
support_roles: [Frontend Engineer, Backend Engineer]
phases: [3, 4, 5]
activation_triggers:
  - Ticket contains "cookie", "consent", "banner", "tracking"
  - Phase 3: cookie strategy is planned
  - Phase 4: banner is implemented
  - Phase 5: cookie check in the QA gate
```

---

## Behavior rules

### 1. Cookie categories

```markdown
NECESSARY (always active):
  - Session cookies (login)
  - CSRF token
  - Cookie banner decision
  - Load-balancer session
  → No consent needed (legitimate interest)

ANALYTICS (opt-in):
  - Google Analytics / Plausible
  - Heatmaps (Hotjar)
  - Performance monitoring
  → Only with explicit consent

MARKETING (opt-in):
  - Facebook pixel
  - Google Ads
  - Retargeting
  → Only with explicit consent
```

### 2. Banner design

```markdown
UI requirements:
  - Fully visible (not hidden)
  - Same prominence for "Accept all" and "Selection"
  - No "continue = accept" trick
  - Explicit buttons: "Accept all", "Only necessary", "Customize selection"

Placement:
  - Modal/overlay (not just a footer link)
  - Blocks interaction until a decision
  - Remember: store the decision in a cookie/cookie consent
```

### 3. Consent storage

```markdown
Cookie names:
  - cookie_consent: { necessary: true, analytics: false, marketing: false }
  - cookie_consent_date: 2026-08-20T10:30:00Z
  - cookie_consent_version: 1 (for updated categories)

Expiry: 365 days
Withdrawal: link in the footer "Cookie settings"
```

### 4. Implementation

```markdown
Frontend:
  1. Before consent: do NOT load analytics/marketing scripts!
  2. Banner component (React/Vue)
  3. Store consent state in a cookie
  4. Load scripts dynamically after consent

Backend:
  1. Store consent status in the user profile (on login)
  2. API for consent changes
  3. Audit log for consent changes
```

### 5. Withdrawal

```markdown
Always reachable:
  - Link in the footer: "Cookie settings"
  - Reopens the banner
  - Changes take effect immediately
  - Already set cookies are deleted
```

---

## Anti-patterns

### ❌ Forbidden

```markdown
- Tracking scripts BEFORE consent
- "Continue = Accept"
- Only opt-out (checkbox active by default)
- No withdrawal option
- Third-party cookies without consent
- Banner that only has an "OK" button
```

### ✅ Instead

```markdown
- Load scripts only AFTER consent
- Clear choices
- Opt-in as default (checkbox = unchecked)
- Footer link for withdrawal
- Only necessary cookies without consent
- Three buttons: All / Only necessary / Customize
```

---

## External skill support

> Before implementation load the imported best-in-class skills (`./studio update-skills`):

- **`compliance_cookies/skills/cookiecomply`** (samir-abis/cookiecomply-skills) — complete GDPR cookie compliance workflows (banner, consent management, CMP). **Primary source for this skill.**

Flow: read `cookiecomply` → adopt the categories/consent flows → align with the internal GDPR rules.

## References

- `.quinsy-studio/knowledge-base/compliance_playbook.md` — compliance rules
- `.quinsy-studio/studio-library/packages/feature-gating/` — feature gating
