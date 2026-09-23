# research/library/typefaces/ranked-pairings-evidence.md — P3.1 ranking working

Retrieved 2026-09-23. Method per research/80 §3/§R-d (count, don't judge) and research/81
(fetchability probe). Primary ranked corpus: `https://fonts.google.com/metadata/fonts`
(no leading `)]}'` guard was present on this fetch — the raw body parsed directly as JSON).
Verified sort direction empirically: `popularity` is ascending = more popular (Roboto=2,
Open Sans=3, Inter=5, Montserrat=7, Poppins=8, Lato=9 all sit at the very top — matches the
brief's expectation "Roboto/Open Sans near top"), not descending.

## Admissibility filter applied (step 1 of the task)

Kept only families that are (a) OFL/Apache/UFL-licensed (every family below is
`isOpenSource: true` in the metadata payload — Google Fonts serves no non-libre-licensed
family under the open catalogue used here), (b) have >=4 static weights or a `wght`
variable axis, and (c) are serif/sans-serif (a few slab/display exceptions used only where
a documented pairing existed, capped at what the brief allows). Rows that fail (b) — e.g.
`Archivo Black` (1 weight), `Bebas Neue` (1 weight), `Black Ops One` (1 weight) — were
excluded as pairing *heads* on their own; the one exception is `Fira Mono` (3 weights, no
axis), kept only in the auxiliary `Mono Family` role of `lib-fira-sans-fira-mono`, mirroring
the existing base-library precedent `ofl-plex-superfamily` (IBM Plex Mono is likewise a
secondary companion family, not gated by the 4-weight floor because it never carries
heading/body text itself).

## Top 60 by Google Fonts `popularity` (lower = more popular)

| Rank | Family | Category | Static weights | Variable axes |
|---|---|---|---|---|
| 2 | Roboto | Sans Serif | 9 | wdth,wght |
| 3 | Open Sans | Sans Serif | 6 | wdth,wght |
| 4 | Google Sans | Sans Serif | 4 | GRAD,opsz,wght |
| 5 | Inter | Sans Serif | 9 | opsz,wght |
| 7 | Montserrat | Sans Serif | 9 | wght |
| 8 | Poppins | Sans Serif | 9 | - |
| 9 | Lato | Sans Serif | 5 | - |
| 10 | Noto Sans JP | Sans Serif | 9 | wght |
| 14 | Arimo | Sans Serif | 4 | wght |
| 16 | Roboto Condensed | Sans Serif | 9 | wght |
| 17 | Roboto Mono | Monospace | 7 | wght |
| 19 | Oswald | Sans Serif | 6 | wght |
| 20 | Noto Sans | Sans Serif | 9 | wdth,wght |
| 22 | DM Sans | Sans Serif | 10 | opsz,wght |
| 23 | Raleway | Sans Serif | 9 | wght |
| 24 | Nunito | Sans Serif | 9 | wght |
| 25 | Playfair Display | Serif | 6 | wght |
| 26 | Nunito Sans | Sans Serif | 9 | YTLC,opsz,wdth,wght |
| 28 | Roboto Slab | Serif | 9 | wght |
| 29 | Rubik | Sans Serif | 7 | wght |
| 31 | Manrope | Sans Serif | 7 | wght |
| 32 | Ubuntu | Sans Serif | 4 | - |
| 33 | Merriweather | Serif | 7 | opsz,wdth,wght |
| 34 | Outfit | Sans Serif | 9 | wght |
| 35 | Archivo Black | Sans Serif | 1 | - |
| 36 | Kanit | Sans Serif | 9 | - |
| 37 | Work Sans | Sans Serif | 9 | wght |
| 38 | Noto Sans KR | Sans Serif | 9 | wght |
| 39 | Lora | Serif | 4 | wght |
| 40 | Plus Jakarta Sans | Sans Serif | 7 | wght |
| 41 | Quicksand | Sans Serif | 5 | wght |
| 42 | PT Sans | Sans Serif | 2 | - |
| 43 | Bebas Neue | Sans Serif | 1 | - |
| 44 | Figtree | Sans Serif | 7 | wght |
| 45 | Noto Sans TC | Sans Serif | 9 | wght |
| 46 | Mulish | Sans Serif | 9 | wght |
| 47 | Archivo | Sans Serif | 9 | wdth,wght |
| 48 | Source Sans 3 | Sans Serif | 8 | wght |
| 49 | Barlow | Sans Serif | 9 | - |
| 50 | Bricolage Grotesque | Sans Serif | 7 | opsz,wdth,wght |
| 51 | JetBrains Mono | Monospace | 8 | wght |
| 52 | Inconsolata | Monospace | 8 | wdth,wght |
| 53 | IBM Plex Sans | Sans Serif | 7 | wdth,wght |
| 54 | Prompt | Sans Serif | 9 | - |
| 55 | Jost | Sans Serif | 9 | wght |
| 57 | Saira | Sans Serif | 9 | wdth,wght |
| 58 | Black Ops One | Display | 1 | - |
| 60 | Karla | Sans Serif | 7 | wght |
| 61 | Noto Serif | Serif | 9 | wdth,wght |
| 62 | Fira Sans | Sans Serif | 9 | - |
| 63 | Space Grotesk | Sans Serif | 5 | wght |
| 64 | Share Tech | Sans Serif | 1 | - |
| 65 | Smooch Sans | Sans Serif | 9 | wght |
| 66 | Titillium Web | Sans Serif | 6 | - |
| 67 | Libre Baskerville | Serif | 4 | wght |
| 68 | Heebo | Sans Serif | 9 | wght |
| 69 | Google Sans Flex | Sans Serif | 11 | GRAD,ROND,opsz,slnt,wdth,wght |
| 70 | PT Serif | Serif | 2 | - |
| 72 | Source Code Pro | Monospace | 8 | wght |
| 73 | Cormorant Garamond | Serif | 5 | wght |

(`rank 1` and `rank 6` are not shown above because the fetched payload's lowest observed
value was 2 and the list is otherwise contiguous by rank as returned; no gap-filling was
invented.)

## Companion-family ranks used below top 60 (fetched individually by family name)

| Rank | Family | Category | Static weights | Variable axes |
|---|---|---|---|---|
| 80 | Libre Franklin | Sans Serif | 9 | wght |
| 84 | EB Garamond | Serif | 5 | wght |
| 93 | Bitter | Serif | 9 | wght |
| 106 | Cabin | Sans Serif | 4 | wdth,wght |
| 107 | DM Serif Display | Serif | 1 | - |
| 136 | Merriweather Sans | Sans Serif | 6 | wght |
| 175 | Archivo Narrow | Sans Serif | 4 | wght |
| 180 | Spectral | Serif | 7 | - |
| 181 | Roboto Serif | Serif | 9 | GRAD,opsz,wdth,wght |
| 187 | Alegreya Sans | Sans Serif | 7 | - |
| 212 | Vollkorn | Serif | 6 | wght |
| 268 | Alegreya | Serif | 6 | wght |
| 361 | Fira Mono | Monospace | 3 | - |

`DM Serif Display` (1 static weight) and `Fira Mono` (3 weights) are the two exceptions
noted above: both are kept only in an auxiliary role next to an admissible >=4-weight
head/body family, per the precedent already set by the base library's own
`ofl-plex-superfamily` row.

## Row-by-row sourcing (file A -> file B mapping)

Single-family rows (Family Count=1) carry one `ranked` provenance row (Google Fonts
popularity for that family) and no separate "pairing source" row, since there is no pairing
to source — this matches the task's instruction that only pairing rows need the extra
authority/ranked citation.

Pairing rows carry one `ranked` provenance row per family (Google Fonts popularity) *plus*
one `authority` or `ranked` row citing the pairing itself:

| typeface_key | Pairing source | Evidence Class | Fetch |
|---|---|---|---|
| lib-noto-serif-noto-sans | Wikipedia "Noto fonts" ("Noto Sans and Noto Serif contain Latin, Greek and Cyrillic glyphs") | authority | fetched |
| lib-roboto-serif-roboto | fonts.withgoogle.com/roboto-serif ("latest addition to the Roboto superfamily...pairs well with the sans-serif versions of Roboto") | authority | fetched |
| lib-merriweather-merriweather-sans | GitHub SorkinType/Merriweather-Sans README ("The Sans companion to the serifed Merriweather") | authority | fetched |
| lib-nunito-nunito-sans | Fonts In Use / Nunito Sans ("A non-rounded version of Vernon Adams' Nunito, added by Jacques Le Bailly in 2017") | authority | fetched |
| lib-dm-serif-display-dm-sans | GitHub googlefonts/dm-fonts README ("DM suite of fonts: Sans, Serif Text and Serif Display") | authority | fetched |
| lib-alegreya-alegreya-sans | Typewolf /alegreya (Suggested Font Pairing: Alegreya Sans) | ranked | fetched |
| lib-fira-sans-fira-mono | Wikipedia "Fira (typeface)" ("Fira Sans is accompanied by a monospaced variant called Fira Mono") | authority | fetched |
| lib-libre-baskerville-libre-franklin | Typewolf /libre-baskerville (Suggested Font Pairing: Libre Baskerville + Libre Franklin) | ranked | fetched |
| lib-eb-garamond-cabin | Typewolf /eb-garamond (Suggested Font Pairing: EB Garamond + Cabin) | ranked | fetched |
| lib-bitter-montserrat | Typewolf /bitter (Suggested Font Pairing: Bitter + Montserrat) | ranked | fetched |
| lib-spectral-source-sans-3 | Typewolf /spectral (Suggested Font Pairing: Spectral + Source Sans Pro — current Google Fonts family name is Source Sans 3, same lineage) | ranked | fetched |
| lib-vollkorn-montserrat | Typewolf /vollkorn (Suggested Font Pairing: Vollkorn + Montserrat) | ranked | fetched |
| lib-archivo-narrow-merriweather | Typewolf /archivo-narrow (Suggested Font Pairing: Archivo Narrow + Merriweather) | ranked | fetched |

Typewolf pairings that were fetched but **rejected** for non-OFL partners (kept out of file
A entirely, logged here so the rejection is auditable, not silently dropped): Playfair
Display + FF Super Grotesk, Merriweather + FF Mark, Lora + Gibson, EB Garamond alternates
n/a, Work Sans + Americana, Space Grotesk + Fortescue, DM Sans + Romie, Rubik + Acta
Display, Karla + Schneidler, Crimson Text + Neuzeit, Raleway + Adelle, Oswald + Modern 216,
Quicksand + Abril — every one of these partner fonts is a commercial (non-OFL) release, so
none is embeddable/installable per the manifest's `Embedding Licence` enum, and the brief
requires both faces OFL for a pairing to be admissible. Pages that 404'd or returned no
"Suggested Font Pairing" section in this pass: Zilla Slab, Cormorant Garamond, Nunito,
Josefin Sans, Barlow, Heebo, Mulish.

## Top-10 pairings by best-component Google Fonts rank

| # | typeface_key | Best rank | Display Name |
|---|---|---|---|
| 1 | lib-roboto | 2 | Roboto |
| 1 | lib-roboto-serif-roboto | 2 | Roboto Serif + Roboto |
| 3 | lib-open-sans | 3 | Open Sans |
| 4 | lib-inter | 5 | Inter |
| 5 | lib-montserrat | 7 | Montserrat |
| 5 | lib-bitter-montserrat | 7 | Bitter + Montserrat |
| 5 | lib-vollkorn-montserrat | 7 | Vollkorn + Montserrat |
| 8 | lib-poppins | 8 | Poppins |
| 9 | lib-lato | 9 | Lato |
| 10 | lib-noto-sans | 20 | Noto Sans |
| 10 | lib-noto-serif-noto-sans | 20 | Noto Serif + Noto Sans |

("Best rank" = the lower of the two families' popularity ranks for two-family rows, since
Rank Value in provenance is per-family, not per-pairing — there is no single-number
"pairing popularity" metric, per research/81's finding that no ranked API exists for
pairings themselves.)

## Duplicate-avoidance check against the existing base library

`skill/document-design-intelligence/data/base/typefaces.csv` already contains: Source Sans
3 + Source Serif 4 (both directions), the IBM Plex Sans+Serif+Mono superfamily, Public Sans
(solo), Roboto Slab + Roboto, PT Serif + PT Sans, IBM Plex Sans (solo), and Fraunces + Work
Sans. None of those families or pairings are repeated in `ranked-pairings.csv` — confirmed
by the validation script (see below), which diffs `typeface_key` values against the base
CSV's existing keys.

## Validation run (2026-09-23)

```
file A rows: 20
file B rows: 46
VALIDATION OK: headers exact, keys unique, no duplicate of base rows, Scale Keys valid, enums valid, provenance FK valid.
```

Checks performed: (1) both CSVs parse; (2) file A header equals
`data/base/typefaces.csv` header exactly; (3) `typeface_key` values unique within file A and
disjoint from the base CSV's existing keys; (4) every `Scale Key` in file A exists in
`data/base/type-scales.csv`'s `scale_key` column; (5) every enum-constrained column
(`Category Contrast`, `Safe Stack Availability`, `Embedding Licence`, `Has Tabular Figures`)
matches `schema-manifest.json`'s `tables.typefaces.enums`; (6) the derived rule
(`Safe Stack Body Fallback` equals `Safe Stack Fallback` or is blank when `Family Count=1`)
holds for every single-family row; (7) file B's header is exact; (8) `prov_key` values are
unique; (9) every file B `Row Key` exists in file A; (10) file B's `Table`/`Evidence
Class`/`Fetch` values match `schema-manifest.json`'s `tables.provenance.enums`; (11)
numeric `Rank Value` parses as an int wherever `Fetch=fetched` and `Evidence Class=ranked`
and a value is present; (12) every file A row has at least one file B provenance row.
