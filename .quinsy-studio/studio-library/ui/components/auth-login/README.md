# AuthLoginForm

Generic sign-in / sign-up / magic-link form. Wire with `@packages/auth/next/client` helpers.

```tsx
import { AuthLoginForm } from '@ui/components/auth-login';
import { createBrowserSupabaseClient, isSupabaseConfigured } from '@packages/auth/next/client';

<AuthLoginForm
  createClient={createBrowserSupabaseClient}
  isConfigured={isSupabaseConfigured}
  homeHref="/"
  homeLabel="Back to app"
/>
```
