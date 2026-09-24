# Conflict Matrix: External Skills vs. Anti-Slop Protocol

> This matrix checks every imported external skill source against the binding
> internal rules (`.quinsy-studio/knowledge-base/anti_ai_slop_protocol.md`,
> `zero-data-architecture`, `compliance_playbook`).
>
> **Principle:** Our own rules override external tendencies toward genericity.
> External skills are tools, NOT authority.

---

## 1. Overview of sources

| Source | Imported as | Domains | Conflict risk |
|--------|-------------|---------|---------------|
| `Nutlope/hallmark` | `external-skills/design` | anti-slop design | 🟢 Low |
| `bergside/awesome-design-skills` | `external-skills/design_awesome` | 67 design styles | 🟡 Medium |
| `seb1n/awesome-ai-agent-skills` | `external-skills/all_domains` | 103 domains | 🟡 Medium |
| `coreyhaines31/marketingskills` | `external-skills/marketing_aeo` | marketing, copy, SEO, AEO | 🟡 Medium |
| `gamedev-skills/awesome-gamedev-agent-skills` | `external-skills/gamedev` | game dev | 🟢 Low |
| `samir-abis/cookiecomply-skills` | `external-skills/compliance_cookies` | GDPR/cookies | 🟢 Low |
| `bloomprotocol/agent-visibility-skill` | `external-skills/geo_visibility` | GEO/AI visibility | 🟡 Medium |
| `obra/superpowers` | `external-skills/superpowers` | debug / review / writing | 🟡 Medium — **`executing-plans` blocked** |
| `anthropics/skills` | `external-skills/anthropic_docs` | pdf/pptx/xlsx/docx | 🟢 Low — artifacts, not product CSS |

**Blocked (do not subscribe):** `npx claude-code-templates` without a **named** skill path (aitmpl blob). Bright Data scrape MCP as a studio default. `executing-plans` / `finishing-a-development-branch` as the studio loop.

---

## 2. Conflict matrix (check → source → rating)

Legend: ✅ conformant · ⚠️ conflict potential · ❌ conflict (blocked)

### Anti-slop text clichés (T1–T10)

| Rule | hallmark | design_awesome | all_domains | marketing_aeo | gamedev | cookiecomply | geo_visibility |
|------|----------|----------------|-------------|---------------|---------|--------------|----------------|
| T1 "This function does X" | ✅ (rejects clichés) | ⚠️ (style guides can be generic) | ⚠️ | ⚠️ (copy skills use persuasion language) | ✅ | ✅ | ⚠️ |
| T2–T10 conversation clichés | ✅ | ✅ | ⚠️ (some scripts) | ⚠️ (marketing tone) | ✅ | ✅ | ✅ |

**Decision:** the internal `validate_anti_slop.py` checks apply to ALL generated
code — regardless of the external source. Text clichés are always rejected.

### Code patterns (C1–C10)

| Rule | hallmark | design_awesome | all_domains | marketing_aeo | gamedev | cookiecomply | geo_visibility |
|------|----------|----------------|-------------|---------------|---------|--------------|----------------|
| C1 swallowed errors | ✅ | ✅ | ✅ (script-based, conformant) | ✅ | ✅ | ✅ | ✅ |
| C6 god function | ✅ | ✅ | ✅ | ✅ | ⚠️ (game code can be monolithic) | ✅ | ✅ |
| C8 `any`/`unknown` | ✅ | ✅ | ✅ | ✅ | ⚠️ (GDScript/C# less strict) | ✅ | ✅ |

**Decision:** game dev (GDScript, C#, Lua) is subject to the internal typing obligation only
where the language supports it. Exceptions → ADR.

### UI patterns (U1–U10)

| Rule | hallmark | design_awesome | all_domains | marketing_aeo | gamedev | cookiecomply | geo_visibility |
|------|----------|----------------|-------------|---------------|---------|--------------|----------------|
| U1 inline styles | ✅ (token obligation) | ⚠️ (each style has its own rules) | ✅ | ✅ | ✅ | ✅ | ✅ |
| U2 hardcoded colors | ✅ | ⚠️ (styles define their own palettes) | ✅ | ✅ | ⚠️ (game art) | ✅ | ✅ |
| U6 semantic elements | ✅ | ⚠️ (web styles) | ✅ | ✅ | ✅ (no HTML) | ✅ | ✅ |
| U10 WCAG contrast | ✅ | ⚠️ (design styles can have low contrast) | ✅ | ✅ | ✅ | ✅ | ✅ |

**Decision:** design styles from `design_awesome` are used ONLY as a starting point.
Token hierarchy (`.quinsy-studio/studio-library/ui/tokens/`), WCAG-AA and the
anti-slop UI rules take precedence. Style-specific palettes are translated into tokens.

### Backend patterns (B1–B8)

| Rule | hallmark | design_awesome | all_domains | marketing_aeo | gamedev | cookiecomply | geo_visibility |
|------|----------|----------------|-------------|---------------|---------|--------------|----------------|
| B1 secrets in code | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ (SKILL.md contains API-key flows) |
| B2 SQL injection | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| B6 rate limiting | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ (recommends external API use) |

**Decision:** `geo_visibility` (Bloom) recommends MCP servers and API keys — that is
a **tooling reference**, not a code obligation. Keys belong in secret managers, never in code.

### Zero-data & GDPR

| Rule | hallmark | design_awesome | all_domains | marketing_aeo | gamedev | cookiecomply | geo_visibility |
|------|----------|----------------|-------------|---------------|---------|--------------|----------------|
| Zero-data pipelines | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ (sends URLs to the Bloom API) |
| GDPR conformant | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ (data to third parties) |

**Decision:** use Bloom (`geo_visibility`) ONLY as an **offline reference** for
llms.txt/JSON-LD patterns. The MCP server/API part is NOT integrated into projects
without an explicit GDPR approval (human-in-the-loop).

---

## 3. Priority order (in case of conflict)

```
1. internal anti_ai_slop_protocol.md        ← always wins
2. zero-data architecture / compliance_playbook
3. internal team skills (.quinsy-studio/teams/)
4. studio-library assets (checked, promoted)
5. external skills (only as tool/reference)
```

---

## 4. Concrete conflict examples

| Situation | External tendency | Internal rule | Solution |
|-----------|-------------------|---------------|----------|
| `design_awesome/glassmorphism` wants free colors | own palette | token obligation (U2) | translate style colors → design tokens |
| `marketing_aeo/copywriting` wants "revolutionize" | buzzwords | blacklist T1-T10 | have copy checked with `validate_anti_slop.py` |
| `all_domains` script wants `catch(e){}` | swallowed error | C1 | stub blocker: always handle errors |
| `geo_visibility` wants MCP + API key | external API | B1, zero-data | use only the markdown patterns, no API integration |
| `gamedev` GDScript without types | unchecked variables | C8 | typing where GDScript allows it, otherwise ADR |
| `cookiecomply` wants a third-party CMP | external banner service | zero-data | build own banner (studio library) |
| `superpowers/executing-plans` | batch then wait | `./studio execute` until HITL | **❌ do not import** — distill debugging/review only |
| aitmpl `npx claude-code-templates` whole tree | ~910 SKILL.md in context | cite → distill → CARD | **❌** named upstream repos only (`skill-dependencies.json`) |
| Bright Data `web-data/scrape` | vendor scrape MCP | secrets-as-names / zero-data | **❌** not a studio default |
| catalog `shadcn` as kit | shadcn/ui as source of truth | studio-library + Radix | **❌** not pullable as kit (LO-0334) |
| `theme-factory` Ocean Depths hex | paste pack into `app/` CSS | aesthetic presets + tokens | HITL pick → one preset / `project-brand-only` → tokens |

---

## 5. Maintenance

- Check the matrix after every `./studio update-skills` (add new sources).
- A new source WITHOUT a row in this matrix is NOT activated (SO-002 Process Guard).
- Conflicts are reported as learning items (`./studio learn ... --signal conflict`).
- After adding `superpowers` or `anthropic_docs`, re-run `./studio update-skills <name>` and confirm `external-skills/INDEX.md`.
