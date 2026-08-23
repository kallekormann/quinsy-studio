export type EmailDeliveryResult =
  | { delivered: true; id?: string; provider: 'mailpit' | 'resend' }
  | { delivered: false; skipped: true; reason: 'missing_api_key' | 'sandbox_restriction' | 'not_configured' };

export type EmailProvider = 'mailpit' | 'resend' | 'none';

export function resolveEmailProvider(): EmailProvider {
  const explicit = process.env.EMAIL_PROVIDER?.trim().toLowerCase();

  if (explicit === 'resend') {
    return process.env.RESEND_API_KEY ? 'resend' : 'none';
  }
  if (explicit === 'mailpit') {
    return 'mailpit';
  }
  if (explicit === 'none' || explicit === 'skip') {
    return 'none';
  }

  if (process.env.NODE_ENV === 'development') {
    return 'mailpit';
  }

  return process.env.RESEND_API_KEY ? 'resend' : 'none';
}

export function mailpitInboxUrl(): string | undefined {
  if (resolveEmailProvider() !== 'mailpit') {
    return undefined;
  }
  return process.env.MAILPIT_URL?.replace(/\/$/, '') ?? 'http://127.0.0.1:54324';
}

export function defaultFromAddress(): string {
  return (
    process.env.EMAIL_FROM ??
    process.env.SMTP_FROM ??
    process.env.RESEND_FROM_EMAIL ??
    'noreply@moodboardly.local'
  );
}
