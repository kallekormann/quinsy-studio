import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { sendMailpitEmail } from '@packages/auth/email/mailpit-client';

describe('sendMailpitEmail', () => {
  const env = process.env;

  beforeEach(() => {
    process.env = { ...env, MAILPIT_URL: 'http://127.0.0.1:54324' };
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue({
        ok: true,
        json: async () => ({ ID: 'msg-1' }),
      }),
    );
  });

  afterEach(() => {
    process.env = env;
    vi.unstubAllGlobals();
  });

  it('posts to Mailpit send API', async () => {
    const result = await sendMailpitEmail({
      to: 'collab@example.com',
      subject: 'Test',
      html: '<p>Hi</p>',
    });

    expect(result.delivered).toBe(true);
    expect(fetch).toHaveBeenCalledWith(
      'http://127.0.0.1:54324/api/v1/send',
      expect.objectContaining({ method: 'POST' }),
    );
  });
});
