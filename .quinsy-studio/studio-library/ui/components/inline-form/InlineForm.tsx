/**
 * Studio Library — inline label + input + submit button row.
 */
'use client';

import { Button } from '../button/Button';
import { Input } from '../input/Input';

export interface InlineFormProps {
  value?: string;
  onChange?: (value: string) => void;
  onSubmit?: () => void;
  placeholder?: string;
  submitLabel?: string;
  inputLabel?: string;
}

export function InlineForm({
  value = '',
  onChange,
  onSubmit,
  placeholder = 'Enter value…',
  submitLabel = 'Submit',
  inputLabel,
}: InlineFormProps) {
  return (
    <div className="flex gap-2">
      <Input
        label={inputLabel}
        value={value}
        onChange={(e) => onChange?.(e.target.value)}
        placeholder={placeholder}
        onKeyDown={(e) => e.key === 'Enter' && onSubmit?.()}
      />
      <Button onClick={onSubmit} className="shrink-0 self-end">
        {submitLabel}
      </Button>
    </div>
  );
}
