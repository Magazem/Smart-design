#!/usr/bin/env python3
"""Content regressions for the generated portable pack (research/87): G1 no brand
rows, G2 severity per category, F1 thresholds, F2 print geometry, F3 palette roles,
F4 font rule, I1 triggers, and the F5 pptx handoff layout."""
import importlib.util
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).parent
SKILL_ROOT = HERE.parent.parent
GENERATOR = SKILL_ROOT.parent.parent / "research" / "build-portable.py"


@unittest.skipUnless(GENERATOR.exists(), "generator not present (skill unpacked without research/)")
class TestPortableContent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("build_portable_content", GENERATOR)
        cls.mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.mod)
        cls.files = cls.mod.generate_all()
        cls.lib = cls.files["DDI-LIBRARY.md"]

    def block(self, doc_key):
        start = self.lib.index(f"(`{doc_key}`)\n")
        end = self.lib.find("\n### ", start + 5)
        return self.lib[start:end]

    def test_g1_brand_overlay_rows_do_not_leak(self):
        tmp = Path(tempfile.mkdtemp(prefix="ddi-portable-g1-"))
        self.addCleanup(lambda: shutil.rmtree(tmp, ignore_errors=True))
        shutil.copytree(SKILL_ROOT / "data", tmp / "data")
        brand = tmp / "data" / "brand" / "acme"
        brand.mkdir(parents=True, exist_ok=True)
        import csv
        for name in ("doctypes", "designs"):
            with (SKILL_ROOT / "data" / "base" / f"{name}.csv").open(encoding="utf-8", newline="") as f:
                rows = list(csv.DictReader(f))
            row = dict(rows[0])
            key = "doc_key" if name == "doctypes" else "design_key"
            row[key] = "acme-zzz"
            row["Display Name"] = "ACME BRAND ROW"
            with (brand / f"{name}.csv").open("w", encoding="utf-8", newline="") as f:
                w = csv.DictWriter(f, fieldnames=list(row), lineterminator="\n")
                w.writeheader()
                w.writerow(row)
        out = self.mod.generate_all(tmp / "data")
        for text in out.values():
            self.assertNotIn("acme", text.lower())
        self.assertEqual(out["DDI-LIBRARY.md"], self.lib)

    def test_f1_thresholds_and_references_resolved(self):
        deck = self.block("slide-deck-projection")
        self.assertIn("= 7.0", deck)   # validate-contrast-screen
        self.assertIn("= 40", deck)    # words_per_slide_body
        self.assertIn("[format:", deck)
        cv = self.block("cv-uk")
        self.assertNotIn("cv-regions:Max Pages", cv)
        self.assertNotIn("page-formats:", self.block("brochure-trifold-a4"))

    def test_f2_print_geometry(self):
        b = self.block("brochure-trifold-a4")
        self.assertIn("panels: 99.5;99.5;98.0mm", b)
        self.assertIn("stock: 120gsm", b)

    def test_f3_palette_roles(self):
        self.assertIn("fill-only roles", self.block("brochure-trifold-a4"))
        self.assertIn("text-safe roles", self.lib.split("## Grand library")[1])

    def test_f4_font_rule(self):
        self.assertIn("docx = safe-stack", self.block("cv-dach"))
        self.assertIn("### Font substitutes", self.lib)

    def test_g2_no_global_worst_severity_fold(self):
        line = next(l for l in self.lib.splitlines() if l.startswith("- `photo` --"))
        self.assertIn("warn:", line)
        self.assertNotRegex(line, r"^- `photo` -- fail$")
        self.assertIn("cv-academic", line)

    def test_i1_triggers_include_family_noun(self):
        agents = self.files["AGENTS.md"]
        for line in agents.splitlines():
            if line.startswith("- **"):
                family = line[4:line.index("**", 4)]
                self.assertIn(family.replace("-", " "), line.lower())
        self.assertIn("resume", agents)
        self.assertIn("brochure", agents)

    def test_s2_designs_heading_names_family(self):
        self.assertIn("### Designs (ranked) -- family: cv", self.lib)
        self.assertNotIn("### Designs (ranked)\n", self.lib)


class TestPptxHandoffLayout(unittest.TestCase):
    def test_pptx_layout_follows_page_format_trim(self):
        import json
        ddi = str(SKILL_ROOT / "scripts" / "ddi.py")
        res = subprocess.run([sys.executable, ddi, "resolve", "--doctype", "slide-deck-projection", "--json"],
                             capture_output=True, text=True, encoding="utf-8")
        tmp = Path(tempfile.mkdtemp(prefix="ddi-h-"))
        self.addCleanup(lambda: shutil.rmtree(tmp, ignore_errors=True))
        (tmp / "r.json").write_text(res.stdout, encoding="utf-8")
        out = subprocess.run([sys.executable, ddi, "handoff", "--json", str(tmp / "r.json"),
                              "--format", "pptx"], capture_output=True, text=True, encoding="utf-8").stdout
        self.assertIn("13.333in x 7.5in", out)
        self.assertNotIn("10in x 5.625in", out)


if __name__ == "__main__":
    unittest.main()


class TestQuoteHeadings(unittest.TestCase):
    """research/87 D1: quote-devis must not inherit invoice heading wording."""

    def test_quote_devis_handoff_has_no_invoice_headings(self):
        ddi = str(SKILL_ROOT / "scripts" / "ddi.py")
        tmp = Path(tempfile.mkdtemp(prefix="ddi-q-"))
        self.addCleanup(lambda: shutil.rmtree(tmp, ignore_errors=True))
        for lang in ("en", "fr", "de"):
            res = subprocess.run([sys.executable, ddi, "resolve", "--doctype", "quote-devis",
                                  "--lang", lang, "--json"], capture_output=True, text=True, encoding="utf-8")
            (tmp / "r.json").write_text(res.stdout, encoding="utf-8")
            for fmt in ("docx", "pdf"):
                out = subprocess.run([sys.executable, ddi, "handoff", "--json", str(tmp / "r.json"),
                                      "--format", fmt], capture_output=True, text=True,
                                     encoding="utf-8").stdout.lower()
                with self.subTest(lang=lang, fmt=fmt):
                    for bad in ("facture", "rechnung", "invoice"):
                        self.assertNotIn(bad, out)
                    self.assertTrue(any(w in out for w in ("devis pour", "quote for", "angebot für")))
