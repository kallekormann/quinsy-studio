import { dataUrlToUint8Array } from './canvas-export';

/** Neutral fallback. Products pass their own name as `text`. */
export const DEFAULT_WATERMARK_TEXT = 'Preview';

export type WatermarkOptions = {
  text?: string;
  opacity?: number;
  marginPx?: number;
  /** When true, returns input unchanged (Pro users). */
  skip?: boolean;
};

export type WatermarkLayout = {
  x: number;
  y: number;
  fontSize: number;
  text: string;
  opacity: number;
  pillWidth: number;
  pillHeight: number;
};

const WATERMARK_LAYOUT = {
  opacity: 0.88,
  marginPx: 28,
  fontScale: 0.028,
  minFontPx: 14,
  pillPaddingX: 10,
  pillPaddingY: 6,
  pillRadius: 6,
} as const;

export function watermarkLayout(
  imageWidth: number,
  imageHeight: number,
  options: WatermarkOptions = {},
): WatermarkLayout {
  const text = options.text ?? DEFAULT_WATERMARK_TEXT;
  const opacity = options.opacity ?? WATERMARK_LAYOUT.opacity;
  const marginPx = options.marginPx ?? WATERMARK_LAYOUT.marginPx;
  const fontSize = Math.max(
    WATERMARK_LAYOUT.minFontPx,
    Math.round(Math.min(imageWidth, imageHeight) * WATERMARK_LAYOUT.fontScale),
  );
  const pillWidth = text.length * fontSize * 0.58 + WATERMARK_LAYOUT.pillPaddingX * 2;
  const pillHeight = fontSize + WATERMARK_LAYOUT.pillPaddingY * 2;

  return {
    x: imageWidth - marginPx,
    y: imageHeight - marginPx,
    fontSize,
    text,
    opacity,
    pillWidth,
    pillHeight,
  };
}

type WatermarkCanvasContext = Pick<
  CanvasRenderingContext2D,
  | 'fillText'
  | 'font'
  | 'globalAlpha'
  | 'fillStyle'
  | 'textAlign'
  | 'textBaseline'
  | 'roundRect'
  | 'shadowColor'
  | 'shadowBlur'
  | 'beginPath'
  | 'fill'
>;

export function drawWatermarkOnCanvas(
  ctx: WatermarkCanvasContext,
  imageWidth: number,
  imageHeight: number,
  options?: WatermarkOptions,
): void {
  const layout = watermarkLayout(imageWidth, imageHeight, options);
  const pillX = layout.x - layout.pillWidth;
  const pillY = layout.y - layout.pillHeight;

  ctx.textAlign = 'right';
  ctx.textBaseline = 'bottom';
  ctx.font = `600 ${layout.fontSize}px system-ui, -apple-system, sans-serif`;

  if (typeof ctx.roundRect === 'function') {
    ctx.globalAlpha = 0.82;
    ctx.fillStyle = 'rgba(255, 255, 255, 0.88)';
    ctx.beginPath();
    ctx.roundRect(pillX, pillY, layout.pillWidth, layout.pillHeight, WATERMARK_LAYOUT.pillRadius);
    ctx.fill();
  }

  ctx.shadowColor = 'rgba(0, 0, 0, 0.22)';
  ctx.shadowBlur = 3;
  ctx.globalAlpha = layout.opacity;
  ctx.fillStyle = '#171717';
  ctx.fillText(
    layout.text,
    layout.x - WATERMARK_LAYOUT.pillPaddingX,
    layout.y - WATERMARK_LAYOUT.pillPaddingY,
  );
}

async function decodeExportImage(
  dataUrl: string,
): Promise<{ width: number; height: number; draw: (ctx: CanvasRenderingContext2D) => void }> {
  // Decode via atob — fetch(dataUrl) fails on large Konva captures.
  if (dataUrl.startsWith('data:') && typeof createImageBitmap === 'function') {
    const { bytes, mime } = dataUrlToUint8Array(dataUrl);
    const copy = new Uint8Array(bytes.byteLength);
    copy.set(bytes);
    const bitmap = await createImageBitmap(new Blob([copy], { type: mime }));
    return {
      width: bitmap.width,
      height: bitmap.height,
      draw: (ctx) => {
        ctx.drawImage(bitmap, 0, 0);
        bitmap.close();
      },
    };
  }

  const image = await new Promise<HTMLImageElement>((resolve, reject) => {
    const el = new Image();
    el.onload = () => resolve(el);
    el.onerror = () => reject(new Error('Failed to load export image for watermark'));
    el.src = dataUrl;
  });
  const width = image.naturalWidth || image.width;
  const height = image.naturalHeight || image.height;
  return {
    width,
    height,
    draw: (ctx) => ctx.drawImage(image, 0, 0),
  };
}

/** Applies a bottom-right brand watermark to a PNG data URL. Skips when `skip` is true. */
export async function applyWatermark(
  dataUrl: string,
  options: WatermarkOptions = {},
): Promise<string> {
  if (options.skip) {
    return dataUrl;
  }

  if (!dataUrl || !dataUrl.startsWith('data:image/')) {
    return dataUrl;
  }

  try {
    const decoded = await decodeExportImage(dataUrl);
    const width = decoded.width;
    const height = decoded.height;
    if (width <= 0 || height <= 0) {
      return dataUrl;
    }

    const canvas = document.createElement('canvas');
    canvas.width = width;
    canvas.height = height;
    const ctx = canvas.getContext('2d');
    if (!ctx) {
      return dataUrl;
    }

    decoded.draw(ctx);
    drawWatermarkOnCanvas(ctx, width, height, options);
    return canvas.toDataURL('image/png');
  } catch {
    // Never block Export PDF/PNG on watermark decode failure.
    return dataUrl;
  }
}
