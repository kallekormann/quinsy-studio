import {
  teamInviteEmailHtml,
  teamInviteEmailSubject,
  type TeamInviteEmailContent,
} from './team-invite-template';
import { sendTransactionalEmail, type EmailDeliveryResult } from './send-transactional-email';

export async function sendTeamInviteEmail(
  to: string,
  content: TeamInviteEmailContent,
): Promise<EmailDeliveryResult> {
  return sendTransactionalEmail({
    to,
    subject: teamInviteEmailSubject(content.appName, content.teamName),
    html: teamInviteEmailHtml(content),
  });
}
