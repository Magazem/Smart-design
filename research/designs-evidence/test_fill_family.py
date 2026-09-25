#!/usr/bin/env python3
"""Regression tests for fill_family.py:  python3 -m pytest research/designs-evidence/test_fill_family.py

1. cv: the script reproduces the committed section-9 CSVs BYTE-FOR-BYTE (the engine's own output).
2. The engine's ranking of the cv evidence (admissible-only shares, C21) and the plan it derives.
R7 (research/82a-r7-rulings.md): tests named R7_n below.
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

    def test_combined_table_counts_admissible_exemplars_only_R7_1(self):
        # research/designs-evidence/cv-header-recode.md "Combined (r2a)" minus the inadmissible exemplars (C21):
        # `1|sans|one-accent|ruled` had 6 items of which NPM:038 and NPM:054 are inadmissible
        want = {"1|serif|mono|plain-centered": (10, 0.1250), "1|sans|one-accent|plain-left": (8, 0.1000),
                "1|sans|one-accent|ruled": (4, 0.0500), "1|sans|mono|plain-left": (4, 0.0500),
                "1|sans|mono|split": (4, 0.0500), "1|serif|one-accent|plain-left": (3, 0.0375)}
        for arch, (k, combined) in want.items():
            with self.subTest(archetype=arch):
                self.assertEqual(self.table[arch]["K"], k)
                self.assertAlmostEqual(self.table[arch]["combined"], combined, places=4)
        ruled = self.table["1|sans|one-accent|ruled"]
        self.assertEqual((ruled["K"], ruled["inadm"], ruled["k"]["NPM"]), (4, 2, 4))
        self.assertNotIn("NPM:038", [e.id for e in ruled["ex"]])

    def test_ruled_archetype_moves_below_the_two_050_ties_R7_1(self):
        order, _ = ff.rank_step1(self.table, self.spec["corpora"], cap=99)
        self.assertEqual(order[:5], ["1|serif|mono|plain-centered", "1|sans|one-accent|plain-left",
                                     "1|sans|mono|split", "1|sans|mono|plain-left", "1|sans|one-accent|ruled"])

    def test_plan_is_ranked_by_the_engine_not_by_the_spec_order(self):
        plan = ff.plan_designs("cv", self.spec, self.table)
        shipped = [s["design"]["design_key"] for s in plan["shipped"]]
        self.assertEqual(shipped[:2], ["cv-serif-plain-centered", "cv-eu-europass"])
        shuffled = dict(self.spec, designs=list(reversed(self.spec["designs"])))
        plan2 = ff.plan_designs("cv", shuffled, self.table)
        self.assertEqual(shipped, [s["design"]["design_key"] for s in plan2["shipped"]])

    def test_cap_is_ten_and_the_doctype_default_takes_the_last_ranked_slot_R7_7(self):
        plan = ff.plan_designs("cv", self.spec, self.table)
        self.assertLessEqual(len(plan["shipped"]), ff.CAP)
        keys = [s["design"]["design_key"] for s in plan["shipped"]]
        self.assertIn("cv-us-uk-designed", keys)          # default, archetype ranks 13th
        self.assertNotIn("cv-sans-accent-split", keys)    # displaced from the last ranked slot
        self.assertEqual([s["rank"] for s in plan["shipped"]], list(range(1, len(keys) + 1)))

    def test_identity_duplicate_is_retired_and_pending_is_not_shipped_R7_7_R7_10(self):
        spec = dict(self.spec)
        spec["designs"] = [dict(d) for d in self.spec["designs"]]
        for d in spec["designs"]:
            d.pop("pending", None)
        plan = ff.plan_designs("cv", spec, self.table)
        retired = dict(plan["retired"])
        self.assertIn("cv-dach-tabular", retired)            # same identity values as cv-academic (default)
        self.assertIn("identity duplicate", retired["cv-dach-tabular"])
        plan = ff.plan_designs("cv", self.spec, self.table)
        self.assertEqual([k for k, _ in plan["pending"]], ["cv-dach-tabular"])
        self.assertNotIn("cv-dach-tabular", [s["design"]["design_key"] for s in plan["shipped"]])

    def test_merged_authority_designs_are_class_ranked_with_an_authority_row_R7_F10(self):
        import csv
        with (RES / "designs/cv.csv").open(encoding="utf-8", newline="") as f:
            classes = {r["design_key"]: r["Evidence Class"] for r in csv.DictReader(f)}
        self.assertEqual(classes["cv-eu-europass"], "ranked")
        self.assertEqual(classes["cv-academic"], "convention")
        with (RES / "provenance/cv.csv").open(encoding="utf-8", newline="") as f:
            prov = [r for r in csv.DictReader(f) if r["Row Key"] == "cv-eu-europass" and r["Table"] == "designs"]
        self.assertIn("authority", {r["Evidence Class"] for r in prov})

    def test_decisions_log_states_the_order_check(self):
        self.assertIn("spec-vs-engine violations: **0**", ff.build("cv")["designs-evidence/cv-fill-log.md"])


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
    """Fill engine section-8 rules: gate-dropped variants, palette evidence order (R7-3), typeface
    medium rule (R7-2), pairing fallback (R2, ratified), declared font (R7-9)."""

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

    def test_engine_fills_every_new_row_from_its_own_proposals(self):
        """No spec row carries a palette/typeface/style key: the resolved rows ARE the engine's first
        candidates (proposal's sans rows via the pairing fallback; cv's serif rows via the medium rule)."""
        for family in ("cv", "proposal"):
            spec = ff.load_spec(family)
            self.assertEqual(spec["reasoning"]["rows"], [])
            res = ff.resolve_family(family, spec)
            self.assertEqual(res["violations"], [])
            self.assertTrue(res["rows"])
            for row in res["rows"]:
                p = res["props"][row["_design"]]
                with self.subTest(family=family, design=row["_design"]):
                    self.assertEqual(row["Palette Key"], p["palettes"][0][0])
                    self.assertEqual(row["Typeface Key"], p["typefaces"][0])

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


class TestR7Rules(unittest.TestCase):
    """82a-r7-rulings.md R7-2 ... R7-11 on synthetic evidence and on the library."""

    @classmethod
    def setUpClass(cls):
        cls.lib = ff.Library("cv")
        cls.ident = ["columns", "heading", "colour", "header"]

    @staticmethod
    def item(id_, corpus, pos, adm=True, **feats):
        return ff.Item(id_, corpus, pos, "x", dict(feats), adm)

    # R7-1 ----------------------------------------------------------------------------------------
    def test_R7_1_inadmissible_items_stay_in_n_but_never_count_or_break_ties(self):
        corpora = [{"id": "A", "n": 10, "level": "L1"}]
        items = [self.item("A:001", "A", 1, True, columns="1", heading="sans", colour="mono", header="split", photo="no"),
                 self.item("A:002", "A", 2, True, columns="1", heading="sans", colour="mono", header="split", photo="no"),
                 self.item("A:003", "A", 3, False, columns="1", heading="sans", colour="mono", header="split", photo="yes")]
        t = ff.combined_table(items, corpora, self.ident)["1|sans|mono|split"]
        self.assertEqual((t["K"], t["inadm"], t["share"]["A"]), (2, 1, 0.2))
        self.assertEqual([e.id for e in t["ex"]], ["A:001", "A:002"])
        self.assertEqual(ff.modal_variant(t["ex"] + [items[2], items[2]], "photo"), "no")   # inadmissible ignored

    def test_R7_1_an_archetype_with_one_admissible_exemplar_is_not_eligible(self):
        corpora = [{"id": "A", "n": 10, "level": "L1"}]
        items = [self.item("A:001", "A", 1, True, columns="1", heading="sans", colour="mono", header="split"),
                 self.item("A:002", "A", 2, False, columns="1", heading="sans", colour="mono", header="split")]
        table = ff.combined_table(items, corpora, self.ident)
        self.assertEqual(ff.rank_step1(table, corpora, 10)[0], [])

    # R7-6 ----------------------------------------------------------------------------------------
    def test_R7_6_corpus_tie_order_is_level_then_n_then_id_not_spec_order(self):
        cs = [{"id": "Z", "n": 40, "level": "L2"}, {"id": "B", "n": 40, "level": "L1"},
              {"id": "A", "n": 20, "level": "L1"}, {"id": "C", "n": 40, "level": "L1"}]
        self.assertEqual([c["id"] for c in ff.corpus_order(cs)], ["B", "C", "A", "Z"])
        self.assertEqual([c["id"] for c in ff.corpus_order(list(reversed(cs)))], ["B", "C", "A", "Z"])

    def test_R7_6_a_tie_is_broken_by_the_higher_level_corpus_whatever_the_listing_order(self):
        def mk(cs):
            items = []
            for a, cid in (("x", "L2C"), ("y", "L1C")):     # same combined share: x from the L2 corpus, y from L1
                for n in (1, 2):
                    items.append(self.item(f"{cid}:00{n}", cid, n, True, columns="1", heading=a, colour="mono", header="split"))
            return ff.rank_step1(ff.combined_table(items, cs, self.ident), cs, 9)[0]
        cs = [{"id": "L2C", "n": 10, "level": "L2"}, {"id": "L1C", "n": 10, "level": "L1"}]
        self.assertEqual(mk(cs), mk(list(reversed(cs))))
        self.assertEqual(mk(cs)[0], "1|y|mono|split")

    # R7-4 ----------------------------------------------------------------------------------------
    def test_R7_4_check_fails_when_the_spec_differs_from_the_engine_without_a_ratified_override(self):
        spec = ff.load_spec("cv")
        spec["reasoning"] = dict(spec["reasoning"], rows=[{"doc_category": "cv-sans-accent-ruled",
                                                            "Palette Key": "lib-carbon-mono"}])
        bad = ff.resolve_family("cv", spec)["violations"]
        self.assertTrue(any("cv-sans-accent-ruled Palette Key" in v for v in bad), bad)

    def test_R7_4_a_ratified_override_is_accepted_and_counted(self):
        spec = ff.load_spec("cv")
        spec["reasoning"] = dict(spec["reasoning"], rows=[{
            "doc_category": "cv-sans-accent-ruled", "Palette Key": "lib-carbon-mono",
            "override": "82a-r7-rulings.md R7-3"}])
        res = ff.resolve_family("cv", spec)
        self.assertEqual(res["violations"], [])
        self.assertEqual(res["overrides"], 1)
        row = next(r for r in res["rows"] if r["doc_category"] == "cv-sans-accent-ruled")
        self.assertEqual(row["Palette Key"], "lib-carbon-mono")

    def test_R7_4_an_override_must_cite_an_existing_ratified_rule(self):
        self.assertTrue(ff._override_ok("82a-r7-rulings.md R7-3"))
        self.assertTrue(ff._override_ok("82a-clarifications-6.md R1"))        # now RATIFIED (status line wins)
        self.assertFalse(ff._override_ok("82a-r7-rulings.md R7-99"))          # no such rule
        self.assertFalse(ff._override_ok("82a-does-not-exist.md R1"))
        self.assertFalse(ff._override_ok(""))
        self.assertFalse(ff._override_ok("because I said so"))

    def test_R7_4_a_new_style_row_that_contradicts_the_mapping_is_a_violation(self):
        spec = ff.load_spec("cv")
        spec["doc_styles"] = [dict(s, **{"Table Rules": "none"}) if s["style_key"] == "cv-sans-accent-ruled" else s
                              for s in spec["doc_styles"]]
        bad = ff.resolve_family("cv", spec)["violations"]
        self.assertTrue(any("cv-sans-accent-ruled" in v and "Table Rules" in v for v in bad), bad)

    def test_R7_4_write_refuses_while_a_violation_stands(self):
        spec = ff.load_spec("cv")
        spec["reasoning"] = dict(spec["reasoning"], rows=[{"doc_category": "cv-sans-accent-ruled", "Typeface Key": "safe-serif-georgia"}])
        old = ff.load_spec
        ff.load_spec = lambda fam: spec
        try:
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                self.assertEqual(ff.cmd_write("cv"), 1)
                self.assertEqual(ff.cmd_check("cv"), 1)
        finally:
            ff.load_spec = old
        self.assertIn("VIOLATION", buf.getvalue())

    # R7-2 ----------------------------------------------------------------------------------------
    def test_R7_2_no_resolved_print_row_uses_a_screen_or_projection_scale(self):
        for family in ("cv", "proposal"):
            res = ff.resolve_family(family, ff.load_spec(family))
            tf = {r["typeface_key"]: r for r in self.lib.typefaces}
            for row in res["rows"]:
                with self.subTest(design=row["_design"]):
                    self.assertIn("print", self.lib.media[tf[row["Typeface Key"]]["Scale Key"]])

    def test_R7_2_an_override_cannot_smuggle_in_a_screen_typeface(self):
        spec = ff.load_spec("cv")
        spec["reasoning"] = dict(spec["reasoning"], rows=[{
            "doc_category": "cv-serif-plain-centered", "Typeface Key": "safe-serif-georgia",
            "override": "82a-r7-rulings.md R7-2"}])
        bad = ff.resolve_family("cv", spec)["violations"]
        self.assertTrue(any("medium rule" in v for v in bad), bad)

    # R7-5 ----------------------------------------------------------------------------------------
    def _style(self, key, checklist, table="hairline", brand="0", kw="cv"):
        return {"style_key": key, "Table Rules": table, "Table Fills": "none", "Emphasis Mechanism": "weight",
                "Field Style": "none", "Rule Brand pt": brand, "Checklist": checklist, "Keywords": kw, "Best For": ""}

    def _proposal(self, photo=None):
        return {"Table Rules": "hairline", "Table Fills": "none", "Emphasis Mechanism": "weight",
                "Field Style": "none", "Rule Brand pt": "0", "Checklist": ["Keep single column"], "photo": photo}

    def test_R7_5_family_prefix_is_the_family_being_filled_not_cv(self):
        rows = [self._style("cv-a", "Keep single column"), self._style("invoice-z", "Keep single column"),
                self._style("invoice-b", "Keep single column"), self._style("aaa", "Keep single column")]
        self.assertEqual(ff.reuse_candidates(self._proposal(), rows, "invoice"), ["invoice-b", "invoice-z", "aaa", "cv-a"])
        self.assertEqual(ff.reuse_candidates(self._proposal(), rows, "cv"), ["cv-a", "aaa", "invoice-b", "invoice-z"])

    def test_R7_5_photo_contradiction_rejects_a_reuse_both_ways(self):
        omit = self._style("cv-omit", "Keep single column;Omit photo")
        allow = self._style("cv-allow", "Keep single column;Photo permitted as a modest avatar")
        plain = self._style("cv-plain", "Keep single column")
        self.assertEqual(ff.reuse_candidates(self._proposal("yes"), [omit, allow, plain], "cv"), ["cv-allow", "cv-plain"])
        self.assertEqual(ff.reuse_candidates(self._proposal("no"), [omit, allow, plain], "cv"), ["cv-omit", "cv-plain"])
        self.assertEqual(ff.reuse_candidates(self._proposal(None), [omit, allow, plain], "cv"),
                         ["cv-allow", "cv-omit", "cv-plain"])

    def test_R7_5_the_typeface_proposal_honours_the_body_class(self):
        keys, notes = ff.propose_typeface("1|serif|mono|plain-centered", self.ident, self.lib.typefaces, self.lib.pop,
                                          "sans", "print", self.lib.media)
        rows = {r["typeface_key"]: r for r in self.lib.typefaces}
        self.assertTrue(all(rows[k]["Category Contrast"] == "serif-sans" for k in keys), keys)
        self.assertFalse(notes and any("relaxed" in n for n in notes))

    # R7-8 ----------------------------------------------------------------------------------------
    def test_R7_8_a_region_specific_style_is_not_reusable_for_a_generic_design(self):
        europass = self._style("cv-europass", "Keep single column;Follow the Europass section order")
        self.assertEqual(ff.reuse_candidates(self._proposal(), [europass], "cv"), [])

    def test_R7_8_contradicting_bias_tokens_are_blanked_and_logged(self):
        defaults = {"Style Bias Terms": "restrained, single column", "Palette Bias Terms": "monochrome, ink on white, quiet",
                    "Typeface Bias Terms": "safe stack, ubiquitous", "Doc Conditions": "", "Severity": "fail"}
        out, blanked = ff.blank_bias(defaults, {"columns": "1", "heading": "sans", "colour": "one-accent"}, "lib-roboto")
        self.assertEqual(out["Palette Bias Terms"], "quiet")
        self.assertEqual(out["Typeface Bias Terms"], "")
        self.assertEqual(out["Style Bias Terms"], "restrained, single column")
        self.assertEqual(len(blanked), 4)
        out, blanked = ff.blank_bias(defaults, {"columns": "1", "heading": "serif", "colour": "mono"}, "safe-serif-times")
        self.assertEqual(blanked, [])

    def test_R7_8_shipped_cv_accent_rows_no_longer_advertise_monochrome(self):
        import csv
        with (RES / "library/doc-reasoning/cv.csv").open(encoding="utf-8", newline="") as f:
            rows = {r["doc_category"]: r for r in csv.DictReader(f)}
        self.assertNotIn("monochrome", rows["cv-sans-accent-ruled"]["Palette Bias Terms"])
        self.assertIn("monochrome", rows["cv-sans-mono-split"]["Palette Bias Terms"])

    # R7-9 ----------------------------------------------------------------------------------------
    def test_R7_9_declared_office_font_selects_the_safe_row_of_that_class(self):
        keys, notes = ff.propose_typeface("1|sans|mono|plain-left", self.ident, self.lib.typefaces, self.lib.pop,
                                          None, "print", self.lib.media, "Arial", True)
        self.assertEqual(keys[0], "safe-sans-arial")
        self.assertTrue(any("declared-font branch" in n for n in notes))
        keys, _ = ff.propose_typeface("1|serif|mono|plain-left", self.ident, self.lib.typefaces, self.lib.pop,
                                      None, "print", self.lib.media, "Georgia", True)
        self.assertNotIn("safe-serif-georgia", keys)                  # print medium rule still applies
        self.assertEqual(keys[0], "safe-serif-times")

    def test_R7_9_a_non_bundled_declared_font_runs_the_ordinary_branch_and_no_font_is_logged(self):
        keys, notes = ff.propose_typeface("1|sans|mono|plain-left", self.ident, self.lib.typefaces, self.lib.pop,
                                          None, "print", self.lib.media, "Lato", True)
        self.assertTrue(any("not OS/Office-bundled" in n for n in notes))
        _, notes = ff.propose_typeface("1|sans|mono|plain-left", self.ident, self.lib.typefaces, self.lib.pop,
                                       None, "print", self.lib.media)
        self.assertTrue(any("not evaluable" in n for n in notes))

    def test_R7_9_modal_declared_font_is_read_from_the_corpus_column(self):
        exs = [self.item(f"A:00{n}", "A", n, True, font=f) for n, f in enumerate(["Arial", "Arial", "Lato"], 1)]
        self.assertEqual(ff.modal_variant(exs, "font"), "Arial")
        self.assertEqual(ff.canon("Declared font"), "font")

    # R7-11 ---------------------------------------------------------------------------------------
    def test_R7_11_palette_classification_covers_mono_one_accent_and_multi_and_never_fill_blocks(self):
        classes = {}
        for r in self.lib.palettes:
            if r.get("Brand Scope", "generic") == "generic":
                classes.setdefault(ff.palette_class(r), []).append(r["palette_key"])
        self.assertEqual(set(classes), {"mono", "one-accent", "multi"})     # a Fill-Only Roles column never yields fill-blocks
        self.assertGreater(len(classes["mono"]), 1)
        self.assertGreater(len(classes["one-accent"]), 1)
        for colour in ("mono", "one-accent", "multi"):
            self.assertTrue(ff.propose_palette(colour, self.lib.palettes, self.lib.evidence), colour)
        row = {r["palette_key"]: r for r in self.lib.palettes}
        self.assertEqual(ff.palette_class(row["lib-radix-sand"]), "mono")            # accent S < 0.20
        self.assertEqual(ff.palette_class({"Primary": "#000000", "Accent": "#c8102e", "Secondary": "#0033a0"}), "multi")
        self.assertEqual(ff.palette_class({"Primary": "#000000", "Accent": "#c8102e"}), "one-accent")
        self.assertEqual(ff.palette_class({"Primary": "#222222", "Accent": "#7d7d7d"}), "mono")

    def test_R7_11_a_palette_with_fill_only_roles_serves_fill_blocks_only_by_that_column(self):
        self.assertTrue(ff.palette_serves("fill-blocks", {"Primary": "#000000", "Fill-Only Roles": "muted"}))
        self.assertFalse(ff.palette_serves("fill-blocks", {"Primary": "#000000", "Fill-Only Roles": ""}))

    # R7-3 ----------------------------------------------------------------------------------------
    def test_R7_3_palette_ties_go_to_the_lowest_key_in_byte_order(self):
        base = {"Foreground": "#000000", "Background": "#ffffff", "Primary": "#000000", "Accent": "", "Brand Scope": "generic"}
        pals = [dict(base, palette_key=k) for k in ("lib-b", "Lib-z", "lib-a")]
        got = [k for k, _ in ff.propose_palette("mono", pals, {})]
        self.assertEqual(got, ["Lib-z", "lib-a", "lib-b"])                # uppercase sorts before lowercase in bytes

    def test_R7_3_no_spec_cites_a_draft_rule_file_and_labels_say_ratified(self):
        src = (HERE / "fill_family.py").read_text(encoding="utf-8")
        self.assertNotIn("unratified", src)
        self.assertNotIn("NOT ratified", src)
        self.assertIn("rule R2, research/82a-clarifications-6.md", src)

    def test_ratified_check_reads_the_status_not_historical_wording(self):
        import shutil
        with tempfile.TemporaryDirectory() as tmp:
            old = ff.RES
            ff.RES = Path(tmp)
            try:
                (Path(tmp) / "82a-x.md").write_text("# x\n\nStatus: DRAFT, not ratified.\n\nR1 -- a rule\n", encoding="utf-8")
                self.assertFalse(ff._override_ok("82a-x.md R1"))
                (Path(tmp) / "82a-y.md").write_text("# y\n\nStatus: **RATIFIED** (was a draft, not ratified before)\n\n## R1 -- a rule\n",
                                                    encoding="utf-8")
                self.assertTrue(ff._override_ok("82a-y.md R1"))
                self.assertFalse(ff._override_ok("82a-y.md R2"))
            finally:
                ff.RES = old

    # R6 / R7 of 82a-clarifications-6 ---------------------------------------------------------------
    def test_R7_audience_tokens_block_style_reuse(self):
        academic = self._style("cv-academic-plain", "Do not enforce a page limit;List publications;Keep single column;Omit photo",
                               table="none")
        prop = dict(self._proposal(), **{"Table Rules": "none"})
        self.assertEqual(ff.reuse_candidates(prop, [academic], "cv"), [])
        self.assertEqual(ff.reuse_candidates(prop, [self._style("cv-restrained", "Keep single column only", table="none")],
                                             "cv"), ["cv-restrained"])
        dach = self._style("cv-dach", "Photo top right;Date format DD.MM.YYYY", kw="cv, dach, tabular")
        self.assertEqual(ff.reuse_candidates(self._proposal(), [dach], "cv"), [])

    def test_R7_cv_serif_accent_plain_left_does_not_reuse_the_academic_row(self):
        res = ff.resolve_family("cv", ff.load_spec("cv"))
        row = next(r for r in res["rows"] if r["doc_category"] == "cv-serif-accent-plain-left")
        self.assertNotEqual(row["Style Key"], "cv-academic-plain")
        self.assertNotIn("cv-academic-plain", res["props"]["cv-serif-accent-plain-left"]["reuse"])

    def test_R6_defaults_count_inside_the_cap_of_ten(self):
        plan = ff.plan_designs("cv", ff.load_spec("cv"), ff.engine_state(ff.load_spec("cv"))[2])
        self.assertEqual(len(plan["shipped"]), 10)
        self.assertEqual(plan["cap1"], 8)          # 10 - cv-us-uk-designed (rank 13) - cv-academic (unmatched)
        self.assertEqual([s["rank"] for s in plan["shipped"][-2:]], [9, 10])
        self.assertEqual([s["design"]["design_key"] for s in plan["shipped"][-2:]], ["cv-us-uk-designed", "cv-academic"])

    # F17 -----------------------------------------------------------------------------------------
    def test_lib_rows_reads_each_library_row_once(self):
        rows = ff._lib_rows("palettes")
        keys = [r["palette_key"] for r in rows]
        self.assertEqual(len(keys), len(set(keys)))

    def test_a_rerun_does_not_see_the_family_own_previous_rows(self):
        own = ff.own_output_keys("cv", "doc-styles", "style_key")
        self.assertIn("cv-serif-plain-centered", own)
        self.assertFalse(own & {r["style_key"] for r in self.lib.styles})
        self.assertTrue(own & {r["style_key"] for r in ff.Library().styles})


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
