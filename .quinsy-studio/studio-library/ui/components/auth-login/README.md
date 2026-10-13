# AuthLoginForm

Sign-in, sign-up, and password reset for a Payload Users collection. The form posts to Payload’s REST auth on the same origin. It does not use a second auth client.

```tsx
import { AuthLoginForm } from '@ui/components/auth-login';

<AuthLoginForm homeHref="/" homeLabel="Back to app" />
```

| Action | Request |
|--------|---------|
| Sign in | `POST /api/users/login` |
| Sign up | `POST /api/users` |
| Already signed in | `GET /api/users/me` |
| Reset | `POST /api/users/forgot-password` |

The first admin user is created in `/admin`. Public registration works when the Users collection allows `create`. Access for every other collection is still named on that collection.
