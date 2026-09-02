import { describe, expect, it, vi, beforeEach, afterEach } from 'vitest';
import { burstSparks } from './burst';

describe('celebration burst (MOOD-0332)', () => {
  beforeEach(() => {
    vi.stubGlobal('requestAnimationFrame', (cb: FrameRequestCallback) => {
      cb(0);
      return 0;
    });
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('appends spark nodes to the provided host', () => {
    const appended: { className: string }[] = [];
    const host = {
      appendChild(node: { className: string }) {
        appended.push(node);
        return node;
      },
    };

    const createElement = vi.fn((tag: string) => {
      expect(tag).toBe('div');
      const el = {
        className: '',
        style: {
          left: '',
          top: '',
          width: '',
          height: '',
          background: '',
          setProperty: vi.fn(),
        },
        setAttribute: vi.fn(),
        classList: { add: vi.fn() },
        remove: vi.fn(),
      };
      return el;
    });
    vi.stubGlobal('document', {
      createElement,
      head: { appendChild: vi.fn() },
      querySelector: () => null,
    });
    vi.stubGlobal('window', {
      setTimeout: vi.fn((fn: () => void) => {
        fn();
        return 0;
      }),
    });

    burstSparks({
      host: host as unknown as ParentNode & { appendChild: (node: Node) => Node },
      cx: 12,
      cy: 34,
      count: 5,
      injectStyles: false,
      className: 'spark',
    });

    expect(appended).toHaveLength(5);
    expect(appended.every((n) => n.className.includes('spark'))).toBe(true);
  });
});
