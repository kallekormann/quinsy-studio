/**
 * Studio Library — generic SVG icons (no emoji).
 */
import type { SVGProps } from 'react';

export type IconProps = SVGProps<SVGSVGElement> & {
  size?: number;
};

function iconProps({ size = 16, className = '', ...props }: IconProps) {
  return {
    width: size,
    height: size,
    viewBox: '0 0 24 24',
    fill: 'none',
    xmlns: 'http://www.w3.org/2000/svg',
    className,
    'aria-hidden': true as const,
    ...props,
  };
}

export function CheckIcon(props: IconProps) {
  return (
    <svg {...iconProps(props)}>
      <path
        d="M5 13l4 4L19 7"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

export function PlusIcon(props: IconProps) {
  return (
    <svg {...iconProps(props)}>
      <path d="M12 5v14M5 12h14" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
    </svg>
  );
}

export function SparkIcon(props: IconProps) {
  return (
    <svg {...iconProps(props)}>
      <path
        d="M12 3v3M12 18v3M3 12h3M18 12h3M6.3 6.3l2.1 2.1M15.6 15.6l2.1 2.1M6.3 17.7l2.1-2.1M15.6 8.4l2.1-2.1"
        stroke="currentColor"
        strokeWidth="1.75"
        strokeLinecap="round"
      />
      <circle cx="12" cy="12" r="2.25" fill="currentColor" />
    </svg>
  );
}
