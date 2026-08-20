# Skill: AI Integration

> LLM-Integration, Prompt Engineering, Token-Management, Fallback-Strategien

## Metadata

```
skill_id: AI-001
name: AI Integration
team: 07-ai-autonomous-systems
lead_role: AI Architect
support_roles: [Backend Engineer, LLM Prompt Engineer]
phases: [2, 3, 4, 5]
activation_triggers:
  - Ticket enthält "AI", "LLM", "GPT", "Claude", "Prompt"
  - Phase 2: KI-Architektur wird definiert
  - Phase 3: KI-Features werden geplant
  - Phase 4: KI wird implementiert
  - Phase 5: KI-QA
```

---

## Verhaltensregeln

### 1. LLM-Integration

```markdown
Provider:
  - OpenAI (GPT-4o, GPT-4o-mini) — Standard
  - Anthropic (Claude) — Für komplexe Analysen
  - Cohere — Für Embeddings
  - Self-Hosted (Llama, Mistral) — Für Data Privacy

Architektur:
  - Abstraktionsschicht (nicht direkt Provider-SDK)
  - Provider-Switching via Config
  - Kosten-Tracking pro Provider
```

### 2. Prompt Engineering

```markdown
System-Prompt:
  - Klare Rolle definieren
  - Output-Format vorgeben
  - Constraints setzen
  - Beispiele (Few-Shot)

User-Prompt:
  - Kontext liefern
  - Spezifische Anfrage
  - Format-Vorgabe

Anti-Slop in Prompts:
  - Keine Floskeln erlauben
  - Strukturierte Outputs verlangen
  - Qualitäts-Checks einbauen
```

### 3. Token-Management

```markdown
Optimierung:
  - System-Prompt kompakt halten
  - Few-Shot Examples effizient nutzen
  - Context Window im Auge behalten
  - Cache für wiederholte Anfragen

Kosten-Kontrolle:
  - Maximale Tokens pro Request
  - Rate-Limiting pro User
  - Budget-Alerts
  - Modell-Selection (günstig = mini)
```

### 4. Fallback-Strategien

```markdown
Wenn LLM-Aufruf fehlschlägt:
  1. Retry mit anderem Provider
  2. Fallback auf kleineres Modell
  3. Statisches Fallback (Template)
  4. Graceful Degradation (Feature deaktiviert)

Error-Handling:
  - Timeout: 30s
  - Rate Limit: exponential backoff
  - Invalid Response: Retry mit Stricter Prompt
```

### 5. Streaming

```markdown
Für User-Interfaces:
  - SSE (Server-Sent Events) für Streaming
  - Token-by-Token Output
  - Abbruch-Möglichkeit
  - Progressive UI-Updates
```

---

## Anti-Patterns

### ❌ Verboten

```markdown
- Direkte Provider-APIs ohne Abstraktion
  - Kein Fallback bei LLM-Ausfall
  - Unkontrollierte Token-Kosten
  - Kein Rate-Limiting
  - Prompts ohne Anti-Slop-Regeln
```

### ✅ Stattdessen

```markdown
- Provider-Abstraktionsschicht
  - Fallback-Kette (Provider → kleineres Modell → Template)
  - Budget-Limits und Monitoring
  - Rate-Limiting pro User/Request
  - Anti-Slop-Regeln in Prompts
```

---

## Referenzen

- `.quinsy-studio/knowledge-base/ai_automation_playbook.md` — AI-Regeln
- `.quinsy-studio/knowledge-base/anti_ai_slop_protocol.md` — Anti-Slop
