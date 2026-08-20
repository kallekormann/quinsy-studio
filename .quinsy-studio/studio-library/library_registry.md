# Studio Library Registry

> Canonical paths, kinds, and promotion rules for reusable UI + code artifacts.
> Machine-readable copy: `library_registry.json` (same folder).

## Philosophy: library-first

1. **Before writing new code** → `./studio library list` / `./studio library suggest <project> <topic>`
2. **Pull boilerplate** → `./studio library pull <project> auth billing button`
3. **Adapt in project** — project tokens, provider keys, business rules stay local
4. **After ticket done** → review: generic enough? → `./studio library promote <project> <path>`

---

## Kinds

| Kind | Project path | Library path | Pull alias |
|------|--------------|--------------|------------|
| `ui-atom` | `ui/components/atoms/<Name>.tsx` | `ui/components/<slug>/` | component name |
| `ui-molecule` | `ui/components/molecules/<Name>.tsx` | `ui/components/<slug>/` | component name |
| `ui-organism` | `ui/components/organisms/<Name>.tsx` | `ui/components/<slug>/` | component name |
| `ui-page-type` | `ui/page-types/<name>/` | `ui/page-types/<name>/` | page-type name |
| `ui-token` | `ui/tokens/design-tokens.json` | `ui/tokens/design-tokens.json` | `tokens` |
| `ui-hook` | `hooks/<name>.ts` | `ui/hooks/<name>.ts` | hook name |
| `package-auth` | `packages/auth/` | `packages/auth/` | `auth` |
| `package-billing` | `packages/billing/` | `packages/billing/` | `billing` |
| `package-feature-gating` | `packages/feature-gating/` | `packages/feature-gating/` | `feature-gating`, `gating` |
| `sticker-sheet` | `design/prototype/app/sticker-sheet/` | `ui/sticker-sheet/` | (gate 2 only) |

---

## Auto-promotion (gate 2)

On `./studio approve <project> --gate 2`:

- `ui-token`, `ui-atom`, `ui-molecule`, `ui-organism`, `ui-page-type`, `sticker-sheet`
- Command: `./studio promote-library <project>` or `./studio library promote-design <project>`

## Manual promotion (code + overrides)

```bash
./studio library promote nudge packages/billing
./studio library promote nudge packages/billing --force   # bump version, overwrite
./studio library promote nudge ui/components/atoms/Badge.tsx
```

Requires ticket reuse review (see `./studio move … done` warnings).

---

## Pull into project

```bash
./studio library pull nudge auth billing tokens button
```

- Copies **library → project** (never overwrites without `--force`)
- Logs to `projects/<p>/docs/library-usage.json`
- Agent rule: **search library before implementing**

---

## Versioning

Each asset in `manifest.json` has:

```json
{
  "name": "billing",
  "kind": "package-billing",
  "version": "1.0.0",
  "path": "packages/billing",
  "source_project": "nudge",
  "promoted": "2026-08-20"
}
```

- New promotion: `1.0.0`
- `--force` on existing: patch bump (`1.0.0` → `1.0.1`)

---

## Reuse enforcement

When moving a ticket to `done`, studio compares files under registry paths to snapshot at `implement`:

- If changed and not logged in `docs/library-promotions.json` → **warning**
- Agent must run `./studio library promote` or document why it stays project-local

---

## Provider layout (billing)

```
packages/billing/
  index.ts                 # BillingProvider interface
  types.ts
  providers/
    stripe.ts              # Stripe adapter stub
    lemon-squeezy.ts       # Lemon Squeezy adapter stub
```

Projects implement provider config; library stays provider-agnostic.
