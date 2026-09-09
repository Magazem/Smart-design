#!/usr/bin/env python3
"""Build the example two-toy-table manifest plus one fixture per failure
class validate_data.py must catch. Each broken fixture is the clean one
with exactly one thing wrong, so the diff between fixtures *is* the spec of
what each check catches.

Toy schema (deliberately trivial — the point is exercising every mechanism
the harness/resolver implements, not modeling anything real):
  categories: category_key (key), Display Name, Status (enum), Primary,
              On Primary (derived: contrast_at_least >= 4.5 against Primary)
  widgets:    role=entry (resolve.py's fuzzy-search table). widget_key
              (key), Display Name (searchable), Category Key (single FK ->
              categories.category_key), Related Category Keys (`;`-list FK
              -> categories.category_key), Brand Scope
"""
import csv
import io
import json
from pathlib import Path

HERE = Path(__file__).parent

MANIFEST = {
    "schemaVersion": 1,
    "tables": {
        "categories": {
            "filename": "categories.csv",
            "columns": ["category_key", "Display Name", "Status", "Primary", "On Primary"],
            "key_column": "category_key",
            "enums": {"Status": ["active", "deprecated"]},
            "foreign_keys": {},
            "searchable_columns": ["Display Name"],
            "typed_json_columns": [],
            "derived": [
                {"check": "contrast_at_least", "column": "On Primary",
                 "against_column": "Primary", "min_ratio": 4.5},
            ],
        },
        "widgets": {
            "filename": "widgets.csv",
            "columns": ["widget_key", "Display Name", "Category Key",
                        "Related Category Keys", "Brand Scope"],
            "key_column": "widget_key",
            "role": "entry",
            "enums": {},
            "foreign_keys": {
                "Category Key": "categories.category_key",
                "Related Category Keys": {"table": "categories", "column": "category_key", "list": True},
            },
            "searchable_columns": ["Display Name"],
            "typed_json_columns": [],
            "derived": [],
        },
    },
}

CATEGORIES_HEADER = ["category_key", "Display Name", "Status", "Primary", "On Primary"]
CATEGORIES_ROWS = [
    ["tools", "Tools", "active", "#1F6F43", "#FFFFFF"],
    ["games", "Games", "active", "#8B5E3C", "#FFFFFF"],
]

WIDGETS_HEADER = ["widget_key", "Display Name", "Category Key", "Related Category Keys", "Brand Scope"]
WIDGETS_ROWS = [
    ["hammer", "Hammer", "tools", "", "generic"],
    ["dice", "Dice", "games", "games;tools", "generic"],
]

BRAND_WIDGETS_ROWS = [
    ["acme-wrench", "Acme Wrench", "tools", "", "should-be-overwritten-by-harness"],
]


def _write_csv(path, header, rows, bom=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    buf = io.StringIO()
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerow(header)
    writer.writerows(rows)
    with open(path, "wb") as f:
        if bom:
            f.write(b"\xef\xbb\xbf")
        f.write(buf.getvalue().encode("utf-8"))


def _write_manifest(root):
    root.mkdir(parents=True, exist_ok=True)
    (root / "schema-manifest.json").write_text(json.dumps(MANIFEST, indent=2), encoding="utf-8")


def build_clean(root):
    _write_manifest(root)
    _write_csv(root / "base" / "categories.csv", CATEGORIES_HEADER, CATEGORIES_ROWS)
    _write_csv(root / "base" / "widgets.csv", WIDGETS_HEADER, WIDGETS_ROWS)
    _write_csv(root / "brand" / "acme" / "widgets.csv", WIDGETS_HEADER, BRAND_WIDGETS_ROWS)


def build_bad_header(root):
    _write_manifest(root)
    _write_csv(root / "base" / "categories.csv", CATEGORIES_HEADER, CATEGORIES_ROWS)
    # Reordered: "Display Name" and "widget_key" swapped.
    reordered = ["Display Name", "widget_key", "Category Key", "Related Category Keys", "Brand Scope"]
    swapped_rows = [[r[1], r[0], r[2], r[3], r[4]] for r in WIDGETS_ROWS]
    _write_csv(root / "base" / "widgets.csv", reordered, swapped_rows)


def build_bad_enum(root):
    _write_manifest(root)
    rows = [list(r) for r in CATEGORIES_ROWS]
    rows[0][2] = "archived"  # not in ["active", "deprecated"]
    _write_csv(root / "base" / "categories.csv", CATEGORIES_HEADER, rows)
    _write_csv(root / "base" / "widgets.csv", WIDGETS_HEADER, WIDGETS_ROWS)


def build_bad_fk(root):
    _write_manifest(root)
    _write_csv(root / "base" / "categories.csv", CATEGORIES_HEADER, CATEGORIES_ROWS)
    rows = [list(r) for r in WIDGETS_ROWS]
    rows[0][2] = "nonexistent-category"
    _write_csv(root / "base" / "widgets.csv", WIDGETS_HEADER, rows)


def build_bad_bom(root):
    _write_manifest(root)
    _write_csv(root / "base" / "categories.csv", CATEGORIES_HEADER, CATEGORIES_ROWS, bom=True)
    _write_csv(root / "base" / "widgets.csv", WIDGETS_HEADER, WIDGETS_ROWS)


def build_bad_json_cell(root):
    _write_manifest(root)
    _write_csv(root / "base" / "categories.csv", CATEGORIES_HEADER, CATEGORIES_ROWS)
    rows = [list(r) for r in WIDGETS_ROWS]
    rows[0][1] = '{"nested": true}'
    _write_csv(root / "base" / "widgets.csv", WIDGETS_HEADER, rows)


def build_bad_contrast(root):
    _write_manifest(root)
    rows = [list(r) for r in CATEGORIES_ROWS]
    rows[0][3], rows[0][4] = "#F7F8F5", "#FFFFFF"  # near-white on white: fails 4.5:1
    _write_csv(root / "base" / "categories.csv", CATEGORIES_HEADER, rows)
    _write_csv(root / "base" / "widgets.csv", WIDGETS_HEADER, WIDGETS_ROWS)


def build_contrast_both_blank_ok(root):
    """BOTH cells of a `contrast_at_least` pair empty -> the row does not define
    that colour role, so there is nothing to rate and the fixture is CLEAN.
    Mirrors `palettes.mono-ink`, which ships `Accent`/`On Accent` blank on purpose."""
    _write_manifest(root)
    rows = [list(r) for r in CATEGORIES_ROWS]
    rows[0][3], rows[0][4] = "", ""  # Primary and On Primary both absent
    _write_csv(root / "base" / "categories.csv", CATEGORIES_HEADER, rows)
    _write_csv(root / "base" / "widgets.csv", WIDGETS_HEADER, WIDGETS_ROWS)


def build_bad_contrast_half_blank(root):
    """EXACTLY ONE cell of the pair empty -> a half-filled pair is an authoring bug
    and must still fail. Both orderings are present, one per row, because the
    problem line is anchored to `column` either way and only two rows can show that
    an empty *against_column* is caught as well as an empty `column`."""
    _write_manifest(root)
    rows = [list(r) for r in CATEGORIES_ROWS]
    rows[0][3], rows[0][4] = "#1F6F43", ""  # ground, no ink
    rows[1][3], rows[1][4] = "", "#FFFFFF"  # ink, no ground
    _write_csv(root / "base" / "categories.csv", CATEGORIES_HEADER, rows)
    _write_csv(root / "base" / "widgets.csv", WIDGETS_HEADER, WIDGETS_ROWS)


def build_bad_key_collision(root):
    _write_manifest(root)
    _write_csv(root / "base" / "categories.csv", CATEGORIES_HEADER, CATEGORIES_ROWS)
    _write_csv(root / "base" / "widgets.csv", WIDGETS_HEADER, WIDGETS_ROWS)
    colliding = [["hammer", "Acme Hammer", "tools", "", "ignored"]]  # "hammer" already in base
    _write_csv(root / "brand" / "acme" / "widgets.csv", WIDGETS_HEADER, colliding)


def build_missing_base_file(root):
    _write_manifest(root)
    _write_csv(root / "base" / "categories.csv", CATEGORIES_HEADER, CATEGORIES_ROWS)
    # widgets.csv deliberately not written at all.


# ---------------------------------------------------------------------------
# Second, separate toy schema exercising the three Revision-2 format
# additions: group FKs (composable with list), non-FK list_columns
# well-formedness, and reference_columns for a polymorphic
# literal-or-"table:column" cell. Kept apart from categories/widgets above
# so those fixtures (and everything that already asserts against them)
# never change shape.
# ---------------------------------------------------------------------------

GROUP_MANIFEST = {
    "schemaVersion": 1,
    "tables": {
        "tags": {
            "filename": "tags.csv",
            "columns": ["tag_key", "Group"],
            "key_column": "tag_key",
            "enums": {},
            "foreign_keys": {},
            "searchable_columns": [],
            "typed_json_columns": [],
            "derived": [],
        },
        "items": {
            "filename": "items.csv",
            "columns": ["item_key", "Display Name", "Tag Group", "Multi Tag Groups",
                        "Panels", "Keywords"],
            "key_column": "item_key",
            "role": "entry",
            "enums": {},
            "foreign_keys": {
                # "Group" is NOT tags' key_column -- it repeats across rows
                # (red/blue both "colors") -- exactly the shape "group": true
                # exists for (research/09 Revision 2, see schema-manifest-NOTES.md §1.1).
                "Tag Group": {"table": "tags", "column": "Group", "group": True},
                "Multi Tag Groups": {"table": "tags", "column": "Group", "group": True, "list": True},
            },
            "searchable_columns": ["Display Name", "Keywords"],
            "typed_json_columns": [],
            "list_columns": {"Panels": ";"},
            # Mirrors the real schema on both sides of the opt-in. "Keywords" is
            # comma-delimited and NOT a list column, yet must not repeat a token;
            # "Panels" IS a list column and MAY repeat one (it stands in for
            # page-formats."Panels mm", where "99.5;99.5;98.0" is a correct trifold).
            "distinct_token_columns": {"Keywords": ",", "Multi Tag Groups": ";"},
            "derived": [],
        },
        "checks": {
            "filename": "checks.csv",
            "columns": ["check_key", "Threshold"],
            "key_column": "check_key",
            "enums": {},
            "foreign_keys": {},
            "searchable_columns": [],
            "typed_json_columns": [],
            "reference_columns": {
                "Threshold": {"pattern": "^[a-z-]+:[A-Za-z ]+$", "must_resolve": True},
            },
            "derived": [],
        },
    },
}

TAGS_HEADER = ["tag_key", "Group"]
TAGS_ROWS = [
    ["red", "colors"],
    ["blue", "colors"],
    ["circle", "shapes"],
    ["square", "shapes"],
]

ITEMS_HEADER = ["item_key", "Display Name", "Tag Group", "Multi Tag Groups",
                "Panels", "Keywords"]
ITEMS_ROWS = [
    ["apple", "Apple", "colors", "colors;shapes", "a;b;c", "apple, fruit, red"],
    ["ball", "Ball", "shapes", "shapes", "x;y", "ball, round, toy"],
]

CHECKS_HEADER = ["check_key", "Threshold"]
CHECKS_ROWS = [
    ["c1", "5"],              # literal -- does not match the pattern, not checked
    ["c2", "tags:Group"],     # reference -- must resolve, and does
]


def _write_group_manifest(root):
    root.mkdir(parents=True, exist_ok=True)
    (root / "schema-manifest.json").write_text(json.dumps(GROUP_MANIFEST, indent=2), encoding="utf-8")


def build_group_ok(root):
    _write_group_manifest(root)
    _write_csv(root / "base" / "tags.csv", TAGS_HEADER, TAGS_ROWS)
    _write_csv(root / "base" / "items.csv", ITEMS_HEADER, ITEMS_ROWS)
    _write_csv(root / "base" / "checks.csv", CHECKS_HEADER, CHECKS_ROWS)


def build_bad_group_fk(root):
    _write_group_manifest(root)
    _write_csv(root / "base" / "tags.csv", TAGS_HEADER, TAGS_ROWS)
    rows = [list(r) for r in ITEMS_ROWS]
    rows[0][2] = "nonexistent-group"  # "Tag Group" -- not present anywhere in tags.Group
    _write_csv(root / "base" / "items.csv", ITEMS_HEADER, rows)
    _write_csv(root / "base" / "checks.csv", CHECKS_HEADER, CHECKS_ROWS)


def build_bad_list_column(root):
    _write_group_manifest(root)
    _write_csv(root / "base" / "tags.csv", TAGS_HEADER, TAGS_ROWS)
    rows = [list(r) for r in ITEMS_ROWS]
    rows[0][4] = "a;;b"  # "Panels" -- empty item between delimiters
    _write_csv(root / "base" / "items.csv", ITEMS_HEADER, rows)
    _write_csv(root / "base" / "checks.csv", CHECKS_HEADER, CHECKS_ROWS)


def build_bad_distinct_token(root):
    _write_group_manifest(root)
    _write_csv(root / "base" / "tags.csv", TAGS_HEADER, TAGS_ROWS)
    rows = [list(r) for r in ITEMS_ROWS]
    rows[0][5] = "apple, fruit, red, fruit"  # "Keywords" -- "fruit" twice
    _write_csv(root / "base" / "items.csv", ITEMS_HEADER, rows)
    _write_csv(root / "base" / "checks.csv", CHECKS_HEADER, CHECKS_ROWS)


def build_repeat_in_undeclared_list_ok(root):
    # "Panels" is a declared list column with NO distinct_token_columns entry, so a
    # repeated panel width must pass -- the page-formats."Panels mm" case.
    _write_group_manifest(root)
    _write_csv(root / "base" / "tags.csv", TAGS_HEADER, TAGS_ROWS)
    rows = [list(r) for r in ITEMS_ROWS]
    rows[0][4] = "99.5;99.5;98.0"
    _write_csv(root / "base" / "items.csv", ITEMS_HEADER, rows)
    _write_csv(root / "base" / "checks.csv", CHECKS_HEADER, CHECKS_ROWS)


def build_bad_reference_column(root):
    _write_group_manifest(root)
    _write_csv(root / "base" / "tags.csv", TAGS_HEADER, TAGS_ROWS)
    _write_csv(root / "base" / "items.csv", ITEMS_HEADER, ITEMS_ROWS)
    rows = [list(r) for r in CHECKS_ROWS]
    rows[1][1] = "nonexistent-table:Some Column"  # matches the pattern, doesn't resolve
    _write_csv(root / "base" / "checks.csv", CHECKS_HEADER, rows)


# ---------------------------------------------------------------------------
# Third toy schema: the document-vocabulary tables `ddi.py handoff` reads
# (page-formats, typefaces, type-scales, palettes, render-targets,
# constraints), using the REAL column names from data/schema-manifest.json
# (Trim W mm, Size pt, Set Key, ...) at toy scale -- so the handoff step is
# exercised against the vocabulary it will actually see once the real tables
# are authored, without waiting on that authoring. Kept apart from
# categories/widgets and tags/items/checks above for the same reason those
# two are kept apart from each other: nothing that already asserts against
# manifest_ok's shape may ever change.
#
# Two entry rows: "report-print" (a page-formatted print doc, two pdf render
# targets -- one submittable-rgb, one pdfx4-rgb, mirroring data/base/
# render-targets.csv's real pdf-chromium/pdf-weasyprint-pdfx4 rows) and
# "keynote-deck" (a slide deck -- deliberately has NO Page Format Key, so the
# FK walk never pulls in a page-formats row for it: pptxgenjs never wants a
# print page format regardless of format naming, per research/24 section 3
# item 2).
# ---------------------------------------------------------------------------

DOCVOCAB_MANIFEST = {
    "schemaVersion": 1,
    "tables": {
        "page-formats": {
            "filename": "page-formats.csv",
            "columns": ["page_format_key", "Display Name", "Trim W mm", "Trim H mm",
                        "Margin Top mm", "Margin Bottom mm", "Margin Inside mm",
                        "Margin Outside mm", "Bleed mm"],
            "key_column": "page_format_key",
            "enums": {},
            "foreign_keys": {},
            "searchable_columns": ["Display Name"],
            "typed_json_columns": [],
            "display_columns": ["Trim W mm", "Trim H mm", "Margin Top mm", "Margin Bottom mm",
                                 "Margin Inside mm", "Margin Outside mm", "Bleed mm"],
            "derived": [],
        },
        "typefaces": {
            "filename": "typefaces.csv",
            "columns": ["typeface_key", "Display Name", "Heading Family", "Body Family",
                        "Safe Stack Fallback", "Scale Key"],
            "key_column": "typeface_key",
            "enums": {},
            "foreign_keys": {
                "Scale Key": {"table": "type-scales", "column": "scale_key", "group": True},
            },
            "searchable_columns": ["Display Name"],
            "typed_json_columns": [],
            "display_columns": ["Heading Family", "Body Family", "Safe Stack Fallback", "Scale Key"],
            "derived": [],
        },
        "type-scales": {
            "filename": "type-scales.csv",
            "columns": ["scale_row_key", "scale_key", "Medium", "Role", "Size pt"],
            "key_column": "scale_row_key",
            "enums": {},
            "foreign_keys": {},
            "searchable_columns": [],
            "typed_json_columns": [],
            "display_columns": ["Medium", "Role", "Size pt"],
            "derived": [],
        },
        "palettes": {
            "filename": "palettes.csv",
            "columns": ["palette_key", "Display Name", "Primary", "Secondary", "Accent",
                        "Background", "Foreground"],
            "key_column": "palette_key",
            "enums": {},
            "foreign_keys": {},
            "searchable_columns": ["Display Name"],
            "typed_json_columns": [],
            "display_columns": ["Primary", "Secondary", "Accent", "Background", "Foreground"],
            "derived": [],
        },
        "render-targets": {
            "filename": "render-targets.csv",
            "columns": ["render_key", "Format", "Engine", "Engine Path", "Engine Invocation",
                        "Font Rule", "Print Tier Max"],
            "key_column": "render_key",
            "enums": {},
            "foreign_keys": {},
            "searchable_columns": [],
            "typed_json_columns": [],
            "display_columns": ["Format", "Engine", "Engine Path", "Engine Invocation",
                                 "Font Rule", "Print Tier Max"],
            "derived": [],
        },
        "constraints": {
            "filename": "constraints.csv",
            "columns": ["constraint_key", "Set Key", "Check"],
            "key_column": "constraint_key",
            "enums": {},
            "foreign_keys": {},
            "searchable_columns": [],
            "typed_json_columns": [],
            "display_columns": ["Set Key"],
            "derived": [],
        },
        "docs": {
            "filename": "docs.csv",
            "columns": ["doc_key", "Display Name", "Page Format Key", "Typeface Key",
                        "Palette Key", "Render Target Keys", "Constraint Set Keys"],
            "key_column": "doc_key",
            "role": "entry",
            "enums": {},
            "foreign_keys": {
                "Page Format Key": "page-formats.page_format_key",
                "Typeface Key": "typefaces.typeface_key",
                "Palette Key": "palettes.palette_key",
                "Render Target Keys": {"table": "render-targets", "column": "render_key", "list": True},
                "Constraint Set Keys": {"table": "constraints", "column": "Set Key", "group": True},
            },
            "searchable_columns": ["Display Name"],
            "typed_json_columns": [],
            "derived": [],
        },
    },
}

PAGE_FORMATS_HEADER = ["page_format_key", "Display Name", "Trim W mm", "Trim H mm",
                        "Margin Top mm", "Margin Bottom mm", "Margin Inside mm",
                        "Margin Outside mm", "Bleed mm"]
PAGE_FORMATS_ROWS = [
    ["a4-print", "A4 Print", "210", "297", "20", "20", "25", "20", "3"],
]

TYPEFACES_HEADER = ["typeface_key", "Display Name", "Heading Family", "Body Family",
                     "Safe Stack Fallback", "Scale Key"]
TYPEFACES_ROWS = [
    ["corp-serif", "Corporate Serif", "Source Serif 4", "Source Sans 3", "Georgia", "print-scale-a"],
]

TYPE_SCALES_HEADER = ["scale_row_key", "scale_key", "Medium", "Role", "Size pt"]
TYPE_SCALES_ROWS = [
    ["print-scale-a__h1", "print-scale-a", "print", "h1", "28"],
    ["print-scale-a__h2", "print-scale-a", "print", "h2", "18"],
    ["print-scale-a__body", "print-scale-a", "print", "body", "11"],
]

PALETTES_HEADER = ["palette_key", "Display Name", "Primary", "Secondary", "Accent",
                    "Background", "Foreground"]
PALETTES_ROWS = [
    ["forest-brand", "Forest Brand", "#1F6F43", "#2E2E2E", "#C08A2E", "#FFFFFF", "#1A1A1A"],
]

RENDER_TARGETS_HEADER = ["render_key", "Format", "Engine", "Engine Path", "Engine Invocation",
                          "Font Rule", "Print Tier Max"]
RENDER_TARGETS_ROWS = [
    # Mirrors data/base/render-targets.csv's real pdf-chromium / pdf-weasyprint-pdfx4 rows.
    ["pdf-chromium", "pdf", "headless-chromium", "/opt/google/chrome/chrome",
     "--headless --no-sandbox --disable-gpu --print-to-pdf=%o --no-pdf-header-footer %i",
     "embed", "submittable-rgb"],
    ["pdf-weasyprint-pdfx4", "pdf", "weasyprint", "weasyprint (module)",
     "--pdf-variant=pdf/x-4 --output-intent=srgb", "embed", "pdfx4-rgb"],
    ["pptxgenjs-deck", "pptx", "pptxgenjs", "pptxgenjs (module)", "", "embed", "none"],
]

CONSTRAINTS_HEADER = ["constraint_key", "Set Key", "Check"]
CONSTRAINTS_ROWS = [
    ["c-dpi", "print-basics", "min-dpi"],
    ["c-margin", "print-basics", "min-margin"],
    ["c-contrast", "brand-contrast", "contrast-ratio"],
]

DOCS_HEADER = ["doc_key", "Display Name", "Page Format Key", "Typeface Key", "Palette Key",
               "Render Target Keys", "Constraint Set Keys"]
DOCS_ROWS = [
    ["report-print", "Print Report", "a4-print", "corp-serif", "forest-brand",
     "pdf-chromium;pdf-weasyprint-pdfx4", "print-basics"],
    ["keynote-deck", "Keynote Deck", "", "corp-serif", "forest-brand",
     "pptxgenjs-deck", "brand-contrast"],
]


def _write_docvocab_manifest(root):
    root.mkdir(parents=True, exist_ok=True)
    (root / "schema-manifest.json").write_text(json.dumps(DOCVOCAB_MANIFEST, indent=2), encoding="utf-8")


def build_docvocab_ok(root):
    _write_docvocab_manifest(root)
    _write_csv(root / "base" / "page-formats.csv", PAGE_FORMATS_HEADER, PAGE_FORMATS_ROWS)
    _write_csv(root / "base" / "typefaces.csv", TYPEFACES_HEADER, TYPEFACES_ROWS)
    _write_csv(root / "base" / "type-scales.csv", TYPE_SCALES_HEADER, TYPE_SCALES_ROWS)
    _write_csv(root / "base" / "palettes.csv", PALETTES_HEADER, PALETTES_ROWS)
    _write_csv(root / "base" / "render-targets.csv", RENDER_TARGETS_HEADER, RENDER_TARGETS_ROWS)
    _write_csv(root / "base" / "constraints.csv", CONSTRAINTS_HEADER, CONSTRAINTS_ROWS)
    _write_csv(root / "base" / "docs.csv", DOCS_HEADER, DOCS_ROWS)


BUILDERS = {
    "manifest_ok": build_clean,
    "manifest_bad_header": build_bad_header,
    "manifest_bad_enum": build_bad_enum,
    "manifest_bad_fk": build_bad_fk,
    "manifest_bad_bom": build_bad_bom,
    "manifest_bad_json_cell": build_bad_json_cell,
    "manifest_bad_contrast": build_bad_contrast,
    "manifest_contrast_both_blank_ok": build_contrast_both_blank_ok,
    "manifest_bad_contrast_half_blank": build_bad_contrast_half_blank,
    "manifest_bad_key_collision": build_bad_key_collision,
    "manifest_missing_base_file": build_missing_base_file,
    "manifest_group_ok": build_group_ok,
    "manifest_bad_group_fk": build_bad_group_fk,
    "manifest_bad_list_column": build_bad_list_column,
    "manifest_bad_distinct_token": build_bad_distinct_token,
    "manifest_repeat_in_undeclared_list_ok": build_repeat_in_undeclared_list_ok,
    "manifest_bad_reference_column": build_bad_reference_column,
    "manifest_docvocab_ok": build_docvocab_ok,
}


if __name__ == "__main__":
    for name, builder in BUILDERS.items():
        builder(HERE / name)
        print(f"wrote {HERE / name}")
