# Auth package

Do not pull this package for a new project.

Sign-in is the Payload Users collection in `apps/web`. The login form is `auth-login`. It posts to `/api/users/login`. Sessions are Payload’s cookie. Access control is the `access` rule on each collection.

This folder is the older Supabase module. It stays in the library so an existing product that already copied it can keep building. A new web project does not add it, and does not add Clerk or a second user table.

```bash
./studio library pull <project> auth-login
```
