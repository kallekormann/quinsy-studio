# Skill: Dual-Loop Learning

> Local Loop (Projekt) vs Global Loop (Studio), Learning Harvesting, Knowledge Promotion

## Metadata

```
skill_id: SO-003
name: Dual-Loop Learning
team: 09-studio-operations-evolution
lead_role: Process Guard
support_roles: [Agile Coach, Documentation Writer]
phases: [6]
activation_triggers:
  - Ticket enthält "Learning", "Retro", "Knowledge", "Promotion"
  - Phase 6: Knowledge Harvesting (Pflicht)
  - /studio learn Befehl
  - /studio promote Befehl
```

---

## Verhaltensregeln

### 1. Local Loop (Projekt-Welt)

```markdown
Was gehört hierher:
  - Projektspezifische Bugs und Workarounds
  - Nischen-Erkenntnisse aus A/B-Tests
  - Kundenspezifische Anforderungen
  - Projekt-spezifische Config-Details

Ablageort:
  projects/[name]/docs/local_learnings.md

Format:
  ## Learning LL-{NNN}
  - **Datum:** YYYY-MM-DD
  - **Kontext:** Was ist passiert?
  - **Erkenntnis:** Was haben wir gelernt?
  - **Aktion:** Was wurde geändert?
  - **Gilt für:** Nur dieses Projekt
```

### 2. Global Loop (Studio-Welt)

```markdown
Was gehört hierher:
  - Universell anwendbare Lösungen
  - Bessere Playbooks
  - Neue Anti-Slop-Regeln
  - Verbesserte Python-Tools
  - Wiederverwendbare Komponenten

Ablageort:
  .quinsy-studio/knowledge-base/  → Playbooks
  .quinsy-studio/studio-tools/    → Python-Scripts
  .quinsy-studio/studio-templates/ → Templates
  studio-library/                 → UI/Packages

Promotion via:
  ./studio promote <project> <asset-path>
```

### 3. Learning Harvesting (Phase 6)

```markdown
Workflow:
  1. Sprint-Retrospektive durchführen
  2. Learning Items sammeln
  3. Für jedes Learning:
     a. Ist es projektspezifisch? → Local Loop
     b. Ist es universell? → Global Loop
  4. Local Learnings → projects/[name]/docs/local_learnings.md
  5. Global Learnings → .quinsy-studio/knowledge-base/ oder studio-tools/
  6. CHANGELOG aktualisieren
```

### 4. Promotion-Workflow

```markdown
Wann promoven?
  - Lösung ist in 2+ Projekten nützlich
  - Code/Design ist generisch
  - Lösung ist bewährt (getestet)

Wie promoven?
  1. ./studio promote <project> <asset-path>
  2. Asset wird in Studio-Library kopiert
  3. README.md wird erstellt/aktualisiert
  4. manifest.json wird aktualisiert
  5. CHANGELOG.md wird aktualisiert
  6. Skill-Registry wird aktualisiert (falls neuer Skill)
```

---

## Anti-Patterns

### ❌ Verboten

```markdown
- Projekt-spezifische Lösungen ins Studio-HQ kopieren
  - Keine Learning Harvesting nach Sprint
  - Promotions ohne Dokumentation
  - Local Learnings die als Global verkauft werden
```

### ✅ Stattdessen

```markdown
- Strikte Trennung Local/Global
  - Obligatorische Learning Harvesting in Phase 6
  - Promotion mit vollständiger Doku
  - Nur universell anwendbare Lösungen im Studio-HQ
```

---

## Referenzen

- `.quinsy-studio/process/learning-loop.md` — Dual-Loop Learning
- `.quinsy-studio/process/lifecycle.md` — Phase 6
- `./studio promote` — Promotion-Befehl
- `./studio learn` — Learning-Interface
