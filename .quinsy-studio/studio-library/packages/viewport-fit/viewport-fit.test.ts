import { describe, expect, it } from 'vitest';
import { viewportZoomToFitBounds } from './viewport-fit';

const STAGE = { width: 800, height: 600 } as const;
const ITEM_SIZE_PX = 100;
const ITEM = { x: 0, y: 0, width: ITEM_SIZE_PX, height: ITEM_SIZE_PX } as const;
const ZOOM = { minZoom: 0.1, maxZoom: 4 } as const;

describe('viewportZoomToFitBounds', () => {
  it('centers and scales bounds into the stage', () => {
    const viewport = viewportZoomToFitBounds(ITEM, STAGE.width, STAGE.height, ZOOM);
    expect(viewport.zoom).toBeGreaterThan(0);
    expect(viewport.x).toBeGreaterThan(0);
    expect(viewport.y).toBeGreaterThan(0);
  });
});
