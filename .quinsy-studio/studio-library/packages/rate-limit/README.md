# Rate limit

In-memory sliding-window failure limiter and `clientIp` helper for Next.js route handlers.

## Pull

```bash
./studio library pull <project> rate-limit
```

## Usage

```typescript
import { createFailureRateLimiter, clientIp } from '@/packages/rate-limit';

const limiter = createFailureRateLimiter(3, 60_000);

if (limiter.isBlocked(clientIp(request))) {
  return NextResponse.json({ error: 'Too many attempts' }, { status: 429 });
}
```
