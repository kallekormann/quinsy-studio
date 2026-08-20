# Design Playbook

> UX-Heuristiken, Cognitive Load Theory, 8pt Grid, Typografie — die globalen Design-Standards.

## Grundprinzip

```
Design ist nicht wie es aussieht.
Design ist wie es funktioniert.
— Steve Jobs
```

---

## UX-Heuristiken (Nielsen/Norman)

| # | Heuristik | Beschreibung | Umsetzung |
|---|-----------|-------------|-----------|
| 1 | **Sichtbarer Systemstatus** | User weiß immer was passiert | Loading-States, Feedback |
| 2 | **System der realen Welt** | Sprache der User, nicht der Technik | Klare Labels, Icons |
| 3 | **User-Kontrolle** | Undo, Back, Cancel | Immer möglich |
| 4 | **Konsistenz & Standards** | Erwartungsgemäßes Verhalten | Design System |
| 5 | **Fehlervermeidung** | Design verhindert Fehler | Guards, Confirmations |
| 6 | **Erkennung statt Erinnerung** | Sichtbare Optionen | Dropdowns > Freitext |
| 7 | **Flexibilität & Effizienz** | Keyboard Shortcuts für Power-User | Accelerators |
| 8 | **Ästhetik & Minimalismus** | Weniger ist mehr | Progressive Disclosure |
| 9 | **Fehlererkennung & -hilfe** | Klare Fehlermeldungen | Spezifische Messages |
| 10 | **Hilfe & Dokumentation** | Hilfe readily available | Tooltips, Context-Help |

---

## Cognitive Load Theory

### Drei Arten von Cognitive Load

| Typ | Beschreibung | Reduzierung |
|-----|-------------|-------------|
| **Intrinsic** | Schwierigkeit der Aufgabe selbst | Vereinfachen, Schritt-für-Schritt |
| **Extraneous** | Schlechtes Design | Klare Struktur, Redundanz vermeiden |
| **Germane** | Lern- und Verstehensprozess | Muster, Konsistenz, Feedback |

### Umsetzung

```
✅ Progressive Disclosure (nicht alles auf einmal)
✅ Chunking (Informationen in Gruppen)
✅ Visuelle Hierarchie (Wichtiges zuerst)
✅ Weißraum (Atmen lassen)
✅ Konsistente Muster (Wiedererkennung)
```

---

## 8pt Grid System

```
Grundeinheit: 8px

Spacing Scale:
  xs:  4px   (0.5 × 8)
  sm:  8px   (1 × 8)
  md:  16px  (2 × 8)
  lg:  24px  (3 × 8)
  xl:  32px  (4 × 8)
  2xl: 48px  (6 × 8)
  3xl: 64px  (8 × 8)
```

### Anwendung

- **Padding:** Immer Vielfaches von 8
- **Margin:** Immer Vielfaches von 8
- **Icon-Größen:** 16, 24, 32, 48
- **Border-Radius:** 4, 8, 12, 16, 999 (pill)
- **Font-Size:** Nicht am Grid, aber Line-Height: 1.5 (Body), 1.2 (Headings)

---

## Typografie-System

### Skala

```css
--text-xs:   0.75rem;   /* 12px */
--text-sm:   0.875rem;  /* 14px */
--text-base: 1rem;      /* 16px */
--text-lg:   1.125rem;  /* 18px */
--text-xl:   1.25rem;   /* 20px */
--text-2xl:  1.5rem;    /* 24px */
--text-3xl:  1.875rem;  /* 30px */
--text-4xl:  2.25rem;   /* 36px */
--text-5xl:  3rem;      /* 48px */
```

### Font-Stack

```css
--font-sans: 'Inter', system-ui, -apple-system, sans-serif;
--font-mono: 'JetBrains Mono', 'Fira Code', monospace;
```

### Hierarchie

| Element | Size | Weight | Line-Height |
|---------|------|--------|-------------|
| Display | 48px | 800 | 1.1 |
| H1 | 36px | 700 | 1.2 |
| H2 | 24px | 600 | 1.3 |
| H3 | 20px | 600 | 1.4 |
| Body | 16px | 400 | 1.5 |
| Small | 14px | 400 | 1.5 |
| Caption | 12px | 400 | 1.5 |

---

## Farb-System

### Prinzip

```
60-30-10 Regel:
  60% — Dominante Farbe (Background)
  30% — Sekundäre Farbe (Text, Borders)
  10% — Akzentfarbe (CTAs, Highlights)
```

### Kontraste

| Element | Mindest-Kontrast |
|---------|-----------------|
| Normal Text | 4.5:1 (WCAG AA) |
| Large Text | 3:1 (WCAG AA) |
| UI Components | 3:1 (WCAG AA) |
| Focus Indicators | 3:1 (WCAG AA) |

---

## Responsive Breakpoints

| Breakpoint | Width | Layout |
|------------|-------|--------|
| Mobile | < 640px | Single Column, Full-Width |
| Tablet | 640-1024px | 2 Columns |
| Desktop | > 1024px | Centered Content (max-width: 640-800px) |

### Mobile-First

```css
/* Base: Mobile */
.element { padding: 16px; }

/* Tablet */
@media (min-width: 640px) {
  .element { padding: 24px; }
}

/* Desktop */
@media (min-width: 1024px) {
  .element { padding: 32px; max-width: 640px; margin: 0 auto; }
}
```

---

## Animation-Prinzipien

### 12 Prinzipien der Animation (Disney)

1. **Squash & Stretch** — Gewicht und Trägheit
2. **Anticipation** — Vorbereitung auf Bewegung
3. **Staging** — Aufmerksamkeit lenken
4. **Straight Ahead & Pose to Pose** — Timing
5. **Follow Through & Overlapping Action** — Nachlauf
6. **Slow In & Slow Out** — Ease
7. **Arcs** — Natürliche Bewegungen
8. **Secondary Action** — Begleitende Bewegung
9. **Timing** — Geschwindigkeit
10. **Exaggeration** — Betonung
11. **Solid Drawing** — 3D in 2D
12. **Appeal** — Sympathie

### CSS-Äquivalente

```css
/* Spring Physics */
transition: transform 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);

/* Smooth Ease */
transition: opacity 0.2s ease-in-out;

/* GPU-beschleunigt */
transform: translateZ(0); /* oder will-change: transform */
```

---

## Barrierefreiheit (a11y)

### WCAG 2.1 AA

- [ ] Alle Interaktionen keyboard-navigierbar
- [ ] Focus-Indikatoren sichtbar
- [ ] Farbkontraste mindestens 4.5:1
- [ ] Alle Bilder haben alt-Texte
- [ ] Formulare haben Labels
- [ ] Fehlermeldungen sind spezifisch
- [ ] Skip-Links vorhanden
- [ ] ARIA-Labels wo nötig

---

## Referenzen

- `.quinsy-studio/process/lifecycle.md` — Phase 2 (Design Blueprinting)
- `.quinsy-studio/knowledge-base/anti_ai_slop_protocol.md` — UI-Slop-Regeln
- `.quinsy-studio/studio-library/ui/tokens/` — Design Tokens
