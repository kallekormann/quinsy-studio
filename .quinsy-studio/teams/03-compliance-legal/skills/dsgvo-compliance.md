# Skill: DSGVO Compliance

> Datenschutz-Grundverordnung, Verarbeitungsverzeichnis, Betroffenenrechte, Datenschutzerklärung

## Metadata

```
skill_id: CL-001
name: DSGVO Compliance
team: 03-compliance-legal
lead_role: Legal & Privacy Officer
support_roles: [Backend Security Engineer]
phases: [0, 1, 2, 3, 4, 5, 6]
activation_triggers:
  - Ticket enthält "DSGVO", "GDPR", "Datenschutz", "Privacy"
  - Jedes Projekt (Pflicht-Check in Phase 1)
  - Phase 5: DSGVO-Audit
  - Externe Dienstleister werden eingebunden
```

---

## Verhaltensregeln

### 1. Verarbeitungsverzeichnis (Art. 30 DSGVO)

```markdown
Pflicht-Einträge pro Verarbeitungstätigkeit:
  1. Name des Verantwortlichen
  2. Zweck der Verarbeitung
  3. Kategorie der betroffenen Personen
  4. Kategorie der personenbezogenen Daten
  5. Kategorie der Empfänger
  6. Drittland-Transfer (ja/nein + Garantien)
  7. Löschfristen
  8. Technische und organisatorische Maßnahmen
```

### 2. Datenschutzerklärung

```markdown
Pflicht-Inhalte:
  1. Verantwortlicher (Name, Adresse, E-Mail)
  2. Datenschutzbeauftragter (falls vorhanden)
  3. Erhobene Datenarten
  4. Zwecke der Verarbeitung
  5. Rechtsgrundlagen (Art. 6 DSGVO)
  6. Speicherdauer / Löschfristen
  7. Betroffenenrechte (Auskunft, Löschung, Berichtigung)
  8. Beschwerderecht (Landesdatenschutzbehörde)
  9. Server-Standort
  10. Kontaktdaten

Aktualisierung: Mindestens jährlich oder bei Änderungen
```

### 3. Cookie-Banner

```markdown
Kategorien:
  - Notwendig (immer aktiv, kein Consent nötig)
  - Analytics (opt-in!)
  - Marketing (opt-in!)

Regeln:
  - Opt-in (nicht opt-out!)
  - Granulare Auswahl pro Kategorie
  - "Alle akzeptieren" UND "Auswahl speichern"
  - Widerruf jederzeit möglich (Link im Footer)
  - Keine Tricker-Cookies ("weiter = akzeptieren")
  - Cookie-Dauer dokumentiert
  - Drittanbieter-Liste aktuell
```

### 4. Rechtsgrundlagen

```markdown
Art. 6 Abs. 1 DSGVO:
  a) Einwilligung          → Cookie-Banner, Newsletter
  b) Vertragserfüllung     → Account-Erstellung, Bestellung
  c) Rechtliche Verpflichtung → Steuerliche Aufbewahrung
  d) Lebenswichtiges Interesse → Notfälle
  e) Öffentliches Interesse → (selten)
  f) Berechtigtes Interesse → Analytics (mit Abwägung!)

Für jedes Datenfeld muss eine Rechtsgrundlage dokumentiert sein!
```

### 5. Betroffenenrechte

```markdown
Rechte der Nutzer:
  - Auskunft (Art. 15): Welche Daten haben wir?
  - Berichtigung (Art. 16): Daten korrigieren
  - Löschung (Art. 17): "Recht auf Vergessenwerden"
  - Einschränkung (Art. 18): Verarbeitung einschränken
  - Datenübertragbarkeit (Art. 20): Daten als Export
  - Widerspruch (Art. 21): Gegen Verarbeitung widersprechen
  - Automatisierte Entscheidungen (Art. 22): Keine ohne Einwilligung

Umsetzung:
  - Self-Service Portal für Auskunft/Export/Löschung
  - Response-Time: 30 Tage (max.)
```

### 6. Drittland-Transfer

```markdown
Wenn Daten außerhalb der EU verarbeitet werden:
  1. Prüfe ob Angemessenheitsbeschluss existiert
  2. Falls nicht: Standard-Vertragsklauseln (SCC)
  3. TOMs (Technische Organisatorische Maßnahmen) dokumentieren
  4. User informieren

Vorrang: EU-Server! Nur bei zwingenden Gründen Drittland.
```

---

## Anti-Patterns

### ❌ Verboten

```markdown
- Tracking ohne Einwilligung
- Kein Cookie-Banner
- Opt-out statt Opt-in
- Kein Verarbeitungsverzeichnis
- Drittland-Transfer ohne SCC
- Daten longer als nötig speichern
- Kein Selbstbedienungs-Portal für Betroffenenrechte
```

### ✅ Stattdessen

```markdown
- Nur mit Einwilligung tracken
- Granularer Cookie-Banner
- Opt-in als Standard
- Vollständiges Verarbeitungsverzeichnis
- EU-Server bevorzugen
- Speicherdauer definieren und umsetzen
- Self-Service für Auskunft/Export/Löschung
```

---

## Referenzen

- `.quinsy-studio/knowledge-base/compliance_playbook.md` — Compliance-Regeln
- `.quinsy-studio/process/gates.md` — DSGVO im Gate 5
- `./studio gate <project> --dsgvo` — DSGVO-Check
