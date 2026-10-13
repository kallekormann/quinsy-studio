# Quinsy Studio — Gates

> Every gate is a quality checkpoint. No gate is manually set to "green" — it is checked automatically.

## Terminology: Phase Gates vs QA Levels

Quinsy Studio uses **two separate gate systems**. Do not conflate them.

| System | CLI | Purpose | Docs |
|--------|-----|---------|------|
| **Phase Gates** | `./studio approve --gate 0\|1\|2a\|2b` | Human checkpoints (0 PRD, 1 architecture, 2a direction, 2b project kit) | This file (human 2a/2b) + QA Gate 2/3 below |
| **QA Levels** | `./studio gate --level N` | Automated tooling checks (lint, types, tests, build) | `run_qa_gate.py` |

- **Human 2a / 2b** = signed design packets (`./studio approve --gate 2a` then `--gate 2b`). Bare `--gate 2` is refused. Legacy `human_gates.2` still counts as design-complete.
- **Phase Gate 1** = human approval after architecture (`./studio approve --gate 1`)
- **QA Level 5** = automated full QA run (`./studio gate --level 5`) — not the same as Phase Gate 5

## Gate philosophy

```
Gate = automated check + human confirmation
```

- **Automated:** as much as possible is checked by tooling
- **Human:** irreversible decisions wait for approval
- **No bypass:** a gate cannot be skipped
- **Sequential human gates:** `./studio approve --gate N` refuses unless the previous human gate is already approved (re-approving the same gate is allowed). Order: **0 → 1 → 2a → 2b**. Gate 1 cannot run while gate 0 is pending; 2a cannot run while 1 is pending; 2b cannot run while 2a is pending.

**Human design packets (not QA `--level 2`):**

| Gate | Approves | CLI |
|------|----------|-----|
| **2a** | Discovery Q&A + unique `DESIGN.md` + `DIRECTION-CRITIQUE.md` all PASS (blocks prototype) | `./studio design --discovery` then `./studio approve --gate 2a` |
| **2b** | Pulled library kit, project CSS tokens, shell routes, sticker inventory, mocks on those tokens. Approval copies the prototype into the product app. | `./studio design` then `./studio approve --gate 2b`. Iterate: `./studio revise --gate 2b` |

QA **Gate 2** below is architecture *level* checks. Do not conflate with human 2a/2b. If the shipped change only flipped a flag, enum, or CSS class and a flicker/regression remains, open a **new** ticket that changes the render path (mount, effect, animation, layout). Do not treat a second status-only patch as the fix.

**Prod infra regression after a “fixed” ship (LO-0176):** If realtime, websockets, or similar production plumbing fails again after a claimed fix, the next tickets are **research + instrumentation** (repro, logs, metrics, hypothesis) — not another speculative code patch.

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
>
> **LO-0137 — project-local Prettier/ESLint:** `./studio gate` must run `npx --no-install prettier` / `eslint` / `tsc` / `vitest` so QA uses the project's `node_modules` binary. Bare `npx prettier` can download a different Prettier and fail a tree that is already formatted with the project version.

---

## Gate 5 — QA Gate (required before `done`)

```bash
./studio gate <project> --level 5
```

**Enforced:** `./studio move <project> <TICKET> done` fails unless the latest gate run is level **5** and status **passed**.

**LO-0145 — tests inside Compose:** `phpunit.xml` `force` env is not enough when Compose injects `DB_*` into the PHP process. The test `TestCase` must pin the isolated test database name in process env **before** the application boots / `RefreshDatabase`. Never run schema refresh against the operator tenant database.

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

**LO-0166 — warm the cache before smoke-heavy sprints:** Before a sprint that will run level-5 smoke repeatedly (or after OS/Playwright upgrades), run the project’s `npm run smoke:install` (or equivalent) once so Chromium is already under `.quinsy-studio/.cache/playwright/<project>/`. Cold/incomplete caches surface as `smoke_routes` exit 1 with “unsupported OS / downloading fallback” noise and can falsely block tickets.

**LO-0071 / LO-0132 — agent sandbox Chromium SIGSEGV:** Cursor and some CI sandboxes cannot launch Playwright Chromium (SIGSEGV / kill EPERM). Agents may set `QUINSY_SKIP_SMOKE=1` **only** as a last resort inside that sandbox — gate output must record the skip explicitly (`run_qa_gate.py` returns “Skipped — QUINSY_SKIP_SMOKE set”). **Before `./studio move … done`:** re-run `npm run smoke` (or `./studio gate … --level 5`) in an **unrestricted** environment so Chromium actually launches. Skipping alone is not done. Human local runs and sprint-review smoke leave `QUINSY_SKIP_SMOKE` unset.

**LO-0165 — npm_audit is soft:** Level 5 `npm_audit` (e.g. moderate Vitest advisory) is a **warning**. `run_qa_gate.py` excludes it from RESULT. Agents must not treat a soft `npm_audit` ❌ as a hard gate failure when RESULT is True / hard checks are green. Report output labels soft fails explicitly.

Add `projects/<p>/docs/smoke-routes.json`:

```json
{
  "description": "Critical user paths",
  "command": "npm run smoke",
  "requires_build": true
}
```

Implement `scripts/smoke-routes.mjs` (Playwright) to visit home, redirects, and client-heavy routes (e.g. canvas). Catches runtime crashes that lint/build miss — e.g. react-konva + Next.js bundling errors.

**LO-0139 / LO-0140 — legal disclosure vs network reality:** If Privacy (or equivalent) claims third-party font CDNs are **not** used pre-auth / for anonymous visitors, the same sprint’s DoD must include a **network assert** on those surfaces (marketing home **and** anonymous public share/presentation if they exist). Shipping disclosure copy alone while anonymous share still injects `fonts.googleapis.com` is not done.

**LO-0143 — plan soft-path DoD:** If a ticket wires Pro/upgrade soft-path to Settings Account, DoD is not “URL changed.” Before `move … done`, assert for a **free** account (unit, UI, or smoke): Free plan label + Upgrade CTA visible on that tab, **or** upgrade dialog auto-opens from the soft-path query. Redirect-only fixes without a free-tier assert leave review gaps.

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

## Ticket state parity (LO-0246, LO-0248)

- **PB-20260914-001** helpful=0 harmful=0 :: The studio state machine is the single source of truth for sprint progress. Code landing without its ticket moving is drift: close every ticket **in the same session the code lands** — receipt filled, gate 5 green, `move done` — never let implementation run ahead of ticket state. A sprint is not "review-claimed done"; it is done when `./studio execute` reaches the review/retro step with zero open sprint tickets. If a sprint is found with shipped code but open tickets, reconstruct verification ticket-by-ticket (run each Verify block) before moving anything to done.

## Deltas

- **PB-20261013-003** helpful=0 harmful=0 :: A PRD rewrite must keep the original specification unchanged and must not drop normative details to fit a length cap. (carried over from the retired learnings catalog, was PB-20260927-001)
- **PB-20261013-002** helpful=0 harmful=0 :: A stack and host named in the PRD must win over the archetype default, and that delta must be an ADR. (carried over from the retired learnings catalog, was PB-20260927-002)
- **PB-20261013-001** helpful=0 harmful=0 :: Gate feedback must be a gate revision and must not be queued as a sprint inbox note while execute is waiting on a human gate. (carried over from the retired learnings catalog, was PB-20260927-003)
- **PB-20260922-001** helpful=0 harmful=0 :: A typeface placed in a composition zone is Primary until the operator picks another. Placement without promoting Primary is not done.
- **PB-20260916-005** helpful=0 harmful=0 :: When host-scoped live chrome never leaves loading, default-flow proof is HTTP/API tests (curl, PHPUnit, Vitest) plus a recorded hang — not a click-through.
- **PB-20260916-004** helpful=0 harmful=0 :: An automation browser stuck on the fleet empty state (select a host) on a host-only route is not proof the API failed. Cover AC with tests or curl; record the hang. Host-only routes belong in HOST_ONLY_PATHS so the host query is restored.
- **PB-20260916-003** helpful=0 harmful=0 :: Operator-authorized go (Inbox Approve, explicit operator dispatch) bypasses exploration or weekly synthesis caps. Those caps throttle autonomous work, not the request the operator just approved.
- **PB-20260916-002** helpful=0 harmful=0 :: Hub or invite previews are not done on a local blob URL. Resolve the cloud content URL the invitee will actually open, then call done.
- **PB-20260916-001** helpful=3 harmful=0 :: A hung loading surface is not browser proof of list chrome. Receipt Default flow must name what actually loaded; if the list never left loading, cover chrome AC with tests and record the hang — do not claim a click-through.
- **PB-20260915-002** helpful=0 harmful=0 :: Level 5 npm_audit remaining moderate on @vitest/mocker (or the same advisory class) is still a soft warning. MOVE_DONE when hard checks are green; do not open a follow-up ticket or hold the sprint for that advisory.
- **PB-20260915-001** helpful=0 harmful=0 :: Close the current ticket (receipt + gate 5 + MOVE_DONE) in the same session the work lands so inbox drain can feed the next sprint instead of stacking mid-loop notes. Do not leave a finished loop ticket open while starting a new slice.
- **PB-20260914-002** helpful=0 harmful=0 :: QA Prettier must ignore generated product session usage JSON; do not fail a ticket because the estimate ledger is unformatted.
