/** Options for dominant-color palette extraction (browser or test). */
export type ExtractPaletteOptions = {
  /** Downsample edge length when rasterizing (default 64). */
  size?: number;
  /** Number of HEX swatches to return (default 5). */
  count?: number;
  /** Pixel stride when sampling RGBA buffer (default 1). */
  sampleStride?: number;
  /** RGB quantize bucket size 1–255 (default 32). */
  quantizeStep?: number;
  /** Minimum alpha 0–255 to include pixel (default 128). */
  minAlpha?: number;
  /** Fill palette when image has fewer distinct colors. */
  fallback?: string[];
};

export type ResolvedExtractPaletteOptions = {
  size: number;
  count: number;
  sampleStride: number;
  quantizeStep: number;
  minAlpha: number;
  fallback: string[];
};

export const DEFAULT_FALLBACK_PALETTE = [
  '#2D3142',
  '#4F5D75',
  '#BFC0C0',
  '#FFFFFF',
  '#EF8354',
] as const;
