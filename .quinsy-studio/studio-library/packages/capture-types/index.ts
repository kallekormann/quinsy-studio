/** Shared capture payload types for extension ↔ web (MOOD-0093+). */

export type CaptureCssMeta = {
  color?: string;
  backgroundColor?: string;
  fontFamily?: string;
  fontSize?: string;
  fontWeight?: string;
  borderRadius?: string;
  boxShadow?: string;
};

export type CaptureBoundingRect = {
  x: number;
  y: number;
  width: number;
  height: number;
};

export type CapturePayload = {
  version: 1;
  capturedAt: string;
  pageUrl: string;
  pageTitle: string;
  tagName: string;
  boundingRect: CaptureBoundingRect;
  /** Window devicePixelRatio at capture time (for screenshot crop). */
  devicePixelRatio: number;
  css: CaptureCssMeta;
  screenshotDataUrl?: string;
  notes?: string;
  /** Auto-tags from capture heuristics / worker (MOOD-0096). */
  tags?: string[];
};

/** Local-first inbox row (extension IDB + web Dexie sync). */
export type InboxItemRecord = {
  id: string;
  createdAt: number;
  /** Set after cloud sync (MOOD-0095). */
  syncedAt?: number | null;
  pageUrl: string;
  pageTitle: string;
  tagName: string;
  cssJson: string;
  boundingRectJson: string;
  mimeType: string;
  width: number;
  height: number;
  /** WebP (or PNG fallback) bytes. */
  screenshot: Blob;
  /** JSON string[] auto-tags (MOOD-0096). */
  tagsJson?: string;
};

export const CAPTURE_MESSAGE = {
  TOGGLE: 'moody:toggle-capture',
  GET_ARMED: 'moody:get-armed',
  SET_ARMED: 'moody:set-armed',
  CAPTURED: 'moody:captured',
  PING: 'moody:ping',
  PONG: 'moody:pong',
  INBOX_SAVED: 'moody:inbox-saved',
} as const;

export type CaptureMessageType = (typeof CAPTURE_MESSAGE)[keyof typeof CAPTURE_MESSAGE];
