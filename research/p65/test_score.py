#!/usr/bin/env python3
"""pytest research/p65 -- the scorer against 3 hand-made fixture outputs per trial."""
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import score  # noqa: E402

PACK = score.DEFAULT_PACK.read_text(encoding="utf-8")
FIX = HERE / "fixtures"


def run(trial, kind):
    return score.score((FIX / f"{trial}-{kind}.md").read_text(encoding="utf-8"), trial, PACK)


def failed(result):
    return sorted(k for k, c in result["clauses"].items() if not c["pass"])


class TestScorer(unittest.TestCase):
    def test_clean_outputs_pass_every_clause(self):
        for t in ("T1", "T2", "T3"):
            with self.subTest(trial=t):
                r = run(t, "pass")
                self.assertEqual(failed(r), [], r["clauses"])
                self.assertTrue(r["pass"])

    def test_invented_hex_fails_clause_1_only(self):
        for t in ("T1", "T2", "T3"):
            with self.subTest(trial=t):
                r = run(t, "bad-hex")
                self.assertEqual(failed(r), ["1_out_of_pack_values"], r["clauses"])
                self.assertFalse(r["pass"])
                self.assertTrue(r["clauses"]["1_out_of_pack_values"]["evidence"]["hex_not_in_pack"])

    def test_wrong_section_order_fails_clause_3_only(self):
        for t in ("T1", "T2", "T3"):
            with self.subTest(trial=t):
                r = run(t, "bad-order")
                self.assertEqual(failed(r), ["3_section_order"], r["clauses"])
                self.assertFalse(r["pass"])

    def test_invented_font_and_size_fail_clause_1(self):
        text = (FIX / "T1-pass.md").read_text(encoding="utf-8")
        for label, mutated in (("font", text.replace("'Source Sans 3'", "Helvetica Neue")),
                               ("pt size", text.replace("10.5pt", "12pt")),
                               ("px size", text.replace("font-size: 13pt", "font-size: 17px"))):
            with self.subTest(mutation=label):
                self.assertIn("1_out_of_pack_values", failed(score.score(mutated, "T1", PACK)))

    def test_added_section_fails_clause_3(self):
        text = (FIX / "T1-pass.md").read_text(encoding="utf-8").replace(
            "## Skills\n", "## Hobbies\nCycling.\n\n## Skills\n")
        r = score.score(text, "T1", PACK)
        self.assertIn("3_section_order", failed(r))
        self.assertIn("hobbies", r["clauses"]["3_section_order"]["evidence"]["extra_sections"])

    def test_omission_needs_disclosure(self):
        text = (FIX / "T1-pass.md").read_text(encoding="utf-8")
        cut = text.replace("## Summary\nGraphic designer with six years' experience in branding, packaging and print.\n\n", "")
        self.assertIn("3_section_order", failed(score.score(cut, "T1", PACK)))
        ok = score.score(cut + "\nSummary omitted: you did not give one.\n", "T1", PACK)
        self.assertNotIn("3_section_order", failed(ok))

    def test_wrong_doctype_and_false_claims(self):
        text = (FIX / "T1-pass.md").read_text(encoding="utf-8")
        self.assertIn("4_doctype", failed(score.score(text.replace("cv-uk", "cv-us"), "T1", PACK)))
        claim = score.score(text + "\nI have created your CV.pdf for download.\n", "T1", PACK)
        self.assertIn("5_no_false_claims", failed(claim))
        check = score.score(text + "\nPreflight passed.\n", "T1", PACK)
        self.assertIn("5_no_false_claims", failed(check))

    def test_no_named_design_fails_clause_2_and_asking_among_designs_passes(self):
        text = (FIX / "T1-pass.md").read_text(encoding="utf-8")
        unnamed = text.replace("cv-us-uk-designed", "x").replace("CV -- Harvard reverse-chronological", "a design")
        self.assertIn("2_named_design", failed(score.score(unnamed, "T1", PACK)))
        asked = unnamed + ("\nWhich design would you like: CV -- Europass-compatible, or CV, DACH "
                           "tabellarisch (cv-dach-tabular)?\n")
        self.assertNotIn("2_named_design", failed(score.score(asked, "T1", PACK)))

    def test_design_override_values_come_from_the_grand_library(self):
        # cv-eu-europass's palette accent (#1A65A6) is in the pack but not in the cv-uk block
        text = (FIX / "T1-pass.md").read_text(encoding="utf-8")
        plain = text.replace("#005EA2", "#1A65A6")
        self.assertIn("1_out_of_pack_values", failed(score.score(plain, "T1", PACK)))
        named = plain.replace("cv-us-uk-designed", "cv-eu-europass")
        r = score.score(named, "T1", PACK)
        self.assertEqual(r["clauses"]["1_out_of_pack_values"]["evidence"]["hex_not_in_pack"], [])
        self.assertEqual(r["clauses"]["1_out_of_pack_values"]["evidence"]["design_overrides_applied"],
                         ["cv-eu-europass"])

    def test_prompts_are_present_verbatim_sources(self):
        for t in ("T1", "T2", "T3"):
            self.assertTrue((HERE / "prompts" / f"{t}.txt").read_text(encoding="utf-8").strip())


if __name__ == "__main__":
    unittest.main()
