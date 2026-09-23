#!/usr/bin/env python3
"""P1.4 (research/80-v05-plan.md §2B, §6): designs.csv catalogue rules over
data/base -- shipped data only, no research/ dependency.

A "design" is a doc-reasoning row catalogued per family (R-b). This file
checks the catalogue is internally consistent:

  1. `Rank` is an integer, contiguous 1..N within each `Family`;
  2. every design's `Reasoning Key` resolves to a real doc-reasoning row;
  3. every `Family` doctypes.csv actually uses has >=1 design;
  4. every doctype's own default `Reasoning Key` is some design's Reasoning
     Key in the SAME family (the doctype default is always catalogued,
     research/80 §2D "Default without --design = doctype default");
  5. `design_key` is prefixed with its own `Family` + "-";
  6. within a family, `convention`-evidence designs rank after every
     non-convention design.

Rule 6 is EXPECTED TO FAIL on the current seed data: cv has convention
designs at ranks 3-4 (cv-ats-strict, cv-academic) ABOVE authority designs at
ranks 5-6 (cv-dach-tabular, cv-editorial). Per the brief this is marked
`expectedFailure` rather than weakened -- seed ranks predate research/82;
Phase 4's cv re-rank removes this xfail.
"""
import csv
import unittest
from pathlib import Path

HERE = Path(__file__).parent
SCRIPTS_DIR = HERE.parent
SKILL_ROOT = SCRIPTS_DIR.parent
BASE = SKILL_ROOT / "data" / "base"


def _rows(table_name):
    with open(BASE / f"{table_name}.csv", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


DESIGNS = _rows("designs")
DOCTYPES = _rows("doctypes")
DOC_REASONING = _rows("doc-reasoning")

REASONING_KEYS = {row["doc_category"] for row in DOC_REASONING}

DESIGNS_BY_FAMILY = {}
for _row in DESIGNS:
    DESIGNS_BY_FAMILY.setdefault(_row["Family"], []).append(_row)


class TestRankIsContiguous(unittest.TestCase):
    def test_rank_is_a_positive_integer(self):
        for row in DESIGNS:
            with self.subTest(design_key=row["design_key"]):
                self.assertRegex(
                    row["Rank"], r"^[1-9][0-9]*$",
                    f"{row['design_key']}: Rank {row['Rank']!r} is not a positive integer")

    def test_rank_is_contiguous_1_to_n_per_family(self):
        for family, rows in DESIGNS_BY_FAMILY.items():
            with self.subTest(family=family):
                ranks = sorted(int(row["Rank"]) for row in rows)
                expected = list(range(1, len(rows) + 1))
                self.assertEqual(
                    ranks, expected,
                    f"family {family!r} has {len(rows)} design(s) but ranks are {ranks}, "
                    f"expected {expected}")


class TestReasoningKeyResolves(unittest.TestCase):
    def test_every_design_reasoning_key_exists_in_doc_reasoning(self):
        for row in DESIGNS:
            with self.subTest(design_key=row["design_key"]):
                self.assertIn(
                    row["Reasoning Key"], REASONING_KEYS,
                    f"{row['design_key']}: Reasoning Key {row['Reasoning Key']!r} is not a "
                    "doc-reasoning.doc_category row")


class TestEveryDoctypeFamilyHasADesign(unittest.TestCase):
    def test_every_family_used_by_doctypes_has_at_least_one_design(self):
        doctype_families = {row["Family"] for row in DOCTYPES if row["Family"]}
        for family in sorted(doctype_families):
            with self.subTest(family=family):
                self.assertIn(
                    family, DESIGNS_BY_FAMILY,
                    f"family {family!r} is used by data/base/doctypes.csv but has no "
                    "row in data/base/designs.csv")


class TestDoctypeDefaultIsCatalogued(unittest.TestCase):
    def test_doctype_reasoning_key_is_a_design_in_the_same_family(self):
        for row in DOCTYPES:
            family = row["Family"]
            reasoning_key = row["Reasoning Key"]
            with self.subTest(doctype=row["doc_key"]):
                family_reasoning_keys = {
                    d["Reasoning Key"] for d in DESIGNS_BY_FAMILY.get(family, [])
                }
                self.assertIn(
                    reasoning_key, family_reasoning_keys,
                    f"{row['doc_key']}: doctype default Reasoning Key {reasoning_key!r} is "
                    f"not any design's Reasoning Key within family {family!r} -- the default "
                    "is supposed to always be catalogued")


class TestDesignKeyIsFamilyPrefixed(unittest.TestCase):
    def test_design_key_starts_with_family_dash(self):
        for row in DESIGNS:
            prefix = f"{row['Family']}-"
            with self.subTest(design_key=row["design_key"]):
                self.assertTrue(
                    row["design_key"].startswith(prefix),
                    f"{row['design_key']}: does not start with {prefix!r} (its own Family)")


class TestConventionRanksAfterNonConvention(unittest.TestCase):
    @unittest.expectedFailure
    def test_convention_designs_never_outrank_non_convention_designs(self):
        # seed ranks predate research/82; Phase 4 cv re-rank removes this xfail
        for family, rows in DESIGNS_BY_FAMILY.items():
            ordered = sorted(rows, key=lambda r: int(r["Rank"]))
            evidence_in_rank_order = [r["Evidence Class"] for r in ordered]
            seen_convention = False
            for evidence_class in evidence_in_rank_order:
                if evidence_class == "convention":
                    seen_convention = True
                elif seen_convention:
                    self.fail(
                        f"family {family!r}: a convention design outranks a later "
                        f"non-convention design -- Evidence Class in Rank order is "
                        f"{evidence_in_rank_order}")


if __name__ == "__main__":
    unittest.main()
