#!/usr/bin/env python3
"""Turn a one-file brand description into a brand-kit ZIP. Stdlib only.

Usage:
    python3 make_brand_kit.py <brand.md> [-o/--output PATH] [--dry-run]

This is the "generate your design system" step: a user (or Claude, on their
behalf) writes ONE `brand.md` file describing their brand, and this script
turns it into rows across the document-design library's tables, self-checks
those rows against the same gate `validate_data.py` runs in CI, and — only if
that gate is clean — zips the result into `<slug>-brand-kit.zip`, the exact
artifact `merge_brand_kit.py` accepts (see that script's own docstring for
the kit contract this produces: `brand.md` at the zip root, `data/<name>.csv`
one path segment under `data/`, `assets/...`).

BRAND.MD FORMAT
===============
A `brand.md` file is plain text with `key: value` lines and `## Section`
headings. A single leading `# Title` line (if present) is ignored. Blank
lines are ignored everywhere. Every other line is checked against a fixed
grammar; anything that doesn't fit — an unrecognised top-level key, an
unrecognised section heading, an unrecognised key inside a section, a
malformed value — is a **hard failure naming the exact line number**. There
is no silent best-effort parsing.

Top level (before any `##` section), only these keys are allowed:
    slug: <value>          required. Must match ^[a-z0-9-]+$. Becomes the
                            kit's brand directory name and doc_key/palette_
                            key/typeface_key prefix.
    logo: <path>            optional. A local filesystem path (relative to
                            brand.md's own directory, or absolute) to an
                            image file. Copied into the kit's assets/.

## Palette   (required)
Six `role: #RRGGBB` lines, all required, in any order:
    primary: #1F6F43
    secondary: #8B5E3C
    accent: #9ACD32
    background: #F7F8F5
    foreground: #1E2A23
    muted: #DCE8DF
On-colours (On Primary, On Secondary, On Accent, On Muted) are NEVER typed
here — they are derived by `lib/color.on_color` (which always returns pure
`#FFFFFF` or `#000000`, whichever has higher contrast against the role's own
colour). Rule Hair/Rule Strong/Rule Brand and the Text-Safe / Fill-Only /
Category-Marker role lists are also derived, not typed — see
`_derive_palette_row`'s docstring for exactly how.

## Typefaces   (required)
    heading: <family name>     required
    body: <family name>        required
    mono: <family name>        optional
Safe Stack Fallback, Safe Stack Availability, Embedding Licence, Has Tabular
Figures, Category Contrast and Scale Key are all derived — see
`_derive_typefaces_row`.

## Doctypes   (required, at least one)
One bare doctype name per line. Two kinds are accepted:
  * the four legacy ENS short-names in DOCTYPE_CATALOG below: `note-interne`,
    `formulaire`, `social`, `slides`;
  * ANY generic base doctype, by its `doc_key` in `data/base/doctypes.csv`
    (e.g. `cv-uk`, `report-short`, `invoice-tabular`, `slide-deck-projection`).
    The kit's row is derived from that base row: Artifact Class, Reasoning
    Key, Page Format Key, Render Target Keys, Constraint Set Keys, Structure
    Key, Region Key, Family and Default Language are copied verbatim (the
    base row is the source this script otherwise lacks); Keywords, Brand
    Scope and doc_key (`<slug>-<doc_key>`) follow the brand path.
A legacy short-name wins over a base doc_key of the same name. Any other name
is a hard failure listing every valid key — this script does not guess an
Artifact Class, Render Target, or Reasoning Key for a doctype it doesn't know:
    note-interne
    cv-uk
    invoice-tabular

## Designs   (optional)
One `<family>: <design_key>` line per family, e.g. `cv: cv-editorial`.
`<family>` must be a doctypes.Family enum token from the schema manifest and
`<design_key>` a row of `data/base/designs.csv` whose Family is that family
(anything else is a hard failure naming the line). For each line the kit gets
a `data/doc-reasoning.csv` row `<slug>-<family>` that COPIES the design's own
doc-reasoning row (Style Key, bias terms, Doc Conditions, Anti-Pattern
Tokens, Severity) but swaps Palette Key / Typeface Key for the brand's own
generated rows (doc-reasoning has no Brand Scope column; the loader scopes
the row from the kit's directory, i.e. to the slug). Every brand doctype of
that family then gets Reasoning Key `<slug>-<family>`. A family with no line
keeps its current Reasoning Key; with no ## Designs section no
doc-reasoning.csv is emitted at all.
    cv: cv-editorial
    invoice: invoice-tabular

## Type scales   (optional)
One `<medium>: <scale_key>` line per medium, e.g. `projection:
lib-perfect-fourth-projection`. `<medium>` must be a type-scales.Medium enum
token from the schema manifest and `<scale_key>` a scale_key of
`data/base/type-scales.csv` whose rows all have that Medium (anything else is
a hard failure naming the line). For each line the kit gets brand type-scale
rows `<slug>-<medium>` COPYING the library scale's roles, sizes and leadings
(scale_row_key `<slug>-<medium>-<medium>-<role>`, same shape as the
## Document defaults path; no Brand Scope column, the kit directory scopes
them). typefaces has ONE Scale Key per row, so the kit emits one typeface row
per listed medium, identical families, typeface_key `<base_key>-<medium>` and
Scale Key `<slug>-<medium>`. A brand doctype's medium is `projection` if its
Constraint Set Keys include `projection`, `screen` if every Render Target is a
png-*/html-* target, else `print`; a ## Designs doc-reasoning row takes the
Typeface Key of the typeface row matching the medium of the first doctype of
its family (falling back to the first listed medium if that medium has no
line). Without this section nothing changes (single typeface row, the
`type-scale` Document defaults path below). A `print:` line here cannot be
combined with `type-scale` lines in ## Document defaults (both would emit
`<slug>-print`) -- a hard failure.
    print: lib-major-third-print
    projection: lib-perfect-fourth-projection

## Voice   (optional)
Free text, any content, no grammar checked. Passed through to the kit's
brand.md verbatim (via `lib/data.py`'s loader this text never becomes a CSV
cell) — it exists for the *next* Claude conversation to read when writing in
this brand's voice, not for this script.

## Document defaults   (optional)
Two directive forms, one per line:
    page-format <doctype>: <page_format_key>
    type-scale <role>: <size in pt>
`<doctype>` must already appear in the ## Doctypes section. `<page_format_key>`
is checked for real against `data/base/page-formats.csv` (that table exists
today) — an unresolvable key is a hard failure, not a warning. `<role>` must
be one of the type-scales table's Role enum values (label, caption, body,
body-dense, lead, h3, h2, h1). If no `type-scale` lines are given, no
`data/type-scales.csv` is produced at all.

WHY SOME FKS ARE STILL BLANK TODAY
===================================
`data/base/structures.csv` exists now, so `Structure Key` is resolved for
real per doctype — see STRUCTURE_KEY_HINT — except for a doctype with no
honest generic match (`social`, today, a canvas artifact with no document
structure to name), which is left blank with a printed gap, same treatment
as `Page Format Key` below. `Region Key` stays blank for all four v1
doctypes regardless: `data/base/cv-regions.csv` also exists, but its seven
region keys are CV-specific, and none of `note-interne`, `formulaire`,
`social`, `slides` is a CV — there is no generic value to reference for any
of them. This script still writes a `Reasoning Key` value on every
doctypes.csv row (a plausible generic `data/base/doc-reasoning.csv`
category — see REASONING_KEY_HINT), except for a doctype with no honest
generic match (`social`, today), which is left blank with a printed gap,
same treatment as `Page Format Key` below.

`Page Format Key` follows the same rule: `data/base/page-formats.csv`
already exists. If the brand.md gives an explicit
`page-format <doctype>: ...` override, it is checked for real (a typo is a
hard failure). If a doctype's catalog entry has no matching generic
page-format (true for `social` and `slides` today — there is no generic
social-media or 16:9 slide format in base yet) and the user gave no
override, the cell is left blank and the gap is printed, not hidden.

SELF-CHECK
==========
After building every row, this script copies `data/base/` and
`data/schema-manifest.json` from the currently-detected skill directory into
a temp dir, writes the generated CSVs under `data/brand/<slug>/`, and calls
`validate_data.validate()` on it — the exact function CI and
`merge_brand_kit.py` both run over the WHOLE merged dataset (base + every
brand). The full raw gate output is always printed. Problems are then split
by SCOPE: "real" is anything located under the `data/brand/<slug>/` files
this run just wrote (the kit's own rows) — that blocks emission. Everything
else — including a still-missing base table, or a pre-existing, unrelated
base data defect nobody has fixed yet — is printed as an "expected" (non-
blocking) gap, because it isn't this kit's row to answer for. If any real
problem remains, the ZIP is refused and only the problems are printed. Every
WCAG contrast pair used by the derived on-colours is also printed
unconditionally, computed via `lib/color.contrast_ratio`.

`--dry-run` runs everything (parse, derive, self-check, print) but never
writes a ZIP, dry-run or not.

Skill directory detection mirrors `merge_brand_kit.py`: this file's own
location's grandparent is the live skill root; override with DDI_SKILL_DIR.
Output defaults to DDI_OUTPUTS_DIR (default `/mnt/user-data/outputs`),
mirroring `merge_brand_kit.py`'s OUTPUTS DIRECTORY convention; `-o/--output`
overrides, and is refused if it resolves inside the read-only uploads mount.
"""
from __future__ import annotations

import argparse
import ast
import csv
import io
import json
import os
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path


def _assert_stdlib_only(extra_allowed=()):
    """Fail loudly at import time if a non-stdlib import is ever added here.

    See lib/color.py and validate_data.py for the identical guard.
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
                    f"non-stdlib import '{name}' found in {__file__} — "
                    "this module must be Python stdlib only"
                )


_assert_stdlib_only(extra_allowed={"color", "validate_data"})

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
import color  # noqa: E402
import validate_data  # noqa: E402


DEFAULT_OUTPUTS_DIR = "/mnt/user-data/outputs"
DEFAULT_UPLOADS_DIR = "/mnt/user-data/uploads"

SLUG_RE = re.compile(r"^[a-z0-9-]+$")
HEX_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")
KV_RE = re.compile(r"^([A-Za-z][A-Za-z0-9 _-]*?):\s*(.*)$")
SECTION_RE = re.compile(r"^##\s+(.+?)\s*$")
H1_RE = re.compile(r"^#\s+(?!#)")
DOC_DEFAULT_RE = re.compile(r"^(page-format|type-scale)\s+([a-z][a-z0-9-]*)\s*:\s*(.+)$")

TOP_LEVEL_KEYS = {"slug", "logo"}
PALETTE_ROLES = ("primary", "secondary", "accent", "background", "foreground", "muted")
TYPEFACE_KEYS = {"heading", "body", "mono"}
ALLOWED_SECTIONS = {"Palette", "Typefaces", "Doctypes", "Voice", "Document defaults", "Designs", "Type scales"}
TYPESCALE_ROLES = ("label", "caption", "body", "body-dense", "lead", "h3", "h2", "h1")

DESIGN_LINE_RE = re.compile(r"^([a-z][a-z0-9-]*)\s*:\s*([a-z0-9][a-z0-9-]*)$")

# v1's fixed, well-formed doctype catalog. Extending this to an arbitrary
# doctype would require a source for Artifact Class / Render Target Keys /
# Reasoning Key that brand.md does not supply — see module docstring.
DOCTYPE_CATALOG = {
    "note-interne": dict(
        display="Note interne", artifact_class="flow",
        render_targets=("docx-office", "pdf-chromium"),
        page_format_hint="a4-professional",
        constraint_hint=("photocopy-safe",),
    ),
    "formulaire": dict(
        display="Formulaire", artifact_class="flow",
        render_targets=("pdf-chromium",),
        page_format_hint="a4-professional",
        constraint_hint=("photocopy-safe", "legal-text"),
    ),
    "social": dict(
        display="Post reseaux sociaux", artifact_class="canvas",
        render_targets=("png-social",),
        page_format_hint=None,
        constraint_hint=(),
    ),
    "slides": dict(
        display="Presentation", artifact_class="canvas",
        render_targets=("pptx-office",),
        page_format_hint=None,
        constraint_hint=("projection",),
    ),
}

# Generic (brand-agnostic) Reasoning Key per doctype -- must name a real
# data/base/doc-reasoning.csv doc_category (checked for real once that
# table is authored, same as Page Format Key). "social" has no honest
# generic match in that table's 15 categories today (all print/paper- or
# deck-shaped); left unset rather than forcing a wrong bias lookup -- see
# the None-hint gap print in main(), mirroring Page Format Key's pattern.
REASONING_KEY_HINT = {
    "note-interne": "memo-internal",
    "formulaire": "form-handfilled",
    "slides": "deck-generic",
}

# Generic (brand-agnostic) Structure Key per doctype -- must name a real
# data/base/structures.csv structure_key (checked for real, same as
# Reasoning Key and Page Format Key). "social" has no honest generic match
# in that table today (all entries are print- or deck-shaped documents with
# a section order; a social post is a canvas with no sections); left unset
# rather than forcing a wrong lookup -- see the None-hint gap print in
# main(), mirroring Page Format Key's and Reasoning Key's pattern.
STRUCTURE_KEY_HINT = {
    "note-interne": "memo-standard",
    "formulaire": "form-standard",
    "slides": "deck-standard",
}

# research/80-v05-plan.md §2A: `doctypes.Family` is non-nullable (no "" in the enum,
# unlike Reasoning Key/Page Format Key/Structure Key above, which stay unset when this
# builder has no honest generic match) -- every emitted doctype row must carry one of
# the 16 FAMILIES tokens. "note-interne"/"formulaire"/"slides" map the same way
# research/26-t1-doctypes-draft.csv maps their generic ENS counterparts
# (ens-note-interne/ens-formulaire/ens-slides). "social" has no dedicated family in the
# enum (it is a single branded marketing image, the same "single canvas, promotional"
# shape as `poster`, not a data-visual like `infographic`) -- classified `poster` for
# the same reason research/26 classifies `ens-social` that way.
FAMILY_HINT = {
    "note-interne": "memo",
    "formulaire": "form",
    "social": "poster",
    "slides": "deck",
}

# Small, deliberately modest classification used only to pick a Category
# Contrast enum value and a sensible Safe Stack Fallback default. Not a
# substitute for data/base/font-substitutes.csv, which is checked first.
SANS_FAMILIES = {
    "manrope", "inter", "arial", "helvetica", "roboto", "open sans", "lato",
    "montserrat", "source sans", "source sans 3", "public sans",
    "ibm plex sans", "noto sans", "work sans", "nunito", "poppins",
    "raleway", "mulish", "rubik", "karla", "dm sans", "figtree",
    "plus jakarta sans", "calibri", "verdana", "trebuchet ms", "candara",
    "corbel", "segoe ui",
}
SERIF_FAMILIES = {
    "times new roman", "georgia", "garamond", "merriweather",
    "source serif", "source serif 4", "ibm plex serif", "playfair display",
    "pt serif", "lora", "noto serif", "crimson text", "spectral",
    "libre baskerville", "eb garamond", "cormorant", "cambria",
    "constantia", "courier new",
}

TYPESCALE_LEADING = {
    "label": 1.3, "caption": 1.3, "body": 1.35, "body-dense": 1.2,
    "lead": 1.35, "h3": 1.15, "h2": 1.15, "h1": 1.1,
}


class BrandKitError(ValueError):
    """A problem with brand.md, or with the rows it produces, that must
    abort before anything is written."""


# ---------------------------------------------------------------------------
# brand.md parsing
# ---------------------------------------------------------------------------

def load_base_doctypes(skill_dir: Path | None = None) -> dict[str, dict]:
    """doc_key -> row for data/base/doctypes.csv ({} if it cannot be found)."""
    skill_dir = skill_dir or find_skill_dir()
    if skill_dir is None:
        return {}
    path = skill_dir / "data" / "base" / "doctypes.csv"
    if not path.is_file():
        return {}
    with path.open(encoding="utf-8", newline="") as f:
        return {r["doc_key"]: r for r in csv.DictReader(f) if r.get("doc_key")}


def load_designs_context(skill_dir: Path | None = None) -> tuple[set[str], dict[str, dict]]:
    """(doctypes.Family enum tokens, design_key -> row of data/base/designs.csv)."""
    skill_dir = skill_dir or find_skill_dir()
    if skill_dir is None:
        return set(), {}
    manifest = json.loads((skill_dir / "data" / "schema-manifest.json").read_text(encoding="utf-8"))
    families = set(manifest["tables"]["doctypes"]["enums"]["Family"])
    path = skill_dir / "data" / "base" / "designs.csv"
    designs = {}
    if path.is_file():
        with path.open(encoding="utf-8", newline="") as f:
            designs = {r["design_key"]: r for r in csv.DictReader(f) if r.get("design_key")}
    return families, designs


def load_scales_context(skill_dir: Path | None = None) -> tuple[set[str], dict[str, set[str]]]:
    """(type-scales.Medium enum tokens, scale_key -> Mediums of its base rows)."""
    skill_dir = skill_dir or find_skill_dir()
    if skill_dir is None:
        return set(), {}
    manifest = json.loads((skill_dir / "data" / "schema-manifest.json").read_text(encoding="utf-8"))
    mediums = set(manifest["tables"]["type-scales"]["enums"]["Medium"])
    scales: dict[str, set[str]] = {}
    path = skill_dir / "data" / "base" / "type-scales.csv"
    if path.is_file():
        with path.open(encoding="utf-8", newline="") as f:
            for r in csv.DictReader(f):
                scales.setdefault(r["scale_key"], set()).add(r["Medium"])
    return mediums, scales


def parse_brand_md(text: str, base_doctypes: dict[str, dict] | None = None,
                   designs_context: tuple[set[str], dict[str, dict]] | None = None,
                   scales_context: tuple[set[str], dict[str, set[str]]] | None = None) -> dict:
    """Parse brand.md into a structured dict. Raises BrandKitError with a
    line number on the first problem found. `base_doctypes` (default: loaded
    from the detected skill dir) supplies the generic doc_keys ## Doctypes
    may name besides the DOCTYPE_CATALOG legacy entries."""
    if base_doctypes is None:
        base_doctypes = load_base_doctypes()
    known_doctypes = set(DOCTYPE_CATALOG) | set(base_doctypes)
    families, base_designs = designs_context if designs_context is not None else load_designs_context()
    mediums, base_scales = scales_context if scales_context is not None else load_scales_context()
    lines = text.splitlines()
    top = {}
    palette = {}
    typefaces = {}
    doctypes = []
    voice_lines = []
    page_format_overrides = {}
    type_scale = {}
    designs = {}
    scale_choices = {}

    section = None  # None, "Palette", "Typefaces", "Doctypes", "Voice", "Document defaults"
    seen_h1 = False

    for line_no, raw in enumerate(lines, start=1):
        stripped = raw.strip()
        if not stripped:
            continue

        section_match = SECTION_RE.match(stripped)
        if section_match:
            name = section_match.group(1)
            name = next((a for a in ALLOWED_SECTIONS if a.lower() == name.lower()), name)
            if name not in ALLOWED_SECTIONS:
                raise BrandKitError(
                    f"brand.md:{line_no}: unknown section heading '## {name}' "
                    f"(allowed: {', '.join(sorted(ALLOWED_SECTIONS))})"
                )
            section = name
            continue

        if section is None and H1_RE.match(stripped) and not seen_h1:
            seen_h1 = True
            continue

        if section == "Voice":
            voice_lines.append(raw)
            continue

        if section is None:
            m = KV_RE.match(stripped)
            if not m:
                raise BrandKitError(f"brand.md:{line_no}: unrecognised line at top level: {stripped!r}")
            key, value = m.group(1).strip().lower(), m.group(2).strip()
            if key not in TOP_LEVEL_KEYS:
                raise BrandKitError(
                    f"brand.md:{line_no}: unknown top-level key '{key}' "
                    f"(allowed: {', '.join(sorted(TOP_LEVEL_KEYS))})"
                )
            top[key] = value
            continue

        if section == "Palette":
            m = KV_RE.match(stripped)
            if not m:
                raise BrandKitError(f"brand.md:{line_no}: unrecognised line in ## Palette: {stripped!r}")
            key, value = m.group(1).strip().lower(), m.group(2).strip()
            if key not in PALETTE_ROLES:
                raise BrandKitError(
                    f"brand.md:{line_no}: unknown palette role '{key}' "
                    f"(allowed: {', '.join(PALETTE_ROLES)})"
                )
            if not HEX_RE.match(value):
                raise BrandKitError(f"brand.md:{line_no}: '{key}' value {value!r} is not a #RRGGBB hex colour")
            palette[key] = value
            continue

        if section == "Typefaces":
            m = KV_RE.match(stripped)
            if not m:
                raise BrandKitError(f"brand.md:{line_no}: unrecognised line in ## Typefaces: {stripped!r}")
            key, value = m.group(1).strip().lower(), m.group(2).strip()
            if key not in TYPEFACE_KEYS:
                raise BrandKitError(
                    f"brand.md:{line_no}: unknown typeface key '{key}' "
                    f"(allowed: {', '.join(sorted(TYPEFACE_KEYS))})"
                )
            if not value:
                raise BrandKitError(f"brand.md:{line_no}: '{key}' has no value")
            typefaces[key] = value
            continue

        if section == "Doctypes":
            m = KV_RE.match(stripped)
            name = m.group(1).strip().lower() if m and not m.group(2) else stripped.lower()
            if name not in known_doctypes:
                raise BrandKitError(
                    f"brand.md:{line_no}: unknown doctype '{name}' "
                    f"(supported: {', '.join(sorted(known_doctypes))})"
                )
            if name in doctypes:
                raise BrandKitError(f"brand.md:{line_no}: doctype '{name}' listed twice")
            doctypes.append(name)
            continue

        if section == "Designs":
            m = DESIGN_LINE_RE.match(stripped.lower())
            if not m:
                raise BrandKitError(
                    f"brand.md:{line_no}: unrecognised line in ## Designs: {stripped!r} "
                    "(expected '<family>: <design_key>')"
                )
            family, design_key = m.groups()
            if family not in families:
                raise BrandKitError(
                    f"brand.md:{line_no}: unknown family '{family}' in ## Designs "
                    f"(allowed: {', '.join(sorted(families))})"
                )
            if family in designs:
                raise BrandKitError(f"brand.md:{line_no}: family '{family}' listed twice in ## Designs")
            row = base_designs.get(design_key)
            if row is None:
                raise BrandKitError(
                    f"brand.md:{line_no}: unknown design '{design_key}' "
                    f"(see data/base/designs.csv; {family} designs: "
                    f"{', '.join(sorted(k for k, r in base_designs.items() if r['Family'] == family)) or 'none'})"
                )
            if row["Family"] != family:
                raise BrandKitError(
                    f"brand.md:{line_no}: design '{design_key}' belongs to family "
                    f"'{row['Family']}', not '{family}'"
                )
            designs[family] = design_key
            continue

        if section == "Type scales":
            m = DESIGN_LINE_RE.match(stripped.lower())
            if not m:
                raise BrandKitError(
                    f"brand.md:{line_no}: unrecognised line in ## Type scales: {stripped!r} "
                    "(expected '<medium>: <scale_key>')"
                )
            medium, scale_key = m.groups()
            if medium not in mediums:
                raise BrandKitError(
                    f"brand.md:{line_no}: unknown medium '{medium}' in ## Type scales "
                    f"(allowed: {', '.join(sorted(mediums))})"
                )
            if medium in scale_choices:
                raise BrandKitError(f"brand.md:{line_no}: medium '{medium}' listed twice in ## Type scales")
            if scale_key not in base_scales:
                raise BrandKitError(
                    f"brand.md:{line_no}: unknown scale '{scale_key}' "
                    f"(see data/base/type-scales.csv; {medium} scales: "
                    f"{', '.join(sorted(k for k, ms in base_scales.items() if medium in ms)) or 'none'})"
                )
            if base_scales[scale_key] != {medium}:
                raise BrandKitError(
                    f"brand.md:{line_no}: scale '{scale_key}' has medium "
                    f"{'/'.join(sorted(base_scales[scale_key]))}, not '{medium}'"
                )
            scale_choices[medium] = scale_key
            continue

        if section == "Document defaults":
            m = DOC_DEFAULT_RE.match(stripped)
            if not m:
                raise BrandKitError(
                    f"brand.md:{line_no}: unrecognised line in ## Document defaults: {stripped!r} "
                    "(expected 'page-format <doctype>: <key>' or 'type-scale <role>: <pt>')"
                )
            directive, arg, value = m.group(1), m.group(2), m.group(3).strip()
            if directive == "page-format":
                if arg not in known_doctypes:
                    raise BrandKitError(
                        f"brand.md:{line_no}: page-format override names unknown doctype '{arg}'"
                    )
                page_format_overrides[arg] = value
            else:
                if arg not in TYPESCALE_ROLES:
                    raise BrandKitError(
                        f"brand.md:{line_no}: type-scale role '{arg}' not in "
                        f"{', '.join(TYPESCALE_ROLES)}"
                    )
                try:
                    pt = float(value)
                except ValueError:
                    raise BrandKitError(f"brand.md:{line_no}: type-scale '{arg}' value {value!r} is not a number")
                if pt <= 0:
                    raise BrandKitError(f"brand.md:{line_no}: type-scale '{arg}' value {pt} must be positive")
                type_scale[arg] = pt
            continue

        raise BrandKitError(f"brand.md:{line_no}: line outside any recognised section: {stripped!r}")

    if "slug" not in top:
        raise BrandKitError("brand.md: missing required 'slug: <value>' line")
    slug = top["slug"]
    if not SLUG_RE.match(slug):
        raise BrandKitError(f"brand.md: invalid slug {slug!r} — must match ^[a-z0-9-]+$")

    missing_palette = [r for r in PALETTE_ROLES if r not in palette]
    if missing_palette:
        raise BrandKitError(f"brand.md: ## Palette is missing role(s): {', '.join(missing_palette)}")

    if "heading" not in typefaces or "body" not in typefaces:
        raise BrandKitError("brand.md: ## Typefaces must give both 'heading' and 'body'")

    if not doctypes:
        raise BrandKitError("brand.md: ## Doctypes must list at least one doctype")

    for doctype in page_format_overrides:
        if doctype not in doctypes:
            raise BrandKitError(
                f"brand.md: page-format override given for '{doctype}', which is not in ## Doctypes"
            )

    if "print" in scale_choices and type_scale:
        raise BrandKitError(
            "brand.md: '## Type scales' has a print line AND '## Document defaults' has "
            "type-scale lines -- both would emit '<slug>-print'; use one or the other"
        )

    return {
        "slug": slug,
        "logo": top.get("logo"),
        "palette": palette,
        "typefaces": typefaces,
        "doctypes": doctypes,
        "voice": "\n".join(voice_lines).strip(),
        "page_format_overrides": page_format_overrides,
        "type_scale": type_scale,
        "designs": designs,
        "scale_choices": scale_choices,
    }


# ---------------------------------------------------------------------------
# row derivation
# ---------------------------------------------------------------------------

def _title_words(slug: str) -> str:
    return " ".join(w.capitalize() for w in slug.split("-"))


#: Safe-stack fallbacks that are serif faces; any other library fallback is sans.
SERIF_FALLBACKS = {"georgia", "times new roman", "cambria", "garamond", "palatino linotype",
                   "book antiqua", "constantia", "courier new"}
DEFAULT_FALLBACK = {"sans": "Arial", "serif": "Georgia"}


def library_family_fallbacks(library_typefaces: list[dict]) -> dict[str, str]:
    """{family (lower): safe-stack fallback} read off data/base/typefaces.csv: a Heading Family
    maps to its Safe Stack Fallback, a Body Family to its Safe Stack Body Fallback (else the
    heading one). This is how families like 'Libre Franklin' are known without a hard-coded list."""
    out: dict[str, str] = {}
    for r in library_typefaces:
        head_fb = r.get("Safe Stack Fallback", "").strip()
        body_fb = r.get("Safe Stack Body Fallback", "").strip() or head_fb
        for fam, fb in ((r.get("Heading Family", ""), head_fb), (r.get("Body Family", ""), body_fb)):
            if fam.strip() and fb:
                out.setdefault(fam.strip().lower(), fb)
    return out


def _classify_family(name: str, library_fallbacks: dict[str, str] | None = None) -> str | None:
    key = name.strip().lower()
    if key in SANS_FAMILIES:
        return "sans"
    if key in SERIF_FAMILIES:
        return "serif"
    fb = (library_fallbacks or {}).get(key)
    if fb:
        return "serif" if fb.strip().lower() in SERIF_FALLBACKS else "sans"
    return None


def derive_palette_row(spec: dict) -> tuple[dict, list[tuple[str, str, str, float]]]:
    """Build the palettes.csv row and the list of (label, fg, bg, ratio)
    contrast pairs actually checked by the schema's derived rules.

    On-colours: white/black only, via lib.color.on_color — never typed.
    Rule Hair/Strong/Brand: not collected from the user; deterministically
    set to Muted/Foreground/Primary respectively (documented assumption,
    see module docstring — this differs from a hand-picked hairline colour
    like ENS's real #B9C4BC, which this format has no field for).
    Text-Safe / Fill-Only / Category Marker roles: computed from
    contrast_ratio(role, Background) >= 4.5 among {primary, secondary,
    accent} only; Category Marker Roles is the intersection of Text-Safe
    with {secondary, accent}.
    """
    p = spec["palette"]
    on = {role: color.on_color(p[role]) for role in ("primary", "secondary", "accent", "muted")}

    pairs = [
        ("On Primary/Primary", on["primary"], p["primary"]),
        ("On Secondary/Secondary", on["secondary"], p["secondary"]),
        ("On Accent/Accent", on["accent"], p["accent"]),
        ("Foreground/Background", p["foreground"], p["background"]),
        ("On Muted/Muted", on["muted"], p["muted"]),
    ]
    contrast_report = [(label, fg, bg, color.contrast_ratio(fg, bg)) for label, fg, bg in pairs]

    text_safe = [r for r in ("primary", "secondary", "accent") if color.contrast_ratio(p[r], p["background"]) >= 4.5]
    fill_only = [r for r in ("primary", "secondary", "accent") if r not in text_safe]
    category_marker = [r for r in text_safe if r in ("secondary", "accent")]

    slug = spec["slug"]
    row = {
        "palette_key": f"{slug}-core",
        "Display Name": f"{_title_words(slug)} Core",
        "Keywords": f"{slug}, {_title_words(slug).lower()}, brand palette",
        "Brand Scope": slug,
        "Primary": p["primary"], "On Primary": on["primary"],
        "Secondary": p["secondary"], "On Secondary": on["secondary"],
        "Accent": p["accent"], "On Accent": on["accent"],
        "Background": p["background"], "Foreground": p["foreground"],
        "Muted": p["muted"], "On Muted": on["muted"],
        "Rule Hair": p["muted"], "Rule Strong": p["foreground"], "Rule Brand": p["primary"],
        "Text-Safe Roles": ";".join(text_safe),
        "Fill-Only Roles": ";".join(fill_only),
        "Category Marker Roles": ";".join(category_marker),
    }
    return row, contrast_report


def derive_typefaces_row(spec: dict, font_substitutes: list[dict],
                         library_typefaces: list[dict] | None = None) -> tuple[dict, list[str]]:
    """Build the typefaces.csv row. Returns (row, warnings).

    Heading and body keep SEPARATE safe-stack fallbacks. If (Heading, Body) is a row of
    data/base/typefaces.csv, its Safe Stack Fallback / Safe Stack Body Fallback / Safe Stack
    Availability / Embedding Licence / Has Tabular Figures are copied. Otherwise each family's
    fallback is: a font-substitutes row, else the fallback the library gives that family in some
    other pairing, else its category default (serif -> Georgia, sans -> Arial)."""
    library_typefaces = library_typefaces or []
    library_fb = library_family_fallbacks(library_typefaces)
    slug = spec["slug"]
    tf = spec["typefaces"]
    heading, body, mono = tf["heading"], tf["body"], tf.get("mono", "")
    warnings = []

    families = [f for f in (heading, body, mono) if f]
    family_count = len(set(f.lower() for f in families))

    cats = {f: _classify_family(f, library_fb) for f in families}
    for f, c in cats.items():
        if c is None:
            warnings.append(
                f"typeface family '{f}' is not in this script's small sans/serif "
                "classification list — defaulted to 'sans'; verify Category Contrast by hand"
            )
    resolved_cats = {f: (c or "sans") for f, c in cats.items()}

    first_words = {f.split()[0].lower() for f in families if f}
    if len(first_words) == 1 and len(families) > 1:
        category_contrast = "superfamily"
    else:
        distinct = set(resolved_cats.get(f) for f in (heading, body) if f)
        if distinct == {"sans"}:
            category_contrast = "sans-sans"
        elif distinct == {"serif"}:
            category_contrast = "serif-serif"
        else:
            category_contrast = "serif-sans"

    def _substitute_for(family: str) -> str | None:
        for row in font_substitutes:
            if row.get("proprietary_family", "").strip().lower() == family.strip().lower():
                sub = row.get("Substitute Family", "").strip()
                if sub:
                    return sub
        return None

    lib_row = next((r for r in library_typefaces
                    if r.get("Heading Family", "").strip().lower() == heading.strip().lower()
                    and r.get("Body Family", "").strip().lower() == body.strip().lower()), None)

    def _fallback_for(family: str) -> str:
        return (_substitute_for(family) or library_fb.get(family.strip().lower())
                or DEFAULT_FALLBACK[resolved_cats.get(family) or "sans"])

    if lib_row:
        fallback = lib_row.get("Safe Stack Fallback", "") or _fallback_for(heading)
        body_fallback = lib_row.get("Safe Stack Body Fallback", "")
    else:
        fallback = _fallback_for(heading)
        body_fallback = _fallback_for(body)
        if body_fallback == fallback:
            body_fallback = ""

    key_bits = "-".join(re.sub(r"[^a-z0-9]+", "", f.lower()) for f in (heading, body) if f)
    typeface_key = f"{slug}-{key_bits}"

    row = {
        "typeface_key": typeface_key,
        "Display Name": f"{_title_words(slug)} {heading} + {body}",
        "Keywords": f"{slug}, {heading.lower()}, {body.lower()}",
        "Best For": f"{_title_words(slug)} documents",
        "Brand Scope": slug,
        "Heading Family": heading,
        "Body Family": body,
        "Mono Family": mono,
        "Category Contrast": category_contrast,
        "Family Count": str(family_count),
        "Safe Stack Fallback": fallback,
        "Safe Stack Body Fallback": body_fallback,
        "Safe Stack Availability": (lib_row or {}).get("Safe Stack Availability") or "os-bundled",
        "Embedding Licence": (lib_row or {}).get("Embedding Licence") or "unknown",
        "Has Tabular Figures": (lib_row or {}).get("Has Tabular Figures") or "unknown",
        # Only reference the print scale this script would itself emit as
        # data/type-scales.csv -- pointing at "<slug>-print" when no
        # ## Document defaults type-scale line was given leaves the FK
        # dangling, since no type-scales.csv row would exist to resolve it.
        "Scale Key": f"{slug}-print" if spec["type_scale"] else "",
    }
    return row, warnings


def doctype_medium(doctype_row: dict) -> str:
    """The type-scale Medium a derived doctypes row is set in."""
    if "projection" in doctype_row["Constraint Set Keys"].split(";"):
        return "projection"
    targets = [t for t in doctype_row["Render Target Keys"].split(";") if t]
    if targets and all(t.startswith(("png", "html")) for t in targets):
        return "screen"
    return "print"


def derive_medium_typeface_rows(spec: dict, typeface_row: dict) -> list[dict]:
    """One typeface row per ## Type scales medium (see module docstring)."""
    slug = spec["slug"]
    rows = []
    for medium in spec["scale_choices"]:
        row = dict(typeface_row)
        row["typeface_key"] = f"{typeface_row['typeface_key']}-{medium}"
        row["Scale Key"] = f"{slug}-{medium}"
        rows.append(row)
    return rows


def derive_library_typescale_rows(spec: dict, base_scale_rows: list[dict]) -> list[dict]:
    """Brand rows `<slug>-<medium>` copying each chosen library scale."""
    rows = []
    for medium, src in spec["scale_choices"].items():
        key = f"{spec['slug']}-{medium}"
        for r in base_scale_rows:
            if r["scale_key"] == src:
                rows.append({
                    "scale_row_key": f"{key}-{medium}-{r['Role']}", "scale_key": key,
                    "Medium": medium, "Role": r["Role"],
                    "Size pt": r["Size pt"], "Leading Ratio": r["Leading Ratio"],
                })
    return rows


def _generic_catalog_entry(base_row: dict) -> dict:
    """A DOCTYPE_CATALOG-shaped entry from a data/base/doctypes.csv row."""
    split = lambda v: tuple(x for x in v.split(";") if x)  # noqa: E731
    return dict(
        display=base_row["Display Name"], artifact_class=base_row["Artifact Class"],
        render_targets=split(base_row["Render Target Keys"]),
        page_format_hint=base_row["Page Format Key"] or None,
        constraint_hint=split(base_row["Constraint Set Keys"]),
    )


def derive_doctype_rows(spec: dict, base_doctypes: dict[str, dict] | None = None) -> list[dict]:
    if base_doctypes is None:
        base_doctypes = load_base_doctypes()
    slug = spec["slug"]
    rows = []
    for doctype in spec["doctypes"]:
        base_row = None if doctype in DOCTYPE_CATALOG else base_doctypes[doctype]
        cat = DOCTYPE_CATALOG[doctype] if base_row is None else _generic_catalog_entry(base_row)
        page_format = spec["page_format_overrides"].get(doctype, cat["page_format_hint"] or "")
        rows.append({
            "doc_key": f"{slug}-{doctype}",
            "Display Name": f"{_title_words(slug)} -- {cat['display']}",
            # dict.fromkeys de-duplicates while keeping first-seen order: a
            # single-word doctype ("social", "slides", "formulaire") makes
            # `doctype.replace("-", " ")` identical to `doctype`, and a repeated
            # keyword doubles that term's frequency in the search index.
            # doctypes."Keywords" is a declared distinct_token_columns entry, so
            # the emitted row would otherwise fail the gate it is checked against.
            "Keywords": ", ".join(dict.fromkeys(
                [doctype, doctype.replace("-", " "), slug])),
            "Artifact Class": cat["artifact_class"],
            "Brand Scope": slug,
            "Reasoning Key": (base_row["Reasoning Key"] if base_row
                              else REASONING_KEY_HINT.get(doctype, "")),
            "Page Format Key": page_format,
            "Render Target Keys": ";".join(cat["render_targets"]),
            "Constraint Set Keys": ";".join(cat["constraint_hint"]),
            "Structure Key": (base_row["Structure Key"] if base_row
                              else STRUCTURE_KEY_HINT.get(doctype, "")),
            "Region Key": base_row["Region Key"] if base_row else "",
            "Family": base_row["Family"] if base_row else FAMILY_HINT[doctype],
            # research/64 D-E (A7): this generic brand-kit builder parses no
            # language signal at all out of a brand .md today -- "en" is the
            # documented fallback for a doctype whose own Display Name carries
            # no market/language signal (rationale/doctypes.md), and adding
            # brand-markdown language parsing is out of this fix's scope.
            "Default Language": base_row["Default Language"] if base_row else "en",
        })
    return rows


def derive_reasoning_rows(spec: dict, palette_key: str, typeface_key: str,
                          skill_dir: Path) -> list[dict]:
    """One doc-reasoning row `<slug>-<family>` per ## Designs line: a copy of
    the design's base doc-reasoning row with the brand's own Palette/Typeface."""
    if not spec["designs"]:
        return []
    _, base_designs = load_designs_context(skill_dir)
    with (skill_dir / "data" / "base" / "doc-reasoning.csv").open(encoding="utf-8", newline="") as f:
        base = {r["doc_category"]: r for r in csv.DictReader(f)}
    rows = []
    for family, design_key in spec["designs"].items():
        rk = base_designs[design_key]["Reasoning Key"]
        if rk not in base:
            raise BrandKitError(
                f"design '{design_key}' has Reasoning Key '{rk}' which is not a row "
                "of data/base/doc-reasoning.csv"
            )
        row = dict(base[rk])
        row.update({"doc_category": f"{spec['slug']}-{family}",
                    "Palette Key": palette_key, "Typeface Key": typeface_key,
                    "Design Key": design_key,
                    # the copied bias terms describe the design's generic palette/type,
                    # not the brand's (R2 F3) -- blank them; Style Bias Terms stay
                    "Palette Bias Terms": "", "Typeface Bias Terms": ""})
        rows.append(row)
    return rows


def derive_typescale_rows(spec: dict) -> list[dict]:
    if not spec["type_scale"]:
        return []
    slug = spec["slug"]
    scale_key = f"{slug}-print"
    medium = "print"
    rows = []
    for role, pt in spec["type_scale"].items():
        rows.append({
            "scale_row_key": f"{scale_key}-{medium}-{role}",
            "scale_key": scale_key,
            "Medium": medium,
            "Role": role,
            "Size pt": f"{pt:g}",
            "Leading Ratio": f"{TYPESCALE_LEADING[role]:g}",
        })
    return rows


# ---------------------------------------------------------------------------
# CSV writing
# ---------------------------------------------------------------------------

def rows_to_csv(columns: list[str], rows: list[dict]) -> bytes:
    buf = io.StringIO(newline="")
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerow(columns)
    for row in rows:
        writer.writerow([row.get(c, "") for c in columns])
    return buf.getvalue().encode("utf-8")


# ---------------------------------------------------------------------------
# skill directory / manifest / self-check
# ---------------------------------------------------------------------------

def find_skill_dir() -> Path | None:
    override = os.environ.get("DDI_SKILL_DIR")
    if override:
        candidate = Path(override)
        if (candidate / "data" / "schema-manifest.json").is_file():
            return candidate
        return None
    candidate = Path(__file__).resolve().parent.parent
    if (candidate / "data" / "schema-manifest.json").is_file():
        return candidate
    return None


def outputs_dir() -> Path:
    return Path(os.environ.get("DDI_OUTPUTS_DIR", DEFAULT_OUTPUTS_DIR))


def uploads_dir() -> Path:
    return Path(os.environ.get("DDI_UPLOADS_DIR", DEFAULT_UPLOADS_DIR))


def load_library_typefaces(skill_dir: Path) -> list[dict]:
    path = skill_dir / "data" / "base" / "typefaces.csv"
    if not path.is_file():
        return []
    with path.open(encoding="utf-8", newline="") as f:
        return [r for r in csv.DictReader(f) if r.get("Brand Scope", "generic") == "generic"]


def load_font_substitutes(skill_dir: Path) -> list[dict]:
    path = skill_dir / "data" / "base" / "font-substitutes.csv"
    if not path.is_file():
        return []
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def run_self_check(skill_dir: Path, manifest: dict, slug: str,
                    csv_files: dict[str, bytes], brand_md_text: str):
    """Copy data/base + schema-manifest.json into a temp dir, write the
    generated CSVs under data/brand/<slug>/, run validate_data.validate()
    over the WHOLE merged dataset (that's the only function CI and
    merge_brand_kit.py have), and classify problems into (expected, real)
    by SCOPE, not by which table they name.

    validate_data.validate() has no way to check "just this kit" -- it
    always re-validates every base table too, so a base-only defect (a
    pre-existing data/base problem this script's brand.md had nothing to do
    with, e.g. a Page Format Key typo authored months ago) shows up in the
    same `problems` list as a defect in the rows this run just generated.
    Blocking on the former means make_brand_kit.py refuses every single
    brand kit the moment ANY base table has an unrelated problem -- which
    defeats the point of a per-kit self-check. So "real" (blocking) is
    scoped to problems whose `file:` prefix names a file THIS RUN wrote
    under data/brand/<slug>/ -- the kit's own rows. Everything else
    (base-only problems, including "table declared but file does not
    exist" for a still-unauthored table) is printed for visibility but
    never blocks: it is not this kit's defect to fix.

    Returns (ok_to_emit, all_problem_lines, expected_lines, real_lines, summary).
    """
    with tempfile.TemporaryDirectory(prefix="ddi-selfcheck-") as tmp:
        tmp_data = Path(tmp) / "data"
        shutil.copytree(skill_dir / "data" / "base", tmp_data / "base")
        shutil.copy2(skill_dir / "data" / "schema-manifest.json", tmp_data / "schema-manifest.json")

        brand_dir = tmp_data / "brand" / slug
        brand_dir.mkdir(parents=True)
        for filename, content in csv_files.items():
            (brand_dir / filename).write_bytes(content)
        (brand_dir / "brand.md").write_text(brand_md_text, encoding="utf-8")

        ok, problems, summary = validate_data.validate(tmp_data)

        brand_dir_prefix = str(brand_dir) + os.sep

        real, expected = [], []
        for line in problems:
            if line.startswith(brand_dir_prefix):
                real.append(line)
            else:
                expected.append(line)

        return (not real), problems, expected, real, summary


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def _resolve_output_path(explicit: str | None, outputs: Path, uploads: Path, default_name: str) -> Path:
    if explicit:
        out = Path(explicit)
        try:
            out.resolve().relative_to(uploads.resolve())
        except ValueError:
            pass
        else:
            raise BrandKitError(f"refusing to write into the read-only uploads directory: {out}")
        return out
    outputs.mkdir(parents=True, exist_ok=True)
    return outputs / default_name


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("brand_md", help="path to the brand.md file to generate a kit from")
    parser.add_argument("-o", "--output", default=None, help="output .zip path (default: outputs dir, <slug>-brand-kit.zip)")
    parser.add_argument("--dry-run", action="store_true", help="parse, derive, self-check and print; write nothing")
    args = parser.parse_args(argv)

    try:
        brand_md_path = Path(args.brand_md)
        if not brand_md_path.is_file():
            raise BrandKitError(f"brand.md not found: {brand_md_path}")
        brand_md_text = brand_md_path.read_text(encoding="utf-8")

        skill_dir = find_skill_dir()
        if skill_dir is None:
            raise BrandKitError(
                "could not locate the skill directory (no data/schema-manifest.json found); "
                "set DDI_SKILL_DIR to override"
            )
        base_doctypes = load_base_doctypes(skill_dir)
        spec = parse_brand_md(brand_md_text, base_doctypes, load_designs_context(skill_dir),
                              load_scales_context(skill_dir))
        slug = spec["slug"]
        manifest = json.loads((skill_dir / "data" / "schema-manifest.json").read_text(encoding="utf-8"))
        font_substitutes = load_font_substitutes(skill_dir)

        logo_bytes = None
        logo_arcname = None
        if spec["logo"]:
            logo_path = Path(spec["logo"])
            if not logo_path.is_absolute():
                logo_path = brand_md_path.parent / logo_path
            if not logo_path.is_file():
                raise BrandKitError(f"brand.md: logo path does not exist: {logo_path}")
            logo_bytes = logo_path.read_bytes()
            logo_arcname = f"assets/{logo_path.name}"

        palette_row, contrast_report = derive_palette_row(spec)
        typefaces_row, font_warnings = derive_typefaces_row(spec, font_substitutes, load_library_typefaces(skill_dir))
        doctype_rows = derive_doctype_rows(spec, base_doctypes)
        typescale_rows = derive_typescale_rows(spec)
        typeface_rows = [typefaces_row]
        family_typeface = {}
        if spec["scale_choices"]:
            typeface_rows = derive_medium_typeface_rows(spec, typefaces_row)
            with (skill_dir / "data" / "base" / "type-scales.csv").open(encoding="utf-8", newline="") as f:
                typescale_rows = derive_library_typescale_rows(spec, list(csv.DictReader(f)))
            by_medium = {r["Scale Key"]: r["typeface_key"] for r in typeface_rows}
            for r in doctype_rows:
                key = f"{slug}-{doctype_medium(r)}"
                family_typeface.setdefault(r["Family"], by_medium.get(key, typeface_rows[0]["typeface_key"]))
        reasoning_rows = derive_reasoning_rows(
            spec, palette_row["palette_key"], typefaces_row["typeface_key"], skill_dir)
        doctype_families = {r["Family"] for r in doctype_rows}
        for fam in spec["designs"]:
            if fam not in doctype_families:
                print(f"WARNING: ## Designs line for family '{fam}' but no doctype of that "
                      f"family is listed in ## Doctypes -- {slug}-{fam} will be an orphan "
                      "doc-reasoning row", file=sys.stderr)
        for rr in reasoning_rows:
            fam = rr["doc_category"][len(slug) + 1:]
            if fam in family_typeface:
                rr["Typeface Key"] = family_typeface[fam]
        for r in doctype_rows:
            fam_key = f"{slug}-{r['Family']}"
            if any(rr["doc_category"] == fam_key for rr in reasoning_rows):
                r["Reasoning Key"] = fam_key

        tables = manifest["tables"]
        csv_files = {
            "palettes.csv": rows_to_csv(tables["palettes"]["columns"], [palette_row]),
            "typefaces.csv": rows_to_csv(tables["typefaces"]["columns"], typeface_rows),
            "doctypes.csv": rows_to_csv(tables["doctypes"]["columns"], doctype_rows),
        }
        if reasoning_rows:
            csv_files["doc-reasoning.csv"] = rows_to_csv(tables["doc-reasoning"]["columns"], reasoning_rows)
        if typescale_rows:
            csv_files["type-scales.csv"] = rows_to_csv(tables["type-scales"]["columns"], typescale_rows)

        print(f"-- {slug}: contrast pairs (lib/color.contrast_ratio) --")
        for label, fg, bg, ratio in contrast_report:
            verdict = "OK" if ratio >= 4.5 - 1e-9 else "FAIL"
            print(f"  {label}: {fg} on {bg} = {ratio:.2f}:1 [{verdict}, threshold 4.5:1]")

        for w in font_warnings:
            print(f"WARNING: {w}")

        for doctype in spec["doctypes"]:
            row = next(r for r in doctype_rows if r["doc_key"] == f"{slug}-{doctype}")
            cat = {"display": row["Display Name"].split(" -- ", 1)[-1]}
            if not row["Page Format Key"]:
                print(
                    f"NOTE: {doctype}: no Page Format Key (none given; no generic "
                    f"'{cat['display']}'-shaped format in data/base/page-formats.csv yet)"
                )
            if not row["Reasoning Key"]:
                print(
                    f"NOTE: {doctype}: no Reasoning Key (no generic doc_category in "
                    f"data/base/doc-reasoning.csv fits '{cat['display']}' yet)"
                )
            if not row["Structure Key"]:
                print(
                    f"NOTE: {doctype}: no Structure Key (no generic structure_key in "
                    f"data/base/structures.csv fits '{cat['display']}' yet)"
                )

        ok_to_emit, all_problems, expected, real, summary = run_self_check(
            skill_dir, manifest, slug, csv_files, brand_md_text
        )

        print(f"\n-- gate output against {skill_dir / 'data'} (full, includes known gaps) --")
        if all_problems:
            for line in all_problems:
                print(line)
        else:
            print(summary)

        if expected:
            print(f"\n-- {len(expected)} problem(s) outside this kit's own rows, not blocking --")
            for line in expected:
                print(line)

        if not ok_to_emit:
            print(f"\n-- {len(real)} REAL problem(s), refusing to emit --")
            for line in real:
                print(line)
            return 1

        if args.dry_run:
            print(
                f"\nDRY-RUN OK: would generate {slug}-brand-kit.zip "
                f"(palettes=1 typefaces={len(typeface_rows)} doctypes={len(doctype_rows)} type-scales={len(typescale_rows)})"
            )
            return 0

        default_name = f"{slug}-brand-kit.zip"
        out_path = _resolve_output_path(args.output, outputs_dir(), uploads_dir(), default_name)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("brand.md", brand_md_text)
            for filename, content in csv_files.items():
                zf.writestr(f"data/{filename}", content)
            if logo_bytes is not None:
                zf.writestr(logo_arcname, logo_bytes)

        print(
            f"\nOK: {out_path} "
            f"(palettes=1 typefaces={len(typeface_rows)} doctypes={len(doctype_rows)} type-scales={len(typescale_rows)})"
        )
        return 0

    except BrandKitError as exc:
        print(f"ERROR: {exc}")
        return 1
    except Exception as exc:  # last-resort guard so a bug never dumps a traceback into context
        print(f"ERROR: unexpected failure - {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
