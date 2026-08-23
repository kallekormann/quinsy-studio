import {
  defaultFromAddress,
  type EmailDeliveryResult,
  mailpitInboxUrl,
} from './email-provider';

export async function sendMailpitEmail(input: {
  to: string;
  subject: string;
  html: string;
  from?: string;
}): Promise<EmailDeliveryResult> {
  const baseUrl = mailpitInboxUrl() ?? 'http://127.0.0.1:54324';
  const fromEmail = input.from ?? defaultFromAddress();

  let response: Response;
  try {
    response = await fetch(`${baseUrl}/api/v1/send`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        From: { Email: fromEmail, Name: 'MoodBoardly' },
        To: [{ Email: input.to }],
        Subject: input.subject,
        HTML: input.html,
      }),
    });
  } catch (error) {
    const message = error instanceof Error ? error.message : 'Mailpit unreachable';
    throw new Error(
      `${message}. Start Mailpit with ./studio env moody up (inbox: ${baseUrl}).`,
    );
  }

  if (!response.ok) {
    const text = await response.text().catch(() => '');
    throw new Error(text || `Mailpit send failed (${response.status})`);
  }

  const data = (await response.json().catch(() => ({}))) as { ID?: string };
  console.info(`[email] Sent via Mailpit to ${input.to} — inbox: ${baseUrl}`);
  return { delivered: true, id: data.ID, provider: 'mailpit' };
}
