# 34 — Seven untyped `figures` columns, and the blank-FK holes the gate cannot see

Coverage and Gap Analyst, 2026-09-09. **Report only. Nothing on disk was changed** —
manifest md5 `0b4a079fbbfd2678cc463a78648dbe86` unchanged, gate still **82**, `data/base/`
mtimes untouched (Sep 8 14:09). Two findings promoted out of `33-nonnull-sweep.md`
(Class 3, and the "why the gate cannot see any of this" section) into a form an author can
act on. Everything here is measured or cited; two claims are confirmed by running the gate
against a throwaway copy, since deleted.

---

## 0. Correction to `33-nonnull-sweep.md`, first, because it blocks

**`33`'s ranked-disposition item 2 — "Author `doctypes.Structure Key` for `infographic`" —
is withdrawn. Both of `infographic`'s blanks are deliberate and were documented at
authoring time.** `research/26-notes.md:222-225`, the T1 author's own words:

> **Infographic** stays close to what `02-coverage-gaps.md` calls it: an *unbuilt scaffold*.
> I gave it a row so it's reachable and doesn't silently 404, but its `Constraint Set Keys`
> and `Structure Key` are blank on purpose — there is no design payload authored anywhere
> for this class yet […] so filling those cells would be inventing content the rest of the
> library doesn't back.

`33` inferred a defect from the shape of the data — all four other non-`flow` doctypes carry
a `Structure Key` — without reading the authoring note that explains the fifth. The T2 author
independently reached the same position for the same row: `29-t2-doc-reasoning-draft.csv:15`
leaves `infographic-scaffold`'s Style/Palette/Typeface Keys blank at confidence **0.3**,
citing "the T1 author's own stated discipline on this doctype". Two authors, two tables, one
consistent abstention. An author working to `33` item 2 as written would have overwritten it.

**Consequence for the counts.** The blank-FK surface is **two columns, six blanks, of which
two are documented-deliberate and four are genuinely open** — not the flat "5 + 1" of `33`'s
Class 1 table. The task title's "2 gaps" counts *columns*, not rows.

**Row-numbering convention.** `33` listed the blank `Constraint Set Keys` rows as 10, 12, 13,
28, 30. Those are **CSV line numbers** (header = line 1). The data rows are `cv-academic`,
`letter-formal`, `memo-internal`, `slide-deck-handout`, `infographic` — the file has not
changed. This note uses keys throughout.

---

## 1. Finding A — seven `figures` columns have no type row anywhere in the schema

`figures.csv` is the only table in the library with undeclared **non-key** columns. (`33`'s
taxonomy counts twelve columns with no type row: these seven, plus five surrogate keys that
are non-null by construction and sit in several tables.) Seven of its
nineteen:

`Data Type`, `Keywords`, `Best Chart Type`, `When to Use`, `Accessibility Grade`,
`A11y Fallback`, `Accessibility Notes`.

**Disambiguation, because two different sevens collide here.** The schema legend at
`09:455` says the `P` letter "applies to exactly seven columns". That is a *different* set —
the prose-payload columns named by the Revision 4 erratum. These seven are the *untyped*
ones. No overlap; the coincidence is noise.

### 1.1 The erratum defined its own scope and then covered a third of it

`09:1495` classifies upstream `charts.csv` as **9 columns "genuinely medium-neutral — keep"**,
with 2 dropped at `09:1500` and 3 "mixed — rework" at `09:1505`. The erratum's typing table,
headed *"Kept upstream columns, typed here at the Revision 4 erratum"* at `09:1523`, types
**three** of that nine: `Secondary Options`, `When NOT to Use`, `Data Volume Threshold`.

The other six of the nine are `Data Type`, `Keywords`, `Best Chart Type`, `When to Use`,
`Accessibility Grade`, `A11y Fallback`. The seventh untyped column, `Accessibility Notes`,
comes from the "mixed — rework" bucket, whose other two members were resolved:
`Data Volume Threshold` typed, `Colour Guidance` dropped. `Accessibility Notes` was reworked
and never typed.

Counted the way the Orchestrator's brief counts it: **the erratum's ambit was ten columns —
the nine kept plus the one reworked-and-kept — and it typed three.** Seven remain.

So the erratum is **incomplete against a scope it stated itself**, not wrong. Its own
justification, the sentence beginning at `09:1523`, is the reason this matters
(`33` cites the same sentence as `09:1525`; `09:1523` is correct):

> They arrive from `charts.csv` and this document had described them in prose without ever
> giving them a row in a typed table — which is how an undeclared column becomes a list
> column by accident. Typed now, so it cannot.

That sentence is true of three columns and false of seven.

### 1.2 Three of the seven are load-bearing in running code

This is the part `33` understated when it said "nothing is broken today". The manifest
already assigns three of the seven a role:

```
figures.searchable_columns = ["Data Type", "Keywords", "Best Chart Type"]
```

and `scripts/resolve.py:240` builds the retrieval document from exactly that list:

```python
documents = [" ".join(str(r.get(c, "")) for c in searchable_columns) for r in rows]
```

**Every figure lookup in the skill is scored against three columns the schema does not
declare.** The machine-readable layer and the human-readable layer disagree about whether
these columns exist. They are `S` in fact and absent in the document.

### 1.3 The other four are `P` by elimination

`When to Use`, `Accessibility Grade`, `A11y Fallback` and `Accessibility Notes` appear in
**none** of `figures`' manifest facets — not `enums`, `foreign_keys`, `list_columns`,
`searchable_columns`, `typed_json_columns` or `derived`. Nothing can read them, which is the
schema's own definition of `P` (`09:452-458`): cited rationale handed to the author or
emitted to the reader, where "feeds no validator" is a stated property rather than an
unexamined `V`.

I am not offering a `grep` of `scripts/` as evidence either way. A name grep cannot see
manifest-driven consumption — which is precisely how `Data Type` and `Best Chart Type` are
read — so it would have produced the wrong answer for two of these seven.

### 1.4 `Keywords` has a five-row precedent and no list ambiguity

The obvious risk in typing `Keywords` is that its values are **comma**-separated
(`bar chart, comparison, categories, magnitude, ranking few`) while `figures`' one declared
list column, `Print Palette Roles`, uses `;`. That risk does not materialise. Five other
tables carry a searchable `Keywords`, and **all five are typed `text` / `S`** with
comma-separated examples:

| schema line | table |
|---|---|
| `09:480` | `doctypes` |
| `09:691` | `doc-styles` |
| `09:739` | `palettes` |
| `09:825` | `typefaces` |
| `09:1054` | `page-formats` |

`figures.Keywords` should be `text` / `S`, identically. The comma is prose punctuation inside
a text field, not a delimiter, on all six.

### 1.5 Typing is not mechanical — one row breaks two of the seven

`Accessibility Grade` reads as a clean enum on ten of eleven rows: `high` ×5, `medium` ×4,
`low-medium` ×1. On the eleventh, `tabular-lookup`, it holds a 96-character sentence:

> `high by construction -- a table is the ground-truth data, no perceptual-encoding step to
> fail at`

`A11y Fallback` on the same row holds `n/a -- a table IS the fallback form for every other
row in this file`.

`tabular-lookup` is the deliberate "the right answer is no chart" row, and it is the row that
breaks `figures`' column shapes — **five cells in total**, counting the three placeholder
values `33` found in its Class 2 (`Print Series Max` = `n/a` on a column typed `int`,
plus `Secondary Options` and `Static Fallback` = `n/a`). All five are the same authorial
move: a row whose point is that the table's premise does not apply to it.

Whoever types `Accessibility Grade` must therefore **rule on `tabular-lookup` first**. Two
options, and the choice is a real one:

- **enum `high`|`medium`|`low-medium`** and move the sentence to `Accessibility Notes`,
  setting the cell to `high`. Buys a gate-enforced enum check on the other ten rows.
- **`text`** and keep the sentence. Costs the enum check on all eleven.

I recommend the enum, on the same reasoning the loader already applied to `Caption Required`:
`25-reheader-map.md` §9 records that the T11 author wrote prose into that `yes`/`no` enum,
the loader normalised it, and the three displaced per-row facts were parked in
`26-t11-caption-qualifications.md` rather than lost. This is the identical situation one
column over, and the precedent for handling it is already set and already documented.

### 1.6 Recommended types

Offered as a starting point for the erratum author, not as a ruling. All seven are populated
on all eleven rows — checked directly, not inferred from `33`'s sweep, which skips undeclared
columns before it counts blanks.

| Column | Type | S/V/R | Basis |
|---|---|---|---|
| `Data Type` | text | **S** | manifest `searchable_columns`; read at `resolve.py:240` |
| `Keywords` | text | **S** | same, plus the five-table precedent in §1.4 |
| `Best Chart Type` | text | **S** | same |
| `When to Use` | text | **P** | in no manifest facet |
| `Accessibility Grade` | enum `high`\|`medium`\|`low-medium` | **V** | 10/11 conform; needs the `tabular-lookup` ruling in §1.5 first |
| `A11y Fallback` | text | **P** | in no manifest facet |
| `Accessibility Notes` | text | **P** | in no manifest facet; "mixed — rework" bucket |

Typing the three `S` columns is documentation of existing behaviour and changes nothing at
runtime. `Accessibility Grade` as an enum is the only entry that would add a manifest change
and a gate line.

---

## 2. Finding B — required FKs can be blank, and the gate is structurally blind to it

### 2.1 The mechanism, and the asymmetry inside it

`scripts/validate_data.py:214`:

```python
value = record.get(column, "")
if not value:
    continue  # nullable FK, no reference to check
```

Documented at lines 114-115 as matching "this schema's own nullable Style/Palette/Typeface
Key design". That rationale is sound for the **five** genuinely-nullable FKs and is applied
to **all thirteen**. (`33` and the docstring both undercount them: the schema marks
`doctypes.Region Key`, `doc-reasoning`'s Style/Palette/Typeface Keys **and**
`render-targets.Fallback Render Key` nullable — five, not the three the comment names.)

The asymmetry is the finding. Twelve lines earlier, the same file's docstring says of enums:

> empty string is only valid if explicitly listed in `enums[column]` — no implicit "blank is
> fine" exception

**The gate is strict about blank for enums and implicitly permissive about blank for foreign
keys.** One column class must earn the right to be empty; the other gets it for free. Nothing
in the schema says FKs should be the lenient class — it is an artefact of where the `continue`
sits.

### 2.1a What an empty FK means today, and whether `R` should ever permit it

**What it means today: unconstrained by silence.** A blank FK is not "no constraint applies".
It is *the check declining to run*. Nothing downstream distinguishes the three things a blank
can mean — deliberate abstention (`infographic`), an unfinished cell (`cv-academic`, on the
evidence), or a value that was typed and lost. The resolver reads the same empty string in
all three cases and simply attaches nothing.

**Should a blank ever be legal for an `R` column? Yes — but only when it is declared, and
that is precisely what is missing.** The flat answer "no, `R` means required, reject it" is
wrong on this data and I will not recommend it: `infographic`'s two blanks are correct,
deliberate and documented, and a hard rule would force an author to invent a `Structure Key`
for a class the library does not back, which is the exact failure `26-notes.md:222` refuses.

So the defect is not the blank. **The defect is that abstention and omission are the same
byte, and the schema has no way to tell them apart.** The schema already solved this problem
once, for enums: `constraints.Element Scope` licenses empty by listing `""` as a legal enum
member, which is a *declaration* the gate reads. Foreign keys have no equivalent — they get
the permission without ever asking for it.

**Recommendation: give FKs the same mechanism enums already have.** A per-column
`nullable: true` in the manifest FK spec, defaulting to **false**. Then `infographic`'s two
cells are legal because someone declared them legal, `cv-academic`'s is a gate line, and the
`R` letter regains its meaning. This is the enabling change for the non-null check in the
ordering below, and it is why "export `nullable` into the manifest" has to precede it — the
check cannot be written against a property the manifest does not carry.

**The schema has already made this exact call, five times, and nobody noticed.** All five
nullable FKs — `doctypes.Region Key`, `doc-reasoning`'s Style/Palette/Typeface Keys and
`render-targets.Fallback Render Key` — are marked **`R`**. So "`R` and nullable" is not a
contradiction I am proposing; it is an established, deliberate combination in this schema
that simply has no machine-readable form. Exporting it is transcription, not new design.

The cost is bounded: five columns already decided, plus whichever abstentions get ruled
legal, against 150 non-nullable columns that gain a check.

### 2.2 The contrast that shows the size of the hole

Both live in `doctypes.Constraint Set Keys`, the same column, in the same load:

| what a row does | gate lines |
|---|---|
| carries a **wrong** value — the 7 regional CV rows naming `us-cv-region` etc., which is finding B2 | **7** |
| carries **no** value — 5 rows | **0** |

A typo is caught seven times. An absence is caught never. B2 was found *because* the gate
shouted; these were found only because someone read the CSV.

### 2.3 The six blanks, scoped

`doctypes.Structure Key` (`R`, → `structures.structure_key`) — blank on **`infographic`**
only. **Deliberate.** See §0.

`doctypes.Constraint Set Keys` (`R`, list group-FK → `constraints.Set Key`) — blank on five:

| doc_key | Reasoning Key | assessment |
|---|---|---|
| `infographic` | `infographic-scaffold` | **deliberate** — §0 |
| `cv-academic` | `cv-academic` | **most likely a real gap** — see below |
| `letter-formal` | `letter-formal` | open — no authoring note either way |
| `memo-internal` | `memo-internal` | open — no authoring note either way |
| `slide-deck-handout` | `deck-generic` | open, and **coupled** — see §2.4 |

Both columns' blanks originate in `research/26-t1-doctypes-draft.csv`, not in the loader —
verified by reading the draft. So any fix is one edit to `research/26` plus a reload, which
is why `33` recommended pairing it with B2: same file, same author, one pass.

**`cv-academic` is the conspicuous one.** All eight other `cv-*` rows carry `ats-strict`
statically; it alone carries nothing. There is a partial defence — `26-notes.md:144` maps the
`cv-academic` *Reasoning Key* to `if_ats_target -> constraint:ats-strict`, so ATS constraints
can reach it conditionally. But that same conditional path also serves the `cv-ats-strict`
Reasoning Key shared by the other eight, **which carry the static key anyway**. The
conditional route is therefore not an alternative to the static one anywhere else in the
table, and `cv-academic` is the only row relying on it alone. I would not ship a CV doctype
whose ATS constraints depend on a condition firing. This needs a ruling, not a silent
backfill, because "no constraints apply" is a defensible authorial position — but on the
evidence it is not the position that was taken here.

`letter-formal` and `memo-internal` have no authoring note in either direction. They are the
only two rows in the table whose blank is neither explained nor obviously wrong.

### 2.4 `slide-deck-handout` is not a free backfill

The three deck rows share one `Reasoning Key`, `deck-generic`. `26-notes.md:148` flags the
consequence — `slide-deck-document` and `slide-deck-handout` would fire a projection
constraint they should not — and proposes an escape hatch:

> `if_projected`'s signal source needs to check something *outside* `doc_category` (e.g. the
> resolved `Render Target`/`Constraint Set Keys`, which do already differ per deck row)

**That escape hatch is weaker than it reads.** Measured on the loaded data:

| doc_key | Render Target Keys | Constraint Set Keys |
|---|---|---|
| `slide-deck-document` | `pptx-office;pdf-chromium` | `screen` |
| `slide-deck-handout` | `pptx-office;pdf-chromium` | *(blank)* |

The two rows are **byte-identical on `Render Target Keys`**. The only column that separates
them is `Constraint Set Keys`, and it separates them by a blank — the one value the gate
cannot see and which may equally mean "not authored yet". If handout's blank is backfilled
with `screen`, the obvious choice given its render targets, **the two rows become identical
on both columns the proposed fix names**, and the escape hatch closes.

So this blank cannot be ruled on in isolation. It is coupled to the still-open deck-condition
decision, and whoever takes that decision should take this one in the same pass.

### 2.5 A third hole in the same column, confirmed by running the gate

`doctypes` declares **no** `list_columns` in the manifest, yet `Constraint Set Keys` and
`Render Target Keys` are both `list: true` foreign keys. The well-formedness check at
`validate_data.py:228` iterates `list_columns` only, so it never runs on them; and the FK
loop skips empty tokens (`if token and token not in valid_values`). A malformed list passes
both.

This is not specific to `doctypes`. **Every list FK in the manifest is undeclared in
`list_columns`** — four columns across three tables:

| table | list FK | declared in `list_columns`? |
|---|---|---|
| `doctypes` | `Render Target Keys` | no |
| `doctypes` | `Constraint Set Keys` | no |
| `structures` | `Section Order` | no |
| `cv-regions` | `Section Order` | no |

The check covers the eight non-FK list columns and zero of the four FK ones. **The generator
is where this originates.** `research/build-manifest.py` writes `list_columns` as six
hand-authored literals — lines 58, 78, 94, 161, 254, 310 — covering those same eight non-FK
columns, and its only guard (line 336) asserts that a named column exists, never that a
`list: true` FK was declared. Nothing derives one facet from the other, so the four FK lists
were simply never added. The consumer's format comment agrees (`validate_data.py:47`,
`"list_columns": {"col6": ";"}  # optional -- non-FK ';'-list`), which is why the omission
reads as intended rather than as a slip.

**Empirical confirmation.** Same malformation, same delimiter, two columns, on a throwaway
copy of `data/`:

| mutation | gate |
|---|---|
| baseline | 82 |
| trailing `;` on `doctypes.Constraint Set Keys` (list FK) | **82** — silent |
| trailing `;` on `figures.Print Palette Roles` (declared non-FK list) | **83** — `malformed ';'-delimited list (empty item)` |

The copy has been deleted; `data/base/` was never touched and the gate still reports 82.
The probe exercised one of the four list FKs, and that one is a group FK. The empty-token
skip at `validate_data.py:214-221` is shared by every FK branch, so the result generalises to
all four; only the group lookup differs, and it runs after the skip.

---

## 3. Recommended disposition

1. **Retract `33`'s item 2 before anyone acts on it.** One line. `infographic`'s two blanks
   are correct as authored; the only edit needed is to the recommendation, not the data.
2. **Rule on the four open `Constraint Set Keys` blanks** as part of the B2 edit to
   `research/26` — same file, same author, one reload. `cv-academic` needs a decision on
   whether a conditional ATS path is acceptable where every peer row is static.
   `slide-deck-handout` must be decided **with** the deck-condition question, not before it.
   `letter-formal` and `memo-internal` need only a yes/no.
3. **Type the seven `figures` columns** as a Revision 4 erratum follow-on, ideally by whoever
   wrote the first one. Six are documentation of existing fact. The seventh,
   `Accessibility Grade`, needs the `tabular-lookup` ruling in §1.5 first.
4. **Record the FK/enum blank asymmetry** (§2.1) and the list-FK well-formedness gap (§2.5)
   against the post-step-6 gate work. `33` argued against teaching the gate a non-null check
   before buckets A and B clear, and that argument stands unchanged. These two are cheaper
   than the non-null check and land in the same pass: the list-FK gap in particular is a
   one-line generator change, since the FK spec already carries `list: true`.

## 4. Explicitly not claimed

- **Not claimed that anything is broken at runtime today.** All seven untyped columns are
  populated on all eleven rows; the three `S` ones work because the manifest declares them.
  The risk is exactly the one the erratum names — an undeclared column acquiring a shape by
  accident — and no more.
- **Not claimed that `letter-formal` or `memo-internal` should carry constraints.** Neither
  has an authoring note; both readings are open.
- **Not claimed that the gate should gain a non-null check now.** See `33`'s closing section;
  its false-positive arithmetic is unaffected by anything here.
