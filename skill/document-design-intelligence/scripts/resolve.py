#!/usr/bin/env python3
"""Runtime resolver -- the mechanism ENS's `[NO ENS MATCH]` grep wrapper
(ENS-plugin-rebuild-v2.md:92) stood in for. One fuzzy step, then pure key
resolution -- research/09-library-schema.md section 0.2's "keep, unchanged in
shape" plus its stated deviation (explicit FK-first, biased search as
fallback -- already partially true of current upstream, see research/13 section 2).

Usage:
    python3 resolve.py --query "<free text>" [--brand <slug>] [--json]
    python3 resolve.py --doctype <entry-table-key> [--brand <slug>] [--json]

Manifest-driven, same as validate_data.py: no table or column name is
hard-coded here. The one table this file treats specially is whichever the
manifest marks `"role": "entry"` (see lib/data.py's `entry_table_name`) --
that is the single fuzzy-search entry point (research/09's T1 doctypes).
Every other table is reached only by following a `foreign_keys` reference
from an already-resolved row -- never searched directly.

STAGE 1 -- the only fuzzy step, against the entry table only:
  1. Identity short-circuit: an exact (casefold) match against the entry
     table's key_column, its `Display Name` column, or -- if present -- a
     pipe-separated `Aliases` column, mirrors upstream ui-ux-pro-max's
     `_style_identity`/`_row_identities`
     (upstream-latest/src/ui-ux-pro-max/scripts/core.py:664-702,
     525-531) -- re-implemented from scratch here (see research/13's
     license posture: clone the mechanism, not the code or data).
  2. `--doctype <key>`: resolves that exact key_column value directly, no
     search, no abstention on this stage -- an explicit override for a
     caller that already knows the entry key.
  3. Otherwise: BM25 (from-scratch, k1=1.5/b=0.75 -- the same formula and
     constants found in upstream's core.py:280-344 and unchanged across
     v2.5.0->v2.13.0 per research/01 and research/10) over the manifest's
     declared `searchable_columns`, WITH ABSTENTION: if the top score
     doesn't clear a floor, or -- when more than one candidate scores above
     zero -- the gap between the top two isn't wide enough to be confident,
     this refuses to guess. It prints the top 3 candidates and exits 2.
     This is deliberately a floor+margin check only, not upstream's full
     calibrated multi-signal abstention (synonym rewriting, per-domain
     score floors, coverage -- research/10 section 6): reimplementing that whole
     suite from scratch was out of scope here; the point being proven is
     that abstention is real, not that it is upstream's exact calibration.

  `--brand <slug>`: TWO INDEPENDENT PASSES, each its own BM25 index over a
  restricted row set -- not one search filtered afterward. Pass 1 searches
  only entry rows with `Brand Scope == slug`; only if pass 1 abstains does
  pass 2 run against `Brand Scope == "generic"` rows. This is the
  mechanical fix for the diagnosis in research/05-SYNTHESIS.md's FIELD
  EVIDENCE section ("The identity is an instruction, not data" -- a brand
  row never even entered the search): scoping happens BEFORE scoring, so a
  brand row wins because a competing generic row was never in its index,
  not because it out-scored one in a combined ranking.

STAGE 2+ -- pure foreign-key walk, no second search anywhere:
  every `foreign_keys` entry on the resolved entry row (single value or a
  `;`-separated list) is followed to fetch the referenced row(s), and this
  repeats one level at a time from whatever new rows were just pulled in,
  until no new table is reached.

`validate-brand-resolution` (research/09-library-schema.md section 0.3, section 4 item
5): if `--brand` was given and the final resolved set contains no row
whose `Brand Scope` equals that brand, this refuses to emit at all --
exit 3, one line, `[NO BRAND ROW] brand=<slug> resolved only generic
rows -- refusing to emit`.

Exit codes: 0 resolved - 1 the underlying data fails validate_data.py's
per-key degradation (research/brief-mechanism-perkey.md): a tier-1
structural problem (bad manifest, missing/malformed file, header
mismatch, duplicate key) still refuses the WHOLE dataset before Stage 1
even runs; a tier-2 row-level problem (bad enum/FK/reference/derived
value on one row) only refuses a resolution once it actually walks
through the broken row -- everything that doesn't touch it answers
normally, with a one-line warning header printed either way. This calls
validate_data.validate_tiered(), it does not re-implement any of its
checks - 2 abstained (no confident match) - 3 brand refusal - 4 `--design`
refusal (unknown design key, or design Family != doctype Family).

Output is the resolved decision only, never a whole table: each resolved
row is shown by table + key + only the columns the manifest marks
`searchable_columns` or `foreign_keys` for that table (or an explicit
`"display_columns"` override -- see `_display_columns`). Stdout is the only
channel into the model's context (research/04-packaging.md, research/10 section 6
on stdout-only script output) -- this is written to stay well under the
~40-line budget for any realistic toy-scale request.

ALIGNMENT WITH ANTHROPIC'S BUILT-IN docx/pdf/pptx/xlsx SKILLS
(research/23-anthropic-builtin-skills.md, proprietary -- conventions learned,
no text copied): those skills each expect a target format, a font choice
(+ a named fallback for anything outside their own safe-font list), a page
geometry, and a color palette as their real inputs, and each ends its own
workflow in a "Verify the output" step with a literal command. This file
speaks that vocabulary generically, without hard-coding any of those as
real column names: once the real schema lands, `Render Target Keys`,
`Typeface Key` (+ `Safe Stack Fallback`), `Page Format Key`, and palette
role columns are ordinary `foreign_keys`/`searchable_columns`/
`display_columns` entries, so they surface in this output with no code
change here -- that's the whole point of staying manifest-driven. What
*is* new in this file for that alignment: `description_column` (below) so
an abstain response is a useful clarifying question, not a bare key list,
and a fixed trailer naming this project's own `preflight.py` as the
"verify the output" step for whatever gets rendered from the decision.
"""
from __future__ import annotations

import argparse
import ast
import json
import re
import sys
import unicodedata
from math import log
from pathlib import Path

# Windows: a piped/redirected stdout (as opposed to a real console) falls
# back to the process's ANSI codepage, not UTF-8 -- non-ASCII heading text
# (accented French/German section names) would otherwise mojibake or raise
# UnicodeEncodeError for callers who capture this script's output. Force
# UTF-8 unconditionally so behavior doesn't depend on the caller's console
# codepage or PYTHONIOENCODING. `reconfigure` is Python 3.7+; guard it for
# anything older that might still run this stdlib-only script.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


def _assert_stdlib_only(extra_allowed=()):
    """Fail loudly at import time if a non-stdlib import is ever added here.

    `extra_allowed` permits importing this project's own sibling stdlib-only
    modules (lib/data.py, and validate_data.py in this same directory)
    without weakening the check for any genuine third-party package.
    """
    tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    allowed = set(sys.stdlib_module_names) | set(extra_allowed)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names = [alias.name.split(".")[0] for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            if node.level or node.module is None:
                continue
            names = [node.module.split(".")[0]]
        else:
            continue
        for name in names:
            if name not in allowed:
                raise AssertionError(
                    f"non-stdlib import '{name}' found in {__file__} -- "
                    "this module must be Python stdlib only"
                )


_assert_stdlib_only(extra_allowed={"data", "validate_data"})

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
import data as datalib  # noqa: E402
import validate_data  # noqa: E402 - sibling script in this same directory

DEFAULT_DATA_DIR = Path(__file__).resolve().parent.parent / "data"

# Floor + margin abstention. A candidate must score above the floor at all,
# and -- once there is more than one nonzero-scoring candidate -- the top
# score must clear the runner-up by at least this fraction of the top score
# (a RELATIVE margin, not absolute -- see research/35-notes.md: an absolute
# cutoff tuned on the ~30-row doctypes.csv corpus does not survive smaller
# corpora, e.g. this project's own test fixtures, where score magnitudes are
# on a different scale entirely). Both values derived from the real 12-query
# score distribution against data/base/doctypes.csv, not guessed -- see
# research/35-notes.md for the full derivation and what would break them.
_SCORE_FLOOR = 0.0
_MIN_MARGIN_RATIO = 0.15

# Closed-class function words + the generic request-verbs ("make me a X",
# "erstelle einen X", "fais-moi un X") that appear near-universally across
# doctypes.csv's Keywords cells as filler around the one content word that
# actually distinguishes a doctype. Left unfiltered, these outscore real
# signal words because they're literal substrings of many rows' Keywords
# (research/brief-mechanism.md: "make me a" overlaps cv-generic's "make me
# a resume", outscoring "flyer"). Minimal, closed-class only -- content
# words are never added here even if frequent (e.g. "cv", "présentation").
# en/de confirmed needed by the E3/D3 failures; fr checked against the
# actual Keywords text (data/base/doctypes.csv: "fais-moi", "rédige mon",
# "un cv", "pour ce client", etc.) and included for the same reason.
_STOPWORDS = frozenset({
    # English
    "a", "an", "the", "i", "me", "my", "you", "your", "for", "to", "of",
    "in", "on", "with", "this", "that", "please", "need", "want",
    "make", "build", "draft", "write", "create", "get", "us", "our",
    # German. NOTE: "fuer" not "fur" -- the tokenizer (BM25.tokenize) splits
    # on any non a-z0-9 character, so the accented source word "fur" (u-umlaut)
    # never survives as a single token in the first place (it breaks into
    # single-letter fragments); an accented literal here would be dead code
    # AND fail this project's ASCII-only-source rule (tests/test_ascii_clean.py)
    # -- omitted rather than added as an ineffective non-ASCII entry.
    "ein", "eine", "einen", "einer", "eines", "der", "die", "das",
    "ich", "mir", "mein", "meine", "von", "zu",
    "erstelle", "erstellen", "schreibe",
    # French. Same note applies to accented "rediger"/"rediger" forms --
    # omitted for the same reason (dead + non-ASCII), not because they were
    # judged unnecessary.
    "un", "une", "le", "la", "les", "moi", "mon", "ma", "mes", "vous",
    "pour", "de", "du", "des", "sur", "avec", "ce", "cet", "cette",
    "fais", "faites",
})

# U+00DF LATIN SMALL LETTER SHARP S, built at runtime (not a source string
# literal) so this file stays ASCII-clean per tests/test_ascii_clean.py.
# NFKD does not decompose eszett (unlike umlauts, it has no canonical
# decomposition), so it needs its own fold step before the generic
# combining-mark strip below handles every other accented letter.
_ESZETT = chr(0xDF)

# German ASCII transliteration digraphs (used when a keyboard/source can't
# produce umlauts) fold to the same letter NFKD decomposition leaves behind
# once its combining diaeresis is stripped -- ae/oe/ue -> a/o/u -- so
# "praesentation" and the accented "prasentation" (post-fold) converge on
# one token. Applied after the generic fold, not before: it must only ever
# touch plain ASCII "ae"/"oe"/"ue" sequences, never interact with the
# combining-mark strip itself.
_GERMAN_DIGRAPHS = (("ae", "a"), ("oe", "o"), ("ue", "u"))


# ============ BM25 (from-scratch; see module docstring for the citation) ============

class BM25:
    def __init__(self, k1=1.5, b=0.75):
        self.k1, self.b = k1, b
        self.doc_tokens = []
        self.doc_freqs = {}
        self.idf = {}
        self.avgdl = 0.0
        self.N = 0

    @staticmethod
    def _fold_diacritics(text):
        """NFKD-normalise, fold eszett, strip combining marks, then collapse
        the German ASCII digraphs -- so an accented spelling and its plain
        ASCII/transliterated spelling reduce to the identical token."""
        text = text.replace(_ESZETT, "ss")
        text = unicodedata.normalize("NFKD", text)
        text = "".join(ch for ch in text if not unicodedata.combining(ch))
        for digraph, letter in _GERMAN_DIGRAPHS:
            text = text.replace(digraph, letter)
        return text

    @staticmethod
    def tokenize(text):
        """Applied identically to document text (in fit()) and query text
        (in scores()), so stopword removal and diacritic folding are
        symmetric by construction -- the brief's explicit requirement, not
        something each caller must remember to do."""
        folded = BM25._fold_diacritics(str(text).lower())
        return [t for t in re.split(r"[^a-z0-9]+", folded)
                if t and t not in _STOPWORDS]

    def fit(self, documents):
        self.doc_tokens = [self.tokenize(doc) for doc in documents]
        self.N = len(self.doc_tokens)
        if self.N == 0:
            return
        self.avgdl = sum(len(d) for d in self.doc_tokens) / self.N
        self.doc_freqs = {}
        for tokens in self.doc_tokens:
            for term in set(tokens):
                self.doc_freqs[term] = self.doc_freqs.get(term, 0) + 1
        for term, freq in self.doc_freqs.items():
            self.idf[term] = log((self.N - freq + 0.5) / (freq + 0.5) + 1)

    def scores(self, query):
        query_tokens = self.tokenize(query)
        result = []
        for tokens in self.doc_tokens:
            length = len(tokens)
            term_freqs = {}
            for t in tokens:
                term_freqs[t] = term_freqs.get(t, 0) + 1
            score = 0.0
            for term in query_tokens:
                idf = self.idf.get(term)
                if idf is None:
                    continue
                tf = term_freqs.get(term, 0)
                denom = tf + self.k1 * (1 - self.b + self.b * length / (self.avgdl or 1))
                if denom:
                    score += idf * (tf * (self.k1 + 1)) / denom
            result.append(score)
        return result


# ============ stage 1: identity short-circuit + BM25 with abstention ============

def _row_identities(row, key_column):
    """Mirrors upstream's _row_identities (core.py:525-531): key, Display
    Name, and a pipe-separated Aliases column if the table has one."""
    identities = []
    for value in (row.get(key_column, ""), row.get("Display Name", "")):
        if value:
            identities.append(value)
    aliases = row.get("Aliases", "")
    if aliases:
        identities.extend(a.strip() for a in aliases.split("|") if a.strip())
    return identities


def _identity_match(rows, key_column, query):
    folded = str(query or "").strip().casefold()
    if not folded:
        return None
    matches = [r for r in rows if folded in {i.casefold() for i in _row_identities(r, key_column)}]
    return matches[0] if len(matches) == 1 else None


def _search(rows, key_column, searchable_columns, query, description_column, top_n=3):
    """Return (resolved_row_or_None, diagnostic_dict). Never guesses: a row
    is only ever returned via an exact identity hit or a BM25 result that
    clears both the score floor and the margin check.

    `description_column` names the column shown as each abstention
    candidate's one-line description (see module docstring's alignment
    note re: research/23 -- abstention must be "genuinely useful, not a
    dead end": once the real schema's entry table (T1 doctypes) has richer
    text than a bare name, the manifest can point here at it so a model
    reading an abstain response can ask the user one useful clarifying
    question instead of just a bare key list)."""
    identity_hit = _identity_match(rows, key_column, query)
    if identity_hit is not None:
        return identity_hit, {"method": "identity", "candidates": []}

    if not rows:
        return None, {"method": "bm25", "candidates": [], "reason": "no-rows-to-search"}

    documents = [" ".join(str(r.get(c, "")) for c in searchable_columns) for r in rows]
    bm25 = BM25()
    bm25.fit(documents)
    scores = bm25.scores(query)
    ranked = sorted(range(len(rows)), key=lambda i: scores[i], reverse=True)

    top_idx = ranked[0]
    top_score = scores[top_idx]
    nonzero = [i for i in ranked if scores[i] > 0]
    runner_up_score = scores[ranked[1]] if len(ranked) > 1 else 0.0

    # Zero-score: nothing matched at all, not even weakly -- distinct from
    # an ambiguous tie between real candidates. Listing scoring-0.0 rows
    # here would imply the resolver found something when it found nothing;
    # say so and list no candidates (research/brief-mechanism.md).
    if top_score <= _SCORE_FLOOR:
        return None, {"method": "bm25", "candidates": [], "reason": "no-match",
                       "top_score": round(top_score, 4)}

    abstain = len(nonzero) > 1 and (top_score - runner_up_score) / top_score < _MIN_MARGIN_RATIO

    candidates = [
        {"key": rows[i].get(key_column, ""), "display": rows[i].get("Display Name", ""),
         "description": rows[i].get(description_column, ""), "score": round(scores[i], 4)}
        for i in ranked[:top_n]
    ]

    if abstain:
        return None, {"method": "bm25", "candidates": candidates, "reason": "ambiguous",
                       "top_score": round(top_score, 4), "runner_up_score": round(runner_up_score, 4)}
    return rows[top_idx], {"method": "bm25", "candidates": candidates, "top_score": round(top_score, 4)}


def _resolve_entry(entry_rows, key_column, searchable_columns, query, brand, description_column):
    """Stage 1 including the brand two-pass. Returns (row_or_None, diagnostic)."""
    if brand:
        brand_rows = [r for r in entry_rows if r.get("Brand Scope") == brand]
        row, diag = _search(brand_rows, key_column, searchable_columns, query, description_column)
        diag["pass"] = "brand"
        if row is not None:
            return row, diag
        generic_rows = [r for r in entry_rows if r.get("Brand Scope") == "generic"]
        row, diag = _search(generic_rows, key_column, searchable_columns, query, description_column)
        diag["pass"] = "generic"
        return row, diag
    row, diag = _search(entry_rows, key_column, searchable_columns, query, description_column)
    diag["pass"] = None
    return row, diag


#: research/88: tiny stopword sets for en/fr/de query-language detection. Tokens are
#: lower-cased and diacritic-folded (`fuer` and `fur` both appear for German u-umlaut).
#: Deliberately small: it only has to separate three languages on a short request, and it
#: is consulted ONLY for the family-default step, never for ranking. English is the default
#: on a tie or no signal.
_LANG_WORDS = {
    "en": {"the", "a", "an", "for", "my", "me", "make", "write", "need", "to", "of", "and", "with",
           "i", "please", "create", "build", "design", "help", "our", "on", "in"},
    "fr": {"le", "la", "les", "un", "une", "des", "de", "du", "pour", "mon", "ma", "mes", "fais",
           "moi", "redige", "ecris", "ecrire", "je", "veux", "besoin", "et", "avec", "poste",
           "d", "l", "au", "aux", "cree", "creer"},
    "de": {"ein", "eine", "einen", "einem", "der", "die", "das", "fuer", "fur", "erstelle",
           "schreibe", "mein", "meine", "und", "mit", "ich", "brauche", "zu", "bitte", "von",
           "fuers", "erstellen"},
}

#: research/89 F3: fr/de stopwords that are also name particles ("Maria de la Cruz", "Anna von
#: der Leyen"). Skipped when the NEXT token in the original query is Capitalised.
_NAME_PARTICLES = {"de", "du", "la", "le", "des", "von", "van", "der", "zu", "di", "da"}
#: research/89 F3: a language beats English only with this many DISTINCT signal tokens.
_MIN_LANG_SIGNALS = 2

#: research/89 F4: US paper-size cue. Case-sensitive for US/USA so the pronoun "us" never
#: matches; "U.S." carries no trailing \b (it can never match after the final dot).
_LETTER_CUE_RE = re.compile(
    r"\bUS\b|\bUSA\b|\bU\.S\.(?:A\.)?"
    r"|(?i:\bamerican\b|\bletter[- ]?(?:size|sized|paper|format|sheet)s?\b|8\.5\s*[x\u00d7]\s*11)")

#: research/89 F2: on the folded text `_named_families` searches (punctuation already spaces,
#: so "u.s." is "u s"), these uses of "letter" are a paper size, not the letter family.
_PAPER_LETTER_RE = re.compile(
    r"\b(?:us|u s|usa|american) letter\b|\bletter (?:size|sized|paper|format|sheet)s?\b")

#: research/89 F6/F7: head nouns that name a family without being its Family token. Small on
#: purpose: only unambiguous document nouns (never "paper", "page", "brief", "angebot").
_FAMILY_ALIASES = {
    "slides": "deck", "slide": "deck", "presentation": "deck", "powerpoint": "deck",
    "resume": "cv", "curriculum vitae": "cv", "lebenslauf": "cv",
    "white paper": "whitepaper", "one pager": "one-pager",
    "devis": "quote", "facture": "invoice", "rechnung": "invoice",
}

#: research/89 F9 (orchestrator ruling): a French request carrying one of these cues is not
#: for the French market -- the family's `eu-generic` regional doctype is taken, language fr.
_NON_HOME_REGION_CUES = {
    "fr": {"belgique", "belgium", "bruxelles", "brussels", "wallonie", "suisse", "switzerland",
           "geneve", "lausanne", "romandie", "quebec", "canada", "montreal", "luxembourg"},
}


def _folded_tokens(query):
    return [t for t in re.split(r"[^a-z0-9]+", BM25._fold_diacritics(str(query or "").lower())) if t]


def _detect_language(query):
    """('en' | 'fr' | 'de', evidence) -- evidence is the list of matched stopwords. A language
    beats English only with >= _MIN_LANG_SIGNALS distinct signals AND more than English has
    (research/89 F3); a name particle directly before a Capitalised word is not a signal.
    Consulted for every --query resolution (research/89 F5), never for ranking."""
    raw = re.findall(r"[^\W_]+", str(query or ""))
    folded = [re.sub(r"[^a-z0-9]", "", BM25._fold_diacritics(t.lower())) for t in raw]
    hits = {lang: [] for lang in _LANG_WORDS}
    for i, tok in enumerate(folded):
        if tok in _NAME_PARTICLES and i + 1 < len(raw) and raw[i + 1][:1].isupper():
            continue
        for lang, words in _LANG_WORDS.items():
            if tok in words and tok not in hits[lang]:
                hits[lang].append(tok)
    best = max((l for l in hits if l != "en"), key=lambda l: (len(hits[l]), l))
    if len(hits[best]) >= _MIN_LANG_SIGNALS and len(hits[best]) > len(hits["en"]):
        return best, hits[best]
    return "en", hits["en"]


def _named_families(entry_rows, query):
    """Every family the query names explicitly, in text order (research/88 round 3; research/89
    F2, F6, F7). A family is named by its own Family token (hyphen, space or nothing between
    words; optional plural s) or by an alias in _FAMILY_ALIASES, as a whole word. Longer names
    match first and are masked, so "cover letter" names cover-letter and not letter; paper-size
    uses of "letter" are masked before matching. Why a code rule and not data: an explicit
    family noun is the strongest signal a request carries, but BM25 weighs it like any keyword,
    so incidental words other families list ("paper", "one page", "A4") could outvote it."""
    families = {r.get("Family", "") for r in entry_rows if r.get("Family", "")}
    text = " " + re.sub(r"[^a-z0-9]+", " ", BM25._fold_diacritics(str(query or "").lower())) + " "
    text = _PAPER_LETTER_RE.sub(lambda m: " " * len(m.group(0)), text)
    patterns = [(f, r"[ ]?".join(re.escape(w) for w in f.split("-"))) for f in families]
    patterns += [(f, re.escape(alias)) for alias, f in _FAMILY_ALIASES.items() if f in families]
    patterns.sort(key=lambda p: -len(p[1]))
    found = []
    for family, pat in patterns:
        m = re.search(r"(?<![a-z0-9])" + pat + r"s?(?![a-z0-9])", text)
        if m:
            if family not in [f for _, f in found]:
                found.append((m.start(), family))
            text = text[:m.start()] + " " * (m.end() - m.start()) + text[m.end():]
    return [f for _, f in sorted(found)]


def _named_family(entry_rows, query):
    """Backwards-compatible single-family form: the one named family, else None."""
    named = _named_families(entry_rows, query)
    return named[0] if len(named) == 1 else None


def _choose_default(pool, family, designs_rows, lang="en", query=""):
    """The doctype a plain, unspecific request for `family` resolves to, or None. In order
    (research/88 round 2, research/89 F9/F11):
      1. language: `lang` is fr/de and exactly ONE pool doctype has that Default Language --
         unless the query carries a non-home-region cue for that language (Belgique, Suisse,
         Quebec, ...), in which case the family's `eu-generic` regional doctype is taken;
      2. the family's `Family Default = y` doctype (data, at most one per family);
      3. derived: Region Key blank and Reasoning Key == the family's rank-1 design's, if one;
      4. a single-doctype family's only row.
    A US/letter cue in the query then swaps an `a4-<x>` pick for its `letter-<x>` sibling."""
    chosen = None
    if lang != "en":
        tokens = set(_folded_tokens(query))
        # the fold also collapses German digraphs (ue -> u), so fold the cues the same way
        cues = {BM25._fold_diacritics(c) for c in _NON_HOME_REGION_CUES.get(lang, set())}
        if tokens & cues:
            eu = [r for r in pool if r.get("Region Key", "") == "eu-generic"]
            chosen = eu[0] if len(eu) == 1 else None
        if chosen is None:
            same = [r for r in pool if r.get("Default Language", "") == lang]
            if len(same) == 1:
                chosen = same[0]
    if chosen is None:
        flagged = [r for r in pool if r.get("Family Default", "") == "y"]
        if len(flagged) == 1:
            chosen = flagged[0]
    if chosen is None:
        rank1 = [d for d in designs_rows if d.get("Family", "") == family and d.get("Rank", "") == "1"]
        if len(rank1) == 1:
            derived = [r for r in pool if not r.get("Region Key", "")
                       and r.get("Reasoning Key", "") == rank1[0].get("Reasoning Key", "")]
            if len(derived) == 1:
                chosen = derived[0]
    if chosen is None and len(pool) == 1:
        chosen = pool[0]
    if chosen is None:
        return None
    fmt = chosen.get("Page Format Key", "")
    if fmt.startswith("a4-") and _LETTER_CUE_RE.search(str(query)):
        sibling = [r for r in pool if r.get("Page Format Key", "") == "letter-" + fmt[3:]]
        if len(sibling) == 1:
            chosen = sibling[0]
    return chosen


def _family_pool(entry_rows, family, scopes):
    return [r for r in entry_rows if r.get("Family", "") == family and r.get("Brand Scope", "") in scopes]


def _family_default(entry_rows, key_column, diag, designs_rows, query="", lang="en"):
    """research/88: an `ambiguous` abstention whose top candidates all belong to ONE Family means
    the query carried nothing that separates that family's variants. Resolve to the family's
    designated default (`_choose_default`), else None and the abstention stands. `lang` is the
    effective language (--lang if given, else the detected query language: research/89 F11)."""
    if diag.get("reason") != "ambiguous":
        return None
    top = diag.get("top_score") or 0
    keys = [c["key"] for c in diag.get("candidates", [])
            if top and (top - c["score"]) / top < _MIN_MARGIN_RATIO]
    by_key = {r.get(key_column, ""): r for r in entry_rows}
    cands = [by_key[k] for k in keys if k in by_key]
    families = {r.get("Family", "") for r in cands}
    scopes = {r.get("Brand Scope", "") for r in cands}
    if len(cands) < 2 or len(families) != 1 or "" in families or len(scopes) != 1:
        return None
    family = families.pop()
    return _choose_default(_family_pool(entry_rows, family, scopes), family, designs_rows, lang, query)


# ============ stage 2+: pure FK walk ============

#: FKs that are validated but never walked: a back-pointer whose target is only
#: attached on request (`--design`), so walking it would put a `designs` row in
#: every resolution.
NON_WALK_FKS = {("doc-reasoning", "Design Key")}


def _fk_walk(entry_table, entry_row, tables_spec, all_rows, rows_by_key):
    """Follow every foreign_keys reference from the entry row outward,
    breadth-first, one level at a time, until no new row is reached.

    A plain FK resolves to exactly one row (rows_by_key: {table_name:
    {key_value: row_dict}}, looked up by that table's own key_column). A
    "group" FK (fk_spec's is_group) resolves to EVERY row in the target
    table whose grouping column equals the value -- research/09 Revision
    2's shape, e.g. doctypes."Constraint Set Keys" -> constraints."Set
    Key": many constraint rows legitimately share one Set Key, so this is
    a membership walk, not a key lookup, and can fan out to more than one
    row per token.

    Returns {table_name: [row_dict, ...]} -- the entry row plus everything
    it (transitively) references, each row appearing once even if reached
    by more than one path.
    """
    resolved = {entry_table: [entry_row]}
    entry_key_col = tables_spec[entry_table]["key_column"]
    seen = {(entry_table, entry_row.get(entry_key_col, ""))}
    frontier = [(entry_table, entry_row)]
    group_index_cache = {}

    def group_index(table, column):
        cache_key = (table, column)
        if cache_key not in group_index_cache:
            index = {}
            for row in all_rows.get(table, []):
                value = row.get(column, "")
                if value:
                    index.setdefault(value, []).append(row)
            group_index_cache[cache_key] = index
        return group_index_cache[cache_key]

    while frontier:
        table_name, row = frontier.pop(0)
        spec = tables_spec[table_name]
        for column, raw_fk in spec.get("foreign_keys", {}).items():
            if (table_name, column) in NON_WALK_FKS:
                continue
            ref_table, ref_column, is_list, is_group = datalib.fk_spec(raw_fk)
            value = row.get(column, "")
            if not value:
                continue
            tokens = [t.strip() for t in value.split(";")] if is_list else [value]
            ref_key_col = tables_spec.get(ref_table, {}).get("key_column")
            for token in tokens:
                if not token:
                    continue
                if is_group:
                    matches = group_index(ref_table, ref_column).get(token, [])
                else:
                    single = rows_by_key.get(ref_table, {}).get(token)
                    matches = [single] if single is not None else []
                for ref_row in matches:
                    marker_key = ref_row.get(ref_key_col, "") if ref_key_col else id(ref_row)
                    marker = (ref_table, marker_key)
                    if marker in seen:
                        continue
                    # validate_data.py already confirmed every plain-FK token
                    # resolves; if a match is still empty here the data
                    # changed underfoot -- skip silently rather than crash.
                    seen.add(marker)
                    resolved.setdefault(ref_table, []).append(ref_row)
                    frontier.append((ref_table, ref_row))

    return resolved


def _apply_design_override(entry_row, design_row):
    """research/80-v05-plan.md section 6 P1.5 (`ddi.py resolve --design`):
    shallow copy the resolved entry (doctype) row -- NEVER mutate the row
    dict `load_all_tables` handed back, since that same dict is shared by
    any other resolution running against the same loaded data -- with its
    Reasoning Key replaced by the design's own, so the FK walk that follows
    pulls in the design's doc-reasoning (and therefore its style/palette/
    typeface) instead of the doctype's own default."""
    overridden = dict(entry_row)
    overridden["Reasoning Key"] = design_row.get("Reasoning Key", "")
    return overridden


def _brand_design_reasoning(brand_row, design_reasoning_row, design_row):
    """In-memory doc-reasoning row: the design's own row with the brand row's
    Palette Key / Typeface Key (and blank bias terms for them). Nothing loaded
    is mutated; the synthesized key is never written anywhere."""
    merged = dict(design_reasoning_row)
    merged.update({
        "doc_category": f"{design_reasoning_row.get('doc_category', '')}+{brand_row.get('doc_category', '')}",
        "Palette Key": brand_row.get("Palette Key", ""),
        "Typeface Key": brand_row.get("Typeface Key", ""),
        "Palette Bias Terms": brand_row.get("Palette Bias Terms", ""),
        "Typeface Bias Terms": brand_row.get("Typeface Bias Terms", ""),
        "Design Key": design_row.get("design_key", ""),
    })
    return merged


def _has_brand_row(resolved, brand):
    return any(row.get("Brand Scope") == brand for rows in resolved.values() for row in rows)


# ============ per-key degradation (research/brief-mechanism-perkey.md) ============

def _poisoned_keys(tier2_entries):
    """{table_name: {key_value, ...}} of every row a tier-2 problem was
    found on -- a resolution that never reaches one of these rows is
    unaffected; one that does must refuse, by name."""
    poisoned = {}
    for entry in tier2_entries:
        if entry["key"]:
            poisoned.setdefault(entry["table"], set()).add(entry["key"])
    return poisoned


def _print_tier2_warning(tier2_entries):
    """The whole-dataset gate summary as a WARNING header, not a refusal
    (the brief's explicit requirement) -- one line, so a normal resolution
    stays well under the ~40-line stdout budget; the full per-problem list
    is what `ddi.py check` is for."""
    if not tier2_entries:
        return
    affected_tables = sorted({e["table"] for e in tier2_entries})
    print(f"[DATA WARNING] {len(tier2_entries)} row-level problem(s) in "
          f"{', '.join(affected_tables)} -- degraded to per-key refusal "
          "(run `python3 scripts/validate_data.py data/base` for the full list)")


def _touched_poison(resolved, tables_spec, poisoned):
    """Every tier-2 entry whose (table, key) appears anywhere in `resolved`
    -- the set of broken keys THIS resolution actually walked through."""
    touched = []
    for table_name, rows in resolved.items():
        key_column = tables_spec.get(table_name, {}).get("key_column")
        poisoned_keys = poisoned.get(table_name, set())
        if not key_column or not poisoned_keys:
            continue
        for row in rows:
            key_val = row.get(key_column, "")
            if key_val in poisoned_keys:
                touched.append((table_name, key_val))
    return touched


def _print_refused_path(subject, touched, tier2_entries):
    """Names every refused path -- table, key, and the exact reason -- so
    the caller sees what was skipped and why (the brief's explicit
    requirement), instead of a silent partial answer."""
    print(f'[REFUSED PATH] resolution for "{subject}" touches a broken key -- refusing to resolve:')
    seen = set()
    for table_name, key_val in touched:
        if (table_name, key_val) in seen:
            continue
        seen.add((table_name, key_val))
        for entry in tier2_entries:
            if entry["table"] == table_name and entry["key"] == key_val:
                print(f"  {table_name}/{key_val}: {entry['line']}")


# ============ output ============

def _display_columns(spec):
    """Columns worth showing for a resolved row of this table -- never the
    whole row. A table may declare an explicit `"display_columns"` list to
    override this outright (needed once the real schema lands: a typeface
    row's `Safe Stack Fallback`, say, is neither searchable nor an FK
    column, but a renderer needs it -- research/23's built-in docx/pptx
    skills both need a font choice paired with its fallback). Absent that,
    the default is what the manifest marks searchable, plus this table's
    own FK source columns (so the reader can see why a further row was
    pulled in)."""
    if "display_columns" in spec:
        return list(spec["display_columns"])
    columns = list(spec.get("searchable_columns", []))
    for column in spec.get("foreign_keys", {}):
        if column not in columns:
            columns.append(column)
    return columns


#: Fixed next-step trailer on every successful resolution -- the analog of
#: research/23's built-in skills each ending in a "Verify the output"
#: section with a literal command. We don't render anything ourselves, so
#: we can't name the rendered file yet; this names the exact script the
#: model should run against whatever it renders from the decision above,
#: which is the one part of that command we DO know without guessing.
_PREFLIGHT_HINT = "python3 scripts/preflight.py <rendered-file>  # verify fonts/DPI/print-boxes against this decision"


def _field_value(row, column, spec, entry_key):
    """RULED (research/brief-mechanism.md item 3): a group-FK list column
    (e.g. structures."Section Order") that is empty on this row must never
    surface as a bare empty answer -- an empty list here is expected data,
    not a broken reference. Say so by name instead of printing nothing."""
    value = row.get(column, "")
    if value:
        return value
    fk = spec.get("foreign_keys", {}).get(column)
    if fk is not None and datalib.fk_spec(fk)[3]:  # is_group
        field = column.lower().replace(" ", "-")
        return f"no {field} guidance for {entry_key}"
    return value


def _resolution_payload(resolved, tables_spec, diag, entry_key, language):
    out_tables = {}
    for table_name, rows in resolved.items():
        spec = tables_spec[table_name]
        key_column = spec["key_column"]
        columns = _display_columns(spec)
        out_tables[table_name] = [
            {"key": row.get(key_column, ""),
             **{c: _field_value(row, c, spec, entry_key) for c in columns}}
            for row in rows
        ]
    return {
        "status": "resolved",
        "method": diag.get("method"),
        "pass": diag.get("pass"),
        "resolved": out_tables,
        "language": language,
        "diagnostics": _diagnostics(diag),
        "next_step": _PREFLIGHT_HINT,
    }


def _diagnostics(diag):
    """research/89 F8: the resolver's assumptions, so a caller can tell the user "I assumed a
    generic CV" / "I assumed French" and offer to switch. Only keys that apply are present."""
    out = {}
    for k in ("named_family", "note", "query_language", "query_language_evidence"):
        if diag.get(k):
            out[k] = diag[k]
    if diag.get("candidates"):
        out["candidates"] = diag["candidates"][:3]
    return out


def _resolve_language(entry_spec, entry_row, lang_override):
    """{"value": en|fr|de, "source": "override"|"doctype-default"} -- `--lang`
    always wins; otherwise the entry row's own `language_column` (manifest-
    driven, same idiom as `description_column` above), defaulting to "en" if
    that column is declared but happens to be blank on this row."""
    if lang_override:
        return {"value": lang_override, "source": "override"}
    lang_column = entry_spec.get("language_column")
    default_value = entry_row.get(lang_column, "") if lang_column else ""
    return {"value": default_value or "en", "source": "doctype-default"}


def _print_resolved(resolved, tables_spec, diag, as_json, entry_key, language):
    if as_json:
        print(json.dumps(
            _resolution_payload(resolved, tables_spec, diag, entry_key, language), indent=2))
        return
    header = f"RESOLVED  (method={diag.get('method')}"
    if diag.get("pass"):
        header += f", pass={diag['pass']}"
    if "top_score" in diag:
        header += f", top_score={diag['top_score']}"
    header += ")"
    print(header)
    print(f"language: {language['value']} (source={language['source']})")
    for k, v in _diagnostics(diag).items():
        if k != "candidates":
            print(f"assumed: {k} = {v}")
    for table_name, rows in resolved.items():
        spec = tables_spec[table_name]
        key_column = spec["key_column"]
        columns = _display_columns(spec)
        for row in rows:
            print(f"  {table_name}/{row.get(key_column, '')}")
            for column in columns:
                print(f"    {column}: {_field_value(row, column, spec, entry_key)}")
    print(f"next: {_PREFLIGHT_HINT}")


def _print_abstain(query, diag, as_json):
    # "no-match" (top-1 scored 0, or nothing to search) is a different claim
    # than "ambiguous" (real candidates, margin too thin): the former means
    # the library has nothing for this request at all, so it must list no
    # candidates in either output -- offering 0.0-scoring rows would imply
    # a narrowing that never happened (research/brief-mechanism.md).
    no_match = diag.get("reason") in ("no-match", "no-rows-to-search")
    if as_json:
        status = "no_match" if no_match else "abstained"
        print(json.dumps({"status": status, **diag}, indent=2))
        return
    if no_match:
        print(f'[NO MATCH] "{query}" does not match any doctype in the library -- nothing to suggest')
        return
    if diag.get("reason") == "multiple-families":
        print(f'[ABSTAIN] "{query}" names {len(diag["named_families"])} document families '
              f"({', '.join(diag['named_families'])}) -- ask which to make first, or make each:")
    else:
        print(f'[ABSTAIN] no confident match for "{query}"')
        print("  top candidates -- ask the user which one they meant:")
    for c in diag["candidates"]:
        line = f"    {c['key']!r} \"{c['display']}\""
        if "score" in c:
            line += f"  score={c['score']}"
        if c.get("family"):
            line += f"  family={c['family']}"
        description = c.get("description", "")
        if description and description != c["display"]:
            line += f"  -- {description}"
        print(line)


# ============ CLI ============

def build_arg_parser():
    parser = argparse.ArgumentParser(
        description="Resolve one request against the document library and print the decision.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--query", default=None, help="free-text request (the only fuzzy step)")
    parser.add_argument("--brand", default=None, help="brand slug to prefer (two-pass resolution)")
    parser.add_argument("--doctype", default=None,
                         help="exact entry-table key -- resolves directly, no search")
    parser.add_argument("--design", default=None,
                         help="design key (data/base/designs.csv) -- overrides the resolved "
                              "doctype's Reasoning Key with this design's own before the FK "
                              "walk, and includes the design row in the resolved output")
    parser.add_argument("--lang", default=None, choices=("en", "fr", "de"),
                         help="override the resolved doctype's own Default Language")
    parser.add_argument("--data-dir", default=None,
                         help=f"data directory (default: {DEFAULT_DATA_DIR})")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    parser = build_arg_parser()
    args = parser.parse_args(argv)

    if not args.query and not args.doctype:
        parser.error("one of --query or --doctype is required")

    data_dir = Path(args.data_dir) if args.data_dir else DEFAULT_DATA_DIR

    tier1_ok, tier1_lines, tier2_entries, _summary = validate_data.validate_tiered(data_dir)
    if not tier1_ok:
        for line in tier1_lines:
            print(line)
        print(f"\n[DATA INVALID] {len(tier1_lines)} structural problem(s) -- refusing to resolve")
        return 1

    if not args.json:
        _print_tier2_warning(tier2_entries)
    poisoned = _poisoned_keys(tier2_entries)

    manifest = datalib.load_manifest(data_dir)
    tables = manifest["tables"]
    entry_name = datalib.entry_table_name(tables)  # tier1_ok above already confirmed exactly one
    entry_spec = tables[entry_name]
    key_column = entry_spec["key_column"]
    searchable_columns = entry_spec.get("searchable_columns", [])
    description_column = entry_spec.get("description_column", "Display Name")

    problems = datalib.ProblemLog()
    all_rows = datalib.load_all_tables(data_dir, tables, problems)
    entry_rows = all_rows[entry_name]

    if args.doctype:
        matches = [r for r in entry_rows if r.get(key_column, "") == args.doctype]
        entry_row = matches[0] if len(matches) == 1 else None
        diag = {"method": "doctype-direct", "candidates": [], "pass": None}
    else:
        q_lang, q_evidence = _detect_language(args.query)
        eff_lang = args.lang or q_lang
        # an exact doctype key / Display Name is the strongest signal of all: never narrowed away
        named_all = [] if _identity_match(entry_rows, key_column, args.query) is not None             else _named_families(entry_rows, args.query)
        scope = {args.brand} if args.brand else {"generic"}
        designs_rows = all_rows.get("designs", [])
        if len(named_all) >= 2:
            # research/89 F7: never silently pick one of two named documents
            cands = []
            for fam in named_all:
                pool = _family_pool(entry_rows, fam, scope) or _family_pool(entry_rows, fam, {"generic"})
                row = _choose_default(pool, fam, designs_rows, eff_lang, args.query) or (pool[0] if pool else None)
                if row is not None:
                    cands.append({"key": row.get(key_column, ""), "display": row.get("Display Name", ""),
                                  "description": row.get(description_column, ""), "family": fam})
            entry_row, diag = None, {"method": "named-family", "reason": "multiple-families",
                                     "named_families": named_all, "candidates": cands, "pass": None}
        else:
            named = named_all[0] if named_all else None
            if named:
                narrowed = [r for r in entry_rows if r.get("Family", "") == named]
                entry_row, diag = _resolve_entry(
                    narrowed, key_column, searchable_columns, args.query, args.brand, description_column)
                diag["named_family"] = named
                if entry_row is None and diag.get("reason") != "ambiguous":
                    # research/89 F6/F12: a named family with no keyword hit (plurals, bare nouns)
                    # goes to that family's default rather than to a search over other families
                    pool = _family_pool(entry_rows, named, scope) or _family_pool(entry_rows, named, {"generic"})
                    entry_row = _choose_default(pool, named, designs_rows, eff_lang, args.query)
                    if entry_row is not None:
                        diag = dict(diag, method="family-default", reason=None,
                                    note="query named the family but no variant; resolved to its designated default")
                entry_rows = narrowed
            else:
                entry_row, diag = _resolve_entry(
                    entry_rows, key_column, searchable_columns, args.query, args.brand, description_column
                )
        if q_lang != "en":
            diag["query_language"] = q_lang
            diag["query_language_evidence"] = q_evidence
        if (entry_row is not None and not args.lang and eff_lang == "fr"
                and diag.get("method") == "bm25"
                and set(_folded_tokens(args.query))
                & {BM25._fold_diacritics(c) for c in _NON_HOME_REGION_CUES["fr"]}):
            # research/89 F9 ruling: a French request with a Belgian/Swiss/Canadian cue is not for
            # the French market, even when BM25 matched a keyword ("suisse" -> cv-dach): take the
            # family's eu-generic doctype, language fr
            fam_pool = _family_pool(entry_rows, entry_row.get("Family", ""), {entry_row.get("Brand Scope", "")})
            eu = [r for r in fam_pool if r.get("Region Key", "") == "eu-generic"]
            if len(eu) == 1 and eu[0] is not entry_row:
                entry_row = eu[0]
                diag = dict(diag, method="family-default",
                            note="French request with a non-France cue: resolved to the EU-generic doctype")

    if entry_row is not None and args.query and not args.doctype:
        # research/89 F10: an explicit A4 cue swaps a letter-size pick back to its a4 sibling
        # (symmetric to the US/letter cue in _choose_default); never when a US cue is also present
        fmt = entry_row.get("Page Format Key", "")
        if (fmt.startswith("letter-") and re.search(r"\bA4\b", str(args.query), re.IGNORECASE)
                and not _LETTER_CUE_RE.search(str(args.query))):
            sib = [r for r in _family_pool(entry_rows, entry_row.get("Family", ""), {entry_row.get("Brand Scope", "")})
                   if r.get("Page Format Key", "") == "a4-" + fmt[7:]]
            if len(sib) == 1:
                entry_row = sib[0]
                diag = dict(diag, note="explicit A4 cue: swapped to the A4 sibling")

    if entry_row is None and args.query and not args.doctype and diag.get("reason") == "ambiguous":
        default_row = _family_default(entry_rows, key_column, diag, all_rows.get("designs", []),
                                      args.query, args.lang or diag.get("query_language", "en"))
        if default_row is not None:
            entry_row = default_row
            diag = dict(diag, method="family-default", reason=None,
                        note="query named no variant of the family; resolved to its designated default")

    if entry_row is None:
        _print_abstain(args.query or args.doctype, diag, args.json)
        return 2

    design_row = None
    original_entry_row = entry_row
    brand_reasoning_key = None
    if args.design:
        designs_spec = tables.get("designs", {})
        designs_key_col = designs_spec.get("key_column", "design_key")
        design_row = next(
            (r for r in all_rows.get("designs", []) if r.get(designs_key_col, "") == args.design),
            None,
        )
        if design_row is None:
            print(f"[NO SUCH DESIGN] design={args.design!r} not found in designs table -- refusing")
            return 4
        entry_family = entry_row.get("Family", "")
        design_family = design_row.get("Family", "")
        if design_family != entry_family:
            print(f"[DESIGN FAMILY MISMATCH] design={args.design!r} Family={design_family!r} "
                  f"!= doctype Family={entry_family!r} -- refusing")
            return 4
        entry_row = _apply_design_override(entry_row, design_row)
        brand_reasoning_key = original_entry_row.get("Reasoning Key", "")

    language = _resolve_language(entry_spec, entry_row, args.lang)
    if diag.get("query_language") and not args.lang:
        # research/89 F5: a detected French/German request gets its headings in that language
        # on every path, not only the family-default one; --lang always wins.
        language = {"value": diag["query_language"], "source": "query"}

    rows_by_key = {
        name: {r.get(spec["key_column"], ""): r for r in all_rows[name]}
        for name, spec in tables.items() if spec.get("key_column")
    }
    if (design_row is not None and original_entry_row.get("Brand Scope", "generic") != "generic"
            and brand_reasoning_key in rows_by_key.get("doc-reasoning", {})):
        # R2 F1: the design supplies layout/style, the brand keeps its colour/type.
        merged = _brand_design_reasoning(
            rows_by_key["doc-reasoning"][brand_reasoning_key],
            rows_by_key["doc-reasoning"].get(design_row.get("Reasoning Key", ""), {}),
            design_row)
        rows_by_key["doc-reasoning"] = dict(rows_by_key["doc-reasoning"],
                                            **{merged["doc_category"]: merged})
        entry_row = dict(entry_row, **{"Reasoning Key": merged["doc_category"]})
    resolved = _fk_walk(entry_name, entry_row, tables, all_rows, rows_by_key)

    if design_row is not None:
        resolved["designs"] = [design_row]

    touched = _touched_poison(resolved, tables, poisoned)
    if touched:
        _print_refused_path(args.query or args.doctype, touched, tier2_entries)
        return 1

    if args.brand and not _has_brand_row(resolved, args.brand):
        print(f"[NO BRAND ROW] brand={args.brand} resolved only generic rows -- refusing to emit")
        return 3

    _print_resolved(resolved, tables, diag, args.json, entry_row.get(key_column, ""), language)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
