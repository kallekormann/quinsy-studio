# Anti-AI-Slop Protocol

> Absolute Blacklist für AI-generierten Code. Kein Verstoß ist akzeptabel.

## Grundprinzip

```
AI-Slop = Code der funktioniert, aber schlecht ist.
Anti-Slop = Code der funktioniert UND gut ist.
```

---

## ABSOLUTE BLACKLIST (Sofortiger Rejection)

### Text-Floskeln (Kommentare, Variablen, Funktionen)

| # | Verboten | Grund |
|---|----------|-------|
| T1 | "This function does X" | Trivial, nicht informativ |
| T2 | "Here we..." | Conversational, unprofessionell |
| T3 | "Let's..." / "Let me..." | AI-typical |
| T4 | "Note that..." | Überflüssig |
| T5 | "It's important to..." | Obvious |
| T6 | "Basically..." / "Simply..." | Herablassend |
| T7 | "In this case..." | Redundant |
| T8 | "As we can see..." | AI-typical |
| T9 | "This is a..." | AI-typical |
| T10 | "We need to..." | Imperative AI |

### Code-Muster

| # | Verboten | Grund |
|---|----------|-------|
| C1 | `catch (e) {}` | Swallowed Error |
| C2 | `catch (e) { console.log(e) }` | Debug-Code |
| C3 | `if (x === true)` | Redundant |
| C4 | `const result = await fn(); return result;` | Überflüssig |
| C5 | `// Initialize` / `// Setup` | Triviale Kommentare |
| C6 | Funktion >100 Zeilen | God Function |
| C7 | >4 Ebenen Verschachtelung | Cognitive Overload |
| C8 | `any` / `unknown` ohne Notwendigkeit | Fehlende Typisierung |
| C9 | Ungenutzte Imports/Variablen | Dead Code |
| C10 | Doppelte Logik | Redundanz |

---

## VERBOTENE UI-MUSTER

### Freies LLM-Styling

| # | Verboten | Stattdessen |
|---|----------|-------------|
| U1 | Inline-Styles | Design Tokens / Tailwind |
| U2 | Hardcoded Farben | CSS Custom Properties |
| U3 | Freie Font-Auswahl | Definierte Typografie-Skala |
| U4 |beliebige Border-Radius | Token-basierte Radii |
| U5 | Freie Shadows | Definierte Shadow-Skala |

### Struktur

| # | Verboten | Stattdessen |
|---|----------|-------------|
| U6 | `div` statt semantischer Elemente | `<button>`, `<nav>`, `<article>` |
| U7 | Fehlende `alt`-Texte | Beschreibende Alternativtexte |
| U8 | Fehlende Keyboard-Navigation | Vollständiger Tab-Reihenfolge |
| U9 | Fehlende ARIA-Labels | Spezifische Labels |
| U10 | Farben ohne Kontrast-Check | WCAG AA Minimum |

---

## VERBOTENE BACKEND-MUSTER

| # | Verboten | Stattdessen |
|---|----------|-------------|
| B1 | Secrets im Code | Environment Variables |
| B2 | SQL-Injection (String Concat) | Prepared Statements / ORM |
| B3 | Fehlende Input-Validierung | Zod / Joi / class-validator |
| B4 | Catch-all Error-Handling | Spezifische Error-Typen |
| B5 | Synchroner Code in Async | Vollständige Async-Kette |
| B6 | Fehlende Rate-Limiting | Express-Rate-Limit / Middleware |
| B7 | Kein CORS-Setup | Explizite Origin-Whitelist |
| B8 | Fehlende Security-Headers | Helmet / Custom Headers |

---

## ERZWINGUNG

### In der Entwicklung

```bash
# Anti-Slop-Check vor jedem Commit
python3 .quinsy-studio/studio-tools/validate_anti_slop.py .

# Bei Verstoß: Commit wird abgebrochen
```

### Im QA-Gate

```bash
# Anti-Slop-Audit als Teil des Gates
./studio gate <project> --anti-slop

# Gate kann nicht grün sein bei Error-Verstößen
```

### Im Code-Review

```markdown
## Anti-Slop Checkliste

- [ ] Keine Text-Floskeln (T1-T10)
- [ ] Keine Code-Muster (C1-C10)
- [ ] Keine UI-Muster (U1-U10)
- [ ] Keine Backend-Muster (B1-B8)
```

---

## AUSNAHMEN (nur mit ADR)

Manchmal ist AI-Slop unvermeidbar:
- Expliziter ADR dokumentiert die Ausnahme
- Risiko-Bewertung durchgeführt
- Tech-Debt-Ticket angelegt
- Zeitrahmen für Bereinigung definiert

---

## Referenzen

- `.quinsy-studio/process/anti-slop.md` — Audit-Tool
- `.quinsy-studio/process/anti-slop-policy.md` — Verbindliche Regeln
- `.quinsy-studio/teams/07-ai-autonomous-systems/` — Anti-Slop Team
