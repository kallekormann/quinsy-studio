# Skill: Impressum & AGB

> Impressum, AGB, Haftungsausschlüsse, EU-Streitschlichtung

## Metadata

```
skill_id: CL-003
name: Impressum & AGB
team: 03-compliance-legal
lead_role: Legal & Privacy Officer
support_roles: []
phases: [3, 4, 5]
activation_triggers:
  - Ticket enthält "Impressum", "AGB", "Nutzungsbedingungen"
  - Phase 3: Rechtliche Seiten werden geplant
  - Phase 4: Rechtliche Seiten werden implementiert
  - Phase 5: Legal-Check im QA-Gate
```

---

## Verhaltensregeln

### 1. Impressum (Pflichtangaben)

```markdown
Für alle Webseiten/Dienste:
  1. Name/Firma des Betreibers
  2. Vollständige Adresse
  3. E-Mail-Kontakt
  4. Telefon (falls vorhanden)
  5. USt-IdNr. (falls vorhanden)
  6. Verantwortlich für Inhalte (§ 55 Abs. 2 RStV)
  7. EU-Streitschlichtung (Link zur ODR-Plattform)

Platzierung:
  - Direkt erreichbar (1 Klick vom Footer)
  - Keine Login-Pflicht
  - Keine Versteckung in AGB
```

### 2. AGB (Allgemeine Geschäftsbedingungen)

```markdown
Pflicht-Inhalte:
  1. Geltungsbereich
  2. Vertragsgegenstand
  3. Registrierung / Account
  4. Preise und Zahlung
  5. Widerrufsrecht (14 Tage bei Verbrauchern)
  6. Gewährleistung
  7. Haftungsausschluss
  8. Salvatorische Klausel
  9. Gerichtsstand
  10. Anwendbares Recht (DE oder AT)

Für SaaS:
  - Kündigungsfristen
  - SLA (Service Level Agreement)
  - Datenexport bei Kündigung
  - Features und Änderungen
```

### 3. Widerrufsrecht

```markdown
Bei Verbrauchern (B2C):
  - 14 Tage Widerrufsrecht
  - Kein Grund nötig
  - Form: Text (E-Mail, Brief, Formular)
  - Fristbeginn: Erhalt der Ware/Dienstleistung
  - Ausnahmen: Verderbliche Waren, digitale Inhalte (nach Download)

Bei B2B:
  - Kein gesetzliches Widerrufsrecht
  - Kann in AGB frei vereinbart werden
```

### 4. Haftungsausschluss

```markdown
Typische Formulierung:
  "Die Haftung für Inhalte externer Links übernehmen wir nicht.
   Für den Inhalt der verlinkten Seiten sind ausschließlich
   deren Betreiber verantwortlich."

Für SaaS:
  - Haftung auf Vorsatz und grobe Fahrlässigkeit beschränken
  - Haftungshöchstbetrag definieren
  - Ausschluss für mittelbare Schäden
```

---

## Anti-Patterns

### ❌ Verboten

```markdown
- Impressum nicht erreichbar
- Unvollständige Pflichtangaben
- Fehlende EU-Streitschlichtung
- Kein Widerrufsrecht (B2C)
- Haftungsausschluss zu weit gefasst
- Impressum nur als PDF (statt HTML-Seite)
```

### ✅ Stattdessen

```markdown
- Direkt im Footer verlinkt
- Alle Pflichtangaben vorhanden
- EU-Streitschlichtung Link korrekt
- 14 Tage Widerrufsrecht korrekt umgesetzt
- Haftungsausschluss juristisch geprüft
- Als eigene HTML-Seite
```

---

## Referenzen

- `.quinsy-studio/knowledge-base/compliance_playbook.md` — Compliance-Regeln
- `.quinsy-studio/process/gates.md` — Legal-Check im Gate 5
