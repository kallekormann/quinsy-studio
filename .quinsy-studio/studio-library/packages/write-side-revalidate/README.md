# Write-side revalidate

Cache-bust a public delivery host **after a write**, from the plane that already holds the secret.

Do **not** import this from a `"use client"` module. Browser bundles cannot see admin-only env: the UI can report Saved while the public host stays stale.

## Pull

```bash
./studio library pull <project> write-side-revalidate
```

## Usage

Call from a server action, route handler, or admin worker — never from client state.

```typescript
import { pickServerOnlySecret, revalidateAfterWrite } from '@/packages/write-side-revalidate';

const secret = pickServerOnlySecret(process.env, ['REVALIDATE_SECRET']);
await revalidateAfterWrite({
  origin: process.env.INTERNAL_DELIVERY_URL ?? '',
  secret,
  payload: { host },
});
```

`pickServerOnlySecret` ignores `NEXT_PUBLIC_*` keys even when they are set.
