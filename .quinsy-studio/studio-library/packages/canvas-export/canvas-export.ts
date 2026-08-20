import type { Stage as KonvaStage } from 'konva/lib/Stage';
import type { BoundsOptions, CanvasExportItem, ExportRect, StageCaptureOptions } from './types';

const EXPORT_LAYOUT = {
  paddingPx: 48,
  defaultPaletteBarPx: 20,
} as const;

function parseFrameChildIds(contentJson: string): string[] {
  try {
    const parsed = JSON.parse(contentJson) as { childIds?: string[] };
    return parsed.childIds ?? [];
  } catch {
    return [];
  }
}

function defaultImageExtraHeight(item: CanvasExportItem): number {
  try {
    const parsed = JSON.parse(item.contentJson) as { palette?: unknown[] };
    return Array.isArray(parsed.palette) && parsed.palette.length > 0
      ? EXPORT_LAYOUT.defaultPaletteBarPx
      : 0;
  } catch {
    return 0;
  }
}

export function itemExportBounds(item: CanvasExportItem, options: BoundsOptions = {}): ExportRect {
  const extra =
    item.type === 'image'
      ? (options.imageExtraHeight ?? defaultImageExtraHeight)(item)
      : 0;
  return { x: item.x, y: item.y, width: item.width, height: item.height + extra };
}

export function unionBounds(rects: ExportRect[]): ExportRect | null {
  if (rects.length === 0) {
    return null;
  }
  const xs = rects.map((r) => r.x);
  const ys = rects.map((r) => r.y);
  const x2 = rects.map((r) => r.x + r.width);
  const y2 = rects.map((r) => r.y + r.height);
  const x = Math.min(...xs);
  const y = Math.min(...ys);
  return {
    x,
    y,
    width: Math.max(...x2) - x,
    height: Math.max(...y2) - y,
  };
}

export function boundsForItems(
  items: CanvasExportItem[],
  options?: BoundsOptions,
): ExportRect | null {
  return unionBounds(items.map((item) => itemExportBounds(item, options)));
}

export function boundsForFrame(
  frame: CanvasExportItem,
  allItems: CanvasExportItem[],
  options?: BoundsOptions,
): ExportRect {
  const frameBounds = itemExportBounds(frame, options);
  const childIds = parseFrameChildIds(frame.contentJson);
  const childItems = allItems.filter((item) => childIds.includes(item.id));
  const merged = unionBounds([
    frameBounds,
    ...childItems.map((item) => itemExportBounds(item, options)),
  ]);
  return merged ?? frameBounds;
}

/** Temporarily reframes the Konva stage and returns a PNG data URL. Restores stage after capture. */
export function captureStageToPng(stage: KonvaStage, options: StageCaptureOptions): string {
  const { bounds, pixelRatio = 2, padding = EXPORT_LAYOUT.paddingPx } = options;

  const prev = {
    width: stage.width(),
    height: stage.height(),
    x: stage.x(),
    y: stage.y(),
    scaleX: stage.scaleX(),
    scaleY: stage.scaleY(),
  };

  const exportWidth = bounds.width + padding * 2;
  const exportHeight = bounds.height + padding * 2;

  stage.width(exportWidth);
  stage.height(exportHeight);
  stage.scale({ x: 1, y: 1 });
  stage.position({ x: -bounds.x + padding, y: -bounds.y + padding });
  stage.batchDraw();

  const dataUrl = stage.toDataURL({ pixelRatio });

  stage.width(prev.width);
  stage.height(prev.height);
  stage.scale({ x: prev.scaleX, y: prev.scaleY });
  stage.position({ x: prev.x, y: prev.y });
  stage.batchDraw();

  return dataUrl;
}

export function downloadDataUrl(dataUrl: string, filename: string): void {
  const link = document.createElement('a');
  link.download = filename;
  link.href = dataUrl;
  link.click();
}

function loadImage(src: string): Promise<HTMLImageElement> {
  return new Promise((resolve, reject) => {
    const image = new Image();
    image.onload = () => resolve(image);
    image.onerror = () => reject(new Error('Failed to load export image'));
    image.src = src;
  });
}

/** Download a one-page PDF from a PNG data URL (peer dep: jspdf). */
export async function downloadPdfFromPng(dataUrl: string, filename: string): Promise<void> {
  const { jsPDF } = await import('jspdf');
  const image = await loadImage(dataUrl);
  const width = image.naturalWidth || image.width;
  const height = image.naturalHeight || image.height;
  const doc = new jsPDF({
    orientation: width >= height ? 'landscape' : 'portrait',
    unit: 'px',
    format: [width, height],
  });
  doc.addImage(dataUrl, 'PNG', 0, 0, width, height);
  doc.save(`${filename}.pdf`);
}

export function sanitizeFilename(name: string): string {
  return (
    name
      .replace(/[^\w\-]+/g, '-')
      .replace(/-+/g, '-')
      .slice(0, 80) || 'board'
  );
}
