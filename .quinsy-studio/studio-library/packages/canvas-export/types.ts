/** Minimal canvas item for Konva bounds/export (map from your board model). */
export type CanvasExportItem = {
  id: string;
  type: string;
  x: number;
  y: number;
  width: number;
  height: number;
  contentJson: string;
};

export type ExportRect = { x: number; y: number; width: number; height: number };

export type BoundsOptions = {
  /** Extra height below image items (palette strip, captions). */
  imageExtraHeight?: (item: CanvasExportItem) => number;
};

export type StageCaptureOptions = {
  bounds: ExportRect;
  pixelRatio?: number;
  padding?: number;
};
