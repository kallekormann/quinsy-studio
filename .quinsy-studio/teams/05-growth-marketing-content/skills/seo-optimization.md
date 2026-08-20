# Skill: SEO Optimization

> Technisches SEO, Content-SEO, Schema.org, Core Web Vitals, Linkbuilding

## Metadata

```
skill_id: GM-001
name: SEO Optimization
team: 05-growth-marketing-content
lead_role: SEO Specialist
support_roles: [Frontend Architect, Content Strategist]
phases: [2, 3, 5, 7]
activation_triggers:
  - Ticket enthält "SEO", "Sichtbarkeit", "Ranking", "Google"
  - Phase 2: URL-Struktur wird definiert
  - Phase 3: Content-Architektur
  - Phase 5: SEO-Audit
  - Phase 7: SEO-Optimierung
```

---

## Verhaltensregeln

### 1. Technisches SEO

```markdown
Core Web Vitals (Pflicht):
  - LCP < 2.5s
  - INP < 200ms
  - CLS < 0.1

Indexierung:
  - robots.txt korrekt (keine wichtigen Seiten blockiert!)
  - XML Sitemap generiert und bei Google eingereicht
  - Canonical Tags für Duplicate Content
  - hreflang für mehrsprachige Seiten
  - Keine noindex auf wichtigen Seiten

URL-Struktur:
  - Kurz und beschreibend
  - Keywords im Slug
  - Keine Parameter in URLs
  - Bindestriche statt Unterstriche
```

### 2. On-Page SEO

```markdown
Pro Seite:
  - Title Tag: 50-60 Zeichen, Hauptkeyword vorne
  - Meta Description: 150-160 Zeichen, Call-to-Action
  - H1: 1× pro Seite, enthält Hauptkeyword
  - H2-H6: Hierarchische Überschriften
  - Alt-Texte: Beschreibend für alle Bilder
  - Internal Linking: 3-5 interne Links pro Seite
  - Schema.org: Structured Data für Rich Snippets
```

### 3. Content-SEO

```markdown
Content-Strategie:
  - Pillar Pages (Hauptthemen, >2000 Wörter)
  - Cluster Content (Unterthemen, >800 Wörter)
  - Hub & Spoke Modell
  - Interne Verlinkung zwischen Pillar und Cluster

Keyword-Recherche:
  - Long-Tail Keywords für neue Domains
  - Search Intent verstehen (Informational, Transactional)
  - Keyword-Difficulty beachten
  - Volumen + Difficulty = Priorität
```

### 4. Schema.org

```markdown
Pflicht-Markups:
  - Organization (Firma)
  - WebSite (mit SearchAction)
  - BreadcrumbList
  - FAQPage (für FAQ-Sektionen)
  - Product (für E-Commerce)
  - Article (für Blog)

Validierung:
  - Google Rich Results Test
  - Schema.org Validator
```

### 5. Linkbuilding

```markdown
Strategien:
  - Content-Marketing (virale Inhalte)
  - Guest Posting (autoritäre Blogs)
  - Broken Link Building
  - HARO (Help A Reporter Out)
  - Partnerships / Cross-Linking

Regeln:
  - Nur natürliche Links
  - Kein Link-Kauf
  - Anchor Text diversifizieren
  - Relevanz > Authority
```

---

## Anti-Patterns

### ❌ Verboten

```markdown
- Keyword-Stuffing
  - Cloaking (andere Inhalte für Google)
  - Link-Kauf
  - Doppelte Inhalte ohne Canonical
  - Keine Sitemap
  - robots.txt blockiert wichtige Seiten
```

### ✅ Stattdessen

```markdown
- Natürliche Keyword-Integration
  - Gleiche Inhalte für alle
  - Organisches Linkbuilding
  - Canonical für Duplicate
  - XML Sitemap generieren
  - Korrekte robots.txt
```

---

## Externe Skill-Unterstützung

> Vor der Umsetzung die importierten Best-in-Class-Skills laden (`./studio update-skills`):

- **`marketing_aeo/skills/seo-audit`** (coreyhaines31/marketingskills) — vollständiger SEO-Audit-Workflow. **Primäre Quelle für Audits.**
- **`marketing_aeo/skills/schema`** — strukturierte Daten / Schema.org-Markup
- **`marketing_aeo/skills/programmatic-seo`** — pSEO-Architektur (Programmatic Pages, Templates)
- **`marketing_aeo/skills/site-architecture`** — URL-/Site-Architektur, Internal Linking
- **`marketing_aeo/skills/keyword-research`** — Keyword-Matrizen, Search Intent

Ablauf: `seo-audit` lesen → pSEO-Architektur prüfen → Schema ergänzen → Link-Rot-Prevention anwenden.

## Referenzen

- `.quinsy-studio/knowledge-base/frontend_playbook.md` — Core Web Vitals
- `.quinsy-studio/knowledge-base/design_playbook.md` — UX für SEO
