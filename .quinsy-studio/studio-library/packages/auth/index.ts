export type UserRole = 'admin' | 'user' | 'viewer';

export interface SessionUser {
  id: string;
  email: string;
  roles: UserRole[];
}

export interface AuthProvider {
  signIn(credentials: { email: string; password: string }): Promise<SessionUser>;
  signOut(): Promise<void>;
  getSession(): Promise<SessionUser | null>;
  hasPermission(user: SessionUser, permission: string): boolean;
}

/** Stub session provider — replace in projects (Supabase, NextAuth, etc.). */
export const stubAuthProvider: AuthProvider = {
  async signIn() {
    throw new Error('Configure auth provider in project');
  },
  async signOut() {},
  async getSession() {
    return null;
  },
  hasPermission(user, permission) {
    if (user.roles.includes('admin')) return true;
    return permission === 'read';
  },
};

export * from './types';
