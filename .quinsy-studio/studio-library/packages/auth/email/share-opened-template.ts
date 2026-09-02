export interface ShareOpenedEmailContent {
  appName: string;
  boardTitle: string;
  boardUrl: string;
  viewCount: number;
}

export function shareOpenedEmailSubject(appName: string, boardTitle: string): string {
  return `Someone viewed ${boardTitle} on ${appName}`;
}

export function shareOpenedEmailHtml(content: ShareOpenedEmailContent): string {
  const subject = shareOpenedEmailSubject(content.appName, content.boardTitle);
  const viewsLine =
    content.viewCount === 1
      ? 'This is the first view on your public share link.'
      : `Your share link has been viewed ${content.viewCount} times.`;

  return `<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><title>${escapeHtml(subject)}</title></head>
<body style="font-family: system-ui, sans-serif; line-height: 1.5; color: #171717; max-width: 480px; margin: 0 auto; padding: 24px;">
  <h1 style="font-size: 20px; margin: 0 0 12px;">Share link opened</h1>
  <p style="font-size: 14px; color: #525252;">Someone opened <strong>${escapeHtml(content.boardTitle)}</strong> via your public share link.</p>
  <p style="font-size: 14px; color: #525252;">${escapeHtml(viewsLine)}</p>
  <p><a href="${content.boardUrl}" style="display: inline-block; background: #6366f1; color: #fff; text-decoration: none; padding: 10px 18px; border-radius: 8px;">Open board</a></p>
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
