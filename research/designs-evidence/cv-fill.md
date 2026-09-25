# cv — F.c filling (research/82 §6, §8, §9)

Follows the pre-registered gate pass recorded in `cv-agreement-r2.md` (header 0.85; density
excluded from filling per the round-1 ruling). Inputs used: `research/82-design-ranking-
protocol.md` §6/§8/§9, `research/82a-cv.md`, `research/82a-clarifications-1..4.md`,
`research/82b-ADOPTED.md`, `research/designs-evidence/cv-header-recode.md` (combined frequency
table, r2a headers), `research/designs-evidence/cv-corpus-github.md` and `cv-corpus-npm-ms.md`
(body class / rules-boxes / photo per item, needed for §8's modal-variant fill and not carried
in the recode file), `research/designs/cv.csv` and `research/provenance/seed-designs.csv`
(seeded designs), and the base library (`typefaces.csv`, `palettes.csv`, `type-scales.csv`,
`doc-styles.csv`, `doc-reasoning.csv`) as it stood at task start, plus a fresh fetch of
`https://fonts.google.com/metadata/fonts` (curl, per §8 "fetched once per task") for Google
Fonts `category`/`popularity`.

Library snapshot at task start: `data/base/typefaces.csv` 34 rows, `palettes.csv` 44 rows,
`type-scales.csv` 82 rows, `doc-styles.csv` 16 rows, `doc-reasoning.csv` 20 rows; no
`research/library/doc-styles/` or `research/library/doc-reasoning/` folders existed yet (cv is
the first family through F.c).

## 1. Rank (§6)

Step 1 (ranked, K>=2, admissible, combined share desc, ties per §6): 14 archetypes qualify
(`cv-header-recode.md`'s admissible-ranking list). Tie-breaks applied (GH is the family's L1
primary corpus per §10, used first for "higher L1 share"):

- `1|sans|mono|plain-left` (GH 0.025/NPM 0.075) vs `1|sans|mono|split` (GH 0.100/NPM 0): GH
  share decides, split ranks above plain-left.
- The eight archetypes tied at combined 0.0250 (K=2 each) were ordered by GH share desc, then
  NPM share desc, then presence-in-corpora, then best native position of either exemplar:
  `1|sans|one-accent|plain-centered` (GH 0.050) > `1|serif|mono|split` (GH 0.050, position
  GH:027 beats GH:040) > `1|sans|one-accent|split` (GH 0.050) > `1|serif|one-accent|
  plain-centered` (GH 0.025, GH:007 beats GH:019) > `1|sans|fill-blocks|plain-left` (GH 0.025)
  > `1|sans|multi|plain-left` (GH 0, NPM position 004 beats 063/067) > `1|serif|one-accent|
  ruled` (GH 0, NPM:063) > `1|sans|one-accent|image-hero` (GH 0, NPM:067).

Step 2 (L3 authority, reserved slots): the family's two fetched authorities are
`cv-us-uk-designed` (Butterick's Practical Typography) and `cv-eu-europass` (europass.europa.eu,
the existing seeded design). Coding each seed's OWN spec against §4 (Style/Palette/Typeface it
already ships):

- `cv-us-uk-designed` -- columns 1 (cv-harvard style), heading serif (Source Serif 4), colour
  one-accent (`cv-harvard` palette, single accent #005ea2), header ruled (`cv-harvard` style
  Rule Brand pt 1, checklist "Reserve the accent rule for the name/header only") -> archetype
  `1|serif|one-accent|ruled`. This is already in the step-1 list (rank tier 0.0250, the lowest
  of the eight-way tie above). Per §6 "an L3 source's design codes to an archetype already in
  step 1, it merges there (extra provenance row, rank unchanged)": `cv-us-uk-designed` KEEPS
  its own design_key and Reasoning Key and occupies that archetype's rank (10th, see §2). It
  remains `cv-uk`/`cv-us`/`cv-generic`'s default Reasoning Key regardless (research/82 §6's
  fitness-default rule) -- forced into the shipped list even though its natural rank position
  (10th of the ranked+L3 set) sits below the 9-slot cap that would otherwise apply (see §2).
- `cv-eu-europass` -- columns 1 (row-aligned label rows are §4's cited exception), heading sans
  (IBM Plex Sans, single multilingual family), colour one-accent (`cv-europass` palette, single
  accent #1a65a6), header plain-left (no header rule; the style's only rule is reserved for
  section-label underscores) -> archetype `1|sans|one-accent|plain-left`. This IS the step-1
  rank-2 archetype (combined 0.100, K=8) -- a clean merge, no forcing needed.

No L3 design produced a NEW archetype outside step 1, so **n_L3 = 0 reserved slots** (§6's
reservation only bites when an L3 archetype is not already ranked); the step-1 cap is
`10 - n_L3 - n_L4 = 10 - 0 - 1 = 9` (see §3 for `n_L4=1`).

Step 3 (ranked singletons, K=1): not needed -- step 1 already gives 14 candidate archetypes,
far more than "<5".

Step 4 (L4 convention, max 1): see §3 below (R1 backlog item b).

## 2. Doctype defaults coded against their own spec (mechanical, same §4 procedure)

- `cv-ats-strict` -- `cv-restrained` style (Table Rules none, Emphasis weight, Rule Brand 0),
  `mono-ink` palette (no accent), `safe-sans-arial` typeface (Arial, sans/sans), no header rule
  -> archetype `1|sans|mono|plain-left`. This matches the step-1 archetype at combined 0.050
  (K=4, GH:036 + NPM:028/040/080) exactly (Table Rules/Fills/Emphasis/FieldStyle/RuleBrand>0 all
  equal what §8 would compute for that archetype from scratch -- confirmed by hand before
  writing any new row). `cv-ats-strict` MERGES there too: same treatment as the two authority
  merges above, no new library rows, keeps its own design_key/Reasoning Key, and (being the
  fitness default for `cv-dach`/`cv-france`/`cv-gulf-gcc`) is never demoted regardless of its
  numeric rank (5th).
- `cv-academic` -- `cv-academic-plain` style (Table Rules none), `mono-ink` palette,
  `safe-serif-times` typeface (serif/serif), no header rule -> archetype
  `1|serif|mono|plain-left`. This is a K=1 SINGLETON in the coded data (GH:068 only, admissible)
  -- not K>=2, so it does not match any step-1 archetype. Per §9, an unmatched seed that is a
  doctype default (here, `cv-academic`'s own doctype) stays, placed by its own evidence: no
  fetched authority backs "academic CV, no page limit" as a layout, so it stays **convention**,
  exempt from the L4 cap, disclosed here. (Its Evidence Class was already `convention` in the
  seed -- unchanged.)

## 3. R1 backlog (b): re-classing `cv-dach-tabular` and `cv-editorial`

Both seeds' "authority" claims cited Typewolf FONT-PAIRING pages (`typewolf.com/pt-serif`,
`typewolf.com/fraunces`), which carry zero layout information -- no page, column, header or
colour-use evidence at all. Per the task brief, each is re-coded from what ITS OWN doc-styles/
doc-reasoning rows actually specify (the only real "layout evidence" that exists for either),
and matched against the step-1 archetype table:

- `cv-dach-tabular` -- `cv-dach-tabular` style: the ~35mm label / remainder content table with
  row padding (not cell borders) is §4's own named exception ("a hanging label/date gutter
  whose entries align row-by-row with the content is `1`") -> columns 1, NOT 2-sidebar. Heading
  serif (PT Serif), colour mono (`cv-dach-formal` palette has no Accent hex at all), header
  plain-left (Rule Brand pt 0, no rule text in the checklist; the 4.5x6cm photo is an avatar,
  not a hero, per §4's explicit CV carve-out) -> archetype `1|serif|mono|plain-left`. This is
  the SAME singleton archetype as `cv-academic` above (K=1, GH:068) -- still not K>=2, so no
  match to a step-1 archetype.
- `cv-editorial` -- `cv-editorial` style/palette/typeface (Fraunces + Work Sans, one Carbon-Blue
  accent restricted to headline size, Rule Brand pt 1.5): columns 1, heading serif (Fraunces'
  Google Fonts `category` is confirmed **Serif**, not Display, by the live fetch -- the style's
  "expressive display serif" is a descriptive label, not the taxonomy class), colour one-accent,
  header ruled (Rule Brand pt 1.5 > 0, the only style attribute that locates a header treatment)
  -> archetype `1|serif|one-accent|ruled`. This IS a step-1 archetype (K=2, the same one
  `cv-us-uk-designed` already merges into, see §1) -- so `cv-editorial` ALSO matches it.

Two seeds cannot both occupy the same merged archetype slot (§9 gives one design_key per
archetype). `cv-us-uk-designed` wins that slot because it is a DOCTYPE DEFAULT (three doctypes
point at it) and per §6 a default is "never changed and never promoted... keeps its place" --
i.e. it has first claim on whatever archetype it codes to. `cv-editorial` is not a default, so
it falls back to §9's unmatched-non-default path: "uses the single L4 slot if free; otherwise
listed 'proposed retirement' and omitted."

Neither `cv-dach-tabular` nor `cv-editorial` matched a K>=2 archetype (dach-tabular is an
unmatched singleton; editorial's only match was taken by the default), so **both are candidates
for the single non-default L4 convention slot**, and only one can ship. Tie-break (not specified
by §9 beyond "the single L4 slot"): `cv-dach-tabular` names a real, independently documented
cultural convention (the German/Austrian/Swiss tabellarischer Lebenslauf, described in HR/
careers-office literature as a named format) -- it is a convention in the ordinary sense of the
word. "Editorial CV" names no external convention at all; it is this product's own aesthetic
category with no documented prevalence anywhere the family's sources reach. Per L4's definition
in §2 ("Convention -- no metric, presence [of a recognised convention]"), `cv-dach-tabular` is
the more defensible occupant of the one slot.

**Disposition:** `cv-dach-tabular` re-classed `authority` -> `convention`, takes the family's
single non-default L4 slot (rank 12, last, per the R1 backlog's rule (a) that convention ranks
after every non-convention design). `cv-editorial` is **retired** -- proposed-retirement per
§9, omitted from `research/designs/cv.csv`; its doc-reasoning/doc-styles/palette/typeface rows
are left in the base library untouched (no design currently points at them; `Design Key` on
that doc-reasoning row is correctly blank after the next `load-base.py` run, same as any
reasoning row no design cites). Its seed provenance row (`designs:cv-editorial:1`, Typewolf
Fraunces page) is dropped from `research/provenance/seed-designs.csv` along with the other five
now-superseded cv seed provenance rows (merged by key into `research/provenance/cv.csv`, or
genuinely retired for `cv-editorial`).

## 4. Full rank order (14 candidate archetypes, cap 10 "ranked" + exempt defaults)

Cap accounting: step-1 cap = 9 (10 - 0 L3-reserved - 1 L4). Filling ranks 1-9 from the ordered
archetype list in §1 exhausts the six clear archetypes (0.125 down to 0.0375) plus the three
highest of the eight-way 0.025 tie (`1|sans|one-accent|plain-centered`, `1|serif|mono|split`,
`1|sans|one-accent|split`). The tenth position is `cv-us-uk-designed`'s merged archetype
(`1|serif|one-accent|ruled`, the LOWEST of the eight-way tie) -- it would not make the 9-slot
cap on rank alone, but ships anyway because a doctype default is never omitted (research/82 §6);
this is the same principle that already exempts `cv-academic`/`cv-dach-tabular` from the L4 cap,
applied here to the ranked cap. Total shipped: **12** (10 ranked/authority + 2 exempt-convention
defaults), inside the protocol's stated cap of 10 for the cap's core meaning ("popularity-
ordered slots") with the family's mandatory defaults added on top and clearly disclosed, per
the same logic that already lets an unmatched default bypass the L4 cap.

| Rank | design_key | Archetype | Evidence Class | Combined share (K) |
|---|---|---|---|---|
| 1 | cv-serif-plain-centered | `1|serif|mono|plain-centered` | ranked | 0.1250 (K=10) |
| 2 | cv-eu-europass (merge) | `1|sans|one-accent|plain-left` | authority | 0.1000 (K=8) |
| 3 | cv-sans-accent-ruled | `1|sans|one-accent|ruled` | ranked | 0.0750 (K=6) |
| 4 | cv-sans-mono-split | `1|sans|mono|split` | ranked | 0.0500 (K=4) |
| 5 | cv-ats-strict (merge) | `1|sans|mono|plain-left` | ranked | 0.0500 (K=4) |
| 6 | cv-serif-accent-plain-left | `1|serif|one-accent|plain-left` | ranked | 0.0375 (K=3) |
| 7 | cv-sans-accent-plain-centered | `1|sans|one-accent|plain-centered` | ranked | 0.0250 (K=2) |
| 8 | cv-serif-mono-split | `1|serif|mono|split` | ranked | 0.0250 (K=2) |
| 9 | cv-sans-accent-split | `1|sans|one-accent|split` | ranked | 0.0250 (K=2) |
| 10 | cv-us-uk-designed (merge, default) | `1|serif|one-accent|ruled` | authority | 0.0250 (K=2) |
| 11 | cv-academic (default, exempt) | (K=1 singleton, own spec) | convention | n/a |
| 12 | cv-dach-tabular (exempt L4 slot) | (K=1 singleton, own spec) | convention | n/a |

Retired: `cv-editorial` (see §3).

Floor 5 / target 8-10: met (10 ranked+authority slots, 12 shipped total). No Shortfall section
needed.

## 5. Filling by rule (§8), tie-breaks logged

Google Fonts metadata fetched once (`https://fonts.google.com/metadata/fonts`, curl,
2026-09-24) for `category`/`popularity` of every candidate Heading Family. Confirmed categories
relevant here: Source Serif 4/PT Serif/Fraunces = Serif; IBM Plex Sans/Roboto/Open Sans/Inter/
Public Sans = Sans Serif. Popularity integers used below: Roboto 2, Open Sans 3, Inter 5,
Montserrat 7, Poppins 8, Lato 9, Noto Sans 20, IBM Plex Sans 53, Public Sans 86 (lower = more
popular).

No per-item hex swatches exist in the coded corpora (only categorical `one-accent`/`mono`/
`multi`/`fill-blocks` enums, per research/82 §4's rubric) -- §8's palette tie-break "accent hue
bin equal to the archetype's modal accent bin" cannot be computed from this evidence and is
disclosed as inapplicable for every one-accent archetype below; the fallback tie-break
(provenance class authority > ranked > convention, then contrast, then key alphabetical) is
used throughout, which mechanically converges every plain one-accent archetype on the same
palette (`lib-atlassian-ink`, the alphabetically-first AUTHORITY one-accent palette that clears
4.5:1 on both text and accent and is not an A7 blue) and every plain mono archetype on the same
palette (`lib-carbon-mono`, the only AUTHORITY mono palette). This is disclosed, not hidden --
it is what "no taste" mechanically produces when the missing evidence (hex swatches) can't
discriminate further.

### Rank 1 -- `1|serif|mono|plain-centered` (new: cv-serif-plain-centered)

- Modal body (10 exemplars GH:003/008/009/023/038/042/071/076, NPM:003/027): serif, 9/10 (GH:071
  is the lone sans-body outlier). Modal rules/boxes: `rules` (majority). Modal photo: `no` (all).
- Style: rules->hairline (cv branch); colour mono->weight; header plain-centered->Rule Brand 0;
  photo no->"Omit photo". No existing row matches (cv-restrained/cv-academic-plain have Table
  Rules `none`; cv-europass/cv-harvard/cv-editorial have Rule Brand pt>0). New row authored.
- Typeface: heading serif + body serif (both fields must be the SAME category) -- only
  `safe-serif-times` and `safe-serif-georgia` qualify (every "pairing" row in the library pairs
  a serif heading with a SANS body, none offer serif+serif). Tie: Embedding Licence tied
  (editable), Category Contrast tied (serif-serif) -> key alphabetical: `safe-serif-georgia`.
- Palette: colour mono -> candidates `mono-ink`, `cv-dach-formal`, `lib-carbon-mono`
  (authority). Authority wins outright -> `lib-carbon-mono`.

### Rank 2 -- merge, cv-eu-europass (no new rows; see §1)

### Rank 3 -- `1|sans|one-accent|ruled` (new: cv-sans-accent-ruled)

- 6 exemplars (NPM:038[x]/044/054[x]/069/075/083), all body sans. rules/boxes tied 3 boxes /
  3 rules -> tie-break "highest-metric exemplar": NPM:038 has the highest downloads.monthly
  (142) of the six and codes `boxes` -> modal = boxes. Photo: no (6/6).
- Style: boxes->hairline + Checklist "Border at most half of the blocks"; colour one-accent->
  weight; header ruled->Rule Brand pt 1. This signature (hairline/none/weight/none/RuleBrand>0)
  matches the EXISTING `cv-europass` row exactly (no contradiction on column count or photo --
  Europass's own checklist makes photo conditional, not a hard omit) -> **reused**, no new style
  row.
- Typeface: heading sans + body sans (single-family or matched-category candidates): lowest
  popularity = Roboto (2) -> `lib-roboto`.
- Palette: one-accent -> `lib-atlassian-ink` (see disclosed fallback above).

### Rank 4 -- `1|sans|mono|split` (new: cv-sans-mono-split)

- 4 exemplars (GH:010/047/055/066), all body sans, all rules=rules. Photo tied 2/2 (010, 066
  yes; 047, 055 no) -> highest-metric exemplar GH:010 (2311 stars, the highest of the four) has
  photo=yes -> modal photo = yes.
- Style: rules->hairline; colour mono->weight; header split->Rule Brand 0; photo yes->"Photo
  permitted as a modest avatar, not a hero image" (no "omit photo" line). No existing row
  matches (same hairline/weight/RuleBrand0 signature as rank 1's new row, but rank 1's checklist
  says "omit photo", which the photo=yes archetype would contradict) -> new row authored.
- Typeface: sans/sans -> `lib-roboto` again (same mechanical outcome as rank 3; disclosed).
- Palette: mono -> `lib-carbon-mono` (same as rank 1; disclosed).

### Rank 5 -- merge, cv-ats-strict (no new rows; see §2)

### Rank 6 -- `1|serif|one-accent|plain-left` (new: cv-serif-accent-plain-left)

- 3 exemplars (GH:041/065, NPM:058), all body serif. rules/boxes: none/rules/none -> modal none
  (2/3). Photo: no (3/3).
- Style: rules-none->Table Rules none; colour one-accent->weight; header plain-left->RuleBrand
  0; photo no->omit photo. Matches `cv-restrained` EXACTLY (none/none/weight/none/RuleBrand0,
  no checklist contradiction on columns or photo) -> **reused**.
- Typeface: serif+serif -> `safe-serif-georgia` (same tie-break as rank 1).
- Palette: one-accent -> `lib-atlassian-ink`.

### Rank 7 -- `1|sans|one-accent|plain-centered` (new: cv-sans-accent-plain-centered)

- 2 exemplars (GH:001, GH:077), both body sans, both rules=rules, both photo=no.
- Style: rules->hairline; colour one-accent->weight; header plain-centered->RuleBrand 0; photo
  no->omit photo. No existing base row matches (cv-europass has RuleBrand pt 1, not 0) -> new
  row authored (this is the row later reused by ranks 8 and 9 below).
- Typeface: sans/sans -> `lib-roboto`.
- Palette: one-accent -> `lib-atlassian-ink`.

### Rank 8 -- `1|serif|mono|split` (new: cv-serif-mono-split)

- 2 exemplars (GH:027, GH:057), both body serif, both rules=rules, both photo=no.
- Style: rules->hairline; colour mono->weight (mono maps to `weight` the same as one-accent);
  header split->RuleBrand 0; photo no->omit photo. Numeric signature identical to rank 7's new
  row AND no checklist contradiction (both photo=no) -> **reused** `cv-sans-accent-plain-
  centered`'s style row (a mono/plain-centered-authored row serving a serif/split archetype is
  exactly what "reuse iff the five mapped fields and checklist agree" intends -- the row's own
  key name is a naming artifact of whichever archetype authored it first, not a constraint on
  reuse).
- Typeface: serif+serif -> `safe-serif-georgia`.
- Palette: mono -> `lib-carbon-mono`.

### Rank 9 -- `1|sans|one-accent|split` (new: cv-sans-accent-split)

- 2 exemplars (GH:040, GH:061), both body sans, both rules=rules. Photo tied 1/1 (040 yes, 061
  no) -> highest-metric exemplar GH:040 (544 stars > GH:061's 274) has photo=yes -> modal=yes.
- Style: rules->hairline; colour one-accent->weight; header split->RuleBrand 0; photo yes->
  "photo permitted" (no omit-photo line). Numeric signature identical to rank 4's new row AND
  matching photo=yes (no contradiction) -> **reused** `cv-sans-mono-split`'s style row.
- Typeface: sans/sans -> `lib-roboto`.
- Palette: one-accent -> `lib-atlassian-ink`.

### Rank 10 -- merge, cv-us-uk-designed (no new rows; see §1)

Net new doc-styles rows: **3** (`cv-serif-plain-centered`, `cv-sans-mono-split`,
`cv-sans-accent-plain-centered`), reused 3 times each by one further archetype (ranks 6/8 and
3, plus base row reuse at rank 3/6). Net new doc-reasoning rows: **7** (one per new design_key
above; bias terms/Doc Conditions/Severity copied verbatim from the family default row
`cv-ats-strict` per §8's literal instruction -- disclosed as a known mechanical artifact: the
copied Palette/Typeface Bias Terms prose describes `cv-ats-strict`'s own choices, not the
archetype's actual resolved palette/typeface, exactly as §8 specifies "copied from the family
default row" with no re-derivation step. Anti-Pattern Tokens = default's tokens minus `photo`
wherever the archetype's own modal photo is `yes` (ranks 4 and 9).

## 6. Outputs

- `research/library/doc-styles/cv.csv` -- 3 new rows.
- `research/library/doc-reasoning/cv.csv` -- 7 new rows.
- `research/designs/cv.csv` -- full 12-row ranked list, replaces the 6-row seed.
- `research/provenance/cv.csv` -- 28 rows: per-corpus share rows for every ranked/merged
  design that has GH/NPM support, the two carried-forward authority citations (Butterick,
  Europass), two convention rows (blank Source/Fetch), and `fill-rule:research/82§8` rows for
  the 3 new doc-styles + 7 new doc-reasoning rows (Rank Value `n/a (fill-rule, not a ranking)`
  since §8 fill decisions carry no ranking number, only a rule citation).
- `research/provenance/seed-designs.csv` -- the 6 cv seed rows removed (merged by key into
  `cv.csv`, or genuinely retired for `cv-editorial`).
- `research/load-base.py` -- `cv.csv` added to `LIBRARY_INPUTS_ENABLED` and
  `PROVENANCE_INPUTS_ENABLED`.
- `skill/document-design-intelligence/scripts/tests/test_designs.py` -- Rule 6's
  `expectedFailure` removed (R1 backlog item a): cv's two convention designs now rank 11-12,
  last in the family, so the rule is a real passing assertion for every family, not an
  acknowledged-broken one.
- Fixture updates in `test_ddi.py`, `test_r2_fixes.py`, `test_make_brand_kit.py`,
  `test_resolve.py`, `research/p65/test_score.py`: every hardcoded reference to the retired
  `cv-editorial` design_key repointed to a still-shipping cv design (`cv-ats-strict`,
  `cv-dach-tabular`, `cv-eu-europass`, or the new `cv-serif-plain-centered`, chosen per test to
  preserve that test's original intent -- e.g. a design whose Style/Palette/Typeface differ
  from the doctype's own default, or whose palette carries a specific hex the test needs);
  "6 authored designs" / "rank N of 6" updated to "12 authored designs" / "rank N of 12", and
  `cv-us-uk-designed`'s own line updated from "rank 1 of 6" to "rank 10 of 12" (it now merges
  into a lower-ranked archetype, per §1, while remaining `cv-uk`'s default). One test
  (`test_r2_fixes.py::test_all_doc_term_does_not_reorder`) compared design **ranks as strings**
  (`sorted(x["rank"] for x in ...)`), which happened to work by coincidence while cv had <=9
  designs; fixed to sort numerically, since a 12-design family exposes the pre-existing bug
  (`"10" < "2"` lexicographically).

## 7. Shortfall

None -- 10 ranked/authority + 2 exempt-convention defaults comfortably clears the 8-10 target
and the floor of 5.

## 8. Verification (2026-09-24)

- `python3 research/load-base.py` -- OK, designs 27 rows (was 15 before the exempt cv-editorial
  seed rows and 6-row cv seed were replaced by 12), provenance 240 rows loaded including
  `cv.csv`, no duplicate-key exits.
- `python3 research/build-portable.py` -- OK, `portable/DDI-LIBRARY.md` rebuilt (171497 chars).
- `python3 scripts/ddi.py check` -- `OK: validated 16 table(s), 874 row(s)`.
- `python3 -m pytest -q` (repo root) -- **321 passed, 1 skipped, 1760 subtests passed, 0
  failures**.
- `python3 scripts/ddi.py designs --doctype cv-uk` -- lists all 12 designs in rank order with
  resolved style/palette/typeface (see transcript kept alongside this file's authoring session;
  rank 1 = `cv-serif-plain-centered`, rank 10 = `cv-us-uk-designed [DEFAULT for this doctype]`).
- `python3 scripts/resolve.py --doctype cv-uk --design cv-serif-plain-centered --json` +
  `python3 scripts/ddi.py handoff --json <resolved> --format docx` -- resolves cleanly; handoff
  shows `design: CV, serif centered (rank 1 of 12, ranked)`, fonts `Georgia / Georgia` (the
  `safe-serif-georgia` safe stack), palette `Primary #161616 / Foreground #161616` (the
  `lib-carbon-mono` authority palette, monochrome as coded), and the new doc-style's Checklist
  verbatim.


## Correction -- corrected 2026-09-25: print scale

The three serif-heading cv reasoning rows first shipped with `safe-serif-georgia`
(`cv-serif-plain-centered`, `cv-serif-accent-plain-left`, `cv-serif-mono-split`). Rank 1's typeface
paragraph above reads "tie ... -> key alphabetical: `safe-serif-georgia`", but section 8 also requires
that the chosen typeface's Scale Key "must have that Medium" (print for cv), and
`safe-serif-georgia`'s Scale Key is `report-screen` (medium `screen`; it also carries only a `body`
row). The medium rule comes before the tie-break, so the print-scaled serif+serif row is chosen:
**`safe-serif-times`** (Scale Key `report-print`, medium print). Diff (research/library/doc-reasoning/
cv.csv, three lines, `Typeface Key` only): `safe-serif-georgia` -> `safe-serif-times` for those three
rows; nothing else in the cv outputs changes (styles, palettes, designs, provenance are byte-identical).
`fill_family.py --family cv` now derives the same typeface from the rules (`propose_typeface`, medium
rule) and `test_fill_family.py` asserts it. Found while filling `proposal` (proposal-fill.md section 5).
