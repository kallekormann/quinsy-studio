import { describe, expect, it } from 'vitest';
import {
  shareOpenedEmailHtml,
  shareOpenedEmailSubject,
} from '@packages/auth/email/share-opened-template';

describe('share-opened-template', () => {
  it('builds subject with board title', () => {
    expect(shareOpenedEmailSubject('Moody', 'Mood board')).toBe(
      'Someone viewed Mood board on Moody',
    );
  });

  it('includes view count in html', () => {
    const html = shareOpenedEmailHtml({
      appName: 'Moody',
      boardTitle: 'Mood board',
      boardUrl: 'http://localhost:3000/board/abc',
      viewCount: 3,
    });

    expect(html).toContain('viewed 3 times');
    expect(html).toContain('Mood board');
  });
});
