# Skill: Client Security (FE-007)

```
skill_id: FE-007
team: 01-frontend-experience
lead_role: Frontend Security Engineer
```

XSS, CSP, and token handling **in the browser**. Server auth stays BE-003 / PE-003.

**Playbook:** [frontend_playbook.md](../../../knowledge-base/frontend_playbook.md)  
**Extension:** [frontend-security-auditor.md](../../../knowledge-base/skill-extensions/frontend-security-auditor.md)

**Do:** treat every string from the network as untrusted; CSP in product docs; session tokens stay httpOnly (never `NEXT_PUBLIC_` secrets).  
**Don’t:** `dangerouslySetInnerHTML` without a documented sanitizer; put vendor keys in the client bundle.  
**Implement-fail:** XSS sink shipped on a changed surface; secret name leaked into client env.

**Tool:** `studio_skill_checks.py` (gate 5 warn). Pair PE-003 for threat model — defensive only, no pentest catalogs.
