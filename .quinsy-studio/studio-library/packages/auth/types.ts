export type UserRole = 'admin' | 'user' | 'viewer';

export interface SessionUser {
  id: string;
  email: string;
  roles: UserRole[];
}
