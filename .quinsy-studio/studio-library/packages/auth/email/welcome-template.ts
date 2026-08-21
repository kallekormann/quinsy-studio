export interface WelcomeEmailContent {
  appName: string;
  tagline: string;
  footerNote?: string;
}

export const defaultWelcomeContent: WelcomeEmailContent = {
  appName: 'Your app',
  tagline: 'Your account is ready.',
  footerNote: 'You can sign in on any device with the same email.',
};

export function welcomeEmailSubject(appName: string): string {
  return `Welcome to ${appName}`;
}

export function welcomeEmailHtml(
  name: string,
  content: WelcomeEmailContent = defaultWelcomeContent,
): string {
  const appUrl = process.env.NEXT_PUBLIC_APP_URL ?? 'http://localhost:3000';
  const subject = welcomeEmailSubject(content.appName);
  return `<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><title>${subject}</title></head>
<body style="font-family: system-ui, sans-serif; line-height: 1.5; color: #171717; max-width: 480px; margin: 0 auto; padding: 24px;">
  <h1 style="font-size: 20px; margin: 0 0 12px;">Welcome, ${escapeHtml(name)}</h1>
  <p>${escapeHtml(content.tagline)}</p>
  <p><a href="${appUrl}" style="display: inline-block; background: #6366f1; color: #fff; text-decoration: none; padding: 10px 18px; border-radius: 8px;">Open ${escapeHtml(content.appName)}</a></p>
  ${content.footerNote ? `<p style="font-size: 13px; color: #737373;">${escapeHtml(content.footerNote)}</p>` : ''}
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
