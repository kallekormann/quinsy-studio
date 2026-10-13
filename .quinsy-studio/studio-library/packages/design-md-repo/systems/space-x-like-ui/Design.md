---
schema_version: '1.0'
id: space-x-like-ui
name: SpaceX-like UI
description: Industrial sci-fi mission control.
token_hooks:
  color_primitives:
    - brand
    - gray
  color_semantic:
    - bg.canvas
    - bg.surface-primary
    - bg.surface-secondary
    - text.primary
    - text.secondary
    - text.tertiary
    - brand.primary
    - brand.secondary
    - status.success-bg
    - status.success-text
    - status.warning-bg
    - status.warning-text
    - status.danger-bg
    - status.danger-text
    - status.info-bg
    - status.info-text
  spacing:
    - 3xs
    - 2xs
    - xs
    - sm
    - md
    - lg
    - xl
    - 2xl
    - 3xl
  radius:
    - xs
    - sm
    - md
    - lg
    - xl
    - 2xl
    - full
spacing_px:
  3xs: 2
  2xs: 4
  xs: 8
  sm: 12
  md: 16
  lg: 24
  xl: 32
  2xl: 48
  3xl: 64
radius_px:
  xs: 2
  sm: 4
  md: 8
  lg: 12
  xl: 16
  2xl: 24
  full: 9999
typography:
  Display/Hero-Large:
    size: 56
    lineHeight: 1.1
    weight: Bold
  Display/Hero-Medium:
    size: 44
    lineHeight: 1.2
    weight: Bold
  Heading/H1:
    size: 32
    lineHeight: 1.3
    weight: Bold
  Heading/H2:
    size: 24
    lineHeight: 1.35
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
  Utility/Code:
    size: 13
    lineHeight: 1.45
    weight: Regular
layout:
  whitespace_bias: dense
  asymmetry:
    enabled: false
    recipes: []
  color_distribution:
    tone: 0.6
    structure: 0.3
    accent: 0.1
  borders:
    default: hairline
    width_token: sm
  shadows:
    default: none
  corners:
    bias: sharp
components:
  button_radius_token: xs
  card_padding_token: sm
  card_border: true
modes:
  light_dark: variable_modes
---

# SpaceX-like UI

Industrial sci-fi mission control.

_Source: aesthetic-presets/space-x-like-ui/SKILL.md_

_Grammar only — Style DNA / board supplies values at generate time. Does not restyle the product's own chrome._
