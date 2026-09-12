# Studio Library Registry

> Canonical paths, kinds, and promotion rules for reusable UI + code artifacts.
> Machine-readable copy: `library_registry.json` (same folder).

## Philosophy: library-first, studio-owned generics

| Layer | Owner | Location |
|-------|--------|----------|
| **Studio library** | Quinsy Studio | `.quinsy-studio/studio-library/` — Tailwind-default tokens, generic UI, package stubs |
| **Project design** | Each project | `projects/<name>/ui/tokens/`, `ui/components/` — brand + domain |

**Rule:** Gate 2 and `./studio library promote` **never merge project tokens or UI into studio-library.**

**Stubs** (`billing`, `feature-gating`) are marked `stub: true` in `manifest.json`. `./studio library pull` **refuses** them. Build the working asset in the project, then promote if it is generic.

**Product-local packages (LO-0162 / LO-0164):** companion surfaces such as `packages/figma-plugin/`, `packages/extension/` (and build junk like `.DS_Store`, `dist/`) are **project-owned**. Reuse review must not propose them for studio-library promote. See `studio-tools/sprint_reuse_review.py` (`PRODUCT_LOCAL_PACKAGE_NAMES` / `is_reuse_noise_path`).

**Brand / domain UI (LO-0171):** magazine chrome, kit-specific atoms, and other non-generic `packages/ui` or `ui/` files should get `./studio reuse <p> --record <path> local` **when the ticket ships**, not as a pile at retro. Reuse then auto-completes (LO-0169) instead of demanding a human `--approve`.

1. **Before writing new code** → `./studio library list` / `./studio library suggest <project> <topic>`
2. **Pull boilerplate** → `./studio library pull <project> tokens button input`
3. **Adapt in project** — map `--color-primary-*` to brand; keep domain components local
4. **Improve generics** → edit `.quinsy-studio/studio-library/` via **LO-* studio ticket** (not project promotion)

---

## Kinds

| Kind | Project path | Library path | Pull alias |
|------|--------------|--------------|------------|
| `ui-primitive` | `ui/primitives/headless/<slug>/` | `ui/primitives/headless/<slug>/` | primitive name (`dialog`, `menu`, …) |
| `ui-atom` | `ui/components/atoms/<Name>.tsx` | `ui/components/<slug>/` | component name |
| `ui-molecule` | `ui/components/molecules/<Name>.tsx` | `ui/components/<slug>/` | component name |
| `ui-organism` | `ui/components/organisms/<Name>.tsx` | `ui/components/<slug>/` | component name |
| `ui-page-type` | `ui/page-types/<name>/` | `ui/page-types/<name>/` | page-type name |
| `ui-token` | `ui/tokens/design-tokens.json` + `.css` | `ui/tokens/` | `tokens` |
| `ui-hook` | `hooks/<name>.ts` | `ui/hooks/<name>.ts` | hook name |
| `package-auth` | `packages/auth/` | `packages/auth/` | `auth`, `supabase-auth`, `supabase` |
| `package-billing` | `packages/billing/` | `packages/billing/` | `billing` |
| `package-feature-gating` | `packages/feature-gating/` | `packages/feature-gating/` | `feature-gating`, `gating` |
| `package-color-extraction` | `packages/color-extraction/` | `packages/color-extraction/` | `color-extraction`, `palette`, `extract-palette` |
| `package-qa-smoke` | `scripts/qa/` | `packages/qa-smoke/` | `qa-smoke`, `smoke-routes`, `smoke` |
| `package-item-tags` | `packages/item-tags/` | `packages/item-tags/` | `item-tags`, `tags` |
| `package-item-search` | `packages/item-search/` | `packages/item-search/` | `item-search`, `search`, `discover` |
| `package-canvas-export` | `packages/canvas-export/` | `packages/canvas-export/` | `canvas-export`, `board-export`, `export` |
| `package-rate-limit` | `packages/rate-limit/` | `packages/rate-limit/` | `rate-limit`, `ratelimit` |
| `package-slug` | `packages/slug/` | `packages/slug/` | `slug`, `slugify` |
| `package-password-gate` | `packages/password-gate/` | `packages/password-gate/` | `password-gate`, `password`, `bcrypt-gate` |
| `package-rect-selection` | `packages/rect-selection/` | `packages/rect-selection/` | `rect-selection`, `marquee-selection`, `marquee` |
| `package-viewport-fit` | `packages/viewport-fit/` | `packages/viewport-fit/` | `viewport-fit`, `zoom-to-fit`, `fit-viewport` |
| `sticker-sheet` | `design/prototype/app/sticker-sheet/` | `ui/sticker-sheet/` | (reference only) |

---

## Gate 2 (design approval)

On `./studio approve <project> --gate 2`:

- **Validates** project has `ui/tokens/design-tokens.json` + prototype sticker sheet
- **Refreshes** studio-library sticker catalog (lists studio-owned components)
- **Does not copy** project tokens, CSS, or components into studio-library

Command: `./studio promote-library <project>` — same validate-only behavior

---

## Manual promotion (packages only)

```bash
./studio library promote nudge packages/billing   # OK — generic package stub
./studio library promote nudge ui/tokens/...      # BLOCKED — studio-owned
./studio library promote nudge ui/components/...  # BLOCKED — adapt via pull, not promote
```

Generic library UI/tokens are edited in `.quinsy-studio/studio-library/` directly.

---

## Pull into project

```bash
./studio library pull nudge tokens button input dialog menu pageshell
```

**Peer dependency:** Headless UI primitives require `@headlessui/react` in the project.

- Copies **library → project** (never overwrites without `--force`)
- Logs to `projects/<p>/docs/library-usage.json`
- Project then **extends** local `ui/tokens/design-tokens.json` / `.css` for brand (e.g. Nudge soft SaaS)

---

## Token stack (Tailwind standard)

| File | Role |
|------|------|
| `design-tokens.json` | Schema: primary/neutral/semantic scales |
| `design-tokens.css` | `--color-primary-*`, `--color-surface`, dark mode |
| `tailwind.preset.ts` | `theme.extend` → CSS variables |

Components use **semantic Tailwind classes** (`primary-600`, `surface`, `neutral-*`) so projects remap tokens without changing component code.

---

## Versioning

Each asset in `manifest.json` has `source_project: "studio"` for generics. Project-specific design is not versioned in the library manifest.

---

## Reuse enforcement

When moving a ticket to `done`, studio compares files under registry watch paths to snapshot at `implement`:

- Changes under `projects/<name>/ui/` are **project-local** — no library promotion required
- Warnings apply only if you changed `packages/` without logging promotion
- **Reuse harvest** auto-opens an LO only for **registry generic packages** (`packages/auth`, billing, …). First-brand token kits (`theme-tokens`, `design-tokens`, `kit-*`), project `ui/`, and first-brand public chrome (`packages/ui`, magazine nav/legal layout, site types used only by that host) stay local — record `./studio reuse --record <path> local`. Do not `library promote` those paths. Do not copy client kits into `studio-library/`.
- **LO-0150 / LO-0206:** Host masthead, site nav, page renderers, and the project `packages/ui` (or scoped `@*/ui`) package are the product face. Reuse records them `local`. The reuse scanner must not demand a promote. Promoting them copies a host into HQ.
