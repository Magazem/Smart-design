# research/82 — Design ranking protocol (P2.2, FROZEN 2026-09-23)

Pre-registered before any family is coded. Binding on every Phase 4 worker. Nothing here is
edited after the first family task starts; corrections go in `research/82a-*.md` (amendment,
dated, stating which family results it invalidates). Inputs: research/80 (§R, §2B, §3),
research/81 (both probes), research/68 (slop), data/base CSVs. Where this file and research/80
§3 differ, this file wins (research/80 §3 said "frozen in research/82").

Protocol-author probe, 2026-09-23 (curl, recorded here so workers need not repeat it):
- **LibreOffice Extensions, tag "Templates" (id 118)** exposes a numeric per-item **download
  count** and a `ord=download_d` sort: `https://extensions.libreoffice.org/en/extensions?Tags%5B%5D=118&ord=download_d`
  (~690 items, 30/page, `&start=30`...). Impress templates = add `&Tags%5B%5D=43` (~120 items).
  `q=` is full-text and noisy. Counts are cumulative since the 03-2020 site migration.
- **Microsoft Create** category URLs that resolve with items in the static payload: resumes (34
  items), cover-letters (16), letters (18, includes newsletters), memos (9), brochures (7),
  flyers (17), presentations (23), invoices (8), posters (10), newsletters (15). Reports,
  proposals, quotes, forms, infographics, white papers, one-pagers: no category resolved.
  Only the first static slice is reachable; page order is editorial, not a metric.
- Apache OpenOffice templates (`templates.openoffice.org`): 403 to curl. Google Docs/Slides
  gallery: login wall (research/81). Apple Pages/Keynote: no public web catalogue.
- GitHub narrowed queries (verified off-topic, do not retry): `memo latex`, `quotation template`,
  `one-pager template` (CVs/landing pages), `infographic template`, `brochure latex` (8),
  `flyer latex` (12). `proposal template latex` is on-topic but academic (thesis/grant).

## 1. Roles and budget

Coders **count; they never judge** which design is better (R-d). Every value they record is
either a number read from a source or an enum chosen by a decision rule in §4. One Sonnet
worker per family task, ~30-45 min, WebFetch + Bash/curl. Hard caps: ≤3 corpora and ≤80
coded items per worker; a family needing more is split by the orchestrator into one coding
task per corpus (F.a) plus one fill task (F.c). Workers never run git, load-base.py or
build-manifest.py (R-g).

Fetch rules: use `curl -s -A "smart-design-research"` for every JSON API (GitHub, npm) and for
LibreOffice/Microsoft HTML — WebFetch's model paraphrases numbers (research/81). GitHub search
is 10 req/min unauthenticated: sleep ≥7 s between calls, `per_page=100`, and log
"rate-limited, retried" on an empty body instead of treating it as dead. Record for every
corpus: exact URL, query, sort, retrieval date (ISO), total_count/N.

## 2. Evidence ladder (layout archetypes)

| Level | What | Metric | designs.Evidence Class | Ranking Metric string |
|---|---|---|---|---|
| L1 | Numeric popularity corpus (GitHub stars, npm `downloads.monthly`, LibreOffice downloads) with **≥40 on-topic codeable items** | k/40 over the top 40 on-topic items in native metric order | ranked | `share:<corpus>:k/40 by <metric>` |
| L2 | Prevalence in a major-vendor curated catalogue (Microsoft Create; LibreOffice/OpenOffice, Google, Apple if fetchable), **or** a numeric corpus with 10-39 on-topic items ("thin L1", coded in full) | k/N over all on-topic items in the reachable catalogue slice | ranked | `prevalence:<catalogue>:k/N` |
| L3 | Juried (named award + year: ARC, Mercury, D&AD, Red Dot, EDA, TDC) or authority (Europass, GOV.UK, USWDS, APA, NISO/DIN via fetched secondary) | none (presence) | juried / authority | `award:<name>:<year>` / `authority:<doc>` |
| L4 | Convention | none | convention | blank |

A catalogue with <10 on-topic items is not coded as a corpus; its items may only corroborate
(listed, not counted). A search-snippet value is never a Rank Value (research/80 §7); only
`Fetch=fetched` rows carry numbers.

## 3. Corpus procedure (F.a)

1. Fetch the corpus URL(s) from §10 exactly. Walk items in native order (metric desc; catalogue
   page order for L2) until 40 on-topic codeable items (L1) or the corpus ends. Walk cap: 200
   raw items.
2. **On-topic** iff the item is a template/theme whose output is a document of the family.
   Off-topic: tools, generators with no fixed design, framework cores (reveal.js, marp-cli),
   awesome-lists, tutorials, other families (a newsletter in the letters category). A repo
   shipping several designs is coded once, on the design shown first in its README. Forks or
   ports of an already-counted design are counted once (highest metric kept). Item titles
   naming quote/estimate/devis/Angebot found in any corpus are cross-listed to `quote`.
3. **Codeable** iff a preview exists at the source: README image, example PDF page 1, gallery
   thumbnail or screenshot. Never compile/render templates. Code from the image (download to the
   system temp dir, view with Read; never into the repo). No preview → excluded "uncodeable",
   and it does not count toward the 40.
4. Code every codeable on-topic item on §4, then apply §5. The denominator N includes
   inadmissible items — admissibility removes archetypes from shipping, not items from N.
5. Record per item: position, name, item URL, metric value, preview URL, all feature codes,
   admissible y/n + reason.

## 4. Coding rubric

Code page 1 (decks: title slide + first content slide; brochures: outside spread). One value
per feature. When a declared font is visible in source (LaTeX `\setmainfont`, CSS
`font-family`, theme file), use it; else judge from glyphs.

| Feature | Values | Decision rule (first match wins) |
|---|---|---|
| **columns** (identity) | `1` · `2-sidebar` · `2-equal` · `3+` · `grid` | Count independently-flowing text columns in the body. A hanging label/date gutter whose entries align row-by-row with the content is `1`. Narrow column ≤40% of text width holding secondary content = `2-sidebar`. Card/tile layouts = `grid`. |
| **heading class** (identity) | `serif` · `sans` · `display` · `mono` | Class of the largest heading (name/title). If the font is known, use the Google Fonts `category` of that family from `https://fonts.google.com/metadata/fonts` (SERIF→serif incl. slabs, SANS_SERIF→sans, DISPLAY/HANDWRITING→display, MONOSPACE→mono); non-Google fonts by foundry class (Helvetica/Calibri/Arial→sans, Times/Garamond/Georgia/Computer Modern→serif). |
| **body class** (variant) | `serif` · `sans` · `mono` | Same rule on body text. |
| **colour use** (identity) | `fill-blocks` · `multi` · `one-accent` · `mono` | Chromatic = HSL S≥0.20 and 0.12≤L≤0.90. (a) any solid non-white fill (chromatic or grey/black, excluding photos and the deck background) ≥10% of page area → `fill-blocks`; else count distinct chromatic hues (≥30° apart) in text, rules and marks: ≥2 `multi`, 1 `one-accent`, 0 `mono`. |
| **header treatment** (identity) | `image-hero` · `band` · `ruled` · `split` · `plain-centered` · `plain-left` | Top 20% of page 1, priority order: image/illustration ≥30% of page area → `image-hero`; filled band behind the header → `band`; full-width rule directly above/below the header block → `ruled`; title and meta/contact on opposite sides of the same band → `split`; centred title → `plain-centered`; else `plain-left`. A CV avatar is not a hero. |
| **rules/boxes** (variant) | `none` · `rules` · `boxes` | Any enclosed bordered block, rounded card or all-cells-bordered table → `boxes`; else any line → `rules`; else `none`. |
| **density** (variant) | `airy` · `standard` · `dense` | Text lines on page 1 normalised to A4/Letter: ≥55 `dense`, ≤30 `airy`. Decks: words on first content slide >40 `dense`, ≤15 `airy`. Poster/flyer/infographic: text blocks >60% of area `dense`, <30% `airy`. |

Family-specific features:

| Family | Feature (role) | Values |
|---|---|---|
| deck | background (identity, replaces columns) | `light` · `dark` · `image` (L<0.5 = dark) |
| deck | title-slide layout (identity, replaces header treatment) | `centered` · `left` · `split` · `full-bleed-image` |
| invoice, quote | totals position (variant) | `right-bottom` · `full-width-bottom` · `other` |
| invoice, quote | table rules (variant) | `none` · `header-and-total` · `row-hairlines` · `all-cells` |
| brochure | panel count (identity, replaces columns) | `2` · `3` · `4+` · `single-sheet` |
| form | field style (identity, replaces header treatment) | `underline` · `box` · `none` |
| cv, cover-letter | photo (variant) | `yes` · `no` |
| letter | letterhead position (variant) | `top-left` · `top-centered` · `top-right` · `address-window` |
| poster | orientation (variant) | `portrait` · `landscape` |
| report, whitepaper, proposal | cover page (variant) | `yes` · `no` |

**Archetype = the 4 identity features**, written `columns|heading|colour|header` (e.g.
`1|serif|one-accent|ruled`). Variant features never split archetypes; the archetype's modal
variant value (ties → the value of its highest-metric exemplar) is used for filling.
**Coarsening (once, family-wide, logged):** if ≥15 items are admissible, >50% of admissible
items are singletons and <5 archetypes have k≥2, drop the 4th identity feature and recount.

## 5. Admissibility (pre-registered; log every exclusion with item, rule id, evidence)

Universal (research/68 + constraints `slop-mechanical`): **A1** >3 visible typeface families;
**A2** emoji; **A3** gradient fill or texture/image fill behind body text; **A4** paint-swipe or
splatter decorative graphic; **A5** ≥3 identical decorative card/icon repeats; **A6** body-text
contrast <4.5:1 (sample text and background hex from the preview; compute with
`skill/document-design-intelligence/scripts/lib/color.py` `contrast_ratio`); **A7** sole accent
is an Office default theme blue (`#4472C4`, `#4F81BD`, `#156082`, `#0563C1`) or an
indigo→purple gradient; **A8** >50% of content blocks individually bordered ("frames around
everything"). Content patterns (bloat, spelling, too much information) are not applied —
templates carry placeholder text.

Family fail constraints:
- **cv, cover-letter** (`ats-strict`, doc-reasoning fail tokens): **C1** columns ≠ `1`
  (multi-column body text, sidebars included); **C2** text inside images; **C3** skill bars,
  rating dots or any icon-only label (`icon-only-skill-bar`); **C4** icon glyphs as list bullets
  (`ats-no-symbol-glyphs`); **C5** graphic timeline; **C6** text boxes / layout tables visible
  as floating blocks.
- **invoice, quote, form**: **C7** table rules = `all-cells` (cell-border ratio >0.5 is fail
  for these doctypes; `boxed-grid` token).
- **brochure, flyer, poster** (`print-marketing` Severity fail): **C8** low-contrast text
  (A6 at 3:1 for text ≥18 pt too), gradient banding (A3). Stock-photo cliché is judge-level and
  is not applied; designs ship with no imagery anyway (features only).
- **deck**: **C9** light-on-dark or dark-on-light body contrast <7:1 is recorded (warn,
  `proj-contrast-margin`) but only <4.5:1 excludes.

## 6. Frequency and rank

Per corpus c: `share_c(a) = k_c(a) / N_c`. Combined share = **unweighted mean over all coded
corpora** of the family (0 where absent) — equal weight per corpus so a large developer corpus
cannot swamp a vendor catalogue; the evidence file must state each corpus's skew (e.g. GitHub
cv = developer/LaTeX; LibreOffice = older, European; Microsoft Create = Microsoft's editorial
pick). Total support `K(a) = Σ k_c(a)`.

Order of the family's list (Rank contiguous 1..N, cap 10):
1. **Ranked, K≥2**, admissible, by combined share desc. Ties: higher L1 share → higher L2
   share → present in more corpora → best native position of any exemplar → archetype code
   alphabetical.
2. **L3** designs (max 3): juried before authority, then by number of independent L3 sources,
   then key alphabetical. If an L3 source's design codes to an archetype already in step 1,
   it merges there (extra provenance row, rank unchanged). L3 slots are reserved: step 1
   fills at most `10 − n_L3 − n_L4`.
3. **Ranked singletons** (K=1), only if steps 1-2 give <5, ordered by the exemplar's native
   position; Evidence Class stays `ranked`, share shown as 1/N.
4. **L4 convention**, max 1, always last.

Target 8-10; floor 5 non-convention; if evidence cannot reach 5, ship what exists and write a
"Shortfall" section. The doctype default (doctypes.Reasoning Key) is never changed and never
promoted: it keeps its place by this procedure and stays the default for fitness (research/72).

## 7. Second coder (falsifier)

The orchestrator spawns an independent worker that receives only §4-§5 and the item list
(ids, URLs, preview URLs) — never the first coder's codes. Sample: all coded items, ids
`<corpus-id>:<position zero-padded to 3>`, sorted lexicographically, then

```python
import math, random
sample = random.Random("82:" + family).sample(ids, max(min(10, len(ids)), math.ceil(0.25 * len(ids))))
```

(string seeds are deterministic across runs). Agreement per feature f, including admissibility
(admit/exclude only, reason ignored): `A_f = (# sample items with identical enum) / n_sample`;
exact match, no partial credit. Cohen's κ is reported, not gating. **Gate: every A_f ≥ 0.80.**
On failure: Opus writes `research/82a-<family>.md` sharpening only the failing rule; the first
coder recodes the whole family; the second coder codes a fresh sample with seed
`"82a:" + family`. A second failure removes that feature from the family's identity
(disclosed); a failing variant feature is not used in filling (family default used instead).

## 8. Filling (F.c) — parts by rule, no taste

Library (base `skill/document-design-intelligence/data/base/` + `research/library/*/` at task
start; list the files used in the evidence file):
- `doc-styles` key `style_key`: Table Rules {hairline, header-and-total, none, row-hairlines},
  Table Fills {none, zebra, header-only}, Emphasis Mechanism {weight, colour-text, fill}, Field
  Style {underline, box, none}, Rule Hair/Strong/Brand pt, Corner Radius mm, Checklist (`;`).
- `palettes` key `palette_key`: Primary…Rule Brand hexes, Text-Safe Roles, Fill-Only Roles.
- `typefaces` key `typeface_key`: Heading/Body Family, Category Contrast, Embedding Licence,
  Safe Stack Fallback, **Scale Key** → `type-scales.scale_key` (Medium {print, projection,
  screen}, Role, Size pt, Leading Ratio). The scale is reached only through the typeface row.
- `doc-reasoning` key `doc_category`: Style/Palette/Typeface Key, bias terms, Doc Conditions,
  Anti-Pattern Tokens, Severity. `designs` key `design_key` → Reasoning Key.

**Style.** Map: rules/boxes none→Table Rules `none`; rules→`header-and-total` for
invoice/quote/report/whitepaper/proposal, else `hairline`; boxes→`hairline` + Checklist "Border
at most half of the blocks". colour use mono/one-accent→Emphasis `weight` (one-accent with
coloured headings→`colour-text`), multi→`colour-text`, fill-blocks→`fill`. header `ruled`→Rule
Brand pt 1, `band`→Emphasis `fill`, else Rule Brand pt 0. form field style→Field Style. Columns,
photo, panel count, totals position, letterhead, density→Checklist lines. Reuse an existing
doc-style iff Table Rules, Table Fills, Emphasis, Field Style and (Rule Brand pt>0) all equal the
mapping and no Checklist line contradicts it (column count, photo); several matches → family-
prefixed key first, then alphabetical. Else author one new row `<family>-<archetype-slug>`.

**Typeface.** If the modal declared font across the archetype's items is OS/Office-bundled
(Arial, Calibri, Times New Roman, Georgia…), pick the `safe-*` row of that class — that is what
the corpus uses. Else candidates = rows whose heading class and body class (modal variant)
match; pick the lowest Google Fonts `popularity` integer of the Heading Family (metadata/fonts,
fetched once per task). Ties: Embedding Licence installable/editable → matching Category
Contrast → key alphabetical. Scale by medium (deck=projection, infographic=screen, else print):
the chosen row's Scale Key must have that Medium; if not, take the next candidate; if none,
log `scale-gap` and use the family default's typeface row.

**Palette.** Derive each palette's class from its own hexes with the §4 thresholds over
Primary, Secondary, Accent, Rule Brand (0 hues mono, 1 one-accent, ≥2 multi; fill-blocks needs
non-empty Fill-Only Roles). Candidates = class match. Order: provenance class authority >
ranked > convention → one-accent: accent hue bin (8 × 45°) equal to the archetype's modal accent
bin → Foreground/Background ≥4.5:1 and accent ≥4.5:1 (≥3:1 if headline-only) → not an A7 blue
→ key alphabetical. No hex is ever invented; no candidate → `palette-gap`, use the family
default's palette, disclose.

**Reasoning row** `<family>-<archetype-slug>`: the three keys above; bias terms, Doc Conditions
and Severity copied from the family default row; Anti-Pattern Tokens = default's tokens minus
any the archetype legitimately uses (e.g. `multi-column` for a non-ATS 2-column brochure).

## 9. Outputs and merge

Per family, workers ADD only these files:
- `research/designs-evidence/<family>.md` — corpora (URL, query, sort, date, total), raw list
  with metric, coded table, exclusions log, frequency table (k per corpus, shares, combined, K),
  bias statement, second-coder section (sample ids, both codings, A_f, κ), fill decisions with
  tie-breaks applied, Shortfall (if any), library snapshot.
- `research/library/doc-styles/<family>.csv`, `research/library/doc-reasoning/<family>.csv` —
  base column order, new rows only.
- `research/designs/<family>.csv` — designs columns; the **full** ranked list for the family.
- `research/provenance/<family>.csv` — `prov_key` `<table>:<row_key>:<n>`; one row per corpus
  the design occurs in (Source URL = exact query URL, Ranking Metric per §2, Rank Value e.g.
  `0.225 (9/40)`, Fetch `fetched`); new doc-styles/doc-reasoning rows cite the same corpus URL
  with metric `fill-rule:research/82§8`.

**Seeded designs (P1.3a).** Each seeded design of the family must appear exactly once or be
listed as retired: if its reasoning row codes (§4 applied to its own spec) to a shipped
archetype, that archetype reuses the seeded `design_key` and Reasoning Key (no new rows) and
takes the archetype's rank/class. An unmatched seed that is a doctype default stays, placed by
its own evidence (L3 if its rationale cites a fetched authority, else convention — exempt from
the L4 cap, disclosed). An unmatched non-default seed uses the single L4 slot if free; otherwise
it is listed "proposed retirement" in the evidence file and omitted. The orchestrator deletes the
family's seed rows when loading (duplicate keys fail the gate).

No template artwork, text, logos or images are copied; only feature codes and source URLs.

## 10. Per-family sources

`GH(q)` = `https://api.github.com/search/repositories?q=<q>&sort=stars&order=desc&per_page=100`;
`LO(q)` = `https://extensions.libreoffice.org/en/extensions?Tags%5B%5D=118&q=<q>&ord=download_d`;
`MS(c)` = `https://create.microsoft.com/en-us/templates/<c>` (follow redirects);
`NPM(t)` = `https://registry.npmjs.org/-/v1/search?text=<t>&size=250`.

| Family | L1 primary | Second corpus / L2 | L3 to fetch | Expected |
|---|---|---|---|---|
| cv | GH(`resume+template`) | NPM(`jsonresume-theme`) names `^jsonresume-theme-`, metric downloads.monthly; L2 MS(`resumes`) | Europass `https://europass.europa.eu/en/create-europass-cv` | ranked 8-10 (split task) |
| cover-letter | GH(`%22cover+letter+template%22`) (L1 if ≥40 on-topic, else thin→L2) | L2 MS(`cover-letters`) | — | ranked 5-8 |
| deck | NPM(`slidev-theme`) names `slidev-theme-*` | LO Impress `...?Tags%5B%5D=118&Tags%5B%5D=43&ord=download_d`; L2 MS(`presentations`) | — | ranked 8-10 (split task) |
| letter | GH(`%22letter+template%22`) | LO(`letter`) (thin→L2); L2 MS(`letters`) minus newsletters | DIN 5008 via fetched secondary (e.g. Sematre/typst-letter-pro README) | ranked 6-9 |
| memo | none | L2 MS(`memos`); LO(`memo`) corroborate only | GOV.UK content guidance (retry) | 2-5, Shortfall |
| report | GH(`%22report+template%22+NOT+OSCP+NOT+pentest`) | — | ARC/Mercury winners page (mercommawards.com, fetch) | ranked+juried 5-8 |
| whitepaper | none (GH(`whitepaper+template`) 45 total → thin→L2 if ≥10 on-topic) | — | — | 2-5, Shortfall |
| proposal | GH(`proposal+template+latex`) (academic skew, disclose) | — | — | ranked 4-7 |
| invoice | GH(`%22invoice+template%22`) | L2 MS(`invoices`); LO(`invoice`) thin→L2 | — | ranked 7-10 |
| quote | none; cross-listed quote/estimate items from any corpus | one WebSearch `site:create.microsoft.com quote template`, fetch if a category resolves | — | 1-3, Shortfall |
| brochure | none | L2 MS(`brochures`) + LO(`brochure`) coded as one catalogue pool (N≈12) | D&AD Catalogues/Brochures (fetch) | 3-6 |
| flyer | none | L2 MS(`flyers`) | — | 3-6 |
| poster | GH(`%22poster+template%22+latex`) (academic skew) | L2 MS(`posters`) | D&AD Posters (fetch) | ranked 6-9 |
| form | none | none | USWDS `https://designsystem.digital.gov/components/form/`, GOV.UK `https://design-system.service.gov.uk/patterns/` | authority 1-3 |
| one-pager | none | none | — | seeds + 1 convention |
| infographic | none | none | — | seeds + 1 convention |

Fallbacks: Apache OpenOffice templates, Google template gallery, Apple — one WebFetch each; use
only if items and (for L1) a metric come back; else note "unreachable 2026-xx-xx".

## 11. Worked mini-example (cv; hypothetical items, illustrates the rules only)

| Item | Observed | columns | heading | colour | header | rules | density | Admissible |
|---|---|---|---|---|---|---|---|---|
| GH:003 | One column; name 28 pt, declared `Roboto`; full-width rule under name; section heads teal; ~62 lines | 1 | sans (Google SANS_SERIF) | one-accent | ruled (beats plain-centered) | rules | dense | yes |
| GH:007 | Dark-grey sidebar 32% width with photo and five skill bars; serif name | 2-sidebar | serif | fill-blocks (grey ≥10% area) | plain-left | none | standard | **no — C1 multi-column, C3 skill bars** |
| MS:012 | Garamond name left, contact right on same line; dates in a row-aligned left gutter; black only; ~38 lines | 1 (gutter is row-aligned) | serif | mono | split | none | standard | yes |

Archetypes: `1|sans|one-accent|ruled` (K=1 so far), `1|serif|mono|split` (K=1); GH:007 counts in
N_GH but its archetype `2-sidebar|serif|fill-blocks|plain-left` is logged as excluded.
If these were final: share_GH(`1|sans|one-accent|ruled`) = 1/40, share_MS = 0/34, combined =
(0.025+0)/2 = 0.0125.

## 12. Pre-registered falsifiers

- **F1 agreement:** any A_f < 0.80 (identity, variant or admissibility) → rubric amendment and
  full recode (§7); second failure → feature dropped for that family, disclosed.
- **F2 corpus validity:** a claimed L1 with <40 on-topic codeable items is reclassified L2;
  any "k/40" already written for it is withdrawn.
- **F3 metric re-check:** the reviewer re-curls 3 random items per corpus; an item missing or
  a metric off by >10% (or order inverted) rejects the evidence file.
- **F4 recount:** the reviewer recomputes the frequency table and ranks from the coded table;
  any difference rejects the family.
- **F5 fill determinism:** a second worker applying §8 to the archetype table must produce the
  same Style/Palette/Typeface keys; any mismatch → §8 amendment, refill.
- **F6 admissibility at render:** any shipped design whose rendered handoff trips a fail-severity
  preflight constraint for its family is withdrawn and the list re-ranked.
- **F7 schema:** `tests/test_provenance.py` and the loader gate must pass on the added files.
The R3 blind panel judges render quality only; it cannot reorder ranks.

## 13. What this protocol cannot claim

- **Popularity is not quality.** Rank 1 means "most frequent admissible feature signature in
  these corpora on this date", not "best design".
- **Corpora are skewed.** GitHub/npm = developers, LaTeX/Typst/web users, English; LibreOffice =
  cumulative downloads favouring pre-2020 items, European bias; Microsoft Create = Microsoft's
  editorial selection and only its first static slice — prevalence of curation, not usage. The
  mainstream consumer tools (Canva, Google, Behance, Dribbble, Figma) are absent: blocked.
- **L2 is labelled `ranked`** in the schema only because the enum has no prevalence class; the
  Ranking Metric prefix `prevalence:` is the honest marker.
- **A shipped design is a reconstruction**, not the template: four identity features filled
  with our library parts by rule. Typographic finesse, grids, imagery and copy of the source
  templates are not captured.
- **Coding is perception**, bounded only by the 80% agreement gate; singletons are noise.
- **Gap families** (memo, quote, form, one-pager, infographic, whitepaper; brochure/flyer thin)
  will ship short lists; their order carries little or no popularity information.
- Point-in-time: every count is as retrieved on the recorded date.
