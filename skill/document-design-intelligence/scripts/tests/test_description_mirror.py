#!/usr/bin/env python3
"""Regression guard: `references/activation.md`'s "as shipped" block must equal
SKILL.md's frontmatter description BYTE FOR BYTE.

Why this file exists
--------------------
RESUME.md carries a binding note that the fenced block under "## The description
as shipped" is a copy of the live description and must stay that way. Nothing
enforced it. The description was edited three times (candidates F, G and H) and
the mirror was checked by hand each time; the check used
`" ".join(x.split())`-style whitespace folding and was reported as
"byte-identical", which is exactly how a real difference could pass unnoticed.
Whitespace folding is not byte comparison. This file does the byte comparison.

Two deliberate choices
----------------------
1. **Both strings are read from disk at runtime.** Neither is embedded here. A
   test carrying its own copy of the description would be a third place to
   forget to update, and would go green while both real files drifted together.
2. **The block is located by a marker, and a missing marker is a hard failure**,
   not a silent skip. This is the same trap `test_description_coverage.py` hit
   when candidate H deleted the string its NEGATIVE_SCOPE_MARKER pointed at: a
   locator that finds nothing must shout, because a test that quietly checks
   nothing is worse than no test.
"""
import re
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent.parent
SKILL_MD = SKILL_ROOT / "SKILL.md"
ACTIVATION_MD = SKILL_ROOT / "references" / "activation.md"

# The heading the fenced copy lives under. If this string stops existing, the
# section was renamed and this file must be updated deliberately -- see
# _read_mirror_block, which refuses to guess.
MIRROR_SECTION_MARKER = "## The description as shipped"

FIX_HINT = (
    "SKILL.md's frontmatter description and the fenced block under "
    "'%s' in references/activation.md are the same string in two places and "
    "must be edited together, in the same change. Copy the description from "
    "SKILL.md into references/activation.md verbatim, on one line, with no "
    "reflowing and no whitespace normalisation."
) % MIRROR_SECTION_MARKER


def _read_description_bytes():
    """The live description, exactly as it sits inside SKILL.md's frontmatter."""
    text = SKILL_MD.read_text(encoding="utf-8")
    match = re.search(r'^description:\s*"(.*)"\s*$', text, re.M)
    if match is None:
        raise AssertionError(
            "SKILL.md has no double-quoted frontmatter description, so there is "
            "nothing to mirror. " + FIX_HINT)
    return match.group(1).encode("utf-8")


def _read_mirror_block_bytes():
    """The fenced block under the marker heading in activation.md."""
    text = ACTIVATION_MD.read_text(encoding="utf-8")
    start = text.find(MIRROR_SECTION_MARKER)
    if start < 0:
        raise AssertionError(
            "MIRROR_SECTION_MARKER %r is not in references/activation.md. The "
            "section was renamed or removed, so this test can no longer find "
            "the copy it is supposed to guard -- it would otherwise pass by "
            "checking nothing. Update the marker in this file to the new "
            "heading. %s" % (MIRROR_SECTION_MARKER, FIX_HINT))
    fence = re.search(r"^```\n(.*?)\n```$",
                      text[start + len(MIRROR_SECTION_MARKER):],
                      re.S | re.M)
    if fence is None:
        raise AssertionError(
            "no fenced code block follows %r in references/activation.md. The "
            "mirrored description is supposed to be the first fenced block "
            "under that heading. %s" % (MIRROR_SECTION_MARKER, FIX_HINT))
    return fence.group(1).encode("utf-8")


class DescriptionMirrorTest(unittest.TestCase):
    def test_activation_md_mirrors_the_description_byte_for_byte(self):
        """The rule. Bytes, not folded whitespace, not a normalised copy."""
        want = _read_description_bytes()
        got = _read_mirror_block_bytes()
        if want == got:
            return

        detail = ["references/activation.md's 'as shipped' block does not match "
                  "SKILL.md's description."]
        if len(want) != len(got):
            detail.append(
                "Lengths differ: SKILL.md %d bytes, activation.md %d bytes."
                % (len(want), len(got)))
        first = next((i for i in range(min(len(want), len(got)))
                      if want[i] != got[i]), min(len(want), len(got)))
        detail.append(
            "First difference at byte %d.\n  SKILL.md       ...%r...\n"
            "  activation.md  ...%r..."
            % (first,
               want[max(0, first - 40):first + 40],
               got[max(0, first - 40):first + 40]))
        detail.append(FIX_HINT)
        self.fail("\n".join(detail))

    def test_the_mirror_block_is_a_single_line(self):
        """A reflowed copy compares unequal for a reason no reader would guess
        from a byte offset, so say the real thing out loud instead."""
        got = _read_mirror_block_bytes()
        self.assertNotIn(
            b"\n", got,
            "the mirrored description in references/activation.md has been "
            "wrapped across lines. It must stay on exactly one line so it can "
            "be compared to SKILL.md's single-line frontmatter value. " +
            FIX_HINT)


if __name__ == "__main__":
    unittest.main()
