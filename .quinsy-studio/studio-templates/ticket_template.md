---
id: [PROJ-NNNN | LO-NNNN]
title: [Prägnante Handlungsanweisung, z.B. "Hash-Generierung für Tickets erzwingen"]
type: [feature | bug | studio-evolution]
status: open
phase: [N]
priority: [P0/P1/P2/P3]
estimate: [S/M/L/XL]
assignee_role: [Director-Rolle, z.B. "Studio Automation Engineer (Director)"]
team: [Team-Ordner, z.B. "09-studio-operations-evolution"]
skills: [Skill-IDs, z.B. ["SO-001"]]
dependencies: [Ticket-IDs, z.B. ["LO-0001"]]
created: [YYYY-MM-DD]
---

# [ID] — [Titel]

## 1. Context & Value

> Eindeutiger Kontext: Ist-Zustand vs. Soll-Zustand, damit Scope und Ziel präzise sind.

- **Ist-Zustand:** [Was ist heute der Fall? Konkret, z.B. "Ticket-IDs werden manuell vergeben, was zu Duplikaten führt."]
- **Soll-Zustand:** [Was soll nach Umsetzung gelten? Messbar, z.B. "Ein Skript generiert zwingend eindeutige IDs."]
- **Value:** [Warum ist das wichtig? Welchen Verlust/Verzögerung verhindert es?]

## 2. Technical Constraints

> Harte Leitplanken. Der Agent darf NICHT den Weg des geringsten Widerstands gehen.

- **Modifikationsbereich:** [Exakte Pfade, z.B. `studio-tools/generate_ticket_manifest.py` — NUR hier]
- **Regel:** [z.B. "Nutze die native Python `uuid` Bibliothek. Keine externen Pakete installieren."]
- **Regel:** [Weitere Beschränkungen, z.B. "Keine Änderung an Kundenprojekten."]
- **Playbook:** [`knowledge-base/backend_playbook.md` — zwingend einhalten]
- **Anti-Slop:** Keine AI-Floskeln, keine unnötigen externen Packages ohne ADR.

## 3. Acceptance Criteria (BDD)

> Maschinell testbares Verhalten statt Implementierungs-Beschreibung.

- **Szenario 1:** [Name, z.B. "Erstellung eines neuen Tickets"]
  - **Given:** [Startzustand, z.B. "Der Agent führt das Intake-Skript aus."]
  - **When:** [Aktion, z.B. "Ein neues Ticket generiert wird."]
  - **Then:** [Messbares Ergebnis, z.B. "Die ID beginnt mit `LO-` gefolgt von einem 8-stelligen alphanumerischen Hash und ist einzigartig."]

- **Szenario 2:** [Optional — weiterer Fall]
  - **Given:** ...
  - **When:** ...
  - **Then:** ...

## 4. Definition of Done

- [ ] [z.B. "`run_qa_gate.py` läuft fehlerfrei durch."]
- [ ] [z.B. "Eine Test-Ausführung erzeugt nachweislich keine Duplikate."]
- [ ] [z.B. "CHANGELOG.md ist um die neue ID-Logik aktualisiert."]
- [ ] QA-Gate grün (`./studio gate <project> --level 5`)
- [ ] Anti-Slop-Audit: 0 Verstöße

## Abhängigkeiten

- [Andere Tickets, die zuerst fertig sein müssen]

## Skills

- [Skill-IDs, die aktiviert werden — für den Agenten zur Rollen-/Wissens-Zuordnung]

## Verlauf

- [YYYY-MM-DD]: Ticket angelegt (Status: open)
