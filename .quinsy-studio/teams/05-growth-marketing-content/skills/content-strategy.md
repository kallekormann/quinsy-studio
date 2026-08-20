# Skill: Content Strategy

> Content-Planung, Blog, Social Media, E-Mail-Marketing, Tone of Voice

## Metadata

```
skill_id: GM-003
name: Content Strategy
team: 05-growth-marketing-content
lead_role: Content Strategist
support_roles: [Growth Manager, SEO Specialist]
phases: [2, 3, 5, 7]
activation_triggers:
  - Ticket enthält "Content", "Blog", "Social", "Newsletter"
  - Phase 2: Content-Architektur wird geplant
  - Phase 3: Content wird erstellt
  - Phase 5: Content-Check
  - Phase 7: Content-Optimierung
```

---

## Verhaltensregeln

### 1. Tone of Voice

```markdown
Für jedes Projekt:
  - Primärer Ton: professionell / locker / technisch / emotionell
  - Sekundärer Ton: variationsabhängig
  - Vermeiden: AI-Floskeln, Buzzwords, Jargon
  - Zielgruppe: Wer spricht wie an?

Anti-AI-Slop:
  - Kein "In today's digital landscape"
  - Kein "Revolutionize" / "Seamless" / "Empower"
  - Kein "Furthermore" / "Moreover"
  - Stattdessen: Direkt, konkret, nützlich
```

### 2. Content-Pillar

```markdown
Für jedes Projekt:
  - 1-2 Hauptthemen (Pillar)
  - 5-10 Unterthemen (Cluster)
  - Pro Cluster: 3-5 Artikel

Beispiel (SaaS-Projekt):
  Pillar: "Task Management"
  Clusters:
    - "Zeitmanagement Tipps"
    - "Team-Koordination"
    - "Projektplanung"
    - "Produktivität steigern"
```

### 3. Content-Formate

```markdown
Blog:
  - How-To Guides (lange, detaillierte Anleitungen)
  - Vergleiche (Feature X vs. Y)
  - Case Studies (Erfolgsgeschichten)
  - Listen (Top 10, Best Practices)

Social Media:
  - LinkedIn: Thought Leadership, Branchen-Insights
  - Twitter/X: Kurze Tipps, Threads
  - Instagram: Visuelle Inhalte, Stories

E-Mail:
  - Willkommens-Serie (Onboarding)
  - Newsletter (regelmäßig)
  - Transaktionale E-Mails
```

### 4. Content-Kalender

```markdown
Format:
  | Datum | Format | Thema | Kanal | Status |
  |-------|--------|-------|-------|--------|

Frequenz:
  - Blog: 1-2× pro Woche
  - Social: 3-5× pro Woche
  - Newsletter: 1× pro Woche/Monat
```

### 5. Performance-Messung

```markdown
Metriken:
  - Organic Traffic
  - Keyword Rankings
  - Engagement (Likes, Comments, Shares)
  - Conversion Rate
  - Newsletter Signups
  - Time on Page
```

---

## Anti-Patterns

### ❌ Verboten

```markdown
- AI-Generierte Floskeln
  - Kein Mehrwert für den Leser
  - Nur promotional (kein informativ)
  - Keine klare Struktur
  - Veraltete Inhalte
```

### ✅ Stattdessen

```markdown
- Direkter, konkreter Stil
  - Jeder Artikel löst ein Problem
  - 80% informativ, 20% promotional
  - Klare Struktur mit Überschriften
  - Regelmäßige Aktualisierung
```

---

## Externe Skill-Unterstützung

> Vor der Umsetzung die importierten Best-in-Class-Skills laden (`./studio update-skills`):

- **`marketing_aeo/skills/copywriting`** (coreyhaines31/marketingskills) — Conversion-orientiertes Copywriting. **Primäre Quelle für Copy.**
- **`marketing_aeo/skills/content-strategy`** — Content-Strategie + Topic-Clustering
- **`marketing_aeo/skills/product-marketing`** — Produkt-Positionierung (Basis für alle anderen Marketing-Skills)
- **`marketing_aeo/skills/customer-research`** — Zielgruppen-/Customer-Research
- **`marketing_aeo/skills/emails`** — E-Mail-Sequenzen (Willkommens-Serie, Newsletter)
- **`all_domains/writing-and-content/copywriting`** — alternative Copywriting-Quelle

Ablauf: `product-marketing` lesen → `copywriting` anwenden → Anti-Slop-Gate (`validate_anti_slop.py`) laufen lassen.

## Referenzen

- `.quinsy-studio/knowledge-base/anti_ai_slop_protocol.md` — Anti-Slop
- `.quinsy-studio/knowledge-base/design_playbook.md` — Content-Struktur
