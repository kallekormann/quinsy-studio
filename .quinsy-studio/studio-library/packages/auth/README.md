# Auth Package

> Authentifizierung und Autorisierung für SaaS-Anwendungen.

## Features

- JWT-basierte Authentifizierung
- Refresh-Token-Rotation
- RBAC (Role-Based Access Control)
- OAuth-Integration (Google, GitHub)
- Session-Management
- Rate-Limiting für Login

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    AUTH FLOW                             │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. Login Request                                       │
│     └─▶ Validate Credentials                           │
│     └─▶ Generate JWT (short-lived)                     │
│     └─▶ Generate Refresh Token                         │
│                                                         │
│  2. API Request                                         │
│     └─▶ Validate JWT                                   │
│     └─▶ Check Permissions (RBAC)                       │
│     └─▶ Process Request                                │
│                                                         │
│  3. Token Refresh                                       │
│     └─▶ Validate Refresh Token                         │
│     └─▶ Rotate Refresh Token                           │
│     └─▶ Issue new JWT                                  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Configuration

```typescript
// auth.config.ts
export const authConfig = {
  jwt: {
    secret: process.env.JWT_SECRET,
    expiresIn: '15m',
  },
  refresh: {
    expiresIn: '7d',
    rotation: true,
  },
  rbac: {
    roles: ['admin', 'user', 'viewer'],
    permissions: {
      admin: ['*'],
      user: ['read', 'write'],
      viewer: ['read'],
    },
  },
};
```

## Usage

```typescript
import { authenticate, authorize, rbac } from '@studio/auth';

// Middleware
app.use(authenticate);

// Route Protection
app.get('/admin', authorize('admin'), adminHandler);

// RBAC Check
if (rbac.hasPermission(user, 'write')) {
  // Allow
}
```

## Security

- Secrets nie im Code
- JWT mit kurzer Ablaufzeit
- Refresh-Token-Rotation
- Rate-Limiting für Login
- CSRF-Schutz
