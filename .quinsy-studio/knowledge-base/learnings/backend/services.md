# backend / services

Portable studio principles (not project incidents).
Matching playbook/skill: `knowledge-base/backend_playbook.md`.

## Principles

- **PB-20260927-001** helpful=1 harmful=0 :: Verify the provider signature on every vendor webhook before any write. A reachable endpoint is normal. An unsigned request must leave stored data unchanged.
- **LO-0352** 2026-09-26 :: Vendor webhooks must verify the provider signature. A reachable URL is normal. An unsigned writer is never the standard.
  - Vendor webhooks must verify the provider signature. A reachable URL is normal. An unsigned writer is never the standard.
