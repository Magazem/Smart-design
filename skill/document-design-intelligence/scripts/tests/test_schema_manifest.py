#!/usr/bin/env python3
"""data/schema-manifest.json is GENERATED. This test says so mechanically.

RULING M: `display_columns` was added to the shipped manifest BY HAND. The file
is written by research/build-manifest.py, so the next run of that generator
wiped the key and the docx handoff block would have gone silently empty again --
the exact v0.1.0 blocker, reintroduced by the fix for it. Nothing in the suite
noticed, because nothing compared the committed file to what the generator emits.

This does. Regenerate into a temp directory and compare BYTES with the committed
copy. Bytes, not text: `Path.read_text` opens in universal-newlines mode and
silently folds CRLF to LF on read, which would make a line-ending comparison
pass no matter what -- and line endings are the one axis a Windows working copy
(CRLF on disk, LF in git's object store) is most likely to differ on. Both sides
here are read as bytes off a Windows filesystem, so this compares CRLF against
freshly-generated CRLF.

The generator lives in research/, OUTSIDE the skill root, and build_zip.py drops
`tests/` from the ZIP anyway -- so this test skips rather than fails wherever the
skill has been unpacked on its own.
"""
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).parent
SCRIPTS_DIR = HERE.parent
SKILL_ROOT = SCRIPTS_DIR.parent
MANIFEST = SKILL_ROOT / "data" / "schema-manifest.json"
#: skill/document-design-intelligence/ -> repo root -> research/
GENERATOR = SKILL_ROOT.parent.parent / "research" / "build-manifest.py"


@unittest.skipUnless(GENERATOR.exists(),
                     f"generator not present ({GENERATOR}) -- skill unpacked without research/")
class TestManifestIsGeneratorOutput(unittest.TestCase):

    def _regenerate(self, tmp):
        """Run the generator with cwd=tmp -- it writes the RELATIVE path
        data/schema-manifest.json, which is why its own docstring says to run it
        from the skill directory."""
        (Path(tmp) / "data").mkdir()
        proc = subprocess.run([sys.executable, str(GENERATOR)],
                              cwd=tmp, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        return Path(tmp) / "data" / "schema-manifest.json"

    def test_committed_manifest_is_byte_identical_to_a_fresh_generation(self):
        with tempfile.TemporaryDirectory() as tmp:
            fresh = self._regenerate(tmp)
            self.assertEqual(
                fresh.read_bytes(), MANIFEST.read_bytes(),
                "data/schema-manifest.json differs from research/build-manifest.py's "
                "output -- it has been hand-edited, and the next regeneration will "
                "silently discard the edit. Put the change in the generator instead.")

    def test_the_comparison_would_catch_a_hand_edit(self):
        """Guard the guard: prove the byte comparison is not vacuous."""
        with tempfile.TemporaryDirectory() as tmp:
            fresh = self._regenerate(tmp)
            tampered = Path(tmp) / "tampered.json"
            shutil.copyfile(fresh, tampered)
            tampered.write_bytes(fresh.read_bytes().replace(b'"schemaVersion": 1', b'"schemaVersion": 2', 1))
            self.assertNotEqual(tampered.read_bytes(), MANIFEST.read_bytes())

    def test_every_handoff_table_declares_display_columns(self):
        """The six tables ddi.py's HANDOFF_VOCAB names must each carry one, or
        that section of the handoff block resolves rows and prints nothing."""
        import json
        sys.path.insert(0, str(SCRIPTS_DIR))
        import ddi
        tables = json.loads(MANIFEST.read_text(encoding="utf-8"))["tables"]
        vocab = ddi.HANDOFF_VOCAB
        named = {vocab[k] for k in vocab if k.endswith("_table")}
        for table in sorted(named):
            with self.subTest(table=table):
                self.assertIn("display_columns", tables[table],
                              f"{table} is read by ddi.py handoff but declares no "
                              "display_columns -- its values will never surface")


if __name__ == "__main__":
    unittest.main()
