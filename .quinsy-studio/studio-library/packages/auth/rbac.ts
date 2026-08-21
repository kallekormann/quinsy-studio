import type { User } from '@supabase/supabase-js';
import type { UserRole } from './types';

const ROLE_ORDER: UserRole[] = ['viewer', 'user', 'admin'];

export function getUserRoles(user: User): UserRole[] {
  const raw = user.app_metadata?.role ?? user.user_metadata?.role ?? 'user';
  if (raw === 'admin' || raw === 'user' || raw === 'viewer') {
    return [raw];
  }
  return ['user'];
}

export function hasRole(roles: UserRole[], required: UserRole): boolean {
  if (roles.includes('admin')) {
    return true;
  }
  const requiredIndex = ROLE_ORDER.indexOf(required);
  return roles.some((role) => ROLE_ORDER.indexOf(role) >= requiredIndex);
}

export function hasPermission(user: User, permission: 'read' | 'write' | 'admin'): boolean {
  const roles = getUserRoles(user);
  if (permission === 'admin') {
    return roles.includes('admin');
  }
  if (permission === 'write') {
    return hasRole(roles, 'user');
  }
  return hasRole(roles, 'viewer');
}
