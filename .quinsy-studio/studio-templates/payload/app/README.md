# {{PROJECT}}

Payload Next.js app. Marketing routes live in `src/app/(marketing)`. The signed-in product lives in `src/app/(app)`. Admin and the REST API live in `src/app/(payload)`.

Local: `./studio env {{PROJECT}} up --approve` from the studio root. That starts Docker Desktop. The first admin user is created in `/admin` on first boot.

Production: Coolify builds this Dockerfile. The image runs `payload migrate`, then `node server.js`. Set `PAYLOAD_SECRET`, `DATABASE_URL`, and `RESEND_API_KEY` in Coolify. Uploads use `@payloadcms/storage-s3` (MinIO locally, Cloudflare R2 in production). Leave that plugin enabled when you create migrations. Do not leave files on the container disk.

Add a locale in `src/payload.config.ts` only after the blueprint `Locales:` line lists it. Mark a field `localized: true` only when that text changes per language.
