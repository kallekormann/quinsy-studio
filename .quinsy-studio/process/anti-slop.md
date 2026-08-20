# Quinsy Studio — Anti-Slop-Audit

> AI-generierter Code hat charakteristische Muster, die manually geschriebenen Code schlechter machen.
> Das Anti-Slop-Audit erkennt und verhindert diese Muster.

## Was ist AI-Slop?

AI-Slop sind Code-Muster, die typischerweise von LLMs generiert werden und die Code-Qualität verschlechtern:

```
- Überflüssige Variablen und Imports
- Overly verbose Funktionen
- Generic error handling (catch-all)
- Fehlende spezifische Fehlermeldungen
- Überkommentierter Code
- Unused parameters
- Redundante Logik
- Fehlende Edge-Case-Behandlung
- "Helper"-Funktionen die nirgends aufgerufen werden
```

---

## Audit-Regeln

### Kategorie 1: Code-Slop

| Regel | Beschreibung | Schwere |
|-------|-------------|---------|
| S1 | Unbenutzte Imports | Warning |
| S2 | Unbenutzte Variablen | Warning |
| S3 | Dead Code (unerreichbarer Code) | Error |
| S4 | Überflüssige Funktionen (nie aufgerufen) | Error |
| S5 | Redundante Bedingungen | Warning |
| S6 | Ungenutzte Funktionparameter | Warning |
| S7 | Übermäßige Verschachtelung (>4 Ebenen) | Warning |

### Kategorie 2: Kommentar-Slop

| Regel | Beschreibung | Schwere |
|-------|-------------|---------|
| C1 | AI-typical Comments ("This function does X") | Warning |
| C2 | TODO-Kommentare ohne Owner/Datum | Info |
| C3 | Auskommentierter Code | Warning |
| C4 | Überkommentierte triviale Funktionen | Warning |

### Kategorie 3: Error-Handling-Slop

| Regel | Beschreibung | Schwere |
|-------|-------------|---------|
| E1 | Catch-all ohne spezifische Behandlung | Error |
| E2 | Fehlende Error-Handling | Error |
| E3 | Swallowed Errors (catch ohne logging/throw) | Error |
| E4 | Generic Error-Messages | Warning |

### Kategorie 4: Architectural-Slop

| Regel | Beschreibung | Schwere |
|-------|-------------|---------|
| A1 | Fehlende Abstraktionsschichten | Warning |
| A2 | Zirkuläre Abhängigkeiten | Error |
| A3 | God-Functions (>100 Zeilen) | Warning |
| A4 | Fehlende Typisierung (any/unknown) | Warning |
| A5 | Inconsistent Naming | Warning |

### Kategorie 5: Dependency-Slop

| Regel | Beschreibung | Schwere |
|-------|-------------|---------|
| D1 | Unused Dependencies | Warning |
| D2 | Duplicate Dependencies | Error |
| D3 | Deprecated Dependencies | Warning |
| D4 | Overly Broad Dependencies | Info |

---

## Audit-Tool

```bash
# Full Anti-Slop-Audit
./studio gate <project> --anti-slop

# Nur spezifische Kategorie
./studio gate <project> --anti-slop --category code
./studio gate <project> --anti-slop --category comments

# Output als JSON (für CI/CD)
./studio gate <project> --anti-slop --json
```

### Audit-Output

```
Anti-Slop-Audit: nudge
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Code-Slop:
  [!] S2: Unbenutzte Variable (src/utils/helpers.ts:42)
  [!] S5: Redundante Bedingung (src/app/page.tsx:18)

Comment-Slop:
  [~] C1: AI-typical Comment (src/components/Button.tsx:12)

Error-Handling:
  [!] E1: Catch-all (src/app/api/route.ts:23)
  [!] E3: Swallowed Error (src/lib/db.ts:67)

Architectural-Slop:
  [!] A3: God-Function (src/services/auth.ts:234)
  [!] A4: Fehlende Typisierung (src/types.ts:15)

Dependency-Slop:
  [~] D1: Unused Dependency (package.json: "left-pad")
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Verstöße: 7 (4 Error, 3 Warning)
Ergebnis: ROT ✗
```

---

## Audit-Report

Nach jedem Audit wird ein Report generiert:

```
<project>/docs/anti-slop/
├── latest.md                 # Aktueller Report
├── history/
│   ├── 2026-08-19.md
│   └── ...
```

### Report-Template

```markdown
# Anti-Slop-Audit Report — YYYY-MM-DD

## Zusammenfassung
- Verstöße: X (Y Error, Z Warning)
- Verbessert seit letztem Audit: +/- N
- Trend: 📈/📉/➡️

## Verstöße nach Kategorie

### Code-Slop (X)
| Datei | Regel | Beschreibung |
|-------|-------|-------------|
| ... | ... | ... |

### Comment-Slop (X)
...

### Error-Handling (X)
...

### Architectural-Slop (X)
...

### Dependency-Slop (X)
...

## Empfohlene Aktionen
1. [Error] Behebe kritische Verstöße zuerst
2. [Warning] Plane Tech-Debt-Reduktion
3. [Info] Überprüfe bei nächster Gelegenheit

## Trend
| Datum | Verstöße | Veränderung |
|-------|----------|-------------|
| 2026-08-19 | 12 | (Erstes Audit) |
| 2026-08-20 | 7 | -5 ✓ |
```

---

## Vermeidungsstrategien

### Für Agenten/Copilot

```markdown
## Prompt-Engineering gegen Slop

1. Spezifische Anweisungen geben
   ❌ "Schreibe eine Funktion die X macht"
   ✅ "Schreibe eine Funktion die X macht, mit Error-Handling für Y und Z"

2. Code-Review einfordern
   ❌ "Schreibe den Code"
   ✅ "Schreibe den Code und prüfe dann auf AI-Slop Muster"

3. Best Practices nennen
   ❌ (keine Vorgaben)
   ✅ "Nutze spezifische Error-Messages, vermeide catch-all"
```

### Für Reviews

```markdown
## Code-Review Checkliste gegen Slop

- [ ] Sind alle Imports benutzt?
- [ ] Sind alle Variablen benutzt?
- [ ] Gibt es unerreichbaren Code?
- [ ] Gibt es überflüssige Funktionen?
- [ ] Sind Fehler spezifisch behandelt?
- [ ] Sind Kommentare informativ (nicht triviell)?
- [ ] Sind Funktionen nicht zu lang (<100 Zeilen)?
```

---

## Integration mit Gates

Das Anti-Slop-Audit ist ein **verpflichtender Teil** von Gate 5 (QA-Gate):

```bash
./studio gate <project> --level 5
# Führt automatisch Anti-Slop-Audit durch
```

**Regel:** Ein Gate kann nicht grün sein, wenn das Anti-Slop-Audit Error-Verstöße hat.

---

## Referenzen

- `.quinsy-studio/process/gates.md` — Gate-Definitionen
- `.quinsy-studio/process/lifecycle.md` — Phase 5 (QA)
- `./studio gate <project> --anti-slop` — Audit ausführen
