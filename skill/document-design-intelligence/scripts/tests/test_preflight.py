#!/usr/bin/env python3
"""Unit tests for scripts/preflight.py — run with the system Python.

Fixtures: lib/tests/fixtures/sample.pdf (real Chromium output, already
covered in detail by lib/tests/test_pdf.py — here we only check preflight's
own dispatch/formatting/unit-conversion on top of it) and
tests/fixtures/sample.{docx,pptx} (hand-built OOXML, see
tests/fixtures/make_ooxml_fixtures.py for exactly what each contains).
"""
import json
import subprocess
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).parent
SCRIPTS_DIR = HERE.parent
sys.path.insert(0, str(SCRIPTS_DIR))
import preflight  # noqa: E402

PDF_FIXTURE = SCRIPTS_DIR / "lib" / "tests" / "fixtures" / "sample.pdf"
DOCX_FIXTURE = HERE / "fixtures" / "sample.docx"
PPTX_FIXTURE = HERE / "fixtures" / "sample.pptx"
PYTHON = sys.executable


@unittest.skipUnless(PDF_FIXTURE.exists(), "sample.pdf fixture not present")
class TestPreflightPdf(unittest.TestCase):
    def test_page_count_and_units(self):
        result = preflight.run(str(PDF_FIXTURE))
        self.assertEqual(result["file_type"], "pdf")
        self.assertEqual(result["page_count"], 1)
        box = result["pages"][0]["MediaBox"]
        # A4-ish page from CSS `size: A4` — pt and mm must agree via the
        # same conversion factor (25.4/72), not independently rounded.
        self.assertAlmostEqual(box["pt"][2] * 25.4 / 72, box["mm"][2], places=1)
        self.assertIsNone(result["pages"][0]["TrimBox"])

    def test_fonts_and_images_carried_through(self):
        result = preflight.run(str(PDF_FIXTURE))
        self.assertEqual(len(result["fonts"]), 2)
        self.assertTrue(all(f["embedded"] for f in result["fonts"]))
        self.assertEqual(len(result["images"]), 1)
        self.assertAlmostEqual(result["images"][0]["placed_width_pt"], 75.0, delta=0.5)

    def test_verdicts_present_and_print_boxes_fail_on_chromium_output(self):
        result = preflight.run(str(PDF_FIXTURE))
        checks = {v["check"]: v["pass"] for v in result["verdicts"]}
        self.assertTrue(checks["fonts-embedded"])
        self.assertTrue(checks["raster-placement-resolved"])
        # Chromium's plain print-to-pdf has no TrimBox/BleedBox at all —
        # research/14-print-production-values.md §1 — so this verdict is
        # correctly a fact-level "FAIL", not an error.
        self.assertFalse(checks["print-production-boxes"])


@unittest.skipUnless(DOCX_FIXTURE.exists(), "sample.docx fixture not present")
class TestPreflightDocx(unittest.TestCase):
    def test_font_embedding_resolved_per_font(self):
        result = preflight.run(str(DOCX_FIXTURE))
        self.assertEqual(result["file_type"], "docx")
        by_name = {f["name"]: f["embedded"] for f in result["fonts"]}
        self.assertEqual(by_name, {"Calibri": True, "Arial": False})

    def test_ats_structural_facts(self):
        result = preflight.run(str(DOCX_FIXTURE))
        s = result["structure"]
        self.assertEqual(s["multi_column_sections"], 0)
        self.assertEqual(s["tables"], 1)
        self.assertEqual(s["text_boxes"], 0)

    def test_contact_only_in_header_is_the_documented_ats_risk_case(self):
        result = preflight.run(str(DOCX_FIXTURE))
        s = result["structure"]
        self.assertFalse(s["contact_in_first_body_paragraph"])
        self.assertTrue(s["contact_in_header"])
        self.assertTrue(s["contact_only_in_header"])


@unittest.skipUnless(PPTX_FIXTURE.exists(), "sample.pptx fixture not present")
class TestPreflightPptx(unittest.TestCase):
    def test_embedded_vs_referenced_only(self):
        result = preflight.run(str(PPTX_FIXTURE))
        self.assertEqual(result["file_type"], "pptx")
        by_name = {f["name"]: f["embedded"] for f in result["fonts"]}
        self.assertEqual(by_name, {"EmbeddedFont": True, "NotEmbeddedFont": False})


class TestReportsNotDecides(unittest.TestCase):
    def test_unsupported_extension_is_a_fact_not_a_crash(self):
        result = preflight.run("nonexistent.txt")
        self.assertIn("error", result)

    def test_missing_file_is_a_fact_not_a_crash(self):
        result = preflight.run("nonexistent_file_12345.pdf")
        self.assertIn("error", result)

    def test_cli_exit_code_is_always_zero(self):
        for args in (
            [str(PDF_FIXTURE)],
            [str(DOCX_FIXTURE), "--json"],
            ["nonexistent.pdf"],
            ["nonexistent.xyz"],
            [],
        ):
            proc = subprocess.run(
                [PYTHON, str(SCRIPTS_DIR / "preflight.py"), *args],
                capture_output=True, text=True,
            )
            self.assertEqual(proc.returncode, 0, f"args={args} stderr={proc.stderr}")

    def test_json_output_is_valid_json(self):
        proc = subprocess.run(
            [PYTHON, str(SCRIPTS_DIR / "preflight.py"), str(PDF_FIXTURE), "--json"],
            capture_output=True, text=True,
        )
        parsed = json.loads(proc.stdout)
        self.assertEqual(parsed["file_type"], "pdf")


if __name__ == "__main__":
    unittest.main()
