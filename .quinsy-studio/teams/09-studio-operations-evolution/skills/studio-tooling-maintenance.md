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

---

## Toolbox (trained — TR-0001–TR-0007)

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

### Reuse harvest (LO-0100)

- Auto-open an LO only for **registry generic packages** (`packages/auth`, billing, …). First-brand token kits and project `ui/` stay local (`./studio reuse --record <path> local`).
- Do not copy client `theme-tokens` / `design-tokens` / `kit-*` into `studio-library/`.

### Laravel serve in Compose (LO-0101)

- `php artisan serve` strips Compose env from the PHP child unless `--no-reload`. CLI artisan can look healthy while HTTP 500s. Pass `--no-reload` or use `php -S`.

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
