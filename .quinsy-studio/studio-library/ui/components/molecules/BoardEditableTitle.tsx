'use client';

import { useEffect, useState } from 'react';
import { Input } from '@ui/components/atoms/Input';
import { inlineEditableInputClassName } from '@ui/components/molecules/inline-editable-input-styles';
import { chromePageTitleClass } from '@ui/styles/chrome-styles';

export function BoardEditableTitle({
  value,
  onCommit,
}: {
  value: string;
  onCommit: (nextTitle: string) => void;
}) {
  const [editing, setEditing] = useState(false);
  const [draft, setDraft] = useState(value);

  useEffect(() => {
    if (!editing) {
      setDraft(value);
    }
  }, [editing, value]);

  function commit() {
    setEditing(false);
    const next = draft.trim() || 'Untitled board';
    if (next !== value) {
      onCommit(next);
    }
  }

  if (editing) {
    return (
      <Input
        autoFocus
        value={draft}
        onChange={(event) => setDraft(event.target.value)}
        onBlur={commit}
        onKeyDown={(event) => {
          if (event.key === 'Enter') {
            event.preventDefault();
            commit();
          }
          if (event.key === 'Escape') {
            event.preventDefault();
            setDraft(value);
            setEditing(false);
          }
        }}
        className={inlineEditableInputClassName('max-w-[12rem] truncate sm:max-w-xs')}
        aria-label="Board title"
      />
    );
  }

  return (
    <button
      type="button"
      onClick={() => setEditing(true)}
      className={`hidden max-w-[12rem] text-left hover:text-accent-600 sm:inline sm:max-w-xs ${chromePageTitleClass}`}
      title="Rename board"
    >
      {value}
    </button>
  );
}
