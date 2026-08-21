import { Resend } from 'resend';
import {
  defaultWelcomeContent,
  welcomeEmailHtml,
  welcomeEmailSubject,
  type WelcomeEmailContent,
} from './welcome-template';

function getResend() {
  const apiKey = process.env.RESEND_API_KEY;
  if (!apiKey) {
    return null;
  }
  return new Resend(apiKey);
}

function getFromAddress(): string {
  return process.env.RESEND_FROM_EMAIL ?? 'onboarding@resend.dev';
}

export async function sendWelcomeEmail(
  to: string,
  content: WelcomeEmailContent = defaultWelcomeContent,
  displayName?: string,
) {
  const resend = getResend();
  if (!resend) {
    console.warn('[email] RESEND_API_KEY not set — skipping welcome email');
    return { skipped: true as const };
  }

  const name = displayName ?? to.split('@')[0] ?? 'there';
  const { data, error } = await resend.emails.send({
    from: getFromAddress(),
    to,
    subject: welcomeEmailSubject(content.appName),
    html: welcomeEmailHtml(name, content),
  });

  if (error) {
    throw new Error(error.message);
  }

  return { id: data?.id };
}
