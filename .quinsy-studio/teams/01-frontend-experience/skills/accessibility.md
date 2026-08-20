# Skill: Accessibility

> WCAG 2.1 AA, Screenreader, Keyboard-Navigation, ARIA, Focus-Management

## Metadata

```
skill_id: FE-004
name: Accessibility (a11y)
team: 01-frontend-experience
lead_role: QA Specialist
support_roles: [Frontend Engineer, UI/Interaction Designer]
phases: [3, 4, 5]
activation_triggers:
  - Ticket enthält "a11y", "Barrierefreiheit", "Accessibility"
  - Phase 5 QA-Gate prüft Accessibility
  - Neue Komponente wird erstellt
  - Nutzer beschwert sich über Bedienbarkeit
```

---

## Verhaltensregeln

### 1. WCAG 2.1 AA Compliance

```markdown
Pflicht-Level (AA):
1. Wahrnehmbar: Alt-Texte, Kontraste, Skalierbar
2. Bedienbar: Keyboard-Navigation, keine Zeitlimits
3. Verständlich: Klare Labels, Fehlermeldungen
4. Robust: Semantische HTML, ARIA korrekt

Metriken:
  - Farbkontrast: min. 4.5:1 (Text), 3:1 (Large Text)
  - Text skalierbar bis 200% ohne horizontal Scroll
  - Alle interaktiven Elemente per Tastatur erreichbar
  - Focus-Indikator immer sichtbar
```

### 2. Semantische HTML

```markdown
Immer nutzen:
  - <nav> für Navigation
  - <main> für Hauptinhalt
  - <section> für inhaltliche Bereiche
  - <article> für eigenständige Inhalte
  - <header>, <footer> für Seitenbereiche
  - <button> für Aktionen (nicht <div onClick>)
  - <a> für Links (nicht <span onClick>)
  - <h1>-<h6> für Hierarchie (nicht überspringen!)
  - <ul>/<ol> für Listen
  - <table> für Tabellen mit <th>, <caption>
```

### 3. ARIA Labels

```markdown
Wann ARIA braucht:
  - Icon-Only Buttons: aria-label="Speichern"
  - Komplexe Widgets: aria-expanded, aria-selected
  - Live Regions: aria-live="polite" für dynamische Inhalte
  - Form-Fehler: aria-describedby für Fehlermeldungen

Niemals:
  - role="button" auf <div> (stattdessen <button>)
  - aria-label auf nicht-interaktiven Elementen
  - ARIA für Sachen die semantische HTML schon lösen
```

### 4. Keyboard-Navigation

```markdown
Tastatur-Shortcuts:
  - Tab: Zum nächsten interaktiven Element
  - Shift+Tab: Zum vorherigen Element
  - Enter/Space: Aktivieren von Buttons/Links
  - Escape: Modal schließen, Dropdown schließen
  - Pfeiltasts: Navigation in Listen/Menus

Focus-Management:
  - Focus-Indikator: sichtbar (min. 2px, kontrastreich)
  - Focus-Trap in Modals
  - Skip-Links für long pages
  - Focus-Reset nach Navigation
```

### 5. Screenreader-Unterstützung

```markdown
Prüfpunkte:
  - Alle Bilder haben alt-Text (oder alt="" für dekorativ)
  - Formulare haben assoziierte Labels
  - Fehlermeldungen sind per Screenreader hörbar
  - Dynamische Inhalte nutzen aria-live
  - Tabellen haben caption und th
  - Links haben aussagekräftigen Text (nicht "hier klicken")
  - Reihenfolge im DOM entspricht visueller Reihenfolge
```

### 6. Testing

```markdown
Tools:
  - axe-core (automatisiert)
  - Lighthouse Accessibility Audit
  - Screenreader-Testing (VoiceOver/NVDA)
  - Keyboard-only Navigation Test
  - Colour Contrast Analyser

Manuelle Checks:
  - Nur Tastatur: Alle Funktionen nutzbar?
  - Screenreader: Alle Inhalte verständlich?
  - Zoom 200%: Layout funktioniert?
  - High Contrast Mode: Alles sichtbar?
```

---

## Anti-Patterns

### ❌ Verboten

```markdown
- <div onClick> statt <button onClick>
- Fehlende alt-Texte bei Bildern
- Kein aria-label bei Icon-Buttons
- Fehlende Keyboard-Navigation
- Focus-Indikator nicht sichtbar (outline: none ohne Ersatz)
- Farbe als einzige Informationsquelle
- Zeitlimits ohne Möglichkeit zu verlängern
- Flackern (mehr als 3x pro Sekunde)
```

### ✅ Stattdessen

```markdown
- Semantische HTML-Elemente
- Aussagekräftige alt-Texte
- ARIA-Labels wo nötig
- Vollständige Keyboard-Support
- Sichtbarer Focus-Indikator
- Farbe + Icon/Text als Information
- Zeitlimits mit Verlängerungsmöglichkeit
- Keine Flackern-Animationen
```

---

## Referenzen

- `.quinsy-studio/knowledge-base/frontend_playbook.md` — Frontend-Regeln
- `.quinsy-studio/knowledge-base/design_playbook.md` — Design-Regeln
- `.quinsy-studio/process/gates.md` — a11y im Gate 5
