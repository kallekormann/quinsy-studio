import { describe, expect, it } from 'vitest';
import { DEFAULT_WATERMARK_TEXT, drawWatermarkOnCanvas, watermarkLayout } from './watermark';

describe('watermark', () => {
  it('places text in bottom-right with margin', () => {
    const layout = watermarkLayout(1200, 800);
    expect(layout.text).toBe(DEFAULT_WATERMARK_TEXT);
    expect(layout.x).toBe(1200 - 28);
    expect(layout.y).toBe(800 - 28);
    expect(layout.pillWidth).toBeGreaterThan(80);
    expect(layout.opacity).toBeGreaterThan(0.5);
    expect(layout.opacity).toBeLessThanOrEqual(1);
  });

  it('respects custom text and skip-friendly layout', () => {
    const layout = watermarkLayout(400, 300, { text: 'Test', marginPx: 16 });
    expect(layout.text).toBe('Test');
    expect(layout.y).toBe(300 - 16);
    expect(layout.x).toBe(400 - 16);
  });

  it('draws watermark on canvas context', () => {
    const calls: Array<{ method: string; args: unknown[] }> = [];
    const ctx = {
      font: '',
      globalAlpha: 1,
      fillStyle: '',
      textAlign: 'left',
      textBaseline: 'alphabetic',
      shadowColor: '',
      shadowBlur: 0,
      beginPath: () => undefined,
      roundRect: (...args: unknown[]) => calls.push({ method: 'roundRect', args }),
      fill: () => calls.push({ method: 'fill', args: [] }),
      fillText: (...args: unknown[]) => calls.push({ method: 'fillText', args }),
    };

    drawWatermarkOnCanvas(ctx as Parameters<typeof drawWatermarkOnCanvas>[0], 800, 600, {
      text: 'Acme',
    });

    expect(calls.some((call) => call.method === 'fillText')).toBe(true);
    const fillText = calls.find((call) => call.method === 'fillText');
    expect(fillText?.args[0]).toBe('Acme');
  });
});
