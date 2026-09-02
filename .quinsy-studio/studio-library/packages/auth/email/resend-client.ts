import { Resend } from 'resend';
import { defaultFromAddress, type EmailDeliveryResult } from './email-provider';

function getResend() {
  const apiKey = process.env.RESEND_API_KEY;
  if (!apiKey) {
    return null;
  }
  return new Resend(apiKey);
}

/** Resend test keys only deliver to the account owner's email until a domain is verified. */
export function isResendSandboxRestriction(message: string): boolean {
  const lower = message.toLowerCase();
  return (
    lower.includes('testing emails') ||
    lower.includes('verify a domain') ||
    lower.includes('resend.com/domains')
  );
}

export async function sendResendEmail(input: {
  to: string;
  subject: string;
  html: string;
  from?: string;
}): Promise<EmailDeliveryResult> {
  const resend = getResend();
  if (!resend) {
    console.warn('[email] RESEND_API_KEY not set — skipping email');
    return { delivered: false, skipped: true, reason: 'missing_api_key' };
  }

  const { data, error } = await resend.emails.send({
    from: input.from ?? defaultFromAddress(),
    to: input.to,
    subject: input.subject,
    html: input.html,
  });

  if (error) {
    if (isResendSandboxRestriction(error.message)) {
      console.warn(
        '[email] Resend sandbox restriction — share invite link manually:',
        error.message,
      );
      return { delivered: false, skipped: true, reason: 'sandbox_restriction' };
    }
    throw new Error(error.message);
  }

  return { delivered: true, id: data?.id, provider: 'resend' };
}
