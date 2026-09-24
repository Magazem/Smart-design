#!/usr/bin/env python3
"""Generate the cv F.c fill output files from the archetype/fill decisions recorded in
research/designs-evidence/cv-fill.md. Run once; the four output CSVs are then hand-reviewed
and committed. Re-run is idempotent (overwrites with the same content)."""
import csv
import pathlib

ROOT = pathlib.Path(r"C:\Users\yazan\Documents\Ai_plugin\Smart-design")
RES = ROOT / "research"
LIB = RES / "library"
DESIGNS = RES / "designs"
PROV = RES / "provenance"

GH_URL = "https://api.github.com/search/repositories?q=resume+template&sort=stars&order=desc&per_page=100"
NPM_URL = "https://registry.npmjs.org/-/v1/search?text=jsonresume-theme&size=250"
DATE = "2026-09-23"

# ---------------------------------------------------------------- doc-styles/cv.csv
doc_styles_cols = ["style_key", "Display Name", "Keywords", "Best For", "Not For",
                    "Brand Scope", "Rule Hair pt", "Rule Strong pt", "Rule Brand pt",
                    "Corner Radius mm", "Table Rules", "Table Fills", "Emphasis Mechanism",
                    "Field Style", "Checklist"]

doc_styles_rows = [
    dict(zip(doc_styles_cols, [
        "cv-serif-plain-centered", "CV, serif centered",
        "cv, resume, serif, centered name, restrained, single column, ats-safe",
        "Single-column CVs with a centred serif name heading and no colour-coded meaning",
        "DACH tabular CVs, Europass multilingual CVs, marketing collateral",
        "generic", "0.5", "1", "0", "0", "hairline", "none", "weight", "none",
        "Keep single column;Centre the name and contact line on the page;"
        "Emphasize by weight and size, not colour;Omit photo;"
        "Reserve hairline rules for section dividers only",
    ])),
    dict(zip(doc_styles_cols, [
        "cv-sans-mono-split", "CV, sans split header",
        "cv, resume, sans, split header, name left contact right, single column, ats-safe",
        "Single-column CVs with the name flush left and a contact block flush right on the "
        "same header row, monochrome ink",
        "DACH tabular CVs, Europass multilingual CVs, marketing collateral",
        "generic", "0.5", "1", "0", "0", "hairline", "none", "weight", "none",
        "Keep single column;Set the name flush left and the contact block flush right on the "
        "same header row;Photo permitted as a modest avatar, not a hero image;"
        "Emphasize by weight and size, not colour;Reserve hairline rules for section dividers only",
    ])),
    dict(zip(doc_styles_cols, [
        "cv-sans-accent-plain-centered", "CV, sans accent centered",
        "cv, resume, sans, one accent, centered name, single column, ats-safe",
        "Single-column CVs with a centred sans name heading and one restrained accent colour",
        "DACH tabular CVs, multi-accent marketing collateral",
        "generic", "0.5", "1", "0", "0", "hairline", "none", "weight", "none",
        "Keep single column;Centre the name and contact line on the page;"
        "Reserve the accent colour for the name/header only, never small print;Omit photo;"
        "Emphasize by weight and size, not colour fills",
    ])),
]

# ------------------------------------------------------------- doc-reasoning/cv.csv
dr_cols = ["doc_category", "Style Key", "Palette Key", "Typeface Key", "Style Bias Terms",
           "Palette Bias Terms", "Typeface Bias Terms", "Doc Conditions",
           "Anti-Pattern Tokens", "Severity", "Design Key"]

DEFAULT_STYLE_BIAS = "restrained, single column, no color blocks, ats-safe structure"
DEFAULT_PALETTE_BIAS = "monochrome, ink on white, no color-coded meaning"
DEFAULT_TYPEFACE_BIAS = "safe stack, ubiquitous, no embedding required"
DEFAULT_COND = "if_ats_target=constraint:ats-strict"
DEFAULT_SEVERITY = "fail"
DEFAULT_ANTI = "multi-column;text-box;icon-only-skill-bar;photo;graphic-timeline;emoji"
ANTI_NO_PHOTO = "multi-column;text-box;icon-only-skill-bar;graphic-timeline;emoji"

dr_defs = [
    ("cv-serif-plain-centered", "cv-serif-plain-centered", "lib-carbon-mono", "safe-serif-georgia", DEFAULT_ANTI),
    ("cv-sans-accent-ruled", "cv-europass", "lib-atlassian-ink", "lib-roboto", DEFAULT_ANTI),
    ("cv-sans-mono-split", "cv-sans-mono-split", "lib-carbon-mono", "lib-roboto", ANTI_NO_PHOTO),
    ("cv-serif-accent-plain-left", "cv-restrained", "lib-atlassian-ink", "safe-serif-georgia", DEFAULT_ANTI),
    ("cv-sans-accent-plain-centered", "cv-sans-accent-plain-centered", "lib-atlassian-ink", "lib-roboto", DEFAULT_ANTI),
    ("cv-serif-mono-split", "cv-sans-accent-plain-centered", "lib-carbon-mono", "safe-serif-georgia", DEFAULT_ANTI),
    ("cv-sans-accent-split", "cv-sans-mono-split", "lib-atlassian-ink", "lib-roboto", ANTI_NO_PHOTO),
]

dr_rows = []
for doc_category, style_key, palette_key, typeface_key, anti in dr_defs:
    dr_rows.append(dict(zip(dr_cols, [
        doc_category, style_key, palette_key, typeface_key,
        DEFAULT_STYLE_BIAS, DEFAULT_PALETTE_BIAS, DEFAULT_TYPEFACE_BIAS,
        DEFAULT_COND, anti, DEFAULT_SEVERITY, doc_category,
    ])))

# ------------------------------------------------------------------ designs/cv.csv
d_cols = ["design_key", "Display Name", "Family", "Rank", "Reasoning Key", "Keywords",
          "Best For", "Not For", "Evidence Class", "Brand Scope"]

d_rows_defs = [
    ("cv-serif-plain-centered", "CV, serif centered", "cv", 1, "cv-serif-plain-centered",
     "cv, résumé, serif, centered name, single column, restrained, ats-safe",
     "Single-column résumés wanting a centred serif name heading with no colour-coded "
     "meaning -- the single most frequent admissible layout in the coded corpora",
     "DACH tabular CVs, Europass multilingual CVs, slide decks, marketing collateral",
     "ranked", "generic"),
    ("cv-eu-europass", "CV -- Europass-compatible", "cv", 2, "cv-eu-europass",
     "cv, europass, eu, multilingual, cross-border, single column, language grid",
     "EU cross-border or Europass-targeted CVs matching the official tool's section order "
     "and language-proficiency grid",
     "DACH tabular CVs, editorial CVs, ATS-strict US/UK CVs",
     "authority", "generic"),
    ("cv-sans-accent-ruled", "CV, sans ruled header", "cv", 3, "cv-sans-accent-ruled",
     "cv, resume, sans, one accent, ruled header, single column, ats-safe",
     "Single-column CVs with a full-width rule directly under the header block (name, "
     "title, contacts) and one restrained accent colour",
     "DACH tabular CVs, Europass multilingual CVs, marketing collateral",
     "ranked", "generic"),
    ("cv-sans-mono-split", "CV, sans split header", "cv", 4, "cv-sans-mono-split",
     "cv, resume, sans, split header, name left contact right, single column, ats-safe, "
     "photo permitted",
     "Single-column CVs with the name flush left and a contact block flush right on the "
     "same header row, monochrome ink, photo permitted as a modest avatar",
     "DACH tabular CVs, Europass multilingual CVs, marketing collateral",
     "ranked", "generic"),
    ("cv-ats-strict", "CV, restrained", "cv", 5, "cv-ats-strict",
     "cv, resume, ats-safe, restrained, single column, no colour blocks",
     "ATS-scanned CVs, cover letters bound to ats-strict, any doctype needing a parseable "
     "single-column structure",
     "slide decks, marketing collateral, colour-coded sections",
     "ranked", "generic"),
    ("cv-serif-accent-plain-left", "CV, serif accent left-aligned", "cv", 6, "cv-serif-accent-plain-left",
     "cv, resume, serif, one accent, plain left-aligned header, single column, ats-safe",
     "Single-column CVs with a left-aligned serif name heading, no header rule, and one "
     "restrained accent colour",
     "DACH tabular CVs, Europass multilingual CVs, marketing collateral",
     "ranked", "generic"),
    ("cv-sans-accent-plain-centered", "CV, sans accent centered", "cv", 7, "cv-sans-accent-plain-centered",
     "cv, resume, sans, one accent, centered name, single column, ats-safe",
     "Single-column CVs with a centred sans name heading and one restrained accent colour",
     "DACH tabular CVs, multi-accent marketing collateral",
     "ranked", "generic"),
    ("cv-serif-mono-split", "CV, serif split header", "cv", 8, "cv-serif-mono-split",
     "cv, resume, serif, split header, name left contact right, single column, ats-safe",
     "Single-column CVs with a serif name flush left and a contact block flush right on "
     "the same header row, monochrome ink",
     "DACH tabular CVs, Europass multilingual CVs, marketing collateral",
     "ranked", "generic"),
    ("cv-sans-accent-split", "CV, sans split header, accent", "cv", 9, "cv-sans-accent-split",
     "cv, resume, sans, split header, one accent, name left contact right, single column, "
     "ats-safe, photo permitted",
     "Single-column CVs with a sans name flush left and a contact block flush right on the "
     "same header row, one restrained accent colour, photo permitted as a modest avatar",
     "DACH tabular CVs, Europass multilingual CVs, marketing collateral",
     "ranked", "generic"),
    ("cv-us-uk-designed", "CV -- Harvard reverse-chronological", "cv", 10, "cv-us-uk-designed",
     "cv, résumé, harvard, us, uk, reverse-chronological, single column, restrained, "
     "serif-sans, ats-safe",
     "US/UK résumés wanting Butterick/Harvard-OCS-grounded typographic hierarchy while "
     "staying ATS-safe and single column",
     "DACH tabular CVs, Europass multilingual CVs, slide decks, marketing collateral",
     "authority", "generic"),
    ("cv-academic", "CV, academic plain", "cv", 11, "cv-academic",
     "academic cv, publication list, long-form, restrained, no page limit",
     "academic CVs, publication-heavy CVs, research profiles",
     "single-page ATS-strict CVs, marketing documents",
     "convention", "generic"),
    ("cv-dach-tabular", "CV, DACH tabellarisch", "cv", 12, "cv-dach-tabular",
     "cv, lebenslauf, dach, germany, austria, switzerland, tabular, two-column, photo, formal",
     "DACH-market Lebenslauf wanting the culturally expected tabular label/content layout "
     "with a formal headshot",
     "ATS-strict single-column CVs, Europass CVs, editorial CVs",
     "convention", "generic"),
]
d_rows = [dict(zip(d_cols, row)) for row in d_rows_defs]

# ---------------------------------------------------------------------- provenance/cv.csv
p_cols = ["prov_key", "Table", "Row Key", "Evidence Class", "Source Name", "Source URL",
          "Ranking Metric", "Rank Value", "Retrieved", "Fetch"]
p_rows = []


def add(row_key, table, evidence_class, source_name, source_url, metric, rank_value, n=None):
    n = n if n is not None else (len([r for r in p_rows if r["Row Key"] == row_key
                                       and r["Table"] == table]) + 1)
    fetch = "" if evidence_class == "convention" else "fetched"
    p_rows.append(dict(zip(p_cols, [
        "%s:%s:%d" % (table, row_key, n), table, row_key, evidence_class, source_name,
        source_url, metric, rank_value, DATE, fetch,
    ])))


# designs — share provenance per corpus (only where k>0), from cv-header-recode.md combined table
add("cv-serif-plain-centered", "designs", "ranked", "GH(resume+template) stars-desc search", GH_URL,
    "share:GH:k/40 by stars", "0.200 (8/40)")
add("cv-serif-plain-centered", "designs", "ranked", "NPM(jsonresume-theme) downloads.monthly search", NPM_URL,
    "share:NPM:k/40 by downloads.monthly", "0.050 (2/40)")

add("cv-eu-europass", "designs", "authority", "Europass -- Create your CV (official)",
    "https://europass.europa.eu/en/create-europass-cv", "authority:doc", "")
add("cv-eu-europass", "designs", "ranked", "GH(resume+template) stars-desc search", GH_URL,
    "share:GH:k/40 by stars", "0.125 (5/40)")
add("cv-eu-europass", "designs", "ranked", "NPM(jsonresume-theme) downloads.monthly search", NPM_URL,
    "share:NPM:k/40 by downloads.monthly", "0.075 (3/40)")

add("cv-sans-accent-ruled", "designs", "ranked", "NPM(jsonresume-theme) downloads.monthly search", NPM_URL,
    "share:NPM:k/40 by downloads.monthly", "0.150 (6/40)")

add("cv-sans-mono-split", "designs", "ranked", "GH(resume+template) stars-desc search", GH_URL,
    "share:GH:k/40 by stars", "0.100 (4/40)")

add("cv-ats-strict", "designs", "ranked", "GH(resume+template) stars-desc search", GH_URL,
    "share:GH:k/40 by stars", "0.025 (1/40)")
add("cv-ats-strict", "designs", "ranked", "NPM(jsonresume-theme) downloads.monthly search", NPM_URL,
    "share:NPM:k/40 by downloads.monthly", "0.075 (3/40)")

add("cv-serif-accent-plain-left", "designs", "ranked", "GH(resume+template) stars-desc search", GH_URL,
    "share:GH:k/40 by stars", "0.050 (2/40)")
add("cv-serif-accent-plain-left", "designs", "ranked", "NPM(jsonresume-theme) downloads.monthly search", NPM_URL,
    "share:NPM:k/40 by downloads.monthly", "0.025 (1/40)")

add("cv-sans-accent-plain-centered", "designs", "ranked", "GH(resume+template) stars-desc search", GH_URL,
    "share:GH:k/40 by stars", "0.050 (2/40)")

add("cv-serif-mono-split", "designs", "ranked", "GH(resume+template) stars-desc search", GH_URL,
    "share:GH:k/40 by stars", "0.050 (2/40)")

add("cv-sans-accent-split", "designs", "ranked", "GH(resume+template) stars-desc search", GH_URL,
    "share:GH:k/40 by stars", "0.050 (2/40)")

add("cv-us-uk-designed", "designs", "authority", "Butterick's Practical Typography -- Résumés",
    "https://practicaltypography.com/resumes.html", "authority:doc", "")
add("cv-us-uk-designed", "designs", "ranked", "NPM(jsonresume-theme) downloads.monthly search", NPM_URL,
    "share:NPM:k/40 by downloads.monthly", "0.050 (2/40)")

add("cv-academic", "designs", "convention", "", "", "", "")
add("cv-dach-tabular", "designs", "convention", "", "", "", "")

FILL_RULE_VALUE = "n/a (fill-rule, not a ranking)"

# new doc-styles rows — fill-rule provenance (cite the corpus that grounds the archetype)
add("cv-serif-plain-centered", "doc-styles", "ranked", "GH+NPM cv corpora, fill applied per rule", GH_URL,
    "fill-rule:research/82§8", FILL_RULE_VALUE)
add("cv-sans-mono-split", "doc-styles", "ranked", "GH cv corpus, fill applied per rule", GH_URL,
    "fill-rule:research/82§8", FILL_RULE_VALUE)
add("cv-sans-accent-plain-centered", "doc-styles", "ranked", "GH cv corpus, fill applied per rule", GH_URL,
    "fill-rule:research/82§8", FILL_RULE_VALUE)

# new doc-reasoning rows — fill-rule provenance
for doc_category, _style, _pal, _type, _anti in dr_defs:
    corpus_url = NPM_URL if doc_category == "cv-sans-accent-ruled" else GH_URL
    add(doc_category, "doc-reasoning", "ranked", "cv corpus archetype, fill applied per rule",
        corpus_url, "fill-rule:research/82§8", FILL_RULE_VALUE)

# ------------------------------------------------------------------------------- write

def write_csv(path, cols, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print("wrote", path, len(rows), "rows")


write_csv(LIB / "doc-styles" / "cv.csv", doc_styles_cols, doc_styles_rows)
write_csv(LIB / "doc-reasoning" / "cv.csv", dr_cols, dr_rows)
write_csv(DESIGNS / "cv.csv", d_cols, d_rows)
write_csv(PROV / "cv.csv", p_cols, p_rows)
