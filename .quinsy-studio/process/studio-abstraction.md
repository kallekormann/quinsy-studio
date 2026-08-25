# Studio abstraction — project-agnostic HQ

Quinsy Studio (`.quinsy-studio/`) is **permanent**. Client projects (`projects/<name>/`) are **temporary**. Studio docs, tools, templates, and examples must not encode a specific active project.

---

## Rules

| ✅ Allowed | ❌ Not allowed in studio HQ |
|-----------|----------------------------|
| Placeholders: `<project>`, `<p>`, `TICKET-0001`, `PROJ-0001` | Hard-coded active project names in process/docs/tools |
| `./studio learn --source <project>` in learning items | Project ticket IDs in templates and CLI help |
| `source_project` in `manifest.json` promotion metadata | Example commands that only work for one project name |
| Meta-retros naming which project a sprint came from | Amendment examples under a fixed project folder in studio templates |
| Generic fictional example: `acme-app`, `ACME-0042` | Project-specific scripts in `.quinsy-studio/tmp/` |

---

## Amendment intake

- **Template:** `.quinsy-studio/studio-templates/amendment_template.md`
- **Full example:** `.quinsy-studio/studio-templates/amendment_01.example.md`
- **Human drop zone:** `intake/amendments/<project>/amendment_NN.md` (gitignored, per project)
- Ticket materialization uses **project prefix** (`MOOD-`, `ACME-`, …) — defined in the **project** repo, not studio templates

Studio docs must say `./studio amend <project> …`, never assume a fixed project name in copy-paste blocks.

---

## Library manifest

`studio-library/manifest.json` may record `source_project` for **promotion provenance** (audit trail). That is metadata, not user-facing documentation.

---

## Verification

```bash
./studio verify-worlds          # two-worlds git separation
./studio verify-abstraction     # scan studio HQ for project-name leaks
```

See `studio_context.verify_studio_abstraction()`.

---

## Agent obligation

When editing `.quinsy-studio/`:

1. Use `<project>` in examples
2. Use `TICKET-0001` or `PROJ-0001` in templates
3. Do not add project-specific scripts under `.quinsy-studio/`
4. Learning from a project → `./studio learn` with `--source <project>` — fix studio generically

---

## Related

- [worlds.md](worlds.md)
- [agent-context.md](agent-context.md)
- [amendment-intake.md](amendment-intake.md)
