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
