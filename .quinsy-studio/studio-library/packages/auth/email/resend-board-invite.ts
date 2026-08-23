import {
  boardInviteEmailHtml,
  boardInviteEmailSubject,
  type BoardInviteEmailContent,
} from './board-invite-template';
import { sendTransactionalEmail, type EmailDeliveryResult } from './send-transactional-email';

export async function sendBoardInviteEmail(
  to: string,
  content: BoardInviteEmailContent,
): Promise<EmailDeliveryResult> {
  return sendTransactionalEmail({
    to,
    subject: boardInviteEmailSubject(content.appName, content.boardTitle),
    html: boardInviteEmailHtml(content),
  });
}
