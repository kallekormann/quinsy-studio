# Skill: Technology Evaluation

> Framework/Library-Evaluierung, PoC-Erstellung, Migration-Planung

## Metadata

```
skill_id: PS-003
name: Technology Evaluation
team: 04-product-strategy-architecture
lead_role: Systems Architect
support_roles: [Backend Architect, Frontend Architect]
phases: [1, 2]
activation_triggers:
  - Ticket enthält "Evaluation", "Framework", "Library", "Migration"
  - Phase 1: Technologien werden bewertet
  - Phase 2: Tech-Stack wird finalisiert
  - Neue Dependency soll eingeführt werden
```

---

## Verhaltensregeln

### 1. Evaluierungsprozess

```markdown
Schritt 1: Anforderungen definieren
  - Funktionale Anforderungen
  - Non-Funktionale (Performance, Skalierbarkeit)
  - Team-Kompetenz
  - Budget

Schritt 2: Optionen identifizieren
  - 3-5 realistische Optionen
  - Keine Exoten (nur wenn zwingend)

Schritt 3: Kriterien gewichten
  - Performance (25%)
  - Community & Support (20%)
  - Lernkurve (20%)
  - Langfristige Wartung (20%)
  - Kosten (15%)

Schritt 4: PoC (bei kritischen Entscheidungen)
  - Max. 2 Tage
  - Realistisches Szenario
  - Benchmark gegen Kriterien

Schritt 5: Empfehlung mit ADR
```

### 2. PoC-Regeln

```markdown
PoC-Ziel:
  - Technische Machbarkeit beweisen
  - Performance messen
  - Lernkurve abschätzen
  - Integrationsaufwand verstehen

PoC-Umfang:
  - Max. 2 Tage
  - Max. 500 Zeilen Code
  - Realistisches Szenario (kein Todo-App)

Dokumentation:
  - ADR mit Empfehlung
  - Benchmark-Ergebnisse
  - Erfahrungen (positiv/negativ)
```

### 3. Migration

```markdown
Wann migrieren:
  - Technologie ist EOL (End of Life)
  - Drastisch bessere Alternative
  - Sicherheitslücken
  - Performance-Probleme

Migration-Strategie:
  1. Strangler Fig Pattern (inkrementell)
  2. Feature-Flag für neue Implementierung
  3. Parallel-Betrieb
  4. A/B-Test
  5. Full Switch
  6. Alte Technologie entfernen
```

---

## Anti-Patterns

### ❌ Verboten

```markdown
- "Weil es cool ist" als Begründung
- Kein PoC für kritische Entscheidungen
- Big Bang Migration
- Kein Rollback-Plan
- Evaluation ohne Kriterien
```

### ✅ Stattdessen

```markdown
- Strukturierte Evaluation mit Gewichtung
- PoC für alles was >3 Monate Auswirkung hat
- Inkrementelle Migration (Strangler Fig)
- Rollback-Plan für jede Migration
- ADR für jede Entscheidung
```

---

## Referenzen

- `.quinsy-studio/process/adr-policy.md` — ADR-Regelwerk
- `.quinsy-studio/process/project-archetypes.md` — Stack-Empfehlungen
