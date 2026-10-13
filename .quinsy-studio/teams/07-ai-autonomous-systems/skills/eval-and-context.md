# Skill: Eval and Context (AI-004)

```
skill_id: AI-004
team: 07-ai-autonomous-systems
lead_role: Autonomous Systems Director
support_roles: [LLM Prompt Engineer]
```

Eval harness, RAG grounding, context-window budget, prompt cache. Pair AI-001 for the adapter, prompts and cost limits; AI-002 for slop; AI-005 (`ai-code-security-audit.md`) for prompt injection and LLM output sinks.

**Playbook:** [ai_automation_playbook.md](../../../knowledge-base/ai_automation_playbook.md)

## Do

- Named eval set (golden prompts + fail examples) before calling the ticket done.
- Truncate / summarize with a budget; do not dump the whole corpus into the window.
- RAG: cite retrieved chunks; empty-retrieval is a user-visible empty state (LO-0017).
- Receipt **## Eval**: what was scored, pass bar, and whether the live key was used or the empty state.

## Eval set rules

- Lives in the repo: `src/ai/evals/<feature>.jsonl`, one case per line with `input`, `expected` (exact value, schema, or rubric) and `kind` (`happy` | `edge` | `failure` | `injection`).
- At least one case of each kind. `injection` cases come from AI-005 (instructions hidden in user text, retrieved chunks and tool output); the pass bar is "ignored, normal answer or refusal".
- Run against the model id, temperature and `max_tokens` that production uses (AI-001). A pass on another model does not count.
- Score with checks a script can run: schema valid, exact field match, contains or excludes strings, citation IDs present and real. An LLM judge is allowed only with a written rubric and is reported separately.
- Every prompt, model or retrieval change re-runs the full set. The receipt reports before and after.
- Cases never contain real personal data.

## Context budget

- Fix the budget per call in config: system prompt, examples, retrieved context, user input, output reserve. Trim the lowest-ranked context first, never the instructions.
- Put the stable part (system prompt, examples) first so provider prompt caching can reuse it.
- Untrusted text goes in delimited blocks (AI-001 rule 2).

## RAG on our stack

- **Where:** pgvector in the Compose Postgres on the `rag` profile. Embeddings are computed by the Python worker; a Payload job only enqueues (payload-playbook). Production may point the worker at a hosted pgvector database; it is never Payload's database of record.
- **Chunks table:** `id`, `source_collection`, `source_id`, `locale`, `tenant_id` (if multi-tenant), `chunk_index`, `content`, `embedding vector(<dim>)`, `embedding_model`, `content_hash`, `updated_at`. Store the model id per row; a model change means re-embedding, not mixing vectors.
- **Index:** HNSW (`vector_cosine_ops`) on `embedding`; B-tree on `source_id`; GIN on the full-text column.
- **Chunking:** by structure first (headings, Lexical blocks, sections), then size. Keep the heading path as chunk metadata. Re-chunk only changed documents (compare `content_hash`) from a Payload `afterChange` hook that enqueues the job; delete chunks on document delete.
- **German full-text:** a generated column `tsv tsvector GENERATED ALWAYS AS (to_tsvector('german', content)) STORED` for German chunks; use the `simple` config for mixed or unknown language and `english` for English. Query with `websearch_to_tsquery` in the same config. Pick the config from `locale`, never hard-code `english`.
- **Hybrid search:** run vector and full-text queries, fuse with reciprocal rank fusion (score `1 / (60 + rank)` per list, the constant from the original RRF paper). Keyword-heavy corpora (product names, legal paragraphs, article numbers) need the full-text side.
- **Filters first:** `tenant_id`, `locale`, access scope and published state are `WHERE` clauses before ranking. Retrieval returns only chunks the requesting user could read through Payload access. A chunk from a draft or another tenant in the context is a data leak.
- **Retrieval eval:** a golden set of 20+ question → expected `source_id` pairs. Report recall@k and the share of answers whose citations point to those sources. Change one variable at a time (chunk size, k, fusion, re-ranker).
- **Re-ranker:** only when the retrieval eval shows precision is the problem and the latency budget allows it.

## Don't

- Fine-tune zoo / Megatron catalogs as product work.
- Vendor-lock observability (LangSmith/Langfuse are optional tools, not a studio default).
- Ship a model id that 404s (LO-0018).
- Embed inside the Next.js process.
- Retrieve before applying tenant, locale and access filters.
- Mix embeddings from two models in one index.

## Implement-fail

- AI-001/AI-004 ticket with no `## Eval` on the execution receipt (`move … done` refuses).
- Adapter + queue with no user-visible surface.
- Eval set without a `failure` or `injection` case.
- RAG ticket without the retrieval recall number.

**Tool:** `studio_skill_checks.ai_eval_receipt_issues`.
**Triggers:** eval, RAG, context window, prompt cache, agent evaluation, pgvector, embeddings, hybrid search.
