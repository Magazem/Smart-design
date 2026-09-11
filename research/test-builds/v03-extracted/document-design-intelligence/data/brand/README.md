# `data/brand/` — the overlay contract

This directory is empty in every released base package. It exists only once a
user installs a brand (see the project `README.md`, "Give it your brand").

## Producing a brand kit (the one-file flow)

A brand kit is never hand-assembled. The user (or Claude, on their behalf)
writes exactly ONE file — `brand.md`, plain `key: value` + `## Section` text
describing the brand's slug, palette, typefaces, doctypes, and voice (see
`scripts/make_brand_kit.py`'s own docstring for the full grammar) — and runs:

```
python3 scripts/make_brand_kit.py <brand.md>
```

`make_brand_kit.py` derives the rows this brand needs, self-checks them
against the same gate `scripts/validate_data.py` runs at release build time,
and zips the result into `<slug>-brand-kit.zip` at the repo root — the exact
artifact `scripts/merge_brand_kit.py` accepts to install it (below). Nothing
about that merge step changes; only how the kit gets made.

## Layout once a brand is installed

```
data/brand/
  active.json        <- {"active": "<slug>"} — which brand overlay, if any, is
                         currently in effect. Written by scripts/merge_brand_kit.py,
                         never by hand.
  <slug>/             <- one directory per installed brand, e.g. data/brand/ens/
    <table>.csv        <- brand-scoped rows for whichever base tables (see
                           data/base/) this brand overrides. A brand overlay
                           need not touch every table — only the ones it
                           customises.
    brand.md            <- brand metadata (name, slug, voice notes). Read by
                           scripts/merge_brand_kit.py to determine <slug>;
                           see that script's docstring for the exact format.
    assets/              <- optional supporting files (logos, reference
                           images) the brand's rows may point to.
```

## The contract

- `<slug>` must match `^[a-z0-9-]+$`. Nothing writes into this directory
  without validating that first — see `scripts/merge_brand_kit.py`.
- A brand overlay CSV is expected to introduce **new** rows (new slugs) in
  whichever base table it extends, not to redefine an existing base slug.
  Row-level key-collision checking happens at validate time
  (`scripts/validate_data.py`, via the manifest's declared `key_column` per
  table — see `data/schema-manifest.json`), so a colliding brand kit fails
  the release gate before it ever reaches `scripts/resolve.py`.
- Only one brand is active at a time (`active.json`). This directory may hold
  more than one brand's folder (e.g. if a user tried a second brand), but the
  resolver only ever reads the one named in `active.json`.
- No installed brand's data ships in a base release — `scripts/build_zip.py`
  excludes every `data/brand/<slug>/` overlay directory (and `active.json`)
  from the built ZIP; this directory's own documentation (this file,
  `.gitkeep`) is the only thing under `data/brand/` that does ship. See
  `research/15-distribution-model.md` §3 in the project repo ("brand
  directories are never part of our release artifact").

Full design rationale: `research/09-library-schema.md` §0.3 and
`research/15-distribution-model.md` §1–2 in the project repository.
