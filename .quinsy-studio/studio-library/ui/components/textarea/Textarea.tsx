/**
 * Moody Bloom — styled textarea (Headless UI + tokens).
 */
'use client';

import type { ComponentProps } from 'react';
import { Textarea as HeadlessTextarea } from '@ui/primitives/headless/textarea';
import {
  fieldClassName,
  fieldErrorClassName,
  fieldHintClassName,
  fieldLabelClassName,
} from '../atoms/field-styles';

export interface TextareaProps extends ComponentProps<typeof HeadlessTextarea> {
  label?: string;
  hint?: string;
  error?: string;
}

export function Textarea({
  label,
  hint,
  error,
  className = '',
  id,
  'aria-invalid': ariaInvalid,
  ...props
}: TextareaProps) {
  const inputId = id || 'textarea';
  const invalid = ariaInvalid ?? (error ? true : undefined);

  return (
    <div className="w-full">
      {label ? (
        <label htmlFor={inputId} className={fieldLabelClassName}>
          {label}
        </label>
      ) : null}
      <HeadlessTextarea
        id={inputId}
        aria-invalid={invalid}
        className={`${fieldClassName} min-h-[72px] resize-y leading-snug ${className}`}
        {...props}
      />
      {error ? <span className={fieldErrorClassName}>{error}</span> : null}
      {!error && hint ? <span className={fieldHintClassName}>{hint}</span> : null}
    </div>
  );
}
