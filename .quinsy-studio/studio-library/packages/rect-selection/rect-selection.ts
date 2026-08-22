export type Rect = {
  x: number;
  y: number;
  width: number;
  height: number;
};

export type BoundedItem = {
  id: string;
  x: number;
  y: number;
  width: number;
  height: number;
  type?: string;
};

export function normalizeRect(rect: Rect): Rect {
  const width = rect.width;
  const height = rect.height;
  return {
    x: width < 0 ? rect.x + width : rect.x,
    y: height < 0 ? rect.y + height : rect.y,
    width: Math.abs(width),
    height: Math.abs(height),
  };
}

function rectsIntersect(a: Rect, b: Rect): boolean {
  return a.x < b.x + b.width && a.x + a.width > b.x && a.y < b.y + b.height && a.y + a.height > b.y;
}

export function boundsFromItem(item: BoundedItem): Rect {
  return {
    x: item.x,
    y: item.y,
    width: item.width,
    height: item.height,
  };
}

/** Return item ids whose bounds intersect the marquee (canvas coordinates). */
export function itemsInMarquee(items: BoundedItem[], marquee: Rect): string[] {
  const box = normalizeRect(marquee);
  if (box.width < 1 && box.height < 1) {
    return [];
  }

  return items
    .filter((item) => item.type !== 'frame' || box.width > 4 || box.height > 4)
    .filter((item) => rectsIntersect(box, boundsFromItem(item)))
    .map((item) => item.id);
}
