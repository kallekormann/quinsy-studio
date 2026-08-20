# Skill: Zero-Data Architecture

> Datenminimierung, Löschkonzepte, Auftragsverarbeitungsverträge, Pseudonymisierung

## Metadata

```
skill_id: CL-004
name: Zero-Data Architecture
team: 03-compliance-legal
lead_role: Legal & Privacy Officer
support_roles: [Backend Architect, Systems Architect]
phases: [2, 3, 4]
activation_triggers:
  - Ticket enthält "Zero-Data", "Datenminimierung", "Löschkonzept"
  - Phase 2: Daten-Architektur wird definiert
  - Externe Dienstleister werden eingebunden
  - Feature erfordert personenbezogene Daten
```

---

## Verhaltensregeln

### 1. Datenminimierung (Art. 5 DSGVO)

```markdown
Prinzip: So wenig Daten wie möglich, so viel wie nötig

Checkliste für jedes Datenfeld:
  - Brauchen wir dieses Feld wirklich?
  - Kann es pseudonymisiert werden?
  - Kann es aggregiert werden?
  - Kann es nach Nutzung gelöscht werden?
  - Gibt es eine less-invasive Alternative?

Beispiele:
  ❌ Geburtsdatum speichern → ✅ Nur "über 18" Boolean
  ❌ vollständige IP-Adresse → ✅ Pseudonymisierte IP
  ❌ Name + E-Mail + Telefon → ✅ Nur E-Mail (Kommunikation)
```

### 2. Löschkonzept

```markdown
Pro Datenkategorie:
  - Speicherdauer definieren (max.!)
  - Automatische Löschung implementieren
  - Löschung muss verifizierbar sein
  - Backup-Löschung berücksichtigen

Löschstrategien:
  - Soft Delete → Hard Delete nach Frist
  - Anonymisierung (statt Löschung wenn Aggregate nötig)
  - Pseudonymisierung (Löschung der Zuordnung)
```

### 3. Auftragsverarbeitungsverträge (AVV/DPA)

```markdown
Pflicht bei jedem externen Dienstleister der personenbezogene Daten verarbeitet:

Inhalte:
  1. Art und Zweck der Verarbeitung
  2. Dauer
  3. Art der personenbezogenen Daten
  4. Kategorie der betroffenen Personen
  5. Pflichten des Auftragsverarbeiters
  6. Technische und organisatorische Maßnahmen
  7. Unterauftragsverarbeiter
  8. Drittland-Transfer (falls vorhanden)

Beispiele für AVV-Pflicht:
  - Hosting (Vercel, AWS, Supabase)
  - Analytics (Plausible, PostHog)
  - E-Mail (SendGrid, Resend)
  - Payment (Stripe)
  - Support (Crisp, Intercom)
```

### 4. Pseudonymisierung

```markdown
Techniken:
  - Hashing für User-IDs in Logs
  - Tokenisierung für Payment-Daten
  - Aggregation für Analytics
  - K-Anonymity für Requests

Vorteile:
  - Datenschutz troz Analyse-Möglichkeit
  - Reduziertes Risiko bei Datenleck
  - Einfachere DSGVO-Konformität
```

### 5. Privacy by Design

```markdown
Architektur-Prinzipien:
  1. Nur notwendige Daten erheben
  2. Daten nur so lange wie nötig speichern
  3. Standardmäßig privat (privacy-first)
  4. Ende-zu-Ende Verschlüsselung wo möglich
  5. Client-seitige Verarbeitung bevorzugen
  6. Keine Third-Party-Tracking ohne Consent
```

---

## Anti-Patterns

### ❌ Verboten

```markdown
- Alles speichern "falls es mal gebraucht wird"
- Keine Löschfristen definiert
- Kein AVV mit Dienstleistern
- IP-Adressen unverschlüsselt speichern
- User-Tracking ohne Consent
- Personenbezogene Daten in Logs
```

### ✅ Stattdessen

```markdown
- Nur notwendige Daten erheben
- Klare Löschfristen + automatische Löschung
- AVV mit allen Dienstleistern
- Pseudonymisierung wo möglich
- Tracking nur mit Consent
- Anonymisierte Logs
```

---

## Referenzen

- `.quinsy-studio/knowledge-base/compliance_playbook.md` — Compliance-Regeln
- `.quinsy-studio/knowledge-base/backend_playbook.md` — Datenbank-Design
