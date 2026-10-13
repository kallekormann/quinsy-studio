# Payload playbook

Web products run on Payload. The blueprint line is `Payload: in` unless an ADR opts out. The app is `projects/<project>/apps/web`, written by `./studio execute` after gate 1 is signed. Do not scaffold it at `./studio init`.

## Surfaces

| Surface | How it uses Payload |
|---------|----------------------|
| Website | Next.js route group `(marketing)`. Public reads set `access.read` to allow anonymous visitors. Drafts and live preview stay on for marketing collections. Publishing revalidates the Next route. |
| Web app | Route group `(app)`. Server code uses the Local API. |
| Desktop, browser extension, mobile | REST or GraphQL clients of the same origin. They do not embed Payload. A second origin needs an ADR, and the blueprint names CORS. |
| Admin | `/admin` is `@payloadcms/ui`. Studio-library does not restyle it. |

## Rules

- Collections, fields, hooks, and access live in the Payload config. Every collection has an access rule. The receipt names it.
- Auth is the Users collection. Do not add Clerk, Supabase Auth, or a second user table.
- Do not add a second ORM (Prisma) or a second content-translation package (`next-intl`, `i18next`) for the same fields.
- One default locale unless `Locales:` lists more. Extra locales are Payload field localization with the named fallback. Chrome strings stay in Next.
- Plugins (Stripe, multi-tenant, SEO, import-export, MCP) are added only when the blueprint marks them `use`.
- Email is `@payloadcms/email-resend` when `RESEND_API_KEY` is set.
- Short work is a Payload job (a Postgres row). If more than one app replica runs, only one runs jobs, or a second container runs `payload jobs:run`.
- Long work (embeddings) is the Python worker on the `rag` profile. A Payload job only enqueues it. Do not run embeddings inside Next.
- Uploads: the scaffold registers `@payloadcms/storage-s3` and leaves it enabled, so migrations include its columns. Local files can use MinIO (`minio` profile). Production uses the same adapter against Cloudflare R2. Do not leave files on the container disk.
- Local development may push schema. Production sets `push: false`. `./studio env <project> migrate --approve` runs `payload migrate` in the app container. Coolify runs the same command before the new container serves traffic.
- Payments go through `studio-library/packages/billing` (Stripe and Lemon Squeezy). Pull it. Do not pull `feature-gating`. Skill BE-008.
- The database adapter is `postgresAdapter` (`@payloadcms/db-postgres`). Examples in the vendored skill (`teams/02-backend-systems/skills/payload/`) use `mongooseAdapter`; translate them. Do not edit the vendored files, because a refresh overwrites them.
- Authenticated or per-user pages are never cached (no ISR, no shared CDN cache). Only public reads are revalidated on publish.
- AI-written collection code is checked with AI-005: no `() => true` on update or delete, no `overrideAccess: true` on a path that takes user input, field-level access on role fields.

## Content engine collections (GM-003 / GM-001 / GM-002)

When the milestone plan carries the `content` (Content engine) or `seo` (SEO and AEO) coverage area, the web app gets these collections in the Payload config. They are the only content model; do not add a second CMS or a markdown folder beside them.

| Collection | Fields | Notes |
|------------|--------|-------|
| `posts` | title, slug, excerpt, body (richText), cover (upload), author (relationship users), categories (relationship), tags, publishedAt, status (draft/published), `seo` group (title, description, canonical, ogImage), `answer` group (question, shortAnswer ≤ 60 words, schemaType), `persona` (relationship personas or select), `source` (select: human, assisted, generated) | drafts + live preview on; public read for published only; publishing revalidates `/blog/[slug]`, the sitemap, and the RSS route |
| `categories` | name, slug, description, `seo` group | one page per category |
| `authors` or `users` extension | name, bio, avatar, links | E-E-A-T: every post names a real author |
| `redirects` (plugin) | from, to | slug changes never 404 |

Rules

- `@payloadcms/plugin-seo` fills `seo`; the answer block (GM-002) is a separate group so AEO text is not the meta description.
- Generated drafts (`source: generated`) stay in `draft` until a human or the content strategist flips `status`; the content engine template (`studio-templates/growth/content-engine-pack.md`) names the review step. Marketing law (UWG) applies to every published post.
- Sitemap, RSS, `robots.txt`, and JSON-LD (`Article`, `FAQPage` when `answer` is set) are generated routes that read these collections; they are part of the `seo` coverage area, not an afterthought.
- Persona pages (`studio-templates/growth/persona-page-set.md`) read `posts` by `persona` for their proof and article sections.

## Local and production

`./studio env <project> up --approve` starts Docker Desktop: Postgres, and the app container once `apps/web` exists. Optional profiles (`redis`, `pooler`, `minio`, `rag`) come from the blueprint `Profiles:` line or `--profile`.

The pooler is session mode. Local app traffic connects to Postgres directly.

Production is Coolify. Coolify installs the packages in `package.json`. It does not apt-install Payload. `PAYLOAD_SECRET` and `DATABASE_URL` are Coolify variables. Cookies are secure because Coolify is HTTPS.

Supabase is not the app database. The `rag` profile may store vectors in pgvector on the Compose Postgres. Production may point that worker at a hosted pgvector database. That database is not Payload's.

Payload does not provide product realtime. Live preview is the editor's draft preview. A product that needs live updates names that service at gate 1.

## Skill

Read `teams/02-backend-systems/skills/payload/SKILL.md` (BE-007) on architecture and implementation tickets when Payload is in.
