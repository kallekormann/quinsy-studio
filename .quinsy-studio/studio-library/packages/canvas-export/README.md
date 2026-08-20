# Canvas export

Konva stage capture → PNG/PDF download. Generic bounds helpers for boards with images, notes, and frames.

## Pull

```bash
./studio library pull <project> canvas-export
```

## Peer dependencies

- `konva` + `react-konva` (stage ref)
- `jspdf` (PDF download only)

## Usage

```typescript
import {
  boundsForItems,
  captureStageToPng,
  downloadDataUrl,
  downloadPdfFromPng,
} from '@/packages/canvas-export';

const bounds = boundsForItems(items);
const png = captureStageToPng(stage, { bounds });
downloadDataUrl(png, 'board.png');
await downloadPdfFromPng(png, 'board');
```

Expose `stageRef` from your canvas via `forwardRef` + `useImperativeHandle`.
