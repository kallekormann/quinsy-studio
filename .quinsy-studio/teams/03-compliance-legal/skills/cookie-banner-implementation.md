# Skill: Cookie Banner Implementation

> Cookie-Banner, Consent-Management, Kategorien, Opt-in, Widerruf

## Metadata

```
skill_id: CL-002
name: Cookie Banner Implementation
team: 03-compliance-legal
lead_role: Legal & Privacy Officer
support_roles: [Frontend Engineer, Backend Engineer]
phases: [3, 4, 5]
activation_triggers:
  - Ticket enthält "Cookie", "Consent", "Banner", "Tracking"
  - Phase 3: Cookie-Strategie wird geplant
  - Phase 4: Banner wird implementiert
  - Phase 5: Cookie-Check im QA-Gate
```

---

## Verhaltensregeln

### 1. Cookie-Kategorien

```markdown
NOTWENDIG (immer aktiv):
  - Session-Cookies (Login)
  - CSRF-Token
  - Cookie-Banner-Entscheidung
  - Load-Balancer-Session
  → Kein Consent nötig (berechtigtes Interesse)

ANALYTICS (opt-in):
  - Google Analytics / Plausible
  - Heatmaps (Hotjar)
  - Performance-Monitoring
  → Nur mit explizitem Consent

MARKETING (opt-in):
  - Facebook Pixel
  - Google Ads
  - Retargeting
  → Nur mit explizitem Consent
```

### 2. Banner-Design

```markdown
UI-Anforderungen:
  - Vollständig sichtbar (nicht versteckt)
  - Gleiche Prominenz für "Alle akzeptieren" und "Auswahl"
  - Kein "weiter = akzeptieren" Tricker
  - Explizite Buttons: "Alle akzeptieren", "Nur notwendige", "Auswahl anpassen"

Platzierung:
  - Modal/Overlay (nicht nur Footer-Link)
  - Blockiert Interaktion bis Entscheidung
  - Remember: Entscheidung in Cookie/Cookie-Consent speichern
```

### 3. Consent-Speicherung

```markdown
Cookie-Namen:
  - cookie_consent: { necessary: true, analytics: false, marketing: false }
  - cookie_consent_date: 2026-08-20T10:30:00Z
  - cookie_consent_version: 1 (für aktualisierte Kategorien)

Ablauf: 365 Tage
Widerruf: Link im Footer "Cookie-Einstellungen"
```

### 4. Implementation

```markdown
Frontend:
  1. Vor Consent: Kein Analytics/Marketing Script laden!
  2. Banner Component (React/Vue)
  3. Consent State in Cookie speichern
  4. Scripts dynamisch laden nach Consent

Backend:
  1. Consent-Status in User-Profil speichern (bei Login)
  2. API für Consent-Änderung
  3. Audit-Log für Consent-Änderungen
```

### 5. Widerruf

```markdown
Immer erreichbar:
  - Link im Footer: "Cookie-Einstellungen"
  - Öffnet erneut den Banner
  - Änderungen werden sofort wirksam
  - Bereits gesetzte Cookies werden gelöscht
```

---

## Anti-Patterns

### ❌ Verboten

```markdown
- Tracking Script BEFORE Consent
- "Weiter = Akzeptieren"
- Nur Opt-out (Checkbox die standardmäßig aktiv ist)
- Kein Widerruf-Möglichkeit
- Third-Party Cookies ohne Consent
- Banner der nur "OK" Button hat
```

### ✅ Stattdessen

```markdown
- Scripts erst NACH Consent laden
- Klare Wahlmöglichkeiten
- Opt-in als Default (Checkbox = unchecked)
- Footer-Link für Widerruf
- Nur notwendige Cookies ohne Consent
- Drei Buttons: Alle / Nur notwendige / Anpassen
```

---

## Externe Skill-Unterstützung

> Vor der Umsetzung die importierten Best-in-Class-Skills laden (`./studio update-skills`):

- **`compliance_cookies/skills/cookiecomply`** (samir-abis/cookiecomply-skills) — vollständige DSGVO-Cookie-Compliance-Workflows (Banner, Consent-Management, CMP). **Primäre Quelle für diese Skill.**

Ablauf: `cookiecomply` lesen → Kategorien/Consent-Flows übernehmen → mit internen DSGVO-Regeln abgleichen.

## Referenzen

- `.quinsy-studio/knowledge-base/compliance_playbook.md` — Compliance-Regeln
- `.quinsy-studio/studio-library/packages/feature-gating/` — Feature-Gating
