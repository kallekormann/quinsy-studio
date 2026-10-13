import { describe, expect, it } from 'vitest';
import {
  shareOpenedEmailHtml,
  shareOpenedEmailSubject,
} from '@packages/auth/email/share-opened-template';

describe('share-opened-template', () => {
  it('builds subject with board title', () => {
    expect(shareOpenedEmailSubject('Acme', 'Launch board')).toBe(
      'Someone viewed Launch board on Acme',
    );
  });

  it('includes view count in html', () => {
    const html = shareOpenedEmailHtml({
      appName: 'Acme',
      boardTitle: 'Launch board',
      boardUrl: 'http://localhost:3000/board/abc',
      viewCount: 3,
    });

    expect(html).toContain('viewed 3 times');
    expect(html).toContain('Launch board');
  });
});
