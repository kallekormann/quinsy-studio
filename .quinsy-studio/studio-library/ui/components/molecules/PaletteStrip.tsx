const MOCK_PALETTES = [
  ['#2D3142', '#4F5D75', '#BFC0C0', '#FFFFFF', '#EF8354'],
  ['#1B4332', '#40916C', '#95D5B2', '#D8F3DC', '#F4A261'],
  ['#3D348B', '#7678ED', '#F7B801', '#F18701', '#F35B04'],
];

export function PaletteStrip({
  colors = MOCK_PALETTES[0],
  className = '',
}: {
  colors?: string[];
  className?: string;
}) {
  return (
    <div className={`flex overflow-hidden rounded-md shadow-sm ${className}`}>
      {colors.map((hex) => (
        <div
          key={hex}
          className="h-3 w-6 first:rounded-l-md last:rounded-r-md"
          style={{ backgroundColor: hex }}
          title={hex}
        />
      ))}
    </div>
  );
}

export function PaletteStripDemo() {
  return (
    <div className="space-y-2">
      {MOCK_PALETTES.map((palette, i) => (
        <PaletteStrip key={i} colors={palette} />
      ))}
    </div>
  );
}
