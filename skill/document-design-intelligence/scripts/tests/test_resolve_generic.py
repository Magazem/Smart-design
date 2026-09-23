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
