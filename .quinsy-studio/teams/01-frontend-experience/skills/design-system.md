# Skill: Design System

> Design Tokens, Typografie, Farbpalette, Spacing-System, Theme-Management

## Metadata

```
skill_id: FE-002
name: Design System Management
team: 01-frontend-experience
lead_role: UI/Interaction Designer
support_roles: [Frontend Architect, Frontend Engineer]
phases: [2, 3]
activation_triggers:
  - Neues Projekt wird initialisiert (Phase 2/3)
  - Design Tokens müssen definiert/aktualisiert werden
  - Farbpalette oder Typografie wird geändert
  - Dark/Light Mode muss implementiert werden
  - Asset wird zur Studio-Library promoted
```

---

## Verhaltensregeln

### 1. Design Tokens Hierarchie

```markdown
Globale Tokens (Studio-HQ):
  → studio-library/ui/tokens/design-tokens.json
  → Gelten für ALLE Projekte

Lokale Tokens (Projekt):
  → projects/[name]/ui/tokens/
  → Können Globale überschreiben (Project-Specific)
```

### 2. Token-Struktur

```markdown
Jeder Token hat:
- Kategorie: color, typography, spacing, shadow, border, breakpoint
- Name: konsistente Benennung (color-primary-500)
- Wert: JSON-kompatibel
- Dark Mode: eigener Wert oder Alias
- Beschreibung: was der Token repräsentiert
```

### 3. Typografie-Skala

```markdown
Standard-Skala (rem-basiert):

Display:    3rem / 48px  — Headline Hero
H1:         2.25rem / 36px
H2:         1.875rem / 30px
H3:         1.5rem / 24px
H4:         1.25rem / 20px
Body-LG:    1.125rem / 18px
Body:       1rem / 16px      ← Base
Body-SM:    0.875rem / 14px
Caption:    0.75rem / 12px

Line-Heights:
  Tight:   1.25 (Headlines)
  Normal:  1.5  (Body)
  Relaxed: 1.75 (Long-form)
```

### 4. Farbpalette

```markdown
Struktur pro Farbe:
  - 50:  Hintergrund (lightest)
  - 100: Light
  - 200: Light
  - 300: Medium-Light
  - 400: Medium
  - 500: Primary (Standard)
  - 600: Medium-Dark
  - 700: Dark
  - 800: Dark
  - 900: Darkest
  - A100-A700: Accent

Basis-Farben:
  - primary: Markenfarbe
  - neutral: Grautöne
  - success: Erfolg
  - warning: Warnung
  - error: Fehler
  - info: Information
```

### 5. Spacing-System

```markdown
8px Grid als Basis:

space-0:   0px
space-1:   4px     (0.25rem)
space-2:   8px     (0.5rem)    ← Base Unit
space-3:   12px    (0.75rem)
space-4:   16px    (1rem)
space-5:   20px    (1.25rem)
space-6:   24px    (1.5rem)
space-8:   32px    (2rem)
space-10:  40px    (2.5rem)
space-12:  48px    (3rem)
space-16:  64px    (4rem)
space-20:  80px    (5rem)
space-24:  96px    (6rem)
```

### 6. Promotion zur Studio-Library

```markdown
Wann promoven?
- Komponente ist in 2+ Projekten identisch
- Design-Entscheidung ist universell
- Token ist project-agnostic

Wie promoven?
1. Code in studio-library/ kopieren
2. README.md mit Dokumentation versehen
3. manifest.json aktualisieren
4. CHANGELOG.md eintragen
```

---

## Anti-Patterns

### ❌ Verboten

```markdown
- Hardcoded Farben in Komponenten (statt Tokens)
- Pixel-Werte statt rem/em
- Einzelne Fonts laden (statt Font-Family)
- Kein Dark Mode (wenn Projekt ihn braucht)
- Tokens direkt in CSS (statt JSON als Source of Truth)
- Keine Konsistenz zwischen Projekten
```

### ✅ Stattdessen

```markdown
- Immer Design Tokens nutzen
- rem/em für alles
- Font-Family mit Fallbacks
- Dark Mode über CSS Custom Properties
- Tokens als JSON + CSS Custom Properties generieren
- Globale Tokens aus Studio-HQ, lokale Overrides
```

---

## Externe Skill-Unterstützung

> Vor der Umsetzung die importierten Best-in-Class-Skills laden (`./studio update-skills`):

- **`design/skills/`** (Nutlope/hallmark) — Anti-AI-Slop-Design: Macrostructure-Auswahl, 57 Slop-Test-Gates, Themes. **Pflicht vor jedem neuen UI-Entwurf.**
- **`design_awesome/skills/<stil>/SKILL.md`** (bergside/awesome-design-skills) — 67 Design-System-Styles (Corporate, Minimal, Glassmorphism, ...) mit SKILL.md + DESIGN.md

Ablauf: Stil aus `design_awesome` wählen → `design` (hallmark) Slop-Test laufen lassen → Tokens definieren → Promotion prüfen.

## Referenzen

- `.quinsy-studio/studio-library/ui/tokens/` — Token-Dateien
- `.quinsy-studio/studio-library/manifest.json` — Registrierung
- `.quinsy-studio/knowledge-base/design_playbook.md` — Design-Regeln
