# T1 doctypes draft — notes (research/26-t1-doctypes-draft.csv)

## UPDATE 2 (Revision 3) — the deck Reasoning Key split is WITHDRAWN, ruled, do not relitigate

`09-library-schema.md`'s Revision 3 CONDITION PLACEMENT ruling (lines 569-586, 2265-2278)
resolves the exact gap flagged below in "Doc Conditions — guidance for whoever authors the
linked T2 rows": **`if_projected` is deleted from `DOC_CONDITION_SIGNALS` outright**, and
the interim fix this file originally shipped (splitting `deck-generic` into
`deck-projection` / `deck-screen` / `deck-handout` so `if_projected` could target the
projected variant alone) is **withdrawn as the wrong answer**, not refined. The admission
test that replaced it: *a condition is admissible only if its truth value is not determined
by the resolved T1 row.* Viewing context is exactly the axis the three deck doctypes already
split on in `Constraint Set Keys` (`projection` / `screen` / empty, unchanged by this
revert), so a Doc Condition restating that fact is a condition whose value is a constant —
not a condition. `slide-deck-projection` still reaches `proj-body-floor` etc. through its
own `Constraint Set Keys=projection`, independent of anything on T2.

**Applied here:** all three `slide-deck-*` rows' `Reasoning Key` reverted to `deck-generic`
(was `deck-projection` / `deck-screen` / `deck-handout`). Nothing else in this file changed —
`Constraint Set Keys` (`projection`/`screen`/empty) were already differentiated before the
split and stay that way; the split and its withdrawal were always a T2 (`Doc Conditions`)
question, not a T1 one. See `research/29-t2-doc-reasoning-draft.csv`'s `deck-generic` row for
the merged T2 side and the trade-off the merge accepts (handout inherits the same
Style/Palette/Typeface as the projected/screen variants). Condition vocabulary is now four
keys, not five: `if_hand_filled`, `if_photocopied`, `if_ats_target`, `if_professional_print`
survive the same admission test; only `if_projected` failed it.

## UPDATE (T2/T6 authoring pass) — two rulings applied, resolving prior open items

**`ens-web-tool` dropped. 34 rows now, not 35.** The conflict flagged below ("a direct
conflict with an earlier design decision") is resolved in favour of T4's exclusion: the
schema explicitly excludes web tools from this document library
(`09-library-schema.md:639-640`, the `colors.csv` `Destructive` discussion — *"a web-tool
is not a document. That doctype stays with upstream's skill."*), and consistency with the
rest of the schema wins over matching the task's literal five-row headcount. ENS's set is
now four rows (`ens-note-interne`, `ens-formulaire`, `ens-social`, `ens-slides`), all still
present. `ens-web-tool`'s web-tool rules stay in ENS's own plugin, per the ruling.

**The three deck rows now have distinct `Reasoning Key`s, resolving the sharing problem
flagged below.** `slide-deck-projection` → `deck-projection`, `slide-deck-document` →
`deck-screen`, `slide-deck-handout` → `deck-handout` (was `deck-generic` on all three).
This is exactly the fix the note below asked for: `Doc Conditions` is keyed by
`doc_category`, and three rows sharing one key meant `if_projected` would have fired on
the screen-read and handout variants too. The three new T2 rows (`research/29`) keep
identical `Style Key` / `Palette Key` / `Typeface Key` where the design payload is genuinely
shared (preserving the economy the original single-key choice was going for) and differ
**only** in `Doc Conditions` — `if_projected` fires on `deck-projection` alone.

Worth noting: T1's own `Constraint Set Keys` column for these three rows was **already**
differentiated before this pass (`projection` / `screen` / empty respectively) — the sharing
defect was specific to T2's `Doc Conditions`, not to T1. See `research/29-notes.md` for the
full T1×T9 cross-check this pass ran.

35 rows (now 34 after the drop): 30 generic + the ENS four (was five). Validated with
`csv.reader` — 11 columns matching Rev 2's exact T1 header, no row-length mismatches, no
duplicate `doc_key`s. Read `09-library-schema.md` in full for T1/T2/T12/§0.3/§3 before
drafting — citations below point at the specific lines that shaped a decision.

## Row count: 34 (originally 35 before the `ens-web-tool` drop), not 40-60 — stated as a finding

Every class the task listed got at least one row, several got sourced, structurally
distinct sub-variants beyond what was literally asked (region CV split into 7 + 2, brochure
into 5 by fold-type × paper-size, slide deck into 3 by viewing context). I stopped adding
rows once I ran out of *structurally distinct* variants — no second CV row for "early
career" (that's `T12`'s `Seniority Band`, computed at validation time, explicitly **not**
a T1 routing key per the design notes at `09-library-schema.md` line ~386: *"Seniority Band
is deliberately not a column here... it is a lookup axis into T12 supplied at validation
time, not a routing key authored per row"*), no gate-fold A4/Letter split (I have sourced
fold-geometry differences for tri-fold across paper sizes, report 03, but not for
gate-fold specifically — inventing one would repeat the exact unsourced-threshold mistake
flagged repeatedly across this project). Landing under target with every additional row
genuinely earning its place, per the project's own recurring standard (T9: 38 rows vs.
80-120, stated as a finding not a failure; T11's `Min Physical Size mm` left blank rather
than invented) rather than padding to hit a number.

## Keyword strategy — what wins BM25 and why

BM25 rewards **term rarity across the corpus**, not just presence — a token every row
shares (`document`, `create`) contributes almost nothing to ranking; a token only 1-2 rows
carry does the actual disambiguating work. Every row's `Keywords` cell was built around
2-4 **distinctive** tokens specific to that row, with common-genre tokens (`cv`, `rapport`,
`présentation`) included because a real query will use them, but not relied on alone:

- **CV region rows** carry the region's own vocabulary as the distinguishing signal:
  `cv-dach` gets `tabellarischer lebenslauf` and `bewerbungsunterlagen` (terms that don't
  appear in any other CV row); `cv-gulf-gcc` gets `uae`, `dubai`, `saudi`, `qatar`;
  `cv-eu-europass` gets the literal `europass` token, which is unique to that one row and
  therefore does all the disambiguating work by itself. `cv-us` deliberately leads with
  **`resume`** ahead of `cv` — in US usage the two terms aren't synonyms the way they are
  in UK/EU English (`cv` in a US context usually means the unlimited-length academic
  document, which is exactly why `cv-academic` exists as its own row — see below) — and
  `cv-generic`'s keywords are intentionally the *thinnest* in the whole CV group, holding
  only the bare, region-agnostic terms. That's a deliberate, load-bearing choice, not an
  oversight — see the `fais-moi un cv` test case (F3) below for why it's also a real risk.
- **Verb phrases, not just nouns.** Every row carries at least one "make me / write /
  turn this into"-style phrase in each language actually likely to produce it: `fais-moi
  une note interne`, `rédige mon cv`, `erstelle einen lebenslauf`, `write my resume`. These
  match the way a real user opens a request far better than a noun list alone — report 03's
  own research never covered this, this is pure BM25-mechanics reasoning specific to how
  the resolver works (`01-mechanism.md`'s BM25-over-`search_cols` design, referenced at
  `09-library-schema.md` line 72).
- **Distinctive multi-word phrases deliberately over single words** where the phrase is
  the actual differentiator: `table des matières` (only on `report-long-toc`, not
  `report-short`), `leave-behind` (only on `slide-deck-handout`), `tabular invoice` (only
  on `invoice-tabular`). A single shared word (`report`, `deck`) can't do this; the phrase
  can.
- **Rows I deliberately kept keyword-overlapping, as a test fixture, not an accident:**
  `ens-note-interne` and `memo-internal` both carry `note interne` and `fais-moi une note
  interne` — this is the schema's own worked example (`09-library-schema.md` §3, request
  *"fais-moi une note interne sur les congés"*), and the overlap is exactly what makes that
  query a real test of the **brand two-pass** (§0.3): with ENS active it should resolve to
  `ens-note-interne`; on the generic-only fallback path it should resolve to `memo-internal`.
  Same overlap, deliberately, on `slide-deck-projection` / `slide-deck-document` /
  `ens-slides` around the bare word `présentation` — see D3 below, a genuine ambiguous case
  I did not paper over with a stronger keyword, because the ambiguity is real: "erstelle
  eine präsentation" alone genuinely doesn't say projected-live vs. read-alone vs. ENS-branded.

## The `cv-generic` risk, stated plainly

`cv-generic` exists so a region-less query has somewhere honest to land instead of the
resolver guessing a region from nothing. But BM25 scores on term overlap, and
`cv-generic`'s keyword list is *deliberately thin* (by design — it shouldn't carry region
tokens it doesn't represent) while the seven regional rows are keyword-dense. A bare query
like "fais-moi un cv" could plausibly score similarly across several rows rather than
clearly favouring the thin generic one. This is not a bug I can fix with more keywords
(padding `cv-generic`'s row with generic terms just reproduces the ambiguity elsewhere) —
it is a real property of a BM25-only resolution step, and it's exactly why T1's own design
notes describe the fuzzy step as one that **"abstains rather than guessing when confidence
is low"** (`09-library-schema.md` line ~378). Test case F3 below is built to surface this,
not to hide it.

## Doc Conditions — guidance for whoever authors the linked T2 rows (not authored here)

T1 doesn't carry `Doc Conditions` itself — that column lives on **T2** (`doc-reasoning.csv`),
keyed by the `Reasoning Key` each T1 row points at. I don't own T2 authorship in this task,
but every `Reasoning Key` I invented is a real forward-reference, so here is what I'd expect
attached, using **only** the closed `DOC_CONDITION_SIGNALS` vocabulary quoted from T2's
design notes (`09-library-schema.md` lines 441-442) — `if_hand_filled`, `if_photocopied`,
`if_projected`, `if_ats_target`, `if_professional_print`. **No other key exists; inventing
one crashes the parser by design (line 446), so I did not.**

| Reasoning Key (mine) | Expected Doc Condition(s) | Signal source |
|---|---|---|
| `cv-ats-strict`, `cv-academic` | `if_ats_target` -> `constraint:ats-strict` | context |
| `form-handfilled`, `ens-formulaire` | `if_hand_filled` -> `constraint:field-underline-only` (or whatever T3 names its field style); `if_photocopied` -> `constraint:photocopy-safe-color` | `if_hand_filled` is context (a form doctype is always hand-fillable by construction); `if_photocopied` is **intent** (nothing in the library knows a specific copy will actually be photocopied — same distinction T2's own design notes make for `ens-note-interne`, line ~465) |
| `ens-office-document` | `if_photocopied` -> `constraint:photocopy-safe-color` | intent (matches the worked example exactly, §3) |
| `print-marketing` (all 5 brochure rows + poster) | `if_professional_print` -> `constraint:print-legibility-l-delta` | context (T7's `Print Mode` already says professional; this is a resolved-context fact, not a guess) |
| `deck-generic`, `ens-slides` | `if_projected` -> `constraint:proj-body-floor` | context, but **only for the `slide-deck-projection` doctype specifically** — `slide-deck-document` and `slide-deck-handout` share the same `Reasoning Key` (`deck-generic`) but should *not* fire `if_projected`, since they're explicitly not projected. This is a real gap: `Doc Conditions` is keyed by `doc_category` (i.e. by `Reasoning Key`), and I gave all three deck rows the *same* `Reasoning Key` for style/palette/typeface economy — which means, as authored, they'd also share the same `Doc Conditions`, silently making `slide-deck-document` and `-handout` fire a projection constraint they shouldn't. **Flagging this now rather than at review**: either the three deck rows need distinct `Reasoning Key`s after all (defeating the economy I was going for), or `if_projected`'s signal source needs to check something *outside* `doc_category` (e.g. the resolved `Render Target`/`Constraint Set Keys`, which do already differ per deck row) so one `doc_category` can still branch correctly. Not resolved here — this is a T2-authoring decision, not mine to make unilaterally, but it's a real interaction between my T1 choices and T2's existing design I'd be withholding if I didn't say so. |

## Where T1's design forced a real classification call

- **`Artifact Class: hybrid`, used twice, deliberately.** `slide-deck-handout` (dense,
  meant to be read without a presenter — closer to a flow document in reading pattern
  despite being a `.pptx`) and `ens-web-tool` (a scrollable, non-paginated, non-fixed-frame
  dashboard) are both genuinely neither `canvas` (one fixed frame) nor `flow` (paginated).
  T1's `Artifact Class` enum names `hybrid` as a third value but I found no worked example
  of it anywhere in the schema doc before this — these are, as far as I can tell, the
  first two rows to actually use it.
- **`ens-web-tool` — a direct conflict with an earlier design decision, flagged loudly,
  now resolved: DROPPED.** The task originally asked for all five ENS rows including
  `web-tool`. But T4's own design notes (`09-library-schema.md`, the `colors.csv`
  dropped-columns discussion) say explicitly: *"Cutting `Destructive` costs us ENS's
  `web-tool` type — deliberate: this is a document library, and a web-tool is not a
  document. That doctype stays with upstream's skill."* That is a direct, stated exclusion
  of exactly this doctype from this library, made earlier in the same schema document I was
  told to treat as authoritative. I originally included the row anyway with a visibly
  thinner payload (no `Structure Key`, no `Page Format Key`, placeholder `Render Target`)
  and left the conflict for whoever owned the scope decision. **Ruling applied in the T2/T6
  authoring pass: T4's exclusion stands. The row is dropped; the ENS set is four rows, not
  five. Consistency with the schema wins over matching the task's literal headcount.**

## Forward-referenced foreign keys — not verified-existing rows

Every `Reasoning Key`, `Page Format Key`, `Structure Key`, and most `Constraint Set Keys`
values I used for the 30 generic rows are **proposed slugs**, not confirmed rows in
T2/T7/T9/T10 — those tables aren't fully authored for these document classes yet. Two
exceptions I deliberately reused rather than inventing, because they're already real,
adopted rows: `print-marketing` / `letter-trifold` / `brochure-3panel` /
`pdf-weasyprint-pdfx4;pdf-chromium` / `professional-print` for `brochure-trifold-letter`
is copied **exactly** from T1's own given example row (`09-library-schema.md` line ~361),
and `cv-ats-strict` / `a4-cv-single-col` / `pdf-chromium;docx-office` for the CV rows
matches the given `cv-uk-2page` example. Everything else — `memo-internal`,
`form-handfilled`, `report-classic`, `whitepaper-formal`, `deck-generic`,
`infographic-scaffold`, and the rest — is my own naming, chosen for consistency, not
verified against an authored T2/T7/T9/T10 row. **Two render-target placeholders don't exist
in T8 at all yet**: `png-chromium` (for `social` and `infographic`'s PNG output) and
`html-export` (for `web-tool` and the screen-read/handout deck variants) — T8's authored
rows only cover `pdf-*`, `docx-office`, `pptx-office` per what I read; `png`/`html` are
named in T8's `Format` enum but I found no actual row for either.

## Region key slugs — my own derivation, not independently confirmed

T12's own documentation gives exactly one example `region_key` value (`uk`). The other six
are my own slugification of the region names I chose in `18-cv-region-rules.csv` (`US`,
`UK`, `EU-generic`, `EU-Europass`, `DACH`, `France`, `Gulf-GCC`) into lowercase-hyphen
slugs: `us`, `uk`, `eu-generic`, `eu-europass`, `dach`, `france`, `gulf-gcc`. If whoever
authored T12's actual rows slugged them differently, every `Region Key` value in the CV
rows here needs a find-and-replace, not a re-think — the mapping is 1:1 either way.

## 12-query test list — for the Mechanism Analyst to run against `resolve.py`

9 clear, 3 deliberately ambiguous (one per language), so the abstain/ask mechanism gets
exercised too, not just the happy path.

| # | Lang | Query | Should resolve to | Why |
|---|---|---|---|---|
| E1 | EN | "build me an academic CV with my publications list" | `cv-academic` | `academic`, `publications list` are tokens unique to this row |
| E2 | EN | "I need a leave-behind version of this deck for the client" | `slide-deck-handout` | `leave-behind` appears on no other row |
| E3 | EN | "make me a flyer" | **ambiguous, by design** — `brochure-flyer-letter` and `brochure-flyer-a4` share the identical token `flyer` with no size/region signal to break the tie | tests whether the resolver asks a follow-up rather than picking one arbitrarily |
| E4 | EN | "draft an invoice for this order" | `invoice-tabular` | `invoice` unique to this row |
| F1 | FR | "fais-moi une note interne sur les congés" | `ens-note-interne` **if ENS brand active**, else `memo-internal` | the schema's own worked example (§3) — both rows share `note interne` / `fais-moi une note interne` on purpose; this is the brand two-pass test |
| F2 | FR | "rédige un devis pour ce client" | `quote-devis` | `devis` unique to this row |
| F3 | FR | "fais-moi un cv" | **ambiguous, by design** — no region signal at all; ideally resolves to `cv-generic` or abstains/asks, but is **not guaranteed** to under pure BM25 since the seven regional rows are keyword-denser than `cv-generic` — see "the `cv-generic` risk" above; this query is the direct test of that risk, not a keyword bug to fix |
| F4 | FR | "rédige un rapport avec table des matières" | `report-long-toc` | `table des matières` appears only here, not on `report-short` |
| D1 | DE | "erstelle einen tabellarischen lebenslauf" | `cv-dach` | `tabellarischer lebenslauf` unique to this row |
| D2 | DE | "ich brauche ein anschreiben für diese bewerbung" | `cover-letter` | `anschreiben` unique to this row |
| D3 | DE | "erstelle eine präsentation" | **ambiguous, by design** — `präsentation` appears on `slide-deck-projection`, `slide-deck-document`, and `ens-slides` alike, with nothing in the query to say projected-live vs. read-alone vs. brand | tests the same abstain path as E3/F3 in the third language |
| D4 | DE | "erstelle einen europass lebenslauf" | `cv-eu-europass` | `europass` unique to this row |

## Doc classes the schema (as I read it) still can't fully express

- **Infographic** stays close to what `02-coverage-gaps.md` calls it: an *unbuilt scaffold*.
  I gave it a row so it's reachable and doesn't silently 404, but its `Constraint Set Keys`
  and `Structure Key` are blank on purpose — there is no design payload authored anywhere
  for this class yet (no T3 style, no T9 constraints specific to infographic composition),
  so filling those cells would be inventing content the rest of the library doesn't back.
- **`ens-web-tool`** — resolved above: dropped, per T4's own stated exclusion.
- **The deck `Doc Conditions` sharing problem** — the split into distinct `Reasoning Key`s
  was the interim answer; **superseded by UPDATE 2 above**: Revision 3 ruled `if_projected`
  inadmissible outright (its truth value is fixed by the resolved T1 row, so it isn't a
  condition), deleted it from `DOC_CONDITION_SIGNALS`, and withdrew the split — all three
  `slide-deck-*` rows carry `Reasoning Key: deck-generic` again.

## B2/B3 fixes (this pass, ruled — see research/brief-ddr.md)

- **B2 — the seven regional CV `Constraint Set Keys` were inventions.** `cv-us`, `cv-uk`,
  `cv-eu-generic`, `cv-eu-europass`, `cv-dach`, `cv-france`, `cv-gulf-gcc` each carried a
  bespoke Set Key (`us-cv-region`, `uk-cv-region`, etc.) that matches no `Set Key` in
  `constraints.csv` — this is exactly the gap this file already flagged below (see the
  "cross-check table" note in `29-notes.md` and the mirrored flag here). `constraints.csv`
  has exactly one CV Set Key, `cv-region` (generic; its rows also reach CV doctypes a second
  way, via `Applies To: doctype:cv-*`), and each row's `Region Key` column (already correct:
  `us`, `uk`, `eu-generic`, `eu-europass`, `dach`, `france`, `gulf-gcc`) is what actually
  drives regional selection downstream. Changed all seven rows' `Constraint Set Keys` to
  `ats-strict;cv-region`, replacing the invented per-region key with the mechanism that
  actually resolves — so nobody re-invents a `<region>-cv-region` Set Key later; regional
  variation belongs in `Region Key`, not in a per-region Set Key name.
- **B3 — `png-chromium` did not exist.** `render-targets.csv`'s only PNG render key is
  `png-social`. Repointed `infographic` and `ens-social` from `png-chromium` to `png-social`
  in `Render Target Keys`.

## The four blank `Constraint Set Keys` (this pass, ruled — see research/brief-ddr.md)

`validate_data.py:214` skips empty FKs, so a blank `Constraint Set Keys` produces zero gate
lines while a wrong one produces seven — the gate cannot tell a considered blank from an
omission. A blank means "no constraint set applies," and that has to be true on purpose, not
by default, so each blank (and each fill) is recorded here per row, in the same spirit as
`infographic`'s deliberate blanks above.

- **`cv-academic` stays BLANK, deliberately.** Its seven `cv-*` regional peers all carry
  `ats-strict` because they're parsed by ATS software before a human ever sees them.
  Academic CVs go to hiring/tenure committees, not ATS parsers — there is no applicant-
  tracking gate in that pipeline, so `ats-strict` does not apply. Leave blank; do not "fix"
  it to match its peers.
- **`memo-internal` stays BLANK, deliberately.** An internal memo has no print-legibility,
  ATS, or region constraint attached to it in the schema as authored — it's the one flow
  doctype with genuinely no constraint payload. Leave blank for the same reason as
  `cv-academic`: no constraint set applies, not an oversight.
- **`letter-formal` — set to `print-legibility`.** A formal business letter is printed on
  ordinary office equipment, same print-on-office-gear logic as the report family.
- **`slide-deck-handout` — set to `print-legibility`.** A handout is the printed deck, so it
  needs a print constraint — but not `photocopy-safe` (that's the `if_photocopied`
  *condition*'s job, since a handout isn't always copied) and not `screen` (that would make
  this row identical to `slide-deck-document` on both `Constraint Set Keys` and `Render
  Target Keys`, which are already byte-identical on Render Target Keys; line 148 above
  already depends on these two rows being distinguishable). `print-legibility` keeps
  `slide-deck-handout` and `slide-deck-document` differentiated on `Constraint Set Keys`.

## D3 keyword asymmetry fix (this pass, ruled — see research/brief-ddr.md)

D3 ("erstelle eine präsentation") was resolving confidently to `slide-deck-projection`
instead of abstaining, breaking the deliberate three-way ambiguity documented above (line
~113: "Same overlap, deliberately, on `slide-deck-projection` / `slide-deck-document` /
`ens-slides` around the bare word `présentation`"). Cause: `slide-deck-projection` carried
**both** a bare accented token and the equivalent verb-phrase for each language —
`présentation` (bare) *and* `fais-moi une présentation`, `präsentation` (bare) *and*
`erstelle eine präsentation` — so the présentation/präsentation stem hit that row's Keywords
cell twice per language (sentation-count was 5, vs. document's 3 and handout's 2 at the
time). The bare tokens added no retrieval value beyond what the phrase already carries (any
tokenizer splitting the phrase produces the same word), so they were pure term-frequency
inflation.

**Fix applied:**
- Removed the bare `présentation` and bare `präsentation` tokens from
  `slide-deck-projection`. The phrases (`fais-moi une présentation`, `erstelle eine
  präsentation`) stay — French and German coverage is unchanged, only the redundant bare
  duplicates are gone. `slide-deck-projection` now matches `slide-deck-document`'s structure
  exactly: one English word, one French phrase, one German phrase (sentation-count 3 for
  both).
- `slide-deck-handout` was the one sibling genuinely thin in German — it had a French phrase
  (`support de présentation à imprimer`) but zero présentation-stem coverage in German
  (`ausdruck der folien` doesn't use the word). Added `präsentation zum ausdrucken` so
  handout isn't silently weaker than its two siblings on the German axis (sentation-count
  now 2 — it still legitimately lacks the bare English `presentation` word, out of scope
  here).
- **German spelling check (asked for, even if already correct):** `erstelle eine
  präsentation` already used the correct German umlaut spelling (`präsentation`, U+00E4) —
  verified at the byte level (UTF-8 `c3 a4`), not the French acute form (`présentation`,
  U+00E9, `c3 a9`). No fix needed; recorded per the brief's "note it either way" instruction.
- **Other exact-duplicate tokens found while scripting the check (not fixed, per the
  brief's scope — flagging only):** `brochure-flyer-a4`'s Keywords cell has `flyer a4`
  listed twice (exact duplicate token). No other row among the 34 has a repeated token.
- File still parses clean: 34 data rows x 11 columns, `csv.reader` round-trip verified.
