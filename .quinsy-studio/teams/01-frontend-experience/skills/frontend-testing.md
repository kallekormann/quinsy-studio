# Skill: Frontend Testing

> Unit-Tests, Integration-Tests, E2E-Tests, Visual Regression, Snapshot-Tests

## Metadata

```
skill_id: FE-006
name: Frontend Testing
team: 01-frontend-experience
lead_role: QA Specialist
support_roles: [Frontend Engineer]
phases: [4, 5]
activation_triggers:
  - Ticket enthält "Test", "Testing", "Coverage"
  - Phase 4: TDD während Implementierung
  - Phase 5: QA-Gate prüft Test-Coverage
  - Reuse-Review: Komponente braucht Tests für Library
```

---

## Verhaltensregeln

### 1. Test-Pyramide

```markdown
        ╱╲
       ╱ E2E ╲           ← 10% (wenige, kritische Pfade)
      ╱────────╲
     ╱ Integration ╲      ← 30% (Komponenten-Zusammenspiel)
    ╱────────────────╲
   ╱     Unit Tests    ╲  ← 60% (schnell, isoliert)
  ╱────────────────────╲

Coverage-Minimum:
  - Statements: > 80%
  - Branches: > 75%
  - Functions: > 80%
  - Lines: > 80%
```

### 2. Unit-Tests (Vitest/Jest)

```markdown
Was testen:
  - Komponenten-Rendering mit verschiedenen Props
  - Event-Handler (onClick, onChange)
  - Bedingte Rendering-Logik
  - Utility-Funktionen
  - Custom Hooks

Wie testen:
  - render() mit Testing Library
  - userEvent für Interaktionen
  - screen.getBy* für Element-Suche
  - expect() für Assertions

Naming:
  describe('ComponentName', () => {
    it('should render with default props', () => {})
    it('should handle click event', () => {})
    it('should be accessible', () => {})
  })
```

### 3. Integration-Tests

```markdown
Was testen:
  - Komponenten-Zusammenspiel
  - Form-Submission mit Validierung
  - API-Integration (gemockt)
  - Navigation zwischen Pages
  - Theme/Context Provider
```

### 4. E2E-Tests (Playwright)

```markdown
Was testen:
  - Kritische User Journeys
  - Login/Logout Flow
  - Checkout/Conversion Flow
  - Form-Submission mit Backend
  - Multi-Step-Workflows

Nur kritische Pfade — nicht jeden Button!
```

### 5. Visual Regression

```markdown
Tools: Chromatic / Percy / Playwright Snapshots

Was testen:
  - Komponenten in allen Varianten
  - Responsive Breakpoints
  - Dark/Light Mode
  - Hover/Focus/Active States
```

### 6. TDD-Workflow

```markdown
1. RED:    Test schreiben der fehlschlägt
2. GREEN:  Code schreiben der Test besteht
3. REFACTOR: Code bereinigen, Tests bleiben grün
```

---

## Anti-Patterns

### ❌ Verboten

```markdown
- Tests die nur prüfen ob Komponente rendert
- Kein Test für Error-Zustände
- Snapshot-Tests die zu oft aktualisiert werden
- Tests die von externen Services abhängen
- Kein Test für Accessibility
- Mocks die zu viel verstecken
```

### ✅ Stattdessen

```markdown
- Tests für alle States (loading, error, success, empty)
- Error-Zustände explizit testen
- Integration-Tests statt zu vieler Snapshots
- API-Mocks mit MSW (Mock Service Worker)
- axe-core Integration in Tests
- Einfache, verständliche Mocks
```

---

## Referenzen

- `.quinsy-studio/knowledge-base/frontend_playbook.md` — Frontend-Regeln
- `.quinsy-studio/process/ticket-workflow.md` — Schritt 5 (Selbstprüfung)
- `./studio gate <project> --tests` — Test-Coverage prüfen
