export type ItemBounds = {
  x: number;
  y: number;
  width: number;
  height: number;
};

export type Viewport = {
  x: number;
  y: number;
  zoom: number;
};

export type ZoomToFitOptions = {
  minZoom: number;
  maxZoom: number;
  viewportPaddingPx?: number;
  zoomCap?: number;
};

export function viewportZoomToFitBounds(
  bounds: ItemBounds,
  stageWidth: number,
  stageHeight: number,
  options: ZoomToFitOptions,
): Viewport {
  const padding = options.viewportPaddingPx ?? 48;
  const zoomCap = options.zoomCap ?? 2;
  const innerWidth = Math.max(stageWidth - padding * 2, 1);
  const innerHeight = Math.max(stageHeight - padding * 2, 1);

  const zoomX = innerWidth / Math.max(bounds.width, 1);
  const zoomY = innerHeight / Math.max(bounds.height, 1);
  const rawZoom = Math.min(zoomX, zoomY, zoomCap);
  const zoom = Math.max(options.minZoom, Math.min(options.maxZoom, rawZoom));

  const centerX = bounds.x + bounds.width / 2;
  const centerY = bounds.y + bounds.height / 2;

  return {
    x: stageWidth / 2 - centerX * zoom,
    y: stageHeight / 2 - centerY * zoom,
    zoom,
  };
}
