# Feature Gating Package

> Feature-Flags, Rollout-Strategien und Segmentierung für progressive Enthüllung.

## Features

- Feature-Flags (boolean, string, JSON)
- Percentage-Based Rollouts
- User-Segmentation
- A/B-Testing-Integration
- Kill-Switch für Features
- Audit-Log für Änderungen

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                FEATURE GATING FLOW                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. Feature Request                                     │
│     └─▶ Check flag status                              │
│     └─▶ Evaluate rules (segment, percentage)           │
│     └─▶ Return feature state                           │
│                                                         │
│  2. Rollout                                            │
│     └─▶ Start with 0%                                  │
│     └─▶ Gradually increase                             │
│     └─▶ Monitor metrics                                │
│     └─▶ Full rollout or rollback                       │
│                                                         │
│  3. Cleanup                                             │
│     └─▶ Remove flag after full rollout                 │
│     └─▶ Clean up code                                  │
│     └─▶ Update documentation                           │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Configuration

```typescript
// feature-gating.config.ts
export const featureConfig = {
  flags: {
    'new-dashboard': {
      enabled: true,
      rollout: 50, // percentage
      segments: ['beta-users', 'internal'],
    },
    'advanced-analytics': {
      enabled: false,
      killSwitch: true,
    },
    'experimental-api': {
      enabled: true,
      rollout: 10,
      segments: ['enterprise'],
    },
  },
};
```

## Usage

```typescript
import { featureFlag, isEnabled, rollout } from '@studio/feature-gating';

// Simple check
if (isEnabled('new-dashboard', user)) {
  // Show new dashboard
}

// With default
const dashboard = featureFlag('new-dashboard', {
  enabled: () => <NewDashboard />,
  disabled: () => <OldDashboard />,
});

// Rollout check
if (rollout('advanced-analytics', user, 25)) {
  // 25% of users see this
}
```

## API

```typescript
// Get all flags for a user
const flags = await featureFlag.getAll(user);

// Update flag
await featureFlag.update('new-dashboard', {
  rollout: 75,
  segments: ['beta-users', 'internal', 'early-adopters'],
});

// Disable flag
await featureFlag.disable('experimental-api');

// Audit log
const history = await featureFlag.getHistory('new-dashboard');
```

## Best Practices

1. **Naming Convention:** `feature-{area}-{name}` (e.g., `feature-dashboard-analytics`)
2. **Default Values:** Always provide sensible defaults
3. **Cleanup:** Remove flags after full rollout
4. **Documentation:** Document flag purpose and rollout plan
5. **Monitoring:** Track flag usage and impact
