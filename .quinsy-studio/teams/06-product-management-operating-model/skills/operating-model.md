# Skill: Operating Model

> Team-Struktur, Agile Prozesse, Ceremonies, OKRs, Metriken

## Metadata

```
skill_id: PM-003
name: Operating Model
team: 06-product-management-operating-model
lead_role: Operating Lead
support_roles: [Product Manager, Agile Coach]
phases: [0, 1, 7]
activation_triggers:
  - Ticket enthält "Operating Model", "Team-Struktur", "Prozess"
  - Phase 0: Team-Struktur wird definiert
  - Phase 1: Prozesse werden etabliert
  - Phase 7: Retro und Optimierung
```

---

## Verhaltensregeln

### 1. Team-Struktur

```markdown
Standard (SaaS-Projekt):
  - Product Manager (1)
  - Frontend Engineer (1-2)
  - Backend Engineer (1-2)
  - QA Specialist (0.5-1)
  - DevOps/Platform (0.5)

Skalierung:
  - Squad-Modell bei >8 Leute
  - Cross-Funktionale Teams
  - Feature Teams statt Component Teams
```

### 2. Agile Prozesse

```markdown
Sprint-Länge: 2 Wochen

Ceremonies:
  - Sprint Planning (Montag, 1h)
  - Daily Standup (täglich, 15 Min)
  - Sprint Review (Freitag, 1h)
  - Sprint Retro (Freitag, 30 Min)
  - Backlog Grooming (Mittwoch, 1h)

Definition of Done:
  - Code geschrieben
  - Tests grün
  - Code Review bestanden
  - QA bestanden
  - Doku aktuell
```

### 3. OKRs

```markdown
Struktur:
  Objective: Was wollen wir erreichen?
  Key Results: Wie messen wir Erfolg?

Beispiel:
  O: "User-Retention verbessern"
  KR1: "30-Tage-Retention von 40% auf 60% steigern"
  KR2: "Onboarding-Completion-Rate auf 80% bringen"
  KR3: "NPS von 30 auf 50 steigern"

Frequenz: Quartalsweise
Review: Monatlich
```

### 4. Metriken

```markdown
North Star Metric:
  - Die EINE Metrik die den Wert misst

Supporting Metrics:
  - Acquisition: Signups, Traffic
  - Activation: Onboarding-Completion
  - Retention: Dauernutzung
  - Revenue: MRR, ARPU
  - Referral: NPS, Shares
```

### 5. Wissenstransfer

```markdown
Dokumentation:
  - Decision Log (Entscheidungen + Begründungen)
  - Sprint Summary (was wurde gelernt?)
  - Onboarding-Doku für neue Team-Mitglieder
  - Architecture Decision Records (ADRs)
```

---

## Anti-Patterns

### ❌ Verboten

```markdown
- Scrum Dogmatisch ohne Anpassung
  - Keine Retros
  - OKRs die nie überprüft werden
  - Kein Wissenstransfer
  - Silos zwischen Teams
```

### ✅ Stattdessen

```markdown
- Agil angepasst an Team-Größe
  - Regelmäßige Retros mit Action Items
  - OKRs monatlich reviewen
  - Doku als Pflicht (nicht optional)
  - Cross-Team Collaboration
```

---

## Referenzen

- `.quinsy-studio/process/iterative-delivery.md` — Sprint/Grooming
- `.quinsy-studio/process/learning-loop.md` — Learning Loop
