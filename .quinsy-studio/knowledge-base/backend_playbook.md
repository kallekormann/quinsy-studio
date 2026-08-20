# Backend Playbook

> Domain-Driven Design (DDD), SOLID, JSONb EAV-Strukturen — die globalen Backend-Standards.

## Grundprinzip

```
Sicher. Skalierbar. Wartbar.
Jede Entscheidung wird dokumentiert.
```

---

## Architektur

### Domain-Driven Design (DDD)

```
┌─────────────────────────────────────────────────────────┐
│                    DDD-STRUKTUR                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────┐     ┌─────────────┐                   │
│  │   Domain    │────▶│ Application │                   │
│  │   Layer     │     │   Layer     │                   │
│  └─────────────┘     └──────┬──────┘                   │
│                             │                           │
│                      ┌──────▼──────┐                   │
│                      │ Interface   │                   │
│                      │   Layer     │                   │
│                      └──────┬──────┘                   │
│                             │                           │
│                      ┌──────▼──────┐                   │
│                      │Infrastructure│                   │
│                      │   Layer     │                   │
│                      └─────────────┘                   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Layer

| Layer | Verantwortlich | Enthält |
|-------|---------------|---------|
| **Domain** | Geschäftslogik | Entities, Value Objects, Aggregates, Domain Events |
| **Application** | Orchestrierung | Use Cases, DTOs, Application Services |
| **Interface** | Kommunikation | API Controllers, CLI, Message Handlers |
| **Infrastructure** | Technische Umsetzung | DB, External APIs, File System |

---

## SOLID Principles

| Prinzip | Beschreibung | Umsetzung |
|---------|-------------|-----------|
| **S**ingle Responsibility | Eine Klasse = eine Verantwortung | Kleine, fokussierte Klassen |
| **O**pen/Closed | Offen für Erweiterung, geschlossen für Modifikation | Interfaces, Strategy Pattern |
| **L**iskov Substitution | Untertypen sind ersetzbar | Saubere Vererbung |
| **I**nterface Segregation | Keine fetten Interfaces | Viele kleine Interfaces |
| **D**ependency Inversion | Abstraktionen statt Konkretheiten | Dependency Injection |

### Umsetzung

```typescript
// ✅ SOLID
interface UserRepository {
  findById(id: string): Promise<User | null>;
  save(user: User): Promise<void>;
}

class CreateUserUseCase {
  constructor(private userRepo: UserRepository) {}
  
  async execute(data: CreateUserDTO): Promise<User> {
    const user = User.create(data);
    await this.userRepo.save(user);
    return user;
  }
}

// ❌ NICHT SOLID
class UserService {
  async createUser(data: any) {
    const db = new Database(); // Dependency Inversion verletzt
    await db.query('INSERT INTO users...'); // SRP verletzt
  }
}
```

---

## PostgreSQL / Supabase

### Datenbank-Design

```sql
-- Enums (Type Safety)
CREATE TYPE user_role AS ENUM ('admin', 'user', 'viewer');
CREATE TYPE task_status AS ENUM ('open', 'in_progress', 'done');

-- Tabellen
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL,
  role user_role NOT NULL DEFAULT 'user',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexe
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
```

### JSONb EAV-Strukturen

```sql
-- Flexibles Attribut-System
CREATE TABLE product_attributes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  product_id UUID NOT NULL REFERENCES products(id),
  attribute_key TEXT NOT NULL,
  attribute_value JSONB NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- GIN-Index für JSONb
CREATE INDEX idx_product_attributes_value 
  ON product_attributes USING GIN(attribute_value);

-- Abfrage
SELECT * FROM product_attributes 
WHERE attribute_value @> '{"color": "red"}';
```

### Migrationen

```bash
# Neue Migration
supabase migration new add_users_table

# Migration ausführen
supabase db reset

# Migration anwenden
supabase db push
```

---

## API Design

### RESTful Ressourcen

```
GET    /api/v1/users          # Liste
GET    /api/v1/users/:id      # Detail
POST   /api/v1/users          # Erstellen
PATCH  /api/v1/users/:id      # Aktualisieren
DELETE /api/v1/users/:id      # Löschen
```

### Response-Format

```typescript
// Erfolg
{
  "data": { ... },
  "meta": { "page": 1, "total": 100 }
}

// Fehler
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Email ist ungültig",
    "details": { "email": "Muss eine gültige E-Mail-Adresse sein" }
  }
}
```

### Versionierung

```
/api/v1/...  # Hauptversion
/api/v2/...  # Breaking Changes
```

---

## Authentifizierung

### JWT + Refresh Token

```typescript
// Login
const accessToken = jwt.sign({ userId: user.id }, SECRET, { expiresIn: '15m' });
const refreshToken = jwt.sign({ userId: user.id }, REFRESH_SECRET, { expiresIn: '7d' });

// Refresh
app.post('/refresh', async (req, res) => {
  const { refreshToken } = req.body;
  const payload = jwt.verify(refreshToken, REFRESH_SECRET);
  const newAccessToken = jwt.sign({ userId: payload.userId }, SECRET, { expiresIn: '15m' });
  res.json({ accessToken: newAccessToken });
});
```

### RBAC

```typescript
type Role = 'admin' | 'user' | 'viewer';
type Permission = 'read' | 'write' | 'delete';

const rolePermissions: Record<Role, Permission[]> = {
  admin: ['read', 'write', 'delete'],
  user: ['read', 'write'],
  viewer: ['read'],
};

function hasPermission(role: Role, permission: Permission): boolean {
  return rolePermissions[role].includes(permission);
}
```

---

## Error Handling

```typescript
// Custom Error Classes
class AppError extends Error {
  constructor(
    public code: string,
    message: string,
    public statusCode: number = 500
  ) {
    super(message);
  }
}

class ValidationError extends AppError {
  constructor(message: string, public details: Record<string, string>) {
    super('VALIDATION_ERROR', message, 400);
  }
}

// Global Error Handler
app.use((err, req, res, next) => {
  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      error: { code: err.code, message: err.message, details: err.details }
    });
  }
  
  // Unbekannter Fehler
  console.error(err);
  res.status(500).json({
    error: { code: 'INTERNAL_ERROR', message: 'Ein interner Fehler ist aufgetreten' }
  });
});
```

---

## Testing

### Unit Tests

```typescript
describe('CreateUserUseCase', () => {
  it('should create a user', async () => {
    const repo = new InMemoryUserRepository();
    const useCase = new CreateUserUseCase(repo);
    
    const user = await useCase.execute({ email: 'test@example.com' });
    
    expect(user.email).toBe('test@example.com');
  });
});
```

### Integration Tests

```typescript
describe('POST /api/users', () => {
  it('should create a user', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ email: 'test@example.com' });
    
    expect(response.status).toBe(201);
    expect(response.body.data.email).toBe('test@example.com');
  });
});
```

---

## Referenzen

- `.quinsy-studio/knowledge-base/anti_ai_slop_protocol.md` — Backend-Slop-Regeln
- `.quinsy-studio/teams/02-backend-systems/` — Backend-Team
- `.quinsy-studio/teams/08-platform-enterprise-engineering/` — Infrastruktur-Team
