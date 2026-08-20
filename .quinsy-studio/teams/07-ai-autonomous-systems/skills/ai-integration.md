# Skill: AI Integration

> LLM integration, prompt engineering, token management, fallback strategies

## Metadata

```
skill_id: AI-001
name: AI Integration
team: 07-ai-autonomous-systems
lead_role: AI Architect
support_roles: [Backend Engineer, LLM Prompt Engineer]
phases: [2, 3, 4, 5]
activation_triggers:
  - Ticket contains "AI", "LLM", "GPT", "Claude", "prompt"
  - Phase 2: AI architecture is defined
  - Phase 3: AI features are planned
  - Phase 4: AI is implemented
  - Phase 5: AI QA
```

---

## Behavior rules

### 1. LLM integration

```markdown
Providers:
  - OpenAI (GPT-4o, GPT-4o-mini) — standard
  - Anthropic (Claude) — for complex analyses
  - Cohere — for embeddings
  - Self-hosted (Llama, Mistral) — for data privacy

Architecture:
  - Abstraction layer (not the provider SDK directly)
  - Provider switching via config
  - Cost tracking per provider
```

### 2. Prompt engineering

```markdown
System prompt:
  - Define a clear role
  - Specify the output format
  - Set constraints
  - Examples (few-shot)

User prompt:
  - Provide context
  - Specific request
  - Format specification

Anti-slop in prompts:
  - Don't allow clichés
  - Require structured outputs
  - Build in quality checks
```

### 3. Token management

```markdown
Optimization:
  - Keep the system prompt compact
  - Use few-shot examples efficiently
  - Keep an eye on the context window
  - Cache repeated requests

Cost control:
  - Maximum tokens per request
  - Rate limiting per user
  - Budget alerts
  - Model selection (cheap = mini)
```

### 4. Fallback strategies

```markdown
When an LLM call fails:
  1. Retry with another provider
  2. Fall back to a smaller model
  3. Static fallback (template)
  4. Graceful degradation (feature disabled)

Error handling:
  - Timeout: 30s
  - Rate limit: exponential backoff
  - Invalid response: retry with a stricter prompt
```

### 5. Streaming

```markdown
For user interfaces:
  - SSE (server-sent events) for streaming
  - Token-by-token output
  - Cancellation option
  - Progressive UI updates
```

---

## Anti-patterns

### ❌ Forbidden

```markdown
- Direct provider APIs without abstraction
- No fallback on LLM failure
- Uncontrolled token costs
- No rate limiting
- Prompts without anti-slop rules
```

### ✅ Instead

```markdown
- Provider abstraction layer
- Fallback chain (provider → smaller model → template)
- Budget limits and monitoring
- Rate limiting per user/request
- Anti-slop rules in prompts
```

---

## References

- `.quinsy-studio/knowledge-base/ai_automation_playbook.md` — AI rules
- `.quinsy-studio/knowledge-base/anti_ai_slop_protocol.md` — anti-slop
