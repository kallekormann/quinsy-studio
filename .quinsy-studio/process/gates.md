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

> **Adopted repo:** gate 0 is **as-built truth** + a synthesized PRD, not a greenfield intake. See [brownfield-adopt.md](brownfield-adopt.md). `./studio approve --gate 0` still requires filled `docs/as-built/` (no `_TODO_`).

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
| 3.7 | Design science audit (`design_math.py`) on token pairs + nav | script check | recommended |

Run contrast / IA checks when `ui/tokens/design-tokens.css` exists:

```bash
python3 .quinsy-studio/studio-tools/design_math.py --audit-tokens projects/<p>/ui/tokens/design-tokens.css
```

---

## Gate 4 — Implementation Gate

```bash
./studio gate <project> --level 4
```

### Checkpoints

| # | Check | Method | Weight |
|---|-------|--------|--------|
| 4.1 | Tests green (`pnpm test` / `npm test`) | shell check | required |
| 4.2 | TypeScript without errors | `tsc --noEmit` | required |
| 4.3 | ESLint + Prettier clean | linter check | required |
| 4.4 | Code review done | field check | recommended |

> **Note:** Level 4 does **not** include build or runtime smoke. Do not mark tickets `done` at level 4.

---

## Gate 5 — QA Gate (required before `done`)

```bash
./studio gate <project> --level 5
```

**Enforced:** `./studio move <project> <TICKET> done` fails unless the latest gate run is level **5** and status **passed**.

### Checkpoints

| # | Check | Method | Weight |
|---|-------|--------|--------|
| 5.1 | Production build successful | `next build` | required |
| 5.2 | **Runtime smoke routes** | Playwright via `docs/smoke-routes.json` | required (when config present) |
| 5.3 | Unit tests green | Vitest/Jest | required |
| 5.4 | No critical/high security issues | npm audit | warning |
| 5.5 | Anti-slop audit: 0 violations | anti-slop check | required |
| 5.6 | Skill-matching (studio registry) | studio check | required |

### Runtime smoke (web apps)

**LO-0052 — durable Playwright browsers:** `./studio gate` sets `PLAYWRIGHT_BROWSERS_PATH` to `.quinsy-studio/.cache/playwright/<project>/` (gitignored). Do not rely on Cursor sandbox temp caches; they rotate and often mismatch mac-arm64 vs mac-x64. First gate may download Chromium once; later gate runs reuse the cache.

**LO-0071 — agent sandbox Chromium SIGSEGV:** Cursor and some CI sandboxes cannot launch Playwright Chromium (SIGSEGV / kill EPERM). Agents may set `QUINSY_SKIP_SMOKE=1` **only** for gate level 5 in that environment — gate output must record the skip explicitly (`run_qa_gate.py` returns “Skipped — QUINSY_SKIP_SMOKE set”). Human local runs and sprint-review smoke must leave it unset; skipping is not a substitute for browser verification before review.

Add `projects/<p>/docs/smoke-routes.json`:

```json
{
  "description": "Critical user paths",
  "command": "npm run smoke",
  "requires_build": true
}
```

Implement `scripts/smoke-routes.mjs` (Playwright) to visit home, redirects, and client-heavy routes (e.g. canvas). Catches runtime crashes that lint/build miss — e.g. react-konva + Next.js bundling errors.

---

## Gate 5 (legacy doc) — extended QA

The following are **planned** for level 6+; not yet automated in `run_qa_gate.py`:

| # | Check | Method | Weight |
|---|-------|--------|--------|
| 5.7 | Core web vitals in budget | performance check | planned |
| 5.8 | Lighthouse score ≥ 90 | shell check | planned |
| 5.9 | GDPR compliant | compliance check | planned |
| 5.10 | Accessibility checked | a11y check | planned |
| 5.11 | Cross-browser tested | field check | recommended |

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
