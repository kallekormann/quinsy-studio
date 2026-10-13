# Studio library packages

Generic pullable packages live here (`slug`, `rate-limit`, `write-side-revalidate`, …). Login for a new project is the Payload Users collection, not `packages/auth`.

**First-brand public chrome** (host magazine layout, legal footer, site nav labels, host-only types) stays in the **project**. After a sprint, record `./studio reuse --record <path> local`. Do not `library promote` those paths into this folder.

`billing` (Stripe and Lemon Squeezy) is pullable. `feature-gating` stays a stub until a working generic exists.
