# Studio skill extensions

> Deep, codebase-aware playbooks that **extend** internal team skills (CL-*, GM-*, UX-*, PE-*).  
> **Not separate ticket IDs** — agents load these when an internal skill is active and the task needs audit depth.

## How to use

1. Ticket matches internal skill (e.g. `CL-002`, `UX-002`) via [skill-registry.md](../../teams/skill-registry.md)
2. Agent reads the thin team skill file under `teams/<NN>-*/skills/`
3. For audits, scans, or drafting → load the matching extension below
4. Extensions are subordinate to [anti_ai_slop_protocol.md](../anti_ai_slop_protocol.md) and Zero-Data Architecture

## Index

| Extension | Extends (internal) | Team | Use when |
|-----------|-------------------|------|----------|
| [delight-micro-interactions.md](delight-micro-interactions.md) | **UX-002**, FE-001 | 10, 01 | Audit empty/wait/peak-end only; rules in `delight-playbook.md` |
| [email-design.md](email-design.md) | **GM-003**, UX-007, BE-005 | 05, 10, 02 | Transactional/newsletter HTML, CTR copy, Outlook-safe tables |
| [product-led-growth.md](product-led-growth.md) | **GM-003**, **PS-001**, **GD-001**, PM-002 | 05, 04, 11, 06 | Viral loops, watermarks, share CTAs, usage-based paywalls, PQL events |
| [affiliate-compliance.md](affiliate-compliance.md) | **GM-001** | 05 | Affiliate links, `rel=sponsored`, disclosures (content/affiliate sites) |
| [privacy-legal-compliance.md](privacy-legal-compliance.md) | **CL-001** | 03 | GDPR/CCPA audit, click-wrap, consent logging, deletion, PII |
| [cookie-compliance.md](cookie-compliance.md) | **CL-002** | 03 | Cookie banner, CMP, script hydration, dark-pattern checks |
| [tos-architect.md](tos-architect.md) | **CL-003** | 03 | ToS/EULA from codebase (billing, AI, sub-processors, IP) |
| [compliance-orchestrator.md](compliance-orchestrator.md) | CL-001 + CL-002 + CL-003 (+ affiliate) | 03 | **Full-route audit** — orchestrator only, not a ticket skill |
| [frontend-security-auditor.md](frontend-security-auditor.md) | **PE-003**, FE-004 | 08, 01 | XSS, CSP, client auth, CSRF, secrets in FE |
| [backend-security-auditor.md](backend-security-auditor.md) | **PE-003**, BE-003 | 08, 02 | BOLA, injection, SSRF, mass assignment, rate limits |

## Intake staging

Human drafts land in `intake/skills/` (gitignored). After review, promote copies here and update team skill pointers.
