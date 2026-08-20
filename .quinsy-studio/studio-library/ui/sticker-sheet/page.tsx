/**
 * Studio Library sticker sheet — generic component inventory reference.
 * Not copied from projects; lists studio-owned artifacts only.
 */
import { Badge } from '../components/badge/Badge';
import { Button } from '../components/button/Button';
import { ChecklistItem } from '../components/checklist-item/ChecklistItem';
import { CheckIcon, SparkIcon } from '../components/icon/Icon';
import { InlineForm } from '../components/inline-form/InlineForm';
import { Input } from '../components/input/Input';
import { PageShell } from '../components/pageshell/PageShell';

export default function StudioStickerSheet() {
  return (
    <PageShell title="Studio Library — Sticker Sheet">
      <div className="space-y-10">
        <section>
          <h2 className="mb-3 text-lg font-semibold text-neutral-900">Surfaces</h2>
          <div className="flex gap-3">
            <div className="h-16 w-24 rounded-lg border border-neutral-200 bg-surface shadow-sm" />
            <div className="h-16 w-24 rounded-lg bg-surface-muted" />
            <div className="h-16 w-24 rounded-lg bg-primary-100" />
          </div>
        </section>

        <section>
          <h2 className="mb-3 text-lg font-semibold">Buttons</h2>
          <div className="flex flex-wrap gap-2">
            <Button variant="primary">Primary</Button>
            <Button variant="secondary">Secondary</Button>
            <Button variant="outline">Outline</Button>
            <Button variant="ghost">Ghost</Button>
          </div>
        </section>

        <section>
          <h2 className="mb-3 text-lg font-semibold">Badges & icons</h2>
          <div className="flex items-center gap-3">
            <Badge>Default</Badge>
            <Badge variant="primary">Primary</Badge>
            <CheckIcon className="text-primary-600" />
            <SparkIcon className="text-primary-600" />
          </div>
        </section>

        <section>
          <h2 className="mb-3 text-lg font-semibold">Form</h2>
          <Input label="Sample" placeholder="Placeholder text" />
          <div className="mt-4">
            <InlineForm submitLabel="Add" />
          </div>
        </section>

        <section>
          <h2 className="mb-3 text-lg font-semibold">Checklist item</h2>
          <ChecklistItem label="Example row" meta="Metadata line" />
        </section>
      </div>
    </PageShell>
  );
}
