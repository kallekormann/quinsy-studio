# Quinsy Studio — Gates

> Jedes Gate ist ein Qualitäts-Schleusentor. Kein Gate wird manuell auf "grün" gesetzt — es wird automatisch geprüft.

## Gate-Philosophie

```
Gate = automatisierte Prüfung + menschliche Bestätigung
```

- **Automatisiert:** So viel wie möglich wird durch Tooling geprüft
- **Menschlich:** Irreversible Entscheidungen warten auf Freigabe
- **Kein bypass:** Ein Gate kann nicht übersprungen werden

---

## Gate 0 — Konzeptions-Gate

```bash
./studio gate <project> --level 0
```

### Prüfpunkte

| # | Prüfung | Methode | Gewicht |
|---|---------|---------|---------|
| 0.1 | PRD vorhanden | Datei-Check | Pflicht |
| 0.2 | PRD enthält: Problem, Zielgruppe, Scope, KPIs | Struktur-Check | Pflicht |
| 0.3 | Archetyp bestimmt | Feld-Check | Pflicht |
| 0.4 | Komplexitäts-Level geschätzt | Feld-Check | Pflicht |
| 0.5 | Mindestens 1 ADR vorhanden | Datei-Check | Pflicht |
| 0.6 | Offene Fragen dokumentiert | Inhalt-Check | Empfohlen |

### Gate-Ausgabe
```
Gate 0: Konzeption
━━━━━━━━━━━━━━━━━━
[✓] PRD vorhanden (docs/intake/prd.md)
[✓] Problem definiert
[✓] Zielgruppe definiert
[✓] Scope definiert (P0/P1/P2)
[✓] KPIs definiert
[✓] Archetyp: saas-application
[✓] Komplexität: P1
[✓] ADRs: 1 vorhanden
[~] Offene Fragen: 3 (dokumentiert)
━━━━━━━━━━━━━━━━━━
Ergebnis: GRÜN ✓
```

---

## Gate 1 — Validierungs-Gate

```bash
./studio gate <project> --level 1
```

### Prüfpunkte

| # | Prüfung | Methode | Gewicht |
|---|---------|---------|---------|
| 1.1 | Technisches Spike vorhanden | Datei-Check | Pflicht |
| 1.2 | Wettbewerbsanalyse vorhanden | Datei-Check | Pflicht |
| 1.3 | Technologie-Stack definiert | Feld-Check | Pflicht |
| 1.4 | Annahmen validiert | Inhalt-Check | Pflicht |
| 1.5 | Go/No-Go-Entscheidung dokumentiert | ADR-Check | Pflicht |

---

## Gate 2 — Architektur-Gate

```bash
./studio gate <project> --level 2
```

### Prüfpunkte

| # | Prüfung | Methode | Gewicht |
|---|---------|---------|---------|
| 2.1 | Architektur-Diagramm vorhanden | Datei-Check | Pflicht |
| 2.2 | Datenmodell definiert | Datei-Check | Pflicht |
| 2.3 | API-Spezifikation vorhanden | Datei-Check | Pflicht |
| 2.4 | Infrastruktur-Plan vorhanden | Datei-Check | Pflicht |
| 2.5 | Sicherheits-Architektur definiert | Inhalt-Check | Pflicht |
| 2.6 | Alle ADRs vorhanden | Datei-Count | Pflicht |

---

## Gate 3 — Design-Gate

```bash
./studio gate <project> --level 3
```

### Prüfpunkte

| # | Prüfung | Methode | Gewicht |
|---|---------|---------|---------|
| 3.1 | DESIGN.md vorhanden | Datei-Check | Pflicht |
| 3.2 | Design-Tokens definiert | Datei-Check | Pflicht |
| 3.3 | UI-Komponenten vorhanden | Verzeichnis-Check | Pflicht |
| 3.4 | Seitentypen definiert | Datei-Check | Pflicht |
| 3.5 | Farbmodus (dark/light) definiert | Inhalt-Check | Empfohlen |
| 3.6 | Animation-Definiert | Inhalt-Check | Empfohlen |

---

## Gate 4 — Implementierungs-Gate

```bash
./studio gate <project> --level 4
```

### Prüfpunkte

| # | Prüfung | Methode | Gewicht |
|---|---------|---------|---------|
| 4.1 | Tests grün (`pnpm test` / `npm test`) | Shell-Check | Pflicht |
| 4.2 | Build erfolgreich (`pnpm build`) | Shell-Check | Pflicht |
| 4.3 | Keine Critical/High Security-Issues | Dependency-Scan | Pflicht |
| 4.4 | TypeScript/ESLint ohne Errors | Linter-Check | Pflicht |
| 4.5 | Code-Review durchgeführt | Feld-Check | Empfohlen |

### Shell-Checks
```bash
# Test-Check
pnpm test -- --reporter=json 2>/dev/null | jq '.numFailedTests == 0'

# Build-Check
pnpm build 2>&1 | tail -1 | grep -q "Successfully"

# Lint-Check
pnpm lint 2>&1 | grep -q "0 errors"
```

---

## Gate 5 — QA-Gate (Das strengste Gate)

```bash
./studio gate <project> --level 5
```

### Prüfpunkte

| # | Prüfung | Methode | Gewicht |
|---|---------|---------|---------|
| 5.1 | Alle E2E-Tests grün | Shell-Check | Pflicht |
| 5.2 | Core Web Vitals im Budget | Performance-Check | Pflicht |
| 5.3 | Lighthouse Score ≥ 90 | Shell-Check | Pflicht |
| 5.4 | Keine Critical/High Security-Issues | OWASP-Scan | Pflicht |
| 5.5 | DSGVO-konform | Compliance-Check | Pflicht |
| 5.6 | Anti-Slop-Audit: 0 Verstöße | Anti-Slop-Check | Pflicht |
| 5.7 | Barrierefreiheit geprüft | a11y-Check | Pflicht |
| 5.8 | Cross-Browser getestet | Feld-Check | Empfohlen |

### Anti-Slop-Audit (Detail)
```bash
./studio gate <project> --anti-slop
```

Prüft auf:
- Überflüssige Variablen, unnötige Imports
- Dead Code
- Übermäßige Kommentare (AI-typical verbose patterns)
- Ungewöhnliche Code-Muster (z.B. `// This function does X`)
- Fehlende Error-Handling
- Ungenutzte Dependencies

---

## Gate 6 — Release-Gate

```bash
./studio gate <project> --level 6
```

### Prüfpunkte

| # | Prüfung | Methode | Gewicht |
|---|---------|---------|---------|
| 6.1 | Deployment erfolgreich | Feld-Check | Pflicht |
| 6.2 | Monitoring aktiv | Feld-Check | Pflicht |
| 6.3 | Rollback-Strategie vorhanden | Datei-Check | Pflicht |
| 6.4 | Release-Notes vorhanden | Datei-Check | Pflicht |
| 6.5 | Smoke-Tests bestanden | Feld-Check | Pflicht |

---

## Gate-Status

Jedes Gate hat einen von vier Status:

| Status | Bedeutung |
|--------|-----------|
| `offen` | Noch nicht geprüft |
| `rot` | Prüfung fehlgeschlagen (Fix nötig) |
| `grün` | Prüfung bestanden |
| `blockiert` | Wartet auf menschliche Entscheidung |

---

## Gate-History

Die Gate-Historie wird in `status.json` des Projekts protokolliert:

```json
{
  "gate_history": [
    {
      "gate": 0,
      "status": "grün",
      "passed_at": "2026-08-19T10:00:00Z",
      "checked_by": "studio-cli"
    },
    {
      "gate": 1,
      "status": "rot",
      "failed_at": "2026-08-19T11:00:00Z",
      "reason": "Wettbewerbsanalyse fehlt"
    }
  ]
}
```

---

##Referenzen

- `.quinsy-studio/process/anti-slop.md` — Anti-Slop-Audit im Detail
- `.quinsy-studio/process/lifecycle.md` — Überblick über alle Phasen
- `./studio gate <project>` — Gate ausführen
