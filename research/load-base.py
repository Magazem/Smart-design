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


# research/80-v05-plan.md §2E: the loader gains glob inputs so workers can ADD rows to
# the five library tables (palettes, typefaces, type-scales, doc-styles, doc-reasoning)
# without hand-editing the numbered drafts above. Other agents are authoring under
# research/library/<table>/*.csv concurrently and their files may still be incomplete,
# so a glob file only loads when its filename is LISTED in LIBRARY_INPUTS_ENABLED --
# left EMPTY on purpose. The orchestrator enables a batch by adding its filename once
# reviewed; an unlisted file sits in research/library/ and is silently skipped (that
# silence is the point of a review gate, not a bug).
LIBRARY_INPUTS_ENABLED = ["ranked-pairings.csv", "authority-design-systems.csv", "ratio-families.csv", "ranked-colourlovers.csv"]


def load_library_extra(table):
    """research/library/<table>/*.csv rows whose filename is in LIBRARY_INPUTS_ENABLED,
    read in sorted-filename order (deterministic append order) and appended AFTER the
    numbered draft for that table -- write()'s duplicate-key check is what actually
    makes a colliding key fail loudly rather than one silently shadowing the other."""
    folder = RES / "library" / table
    if not folder.is_dir():
        return []
    extra = []
    for path in sorted(folder.glob("*.csv")):
        if path.name not in LIBRARY_INPUTS_ENABLED:
            continue
        with path.open(encoding="utf-8-sig", newline="") as f:
            extra.extend(csv.DictReader(f))
    return extra


def write(table, rows):
    cols = MANIFEST["tables"][table]["columns"]
    key_col = MANIFEST["tables"][table]["key_column"]
    path = BASE / MANIFEST["tables"][table]["filename"]
    rows = generic_only(rows, table)
    if "Threshold" in cols:
        rows = [dict(r, Threshold=norm_threshold(r.get("Threshold"),
                                                 "%s/%s" % (table, r[cols[0]])))
                for r in rows]
    # research/80-v05-plan.md §2E: numbered drafts are read first and glob inputs are
    # appended after them (both T2/T3/T4/T6/T5's own library folders and the new
    # designs/provenance tables), so a key authored twice -- draft vs glob, or glob vs
    # glob -- must fail loudly here rather than one silently shadowing the other.
    seen = {}
    for r in rows:
        seen.setdefault(r.get(key_col), 0)
        seen[r.get(key_col)] += 1
    dups = sorted(k for k, n in seen.items() if n > 1)
    if dups:
        sys.exit("%s: duplicate %s value(s): %s" % (table, key_col, ", ".join(dups)))
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
src = read("19-t5-typefaces-draft.csv") + load_library_extra("typefaces")
rows = []
OS_BUNDLED = {"Arial", "Times New Roman", "Georgia", "Verdana", "Trebuchet MS", "Courier New"}
for r in src:
    r = dict(r)
    fb = r["Safe Stack Fallback"].strip()
    r["Safe Stack Availability"] = "os-bundled" if fb in OS_BUNDLED else "office-bundled"
    rows.append(r)
CHANGES.append("T5: +Safe Stack Availability on all %d rows (os-bundled for every row here "
               "since all fall back to an OS-bundled family; none resolve to an "
               "Office-only fallback)" % len(rows))
CHANGES.append("T5: +safe-sans-deck (Arial, Scale Key deck-projection) -- v0.3 D3 "
               "(research/51-invoked-quality.md): deck-generic pointed at safe-sans-arial, "
               "whose Scale Key is cv-print, so a projected deck resolved the CV's 11pt print "
               "scale instead of the deck-projection scale research/30 already authored. "
               "safe-sans-deck is the T5 row research/30-notes.md said was still PROPOSED; "
               "safe-sans-arial itself is unchanged, so cv-* doctypes are unaffected.")
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

# `Element Scope` is in the manifest but in neither draft -- it is derived here. A key
# absent from this map loads EMPTY, which the schema defines as a real value ("whole
# document; no container-type routing"), not a missing one. Two of the page-flow rows
# are deliberately absent: `report-heading-keep-with-next` and
# `report-figure-caption-keep-together` carry their block type in `Parameter`
# (`applies_to_block=`/`binds_to=`), the same way photocopy-safe-color keeps `roles=`
# there -- `Element Scope` has no `heading` or `figure` value and must not grow one.
# Reasoning in research/45-notes.md. Do not "fix" them into this map.
ELEMENT_SCOPE = {
    "report-measure-cpl": "body-paragraph",
    "report-widow-orphan-control": "body-paragraph",
    "report-table-row-no-split": "table-cell",
    "report-table-header-repeat": "table-cell",
}

out = []
for r in np_rows + pr_rows:
    k = r["constraint_key"]
    if k in CV_LENGTH or k in CV_FIELD or k in DROP:
        continue
    r = dict(r)
    r["Element Scope"] = ELEMENT_SCOPE.get(k, "")
    if k == "report-measure-cpl":
        # the scope came OUT of Parameter; leave only the two CPL numbers behind
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
CHANGES.append("T9: Element Scope derivation is now a key->scope map, not one hardcoded key. "
               "+5 page-flow rows: report-widow-orphan-control=body-paragraph, "
               "report-table-row-no-split / report-table-header-repeat=table-cell. "
               "report-heading-keep-with-next and report-figure-caption-keep-together "
               "stay EMPTY by design -- their block type lives in Parameter "
               "(applies_to_block=/binds_to=) because the enum has no heading/figure "
               "value. That is not a gap; see research/45-notes.md")
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
for name in HEADING_FILES:
    for r in read(name):
        key = (r["canonical_section"], r["language"])
        n[key] = n.get(key, 0) + 1
        hk = "%s-%s-%d" % (r["canonical_section"], r["language"], n[key])
        # The input filename rides along in the third slot so the rationale prose below
        # can split the CV rows from the phase A ones without re-reading the four files.
        head_sources.append((hk, (r.get("source") or "").strip(), name))
        rows.append({"heading_key": hk,
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
for hk, hs, _src_file in head_sources:
    by_src.setdefault(hs or "(none given)", []).append(hk)

# Every number in the prose below is counted here rather than typed, so the next input
# file added to HEADING_FILES cannot leave the paragraph describing an older shape.
# HEADING_FILES[0] is the CV input; the other three are the phase A drafts.
CV_INPUT = HEADING_FILES[0]
cv_cites = [hs for _hk, hs, fn in head_sources if fn == CV_INPUT]
cv_sourced = [c for c in cv_cites if c.lower().startswith("report 03")]
cv_identical = [c for c in cv_cites if c == "convention (not in report 03)"]
rest_cites = [hs for _hk, hs, fn in head_sources if fn != CV_INPUT]


def primary(section, lang):
    """The `is_primary` heading text for one (section, language), read back out of the
    rows just built -- so the reuse rule's worked examples quote the shipped data and
    cannot drift from it."""
    for r in rows:
        if (r["canonical_section"] == section and r["Language"] == lang
                and r["Is Primary"] == "yes"):
            return r["Heading Text"]
    return "(absent)"


(RATIONALE / "headings.md").write_text(
    "# rationale/headings.md\n\n"
    "Written by `research/load-base.py`. **Do not hand-edit** -- the source is the\n"
    "`source` column of the %d heading inputs (%s).\n\n"
    % (len(HEADING_FILES), ", ".join("`research/%s`" % f for f in HEADING_FILES))
    + "Rule 2 (`09-library-schema.md:70`): rationale and provenance live in a sibling\n"
    "`rationale/<table>.md`, not in a column.\n\n"
    "T13 is the table where that citation carries the most weight and repeats the most:\n"
    "%d rows over %d distinct citations. No single distinction runs through all of them,\n"
    "because the rows arrive from four inputs authored against different evidence.\n\n"
    "The %d CV rows (`%s`) are the ones that measure themselves against **report 03**:\n"
    "%d name it as their source and %d are convention, of which %d carry the identical\n"
    "`convention (not in report 03)` string.\n\n"
    "The remaining %d transactional, long-form and marketing rows are cited against\n"
    "different evidence, over %d distinct strings. **Not one of them names report 03 as\n"
    "a source.** %d mention it at all, and only to disclaim it (`not in report 03`) --\n"
    "report 03 is a CV document, and these classes are outside it. %d carry a `sourced`\n"
    "citation to a standard or convention of their own, and %d name the phase A notes\n"
    "file beside their draft. Grouped by citation rather than listed per row, so the\n"
    "shape of the evidence is visible instead of buried in the repetition.\n\n"
    % (len(head_sources), len(by_src), len(cv_cites), CV_INPUT, len(cv_sourced),
       len(cv_cites) - len(cv_sourced), len(cv_identical), len(rest_cites),
       len(set(rest_cites)),
       len([c for c in rest_cites if "report 03" in c.lower()]),
       len([c for c in rest_cites if c.lower().startswith("sourced")]),
       len([c for c in rest_cites if "-notes.md" in c]))
    + "## The reuse rule for `canonical_section`\n\n"
    "Never reuse a `canonical_section` across document classes when its **FR or DE**\n"
    "primary heading text reads as a word belonging to the other class. Check the actual\n"
    "heading text in all three languages before reusing a section, not just the English\n"
    "canonical name -- an English name that fits is exactly what makes a wrong reuse look\n"
    "right.\n\n"
    "Three worked examples, quoting the shipped rows:\n\n"
    "- `summary` was refused for a proposal's executive summary. Its EN primary is\n"
    "  \"%s\", which fits, but its FR primary is \"%s\" and its DE primary \"%s\" -- a CV\n"
    "  word in both. `executive-summary` was authored instead (FR \"%s\", DE \"%s\").\n"
    "- `references` was refused for a report's bibliography. Its DE primary \"%s\"\n"
    "  reads as testimonials, not as a list of works cited. `bibliography` was authored\n"
    "  instead (DE \"%s\").\n"
    "- `proposed-solution` was refused for a whitepaper: its DE primary \"%s\" carries a\n"
    "  commercial-bid flavour a whitepaper's solution section does not have, so\n"
    "  `solution-approach` (DE \"%s\") was authored for it. That same `proposed-solution`\n"
    "  was then REUSED for a pitch deck, where the bid flavour is correct. The rule cuts\n"
    "  both ways -- it forbids the wrong reuse, not reuse.\n\n"
    % (primary("summary", "en"), primary("summary", "fr"), primary("summary", "de"),
       primary("executive-summary", "fr"), primary("executive-summary", "de"),
       primary("references", "de"), primary("bibliography", "de"),
       primary("proposed-solution", "de"), primary("solution-approach", "de"))
    + "## Citations\n\n"
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

# research/64 D-E / RESUME backlog item 4: `structures.'Heading Language'` is a
# per-structure constant of `en`, so a doctype normally authored in French or German
# still handed over English section headings -- `Default Language` fixes the DOCTYPE
# instead, since several doctypes share one Structure Key. CONVENTION, no external
# authority: a doctype defaults to fr/de only when its own Display Name is authored
# in that language, not because its multilingual Keywords cell contains a foreign
# search term (nearly every CV doctype's Keywords carries all three languages'
# request phrasing, so that could never discriminate).
NON_EN_WHY = {
    "cv-dach": "Display Name \"CV -- DACH (Lebenslauf)\" -- Lebenslauf is German",
    "cv-france": "Display Name \"CV -- France\" authored for the French market; "
                 "cv-france is the only CV doctype whose Display Name and Reasoning "
                 "Key both name a single French-speaking market",
    "ens-note-interne": "Display Name \"ENS -- Note interne\" is French; Brand Scope "
                        "ens (Luxembourg ASBL, operates in French)",
    "ens-formulaire": "Display Name \"ENS -- Formulaire\" is French; Brand Scope ens",
    "ens-social": "Display Name \"ENS -- Post reseaux sociaux\" is French; Brand Scope ens",
    "ens-slides": "Display Name \"ENS -- Presentation\" is French; Brand Scope ens",
}
RATIONALE.mkdir(parents=True, exist_ok=True)
(RATIONALE / "doctypes.md").write_text(
    "# rationale/doctypes.md\n\n"
    "Written by `research/load-base.py`. **Do not hand-edit** -- the source is the\n"
    "`Default Language` column of `research/26-t1-doctypes-draft.csv`.\n\n"
    "Rule 2 (`09-library-schema.md:70`): rationale and provenance live in a sibling\n"
    "`rationale/<table>.md`, not in a column.\n\n"
    "## `Default Language` -- CONVENTION, no external authority (research/64 D-E)\n\n"
    "Criterion: `fr`/`de` only when the doctype's OWN `Display Name` is authored in\n"
    "that language. `quote-devis` and `invoice-tabular` stay `en` even though their\n"
    "Keywords carry `devis`/`facture` -- those are alternate-language search tokens,\n"
    "not a claim the rendered document is authored in French, and neither exists as a\n"
    "separate French-only doctype row.\n\n"
    "| `doc_key` | Default Language | why |\n"
    "|---|---|---|\n"
    + "".join("| `%s` | %s | %s |\n" % (r["doc_key"], r["Default Language"],
                                        NON_EN_WHY.get(r["doc_key"], "no market/language "
                                                       "signal in its own Display Name"))
              for r in rows if r["Default Language"] != "en")
    + "\nAll other %d doctypes default to `en` (no market/language signal of their own\n"
      "Display Name)." % len([r for r in rows if r["Default Language"] == "en"]),
    encoding="utf-8")
CHANGES.append("T1: +Default Language (research/64 D-E) -- cv-dach=de, cv-france=fr, "
               "the 4 ens-* doctypes=fr (French Display Names, Brand Scope=ens), the "
               "other 28 doctypes=en. rationale/doctypes.md written")

# ------------------------------------------------------------- T2 doc-reasoning
# `Reasoning` and `Confidence` are DRAFT-ONLY columns -- the author's argument for the
# row, and their own 0-1 rating of it. Rule 2 (09-library-schema.md:70) keeps provenance
# out of the table and in a sibling `rationale/<table>.md`. write() projects to the
# manifest's 10 columns, so the strip is automatic; this block only has to not lose the
# prose on the way past.
src = read("29-t2-doc-reasoning-draft.csv") + load_library_extra("doc-reasoning")
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
src = read("31-t3-doc-styles-draft.csv") + load_library_extra("doc-styles")
rows = write("doc-styles", src)
CHANGES.append("T3: %d draft rows -> %d generic (2 ENS styles are `Brand Scope` ens). "
               "`Checklist` loaded as authored -- it is a DECLARED list column, short "
               "imperative items separated by `;`, and the draft honours that"
               % (len(src), len(rows)))

# --------------------------------------------------------------- T6 type-scales
src = read("30-t6-type-scales-draft.csv") + load_library_extra("type-scales")
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
src = read("32-t4-palettes-draft.csv") + load_library_extra("palettes")
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
# `Section Order` is a group-FK list into `headings.canonical_section`: each `;`-token
# must match a canonical_section that headings.csv actually carries, checked token by
# token by the gate. It is now populated on every row. The two CV rows were authored
# with the draft; the other fifteen were filled in the draft by
# research/42-merge-section-orders.py from the phase A section-order drafts (39/40/41),
# which the phase A heading drafts gave canonical_section tokens for.
#
# The fill happened in research/36-t10-structures-draft.csv, and that is the only place
# it may ever happen: data/base/structures.csv is written by this loader and by nothing
# else. Hand-editing it puts the shipped table out of step with its own draft and the
# next load silently reverts the edit.

# ----------------------------------------------------------------- T10 structures
src = read("36-t10-structures-draft.csv")
rows = write("structures", src)
CV_AUTHORED = ("cv-academic", "cv-experienced")  # authored with the draft, before phase A
CHANGES.append("T10: %d draft rows -> %d generic (no ENS rows in the draft; the 4 "
               "ENS-scoped structure keys T1 references are out of scope until the "
               "brand overlay authors them). `Section Order` carries an order on %d of "
               "%d rows: %s were authored with the draft, the other %d were merged into "
               "it by research/42-merge-section-orders.py from the phase A section-order "
               "drafts" % (len(src), len(rows),
                           sum(1 for r in rows if r["Section Order"]), len(rows),
                           " and ".join(CV_AUTHORED),
                           len([r for r in rows
                                if r["structure_key"] not in CV_AUTHORED])))

# ============================================================ LOAD PASS 5 ====
# v0.5 designs + provenance (research/80-v05-plan.md §2B/§2C, R-b/R-c; P1.2/P1.3).
# Neither table has a numbered draft -- both are populated entirely from glob inputs,
# authored directly against the manifest header, so there is no re-header step.

# ------------------------------------------------------------------- designs
# research/designs/<family>.csv, one file per family, read in sorted (family) order.
# Unlike research/library/ and research/provenance/, no other agent writes here in this
# phase, so every file present loads -- no allow-list gate.
DESIGNS_DIR = RES / "designs"
_designs_files = sorted(DESIGNS_DIR.glob("*.csv")) if DESIGNS_DIR.is_dir() else []
src = []
for path in _designs_files:
    with path.open(encoding="utf-8-sig", newline="") as f:
        src.extend(csv.DictReader(f))
rows = write("designs", src)
CHANGES.append("designs: %d rows loaded from %d research/designs/<family>.csv file(s) "
               "(P1.3a seed -- one design per existing doc-reasoning row, print-marketing "
               "catalogued once per family it serves: brochure/flyer/poster)"
               % (len(rows), len(_designs_files)))

# ----------------------------------------------------------------- provenance
# research/provenance/*.csv. Other agents are authoring provenance batches under this
# same directory concurrently and their files may be incomplete, so the same review
# gate as LIBRARY_INPUTS_ENABLED applies: only a filename LISTED in
# PROVENANCE_INPUTS_ENABLED loads. Today that is only the seed file this phase authored
# for the designs seeded just above.
PROVENANCE_INPUTS_ENABLED = ["seed-designs.csv", "typefaces-ranked-pairings.csv", "palettes-authority-design-systems.csv", "type-scales-ratio-families.csv", "palettes-ranked-colourlovers.csv"]
PROVENANCE_DIR = RES / "provenance"
_prov_files = ([p for p in sorted(PROVENANCE_DIR.glob("*.csv"))
               if p.name in PROVENANCE_INPUTS_ENABLED] if PROVENANCE_DIR.is_dir() else [])
src = []
for path in _prov_files:
    with path.open(encoding="utf-8-sig", newline="") as f:
        src.extend(csv.DictReader(f))
rows = write("provenance", src)
CHANGES.append("provenance: %d rows loaded from %s (PROVENANCE_INPUTS_ENABLED; every "
               "other file under research/provenance/ is left un-listed until the "
               "orchestrator reviews its batch)"
               % (len(rows), ", ".join(p.name for p in _prov_files)))

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
