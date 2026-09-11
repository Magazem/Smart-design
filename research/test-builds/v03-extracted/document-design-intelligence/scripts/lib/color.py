#!/usr/bin/env python3
"""WCAG 2.x contrast primitives for #RRGGBB sRGB colors.

The relative-luminance and contrast-ratio formulas here are ported verbatim
from upstream ui-ux-pro-max's own build-time validator, which already
implements the WCAG 2.x formula correctly and is exercised in production:
`upstream-latest/src/ui-ux-pro-max/scripts/validate_data.py`, functions
`_relative_luminance` (lines 148-154) and `contrast_ratio` (lines 157-160).
Only the hex-validation regex and function names differ here (kept local so
this module has no dependency on that file); the arithmetic is identical.

This module is also the schema's replacement for `print-l-delta` per
research/14-print-production-values.md section 4: no standardized print-contrast
metric exists (CIE L* delta is convention with no source), so print
legibility is checked with this same WCAG ratio against the actual sRGB
values every current render target rasterizes, rather than an invented
Lab-space threshold.
"""

import ast
import re
import sys
from pathlib import Path


def _assert_stdlib_only():
    """Fail loudly at import time if a non-stdlib import is ever added here.

    See fonts.py for the identical guard and rationale; duplicated here
    (rather than imported) so this file is independently self-verifying.
    """
    tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    stdlib = sys.stdlib_module_names
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names = [alias.name.split(".")[0] for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            if node.level or node.module is None:
                continue
            names = [node.module.split(".")[0]]
        else:
            continue
        for name in names:
            if name not in stdlib:
                raise AssertionError(
                    f"non-stdlib import '{name}' found in {__file__} -- "
                    "this module must be Python stdlib only"
                )


_assert_stdlib_only()


_HEX_COLOR = re.compile(r"#[0-9A-Fa-f]{6}")


def relative_luminance(hex_color):
    """WCAG 2.x relative luminance of an opaque six-digit sRGB hex color.

    Checks: applies the WCAG 2.x formula exactly (sRGB channel -> linear
    -> Rec. 709 luma weights 0.2126/0.7152/0.0722), matching
    `validate_data.py:_relative_luminance` line for line.

    Cannot know anything about a color's appearance under a specific
    display's actual gamma/calibration, or about a color that isn't plain
    opaque sRGB (no alpha, no wide-gamut, no print ink model).

    Raises:
        ValueError if `hex_color` is not exactly `#RRGGBB` -- this is a
        hard failure, not a return value, because a malformed color is a
        caller bug, not a fact about the world worth reporting as data.
    """
    if not _HEX_COLOR.fullmatch(hex_color or ""):
        raise ValueError(f"invalid hex color '{hex_color}'")
    channels = [int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    linear = [
        c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
        for c in channels
    ]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast_ratio(hex_fg, hex_bg):
    """WCAG contrast ratio between two opaque six-digit sRGB colors.

    Checks: `(L1 + 0.05) / (L2 + 0.05)` with L1/L2 the lighter/darker
    relative luminance -- the exact WCAG 2.x formula, matching
    `validate_data.py:contrast_ratio` line for line. Order of the two
    arguments does not matter; the ratio is symmetric.

    Cannot know whether the ratio clears any particular pass/fail
    threshold (4.5:1 normal text, 3:1 large text/UI) -- that judgment
    belongs to the caller, not this function.

    Raises:
        ValueError (via relative_luminance) if either color is not a
        valid `#RRGGBB` string.
    """
    first, second = relative_luminance(hex_fg), relative_luminance(hex_bg)
    return (max(first, second) + 0.05) / (min(first, second) + 0.05)


def on_color(hex_background):
    """Pick the higher-contrast of pure white or pure black text for a background.

    Checks: computes contrast_ratio against both #FFFFFF and #000000 and
    returns whichever is higher. Ties resolve to white.

    Cannot know anything about a background that isn't plain opaque sRGB,
    and does not guarantee the winning ratio clears any accessibility
    threshold -- a background close to mid-gray can have both ratios fail
    4.5:1 even though one is "higher" than the other. Callers that need a
    pass/fail answer should check `contrast_ratio(on_color(bg), bg)`
    against the threshold themselves.

    Returns:
        "#FFFFFF" or "#000000".

    Raises:
        ValueError (via relative_luminance) if `hex_background` is not a
        valid `#RRGGBB` string.
    """
    white_ratio = contrast_ratio("#FFFFFF", hex_background)
    black_ratio = contrast_ratio("#000000", hex_background)
    return "#FFFFFF" if white_ratio >= black_ratio else "#000000"


if __name__ == "__main__":
    for _hex in sys.argv[1:]:
        _on = on_color(_hex)
        print(f"{_hex}: luminance={relative_luminance(_hex):.4f} "
              f"on_color={_on} contrast={contrast_ratio(_on, _hex):.2f}:1")
