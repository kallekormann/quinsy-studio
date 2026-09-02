import {
  shareOpenedEmailHtml,
  shareOpenedEmailSubject,
  type ShareOpenedEmailContent,
} from './share-opened-template';
import { sendTransactionalEmail, type EmailDeliveryResult } from './send-transactional-email';

export async function sendShareOpenedEmail(
  to: string,
  content: ShareOpenedEmailContent,
): Promise<EmailDeliveryResult> {
  return sendTransactionalEmail({
    to,
    subject: shareOpenedEmailSubject(content.appName, content.boardTitle),
    html: shareOpenedEmailHtml(content),
  });
}
