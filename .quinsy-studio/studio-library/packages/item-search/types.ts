/** Generic canvas/board item for metadata search (adapt from your Dexie model). */
export type SearchableItem = {
  id: string;
  type: string;
  contentJson: string;
};

export type ItemSearchOptions = {
  /** Extra height below image items (palette bar, etc.). Default 0. */
  imageExtraHeight?: (item: SearchableItem) => number;
};
