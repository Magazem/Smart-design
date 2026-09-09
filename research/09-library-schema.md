# Document Library Schema

**Revision: 4**

Design for the retrieval library of a document-shaped design system. Replaces
upstream's web-shaped `src/ui-ux-pro-max/data/*.csv` while keeping its routing engine.

Inputs read: `05-SYNTHESIS.md` (esp. "THE LIBRARY IS WEB-SHAPED"), `01-mechanism.md`
(§1.2–1.4, §1.9), `03-document-design-knowledge.md` (all thresholds),
`02-coverage-gaps.md`, `ENS-plugin-rebuild-v2.md` §1 and §3.

Revision 1 additionally incorporates four commissioned reviews:
`12-typescale-and-fstype.md` (type scales, `fsType`), `13-schema-mechanism-review.md`
(current upstream mechanism), `14-print-production-values.md` (print values and the
print-ready ruling), `15-distribution-model.md` (brand distribution).

Revision 2 incorporates the first **real library rows** and the pilot's acceptance test:
`16-t9-constraints-draft.csv` + notes (38 authored constraints), `17-print-live-tests.md`
(engine availability, confirmed live), `18-cv-region-rules.csv` / `18-ats-headings.csv` +
notes (CV regions and the heading dictionary), `19-notes.md` (safe-stack availability and
metric-compatible substitutes), and `05-SYNTHESIS.md`'s "ENS PILOT — ACCEPTANCE PASSED".
Real rows change a schema in ways review cannot; three tables are added and two columns
die here. Changelog at §9.

Revision 3 is a **maintenance revision, not a redesign**: it folds in what running the
library taught. Inputs: `25-reheader-map.md` §9 (load pass 1 — 190 rows through the real
gate, and the six corrections that pass forced), `26-notes.md` (T1 authored, and the
condition-placement collision it surfaced), `26-t11-caption-qualifications.md` (three real
per-row facts a `yes`/`no` enum could not carry), `27-t14-font-substitutes-draft.csv`.
Two things change shape rather than content: one vocabulary entry is **deleted** after a
placement ruling (§T2), and the manifest's group-FK format request was granted, so all
five dropped foreign keys are declared. Changelog at §9.

---

## 0. Read this before reading the tables

**The schema is a week. The library is the project.** Eleven tables with good columns
and no rows is worth nothing. Rough authoring estimate below (§6). Nobody should read a
finished schema as a finished library.

**Four design rules, each derived from an observed failure — the first three from
upstream, the fourth from authoring our own rows.**

**Rule 1 — no cell may contain *untyped* logic.** *Rewritten at Revision 1; the original
said "no logic" and justified it with a claim about upstream that is no longer true.*

*The correction* (`13-schema-mechanism-review.md` §5). Upstream's `ui-reasoning.csv`
`Decision_Rules` column is **not** inert. `src/ui-ux-pro-max/scripts/reasoning_contract.py`
— imported at `design_system.py:28`, called at `:385-386` — parses it against
`CONDITION_SIGNALS`, a closed, executing 32-key vocabulary, with a parser that raises on an
unknown condition or a malformed action rather than dropping it. The claim that survives in
every version is narrower: **a condition key outside the fixed vocabulary never fires.**
"Custom keys never match" and "nothing fires" are different statements; `01-mechanism.md`
§4's "no evaluator exists" was correct for the v2.5.0 checkout it was written against and
is stale for current upstream (2.13.0, HEAD `4aad0584`). The previous wording asserted the
stronger claim and was self-contradictory on its face — "a fixed set of built-in condition
keys can ever fire" describes a working evaluator.

*The rule that survives.* The hazard was never conditionality; it is **conditionality that
nothing type-checks**. A cell may hold a condition→action pair if and only if both sides
are drawn from a closed vocabulary and a parser hard-fails on anything outside it. That is
the discipline this schema already applies to `Artifact Class` and `Table Rules` — an enum
with a validator — applied to a pair instead of a single value. Free-text JSON stays
forbidden, and free text is what upstream's actual column would be for us: its 32 keys are
`if_booking`, `if_checkout`, `if_luxury` and the rest of the same web vocabulary, none of
which describe a document. We build our own vocabulary (T2 `Doc Conditions`), not carry
theirs.

**Rule 2 — every column must be searched, be a routing key, or feed a validator.**
Stated in the assignment; I apply it strictly, including one sharpening: *an emitted
value counts as validator-feeding only if a named validator checks it survived into the
output.* A margin of 25 mm that nothing verifies is prose with a number in it. Each
table below lists the validators it enables; a column not reachable from that list is
cut. Rationale and provenance live in a sibling `rationale/<table>.md` keyed by slug,
not in a column — this keeps every row a one-line diff, which matters because
contribution to the library *is* the contribution model.

**Rule 3 — linkage keys are slugs, not display text.** Upstream links on human-facing
strings: `products.csv:Product Type` = `"ENS - Eng nei Schaff"` must be byte-identical
to `ui-reasoning.csv:UI_Category`. `ENS-plugin-rebuild-v2.md:15` records the discipline
("plain hyphen, single spaces") and `:95` records the scar tissue — a comment in every
CSV saying *"Product Type text is the key — do not edit it."* A schema that needs that
comment is asking humans to be a foreign-key constraint. **The byte-identical discipline
stays, but it applies to a stable `*_key` slug column, never to a name anyone will want
to reword.** Display names are free to change. This is checked at build time by
`validate-keys` (§5), a hard fail — not a wrapper script, not a convention.

**Rule 4 — a check is defined once, indexed everywhere, and bound only in T9.**
*Added at Revision 2, because the first real constraint rows immediately raised it.* Three
different things in this document look like they declare a validator, and they are not the
same thing:

- **§4 is the only definition.** A validator is a named function with a signature, declared
  parameter names, and one implementation. It appears in §4 exactly once.
- **A table's "Validators enabled" line is a reverse index**, not a declaration. It answers
  "what does this table make checkable," so a reader can see whether a column earns its
  place under Rule 2. It creates nothing.
- **A T9 row is a binding.** It attaches a validator, by id, to a scope (doctype / artifact
  class / format / container) with a threshold and a severity. **T9 rows never define
  checks.** Two T9 rows naming the same validator with different scopes are correct and
  expected; two *definitions* of one check are a defect.

The case that forced this: `16-t9-constraints-notes.md` drafted a `pptx-font-embedded` row
and asked whether it duplicated T5's declared `validate-font-embedded`. It does not. T5
declares a font's **properties** (licence bits, tabular-figure capability); §4 defines the
**check**; the T9 row **binds** that check to PPTX targets at `fail` severity. Same pattern
resolves every future instance of the question.

### 0.1 Storage format: CSV, with one deliberate exception

**Recommendation: CSV.** Not JSON, not SQLite.

- **vs. JSON:** the library is the product and its contribution model is a pull request
  adding a row. CSV gives a one-line diff; JSON gives a noisy nested diff. BM25 needs
  flat text anyway, so nesting buys nothing at the retrieval layer. Report 04's
  stdlib-only constraint is satisfied by both (`csv` / `json`).
- **vs. SQLite:** real joins and FTS5 are genuinely attractive, and I considered it. It
  loses on two grounds: FTS5 compilation is not guaranteed in an arbitrary container, and
  a binary blob is not reviewable in a PR. A contributor cannot see what changed. For a
  library whose whole value is curated rows, opacity is disqualifying. If the row count
  ever passes ~5,000 (it should not; see §6) revisit.

**The exceptions, restated at Revision 1.** The original line was *lists yes, maps no*.
With Rule 1 corrected to forbid *untyped* logic, the line moves: **lists yes; maps only
under a closed, parser-enforced vocabulary.** Three columns are affected, and each is named
here rather than left to be discovered:

- `Render Target Keys` and `Panels mm` hold `;`-separated **lists**. A list is a value.
  Unchanged. **Revision 4 declares them**, so "is a list" is now checked rather than
  asserted: the manifest carries a `list_columns` entry per list column and the gate rejects
  any value that splits into an empty item (a leading, trailing or doubled `;`). The eight
  columns declared at Revision 4 are `doc-reasoning.Anti-Pattern Tokens`,
  `doc-styles.Checklist`, `palettes.{Text-Safe,Fill-Only,Category Marker} Roles`,
  `page-formats.Panels mm`, `figures.Print Palette Roles` and
  `font-substitutes.Weights Covered`.

  **Corrected at load pass 3: the four list columns that are *also* foreign keys are now
  declared too, and the count is twelve.** They are `doctypes.Render Target Keys`,
  `doctypes.Constraint Set Keys`, `structures.Section Order` and `cv-regions.Section Order`.
  Revision 4 left them out on the reading that the FK checker "already splits" them. It does
  split them — and then skips every empty token before looking anything up
  (`validate_data.py`, the `if token and token not in valid_values` line), so a leading,
  trailing or doubled `;` passed the FK loop *and* never reached the well-formedness loop,
  which iterates `list_columns` alone. The check therefore ran on eight columns and on none
  of the four it was most needed for. **Measured, not argued:** a trailing `;` on
  `doctypes.Constraint Set Keys` left the gate at 82 problems; the identical malformation on
  `figures.Print Palette Roles` took it to 83. The generator now asserts the inverse of its
  old guard — every `list: true` foreign key must appear in `list_columns` — so the next list
  FK cannot be added without one. The four are still *listed* rather than derived: adding a
  list column stays an author's decision.

  Two *kinds* of `;`-bearing column are deliberately **not** declared. `constraints.Parameter`
  is a `name=value` map, not a list — declaring it would type it as the wrong thing. And
  **six prose columns carry `; ` as a sentence separator, not as a list delimiter.** Revision 3
  recorded the first of them as an open gap against T11; the **Revision 4 erratum (§9) rules
  it and retypes all six as `text`**, because the authored cells are cited rationale and the
  citation is the value — a token list would throw away the thing that makes the row worth
  shipping. The six are `figures.{Anti-Patterns, Secondary Options, When NOT to Use,
  Data Volume Threshold, Static Fallback}` and `cv-regions.Language Expectation`. Each would
  *pass* a list check while meaning something else, so declaring any of them would ratify the
  drift rather than catch it. They are named here, and typed in their own column tables, so a
  future contributor counting semicolons does not declare them by mistake.
- `Doc Conditions` (T2, new this revision) holds condition→action pairs drawn from a closed
  `DOC_CONDITION_SIGNALS` vocabulary with a hard-fail parser. It is *licensed* by Rule 1 as
  rewritten, not an exception to it.
- `Parameter` (T9) holds `name=value` pairs and was previously admitted as "the one place I
  accept the smell." That framing is no longer consistent with Rule 1 and is withdrawn. It
  is licensed by the same rule as `Doc Conditions` **on condition that it gets the same
  treatment**: each validator function declares the parameter names it accepts, and
  `validate-checks-implemented` is extended to reject a `Parameter` key the named `Check`
  does not declare. Without that extension the column is untyped and Rule 1 forbids it;
  with it, it is an enum keyed by function.

- `Threshold` (T9) is **polymorphic as of Revision 2**: either a literal value, or a
  typed reference of the form `<table>:<Column Name>` (e.g. `cv-regions:Max Pages`) resolved
  through a foreign key the doctype already carries. The reference form is licensed on the
  same terms as the two above — `validate-checks-implemented` resolves the table and column
  and hard-fails on either being absent. Free-text in `Threshold` remains forbidden.

  **The column half names the re-headered column, not the draft's snake_case.** Corrected
  at Revision 3, from `25-reheader-map.md` §9 correction 3: this document wrote
  `T12:max_pages` through two revisions, but by the time a row is *in the library* that
  column is `Max Pages`, and a reference that names a column no table has resolves to
  nothing. On the column half the shipped `constraints.csv` rows were already right and the
  document was the thing that was wrong. A reference resolves against **the loaded header**,
  which is the only name the validator can see. (The *table* half of those same rows was
  wrong in the data, and is corrected below.)

  **The table half names the manifest table, not this document's `T#` label. RULED at
  Revision 4.** `lib/data.py` carries a `reference_columns` spec and `validate_data.py:249`
  implements it as `value.partition(":")` followed by `tables.get(ref_table)` — where
  `tables` is keyed by **manifest table name** (`cv-regions`), not by this document's `T12`
  label. Revision 3 escalated the choice rather than taking it. The ruling: the canonical
  form is `<manifest-table-name>:<Column Name>` — `cv-regions:Max Pages`. The rejected
  alternative was a per-table `"schema_label": "T12"` in the manifest with the resolver
  accepting either form; it keeps this document's prose readable at the cost of a second
  naming layer, and a second naming layer is precisely the drift this schema-plus-manifest
  pairing exists to remove. `T#` is a *section number in this document*, not a name the
  data layer has ever known.

  **Five shipped rows carried the `T#:` form, not one.** Revision 3 said "the one row that
  uses it" and §8 item 6 said the same; both were counted from `cv-page-count` alone. The
  loaded `constraints.csv` also carries four `T7:` references — `pro-bleed-geometry`,
  `pro-trim-safe-margin`, `pro-min-dpi-raster`, `pro-min-dpi-line-art` — which enter from
  `21-t9-print-constraints-draft.csv` rather than from the loader's own literals, which is
  why reading the loader did not surface them. `research/load-base.py` now normalises the
  table half of every `Threshold` reference through a single `T#` → manifest-name map, so
  the rule holds for drafts not yet loaded as well as for these five.

  Revision 4 therefore **declares** `reference_columns` on `constraints.Threshold`:

  ```json
  "reference_columns": {
    "Threshold": {"pattern": "^[a-z][a-z-]*:[A-Za-z][A-Za-z0-9 -]*$", "must_resolve": true}
  }
  ```

  The pattern decides *reference vs. literal*, and a non-match is silently a literal — so
  it is written to be tight on the left and generous on the right. Anchoring the table half
  on a lowercase letter keeps the literal `16:9` (`deck-aspect-ratio-default`) out; widening
  the column half to admit digits and hyphens means a future reference to `Trim W mm` or
  `Text-Safe Roles` resolves instead of being silently swallowed as a literal. Every other
  shipped `Threshold` — `0`, `1.0`, `present`, `45-75`, `16:9` — fails the pattern and is
  read as the literal it is.

What stays forbidden is the free-text map. The per-medium type scale is still its own
long-format table (T6) rather than a `print.body=11;print.h1=24` cell, because no closed
vocabulary bounds it — its key space is the cross product of two enums and grows with
both.


### 0.1.1 Surrogate keys, added when the schema was transcribed to a manifest

*Added at Revision 2, after `data/schema-manifest.json` was produced from this document.*
The manifest format allows one `key_column` per table. Four tables here have **composite
natural keys**, so each gains a surrogate key column — declared first, with the natural key
kept as ordinary columns beside it:

| Table | Natural key | Surrogate |
|---|---|---|
| T6 `type-scales` | (`scale_key`, `Medium`, `Role`) | `scale_row_key` |
| T12 `cv-regions` | (`region_key`, `Seniority Band`) | `cv_region_key` |
| T13 `headings` | (`canonical_section`, `Heading Text`, `Language`) | `heading_key` |
| T14 `font-substitutes` | (`proprietary_family`, `Lineage`) | `substitute_key` |

T14's is the one worth pausing on: Arial has **two** substitutes — Liberation Sans under OFL
and Arimo under Apache 2.0 — so `proprietary_family` was never unique, and picking between
the rows is a licence decision. That is why `Lineage` and `Licence` are separate columns.
T11 `figures` takes `chart_key`, the key its authored draft names and this document
never did.

**Convention for anything added later:** a surrogate is `<singular>_key`, declared first,
and it never replaces the natural key columns — those stay, because they are what a
contributor reads and what the resolver joins on.

**The grouping-FK consequence — filed at Revision 2, closed at Revision 3.** Five foreign
keys in this schema reference a *grouping* column rather than a key column, and the manifest
format could not declare them, so they were dropped and `validate-keys` mechanised only part
of its job. The format change request was granted: `lib/data.py:82` now accepts
`{"table": …, "column": …, "group": true}`, meaning *the value must exist somewhere in that
column, which need not be unique*, and it composes with `"list": true`. All five are
declared as of Revision 3:

| Table | Column | Target | Also a list |
|---|---|---|---|
| T1 `doctypes` | `Constraint Set Keys` | `constraints.Set Key` | yes |
| T1 `doctypes` | `Region Key` | `cv-regions.region_key` | no |
| T5 `typefaces` | `Scale Key` | `type-scales.scale_key` | no |
| T10 `structures` | `Section Order` | `headings.canonical_section` | yes |
| T12 `cv-regions` | `Section Order` | `headings.canonical_section` | yes |

**Two counts were wrong and are corrected here.** It is *five* dropped, not four — §0.1.1
as written collapsed T10's and T12's `Section Order` into one bullet, but §4 entry 1 names
both and they are two independent declarations. And the total is **13** FK relationships,
not 8: T1 carries six, T2 three, T5 one, T8 one, T10 one, T12 one. So Revision 2 mechanised
**8 of 13**, not "4 of 8", and Revision 3 mechanises **13 of 13**. The shape was never four
accidents — it is what a schema built on long-format dictionaries does, and the format now
says so.

### 0.2 What we keep from upstream's engine, and the one place I deviate

*Rewritten at Revision 1.* The previous description was accurate for the v2.5.0 checkout
`01-mechanism.md` was written against, and it undersold how far upstream has since moved —
toward this schema's own proposed deviation (`13-schema-mechanism-review.md` §1–§2, checked
against 2.13.0, HEAD `4aad0584`, `2026-09-06`; upstream has not moved since report 10).

Keep, unchanged in shape:

1. **Exact-identity resolution before BM25.** `search()` (`core.py:755-845`) first tries
   `_style_identity()` / `_exact_row_identity()` — a plain dict lookup built once at load
   (`_build_style_lookup`, `design_system.py:296-305`) over `Style ID` / `Style Category` /
   `Aliases`. BM25 executes only on a miss. **T1 adopts the same shape**: an exact `doc_key`
   or `Display Name` hit resolves with zero fuzziness, and BM25 is the fallback rather than
   the primary path. "BM25 over `search_cols`" now describes the fallback, not the engine.
2. **BM25 over designated `search_cols`, and it abstains.** From-scratch, k1=1.5 / b=0.75,
   no embeddings, no model call (`core.py:285`; the formula itself is unchanged). What is
   new is the calibration around it: per-domain score floors, coverage thresholds and margin
   checks (`_SEARCH_THRESHOLDS`, `core.py:203-213`) make a low-confidence query return
   **zero results plus suggestions** rather than a weak top-1 guess. We keep that behaviour,
   and it is load-bearing downstream — see below.
3. **The chain**: doctype table → match resolves a reasoning row → reasoning resolves or
   biases the style / palette / typeface lookups. Architecturally unchanged (`generate()`,
   `design_system.py:461-476`).
4. **Closed-form rerank** (`_select_best_match`) — but it is no longer only a rerank; see
   the deviation.

**Why abstention matters to this schema specifically.** `validate-brand-resolution` (§0.3)
hard-fails when a brand is active and no brand-scoped row was resolved. Were retrieval to
return a weak generic guess instead of nothing, that validator would have to distinguish
"resolved the wrong row" from "resolved no row" — a judgment call, and judgment calls are
what §0.3 exists to remove. An abstaining retriever turns it into a presence check. The
abstaining retriever and the hard-failing validator are the same decision made twice, and
they compose.

**The deviation — smaller than the previous revision claimed.** Upstream's stage 3 re-runs
BM25 on style/colour/typography with the reasoning row's keywords appended to the query
(`01-mechanism.md` §1.3 step 3). For documents this schema proposes **explicit foreign keys
with biased search as the fallback**: the reasoning row names `Style Key`, `Palette Key`,
`Typeface Key`; a present key is a direct lookup, an empty one falls back to biased BM25
exactly as upstream does.

**For styles this is not a deviation at all — it is already shipping upstream, and that
strengthens the case rather than weakening it.** `_select_best_match()`
(`design_system.py:408-443`) now tries `_resolve_style(priority)` — a direct dict lookup
with deprecation-chain walking via `Parent Style ID` (`design_system.py:307-317`) — for
every priority keyword *before* falling back to keyword scoring. That is foreign-key
resolution with biased search as fallback, in upstream's own code, in the version its
`validate_data.py` and `MASTER.md` formatting are validated against. It is proof by
existence that a direct-lookup stage does not break the output contract: `search()`'s return
shape is produced by `_project_row` on both paths, so a dict hit is indistinguishable
downstream from a BM25 hit.

**Be precise about the scope of that precedent.** The convergence is style-only.
`Color_Mood` / `Typography_Mood` (`_apply_reasoning`, `design_system.py:393-406`) are still
plain text folded into the biased query in `_multi_domain_search`; there is no
`_resolve_palette` or `_resolve_typeface`. So: **`Style Key` mirrors a shipping upstream
mechanism. `Palette Key` and `Typeface Key` extend it to two stages upstream has not
reached.** The extension is one more dict built at load, same shape, stdlib-only — but it
is upstream's own next step taken early, not a pattern already proven for all three.

The field evidence for taking it early is unchanged and still the reason:
`ENS-plugin-rebuild-v2.md:8` records that `Parent Style ID` carries *"only a pointer — no
inheritance of rule content — so everything is restated in the ENS row anyway."* ENS pinned
every value by hand because the second-stage search would not reliably return them. For a
CV where the same input must produce the same margins twice, a heuristic in the resolution
path is a defect. The fallback preserves long-tail behaviour for doctypes nobody has fully
specified, so the engine still works out of the box.

### 0.3 Brand inheritance as data — and how a brand actually gets installed

The ENS diagnosis, in the field instance's own words (`05-SYNTHESIS.md:135`):
**"The identity is an instruction, not data."** BM25 returns generic rows (navy,
Garamond); the brand file then tells the model to override them afterwards. Every patch
is a judgment call, and judgment calls drift.

**Fix, mechanical:** brand rows are real rows in the searched tables, carrying brand
match tokens in their `search_cols`. Every table below has a `Brand Scope` column
(`generic` or a brand slug). Resolution is two-pass and deterministic:

1. If a brand is active, resolve the doctype against `Brand Scope == <brand>` rows only.
2. If that returns nothing, fall back to `Brand Scope == generic`.
3. Downstream of the doctype, everything resolves by foreign key (§0.2), so the brand
   propagates without a second retrieval and without a chance to drift.

Note what this makes unnecessary: no boost constant, no score threshold, no tuning. The
only fuzzy step is step 1, and it is scoped to a small candidate set.

**Where the rows physically live — §7 Q4, now closed.** `15-distribution-model.md`
answers it and the orchestrator has adopted the answer. It is **not** one of the three
options Q4 listed, because two of them answer different questions: the decision is a
**runtime overlay directory for resolution, plus scripted regeneration of the ZIP for
distribution**.

```
data/
  base/           <- the 11 shipped tables
  brand/
    active.json   <- {"active": "ens"} or {"active": null}; exactly one brand active
    ens/          <- any subset of the 11 table filenames, brand rows only
```

`scripts/resolve.py` loads `data/base/<table>.csv` unconditionally and **appends**
`data/brand/<active>/<table>.csv` where it exists. Three consequences this schema depends
on:

- **`Brand Scope` is set by the directory, not typed per row.** The loader stamps or
  verifies the column from the containing folder's name; a brand CSV carrying a
  contradicting value is a load error, not a silent override. This is Rule 3's reasoning
  applied to the one column that would otherwise reintroduce exactly the problem Rule 3
  removes — a human being asked to be a foreign-key constraint.
- **Key collision is a hard fail at load.** A brand overlay is expected to introduce *new*
  slugs (`ens-note-interne`). If a brand row's primary slug collides with a base slug, the
  resolver refuses to run and prints which file and which slug collided. An overlay row
  that shadows a differently-authored base row is not an override; it is invisible
  divergence. This is `validate-brand-resolution`'s posture applied one step earlier — at
  load rather than at resolution.
- **`resolve.py` prints only the resolved decision to stdout, never raw tables.** Only a
  script's stdout enters context (`04-packaging.md` §1.2), so the merge has to happen
  inside the script. A resolver that printed both tables and let the model reconcile them
  would have turned the identity back into an instruction — the precise defect this
  section exists to remove.

Distribution is the other half of the answer. claude.ai's persistence unit is the whole
uploaded ZIP and there is no partial-update path, so any change to base *or* brand means a
full rebuild and re-upload. The difference from what ENS did is not that regeneration goes
away — it is that a bundled stdlib script does it instead of a human. Two assumptions
underneath that flow are **unverified and flagged as such** (`15-distribution-model.md`
§2): that files a script writes into the skill directory during one chat do *not* survive
into a new chat (assume no until tested), and that an attached ZIP is reachable from the
script's working directory. The design deliberately does not depend on either resolving
favourably.

**One `description` field.** claude.ai's Settings → Skills flow reads nothing but
`SKILL.md`'s frontmatter. The four parallel manifests upstream maintains are Claude Code
and marketplace concepts, and they drifted from each other for over a month once upstream's
own sync automation broke (`04-packaging.md` §1.1, `11-upstream-releases.md` §5). We keep
exactly one `name` and one `description`, in `SKILL.md`, full stop.

**But brand-as-rows does not fix the defect the pilot actually hit.** The synthesis
records three separate occurrences of the model *not consulting the library at all* —
`:150-156` ("I skipped the plugin entirely twice"), and `:186-189`, where after being
told "use the ENS brand" it **invented** an ENS green (`#2E7D32`) and guessed the
running-header text. Better rows do not help a resolver that was never called. ENS's
answer was a wrapper script grepping for `[NO ENS MATCH]` (`ENS-plugin-rebuild-v2.md:92`)
— again, scar tissue for a missing mechanism.

**Schema answer:** `validate-brand-resolution` (§4). If a brand is active and the
resolved row set contains no brand-scoped row, the resolver hard-fails and refuses to
emit. It is the cheapest validator in the set and the only one targeting a defect we
have actually observed in production rather than predicted.

---

## 1. Table map

**Spine (routing)**
- T1 `doctypes.csv` — entry point, the only fuzzy step
- T2 `doc-reasoning.csv` — biasing / key-resolution table

**Design payload (values that get emitted)**
- T3 `doc-styles.csv` — visual grammar
- T4 `palettes.csv` — colour roles, print-aware
- T5 `typefaces.csv` — families and per-medium behaviour
- T6 `type-scales.csv` — long-format point sizes
- T7 `page-formats.csv` — geometry; **no upstream analog**

- T14 `font-substitutes.csv` — metric-compatible fallbacks; **no upstream analog**

**Output & enforcement**
- T8 `render-targets.csv` — the format fork; **no upstream analog**
- T9 `constraints.csv` — the validator rule table; **no upstream analog**
- T10 `structures.csv` — section order and document skeleton
- T11 `figures.csv` — charts, medium-aware (derived from upstream `charts.csv`)

**Reference dictionaries (added at Revision 2)**
- T12 `cv-regions.csv` — region × seniority CV norms; **no upstream analog**
- T13 `headings.csv` — the ATS heading dictionary, long format; **no upstream analog**

Fourteen tables, not eleven. Three of the four Revision 2 additions exist because authoring
real rows exposed a fact being restated across many rows — the same test that split T6 out
of T5. §7 Q6 asks whether fourteen is more than contributors will maintain; the honest
answer is that all three new tables are *smaller* than the duplication they remove.

Legend in every column table: **S** searchable · **V** feeds a named validator ·
**R** routing key · **P** prose payload. A column with none of these is not in the schema.

**`P` is added at the Revision 4 erratum (§9)** and applies to exactly seven columns. A `P`
column is cited rationale that the resolver hands to the *author* or the generator emits to
the *reader*; no check reads it, and none can, because the value is a sentence and not a
token. It exists so that "feeds no validator" is a stated property rather than a `V` that is
quietly untrue — the seven all carried `V` or no type row at all before the erratum. Adding
an eighth `P` column should be an argument, not a default: the letter marks the boundary of
what this library can mechanically enforce, and every column past it is knowledge the
library can only *show*. **`T11.Caption Must State` was the seventh and is closed at the
follow-on erratum (§9)**, by the test the letter is supposed to follow: the column is `P`
because no line of `scripts/` reads it. Its `V` was a mislabel, not a widening — enforcement
did not drop when the letter changed, the count of *honest* labels rose. Keeping that
distinction is what leaves §8 item 11's warning live for a genuine eighth.

---

## T1. `doctypes.csv`

**Purpose.** The single fuzzy entry point. Natural language in ("a two-page CV for a UK
job", "note interne ENS") → one row out. Everything downstream is key resolution.
`search_cols = [Display Name, Keywords]`.

| Column | Type | Example (ENS) | Example (generic) | S/V/R |
|---|---|---|---|---|
| `doc_key` | slug | `ens-note-interne` | `cv-uk-2page` | R |
| `Display Name` | text | ENS — Note interne | CV — UK, 2 page | S |
| `Keywords` | text | note interne, courrier, ens, eng nei schaff, bettembourg, luxembourg, asbl | cv, curriculum vitae, resume, uk, british, ats, job application | S |
| `Artifact Class` | enum `canvas`\|`flow`\|`hybrid` | `flow` | `flow` | R V |
| `Brand Scope` | slug | `ens` | `generic` | R V |
| `Reasoning Key` | slug FK → T2 | `ens-office-document` | `cv-ats-strict` | R |
| `Page Format Key` | slug FK → T7 | `a4-ens-note` | `a4-cv-single-col` | R |
| `Render Target Keys` | slug list FK → T8 | `docx-office;pdf-chromium` | `pdf-chromium;docx-office` | R |
| `Constraint Set Keys` | slug list FK → T9 | `ens-house;photocopy-safe` | `ats-strict;uk-cv-region` | R |
| `Structure Key` | slug FK → T10 | `ens-note` | `cv-experienced` | R |
| `Region Key` | slug FK → T12, nullable | — | `uk` | R |

**Example rows (abbrev.)**

```
ens-note-interne | ENS — Note interne | note interne,courrier,ens,… | flow | ens |
  ens-office-document | a4-ens-note | docx-office;pdf-chromium | ens-house;photocopy-safe | ens-note
cv-uk-2page | CV — UK, 2 page | cv,resume,uk,ats,… | flow | generic |
  cv-ats-strict | a4-cv-single-col | pdf-chromium;docx-office | ats-strict;uk-cv-region | cv-experienced
brochure-trifold-letter | Brochure — tri-fold, US Letter | brochure,trifold,leaflet,flyer | flow | generic |
  print-marketing | letter-trifold | pdf-weasyprint-pdfx4;pdf-chromium | professional-print | brochure-3panel
```

**Design notes.**

- `Artifact Class` is my canvas-vs-flow finding (`02-coverage-gaps.md` §1.2,
  `05-SYNTHESIS.md:14-31`) promoted from prose to a routing key. It gates which
  validators run: `flow` requires pagination checks and a page format with margins;
  `canvas` forbids them and requires a fixed frame instead. This is the column that stops
  the system silently applying slide logic to a report.
- **`Brand Scope` is populated by the loader from the overlay directory name (§0.3), not
  typed per row.** A brand's rows arrive in `data/brand/<slug>/`, so the column is stamped
  or verified at load and a contradicting value is a load error. Nobody authoring a brand
  row has to retype a slug byte-identically — Rule 3's reasoning applied to the one column
  that would otherwise reintroduce the problem Rule 3 removes.
- **The fuzzy step is a fallback, not the primary path** (§0.2, added at Revision 1). An
  exact `doc_key` or `Display Name` hit resolves first with zero fuzziness; BM25 runs only
  on a miss, and abstains rather than guessing when confidence is low.
- **Region was a doctype variant. At Revision 2 it is a foreign key, and I was wrong.**
  The original design put region gates (length ceiling, photo, DOB, marital status, section
  order) in four doctype rows — `cv-us-1page`, `cv-uk-2page`, `cv-eu-europass`, `cv-gulf` —
  resolving through `Structure Key` and `Constraint Set Keys`. That held at four regions
  with implicit banding. `18-cv-region-rules.csv` authored **seven regions**, and at seven
  the four facts get restated in every row: precisely the duplication that split T6 out of
  T5. `Region Key` now points at T12, and the region facts are stored once.
  **`Seniority Band` is deliberately not a column here** — it is not a property of the
  doctype, it is computed from the document's own parsed experience dates, so it is a
  lookup axis into T12 supplied at validation time, not a routing key authored per row.
- **What survives from the original reasoning:** region is still not a parameter threaded
  through the resolver, and there is still no special-case code path. It is a foreign key
  like every other, which is the same argument one level further down.

- **`Constraint Set Keys` is where a doctype-determined fact goes — ruled at Revision 3,
  and the answer is "neither branch."** `26-notes.md` found a real collision: three deck
  doctypes share one `Reasoning Key` (`deck-generic`) for style/palette/typeface economy,
  so T2's `Doc Conditions` — keyed by `doc_category` — would fire `if_projected` on the
  handout and the read-on-screen deck too. The question put to this revision was whether
  **context** conditions belong here on T1, leaving only **intent** conditions on T2.
  **They do not, and no new column is added.** T1 already has the column that says "this
  doctype carries this constraint," it is `Constraint Set Keys`, `validate-keys` already
  checks it, and the three deck rows *already carry the discriminator in it*:
  `projection` / `screen` / empty. A `Context Conditions` column on T1 would be a second,
  grammar-bearing way to state what an FK list already states — the untyped-second-path
  shape Rule 1 exists to refuse, and it would need its own parser, its own validator entry
  and its own manifest declaration to say nothing new.
  The ruling and its test live on T2, where the vocabulary lives; the consequence for this
  table is one sentence: **if the fact is true of the doctype, it is a constraint key on the
  T1 row, not a condition on the T2 row it shares.**

**Validators enabled:** `validate-keys`, `validate-brand-resolution`,
`validate-artifact-class` (a `flow` row must reference a page format with non-zero
margins and a `Structure Key`; a `canvas` row must not reference pagination constraints).

---

## T2. `doc-reasoning.csv`

**Purpose.** Upstream's `ui-reasoning.csv` role: turn a resolved doctype category into
design decisions. Under §0.2 it resolves keys where specified and biases search where
not. `search_cols = [Doc Category, Style Bias Terms]` (searched only on the fallback
path).

| Column | Type | Example (ENS) | Example (generic) | S/V/R |
|---|---|---|---|---|
| `doc_category` | slug | `ens-office-document` | `cv-ats-strict` | R |
| `Style Key` | slug FK → T3, nullable | `ens-document-grid` | `cv-restrained` | R |
| `Palette Key` | slug FK → T4, nullable | `ens-core` | `mono-ink` | R |
| `Typeface Key` | slug FK → T5, nullable | `ens-manrope-inter` | `cv-safe-sans` | R |
| `Style Bias Terms` | text | grid, hairline rules, no fills, photocopy-safe | restrained, single column, no color blocks | S |
| `Palette Bias Terms` | text | forest green structure, earth brown secondary | monochrome, ink on white | S |
| `Typeface Bias Terms` | text | clear, functional, sans, embeddable | safe stack, ubiquitous, no embedding | S |
| `Doc Conditions` | closed grammar, nullable | `if_hand_filled=constraint:field-underline-only;if_photocopied=constraint:photocopy-safe-color` | `if_ats_target=constraint:ats-strict` | V |
| `Anti-Pattern Tokens` | text list | gradient;emoji;navy;#000080;rounded-card;lime-text | multi-column;text-box;icon-only-skill-bar;photo | V |
| `Severity` | enum `fail`\|`warn` | `fail` | `fail` | V |

**Design notes.**

- `Anti-Pattern Tokens` is upstream's `Anti_Patterns` column (prose the model is asked to
  remember) converted into a **grep list the output validator runs**. ENS's real rules —
  *"no emoji, gradients, navy/blue, or lime as text"* (`ENS-plugin-rebuild-v2.md:117`) —
  become mechanically enforceable. This is the single cheapest anti-slop upgrade in the
  schema and it costs one column.
- **`Doc Conditions` — added at Revision 1, and it is a reversal I am stating as one.**
  The previous revision refused any conditional column, on the strength of a claim that
  upstream's `Decision_Rules` is inert. That claim is wrong for current upstream (Rule 1,
  corrected). `reasoning_contract.py` is a ~120-line stdlib-only module that parses a
  closed 32-key `CONDITION_SIGNALS` dict and raises on an unknown condition or a malformed
  action rather than dropping it silently. A closed vocabulary with a rejecting parser is
  the same discipline as an enum with a validator, and refusing it costs a real capability:
  without it, a hand-filled form and a non-hand-filled variant of the same `doc_category`
  need two rows differing in one cell, and that pair drifts. The reason to still not carry
  upstream's column *content* forward is unchanged and narrower than before — its 32 keys
  are `if_booking`, `if_checkout`, `if_luxury` and the rest of the same web vocabulary, and
  none of them describe a document.

- **Contract for `doc_reasoning_contract.py`.** Build it on upstream's shape, not its
  vocabulary:
  - `DOC_CONDITION_SIGNALS` is a closed dict, holding `if_hand_filled`, `if_photocopied`,
    `if_ats_target` and `if_professional_print`, and grown only by editing that dict —
    subject to the admission test below. **`if_projected` was seeded at Revision 1 and is
    deleted at Revision 3**; it failed that test. Four keys, not five.
  - Actions are restricted to the prefix `constraint:` — plus `style:` for
    context-sourced conditions only, see below. Nothing else parses.
  - Unknown condition key, unknown action prefix, or malformed pair → `ValueError` at
    build time, never a silent drop. `validate-doc-conditions` runs the parser over every
    T2 row in CI, mirroring `validate_data.py`'s `_check_reasoning_contract`.
  - `validate-severity-map` extends to the same closed loop upstream applies to style and
    pattern actions (`validate_data.py:366-372`): every condition that can activate must
    reach a real T9 constraint.

- **One deliberate deviation from upstream's contract: the signal source.** Upstream
  matches `CONDITION_SIGNALS` entries as substrings of the raw user query (`if_data_heavy`
  → `("data heavy", "data-heavy", "analytics", "large dataset")`). Copying that would
  reintroduce into the resolution path exactly the fuzzy step §0.2 spends its length
  removing: whether a constraint fires would depend on the user's phrasing, so the same
  document requested twice in different words would validate differently. Each vocabulary
  entry therefore carries a **signal source tag**:
  - `context` — evaluated against the resolved context, but only against a part of it the
    T1 row does **not** fix: which render target was selected from that row's
    `Render Target Keys` list. `if_professional_print` is the one entry, and it is the one
    the admission test below lets through.
  - `intent` — genuinely request-level and not derivable from any resolved row.
    `if_hand_filled`, `if_photocopied` and `if_ats_target` are the three, and the
    distinction is real rather than a hedge: T3's `Field Style` tells you a form is
    hand-*fillable*, never that this copy will be hand-*filled*; nothing in the library
    knows a note is destined for a photocopier; and nothing in it knows whether a CV is
    going into an applicant-tracking portal or across a table at a careers fair.

- **The admission test — new at Revision 3, and it deletes an entry.** `26-notes.md` found
  the failure: three deck doctypes share `Reasoning Key: deck-generic`, `Doc Conditions` is
  keyed by `doc_category`, so `if_projected` on that row fires on the handout and the
  read-on-screen deck as well. The interim fix was to split `deck-generic` into three
  reasoning keys differing in one cell — which is **exactly the drifting pair this column
  was introduced to prevent**, so it cannot be the answer. The rule that is:

  > **A condition is admissible only if its truth value is not determined by the resolved
  > T1 row.** If the row determines it, the row already knows the answer, and a row that
  > knows the answer states it as a constraint key in `Constraint Set Keys`. A condition
  > whose value is a constant is not a condition.

  Applied to `if_projected`, the evidence is closed rather than arguable: viewing context
  *is* the axis the three deck doctypes are split on, and their T1 rows already carry
  `projection` / `screen` / `` in `Constraint Set Keys`, with `projection` a real Set Key in
  the authored `constraints.csv`. The condition can only restate the row. **Deleted.**
  `deck-generic` goes back to one reasoning key, the interim three-key fix is withdrawn, and
  the projection constraints reach `slide-deck-projection` and nothing else.

  Applied to `if_professional_print`, the same test **keeps** it, and the reason is worth
  recording because it is not obvious: all six `print-marketing` doctypes carry
  `professional-print` in `Constraint Set Keys`, so *at the doctype level* it looks equally
  constant. But every one of them lists `pdf-weasyprint-pdfx4;pdf-chromium` — `pdfx4-rgb`
  and `submittable-rgb` — and which of the two is selected is a render-time choice the T1
  row does not fix. The truth value varies **inside** a single row, which is finer than the
  test demands. That is also why §4 entry 9 (`validate-print-mode-coherence`) exists at all.

  **What the test does *not* license: a `Context Conditions` column on T1.** The whole class
  of doctype-determined facts already has a column, and it is an FK list `validate-keys`
  checks byte-identically. Giving them a second, grammar-bearing home would need a parser, a
  validator entry and a manifest declaration to express what `Constraint Set Keys` expresses
  today. The condition column stays on T2 and gets smaller instead.

  **Honest limit on mechanising this.** The tempting check — "fail any `context` condition
  whose discriminating field is identical across every T1 row referencing this T2 row" — is
  real and computable, but it needs each vocabulary entry to *declare which resolved field
  it reads*, and `doc_reasoning_contract.py` is not built (`schema-manifest-NOTES.md` §1.3).
  Until it is, the admission test is an **authoring-time gate on a closed hand-edited
  dict**, which is where it has to live anyway: the dict is the only place a new signal can
  enter, so that is the only place the question gets asked.

  **The parser enforces the asymmetry: an `intent`-sourced condition may emit only
  `constraint:` actions, never `style:`.** A missed intent signal can therefore change
  *which checks run* and never *what gets emitted* — intent can tighten the output, never
  alter it. That is the property that keeps §0.2's reproducibility argument true under a
  fuzzy signal, and it is build-time checkable: `validate-doc-conditions` fails if any
  `intent`-tagged entry can reach a non-`constraint:` action.

**Validators enabled:** `validate-keys`, `validate-anti-patterns`, `validate-severity-map`
(every `fail`-severity reasoning row must reach at least one hard constraint in T9 —
prevents a row that declares itself strict and enforces nothing),
`validate-doc-conditions` (closed-vocabulary parse + the `intent` ⇒ `constraint:`-only
rule).

---

## T3. `doc-styles.csv`

**Purpose.** The visual grammar payload — upstream's `styles.csv` role, minus its 22
columns of web questions. `search_cols = [Display Name, Keywords, Best For]`.

| Column | Type | Example (ENS) | Example (generic) | S/V/R |
|---|---|---|---|---|
| `style_key` | slug | `ens-document-grid` | `report-classic-serif` | R |
| `Display Name` | text | ENS Document Grid | Classic report, serif | S |
| `Keywords` | text | grid, hairline, single accent, no fills, hand-fillable, photocopy-safe | report, whitepaper, formal, scholarly, serif body | S |
| `Best For` | text | internal notes, forms, fiches, letters, tables | long-form reports, whitepapers, policy documents | S |
| `Not For` | text | social posts, banners | slide decks, one-page flyers | S |
| `Brand Scope` | slug | `ens` | `generic` | R |
| `Rule Weights` | text list | `hair=0.5pt;strong=1pt;brand=1.6pt` → see note | `hair=0.5pt;strong=1pt` | V |
| `Corner Radius mm` | number | `0` | `0` | V |
| `Table Rules` | enum `hairline`\|`header-and-total`\|`none` | `hairline` | `header-and-total` | V |
| `Table Fills` | enum `none`\|`zebra`\|`header-only` | `none` | `none` | V |
| `Emphasis Mechanism` | enum `weight`\|`colour-text`\|`fill` | `weight` | `weight` | V |
| `Field Style` | enum `underline`\|`box`\|`none` | `underline` | `none` | V |
| `Checklist` | text list | one green rule under title;labels 8.5pt uppercase;tables hairline only;… | headings H1–H3 only;figure captions below;… | V |

**Design notes.**

- `Rule Weights` is a **map**, which Rule 1 forbids. Correction applied: it becomes three
  scalar columns `Rule Hair pt`, `Rule Strong pt`, `Rule Brand pt`. Listed above as one
  row for readability only; the shipped schema has three columns. Flagging my own slip
  because the same temptation will recur on every table.
- `Emphasis Mechanism` encodes ENS's *"Emphasis = bold … never background"*
  (`ENS-plugin-rebuild-v2.md:136`) as an enum the validator can check against the rendered
  output. It also encodes report 03's CV signal — hierarchy by weight/size, not colour
  blocks, being the tell that separates a real CV from a template.
- `Checklist` survives from upstream because of a mechanism worth copying verbatim:
  `01-mechanism.md` §1.5 notes upstream **bakes the checklist into generator output**
  rather than leaving it as instructions. The column is validator-feeding in exactly that
  sense — the generator must emit it, and a check confirms it did.

**Dropped from upstream `styles.csv`:** `Framework Compatibility`, `CSS/Technical
Keywords`, `Mobile-Friendly`, `Conversion-Focused`, `Light Mode ✓`, `Dark Mode ✓`,
`Performance`, `Era/Origin`, `Complexity`, `AI Prompt Keywords`, `Effects & Animation`.
Eleven of twenty-two columns are web questions. `Effects & Animation` goes because print
has none and, per `02-coverage-gaps.md` §3.3, an emphasis expressed as animation
*silently vanishes* on paper rather than degrading — worse than useless.

**Validators enabled:** `validate-anti-patterns`, `validate-emphasis-mechanism`,
`validate-checklist-emitted`, `validate-table-rules`, `validate-table-alignment`.

---

## T4. `palettes.csv`

**Purpose.** Colour roles with contrast-safe pairing, extended for paper.
`search_cols = [Display Name, Keywords]`.

| Column | Type | Example (ENS) | Example (generic) | S/V/R |
|---|---|---|---|---|
| `palette_key` | slug | `ens-core` | `mono-ink` | R |
| `Display Name` | text | ENS core | Monochrome ink | S |
| `Keywords` | text | ens, forest green, earth brown, luxembourg, asbl | monochrome, black on white, cv, ats, neutral | S |
| `Brand Scope` | slug | `ens` | `generic` | R |
| `Primary` / `On Primary` | hex | `#1F6F43` / `#FFFFFF` | `#1A1A1A` / `#FFFFFF` | V |
| `Secondary` / `On Secondary` | hex | `#8B5E3C` / `#FFFFFF` | `#4A4A4A` / `#FFFFFF` | V |
| `Accent` / `On Accent` | hex | `#9ACD32` / `#1E2A23` | — | V |
| `Background` / `Foreground` | hex | `#F7F8F5` / `#1E2A23` | `#FFFFFF` / `#111111` | V |
| `Muted` / `On Muted` | hex | `#DCE8DF` / `#5B665F` | `#F2F2F2` / `#555555` | V |
| `Rule Hair` / `Rule Strong` / `Rule Brand` | hex | `#B9C4BC` / `#1E2A23` / `#1F6F43` | `#CCCCCC` / `#111111` / `#111111` | V |
| `Text-Safe Roles` | slug list | `primary;secondary;foreground;on-muted` | `foreground;primary;secondary` | V |
| `Fill-Only Roles` | slug list | `accent;muted` | `muted` | V |
| `Category Marker Roles` | slug list | `secondary` | — | V |

**Design notes.**

- **`Text-Safe Roles` / `Fill-Only Roles` is the exemplar of the whole schema.** ENS's
  rule — *"lime = filled badge with dark text, marketing only, never text"*
  (`ENS-plugin-rebuild-v2.md:125`, closed decision #2 at `05-SYNTHESIS.md:234`) — is
  currently a sentence in a prose file that the model is asked to remember, and which the
  field instance demonstrably failed to remember. As two list columns it becomes a check:
  grep the emitted output for text rendered in a fill-only role, fail. One column pair
  converts a house rule into a guarantee.
- **Blank cells: a colour pair is skipped only when BOTH halves are empty (RULED).**
  The generic column above prints an em-dash under `Accent` / `On Accent`, and
  `mono-ink` really does ship both blank — a monochrome palette does not define an accent
  role, so there is no pair to rate. `validate_data.py`'s `contrast_at_least` therefore
  **skips a derived contrast rule when both `column` and `against_column` are empty, and
  still errors when exactly one is.** A half-filled pair is an ink with no ground (or a
  ground with no ink): an authoring bug, not an omission, and it must fail.
  **This is deliberately NOT the same rule blank foreign keys get, and the difference is
  the point.** A blank FK is skipped *one cell at a time* ("nullable Style/Palette/Typeface
  Key" — no reference to check). A contrast rule is skipped *only pairwise*, because the
  unit of meaning is the pair, not the cell. Stated here because both behaviours were
  real, neither was written down, and the undeclared version of this rule has now cost
  this project three passes. Any future derived check must declare its own blank
  behaviour in its table's section before it ships.
- **Every `On X` value stays derived, not authored.** `01-mechanism.md` §1.5 documents
  upstream computing WCAG relative luminance in `_sync_all.py:22-31` to pick
  white-or-near-black foregrounds. That code is directly reusable and should be, because a
  hand-picked `On X` is an unverified claim.
- **`Min L* Delta` is NOT a column here.** I drafted it, then cut it: it is a *threshold*,
  and thresholds live in T9. A palette holds colours. Keeping the number in two tables
  guarantees they drift.
- **The print-contrast threshold changed basis at Revision 1, and this table is where it
  now computes.** `14-print-production-values.md` §4 confirms — as an absence, not a
  failure to find — that no standardised print text-contrast metric exists. Report 03's
  40–50 L\* delta is convention with no standard behind it, and the nearest real published
  standard (ADA/ANSI A117.1's ≥70% LRV for accessible signage) is both the wrong domain
  (signage at distance, not a brochure read at arm's length) and a different quantity: LRV
  is approximately linear reflectance, L\* is that under a cube-root compression, so the
  two numbers do not substitute 1:1 without doing the conversion per colour pair. The
  constraint is therefore re-expressed as a **WCAG relative-luminance ratio (4.5:1 body /
  3:1 large text) computed directly on these hex values at build time.** Every current
  render target is RGB end to end (T8), so these sRGB values *are* what gets rasterised —
  there is no separate print colour for a print-specific metric to diverge from. Because it
  needs no rendered artifact, `validate-contrast-print` moves out of the post-render bucket
  in §4 and into the build-time bucket.
- **L\* survives in exactly one place, and it is a different quantity.**
  `validate-text-safe-color` uses an *absolute* lightness ceiling on a single ink
  (`l_star_max=15`), not a pairwise delta between two. A mid-L\* ink — ENS's `#1F6F43` at
  L\*≈41 — photocopies to grey, and grey reads worse than black at the same size
  (`12-typescale-and-fstype.md` §Q1). Absolute lightness of one colour is well defined and
  computable; the delta that was cut was a property of a pair and had no standard behind
  it. Do not read the survival of L\* here as a partial retention of the delta.
- **`CMYK Overrides` is cut at Revision 1, for the same reason as T7's `Colour Space`.**
  It held `primary=88,32,84,22`-style values against a CMYK output path. There is no such
  path: tier 3 (`cmyk-press`) is unreachable on every render target until a redistributable
  ICC profile is bundled (T8), so nothing consumes these numbers and the only validator that
  could — `validate-color-space` — hard-fails on every current target anyway. It is also a
  `name=value` map, so under Rule 1 as rewritten it would need a closed grammar to survive,
  and a grammar for an unreachable feature is work spent on nothing. **When the ICC asset
  ships, this column comes back with it** — it is a tier-3 column, and tier 3 does not exist
  yet. Recorded here so its return is a decision rather than a rediscovery.
- **`Greyscale Distinct` is NOT a column here.** It is computable from the hexes, so
  storing it creates a second source of truth that can disagree with the first. It becomes
  `validate-greyscale`, which computes it.
- **Dropped from upstream `colors.csv`:** `Card` / `Card Foreground` (kept, renamed to the
  neutral `Muted` pair), `Ring` (a focus ring — screen-only), `Destructive` /
  `On Destructive` (application semantics, not document semantics). Cutting `Destructive`
  costs us ENS's `web-tool` type — deliberate: this is a document library, and a web-tool
  is not a document. That doctype stays with upstream's skill.

**Validators enabled:** `validate-contrast-screen` (WCAG 4.5:1 / 3:1),
`validate-contrast-print` (**re-based at Revision 1** — WCAG relative-luminance ratio on
these hexes, computed at build time; no longer a CIE Lab L\* delta),
`validate-text-safe-color` (absolute L\* ceiling for the smallest roles on photocopy-safe
doctypes), `validate-greyscale`, `validate-text-safe-roles`, `validate-palette-only` (no
hex in output outside the resolved palette — upstream's `html-token-validator.py` pattern,
`01-mechanism.md` §1.5).

---

## T5. `typefaces.csv`

**Purpose.** Families plus the per-medium behaviour that decides what a recipient actually
sees. `search_cols = [Display Name, Keywords, Best For]`.

| Column | Type | Example (ENS) | Example (generic) | S/V/R |
|---|---|---|---|---|
| `typeface_key` | slug | `ens-manrope-inter` | `cv-safe-sans` | R |
| `Display Name` | text | ENS Manrope + Inter | Safe sans (Arial/Calibri) | S |
| `Keywords` | text | ens, manrope, inter, clear, functional, down-to-earth | safe stack, arial, calibri, ats, no embedding, ubiquitous | S |
| `Best For` | text | ENS documents, forms, slides, social | CVs, documents that must survive any machine | S |
| `Brand Scope` | slug | `ens` | `generic` | R |
| `Heading Family` | text | Manrope | Arial | V |
| `Body Family` | text | Inter | Arial | V |
| `Mono Family` | text, nullable | — | — | V |
| `Category Contrast` | enum `serif-sans`\|`sans-sans`\|`serif-serif`\|`superfamily` | `sans-sans` | `sans-sans` | V |
| `Family Count` | int | `2` | `1` | V |
| `Safe Stack Fallback` | text | Arial | Arial | V |
| `Safe Stack Availability` | enum `os-bundled`\|`office-bundled`\|`none` | `os-bundled` | `os-bundled` | V |
| `Embedding Licence` | enum `installable`\|`editable`\|`preview-print`\|`restricted`\|`unknown` | `installable` | `editable` | V |
| `Has Tabular Figures` | enum `yes`\|`unknown` | `yes` | `unknown` | V |
| `Scale Key` | slug FK → T6 | `ens-print` | `cv-print` | R |

**Design notes.**

- **`Embedding Licence` is back, and cutting it was wrong.** I cut it on the premise that
  reading a font's `fsType` permission bit requires `fontTools`. `12-typescale-and-fstype.md`
  §Q2 disproves that premise directly: `fsType` is a fixed-offset `uint16` in the `OS/2`
  table, itself a fixed-offset entry in the sfnt table directory every `.ttf`/`.otf` opens
  with, so `struct` + `open` suffices. Verified on six real fonts across both TrueType
  (`\x00\x01\x00\x00`) and CFF-flavoured OpenType (`OTTO`). The column returns as a
  genuine **preflight** check.
- **Two checks, two different failure modes — keep both.** `validate-embedding-licence`
  checks *permission* before rendering; `validate-font-embedded` checks *outcome* after —
  for PPTX, open the package with stdlib `zipfile` and assert the font is present
  (`ppt/fonts/*`, with `<p:embeddedFont>` in `ppt/presentation.xml`); for DOCX,
  `word/fonts/*` with `w:embedRegular` in `word/fontTable.xml`. The first catches
  "embedded something it had no licence to embed"; the second catches report 03 §B's actual
  observed failure — *the option can be on and the font still won't embed, with no obvious
  warning*. It is also the check `ENS-plugin-rebuild-v2.md:56` asserts ("embedding ON,
  **verified**") without saying how. Now it says how, twice, at two different moments.
- **The licence validator's polarity, stated explicitly because it is easy to implement
  backwards.** `fsType` usage bits `0` (installable), `4` (preview & print) and `8`
  (editable) all permit embedding; only bit `2` (`restricted`) forbids it.
  `12-typescale-and-fstype.md` measured Arial, Calibri, Times New Roman and Consolas at
  `fsType=8` — so a validator that fails anything other than `installable` would reject
  every Microsoft core font, including the `Safe Stack Fallback` this table names.
  **`validate-embedding-licence` fails on `restricted` only**; `preview-print` and
  `editable` pass; `unknown` warns. Subsetting (`0x0100`) and bitmap-only (`0x0200`) flags
  are recorded in `rationale/typefaces.md`, not in the enum.
- **`Safe Stack Availability` is new at Revision 2, and it is the column that makes
  `Safe Stack Fallback` mean something.** "Safe" was doing unexamined work: `19-notes.md`
  verified against current sources that the classic Microsoft set bifurcates. Arial, Times
  New Roman, Georgia, Verdana, Trebuchet MS and Courier New are **OS-bundled** on both
  Windows and macOS. Calibri, Cambria, Candara, Corbel, Constantia and Consolas are
  **Office-bundled** — present on Windows, but absent from macOS unless Office for Mac is
  installed, and absent from LibreOffice entirely. The distinction bites exactly where T8's
  `Font Rule: safe-stack` applies: an unembedded `.docx` needs the font present in whatever
  application opens it, so an Office-bundled fallback is safe only if you may assume the
  recipient opens it in Microsoft Office. `validate-font-resolution` reads this column and
  warns when a `safe-stack` target resolves to an `office-bundled` family.
- **Two current facts worth recording before they go stale**, both verified in
  `19-notes.md` rather than recalled: Microsoft's default moved from Calibri to **Aptos**
  (2023+), so "Calibri is the default" is no longer true though Calibri is still bundled;
  and Aptos is too new to have a metric-compatible substitute, so it is `none` in T14.
- `Family Count` exists so report 03 §E's cap (2 families, 3 with mono) is a number a
  validator reads, not a sentence.
- **`Has Tabular Figures` drops `no` from its enum.** The check is a stdlib `GSUB`
  `FeatureList` scan for a `tnum` tag — the same fixed-offset technique as `fsType`, and
  `12-typescale-and-fstype.md` §Q2 built it. But **tag presence and "has tabular figures"
  are not the same fact**, and the counter-example is concrete: Consolas reports no `tnum`
  and is monospaced, so its digits are already fixed-width and need no switchable feature.
  A *missing* tag is ambiguous between "no tabular figures" and "always tabular, no feature
  needed." So the check strengthens `yes` and can never produce `no`: `tnum` present →
  `yes` (high confidence); `tnum` absent → stays `unknown`. A true `no` would need
  comparing `hmtx` advance widths for the digit glyphs, a materially harder variable-length
  parse that nobody has built.
- **`unknown` warns — never passes, never fails.** It covers two opposite realities
  (proportional digits, and tabular-by-default like Consolas) and the check cannot tell
  them apart. Silently passing would let a proportional-digit font into a numeric table;
  failing would reject Consolas. `validate-tabular-figures` on `unknown` emits a warning and
  defers to the §7 Q5 warn-channel decision.
- **Upstream's `google-fonts.csv` (1,923 rows, 15 columns) does not answer any of this.**
  It is a catalogue — Family, Subsets, Variable Axes, Popularity Rank. Repo-wide grep for
  `fsType` returns zero. That finding is about the *catalogue*, not about readability: the
  bit is trivially readable from the font binary (above); upstream simply never records it.
  Keep the file as an optional metadata lookup if we want font discovery; it cannot back
  T5's columns.
- **Dropped from upstream `typography.csv`:** `Google Fonts URL`, `CSS Import`, `Tailwind
  Config`. Three of eleven columns are web delivery mechanics.

**Validators enabled:** `validate-embedding-licence` (preflight, `fsType`; fails on
`restricted` only), `validate-font-embedded` (post-render `zipfile` assertion, per above),
`validate-font-resolution` (T5 × T8 join, see T8; warns on an `office-bundled` fallback),
`validate-family-count`, `validate-tabular-figures` (`unknown` ⇒ warn),
`validate-substitute-available` (T5 × T14 join, see T14).

---

## T6. `type-scales.csv` — long format

**Purpose.** Point sizes per medium and role. Long format, deliberately.
Not searched — resolved by key.

*Collapsed at Revision 1.* `12-typescale-and-fstype.md` §Q1 answered the two questions this
table was built on guesses about, and both answers shrink it.

| Column | Type | Example (ENS) | Example (generic) |
|---|---|---|---|
| `scale_key` | slug | `ens-print` | `deck-projection` |
| `Medium` | enum `print`\|`projection`\|`screen` | `print` | `projection` |
| `Role` | enum `legal`\|`label`\|`caption`\|`body`\|`body-dense`\|`lead`\|`h3`\|`h2`\|`h1` | `body` | `body` |
| `Size pt` | number | `11` | `24` |
| `Leading Ratio` | number | `1.35` | `1.20` |

All four value columns are **V** (routing on `scale_key` is inherited from T5).

**`legal` added to `Role` at Revision 4.** The enum is ordered by size, ascending, and
`legal` is the new floor — below `label`. It exists because T9 already ships
`legal-text-min-size` (`validate-type-floor`, threshold `8`) and
`legal-text-no-sustained-uppercase`, and a floor check needs a role to check *against*: with
no `legal` row in T6 the constraint has nothing to resolve to, and the 8 pt figure lives only
in the constraint's `Threshold` where no scale can contradict it. The role covers the fine
print a document is obliged to carry and nobody is expected to read comfortably — footers,
disclaimers, source lines, terms. It is deliberately **not** `caption`: a caption is meant to
be read alongside the thing it labels, and sizing the two together would drag captions down
to the legal floor.

**Change 1 — `photocopy` is cut as a `Medium`.** Report 03 contains no photocopy-specific
point-size threshold anywhere, and the photocopy risk is a **colour/weight** problem, not a
size problem: a mid-lightness ink renders as grey on a monochrome copy, and grey reads worse
than black at the same size. The mechanism is the colour. The risk moves to T9 as
`photocopy-safe-color` (`validate-text-safe-color`, `l_star_max=15`, `warn`), with the ENS
green-section-number finding as its worked example. The draft's `photocopy-body-min` row at
8.5 pt goes with it — there is no source for it as a size threshold.

**Change 2 — report 03 gives no absolute print point-size floor, so T6's print rows are not
sourced lookups.** Its two print typography rules are both **ratios**, not sizes: measure of
45–75 characters per line (Bringhurst) and leading of 120–145% of body size. Neither is a
point value. Any number written into `Size pt` for a print role is therefore either a
brand's own house choice — legitimate, but authored — or an invented threshold with exactly
the problem T11's `Min Physical Size mm` was already flagged for. **Print rows are
brand-authored constants validated by the formula below, never by a floor.** ENS's 11 pt
body and 8.5 pt labels are real ENS decisions, and `rationale/type-scales.md` must record
them as such so nobody later reads them as a sourced minimum.

**What is actually sourced** (`12-typescale-and-fstype.md` §Q1), and where it lives:

| Medium | Role | Value | Tag | Lives in |
|---|---|---|---|---|
| projection | body | 24 pt floor | CONVENTION, report 03 §B | T9 `proj-body-floor` |
| projection | body-dense | 18 pt floor — the dense-callout *exception*, not a default | CONVENTION, report 03 §B | T9 `proj-body-dense-floor` |
| projection | h1 / title | 36–44 pt range | CONVENTION, report 03 §B | T9 `proj-title-floor` |
| screen | body | 18–20 pt floor, screen-only decks, explicitly distinct from projection | CONVENTION, report 03 §B | T9 `screen-body-floor` |
| screen | h1 / title | *no source* — do not assume it inherits projection's range | — | nowhere |
| print | any role | *no source*; formula only | — | the formula below |

**Why the floors are T9 rows and not a `Value Basis` column on T6.** The obvious move is a
column marking each row sourced-floor or brand-authored. It is the wrong move for the same
reason `Min L* Delta` was cut from T4: a floor is a **threshold**, and thresholds live in
T9. Four sourced tuples do not earn a column that would then encode the sourced/authored
decision in two places and let them disagree. T6 holds authored values; T9 holds the floors
they are checked against; `validate-type-floor` is the join — which is precisely the reason
this table is long format.

**The formula that replaces a print size floor.** Two validators share it —
`validate-measure` (the CPL half, scoped by T9's `Element Scope`) and
`validate-leading-ratio` — with every input named, because a formula whose inputs are
implicit is prose with an equals sign in it:

- `M` = T7 `Measure mm` — the text column width of the resolved page format
- `S` = T6 `Size pt` where `Medium=print`, `Role=body`, on the resolved `Scale Key`
- `L` = T6 `Leading Ratio` for that same row
- `W` = average character advance width of T5's resolved `Body Family`, in em

Then:

```
S_mm = S × 25.4 / 72
CPL  = M / (S_mm × W)
assert 45 <= CPL <= 75      # validate-measure       — Bringhurst, report 03 §D, convention
assert 1.20 <= L <= 1.45    # validate-leading-ratio — report 03 §D, convention
```

**Why two validators and not one.** They were bundled until Revision 2. Measure scopes by
container — ENS's acceptance test found that a page-wide 130 mm measure cramped a table, so
tables are exempt (T9 `Element Scope`) — while leading applies to every text run
regardless of the block it sits in. One validator cannot carry two scopes, and the authored
CSV had already split them.

`W` is the only input not already in a table. Read it from the font binary: sum `hmtx`
advance widths over a representative character set and divide by `unitsPerEm` from `head` —
both fixed-offset stdlib reads, the same technique `fsType` uses (T5). Where the font cannot
be opened — a `safe-stack` target naming a family we do not ship — fall back to `W = 0.5` em
and **downgrade the assertion to a warning**, because the input is then an estimate rather
than a measurement and a hard fail on an estimate is a false precision.

**Example rows**

```
ens-print       | print      | label      | 8.5 | 1.20   (brand-authored)
ens-print       | print      | body       | 11  | 1.35   (brand-authored)
ens-print       | print      | h1         | 24  | 1.10   (brand-authored)
deck-projection | projection | body       | 24  | 1.25
deck-projection | projection | body-dense | 18  | 1.25
deck-projection | projection | h1         | 36  | 1.10
```

**Why long format, not a `print.body=11;print.h1=24` cell.** A mini-syntax here is a map
with an unbounded key space — the cross product of two enums — so Rule 1 as rewritten still
forbids it: there is no closed vocabulary to validate it against. Long format also makes
`validate-type-floor` a **join** against T9 rather than a string parse, which is the
difference between a check that works and a check that works until someone types a
semicolon.

**Scale is its own entity, referenced by T5.** Most typefaces share a scale, so keying it
separately dedupes hard.

**Validators enabled:** `validate-type-floor` — resolved `Size pt` for a
(`Medium`, `Role`) pair must clear the floor T9 sets for it, where T9 sets one (projection
and screen only); `validate-measure` and `validate-leading-ratio` — the print path, per the
formula above.

---

## T7. `page-formats.csv` — no upstream analog

**Purpose.** Physical geometry. This is the table upstream has no version of, and its
absence is the whole finding of `05-SYNTHESIS.md:252` ("No column exists for page format,
margins, measure, running heads, bleed, paper"). `search_cols = [Display Name, Keywords]`.

*Print columns populated at Revision 1* from `14-print-production-values.md` §2, which was
commissioned for exactly this (§5).

| Column | Type | Example (ENS) | Example (generic) | S/V/R |
|---|---|---|---|---|
| `page_format_key` | slug | `a4-ens-note` | `letter-trifold` | R |
| `Display Name` | text | A4 — ENS note interne | US Letter — tri-fold brochure | S |
| `Keywords` | text | a4, note interne, side column | letter, trifold, brochure, leaflet, fold | S |
| `Trim W mm` / `Trim H mm` | number | `210` / `297` | `279.4` / `215.9` | V |
| `Bleed mm` | number | `0` | `3` | V |
| `Safe Margin mm` | number | `0` | `3` | V |
| `Margin Top/Bottom/Inside/Outside mm` | number ×4 | `20`/`20`/`25`/`55` | `10`/`10`/`6`/`6` | V |
| `Measure mm` | number | `130` | `89` | V |
| `Columns` | int | `1` | `1` (per panel) | V |
| `Running Head` | enum `none`\|`verso-recto`\|`centered` | `none` | `none` | V |
| `Folio Style` | enum `none`\|`arabic`\|`roman-front-arabic-body` | `arabic` | `none` | V |
| `Fold Type` | enum `none`\|`tri-fold`\|`z-fold`\|`gate-fold`\|`roll-fold` | `none` | `tri-fold` | R V |
| `Panels mm` | number list, nullable | — | `93.66;93.66;92.08` | V |
| `Stock gsm` | int, nullable | — | `120` | V |
| `Print Mode` | enum `office`\|`photocopy`\|`professional` | `photocopy` | `professional` | R V |
| `Min DPI Raster` | int | `150` | `300` | V |
| `Min DPI Line Art` | int | `600` | `600` | V |

**Sourced values for the print columns.** Tags preserved from
`14-print-production-values.md` §2. These are the values authors draw on; they are not
themselves a column, for the same reason `Evidence Class` was cut from T9 — provenance that
does not change validator behaviour belongs in `rationale/page-formats.md`, and this table
is that rationale in summary form.

| Item | Value | Tag |
|---|---|---|
| A4 / A5 / A3 / A2 / A1 | 210×297 / 148×210 / 297×420 / 420×594 / 594×841 mm | FACT — ISO 216 |
| US Letter | 215.9 × 279.4 mm | convention, US/CA — no ISO analog |
| DL envelope | 110 × 220 mm | FACT — ISO 269 |
| DL leaflet (⅓ A4) | 99 × 210 mm | convention — derived from the A4 tri-fold panel, not an ISO size |
| Business card EU / US / A8 | 85×55 / 88.9×50.8 / 74×52 mm | convention, regional (A8 is FACT but rare in practice) |
| Bleed, standard formats | 3 mm (0.125 in) — a floor, not a ceiling | convention, near-universal shop minimum; depends on shop |
| Bleed, large format | 5–10 mm | convention; depends on shop and substrate |
| Safe margin, business card | 5 mm (≈7 mm clear where corners are rounded) | convention; depends on shop |
| Safe margin, poster/flyer ≤A2 | 6 mm (0.25 in) | convention |
| Safe margin, large-format ≥36×48 in | 12.7 mm (6–10 for banners) | convention — cutting tolerance widens on large sheets |
| Safe margin, A4/A5/DL | 3–6 mm | convention; sources do not differentiate this range by format |
| Trim/cutting tolerance | 0.5–1.5 mm, up to ~2 on multi-sheet stacks | convention/shop-spec — stack shift dominates, not blade tolerance |
| Z-fold, US Letter | 93.13 / 93.13 / 93.14 mm | FACT — no panel tucks, so no thickness compensation |
| Tri-fold, US Letter | 93.66 / 93.66 / 92.08 mm | convention, shop spec — sums to 279.40 exactly |
| Tri-fold, A4 | 99.5 / 99.5 / 98.0 mm | convention — no single authoritative A4 source; figures cluster here |
| Gate-fold, finished width W | wide = W/4 + 0.8; narrow = wide − 1.6 mm | shop formula |
| Roll-fold, 4+ panels | each inward panel narrower by 1.5 (text) or 3 (cover) mm per nest | convention — **no closed form exists**, so no roll-fold row was authored; the `Fold Type` value stays in the enum for when one is |
| Fold-in allowance, text stock 80–120 gsm | ≈0.8 mm per fold | shop convention |
| Fold-in allowance, cover stock 200–300 gsm | 1.5–3 mm per fold | shop convention |
| Scoring required above | 170 gsm | convention, general bindery practice |
| Stock, any multi-panel fold | 80–100 lb text ≈ 120–150 gsm; avoid cover stock entirely | convention |
| Stock, business card | 14–18 pt ≈ 350–450 gsm | convention |
| Stock, single-panel flyer/poster | ~200 gsm+ | **cannot be sourced to a figure** — see §8 |
| Min DPI, continuous tone <1 m | 300 | convention — 2× a 150 lpi halftone screen |
| Min DPI, line art / 1-bit | 600–1200 | convention |
| Min DPI, large format 1–2 m / 3 m+ | 150 / ≤100 | convention — halve per doubling of viewing distance |
| Min DPI, office / photocopy | 150 | matches this schema's own existing convention |

**Design notes.**

- `Measure mm` is ENS's *"Text measure 130 mm"* (`ENS-plugin-rebuild-v2.md:133`) — the
  reason its right margin is 55 mm, so a side column stays free for handwritten notes. A
  real, load-bearing, entirely non-web number that upstream's library cannot express.
- **CPL is computed, not stored.** `validate-measure` (T6) computes
  characters-per-line from `Measure mm`, `Size pt` and the font's average character width.
  Storing a CPL range per format would be a second source of truth for a derived value —
  same reasoning that cut `Greyscale Distinct`.
- **`Safe Margin mm` is a separate column from `Bleed mm` and both are separate from the
  four `Margin` columns.** They answer three different questions: how far art extends
  *past* the trim, how far content must stay *inside* it, and where the text block sits.
  The safe margin absorbs the guillotine's 0.5–1.5 mm cutting tolerance, which is why it is
  not itself a column — a tolerance the safe margin already covers would be a second
  encoding of one decision.
- **`Fold Type` decides which fold rule applies, which is why it is a column and not
  inferable from `Panels mm`.** A Z-fold's panels are equal because no panel tucks inside
  another; every other fold's innermost panel must be narrower or the piece will not close
  flat — the mechanical reason behind the asymmetry, sourced rather than asserted. With
  `Fold Type` and `Stock gsm`, `validate-fold-geometry` checks three things instead of one:
  panels sum to the folded dimension; for non-Z folds the tuck panel is narrowest by at
  least the stock's fold-in allowance (0.8 mm text, 1.5–3 mm cover); and stock above
  170 gsm carries a scoring note.
- **`Colour Space` is cut.** It was `sRGB`\|`CMYK` and it encoded one decision twice:
  `14-print-production-values.md` §2.6 is explicit that for office and photocopy modes the
  value is "not an independent print-industry fact, a pipeline consequence" — it follows
  from T8's engine capability — while for `professional` it follows from `Print Mode`.
  Either way the page format is not where it is decided. What replaces it is T8's
  `Print Tier Max` (below), which is the thing a resolver actually needs to answer.
- `Print Mode` gates three consistent bundles rather than letting bleed / DPI / stock be
  set independently and incoherently. Kept inline rather than normalised — three rows does
  not earn a join. If a fourth mode appears, normalise.

**Validators enabled:** `validate-measure`, `validate-leading-ratio`,
`validate-fold-geometry`,
`validate-bleed` (artboard = trim + 2×bleed), `validate-safe-margin` (no content inside
`Safe Margin mm` of the trim edge), `validate-pagination`, `validate-dpi` (both floors),
`validate-print-mode-coherence` (see T8).

---

## T8. `render-targets.csv` — no upstream analog

**Purpose.** Resolve the output-format fork as data, including the engine decision and its
fallback chain. Not searched — resolved by key from T1.

*Corrected and extended at Revision 1.* The previous revision's flat `no` on bleed and CMYK
for every row was stale for WeasyPrint on both axes (`14-print-production-values.md` §1).

| Column | Type | Example A | Example B | S/V/R |
|---|---|---|---|---|
| `render_key` | slug | `pdf-chromium` | `docx-office` | R |
| `Format` | enum `pdf`\|`docx`\|`pptx`\|`png`\|`html` | `pdf` | `docx` | R |
| `Engine` | text | headless-chromium | python-docx | R |
| `Engine Path` | text | `/opt/google/chrome/chrome` | `docx` (module) | V |
| `Engine Min Version` | text, nullable | — | — | V |
| `Engine Invocation` | text | `--headless --no-sandbox --disable-gpu --print-to-pdf=%o --no-pdf-header-footer %i` | — | V |
| `Font Rule` | enum `embed`\|`safe-stack`\|`inline-webfont` | `embed` | `safe-stack` | R V |
| `Supports Paged Media` | bool | `yes` | `n/a` | V |
| `Supports Bleed` | bool | `no` | `n/a` | V |
| `Supports CMYK` | bool | `no` | `n/a` | V |
| `Print Tier Max` | enum `none`\|`submittable-rgb`\|`pdfx4-rgb`\|`cmyk-press` | `submittable-rgb` | `none` | V |
| `Editable By Recipient` | bool | `no` | `yes` | R |
| `Availability` | enum `preinstalled`\|`pip`\|`unverified` | `preinstalled` | `preinstalled` | V |
| `Fallback Render Key` | slug FK, nullable | `pdf-weasyprint` | — | R |

**Example rows** (columns abbreviated to those that differ)

```
render_key            fmt  engine        min-ver  bleed cmyk  tier              avail         fallback
pdf-chromium          pdf  chromium      —        no    no    submittable-rgb   preinstalled  pdf-weasyprint
pdf-weasyprint        pdf  weasyprint    0.41     yes   no    submittable-rgb   pip           pdf-wkhtmltopdf
pdf-weasyprint-pdfx4  pdf  weasyprint    67.0     yes   yes   pdfx4-rgb         pip           pdf-weasyprint
docx-office           docx python-docx   —        n/a   n/a   none              preinstalled  —
pptx-office           pptx python-pptx   —        n/a   n/a   none              preinstalled  —

pdf-weasyprint-pdfx4 Engine Invocation adds: --pdf-variant=pdf/x-4 --output-intent=srgb
```

**Print becomes three tiers, as data.** `14-print-production-values.md` §1 settles §7 Q2 by
splitting the question the previous revision treated as binary:

1. **`submittable-rgb`** — correct trim size, fonts embedded, images clear the DPI floor,
   art physically extends past the trim where bleed is declared. No PDF/X machinery; the
   shop's prepress does colour conversion and box interpretation. **Reachable on every
   current target**, and honest to promise today.
2. **`pdfx4-rgb`** — a structurally valid PDF/X-4 file (ISO 15930-7) whose content never
   leaves RGB, carrying an sRGB output intent. PDF/X-4 permits this where PDF/X-1a forbids
   RGB outright. **WeasyPrint ≥67 only**, via `--pdf-variant=pdf/x-4 --output-intent=srgb`.
   It needs no CMYK asset and no licensing decision, because sRGB (IEC 61966-2-1) ships with
   essentially every OS — unlike the GRACoL/SWOP profiles Adobe distributes under its own
   terms.
3. **`cmyk-press`** — full press-ready CMYK. **Hard-fails everywhere today.** The engine
   capability exists (WeasyPrint ≥67 added `device-cmyk()`, `@color-profile` and
   `--output-intent`), which is why `Supports CMYK` is `yes` on that row; what is missing is
   a redistributable CMYK ICC profile shipped as a binary asset. That is a packaging
   decision, not an engine one — ECI's `ISOcoated_v2_eci.icc` is stated freely
   distributable, Adobe's profiles are not. Until the asset ships, no row reaches tier 3.

**Note the deliberate separation: `Supports CMYK` is an engine capability;
`Print Tier Max` is what this row's invocation actually delivers.** They differ on
`pdf-weasyprint-pdfx4` precisely because tier 3 is gated on an asset rather than on the
engine, and collapsing them would hide which of the two is missing.

**Where the tier lives, and why it is not on T7.** A print tier is a property of the
(engine, invocation) pair — which is exactly what a T8 row *is* — not of page geometry. One
A4 `professional` format reaches tier 1 through Chromium and tier 2 through WeasyPrint;
same geometry, different tier. Putting a `Print Tier Required` column on T7 would encode one
decision twice, since it would be a function of `Print Mode` — the sin that cut
`Min L* Delta` and `Evidence Class`. **The `Print Mode` → minimum-tier mapping is a constant
in the resolver, not a column** (`office`/`photocopy` → tier 1, `professional` → tier 2),
because Rule 1 puts logic in code.

`validate-print-mode-coherence` is rewritten accordingly: *the resolved target's
`Print Tier Max` must be ≥ the floor the format's `Print Mode` requires, else hard-fail,
naming the tier reached and the tier required.* That is the check that lets the resolver say
which tier a request can reach and refuse tier 3 rather than silently emitting an RGB PDF
and calling it press-ready.

**Design notes.**

- This table is `05-SYNTHESIS.md:212-230` turned into rows: Chromium primary (preinstalled,
  verified invocation including the mandatory `--no-pdf-header-footer`), WeasyPrint optional,
  wkhtmltopdf last and avoided.
- **`Availability` absorbs the tier risk, and this is the reason that column exists.** Tiers
  2 and 3 live only on WeasyPrint, WeasyPrint is `pip`, and pip means network — which the
  synthesis at `:199-201` already recorded as not guaranteed (it was installed on the fly,
  session-scoped). A doctype whose `professional` print mode can only be satisfied by a
  `pip` target therefore fails preflight when network is absent, and fails loudly rather
  than degrading to tier 1 unannounced.
- **`Engine Min Version` is new and load-bearing, not bookkeeping.** Tier 2 needs WeasyPrint
  ≥67.0 (`--pdf-variant` / `--output-intent`, released 2025-12-02); bleed needs ≥0.41.
  `pip` gives whatever it gives — currently 69.0 — so `validate-engine-available` must check
  the version, not merely the presence, or a tier-2 request silently produces a tier-1 file.
- **Chromium's row stays `no`/`no`, and that is not pessimism.** Its output has no
  `TrimBox`/`BleedBox`, no `/OutputIntents`, and RGB content only. Several of T9's
  professional-print checks are consequently *always* failing on Chromium — which is
  `validate-print-mode-coherence` doing its job at the target level, not a per-document
  defect.
- **`Font Rule` × T5 is the join that answers requirement 4.** ENS's rule reads
  *"Manrope+Inter embedded in PDF/HTML/PNG/PPTX; Arial in DOCX/XLSX"*
  (`ENS-plugin-rebuild-v2.md:114`). Under this schema that sentence is not stored anywhere —
  it is **derived**: `pdf-chromium.Font Rule = embed` → use `Heading/Body Family`;
  `docx-office.Font Rule = safe-stack` → use `Safe Stack Fallback` (Arial). One join, and a
  new document type inherits the rule automatically instead of needing it restated.

**Validators enabled:** `validate-font-resolution`, `validate-font-embedded`,
`validate-print-mode-coherence` (tier comparison, per above), `validate-engine-available`
(presence **and** `Engine Min Version`).

---

## T9. `constraints.csv` — no upstream analog

**Purpose.** Every mechanically-checkable rule from report 03, as rows. This is the table
that makes the rest enforceable. Not searched — resolved by `Set Key` from T1.

| Column | Type | Example A (ATS) | Example B (projection) | S/V/R |
|---|---|---|---|---|
| `constraint_key` | slug | `ats-no-multi-column` | `proj-body-floor` | R |
| `Set Key` | slug | `ats-strict` | `projection` | R |
| `Applies To` | enum `artifact-class:*`\|`format:*`\|`doctype:*` | `doctype:cv-*` | `artifact-class:canvas` | R |
| `Check` | validator fn name | `validate-ats-structure` | `validate-type-floor` | V |
| `Element Scope` | enum `body-paragraph`\|`table-cell`\|`caption-block`\|`sidebar-column`\|`header-footer`; empty = whole document | *(empty)* | *(empty)* | R V |
| `Parameter` | closed grammar, per `Check` | `columns` | `medium=projection;role=body` | V |
| `Threshold` | literal, or `<table>:<Column Name>` reference | `0` | `cv-regions:Max Pages` | V |
| `Severity` | enum `fail`\|`warn` | `fail` | `fail` | V |

**Example rows**

*Realigned at Revision 2 to `16-t9-constraints-draft.csv`, which is authored, sourced and
provenance-tagged where these were illustrative. Where they disagreed, the CSV won.*

```
constraint_key        Set Key            Applies To             Check                          Element Scope   Parameter                             Threshold      Sev.
ats-no-multi-column   ats-strict         doctype:cv-*           validate-ats-structure         —               columns                               0              fail
ats-no-textbox        ats-strict         doctype:cv-*           validate-ats-structure         —               text_boxes                            0              fail
ats-text-layer        ats-strict         doctype:cv-*           validate-text-layer            —               selectable_ratio                      1.0            fail
cv-page-count         cv-region          doctype:cv-*           validate-page-count            —               —                                     cv-regions:Max Pages  warn
cv-field-norms        cv-region          doctype:cv-*           validate-text-safe-fields      —               fields=photo|dob|marital|visa         —              warn
proj-body-floor       projection         artifact-class:canvas  validate-type-floor            —               medium=projection;role=body           24             warn
deck-density-bullets  projection         artifact-class:canvas  validate-density               —               bullets_per_slide                     6              warn
ens-deck-density      ens-house          doctype:ens-*          validate-density               —               bullets_per_slide                     5              warn
report-measure-cpl    report-typography  artifact-class:flow    validate-measure               body-paragraph  cpl_min=45;cpl_max=75                 45-75          warn
report-leading-ratio  report-typography  artifact-class:flow    validate-leading-ratio         —               ratio_min=1.20;ratio_max=1.45         1.20-1.45      warn
photocopy-safe-color  photocopy-safe     doctype:*              validate-text-safe-color       —               roles=label|legal;metric=text_l_star  15             warn
print-contrast-ratio  print-legibility   doctype:*              validate-contrast-print        —               —                                     4.5            warn
ens-lime-never-text   ens-house          doctype:ens-*          validate-text-safe-roles       —               role=accent                           0              fail
pptx-font-embedded    projection         format:pptx            validate-font-embedded         —               target=ppt/fonts                      present        fail
redesign-text-frozen  redesign           doctype:*-redesign     validate-content-preservation  —               —                                     0              fail
```

**The `professional-print` set** — adopted wholesale at Revision 1 from
`14-print-production-values.md` §3. Each row already carries a severity and a stdlib
feasibility verdict, which is why it is adopted rather than adapted. The feasibility column
is not a schema column; it belongs in `rationale/constraints.md` and is reproduced here
because it is the honest cost of the set.

| `constraint_key` | Check | Threshold | Sev. | stdlib-checkable on a Chromium PDF |
|---|---|---|---|---|
| `pro-bleed-geometry` | `validate-bleed` | bleed ≥3 mm (≥5 large-format) | fail | **no** — Chromium emits no TrimBox/BleedBox at all; on WeasyPrint `@page{bleed;marks}` output, partial (a regex-scannable dictionary entry once decompressed) |
| `pro-output-intent-present` | `validate-output-intent` | `/OutputIntents` with `/S /GTS_PDFX` + `/DestOutputProfile` | fail | **no** on Chromium (never present); partial in general — dictionary presence is scannable, validating the embedded ICC binary is not |
| `pro-color-space-cmyk` | `validate-color-space` | 0 occurrences of `rg`/`RG`/`/DeviceRGB` | fail | **no** on Chromium (100% RGB by construction); partial in general — vector and text operators are catchable, raster images' internal colour mode is not |
| `pro-fonts-embedded` | `validate-font-embedded` | 100% of `/Font` have `/FontFile*` | fail | **partial/yes** — dictionary scan; caveat if the writer uses compressed object streams |
| `pro-trim-safe-margin` | `validate-safe-margin` | ≥ T7 `Safe Margin mm` from the trim edge | warn | **no** — needs glyph placement resolved against a real TrimBox; a layout problem, not a dictionary scan |
| `pro-min-dpi-raster` | `validate-dpi` | T7 `Min DPI Raster` / `Min DPI Line Art` | warn | **yes** — `/Width`/`/Height` are plain dictionary entries and placement comes from the transform matrix; no image decoding needed |
| `pro-spot-color-declared` | `validate-spot-color` | `/Separation` naming the brand's spot | warn | **partial** — regex over decompressed streams |

A structural note behind every "partial": PDF is largely a plain-text object-dictionary
format with `FlateDecode` streams, and both `re` and `zlib` are stdlib. That makes presence
checks and content-stream token scans genuinely feasible. It does **not** make full PDF
semantics feasible — indirect object graphs, compressed cross-reference streams, embedded
image colour modes. There is no PDF object model in the standard library, and no row above
pretends otherwise.

**Design notes.**

- **`Element Scope` is new at Revision 2, and the pilot's acceptance test paid for it.**
  ENS's rebuilt plugin passed on all three deliverables, and the one rule that needed
  correcting was the measure: *"130 mm measure applied page-wide cramped a table and forced
  a second page. Corrected rule: body-text measure 130 mm; tables may use full width"*
  (`05-SYNTHESIS.md:578-581`). A page-wide measure constraint is wrong, not merely strict.
  The DDR reached the same conclusion independently and encoded it inside `Parameter` as
  `scope=body-paragraph;exempt=table-cell|caption|sidebar-column`; promoting it to a column
  makes it a routing key the resolver can filter on rather than a string a validator has to
  parse, and it empties that Parameter cell of everything but the CPL bounds.
- **`Element Scope` is orthogonal to T6's `Role`, and the two vocabularies must never
  share a token.** The discriminating case is exactly the ENS one: body text at 130 mm and
  body text *inside a table* at full width are the same `Role` in different containers. So
  `Role` answers "what size is this text" and `Element Scope` answers "what block is it
  in." `legal` stays a `Role` — hence `photocopy-safe-color` keeps `roles=label|legal` in
  `Parameter` with an empty `Element Scope`. The one token that would have collided is
  renamed: the CSV's exempt-list `caption` becomes **`caption-block`** as an element,
  because `caption` is already a `Role` and one token must not mean two things. That is a
  one-cell edit for the DDR and it is in the §9 mapping.
- **Empty means whole document, and there is no `all` value.** The column is an allow-list:
  naming elements narrows the check, naming nothing leaves it document-wide. An explicit
  `all` would be a second spelling of empty, and the two would eventually disagree about
  which is the default. The counter-example that settles the design is
  `validate-content-preservation` (§4 entry 13): it must catch a changed word *anywhere*,
  so its scope is empty — and a rule whose correct scope is "everywhere" proves the column
  has to be optional rather than mandatory-with-a-wildcard.
- **The reference form is numeric-only, deliberately.** `Threshold: cv-regions:Max Pages` is an
  int resolving into a slot that expects an int. T12's field columns are *directions*
  (`expected` / `negative-signal` / `contested`), not ceilings, so they must never appear
  there — an enum resolved into a numeric threshold would pass
  `validate-checks-implemented`'s existence check and fail at runtime. Field norms therefore
  bind `validate-text-safe-fields` with an **empty** `Threshold`: the validator reads T12
  through the doctype's `Region Key` itself, including the inverted polarity Gulf needs. That
  is Rule 4 working as intended — the row binds, the validator resolves. Until the per-parameter
  typing in §8 item 6 exists, `validate-checks-implemented` cannot enforce numeric-only, so
  this is a convention the manifest states and the parser does not yet check.
- **`Threshold` may now reference another table, and that collapsed five rows into one.**
  `18-cv-region-rules.csv` holds `max_pages` per (region, band); the CSV also had
  `us-cv-length-under10y`, `us-cv-length-10y-plus`, `uk-cv-length`, `eu-cv-length` and
  `gulf-cv-length` each restating a page ceiling. Two sources of truth for one fact. Under
  Rule 4 the T9 row is a **binding**, so the binding survives and the threshold resolves:
  one `cv-page-count` row with `Threshold: cv-regions:Max Pages`, looked up through the doctype's
  `Region Key` and the computed seniority band. The `condition=experience_years<10`
  Parameter disappears with it, because the band *is* the lookup key.
- **Constraint sets union; they do not override.** T1 names several `Constraint Set Keys`,
  and this is the first revision where two rows bind the same validator at different
  thresholds — generic `deck-density-bullets` at 6 (report 03's 6×6) and ENS's house
  preference at 5. Both fire. Note the brand row is keyed **`ens-deck-density`, not
  `deck-density`**: §0.3 makes a brand slug colliding with a base slug a refuse-to-run, so
  a brand cannot silently shadow a generic row, only add a stricter one alongside it.
- **A region convention that conflicts with a `fail` constraint loses, and DACH is the
  worked example.** `18-notes.md` records that the traditional German *tabellarischer
  Lebenslauf* is a two-column layout — which `ats-no-multi-column` forbids at `fail`
  severity for every CV doctype. These are not reconcilable by tuning. The precedence rule:
  **a `fail`-severity structural constraint outranks a `warn`-severity regional convention,
  and the convention degrades to its content-level residue.** The resolver therefore emits
  an ATS-safe single-column structure carrying DACH-appropriate *content* (the fields and
  section order T12 specifies for that region), not a DACH-appropriate *layout*. Stated
  here rather than left to a resolver author to rediscover, because the two rules look
  independent until they collide on one document.
- **`print-l-delta` is dropped and replaced by `print-contrast-ratio`.** The L\* delta floor
  had no standard behind it, and `14-print-production-values.md` §4 confirms that as an
  *absence* rather than a failure to find one: WCAG's ratios are defined for self-luminous
  sRGB displays and have no adopted print equivalent; ISO 12647-2 governs press calibration,
  not legibility; ADA/ANSI A117.1's ≥70% LRV is real but scoped to signage at distance and
  is a different quantity from L\* (see T4). The replacement is the **WCAG
  relative-luminance ratio, 4.5:1 body / 3:1 large text, computed on T4's hex values at
  build time** — no rendered PDF required, which makes it the strongest check in the print
  set rather than the weakest. Severity stays `warn`: the formula is real and published, but
  applying a screen-derived threshold to paper is still convention. **Two rows collapse into
  this one, not one**: the CSV independently drafted `print-legibility-l-delta` under a
  broader `print-legibility` Set Key, correctly observing that report 03 §E's rule is
  general rather than professional-print-only. Both are superseded by the same finding —
  there is no standard behind the L\* floor — so the surviving row takes the CSV's broader
  Set Key and scope (`doctype:*`, every medium, since every target is RGB end to end) and
  the Print Specialist's basis. Its `Parameter` is empty; the thresholds are the WCAG
  constants.
- **`photocopy-body-min` is dropped and replaced by `photocopy-safe-color`.** There is no
  source for 8.5 pt as a photocopy size threshold (`12-typescale-and-fstype.md` §Q1). The
  real mechanism is colour: a mid-L\* ink photocopies to grey. `l_star_max=15` on the
  smallest roles, `warn` — warn rather than fail because the threshold is the researcher's
  own convention-level reasoning, not a report 03 [FACT].
- **`Parameter` is a closed grammar now, not "the one place I accept the smell."** Under
  Rule 1 as rewritten (§0.1) it is licensed on the same terms as T2's `Doc Conditions`: each
  validator function declares the parameter names it accepts, and
  `validate-checks-implemented` is extended to reject a `Parameter` key the named `Check`
  does not declare. Untyped, it would be forbidden. Typed, it is an enum keyed by function.
  The previous revision's "if it grows past two keys, normalise it" instinct is superseded —
  what made it risky was the absence of a type, not the number of keys.
- **There is still no `Evidence Class` column, and the reason is now cleaner.** The original
  argument used the L\* delta as its example of a FACT enforced softly; that example is
  gone. It is replaced by a better one: `print-contrast-ratio` rests on a real, rigorously
  published formula and is `warn` because it is applied out of its domain, while **ENS's
  house rules are pure CONVENTION and hard-fail**. Provenance and severity are still not 1:1,
  so two columns would encode one decision twice and disagree within a year. Severity is a
  policy call per constraint; provenance goes in `rationale/constraints.md`.
- **`Severity: warn` is load-bearing, not a cop-out.** Report 03 §5 is explicit that ATS
  vendor behaviour differs by vendor and drifts, and that its rules are "conservative
  safe-under-any-parser" rather than verified current behaviour for a named vendor. Region
  conventions likewise. Encoding that uncertainty as `warn` is more honest than either
  hard-failing on a convention or dropping the rule. What `warn` *does* remains §7 Q5.

**Validators enabled:** this table *is* the validator manifest. Every `Check` value must
resolve to an implemented function, and every `Parameter` key must be one that function
declares — `validate-checks-implemented` runs at build time and hard-fails on either. That
check is what stops this table degrading into the aspirational-rule list every design system
accumulates.

---

## T10. `structures.csv`

**Purpose.** Section order and document skeleton — report 03 §A (CV ordering) and §D
(report conventions). `search_cols = [Display Name]`.

| Column | Type | Example (ENS) | Example (generic) | S/V/R |
|---|---|---|---|---|
| `structure_key` | slug | `ens-note` | `cv-experienced` | R |
| `Display Name` | text | ENS note interne | CV — experienced hire | S |
| `Section Order` | slug list, FK → T13 `canonical_section` | `header;title;body;table?;signoff;footer` | `contact;summary?;experience;education;skills;certifications?` | V |
| `Heading Language` | enum `en`\|`fr`\|`de` | `fr` | `en` | R V |
| `Heading Depth Max` | int | `2` | `2` | V |
| `TOC Depth` | int | `0` | `0` | V |
| `Front Matter Numbering` | enum `none`\|`roman` | `none` | `none` | V |
| `Caption Position` | text | `fig=below;table=above` | `fig=below;table=above` | V |
| `Cross-Ref Style` | enum `numbered`\|`positional` | `numbered` | `numbered` | V |

**Design notes.**

- **`Canonical Headings` is cut and replaced by a join, at Revision 2.** It was a
  pipe-separated list cell, English-only. `18-ats-headings.csv` authored the real dictionary
  — 11 canonical sections × 3 languages (EN/FR/DE, because Luxembourg is the pilot market) —
  and the list cell cannot hold three languages without either a language-tagged mini-syntax
  inside the cell, which Rule 1 forbids, or one T10 row per language, which duplicates every
  other column in this table. The dictionary becomes **T13**, and `validate-canonical-headings`
  joins `Section Order` × `Heading Language` → T13.
- **What I did *not* adopt, and why:** the recommendation was a `Headings Key` FK column.
  There is nothing for it to point at. T13 is keyed `(canonical_section, language)`, and
  T10 already names its sections in `Section Order` — so the only missing half is the
  language, which is one enum column. A `Headings Key` would be a third key naming a set
  that is already fully determined by two columns this table has. The *substance* of the
  recommendation — headings become their own FK'd table, the list cell dies — is adopted in
  full.
- **`Section Order` is now a foreign-key list, which extends `validate-keys`.** Its slugs
  must match T13's `canonical_section` values byte-identically. That is a new obligation on
  a column that was previously free-form, and it is safe only because Rule 3 already
  requires linkage on slugs rather than display text — the heading *text* a reader sees
  lives in T13 and is free to be reworded.
- **`Section Order Early Career` is cut, at Revision 2.** It covered the early-career
  Education-above-Experience swap, which `18-cv-region-rules.csv` also holds as
  `education_before_experience` per (region, band). Two sources of truth for one fact. T12
  wins, because the swap is not universal — it interacts with region — and a nullable column
  here could never express that. This is the second column this revision deletes for
  duplication, and both were mine.
- `Cross-Ref Style: positional` exists only so it can be forbidden — report 03 §D notes
  "see figure below" breaks the moment pagination reflows, which is precisely what a flow
  layer does constantly.
- **Deliberately out of scope: narrative arc.** Upstream's `slide-strategies.csv` (15 deck
  structures with emotion arcs and Duarte sparkline beats) is *rhetoric*, not layout. It
  is a real gap — `02-coverage-gaps.md` §4.7 names it — but it belongs in a content
  library, not this one, and mixing them would put "curiosity→frustration→hope" in the
  same table as TOC depth. Flagged for a later `narratives.csv`.

**Validators enabled:** `validate-section-order`, `validate-canonical-headings` (T10 ×
T13 join), `validate-heading-depth`, `validate-caption-position`, `validate-cross-refs`.

---

## T11. `figures.csv` — derived from upstream `charts.csv`

**Assessment of upstream `charts.csv` (25 rows, 14 columns), as asked.** It is the most
medium-neutral table upstream has, but "nearly neutral" overstates it. Counted:

**Genuinely medium-neutral — keep (9/14):** `Data Type`, `Keywords`, `Best Chart Type`,
`Secondary Options`, `When to Use`, `When NOT to Use`, `Data Volume Threshold`,
`Accessibility Grade`, `A11y Fallback`. These answer *which form fits this data*, which
does not depend on the medium.

**Screen-only — drop (2/14):** `Library Recommendation` is 100% web libraries (17× D3.js,
9× Recharts, 9× Plotly, 6× Chart.js, 3× Deck.gl). `Interactive Level` is
hover/drilldown/pan/zoom — the file contains **23 mentions of hover**, none of which mean
anything on paper.

**Mixed — rework (3/14):** `Color Guidance` carries hex values and opacity percentages and
assumes RGB. `Accessibility Notes` mixes medium-neutral advice with "mobile context" and
keyboard navigation. `Data Volume Threshold` is neutral in kind but its values are tuned
to canvas/WebGL rendering limits (">500 nodes"), not to what a reader can resolve in print.

**Added columns (document questions upstream never asks):**

| Column | Type | Example | S/V/R |
|---|---|---|---|
| `Label Strategy` | enum `direct`\|`legend`\|`either` | `direct` | V |
| `Static Fallback` | text | direct-label each series at its line end | P |
| `Print Series Max` | int | `5` | V |
| `Greyscale Safe` | enum `yes`\|`needs-pattern`\|`no` | `needs-pattern` | V |
| `Print Palette Roles` | slug list | `primary;secondary;muted` | V |
| `Caption Required` | bool | `yes` | V |
| `Caption Must State` | text, nullable | `must state bin width for histograms specifically` | P |
| `Anti-Patterns` | text | `3D bars (Tufte: adds a perspective-distorted third dimension that misrepresents the actual 2D magnitude, pure chartjunk); rainbow/spectral palette across categories…` | P |

**Kept upstream columns, typed here at the Revision 4 erratum (§9).** They arrive from
`charts.csv` and this document had described them in prose without ever giving them a row in
a typed table — which is how an undeclared column becomes a list column by accident. Typed
now, so it cannot.

| Column | Type | Example | S/V/R |
|---|---|---|---|
| `Secondary Options` | text | `Pie chart, only if <=5 slices and a single snapshot (no cross-total comparison); treemap for hierarchical parts…` | P |
| `When NOT to Use` | text | `Not for parts of one whole (use part-to-whole); not once category count exceeds ~7-8 (use comparison-many)` | P |
| `Data Volume Threshold` | text | `Comfortably readable up to ~7-8 categories in a print-width figure; beyond that, category-label collision…` | P |

**Four more kept upstream columns, typed at the load-pass-3 erratum follow-on (§9).** The
erratum above stated its own ambit — the nine "keep" columns plus the one reworked-and-kept
`Accessibility Notes` — and typed three of the ten. These four close the load-bearing
remainder.

| Column | Type | Example | S/V/R |
|---|---|---|---|
| `Data Type` | text | `magnitudes of a value across a small set of named categories` | S |
| `Keywords` | text | `bar chart, comparison, categories, magnitude, ranking few` | S |
| `Best Chart Type` | text | `Horizontal bar chart` | S |
| `Accessibility Grade` | enum `high`\|`medium`\|`low-medium` | `high` | V |

The first three are **not a widening of anything**: the manifest has listed them as
`figures.searchable_columns` since it was written, and `resolve.py` builds the retrieval
document for every figure lookup from exactly that list. They were `S` in running code and
absent from this document — the machine-readable layer and this one disagreed about whether
they existed. `Keywords` is comma-separated, and that is prose punctuation, not a delimiter:
the same column is typed `text`/`S` on `doctypes`, `doc-styles`, `palettes`, `typefaces` and
`page-formats`, all with comma-separated examples.

`Accessibility Grade` is the only one of the four that adds a check. See §9 for the
`tabular-lookup` ruling it required first.

`Label Strategy` matters more than it looks: a legend is a lookup the reader performs
with their eyes, and on screen a hover tooltip covers for a bad legend. On paper there is
no hover, so `direct` should be the default and `legend` should require a reason.
`Print Series Max` is report 03 §B's 5–7 spaghetti threshold as an enforceable number.

**Changes at Revision 2, from `22-t11-figures-draft.csv` (11 authored rows).**

- **`Min Physical Size mm` is cut.** It survived three revisions as this document's
  longest-standing invented threshold, and the author showed why it could never be a
  constant: a legible minimum depends on how many labels the figure carries, so it is
  *computed*, not stored — the same class as CPL, and cut for the same reason
  (`Greyscale Distinct`, `Min L* Delta`). Good riddance; it was §8's bottom entry every time.
- **`Caption Required` and `Anti-Patterns` are added**, both beyond what this document
  specified, both kept.
- **T11's `Anti-Patterns` is not a duplicate of T2's `Anti-Pattern Tokens`.** *Rewritten at
  the Revision 4 erratum (§9), which falsified the previous argument.* Revision 2 said the
  two were "two text lists feeding one validator" bound at different `Element Scope`s — T2
  at document scope, T11 at figure scope — and offered that as Rule 4's first case of two
  *payload* tables carrying the scoping. **That reading is now wrong on its facts.** T11's
  column was authored as prose and is typed `text`/`P` at the erratum; nothing tokenises it,
  so `validate-anti-patterns` cannot read it and never did. The claim was already
  contradicted inside this section — T11's own "Validators enabled" line, three paragraphs
  below, has never listed `validate-anti-patterns` — and the erratum resolves the
  contradiction in favour of the line that matched the code.

  What survives is the generalisation, which was the valuable half: a table may carry the
  data a check reads while T9 binds when and how strictly it runs, and one validator may be
  bound at several scopes. T11 is simply **not an instance of it**. The two columns are
  distinguished by kind, not by scope: T2's is an enforceable token list, T11's is cited
  rationale for a human. If a figure-scoped anti-pattern check is ever wanted, it needs a
  *new* tokenised column beside the prose one — reusing this column would mean re-authoring
  eleven rows and discarding their citations, which §9 explicitly declined to do.
- **The key column is `chart_key`, not `figure_key`.** The authored file names it and the
  CSV wins. `Colour Guidance` — listed here as "mixed, rework" — was dropped by the author
  and stays dropped: its hexes and opacity percentages are the palette's job (T4), which is
  where `Print Palette Roles` already points.

**Change at Revision 3: `Caption Must State` is added, and the load pass is why.**
`22-t11-figures-draft.csv` authored prose in `Caption Required` — a `yes`/`no` enum column —
and the loader had to normalise it to `yes`, parking three real per-row facts in
`26-t11-caption-qualifications.md` rather than losing them
(`25-reheader-map.md` §9, "Information dropped, recorded rather than lost"):

| `chart_key` | `Caption Must State` (as loaded, the author's own words) |
|---|---|
| `distribution` | must state bin width for histograms specifically |
| `correlation` | should state sample size (n) and, where relevant, the correlation coefficient |
| `tabular-lookup` | and captioned ABOVE the table, not below, per report 03 Section D and T10's Caption Position convention |

The loader splits the authored cell at the first `--` and drops anything after a second
one (the author's file-level aside), so the column carries the authored words rather than a
paraphrase, and the split is idempotent from the untouched draft.

Three observations, because the shape matters more than the three cells:

- **This is not the enum being wrong; it is a second fact wearing the enum's clothes.**
  *Whether* a caption is required and *what it must contain* are different questions, and
  the draft answered the second one in the column that asks the first. Splitting them is the
  same move `validate-cpl-and-leading` needed (§4, "on the two splits") — one column, two
  scopes, no way to check either.
- **It is free text, deliberately, and that is not a Rule 1 violation.** Rule 1 forbids
  untyped *logic* in a cell. This carries no logic and drives no branch: it is caption
  copy the generator must emit and a human reads. The closest analogue is T11's own
  `Static Fallback`, which is prose for the same reason.
- **`tabular-lookup` is the row that does not fit, and it is left not fitting.** "Captioned
  ABOVE the table" is a *position*, not a *statement*, and it belongs to T10's
  `Caption Position` convention (report 03 §D), which already has the column and the
  validator. It is recorded here as `position: above the table` so the fact stays findable
  from the row that has it, but **T10 remains authoritative and
  `validate-caption-position` reads T10, not this cell** — if the two ever disagree, T10
  wins and that is a data bug, not a precedence question. Written down because a text
  column with one row's worth of position advice in it is exactly how a second source of
  truth starts.

*Naming:* `25-reheader-map.md` §9 and `26-t11-caption-qualifications.md` both call for
`Caption Must State`; the task brief called it `Caption Note`. The provenance files' name
wins so the trail stays followable — noted here because the brief's name will appear in
the task board and should not read as a different column.

**Validators enabled:** `validate-chart-series`, `validate-figure-size`,
`validate-greyscale` (figures share the palette check), `validate-label-strategy`,
`validate-caption-position` (via T10).

---

## T12. `cv-regions.csv` — no upstream analog

**Purpose.** CV norms that vary by region and seniority, stored once instead of restated in
every doctype row. Not searched — resolved by `Region Key` from T1, plus a seniority band
computed at validation time. *Added at Revision 2 from `18-cv-region-rules.csv`.*

| Column | Type | Example | S/V/R |
|---|---|---|---|
| `region_key` | slug | `uk` | R |
| `Seniority Band` | enum `early`\|`experienced` | `early` | R |
| `Max Pages` | int | `2` | V |
| `Photo` / `Date of Birth` / `Nationality` / `Marital Status` / `Visa Status` | enum `expected`\|`customary`\|`neutral`\|`negative-signal`\|`contested` | `negative-signal` | V |
| `Section Order` | slug list, FK → T13 `canonical_section` | `contact;summary;experience;education;skills` | V |
| `Education Before Experience` | bool | `true` | V |
| `Format` | enum `reverse-chronological`\|`functional`\|`hybrid` | `reverse-chronological` | V |
| `Language Expectation` | text | `English standard for multinational/private-sector roles; Arabic for government/local-market roles` | P |
| `Evidence Class` | enum `FACT`\|`CONVENTION`\|`CONTESTED` | `CONVENTION` | V |

**Design notes.**

- **Seven regions × two bands = 14 rows.** The source CSV has 7 × 4 = 28, and the collapse
  is the researcher's own finding: mid, senior and executive rows are **identical to each
  other within every region**, and there is no sourced basis for a further split. Inventing
  one would be the unsourced threshold this project keeps refusing (T11's
  `Min Physical Size mm`, T6's print floors, the L\* delta). Only early-vs-experienced has a
  source — report 03's Education-above-Experience swap for ≤2 years / new graduates.
  **Adopted as recommended.** If a mid/senior distinction is ever sourced, the enum grows;
  it does not need re-shaping.
- **T12's `Section Order` outranks T10's when `Region Key` is set, and this needs saying
  out loud.** A CV doctype resolves both — `Structure Key` → T10 and `Region Key` → T12 —
  and both carry a `Section Order`. Region genuinely determines CV section order (that is
  why the source CSV holds it per region), so **T12 wins for any doctype with a non-null
  `Region Key`; T10's column is authoritative only when `Region Key` is null.** Without this
  sentence the resolver author picks arbitrarily, and the ambiguity would be the
  `Section Order Early Career` duplication this revision deleted, reintroduced one table
  over. T10's `Section Order` remains the FK list that `validate-keys` checks in both cases.
- **`Seniority Band` is a lookup axis, not a routing key on T1.** It is computed from the
  document's own parsed Experience-section date ranges — the mechanism the CSV's
  `us-cv-length-*` rows already used — so it belongs to the artifact being validated, not to
  the doctype being requested. T1 carries `Region Key` only.
- **The field columns are five-valued, not boolean, and that is load-bearing.**
  `negative-signal` (US/UK: a photo actively hurts) and `expected` (its absence is the
  anomaly) are opposite violations, and `validate-text-safe-fields` needs to know which
  direction to check — the CSV flagged this inverted polarity explicitly. `contested` is the
  honest state for Europass's current personal-data fields, which `18-notes.md` could not
  verify against current documentation and therefore refused to pick; a `contested` cell
  produces no check at all rather than a guessed one.

- **`customary` is a fifth value, added at Revision 3 because the authored data used it and
  this document's four-value enum could not hold it** (`25-reheader-map.md` §9 correction
  5). It is not a synonym for anything already here. The ladder, stated as what each value
  makes the machine do:

  | Value | Validator verdict on **presence** | on **absence** | Generator default |
  |---|---|---|---|
  | `expected` | pass | **fail** | include |
  | `customary` | pass | pass | include |
  | `neutral` | pass | pass | no default |
  | `negative-signal` | **fail** | pass | omit |
  | `contested` | no check | no check | no default |

  **`customary` is the only value that separates the generator's default from the
  validator's verdict**, and that separation is the whole reason it exists: a DACH CV
  normally carries a photo, so we should emit one, but a DACH CV without a photo is not
  defective and failing it would be inventing a rule. `neutral` says the library has no
  opinion; `customary` says it has one and declines to enforce it.

- **The `expected` example in the line above is now this document's, not the data's — and
  that is a correction, not a hedge.** Revision 2 cited Gulf-GCC as the `expected` case.
  The authored `cv-regions.csv` gives Gulf `customary` for all five fields, and across
  fourteen rows and seventy cells **`expected` is used zero times**: `customary` 32,
  `contested` 18, `negative-signal` 16, `neutral` 4. The researcher looked at the strongest
  candidate for "absence is an anomaly" and declined to make it one. `expected` therefore
  stays in the enum as the pole that gives `negative-signal` its meaning and as the value a
  future sourced row would take — but **no row currently claims it, and this document should
  stop implying one does.** An enum value with no rows is a shape the schema is entitled to
  keep; an example that contradicts the data is not.
- **`Evidence Class` exists here and nowhere else, and that is not a contradiction.** T9
  cuts it because `Severity` already encodes the policy call and the two would disagree. T12
  has no severity — it holds facts, not bindings — and its rows are visibly mixed in
  provenance: US/UK are report-03-sourced, DACH and EU-generic are general HR convention the
  researcher supplied and tagged as weaker. A reader choosing between them needs to see
  which is which, and no other column carries it.

**Validators enabled:** `validate-page-count` (via `Threshold: cv-regions:Max Pages`),
`validate-text-safe-fields`, `validate-section-order`, `validate-keys`.

---

## T13. `headings.csv` — long format, no upstream analog

**Purpose.** The ATS heading dictionary: which literal heading strings map to which
canonical section, per language. Not searched — resolved by join.
*Added at Revision 2 from `18-ats-headings.csv` (80 rows).*

| Column | Type | Example | S/V/R |
|---|---|---|---|
| `canonical_section` | slug | `experience` | R |
| `Heading Text` | text | `Employment History` | V |
| `Language` | enum `en`\|`fr`\|`de` | `en` | R |
| `Is Primary` | bool | `no` | V |

**Design notes.**

- **Long format for the same reason as T6.** 11 sections × 3 languages × 2–5 variants is a
  three-axis fact. Any cell-based encoding is a map, and Rule 1 forbids maps without a
  closed vocabulary — which a synonym list, by nature, does not have.
- **`Is Primary` is the emit/accept distinction.** The generator emits the primary heading
  for a section; the validator accepts any variant. One column serves both directions, and
  without it the dictionary could only be read, not written from.
- **Exact match only — no fuzzy matching, deliberately.** `18-notes.md` specifies lookup on
  `(NFC-normalised, casefolded heading text, language)`. A heading dictionary that "sort of
  matches" reproduces the ambiguity ATS vendors themselves fail to resolve (report 03 §5). A
  miss is a miss. That is also why `18-ats-headings-rejected.csv` exists: 15 negative
  controls, so `validate-canonical-headings`'s false-negative rate on genuinely
  non-canonical headings is **measured rather than assumed**. Those 15 rows are test
  fixtures, not library content — they live with the validator tests and are not a table.
- **One deliberate omission, flagged rather than guessed.** "Qualifications" (English) is
  excluded from the dictionary and parked in the rejected file, because real parser
  behaviour treats it inconsistently — education, certifications, or a scoring section
  depending on vendor. A wrong synonym silently misfiles a section, which is worse than a
  miss the validator reports.

**Validators enabled:** `validate-canonical-headings`, `validate-section-order`,
`validate-keys`.

---

## T14. `font-substitutes.csv` — no upstream analog

**Purpose.** Metric-compatible fallbacks per family. Not searched — resolved by lookup on a
family name. *Added at Revision 2 from `19-notes.md`.*

| Column | Type | Example | S/V/R |
|---|---|---|---|
| `proprietary_family` | text | `Calibri` | R |
| `Substitute Family` | text, nullable | `Carlito` | V |
| `Lineage` | enum `liberation`\|`croscore`\|`crosextra`\|`independent`\|`none` | `crosextra` | V |
| `Licence` | enum `OFL-1.1`\|`Apache-2.0`\|`none` | `OFL-1.1` | V |
| `Metric Identical` | enum `yes`\|`no`; empty = not applicable | `yes` | V |
| `Weights Covered` | text list | `Regular;Bold;Italic;Bold Italic` | V |

**Example rows**

```
proprietary      | substitute       | lineage    | licence   | metric | Weights Covered
Arial            | Liberation Sans  | liberation | OFL-1.1   | yes    | Regular;Bold;Italic;Bold Italic
Arial            | Arimo            | croscore   | Apache-2.0| yes    | Regular;Bold;Italic;Bold Italic
Times New Roman  | Liberation Serif | liberation | OFL-1.1   | yes    | Regular;Bold;Italic;Bold Italic
Times New Roman  | Tinos            | croscore   | Apache-2.0| yes    | Regular;Bold;Italic;Bold Italic
Courier New      | Cousine          | croscore   | Apache-2.0| yes    | Regular;Bold;Italic;Bold Italic
Calibri          | Carlito          | crosextra  | OFL-1.1   | yes    | Regular;Bold;Italic;Bold Italic
Cambria          | Caladea          | crosextra  | OFL-1.1   | yes    | Regular;Bold;Italic;Bold Italic
Georgia          | Gelasio          | independent| OFL-1.1   | yes    | Regular;Bold;Italic;Bold Italic
Candara          | —                | none       | none      |        |
Consolas         | —                | none       | none      |        |
Aptos            | —                | none       | none      |        |
```

`Metric Identical` and `Weights Covered` are both **empty** on the no-substitute rows, not
`no` and not a weight list: there is no substitute for either to describe. Revision 2's
example block showed `no` in that position and was wrong on its own stated rule.

**Design notes.**

- **A separate table, not a column on T5, and the test is the one this schema keeps
  applying.** The substitution is a fact about a *family*, not about a pairing: Calibri's
  substitute is Carlito regardless of which T5 row uses Calibri as a heading or body face.
  A column on T5 restates it on every referencing row — the T6-out-of-T5 argument at the
  family level.
- **Three lineages, and they do not share a licence.** Liberation (Red Hat) is OFL and is
  LibreOffice's default; Croscore (Google, from Ascender) is **Apache 2.0** and covers the
  same three substitutions; Crosextra (Google, later) is **OFL 1.1** and covers Calibri and
  Cambria. `19-notes.md` verified each against current sources rather than memory, and
  corrected two of its own assumptions doing so — Crosextra is not Apache like Croscore, and
  JetBrains Mono is OFL not Apache. `Lineage` and `Licence` are separate columns because the
  same substitution is available under two different licences, and a project with a licence
  constraint needs to choose.
- **`none` is a real and useful row.** Candara, Corbel, Constantia and Consolas have no
  established metric-compatible substitute, and neither does Aptos — too new for a
  substitute ecosystem to exist. A doctype resolving to one of these has no safe fallback
  identity and must embed or avoid it. `validate-substitute-available` fails a `safe-stack`
  target whose family has `Substitute Family: —` and is not `os-bundled`, which is the
  precise combination that produces a silently reflowed document on the recipient's machine.
- **Three rulings applied at Revision 2, from `27-t14-font-substitutes-draft.csv`
  (15 authored rows).**
  - **`Lineage` gains `independent`.** Gelasio — Georgia's metric-compatible substitute,
    OFL, SorkinType — belongs to none of the three Google/Red Hat lineages and is not
    `none` either, because a substitute genuinely exists. The draft shipped it as `other`;
    `independent` says the same thing without becoming the bucket everything unclassified
    falls into.
  - **`Metric Identical` may be empty, and empty means *not applicable*.** The six rows with
    no substitute (Candara, Corbel, Constantia, Consolas, Verdana, Trebuchet MS) leave it
    blank rather than `no`. This is the `Element Scope` principle again: empty is a real
    state, not a missing value. **`no` is reserved for "a substitute exists but its metrics
    differ"** — currently an empty set, and worth keeping empty, because a
    non-metric-identical substitute reflows the document and is a different product from
    what this table promises.
  - **`Weights Covered` is added, because a substitution can fail on weight alone.** Carlito
    ships Regular, Bold, Italic and Bold Italic only; Gelasio's newer Medium and SemiBold
    weights have no Georgia counterpart. A T5 row calling for Calibri Light resolves to
    Carlito and then silently falls back to a weight that was never designed to match.
    `validate-substitute-available` reads this column and fails when the requested weight is
    absent — which turns a silent reflow into a refusal.
- **The natural key is (`proprietary_family`, `Lineage`), not family alone.** Arial, Times
  New Roman and Courier New each have two rows — a Liberation one under OFL and a Croscore
  one under Apache 2.0 — so the family is not unique and the choice between rows is a
  licence decision. The surrogate `substitute_key` (§0.1.1) carries the composite.
- **This is the lookup T5's design notes asked for.** T5 records that upstream's 1,923-row
  `google-fonts.csv` "cannot back T5's columns" and is worth keeping only as optional
  metadata. T14 is the purpose-built five-column version of the one fact that was actually
  needed.

**Validators enabled:** `validate-substitute-available`, `validate-font-resolution`,
`validate-keys`.

---

## 2. What we drop from upstream, entirely

| Upstream asset | Rows | Verdict | Reason |
|---|---|---|---|
| `stacks/` (16 files) | — | **drop** | react-native, swiftui, flutter, threejs, laravel… zero document relevance |
| `landing.csv` | 34 | **drop** | landing-page section orders and CTA placement |
| `react-performance.csv` | — | **drop** | same 10-col shape as ux-guidelines, web-only content |
| `app-interface.csv` | — | **drop** | same |
| `ux-guidelines.csv` | 98 | **drop table, keep shape** | `Code Example Good`/`Bad` are React/CSS; content is touch targets and hover states. Its `Category/Issue/Do/Don't/Severity` shape is good and is already absorbed into T9 |
| `icons.csv` | 104 | **drop** | `Library` + `Import Code` are Lucide-React imports |
| `design.csv` / `draft.csv` | — | **drop** | `01-mechanism.md` §1.8: orphaned. Not in `CSV_CONFIG`, zero repo references, freeform Chinese prose — not a schema at all |
| `products.csv` | 161 | **replace** | shape → T1. 76/161 rows are landing/dashboard/SaaS/app (`05-SYNTHESIS.md:249`) |
| `ui-reasoning.csv` | 161 | **replace** | shape → T2, minus the inert `Decision_Rules` |
| `styles.csv` | 84 | **replace** | shape → T3, 11 of 22 columns dropped |
| `colors.csv` | 160 | **replace** | shape → T4; the luminance-derivation *code* is kept and reused |
| `typography.csv` | 73 | **replace** | shape → T5+T6, 3 of 11 columns dropped |
| `charts.csv` | 25 | **adapt** | → T11, 9 columns kept, 2 dropped, 3 reworked, 6 added |
| `google-fonts.csv` | 1,923 | **keep as optional lookup** | useful catalogue; answers no document question. No embedding/licence column; repo-wide `fsType` grep = 0 |

**Kept unchanged: no table.** The honest answer to "what do we keep unchanged" is *the
engine, not the data*. `core.py`'s BM25 + `CSV_CONFIG` pattern, `_select_best_match`'s
closed-form rerank, `_sync_all.py`'s WCAG luminance derivation, and
`html-token-validator.py`'s hard/soft-fail split are all directly reusable. Every row of
content is web vocabulary and none of it transfers — which `01-mechanism.md` §3 already
concluded, and this schema exercise confirms column by column.

**Licence posture unchanged:** schemas and mechanisms are ideas and ours to re-implement;
no row content is copied. The named temptation stays the `slide-*.csv` decision tables.

---

## 3. Worked example — how one request resolves

Request: *« fais-moi une note interne sur les congés »*, ENS brand active. No mention of
ENS, brand, or plugin — the activation case `ENS-plugin-rebuild-v2.md:108` specifies.

*Updated at Revision 2 to route through the three new tables.*

```
exact doc_key / Display Name hit?  ─→ miss
BM25 over T1, Brand Scope=ens      ─→ doctypes: ens-note-interne     [the only fuzzy step]
  ├ Artifact Class      flow                    → pagination validators ON
  ├ Region Key          — (not a CV)            → T12 not consulted
  ├ Reasoning Key       ens-office-document     → T2
  │   ├ Style Key       ens-document-grid       → T3  rules, no fills, emphasis=weight
  │   ├ Palette Key     ens-core                → T4  text-safe={primary,secondary,fg}
  │   ├ Typeface Key    ens-manrope-inter       → T5  scale=ens-print
  │   ├ Doc Conditions  if_photocopied [intent] → constraint:photocopy-safe-color
  │   └ Anti-Pattern Tokens  gradient;emoji;navy;lime-text   → T2, not T11
  ├ Page Format Key     a4-ens-note             → T7  210×297, measure 130mm, 25/55 margins
  ├ Structure Key       ens-note                → T10 header;title;body;table?;signoff;footer
  │   └ Heading Language  fr                    → T13 (section, fr) → emitted heading text
  ├ Constraint Sets     ens-house;photocopy-safe→ T9  bound checks, scoped and severitied
  │   └ report-measure-cpl  Element Scope=body-paragraph  → the table is exempt
  └ Render Targets      docx-office;pdf-chromium→ T8
        docx-office  Font Rule=safe-stack → Arial          (T5.Safe Stack Fallback)
                                          → os-bundled     (T5.Safe Stack Availability)
                                          → T14: Liberation Sans / Arimo if absent
        pdf-chromium Font Rule=embed      → Manrope + Inter (T5.Heading/Body Family)
                                          → fsType checked  (validate-embedding-licence)
```

Five things to notice. **One fuzzy step, then pure key resolution** — the same request
resolves identically every time, and at Revision 2 even that step is a fallback: an exact
`doc_key` hit short-circuits it. **The Arial-in-Word rule is derived, not stored** — it
falls out of the `Font Rule` × `Safe Stack Fallback` join, and Revision 2 adds the fact that
makes it *safe*: Arial is `os-bundled`, so the unembedded `.docx` renders correctly even if
the recipient never opens Office. Had the fallback been Calibri, the same join would have
resolved and `validate-substitute-available` would have flagged it.
**`validate-brand-resolution` fires if step 1 returns no ENS row**, which is the case the
field instance actually failed (`05-SYNTHESIS.md:186-189`). **The French headings are a
join, not a cell** — T10 names the sections, `Heading Language: fr` picks the language, T13
supplies the text. **And the measure constraint exempts the table**, which is the one rule
the ENS acceptance test proved wrong before `Element Scope` existed.

---

## 4. Validator manifest

*Restructured again at Revision 2.* Fourteen entries added, five renamed or split to match
the names `16-t9-constraints-draft.csv` actually uses. **Where the authored CSV and this
manifest disagreed on a name, the CSV won** — editing 38 sourced, provenance-tagged rows to
match a document is backwards, and the two splits it forced are independently right (see
below). Full mapping in §9. Upstream precedent marked **[P]**; everything unmarked is
net-new build work, not adaptation.

Per Rule 4, this section is the **only** place a check is defined. Tables index; T9 binds.

Build-time (hard fail, run in CI on the library itself):

1. `validate-keys` — every FK resolves byte-identically to an existing slug **[P]**. Scope
   widened at Revision 2: T10 `Section Order` and T12 `Section Order` are now FK lists into
   T13 `canonical_section`. **Fully mechanised at Revision 3** — the manifest gained the
   `"group": true` FK form, so the five FKs that target a grouping column rather than a key
   column are declared and checked (§0.1.1). 13 of 13, up from 8 of 13.
2. `validate-checks-implemented` — every T9 `Check` names a real function; every `Parameter`
   key is one that function declares; **and every `<table>:<Column Name>` reference in
   `Threshold` resolves to a real table and a real column of it**, matching the re-headered
   column name the library actually loads (`cv-regions:Max Pages`, not `T12:max_pages`).
   Both halves are settled at Revision 4: the column half is the re-headered name, the table
   half is the **manifest table name** (§0.1). `validate_data.py`'s `reference_columns` is
   declared on `constraints.Threshold` and resolves all five shipped references.
3. `validate-severity-map` — every `fail`-severity reasoning row reaches ≥1 hard constraint;
   every activatable `Doc Conditions` condition reaches a real constraint
4. `validate-artifact-class` — flow/canvas rows reference coherent formats and structures
5. `validate-doc-conditions` — closed-vocabulary parse plus the `intent` ⇒ `constraint:`-only
   rule **[P]** (`_check_reasoning_contract`). The Revision 3 **admission test** (T2 — a
   condition whose truth value the resolved T1 row determines is not a condition) is an
   authoring-time gate on the closed dict, not part of this check; mechanising it needs each
   signal to declare the resolved field it reads, which `doc_reasoning_contract.py` does not
   yet do. Stated so nobody assumes the validator is enforcing it.
6. `validate-contrast-print` — WCAG relative-luminance ratio on T4 hexes **[P]**
   (`_check_color_contract`). The one build-time entry that is not a hard fail: T9 sets it
   `warn`, because a real formula applied outside its domain is still convention.

Preflight (before generating):

7. `validate-brand-resolution` — brand active ⇒ a brand-scoped row was resolved
8. `validate-engine-available` — target present at ≥ `Engine Min Version`; walk the fallback
9. `validate-print-mode-coherence` — `Print Tier Max` ≥ the tier `Print Mode` requires
10. `validate-font-resolution` — `Font Rule` × typeface yields a concrete family; warns when
    a `safe-stack` target resolves to an `office-bundled` family **[P, partial]**
11. `validate-embedding-licence` — `fsType` permits embedding; fails on `restricted` only
12. `validate-substitute-available` — **written out precisely at Revision 3**, because
    `Weights Covered` gives it a second failure mode and a check with two failure modes
    needs both spelled out.

    *Input.* The resolved T5 row's `Safe Stack Fallback` family, its
    `Safe Stack Availability`, and the resolved T8 row's `Font Rule`. Runs only when
    `Font Rule` is `safe-stack`; `embed` and `inline-webfont` targets carry their own
    fonts and this check does not apply to them.

    *Lookup.* Family → T14 on `proprietary_family`. The family is not unique (Arial has a
    Liberation row and a Croscore row), so the lookup returns a **row set**, and the check
    passes if **any** row in it satisfies both conditions below. Choosing among satisfying
    rows is a licence decision and is not this check's business — that is the whole reason
    `substitute_key` is `(proprietary_family, Lineage)` (§0.1.1).

    *Failure mode 1 — no substitute at all.* `Safe Stack Availability` is not `os-bundled`
    **and** every matching T14 row has an empty `Substitute Family` (or there is no
    matching row) ⇒ **fail**. This is the Candara / Corbel / Constantia / Consolas /
    Verdana / Trebuchet MS / Aptos set: the document reflows silently on the recipient's
    machine and nothing in the artifact says so.

    *Failure mode 2 — the substitute exists but does not cover the weight* (new). A
    matching row's `Weights Covered` does not contain a requested weight ⇒ **fail**, naming
    the weight and the substitute. Carlito ships `Regular;Bold;Italic;Bold Italic` only, so
    a stack calling for Calibri Light resolves to Carlito and then falls back again, to a
    weight nobody designed to match — a silent reflow inside an apparently successful
    substitution, which is worse than the first mode because it looks like it worked.

    *Where the requested weight set comes from — and the gap, named rather than assumed.*
    **Baseline:** `Regular`, `Bold`, `Italic`, `Bold Italic`. Any document with body text
    and emphasis needs all four, and T3's `Emphasis Mechanism: weight` makes `Bold`
    non-optional; the baseline is therefore checkable today against the eight authored T5
    rows without any new column. **Beyond the baseline, the schema does not say.** No table
    declares that a stack wants Light, Medium or SemiBold: T5 holds family names with no
    weight axis, and T6 holds sizes and leading with no weight axis either. Until one of
    them does, the check enforces the baseline and cannot enforce more. This is filed as a
    real gap (§8), not papered over — the alternative, parsing weights out of family
    strings like `Calibri Light`, is exactly the untyped inference Rule 1 forbids.

    *Severity.* `fail`. Both modes end in a document that does not look like the one that
    was designed, on a machine nobody can inspect. *(entry added at R2, contract written
    at R3)*

Post-render (on the artifact):

13. `validate-content-preservation` — **on redesign jobs, the extracted text of the output
    must equal the extracted text of the input**, modulo whitespace normalisation only.
    **Zero text changes, full stop** — no allow-list argument, no exceptions parameter.
    DOCX `w:t`, PPTX `a:t`, PDF text-showing operators. Empty `Element Scope`: a changed
    word anywhere is a failure. *(new at R2 — see the note below; the most important entry
    added this revision)*
14. `validate-measure` — 45–75 characters per line, **scoped by `Element Scope`**
15. `validate-leading-ratio` — leading ∈ [1.20, 1.45] × body size
16. `validate-type-floor` — resolved sizes clear the floor T9 sets
17. `validate-contrast-screen` — WCAG 4.5:1 / 3:1 **[P]** (same function as 6)
18. `validate-text-safe-color` — absolute L\* ceiling on the smallest roles
19. `validate-greyscale` — palette roles stay distinct after greyscale conversion
20. `validate-text-safe-roles` — no text rendered in a fill-only role
21. `validate-palette-only` — no hex outside the resolved palette **[P]**
22. `validate-anti-patterns` — grep the token list **[P]**
23. `validate-font-embedded` — `zipfile` assertion on OOXML; `/FontFile*` scan on PDF
24. `validate-ats-structure` — columns, tables, text boxes, header/footer content, symbol fonts
25. `validate-text-safe-fields` — presence/absence of DOB, marital status, photo, visa, per
    T12's four-valued field columns, **in the direction that row specifies** *(new at R2)*
26. `validate-image-text-parity` — inline images with no adjacent text run; a proxy, and
    `warn` because it is one *(new at R2)*
27. `validate-text-layer` — body text is selectable (not a rasterised PDF)
28. `validate-page-count` — page count against a ceiling, literal or `cv-regions:Max Pages`
29. `validate-pagination` — forced breaks and page structure
30. `validate-running-heads` — verso/recto headers structurally present *(new at R2)*
31. `validate-pagination-format` — roman front matter, decimal body restart *(new at R2)*
32. `validate-bleed` — artboard = trim + 2×bleed; TrimBox/BleedBox where required
33. `validate-safe-margin` — no content within `Safe Margin mm` of the trim edge
34. `validate-fold-geometry` — panels sum to trim; tuck narrowest by ≥ the fold allowance
35. `validate-tabular-figures` — numeric columns use `tnum`; `unknown` ⇒ warn
36. `validate-density` — bullets per slide, words per bullet
37. `validate-text-density` — words per slide body *(new at R2)*
38. `validate-aspect-ratio` — deck aspect ratio *(new at R2)*
39. `validate-output-intent` — `/OutputIntents` with `/S /GTS_PDFX` present
40. `validate-color-space` — no RGB operators where CMYK is required
41. `validate-spot-color` — declared brand spot appears as a `/Separation`
42. `validate-section-order` / `validate-canonical-headings` (T10 × T13 join) /
    `validate-heading-depth` / `validate-caption-position` / `validate-cross-refs`
43. `validate-checklist-emitted` — T3 checklist present in output **[P, loose]**
44. `validate-figure-size` / `validate-chart-series` / `validate-label-strategy` **[P,
    partial]** (`_check_chart_contract` validates the catalogue, not rendered geometry)
45. `validate-table-rules` — vertical borders absent, horizontals on header/total only *(split)*
46. `validate-table-alignment` — numeric columns right-aligned, text columns left *(split)*
47. `validate-text-case` — sustained all-caps runs in `legal` role text *(new at R2)*
48. `validate-emphasis-mechanism` / `validate-family-count` / `validate-dpi`

**On entry 13, because it is the one the pilot argued for.** ENS's acceptance test passed on
all three deliverables, and in the middle of it the model *shortened three regulatory labels
to make them fit, caught itself against the verbatim rule, reverted, and re-fitted by
spacing* (`05-SYNTHESIS.md:569-572`). The outcome was correct. The mechanism was model
discipline, and this schema's entire premise is that **validators catch this, not
discipline** — the same premise §0.3 rests on, where a model that was told to use the ENS
brand invented a green instead. A redesign job has an unambiguous invariant: the words are
the user's and the design is ours. Entry 13 makes that a check. It binds in T9 for every
redesign doctype at `fail`, and it is the only validator here whose failure mode is losing
the user's content rather than mis-styling it.

**And it takes no allow-list — decided, not deferred.** The obvious design gives the
validator a list of sanctioned typo fixes. That requires a "corrections log" concept the
schema does not have and would have to invent: who writes it, when, and what stops it
becoming the hole every change escapes through. **The rule is zero text changes on a
redesign.** A typo fix is then a *separate, explicit user request* — which is what ENS's own
rule already says, correctly read: *only obvious typos may be fixed and must be listed to
the user* is a **reporting obligation on a requested change**, not a silent allowance during
a redesign. The simpler rule is also the enforceable one: a validator comparing two strings
needs no schema support, while an allow-list needs a table, a writer and a policy.

**On the two splits.** `validate-cpl-and-leading` becomes `validate-measure` +
`validate-leading-ratio`, and `validate-table-style` becomes `validate-table-rules` +
`validate-table-alignment`. Both match the CSV, and both are right independent of it:
measure now scopes by `Element Scope` (tables are exempt) while leading does not, and
border rules and numeric alignment fail for unrelated reasons and want separate severities.
A bundled validator cannot carry two scopes.

**The precedent split, with its counting basis stated.** Counting **numbered manifest
entries** (42, 44 and 48 bundle several functions, so a function-level count is larger):
**9 of 48 have upstream precedent, 39 are net-new.** The precedented set did not grow this
revision — every one of the fourteen additions is against a format upstream has no concept
of. Earlier bases for comparison: 9 of 36 at Revision 1, 7 of 28 at Revision 0.

For the **[P]** rows, port the upstream function shape — same constants, same hard/soft-fail
split — rather than re-deriving it. Everything unmarked is new because upstream has no flow,
print, OOXML or font-binary concept at all.

Forty-eight validators is the honest count of what "encode the thresholds as data" cashes
out to, and it grew by 33% the moment someone authored real rows. It is also the answer to
"does each column earn its place" — a column not reachable from this list is not in the
schema.

---

## 5. Helper requests — all returned, and then some

*Status added at Revision 1, reframed at Revision 2. Kept rather than deleted, because the
record of what was asked is part of the record of what changed.*

**Revision 2's inputs were not answers to anything on this list.** `16` (38 authored
constraints), `17` (live engine tests), `18` (CV regions and headings) and `19` (safe-stack
availability and substitutes) arrived as unsolicited deliverables from specialists who went
and authored rows. They changed the schema more than the four commissioned reviews did —
three tables added, three columns deleted, fourteen validators. Worth recording as a finding
about process: **the reviews found errors, the authoring found structure.** The next thing
this schema needs is more rows, not more review.

**One specialist: print production.** *Answered — `14-print-production-values.md`.* T7's
print columns and T9's `professional-print` set are populated from its §2 and §3. On the
question the request called a promise we should not overpromise on: the verdict is **three
tiers, not one** — print-shop-submittable RGB today on every target, PDF/X-4 with an sRGB
output intent on WeasyPrint ≥67, and full CMYK press-ready gated on a bundled ICC asset and
currently unreachable. See T8.

**Not requesting an ATS specialist.** Unchanged; report 03 §A already gives the column set
and thresholds, and the remaining uncertainty is validator implementation, not schema.

**Two sub-questions for the Document Design Researcher.** *Both answered —
`12-typescale-and-fstype.md`.* (1) `photocopy` needed neither a full scale nor a partial one
and is cut as a `Medium`; report 03 gives no absolute print size floor at all, so T6's print
rows are brand-authored constants validated by a formula. (2) `fsType` **is** readable
stdlib-only, verified on six fonts across TTF and OTF, so the `Embedding Licence` column is
restored as a preflight check.

**One question not asked but answered anyway.** `13-schema-mechanism-review.md` found §0.2's
description of upstream stale and one claim in T2 factually wrong. Both are corrected in
this revision; the review is the reason Rule 1 changed.

---

## 6. Authoring cost — the part nobody should skim

*Revised again at Revision 2, and this time against **authored rows** rather than
estimates. Three tables were added and the total still fell.*

| Table | Est. rows | Notes |
|---|---|---|
| T1 doctypes | 60–80 | 8 document classes × format variants; region no longer multiplies them |
| T2 doc-reasoning | 25–35 | one per doctype *category*, not per doctype |
| T3 doc-styles | 20–30 | |
| T4 palettes | 40–60 | `On X` values derived, not authored |
| T5 typefaces | 30–50 | 8 authored so far (`19-t5-typefaces-draft.csv`) |
| T6 type-scales | 50–80 | `photocopy` cut; print rows are per-brand authored constants |
| T7 page-formats | 25–40 | more columns, not more rows |
| T8 render-targets | 10–14 | grew by the PDF/X-4 row |
| T9 constraints | **45–70** | was 85–130 — see below |
| T10 structures | 15–25 | lost two columns to T12 and T13 |
| T11 figures | 25–30 | 25 adapted + document-specific additions |
| T12 cv-regions | **14** | 7 regions × 2 bands, authored |
| T13 headings | **80** | 11 sections × 3 languages, authored |
| T14 font-substitutes | **~10** | one row per proprietary family with a lineage |
| **Total** | **~450–620 rows** | was ~450–750 at R1, ~600–900 at R0 |

**T9's estimate fell from 85–130 to 45–70, and that is good news rather than a shortfall.**
The DDR authored 38 non-print rows against an 80–120 estimate and flagged the gap rather
than padding to meet it. Three reasons, all sound:

1. **Seven rules are owned by other tables' validators, not by T9** — canonical headings,
   heading depth, caption position, cross-reference style, tabular figures, family count,
   and the safe-stack/embed fork. Each already had a table and a validator; a T9 row would
   have been a second definition, which Rule 4 now forbids by name.
2. **Ten items are advisory-only and were correctly refused as rows** — serif-vs-sans in
   body text, "template-looking" visual signals, running-head *content* correctness,
   chart-vs-table editorial judgment, speaker-note conventions, typeface pairing *harmony*,
   and others. Each is real and none has a threshold. Forcing them into rows would have
   produced exactly the aspirational-rule list `validate-checks-implemented` exists to
   prevent.
3. **A further four rows collapsed into one this revision** when `Threshold` gained the
   `cv-regions:Max Pages` reference form.

The pattern generalises: **a well-designed schema makes its own constraint table smaller**,
because every fact that belongs to a specific table stops being restated as a rule.

**The validator cost is where the growth went, and it is now the dominant number.**
Forty-eight manifest entries, of which **39 have no upstream analog** (§4) — up from 26 at
Revision 1. Fourteen were added by one pass of real authoring. Nine can be ported from
upstream; three (`pro-bleed-geometry`, `pro-output-intent-present`, `pro-color-space-cmyk`)
cannot run at all on the preinstalled engine. Budget the rest as new code against paged PDF,
OOXML packages and font binaries.

Each row needs a sourced value, not a plausible one — that is the difference between this
and the "AI slop" the project exists to eliminate. **The schema is a week. The library is
months.** Revision 2 is the first evidence for that claim rather than an assertion of it:
132 rows exist, and authoring them changed the schema three times.

---

## 7. Open questions

**Closed at Revision 1:**

1. ~~**Is `fsType` readable stdlib-only?**~~ **CLOSED — yes**
   (`12-typescale-and-fstype.md` §Q2). Fixed-offset `uint16` in `OS/2`; `struct` + `open`
   suffices; verified on six fonts, TTF and OTF. `Embedding Licence` returns to T5 as a
   preflight check, complementary to the post-render `zipfile` assertion.
2. ~~**Does any available path produce CMYK with bleed?**~~ **CLOSED — three tiers, not a
   yes/no** (`14-print-production-values.md` §1). Bleed: yes, WeasyPrint ≥0.41. PDF/X-4 with
   an sRGB output intent: yes, WeasyPrint ≥67. Full CMYK press-ready: not until a
   redistributable CMYK ICC profile is bundled — an engine-capable, asset-blocked tier. The
   promise we make is "print-shop-submittable RGB" everywhere and "PDF/X-4 RGB" where
   WeasyPrint ≥67 is present. See T8.
4. ~~**How does a brand get installed into the library?**~~ **CLOSED — overlay plus
   scripted re-zip** (`15-distribution-model.md`, adopted). `data/brand/<slug>/` merged at
   load by `resolve.py`, `Brand Scope` set by directory, key collision a hard fail; the ZIP
   regenerated by a bundled script rather than by hand. See §0.3.

**Still open:**

3. **Half closed at Revision 2, and the surviving half is the one that matters.**
   *Closed:* Chromium **is** genuinely preinstalled — confirmed by live test on a fresh
   container (`17-print-live-tests.md`), not inferred from one session. T8's
   `Availability: preinstalled` on `pdf-chromium` is verified, and `pdf-weasyprint` is
   confirmed `pip`. *Still open:* that confirmation makes tier 1 safe and leaves **tiers 2
   and 3 network-dependent**, because they exist only on the `pip` engine. So the question
   narrows rather than disappears: **is `pip` reachable at generation time, and what should
   a tier-2 request do when it is not?** Silently emitting tier 1 is the wrong answer;
   `validate-print-mode-coherence` currently hard-fails, which is defensible but has never
   been tested against a user who actually wanted a brochure.
5. **Does the `Severity: warn` channel actually change behaviour?** A warning nobody surfaces
   is a comment. Where warnings go — refuse, annotate the artifact, print to stdout (the only
   channel that enters context per `05-SYNTHESIS.md:65`) — is a resolver decision this schema
   assumes rather than specifies. It got heavier this revision: `validate-tabular-figures` on
   `unknown`, `validate-measure` on an estimated character width, and five of the
   seven `professional-print` rows all resolve to `warn`.
6. **Does *fourteen* tables exceed what contributors will maintain?** The question got
   sharper, not softer: Revision 2 added three tables while upstream has eleven domains. Two
   things argue it is still fine. Each new table is **smaller than the duplication it
   removes** — T12's 14 rows replace region facts restated across 28 doctype rows, T13's 80
   rows replace a list cell that could not hold three languages at all. And the tables that
   grew are dictionaries, which contributors extend one row at a time rather than maintain.
   The merge candidates if authoring stalls are unchanged in order — T10→T2, T6→T5, T3→T2 —
   and **T10 is now the strongest candidate**, having lost two of its nine columns this
   revision to tables that hold those facts better. §8 says the same from the other end.

---

## 8. Columns I am least confident in

Ranked, most doubtful first. *Re-ranked at Revision 2. The top of this list changed
completely, because authoring real rows moves doubt from "is this column right" to "is this
column reachable."*

1. **T13's exact-match-only heading lookup.** The dictionary is 80 authored rows and the
   matching rule is deliberately strict — NFC-normalised, casefolded, exact, no edit
   distance. That is the right call against fuzzy-matching's failure mode, but it means the
   validator's usefulness is entirely a function of dictionary coverage in three languages,
   and coverage is unmeasurable except against the 15 negative controls. A heading the
   dictionary has never seen is indistinguishable from a heading that is genuinely wrong.
   The fixtures make the false-negative rate measurable; nothing makes the *coverage* rate
   measurable. This is the only validator in the set whose accuracy degrades silently as the
   world adds heading synonyms.
2. **`Element Scope` as a six-value enum.** It is one revision old and was derived from a
   single observed failure (ENS's table cramped by a page-wide measure). Six containers is a
   guess at the shape of a space I have one data point in. `header-footer` in particular is
   in the enum because ATS rules care about it, not because any constraint scopes to it yet
   — an unfired value is a value nobody has tested.
3. **T12 `Seniority Band` collapsed to two values.** Adopted as recommended and I believe
   it is right — mid/senior/executive were identical within every region, and inventing a
   distinction would be the unsourced threshold this project keeps refusing. But "identical
   in the sourced material" and "identical in reality" are different claims, and the
   collapse is harder to reverse than it looks: re-splitting means re-authoring every region
   row, not adding a column.
4. **T2 `Doc Conditions` and the `intent` signal source.** Unchanged from Revision 1 and
   still a real bet. The closed vocabulary and hard-fail parser I am confident in; the
   `intent` tag rests on `if_hand_filled` and `if_photocopied` genuinely not being derivable
   from any resolved row — true today, and a future T1 column would quietly change it. The
   `intent` ⇒ `constraint:`-only rule contains the damage either way.
5. **T8 `Print Tier Max` on `pdf-weasyprint-pdfx4`.** The tier is inferred, not tested.
   `14-print-production-values.md` §5 is explicit that nobody ran the output through a real
   prepress validator. Revision 2 confirmed the engine *availability* question by live test
   and left this one exactly where it was — which, now that the neighbouring uncertainty is
   resolved, makes it the least-verified claim in T8.
6. **T9 `Parameter` as a closed grammar.** `Threshold` leaves this list at Revision 4: its
   reference form is declared (`reference_columns` on `constraints.Threshold`) and the gate
   resolves all five shipped references, so it is typed by running code rather than by
   promise. `Parameter` is not. It is still licensed on condition of typing that does not
   exist: every validator must declare its parameter names and
   `validate-checks-implemented` must reject a key the named `Check` does not declare. Until
   that lands `Parameter` is exactly as untyped as before, and it is now the **only** place
   in the schema where a rule is satisfied by unwritten work.
7. **T14's `Licence` column as an enum of three values.** Liberation/Croscore/Crosextra are
   the three lineages that exist for the Microsoft set, and `19-notes.md` corrected two of
   its own assumptions verifying them. That is reassuring about the values and says nothing
   about the enum's shape when a fourth lineage appears.
8. **T7 `Print Mode` as three inline enums** rather than a normalised table. Fine at three;
   a fourth should trigger the refactor. Less doubtful than before — the tier moved to T8
   and `Colour Space` is gone.
9. **T4 `Category Marker Roles`.** Derived from exactly one data point — ENS's brown as a
   secondary category marker. One brand is not a pattern.
10. **The requested-weight set, new at Revision 3, and it goes straight in near the top.**
    §4 entry 12 can enforce a four-weight baseline and no more, because **no table declares
    which weights a stack wants**: T5 holds family names with no weight axis, T6 holds sizes
    and leading with no weight axis. Every weight beyond `Regular;Bold;Italic;Bold Italic`
    — Light, Medium, SemiBold, the ones `Weights Covered` was added to catch — is therefore
    unenforceable, which means the column half-does the job it was added for. The fix is a
    column (a `Weights Used` list on T5, most likely) and it should not be guessed here.
11. **The seven prose columns, and how far they now reach.** *Was `Caption Must State` alone;
    widened at the Revision 4 erratum, and it moves up this list rather than down.*
    `Caption Must State` is still licensed because it carries no logic, and the
    `tabular-lookup` row is still the awkward case: a *position* stored in a *statement*
    column, with T10 authoritative. What changed is the count. The erratum typed six more
    columns `P` — `figures.{Anti-Patterns, Secondary Options, When NOT to Use,
    Data Volume Threshold, Static Fallback}` and `cv-regions.Language Expectation` — and the
    follow-on erratum then typed `Caption Must State` itself, so **seven of T11/T12's columns
    are marked as knowledge the library can show and cannot check.** Counting the `P` markers
    in the column tables and reading the tables for prose now return the same answer. While
    those two numbers disagreed, this entry was describing a seam; now it describes a
    boundary, which is the thing it was written to watch.
    Each retype was individually right: the cells hold cited rationale, and tokenising them
    would delete the citation. The doubt is cumulative, not individual. Two facts keep it
    honest rather than alarming: six of the seven sit in `figures.csv`, which is an advisory
    table by design — it tells an author which chart form fits, a judgement no validator was
    ever going to make — and the `P` letter now makes the boundary countable, so this entry
    has a number that can be watched instead of a feeling. The failure mode to watch is a
    *validated* fact drifting into a `P` column because prose was easier to author than a
    token: `Anti-Patterns` is exactly that story, caught only because someone tried to
    declare it as a list. Nothing catches the next one automatically. An **eighth** `P`
    column should be treated as evidence the schema is losing enforcement, not as a routine
    addition — and read the follow-on erratum's distinction first: relabelling a column that
    was never checked is a correction, while giving up a check something used to do is the
    failure this entry is watching for. The seventh was the former.
12. **T11 `Min Physical Size mm`** — *cut at Revision 2.* Kept in this list as the entry
    that was bottom-ranked for three consecutive revisions before the authored data made
    the case to delete it. That is the pattern worth remembering: the columns at the bottom
    of §8 do not get fixed, they get removed once someone tries to fill them in.

**Resolved at Revision 3 and dropped from this list:** nothing — item 6 (`Parameter` and
`Threshold` as closed grammars) got *narrower* rather than resolved: the harness now has a
`reference_columns` spec, so the reference form is one naming decision away from being
checked, but that decision (§0.1, the `T12:` vs `cv-regions:` table token) is open and the
column is still undeclared. Item 4 shrank by one entry: `if_projected` was deleted, and its
deletion is evidence for the item rather than against it — the `context`/`intent` split held
up, and the entry that failed the admission test was one nobody had yet authored a row
against.

**Resolved since Revision 1 and dropped from this list:** T7 `Stock gsm` (the fold-allowance
thresholds it feeds are now sourced values in T7's reference table, and the column's job is
narrow and clear). T10 as a whole table has *moved off* this list, having been the top entry
for two revisions — not because editorial taste became mechanical, but because the two
columns carrying the most taste (`Canonical Headings`, `Section Order Early Career`) are
gone, replaced by dictionaries with stated provenance. What remains in T10 is genuinely
structural.

## 9. Changelog

**Revision 4** — a small revision that closes two of Revision 3's escalations by ruling on
them, and declares the two manifest keys that were written but unused. Net shape change:
**0 columns, +1 enum value, 0 tables, 0 validators added**; the manifest gains
`list_columns` (8 columns over 6 tables) and `reference_columns` (1 column).

- **The `Threshold` reference form is ruled, both halves.** Table half = **manifest table
  name**, not this document's `T#` label (§0.1). Revision 3 escalated it; the rejected
  alternative was a `"schema_label"` per table. `reference_columns` is now declared and the
  gate resolves the references instead of ignoring them. §8 item 6 shrinks to `Parameter`
  alone.
- **`T#:` references in shipped data were five rows, not one.** Revision 3, §8 item 6 and
  `handover-coverage.md` all said "the one row that uses it", having counted only
  `cv-page-count`. `constraints.csv` also ships `pro-bleed-geometry`, `pro-trim-safe-margin`,
  `pro-min-dpi-raster` and `pro-min-dpi-line-art`, all `T7:` → `page-formats:`. They arrive
  from `21-t9-print-constraints-draft.csv` rather than from a literal in the loader, which is
  why every count taken by reading `load-base.py` missed them. The loader now normalises the
  table half through one `T#` → manifest-name map rather than by editing literals, so drafts
  not yet loaded inherit the rule. *Found by grepping the loaded column, not by reading.*
- **`legal` added to T6 `Role`**, as the size-ordered floor below `label`. T9 already shipped
  `legal-text-min-size` with nothing in T6 to resolve against (T6 design note).
- **`list_columns` declared for eight columns** (§0.1), with `constraints.Parameter` and
  `figures.Anti-Patterns` deliberately excluded. `Parameter`'s exclusion is permanent (it is
  a map). `Anti-Patterns` was left as an *open gap* here and is **closed by the erratum
  below**, which retypes it rather than declaring it.
- **The loader now skips brand-scoped draft rows.** `data/base/` ships `Brand Scope ==
  generic` only; §0.3 always said `Brand Scope` is set by the directory, and the loader was
  contradicting it by re-creating `ens-manrope-inter` in `base/typefaces.csv` from
  `19-t5-typefaces-draft.csv`. Brand rows reach the library through
  `examples/ens-brand.md` → `make_brand_kit.py` → `data/brand/ens/` and by no other path.

*Erratum, 2026-09-08 — the six prose columns.* Ruled after Revision 4 shipped; recorded
here rather than as a Revision 5 because **no data, no code and no manifest byte changes**.
The regenerated `schema-manifest.json` is md5-identical across this erratum, which is the
evidence that the change was scoped correctly: the manifest carries no per-column type
field, so a retype is a fact about this document and nothing else. Deliberately *not*
"fixed" by adding one.

- **Six columns are retyped or newly typed `text`, and marked `P`.** They are
  `figures.{Anti-Patterns, Secondary Options, When NOT to Use, Data Volume Threshold,
  Static Fallback}` and `cv-regions.Language Expectation`. **The brief called this six
  retypes; on disk it was three different things**, and the difference is the finding. Only
  `Anti-Patterns` was actually typed `text list` (T11's added-columns table). `Static
  Fallback` and `Language Expectation` were already `text` and needed only the `P` marker
  and a truthful example. `Secondary Options`, `When NOT to Use` and `Data Volume Threshold`
  **had no type row anywhere in this document** — they were described in T11's prose survey
  of upstream `charts.csv` and never tabled. That is the more dangerous state of the three:
  a column nobody typed is a column the next contributor types by guessing, and all three
  guess as list columns because all three contain `; `. They now have a table of their own.
- **Why prose wins over tokens here.** Every one of the eleven authored `Anti-Patterns`
  cells carries its source (Tufte on chartjunk; Cleveland & McGill 1984 on angle judgement).
  Tokenising to `3d-perspective;rainbow-palette` would leave a validator able to fire and an
  author unable to learn why — and the citation is the reason a curated library beats the
  model's own priors. Rejected alternative: keep the token list and move the rationale to a
  parallel `*-notes` column. It doubles the column count on the table with the most prose,
  and no validator is waiting to consume the tokens, so it buys nothing today and costs an
  edit to eleven rows.
- **`P` is added to the S/V/R legend** (§ "Legend in every column table"). Without it these
  six had to claim `V` — that a named validator reads them — which is false, or `R`
  (routing key), which is worse. `P` states "feeds no check" as a property, so §8 item 11
  can count the boundary instead of describing it. **Applied to the six ruled columns only.**
  `T11.Caption Must State` met the definition and kept `V`, because it was not in the
  ruling; the seam was recorded in the legend and §8 rather than closed unilaterally, and is
  closed by the follow-on erratum below.
- **Correction: Revision 2's Rule 4 argument for T11 was wrong on its facts.** It called
  T11's `Anti-Patterns` and T2's `Anti-Pattern Tokens` "two text lists feeding one
  validator" at different `Element Scope`s, and offered T11 as Rule 4's first two-payload-
  table case. T11's column is prose; `validate-anti-patterns` cannot read it and never did.
  The document already contradicted itself — T11's "Validators enabled" line has never
  listed that check — and the erratum keeps the line that matched the code. The Rule 4
  *generalisation* stands; T11 is not an instance of it (T11 notes, rewritten).
- **`cv-regions.Language Expectation` was checked against its data, not assumed.** Eight of
  fourteen rows contain `;`, which is what a token list looks like from a distance. They are
  clauses (`English standard for multinational/private-sector roles; Arabic for
  government/local-market roles`), so the column belongs with the other five. The example in
  T12's table was `English` — true of six rows and misleading about eight — and is replaced.
- **Left alone on purpose:** the authored cell values (this is a typing change, not a
  re-authoring), `constraints.Parameter`, and the four list-FK columns the FK checker
  already splits.

*Erratum follow-on, 2026-09-08 — the seventh prose column.* Ruled at load pass 2. Same scope
as the erratum above, and the same evidence that the scope is right: **no data, no code, no
manifest byte** — the regenerated `schema-manifest.json` is md5-identical across it.

- **`T11.Caption Must State` is retyped `V` → `P`**, closing the seam the erratum above left
  open deliberately. The ruling that opened it also fixed the test: *the letter follows
  whether a script actually reads the column.* Checked rather than assumed — a recursive
  grep for the column name across `skill/` returns `data/base/figures.csv` (the header),
  `data/schema-manifest.json` (the column list) and `data/schema-manifest-NOTES.md` (the
  Revision 3 entry), and **nothing under `scripts/`**: not `preflight.py`, which the ruling
  named as the specific candidate, and not `resolve.py`, `validate_data.py` or `ddi.py`.
- **This is a correction of a mislabel, not a widening of `P`.** The distinction is load-
  bearing, because §8 item 11 asks that a new `P` column be read as evidence the schema is
  losing enforcement. Nothing was enforced here and then stopped: the column has been prose
  since Revision 3 created it, and its `V` claimed a validator that never existed. The count
  of `P` columns rose because the count of truthful labels rose. An eighth `P` column that
  gives up a check something actually did is still the alarm item 11 describes.
- **The `tabular-lookup` row is untouched and still awkward.** Its value is a *position*
  (`captioned ABOVE the table, not below`) held in a *statement* column, with T10's
  `Caption Position` authoritative. That is orthogonal to the letter: it was true while the
  column was `V` and is equally true now.

*Erratum follow-on, 2026-09-09 - the four load-bearing figures columns, and the list-FK
declaration.* Ruled at load pass 3. Unlike the two errata above, this one **does change the
manifest** - md5 `0b4a079fbbfd2678cc463a78648dbe86` -> `731d874ff6052d8c3809a3d44a9d4196`,
14 tables / 174 columns / 13 FKs unchanged, `8 list columns` -> `12`, and one new enum. That
is the honest signal: the two earlier errata were facts about this document alone and their
md5-identity was the proof; this one adds two checks, so it must not be md5-identical.

- **`figures.{Data Type, Keywords, Best Chart Type}` are typed `text` / `S`.** The erratum
  above named ten columns as its ambit and typed three. These are three of the seven it left,
  and they are the three that were never optional: `figures.searchable_columns` has listed
  all three since the manifest was written, and `resolve.py` builds the retrieval document
  for **every** figure lookup from exactly that list. A name `grep` of `scripts/` would have
  answered "nothing reads them" and been wrong, because the consumption is manifest-driven.
  They were `S` in fact and unwritten here; typing them documents behaviour and changes
  nothing at runtime.
- **`figures.Accessibility Grade` is typed `enum high|medium|low-medium` / `V`,** and the
  `tabular-lookup` row that blocked it is ruled. The column reads as a clean enum on ten of
  eleven rows; the eleventh holds a 96-character sentence (`high by construction -- a table
  is the ground-truth data, no perceptual-encoding step to fail at`). **Ruled: keep the enum
  and move the sentence**, by the `Caption Required` precedent recorded in
  `25-reheader-map.md` section 9 - the same author, the same table, the same move one column
  over. `research/load-base.py` splits the cell at the first `--`, writes `high` into the
  enum column and appends the sentence to the prose column beside it,
  `Accessibility Notes`, joined with `; `. The draft is not touched: drafts are provenance.
  The alternative - type the column `text` and keep the sentence - costs the enum check on
  all eleven rows to license one cell, which is the trade this document declines everywhere
  else.
- **The four list foreign keys are declared in `list_columns`** (section 0.1, corrected
  there). This is the one item here that fixes a hole rather than a label: the
  well-formedness check ran on eight columns and zero of the four FK ones, confirmed by
  probe. `research/build-manifest.py`'s guard is inverted rather than removed.
- **Three `figures` columns are still untyped, and are deliberately left so:** `When to Use`,
  `A11y Fallback` and `Accessibility Notes`. All three are `P` by elimination - they appear
  in no manifest facet, so nothing can read them - and typing them is a two-line table edit.
  What is *not* cheap is the count they move. The legend says `P` "applies to exactly seven
  columns"; section 8 item 11 builds an argument on that seven ("six of the seven sit in
  `figures.csv`", "an **eighth** `P` column should be treated as evidence the schema is
  losing enforcement"). Three at once turns that entry from an increment into a rewrite, and
  the rewrite is the substance, not the number. Recorded as open rather than done, with the
  argument already made: like `Caption Must State`, these three are corrections of an
  omission and not a widening, because nothing was ever enforced on them. **Note the
  arithmetic: after this follow-on the untyped `figures` columns number three, not the four
  the load-pass-3 brief predicted** - `Accessibility Grade` moved out of that set by being
  ruled rather than deferred.
- **One seam this follow-on opens, and closes in the same breath.** The loader now appends
  `; grade rationale: <sentence>` to `figures.Accessibility Notes` - a `; ` in a column this
  follow-on has just decided to leave untyped. That is verbatim the failure the first
  erratum's justification names: an undeclared column acquiring a shape by accident. The
  separator is a *sentence* separator, exactly as in `Anti-Patterns`, `Secondary Options`,
  `When NOT to Use`, `Data Volume Threshold` and `cv-regions.Language Expectation`, and
  `Accessibility Notes` is now named beside those five in `research/build-manifest.py`'s
  standing "DO NOT declare these as list columns" comment. Naming it there costs nothing and
  moves no count; a `list_columns` entry would pass on prose while meaning something else.
- **Left alone on purpose:** the authored cell values in every draft, `constraints.Parameter`
  (a `name=value` map, not a list), and `cv-regions.Language Expectation`.

**Revision 3** — a maintenance revision folding in what running the library taught:
`25-reheader-map.md` §9 (load pass 1 — 190 rows through the real gate),
`26-notes.md` (T1 authored), `26-t11-caption-qualifications.md`, and the granted
group-FK format request. Net shape change: **+2 columns, +1 enum value, −1 vocabulary
entry, 0 tables, 0 validators added** (one rewritten in full).

*Corrections to things that were wrong:*

- **The `Threshold` reference form named the wrong column.** This document wrote
  `T12:max_pages` through two revisions; the loaded column is `Max Pages`, so the reference
  resolved to nothing. Canonical form is now `<table>:<Column Name>` against the
  **re-headered** name. The shipped `constraints.csv` row was already right — the document
  was the thing that was wrong (§0.1, §4 entries 2 and 28, T9, §8 item 6). *Found by running
  the loader, not by reading.*
- **The dropped-FK count was wrong twice over.** §0.1.1 said "four foreign keys" and "4 of
  8". It is **five** dropped — T10 `Section Order` and T12 `Section Order` are two
  declarations, not one — out of **13** total. Revision 2 mechanised 8 of 13; Revision 3
  mechanises 13 of 13.
- **T12's `expected` example contradicted the data.** Revision 2 cited Gulf-GCC as the
  "absence is the anomaly" case; the authored rows give Gulf `customary` on all five fields,
  and `expected` appears in **zero of seventy cells**. The value stays in the enum as the
  pole that gives `negative-signal` meaning; the example claiming a row uses it is gone.
- **T14's example block showed `Metric Identical: no` on the no-substitute rows**, against
  its own stated rule that empty means *not applicable* and `no` is reserved for "a
  substitute exists but its metrics differ." Corrected, and `Weights Covered` added to the
  block.

*Decisions taken:*

- **CONDITION PLACEMENT — ruled, and the answer is neither branch.** The question was
  whether `context` conditions belong on T1 with only `intent` conditions on T2. **No new
  T1 column.** The rule instead: *a condition is admissible only if its truth value is not
  determined by the resolved T1 row* — because a row that determines it already states it in
  `Constraint Set Keys`, an FK list `validate-keys` checks. A `Context Conditions` column
  would be a second, grammar-bearing way to say the same thing, needing its own parser,
  validator entry and manifest declaration to add nothing.
  **`if_projected` is deleted from `DOC_CONDITION_SIGNALS`** — the three deck doctypes'
  T1 rows already carry `projection` / `screen` / `` — and the interim three-Reasoning-Key
  fix is **withdrawn**: `deck-generic` goes back to one key. `if_professional_print` is
  *kept* by the same test, because all six `print-marketing` rows list
  `pdf-weasyprint-pdfx4;pdf-chromium` and which is selected is a render-time choice the row
  does not fix. Vocabulary: four keys, one `context` and three `intent`. Full reasoning at
  T2; the T1 consequence at T1.
- **All five grouping FKs are declared** (§0.1.1). `lib/data.py:82` now accepts
  `{"table", "column", "group": true}`, composing with `"list": true`. `validate-keys` is
  fully mechanised.
- **`Caption Must State` added to T11** — free text, nullable — restoring the three per-row
  facts the `yes`/`no` `Caption Required` enum could not carry. Not a Rule 1 violation: it
  holds caption copy, not logic. `tabular-lookup`'s position advice is recorded but **T10
  stays authoritative** for caption position.
- **`customary` added to T12's field-direction enum**, a fifth value the authored data used
  and this document did not have. It is the only value that separates the *generator's
  default* from the *validator's verdict*: include it, but do not fail its absence. Full
  ladder at T12.
- **`validate-substitute-available` written out in full** (§4 entry 12): two failure modes —
  no substitute at all, and a substitute whose `Weights Covered` lacks a requested weight —
  with the row-set lookup on the non-unique `proprietary_family`, and the requested-weight
  gap named rather than assumed.

*Escalated, not decided here:*

- **The table token in a `Threshold` reference.** `validate_data.py:249` resolves the token
  against **manifest table names** (`cv-regions`), not this document's `T12` labels, so
  `T12:Max Pages` is unresolvable by the code that exists and `reference_columns` is
  deliberately **not** declared this revision. Recommendation: make it
  `cv-regions:Max Pages` and delete the second naming layer. This blocks closing
  `schema-manifest-NOTES.md` §1.2 and will silently break the gate for whoever declares
  `reference_columns` next.
- **`ens-slides` references render target `html-export`, which no `render-targets.csv` row
  defines** (`html-static` does). Not this document's data, but it is a `validate-keys`
  failure waiting for `doctypes.csv` to land, so it is recorded where the T1 author will
  see it.


**Revision 1** — one combined revision incorporating `12-typescale-and-fstype.md`,
`13-schema-mechanism-review.md`, `14-print-production-values.md` and
`15-distribution-model.md`. Net shape change: **+7 columns, −2 columns, +7 validators
(plus one previously omitted from the manifest), −1 table medium, −150 estimated rows.**

*Corrections to things that were wrong:*

- **Rule 1 rewritten** from "no cell may contain logic" to "no cell may contain *untyped*
  logic." The old rule rested on the claim that upstream's `Decision_Rules` is inert. It is
  not: `reasoning_contract.py` executes a closed 32-key vocabulary with a hard-fail parser.
  The old text was also self-contradictory — "a fixed set of keys can ever fire" describes a
  working evaluator. Corrected to distinguish "custom keys never fire" (true in every
  version) from "nothing fires" (true only of the v2.5.0 checkout `01-mechanism.md` read).
- **§0.2 rewritten.** Upstream now short-circuits to an exact-identity dict lookup before
  BM25, and its BM25 abstains on low confidence rather than returning a weak guess. Added
  why abstention composes with `validate-brand-resolution`.
- **The FK deviation is smaller than claimed.** `_resolve_style`/`_build_style_lookup` is
  already shipping upstream, so `Style Key` *mirrors* upstream; `Palette Key` and
  `Typeface Key` *extend* it to two stages upstream has not reached. Stated as such.
- **T8's `pdf-weasyprint` row was stale on both print axes.** Bleed since v0.41, CMYK plus
  PDF/X and ICC output intent since v67.0. Chromium's row is unchanged and correct.
- **T5's `Embedding Licence` cut was based on a false premise.** `fsType` is readable
  stdlib-only. Column restored.

*Decisions taken:*

- **Adopted the closed `DOC_CONDITION_SIGNALS` vocabulary** recommended by
  `13-schema-mechanism-review.md` §3, as T2's new `Doc Conditions` column — with one
  deviation from upstream's contract: signals are tagged `context` or `intent`, and
  `intent`-sourced conditions may emit only `constraint:` actions. A missed intent signal can
  change which checks run, never what gets emitted.
- **Brand distribution: overlay plus scripted re-zip** (§7 Q4 closed). §0.3 and T1's
  `Brand Scope` semantics rewritten against it; `Brand Scope` is set by directory, key
  collisions hard-fail at load, `resolve.py` prints only the resolved decision. One
  `description` field, in `SKILL.md`, full stop.
- **Print is three tiers, encoded on T8 as `Print Tier Max`** (§7 Q2 closed) — not on T7,
  because the tier is a property of the (engine, invocation) pair, not of page geometry. The
  `Print Mode` → minimum-tier mapping is a resolver constant, not a column.
- **`print-l-delta` dropped**, replaced by `print-contrast-ratio` — WCAG relative luminance
  on T4 hexes at build time. No print-contrast standard exists; this is confirmed absent, not
  unfound.

*Table-level changes:*

- **T2** +`Doc Conditions`; `Decision_Rules` note rewritten; +`validate-doc-conditions`.
- **T4** −`CMYK Overrides` (a tier-3 column, and tier 3 is unreachable until an ICC asset
  ships — it returns with the asset); `validate-contrast-print` re-based and moved to the
  build-time bucket; +`validate-text-safe-color`.
- **T5** +`Embedding Licence` (fails on `restricted` only — `editable` and `preview-print`
  pass, or every Microsoft core font would fail preflight); `Has Tabular Figures` enum
  narrowed to `yes`/`unknown`, `unknown` ⇒ warn.
- **T6** `photocopy` cut as a `Medium`; print rows are brand-authored constants validated by
  the CPL/leading formula, whose four inputs are now named explicitly; sourced floors live in
  T9 rather than in a new `Value Basis` column; ~200 rows → 50–80.
- **T7** +`Safe Margin mm`, +`Fold Type`, +`Stock gsm`, +`Min DPI Line Art` (`Min DPI` →
  `Min DPI Raster`); −`Colour Space` (a pipeline consequence, not a page-format property);
  §2's sourced values added as a tagged reference table in the design notes rather than as a
  provenance column.
- **T8** +`Engine Min Version`, +`Print Tier Max`; +`pdf-weasyprint-pdfx4` row;
  `validate-print-mode-coherence` rewritten as a tier comparison.
- **T9** +7 `professional-print` rows adopted wholesale; `print-l-delta` and
  `photocopy-body-min` dropped; `Parameter` reclassified from "accepted smell" to closed
  grammar conditional on per-function parameter declarations.

*Sections:* §4 restructured with upstream-precedent marks and a stated counting basis (9 of
36 precedented; the brief's "18 of 28" could not be reproduced from the source table, which
yields 7 of 28 on the same basis). The recount also surfaced `validate-page-count`, required
by Revision 0's own T9 rows but absent from its manifest. §5 marked answered. §6 recosted. §7 Q1/Q2/Q4 closed,
Q3/Q5/Q6 open. §8 re-ranked.

---

**Revision 2** — the first revision driven by **authored rows** rather than review.
Incorporates `16-t9-constraints-draft.csv` (38 constraints), `17-print-live-tests.md`,
`18-cv-region-rules.csv` / `18-ats-headings.csv` (108 rows), `19-notes.md`, and
`05-SYNTHESIS.md`'s ENS acceptance test. Net shape change: **+3 tables, +5 columns,
−3 columns, +14 validators, −130 estimated rows.**

*The finding behind the revision:* every one of the three new tables exists because someone
authoring real rows hit a fact being restated. Review could not have found these. The
schema's own test — *does this column get restated across rows?* — was applied by the
authors, not by me, and it caught two columns I had defended in writing.

*Rules:*

- **Rule 4 added — a check is defined once (§4), indexed everywhere (per-table "Validators
  enabled"), and bound only in T9.** T9 rows never define checks. This resolves the
  T9-vs-T5 font-embedding question and generalises to every future instance.
- **`Threshold` becomes polymorphic** — literal, or a typed `<table>:<Column Name>` reference
  validated by `validate-checks-implemented`. It collapsed five region page-count rows into
  one.

*Decisions taken:*

- **Adopted recommendations 1 and 3 from `18-notes.md` as stated** (region rules become
  their own FK'd table; seniority collapses to `early`/`experienced`).
- **Adopted recommendation 2's substance and refuted its shape.** Headings become their own
  FK'd table (T13) and T10's list cell dies — but there is no `Headings Key` column, because
  T13 is keyed `(canonical_section, language)` and T10 already names its sections in
  `Section Order`; only the language was missing, and that is one enum. A `Headings Key`
  would be a third key naming a set two existing columns already determine.
- **Adopted `19-notes.md`'s separate-table recommendation** for substitutes (T14) rather
  than a column on T5, for the reason it gives: the fact is per-family, not per-pairing.
- **Where this document and the authored CSV disagreed, the CSV won** — `proj-body-floor` is
  `warn` (report 03 tags 24 pt CONVENTION), deck bullet density is `6` (report 03's 6×6),
  and five validator names change. The CSV's rows carry stated provenance; these examples
  did not.
- **Constraint sets union rather than override**, forced by ENS's density preference of 5
  sitting alongside the generic 6. The brand row is keyed `ens-deck-density`, because §0.3
  makes a colliding brand slug a refuse-to-run.
- **`fail`-severity structural constraints outrank `warn`-severity regional conventions.**
  DACH's two-column *tabellarischer Lebenslauf* conflicts with `ats-no-multi-column`;
  resolver default is ATS-safe structure carrying DACH-appropriate content.

*Table-level changes:*

- **T1** +`Region Key` (FK → T12). Region stops being a doctype variant.
- **T5** +`Safe Stack Availability` (`os-bundled`/`office-bundled`/`none`) — the column that
  makes `Safe Stack Fallback` mean something on macOS and LibreOffice.
- **T9** +`Element Scope`; `Threshold` grammar extended; examples realigned to the CSV;
  the two L\* rows collapse into one `print-legibility` WCAG row with an empty `Parameter`.
- **T10** −`Canonical Headings` (→ T13), −`Section Order Early Career` (→ T12),
  +`Heading Language`; `Section Order` becomes an FK list.
- **T12 / T13 / T14 added.**
- **Surrogate keys added (§0.1.1)** on T6, T11, T12, T13 and T14 when the schema was
  transcribed into `data/schema-manifest.json` — the manifest allows one key column per
  table and five tables had composite or unnamed keys.

*Rename mapping — for re-heading `16-t9-constraints-draft.csv` in one pass:*

| Kind | From | To |
|---|---|---|
| column | *(new)* | `Element Scope` — insert between `Check` and `Parameter`; empty = whole document, there is no `all` value |
| column value | `scope=body-paragraph;exempt=…` inside `Parameter` | move to `Element Scope`; leave only `cpl_min`/`cpl_max` in `Parameter` |
| column value | container `caption` | `caption-block` (T6 already uses `caption` as a `Role`) |
| rows | `us-cv-length-under10y`, `us-cv-length-10y-plus`, `uk-cv-length`, `eu-cv-length`, `gulf-cv-length` | one row `cv-page-count`, `Threshold: cv-regions:Max Pages` |
| row | `print-legibility-l-delta` | `print-contrast-ratio` (WCAG ratio, `Threshold: 4.5`, empty `Parameter`) |
| row | ENS density at 5 | key it `ens-deck-density`, not `deck-density` |
| row | `us-cv-no-photo`, `us-cv-no-dob`, `us-cv-no-marital-status`, `gulf-cv-photo-expected` | one row `cv-field-norms`, empty `Threshold`, direction read from T12 |
| validator | `validate-cpl-and-leading` | `validate-measure` + `validate-leading-ratio` |
| validator | `validate-table-style` | `validate-table-rules` + `validate-table-alignment` |
| validator | `validate-series-count` | `validate-chart-series` |

All other validator names in the CSV are adopted into §4 unchanged, including the twelve it
introduced that had no manifest entry — that gap would have hard-failed
`validate-checks-implemented` on first run and is closed.

*Sections:* §4 rebuilt (48 entries, 9 precedented, 39 net-new; bases at R1 and R0 given for
comparison). §6 recosted against authored rows — T9 falls to 45–70 and the reason is good
news. §7 Q3 half-closed: Chromium confirmed preinstalled by live test, the `pip`
availability of tiers 2–3 kept open as the surviving half. Q6 re-asked at fourteen tables.
§8 re-ranked; T10 leaves the top of the list for the first time.

*Still not done, and named so it is not mistaken for finished:* the typing that licenses
`Parameter` and `Threshold` (§8 item 6) is unwritten, and `data/schema-manifest.json` waits
on the validator harness defining its format.
