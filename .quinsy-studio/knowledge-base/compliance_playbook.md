# Compliance Playbook

> Zero-Data-Architecture, DSGVO, Cookie-Consent — die globalen Compliance-Standards.

## Grundprinzip

```
Compliance ist kein Feature — es ist Pflicht.
Datenminimierung ist das Default.
```

---

## Zero-Data Architecture

### Prinzip

```
Sammle nur das, was du brauchst.
Lösche, was du nicht mehr brauchst.
Schütze, was du haben musst.
```

### Umsetzung

| Prinzip | Maßnahme |
|---------|----------|
| **Datenminimierung** | Nur essentielle Daten erheben |
| **Zweckbindung** | Daten nur für definierten Zweck nutzen |
| **Speicherbegrenzung** | Automatische Löschfristen |
| **Pseudonymisierung** | IDs statt echter Namen |
| **Verschlüsselung** | At-rest und in-transit |

### Technische Maßnahmen

```typescript
// 1. Pseudonymisierung
const pseudonym = crypto.createHash('sha256').update(userId).digest('hex');

// 2. Automatische Löschung
await db.query(`
  DELETE FROM analytics 
  WHERE created_at < NOW() - INTERVAL '90 days'
`);

// 3. Verschlüsselung
const encrypted = crypto.createCipheriv('aes-256-gcm', key, iv);
```

---

## DSGVO

### Betroffenenrechte

| Recht | Beschreibung | Umsetzung |
|-------|-------------|-----------|
| **Auskunft** | Welche Daten gespeichert? | API-Endpoint: `GET /me/data` |
| **Berichtigung** | Daten korrigieren | API-Endpoint: `PATCH /me` |
| **Löschung** | Daten löschen ("Recht auf Vergessen") | API-Endpoint: `DELETE /me` |
| **Datenübertragbarkeit** | Daten als Export | API-Endpoint: `GET /me/export` |
| **Widerspruch** | Gegen Verarbeitung | Checkbox in Settings |
| **Einwilligung** | Opt-in für Tracking | Cookie-Banner |

### Verarbeitungsverzeichnis

```markdown
# Verarbeitungsverzeichnis

| Verarbeitung | Zweck | Rechtsgrundlage | Speicherdauer |
|-------------|-------|-----------------|---------------|
| User-Account | Diensterbringung | Art. 6(1)(b) DSGVO | Bis zur Löschung |
| Analytics | Produktverbesserung | Art. 6(1)(a) DSGVO | 90 Tage |
| Newsletter | Marketing | Art. 6(1)(a) DSGVO | Bis Abmeldung |
```

---

## Cookie-Banner

### Anforderungen

1. **Opt-in** (nicht opt-out!)
2. **Granulare Auswahl** (Notwendig, Analytics, Marketing)
3. **Widerruf** jederzeit möglich
4. **Keine Tricker** (z.B. "weiter = akzeptieren")
5. **Cookie-Dauer** dokumentiert
6. **Drittanbieter-Liste** aktuell

### Implementierung

```typescript
// Cookie-Kategorien
const cookieCategories = {
  necessary: {
    name: 'Notwendig',
    description: 'Essentiell für die Nutzung der Seite',
    required: true, // Nicht deaktivierbar
  },
  analytics: {
    name: 'Analytics',
    description: 'Helfen uns die Seite zu verbessern',
    required: false,
  },
  marketing: {
    name: 'Marketing',
    description: 'Personalisierte Werbung',
    required: false,
  },
};

// Consent-Management
function setConsent(category: keyof typeof cookieCategories, value: boolean) {
  localStorage.setItem(`consent_${category}`, String(value));
}

function hasConsent(category: keyof typeof cookieCategories): boolean {
  if (cookieCategories[category].required) return true;
  return localStorage.getItem(`consent_${category}`) === 'true';
}
```

---

## Impressum

### Pflichtangaben

```markdown
# Impressum

## Verantwortlich für den Inhalt
[Name/Firma]
[Straße, Hausnummer]
[PLZ, Ort]
[E-Mail]
[Telefon] (optional)

## Umsatzsteuer-ID (falls vorhanden)
[Steuernummer oder USt-IdNr.]

## Streitschlichtung
Die Europäische Kommission stellt eine Plattform zur Online-Streitbeilegung (OS) bereit: https://ec.europa.eu/consumers/odr/

Wir sind nicht bereit oder verpflichtet, an Streitbeileungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen.

## Haftungsausschluss
[Inhaltlich wie rechtlich]
```

---

## Datenschutzerklärung

### Struktur

```markdown
# Datenschutzerklärung

## 1. Verantwortlicher
[Name, Adresse, E-Mail]

## 2. Datenschutzbeauftragter (falls vorhanden)
[Name, E-Mail]

## 3. Erhobene Datenarten
- Account-Daten (Email, Name)
- Nutzungsverhalten (Analytics)
- Technische Daten (IP, Browser)

## 4. Zwecke der Verarbeitung
- Diensterbringung
- Produktverbesserung
- Marketing (mit Einwilligung)

## 5. Rechtsgrundlagen
- Art. 6(1)(a) DSGVO: Einwilligung
- Art. 6(1)(b) DSGVO: Vertragsanbahnung
- Art. 6(1)(f) DSGVO: Berechtigtes Interesse

## 6. Speicherdauer
- Account-Daten: Bis zur Löschung
- Analytics: 90 Tage
- Logs: 30 Tage

## 7. Betroffenenrechte
- Auskunft (Art. 15 DSGVO)
- Berichtigung (Art. 16 DSGVO)
- Löschung (Art. 17 DSGVO)
- Datenübertragbarkeit (Art. 20 DSGVO)
- Widerspruch (Art. 21 DSGVO)

## 8. Beschwerderecht
[Beschwerdestelle]

## 9. Server-Standort
[EU/Angabe]

## 10. Cookies
[Cookie-Liste]
```

---

## AVV / DPA

### Checkliste für Dienstleister

- [ ] Auftragsverarbeitungsvertrag (AVV) vorhanden
- [ ] Server-Standort in EU
- [ ] Verschlüsselung at-rest und in-transit
- [ ] Sub-Processor dokumentiert
- [ ] Löschkonzept definiert
- [ ] Sicherheitsmaßnahmen dokumentiert

---

## Gate-Integration

```bash
# DSGVO-Check
./studio gate <project> --dsgvo

# Cookie-Banner-Check
./studio gate <project> --cookies

# Impressum-Check
./studio gate <project> --impressum
```

---

## Referenzen

- `.quinsy-studio/teams/03-compliance-legal/` — Compliance-Team
- `.quinsy-studio/process/human-in-the-loop.md` — HITL für Compliance-Entscheidungen
- `.quinsy-studio/process/gates.md` — Gate-Definitionen
