# `data/base/` — the generic library

**Only `research/load-base.py` writes this directory. Do not hand-edit these files.**

Every CSV here is generated. The loader re-headers the authored drafts in `research/`
into the exact column order `data/schema-manifest.json` declares, writing UTF-8 without
a BOM and LF newlines. It is idempotent: running it twice produces byte-identical files.
A hand-edit survives until the next run and then vanishes without a trace, which is the
worst failure mode a data file has — the change is lost *and* nobody knows when.

To change a row here, change the draft in `research/` (or the loader's transform, if the
value is one the loader computes) and re-run:

```
cd skill/document-design-intelligence && python3 ../../research/load-base.py
```

Then run the gate: `python3 scripts/validate_data.py data`.

## What belongs here: generic rows only

These files are the **generic** library — the rows that ship to everyone. The loader
skips every draft row whose `Brand Scope` is not `generic`, and reports what it skipped.
`grep ",ens," data/base/*.csv` returning nothing is the invariant.

Brand rows live in `data/brand/<brand>/` and get there by exactly one path:

```
examples/<brand>-brand.md  ->  scripts/make_brand_kit.py  ->  data/brand/<brand>/
```

`Brand Scope` is set by the **directory a row is loaded from**, not typed per row
(schema `research/09-library-schema.md` §0.3). A brand row appearing in `base/` is not a
cosmetic problem: it means the generic fallback can resolve to one organisation's
typeface, and the two-step resolve in §0.3 — brand rows first, generic on miss — stops
being a fallback at all.

## Provenance

Each table's authored source and the transforms applied to it are listed by the loader
itself on every run, and recorded in `research/25-reheader-map.md`.
