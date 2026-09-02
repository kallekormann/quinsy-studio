import type { ReactNode } from 'react';

export type AvatarStackPerson = {
  id: string;
  /** Visible initials when no image */
  initials: string;
  title: string;
  imageUrl?: string;
  /** CSS background (gradient or solid) behind initials */
  background?: string;
  /** Presence ring color (editing / live) */
  ringColor?: string;
  isYou?: boolean;
  onClick?: () => void;
};

export type AvatarStackProps = {
  people: AvatarStackPerson[];
  /** Visible avatars before +N overflow (mock 13: 4 + remainder) */
  maxVisible?: number;
  'aria-label'?: string;
  className?: string;
  size?: 'sm' | 'md';
};

const SIZE_CLASS = {
  sm: 'h-6 w-6 text-[9px] border-[1.5px] -ml-1.5 first:ml-0',
  md: 'h-7 w-7 text-[10px] border-2 -ml-2 first:ml-0',
} as const;

function AvatarBubble({
  person,
  size,
  overflowLabel,
}: {
  person: AvatarStackPerson;
  size: 'sm' | 'md';
  overflowLabel?: string;
}) {
  const isMore = Boolean(overflowLabel);
  const Tag = person.onClick && !isMore ? 'button' : 'span';
  const ringInset = size === 'sm' ? '-inset-0.5' : '-inset-[3px]';

  const body: ReactNode = isMore ? (
    overflowLabel
  ) : person.imageUrl ? (
    // eslint-disable-next-line @next/next/no-img-element
    <img src={person.imageUrl} alt="" className="h-full w-full object-cover" />
  ) : (
    person.initials
  );

  return (
    <Tag
      type={Tag === 'button' ? 'button' : undefined}
      role="listitem"
      title={isMore ? overflowLabel : person.title}
      aria-label={isMore ? overflowLabel : person.title}
      onClick={person.onClick}
      className={`relative z-[1] grid shrink-0 place-items-center overflow-hidden rounded-full border-[color:var(--color-chrome)] font-semibold tracking-tight text-white transition-[opacity,box-shadow] hover:z-10 hover:opacity-90 focus-visible:z-10 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-1 focus-visible:outline-accent-500 dark:border-[color:var(--color-chrome)] ${SIZE_CLASS[size]} ${
        isMore
          ? 'bg-surface-2 font-semibold text-body dark:bg-neutral-800 dark:text-neutral-300'
          : ''
      } ${person.isYou && !isMore ? 'shadow-[0_0_0_1px_color-mix(in_srgb,var(--color-accent-500)_35%,transparent)]' : ''}`}
      style={!isMore && person.background ? { background: person.background } : undefined}
    >
      {!isMore && person.ringColor ? (
        <span
          className={`pointer-events-none absolute ${ringInset} rounded-full border-2 opacity-95`}
          style={{ borderColor: person.ringColor }}
          aria-hidden
        />
      ) : null}
      {body}
    </Tag>
  );
}

export function AvatarStack({
  people,
  maxVisible = 4,
  'aria-label': ariaLabel = 'Collaborators',
  className = '',
  size = 'md',
}: AvatarStackProps) {
  if (people.length < 1) return null;

  const visible = people.slice(0, maxVisible);
  const overflow = people.length - maxVisible;

  return (
    <div
      role="list"
      aria-label={ariaLabel}
      className={`inline-flex items-center pl-0.5 ${className}`}
    >
      {visible.map((person) => (
        <AvatarBubble key={person.id} person={person} size={size} />
      ))}
      {overflow > 0 ? (
        <AvatarBubble
          person={{ id: '__more', initials: '', title: `${overflow} more` }}
          size={size}
          overflowLabel={`+${overflow}`}
        />
      ) : null}
    </div>
  );
}

/** Sticker-sheet / story fixtures aligned to mock 13-collaboration.html */
export const AVATAR_STACK_DEMO_PEOPLE: AvatarStackPerson[] = [
  {
    id: 'you',
    initials: 'KA',
    title: 'You',
    background: 'linear-gradient(145deg, var(--color-accent-300), var(--color-accent-500))',
    isYou: true,
  },
  {
    id: 'alex',
    initials: 'AR',
    title: 'Alex Rivera · editing',
    background: 'linear-gradient(145deg, #60a5fa, #1d4ed8)',
    ringColor: '#3b82f6',
  },
  {
    id: 'sam',
    initials: 'SC',
    title: 'Sam Chen · viewing',
    background: 'linear-gradient(145deg, #34d399, #047857)',
    ringColor: '#10b981',
  },
  {
    id: 'jordan',
    initials: 'JL',
    title: 'Jordan Lee',
    background: 'linear-gradient(145deg, #fbbf24, #b45309)',
  },
  {
    id: 'morgan',
    initials: 'MO',
    title: 'Morgan Park',
    background: 'linear-gradient(145deg, #c084fc, #7c3aed)',
  },
  {
    id: 'taylor',
    initials: 'TR',
    title: 'Taylor Kim',
    background: 'linear-gradient(145deg, #f472b6, #db2777)',
  },
];
