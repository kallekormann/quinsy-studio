/**
 * Kit-token Dropdown — Headless Listbox (not native OS chrome).
 * Paint via kit CSS variables so any brand restyles the same component.
 */
"use client";

import { useId, type ReactNode } from "react";
import {
  Listbox,
  ListboxButton,
  ListboxOption,
  ListboxOptions,
} from "@ui/primitives/headless/listbox";
import { ChevronDownIcon } from "@ui/components/atoms/Icon";

export type DropdownOption<T extends string | number = string> = {
  value: T;
  label: ReactNode;
  disabled?: boolean;
};

export type DropdownProps<T extends string | number = string> = {
  value: T;
  onChange: (value: T) => void;
  options: DropdownOption<T>[];
  label?: ReactNode;
  disabled?: boolean;
  className?: string;
  buttonClassName?: string;
  "aria-label"?: string;
};

const labelClassName =
  "mb-1 block text-[11px] font-medium uppercase leading-none tracking-[0.1em] text-[color:var(--color-muted,var(--color-text-muted))] font-[family-name:var(--font-ui,var(--font-sans))]";

const buttonClass =
  "relative flex h-[34px] w-full items-center justify-between gap-2 rounded-md border border-[color:var(--color-border)] bg-[color:var(--color-background,var(--color-surface))] px-3 text-left text-sm text-[color:var(--color-foreground,var(--color-text))] font-[family-name:var(--font-ui,var(--font-sans))] transition-[border-color,background-color] hover:bg-[color:var(--color-surface-muted,var(--color-surface))] focus-visible:border-[color:var(--color-accent,var(--color-primary-500))] focus-visible:outline-none data-[open]:border-[color:var(--color-accent,var(--color-primary-500))] disabled:cursor-not-allowed disabled:opacity-45";

const panelClass =
  "z-[9999] mt-1 max-h-60 w-[var(--button-width)] overflow-auto rounded-md border border-[color:var(--color-border)] bg-[color:var(--color-background,var(--color-surface))] py-1 shadow-md font-[family-name:var(--font-ui,var(--font-sans))]";

function optionClass(focus: boolean, selected: boolean, disabled?: boolean) {
  return [
    "flex w-full cursor-default px-2.5 py-2 text-left text-sm text-[color:var(--color-foreground,var(--color-text))]",
    disabled ? "opacity-40" : "",
    focus
      ? "bg-[color:var(--color-surface-muted,var(--color-neutral-100))]"
      : "",
    selected
      ? "font-medium text-[color:var(--color-accent,var(--color-primary-500))]"
      : "",
  ]
    .filter(Boolean)
    .join(" ");
}

export function Dropdown<T extends string | number = string>({
  value,
  onChange,
  options,
  label,
  disabled = false,
  className = "",
  buttonClassName = "",
  "aria-label": ariaLabel,
}: DropdownProps<T>) {
  const labelId = useId();
  const selected = options.find((opt) => opt.value === value) ?? options[0];

  return (
    <div className={`w-full ${className}`}>
      {label ? (
        <span id={labelId} className={labelClassName}>
          {label}
        </span>
      ) : null}
      <Listbox value={value} onChange={onChange} disabled={disabled}>
        <ListboxButton
          className={`${buttonClass} ${buttonClassName}`}
          aria-label={ariaLabel}
          aria-labelledby={label ? labelId : undefined}
        >
          <span className="truncate">{selected?.label ?? "Select…"}</span>
          <ChevronDownIcon
            size={16}
            className="shrink-0 text-[color:var(--color-muted,var(--color-text-muted))]"
            aria-hidden
          />
        </ListboxButton>
        <ListboxOptions portal anchor="bottom start" className={panelClass}>
          {options.map((opt) => (
            <ListboxOption
              key={String(opt.value)}
              value={opt.value}
              disabled={opt.disabled}
              className={({ focus, selected: isSelected }) =>
                optionClass(focus, isSelected, opt.disabled)
              }
            >
              {opt.label}
            </ListboxOption>
          ))}
        </ListboxOptions>
      </Listbox>
    </div>
  );
}
