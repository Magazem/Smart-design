#!/usr/bin/env python3
"""Unit tests for scripts/make_brand_kit.py.

Every test runs against an ISOLATED snapshot of the real data/base +
schema-manifest.json (via DDI_SKILL_DIR), taken fresh in setUp and with the
stray `ens-manrope-inter` row removed from the snapshot's typefaces.csv if
present -- so these tests are deterministic and independent of whatever the
live shared data/base/*.csv happens to contain at the moment they run (see
this project's own report: that file has been observed changing mid-session
from a concurrent process). The point of these tests is to prove
make_brand_kit.py's own logic is correct; the live-base collision is a
separate, already-reported data bug, not something these tests should
depend on either way.
"""
import csv
import io
import contextlib
import os
import shutil
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

HERE = Path(__file__).parent
SCRIPTS_DIR = HERE.parent
REAL_SKILL_DIR = SCRIPTS_DIR.parent
sys.path.insert(0, str(SCRIPTS_DIR))
import make_brand_kit as mbk  # noqa: E402


def _snapshot_skill_dir() -> Path:
    """Copy the real data/schema-manifest.json + data/base into a fresh temp
    dir, with any stray non-generic Brand Scope row scrubbed from every
    base CSV (defence against the live concurrent-edit issue noted above --
    a base table should never carry brand rows, so scrubbing them here is
    restoring the invariant, not hiding a real test failure)."""
    tmp = Path(tempfile.mkdtemp(prefix="ddi-test-skill-"))
    data = tmp / "data"
    shutil.copytree(REAL_SKILL_DIR / "data" / "base", data / "base")
    shutil.copy2(REAL_SKILL_DIR / "data" / "schema-manifest.json", data / "schema-manifest.json")

    for csv_path in (data / "base").glob("*.csv"):
        with csv_path.open(encoding="utf-8", newline="") as f:
            rows = list(csv.reader(f))
        if not rows or "Brand Scope" not in rows[0]:
            continue
        idx = rows[0].index("Brand Scope")
        cleaned = [rows[0]] + [r for r in rows[1:] if r[idx] in ("", "generic")]
        if len(cleaned) != len(rows):
            with csv_path.open("w", encoding="utf-8", newline="") as f:
                csv.writer(f, lineterminator="\n").writerows(cleaned)

    return tmp


class MakeBrandKitTestCase(unittest.TestCase):
    def setUp(self):
        self.skill_dir = _snapshot_skill_dir()
        self._old_env = {k: os.environ.get(k) for k in ("DDI_SKILL_DIR", "DDI_OUTPUTS_DIR", "DDI_UPLOADS_DIR")}
        os.environ["DDI_SKILL_DIR"] = str(self.skill_dir)
        self.outputs = Path(tempfile.mkdtemp(prefix="ddi-test-outputs-"))
        os.environ["DDI_OUTPUTS_DIR"] = str(self.outputs)
        self.addCleanup(self._restore_env)
        self.addCleanup(lambda: shutil.rmtree(self.skill_dir, ignore_errors=True))
        self.addCleanup(lambda: shutil.rmtree(self.outputs, ignore_errors=True))

    def _restore_env(self):
        for k, v in self._old_env.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v

    def _write_brand_md(self, text: str) -> Path:
        fd, name = tempfile.mkstemp(suffix=".md", prefix="brand-")
        os.close(fd)  # Windows can't unlink a still-open file descriptor
        path = Path(name)
        path.write_text(text, encoding="utf-8")
        self.addCleanup(lambda: path.unlink(missing_ok=True))
        return path

    def _run(self, argv):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = mbk.main(argv)
        return code, buf.getvalue()


ENS_BRAND_MD = """# ENS

slug: ens

## Palette
primary: #1F6F43
secondary: #8B5E3C
accent: #9ACD32
background: #F7F8F5
foreground: #1E2A23
muted: #DCE8DF

## Typefaces
heading: Manrope
body: Inter

## Doctypes
note-interne
formulaire
social
slides

## Voice
Reliable, clear, down-to-earth.

## Document defaults
page-format note-interne: a4-professional
page-format formulaire: a4-professional
type-scale label: 8.5
type-scale caption: 9
type-scale body: 11
type-scale lead: 12
type-scale h3: 16
type-scale h1: 24
"""


class TestHappyPath(MakeBrandKitTestCase):
    def test_dry_run_ok_against_clean_snapshot(self):
        path = self._write_brand_md(ENS_BRAND_MD)
        code, out = self._run([str(path), "--dry-run"])
        self.assertEqual(code, 0, out)
        self.assertIn("DRY-RUN OK", out)
        self.assertIn("doctypes=4", out)
        self.assertIn("type-scales=6", out)
        self.assertNotIn("REAL problem", out)

    def test_dry_run_writes_nothing(self):
        path = self._write_brand_md(ENS_BRAND_MD)
        self._run([str(path), "--dry-run"])
        self.assertEqual(list(self.outputs.iterdir()), [])

    def test_real_run_produces_zip_with_expected_members(self):
        path = self._write_brand_md(ENS_BRAND_MD)
        code, out = self._run([str(path)])
        self.assertEqual(code, 0, out)
        out_path = self.outputs / "ens-brand-kit.zip"
        self.assertTrue(out_path.is_file())
        with zipfile.ZipFile(out_path) as zf:
            names = set(zf.namelist())
            self.assertEqual(
                names,
                {"brand.md", "data/palettes.csv", "data/typefaces.csv",
                 "data/doctypes.csv", "data/type-scales.csv"},
            )
            palette_rows = list(csv.DictReader(io.StringIO(zf.read("data/palettes.csv").decode("utf-8"))))
            self.assertEqual(len(palette_rows), 1)
            self.assertEqual(palette_rows[0]["palette_key"], "ens-core")
            self.assertEqual(palette_rows[0]["Primary"], "#1F6F43")
            self.assertEqual(palette_rows[0]["On Primary"], "#FFFFFF")
            self.assertEqual(palette_rows[0]["Brand Scope"], "ens")

            doctype_rows = list(csv.DictReader(io.StringIO(zf.read("data/doctypes.csv").decode("utf-8"))))
            self.assertEqual({r["doc_key"] for r in doctype_rows},
                              {"ens-note-interne", "ens-formulaire", "ens-social", "ens-slides"})
            note = next(r for r in doctype_rows if r["doc_key"] == "ens-note-interne")
            self.assertEqual(note["Page Format Key"], "a4-professional")
            social = next(r for r in doctype_rows if r["doc_key"] == "ens-social")
            self.assertEqual(social["Page Format Key"], "")

    def test_typescales_omitted_when_no_constants_given(self):
        text = ENS_BRAND_MD.replace(
            "type-scale label: 8.5\ntype-scale caption: 9\ntype-scale body: 11\n"
            "type-scale lead: 12\ntype-scale h3: 16\ntype-scale h1: 24\n",
            "",
        )
        path = self._write_brand_md(text)
        code, out = self._run([str(path)])
        self.assertEqual(code, 0, out)
        with zipfile.ZipFile(self.outputs / "ens-brand-kit.zip") as zf:
            self.assertNotIn("data/type-scales.csv", zf.namelist())


class TestParseErrors(MakeBrandKitTestCase):
    def test_missing_slug_line(self):
        text = ENS_BRAND_MD.replace("slug: ens\n", "")
        path = self._write_brand_md(text)
        code, out = self._run([str(path), "--dry-run"])
        self.assertEqual(code, 1)
        self.assertIn("missing required 'slug:", out)

    def test_unknown_top_level_key_names_line_number(self):
        text = ENS_BRAND_MD.replace("slug: ens\n", "slug: ens\ncolor: blue\n")
        path = self._write_brand_md(text)
        code, out = self._run([str(path), "--dry-run"])
        self.assertEqual(code, 1)
        self.assertIn("brand.md:4:", out)
        self.assertIn("unknown top-level key 'color'", out)

    def test_unknown_section_heading_names_line_number(self):
        text = ENS_BRAND_MD.replace("## Voice", "## Vibes")
        path = self._write_brand_md(text)
        code, out = self._run([str(path), "--dry-run"])
        self.assertEqual(code, 1)
        self.assertIn("unknown section heading '## Vibes'", out)

    def test_unknown_palette_key_names_line_number(self):
        text = ENS_BRAND_MD.replace("primary: #1F6F43", "primary: #1F6F43\ntertiary: #000000")
        path = self._write_brand_md(text)
        code, out = self._run([str(path), "--dry-run"])
        self.assertEqual(code, 1)
        self.assertIn("unknown palette role 'tertiary'", out)

    def test_bad_hex_color_rejected(self):
        text = ENS_BRAND_MD.replace("primary: #1F6F43", "primary: forest-green")
        path = self._write_brand_md(text)
        code, out = self._run([str(path), "--dry-run"])
        self.assertEqual(code, 1)
        self.assertIn("is not a #RRGGBB hex colour", out)

    def test_missing_palette_role_rejected(self):
        text = ENS_BRAND_MD.replace("muted: #DCE8DF\n", "")
        path = self._write_brand_md(text)
        code, out = self._run([str(path), "--dry-run"])
        self.assertEqual(code, 1)
        self.assertIn("missing role(s): muted", out)

    def test_unknown_doctype_rejected_with_supported_list(self):
        text = ENS_BRAND_MD.replace("slides\n", "slides\nweb-tool\n")
        path = self._write_brand_md(text)
        code, out = self._run([str(path), "--dry-run"])
        self.assertEqual(code, 1)
        self.assertIn("unknown doctype 'web-tool'", out)
        self.assertIn("supported:", out)

    def test_page_format_override_for_undeclared_doctype_rejected(self):
        text = ENS_BRAND_MD + "page-format cv: a4-professional\n"
        path = self._write_brand_md(text)
        code, out = self._run([str(path), "--dry-run"])
        self.assertEqual(code, 1)
        self.assertIn("unknown doctype", out)


class TestGateRefusals(MakeBrandKitTestCase):
    def test_bad_contrast_palette_refuses_to_emit(self):
        # Foreground barely distinguishable from Background -> On Muted/Muted
        # style contrast rules aren't hit, but Foreground/Background is.
        text = ENS_BRAND_MD.replace("background: #F7F8F5", "background: #1F2A22")
        path = self._write_brand_md(text)
        code, out = self._run([str(path), "--dry-run"])
        self.assertEqual(code, 1, out)
        self.assertIn("REAL problem", out)
        self.assertIn("is below required", out)
        self.assertEqual(list(self.outputs.iterdir()), [])

    def test_page_format_typo_is_a_real_unresolvable_fk_not_a_skip(self):
        text = ENS_BRAND_MD.replace(
            "page-format note-interne: a4-professional",
            "page-format note-interne: a4-profesional",  # typo
        )
        path = self._write_brand_md(text)
        code, out = self._run([str(path), "--dry-run"])
        self.assertEqual(code, 1, out)
        self.assertIn("REAL problem", out)
        self.assertIn("'a4-profesional' does not resolve to page-formats.page_format_key", out)

    def test_typeface_key_collision_with_base_refuses_to_emit(self):
        # Plant a base row whose typeface_key is exactly what the ENS
        # example's generator will independently produce, to prove the
        # self-check's duplicate-key detection actually blocks emission
        # (this is the real defect this project found live in data/base --
        # see the task report -- reproduced here deterministically).
        typefaces_csv = self.skill_dir / "data" / "base" / "typefaces.csv"
        with typefaces_csv.open(encoding="utf-8", newline="") as f:
            rows = list(csv.reader(f))
        header = rows[0]
        planted = ["ens-manrope-inter"] + [""] * (len(header) - 1)
        planted[header.index("Brand Scope")] = "generic"  # even as "generic" the KEY still collides
        rows.insert(1, planted)
        with typefaces_csv.open("w", encoding="utf-8", newline="") as f:
            csv.writer(f, lineterminator="\n").writerows(rows)

        path = self._write_brand_md(ENS_BRAND_MD)
        code, out = self._run([str(path), "--dry-run"])
        self.assertEqual(code, 1, out)
        self.assertIn("REAL problem", out)
        self.assertIn("duplicate key 'ens-manrope-inter'", out)
        self.assertEqual(list(self.outputs.iterdir()), [])


class TestOutputPathHandling(MakeBrandKitTestCase):
    def test_output_refused_inside_uploads_dir(self):
        uploads = Path(tempfile.mkdtemp(prefix="ddi-test-uploads-"))
        self.addCleanup(lambda: shutil.rmtree(uploads, ignore_errors=True))
        os.environ["DDI_UPLOADS_DIR"] = str(uploads)
        path = self._write_brand_md(ENS_BRAND_MD)
        code, out = self._run([str(path), "-o", str(uploads / "ens-brand-kit.zip")])
        self.assertEqual(code, 1)
        self.assertIn("refusing to write into the read-only uploads directory", out)


GENERIC_BRAND_MD = ENS_BRAND_MD.replace(
    "note-interne\nformulaire\nsocial\nslides\n",
    "cv-uk\ninvoice-tabular\nslide-deck-projection\nreport-short\nnote-interne\n",
).replace(
    "page-format note-interne: a4-professional\npage-format formulaire: a4-professional\n",
    "page-format note-interne: a4-professional\n",
)


def _base_doctype_rows(skill_dir: Path) -> dict:
    with (skill_dir / "data" / "base" / "doctypes.csv").open(encoding="utf-8", newline="") as f:
        return {r["doc_key"]: r for r in csv.DictReader(f)}


class TestGenericBaseDoctypes(MakeBrandKitTestCase):
    def test_generic_doctypes_dry_run_ok(self):
        path = self._write_brand_md(GENERIC_BRAND_MD)
        code, out = self._run([str(path), "--dry-run"])
        self.assertEqual(code, 0, out)
        self.assertIn("doctypes=5", out)
        self.assertNotIn("REAL problem", out)

    def test_generic_rows_copy_base_row(self):
        path = self._write_brand_md(GENERIC_BRAND_MD)
        code, out = self._run([str(path)])
        self.assertEqual(code, 0, out)
        with zipfile.ZipFile(self.outputs / "ens-brand-kit.zip") as zf:
            rows = {r["doc_key"]: r for r in csv.DictReader(
                io.StringIO(zf.read("data/doctypes.csv").decode("utf-8")))}
        base = _base_doctype_rows(self.skill_dir)
        for key in ("cv-uk", "invoice-tabular", "slide-deck-projection", "report-short"):
            row, b = rows[f"ens-{key}"], base[key]
            for col in ("Artifact Class", "Reasoning Key", "Page Format Key",
                        "Render Target Keys", "Constraint Set Keys", "Structure Key",
                        "Region Key", "Family", "Default Language"):
                self.assertEqual(row[col], b[col], f"{key}: {col}")
            self.assertEqual(row["Brand Scope"], "ens")
            self.assertIn(key, row["Keywords"])
            self.assertIn("ens", row["Keywords"])

    def test_generic_page_format_override_applies(self):
        text = GENERIC_BRAND_MD.replace(
            "type-scale label", "page-format cv-uk: a4-professional\ntype-scale label")
        path = self._write_brand_md(text)
        code, out = self._run([str(path)])
        self.assertEqual(code, 0, out)
        with zipfile.ZipFile(self.outputs / "ens-brand-kit.zip") as zf:
            rows = {r["doc_key"]: r for r in csv.DictReader(
                io.StringIO(zf.read("data/doctypes.csv").decode("utf-8")))}
        self.assertEqual(rows["ens-cv-uk"]["Page Format Key"], "a4-professional")

    def test_unknown_key_lists_generic_and_legacy_keys(self):
        path = self._write_brand_md(ENS_BRAND_MD.replace("slides\n", "slides\nno-such-doc\n"))
        code, out = self._run([str(path), "--dry-run"])
        self.assertEqual(code, 1)
        self.assertIn("unknown doctype 'no-such-doc'", out)
        for key in ("cv-uk", "invoice-tabular", "slide-deck-projection", "note-interne"):
            self.assertIn(key, out)


if __name__ == "__main__":
    unittest.main()
