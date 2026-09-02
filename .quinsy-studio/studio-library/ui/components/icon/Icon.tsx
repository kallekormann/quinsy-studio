/**
 * Moody icons — Lucide wrappers (do not invent custom SVG paths).
 * Same export names as before so call sites stay stable.
 */
'use client';

import type { LucideIcon, LucideProps } from 'lucide-react';
import {
  Briefcase,
  ChevronDown,
  ChevronUp,
  Download,
  Eye,
  EyeOff,
  Frame,
  GripVertical,
  Hand,
  Image,
  Inbox,
  Info,
  Library,
  Map,
  Maximize2,
  MoreHorizontal,
  MousePointer2,
  Plus,
  Presentation,
  ScanSearch,
  Search,
  Settings,
  Share,
  Shield,
  StickyNote,
  X,
  ZoomIn,
  ZoomOut,
} from 'lucide-react';

export type IconProps = {
  size?: number;
  className?: string;
  strokeWidth?: number;
  absoluteStrokeWidth?: boolean;
};

function LucideWrap(
  Icon: LucideIcon,
  { size = 20, className = '', strokeWidth = 2, ...rest }: IconProps & Omit<LucideProps, 'ref'>,
) {
  return <Icon size={size} className={className} strokeWidth={strokeWidth} aria-hidden {...rest} />;
}

export function PlusIcon(props: IconProps) {
  return LucideWrap(Plus, props);
}
export function ShareIcon(props: IconProps) {
  return LucideWrap(Share, props);
}
export function LibraryIcon(props: IconProps) {
  return LucideWrap(Library, props);
}
export function FrameIcon(props: IconProps) {
  return LucideWrap(Frame, props);
}
export function GripVerticalIcon(props: IconProps) {
  return LucideWrap(GripVertical, props);
}
export function ImageIcon(props: IconProps) {
  return LucideWrap(Image, props);
}
export function NoteIcon(props: IconProps) {
  return LucideWrap(StickyNote, props);
}
export function SettingsIcon(props: IconProps) {
  return LucideWrap(Settings, props);
}
/** Generic zoom affordance — prefer ZoomIn/Out/Fit for specific actions */
export function ZoomIcon(props: IconProps) {
  return LucideWrap(ScanSearch, props);
}
export function ExportIcon(props: IconProps) {
  return LucideWrap(Download, props);
}
export function SearchIcon(props: IconProps) {
  return LucideWrap(Search, props);
}
export function ZoomOutIcon(props: IconProps) {
  return LucideWrap(ZoomOut, props);
}
export function ZoomInIcon(props: IconProps) {
  return LucideWrap(ZoomIn, props);
}
export function ZoomFitIcon(props: IconProps) {
  return LucideWrap(Maximize2, props);
}
export function HandPanIcon(props: IconProps) {
  return LucideWrap(Hand, props);
}
export function CursorSelectIcon(props: IconProps) {
  return LucideWrap(MousePointer2, props);
}
export function SelectCursorIcon(props: IconProps) {
  return LucideWrap(MousePointer2, props);
}
export function ScrollZoomIcon(props: IconProps) {
  return LucideWrap(ScanSearch, props);
}
export function InfoCircleIcon(props: IconProps) {
  return LucideWrap(Info, props);
}
export function ChevronDownIcon(props: IconProps) {
  return LucideWrap(ChevronDown, props);
}
export function ChevronUpIcon(props: IconProps) {
  return LucideWrap(ChevronUp, props);
}
export function PresentationDeckIcon(props: IconProps) {
  return LucideWrap(Presentation, props);
}
export function EyeIcon(props: IconProps) {
  return LucideWrap(Eye, props);
}
export function EyeOffIcon(props: IconProps) {
  return LucideWrap(EyeOff, props);
}
export function MapIcon(props: IconProps) {
  return LucideWrap(Map, props);
}
export function CloseIcon(props: IconProps) {
  return LucideWrap(X, props);
}
export function InboxIcon(props: IconProps) {
  return LucideWrap(Inbox, props);
}
/** Studio rail — selection metadata (MOOD-0430). */
export function InspectorIcon(props: IconProps) {
  return LucideWrap(Shield, props);
}
/** Studio rail — brand kit peer (MOOD-0430). */
export function BrandKitIcon(props: IconProps) {
  return LucideWrap(Briefcase, props);
}
/** Overflow / manage menus — use instead of “⋯” text glyphs */
export function MoreHorizontalIcon(props: IconProps) {
  return LucideWrap(MoreHorizontal, props);
}
