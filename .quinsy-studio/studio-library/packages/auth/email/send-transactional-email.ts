import { resolveEmailProvider, type EmailDeliveryResult } from './email-provider';
import { sendMailpitEmail } from './mailpit-client';
import { sendResendEmail } from './resend-client';

export async function sendTransactionalEmail(input: {
  to: string;
  subject: string;
  html: string;
  from?: string;
}): Promise<EmailDeliveryResult> {
  const provider = resolveEmailProvider();

  if (provider === 'mailpit') {
    return sendMailpitEmail(input);
  }

  if (provider === 'resend') {
    return sendResendEmail(input);
  }

  console.warn('[email] No email provider configured — skipping send');
  return { delivered: false, skipped: true, reason: 'not_configured' };
}

export type { EmailDeliveryResult } from './email-provider';
export { mailpitInboxUrl, resolveEmailProvider } from './email-provider';
