#!/usr/bin/env python3
"""Regression guard: every document family the library can lay out must be
reachable from SKILL.md's frontmatter `description`.

Why this file exists
--------------------
v0.2 added section guidance for fifteen document families but nobody widened
the description's trigger noun list. The description is the ONLY activation
lever (references/activation.md): a skill that never activates never has its
SKILL.md body read, so no amount of correct data/base content can rescue a
doctype whose noun is absent from that one string. The v0.2 acceptance run
failed on all of prompts 1-5 for exactly this reason -- "invoice", "memo",
"proposal" and "one-pager" appear nowhere in the shipped description.

The rule
--------
For every row of data/base/doctypes.csv with a non-empty Structure Key, at
least one of its Keywords phrases, or its display-name noun, must appear in
the description -- case- and diacritic-folded, token-level -- in at least one
language.

Two deliberate narrowings, both of which make the test stricter, not looser:

1. Only the POSITIVE region of the description counts. Everything from
   "When a specific file format" onward is the deferral/exclusion boundary --
   the sentences that tell the model NOT to fire. "PowerPoint" and ".pptx"
   live only there, so crediting slide-deck-projection from them would score
   the skill as covered by the very sentence that silences it.

2. Matching is token-level, not substring. "brief" does not count as a hit
   inside "briefing", and "gate" does not count inside "gatefold". English
   plurals are folded (description says "brochures", the CSV says
   "brochure"), and diacritics are stripped so "depliant" matches
   "dpliant" and "Broschure" matches "Broschre".

GENERIC_COVERED below is the point of this file. A doctype that is reachable
only through a broader parent noun -- cv-academic through "CVs",
brochure-gatefold through "brochures" -- passes ONLY if it is listed there
with the parent noun it rides on. Adding a family without stating that claim
out loud is what this test is here to stop.
"""
import csv
import re
import unicodedata
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent.parent
SKILL_MD = SKILL_ROOT / "SKILL.md"
DOCTYPES_CSV = SKILL_ROOT / "data" / "base" / "doctypes.csv"

# Everything from here on is the deferral/exclusion boundary, not coverage.
# Candidate H rewrote that boundary sentence: it used to open "When a specific
# file format", and the old marker string stopped existing the moment H landed.
# A marker that is never found silently widens the positive region to the whole
# description -- the narrowing above would have gone quiet without failing.
NEGATIVE_SCOPE_MARKER = "Creating any document type above"

# Doctypes reachable only through a broader parent noun already in the
# description. Value = the parent noun it rides on, which must itself still be
# present. If you add a family and it lands here, say so explicitly -- do not
# widen the rule.
GENERIC_COVERED = {
    # Every regional CV variant rides on the single noun "CVs" / "resumes".
    # The description cannot afford one noun per region and does not need to:
    # region is a resolver dimension, not an activation dimension.
    "cv-us": "resumes",
    "cv-eu-generic": "CVs",
    "cv-eu-europass": "CVs",          # "europass" itself is absent
    "cv-france": "CVs",
    "cv-gulf-gcc": "CVs",
    "cv-generic": "CVs",
    "cv-academic": "CVs",             # "academic cv" itself is absent
    # Panel count and page size are page-format dimensions, not content ones.
    "brochure-trifold-a4": "brochures",
    "brochure-gatefold": "brochures",  # "gatefold" itself is absent
    "brochure-flyer-letter": "flyers",
    "brochure-flyer-a4": "flyers",
    # "reports" fires for both report families; the TOC is what separates
    # them, and that is a structures.csv distinction, not a trigger one.
    "report-long-toc": "reports",
    # All three deck variants ride on "slide decks" / "presentations".
    # German rides on the loanword "deck" inside "slide decks" -- German
    # "Praesentation" and "Folien" are both absent, dropped from candidate G
    # for character budget (see research/38-description-candidate.md, G.6).
    "slide-deck-projection": "slide decks",
    "slide-deck-document": "slide decks",
    "slide-deck-handout": "slide decks",
}

# EMPTY, and it stays empty. This was the skip list that held invoice-tabular
# and one-pager out of the rule while candidate G was unapplied -- an xfail in
# all but name. G has landed ("invoice", "facture", "Rechnung", "one-pager" are
# in the description), so both doctypes are now guarded for real by the rule
# below. Never re-populate this to make a red build green: widen the
# description instead, or declare the family in GENERIC_COVERED.
PENDING_CANDIDATE_G = set()


def _read_description():
    """Read the live description out of SKILL.md's frontmatter at runtime, so
    this test fails the moment someone edits it."""
    text = SKILL_MD.read_text(encoding="utf-8")
    match = re.search(r'^description:\s*"(.*)"\s*$', text, re.M)
    if match is None:
        raise AssertionError("SKILL.md has no double-quoted frontmatter description")
    return match.group(1)


def _fold(text):
    decomposed = unicodedata.normalize("NFD", text)
    return "".join(c for c in decomposed if unicodedata.category(c) != "Mn").lower()


def _tokens(text):
    return [t for t in re.sub(r"[^a-z0-9]+", " ", _fold(text)).split() if t]


# Words that must never be singularised: acronyms and region codes where the
# trailing "s" is part of the word.
_NEVER_SINGULAR = {"ats", "us", "uk", "eu", "gcc", "uae", "dach", "css"}


def _singular(token):
    if token in _NEVER_SINGULAR:
        return token
    if len(token) >= 4 and token.endswith("es") and token[-3:-2] in ("h", "x", "s", "z"):
        return token[:-2]
    if len(token) >= 3 and token.endswith("s") and not token.endswith("ss"):
        return token[:-1]
    return token


def _norm(text):
    return [_singular(t) for t in _tokens(text)]


class _Description:
    """The positive region of the description, prepared for token matching."""

    def __init__(self, raw):
        cut = raw.find(NEGATIVE_SCOPE_MARKER)
        if cut < 0:
            raise AssertionError(
                "NEGATIVE_SCOPE_MARKER %r is not in the description. The "
                "boundary sentence was reworded; update the marker. Falling "
                "back to the whole string would count the deferral sentence "
                "as coverage and quietly void this file's main narrowing."
                % NEGATIVE_SCOPE_MARKER)
        self.positive = raw[:cut]
        self.tokens = _norm(self.positive)
        self.items = []
        for chunk in re.split(r"[;,:.()]", self.positive):
            item = _norm(chunk)
            while item and item[0] in ("also", "and", "or"):
                item = item[1:]
            if item:
                self.items.append(item)

    def match(self, phrase):
        """'full' when the phrase is a whole list item or trigger utterance,
        'fragment' when it only appears inside a longer one, None otherwise."""
        want = _norm(phrase)
        if not want:
            return None
        if any(item == want for item in self.items):
            return "full"
        span = len(want)
        for i in range(len(self.tokens) - span + 1):
            if self.tokens[i:i + span] == want:
                return "fragment"
        return None


def _display_name_nouns(display_name):
    """The doctype's own name: the head phrase before any '--' or '(', split on
    '/', plus that phrase's final token ('Formal business letter' -> 'letter')."""
    head = re.split(r"\s--\s|\s\(", display_name)[0]
    nouns = []
    for part in head.split("/"):
        part = part.strip()
        if not part:
            continue
        nouns.append(part)
        tokens = _tokens(part)
        if len(tokens) > 1:
            nouns.append(tokens[-1])
    return nouns


def _load_doctypes():
    with DOCTYPES_CSV.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


class DescriptionCoverageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.desc = _Description(_read_description())
        cls.rows = _load_doctypes()
        cls.structured = [r for r in cls.rows if r["Structure Key"].strip()]
        # A keyword shared with another doctype cannot distinguish this family,
        # so it counts as generic coverage rather than specific coverage.
        counts = {}
        for row in cls.rows:
            phrases = {_fold(k).strip() for k in row["Keywords"].split(",") if k.strip()}
            for phrase in phrases:
                counts[phrase] = counts.get(phrase, 0) + 1
        cls.share = counts

    def _keywords(self, row):
        return [k.strip() for k in row["Keywords"].split(",") if k.strip()]

    def _hits(self, row):
        """(specific, generic) lists of phrases from this row found in the
        positive region of the description."""
        specific, generic = [], []
        for phrase in self._keywords(row):
            kind = self.desc.match(phrase)
            if kind is None:
                continue
            unique = self.share[_fold(phrase).strip()] == 1
            (specific if unique and kind == "full" else generic).append(phrase)
        for noun in _display_name_nouns(row["Display Name"]):
            if self.desc.match(noun) is not None:
                generic.append("display name: " + noun)
        return specific, generic

    def test_every_structured_doctype_is_reachable(self):
        """The rule. A doctype the library can lay out but the description
        cannot trigger is dead weight in the shipped skill."""
        unreachable = []
        for row in self.structured:
            key = row["doc_key"]
            if key in PENDING_CANDIDATE_G:
                continue
            specific, generic = self._hits(row)
            if not specific and not generic:
                unreachable.append(key)
        self.assertEqual(
            unreachable, [],
            "no keyword or display-name noun of these doctypes appears in the "
            "description's positive region, so the skill can never fire on "
            "them: %s. Add the noun to SKILL.md's description, or, if the "
            "family is genuinely reachable through a broader noun, add it to "
            "GENERIC_COVERED with that noun named." % unreachable)

    def test_generic_only_doctypes_are_declared(self):
        """A family reachable only through a parent noun has to say so."""
        undeclared = []
        for row in self.structured:
            key = row["doc_key"]
            if key in PENDING_CANDIDATE_G:
                continue
            specific, generic = self._hits(row)
            if not specific and generic and key not in GENERIC_COVERED:
                undeclared.append((key, generic))
        self.assertEqual(
            undeclared, [],
            "these doctypes are reachable only through a broader parent noun "
            "and must be listed in GENERIC_COVERED with the noun they ride "
            "on: %s" % undeclared)

    def test_generic_covered_parents_are_still_present(self):
        """The declared parent noun must actually be in the description --
        otherwise the list is a comment, not a check."""
        missing = [(key, parent) for key, parent in sorted(GENERIC_COVERED.items())
                   if self.desc.match(parent) is None]
        self.assertEqual(
            missing, [],
            "GENERIC_COVERED names parent nouns that are no longer in the "
            "description: %s" % missing)

    def test_generic_covered_has_no_stale_entries(self):
        """Once a family gets its own noun, take it off the generic list."""
        by_key = {r["doc_key"]: r for r in self.rows}
        stale = []
        for key in sorted(GENERIC_COVERED):
            row = by_key.get(key)
            self.assertIsNotNone(row, "GENERIC_COVERED names an unknown doctype: %s" % key)
            specific, _ = self._hits(row)
            if specific:
                stale.append((key, specific))
        self.assertEqual(
            stale, [],
            "these doctypes now have their own noun in the description and "
            "should be removed from GENERIC_COVERED: %s" % stale)

    def test_pending_list_has_no_stale_entries(self):
        """Forces PENDING_CANDIDATE_G empty the moment candidate G is applied."""
        by_key = {r["doc_key"]: r for r in self.rows}
        fixed = []
        for key in sorted(PENDING_CANDIDATE_G):
            row = by_key.get(key)
            self.assertIsNotNone(row, "PENDING_CANDIDATE_G names an unknown doctype: %s" % key)
            specific, generic = self._hits(row)
            if specific or generic:
                fixed.append(key)
        self.assertEqual(
            fixed, [],
            "candidate G (or an equivalent edit) has landed for %s -- remove "
            "them from PENDING_CANDIDATE_G so the rule guards them for real. "
            "See research/38-description-candidate.md." % fixed)

    def test_description_still_fits_the_upload_cap(self):
        """claude.ai's Skills upload UI rejects at 1024: 1023 is the maximum."""
        raw = _read_description()
        self.assertLessEqual(
            len(raw), 1023,
            "description is %d characters; claude.ai enforces 'under 1024'" % len(raw))


if __name__ == "__main__":
    unittest.main()
