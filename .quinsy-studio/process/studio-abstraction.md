# Studio abstraction — project-agnostic HQ

Quinsy Studio (`.quinsy-studio/`) is **permanent**. Client projects (`projects/<name>/`) are **temporary**. Nothing studio git commits may name a product or carry product logic. That covers the process, skills, playbooks, learnings catalog, library, templates, tools, tests, both READMEs, AGENTS.md, CLAUDE.md, GEMINI.md, and both CHANGELOGs. A product reference in any of them is a bug.

---

## Rules

| ✅ Allowed | ❌ Not allowed anywhere studio git commits |
|-----------|----------------------------|
| Placeholders: `<project>`, `<p>`, `<ticket>`, `TICKET-0001`, `PROJ-0001` | A product folder name, in any line, including "Source:" and "provenance" lines |
| Reserved example project: `demo` (`DEMO-0001`); fictional `acme-app`, `ACME-0042` | A product's ticket IDs (`<first four letters>-NNNN`), in comments, tests, examples, or CHANGELOG |
| `./studio learn --source <project>`: the name lands in the local LO and the project's own log | A product's brand, screen, host, or design-system name (its look stays in its repo) |
| Generic library assets, with brand values passed in as parameters | Library code with a product's protocol, brand defaults, or hard-coded paths |
| Vendor names used as examples (Stripe, Openverse) | Project-specific scripts anywhere under `.quinsy-studio/` |

---

## Where provenance lives

The name of the product a lesson or asset came from stays out of studio git:

- **Learnings:** the LO in `backlog/` (gitignored) keeps `source:`. `inbox.md` and the catalog do not.
- **Library promotions:** `projects/<p>/docs/library-promotions.json` in the product repo. `studio-library/manifest.json` records the asset, version, and ticket-free reason only.
- **Product surface names:** a product lists its own screens, brands, and hosts in `projects/<p>/docs/portability-nouns.txt` (one per line). Harvest and infusion refuse them; HQ never lists them.
- **Vendored folders** that a product wants the anti-slop gate to skip go in `projects/<p>/docs/anti-slop-ignore.txt`.

---

## Amendment intake

- **Template:** `.quinsy-studio/studio-templates/amendment_template.md`
- **Full example:** `.quinsy-studio/studio-templates/amendment_01.example.md`
- **Human drop zone:** `intake/amendments/<project>/amendment_NN.md` (gitignored, per project)
- Ticket materialization uses the **project prefix** (`ACME-`, …), derived in the project, not written in studio templates

Studio docs say `./studio amend <project> …`, never a fixed project name in copy-paste blocks.

---

## Verification

```bash
./studio verify-worlds          # two-worlds git separation
./studio verify-abstraction     # every file studio git would commit, every product name and ticket prefix
```

`verify-abstraction` reads the file list from `git ls-files` (tracked plus untracked-not-ignored, outside `projects/`, `intake/`, `ideation/`), so a new folder or file type cannot slip past. Names come from the real `projects/*` folders; ticket prefixes are their first four letters. `demo`, `example`, `sample` are never products. See `studio_context.verify_studio_abstraction()`.

---

## Agent obligation

When editing anything studio git commits:

1. Use `<project>` or `demo` in examples, `<ticket>` or `DEMO-0001` for tickets
2. Do not cite a product ticket as the reason for a line of code; state the constraint
3. Do not add project-specific scripts under `.quinsy-studio/`
4. Learning from a project → `./studio learn` with `--source <project>` — fix studio generically
5. Run `./studio verify-abstraction` before a studio commit

---

## Related

- [worlds.md](worlds.md)
- [agent-context.md](agent-context.md)
- [amendment-intake.md](amendment-intake.md)
