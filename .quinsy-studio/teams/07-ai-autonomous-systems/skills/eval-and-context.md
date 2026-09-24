# Skill: Eval and Context (AI-004)

```
skill_id: AI-004
team: 07-ai-autonomous-systems
lead_role: Autonomous Systems Director
support_roles: [LLM Prompt Engineer]
```

Eval harness, RAG grounding, context-window budget, prompt cache. Pair AI-001 for the adapter; AI-002 for slop; PE-003 for prompt-injection (defensive).

**Playbook:** [ai_automation_playbook.md](../../../knowledge-base/ai_automation_playbook.md)

## Do

- Named eval set (golden prompts + fail examples) before calling the ticket done.
- Truncate / summarize with a budget; do not dump the whole corpus into the window.
- RAG: cite retrieved chunks; empty-retrieval is a user-visible empty state (LO-0017).
- Receipt **## Eval**: what was scored, pass bar, and whether the live key was used or the empty state.

## Don’t

- Fine-tune zoo / Megatron catalogs as product work.
- Vendor-lock observability (LangSmith/Langfuse are optional tools, not a studio default).
- Ship a model id that 404s (LO-0018).

## Implement-fail

- AI-001/AI-004 ticket with no `## Eval` on the execution receipt (`move … done` refuses).
- Adapter + queue with no user-visible surface.

**Tool:** `studio_skill_checks.ai_eval_receipt_issues`.  
**Triggers:** eval, RAG, context window, prompt cache, agent evaluation.
