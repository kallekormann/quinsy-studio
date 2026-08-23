import {
  defaultWelcomeContent,
  welcomeEmailHtml,
  welcomeEmailSubject,
  type WelcomeEmailContent,
} from './welcome-template';
import { sendTransactionalEmail, type EmailDeliveryResult } from './send-transactional-email';

export async function sendWelcomeEmail(
  to: string,
  content: WelcomeEmailContent = defaultWelcomeContent,
  displayName?: string,
): Promise<EmailDeliveryResult> {
  const name = displayName ?? to.split('@')[0] ?? 'there';
  return sendTransactionalEmail({
    to,
    subject: welcomeEmailSubject(content.appName),
    html: welcomeEmailHtml(name, content),
  });
}
