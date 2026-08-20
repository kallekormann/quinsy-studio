# Skill: AEO (Answer Engine Optimization)

> Optimierung für KI-Suchmaschinen, strukturierte Daten, zitierfähige Inhalte

## Metadata

```
skill_id: GM-002
name: Answer Engine Optimization (AEO)
team: 05-growth-marketing-content
lead_role: SEO Specialist
support_roles: [Content Strategist, Frontend Engineer]
phases: [3, 5, 7]
activation_triggers:
  - Ticket enthält "AEO", "AI Search", "ChatGPT", "Perplexity"
  - Phase 3: Content wird für AEO optimiert
  - Phase 5: AEO-Audit
  - Phase 7: AEO-Optimierung
```

---

## Verhaltensregeln

### 1. Strukturierte Daten für LLMs

```markdown
LLMs extrahieren:
  - Tabellen (Markdown/HTML)
  - Listen (nummeriert und unnummeriert)
  - Definitionen (klare Begriffe)
  - Vergleiche (Side-by-Side)
  - FAQ-Sektionen

Formatierung:
  - Klare Überschriften (H2, H3)
  - Bullet Points für Aufzählungen
  - Tabellen für Vergleiche
  - Code-Blöcke für technische Inhalte
```

### 2. Zitierfähige Antworten

```markdown
Jede Hauptbehauptung:
  1. Direkte Antwort (1-2 Sätze)
  2. Detaillierte Erklärung
  3. Quelle / Referenz
  4. Beispiel

Struktur:
  "Ja/Nein/Fakt. [Detaillierte Erklärung]. 
   Laut [Quelle] ist [spezifischer Wert/Fakt]."
```

### 3. FAQ-Optimierung

```markdown
Für jede wichtige Seite:
  - 3-5 häufige Fragen
  - Klare, direkte Antworten
  - FAQPage Schema.org Markup
  - Fragen aus "People Also Ask" ableiten
```

### 4. Vergleichstabellen

```markdown
Für Produkt-/Feature-Vergleiche:
  - Markdown-Tabellen
  - Klare Spalten-Überschriften
  - Feature vs. Feature
  - Preis vs. Preis

Beispiel:
  | Feature | Free | Pro | Enterprise |
  |---------|------|-----|------------|
  | Users   | 1    | 10  | Unlimited  |
  | Storage | 1GB  | 10GB| 100GB      |
```

### 5. Authority-Signale

```markdown
Für LLM-Rankings:
  - Autoren-Bio mit Expertise
  - Zitate und Referenzen
  - Aktualität (Datum aktualisieren)
  - Domain-Authorität aufbauen
  - Brand-Erwähnungen
```

---

## Anti-Patterns

### ❌ Verboten

```markdown
- Nur Fließtext ohne Struktur
  - Keine Quellen für Behauptungen
  - Keine Tabellen für Vergleiche
  - Veraltete Inhalte
  - Keine FAQ-Sektionen
```

### ✅ Stattdessen

```markdown
- Strukturierte Inhalte mit Listen/Tabellen
  - Quellen für jede Behauptung
  - Vergleichstabellen für Features
  - Regelmäßige Aktualisierung
  - FAQ mit Schema.org Markup
```

---

## Externe Skill-Unterstützung

> Vor der Umsetzung die importierten Best-in-Class-Skills laden (`./studio update-skills`):

- **`marketing_aeo/skills/ai-seo`** (coreyhaines31/marketingskills) — vollständiger AEO-Workflow: In AI-Search-Ergebnissen und LLM-Antworten zitiert werden. **Primäre Quelle für diese Skill.**
- **`marketing_aeo/skills/schema`** — strukturierte Daten / JSON-LD / Schema.org-Markup für KI-Sichtbarkeit
- **`geo_visibility/SKILL.md`** (bloomprotocol) — AI-Visibility-Audit, llms.txt, Vergleichsseiten-Generator
- **`marketing_aeo/skills/competitors`** — Vergleichs-/Alternativen-Seiten (`/alternatives-to/`)

Ablauf: `ai-seo` lesen → Audit-Punkte anwenden → Schema-Markup ergänzen → llms.txt prüfen.

## Referenzen

- `.quinsy-studio/knowledge-base/design_playbook.md` — Content-Struktur
- `.quinsy-studio/knowledge-base/frontend_playbook.md` — Schema.org
