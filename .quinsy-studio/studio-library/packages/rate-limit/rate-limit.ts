type RateLimitBucket = {
  failures: number[];
  blockedUntil: number;
};

/** In-memory failure counter with sliding window — use per-route singleton in serverless with care. */
export function createFailureRateLimiter(maxFailures: number, windowMs: number) {
  const buckets = new Map<string, RateLimitBucket>();

  function getBucket(key: string): RateLimitBucket {
    const existing = buckets.get(key);
    if (existing) {
      return existing;
    }
    const bucket = { failures: [], blockedUntil: 0 };
    buckets.set(key, bucket);
    return bucket;
  }

  return {
    isBlocked(key: string, now = Date.now()): boolean {
      const bucket = getBucket(key);
      if (bucket.blockedUntil > now) {
        return true;
      }
      bucket.failures = bucket.failures.filter((t) => now - t < windowMs);
      return bucket.failures.length >= maxFailures;
    },

    recordFailure(key: string, now = Date.now()): void {
      const bucket = getBucket(key);
      bucket.failures = bucket.failures.filter((t) => now - t < windowMs);
      bucket.failures.push(now);
      if (bucket.failures.length >= maxFailures) {
        bucket.blockedUntil = now + windowMs;
      }
    },

    reset(key: string): void {
      buckets.delete(key);
    },
  };
}

export function clientIp(request: Request): string {
  return request.headers.get('x-forwarded-for')?.split(',')[0]?.trim() ?? 'local';
}
