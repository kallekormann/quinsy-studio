# Skill: Architecture Decisions

> ADRs, Tech-Stack-Wahl, Build vs Buy, Monolith vs Microservices

## Metadata

```
skill_id: PS-002
name: Architecture Decisions
team: 04-product-strategy-architecture
lead_role: Systems Architect
support_roles: [Backend Architect, Frontend Architect, Platform Architect]
phases: [2, 3]
activation_triggers:
  - Ticket enthält "ADR", "Architektur", "Tech-Stack", "Build vs Buy"
  - Phase 2: Gesamtarchitektur wird definiert
  - Phase 3: Technologie-Entscheidungen
  - Grundsätzliche Architektur-Änderung
```

---

## Verhaltensregeln

### 1. ADR-Format

```markdown
# ADR-{NNN}: {Titel}

## Status
  proposed | accepted | deprecated | superseded

## Kontext
  Welches Problem wird gelöst?

## Entscheidung
  Was wurde entschieden?

## Begründung
  Warum wurde so entschieden?

## Alternativen
  Was wurde verworfen und warum?

## Konsequenzen
  Positive und negative Auswirkungen

## Risiken
  Was könnte schiefgehen?
```

### 2. Tech-Stack-Entscheidung

```markdown
Framework:
  - Next.js (React SSR/ISR) → Standard für Web
  - Laravel (PHP) → Bei Enterprise/PHP-Bestand
  - Supabase → Als Database/Backend (schnell)

Database:
  - PostgreSQL (Supabase) → Standard
  - Redis → Cache, Queues, Sessions
  - SQLite → Embedded, Testing

Deployment:
  - Vercel → Standard für Next.js
  - Docker → Für komplexe Setups
  - Railway / Fly.io → Für Backends

Entscheidungskriterien:
  1. Team-Kompetenz
  2. Community & Ökosystem
  3. Langfristige Wartung
  4. Performance
  5. Kosten
```

### 3. Build vs Buy

```markdown
Bauen wenn:
  - Kernkompetenz (Differenzierung)
  - Volle Kontrolle nötig
  - Keine gute Alternative existiert
  - Langfristig günstiger

Kaufen wenn:
  - Nicht-Kernkompetenz
  - Time-to-Market kritisch
  - Best Practice existiert
  - Support & Maintenance nötig

Beispiele:
  ✅ Kaufen: Auth (Supabase Auth), Payment (Stripe), E-Mail (Resend)
  ✅ Bauen: Kern-Features, UI, Business Logic
```

### 4. Monolith vs Microservices

```markdown
Standard: Modular Monolith
  - Ein Deployment
  - Klare Modulgrenzen
  - Internal APIs (nicht HTTP)
  - Später auf Microservices aufteilen wenn nötig

Microservices wenn:
  - Verschiedene Teams
  - Unterschiedliche Skalierungsbedürfnisse
  - Verschiedene Tech-Stacks nötig
  - >50 Entwickler
```

---

## Anti-Patterns

### ❌ Verboten

```markdown
- Keine ADR für Grundsatzentscheidungen
- Tech-Choice basierend auf "Hype"
- Microservices ohne klare Grenzen
- Build wenn Buy existiert (NIH-Syndrom)
- Kein ADR für abgelehnte Alternativen
```

### ✅ Stattdessen

```markdown
- ADR für jede Grundsatzentscheidung
- Tech-Choice basierend auf Kriterien
- Modular Monolith als Standard
- Build nur wenn Kernkompetenz
- Vollständige ADRs mit Alternativen
```

---

## Referenzen

- `.quinsy-studio/process/adr-policy.md` — ADR-Regelwerk
- `.quinsy-studio/process/project-archetypes.md` — Stack-Empfehlungen
- `projects/[name]/docs/adr/` — ADR-Ablage
