import type { AuthProvider, SessionUser } from './types';

/** @deprecated Use Supabase SSR clients from `./next/*` instead. */
export const stubAuthProvider: AuthProvider = {
  async signIn() {
    throw new Error('Use @packages/auth/next client helpers with Supabase');
  },
  async signOut() {},
  async getSession() {
    return null;
  },
  hasPermission(user: SessionUser, permission: string) {
    if (user.roles.includes('admin')) return true;
    return permission === 'read';
  },
};
