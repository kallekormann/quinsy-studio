# Skill: Studio Tooling Maintenance

> Maintenance, refactoring and improvement of the Python tools in the Studio HQ

## Metadata

```
skill_id: SO-001
name: Studio Tooling Maintenance
team: 09-studio-operations-evolution
lead_role: Studio Automation Engineer
support_roles: [Platform Architect]
phases: [6, 7]
activation_triggers:
  - Ticket contains "Studio Tools", "Python", "Tooling", "Maintenance"
  - /studio-evolution command
  - Phase 6: Learning Loop identifies tooling improvements
  - Performance problems with studio tools
```

---

## Behavioral Rules

### 1. Maintain Python Tools

```markdown
Files in .quinsy-studio/studio-tools/:
  - validate_anti_slop.py    → Anti-slop detection
  - run_qa_gate.py           → QA gate orchestration
  - generate_ticket_manifest.py → Ticket generation
  - sync_global_assets.py    → Asset promotion
  - init_project_env.py      → Project initialization
  - requirements.txt         → Dependencies

Regular maintenance:
  - Update dependencies (weekly)
  - Security scans
  - Performance benchmarks
  - Write/update unit tests
```

### 2. Refactoring Rules

```markdown
When refactoring:
  - Keep API backward-compatible
  - Update CHANGELOG.md
  - Update README.md
  - Update tests
  - No breaking changes without version bump
```

### 3. Monitoring

```markdown
What to track:
  - Execution time per tool
  - Success rate
  - Usage frequency
  - Error logs
```

### 4. Rules for the `./studio` CLI

Agents call `./studio` dozens of times a session and parse what it prints. Every command follows these rules.

- **Help in both blocks.** A new command gets a line in the module docstring and in the printed help of `studio.py`, same wording. `test_cli_help.py` fails otherwise.
- **Exit codes.** `0` when the command did what it says, `1` when it refused or failed. A refusal never exits `0`.
- **A refusal says why and what to run next.** Print the reason, then the exact next command (`./studio qa <p> <T> --finish`). Never a bare "error".
- **No prompts.** Commands never wait for input. Human approval is a flag (`--approve`, `--verdict`, `--finish`) that the human's message authorises; without it the command prints what it would do and exits.
- **Execute output is a contract.** `ACTION`, `NEXT`, `READ` and `CARD` lines from `./studio execute` are parsed by agents. Change their shape only with a CHANGELOG entry and updated tests.
- **Idempotent writes.** Running a command twice leaves the same files. Templates are written only when missing; a filled file is never overwritten.
- **Secrets are names only.** No command opens `.env`, `.env.local` or `*.pem`, and none prints a secret value. Values reach containers only through `./studio env … --approve`.
- **Two worlds.** Product commands write under `projects/<p>/` and commit with `git -C projects/<p>`. HQ commands write under `.quinsy-studio/`. No command writes to a sibling project.
- **Every new check has a pass and a fail fixture** in a `test_*.py` next to the tool, and NOT TESTED is a separate state from PASS.

---

## Toolbox (trained — TR-0001–TR-0007, TR-0011, TR-0077)

Distilled principles from parallel train jobs (Openverse imagery sprint). Full detail in linked playbooks — no client product names.

### Provider licence adapters

- Stock APIs return **short slugs** (`by`, `by-sa`, …) — not `cc-by` display forms. Allowlists and normalizers must accept provider-native codes at the adapter boundary ([backend_playbook.md](../../../knowledge-base/backend_playbook.md)).
- One map: `provider_slug → canonical enum → display label`. Never match allowlists on human-readable strings.
- Unit-test fixtures from the provider OpenAPI examples, not invented `cc-*` strings.

### Imagery presentation / bento mosaics

- Compute **per-cell pixel budget** before calling layout done; assign highest-resolution sources to largest cells ([design_playbook.md](../../../knowledge-base/design_playbook.md)).
- Selection order is curation order, **not** placement order ([contextual-ia-playbook.md](../../../knowledge-base/contextual-ia-playbook.md)).
- Low-res thumbs must not occupy lead cells — demote to small tiles or solid-fill fallbacks.

### Suggested / degraded imagery UX

- Distinguish **provider outage** (5xx) from **filter-empty** (mapper rejects valid slugs) in copy and logs ([human-in-the-loop.md](../../../process/human-in-the-loop.md) LO-0069 / LO-0074).
- Smoke signed-in Suggested path + forced error path before review — optimistic “Looking up…” with zero results is not shipped.
- Keep **Openverse (or primary aggregator) first**; add Unsplash/Pexels only after mapper fix + healthy primary API still yields empty Suggested ([backend_playbook.md](../../../knowledge-base/backend_playbook.md) LO-0075).

### Gate smoke in agent sandboxes (LO-0071)

- Chromium may SIGSEGV in Cursor/CI sandboxes — `QUINSY_SKIP_SMOKE=1` is an **explicit agent opt-out** for `./studio gate --level 5` only; gate output must say skipped.
- Human machines and sprint review: leave unset; document skip in the ticket receipt when agents cannot run smoke.

### Anti-slop ignore list (LO-0082)

- Treat published third-party admin panel assets (`public/js|css|fonts/<panel>/`) and Composer `vendor/` like `node_modules`: do not scan minified vendor JS for magic numbers or type assertions.
- `validate_anti_slop.py` `IGNORE_PATTERNS` is the allowlist of generated trees; extend it when a PHP/JS admin kit publishes into `public/`, not by rewriting vendor files.

### Generated session usage vs Prettier (LO-0254)

- Product `.studio-session-usage.json` is a studio-written estimate ledger, not source. QA Prettier must not fail tickets on it.
- `ensure_prettierignore_cost_lines` (and `.gitignore`) keep the file out of `--check .`. Do not format it as a ticket fix.

### Reuse harvest (LO-0100)

- Auto-open an LO only for **registry generic packages** (`packages/auth`, billing, …). First-brand token kits and project `ui/` stay local (`./studio reuse --record <path> local`).
- Do not copy client `theme-tokens` / `design-tokens` / `kit-*` into `studio-library/`.

### Laravel serve in Compose (LO-0101)

- `php artisan serve` strips Compose env from the PHP child unless `--no-reload`. CLI artisan can look healthy while HTTP 500s. Pass `--no-reload` or use `php -S`.

### Operator go vs exploration caps (LO-0286, TR-0083)

- An operator Approve / explicit dispatch is a go. Weekly or exploration budget caps throttle **autonomous** jobs, not the request the operator just authorized ([gates.md](../../../process/gates.md), [backend_playbook.md](../../../knowledge-base/backend_playbook.md)).
- Do not pause an operator-authorized synthesis because the unattended weekly cap is already reached. Re-check caps on the next autonomous call.

### Receipt honesty when live UI hangs (LO-0276, LO-0291, TR-0077)

- A hung loading surface is not browser proof of list chrome. Receipt Default flow must name what actually loaded; if the list never left loading, cover chrome AC with HTTP/API tests (curl, PHPUnit, Vitest) and record the hang ([qa-gate-playbook.md](../../../knowledge-base/qa-gate-playbook.md), [gates.md](../../../process/gates.md)).
- Host-scoped operator chrome that never leaves the loading state is the same class: do not treat a spinner as click-through (LO-0276, LO-0291).
- Host-only operator pages that still show the fleet empty state (select a host) in an automation tab are the same class: cite API or tests, record the hang, put the route in HOST_ONLY_PATHS. Do not treat a spinner screenshot as operator click-through.

### Upgrade soft-path DoD (LO-0142 / LO-0143, TR-0011)

- Soft-path to Settings/Account is **not** done when only the URL changes. Before `move … done`, assert free-tier: plan label + Upgrade CTA visible, **or** upgrade dialog auto-opens (`?upgrade=1`).
- Pattern: [upgrade-soft-path.md](../../../studio-library/ui/docs/patterns/upgrade-soft-path.md). Gate rule: [gates.md](../../../process/gates.md) LO-0143.

---

## Anti-Patterns

### ❌ Prohibited

```markdown
- Breaking changes without versioning
  - No tests for changed tools
  - Not updating dependencies
  - Debug code in production
```

### ✅ Instead

```markdown
- Semantic versioning
  - Tests before every deploy
  - Regular dependency updates
  - Clean production code
```

---

## References

- `.quinsy-studio/studio-tools/` — Python automation
- `.quinsy-studio/process/learning-loop.md` — Learning Loop
