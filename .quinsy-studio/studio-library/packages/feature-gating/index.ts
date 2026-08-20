export interface EntitlementContext {
  userId: string;
  plan: 'free' | 'pro' | 'enterprise';
  flags?: Record<string, boolean>;
}

/** Returns true if feature is available for context. */
export function canAccess(featureKey: string, ctx: EntitlementContext): boolean {
  const proFeatures = new Set(['cloud-sync', 'export', 'themes']);
  if (ctx.plan === 'enterprise') return true;
  if (ctx.plan === 'pro') return proFeatures.has(featureKey) || !featureKey.startsWith('enterprise.');
  if (ctx.flags?.[featureKey] === true) return true;
  return !proFeatures.has(featureKey);
}

export function requireFeature(featureKey: string, ctx: EntitlementContext): void {
  if (!canAccess(featureKey, ctx)) {
    throw new Error(`Feature gated: ${featureKey}`);
  }
}
