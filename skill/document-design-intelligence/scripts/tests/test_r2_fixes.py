#!/usr/bin/env python3
"""research/86 R2 fixes: brand-aware --design (F1), doc-reasoning Design Key
(F2), blank kit bias terms (F3), all-doc BM25 terms (F4), and advisories.
Runs against a snapshot of data/base with a freshly made brand kit's rows
appended (what merge_brand_kit does), addressed by --data-dir."""
import contextlib
import csv
import io
import json
import sys
import zipfile
import unittest
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))
from test_make_brand_kit import (MakeBrandKitTestCase, DESIGNS_BRAND_MD,  # noqa: E402
                                 SCALES_BRAND_MD)
import ddi  # noqa: E402


def _append(path: Path, rows):
    with path.open(encoding="utf-8", newline="") as f:
        cols = next(csv.reader(f))
    with path.open("a", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n")
        for r in rows:
            w.writerow({c: r.get(c, "") for c in cols})


class R2Case(MakeBrandKitTestCase):
    def merged(self, text=DESIGNS_BRAND_MD):
        code, out = self._run([str(self._write_brand_md(text))])
        self.assertEqual(code, 0, out)
        self.kit = {}
        with zipfile.ZipFile(self.outputs / "ens-brand-kit.zip") as zf:
            for n in zf.namelist():
                if n.endswith(".csv"):
                    rows = list(csv.DictReader(io.StringIO(zf.read(n).decode("utf-8"))))
                    self.kit[Path(n).name] = rows
                    _append(self.skill_dir / "data" / "base" / Path(n).name, rows)
        return self.skill_dir / "data"

    def ddi(self, *argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = ddi.main(list(argv))
        return code, out.getvalue(), err.getvalue()

    def resolved(self, data, *argv):
        code, out, _ = self.ddi("resolve", "--data-dir", str(data), "--json", *argv)
        self.assertEqual(code, 0, out)
        return json.loads(out)


class TestF1BrandDesign(R2Case):
    def test_design_keeps_brand_palette_and_typeface(self):
        data = self.merged()
        base = self.resolved(data, "--brand", "ens", "--doctype", "ens-cv-uk")
        over = self.resolved(data, "--brand", "ens", "--doctype", "ens-cv-uk",
                             "--design", "cv-serif-plain-centered")
        keys = lambda r, t: [x["key"] for x in r["resolved"][t]]  # noqa: E731
        self.assertEqual(keys(base, "palettes"), keys(over, "palettes"))
        self.assertEqual(keys(base, "typefaces"), keys(over, "typefaces"))
        self.assertNotEqual(keys(base, "doc-styles"), keys(over, "doc-styles"))

    def test_loaded_data_not_mutated_by_override(self):
        data = self.merged()
        before = (data / "base" / "doc-reasoning.csv").read_bytes()
        self.resolved(data, "--brand", "ens", "--doctype", "ens-cv-uk", "--design", "cv-serif-plain-centered")
        self.assertEqual(before, (data / "base" / "doc-reasoning.csv").read_bytes())


class TestF2DesignKey(R2Case):
    def test_base_rows_carry_derived_design_key(self):
        rows = {r["doc_category"]: r for r in
                csv.DictReader(open(HERE.parent.parent / "data/base/doc-reasoning.csv", encoding="utf-8"))}
        self.assertEqual(rows["cv-ats-strict"]["Design Key"], "cv-ats-strict")
        self.assertEqual(rows["print-marketing"]["Design Key"], "")  # shared by 3 families

    def test_kit_rows_set_design_key(self):
        self.merged()
        rr = {r["doc_category"]: r for r in self.kit["doc-reasoning.csv"]}
        self.assertEqual(rr["ens-cv"]["Design Key"], "cv-ats-strict")
        self.assertEqual(rr["ens-invoice"]["Design Key"], "invoice-tabular")

    def test_designs_default_marker_for_brand_doctype(self):
        data = self.merged()
        code, out, _ = self.ddi("designs", "--doctype", "ens-cv-uk", "--json", "--data-dir", str(data))
        self.assertEqual(code, 0)
        defaults = [d["design_key"] for d in json.loads(out)["designs"] if d["is_default"]]
        self.assertEqual(defaults, ["cv-ats-strict"])

    def test_handoff_design_line_for_brand_doctype(self):
        data = self.merged()
        r = self.resolved(data, "--brand", "ens", "--doctype", "ens-cv-uk")
        line = ddi._design_handoff_line(r["resolved"], data)
        self.assertIn("design:", line or "")


class TestF3BiasTerms(R2Case):
    def test_kit_bias_terms_blank_style_kept(self):
        self.merged()
        for r in self.kit["doc-reasoning.csv"]:
            self.assertEqual((r["Palette Bias Terms"], r["Typeface Bias Terms"]), ("", ""))
            self.assertTrue(r["Style Bias Terms"])


class TestF4Bm25(R2Case):
    def test_all_doc_term_does_not_reorder(self):
        code, out, _ = self.ddi("designs", "--doctype", "cv-uk", "--query", "cv", "--json")
        d = json.loads(out)
        self.assertEqual(d["method"], "rank")
        ranks = [int(x["rank"]) for x in d["designs"]]
        self.assertEqual(ranks, sorted(ranks))
        self.assertNotIn("score", d["designs"][0])

    def test_discriminating_term_still_bm25(self):
        code, out, _ = self.ddi("designs", "--doctype", "cv-uk", "--query", "cv academic", "--json")
        d = json.loads(out)
        self.assertEqual(d["method"], "bm25")
        self.assertEqual(d["designs"][0]["design_key"], "cv-academic")


class TestAdvisories(R2Case):
    def test_library_unknown_brand_errors(self):
        code, out, _ = self.ddi("library", "palettes", "--brand", "nosuch")
        self.assertEqual(code, 1)
        self.assertIn("NO SUCH BRAND", out)

    def test_zero_score_query_reports_rank(self):
        code, out, _ = self.ddi("library", "palettes", "--query", "zzzqqq", "--json")
        self.assertEqual(json.loads(out)["method"], "rank")

    def test_convention_provenance_wording(self):
        code, out, _ = self.ddi("library", "palettes", "--limit", "1")
        self.assertIn("convention -- no external source", out)
        self.assertNotIn("unnamed source", out)

    def test_type_scales_scope_filter(self):
        data = self.merged(SCALES_BRAND_MD)
        d = str(data)
        _, out, _ = self.ddi("library", "type-scales", "--json", "--data-dir", d)
        self.assertNotIn("ens-print", [e["key"] for e in json.loads(out)["entries"]])
        _, out, _ = self.ddi("library", "type-scales", "--json", "--brand", "ens", "--data-dir", d)
        keys = [e["key"] for e in json.loads(out)["entries"]]
        self.assertTrue(keys and all(k.startswith("ens-") for k in keys))

    def test_headers_case_insensitive(self):
        text = (DESIGNS_BRAND_MD.replace("## Designs", "## DESIGNS")
                .replace("cv: cv-ats-strict", "CV: cv-ats-strict"))
        code, out = self._run([str(self._write_brand_md(text)), "--dry-run"])
        self.assertEqual(code, 0, out)

    def test_orphan_design_family_warns_on_stderr(self):
        text = DESIGNS_BRAND_MD.replace("invoice: invoice-tabular", "deck: deck-generic")
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            code, _ = self._run([str(self._write_brand_md(text))])
        self.assertEqual(code, 0)
        self.assertIn("deck", err.getvalue())
        self.assertIn("WARNING", err.getvalue())


if __name__ == "__main__":
    unittest.main()
