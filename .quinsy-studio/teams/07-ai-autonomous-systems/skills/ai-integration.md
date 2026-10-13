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
  - One adapter (not every cloud SDK on the CARD)
  - Eval set + user-visible surface same sprint (AI-004, LO-0017)
  - Provider switching via config; cost tracking
  - Do not list GPT/Claude/Cohere as the architecture
```

### 2. Prompt engineering

```markdown
Before writing the prompt:
  - Write the output contract first: JSON schema (validated with Zod) or an exact
    Markdown template, plus what counts as a pass
  - List 3+ test inputs: happy path, edge case, failure/refusal case (AI-004 eval set)

System prompt structure: Role → Task → Constraints → Output format → Examples
  - Role and task in one or two sentences; one job per prompt
  - Constraints are measurable: "at most 2 sentences", "max 5 tags", not "be concise"
  - Out-of-scope input gets a fixed fallback answer, written in the prompt
  - Few-shot examples are realistic and include one edge case
  - Ground facts in supplied context; do not rely on what the model may know
  - Untrusted text (user input, retrieved chunks, tool output, web pages) goes in
    clearly delimited blocks and is treated as data, never as instructions (AI-005)

Prompts are code:
  - Stored as files in the repo (`src/ai/prompts/<name>.v<N>.md`), never inline strings
  - Versioned with a changelog line per change; one change at a time
  - Pinned: model id, temperature, max output tokens recorded next to the prompt
  - Every change re-runs the AI-004 eval set before merge

Anti-slop in prompts:
  - Don't allow clichés
  - Require structured outputs
  - Build in quality checks
```

### 3. Token management and cost guardrails

```markdown
Optimization:
  - Keep the system prompt compact
  - Use few-shot examples efficiently
  - Keep an eye on the context window (AI-004 budget)
  - Cache repeated requests and use provider prompt caching for long fixed prefixes

Hard limits (all enforced in the adapter, not the caller):
  - Per request: `max_tokens` (output) set on every call; input trimmed to the
    context budget before the call. No call without both
  - Per user per day: token or cost budget stored in Postgres (a Payload collection
    or a counter table). Reserve the estimated cost before the call, settle after;
    over budget → a clear user-facing message (BE-004 rubric), no call
  - Per project per day: a global ceiling with an admin alert at a set fraction
  - Per job: a run budget; a loop or agent step that exceeds it stops and fails
    the job instead of retrying
  - Limits and model ids are config with env names in env.schema.json, not literals

Model fallback chain (named in the architecture doc):
  - Primary model → cheaper model of the same provider → static fallback or
    feature-off state
  - Fall back on timeout, 429, 5xx or a budget trip; never on a 4xx caused by our request
  - Trip a circuit breaker on repeated 402/429/5xx (BE-004); alert the admin
  - Retries count against the same budget; a timeout does not cancel provider billing

Cost logging:
  - One log row per call: feature, model, input tokens, output tokens, estimated
    cost, latency, outcome, user id (pseudonymous), request_id
  - Never log prompt or completion text that may contain personal data. If a
    sample is needed for debugging, store it redacted, opt-in, with a retention date (CL-004)
  - A daily rollup per feature and per user drives the budget checks and the admin view
```

### 4. Fallback strategies

```markdown
When an LLM call fails:
  1. Retry with another provider
  2. Fall back to a smaller model
  3. Static fallback (template)
  4. Graceful degradation (feature disabled)

Error handling:
  - Timeout: 30s (or the value in the architecture doc; fits the BE-004 budget)
  - Rate limit: exponential backoff, honor Retry-After
  - Invalid response: schema validation fails → one retry with the validation
    error appended, then fallback; never pass unvalidated output on
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
- A call without `max_tokens`
- Unbounded retry or agent loops
- Prompts or completions with personal data in logs
- Vague constraints ("be helpful", "be concise")
- Prompt strings inline in route code
- User or retrieved text concatenated into the instruction part of a prompt
```

### ✅ Instead

```markdown
- Provider abstraction layer
- Fallback chain (provider → smaller model → template)
- Budget limits and monitoring
- Rate limiting per user/request
- Anti-slop rules in prompts
- Per-request, per-user/day and per-project/day limits in the adapter
- Token and cost counts in logs, text redacted or absent
- Measurable constraints and a schema-validated output
- Versioned prompt files with pinned model settings
- Delimited untrusted input, treated as data (AI-005)
```

---

## Done evidence (receipt)

AI-001 tickets add to the AI-004 `## Eval` section:

- Model id, temperature and `max_tokens` used
- The per-user/day and per-project/day limits and where they are enforced
- One cost log line (trimmed) showing tokens and cost without prompt text
- Fallback tested: primary forced to fail → fallback or feature-off state shown

---

## References

- `.quinsy-studio/knowledge-base/ai_automation_playbook.md` — AI rules
- `.quinsy-studio/knowledge-base/anti_ai_slop_protocol.md` — anti-slop
- AI-004 eval and context, AI-005 AI-code security audit (prompt injection, LLM sinks)
- BE-004 timeouts and circuit breaker, CL-004 data minimization
