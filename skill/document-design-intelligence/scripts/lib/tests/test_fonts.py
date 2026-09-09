#!/usr/bin/env python3
"""Unit tests for lib/fonts.py — run with the system Python (stdlib only).

Uses real fonts from C:\\Windows\\Fonts so the assertions are against actual
sfnt binaries, not synthetic ones: Arial (TrueType, restricted-embedding-
by-policy but declared "editable" via fsType) and one CFF-flavored OTF
(David CLM, declared "installable").
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import fonts  # noqa: E402

WINDOWS_FONTS = Path(r"C:\Windows\Fonts")
ARIAL = WINDOWS_FONTS / "arial.ttf"
CONSOLA = WINDOWS_FONTS / "consola.ttf"
TIMES = WINDOWS_FONTS / "times.ttf"
DAVID_OTF = WINDOWS_FONTS / "DavidCLM-Bold.otf"


@unittest.skipUnless(ARIAL.exists(), "Arial not present on this machine")
class TestReadFsType(unittest.TestCase):
    def test_arial_ttf_is_editable(self):
        fs_type, label = fonts.read_fstype(str(ARIAL))
        self.assertEqual(fs_type, 8)
        self.assertEqual(label, "editable")

    @unittest.skipUnless(DAVID_OTF.exists(), "David CLM OTF not present")
    def test_otf_cff_flavored_font_is_readable(self):
        fs_type, label = fonts.read_fstype(str(DAVID_OTF))
        self.assertEqual(fs_type, 0)
        self.assertEqual(label, "installable")

    def test_not_a_font_returns_none_and_reason(self):
        not_a_font = Path(__file__)  # this .py file is not a font
        fs_type, reason = fonts.read_fstype(str(not_a_font))
        self.assertIsNone(fs_type)
        self.assertIn("not a TTF/OTF", reason)

    def test_bit_decoding_is_stable_across_two_ttf_families(self):
        # Both TrueType families in this test set ship fsType=8; assert the
        # decode path (not just a hardcoded expectation) is consistent.
        for path in (ARIAL, TIMES):
            fs_type, label = fonts.read_fstype(str(path))
            self.assertEqual(fs_type & 0x000F, 8)
            self.assertEqual(label.split("+")[0], "editable")


@unittest.skipUnless(ARIAL.exists() and CONSOLA.exists(), "fonts not present")
class TestHasTnum(unittest.TestCase):
    def test_arial_reports_yes(self):
        self.assertEqual(fonts.has_tnum(str(ARIAL)), "yes")

    def test_consolas_reports_unknown_not_no(self):
        # The documented ambiguous case: Consolas is monospaced (digits are
        # already tabular) but carries no GSUB `tnum` tag. This function
        # must never claim "no" here.
        result = fonts.has_tnum(str(CONSOLA))
        self.assertEqual(result, "unknown")
        self.assertNotEqual(result, "no")

    def test_never_returns_the_literal_string_no(self):
        for path in (ARIAL, CONSOLA, TIMES):
            self.assertIn(fonts.has_tnum(str(path)), ("yes", "unknown"))

    def test_garbage_file_is_unknown_not_a_crash(self):
        self.assertEqual(fonts.has_tnum(str(Path(__file__))), "unknown")


if __name__ == "__main__":
    unittest.main()
