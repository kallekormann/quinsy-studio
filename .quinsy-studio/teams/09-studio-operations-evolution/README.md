# Team 09 — Studio Operations & Evolution (Self-Learning Core)

> Verantwortlich für die Wartung und Evolution des Studios selbst — unabhängig von laufenden Kundenprojekten. Dies ist das Herz des Dual-Loop Learning Systems.

## Director-Level Rollen

| Rolle | Level | Verantwortlichkeiten |
|-------|-------|---------------------|
| **Studio Automation Engineer** | Director | Wartung der Python-Skripte und Tools im Studio-HQ |
| **Process Guard** | Director | Überwachung der Sprint-Disziplin und Optimierung der Studio-Abläufe unabhängig vom Projektgeschäft |
| **Agile Coach** | Director | Optimierung der Studio-Prozesse, Retrospektiven, Team-Performance |
| **Documentation Writer** | Lead | Pflegt strikt die Trennung zwischen Studio-Playbooks und Projekt-Dokumentationen |

---

## Skills

| ID | Skill | Lead-Rolle | Datei |
|----|-------|------------|-------|
| SO-001 | Studio Tooling Maintenance | Studio Automation Engineer | `skills/studio-tooling-maintenance.md` |
| SO-002 | Process Optimization | Process Guard | `skills/process-optimization.md` |
| SO-003 | Dual-Loop Learning | Process Guard + Agile Coach | `skills/dual-loop-learning.md` |
| SO-004 | Documentation Governance | Documentation Writer | `skills/documentation-governance.md` |

---

## Verantwortlichkeiten

### Studio-HQ Wartung
- Python-Tools in `.quinsy-studio/studio-tools/` pflegen
- Playbooks in `.quinsy-studio/knowledge-base/` aktualisieren
- Templates in `.quinsy-studio/studio-templates/` verbessern
- Skill-Registry aktuell halten

### Dual-Loop Learning

```
LOCAL LOOP (Projekt-Welt)           GLOBAL LOOP (Studio-Welt)
────────────────────────            ──────────────────────────
• Projektspezifische Bugs           • Universelle Playbooks
• Nischen-Erkenntnisse              • Python-Tooling-Updates
• Workarounds                       • Anti-Slop-Regel-Updates
• Ablage: projects/[name]/          • Ablage: .quinsy-studio/
  docs/local_learnings.md             knowledge-base/

⚠️ Beeinflusst NICHT andere         ✅ Gilt für ALLE zukünftigen
   Projekte                            Projekte
```

### Prozess-Optimierung
- Sprint-Disziplin überwachen
- Studio-Abläufe unabhängig vom Projektgeschäft optimieren
- Anti-Patterns im Studio-Prozess erkennen und beheben
- Metriken sammeln und analysieren

### Dokumentations-Governance
- Strikte Trennung zwischen Studio-Playbooks und Projekt-Dokumentationen
- CHANGELOG pflegen
- READMEs aktuell halten
- Wissenstransfer sicherstellen

---

## Phasen-Beteiligung

| Phase | Lead-Rollen | Support-Rollen |
|-------|-------------|----------------|
| Phase 0 | — | Documentation Writer |
| Phase 1 | — | Documentation Writer |
| Phase 2 | — | Process Guard (Prozess-Check) |
| Phase 3 | Process Guard | Studio Automation Engineer |
| Phase 4 | — | Studio Automation Engineer (Tooling) |
| Phase 5 | Process Guard | Documentation Writer |
| Phase 6 | **Process Guard, Agile Coach** | Documentation Writer, Studio Automation Engineer |
| Phase 7 | Studio Automation Engineer | Process Guard |

---

## Studio-Evolution Command

```bash
# Studio in autonomen Wartungs-Sprint versetzen
./studio evolve

# Nur eigene Tools refactored, kein Kundenprojekt
# Playbooks verbessert, Skills aktualisiert
# Python-Scripts optimiert
```

---

## Referenzen

- `.quinsy-studio/process/learning-loop.md` — Dual-Loop Learning
- `.quinsy-studio/process/lifecycle.md` — Phasen
- `.quinsy-studio/studio-tools/` — Python-Automation
- `.quinsy-studio/knowledge-base/` — Playbooks
