import bcrypt from 'bcryptjs';

export const DEFAULT_BCRYPT_ROUNDS = 10;
export const DEFAULT_VERIFY_MAX_AGE_SECONDS = 60 * 60 * 24;

export async function hashPassword(
  password: string,
  rounds = DEFAULT_BCRYPT_ROUNDS,
): Promise<string> {
  return bcrypt.hash(password, rounds);
}

export async function verifyPassword(password: string, passwordHash: string): Promise<boolean> {
  return bcrypt.compare(password, passwordHash);
}

export function verifyCookieName(prefix: string, token: string): string {
  return `${prefix}_${token}`;
}

export function isVerifyCookieSet(request: Request, cookieName: string): boolean {
  const cookieHeader = request.headers.get('cookie') ?? '';
  return cookieHeader.split(';').some((part) => {
    const [key, value] = part.trim().split('=');
    return key === cookieName && value === '1';
  });
}
