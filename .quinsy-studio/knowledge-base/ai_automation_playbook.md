# AI Automation Playbook

> Token optimization, RAG architecture, agent systems — the global AI standards.

## Core principle

```
AI is a tool, not a substitute for judgment.
Tokens are expensive — use them wisely.
```

---

## Token optimization

### Strategies

| Strategy | Description | Savings |
|----------|-------------|---------|
| **Prompt engineering** | clear, precise prompts | 20-40% |
| **Few-shot learning** | examples instead of explanations | 30-50% |
| **Chunking** | split large documents | 50-70% |
| **Caching** | cache frequent queries | 40-60% |
| **Model selection** | small model for simple tasks | 60-80% |

### Prompt template

```markdown
# System prompt (minimal)

You are [role]. Answer [format].

# Context (only relevant parts)

[Chunk 1]
[Chunk 2]

# Task

[Concrete question]
```

### Cache strategy

```typescript
const cache = new Map();

async function cachedLLM(prompt: string): Promise<string> {
  const hash = crypto.createHash('md5').update(prompt).digest('hex');
  
  if (cache.has(hash)) {
    return cache.get(hash);
  }
  
  const result = await llm.complete(prompt);
  cache.set(hash, result);
  return result;
}
```

---

## RAG architecture

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    RAG PIPELINE                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────┐     ┌─────────────┐                   │
│  │  Document   │────▶│  Chunking   │                   │
│  │  ingestion  │     │             │                   │
│  └─────────────┘     └──────┬──────┘                   │
│                             │                           │
│                      ┌──────▼──────┐                   │
│                      │ embedding   │                   │
│                      │ generation  │                   │
│                      └──────┬──────┘                   │
│                             │                           │
│                      ┌──────▼──────┐                   │
│                      │ vector DB   │                   │
│                      │ (Pinecone,  │                   │
│                      │  Supabase)  │                   │
│                      └──────┬──────┘                   │
│                             │                           │
│  ┌─────────────┐     ┌──────▼──────┐                   │
│  │   user      │────▶│  retrieval  │                   │
│  │   query     │     │  + ranking  │                   │
│  └─────────────┘     └──────┬──────┘                   │
│                             │                           │
│                      ┌──────▼──────┐                   │
│                      │   LLM +     │                   │
│                      │  response   │                   │
│                      └─────────────┘                   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Implementation

```typescript
// 1. document ingestion
async function ingestDocument(doc: Document) {
  const chunks = chunkDocument(doc, { size: 500, overlap: 50 });
  
  for (const chunk of chunks) {
    const embedding = await generateEmbedding(chunk.text);
    await vectorDB.upsert({
      id: chunk.id,
      values: embedding,
      metadata: { source: doc.source, page: chunk.page }
    });
  }
}

// 2. retrieval
async function retrieve(query: string, topK: number = 5) {
  const queryEmbedding = await generateEmbedding(query);
  const results = await vectorDB.query({
    vector: queryEmbedding,
    topK,
    includeMetadata: true
  });
  return results;
}

// 3. RAG response
async function ragResponse(query: string) {
  const context = await retrieve(query);
  const prompt = buildRAGPrompt(query, context);
  return await llm.complete(prompt);
}
```

### Chunking strategies

| Strategy | Description | Use case |
|----------|-------------|----------|
| **Fixed size** | fixed size (e.g. 500 tokens) | general |
| **Recursive** | split by punctuation | natural language |
| **Semantic** | split at topic changes | documents |
| **Hierarchical** | super-/subcategories | structured data |

---

## Agent systems

### Agent architecture

```
┌─────────────────────────────────────────────────────────┐
│                    AGENT LOOP                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────┐                                       │
│  │   input     │                                       │
│  └──────┬──────┘                                       │
│         │                                               │
│  ┌──────▼──────┐                                       │
│  │   plan      │                                       │
│  │  (LLM)      │                                       │
│  └──────┬──────┘                                       │
│         │                                               │
│  ┌──────▼──────┐     ┌─────────────┐                   │
│  │   execute   │────▶│   tools     │                   │
│  │  (code)     │     │  (APIs, DB) │                   │
│  └──────┬──────┘     └─────────────┘                   │
│         │                                               │
│  ┌──────▼──────┐                                       │
│  │   observe   │                                       │
│  │  (result)   │                                       │
│  └──────┬──────┘                                       │
│         │                                               │
│  ┌──────▼──────┐                                       │
│  │   reflect   │                                       │
│  │  (LLM)      │                                       │
│  └──────┬──────┘                                       │
│         │                                               │
│         └─────────────▶ back to plan or stop           │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Tool use

```typescript
const tools = [
  {
    name: 'search_database',
    description: 'Search the database for records',
    parameters: {
      query: { type: 'string', description: 'SQL query' }
    },
    execute: async (params) => await db.query(params.query)
  },
  {
    name: 'call_api',
    description: 'Call an external API',
    parameters: {
      url: { type: 'string', description: 'API endpoint' },
      method: { type: 'string', enum: ['GET', 'POST'] }
    },
    execute: async (params) => await fetch(params.url, { method: params.method })
  }
];
```

### Guardrails

```typescript
const guardrails = {
  maxTokens: 4000,
  maxToolCalls: 10,
  timeout: 30000,
  blockedPatterns: [
    /sudo/,
    /rm -rf/,
    /DROP TABLE/,
  ],
  requireConfirmation: [
    'delete',
    'deploy',
    'publish'
  ]
};
```

---

## Monitoring

### Metrics

| Metric | Description | Alert |
|--------|-------------|-------|
| **Latency** | response time | > 5s |
| **Cost** | token costs | > budget |
| **Errors** | error rate | > 5% |
| **Quality** | user satisfaction | < 3/5 |

### Logging

```typescript
function logLLMCall(call: LLMCall) {
  console.log(JSON.stringify({
    timestamp: new Date().toISOString(),
    model: call.model,
    inputTokens: call.inputTokens,
    outputTokens: call.outputTokens,
    latency: call.latency,
    cost: calculateCost(call),
    success: call.success
  }));
}
```

---

## References

- `.quinsy-studio/teams/07-ai-autonomous-systems/` — AI team
- `.quinsy-studio/knowledge-base/anti_ai_slop_protocol.md` — AI slop rules
- `.quinsy-studio/process/learning-loop.md` — learning loop
