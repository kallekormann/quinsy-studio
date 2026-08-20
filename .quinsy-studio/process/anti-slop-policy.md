# Quinsy Studio — Anti-Slop-Policy

> AI-generierter Code hat charakteristische Muster, die manually geschriebenen Code schlechter machen.
> Diese Policy definiert die verbindlichen Regeln zur Vermeidung von AI-Slop.

## Grundprinzip

```
Kein AI-Slop im Production-Code.
Anti-Slop-Audit muss grün sein, bevor ein Gate bestanden gilt.
```

---

## Registrierung von Slop-Mustern

### Kategorie 1: Code-Slop (Schwere: Error)

| Regel | Muster | Erkennung |
|-------|--------|-----------|
| S1 | Unbenutzte Imports | `import .* from` ohne Nachweis |
| S2 | Unbenutzte Variablen | Deklariert aber nie referenziert |
| S3 | Dead Code | Unerreichbarer Code nach return/throw |
| S4 | Überflüssige Funktionen | Nie aufgerufen |
| S5 | Redundante Bedingungen | `if (x === true)` statt `if (x)` |
| S6 | Ungenutzte Parameter | Funktionsparameter ohne Nutzung |
| S7 | Übermäßige Verschachtelung | >4 Ebenen |

### Kategorie 2: Kommentar-Slop (Schwere: Warning)

| Regel | Muster | Erkennung |
|-------|--------|-----------|
| C1 | AI-typical Comments | "This function does X", "Here we..." |
| C2 | TODO ohne Owner/Datum | `// TODO` ohne `@name YYYY-MM-DD` |
| C3 | Auskommentierter Code | `// ... (alter Code)` |
| C4 | Überkommentierte Trivialitäten | Kommentar für `const x = 1` |

### Kategorie 3: Error-Handling-Slop (Schwere: Error)

| Regel | Muster | Erkennung |
|-------|--------|-----------|
| E1 | Catch-all | `catch (e) {}` oder `catch (e) { console.log(e) }` |
| E2 | Fehlende Error-Handling | Async-Funktion ohne try/catch |
| E3 | Swallowed Errors | Catch ohne throw/logging |
| E4 | Generic Messages | "An error occurred" ohne Details |

### Kategorie 4: Architectural-Slop (Schwere: Warning)

| Regel | Muster | Erkennung |
|-------|--------|-----------|
| A1 | Fehlende Abstraktion | Alles in einer Datei |
| A2 | Zirkuläre Abhängigkeiten | A → B → A |
| A3 | God-Functions | >100 Zeilen |
| A4 | Fehlende Typisierung | `any`/`unknown` ohne Notwendigkeit |
| A5 | Inconsistent Naming | camelCase und snake_case gemischt |

---

## Audit-Modus

```bash
# Full Audit
./studio gate <project> --anti-slop

# Nur Code-Slop
./studio gate <project> --anti-slop --category code

# Output als JSON
./studio gate <project> --anti-slop --json
```

---

## Vermeidungsstrategien

### Für Agenten

1. **Spezifische Anweisungen**
   ```
   ❌ "Schreibe eine Funktion die X macht"
   ✅ "Schreibe eine Funktion die X macht, mit Error-Handling für Y und Z"
   ```

2. **Code-Review einfordern**
   ```
   ❌ "Schreibe den Code"
   ✅ "Schreibe den Code und prüfe dann auf AI-Slop Muster"
   ```

3. **Best Practices nennen**
   ```
   ❌ (keine Vorgaben)
   ✅ "Nutze spezifische Error-Messages, vermeide catch-all"
   ```

### Für Humans

1. **PR-Review Checkliste**
   - [ ] Sind alle Imports benutzt?
   - [ ] Sind alle Variablen benutzt?
   - [ ] Gibt es unerreichbaren Code?
   - [ ] Sind Fehler spezifisch behandelt?
   - [ ] Sind Kommentare informativ (nicht triviell)?

2. **Automatisierung**
   - ESLint mit Custom Rules
   - TypeScript strict mode
   - Pre-commit hooks

---

## Integration mit Gates

Das Anti-Slop-Audit ist ein **verpflichtender Teil** von Gate 5 (QA-Gate):

```bash
./studio gate <project> --level 5
# Führt automatisch Anti-Slop-Audit durch
```

**Regel:** Ein Gate kann nicht grün sein, wenn das Anti-Slop-Audit Error-Verstöße hat.

---

## Änderungspolitik

Anti-Slop-Regeln können geändert werden:
1. Learning Item anlegen: `./studio learn "Regel X ist zu streng" --signal tooling-gap`
2. Im Meta-Retro besprechen
3. Entscheidung dokumentieren
4. CHANGELOG-Eintrag erstellen

---

## Referenzen

- `.quinsy-studio/process/gates.md` — Gate-Definitionen
- `.quinsy-studio/process/learning-loop.md` — Learning Loop
- `.quinsy-studio/teams/07-ai-autonomous-systems/` — Anti-Slop Team
