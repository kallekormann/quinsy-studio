import { Avatar, AvatarFallback, AvatarImage } from '../avatar';

export type AvatarStackPerson = {
  id: string;
  initials: string;
  title: string;
  imageUrl?: string;
  isYou?: boolean;
  onClick?: () => void;
};

export type AvatarStackProps = {
  people: AvatarStackPerson[];
  maxVisible?: number;
  'aria-label'?: string;
  className?: string;
  size?: 'sm' | 'md';
};

const FILLS = [
  'bg-[var(--accent)] text-[var(--on-accent)]',
  'bg-[var(--rhodes)] text-[var(--on-rhodes)]',
  'bg-[var(--accent-bright)] text-[var(--on-accent)]',
] as const;

function AvatarBubble({
  person,
  index,
  overflowLabel,
}: {
  person: AvatarStackPerson;
  index: number;
  overflowLabel?: string;
}) {
  const isMore = Boolean(overflowLabel);
  const fill = FILLS[index % FILLS.length];

  return (
    <span className="relative -ml-2 inline-flex rounded-full ring-2 ring-surface first:ml-0" role="listitem" title={person.title}>
      <Avatar className="size-7">
        {!isMore && person.imageUrl ? <AvatarImage src={person.imageUrl} alt="" /> : null}
        <AvatarFallback className={isMore ? 'bg-surface-raised text-xs text-ink' : fill}>
          {isMore ? overflowLabel : person.initials}
        </AvatarFallback>
      </Avatar>
    </span>
  );
}

export function AvatarStack({
  people,
  maxVisible = 4,
  'aria-label': ariaLabel = 'People',
  className = '',
}: AvatarStackProps) {
  if (people.length < 1) return null;
  const visible = people.slice(0, maxVisible);
  const overflow = people.length - maxVisible;

  return (
    <div role="list" aria-label={ariaLabel} className={`inline-flex items-center ${className}`}>
      {visible.map((person, index) => (
        <AvatarBubble key={person.id} person={person} index={index} />
      ))}
      {overflow > 0 ? (
        <AvatarBubble
          person={{ id: '__more', initials: '', title: `${overflow} more` }}
          index={visible.length}
          overflowLabel={`+${overflow}`}
        />
      ) : null}
    </div>
  );
}
