# T5 typefaces draft — sources and design notes

`19-t5-typefaces-draft.csv` has 8 rows, matching T5's current columns exactly
(`09-library-schema.md:349-363`), with `Embedding Licence` and `Has Tabular Figures` left
blank in every row — both are script-derived (fsType read, GSUB `tnum` presence per
research/12) and will be filled by the Mechanism Analyst's `fonts.py`, not hand-typed here.
`Scale Key` values (`ens-print`, `cv-print`, `report-print`, `report-screen`,
`report-technical`, `form-print`) are placeholder FKs into T6 — I don't own T6 authorship
in this task, so treat them as intent, not verified-existing rows; the Coverage Analyst
should confirm or rename at merge time.

I verified the safe-stack and licence claims below against current (September 2026) web
sources rather than relying on training-data memory alone, since this file is exactly the
kind of thing that goes stale — Microsoft changed its Office default font mid-2023 and I
wanted current status, not what I remembered.

Sources: [Aptos vs Calibri](https://www.wps.com/blog/aptos-vs-calibri-comparison-of-microsoft-s-old-and-new-default-fonts/),
[Microsoft Q&A on Aptos rollout](https://learn.microsoft.com/en-us/answers/questions/5682218/when-will-aptos-be-the-microsoft-default-font),
[List of typefaces included with macOS](https://grokipedia.com/page/List_of_typefaces_included_with_macOS),
[Liberation fonts (Wikipedia)](https://en.wikipedia.org/wiki/Liberation_fonts),
[Croscore fonts (Wikipedia)](https://en.wikipedia.org/wiki/Croscore_fonts),
[Caladea metric-compatibility, Debian wiki](https://wiki.debian.org/SubstitutingCalibriAndCambriaFonts),
[IBM Plex license, GitHub](https://github.com/IBM/plex/blob/master/LICENSE.txt),
[JetBrains Mono OFL, GitHub](https://github.com/JetBrains/JetBrainsMono/blob/master/OFL.txt),
[Roboto family OFL re-license discussion, GitHub](https://github.com/google/fonts/issues/9143).

## 1. Safe-stack platform-availability grid (item 1)

"Present" = bundled with the OS or app itself, no download/install step, no embedding
needed. This is the table that answers "will this .docx open identically on someone
else's machine" — and it bifurcates by **OS-bundled vs. Office-bundled**, which matters
exactly where the task said it would: a PDF only needs the OS (or nothing, if fonts are
embedded); a **native, unembedded .docx** needs the font present in whatever app opens
it, which for the classic Microsoft ClearType set means **Office itself**, not the OS.

| Family | Windows 11 (OS) | macOS current (OS) | Microsoft Office (any OS) | Google Docs / Workspace | LibreOffice | Metric-compatible substitute |
|---|---|---|---|---|---|---|
| Arial | present | present | present | present (core web font set) | present (bundled) | — (already universal) |
| Times New Roman | present | present | present | present | present (bundled) | — |
| Calibri | present, but **no longer the default** since Office switched to Aptos (2023+) — still bundled, existing docs keep it | **absent from the OS**; present only via Office for Mac install | present | present (added to the core set) | **absent** unless installed | Carlito (OFL 1.1, metric-identical, Google Crosextra) |
| Cambria | present | absent from OS; Office for Mac only | present | not in the core set | absent unless installed | Caladea (OFL 1.1, metric-identical, Google Crosextra) |
| Candara / Corbel / Constantia | present | absent from OS; Office for Mac only | present | not in the core set | absent unless installed | none well-established; treat as embed-or-avoid |
| Consolas (mono) | present | absent from OS; Office for Mac only | present | not in the core set | absent unless installed | none well-established; Courier New or an OFL mono is the safer default |
| Georgia | present | present | present | present | present (bundled) | — |
| Verdana | present | present | present | present | present (bundled) | — |
| Trebuchet MS | present | present | present | present | present (bundled) | — |
| Courier New (mono) | present | present | present | present | present (bundled) | — |
| Helvetica / Helvetica Neue | absent (Windows has no native Helvetica) | present | absent unless installed | not in the core set | absent unless installed | Arial (not metric-identical, but the conventional stand-in) |
| Segoe UI | present | absent | present (Office UI chrome, not usually a body-copy choice) | not in the core set | absent | — (not really a document body font; UI font) |
| Aptos | present (new Windows/Office default, 2023+) | present via current Office for Mac | present | not yet in the core set (as of this check) | absent | none established yet — too new for a substitute ecosystem to exist |

**Reading this table for a doctype:** if a doctype's render target is `docx-office` with
`Font Rule: safe-stack` (T8), only the first row-group (Arial, Times New Roman, Georgia,
Verdana, Trebuchet MS, Courier New) is truly safe **without depending on Office being the
opening application** — those are OS-bundled on both Windows and Mac. Calibri/Cambria/
Candara/Corbel/Constantia/Consolas are **Office-bundled, not OS-bundled**: safe if you can
assume the recipient opens the file in Microsoft Office, not safe if they might open it in
a bare OS text viewer, Preview, or a non-Office app. That distinction was implicit in
report 03 §B's font-embedding discussion; this table makes it a lookup instead of a
sentence.

## 2. Open-licence document faces (item 2) — catalog, ~20 families

All Google Fonts unless noted. No display/decorative faces. Licence verified per-family
this session, not assumed from memory (see sources above) — two corrections against my own
prior assumption while researching this: **Roboto's core family was re-licensed from
Apache 2.0 to OFL** (not all Roboto variants migrated at the same time — verify the exact
variant if this matters downstream), and **JetBrains Mono is OFL 1.1, not Apache** (I
initially assumed Apache given its origin as a developer-tools company release; checked
before using it in the T5 catalog).

| Family | Category | Licence | Google Fonts URL | Has Tabular Figures | Recommended role | x-height class | Pairs with |
|---|---|---|---|---|---|---|---|
| Inter | sans-text | OFL | fonts.google.com/specimen/Inter | unknown — not verified this session | body / both | large (tag: convention — widely described as high-x-height, not independently measured here) | Manrope (already ENS's pair) |
| Source Sans 3 | sans-text | OFL | fonts.google.com/specimen/Source+Sans+3 | unknown | heading / body | medium (convention) | Source Serif 4 |
| Source Serif 4 | serif-text | OFL | fonts.google.com/specimen/Source+Serif+4 | unknown | body | medium (convention) | Source Sans 3 |
| Source Code Pro | mono | OFL | fonts.google.com/specimen/Source+Code+Pro | unknown | mono | medium (convention) | Source Sans 3, Source Serif 4 |
| IBM Plex Sans | sans-text | OFL | fonts.google.com/specimen/IBM+Plex+Sans | unknown | heading / both | medium (convention) | IBM Plex Serif, IBM Plex Mono |
| IBM Plex Serif | serif-text | OFL | fonts.google.com/specimen/IBM+Plex+Serif | unknown | body | medium (convention) | IBM Plex Sans, IBM Plex Mono |
| IBM Plex Mono | mono | OFL | fonts.google.com/specimen/IBM+Plex+Mono | unknown | mono | medium (convention) | IBM Plex Sans, IBM Plex Serif |
| Public Sans | humanist-sans | OFL | fonts.google.com/specimen/Public+Sans | unknown | body / both | large (convention — designed for small-size legibility, US Web Design System) | Source Serif 4 |
| Work Sans | humanist-sans | OFL | fonts.google.com/specimen/Work+Sans | unknown | body / both | medium (convention) | Lora |
| Karla | humanist-sans | OFL | fonts.google.com/specimen/Karla | unknown | body / both | medium (convention) | Bitter |
| Lora | serif-text | OFL | fonts.google.com/specimen/Lora | unknown | body | medium (convention) | Work Sans |
| Merriweather | serif-text | OFL | fonts.google.com/specimen/Merriweather | unknown | body | large (convention — explicitly designed for on-screen reading) | Source Sans 3 |
| PT Serif | serif-text | OFL | fonts.google.com/specimen/PT+Serif | unknown | body | medium (convention) | PT Sans |
| PT Sans | sans-text | OFL | fonts.google.com/specimen/PT+Sans | unknown | heading | medium (convention) | PT Serif |
| Libre Baskerville | serif-text | OFL | fonts.google.com/specimen/Libre+Baskerville | unknown | body (small sizes only — cut for that use) | small (convention — classic revival proportions) | Work Sans |
| Crimson Pro | serif-text | OFL | fonts.google.com/specimen/Crimson+Pro | unknown | body | small (convention — book-style proportions) | Karla |
| Noto Serif | serif-text | OFL | fonts.google.com/specimen/Noto+Serif | unknown | body | medium (convention) | Noto Sans |
| Noto Sans | sans-text | OFL | fonts.google.com/specimen/Noto+Sans | unknown | heading / both | medium (convention) | Noto Serif |
| Roboto Slab | slab | **Apache License 2.0 — corrected below; not re-licensed to OFL like base Roboto** | fonts.google.com/specimen/Roboto+Slab | unknown (confirmed below) | heading | medium (convention) | Roboto |
| Roboto | sans-text | OFL (re-licensed from Apache; verify variant) | fonts.google.com/specimen/Roboto | unknown | body | medium (convention) | Roboto Slab |
| Zilla Slab | slab | OFL | fonts.google.com/specimen/Zilla+Slab | unknown | heading | medium (convention) | Work Sans |
| Bitter | slab | OFL | fonts.google.com/specimen/Bitter | unknown | body / heading | medium (convention) | Karla |
| JetBrains Mono | mono | OFL 1.1 (corrected — see note above) | fonts.google.com/specimen/JetBrains+Mono | unknown | mono | medium (convention) | any of the above |
| Manrope | sans-text | OFL | fonts.google.com/specimen/Manrope | unknown | heading | large (convention) | Inter (ENS's pair) |

`x-height class` is tagged `convention` throughout — this is a real, sourced-in-spirit
typographic property (report 03 §E cites x-height as a pairing-harmony factor) but I did
not independently measure any of these values against font metrics this session; treat
these as directional, not verified numbers, until someone runs actual x-height/cap-height
ratios from the font files (a stdlib-feasible follow-on, similar in spirit to the fsType
work in research/12 — `hhea`/`OS/2` tables carry `sxHeight` directly, so this is buildable,
just not built here).

`Has Tabular Figures` is `unknown` for every row in this catalog, on principle — I did not
run the GSUB `tnum` check from research/12 against these 20+ families this session
(scope/time), and per that research's own finding, absence-of-check should read `unknown`,
never a guessed `no`. Whoever runs `fonts.py` against these families should populate both
this catalog and the T5 CSV's blank columns from the same pass.

## Metric-compatible-substitute logic — how it actually works, and where it should live

**The mechanism.** A metric-compatible font is built to have identical per-glyph advance
widths to a proprietary target, so text set in the substitute reflows and paginates
*exactly* like text set in the original — only the glyph shapes differ. Two independent
lineages exist for the classic Microsoft set:
- **Liberation fonts** (Red Hat/originally commissioned to settle a font-availability gap
  on Linux) — Liberation Sans↔Arial, Liberation Serif↔Times New Roman, Liberation
  Mono↔Courier New. OFL. Default in LibreOffice.
- **Croscore fonts** (Google, licensed from Ascender Corp) — Arimo↔Arial/Helvetica,
  Tinos↔Times New Roman, Cousine↔Courier New. **Apache 2.0**, not OFL — a real licence
  difference from Liberation covering the same three substitutions, worth keeping straight
  if the schema ever needs to pick one.
- **Crosextra** (Google, a separate, later release) — Carlito↔Calibri, Caladea↔Cambria.
  **OFL 1.1** (confirmed this session, correcting an initial assumption it might match the
  Croscore Apache licence — it doesn't; Crosextra deliberately used OFL).

No established metric-compatible substitute exists for Candara, Corbel, Constantia, or
Consolas — those four are genuinely Office-only with no safe fallback identity; a doctype
depending on them needs embedding or should avoid them.

**Column or separate table?** Recommend a **separate small table**, not a column on T5.
Reasons: (1) the substitute relationship is per-*family*, not per-*pairing* — Calibri's
substitute is Carlito regardless of which T5 row happens to use Calibri as a Heading or
Body Family, so putting it on T5 means restating the same fact on every row that
references Calibri; (2) it's genuinely a 1:1 lookup (`proprietary_family → substitute_family,
licence, source`), the same shape T6 was split into its own table for — Rule 1's
"lists yes, maps no" logic applies here too, just at the family level instead of the
scale level; (3) T5's own design notes already point at this exact gap — "Upstream's
`google-fonts.csv`... cannot back T5's columns... keep it as an optional metadata lookup"
(`09-library-schema.md:384-387`). A small `font-substitutes.csv` (proprietary_family,
substitute_family, licence, metric_identical: bool, source) is that lookup, purpose-built
for this one fact rather than upstream's 1,923-row general catalog.

## 3. `fonts.py` results — every family referenced in the 8 T5 rows

Ran `read_fstype` and `has_tnum` from `skill/document-design-intelligence/scripts/lib/fonts.py`
against all 13 families (3 local system fonts + 10 downloaded), using
`C:\Users\ysuliman\AppData\Local\Microsoft\WindowsApps\python3.exe`. **Zero parse
failures** — every file returned a valid `(fsType, label)` pair and a `tnum` result, none
hit the `None`/"not a recognizable TTF/OTF" or "no OS/2 table" failure paths.

System fonts were read directly from `C:\Windows\Fonts` — no download needed, no hash
recorded (not a distributable artifact this session touched, already resident on the
machine both before and after this task).

| Family | File | Source URL | SHA-256 | fsType | Label | tnum |
|---|---|---|---|---|---|---|
| Arial | `C:\Windows\Fonts\arial.ttf` | (local system font, not downloaded) | — | 8 | editable | yes |
| Times New Roman | `C:\Windows\Fonts\times.ttf` | (local system font, not downloaded) | — | 8 | editable | yes |
| Georgia | `C:\Windows\Fonts\georgia.ttf` | (local system font, not downloaded) | — | 8 | editable | yes |
| Manrope | `manrope.ttf` | github.com/google/fonts, `ofl/manrope/Manrope[wght].ttf` | `d0639be45d0af36e798172419d7bd173c4bd4f29e2b76cbb69db1d11bf8b0a40` | 0 | installable | yes |
| Inter | `inter.ttf` | github.com/google/fonts, `ofl/inter/Inter[opsz,wght].ttf` | `29160a80ff49ddcab2c97711247e08b1fab27a484a329ce8b813d820dc559031` | 0 | installable | yes |
| Source Sans 3 | `sourcesans3.ttf` | github.com/google/fonts, `ofl/sourcesans3/SourceSans3[wght].ttf` | `042fe2cc0b933e328410d7acbd0aa6a1873dca5aef81875f4bc214b08825c7b9` | 0 | installable | unknown |
| Source Serif 4 | `sourceserif4.ttf` | github.com/google/fonts, `ofl/sourceserif4/SourceSerif4[opsz,wght].ttf` | `97b2d4da6e3cb494b5a1e66ae176914d852ccabef49e0c02c0df25f3e39aca0b` | 0 | installable | yes |
| IBM Plex Sans | `ibmplexsans.ttf` | github.com/google/fonts, `ofl/ibmplexsans/IBMPlexSans[wdth,wght].ttf` | `3b031aa4216174205bd8471f88a49b91f093169e9e87bd5262242bc5967fe2e3` | 0 | installable | unknown |
| IBM Plex Serif | `ibmplexserif-regular.ttf` | github.com/google/fonts, `ofl/ibmplexserif/IBMPlexSerif-Regular.ttf` | `e882efa9c41949a528ac2369079ec5ef050c1c996bbd0bacce3c3326d44cf80d` | 0 | installable | unknown |
| IBM Plex Mono | `ibmplexmono-regular.ttf` | github.com/google/fonts, `ofl/ibmplexmono/IBMPlexMono-Regular.ttf` | `6a3412f058c7d8dfd9170c41e85ade48e5156ecb89356110ca57a0a27734af46` | 0 | installable | unknown |
| Public Sans | `publicsans.ttf` | github.com/google/fonts, `ofl/publicsans/PublicSans[wght].ttf` | `d75a7dc1a27eb9e336d5b33f55489d2ecb5621bf694d5c43b2415bce2ca830a8` | 0 | installable | yes |
| Roboto Slab | `robotoslab.ttf` | github.com/google/fonts, `apache/robotoslab/RobotoSlab[wght].ttf` | `786ae192477447d33c6672c3055fba7cbfe45184c9a79e77a14f15716ca05b16` | 0 | installable | unknown |
| Roboto | `roboto.ttf` | github.com/google/fonts, `ofl/roboto/Roboto[wdth,wght].ttf` | `d7598e12c5dbef095ff8272cfc55da0250bd07fbdecbac8a530b9b277872a134` | 0 | installable | yes |

**Files the functions could not parse:** none. All 13 succeeded.

**A directory-path finding, not a parser finding:** `ofl/robotoslab/` returned 404 —
Roboto Slab is **not** under `ofl/` in the canonical repo, it's under `apache/robotoslab/`,
and its `LICENSE.txt` there is Apache License 2.0, confirmed by direct fetch. This
corrects §2's catalog entry above (originally guessed "OFL, re-licensed from Apache" by
analogy with base Roboto — wrong; the two fonts are still on different licences in the
canonical repo, only base Roboto migrated). Caught before it reached the CSV because I
fetched the real path rather than assuming the `ofl/<slug>/` pattern held universally.

**fsType-vs-licence agreement check: no disagreement found.** Every OFL and Apache-licensed
font in this set (Manrope, Inter, Source Sans 3, Source Serif 4, IBM Plex Sans/Serif/Mono,
Public Sans, Roboto Slab, Roboto — 10 files, two licence texts, one shared property) reports
`fsType=0` (installable, no restriction). That's the expected, consistent result — an
open-licence font vendor has no reason to set embedding-restriction bits — but it was
checked per-file against the actual binary, not assumed from the licence text, which is
the point of this column existing at all. If a future family shows an open licence text
paired with a restrictive fsType, that actually-checked disagreement is the load-bearing
kind of finding this mechanism exists to catch; this batch didn't produce one.

**T5 CSV filled in place**, `Embedding Licence`/`Has Tabular Figures` per row: `ens-manrope-inter`
→ installable/yes (both Manrope and Inter agree); `safe-sans-arial` → editable/yes;
`safe-serif-times` → editable/yes; `safe-serif-georgia` → editable/yes;
`ofl-source-sans-serif` → installable/yes (Has Tabular Figures resolved from the **Body**
family, Source Serif 4=yes, since table-cell digits are set in body text, not headings —
Source Sans 3 itself independently reported `unknown`, noted here rather than silently
dropped); `ofl-plex-superfamily` → installable/unknown (Body family IBM Plex Serif=unknown;
Mono family IBM Plex Mono is also `unknown` despite being a monospace-adjacent design —
same explainable pattern as Consolas in research/12, no tnum tag needed when digits are
already fixed-width by design, not a red flag); `ofl-public-sans` → installable/yes;
`ofl-roboto-slab` → installable/yes (Body family Roboto=yes; Heading family Roboto Slab
itself is `unknown`, same body-family resolution rule applied).

**Temp downloads deleted.** All 10 files removed from the temp directory after hashing and
testing; deletion confirmed (subsequent `ls` on the directory returned "No such file or
directory"). Nothing was added to `skill/`.
