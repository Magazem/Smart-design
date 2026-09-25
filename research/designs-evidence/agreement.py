#!/usr/bin/env python3
"""
research/designs-evidence/agreement.py

Generic inter-coder agreement computer for research/82-design-ranking-protocol.md §7
(second coder / falsifier), amended by research/82a-clarifications-1.md C10 (family-wide
sample). Reusable across families: pass the family name, one or more first-coder evidence
files (each may cover one corpus), and the second-coder evidence file.

Usage:
    python agreement.py --family cv \
        --first GH:research/designs-evidence/cv-corpus-github.md \
                NPM:research/designs-evidence/cv-corpus-npm-ms.md \
        --second research/designs-evidence/cv-second-coder.md \
        [--exclude GH:003 GH:007 GH:008]

    python agreement.py --family deck \
        --first NPM:research/designs-evidence/deck-corpus-npm.md \
                LO:research/designs-evidence/deck-corpus-lo-ms.md \
        --second research/designs-evidence/deck-second-coder.md

Each --first entry is "LABEL:path". LABEL is only used to synthesize an id (LABEL:NNN) for
coded tables that key rows by a bare position/rank column instead of an explicit id column
(e.g. "Pos" in an NPM-style table). Tables that already carry an explicit id column (e.g.
"GH:001", "LO:001", "MS:001") are read as-is and LABEL is only used to sanity-check the
prefix. A single evidence file may contain more than one coded table keyed by different id
prefixes (e.g. `deck-corpus-lo-ms.md` has an `LO.3` section keyed `LO:###` and an `MS.2-3`
section keyed `MS:###`) — every qualifying table in a file is parsed and merged.

Feature set per family (research/82 §4): every family shares 2 universal identity features
(heading, colour) and 3 universal variant features (body, rules/boxes, density). The other 2
identity-feature slots and any extra variant features are family-specific:

  - cv, cover-letter:            identity = columns, heading, colour, header
                                  + variant photo
  - deck:                        identity = background (replaces columns), heading, colour,
                                  title-slide layout (replaces header)
  - invoice, quote:              identity = columns, heading, colour, header
                                  + variant totals position, table rules
  - brochure:                    identity = panel count (replaces columns), heading, colour,
                                  header
  - form:                        identity = columns, heading, colour, field style (replaces
                                  header)
  - letter:                      identity = columns, heading, colour, header
                                  + variant letterhead position
  - poster:                      identity = columns, heading, colour, header
                                  + variant orientation
  - report, whitepaper, proposal: identity = columns, heading, colour, header
                                  + variant cover page
  - any other family:            identity = columns, heading, colour, header (default)

What it does:
  1. Parses every markdown table in each input file (a file may contain many: raw list,
     coded table(s), exclusions log, frequency table, sources...). Selects the "coded"
     table(s) in each file: those whose header row contains (after tolerant normalization,
     using the family's own feature-alias set) a sufficient subset of that family's identity
     features plus an admissible/adm column. A file may contain more than one qualifying
     table (e.g. LO and MS sections); every one found is parsed and merged.
  2. Builds an id -> {feature: value} record for every coded row, id = existing "id" cell if
     present, else f"{LABEL}:{int(pos):03d}".
  3. Also builds a name index (repo/package column, normalized) per id, for cases where the
     id scheme of the first coder(s) and the second coder differ (§7 amendment: the script
     resolves by name and reports the mapping used).
  4. Reads the second coder's own coded table(s) (same parser) — its ids define the sample.
  5. For each sampled id, looks up the matching first-coder row (by id; falls back to name
     match, reporting every fallback used) and compares every shared feature.
  6. Per 82a **C7**: a coded value of `unknown` (or a bare `-` placeholder, used the same way
     by some corpora) means "not codeable from the available preview" and is not a real code;
     such cells are excluded from both coders' denominators for that feature — agreement is
     computed only over items where BOTH coders recorded a non-unknown value for that
     feature, and n (the shared-value count) is reported per feature so this is auditable.
  7. Reports, per feature (grouped identity / variant / admissible), n, agreements, A_f,
     Cohen's kappa, and the full disagreement list (id, feature, coder1 value, coder2 value).
  8. Gate: every IDENTITY feature (plus admissible) must reach A_f >= 0.80 to pass; this is
     the family's falsifier gate. A failing VARIANT feature does not fail the gate — it is
     simply disqualified from filling (§8), which is reported separately.
  9. n=0 for any gating feature (an identity feature, or admissible) is never silently
     reported as passing: it means detection failed (no shared coded sample was found), and
     the script exits non-zero with an explicit ERROR instead of printing PASS.
 10. If --exclude is given, reruns the whole computation with those ids removed from the
     sample (a "sensitivity run"), and reports that table too.

The script only counts and computes; it never judges which coder is "right" (R-d).
"""
import argparse
import math
import re
import sys
from collections import OrderedDict

# ---------------------------------------------------------------------------------------
# Feature aliases: header-cell text (after normalize_header: lowercase, strip non-alnum)
# -> canonical feature key. Deliberately tolerant of abbreviation ("adm", "dens", "bg",
# "head", "rules") and of longer/rephrased headers ("colour use", "title-slide layout",
# "header treatment") so a coded table is recognized regardless of which corpus wrote it.
# ---------------------------------------------------------------------------------------
ALIASES = {
    "id": "id",
    "repo": "name",
    "package": "name",
    "repopackage": "name",
    "repopackagename": "name",
    "item": "name",
    "template": "name",
    "pos": "pos",
    "rank": "pos",
    # universal identity/variant features
    "columns": "columns",
    "column": "columns",
    "heading": "heading",
    "head": "heading",
    "headingclass": "heading",
    "body": "body",
    "bodyclass": "body",
    "colour": "colour",
    "color": "colour",
    "colouruse": "colour",
    "coloruse": "colour",
    "header": "header",
    "headertreatment": "header",
    "rulesboxes": "rules_boxes",
    "rules": "rules_boxes",
    "density": "density",
    "dens": "density",
    "admissible": "admissible",
    "adm": "admissible",
    # deck-specific (replace columns/header)
    "background": "background",
    "bg": "background",
    "titlelayout": "title_layout",
    "titleslidelayout": "title_layout",
    "titleslide": "title_layout",
    "title": "title_layout",
    # cv/cover-letter
    "photo": "photo",
    # invoice/quote
    "totalsposition": "totals_position",
    "totals": "totals_position",
    "tablerules": "table_rules",
    # brochure
    "panelcount": "panel_count",
    "panels": "panel_count",
    # form (corpus files use the bare header "field"; second-coder files spell it out as
    # "field style" — both must resolve to the same canonical key)
    "field": "field_style",
    "fieldstyle": "field_style",
    # letter
    "letterheadposition": "letterhead_position",
    "letterhead": "letterhead_position",
    # poster
    "orientation": "orientation",
    # report/whitepaper/proposal
    "coverpage": "cover_page",
}

# Feature keys whose value is parsed like "admissible" (leading yes/no/y/n, rest is a
# disclosed reason and is ignored for comparison).
YESNO_KEYS = {"admissible"}

# Per-family feature set: (identity feature keys, variant feature keys). "admissible" is
# implicit in every family (always compared, always a gating feature) and is not repeated
# here. Order given here is the report order.
DEFAULT_IDENTITY = ["columns", "heading", "colour", "header"]
DEFAULT_VARIANT = ["body", "rules_boxes", "density"]

FAMILY_FEATURES = {
    "cv": (DEFAULT_IDENTITY, DEFAULT_VARIANT + ["photo"]),
    "cover-letter": (DEFAULT_IDENTITY, DEFAULT_VARIANT + ["photo"]),
    "deck": (["background", "heading", "colour", "title_layout"], DEFAULT_VARIANT),
    "invoice": (DEFAULT_IDENTITY, DEFAULT_VARIANT + ["totals_position", "table_rules"]),
    "quote": (DEFAULT_IDENTITY, DEFAULT_VARIANT + ["totals_position", "table_rules"]),
    "brochure": (["panel_count", "heading", "colour", "header"], DEFAULT_VARIANT),
    "form": (["columns", "heading", "colour", "field_style"], DEFAULT_VARIANT),
    "letter": (DEFAULT_IDENTITY, DEFAULT_VARIANT + ["letterhead_position"]),
    "poster": (DEFAULT_IDENTITY, DEFAULT_VARIANT + ["orientation"]),
    "report": (DEFAULT_IDENTITY, DEFAULT_VARIANT + ["cover_page"]),
    "whitepaper": (DEFAULT_IDENTITY, DEFAULT_VARIANT + ["cover_page"]),
    "proposal": (DEFAULT_IDENTITY, DEFAULT_VARIANT + ["cover_page"]),
}


def family_features(family):
    """Return (identity_keys, variant_keys, all_feature_keys) for a family, falling back to
    the universal default (columns/heading/colour/header + body/rules_boxes/density) for any
    family not listed explicitly."""
    identity, variant = FAMILY_FEATURES.get(family, (DEFAULT_IDENTITY, DEFAULT_VARIANT))
    identity = list(identity)
    variant = list(variant)
    all_keys = identity + variant + ["admissible"]
    return identity, variant, all_keys


def normalize_header(cell):
    return re.sub(r"[^a-z0-9]", "", cell.strip().lower())


def normalize_name(cell):
    # strip markdown emphasis/backticks/links, keep alnum for matching
    cell = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", cell)  # [text](url) -> text
    cell = re.sub(r"[`*_]", "", cell)
    return re.sub(r"[^a-z0-9]", "", cell.strip().lower())


def split_row(line):
    """Split a markdown table row on "|", honoring markdown's own escape convention: a
    backslash-escaped pipe (`\\|`) inside a cell is literal text, not a column separator (seen
    in flyer-second-coder.md's MSF:012 row, which escapes pipes inside a quoted schedule
    string). Escaped pipes are unescaped back to a plain "|" in the returned cell text."""
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    parts = re.split(r"(?<!\\)\|", line)
    return [p.strip().replace("\\|", "|") for p in parts]


def is_separator_row(cells):
    return all(re.fullmatch(r":?-{2,}:?", c.strip()) for c in cells if c.strip() != "") and len(cells) > 0


def find_tables(text):
    """Yield lists of raw rows (each row = list of cell strings) for every markdown table."""
    lines = text.splitlines()
    i = 0
    tables = []
    n = len(lines)
    while i < n:
        if lines[i].lstrip().startswith("|"):
            block = []
            j = i
            while j < n and lines[j].lstrip().startswith("|"):
                block.append(lines[j])
                j += 1
            if len(block) >= 2:
                header = split_row(block[0])
                sep = split_row(block[1])
                if is_separator_row(sep):
                    rows = [split_row(r) for r in block[2:]]
                    tables.append((header, rows))
            i = j
        else:
            i += 1
    return tables


def map_header(header):
    """Return dict: canonical_key -> column index, for columns we recognize."""
    mapping = {}
    for idx, cell in enumerate(header):
        norm = normalize_header(cell)
        if norm in ALIASES:
            key = ALIASES[norm]
            # first match wins (avoid a later alias collision overwriting)
            mapping.setdefault(key, idx)
    return mapping


def table_is_coded(colmap, identity_keys):
    """A table qualifies as "the" (a) coded table for this family if it carries an
    admissible/adm column and a sufficient subset of the family's identity features —
    tolerant of one missing/unrecognized identity header, but never of a missing admissible
    column (every coded table in every family evidence file records admissibility)."""
    if "admissible" not in colmap:
        return False
    matched = sum(1 for k in identity_keys if k in colmap)
    return matched >= max(1, len(identity_keys) - 1)


def clean_feature_cell(raw):
    """Extract the canonical enum value from a feature cell, stripping any disclosed
    parenthetical annotation or free-text note a coder appended after it (e.g.
    `one-accent (gold)` -> `one-accent`; `display (handwriting-style "Excalifont"/Virgil
    glyphs)` -> `display`; `standard (~30 words on content slide)` -> `standard`; `sans —
    also carries an emoji` -> `sans`). Enum values themselves only ever use a plain hyphen
    (`one-accent`, `full-bleed-image`, `2-sidebar`, ...), never a parenthesis or an em/en
    dash, so splitting on those is safe and does not touch the value itself."""
    cell = raw.strip()
    cell = re.sub(r"^`|`$", "", cell)
    cell = cell.strip()
    # markdown emphasis (recode files bold a changed value, e.g. "**image-hero**") is never
    # part of the enum value itself — strip leading/trailing asterisks the same way backticks
    # are stripped above, before the parenthetical/dash splits below.
    cell = re.sub(r"^\*+", "", cell)
    cell = re.sub(r"\*+$", "", cell)
    cell = cell.strip()
    cell = re.split(r"\s*\(", cell, maxsplit=1)[0]
    cell = re.split(r"\s+[–—]\s+", cell, maxsplit=1)[0]
    cell = re.split(r"\s+--\s+", cell, maxsplit=1)[0]
    cell = cell.strip()
    # a value immediately followed by its own opening "**" (e.g. "multi **(disclosed low-
    # confidence...)**") only has that trailing marker exposed once the parenthetical above is
    # split off, since the first strip above only catches asterisks at the then-current end of
    # the whole cell — repeat it now that the parenthetical/dash trailer is gone.
    cell = re.sub(r"\*+$", "", cell).strip()
    return cell


def parse_yesno_cell(raw):
    """Admissible-like cell: leading yes/no (or y/n abbreviation, optionally preceded by
    markdown bold `**`), rest of the cell is a disclosed reason and is dropped."""
    cell = re.sub(r"[`]", "", raw.strip())
    m = re.match(r"^\**\s*(yes|no|y|n)\b", cell, re.I)
    if m:
        val = m.group(1).lower()
        return "yes" if val in ("yes", "y") else "no"
    return clean_feature_cell(raw)  # fall back to raw text, disagreement will show it


UNKNOWN_RE = re.compile(r"(?i)^unknown\b")


def is_uncoded(value):
    """82a C7: a coded value that isn't really a code — the coder couldn't determine this
    feature from the available preview. Covers the literal `unknown` (optionally followed by
    a parenthetical reason, e.g. `unknown (2nd image is ... — C7)`), a bare `-` placeholder
    (used the same way by the MS deck corpus for features it structurally can't code), and
    empty cells."""
    if value is None:
        return True
    v = value.strip()
    if v == "" or v == "-":
        return True
    if UNKNOWN_RE.match(v):
        return True
    if v.lower() in ("n/a", "na"):
        return True
    return False


PAREN_RE = re.compile(r"\(([^)]*)\)")


def strip_parenthetical(cell):
    """Drop any parenthetical annotation from a header cell, e.g. "header (r1)" -> "header",
    "colour (Fm.8.3)" -> "colour", "header (r1, F.11.2)" -> "header"."""
    return PAREN_RE.sub("", cell).strip()


def feature_alias_tokens(feature_key):
    """Every normalized header-cell alias that resolves to this canonical feature key (reverse
    lookup into ALIASES), e.g. feature_key="header" -> {"header", "headertreatment"}."""
    return {norm for norm, key in ALIASES.items() if key == feature_key}


def find_value_column(header, feature_key):
    """Find the column in a header row that carries FEATURE_KEY's override/recode value.

    Recode/verification files (research/*-recode-82ag.md) name their columns in one of three
    ways, all handled here by stripping any parenthetical suffix and exact-matching the result
    against the feature's alias set (never a prefix match, so a column like "header check
    against 82a-general A" — much longer once stripped — is correctly never mistaken for the
    value column itself):
      - a direct/bare column, e.g. "header", "colour" (a fresh-to-82a-general coding with no
        pre-recode value to diff against, e.g. memo's M.6, or a later verification addendum,
        e.g. form's "colour (Fm.8.3)") -> used as-is;
      - a translation-recode pair, e.g. "header (r1)" + "header (r2ag)" (brochure, flyer, form)
        -> the "(r2ag)" column is the override value, the "(r1)" column (the pre-recode value)
        is never selected as a value source, even if it is the only match in a table;
      - a variant spelling of the "(r1)" tag with extra disclosure text in the parens, e.g.
        "header (r1, F.11.2)" (flyer's second recode table) -> still recognized as "r1" (skip)
        because the parenthetical is checked by substring, not exact match.
    Returns the column index, or None if this header row has no usable column for this feature.
    """
    tokens = feature_alias_tokens(feature_key)
    best = None  # (priority, idx); priority 2 = explicit "(r2ag)" override, 1 = direct/bare
    for idx, cell in enumerate(header):
        base = normalize_header(strip_parenthetical(cell))
        if base not in tokens:
            continue
        m = PAREN_RE.search(cell)
        paren = m.group(1).lower() if m else ""
        if "r1" in paren and "r2ag" not in paren:
            continue  # the pre-recode value is never usable as an override
        priority = 2 if "r2ag" in paren else 1
        if best is None or priority > best[0]:
            best = (priority, idx)
    return best[1] if best else None


def load_override_map(path, feature_key):
    """Parse every markdown table in PATH, return (overrides, tables_used) where overrides is
    dict id -> override value for FEATURE_KEY, drawn from whichever table(s) in the file carry
    both an "id" column and a usable value column for this feature (find_value_column). A file
    may have more than one such table (e.g. an original recode table plus a later addendum
    covering additional ids, or additional items added while the recode was in progress); later
    tables' rows win on a repeated id (so a later addendum/correction supersedes an earlier one
    for the same id)."""
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    tables = find_tables(text)
    overrides = OrderedDict()
    tables_used = 0
    for header, rows in tables:
        id_idx = None
        for idx, cell in enumerate(header):
            if normalize_header(cell) == "id":
                id_idx = idx
                break
        if id_idx is None:
            continue
        val_idx = find_value_column(header, feature_key)
        if val_idx is None:
            continue
        tables_used += 1
        for row in rows:
            if len(row) < len(header):
                row = row + [""] * (len(header) - len(row))
            if id_idx >= len(row) or not row[id_idx].strip():
                continue
            rid = clean_feature_cell(row[id_idx])
            rid = re.sub(r"[`*]", "", rid).strip()
            if not rid or val_idx >= len(row):
                continue
            raw_val = row[val_idx]
            val = parse_yesno_cell(raw_val) if feature_key in YESNO_KEYS else clean_feature_cell(raw_val)
            overrides[rid] = val
    return overrides, tables_used


def apply_overrides(first_by_id, override_specs, feature_keys, fh=sys.stdout):
    """override_specs: list of (feature_key, path). For each spec, loads the override map and
    replaces first_by_id[id][feature_key] with the override value for every id already present
    in first_by_id (an override never introduces a new id — it only corrects a feature's value
    for an id the corpus already coded). Prints an audit section listing, per spec, how many
    override rows were found, how many matched an existing first-coder id, and every id where
    the value actually changed (id, old, new) — a silent no-op recode (recoder confirmed the
    original value) is reported too, just with old==new."""
    if not override_specs:
        return
    print("\n## Overrides applied (recode files superseding first-coder values)\n")
    for feature_key, path in override_specs:
        if feature_key not in feature_keys:
            print(f"- `{feature_key}` is not a tracked feature for this family — skipped "
                  f"(no-op) for `{path}`.")
            continue
        overrides, tables_used = load_override_map(path, feature_key)
        if tables_used == 0:
            print(f"- `{feature_key}` from `{path}`: no usable column found for this feature — "
                  f"skipped (no-op).")
            continue
        changed = []
        matched = 0
        for rid, val in overrides.items():
            if rid not in first_by_id:
                continue
            matched += 1
            old = first_by_id[rid].get(feature_key)
            if old != val:
                changed.append((rid, old, val))
            first_by_id[rid][feature_key] = val
        print(f"- `{feature_key}` from `{path}`: {len(overrides)} override row(s) found "
              f"({tables_used} table(s)), {matched} matched an existing first-coder id, "
              f"{len(changed)} value(s) changed.")
        if changed:
            print("\n  | id | old (r1) | new (recode) |", file=fh)
            print("  |---|---|---|", file=fh)
            for rid, old, new in changed:
                print(f"  | {rid} | {old} | {new} |", file=fh)


def load_coded_records(path, feature_keys, identity_keys, label=None):
    """
    Parse a file, return (records, tables_used) where records is dict
    id -> {feature_key: value, '_name': normalized name, '_raw_name': original name text}.
    Every qualifying coded table in the file (there may be more than one, e.g. an LO section
    and an MS section in the same file, each keyed by its own id prefix) is parsed and
    merged.
    """
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    tables = find_tables(text)
    records = OrderedDict()
    tables_used = 0
    for header, rows in tables:
        colmap = map_header(header)
        if not table_is_coded(colmap, identity_keys):
            continue
        tables_used += 1
        for row in rows:
            if len(row) < len(header):
                row = row + [""] * (len(header) - len(row))
            if "id" in colmap and colmap["id"] < len(row) and row[colmap["id"]].strip():
                rid = clean_feature_cell(row[colmap["id"]])
                rid = re.sub(r"[`*]", "", rid).strip()
            elif "pos" in colmap:
                posraw = clean_feature_cell(row[colmap["pos"]])
                posdigits = re.sub(r"[^0-9]", "", posraw)
                if not posdigits:
                    continue
                if label is None:
                    raise ValueError(
                        f"{path}: table has a Pos/Rank column but no id column, and no "
                        f"--first LABEL was given to synthesize one."
                    )
                rid = f"{label}:{int(posdigits):03d}"
            else:
                continue
            rec = {}
            for key in feature_keys:
                if key in colmap and colmap[key] < len(row):
                    raw = row[colmap[key]]
                    if key in YESNO_KEYS:
                        rec[key] = parse_yesno_cell(raw)
                    else:
                        rec[key] = clean_feature_cell(raw)
            name_raw = ""
            if "name" in colmap and colmap["name"] < len(row):
                name_raw = row[colmap["name"]]
            rec["_name"] = normalize_name(name_raw)
            rec["_raw_name"] = name_raw.strip()
            if rid in records:
                # duplicate id within same file across multiple qualifying tables: keep first
                continue
            records[rid] = rec
    return records, tables_used


def build_first_coder_index(first_specs, feature_keys, identity_keys):
    """
    first_specs: list of (label, path). Returns:
      by_id: id -> record (merged across all files; later files don't override earlier)
      by_name: normalized_name -> id  (for fallback matching)
      per_file_report: list of (label, path, n_records, n_tables_used)
    """
    by_id = {}
    by_name = {}
    report = []
    for label, path in first_specs:
        records, tables_used = load_coded_records(path, feature_keys, identity_keys, label=label)
        report.append((label, path, len(records), tables_used))
        for rid, rec in records.items():
            if rid not in by_id:
                by_id[rid] = rec
            if rec.get("_name"):
                by_name.setdefault(rec["_name"], rid)
    return by_id, by_name, report


def cohens_kappa(pairs):
    """pairs: list of (v1, v2). Returns (po, pe, kappa, n)."""
    n = len(pairs)
    if n == 0:
        return None, None, None, 0
    agree = sum(1 for a, b in pairs if a == b)
    po = agree / n
    cats = sorted(set(a for a, _ in pairs) | set(b for _, b in pairs))
    n1 = {c: 0 for c in cats}
    n2 = {c: 0 for c in cats}
    for a, b in pairs:
        n1[a] += 1
        n2[b] += 1
    pe = sum((n1[c] / n) * (n2[c] / n) for c in cats)
    if pe >= 1.0:
        kappa = 1.0 if po >= 1.0 else 0.0
    else:
        kappa = (po - pe) / (1 - pe)
    return po, pe, kappa, n


def compute_feature_table(pairs_by_feature, identity_keys, variant_keys):
    """Returns list of rows (feat, role, n, po, pe, kappa), identity features first (role
    "identity"), then variant features (role "variant"), then admissible last (role
    "admit/exclude")."""
    out = []
    for feat in identity_keys:
        pairs = pairs_by_feature.get(feat, [])
        po, pe, kappa, n = cohens_kappa([(a, b) for _, a, b in pairs])
        out.append((feat, "identity", n, po, pe, kappa))
    for feat in variant_keys:
        pairs = pairs_by_feature.get(feat, [])
        po, pe, kappa, n = cohens_kappa([(a, b) for _, a, b in pairs])
        out.append((feat, "variant", n, po, pe, kappa))
    pairs = pairs_by_feature.get("admissible", [])
    po, pe, kappa, n = cohens_kappa([(a, b) for _, a, b in pairs])
    out.append(("admissible", "admit/exclude", n, po, pe, kappa))
    return out


def gather_pairs(sample_ids, second_records, first_by_id, first_by_name, feature_keys):
    """
    Returns (pairs_by_feature, disagreements, name_fallbacks, unmatched, uncoded_skips)
    pairs_by_feature: feature -> list of (id, c1_value, c2_value)  (only where BOTH coders
    recorded a non-unknown value for that feature — 82a C7)
    disagreements: list of (id, feature, c1_value, c2_value) where they differ
    name_fallbacks: list of (id, resolved_first_coder_id) used when direct id lookup failed
    unmatched: list of ids in the sample with no first-coder match at all (by id or name)
    uncoded_skips: list of (id, feature, c1_value, c2_value) excluded from n because at least
    one side was unknown/uncoded (82a C7 audit trail)
    """
    pairs_by_feature = {k: [] for k in feature_keys}
    disagreements = []
    name_fallbacks = []
    unmatched = []
    uncoded_skips = []
    for sid in sample_ids:
        second_rec = second_records[sid]
        first_rec = first_by_id.get(sid)
        if first_rec is None:
            # id schemes differ: fall back to name match
            nm = second_rec.get("_name")
            fid = first_by_name.get(nm) if nm else None
            if fid is not None:
                first_rec = first_by_id[fid]
                name_fallbacks.append((sid, fid))
            else:
                unmatched.append(sid)
                continue
        for feat in feature_keys:
            v1 = first_rec.get(feat)
            v2 = second_rec.get(feat)
            if v1 is None or v2 is None:
                continue
            if is_uncoded(v1) or is_uncoded(v2):
                uncoded_skips.append((sid, feat, v1, v2))
                continue
            pairs_by_feature[feat].append((sid, v1, v2))
            if v1 != v2:
                disagreements.append((sid, feat, v1, v2))
    return pairs_by_feature, disagreements, name_fallbacks, unmatched, uncoded_skips


def print_feature_table(title, rows, fh=sys.stdout):
    print(f"\n### {title}\n", file=fh)
    print("| Feature | Role | n | Agreements | A_f | Cohen's kappa | Gate (>=0.80) |", file=fh)
    print("|---|---|---|---|---|---|---|", file=fh)
    for feat, role, n, po, pe, kappa in rows:
        if n == 0:
            print(f"| {feat} | {role} | 0 | - | n/a (no shared coded sample) | n/a | n/a |", file=fh)
            continue
        agree = round(po * n)
        gate = "PASS" if po >= 0.80 else "FAIL"
        print(
            f"| {feat} | {role} | {n} | {agree} | {po:.4f} | {kappa:.4f} | {gate} |",
            file=fh,
        )


def print_disagreements(title, disagreements, fh=sys.stdout):
    print(f"\n### {title}\n", file=fh)
    if not disagreements:
        print("None.", file=fh)
        return
    print("| id | feature | coder1 | coder2 |", file=fh)
    print("|---|---|---|---|", file=fh)
    for sid, feat, v1, v2 in disagreements:
        print(f"| {sid} | {feat} | {v1} | {v2} |", file=fh)


def gate_verdict(rows, fh=sys.stdout):
    """Prints the gate verdict for one feature table (`rows` from compute_feature_table) and
    returns (zero_gating_features, identity_or_admissible_fail). `rows` includes identity,
    variant and admissible features; the gate is: every identity feature AND admissible must
    reach A_f >= 0.80 (research/82 §7). A failing variant feature does not fail the gate — it
    is dropped from filling (§8) instead, and reported as such. n=0 on a gating feature
    (identity or admissible) is an ERROR, never a silent PASS."""
    gating_zero = [feat for feat, role, n, po, pe, kappa in rows
                   if role in ("identity", "admit/exclude") and n == 0]
    identity_fail = [feat for feat, role, n, po, pe, kappa in rows
                     if role == "identity" and n > 0 and po < 0.80]
    admissible_fail = [feat for feat, role, n, po, pe, kappa in rows
                        if role == "admit/exclude" and n > 0 and po < 0.80]
    variant_fail = [feat for feat, role, n, po, pe, kappa in rows
                     if role == "variant" and n > 0 and po < 0.80]
    variant_zero = [feat for feat, role, n, po, pe, kappa in rows
                     if role == "variant" and n == 0]

    print("\n### Gate verdict\n", file=fh)
    if gating_zero:
        print(
            f"ERROR — n=0 for gating feature(s) {', '.join(gating_zero)}: no shared coded "
            f"sample was found (both coders' non-unknown values). This means table/feature "
            f"detection failed for this family/invocation — it is NOT a pass. Fix detection "
            f"before trusting any other number in this report.",
            file=fh,
        )
        return gating_zero, True

    if identity_fail or admissible_fail:
        parts = []
        if identity_fail:
            parts.append(f"identity feature(s) {', '.join(identity_fail)}")
        if admissible_fail:
            parts.append(f"admissible")
        print(f"FAIL — {' and '.join(parts)} below A_f >= 0.80 (falsifier gate).", file=fh)
    else:
        print("PASS — every identity feature (and admissible) A_f >= 0.80.", file=fh)

    if variant_fail:
        print(
            f"\nVariant feature(s) below A_f >= 0.80, dropped from filling (family default "
            f"used instead), per §7's last sentence — does not fail the gate: "
            f"{', '.join(variant_fail)}.",
            file=fh,
        )
    if variant_zero:
        print(
            f"\nVariant feature(s) with n=0 shared coded sample (e.g. all sampled items were "
            f"`unknown` for both coders): {', '.join(variant_zero)}. Not gating, not usable "
            f"for filling either — family default used.",
            file=fh,
        )
    return gating_zero, False


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--family", required=True)
    ap.add_argument(
        "--first", nargs="+", required=True,
        help='One or more "LABEL:path" first-coder evidence files.',
    )
    ap.add_argument("--second", required=True, help="Second-coder evidence file.")
    ap.add_argument(
        "--exclude", nargs="*", default=[],
        help="ids to drop for a sensitivity re-run (e.g. disclosed prior-exposure items).",
    )
    ap.add_argument(
        "--override", nargs="*", default=[], metavar="FEATURE=path",
        help='Override the first-coder value of FEATURE, per id, from a recode/verification '
             'file (research/*-recode-82ag.md-style: an "id" column plus a column for FEATURE, '
             'see find_value_column). Repeatable, e.g. --override header=foo.md colour=foo.md. '
             'Only ids already present in a --first file are affected.',
    )
    ap.add_argument(
        "--recode", default=None,
        help="Shorthand for --override header=PATH colour=PATH (a *-recode-82ag.md file "
             "recoding header treatment + colour use under research/82a-general.md). A family "
             "without one of those two features (e.g. form, whose header slot is field_style) "
             "simply gets a no-op for the missing one.",
    )
    ap.add_argument(
        "--override-features", default=None, metavar="F1,F2,...",
        help="Comma-separated feature keys, used together with --override-file: a generic form "
             "for a recode file that already overrides several features at once from one table "
             "(e.g. deck-recode.md: --override-features heading,colour,title_layout,admissible "
             "--override-file research/designs-evidence/deck-recode.md).",
    )
    ap.add_argument(
        "--override-file", default=None,
        help="Path used with --override-features.",
    )
    args = ap.parse_args()

    # Evidence files carry em dashes, curly quotes etc.; force utf-8 stdout so this runs
    # unchanged on a Windows console (cp1252) as well as everywhere else.
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    identity_keys, variant_keys, feature_keys = family_features(args.family)

    first_specs = []
    for spec in args.first:
        if ":" not in spec:
            ap.error(f'--first entries must be "LABEL:path", got: {spec}')
        label, path = spec.split(":", 1)
        first_specs.append((label, path))

    first_by_id, first_by_name, report = build_first_coder_index(first_specs, feature_keys, identity_keys)
    second_records, second_tables_used = load_coded_records(args.second, feature_keys, identity_keys, label=None)

    override_specs = []
    for spec in args.override:
        if "=" not in spec:
            ap.error(f'--override entries must be "FEATURE=path", got: {spec}')
        feat, path = spec.split("=", 1)
        override_specs.append((feat.strip(), path))
    if args.recode:
        override_specs.append(("header", args.recode))
        override_specs.append(("colour", args.recode))
    if args.override_features or args.override_file:
        if not (args.override_features and args.override_file):
            ap.error("--override-features and --override-file must be given together.")
        for feat in args.override_features.split(","):
            override_specs.append((feat.strip(), args.override_file))

    print(f"# Agreement computation — family: {args.family}\n")
    print(f"Identity features (gating): {', '.join(identity_keys)}, admissible.")
    print(f"Variant features (non-gating, dropped from filling on failure): {', '.join(variant_keys)}.\n")
    print("## Inputs\n")
    for label, path, n_records, n_tables in report:
        print(f"- First coder [{label}] `{path}`: {n_records} coded rows found "
              f"({n_tables} coded table(s) detected).")
    print(f"- Second coder `{args.second}`: {len(second_records)} coded rows found "
          f"({second_tables_used} coded table(s) detected).")

    apply_overrides(first_by_id, override_specs, feature_keys)

    sample_ids = list(second_records.keys())
    print(f"\n## Sample\n\n{len(sample_ids)} ids: {', '.join(sample_ids)}\n")

    pairs_by_feature, disagreements, name_fallbacks, unmatched, uncoded_skips = gather_pairs(
        sample_ids, second_records, first_by_id, first_by_name, feature_keys
    )

    if unmatched:
        print("\n## WARNING: unmatched sample ids (no first-coder row by id or name)\n")
        for u in unmatched:
            print(f"- {u}")

    if name_fallbacks:
        print("\n## id-scheme mapping (resolved by repo/package name, not id)\n")
        print("| second-coder id | first-coder id |", file=sys.stdout)
        print("|---|---|", file=sys.stdout)
        for sid, fid in name_fallbacks:
            print(f"| {sid} | {fid} |")
    else:
        print("\n## id-scheme check\n\nAll sampled ids matched a first-coder row directly "
              "by id (no name-based fallback needed).")

    if uncoded_skips:
        print(f"\n## Unknown/uncoded values excluded from n (82a C7) — {len(uncoded_skips)} cell(s)\n")
        print("| id | feature | coder1 | coder2 |", file=sys.stdout)
        print("|---|---|---|---|", file=sys.stdout)
        for sid, feat, v1, v2 in uncoded_skips:
            print(f"| {sid} | {feat} | {v1} | {v2} |")

    rows = compute_feature_table(pairs_by_feature, identity_keys, variant_keys)
    print_feature_table("Per-feature agreement (full sample)", rows)
    print_disagreements("Disagreements (full sample)", disagreements)
    _, fatal = gate_verdict(rows)

    if args.exclude:
        excl = set(args.exclude)
        sub_ids = [i for i in sample_ids if i not in excl]
        dropped = [i for i in sample_ids if i in excl]
        print(f"\n## Sensitivity run — excluding {', '.join(dropped) if dropped else '(none matched)'}\n")
        pbf2, dis2, nf2, um2, unc2 = gather_pairs(sub_ids, second_records, first_by_id, first_by_name, feature_keys)
        rows2 = compute_feature_table(pbf2, identity_keys, variant_keys)
        print_feature_table("Per-feature agreement (sensitivity run)", rows2)
        print_disagreements("Disagreements (sensitivity run)", dis2)
        _, fatal2 = gate_verdict(rows2)
        fatal = fatal or fatal2

    if fatal:
        sys.exit(1)


if __name__ == "__main__":
    main()
