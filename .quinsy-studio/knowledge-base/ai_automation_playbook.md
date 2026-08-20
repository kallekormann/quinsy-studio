# AI Automation Playbook

> Token-Optimierung, RAG-Architektur, Agent-Systeme — die globalen AI-Standards.

## Grundprinzip

```
KI ist ein Werkzeug, kein Ersatz für Verstand.
Token sind teuer — nutze sie weise.
```

---

## Token-Optimierung

### Strategien

| Strategie | Beschreibung | Einsparung |
|-----------|-------------|-----------|
| **Prompt Engineering** | Klare, präzise Prompts | 20-40% |
| **Few-Shot Learning** | Beispiele statt Erklärungen | 30-50% |
| **Chunking** | Große Dokumente aufteilen | 50-70% |
| **Caching** | Häufige Queries zwischenspeichern | 40-60% |
| **Modellwahl** | Kleines Modell für einfache Aufgaben | 60-80% |

### Prompt-Template

```markdown
# System Prompt (minimal)

Du bist [Rolle]. Antworte [Format].

# Kontext (nur relevante Teile)

[Chunk 1]
[Chunk 2]

# Aufgabe

[Konkrete Frage]
```

### Cache-Strategie

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

## RAG-Architektur

### Architektur

```
┌─────────────────────────────────────────────────────────┐
│                    RAG PIPELINE                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────┐     ┌─────────────┐                   │
│  │  Document   │────▶│  Chunking   │                   │
│  │  Ingestion  │     │             │                   │
│  └─────────────┘     └──────┬──────┘                   │
│                             │                           │
│                      ┌──────▼──────┐                   │
│                      │ Embedding   │                   │
│                      │ Generation  │                   │
│                      └──────┬──────┘                   │
│                             │                           │
│                      ┌──────▼──────┐                   │
│                      │ Vector DB   │                   │
│                      │ (Pinecone,  │                   │
│                      │  Supabase)  │                   │
│                      └──────┬──────┘                   │
│                             │                           │
│  ┌─────────────┐     ┌──────▼──────┐                   │
│  │   User      │────▶│  Retrieval  │                   │
│  │   Query     │     │  + Ranking  │                   │
│  └─────────────┘     └──────┬──────┘                   │
│                             │                           │
│                      ┌──────▼──────┐                   │
│                      │   LLM +     │                   │
│                      │  Response   │                   │
│                      └─────────────┘                   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Implementierung

```typescript
// 1. Document Ingestion
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

// 2. Retrieval
async function retrieve(query: string, topK: number = 5) {
  const queryEmbedding = await generateEmbedding(query);
  const results = await vectorDB.query({
    vector: queryEmbedding,
    topK,
    includeMetadata: true
  });
  return results;
}

// 3. RAG Response
async function ragResponse(query: string) {
  const context = await retrieve(query);
  const prompt = buildRAGPrompt(query, context);
  return await llm.complete(prompt);
}
```

### Chunking-Strategien

| Strategie | Beschreibung | Use Case |
|-----------|-------------|----------|
| **Fixed Size** | Feste Größe (z.B. 500 Tokens) | Allgemein |
| **Recursive** | Nach Satzzeichen aufteilen | Natürliche Sprache |
| **Semantic** | Nach Themenwechsel | Dokumente |
| **Hierarchical** | Über-/Unterkategorien | Strukturierte Daten |

---

## Agent-Systeme

### Agent-Architektur

```
┌─────────────────────────────────────────────────────────┐
│                    AGENT LOOP                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────┐                                       │
│  │   Input     │                                       │
│  └──────┬──────┘                                       │
│         │                                               │
│  ┌──────▼──────┐                                       │
│  │   Plan      │                                       │
│  │  (LLM)     │                                       │
│  └──────┬──────┘                                       │
│         │                                               │
│  ┌──────▼──────┐     ┌─────────────┐                   │
│  │   Execute   │────▶│   Tools     │                   │
│  │  (Code)     │     │  (APIs, DB) │                   │
│  └──────┬──────┘     └─────────────┘                   │
│         │                                               │
│  ┌──────▼──────┐                                       │
│  │   Observe   │                                       │
│  │  (Result)   │                                       │
│  └──────┬──────┘                                       │
│         │                                               │
│  ┌──────▼──────┐                                       │
│  │   Reflect   │                                       │
│  │  (LLM)     │                                       │
│  └──────┬──────┘                                       │
│         │                                               │
│         └─────────────▶ Zurück zu Plan oder Stop       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Tool-Use

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

### Metriken

| Metrik | Beschreibung | Alert |
|--------|-------------|-------|
| **Latency** | Antwortzeit | > 5s |
| **Cost** | Token-Kosten | > Budget |
| **Errors** | Fehlerquote | > 5% |
| **Quality** | Nutzerzufriedenheit | < 3/5 |

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

## Referenzen

- `.quinsy-studio/teams/07-ai-autonomous-systems/` — AI-Team
- `.quinsy-studio/knowledge-base/anti_ai_slop_protocol.md` — AI-Slop-Regeln
- `.quinsy-studio/process/learning-loop.md` — Learning Loop
