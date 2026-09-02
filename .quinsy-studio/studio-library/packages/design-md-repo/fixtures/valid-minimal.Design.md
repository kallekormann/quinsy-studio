---
schema_version: '1.0'
id: moody-bloom-fixture
name: Moody Bloom Fixture
description: Minimal valid Design.md for validator tests
style_dna_affinity:
  - Soft
  - Warm
token_hooks:
  color_primitives:
    - brand
    - gray
  color_semantic:
    - bg.canvas
    - bg.surface-primary
    - text.primary
    - brand.primary
  spacing:
    - xs
    - sm
    - md
    - lg
  radius:
    - sm
    - md
    - lg
    - full
spacing_px:
  xs: 8
  sm: 12
  md: 16
  lg: 24
radius_px:
  sm: 4
  md: 8
  lg: 12
  full: 9999
typography:
  Display/Hero-Large:
    size: 56
    lineHeight: 1.1
    weight: Bold
  Heading/H1:
    size: 32
    lineHeight: 1.3
    weight: Bold
  Heading/H2:
    size: 24
    lineHeight: 1.3
    weight: SemiBold
  Heading/H3:
    size: 20
    lineHeight: 1.4
    weight: SemiBold
  Body/Regular:
    size: 16
    lineHeight: 1.5
    weight: Regular
  Utility/Caption:
    size: 12
    lineHeight: 1.4
    weight: Regular
layout:
  whitespace_bias: generous
  asymmetry:
    enabled: false
    recipes: []
  color_distribution:
    tone: 0.6
    structure: 0.3
    accent: 0.1
  borders:
    default: none
    width_token: null
  shadows:
    default: soft
  corners:
    bias: rounded
components:
  button_radius_token: md
  card_padding_token: md
  card_border: false
modes:
  light_dark: variable_modes
---

# Narrative

Fixture only — not a shipping core.
