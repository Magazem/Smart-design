#!/usr/bin/env python3
"""Unit tests for lib/color.py — run with the system Python (stdlib only)."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import color  # noqa: E402


class TestRelativeLuminance(unittest.TestCase):
    def test_white_is_one(self):
        self.assertAlmostEqual(color.relative_luminance("#FFFFFF"), 1.0, places=6)

    def test_black_is_zero(self):
        self.assertAlmostEqual(color.relative_luminance("#000000"), 0.0, places=6)

    def test_rejects_malformed_hex(self):
        for bad in ("1F6F43", "#1F6F4", "#GGGGGG", "", None):
            with self.assertRaises(ValueError):
                color.relative_luminance(bad)


class TestContrastRatio(unittest.TestCase):
    def test_black_on_white_is_21_to_1(self):
        self.assertAlmostEqual(color.contrast_ratio("#000000", "#FFFFFF"), 21.0, places=2)

    def test_symmetric(self):
        a = color.contrast_ratio("#1F6F43", "#FFFFFF")
        b = color.contrast_ratio("#FFFFFF", "#1F6F43")
        self.assertAlmostEqual(a, b, places=9)

    def test_same_color_is_one_to_one(self):
        self.assertAlmostEqual(color.contrast_ratio("#1F6F43", "#1F6F43"), 1.0, places=9)

    def test_matches_upstream_validate_data_formula(self):
        # Hand-computed against the exact ported formula
        # (validate_data.py:_relative_luminance/contrast_ratio) — WCAG 2.x.
        ratio = color.contrast_ratio("#1F6F43", "#FFFFFF")
        self.assertAlmostEqual(ratio, 6.15, places=1)


class TestOnColor(unittest.TestCase):
    def test_dark_background_gets_white_text(self):
        self.assertEqual(color.on_color("#1F6F43"), "#FFFFFF")

    def test_light_background_gets_black_text(self):
        self.assertEqual(color.on_color("#F7F8F5"), "#000000")

    def test_chosen_color_never_has_lower_contrast_than_the_other(self):
        for bg in ("#1F6F43", "#9ACD32", "#8B5E3C", "#F7F8F5", "#B4261F"):
            chosen = color.on_color(bg)
            other = "#000000" if chosen == "#FFFFFF" else "#FFFFFF"
            self.assertGreaterEqual(
                color.contrast_ratio(chosen, bg) + 1e-9,
                color.contrast_ratio(other, bg),
            )

    def test_lime_as_text_fails_on_white_and_on_ens_green(self):
        # ENS-rebuild-corrections.md's finding: lime (#9ACD32) used as a TEXT
        # color fails contrast against both white and the ENS green — the
        # documented reason the ENS rules only ever use lime as a filled
        # badge background (with on_color() picking its own text), never as
        # text on top of another surface. This is a contrast_ratio check on
        # the (lime-as-foreground, other-as-background) pair, not on_color().
        lime = "#9ACD32"
        self.assertLess(color.contrast_ratio(lime, "#FFFFFF"), 4.5)
        self.assertLess(color.contrast_ratio(lime, "#1F6F43"), 4.5)

    def test_lime_as_a_filled_badge_background_is_fine(self):
        # The ENS-approved use: lime as a background with on_color() picking
        # the text on top of it. This pairing should clear 4.5:1 easily.
        lime = "#9ACD32"
        self.assertEqual(color.on_color(lime), "#000000")
        self.assertGreaterEqual(color.contrast_ratio(color.on_color(lime), lime), 4.5)


if __name__ == "__main__":
    unittest.main()
