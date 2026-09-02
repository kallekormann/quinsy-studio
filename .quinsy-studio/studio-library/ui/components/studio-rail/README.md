# StudioRail

Reusable **right-rail dock** organism: narrow **icon rail navigation** + **detail panel** that opens for the active peer (inspect / inbox / library / export / tools). Solid `bg-chrome`; exclusive peer panels.

Prefer this composition whenever a SaaS or canvas product needs tools beside the stage — see LO-0040 (component reuse ladder) and `saas-application` UX options in `process/project-archetypes.md`.

## Usage

```tsx
import { StudioDock, type StudioPeerId } from '@ui/components/studio-rail';
import {
  InspectorIcon,
  InboxIcon,
  LibraryIcon,
  ExportIcon,
  BrandKitIcon,
} from '@ui/components/atoms/Icon';

const [activePeer, setActivePeer] = useState<StudioPeerId | null>(null);

<StudioDock
  items={[
    { id: 'inspector', label: 'Inspector', icon: <InspectorIcon size={18} /> },
    { id: 'inbox', label: 'Inbox', icon: <InboxIcon size={18} />, badge: <Badge>3</Badge> },
    { id: 'library', label: 'Library', icon: <LibraryIcon size={18} /> },
    { id: 'export', label: 'Export', icon: <ExportIcon size={18} /> },
    { id: 'brand-kit', label: 'Brand kit', icon: <BrandKitIcon size={18} /> },
  ]}
  activePeer={activePeer}
  onPeerChange={setActivePeer}
  panelTitle="Inspector"
>
  {activePeer === 'inspector' ? <InspectorContent /> : null}
</StudioDock>;
```

| Export        | Notes                                          |
| ------------- | ---------------------------------------------- |
| `StudioRail`  | Icon column only                               |
| `StudioPanel` | Panel shell (title + scroll body)              |
| `StudioDock`  | Panel + rail; panel hidden when `activePeer` is `null` |

Peer ids are product-specific — pass your own `items` / content. Map widgets (or similar floats) are **not** rail peers by default; keep them outside the dock.
