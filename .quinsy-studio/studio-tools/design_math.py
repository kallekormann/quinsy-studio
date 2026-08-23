#!/usr/bin/env python3
"""Calculable design rules — contrast, golden scale, palette split, IA nav audit."""

from __future__ import annotations

import math
import re
from typing import Dict, List, Tuple

PHI = 1.6180339887


def _srgb_to_linear(channel: float) -> float:
    c = channel / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def relative_luminance(hex_color: str) -> float:
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    r = int(h[0:2], 16)
    g = int(h[2:4], 16)
    b = int(h[4:6], 16)
    r_l = _srgb_to_linear(r)
    g_l = _srgb_to_linear(g)
    b_l = _srgb_to_linear(b)
    return 0.2126 * r_l + 0.7152 * g_l + 0.0722 * b_l


def contrast_ratio(fg_hex: str, bg_hex: str) -> float:
    l1 = relative_luminance(fg_hex)
    l2 = relative_luminance(bg_hex)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def wcag_aa_pass(ratio: float, *, large_text: bool = False) -> bool:
    return ratio >= 3.0 if large_text else ratio >= 4.5


def golden_scale(base_px: float, steps: int = 6) -> List[float]:
    sizes = [base_px]
    for _ in range(steps - 1):
        sizes.append(round(sizes[-1] * PHI, 2))
    return sizes


def palette_60_30_10(primary: str, neutral: str, accent: str | None = None) -> Dict[str, str]:
    accent = accent or primary
    return {
        "dominant_60": neutral,
        "secondary_30": primary,
        "accent_10": accent,
    }


def ia_nav_audit(top_level_count: int, max_depth: int) -> List[str]:
    warnings: List[str] = []
    if top_level_count > 7:
        warnings.append(f"Top-level nav has {top_level_count} items (target ≤7)")
    if max_depth > 3:
        warnings.append(f"Nav depth is {max_depth} (target ≤3)")
    return warnings


_HEX_RE = re.compile(r"#([0-9a-fA-F]{3,8})\b")


def extract_hex_colors(css_text: str) -> List[str]:
    found = _HEX_RE.findall(css_text)
    normalized: List[str] = []
    for h in found:
        if len(h) in (3, 4):
            h = "".join(c * 2 for c in h[:3])
        if len(h) >= 6:
            normalized.append(f"#{h[:6].lower()}")
    return list(dict.fromkeys(normalized))


def audit_token_contrast_pairs(
    css_text: str,
    pairs: List[Tuple[str, str]],
) -> List[Dict[str, object]]:
    colors = {c: c for c in extract_hex_colors(css_text)}
    results: List[Dict[str, object]] = []
    for fg_name, bg_name in pairs:
        fg = colors.get(fg_name) or fg_name
        bg = colors.get(bg_name) or bg_name
        if not fg.startswith("#") or not bg.startswith("#"):
            continue
        ratio = round(contrast_ratio(fg, bg), 2)
        results.append({
            "foreground": fg,
            "background": bg,
            "ratio": ratio,
            "aa_normal": wcag_aa_pass(ratio),
            "aa_large": wcag_aa_pass(ratio, large_text=True),
        })
    return results


if __name__ == "__main__":
    import argparse
    import sys
    from pathlib import Path

    parser = argparse.ArgumentParser(description="Design math utilities")
    parser.add_argument("--audit-tokens", type=Path, help="CSS file with color tokens")
    args = parser.parse_args()
    if args.audit_tokens:
        css = args.audit_tokens.read_text()
        colors = extract_hex_colors(css)
        print(f"Found {len(colors)} hex colors in {args.audit_tokens}")
        if len(colors) >= 2:
            ratio = contrast_ratio(colors[0], colors[-1])
            print(f"Sample contrast {colors[0]} on {colors[-1]}: {ratio:.2f} (AA: {wcag_aa_pass(ratio)})")
        sys.exit(0)
    print("Use --audit-tokens <path> or import as module")
