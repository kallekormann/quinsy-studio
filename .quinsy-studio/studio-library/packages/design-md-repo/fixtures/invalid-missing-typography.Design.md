---
schema_version: '1.0'
id: missing-typography
name: Missing Typography Floor
token_hooks:
  color_primitives: [brand]
  color_semantic: [text.primary]
  spacing: [md]
  radius: [md]
spacing_px:
  md: 16
radius_px:
  md: 8
typography:
  Heading/H1:
    size: 32
    lineHeight: 1.3
    weight: Bold
layout:
  color_distribution:
    tone: 0.6
    structure: 0.3
    accent: 0.1
  borders:
    default: none
  shadows:
    default: none
  corners:
    bias: sharp
modes:
  light_dark: variable_modes
---
