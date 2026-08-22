import { describe, expect, it } from 'vitest';
import { createFailureRateLimiter } from './rate-limit';

describe('createFailureRateLimiter', () => {
  it('blocks after max failures within the window', () => {
    const limiter = createFailureRateLimiter(3, 60_000);
    const key = '127.0.0.1:token';
    const now = 1_000_000;

    expect(limiter.isBlocked(key, now)).toBe(false);
    limiter.recordFailure(key, now);
    limiter.recordFailure(key, now + 1);
    expect(limiter.isBlocked(key, now + 2)).toBe(false);
    limiter.recordFailure(key, now + 2);
    expect(limiter.isBlocked(key, now + 3)).toBe(true);
  });
});
