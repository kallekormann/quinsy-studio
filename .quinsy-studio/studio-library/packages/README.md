# Studio library packages

Generic pullable packages live here (`auth`, `slug`, `rate-limit`, `write-side-revalidate`, …).

**First-brand public chrome** (host magazine layout, legal footer, site nav labels, host-only types) stays in the **project**. After a sprint, record `./studio reuse --record <path> local`. Do not `library promote` those paths into this folder.

Stubs (`billing`, `feature-gating`) are not pullable until a working generic exists.
