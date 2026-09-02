import { forwardRef, type ComponentProps } from 'react';
import { fieldClassName } from './field-styles';

/** True when caller sets an explicit width utility (hub filter is 220px fixed). */
function hasExplicitWidth(className: string): boolean {
  return /(?:^|\s)(?:!)?(?:w-|min-w-|max-w-|basis-)/.test(className);
}

export const Input = forwardRef<HTMLInputElement, ComponentProps<'input'>>(function Input(
  { className = '', ...props },
  ref,
) {
  const widthClass = hasExplicitWidth(className) ? '' : 'w-full';
  return <input ref={ref} className={`${fieldClassName} ${widthClass} ${className}`} {...props} />;
});
