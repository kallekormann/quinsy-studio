# PRD — "Nudge" 

> **Archetyp & Komplexität**
> * **Archetyp:** SaaS-Application (B2C Micro-SaaS)
> * **Komplexität:** P1 (Fokus auf maximale UX-Politur, flüssige Micro-Interactions und minimalen Scope bei den Kernfeatures)
> 
> 

---

## ## Titel / Überblick

Nudge ist eine minimalistische, hochgradig spielerische ToDo-Anwendung für Endverbraucher, die Produktivität mit einem Dopamin-Kick verbindet. Statt trockener Listen setzt die App auf ein frisches, "Juicy Design" mit haptischem Feedback, Physik-basierten Animationen und spielerischen Belohnungen. Das Ziel ist es, die tägliche ToDo-Liste von einer nervigen Pflicht in eine befriedigende Gewohnheit zu verwandeln.

---

## ## Problem

Herkömmliche ToDo-Apps (wie Apple Reminders, Todoist oder Microsoft To Do) sind oft funktional, aber steril und langweilig. Sie fühlen sich wie digitale Aktenordner an. Das führt dazu, dass Nutzer die Apps nach kurzer Zeit wieder verlassen oder das Abhaken von Aufgaben sich wie Arbeit anfühlt. Es fehlt an emotionaler Resonanz, visuellem Feedback und echtem Spaﬂ bei der Interaktion.

---

## ## Zielgruppe & Nutzer

* **Primäre Zielgruppe:** Digital-native Millennials und Gen Z (18–35 Jahre), die Ästhetik, Design und moderne Apps schätzen.
* **Jobs-to-be-done:**
* *"Hilf mir, meine täglichen Aufgaben zu organisieren, ohne dass es sich nach Bürokräften-Stress anfühlt."*
* *"Gib mir ein gutes Gefühl und kleine Erfolgserlebnisse, wenn ich etwas erledigt habe."*



---

## ## Ziele & Erfolgskriterien

* **North Star Metric:** Wöchentlich aktive Nutzer (WAU), die mindestens 5 Aufgaben pro Tag abhaken.
* **KPIs:**
* Hohe Retention-Rate nach Tag 7 (Ziel > 30% durch den "Delight-Faktor").
* Virales Sharing: Nutzer teilen ihre "Completion Animations" oder Streaks in Social Media (TikTok/Insta Story Export).



---

## ## Umfang

* **In Scope (P0):**
* Superschnelle Aufgabenerstellung (Natural Language Input, z. B. "Morgen um 15 Uhr Sport").
* Das "Juicy Interface": Physik-basierte Animationen beim Abhaken (z. B. Aufgaben platzen weg wie Seifenblasen, Konfetti-Effekte, schwebende Elemente via Framer Motion / CSS Physics).
* Tägliche Streaks & Mini-Gamification (Level-Up für erledigte Aufgaben).
* Frisches Farbkonzept (Neo-Brutalism meets Soft Gradients, dunkler & heller Modus mit lebendigen Akzentfarben).


* **Out of Scope (P1/P2):**
* Komplexe Team-Collaboration, Datei-Anhänge, Unterprojekte, Zeiterfassung.



---

## ## Anforderungen

* **Funktionale Anforderungen:**
* **P0:** Aufgaben erstellen, bearbeiten, löschen und per Swipe/Tap mit haptischem & visuellem Feedback abhaken.
* **P0:** Lokale Speicherung mit optionaler Cloud-Synchronisation (Local-First-Ansatz für instantane Reaktionszeiten).
* **P1:** Sound-Design (dezent, befriedigende "Pop"- und "Chime"-Geräusche beim Erledigen).
* **P1:** Anpassbare Themes (verschiedene Farbwelten und Animationstypen).



---

## ## Nicht-funktionale Anforderungen

* **Performance:** 60/120 FPS bei allen Animationen; Ladezeiten unter 100ms (Lokaler Cache).
* **Usability:** Zero-Onboarding-Hürde; die App muss intuitiv ohne Tutorial bedienbar sein.
* **Plattformen:** Progressive Web App (PWA) mit nativem Look & Feel für iOS und Android sowie optimierte Desktop-Web-Ansicht.

---

## ## Monetarisierung

* **Modell:** Freemium mit Einmal-Kauf ("Pro Pass") oder kleiner Abo-Modell.
* **Free-Tier:** Alle Kernfunktionen mit Standard-Themes.
* **Pro-Tier (ca. 4,99 € einmalig oder 1,49 €/Monat):** Exklusive Sound-Packs, erweiterte Animations-Themes (z. B. Cyberpunk, Neon, Zen-Garden) und Cloud-Sync.

---

## ## Compliance & Recht

* **DSGVO:** Minimale Datenerhebung (keine Tracking-Analyse ohne Einwilligung, DSGVO-konforme Serverstandorte in der EU falls Cloud-Sync aktiv).
* **Impressum & Datenschutz:** Standardkonforme Pflichtangaben im Footer/Settings-Bereich.

---

## ## Risiken & offene Fragen

* **Risiko:** Die App könnte nach dem Neuheitsfaktor ("Novelty Effect") langweilig werden.
* **Offene Frage:** Welche Sound- und Animations-Kombinationen treffen den schmalen Grat zwischen "macht Spaß" und "nervt nach dem 100. Mal"? (Lösung: Schneller Usability-Test mit einem ersten Prototypen).