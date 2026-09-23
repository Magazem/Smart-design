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

Each --first entry is "LABEL:path". LABEL is only used to synthesize an id (LABEL:NNN) for
coded tables that key rows by a bare position/rank column instead of an explicit id column
(e.g. "Pos" in an NPM-style table). Tables that already carry an explicit id column (e.g.
"GH:001") are read as-is and LABEL is only used to sanity-check the prefix.

What it does:
  1. Parses every markdown table in each input file (a file may contain many: raw list,
     coded table, exclusions log, frequency table, sources...). Selects the "coded" table(s)
     in each file: those whose header row contains (after normalization) columns/heading/
     colour/header/admissible.
  2. Builds an id -> {feature: value} record for every coded row, id = existing "id" cell if
     present, else f"{LABEL}:{int(pos):03d}".
  3. Also builds a name index (repo/package column, normalized) per id, for cases where the
     id scheme of the first coder(s) and the second coder differ (§7 amendment: the script
     resolves by name and reports the mapping used).
  4. Reads the second coder's own coded table (same parser) — its ids define the sample.
  5. For each sampled id, looks up the matching first-coder row (by id; falls back to name
     match, reporting every fallback used) and compares every shared feature.
  6. Reports, per feature: n, agreements, A_f, Cohen's kappa, and the full disagreement list
     (id, feature, coder1 value, coder2 value).
  7. If --exclude is given, reruns the whole computation with those ids removed from the
     sample (a "sensitivity run"), and reports that table too.

The script only counts and computes; it never judges which coder is "right" (R-d).
"""
import argparse
import math
import re
import sys
from collections import OrderedDict

# Canonical feature keys and the header-cell aliases that map onto them after normalization
# (normalization = lowercase, strip everything but letters/digits).
ALIASES = {
    "id": "id",
    "repo": "name",
    "package": "name",
    "repopackage": "name",
    "item": "name",
    "pos": "pos",
    "rank": "pos",
    "columns": "columns",
    "heading": "heading",
    "body": "body",
    "colour": "colour",
    "color": "colour",
    "header": "header",
    "rulesboxes": "rules_boxes",
    "density": "density",
    "photo": "photo",
    "admissible": "admissible",
}

# The columns that must be present (mapped) for a table to be treated as "the" coded table.
CODED_TABLE_MARKERS = {"columns", "heading", "colour", "header", "admissible"}

# All feature keys we ever compare (order = report order). "id"/"name"/"pos" are structural,
# not features.
FEATURE_KEYS = [
    "columns", "heading", "body", "colour", "header",
    "rules_boxes", "density", "photo", "admissible",
]


def normalize_header(cell):
    return re.sub(r"[^a-z0-9]", "", cell.strip().lower())


def normalize_name(cell):
    # strip markdown emphasis/backticks/links, keep alnum for matching
    cell = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", cell)  # [text](url) -> text
    cell = re.sub(r"[`*_]", "", cell)
    return re.sub(r"[^a-z0-9]", "", cell.strip().lower())


def split_row(line):
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip() for c in line.split("|")]


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
            # first match wins (avoid a later "photo"-like collision overwriting)
            mapping.setdefault(key, idx)
    return mapping


def clean_feature_cell(raw):
    cell = raw.strip()
    cell = re.sub(r"^`|`$", "", cell)
    return cell.strip()


def parse_admissible_cell(raw):
    cell = re.sub(r"[`]", "", raw.strip())
    m = re.match(r"^\**\s*(yes|no)\b", cell, re.I)
    if m:
        return m.group(1).lower()
    return clean_feature_cell(raw)  # fall back to raw text, disagreement will show it


def load_coded_records(path, label=None):
    """
    Parse a file, return dict id -> {feature_key: value, '_name': normalized name,
    '_raw_name': original name text}. Also returns a list of (table_header) diagnostics.
    """
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    tables = find_tables(text)
    records = OrderedDict()
    tables_used = 0
    for header, rows in tables:
        colmap = map_header(header)
        if not CODED_TABLE_MARKERS.issubset(colmap.keys()):
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
            for key in FEATURE_KEYS:
                if key in colmap and colmap[key] < len(row):
                    raw = row[colmap[key]]
                    if key == "admissible":
                        rec[key] = parse_admissible_cell(raw)
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


def build_first_coder_index(first_specs):
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
        records, tables_used = load_coded_records(path, label=label)
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


def compute_feature_table(pairs_by_feature):
    """pairs_by_feature: feature -> list of (id, v1, v2). Returns list of rows."""
    out = []
    for feat in FEATURE_KEYS:
        pairs = pairs_by_feature.get(feat, [])
        po, pe, kappa, n = cohens_kappa([(a, b) for _, a, b in pairs])
        out.append((feat, n, po, pe, kappa))
    return out


def gather_pairs(sample_ids, second_records, first_by_id, first_by_name):
    """
    Returns (pairs_by_feature, disagreements, name_fallbacks, unmatched)
    pairs_by_feature: feature -> list of (id, c1_value, c2_value)  (only where both coders
    recorded a value for that feature)
    disagreements: list of (id, feature, c1_value, c2_value) where they differ
    name_fallbacks: list of (id, resolved_first_coder_id) used when direct id lookup failed
    unmatched: list of ids in the sample with no first-coder match at all (by id or name)
    """
    pairs_by_feature = {k: [] for k in FEATURE_KEYS}
    disagreements = []
    name_fallbacks = []
    unmatched = []
    for sid in sample_ids:
        second_rec = second_records[sid]
        first_rec = first_by_id.get(sid)
        resolved_via = "id"
        if first_rec is None:
            # id schemes differ: fall back to name match
            nm = second_rec.get("_name")
            fid = first_by_name.get(nm) if nm else None
            if fid is not None:
                first_rec = first_by_id[fid]
                name_fallbacks.append((sid, fid))
                resolved_via = "name"
            else:
                unmatched.append(sid)
                continue
        for feat in FEATURE_KEYS:
            v1 = first_rec.get(feat)
            v2 = second_rec.get(feat)
            if v1 is None or v2 is None or v1 == "" or v2 == "":
                continue
            pairs_by_feature[feat].append((sid, v1, v2))
            if v1 != v2:
                disagreements.append((sid, feat, v1, v2))
    return pairs_by_feature, disagreements, name_fallbacks, unmatched


def print_feature_table(title, rows, fh=sys.stdout):
    print(f"\n### {title}\n", file=fh)
    print("| Feature | n | Agreements | A_f | Cohen's kappa | Gate (>=0.80) |", file=fh)
    print("|---|---|---|---|---|---|", file=fh)
    for feat, n, po, pe, kappa in rows:
        if n == 0:
            print(f"| {feat} | 0 | - | n/a (no shared sample) | n/a | n/a |", file=fh)
            continue
        agree = round(po * n)
        gate = "PASS" if po >= 0.80 else "FAIL"
        print(
            f"| {feat} | {n} | {agree} | {po:.4f} | {kappa:.4f} | {gate} |",
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
    args = ap.parse_args()

    first_specs = []
    for spec in args.first:
        if ":" not in spec:
            ap.error(f'--first entries must be "LABEL:path", got: {spec}')
        label, path = spec.split(":", 1)
        first_specs.append((label, path))

    first_by_id, first_by_name, report = build_first_coder_index(first_specs)
    second_records, second_tables_used = load_coded_records(args.second, label=None)

    print(f"# Agreement computation — family: {args.family}\n")
    print("## Inputs\n")
    for label, path, n_records, n_tables in report:
        print(f"- First coder [{label}] `{path}`: {n_records} coded rows found "
              f"({n_tables} coded table(s) detected).")
    print(f"- Second coder `{args.second}`: {len(second_records)} coded rows found "
          f"({second_tables_used} coded table(s) detected).")

    sample_ids = list(second_records.keys())
    print(f"\n## Sample\n\n{len(sample_ids)} ids: {', '.join(sample_ids)}\n")

    pairs_by_feature, disagreements, name_fallbacks, unmatched = gather_pairs(
        sample_ids, second_records, first_by_id, first_by_name
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

    rows = compute_feature_table(pairs_by_feature)
    print_feature_table("Per-feature agreement (full sample)", rows)
    print_disagreements("Disagreements (full sample)", disagreements)

    n_gate_fail = [feat for feat, n, po, pe, kappa in rows if n > 0 and po < 0.80]
    print("\n### Gate verdict (full sample)\n")
    if n_gate_fail:
        print(f"FAIL — feature(s) below A_f >= 0.80: {', '.join(n_gate_fail)}")
    else:
        print("PASS — every feature A_f >= 0.80.")

    if args.exclude:
        excl = set(args.exclude)
        sub_ids = [i for i in sample_ids if i not in excl]
        dropped = [i for i in sample_ids if i in excl]
        print(f"\n## Sensitivity run — excluding {', '.join(dropped) if dropped else '(none matched)'}\n")
        pbf2, dis2, nf2, um2 = gather_pairs(sub_ids, second_records, first_by_id, first_by_name)
        rows2 = compute_feature_table(pbf2)
        print_feature_table("Per-feature agreement (sensitivity run)", rows2)
        print_disagreements("Disagreements (sensitivity run)", dis2)
        n_gate_fail2 = [feat for feat, n, po, pe, kappa in rows2 if n > 0 and po < 0.80]
        print("\n### Gate verdict (sensitivity run)\n")
        if n_gate_fail2:
            print(f"FAIL — feature(s) below A_f >= 0.80: {', '.join(n_gate_fail2)}")
        else:
            print("PASS — every feature A_f >= 0.80.")


if __name__ == "__main__":
    main()
