# Skill: UI Component Design

> Atomic Design, TypeScript, Props-API, Storybook-Dokumentation

## Metadata

```
skill_id: FE-001
name: UI Component Design
team: 01-frontend-experience
lead_role: Frontend Engineer
support_roles: [UI/Interaction Designer, QA Specialist]
phases: [3, 4, 5]
activation_triggers:
  - Ticket enthält "Komponente", "Component", "UI-Element"
  - Neues UI-Feature wird implementiert
  - Design System wird erweitert
  - Reuse-Review identifiziert wiederverwendbare Komponente
```

---

## Verhaltensregeln

### 1. Atomic Design Hierarchie

```markdown
Jede Komponente wird dem richtigen Level zugeordnet:

ATOMS (kleinste Einheit):
  - Button, Input, Badge, Icon, Avatar, Checkbox, Radio, Switch
  - Props: variant, size, disabled, loading, icon
  - Keine internen Abhängigkeiten zu anderen Komponenten

MOLECULES (Kombination aus Atoms):
  - Card, Form, Modal, Dropdown, SearchBar, FormField
  - Bestehen aus 2+ Atoms
  - Haben eine spezifische Funktion

ORGANISMS (komplexe Bereiche):
  - Header, Footer, Sidebar, Navigation, DataTable, Hero
  - Bestehen aus Molecules + Atoms
  - Erobern einen ganzen View-Bereich

TEMPLATES (Seiten-Layouts):
  - Seiten-Layouts ohne konkrete Inhalte
  - Definieren die Informationsarchitektur

PAGES (konkrete Implementierungen):
  - Templates befüllt mit echten Daten
```

### 2. Komponenten-Spezifikation

```markdown
Jede Komponente MUSS folgende Dateien erhalten:

src/components/{name}/
  ├── index.ts              # Public API (Named Exports)
  ├── {name}.tsx            # Implementierung
  ├── {name}.test.tsx       # Unit-Tests
  ├── {name}.stories.tsx    # Storybook-Dokumentation
  └── {name}.types.ts       # TypeScript-Typen (falls komplex)
```

### 3. Props-Design

```markdown
Regeln für Props:

1. Konsistente Naming:
   - Boolean props: is{State} oder has{Property} (isDisabled, hasIcon)
   - Event handlers: on{Event} (onClick, onChange)
   - Content props: children oder spezifisch (label, title)
   - Layout props: align, direction, gap

2. Sensible Defaults:
   - Alle props mit Ausnahme von children haben Defaults
   - Defaults sind in der Dokumentation sichtbar

3. TypeScript:
   - Props sind explizit getypt (keine any)
   - Union Types für Varianten
   - Optional props mit ? markiert

4. Ref forwarding:
   - Komponenten die auf DOM-Elemente zugreifen, leiten refs weiter
```

### 4. Styling Rules

```markdown
1. Tailwind CSS als Primär-Styling
2. CSS Custom Properties für Theme-Variablen
3. Keine Inline-Styles (außer dynamische Werte)
4. Responsive: Mobile-First (sm:, md:, lg:, xl:)
5. Dark Mode: über CSS Custom Properties / Theme
6. Animationen: nur GPU-beschleunigt (transform, opacity)
```

### 5. Storybook Rules

```markdown
Jede Komponente hat:
- Default Story
- Alle Varianten als eigene Stories
- Empty State Story (falls relevant)
- Disabled State Story
- Loading State Story
- Mobile Viewport Story
```

---

## Anti-Patterns

### ❌ Verboten

```markdown
- Inline-Styles statt Tailwind
- div statt semantischer HTML-Elemente (button, nav, main, section)
- Fehlende aria-Labels bei interaktiven Elementen
- Hardcoded Farben statt Design Tokens
- Komponente mit >20 Props (zu komplex — aufteilen!)
- Keine TypeScript-Typen
- Kein Default Export (nur Named Exports)
- CSS-in-JS ohne zwingenden Grund
-任何 styles die nicht responsive sind
```

### ✅ Stattdessen

```markdown
- Tailwind + CSS Custom Properties
- Semantische HTML-Elemente
- ARIA-Labels wo nötig
- Design Tokens (.quinsy-studio/studio-library/ui/tokens/)
- Props aufteilen in Sub-Komponenten
- Volle TypeScript-Typisierung
- Named Exports (barrel exports via index.ts)
- Tailwind für Fast-Path, CSS Modules für komplexe Animationen
- Mobile-First Responsive Design
```

---

## Qualitäts-Checkliste

- [ ] Komponente ist generisch und konfigurierbar
- [ ] TypeScript-Typen sind vollständig
- [ ] Props haben sinnvolle Defaults
- [ ] Storybook-Dokumentation vorhanden
- [ ] Unit-Tests vorhanden
- [ ] Barrierefreiheit geprüft (a11y)
- [ ] Responsive (Mobile-First)
- [ ] Dark/Light Mode unterstützt
- [ ] Performance im Budget (kein unnötiges Re-Rendering)
- [ ] Kein AI-Slop im Code
- [ ] Semantische HTML-Elemente verwendet
- [ ] Ref-Forwarding implementiert (bei Bedarf)

---

## Externe Skill-Unterstützung

> Vor der Umsetzung die importierten Best-in-Class-Skills laden (`./studio update-skills`):

- **`design/skills/`** (Nutlope/hallmark) — `hallmark audit` vor UI-Review, `hallmark build` für neue Entwürfe (57 Slop-Gates).
- **`design_awesome/skills/<stil>/SKILL.md`** (bergside) — konkrete Stil-Guides für Komponenten (Corporate, Minimal, ...)
- **`all_domains/design-and-ui-ux/frontend-design`** — generischer Frontend-Design-Workflow

Ablauf: Komponente bauen → `hallmark audit` laufen lassen → Slop-Verstöße fixen → Storybook + Tests.

## Referenzen

- `.quinsy-studio/studio-library/ui/tokens/` — Design Tokens
- `.quinsy-studio/studio-library/ui/components/` — Bestehende Komponenten
- `.quinsy-studio/knowledge-base/design_playbook.md` — Design-Regeln
- `.quinsy-studio/knowledge-base/frontend_playbook.md` — Frontend-Regeln
- `.quinsy-studio/knowledge-base/anti_ai_slop_protocol.md` — Anti-Slop
