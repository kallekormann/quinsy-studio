import type { ExtractPaletteOptions, ResolvedExtractPaletteOptions } from './types';
import { DEFAULT_FALLBACK_PALETTE } from './types';

export function resolveExtractPaletteOptions(
  options: ExtractPaletteOptions = {},
): ResolvedExtractPaletteOptions {
  return {
    size: options.size ?? 64,
    count: options.count ?? 5,
    sampleStride: options.sampleStride ?? 1,
    quantizeStep: options.quantizeStep ?? 32,
    minAlpha: options.minAlpha ?? 128,
    fallback: options.fallback ?? [...DEFAULT_FALLBACK_PALETTE],
  };
}

function rgbToHex(r: number, g: number, b: number): string {
  const toHex = (n: number) => n.toString(16).padStart(2, '0').toUpperCase();
  return `#${toHex(r)}${toHex(g)}${toHex(b)}`;
}

/** Rank dominant colors from raw RGBA pixel data (works in Node tests + browser). */
export function extractPaletteFromPixels(
  data: Uint8ClampedArray,
  options?: ExtractPaletteOptions,
): string[] {
  const opts = resolveExtractPaletteOptions(options);
  const buckets = new Map<string, number>();
  const step = Math.max(1, opts.quantizeStep);

  for (let i = 0; i < data.length; i += 4 * opts.sampleStride) {
    const alpha = data[i + 3];
    if (alpha < opts.minAlpha) continue;

    const r = Math.round(data[i] / step) * step;
    const g = Math.round(data[i + 1] / step) * step;
    const b = Math.round(data[i + 2] / step) * step;
    const hex = rgbToHex(Math.min(255, r), Math.min(255, g), Math.min(255, b));
    buckets.set(hex, (buckets.get(hex) ?? 0) + 1);
  }

  const ranked = [...buckets.entries()]
    .sort((a, b) => b[1] - a[1])
    .map(([hex]) => hex);

  const palette: string[] = [];
  for (const hex of ranked) {
    if (palette.includes(hex)) continue;
    palette.push(hex);
    if (palette.length >= opts.count) break;
  }

  for (const fallback of opts.fallback) {
    if (palette.length >= opts.count) break;
    if (!palette.includes(fallback)) palette.push(fallback);
  }

  return palette.slice(0, opts.count);
}

export function extractPaletteFromImageData(
  imageData: ImageData,
  options?: ExtractPaletteOptions,
): string[] {
  return extractPaletteFromPixels(imageData.data, options);
}

async function rasterizeToImageData(
  source: CanvasImageSource,
  options: ResolvedExtractPaletteOptions,
): Promise<ImageData | null> {
  if (typeof document === 'undefined') {
    return null;
  }

  const canvas = document.createElement('canvas');
  canvas.width = options.size;
  canvas.height = options.size;
  const ctx = canvas.getContext('2d');
  if (!ctx) return null;

  ctx.drawImage(source, 0, 0, options.size, options.size);
  return ctx.getImageData(0, 0, options.size, options.size);
}

/** Extract palette from any blob with an image MIME type (browser). */
export async function extractPaletteFromBlob(
  blob: Blob,
  options?: ExtractPaletteOptions,
): Promise<string[]> {
  const opts = resolveExtractPaletteOptions(options);
  if (typeof document === 'undefined' || !blob.type.startsWith('image/')) {
    return opts.fallback.slice(0, opts.count);
  }

  const bitmap = await createImageBitmap(blob);
  const imageData = await rasterizeToImageData(bitmap, opts);
  bitmap.close();

  return imageData
    ? extractPaletteFromImageData(imageData, options)
    : opts.fallback.slice(0, opts.count);
}

/** Extract palette from a File input (browser). */
export async function extractPaletteFromFile(
  file: File,
  options?: ExtractPaletteOptions,
): Promise<string[]> {
  return extractPaletteFromBlob(file, options);
}
