import { describe, expect, it } from 'vitest';
import {
  hashPassword,
  isVerifyCookieSet,
  verifyCookieName,
  verifyPassword,
} from './password-gate';

describe('password-gate', () => {
  it('hashes and verifies passwords', async () => {
    const hash = await hashPassword('secret-pass');
    expect(hash).not.toBe('secret-pass');
    await expect(verifyPassword('secret-pass', hash)).resolves.toBe(true);
    await expect(verifyPassword('wrong', hash)).resolves.toBe(false);
  });

  it('detects verify cookie', () => {
    const name = verifyCookieName('app_share_verified', 'abc123');
    const request = new Request('http://localhost/share/abc123', {
      headers: { cookie: `${name}=1` },
    });
    expect(isVerifyCookieSet(request, name)).toBe(true);
  });
});
