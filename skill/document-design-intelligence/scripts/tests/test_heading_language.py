#!/usr/bin/env python3
"""A7 (research/64 D-E, RESUME backlog item 4): heading language follows the
document's actual language, not structures.csv's hard-coded "en" constant.
Red-then-green coverage for:

  - resolve.py's JSON payload always carries a "language" block ({"value":
    ..., "source": "override"|"doctype-default"})
  - cv-dach's docx handoff shows German section headings (its own Default
    Language, doctype-default source)
  - cv-france's docx handoff shows French section headings
  - `--lang fr` overrides report-short's own English default
  - a resolved language with no authored heading row for a section falls
    back to the structure's own Heading Language and says so on that line,
    never silently
"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).parent
SCRIPTS_DIR = HERE.parent

PYTHON = sys.executable
RESOLVE_PY = SCRIPTS_DIR / "resolve.py"
DDI_PY = SCRIPTS_DIR / "ddi.py"


def _resolve(args):
    return subprocess.run([PYTHON, str(RESOLVE_PY), *args], capture_output=True, text=True)


def _ddi(args):
    return subprocess.run([PYTHON, str(DDI_PY), *args], capture_output=True, text=True)


class TestResolveLanguageField(unittest.TestCase):
    def test_doctype_default_language_and_source(self):
        proc = _resolve(["--doctype", "cv-dach", "--json"])
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["language"], {"value": "de", "source": "doctype-default"})

    def test_lang_override_takes_priority(self):
        proc = _resolve(["--doctype", "cv-dach", "--lang", "fr", "--json"])
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["language"], {"value": "fr", "source": "override"})

    def test_default_english_doctype_still_carries_the_field(self):
        proc = _resolve(["--doctype", "cv-uk", "--json"])
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["language"], {"value": "en", "source": "doctype-default"})

    def test_bad_lang_value_rejected(self):
        proc = _resolve(["--doctype", "cv-uk", "--lang", "es", "--json"])
        self.assertNotEqual(proc.returncode, 0)


class TestHandoffLanguageSelectsHeadingWording(unittest.TestCase):
    def _handoff(self, doctype, extra_resolve_args=(), fmt="docx"):
        proc = _resolve(["--doctype", doctype, "--json", *extra_resolve_args])
        self.assertEqual(proc.returncode, 0, proc.stderr)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "resolved.json"
            path.write_text(proc.stdout, encoding="utf-8")
            return _ddi(["handoff", "--json", str(path), "--format", fmt])

    def test_cv_dach_docx_handoff_shows_german_headings(self):
        proc = self._handoff("cv-dach")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("language=de, source=doctype-default", proc.stdout)
        for section, text in (
            ("contact", "Kontakt"), ("experience", "Berufserfahrung"),
            ("education", "Ausbildung"), ("skills", "Kenntnisse"),
        ):
            with self.subTest(section=section):
                self.assertIn(f"{section}: {text}", proc.stdout)

    def test_cv_france_docx_handoff_shows_french_headings(self):
        proc = self._handoff("cv-france")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("language=fr, source=doctype-default", proc.stdout)
        for section, text in (
            ("contact", "Coordonnées"), ("experience", "Expérience professionnelle"),
            ("education", "Formation"), ("skills", "Compétences"),
        ):
            with self.subTest(section=section):
                self.assertIn(f"{section}: {text}", proc.stdout)

    def test_lang_override_shows_french_on_an_english_default_doctype(self):
        proc = self._handoff("report-short", extra_resolve_args=["--lang", "fr"])
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("language=fr, source=override", proc.stdout)
        for section, text in (
            ("executive-summary", "Résumé exécutif"),
            ("introduction", "Introduction"),
            ("findings", "Résultats"), ("conclusion", "Conclusion"),
        ):
            with self.subTest(section=section):
                self.assertIn(f"{section}: {text}", proc.stdout)


class TestMissingLanguageRowFallsBackAndSaysSo(unittest.TestCase):
    """A hand-built resolved.json (no authored `de` heading for `agenda`),
    since every canonical_section actually reachable from a real doctype
    today has full en/fr/de coverage (research/74-heading-language.md's
    census) -- the fallback branch has no real-data trigger to exercise."""

    _RESOLVED = {
        "status": "resolved",
        "language": {"value": "de", "source": "override"},
        "resolved": {
            "structures": [{"key": "toy", "Section Order": "agenda",
                             "Heading Language": "en"}],
            "headings": [
                {"key": "agenda-en-1", "canonical_section": "agenda",
                 "Heading Text": "Agenda", "Language": "en", "Is Primary": "yes"},
                {"key": "agenda-fr-1", "canonical_section": "agenda",
                 "Heading Text": "Agenda", "Language": "fr", "Is Primary": "yes"},
            ],
        },
    }

    def test_missing_german_row_falls_back_to_english_and_says_so(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "resolved.json"
            path.write_text(json.dumps(self._RESOLVED), encoding="utf-8")
            proc = _ddi(["handoff", "--json", str(path), "--format", "docx"])
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("language=de, source=override", proc.stdout)
        self.assertIn("agenda: Agenda", proc.stdout)
        self.assertIn("(no de wording authored; en used)", proc.stdout)


if __name__ == "__main__":
    unittest.main()
