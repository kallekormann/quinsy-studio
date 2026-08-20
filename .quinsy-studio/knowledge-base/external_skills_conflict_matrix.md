# Konflikt-Matrix: Externe Skills vs. Anti-Slop-Protocol

> Diese Matrix prüft jede importierte externe Skill-Quelle gegen die verbindlichen
> internen Regeln (`.quinsy-studio/knowledge-base/anti_ai_slop_protocol.md`,
> `zero-data-architecture`, `compliance_playbook`).
>
> **Grundsatz:** Eigene Regeln überschreiben externe Tendenzen zur Generik.
> Externe Skills sind Werkzeuge, KEINE Autorität.

---

## 1. Übersicht der Quellen

| Quelle | Importiert als | Domains | Konflikt-Risiko |
|--------|---------------|---------|-----------------|
| `Nutlope/hallmark` | `external-skills/design` | Anti-Slop-Design | 🟢 Niedrig |
| `bergside/awesome-design-skills` | `external-skills/design_awesome` | 67 Design-Stile | 🟡 Mittel |
| `seb1n/awesome-ai-agent-skills` | `external-skills/all_domains` | 103 Domains | 🟡 Mittel |
| `coreyhaines31/marketingskills` | `external-skills/marketing_aeo` | Marketing, Copy, SEO, AEO | 🟡 Mittel |
| `gamedev-skills/awesome-gamedev-agent-skills` | `external-skills/gamedev` | Game-Dev | 🟢 Niedrig |
| `samir-abis/cookiecomply-skills` | `external-skills/compliance_cookies` | DSGVO/Cookies | 🟢 Niedrig |
| `bloomprotocol/agent-visibility-skill` | `external-skills/geo_visibility` | GEO/AI-Visibility | 🟡 Mittel |

---

## 2. Konflikt-Matrix (Check → Quelle → Bewertung)

Legende: ✅ konform · ⚠️ Konfliktpotenzial · ❌ Konflikt (Blockade)

### Anti-Slop Text-Floskeln (T1–T10)

| Regel | hallmark | design_awesome | all_domains | marketing_aeo | gamedev | cookiecomply | geo_visibility |
|-------|----------|----------------|-------------|---------------|---------|--------------|----------------|
| T1 "This function does X" | ✅ (lehnt Floskeln ab) | ⚠️ (Style-Guides können generisch sein) | ⚠️ | ⚠️ (Copy-Skills nutzen Überzeugungs-Sprache) | ✅ | ✅ | ⚠️ |
| T2–T10 Conversation-Floskeln | ✅ | ✅ | ⚠️ (einige Skripte) | ⚠️ (Marketing-Ton) | ✅ | ✅ | ✅ |

**Entscheidung:** Die internen `validate_anti_slop.py`-Checks gelten für ALLEN generierten
Code — unabhängig von der externen Quelle. Text-Floskeln werden immer abgelehnt.

### Code-Muster (C1–C10)

| Regel | hallmark | design_awesome | all_domains | marketing_aeo | gamedev | cookiecomply | geo_visibility |
|-------|----------|----------------|-------------|---------------|---------|--------------|----------------|
| C1 Swallowed Errors | ✅ | ✅ | ✅ (skriptbasiert, konform) | ✅ | ✅ | ✅ | ✅ |
| C6 God Function | ✅ | ✅ | ✅ | ✅ | ⚠️ (Game-Code kann monolithisch sein) | ✅ | ✅ |
| C8 `any`/`unknown` | ✅ | ✅ | ✅ | ✅ | ⚠️ (GDScript/C# weniger strikt) | ✅ | ✅ |

**Entscheidung:** Game-Dev (GDScript, C#, Lua) unterliegt der internen Typpflicht nur
dort, wo die Sprache es unterstützt. Ausnahmen → ADR.

### UI-Muster (U1–U10)

| Regel | hallmark | design_awesome | all_domains | marketing_aeo | gamedev | cookiecomply | geo_visibility |
|-------|----------|----------------|-------------|---------------|---------|--------------|----------------|
| U1 Inline-Styles | ✅ (Token-Pflicht) | ⚠️ (jeder Stil hat eigene Regeln) | ✅ | ✅ | ✅ | ✅ | ✅ |
| U2 Hardcoded Farben | ✅ | ⚠️ (Stile definieren eigene Paletten) | ✅ | ✅ | ⚠️ (Game-Art) | ✅ | ✅ |
| U6 Semantische Elemente | ✅ | ⚠️ (Web-Stile) | ✅ | ✅ | ✅ (kein HTML) | ✅ | ✅ |
| U10 WCAG-Kontrast | ✅ | ⚠️ (Design-Stile können niedrigen Kontrast haben) | ✅ | ✅ | ✅ | ✅ | ✅ |

**Entscheidung:** Design-Stile aus `design_awesome` werden NUR als Ausgangspunkt genutzt.
Token-Hierarchie (`.quinsy-studio/studio-library/ui/tokens/`), WCAG-AA und die
Anti-Slop-UI-Regeln haben Vorrang. Stil-spezifische Paletten werden in Token übersetzt.

### Backend-Muster (B1–B8)

| Regel | hallmark | design_awesome | all_domains | marketing_aeo | gamedev | cookiecomply | geo_visibility |
|-------|----------|----------------|-------------|---------------|---------|--------------|----------------|
| B1 Secrets im Code | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ (SKILL.md enthält API-Key-Flows) |
| B2 SQL-Injection | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| B6 Rate-Limiting | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ (empfiehlt externe API-Nutzung) |

**Entscheidung:** `geo_visibility` (Bloom) empfiehlt MCP-Server und API-Keys — das ist
ein **Tooling-Referenz**, keine Codepflicht. Keys gehören in Secret-Manager, nie in Code.

### Zero-Data & DSGVO

| Regel | hallmark | design_awesome | all_domains | marketing_aeo | gamedev | cookiecomply | geo_visibility |
|-------|----------|----------------|-------------|---------------|---------|--------------|----------------|
| Zero-Data-Pipelines | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ (sendet URLs an Bloom-API) |
| DSGVO-konform | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ (Daten an Drittanbieter) |

**Entscheidung:** Bloom (`geo_visibility`) NUR als **offline-Referenz** für
llms.txt/JSON-LD-Muster nutzen. Der MCP-Server/API-Teil wird NICHT in Projekte
eingebunden ohne explizite DSGVO-Freigabe (Human-in-the-Loop).

---

## 3. Prioritäten-Reihenfolge (Konfliktfall)

```
1. internes anti_ai_slop_protocol.md        ← immer gewinnt
2. Zero-Data-Architecture / compliance_playbook
3. interne Team-Skills (.quinsy-studio/teams/)
4. studio-library Assets (geprüft, promoted)
5. externe Skills (nur als Werkzeug/Referenz)
```

---

## 4. Konkrete Konflikt-Beispiele

| Situation | Externe Tendenz | Interne Regel | Lösung |
|-----------|----------------|---------------|--------|
| `design_awesome/glassmorphism` will freie Farben | Eigene Palette | Token-Pflicht (U2) | Stil-Farben → Design-Tokens übersetzen |
| `marketing_aeo/copywriting` will "revolutionize" | Buzzwords | Blacklist T1-T10 | Copy prüfen lassen mit `validate_anti_slop.py` |
| `all_domains` Script will `catch(e){}` | Swallowed Error | C1 | Stub-Blocker: Fehler immer behandeln |
| `geo_visibility` will MCP + API-Key | Externe API | B1, Zero-Data | Nur Markdown-Muster nutzen, keine API-Anbindung |
| `gamedev` GDScript ohne Typen | Ungeprüfte Variablen | C8 | Typisierung wo GDScript es kann, sonst ADR |
| `cookiecomply` will Third-Party-CMP | Externer Banner-Dienst | Zero-Data | Eigenen Banner bauen (Studio-Library) |

---

## 5. Wartung

- Matrix nach jedem `./studio update-skills` prüfen (neue Quellen hinzufügen).
- Neue Quelle OHNE Zeile in dieser Matrix wird NICHT aktiviert (SO-002 Process Guard).
- Konflikte werden als Learning Items gemeldet (`./studio learn ... --signal conflict`).
