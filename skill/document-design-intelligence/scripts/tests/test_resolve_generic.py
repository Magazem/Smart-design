#!/usr/bin/env python3
"""research/88: a plain request with no region/variant cue must not abstain between
variants of ONE family when that family has a single derivable default doctype; genuine
cross-family ambiguity and genuinely different variants (brochure sizes, deck purposes,
report lengths) keep abstaining."""
import contextlib
import io
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
import resolve  # noqa: E402


def run(query, *extra):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = resolve.main(["--query", query, "--json", *extra])
    return rc, json.loads(buf.getvalue())


class TestFamilyDefault(unittest.TestCase):
    def assertResolvesTo(self, query, key):
        rc, out = run(query)
        self.assertEqual(rc, 0, out)
        self.assertEqual(out["resolved"]["doctypes"][0]["key"], key)

    def test_cv_requests_without_region_resolve_to_cv_generic(self):
        for q in ("make me a CV for a marketing coordinator", "write my resume",
                  "I need a curriculum vitae"):
            with self.subTest(q=q):
                self.assertResolvesTo(q, "cv-generic")
                rc, out = run(q)
                self.assertEqual(out["method"], "family-default")

    def test_explicit_region_still_wins(self):
        self.assertResolvesTo("write my cv uk", "cv-uk")

    def test_cross_family_tie_still_abstains(self):
        rc, out = run("erstelle ein Angebot fuer eine Renovierung")
        self.assertEqual(rc, 2)

    def test_flagged_family_defaults(self):
        for q, key in (("I need a brochure", "brochure-trifold-a4"), ("make a flyer for my bake sale", "brochure-flyer-a4"),
                       ("I need a report", "report-short"), ("I need a slide deck", "slide-deck-projection"),
                       ("make slides for my team meeting", "slide-deck-projection")):
            with self.subTest(q=q):
                self.assertResolvesTo(q, key)

    def test_us_letter_cue_picks_the_letter_sibling(self):
        for q, key in (("I need a brochure for US letter paper", "brochure-trifold-letter"),
                       ("flyer for a US bake sale", "brochure-flyer-letter"),
                       ("I need a flyer, 8.5x11", "brochure-flyer-letter")):
            with self.subTest(q=q):
                self.assertResolvesTo(q, key)

    def test_query_language_picks_family_doctype_and_language(self):
        for q, key, lang in (("erstelle einen Lebenslauf fuer eine Bewerbung", "cv-dach", "de"),
                             ("fais-moi un CV pour un poste de comptable", "cv-france", "fr")):
            with self.subTest(q=q):
                rc, out = run(q)
                self.assertEqual(rc, 0, out)
                self.assertEqual(out["resolved"]["doctypes"][0]["key"], key)
                self.assertEqual(out["language"]["value"], lang)

    def test_english_cv_stays_generic_english(self):
        rc, out = run("make me a CV for a marketing coordinator")
        self.assertEqual(out["language"]["value"], "en")

    def test_lettre_a_mon_proprietaire_is_a_formal_letter(self):
        for q in ("écris une lettre à mon propriétaire", "ecris une lettre a mon proprietaire"):
            with self.subTest(q=q):
                self.assertResolvesTo(q, "letter-formal")

    def test_exactly_one_flag_per_designated_family(self):
        import csv
        base = HERE.parent.parent / "data" / "base" / "doctypes.csv"
        flags = {}
        for r in csv.DictReader(open(base, encoding="utf-8", newline="")):
            if r["Family Default"] == "y":
                flags.setdefault(r["Family"], []).append(r["doc_key"])
        self.assertTrue(flags and all(len(v) == 1 for v in flags.values()), flags)
        self.assertEqual(flags["cv"], ["cv-generic"])

    def test_identity_and_clear_matches_unchanged(self):
        self.assertResolvesTo("write a memo about the new office hours", "memo-internal")
        self.assertResolvesTo("make an invoice for my consulting work", "invoice-tabular")

    def test_explicit_family_noun_beats_incidental_words(self):
        """research/88 round 3: "paper", "page", "A4", "US" must not move a request out of
        the family the user named."""
        for q, key in (("make a brochure on 8.5x11 paper", "brochure-trifold-letter"),
                       ("make a flyer on 8.5x11 paper", "brochure-flyer-letter"),
                       ("flyer for US paper", "brochure-flyer-letter"),
                       ("make a poster on A4 paper", "poster"),
                       ("professional CV on A4 paper", "cv-generic"),
                       ("make a simple invoice template on A4 paper", "invoice-tabular"),
                       ("modern price quote, one page", "quote-devis"),
                       ("make a printable form on A4 paper", "form-handfilled"),
                       ("a one page memo on company paper", "memo-internal")):
            with self.subTest(q=q):
                self.assertResolvesTo(q, key)

    def test_one_page_cv_stays_a_cv(self):
        # "one page" is a keyword of cv-us and one-pager; the named family keeps it a CV
        rc, out = run("make a simple one page CV template")
        self.assertEqual(rc, 0, out)
        self.assertTrue(out["resolved"]["doctypes"][0]["key"].startswith("cv-"))

    def test_two_family_nouns_do_not_trigger_the_rule(self):
        # a cover letter is one family, not "letter" + something
        self.assertResolvesTo("simple cover letter template, one page", "cover-letter")
        self.assertResolvesTo("make a one pager on US letter paper", "one-pager")


if __name__ == "__main__":
    unittest.main()


class TestR5Review(unittest.TestCase):
    """research/89 R5 review fixes (orchestrator rulings in the task text)."""

    def resolved(self, q, *extra):
        rc, out = run(q, *extra)
        self.assertEqual(rc, 0, out)
        return out

    def key(self, q, *extra):
        return self.resolved(q, *extra)["resolved"]["doctypes"][0]["key"]

    # F2 -- "letter" as a paper size does not name the letter family
    def test_f2_letter_paper_size_words_do_not_name_letter_family(self):
        for q, key in (("report on letter paper", "report-short"), ("memo on letter paper", "memo-internal"),
                       ("a memo on US letter paper", "memo-internal"), ("invoice on letter paper", "invoice-tabular"),
                       ("write a formal letter on letter-size paper", "letter-formal")):
            with self.subTest(q=q):
                self.assertEqual(self.key(q), key)

    # F3 -- name particles do not flip language or region
    def test_f3_name_particles_do_not_flip_language(self):
        for q in ("CV for Maria de la Cruz", "CV for Jean-Luc de la Fontaine", "resume for Anna von der Leyen"):
            with self.subTest(q=q):
                out = self.resolved(q)
                self.assertEqual(out["resolved"]["doctypes"][0]["key"], "cv-generic")
                self.assertEqual(out["language"]["value"], "en")

    def test_f3_two_signal_tokens_needed_but_real_french_still_detected(self):
        self.assertEqual(resolve._detect_language("a flyer for le petit cafe")[0], "en")
        self.assertEqual(resolve._detect_language("fais-moi un CV pour un poste de comptable")[0], "fr")
        self.assertEqual(resolve._detect_language("erstelle einen Lebenslauf fuer eine Bewerbung")[0], "de")

    # F4 -- US cue: pronoun "us" is not a size cue; "U.S." is
    def test_f4_us_cue_tokens(self):
        for q, key in (("make a flyer for us", "brochure-flyer-a4"), ("brochure for us", "brochure-trifold-a4"),
                       ("flyer for the U.S. office", "brochure-flyer-letter"),
                       ("a flyer for the US market", "brochure-flyer-letter"),
                       ("I need a flyer, 8.5x11", "brochure-flyer-letter")):
            with self.subTest(q=q):
                self.assertEqual(self.key(q), key)

    # F5 -- query language applies on the direct BM25 path too
    def test_f5_query_language_applies_to_direct_matches(self):
        for q, key, lang in (("fais-moi une presentation", "slide-deck-projection", "fr"),
                             ("erstelle eine Praesentation", "slide-deck-projection", "de"),
                             ("redige un rapport long avec sommaire", "report-long-toc", "fr")):
            with self.subTest(q=q):
                out = self.resolved(q)
                self.assertEqual(out["resolved"]["doctypes"][0]["key"], key)
                self.assertEqual(out["language"], {"value": lang, "source": "query"})

    def test_f5_explicit_lang_still_wins_over_detected(self):
        out = self.resolved("fais-moi une presentation", "--lang", "en")
        self.assertEqual(out["language"]["value"], "en")

    # F6 -- plural family nouns name the family
    def test_f6_plurals_resolve(self):
        for q, key in (("flyers", "brochure-flyer-a4"), ("invoices", "invoice-tabular"),
                       ("posters", "poster"), ("CVs for my team", "cv-generic")):
            with self.subTest(q=q):
                self.assertEqual(self.key(q), key)

    # F7 -- two or more named families abstain with both families' candidates
    def test_f7_multiple_families_abstain_with_candidates(self):
        for q, fams in (("a CV and a cover letter", {"cv", "cover-letter"}),
                        ("slides for the report", {"deck", "report"}),
                        ("deck builder CV", {"deck", "cv"})):
            with self.subTest(q=q):
                rc, out = run(q)
                self.assertEqual(rc, 2, out)
                self.assertEqual(out["reason"], "multiple-families")
                self.assertEqual(set(out["named_families"]), fams)
                self.assertEqual({c["family"] for c in out["candidates"]}, fams)

    # F8 -- diagnostics are visible in --json
    def test_f8_json_exposes_diagnostics(self):
        out = self.resolved("CV")
        d = out["diagnostics"]
        self.assertEqual(out["method"], "family-default")
        self.assertIn("note", d)
        self.assertEqual(d["named_family"], "cv")
        self.assertIn("candidates", d)
        out2 = self.resolved("fais-moi une presentation")
        self.assertEqual(out2["diagnostics"]["query_language"], "fr")
        self.assertTrue(out2["diagnostics"]["query_language_evidence"])

    # F9 -- French: Belgian/Swiss/Canadian cue -> cv-eu-generic with fr; no cue -> cv-france
    def test_f9_french_regional_cues(self):
        for q, key in (("fais-moi un CV pour un poste a Bruxelles, Belgique", "cv-eu-generic"),
                       ("redige mon CV pour Geneve en Suisse", "cv-eu-generic"),
                       ("fais-moi un CV pour le Quebec", "cv-eu-generic"),
                       ("fais-moi un CV pour un poste de comptable", "cv-france")):
            with self.subTest(q=q):
                out = self.resolved(q)
                self.assertEqual(out["resolved"]["doctypes"][0]["key"], key)
                self.assertEqual(out["language"]["value"], "fr")

    # F10 -- an explicit A4 cue beats a letter-size keyword hit
    def test_f10_explicit_a4_cue(self):
        self.assertEqual(self.key("professional flyer one page A4"), "brochure-flyer-a4")
        self.assertEqual(self.key("professional flyer one page A4 US market"), "brochure-flyer-letter")

    # F11 -- --lang feeds the family-default doctype choice
    def test_f11_lang_flag_feeds_doctype_choice(self):
        out = self.resolved("make me a CV", "--lang", "de")
        self.assertEqual(out["resolved"]["doctypes"][0]["key"], "cv-dach")
        self.assertEqual(out["language"], {"value": "de", "source": "override"})


class TestF1BrandKitPrefixHeader(unittest.TestCase):
    """research/89 F1: a brand kit built before a nullable column was appended must still load
    (padded with blank, tier-2 advisory), and must never refuse generic queries."""

    def setUp(self):
        import csv, shutil, tempfile
        skill = HERE.parent.parent
        self.tmp = Path(tempfile.mkdtemp(prefix="ddi-f1-"))
        shutil.copytree(skill / "data", self.tmp / "data")
        brand = self.tmp / "data" / "brand" / "old"
        brand.mkdir(parents=True)
        with (skill / "data" / "base" / "doctypes.csv").open(encoding="utf-8", newline="") as f:
            rows = list(csv.reader(f))
        hdr = rows[0]
        self.assertEqual(hdr[-1], "Family Default")
        row = list(rows[1])
        row[0] = "old-cv"
        row[4] = "old"
        with (brand / "doctypes.csv").open("w", encoding="utf-8", newline="") as f:
            w = csv.writer(f, lineterminator="\n")
            w.writerow(hdr[:-1])
            w.writerow(row[:-1])
        self.data = str(self.tmp / "data")

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_generic_query_still_resolves_with_an_old_kit_installed(self):
        rc, out = run("make a memo about office hours", "--data-dir", self.data)
        self.assertEqual(rc, 0, out)
        self.assertEqual(out["resolved"]["doctypes"][0]["key"], "memo-internal")

    def test_old_kit_row_itself_loads_padded(self):
        rc, out = run("old-cv", "--data-dir", self.data, "--brand", "old")
        self.assertEqual(rc, 0, out)
        self.assertEqual(out["resolved"]["doctypes"][0]["key"], "old-cv")
        self.assertEqual(out["resolved"]["doctypes"][0].get("Family Default", ""), "")
