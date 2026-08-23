export interface BoardInviteEmailContent {
  appName: string;
  boardTitle: string;
  acceptUrl: string;
  inviterEmail?: string;
}

export function boardInviteEmailSubject(appName: string, boardTitle: string): string {
  return `${boardTitle} was shared with you on ${appName}`;
}

export function boardInviteEmailHtml(content: BoardInviteEmailContent): string {
  const subject = boardInviteEmailSubject(content.appName, content.boardTitle);
  const inviterLine = content.inviterEmail
    ? `<p style="font-size: 14px; color: #525252;">${escapeHtml(content.inviterEmail)} invited you to collaborate on <strong>${escapeHtml(content.boardTitle)}</strong>.</p>`
    : `<p style="font-size: 14px; color: #525252;">You have been invited to collaborate on <strong>${escapeHtml(content.boardTitle)}</strong>.</p>`;

  return `<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><title>${escapeHtml(subject)}</title></head>
<body style="font-family: system-ui, sans-serif; line-height: 1.5; color: #171717; max-width: 480px; margin: 0 auto; padding: 24px;">
  <h1 style="font-size: 20px; margin: 0 0 12px;">Board invitation</h1>
  ${inviterLine}
  <p><a href="${content.acceptUrl}" style="display: inline-block; background: #6366f1; color: #fff; text-decoration: none; padding: 10px 18px; border-radius: 8px;">Open board</a></p>
  <p style="font-size: 13px; color: #737373;">Sign in with the email address this invite was sent to. Or copy this link: ${escapeHtml(content.acceptUrl)}</p>
</body>
</html>`;
}

function escapeHtml(value: string): string {
  return value
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}
