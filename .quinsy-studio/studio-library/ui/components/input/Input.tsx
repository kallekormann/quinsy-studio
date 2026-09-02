/**
 * Moody Bloom — generic text input with optional label, hint, and error.
 */
import type { ComponentProps } from 'react';
import { Input as BaseInput } from '../atoms/Input';
import {
  fieldErrorClassName,
  fieldHintClassName,
  fieldLabelClassName,
} from '../atoms/field-styles';

export interface InputProps extends ComponentProps<'input'> {
  label?: string;
  hint?: string;
  error?: string;
}

export function Input({
  label,
  hint,
  error,
  className = '',
  id,
  'aria-invalid': ariaInvalid,
  ...props
}: InputProps) {
  const inputId = id || 'input';
  const invalid = ariaInvalid ?? (error ? true : undefined);

  return (
    <div className="w-full">
      {label ? (
        <label htmlFor={inputId} className={fieldLabelClassName}>
          {label}
        </label>
      ) : null}
      <BaseInput id={inputId} aria-invalid={invalid} className={className} {...props} />
      {error ? <span className={fieldErrorClassName}>{error}</span> : null}
      {!error && hint ? <span className={fieldHintClassName}>{hint}</span> : null}
    </div>
  );
}
