#!/usr/bin/env python3
"""Load pass 1 — re-header the authored research/ drafts into data/base/*.csv.

Drafts in research/ are provenance and are never modified. Every output file gets
the EXACT manifest header, UTF-8 without BOM, LF newlines.

Surrogate key rules (deterministic, stated so they can be regenerated):
  cv_region_key  = <region-slug>-<band>              e.g. eu-europass-early
  heading_key    = <canonical_section>-<lang>-<n>    n = 1-based within (section, lang)
  substitute_key = <family-slug>-<lineage>           e.g. arial-liberation, candara-none

Two rules that apply to EVERY table block, not just the ones written so far:
  * `data/base/` ships GENERIC rows only. Any draft row whose `Brand Scope` is not
    `generic` is skipped here -- see generic_only(). Brand rows reach the library
    through examples/<brand>.md -> make_brand_kit.py -> data/brand/<brand>/ and by no
    other path (schema Revision 4, S0.3: `Brand Scope` is set by the DIRECTORY).
  * Two tables have no `Brand Scope` column and brand rows anyway -- see BRAND_ROWS.
    The same S0.3 that makes the column unnecessary is why they will never gain one,
    so their brand rows are LISTED by key. assert_no_brand_rows() proves the result.
  * A `Threshold` reference names the MANIFEST table, not this project's `T#` schema
    label -- see norm_threshold(). `T#` is a section number in 09-library-schema.md;
    the data layer has never known it.
"""
import csv, json, re, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
RES = ROOT / "research"
SKILL = ROOT / "skill" / "document-design-intelligence"
BASE = SKILL / "data" / "base"
RATIONALE = SKILL / "data" / "rationale"
MANIFEST = json.loads((SKILL / "data" / "schema-manifest.json").read_text(encoding="utf-8"))

BASE.mkdir(parents=True, exist_ok=True)
CHANGES = []
SKIPPED = []


# `T#` schema-section label -> manifest table name. The schema document numbers its
# sections T1..T14; `validate_data.py` resolves a reference's table half against
# manifest table names and has never known the T-labels. Ruled at schema Revision 4.
T_LABEL = {
    "T1": "doctypes", "T2": "doc-reasoning", "T3": "doc-styles", "T4": "palettes",
    "T5": "typefaces", "T6": "type-scales", "T7": "page-formats",
    "T8": "render-targets", "T9": "constraints", "T10": "structures",
    "T11": "figures", "T12": "cv-regions", "T13": "headings",
    "T14": "font-substitutes",
}
T_REF = re.compile(r"^(T\d+):(.+)$")


# Tables whose draft carries brand rows but whose SCHEMA has no `Brand Scope` column.
# Revision 4 S0.3 sets `Brand Scope` by the DIRECTORY, so T2 and T6 will never gain the
# column -- but their drafts are provenance for the generic table AND the brand overlay,
# exactly as T1's and T3's are. Only the generic half belongs in `data/base/`.
#
# The rows are LISTED, never prefix-matched. A generic key is allowed to begin with a
# brand's letters, and a pattern here would silently eat it -- the same failure mode as
# the `T#:` literals that every count taken by reading this file used to miss.
#   doc-reasoning: the 4 ENS categories that T1's 4 ENS doctypes point at.
#   type-scales:   the 7 `ens-print` rows. Nothing is lost -- make_brand_kit.py re-emits
#                  ENS's type scale from examples/ens-brand.md into data/brand/ens/.
BRAND_ROWS = {
    "doc-reasoning": ("doc_category", {"ens-office-document", "ens-formulaire",
                                       "ens-marketing", "ens-slides"}),
    "type-scales": ("scale_key", {"ens-print"}),
}

# Brand slugs that must appear NOWHERE in data/base/ after a run.
# The historical check -- `grep ",ens," data/base/*.csv` -- matches a field whose WHOLE
# value is `ens`, i.e. a `Brand Scope` cell. It was blind to `doc_category=ens-slides`
# and `scale_key=ens-print`: eleven brand rows could have loaded clean under it.
# assert_no_brand_rows() checks whole `;`-tokens for `<slug>` and `<slug>-` instead.
BRAND_SLUGS = {"ens"}


def norm_threshold(value, where):
    """Rewrite a `T#:<Column>` Threshold reference to `<manifest-table>:<Column>`.

    Applied to every row of every block, so drafts loaded later inherit the rule
    instead of needing a literal edited. Non-references pass through untouched --
    including the literal `16:9`, which T_REF does not match."""
    m = T_REF.match((value or "").strip())
    if not m:
        return value
    label, column = m.group(1), m.group(2)
    if label not in T_LABEL:
        sys.exit("%s: Threshold names unknown schema label %r" % (where, label))
    table = T_LABEL[label]
    cols = MANIFEST["tables"][table]["columns"]
    if column not in cols:
        sys.exit("%s: Threshold reference %r names no column of %s"
                 % (where, value, table))
    return "%s:%s" % (table, column)


def generic_only(rows, table):
    """Drop every draft row that is not generic, by whichever of the two rules applies.

    `data/base/` is the generic library. A draft that carries brand rows is
    provenance for BOTH the generic table and the brand overlay; only the generic
    half belongs here.

    Rule 1, `Brand Scope != generic`: for tables that HAVE the column (T1, T3, T5).
    Rule 2, BRAND_ROWS: for tables that never will (T2, T6) -- the brand rows are
    listed by key there. A table can be subject to both; neither is a fallback for
    the other. A draft matching neither passes through whole."""
    dropped = {}
    if rows and "Brand Scope" in rows[0]:
        kept = []
        for r in rows:
            scope = (r.get("Brand Scope") or "").strip()
            if scope == "generic":
                kept.append(r)
            else:
                dropped[scope or "(blank)"] = dropped.get(scope or "(blank)", 0) + 1
    else:
        kept = list(rows)
    if table in BRAND_ROWS:
        column, brand_keys = BRAND_ROWS[table]
        if kept and column not in kept[0]:
            sys.exit("%s: BRAND_ROWS names column %r, which the draft does not have"
                     % (table, column))
        listed, unseen = [], set(brand_keys)
        for r in kept:
            value = (r.get(column) or "").strip()
            if value in brand_keys:
                unseen.discard(value)
                label = "%s=%s" % (column, value)
                dropped[label] = dropped.get(label, 0) + 1
            else:
                listed.append(r)
        if unseen:
            # A listed key that matches nothing is a stale list, not a clean run: the
            # draft was re-authored and the brand row is now loading under a new name.
            sys.exit("%s: BRAND_ROWS lists %s, which no draft row uses"
                     % (table, ", ".join(sorted(unseen))))
        kept = listed
    if dropped:
        detail = ", ".join("%s x %d" % (k, v) for k, v in sorted(dropped.items()))
        n = sum(dropped.values())
        SKIPPED.append("%s: skipped %d brand-scoped rows: %s" % (table, n, detail))
        print("  %-16s skipped %d brand-scoped rows: %s" % (table, n, detail))
    return kept


def assert_no_brand_rows():
    """Fail the run if any brand-scoped value survived into `data/base/`.

    Enforces the standing rule instead of leaving it to be remembered, and covers the
    seam the old `grep ",ens," data/base/*.csv` check could not see (see BRAND_SLUGS).
    Every cell is split on `;` -- list columns hold their keys that way -- and each
    token is compared whole, so `body-dense` cannot be mistaken for a brand row."""
    hits = []
    for spec in MANIFEST["tables"].values():
        path = BASE / spec["filename"]
        if not path.exists():
            continue
        with path.open(encoding="utf-8", newline="") as f:
            for n, row in enumerate(csv.DictReader(f), start=2):
                for column, value in row.items():
                    for token in (value or "").split(";"):
                        token = token.strip()
                        for brand in BRAND_SLUGS:
                            if token == brand or token.startswith(brand + "-"):
                                hits.append("%s:%d:%s: %r"
                                            % (path.name, n, column, token))
    if hits:
        sys.exit("brand-scoped values reached data/base/:\n  " + "\n  ".join(hits))
    print("Brand check: no %s value in data/base/ (whole token or `<slug>-` prefix)"
          % " / ".join("`%s`" % b for b in sorted(BRAND_SLUGS)))


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def read(name):
    with (RES / name).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write(table, rows):
    cols = MANIFEST["tables"][table]["columns"]
    path = BASE / MANIFEST["tables"][table]["filename"]
    rows = generic_only(rows, table)
    if "Threshold" in cols:
        rows = [dict(r, Threshold=norm_threshold(r.get("Threshold"),
                                                 "%s/%s" % (table, r[cols[0]])))
                for r in rows]
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        for r in rows:
            missing = [c for c in cols if c not in r]
            if missing:
                sys.exit("%s: row missing %s" % (table, missing))
            w.writerow({c: r[c] for c in cols})
    print("  %-16s %3d rows -> %s" % (table, len(rows), path.name))
    return rows  # pre-projection: draft-only columns are still on these dicts


# ---------------------------------------------------------------- T5 typefaces
src = read("19-t5-typefaces-draft.csv")
rows = []
OS_BUNDLED = {"Arial", "Times New Roman", "Georgia", "Verdana", "Trebuchet MS", "Courier New"}
for r in src:
    r = dict(r)
    fb = r["Safe Stack Fallback"].strip()
    r["Safe Stack Availability"] = "os-bundled" if fb in OS_BUNDLED else "office-bundled"
    rows.append(r)
CHANGES.append("T5: +Safe Stack Availability on all 8 rows (os-bundled for the six "
               "OS-bundled families; none of the 8 resolve to an Office-only fallback)")
write("typefaces", rows)

# ------------------------------------------------------------- T7 page-formats
rows = read("21-t7-page-formats-draft.csv")
CHANGES.append("T7: 11 rows loaded verbatim — header already matched the manifest exactly")
write("page-formats", rows)

# --------------------------------------------------------------- T9 constraints
np_rows = read("16-t9-constraints-draft.csv")
pr_rows = read("21-t9-print-constraints-draft.csv")

CV_LENGTH = {"us-cv-length-under10y", "us-cv-length-10y-plus", "uk-cv-length",
             "eu-cv-length", "gulf-cv-length"}
CV_FIELD = {"us-cv-no-photo", "uk-cv-no-photo", "gulf-cv-photo-expected",
            "us-cv-no-dob", "us-cv-no-marital-status"}
DROP = {"print-legibility-l-delta"}

out = []
for r in np_rows + pr_rows:
    k = r["constraint_key"]
    if k in CV_LENGTH or k in CV_FIELD or k in DROP:
        continue
    r = dict(r)
    r["Element Scope"] = ""
    if k == "report-measure-cpl":
        r["Element Scope"] = "body-paragraph"
        r["Parameter"] = "cpl_min=45;cpl_max=75"
    out.append(r)

# the two collapse rows
out.insert(7, {"constraint_key": "cv-page-count", "Set Key": "cv-region",
               "Applies To": "doctype:cv-*", "Check": "validate-page-count",
               "Element Scope": "", "Parameter": "max_pages",
               "Threshold": "T12:Max Pages", "Severity": "warn"})
out.insert(8, {"constraint_key": "cv-field-norms", "Set Key": "cv-region",
               "Applies To": "doctype:cv-*", "Check": "validate-text-safe-fields",
               "Element Scope": "",
               "Parameter": "fields=photo|date_of_birth|marital_status|nationality|visa_status",
               "Threshold": "", "Severity": "warn"})
# the two new bindings
out.append({"constraint_key": "font-substitute-available", "Set Key": "font-safety",
            "Applies To": "format:docx", "Check": "validate-substitute-available",
            "Element Scope": "", "Parameter": "weights_required_from=T5",
            "Threshold": "present", "Severity": "warn"})
out.append({"constraint_key": "redesign-text-frozen", "Set Key": "redesign",
            "Applies To": "doctype:*-redesign", "Check": "validate-content-preservation",
            "Element Scope": "", "Parameter": "normalise=whitespace",
            "Threshold": "0", "Severity": "fail"})

CHANGES.append("T9: 10 CV rows -> 2 (cv-page-count reading cv-regions:Max Pages; cv-field-norms "
               "reading direction from T12). Brief said nine — uk-cv-no-photo is a tenth "
               "row of the same kind and was collapsed too")
CHANGES.append("T9: -print-legibility-l-delta (superseded; research/21 already authored the "
               "two WCAG rows print-contrast-ratio 4.5 body / 3.0 large)")
CHANGES.append("T9: report-measure-cpl Parameter scope=/exempt= -> Element Scope=body-paragraph")
CHANGES.append("T9: +font-substitute-available, +redesign-text-frozen binding rows")
CHANGES.append("T9: Threshold table half T# -> manifest table name on FIVE rows -- "
               "cv-page-count (T12->cv-regions) and pro-bleed-geometry / "
               "pro-trim-safe-margin / pro-min-dpi-raster / pro-min-dpi-line-art "
               "(T7->page-formats). The four T7 rows arrive from "
               "21-t9-print-constraints-draft.csv, which is why every count taken by "
               "reading this loader said 'one row'")
write("constraints", out)

# ------------------------------------------------------------------ T11 figures
LABEL = {  # prose -> enum, one judgment per row, recorded in the report
    "comparison-few-categories": "direct", "comparison-many": "either",
    "part-to-whole": "direct", "change-over-time-few-series": "direct",
    "change-over-time-many": "direct", "distribution": "direct",
    "correlation": "either", "ranking": "direct", "geographic": "either",
    "flow-process": "direct", "tabular-lookup": "direct",
}
rows = []
caption_notes = []
grade_notes = []
GRADE = ("low-medium", "medium", "high")  # longest-first: `low-medium` before `medium`
for r in read("22-t11-figures-draft.csv"):
    r = dict(r)
    r.pop("Min Physical Size mm", None)
    r["Label Strategy"] = LABEL[r["chart_key"]]
    g = r["Greyscale Safe"].strip()
    for v in ("needs-pattern", "yes", "no"):
        if g.lower().startswith(v):
            r["Greyscale Safe"] = v
            break
    # Rev 3: `Caption Required` is the yes/no enum; the prose the draft put in it is a
    # SECOND fact ("what the caption must contain") and now has its own column. Split at
    # the first "--"; anything after a further "--" is the author's file-level aside, not
    # caption copy, so it is dropped from the cell and kept in the provenance file.
    cap = r["Caption Required"].strip()
    head, sep, tail = cap.partition("--")
    norm = head.strip().lower()
    norm = "yes" if norm.startswith("yes") else ("no" if norm.startswith("no") else cap)
    must_state = tail.split("--")[0].strip() if sep else ""
    if must_state:
        caption_notes.append((r["chart_key"], cap, must_state))
    r["Caption Required"] = norm
    r["Caption Must State"] = must_state
    # Revision 4 erratum follow-on: `Accessibility Grade` is an enum (`high`|`medium`|
    # `low-medium`), clean on ten of the eleven authored rows. `tabular-lookup` wrote a
    # 96-char sentence into it -- the SAME authorial move as the prose in
    # `Caption Required`, one column over -- so it gets the same handling: the enum token
    # stays in the enum column, and the displaced sentence moves to the prose column
    # beside it, `Accessibility Notes`. Ruled that way rather than typing the column
    # `text`, which would cost the enum check on all eleven rows to license one cell.
    grade = r["Accessibility Grade"].strip()
    head, sep, tail = grade.partition("--")
    norm_grade = head.strip().lower()
    for v in GRADE:
        if norm_grade.startswith(v):
            norm_grade = v
            break
    else:
        norm_grade = grade  # unrecognised: leave it as authored and let the gate say so
    displaced = tail.strip() if sep else ""
    if displaced:
        grade_notes.append((r["chart_key"], grade, norm_grade, displaced))
        notes = r["Accessibility Notes"].strip()
        r["Accessibility Notes"] = ("%s; grade rationale: %s" % (notes, displaced)
                                    if notes else displaced)
    r["Accessibility Grade"] = norm_grade
    rows.append(r)
CHANGES.append("T11: -Min Physical Size mm (per ruling). Label Strategy prose -> enum on 11 "
               "rows. +Caption Must State (Rev 3): Caption Required prose split into the "
               "yes/no enum plus the qualification on %d rows -- restored into the table, "
               "no longer provenance-only" % len(caption_notes))
CHANGES.append("T11: Accessibility Grade prose -> enum on %d row(s) (Revision 4 erratum "
               "follow-on). The displaced sentence is appended to Accessibility Notes, "
               "not dropped -- the same split as Caption Required/Caption Must State"
               % len(grade_notes))
write("figures", rows)
(RES / "26-t11-caption-qualifications.md").write_text(
    "# T11 `Caption Required` qualifications -- RESTORED at Revision 3\n\n"
    "`Caption Required` is a yes/no enum; research/22 authored prose in it, because it was\n"
    "answering a second question the column did not ask. Revision 3 added\n"
    "`Caption Must State`, and this loader now splits the prose across both columns, so\n"
    "these three facts are **in the library**, not only here. This file stays as\n"
    "provenance: it records the authored cell verbatim beside what the split produced.\n\n"
    "| `chart_key` | authored `Caption Required` | loaded `Caption Must State` |\n"
    "|---|---|---|\n"
    + "".join("| `%s` | %s | %s |\n" % (k, v.replace("|", "\\|"), m.replace("|", "\\|"))
              for k, v, m in caption_notes)
    + "\n`tabular-lookup`'s value is a *position*, not a statement. T10's `Caption Position`\n"
      "stays authoritative for that (schema T11 design note, Revision 3); the cell records\n"
      "the fact where the row that carries it can be read, and does not drive the check.\n"
      "\n## `Accessibility Grade` -- the same split, one column over\n\n"
      "`Accessibility Grade` became an enum at the Revision 4 erratum follow-on. The T11\n"
      "author wrote prose into it on the same row and for the same reason, so the loader\n"
      "applies the same rule: the enum token stays, the sentence moves to the prose column\n"
      "beside it (`Accessibility Notes`), joined with `; ` -- the sentence separator those\n"
      "columns already use. Nothing is lost, and the draft is not hand-edited.\n\n"
      "| `chart_key` | authored `Accessibility Grade` | loaded | moved to `Accessibility Notes` |\n"
      "|---|---|---|---|\n"
    + "".join("| `%s` | %s | `%s` | %s |\n"
              % (k, v.replace("|", "\\|"), g, m.replace("|", "\\|"))
              for k, v, g, m in grade_notes),
    encoding="utf-8")

# --------------------------------------------------------------- T12 cv-regions
src = read("18-cv-region-rules.csv")
cv_sources = []   # (cv_region_key, region, band, authored band, source) for rationale/
by_region = {}
for r in src:
    by_region.setdefault(r["region"], {})[r["seniority_band"]] = r
rows = []
for region, bands in by_region.items():
    for band, srcband in (("early", "early"), ("experienced", None)):
        if band == "early":
            r = bands["early"]
        else:  # widest ceiling among mid/senior/executive; they are otherwise identical
            cands = [bands[b] for b in ("mid", "senior", "executive") if b in bands]
            r = max(cands, key=lambda x: int(x["max_pages"]))
        rows.append({
            "cv_region_key": "%s-%s" % (slug(region), band),
            "region_key": slug(region), "Seniority Band": band,
            "Max Pages": r["max_pages"], "Photo": r["photo"],
            "Date of Birth": r["date_of_birth"], "Nationality": r["nationality"],
            "Marital Status": r["marital_status"], "Visa Status": r["visa_status"],
            "Section Order": r["section_order"].replace("|", ";"),
            "Education Before Experience": {"true": "yes", "false": "no"}[
                r["education_before_experience"].strip().lower()],
            "Format": r["format"], "Language Expectation": r["language_expectation"],
            # research/18 rows "EU-Europass mid" and "Gulf-GCC early" have unescaped commas
            # in `source`, so csv overflows into None. Evidence class is the last field.
            "Evidence Class": (r[None][-1] if r.get(None) else r["evidence_class"]).strip().upper(),
        })
        # `source` is a draft-only column -- the citation behind the row. Rule 2 puts it in
        # rationale/, and this loader has promised that file in its own CHANGES string
        # since load pass 1 without ever writing it. Written now.
        cv_sources.append(("%s-%s" % (slug(region), band), region, band,
                           r["seniority_band"], (r.get("source") or "").strip()))
CHANGES.append("T12: 28 -> 14 rows (bands collapsed to early/experienced; experienced takes "
               "the widest ceiling among mid/senior/executive). 13 columns renamed, "
               "`source` dropped to rationale/, section_order separator | -> ;")
write("cv-regions", rows)
RATIONALE.mkdir(parents=True, exist_ok=True)
(RATIONALE / "cv-regions.md").write_text(
    "# rationale/cv-regions.md\n\n"
    "Written by `research/load-base.py`. **Do not hand-edit** -- the source is the\n"
    "`source` column of `research/18-cv-region-rules.csv`.\n\n"
    "Rule 2 (`09-library-schema.md:70`): rationale and provenance live in a sibling\n"
    "`rationale/<table>.md`, not in a column. T12's draft carries a `source` citation the\n"
    "table does not have, and the 28 authored (region, seniority band) rows collapse to 14\n"
    "(`early`, plus `experienced` = the widest page ceiling among mid/senior/executive), so\n"
    "each entry below also records WHICH authored band the loaded row was taken from --\n"
    "without it the citation cannot be traced back to the row it was written for.\n\n"
    "One entry per row of `data/base/cv-regions.csv`, in file order.\n\n"
    "| `cv_region_key` | region | loaded band | authored band used | source |\n"
    "|---|---|---|---|---|\n"
    + "".join("| `%s` | %s | %s | %s | %s |\n"
              % (k, region, band, srcband, (src or "(none given)").replace("|", "&#124;"))
              for k, region, band, srcband, src in cv_sources),
    encoding="utf-8")
CHANGES.append("T12: rationale/cv-regions.md written (%d entries) -- the draft-only "
               "`source` column, promised by this loader's own CHANGES string since load "
               "pass 1 and never written until now" % len(cv_sources))

# ----------------------------------------------------------------- T13 headings
rows, n = [], {}
head_sources = []
HEADING_FILES = ["18-ats-headings.csv", "39-headings-transactional-draft.csv",
                 "40-headings-longform-draft.csv", "41-headings-marketing-draft.csv"]
# `n` is deliberately shared across all four files: it numbers the `<section>-<lang>-<n>`
# surrogate globally, so a section that appears in two inputs keeps counting up rather
# than restarting and colliding.
for r in [row for name in HEADING_FILES for row in read(name)]:
    key = (r["canonical_section"], r["language"])
    n[key] = n.get(key, 0) + 1
    head_sources.append(("%s-%s-%d" % (r["canonical_section"], r["language"], n[key]),
                         (r.get("source") or "").strip()))
    rows.append({"heading_key": "%s-%s-%d" % (r["canonical_section"], r["language"], n[key]),
                 "canonical_section": r["canonical_section"],
                 "Heading Text": r["heading_text"], "Language": r["language"],
                 "Is Primary": r["is_primary"]})
if len({r["heading_key"] for r in rows}) != len(rows):
    sys.exit("T13: duplicate heading_key across the %d heading inputs"
             % len(HEADING_FILES))
CHANGES.append("T13: %d rows over %d heading inputs, +heading_key surrogate, "
               "3 columns renamed, `source` dropped"
               % (len(rows), len(HEADING_FILES)))
write("headings", rows)
RATIONALE.mkdir(parents=True, exist_ok=True)
by_src = {}
for hk, hs in head_sources:
    by_src.setdefault(hs or "(none given)", []).append(hk)
(RATIONALE / "headings.md").write_text(
    "# rationale/headings.md\n\n"
    "Written by `research/load-base.py`. **Do not hand-edit** -- the source is the\n"
    "`source` column of `research/18-ats-headings.csv`.\n\n"
    "Rule 2 (`09-library-schema.md:70`): rationale and provenance live in a sibling\n"
    "`rationale/<table>.md`, not in a column.\n\n"
    "T13 is the table where that citation carries the most weight and repeats the most:\n"
    "the distinction governing every row is whether a heading string comes from **report\n"
    "03** or is an unsourced **convention**, and %d of the %d rows carry the identical\n"
    "`convention (not in report 03)` string. Grouped by citation rather than listed per\n"
    "row, so the shape of the evidence is visible instead of buried in the repetition.\n\n"
    % (len(by_src.get("convention (not in report 03)", [])), len(head_sources))
    + "".join("### %s\n\n%d heading(s): %s\n\n"
              % (src, len(keys), ", ".join("`%s`" % k for k in keys))
              for src, keys in sorted(by_src.items(), key=lambda kv: (-len(kv[1]), kv[0]))),
    encoding="utf-8")
CHANGES.append("T13: rationale/headings.md written (%d rows over %d distinct citations) -- "
               "the draft-only `source` column, promised by this loader's own CHANGES "
               "string since load pass 1 and never written until now"
               % (len(head_sources), len(by_src)))

# -------------------------------------------------------- T14 font-substitutes
WEIGHTS = {"Carlito": "Regular;Bold;Italic;Bold Italic",
           "Caladea": "Regular;Bold;Italic;Bold Italic",
           "Gelasio": "Regular;Bold;Italic;Bold Italic"}
DEFAULT_W = "Regular;Bold;Italic;Bold Italic"
rows = []
for r in read("27-t14-font-substitutes-draft.csv"):
    lin = "independent" if r["Lineage"] == "other" else r["Lineage"]
    sub = r["Substitute Family"].strip()
    rows.append({"substitute_key": "%s-%s" % (slug(r["proprietary_family"]), lin),
                 "proprietary_family": r["proprietary_family"], "Substitute Family": sub,
                 "Lineage": lin, "Licence": r["Licence"],
                 "Metric Identical": r["Metric Identical"].strip(),
                 "Weights Covered": WEIGHTS.get(sub, DEFAULT_W if sub else "")})
CHANGES.append("T14: 15 rows, +substitute_key, +Weights Covered, Lineage other->independent "
               "(Gelasio). Metric Identical left blank on the 6 no-substitute rows")
write("font-substitutes", rows)

# ------------------------------------------------------------ T8 render-targets
CHROME = "--headless --no-sandbox --disable-gpu --print-to-pdf=%o --no-pdf-header-footer %i"
t8 = [
    ("pdf-chromium", "pdf", "headless-chromium", "/opt/google/chrome/chrome", "", CHROME,
     "embed", "yes", "no", "no", "submittable-rgb", "no", "preinstalled", "pdf-weasyprint"),
    ("pdf-weasyprint", "pdf", "weasyprint", "weasyprint (module)", "0.41", "",
     "embed", "yes", "yes", "no", "submittable-rgb", "no", "pip", "pdf-wkhtmltopdf"),
    ("pdf-weasyprint-pdfx4", "pdf", "weasyprint", "weasyprint (module)", "67.0",
     "--pdf-variant=pdf/x-4 --output-intent=srgb",
     "embed", "yes", "yes", "yes", "pdfx4-rgb", "no", "pip", "pdf-weasyprint"),
    ("pdf-wkhtmltopdf", "pdf", "wkhtmltopdf", "wkhtmltopdf", "", "",
     "embed", "yes", "no", "no", "submittable-rgb", "no", "unverified", ""),
    ("docx-office", "docx", "python-docx", "docx (module)", "", "",
     "safe-stack", "n/a", "n/a", "n/a", "none", "yes", "preinstalled", ""),
    ("pptx-office", "pptx", "python-pptx", "pptx (module)", "", "",
     "embed", "n/a", "n/a", "n/a", "none", "yes", "preinstalled", ""),
    ("png-social", "png", "headless-chromium", "/opt/google/chrome/chrome", "",
     "--headless --no-sandbox --disable-gpu --screenshot=%o --window-size=1080,1350 %i",
     "embed", "n/a", "n/a", "n/a", "none", "no", "preinstalled", ""),
    ("html-static", "html", "stdlib-template", "python (stdlib)", "", "",
     "inline-webfont", "yes", "n/a", "n/a", "none", "yes", "preinstalled", ""),
]
cols = MANIFEST["tables"]["render-targets"]["columns"]
CHANGES.append("T8: 8 rows authored directly from the schema's own T8 section "
               "(Chromium preinstalled and WeasyPrint pip both confirmed by live test)")
write("render-targets", [dict(zip(cols, r)) for r in t8])

# ============================================================ LOAD PASS 2 ====
# T1/T2/T3/T6. All four drafts were authored against the manifest header directly, so
# there is no re-header step here -- the work is the brand split (T2, T6) and Rule 2's
# rationale strip (T2).

# ------------------------------------------------------------------ T1 doctypes
src = read("26-t1-doctypes-draft.csv")
rows = write("doctypes", src)
CHANGES.append("T1: %d draft rows -> %d generic (the 4 ENS doctypes are `Brand Scope` "
               "ens and reach the library through data/brand/ens/). Header already "
               "matched the manifest exactly" % (len(src), len(rows)))

# ------------------------------------------------------------- T2 doc-reasoning
# `Reasoning` and `Confidence` are DRAFT-ONLY columns -- the author's argument for the
# row, and their own 0-1 rating of it. Rule 2 (09-library-schema.md:70) keeps provenance
# out of the table and in a sibling `rationale/<table>.md`. write() projects to the
# manifest's 10 columns, so the strip is automatic; this block only has to not lose the
# prose on the way past.
src = read("29-t2-doc-reasoning-draft.csv")
rows = write("doc-reasoning", src)
ens_t2 = sorted(BRAND_ROWS["doc-reasoning"][1])
RATIONALE.mkdir(parents=True, exist_ok=True)
(RATIONALE / "doc-reasoning.md").write_text(
    "# rationale/doc-reasoning.md\n\n"
    "Written by `research/load-base.py`. **Do not hand-edit** -- the source is the\n"
    "`Reasoning` and `Confidence` columns of `research/29-t2-doc-reasoning-draft.csv`.\n\n"
    "Rule 2 (`09-library-schema.md:70`): rationale and provenance live in a sibling\n"
    "`rationale/<table>.md`, not in a column, so that every row stays a one-line diff.\n"
    "T2's draft authors two columns the table does not have; the loader strips them here.\n"
    "`Confidence` is the author's own rating, not a measurement.\n\n"
    "One entry per row of `data/base/doc-reasoning.csv`, in file order.\n\n"
    + "".join("### `%s` -- confidence %s\n\n%s\n\n"
              % (r["doc_category"], (r.get("Confidence") or "(none)").strip(),
                 (r.get("Reasoning") or "(none given)").strip())
              for r in rows)
    + "---\n\n"
      "The draft also carries %d ENS rows (%s). They are not in `data/base/`\n"
      "(`BRAND_ROWS`), and `make_brand_kit.py` does not emit a `doc-reasoning.csv`, so\n"
      "their reasoning reaches no shipped file today and lives in\n"
      "`research/29-t2-doc-reasoning-draft.csv` alone. Recorded here so the gap is\n"
      "visible from the table it belongs to.\n"
      % (len(ens_t2), ", ".join("`%s`" % k for k in ens_t2)),
    encoding="utf-8")
CHANGES.append("T2: %d draft rows -> %d generic (4 ENS categories listed in BRAND_ROWS; "
               "T2 has no `Brand Scope` column and never will). Draft-only `Reasoning`/"
               "`Confidence` stripped to data/rationale/doc-reasoning.md per Rule 2"
               % (len(src), len(rows)))

# ---------------------------------------------------------------- T3 doc-styles
src = read("31-t3-doc-styles-draft.csv")
rows = write("doc-styles", src)
CHANGES.append("T3: %d draft rows -> %d generic (2 ENS styles are `Brand Scope` ens). "
               "`Checklist` loaded as authored -- it is a DECLARED list column, short "
               "imperative items separated by `;`, and the draft honours that"
               % (len(src), len(rows)))

# --------------------------------------------------------------- T6 type-scales
src = read("30-t6-type-scales-draft.csv")
rows = write("type-scales", src)
CHANGES.append("T6: %d draft rows -> %d generic (the 7 `ens-print` rows are listed in "
               "BRAND_ROWS; make_brand_kit.py re-emits ENS's scale from "
               "examples/ens-brand.md). This is what resolves T5's 7 dangling "
               "`Scale Key` values" % (len(src), len(rows)))

# ============================================================ LOAD PASS 3 ====
# T4 palettes. The draft was authored against the manifest header directly and carries a
# `Brand Scope` column, so generic_only()'s Rule 1 handles the ENS row and there is no
# re-header step. This is the table 14 `doc-reasoning.Palette Key` lines were dangling on.

# ------------------------------------------------------------------ T4 palettes
src = read("32-t4-palettes-draft.csv")
rows = write("palettes", src)
CHANGES.append("T4: %d draft rows -> %d generic (`ens-core` is `Brand Scope` ens and "
               "reaches the library through data/brand/ens/). Header already matched the "
               "manifest exactly; the 5 On-X contrast pairs per row are checked by the "
               "gate's `derived` contrast_at_least rules, not by this loader"
               % (len(src), len(rows)))

# ============================================================ LOAD PASS 4 ====
# T10 structures. The draft header equals the manifest `structures.columns` list
# exactly, and every row is generic -- T10 has no `Brand Scope` column and the 4
# ENS-scoped structure keys T1 references were left out of the draft on purpose, so
# generic_only() passes the rows through whole (neither Rule 1 nor Rule 2 applies).
# This is the table 29 `doctypes.Structure Key` lines were dangling on.
#
# `Section Order` is EMPTY on 15 of 17 rows BY RULING, not by omission: it is a
# group-FK list into `headings.canonical_section`, and headings.csv holds only the 11
# CV sections. Authoring the rest is step 9, after v0.1.0 -- research/36-notes.md
# lists exactly which tokens each document family still needs. Do not read those
# blanks as a load defect and do not fill them here.

# ----------------------------------------------------------------- T10 structures
src = read("36-t10-structures-draft.csv")
rows = write("structures", src)
CHANGES.append("T10: %d draft rows -> %d generic (no ENS rows in the draft; the 4 "
               "ENS-scoped structure keys T1 references are out of scope until the "
               "brand overlay authors them). `Section Order` is blank on %d of %d "
               "rows by ruling -- headings.csv covers CV sections only, see "
               "research/36-notes.md" % (len(src), len(rows),
                                         sum(1 for r in rows if not r["Section Order"]),
                                         len(rows)))

assert_no_brand_rows()

print("\nChanges applied:")
for c in CHANGES:
    print("  - " + c)
print("")
if SKIPPED:
    print("Brand-scoped rows skipped (data/base is the generic library):")
    for c in SKIPPED:
        print("  - " + c)
else:
    print("Brand-scoped rows skipped: none")
