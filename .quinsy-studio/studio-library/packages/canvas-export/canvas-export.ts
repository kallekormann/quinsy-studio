import type { Stage as KonvaStage } from 'konva/lib/Stage';
import type { BoundsOptions, CanvasExportItem, ExportRect, StageCaptureOptions } from './types';

const EXPORT_LAYOUT = {
  paddingPx: 48,
  defaultPaletteBarPx: 20,
} as const;

/** Reject empty / truncated downloads (MOOD-0357). Tiny valid PNG is larger than this. */
const MIN_EXPORT_FILE_BYTES = 32;

/** Delay object-URL revoke so the browser can finish starting the download. */
const OBJECT_URL_REVOKE_MS = 60_000;

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
    item.type === 'image' ? (options.imageExtraHeight ?? defaultImageExtraHeight)(item) : 0;
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
    draggable: stage.draggable(),
  };

  const exportWidth = bounds.width + padding * 2;
  const exportHeight = bounds.height + padding * 2;

  // Prevent pan/drag handlers from firing while we reframe the stage for export.
  stage.stopDrag();
  stage.draggable(false);

  stage.width(exportWidth);
  stage.height(exportHeight);
  stage.scale({ x: 1, y: 1 });
  stage.position({ x: -bounds.x + padding, y: -bounds.y + padding });
  stage.batchDraw();

  let dataUrl: string;
  try {
    dataUrl = stage.toDataURL({ pixelRatio });
  } finally {
    stage.width(prev.width);
    stage.height(prev.height);
    stage.scale({ x: prev.scaleX, y: prev.scaleY });
    stage.position({ x: prev.x, y: prev.y });
    stage.draggable(prev.draggable);
    stage.batchDraw();
  }

  return dataUrl;
}

function bytesToBlob(bytes: Uint8Array, mime: string): Blob {
  const copy = new Uint8Array(bytes.byteLength);
  copy.set(bytes);
  return new Blob([copy], { type: mime });
}

/** Blob download with size check — avoids 0KB saves from oversized `data:` hrefs (MOOD-0357). */
export function downloadBlob(blob: Blob, filename: string): void {
  if (blob.size < MIN_EXPORT_FILE_BYTES) {
    throw new Error('Export produced an empty file — try a lower resolution or fewer items.');
  }
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.download = filename;
  link.href = url;
  link.rel = 'noopener';
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  window.setTimeout(() => URL.revokeObjectURL(url), OBJECT_URL_REVOKE_MS);
}

export function assertExportDataUrl(dataUrl: string): void {
  if (!dataUrl.startsWith('data:')) {
    throw new Error('Export capture failed — empty or invalid image.');
  }
  const { bytes } = dataUrlToUint8Array(dataUrl);
  if (bytes.byteLength < MIN_EXPORT_FILE_BYTES) {
    throw new Error('Export capture was empty — nothing to download.');
  }
}

export function downloadDataUrl(dataUrl: string, filename: string): void {
  assertExportDataUrl(dataUrl);
  const { bytes, mime } = dataUrlToUint8Array(dataUrl);
  downloadBlob(bytesToBlob(bytes, mime), filename);
}

function loadImage(src: string): Promise<HTMLImageElement> {
  return new Promise((resolve, reject) => {
    const image = new Image();
    image.onload = () => resolve(image);
    image.onerror = () => reject(new Error('Failed to load export image'));
    image.src = src;
  });
}

/** Decode a data URL without fetch() — large Konva PNGs often fail fetch(dataUrl) (MOOD-0356). */
export function dataUrlToUint8Array(dataUrl: string): { bytes: Uint8Array; mime: string } {
  const comma = dataUrl.indexOf(',');
  if (comma < 0) {
    throw new Error('Invalid data URL');
  }
  const header = dataUrl.slice(0, comma);
  const payload = dataUrl.slice(comma + 1);
  const mime = /data:([^;]+)/.exec(header)?.[1] ?? 'image/png';
  const isBase64 = /;base64/i.test(header);
  if (!isBase64) {
    const decoded = decodeURIComponent(payload);
    const bytes = new Uint8Array(decoded.length);
    for (let i = 0; i < decoded.length; i += 1) {
      bytes[i] = decoded.charCodeAt(i);
    }
    return { bytes, mime };
  }
  const binary = atob(payload);
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i += 1) {
    bytes[i] = binary.charCodeAt(i);
  }
  return { bytes, mime };
}

const PDF_IMAGE_LIMITS = {
  jpegQuality: 0.9,
  largeEdgePx: 3600,
  largeDataUrlChars: 1_500_000,
} as const;

async function decodePngDataUrl(
  dataUrl: string,
): Promise<{ width: number; height: number; exportDataUrl: string; format: 'PNG' | 'JPEG' }> {
  let blob: Blob;
  if (dataUrl.startsWith('data:')) {
    const { bytes, mime } = dataUrlToUint8Array(dataUrl);
    blob = bytesToBlob(bytes, mime);
  } else {
    const response = await fetch(dataUrl);
    blob = await response.blob();
  }

  if (blob.size < MIN_EXPORT_FILE_BYTES) {
    throw new Error('Export image is empty');
  }

  let width = 0;
  let height = 0;
  let exportDataUrl = dataUrl;
  let format: 'PNG' | 'JPEG' = 'PNG';

  if (typeof createImageBitmap === 'function') {
    const bitmap = await createImageBitmap(blob);
    width = bitmap.width;
    height = bitmap.height;
    const canvas = document.createElement('canvas');
    canvas.width = width;
    canvas.height = height;
    const ctx = canvas.getContext('2d');
    if (!ctx) {
      bitmap.close();
      throw new Error('Failed to load export image');
    }
    ctx.drawImage(bitmap, 0, 0);
    bitmap.close();
    // Large captures: JPEG is more reliable for jsPDF than multi‑MB PNG data URLs
    const large =
      Math.max(width, height) > PDF_IMAGE_LIMITS.largeEdgePx ||
      dataUrl.length > PDF_IMAGE_LIMITS.largeDataUrlChars;
    if (large) {
      exportDataUrl = canvas.toDataURL('image/jpeg', PDF_IMAGE_LIMITS.jpegQuality);
      format = 'JPEG';
    } else {
      exportDataUrl = canvas.toDataURL('image/png');
      format = 'PNG';
    }
  } else {
    const image = await loadImage(dataUrl);
    width = image.naturalWidth || image.width;
    height = image.naturalHeight || image.height;
  }

  if (width <= 0 || height <= 0) {
    throw new Error('Export image has no dimensions');
  }

  return { width, height, exportDataUrl, format };
}

/** Download a one-page PDF from a PNG data URL (peer dep: jspdf). */
export async function downloadPdfFromPng(dataUrl: string, filename: string): Promise<void> {
  const { jsPDF } = await import('jspdf');

  let decoded: Awaited<ReturnType<typeof decodePngDataUrl>>;
  try {
    decoded = await decodePngDataUrl(dataUrl);
  } catch {
    // Last resort: give the user a PNG instead of a dead-end error (MOOD-0356).
    downloadDataUrl(dataUrl, `${filename}.png`);
    throw new Error('PDF encode failed — downloaded PNG instead. Try a lower resolution.');
  }

  const { width: imgWidth, height: imgHeight, exportDataUrl, format } = decoded;

  const orientation = imgWidth >= imgHeight ? 'landscape' : 'portrait';
  const doc = new jsPDF({ orientation, unit: 'pt', format: 'a4' });
  const pageWidth = doc.internal.pageSize.getWidth();
  const pageHeight = doc.internal.pageSize.getHeight();
  const margin = 36;
  const maxWidth = pageWidth - margin * 2;
  const maxHeight = pageHeight - margin * 2;
  const scale = Math.min(maxWidth / imgWidth, maxHeight / imgHeight);
  const width = imgWidth * scale;
  const height = imgHeight * scale;
  const x = (pageWidth - width) / 2;
  const y = (pageHeight - height) / 2;

  doc.addImage(exportDataUrl, format, x, y, width, height);
  const pdfBytes = doc.output('arraybuffer');
  downloadBlob(new Blob([pdfBytes], { type: 'application/pdf' }), `${filename}.pdf`);
}

export function sanitizeFilename(name: string): string {
  return (
    name
      .replace(/[^\w\-]+/g, '-')
      .replace(/-+/g, '-')
      .slice(0, 80) || 'board'
  );
}
