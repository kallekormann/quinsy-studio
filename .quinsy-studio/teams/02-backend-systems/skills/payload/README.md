# Payload Skill for AI Coding Agents

Agent skill providing comprehensive guidance for Payload development with TypeScript patterns, field configurations, hooks, access control, and API examples.

## Studio notes (read first)

`SKILL.md` and `reference/` are vendored from upstream and get overwritten on refresh. Studio rules live here and in `knowledge-base/payload-playbook.md`. Where they differ, the studio rule wins.

### Postgres, not MongoDB

The vendored examples use `mongooseAdapter` from `@payloadcms/db-mongodb`. Studio projects use `postgresAdapter` from `@payloadcms/db-postgres`, as in `studio-templates/payload/app/src/payload.config.ts`:

```ts
db: postgresAdapter({
  pool: { connectionString: process.env.DATABASE_URL },
  push: process.env.NODE_ENV !== 'production',
}),
```

Read every Mongo example with Postgres in mind:

- Schema changes need a migration: `payload migrate:create <name>`, then `./studio env <p> migrate --approve`. Production runs with `push: false`.
- IDs are serial integers unless gate 1 set `idType: 'uuid'`. Do not mix (BE-002).
- Mongo-only query features and raw `mongoose` calls do not apply. Raw SQL goes through `payload.db.drizzle`, sparingly.
- Transactions work on Postgres; pass `req` to nested Local API calls so they share it.

### Admin form layout

Editors use `/admin` every day. Structure the form before polishing labels.

- **More than about eight fields in one flat list:** split them. Use `tabs` for distinct groups (Content / SEO / Settings) and `row` to put short related fields side by side (first and last name, start and end date).
- **Sidebar:** `admin: { position: 'sidebar' }` for metadata the editor scans but rarely edits: status, slug, publish date, author, relationships to taxonomies.
- **Collapse the rare:** `collapsible` fields, or `admin.initCollapsed: true` on arrays and blocks, for sections that are empty on most documents (notes, overrides).
- **Name array rows:** give arrays a `RowLabel` component so rows read "14:00 — Lunch", not "Item 01".
- **Descriptions only where needed:** `admin.description` when a field's intent is not obvious (format, where it shows, character limit). Not on title, date or email. One guidance layer per field: label plus description, not also a placeholder repeating them.
- **List view:** set `admin.useAsTitle` and `admin.defaultColumns` on every collection; group collections with `admin.group`.
- **Conditional fields:** `admin.condition` hides fields that do not apply, and the field's `validate` must not require a hidden field.
- **Check:** every original field is still present after a layout change; walk both "create" and "edit".

### Caching of private pages

Pages that depend on the logged-in user are never cached:

- Routes in `(app)`, account, checkout, cart and any route that reads `payload.auth()` or cookies render dynamically (`export const dynamic = 'force-dynamic'`, or `cache: 'no-store'` on fetches).
- Do not use `unstable_cache` or `'use cache'` around data that is filtered by `req.user`.
- The CDN or proxy (Coolify, Cloudflare) must not cache HTML for these routes; send `Cache-Control: private, no-store`.
- Public `(marketing)` pages may be static or ISR and revalidate from an `afterChange` hook. Draft and live-preview requests are never cached.

## What's Included

The `payload` skill provides expert guidance on:

- **Collections**: Auth, uploads, drafts, live preview configurations
- **Fields**: All field types including relationships, arrays, blocks, joins, virtual fields
- **Hooks**: beforeChange, afterChange, beforeValidate, field hooks
- **Access Control**: Collection, field, and global access patterns including RBAC and multi-tenant
- **Queries**: Local API, REST, and GraphQL with complex operators
- **Database Adapters**: MongoDB, Postgres, SQLite configurations and transactions
- **Advanced Features**: Jobs queue, custom endpoints, localization, plugins

## Usage

Once installed, the Agent will automatically invoke the skill when you're working on Payload projects. The skill activates when you:

- Edit `payload.config.ts` files
- Work with collection or global configurations
- Ask about Payload-specific patterns
- Need guidance on fields, hooks, or access control

You can also explicitly invoke it:

```
@payload how do I implement row-level access control?
```

## Documentation Structure

```
skills/payload/
├── SKILL.md                              # Main skill file with quick reference
└── reference/
    ├── FIELDS.md                         # All field types and configurations
    ├── FIELD-TYPE-GUARDS.md              # Type guards for field discrimination
    ├── COLLECTIONS.md                    # Collection patterns
    ├── HOOKS.md                          # Hook patterns and examples
    ├── ACCESS-CONTROL.md                 # Basic access control
    ├── ACCESS-CONTROL-ADVANCED.md        # Advanced access patterns
    ├── QUERIES.md                        # Query patterns and APIs
    ├── ENDPOINTS.md                      # Custom endpoints
    ├── ADAPTERS.md                       # Database and storage adapters
    ├── PLUGIN-DEVELOPMENT.md             # Plugin development patterns
    └── ADVANCED.md                       # Jobs, endpoints, localization
```

## Resources

- [Payload Documentation](https://payloadcms.com/docs)
- [GitHub Repository](https://github.com/payloadcms/payload)
- [Examples](https://github.com/payloadcms/payload/tree/main/examples)
- [Templates](https://github.com/payloadcms/payload/tree/main/templates)

## License

MIT
