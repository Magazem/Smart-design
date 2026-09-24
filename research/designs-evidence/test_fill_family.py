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
            rc = ff.dry_run("whitepaper")
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
