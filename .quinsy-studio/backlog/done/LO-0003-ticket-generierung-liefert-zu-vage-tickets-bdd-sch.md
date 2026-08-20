---
id: LO-0003
title: Ticket-Generierung liefert zu vage Tickets — BDD-Schema + Rollenzuweisung implementiert
type: studio-evolution
status: done
phase: 6
priority: P2
estimate: M
assignee_role: Studio Automation Engineer (Director)
team: 09-studio-operations-evolution
skills: ['SO-001']
dependencies: []
created: 2026-08-20
---

# LO-0003 — Ticket-Generierung liefert zu vage Tickets — BDD-Schema + Rollenzuweisung implementiert

## 1. Context & Value
- **Ist-Zustand:** Beobachtung: Ticket-Generierung liefert zu vage Tickets — BDD-Schema + Rollenzuweisung implementiert (Signal: tooling-gap, Quelle: Schema-Review 2026-08-20)
- **Soll-Zustand:** Das Studio ist so verbessert, dass dieses Signal nicht erneut auftritt.
- **Value:** Das Studio lernt aus Projekten (Dual-Loop) und verbessert Prozess, Skills oder Tooling.

## 2. Technical Constraints
- **Modifikationsbereich:** .quinsy-studio/process/, .quinsy-studio/studio-tools/, .quinsy-studio/teams/
- **Regel:** Keine Änderung an Kundenprojekten (nur Studio-HQ)
- **Regel:** Jede Änderung → CHANGELOG.md-Eintrag
- **Regel:** Nach Umsetzung: Skill-Matching-Test + QA-Gate grün
- **Regel:** Signal: tooling-gap — Quelle: Schema-Review 2026-08-20
- **Playbook:** `process/learning-loop.md` (zwingend einhalten)
- **Anti-Slop:** Keine AI-Floskeln, keine unnötigen externen Pakete ohne ADR

## 3. Acceptance Criteria (BDD)
**Szenario 1:** Studio-Verbesserung wirkt
- **Given:** Das Lern-Signal ({signal}) tritt erneut auf
- **When:** Der verbesserte Prozess/Skill/Tool angewendet wird
- **Then:** Das Signal tritt nicht mehr auf oder wird korrekt abgefangen

## 4. Definition of Done
- [ ] Im Meta-Retro besprochen
- [ ] Umgesetzt (CHANGELOG.md-Eintrag)
- [ ] Skill-Matching-Test grün
- [ ] QA-Gate grün

## Skills
- SO-001