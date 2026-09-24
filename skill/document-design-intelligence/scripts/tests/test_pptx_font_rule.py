#!/usr/bin/env python3
"""research/87 F10 / research/90 F10: `pptx-font-embedded` passes when the fonts are embedded OR the
file declares the safe-stack fallback (python-pptx cannot embed); it fails only when neither holds."""
import csv
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

HERE = Path(__file__).parent
SCRIPTS_DIR = HERE.parent
sys.path.insert(0, str(SCRIPTS_DIR))
import preflight  # noqa: E402

SAMPLE = HERE / "fixtures" / "sample.pptx"
DDI = SCRIPTS_DIR / "ddi.py"
BASE = SCRIPTS_DIR.parent / "data" / "base"

CORE_XML = ('<?xml version="1.0" encoding="UTF-8"?><cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/'
            'package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/"><cp:keywords>'
            '{kw}</cp:keywords></cp:coreProperties>')


def with_core_keywords(src: Path, dst: Path, keywords: str):
    with zipfile.ZipFile(src) as zin, zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            zout.writestr(item, zin.read(item.filename))
        zout.writestr("docProps/core.xml", CORE_XML.format(kw=keywords))


class TestVerdictLogic(unittest.TestCase):
    F_EMB = [{"name": "A", "embedded": True}, {"name": "B", "embedded": True}]
    F_MIX = [{"name": "A", "embedded": True}, {"name": "B", "embedded": False}]
    F_NONE = [{"name": "A", "embedded": False}]

    def test_all_embedded_passes_without_a_declaration(self):
        self.assertTrue(preflight.pptx_font_verdict(self.F_EMB, False)["pass"])

    def test_declared_safe_stack_passes_even_with_nothing_embedded(self):
        v = preflight.pptx_font_verdict(self.F_NONE, True)
        self.assertTrue(v["pass"])
        self.assertIn("safe-stack fallback declared", v["detail"])

    def test_neither_embedded_nor_declared_fails_and_says_what_to_do(self):
        for fonts in (self.F_MIX, self.F_NONE, []):
            with self.subTest(fonts=fonts):
                v = preflight.pptx_font_verdict(fonts, False)
                self.assertFalse(v["pass"])
                self.assertIn("declare the safe-stack fallback", v["detail"])


@unittest.skipUnless(SAMPLE.exists(), "sample.pptx fixture not present")
class TestPreflightPptxFile(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="ddi-pptx-"))
        self.addCleanup(lambda: shutil.rmtree(self.tmp, ignore_errors=True))

    def verdict(self, path):
        result = preflight.run(str(path))
        return {v["check"]: v for v in result["verdicts"]}["pptx-font-embedded"], result

    def test_undeclared_partly_embedded_deck_fails(self):
        v, result = self.verdict(SAMPLE)
        self.assertFalse(v["pass"])
        self.assertFalse(result["font_rule_declared"])

    def test_declaration_in_core_keywords_makes_it_pass(self):
        dst = self.tmp / "declared.pptx"
        with_core_keywords(SAMPLE, dst, "brand, ddi-font-rule=safe-stack")
        v, result = self.verdict(dst)
        self.assertTrue(v["pass"], v)
        self.assertTrue(result["font_rule_declared"])

    def test_an_unrelated_keyword_does_not_declare(self):
        dst = self.tmp / "other.pptx"
        with_core_keywords(SAMPLE, dst, "quarterly, sales")
        self.assertFalse(self.verdict(dst)[0]["pass"])

    def test_human_output_prints_the_verdict(self):
        dst = self.tmp / "declared.pptx"
        with_core_keywords(SAMPLE, dst, "ddi-font-rule=safe-stack")
        out = subprocess.run([sys.executable, str(SCRIPTS_DIR / "preflight.py"), str(dst)],
                             capture_output=True, text=True, encoding="utf-8").stdout
        self.assertIn("[PASS] pptx-font-embedded", out)


class TestHandoffAndData(unittest.TestCase):
    def test_pptx_handoff_says_how_to_declare_the_fallback(self):
        tmp = Path(tempfile.mkdtemp(prefix="ddi-hp-"))
        self.addCleanup(lambda: shutil.rmtree(tmp, ignore_errors=True))
        res = subprocess.run([sys.executable, str(DDI), "resolve", "--doctype", "slide-deck-projection", "--json"],
                             capture_output=True, text=True, encoding="utf-8")
        (tmp / "r.json").write_text(res.stdout, encoding="utf-8")
        out = subprocess.run([sys.executable, str(DDI), "handoff", "--json", str(tmp / "r.json"), "--format", "pptx"],
                             capture_output=True, text=True, encoding="utf-8").stdout
        self.assertIn("ddi-font-rule=safe-stack", out)
        self.assertIn("python-pptx cannot embed fonts", out)

    def test_constraint_row_is_the_relaxed_one_and_still_fail_severity(self):
        with (BASE / "constraints.csv").open(encoding="utf-8", newline="") as f:
            row = next(r for r in csv.DictReader(f) if r["constraint_key"] == "pptx-font-embedded")
        self.assertEqual(row["Threshold"], "present-or-declared")
        self.assertIn("or=declared-safe-stack", row["Parameter"])
        self.assertEqual(row["Severity"], "fail")            # fail only when neither holds


if __name__ == "__main__":
    unittest.main()
