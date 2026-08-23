export interface TeamInviteEmailContent {
  appName: string;
  teamName: string;
  acceptUrl: string;
  inviterEmail?: string;
}

export function teamInviteEmailSubject(appName: string, teamName: string): string {
  return `Join ${teamName} on ${appName}`;
}

export function teamInviteEmailHtml(content: TeamInviteEmailContent): string {
  const subject = teamInviteEmailSubject(content.appName, content.teamName);
  const inviterLine = content.inviterEmail
    ? `<p style="font-size: 14px; color: #525252;">${escapeHtml(content.inviterEmail)} invited you to collaborate on <strong>${escapeHtml(content.teamName)}</strong>.</p>`
    : `<p style="font-size: 14px; color: #525252;">You have been invited to collaborate on <strong>${escapeHtml(content.teamName)}</strong>.</p>`;

  return `<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><title>${escapeHtml(subject)}</title></head>
<body style="font-family: system-ui, sans-serif; line-height: 1.5; color: #171717; max-width: 480px; margin: 0 auto; padding: 24px;">
  <h1 style="font-size: 20px; margin: 0 0 12px;">Team invite</h1>
  ${inviterLine}
  <p><a href="${content.acceptUrl}" style="display: inline-block; background: #6366f1; color: #fff; text-decoration: none; padding: 10px 18px; border-radius: 8px;">Accept invite</a></p>
  <p style="font-size: 13px; color: #737373;">Or copy this link: ${escapeHtml(content.acceptUrl)}</p>
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
