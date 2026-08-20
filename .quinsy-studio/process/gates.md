# Quinsy Studio — Gates

> Every gate is a quality checkpoint. No gate is manually set to "green" — it is checked automatically.

## Terminology: Phase Gates vs QA Levels

Quinsy Studio uses **two separate gate systems**. Do not conflate them.

| System | CLI | Purpose | Docs |
|--------|-----|---------|------|
| **Phase Gates** | `./studio approve --gate N` | Human checkpoints in the 7-phase lifecycle | This file (Phase Gate 0–6) |
| **QA Levels** | `./studio gate --level N` | Automated tooling checks (lint, types, tests, build) | `run_qa_gate.py` |

- **Phase Gate 1** = human approval after concept/design blueprint (`./studio approve --gate 1`)
- **QA Level 5** = automated full QA run (`./studio gate --level 5`) — not the same as Phase Gate 5

## Gate philosophy

```
Gate = automated check + human confirmation
```

- **Automated:** as much as possible is checked by tooling
- **Human:** irreversible decisions wait for approval
- **No bypass:** a gate cannot be skipped

---

## Gate 0 — Conception Gate

```bash
./studio gate <project> --level 0
```

> **Note:** `--level` runs **QA Levels** (automated checks). Phase Gate 0 checkpoints below are the lifecycle conception gate; implement via `./studio gate --level 0` plus manual ADR/definitions review until fully automated.

### Checkpoints

| # | Check | Method | Weight |
|---|-------|--------|--------|
| 0.1 | PRD present | file check | required |
| 0.2 | PRD contains: problem, target audience, scope, KPIs | structure check | required |
| 0.3 | Archetype determined | field check | required |
| 0.4 | Complexity level estimated | field check | required |
| 0.5 | At least 1 ADR present | file check | required |
| 0.6 | Open questions documented | content check | recommended |

### Gate output
```
Gate 0: Conception
━━━━━━━━━━━━━━━━━━
[✓] PRD present (docs/intake/prd.md)
[✓] Problem defined
[✓] Target audience defined
[✓] Scope defined (P0/P1/P2)
[✓] KPIs defined
[✓] Archetype: saas-application
[✓] Complexity: P1
[✓] ADRs: 1 present
[~] Open questions: 3 (documented)
━━━━━━━━━━━━━━━━━━
Result: GREEN ✓
```

---

## Gate 1 — Validation Gate

```bash
./studio gate <project> --level 1
```

### Checkpoints

| # | Check | Method | Weight |
|---|-------|--------|--------|
| 1.1 | Technical spike present | file check | required |
| 1.2 | Competitive analysis present | file check | required |
| 1.3 | Technology stack defined | field check | required |
| 1.4 | Assumptions validated | content check | required |
| 1.5 | Go/no-go decision documented | ADR check | required |

---

## Gate 2 — Architecture Gate

```bash
./studio gate <project> --level 2
```

### Checkpoints

| # | Check | Method | Weight |
|---|-------|--------|--------|
| 2.1 | Architecture diagram present | file check | required |
| 2.2 | Data model defined | file check | required |
| 2.3 | API specification present | file check | required |
| 2.4 | Infrastructure plan present | file check | required |
| 2.5 | Security architecture defined | content check | required |
| 2.6 | All ADRs present | file count | required |

---

## Gate 3 — Design Gate

```bash
./studio gate <project> --level 3
```

### Checkpoints

| # | Check | Method | Weight |
|---|-------|--------|--------|
| 3.1 | DESIGN.md present | file check | required |
| 3.2 | Design tokens defined | file check | required |
| 3.3 | UI components present | directory check | required |
| 3.4 | Page types defined | file check | required |
| 3.5 | Color mode (dark/light) defined | content check | recommended |
| 3.6 | Animation defined | content check | recommended |

---

## Gate 4 — Implementation Gate

```bash
./studio gate <project> --level 4
```

### Checkpoints

| # | Check | Method | Weight |
|---|-------|--------|--------|
| 4.1 | Tests green (`pnpm test` / `npm test`) | shell check | required |
| 4.2 | Build successful (`pnpm build`) | shell check | required |
| 4.3 | No critical/high security issues | dependency scan | required |
| 4.4 | TypeScript/ESLint without errors | linter check | required |
| 4.5 | Code review done | field check | recommended |

### Shell checks
```bash
# Test check
pnpm test -- --reporter=json 2>/dev/null | jq '.numFailedTests == 0'

# Build check
pnpm build 2>&1 | tail -1 | grep -q "Successfully"

# Lint check
pnpm lint 2>&1 | grep -q "0 errors"
```

---

## Gate 5 — QA Gate (the strictest gate)

```bash
./studio gate <project> --level 5
```

### Checkpoints

| # | Check | Method | Weight |
|---|-------|--------|--------|
| 5.1 | All E2E tests green | shell check | required |
| 5.2 | Core web vitals in budget | performance check | required |
| 5.3 | Lighthouse score ≥ 90 | shell check | required |
| 5.4 | No critical/high security issues | OWASP scan | required |
| 5.5 | GDPR compliant | compliance check | required |
| 5.6 | Anti-slop audit: 0 violations | anti-slop check | required |
| 5.7 | Accessibility checked | a11y check | required |
| 5.8 | Cross-browser tested | field check | recommended |

### Anti-slop audit (detail)
```bash
./studio gate <project> --anti-slop
```

Checks for:
- Redundant variables, unnecessary imports
- Dead code
- Excessive comments (AI-typical verbose patterns)
- Unusual code patterns (e.g. `// This function does X`)
- Missing error handling
- Unused dependencies

---

## Gate 6 — Release Gate

```bash
./studio gate <project> --level 6
```

### Checkpoints

| # | Check | Method | Weight |
|---|-------|--------|--------|
| 6.1 | Deployment successful | field check | required |
| 6.2 | Monitoring active | field check | required |
| 6.3 | Rollback strategy present | file check | required |
| 6.4 | Release notes present | file check | required |
| 6.5 | Smoke tests passed | field check | required |

---

## Gate status

Every gate has one of four statuses:

| Status | Meaning |
|--------|---------|
| `open` | Not checked yet |
| `red` | Check failed (fix needed) |
| `green` | Check passed |
| `blocked` | Waiting for a human decision |

---

## Gate history

The gate history is logged in the project's `status.json`:

```json
{
  "gate_history": [
    {
      "gate": 0,
      "status": "green",
      "passed_at": "2026-08-19T10:00:00Z",
      "checked_by": "studio-cli"
    },
    {
      "gate": 1,
      "status": "red",
      "failed_at": "2026-08-19T11:00:00Z",
      "reason": "Competitive analysis missing"
    }
  ]
}
```

---

## References

- `.quinsy-studio/process/anti-slop.md` — anti-slop audit in detail
- `.quinsy-studio/process/lifecycle.md` — overview of all phases
- `./studio gate <project>` — run the gate
