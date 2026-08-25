# Backend Playbook

> Domain-driven design (DDD), SOLID, JSONb EAV structures — the global backend standards.

## Core principle

```
Secure. Scalable. Maintainable.
Every decision is documented.
```

---

## Architecture

### Domain-driven design (DDD)

```
┌─────────────────────────────────────────────────────────┐
│                    DDD STRUCTURE                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────┐     ┌─────────────┐                   │
│  │   Domain    │────▶│ Application │                   │
│  │   layer     │     │   layer     │                   │
│  └─────────────┘     └──────┬──────┘                   │
│                             │                           │
│                      ┌──────▼──────┐                   │
│                      │ interface   │                   │
│                      │   layer     │                   │
│                      └──────┬──────┘                   │
│                             │                           │
│                      ┌──────▼──────┐                   │
│                      │infrastructure│                   │
│                      │   layer     │                   │
│                      └─────────────┘                   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Layers

| Layer | Responsible | Contains |
|-------|-------------|----------|
| **Domain** | business logic | entities, value objects, aggregates, domain events |
| **Application** | orchestration | use cases, DTOs, application services |
| **Interface** | communication | API controllers, CLI, message handlers |
| **Infrastructure** | technical implementation | DB, external APIs, file system |

### Local development & migrations

| Stack | Migrate command | Notes |
|-------|-----------------|-------|
| Studio docker template | `./studio env <project> up` | Generic Postgres on 5432 |
| Supabase CLI (local) | `npm run db:migrate:supabase` in **project** repo | API ~54321, DB ~54322 — not legacy port 54320 |
| Local-first canvas | See [local-first-sync-playbook.md](local-first-sync-playbook.md) | Continuous sync, not one-time migration |

Agents: read project `package.json` scripts and `.env.local` before suggesting `psql` or migrate commands.

---

## SOLID principles

| Principle | Description | Implementation |
|-----------|-------------|----------------|
| **S**ingle Responsibility | one class = one responsibility | small, focused classes |
| **O**pen/Closed | open for extension, closed for modification | interfaces, strategy pattern |
| **L**iskov Substitution | subtypes are replaceable | clean inheritance |
| **I**nterface Segregation | no fat interfaces | many small interfaces |
| **D**ependency Inversion | abstractions instead of concretions | dependency injection |

### Implementation

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

// ❌ NOT SOLID
class UserService {
  async createUser(data: any) {
    const db = new Database(); // violates dependency inversion
    await db.query('INSERT INTO users...'); // violates SRP
  }
}
```

---

## PostgreSQL / Supabase

### Database design

```sql
-- Enums (type safety)
CREATE TYPE user_role AS ENUM ('admin', 'user', 'viewer');
CREATE TYPE task_status AS ENUM ('open', 'in_progress', 'done');

-- Tables
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL,
  role user_role NOT NULL DEFAULT 'user',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
```

### JSONb EAV structures

```sql
-- Flexible attribute system
CREATE TABLE product_attributes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  product_id UUID NOT NULL REFERENCES products(id),
  attribute_key TEXT NOT NULL,
  attribute_value JSONB NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- GIN index for JSONb
CREATE INDEX idx_product_attributes_value 
  ON product_attributes USING GIN(attribute_value);

-- Query
SELECT * FROM product_attributes 
WHERE attribute_value @> '{"color": "red"}';
```

### Migrations

```bash
# new migration
supabase migration new add_users_table

# run migrations
supabase db reset

# apply migrations
supabase db push
```

---

## API design

### RESTful resources

```
GET    /api/v1/users          # list
GET    /api/v1/users/:id      # detail
POST   /api/v1/users          # create
PATCH  /api/v1/users/:id      # update
DELETE /api/v1/users/:id      # delete
```

### Response format

```typescript
// success
{
  "data": { ... },
  "meta": { "page": 1, "total": 100 }
}

// error
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Email is invalid",
    "details": { "email": "Must be a valid email address" }
  }
}
```

### Versioning

```
/api/v1/...  # main version
/api/v2/...  # breaking changes
```

---

## Authentication

### JWT + refresh token

```typescript
// login
const accessToken = jwt.sign({ userId: user.id }, SECRET, { expiresIn: '15m' });
const refreshToken = jwt.sign({ userId: user.id }, REFRESH_SECRET, { expiresIn: '7d' });

// refresh
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

## Error handling

```typescript
// custom error classes
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

// global error handler
app.use((err, req, res, next) => {
  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      error: { code: err.code, message: err.message, details: err.details }
    });
  }
  
  // unknown error
  console.error(err);
  res.status(500).json({
    error: { code: 'INTERNAL_ERROR', message: 'An internal error occurred' }
  });
});
```

---

## Testing

### Unit tests

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

### Integration tests

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

## References

- `.quinsy-studio/knowledge-base/anti_ai_slop_protocol.md` — backend slop rules
- `.quinsy-studio/teams/02-backend-systems/` — backend team
- `.quinsy-studio/teams/08-platform-enterprise-engineering/` — infrastructure team
