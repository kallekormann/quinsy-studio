import { describe, expect, it } from 'vitest';
import type { User } from '@supabase/supabase-js';
import { getUserRoles, hasPermission, hasRole } from './rbac';

function userWithRole(role: string): User {
  return {
    id: '00000000-0000-0000-0000-000000000001',
    app_metadata: { role },
    user_metadata: {},
    aud: 'authenticated',
    created_at: new Date().toISOString(),
  } as User;
}

describe('rbac', () => {
  it('defaults to user role', () => {
    expect(getUserRoles({ id: 'x' } as User)).toEqual(['user']);
  });

  it('admin satisfies elevated checks', () => {
    expect(hasRole(getUserRoles(userWithRole('admin')), 'user')).toBe(true);
    expect(hasPermission(userWithRole('admin'), 'admin')).toBe(true);
  });

  it('viewer cannot write', () => {
    expect(hasPermission(userWithRole('viewer'), 'write')).toBe(false);
    expect(hasPermission(userWithRole('viewer'), 'read')).toBe(true);
  });
});
