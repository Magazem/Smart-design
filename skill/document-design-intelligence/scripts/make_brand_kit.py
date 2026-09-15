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
One bare doctype short-name per line. v1 supports a fixed catalog (see
DOCTYPE_CATALOG below): `note-interne`, `formulaire`, `social`, `slides`.
Any other name is a hard failure — this script does not guess an Artifact
Class, Render Target, or Reasoning Key for a doctype it doesn't know:
    note-interne
    formulaire
    social
    slides

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
ALLOWED_SECTIONS = {"Palette", "Typefaces", "Doctypes", "Voice", "Document defaults"}
TYPESCALE_ROLES = ("label", "caption", "body", "body-dense", "lead", "h3", "h2", "h1")

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

def parse_brand_md(text: str) -> dict:
    """Parse brand.md into a structured dict. Raises BrandKitError with a
    line number on the first problem found."""
    lines = text.splitlines()
    top = {}
    palette = {}
    typefaces = {}
    doctypes = []
    voice_lines = []
    page_format_overrides = {}
    type_scale = {}

    section = None  # None, "Palette", "Typefaces", "Doctypes", "Voice", "Document defaults"
    seen_h1 = False

    for line_no, raw in enumerate(lines, start=1):
        stripped = raw.strip()
        if not stripped:
            continue

        section_match = SECTION_RE.match(stripped)
        if section_match:
            name = section_match.group(1)
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
            if name not in DOCTYPE_CATALOG:
                raise BrandKitError(
                    f"brand.md:{line_no}: unknown doctype '{name}' "
                    f"(supported: {', '.join(sorted(DOCTYPE_CATALOG))})"
                )
            if name in doctypes:
                raise BrandKitError(f"brand.md:{line_no}: doctype '{name}' listed twice")
            doctypes.append(name)
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
                if arg not in DOCTYPE_CATALOG:
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

    return {
        "slug": slug,
        "logo": top.get("logo"),
        "palette": palette,
        "typefaces": typefaces,
        "doctypes": doctypes,
        "voice": "\n".join(voice_lines).strip(),
        "page_format_overrides": page_format_overrides,
        "type_scale": type_scale,
    }


# ---------------------------------------------------------------------------
# row derivation
# ---------------------------------------------------------------------------

def _title_words(slug: str) -> str:
    return " ".join(w.capitalize() for w in slug.split("-"))


def _classify_family(name: str) -> str | None:
    key = name.strip().lower()
    if key in SANS_FAMILIES:
        return "sans"
    if key in SERIF_FAMILIES:
        return "serif"
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


def derive_typefaces_row(spec: dict, font_substitutes: list[dict]) -> tuple[dict, list[str]]:
    """Build the typefaces.csv row. Returns (row, warnings)."""
    slug = spec["slug"]
    tf = spec["typefaces"]
    heading, body, mono = tf["heading"], tf["body"], tf.get("mono", "")
    warnings = []

    families = [f for f in (heading, body, mono) if f]
    family_count = len(set(f.lower() for f in families))

    cats = {f: _classify_family(f) for f in families}
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

    fallback = _substitute_for(heading) or _substitute_for(body) or "Arial"

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
        "Safe Stack Availability": "os-bundled",
        "Embedding Licence": "unknown",
        "Has Tabular Figures": "unknown",
        # Only reference the print scale this script would itself emit as
        # data/type-scales.csv -- pointing at "<slug>-print" when no
        # ## Document defaults type-scale line was given leaves the FK
        # dangling, since no type-scales.csv row would exist to resolve it.
        "Scale Key": f"{slug}-print" if spec["type_scale"] else "",
    }
    return row, warnings


def derive_doctype_rows(spec: dict) -> list[dict]:
    slug = spec["slug"]
    rows = []
    for doctype in spec["doctypes"]:
        cat = DOCTYPE_CATALOG[doctype]
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
            "Reasoning Key": REASONING_KEY_HINT.get(doctype, ""),
            "Page Format Key": page_format,
            "Render Target Keys": ";".join(cat["render_targets"]),
            "Constraint Set Keys": ";".join(cat["constraint_hint"]),
            "Structure Key": STRUCTURE_KEY_HINT.get(doctype, ""),
            "Region Key": "",
            # research/64 D-E (A7): this generic brand-kit builder parses no
            # language signal at all out of a brand .md today -- "en" is the
            # documented fallback for a doctype whose own Display Name carries
            # no market/language signal (rationale/doctypes.md), and adding
            # brand-markdown language parsing is out of this fix's scope.
            "Default Language": "en",
        })
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

        spec = parse_brand_md(brand_md_text)
        slug = spec["slug"]

        skill_dir = find_skill_dir()
        if skill_dir is None:
            raise BrandKitError(
                "could not locate the skill directory (no data/schema-manifest.json found); "
                "set DDI_SKILL_DIR to override"
            )
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
        typefaces_row, font_warnings = derive_typefaces_row(spec, font_substitutes)
        doctype_rows = derive_doctype_rows(spec)
        typescale_rows = derive_typescale_rows(spec)

        tables = manifest["tables"]
        csv_files = {
            "palettes.csv": rows_to_csv(tables["palettes"]["columns"], [palette_row]),
            "typefaces.csv": rows_to_csv(tables["typefaces"]["columns"], [typefaces_row]),
            "doctypes.csv": rows_to_csv(tables["doctypes"]["columns"], doctype_rows),
        }
        if typescale_rows:
            csv_files["type-scales.csv"] = rows_to_csv(tables["type-scales"]["columns"], typescale_rows)

        print(f"-- {slug}: contrast pairs (lib/color.contrast_ratio) --")
        for label, fg, bg, ratio in contrast_report:
            verdict = "OK" if ratio >= 4.5 - 1e-9 else "FAIL"
            print(f"  {label}: {fg} on {bg} = {ratio:.2f}:1 [{verdict}, threshold 4.5:1]")

        for w in font_warnings:
            print(f"WARNING: {w}")

        for doctype in spec["doctypes"]:
            cat = DOCTYPE_CATALOG[doctype]
            row = next(r for r in doctype_rows if r["doc_key"] == f"{slug}-{doctype}")
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
                f"(palettes=1 typefaces=1 doctypes={len(doctype_rows)} type-scales={len(typescale_rows)})"
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
            f"(palettes=1 typefaces=1 doctypes={len(doctype_rows)} type-scales={len(typescale_rows)})"
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
