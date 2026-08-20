/** Minimal shape for tag storage in `contentJson.tags`. */
export type TaggedContentJson = {
  tags?: string[];
};

export type TagContentCarrier = {
  contentJson: string;
};
