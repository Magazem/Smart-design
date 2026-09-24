#!/usr/bin/env python3
"""research/90 R6 review: brand-kit fixes. The two briefs the reviewer built by hand are re-run
here (B1 children's charity with a failing orange accent, bilingual; B2 fintech on a tinted
Material palette). Kit rows are appended to a snapshot of data/base the way merge_brand_kit
does, then addressed with --data-dir."""
import contextlib
import csv
import io
import json
import sys
import unittest
import zipfile
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))
from test_make_brand_kit import MakeBrandKitTestCase  # noqa: E402
import ddi  # noqa: E402
import make_brand_kit as mbk  # noqa: E402

B1 = """# Little Steps

slug: little-steps

## Palette
primary: #0b0c0c
secondary: #484949
accent: #F28C28
background: #ffffff
foreground: #0b0c0c
muted: #f4f8fb

## Typefaces
heading: Nunito
body: Nunito Sans

## Doctypes
letter-formal
brochure-flyer-a4
report-short

## Designs
letter: letter-formal
flyer: print-marketing-bold-flyer
report: report-classic

## Type scales
print: lib-major-third-print

## Languages
en, fr
"""

B2 = """# Ledgerline

slug: ledgerline

## Palette
primary: #1d1b20
secondary: #49454F
accent: #6750A4
background: #fef7ff
foreground: #1d1b20
muted: #E7E0EC

## Typefaces
heading: Inter
body: Inter

## Doctypes
slide-deck-projection
invoice-tabular
one-pager

## Designs
deck: deck-generic
invoice: invoice-tabular
one-pager: one-pager-restrained

## Type scales
print: lib-major-third-print
projection: lib-perfect-fourth-projection
"""


def _designs(skill_dir):
    with (skill_dir / "data" / "base" / "designs.csv").open(encoding="utf-8", newline="") as f:
        return {r["Family"]: r["design_key"] for r in csv.DictReader(f) if r["Rank"] == "1"}


def _append(path, rows):
    with path.open(encoding="utf-8", newline="") as f:
        cols = next(csv.reader(f))
    with path.open("a", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n")
        for r in rows:
            w.writerow({c: r.get(c, "") for c in cols})


class R6Case(MakeBrandKitTestCase):
    def brand(self, text, slug):
        # the flyer's rank-1 design key is data; substitute the real one
        tops = _designs(self.skill_dir)
        text = text.replace("print-marketing-bold-flyer", tops["flyer"])
        code, out = self._run([str(self._write_brand_md(text)), "--dry-run"])
        self.dry_run_output, self.dry_run_code = out, code
        code, _ = self._run([str(self._write_brand_md(text))])
        self.assertEqual(code, 0, out)
        self.kit = {}
        with zipfile.ZipFile(self.outputs / f"{slug}-brand-kit.zip") as zf:
            for n in zf.namelist():
                if n.endswith(".csv"):
                    rows = list(csv.DictReader(io.StringIO(zf.read(n).decode("utf-8"))))
                    self.kit[Path(n).name] = rows
                    _append(self.skill_dir / "data" / "base" / Path(n).name, rows)
        return self.skill_dir / "data"

    def ddi(self, *argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
            code = ddi.main(list(argv))
        return code, out.getvalue()

    def handoff(self, data, doctype, fmt, *extra):
        code, out = self.ddi("resolve", "--data-dir", str(data), "--json", "--brand", extra[0] if extra else "",
                             "--doctype", doctype) if extra else self.ddi(
            "resolve", "--data-dir", str(data), "--json", "--doctype", doctype)
        self.assertEqual(code, 0, out)
        path = self.outputs / "r.json"
        path.write_text(out, encoding="utf-8")
        code, text = self.ddi("handoff", "--json", str(path), "--format", fmt)
        self.assertEqual(code, 0, text)
        return text


class TestB1FailingAccent(R6Case):
    def test_f2_dry_run_shows_accent_pair_and_demotion(self):
        self.brand(B1, "little-steps")
        out = self.dry_run_output
        self.assertIn("Accent/Background", out)
        self.assertRegex(out, r"Accent/Background: #F28C28 on #ffffff = 2\.\d\d:1 \[fill-only")
        self.assertIn("accent demoted to fill-only", out)
        self.assertIn("WCAG 1.4.11", out)           # 2.45 < 3:1 non-text warning
        self.assertNotIn("FAIL", out.split("gate output")[0])  # a demotion is not a FAIL

    def test_f2_accent_kept_as_fill_only_in_data(self):
        self.brand(B1, "little-steps")
        pal = self.kit["palettes.csv"][0]
        self.assertEqual(pal["Accent"], "#F28C28")
        self.assertEqual(pal["Fill-Only Roles"], "accent")

    def test_f5_text_safe_includes_foreground_and_rule_brand_is_primary(self):
        self.brand(B1, "little-steps")
        pal = self.kit["palettes.csv"][0]
        self.assertEqual(pal["Text-Safe Roles"].split(";"), ["foreground", "primary", "secondary"])
        self.assertEqual(pal["Rule Brand"], pal["Primary"])    # accent is not text-safe

    def test_f4_rule_hair_copied_from_the_library_palette(self):
        self.brand(B1, "little-steps")
        pal = self.kit["palettes.csv"][0]
        self.assertEqual(pal["Rule Hair"].lower(), "#cecece")   # lib-govuk-ink's own value
        self.assertIn("library palette lib-govuk-ink", self.dry_run_output)

    def test_f3_every_handoff_format_names_text_safe_and_fill_only_roles(self):
        data = self.brand(B1, "little-steps")
        for fmt in ("docx", "pptx", "pdf", "png"):
            with self.subTest(fmt=fmt):
                text = self.handoff(data, "little-steps-report-short", fmt, "little-steps")
                self.assertIn("text-safe roles", text)
                self.assertIn("fill-only roles: accent", text)
                self.assertIn("never set text in a fill-only role", text)

    def test_f6_second_language_is_reachable(self):
        data = self.brand(B1, "little-steps")
        rows = {r["doc_key"]: r for r in self.kit["doctypes.csv"]}
        kw = rows["little-steps-report-short"]["Keywords"]
        self.assertIn("rapport", kw)                       # the base doctype's French keyword kept
        self.assertIn("little-steps", kw)
        code, out = self.ddi("resolve", "--data-dir", str(data), "--brand", "little-steps", "--query",
                             "fais-moi un rapport", "--json")
        self.assertEqual(code, 0, out)
        d = json.loads(out)
        self.assertEqual(d["resolved"]["doctypes"][0]["key"], "little-steps-report-short")
        self.assertEqual(d["language"]["value"], "fr")
        code, out = self.ddi("resolve", "--data-dir", str(data), "--brand", "little-steps", "--query",
                             "a report for our donors", "--lang", "fr", "--json")
        self.assertEqual(json.loads(out)["language"], {"value": "fr", "source": "override"})

    def test_f10_flyer_docx_names_fonts_even_without_a_docx_target(self):
        data = self.brand(B1, "little-steps")
        text = self.handoff(data, "little-steps-brochure-flyer-a4", "docx", "little-steps")
        self.assertNotIn("fonts: (embed vs. safe-stack per render target's Font Rule)\n    (not present", text)
        self.assertIn("no docx render target for this doctype", text)
        self.assertIn("brand fonts Nunito / Nunito Sans", text)


class TestB2Fintech(R6Case):
    def test_f5_tinted_background_gets_a_white_print_variant(self):
        self.brand(B2, "ledgerline")
        keys = {r["palette_key"]: r for r in self.kit["palettes.csv"]}
        self.assertEqual(set(keys), {"ledgerline-core", "ledgerline-print"})
        self.assertEqual(keys["ledgerline-print"]["Background"].upper(), "#FFFFFF")
        self.assertEqual(keys["ledgerline-core"]["Background"].lower(), "#fef7ff")
        self.assertIn("print-medium families use palette ledgerline-print", self.dry_run_output)
        rr = {r["doc_category"]: r for r in self.kit["doc-reasoning.csv"]}
        self.assertEqual(rr["ledgerline-invoice"]["Palette Key"], "ledgerline-print")
        self.assertEqual(rr["ledgerline-deck"]["Palette Key"], "ledgerline-core")   # projection keeps it

    def test_f5_print_background_keep_opts_out(self):
        self.brand(B2.replace("slug: ledgerline", "slug: ledgerline\nprint-background: keep"), "ledgerline")
        self.assertEqual([r["palette_key"] for r in self.kit["palettes.csv"]], ["ledgerline-core"])

    def test_f11_projection_contrast_threshold_reported_per_doctype(self):
        self.brand(B2, "ledgerline")
        out = self.dry_run_output
        self.assertRegex(out, r"WARN ledgerline-slide-deck-projection: proj-contrast-margin .*>= 7:1: below "
                              r"threshold -> .*accent 6\.\d\d")
        self.assertNotRegex(out, r"WARN ledgerline-invoice-tabular")

    def test_f5_legal_role_kept_for_invoices(self):
        self.brand(B2, "ledgerline")
        roles = {r["Role"] for r in self.kit["type-scales.csv"] if r["scale_key"] == "ledgerline-print"}
        self.assertIn("legal", roles)

    def test_f5_base_doctype_page_format_is_kept(self):
        self.brand(B2, "ledgerline")
        base = {r["doc_key"]: r for r in mbk.load_base_doctypes(self.skill_dir).values()}
        for r in self.kit["doctypes.csv"]:
            self.assertEqual(r["Page Format Key"], base[r["doc_key"].split("-", 1)[1]]["Page Format Key"])

    def test_f10_pptx_embeds_when_the_library_licence_allows(self):
        data = self.brand(B2, "ledgerline")     # Inter/Inter is a library pairing: licence copied
        text = self.handoff(data, "ledgerline-slide-deck-projection", "pptx", "ledgerline")
        self.assertIn("(embed): Inter / Inter", text)
        self.assertNotIn("does not allow embedding", text)

    def test_f10_pptx_falls_back_when_the_licence_is_unknown_and_says_so(self):
        data = self.brand(B2.replace("heading: Inter\nbody: Inter", "heading: Zilla Slab\nbody: Zilla Slab"),
                          "ledgerline")
        text = self.handoff(data, "ledgerline-slide-deck-projection", "pptx", "ledgerline")
        self.assertIn("does not allow embedding; safe-stack fallback instead", text)
        self.assertIn("brand fonts Zilla Slab", text)


class TestGrammarAndDerivations(MakeBrandKitTestCase):
    def b1(self, text=None):
        return (text or B1).replace("print-marketing-bold-flyer", _designs(self.skill_dir)["flyer"])

    def test_unknown_language_is_a_line_numbered_error(self):
        code, out = self._run([str(self._write_brand_md(self.b1(B1.replace("en, fr", "en, es")))), "--dry-run"])
        self.assertEqual(code, 1)
        self.assertIn("unknown language 'es'", out)

    def test_derived_rule_hair_skips_an_invisible_muted(self):
        text = self.b1(B1.replace("secondary: #484949", "secondary: #494949"))   # breaks the library match
        code, out = self._run([str(self._write_brand_md(text)), "--dry-run"])
        self.assertEqual(code, 0, out)
        line = next(l for l in out.splitlines() if l.strip().startswith("Rule Hair"))
        self.assertIn("palette secondary", line)          # muted #f4f8fb is 1.07:1, so it is skipped
        self.assertIn("CONVENTION", line)

    def test_rule_brand_is_accent_when_the_accent_is_text_safe(self):
        text = self.b1(B1.replace("#F28C28", "#1d70b8"))
        code, out = self._run([str(self._write_brand_md(text))])
        self.assertEqual(code, 0, out)
        with zipfile.ZipFile(self.outputs / "little-steps-brand-kit.zip") as zf:
            pal = list(csv.DictReader(io.StringIO(zf.read("data/palettes.csv").decode("utf-8"))))[0]
        self.assertEqual(pal["Rule Brand"], "#1d70b8")
        self.assertIn("accent", pal["Text-Safe Roles"])

    def test_failing_body_text_pair_stops_with_a_plain_message(self):
        text = self.b1(B1.replace("foreground: #0b0c0c", "foreground: #eeeeee"))
        code, out = self._run([str(self._write_brand_md(text)), "--dry-run"])
        self.assertEqual(code, 1)
        self.assertIn("STOP: foreground #eeeeee", out)

    def test_library_palettes_cli_shows_every_role(self):
        code, out = ddi.main(["library", "palettes", "--query", "govuk ink", "--limit", "1"]), None
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            ddi.main(["library", "palettes", "--query", "govuk ink", "--limit", "1"])
        text = buf.getvalue()
        for label in ("Primary:", "Secondary:", "Accent:", "Background:", "Foreground:", "Muted:",
                      "Text-Safe Roles:", "Fill-Only Roles:"):
            self.assertIn(label, text)


if __name__ == "__main__":
    unittest.main()
