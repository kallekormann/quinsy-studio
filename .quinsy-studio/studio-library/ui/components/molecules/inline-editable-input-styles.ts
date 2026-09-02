/** Shared chrome for inline rename fields (board title, zone title). */
import { fieldClassName } from '../atoms/field-styles';

export function inlineEditableInputClassName(extra = ''): string {
  return [fieldClassName, 'rounded-md px-2 py-0.5 font-medium', extra].filter(Boolean).join(' ');
}
