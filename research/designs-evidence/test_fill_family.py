#!/usr/bin/env python3
"""Regression tests for fill_family.py:  python3 -m pytest research/designs-evidence/test_fill_family.py

1. cv: the script reproduces the committed section-9 CSVs BYTE-FOR-BYTE (generate_cv_fill.py's outputs).
2. The engine's ranking of the cv evidence matches the recorded combined table and the decided order.
3. --dry-run works for every family with evidence and never writes a file.
4. 82b A5 borrowing: twin detection.
"""
import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import fill_family as ff  # noqa: E402

RES = HERE.parent
CV_FILES = ("library/doc-styles/cv.csv", "library/doc-reasoning/cv.csv", "designs/cv.csv", "provenance/cv.csv")


def snapshot():
    """{path: (size, mtime_ns)} for every file the fill could touch."""
    out = {}
    for sub in ("library", "designs", "provenance", "designs-evidence"):
        for p in (RES / sub).rglob("*"):
            if p.is_file() and "__pycache__" not in p.parts:
                st = p.stat()
                out[str(p)] = (st.st_size, st.st_mtime_ns)
    return out


class TestCvRegression(unittest.TestCase):
    def test_cv_outputs_are_reproduced_byte_for_byte(self):
        built = ff.build("cv")
        for rel in CV_FILES:
            with self.subTest(file=rel):
                self.assertEqual(built[rel].encode("utf-8"), (RES / rel).read_bytes())

    def test_write_mode_produces_the_same_bytes_in_a_scratch_tree(self):
        with tempfile.TemporaryDirectory() as tmp:
            old = ff.RES
            ff.RES = Path(tmp)
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(ff.cmd_write("cv"), 0)
            finally:
                ff.RES = old
            for rel in CV_FILES:
                with self.subTest(file=rel):
                    self.assertEqual((Path(tmp) / rel).read_bytes(), (RES / rel).read_bytes())

    def test_check_mode_reports_same(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            self.assertEqual(ff.cmd_check("cv"), 0)
        self.assertNotIn("DIFFERS", buf.getvalue())

    def test_build_is_deterministic(self):
        self.assertEqual(ff.build("cv"), ff.build("cv"))


class TestEngineOnCv(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spec = ff.load_spec("cv")
        cls.items, cls.changes, cls.table = ff.engine_state(cls.spec)

    def test_evidence_counts(self):
        self.assertEqual(len(self.items), 80)
        self.assertEqual(sum(i.admissible for i in self.items), 56)
        self.assertEqual(len(self.changes), 32)      # cv-header-recode.md: 32 header codes changed

    def test_combined_table_matches_the_recorded_one(self):
        # research/designs-evidence/cv-header-recode.md "Combined (r2a)"
        want = {"1|serif|mono|plain-centered": (10, 0.1250), "1|sans|one-accent|plain-left": (8, 0.1000),
                "1|sans|one-accent|ruled": (6, 0.0750), "1|sans|mono|plain-left": (4, 0.0500),
                "1|sans|mono|split": (4, 0.0500), "1|serif|one-accent|plain-left": (3, 0.0375)}
        for arch, (k, combined) in want.items():
            with self.subTest(archetype=arch):
                self.assertEqual(self.table[arch]["K"], k)
                self.assertAlmostEqual(self.table[arch]["combined"], combined, places=4)

    def test_engine_order_agrees_with_the_decided_order(self):
        order, _ = ff.rank_step1(self.table, self.spec["corpora"], cap=9)
        decided = [d["archetype"] for d in self.spec["designs"] if d["archetype"] in order]
        self.assertEqual(decided, [a for a in order if a in decided])
        # the first six ranks are exactly the engine's first six
        self.assertEqual(order[:6], [d["archetype"] for d in self.spec["designs"][:6]])

    def test_engine_cap_leaves_the_recorded_five_outside(self):
        order, beyond = ff.rank_step1(self.table, self.spec["corpora"], cap=9)
        self.assertEqual((len(order), len(beyond)), (9, 5))

    def test_decisions_log_states_the_order_check(self):
        self.assertIn("appear in the engine's order: **yes**", ff.build("cv")["designs-evidence/cv-fill-log.md"])


class TestGatedIdentity(unittest.TestCase):
    def test_dropped_identity_feature_coarsens_the_archetype(self):
        spec = dict(ff.load_spec("cv"), dropped_identity=["header"])
        self.assertEqual(ff.spec_identity(spec), ["columns", "heading", "colour"])
        _items, _changes, table = ff.engine_state(spec)
        self.assertTrue(all(a.count("|") == 2 for a in table))
        self.assertIn("1|serif|mono", table)

    def test_dry_run_shows_the_agreement_files_gate_notes(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            ff.dry_run("invoice")
        self.assertIn("gate: invoice-agreement.md", buf.getvalue())


class TestSection8Engine(unittest.TestCase):
    """Fill engine rules (research/82a-clarifications-6.md): gate-dropped variants, palette evidence
    strength, typeface medium rule and pairing fallback."""

    @classmethod
    def setUpClass(cls):
        cls.lib = ff.Library()

    def proposals(self, family):
        spec = ff.load_spec(family)
        items, _c, table = ff.engine_state(spec)
        identity = ff.spec_identity(spec)
        dropped = frozenset(ff.dropped_variants(family, spec))
        default_style = ff.family_default_style(family)
        out = {}
        for d in spec["designs"]:
            if d["archetype"]:
                out[d["design_key"]] = ff.section8_proposal(
                    family, d["archetype"], table[d["archetype"]]["ex"], identity, self.lib, dropped, default_style)
        return spec, out

    def test_agreement_file_variants_are_read(self):
        self.assertEqual(ff.dropped_variants("proposal"), {"rules boxes", "density", "cover"})
        self.assertIn("density", ff.dropped_variants("invoice"))
        self.assertEqual(ff.dropped_variants("zz-no-such-family"), set())

    def test_dropped_rules_boxes_use_the_family_default_table_rules(self):
        spec, props = self.proposals("proposal")
        default = ff.family_default_style("proposal")
        self.assertEqual(default["style_key"], "report-classic-serif")
        for key, p in props.items():
            with self.subTest(design=key):
                self.assertEqual(p["style"]["Table Rules"], default["Table Rules"])
                self.assertTrue(any("dropped by the gate" in n for n in p["notes"]))

    def test_without_a_drop_the_corpus_modal_value_is_used(self):
        spec = ff.load_spec("cv")
        _i, _c, table = ff.engine_state(spec)
        a = "1|serif|mono|plain-centered"
        kept = ff.propose_style("cv", a, table[a]["ex"], ff.spec_identity(spec))
        dropped = ff.propose_style("cv", a, table[a]["ex"], ff.spec_identity(spec),
                                   frozenset({"rules boxes"}), {"Table Rules": "none"})
        self.assertEqual(kept["Table Rules"], "hairline")     # modal `rules`, cv branch
        self.assertEqual(dropped["Table Rules"], "none")      # family default

    def test_engine_palettes_and_typefaces_equal_the_decided_ones(self):
        """For every NEW reasoning row of cv and proposal the rules yield the decided palette and typeface
        (proposal's sans-heading rows via the pairing fallback; cv's serif rows via the medium rule)."""
        for family in ("cv", "proposal"):
            spec, props = self.proposals(family)
            by_key = {d["design_key"]: d for d in spec["designs"]}
            for row in spec["reasoning"]["rows"]:
                key = next(k for k, d in by_key.items() if d["Reasoning Key"] == row["doc_category"])
                if key not in props:
                    continue
                with self.subTest(family=family, design=key):
                    p = props[key]
                    self.assertEqual(p["palettes"][0][0], row["Palette Key"])
                    self.assertEqual(p["typefaces"][0], row["Typeface Key"])

    def test_medium_rule_rejects_a_screen_scaled_typeface_for_print(self):
        ident = ["columns", "heading", "colour", "header"]
        keys, notes = ff.propose_typeface("1|serif|mono|plain-centered", ident, self.lib.typefaces,
                                          self.lib.pop, "serif", "print", self.lib.media)
        self.assertEqual(keys[0], "safe-serif-times")
        self.assertNotIn("safe-serif-georgia", keys)
        self.assertTrue(any("safe-serif-georgia" in n and "medium rule" in n for n in notes))
        keys, _ = ff.propose_typeface("1|serif|mono|plain-centered", ident, self.lib.typefaces,
                                      self.lib.pop, "serif", "screen", self.lib.media)
        self.assertIn("safe-serif-georgia", keys)               # a screen family may use its report-screen scale

    def test_pairing_fallback_keeps_the_heading_class(self):
        ident = ["columns", "heading", "colour", "header"]
        keys, notes = ff.propose_typeface("1|sans|mono|plain-left", ident, self.lib.typefaces, self.lib.pop,
                                          "serif", "print", self.lib.media)
        self.assertEqual(keys[0], "lib-roboto")                 # sans heading, lowest popularity, print scale
        self.assertTrue(any("rule R2" in n for n in notes))
        strict, no_notes = ff.propose_typeface("1|sans|mono|plain-left", ident, self.lib.typefaces, self.lib.pop,
                                               "sans", "print", self.lib.media)
        self.assertEqual(strict[0], "lib-roboto")
        self.assertFalse(any("rule R2" in n for n in no_notes))

    def test_palette_fetched_authority_outranks_search_corroborated(self):
        ev = self.lib.evidence
        self.assertEqual(ev["lib-carbon-mono"], 0)              # authority, fetched
        self.assertEqual(ev["cv-dach-formal"], 1)               # authority, search-corroborated (legacy backfill)
        mono = [k for k, _ in ff.propose_palette("mono", self.lib.palettes, ev)]
        self.assertEqual(mono[0], "lib-carbon-mono")
        self.assertLess(mono.index("lib-carbon-mono"), mono.index("cv-dach-formal"))

    def test_one_accent_palette_needs_accent_contrast_and_avoids_a7_blues(self):
        cands = ff.propose_palette("one-accent", self.lib.palettes, self.lib.evidence)
        keys = [k for k, _ in cands]
        self.assertEqual(keys[0], "lib-atlassian-ink")
        self.assertNotIn("lib-carbon-dark-slide", keys)         # accent 3.6:1 on its background
        row = {r["palette_key"]: r for r in self.lib.palettes}
        for k in keys:
            self.assertNotIn(row[k]["Accent"].lower(), ff.A7_BLUES)
            self.assertGreaterEqual(ff.contrast(row[k]["Accent"], row[k]["Background"]), 4.5)

    def test_palette_class_is_a_hue_count_and_fill_blocks_is_served_by_fill_only_roles(self):
        row = {r["palette_key"]: r for r in self.lib.palettes}
        self.assertEqual(ff.palette_class(row["lib-carbon-mono"]), "mono")
        self.assertEqual(ff.palette_class(row["lib-atlassian-ink"]), "one-accent")
        self.assertTrue(ff.palette_serves("fill-blocks", row["lib-atlassian-ink"]))   # muted is fill-only

    def test_dry_run_prints_palette_and_typeface_and_drops(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            ff.dry_run("proposal")
        out = buf.getvalue()
        self.assertIn("variants dropped by the gate (family default used): cover, density, rules boxes", out)
        self.assertIn("palette=lib-carbon-mono", out)
        self.assertIn("typeface=safe-serif-times", out)


class TestCvPrintScaleCorrection(unittest.TestCase):
    def test_no_cv_fill_row_uses_a_screen_scaled_typeface(self):
        import csv
        media = ff.scale_media()
        tf = {r["typeface_key"]: r for r in ff._lib_rows("typefaces")}
        with (RES / "library/doc-reasoning/cv.csv").open(encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                with self.subTest(row=row["doc_category"]):
                    self.assertIn("print", media[tf[row["Typeface Key"]]["Scale Key"]])

    def test_the_three_corrected_rows_use_safe_serif_times(self):
        import csv
        with (RES / "library/doc-reasoning/cv.csv").open(encoding="utf-8", newline="") as f:
            rows = {r["doc_category"]: r for r in csv.DictReader(f)}
        for key in ("cv-serif-plain-centered", "cv-serif-mono-split", "cv-serif-accent-plain-left"):
            self.assertEqual(rows[key]["Typeface Key"], "safe-serif-times")


class TestDryRun(unittest.TestCase):
    FAMILIES = ("deck", "invoice", "letter", "cover-letter", "report", "poster", "memo", "brochure",
                "infographic", "flyer", "proposal", "quote", "cv")

    def test_dry_run_prints_a_ranking_and_writes_nothing(self):
        before = snapshot()
        for fam in self.FAMILIES:
            with self.subTest(family=fam):
                buf = io.StringIO()
                with contextlib.redirect_stdout(buf):
                    rc = ff.dry_run(fam)
                self.assertEqual(rc, 0, buf.getvalue())
                self.assertIn("(dry-run: nothing written)", buf.getvalue())
                self.assertIn("proposed step-1 ranking", buf.getvalue())
        self.assertEqual(before, snapshot())

    def test_family_without_a_parsable_table_is_reported_not_crashed(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = ff.dry_run("zz-no-such-family")      # never has evidence files
        self.assertEqual(rc, 1)
        self.assertIn("nothing to rank", buf.getvalue())

    def test_write_without_a_spec_refuses(self):
        with self.assertRaises(SystemExit):
            ff.build("deck")


class TestBorrowing(unittest.TestCase):
    def test_structural_twins(self):
        self.assertTrue(ff.twin_check("quote", "invoice")[0])
        self.assertTrue(ff.twin_check("whitepaper", "report")[0])
        self.assertFalse(ff.twin_check("cv", "deck")[0])

    def test_borrow_mode_is_dry_run_only_and_labels_designs(self):
        buf = io.StringIO()
        before = snapshot()
        with contextlib.redirect_stdout(buf):
            self.assertEqual(ff.cmd_borrow("quote", "invoice"), 0)
        self.assertIn("structural twins", buf.getvalue())
        self.assertEqual(before, snapshot())


if __name__ == "__main__":
    unittest.main()
