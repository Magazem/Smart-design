#!/usr/bin/env python3
"""portable/ is GENERATED. This test says so mechanically.

`research/build-portable.py` builds `portable/AGENTS.md`, `portable/
DDI-LIBRARY.md` and `portable/INSTALL.md` from `data/base/*.csv` -- the exact
same failure mode as `data/schema-manifest.json` (see
test_schema_manifest.py's own docstring): if the committed `portable/` files
ever drift from what the generator emits, the next regeneration silently
discards whatever hand-edit caused the drift. This test regenerates every
file IN MEMORY (importing the generator's own `generate_all()`, not
shelling out) and compares it byte-for-byte with the committed copy.

Bytes, not text: `Path.read_text` opens in universal-newlines mode and would
silently fold CRLF to LF AND mask a real single-`\\r`/mixed-newline
corruption, so this reads both sides as bytes and folds CRLF -> LF itself,
the same way test_schema_manifest.py does, for the same reason (a Windows
checkout legitimately holds CRLF while the generator emits LF; git/
.gitattributes owns that distinction, not this test).

The generator lives in research/, OUTSIDE the skill root, and build_zip.py
drops `tests/` from the ZIP anyway -- this test skips rather than fails
wherever the skill has been unpacked on its own (mirrors
test_schema_manifest.py's `GENERATOR.exists()` guard).
"""
import unittest
from pathlib import Path

HERE = Path(__file__).parent
SCRIPTS_DIR = HERE.parent
SKILL_ROOT = SCRIPTS_DIR.parent
#: skill/document-design-intelligence/ -> repo root -> research/
RESEARCH_DIR = SKILL_ROOT.parent.parent / "research"
GENERATOR = RESEARCH_DIR / "build-portable.py"
PORTABLE_DIR = SKILL_ROOT.parent.parent / "portable"

PORTABLE_FILES = ("AGENTS.md", "DDI-LIBRARY.md", "INSTALL.md")
AGENTS_MD_CHAR_LIMIT = 8000


@unittest.skipUnless(GENERATOR.exists(),
                     f"generator not present ({GENERATOR}) -- skill unpacked without research/")
class TestPortableIsGeneratorOutput(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # `research/build-portable.py`'s filename contains a hyphen, which is not a
        # valid Python identifier for a plain `import` -- load it explicitly by file
        # path instead (importlib.util.spec_from_file_location), the standard way to
        # import a hyphenated-filename module.
        import importlib.util
        spec = importlib.util.spec_from_file_location("build_portable", GENERATOR)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        cls.build_portable = module

    @staticmethod
    def _normalize_newlines(data):
        return data.replace(b"\r\n", b"\n")

    def test_committed_files_are_byte_identical_to_a_fresh_generation(self):
        fresh = self.build_portable.generate_all()
        for name in PORTABLE_FILES:
            with self.subTest(file=name):
                committed_path = PORTABLE_DIR / name
                self.assertTrue(committed_path.exists(),
                                 f"portable/{name} does not exist -- run "
                                 "research/build-portable.py")
                fresh_bytes = fresh[name].encode("utf-8")
                committed_bytes = committed_path.read_bytes()
                self.assertEqual(
                    self._normalize_newlines(fresh_bytes),
                    self._normalize_newlines(committed_bytes),
                    f"portable/{name} differs from research/build-portable.py's output -- "
                    "it has been hand-edited, and the next regeneration will silently "
                    "discard the edit. Put the change in the generator instead.")

    def test_the_comparison_would_catch_a_hand_edit(self):
        """Guard the guard: prove the byte comparison is not vacuous."""
        fresh = self.build_portable.generate_all()
        tampered = fresh["INSTALL.md"] + "\nhand-edited line\n"
        committed_bytes = (PORTABLE_DIR / "INSTALL.md").read_bytes()
        self.assertNotEqual(
            self._normalize_newlines(tampered.encode("utf-8")),
            self._normalize_newlines(committed_bytes))

    def test_agents_md_is_under_the_character_limit(self):
        fresh = self.build_portable.generate_all()
        length = len(fresh["AGENTS.md"])
        self.assertLess(
            length, AGENTS_MD_CHAR_LIMIT,
            f"portable/AGENTS.md is {length} chars -- must stay under "
            f"{AGENTS_MD_CHAR_LIMIT} so any agent's instructions field can hold it")

    def test_committed_agents_md_is_also_under_the_character_limit(self):
        committed = (PORTABLE_DIR / "AGENTS.md").read_text(encoding="utf-8")
        self.assertLess(len(committed), AGENTS_MD_CHAR_LIMIT)

    def test_generation_is_idempotent(self):
        """Running the generator twice must produce byte-identical output --
        no timestamps, no unordered-dict/set iteration leaking through."""
        first = self.build_portable.generate_all()
        second = self.build_portable.generate_all()
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
