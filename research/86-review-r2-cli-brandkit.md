# research/86 — R2 review: `ddi.py designs` / `library` / `resolve --design` + brand-kit P5.1/P5.2

Reviewer: Opus (adversarial, read-only). Date: 2026-09-23.
Commits: 11e8dca (designs, library, --design, handoff design line, SKILL.md step), 2ffac1d (P5.1
generic base doctypes), 7577168 (P5.2 `## Designs`). Checked against research/80 §2D/§4 and RESUME
standing rules. Every finding below was run, not just read.

Test bed: the skill dir copied to `%TEMP%/r2rev/skill`. A real kit `acme` was built with doctypes
`cv-uk, cv-us, invoice-tabular, note-interne` and `## Designs: cv: cv-editorial / invoice:
invoice-tabular`, then merged with `merge_brand_kit.py -b` into a temp copy (`r2rev/m/skill`). The
ENS kit was then dropped in too. All commands below run from `r2rev/m/skill/scripts` unless stated.

**Verdict: 0 blockers, 4 should-fix, 9 advisory.** The main problem: `--design` and brand kits
don't work together (F1, F2). Everything is fine on unbranded data.

## Confirmed OK
- `pytest scripts/tests`: 227 passed, 1 xfailed (HEAD).
- Gate after merge: `make_brand_kit.py` self-check OK. `merge_brand_kit.py` OK (brand=acme
  files=5). `ddi.py check` on the merged tree: `OK: validated 16 table(s), 820 row(s)`. It still
  passes with the ENS kit added (832).
- The brand doc-reasoning row keeps all 10 manifest columns (it's a full copy plus 3 overrides).
- ENS legacy kit is byte-stable. `2ffac1d~1:make_brand_kit.py` and HEAD produce identical
  `brand.md`, `palettes/typefaces/doctypes/type-scales.csv`. Dry-run stdout differs only in the
  temp path.
- The handoff `design:` line appears on docx, pptx, pdf and png, both with `--design` (`rank 6 of 6,
  authority`) and without it (the doctype's default, `rank 1 of 6`).
- `--design` with a wrong family, or with an unknown key, prints a one-line refusal and exits 4.
- Reasoning Key `print-marketing` is shared by 3 families (brochure/flyer/poster). Both default
  lookups filter by Family first, so this is handled correctly.
- `designs --query` tie-break: `(-score, Rank)` is correct. `library` ties keep the authored order
  (stable sort).
- JSON: `--design` adds `resolved.designs[]` in the same `{key, ...columns}` shape as every other
  table. The doctype row shows the overridden Reasoning Key, which is honest.

## Findings

### F1 — SHOULD — `--brand` + `--design` silently drops the brand's palette and typeface (exit 0)
`scripts/resolve.py:719-746` (`_apply_design_override` at :449)

`--design` replaces the doctype's Reasoning Key with the generic design's. The FK walk then pulls
in the generic design's palette and typeface. `_has_brand_row` (:753) still passes, because the
doctype row itself is brand-scoped. The result is a "branded" resolution with no brand colours or
fonts, and no warning.
```
ddi.py resolve --brand acme --doctype acme-cv-uk --json          # rc=0
  doc-reasoning=[acme-cv] palettes=[acme-core] typefaces=[acme-sourceserif4-sourcesans3]
ddi.py resolve --brand acme --doctype acme-cv-uk --design cv-editorial --json   # rc=0
  doc-reasoning=[cv-editorial] palettes=[cv-editorial] typefaces=[fraunces-work-sans]
ddi.py resolve --brand acme --query "write my cv uk" --design cv-ats-strict --json  # rc=0
  doctypes=[acme-cv-uk] palettes=[mono-ink] typefaces=[safe-sans-arial]
```
The SKILL.md step 3 re-run line (`resolve --doctype <key> --design <design_key> --json`) also drops
`--brand` (and `--lang`), so an agent following it word for word loses the brand even before this
bug.

Fix, pick one:
- (a) When `entry_row["Brand Scope"] != "generic"`, build the override in memory. Copy the design's
  doc-reasoning row, keep the Palette Key and Typeface Key from the doctype's current (brand)
  reasoning row, and walk from that. This is the same rule `derive_reasoning_rows` applies at kit
  time.
- (b) Minimum: refuse with exit 4 `[DESIGN OVERRIDES BRAND]`.

Either way, change the SKILL.md line to "re-run step 2 with the same flags plus `--design`".

### F2 — SHOULD — brand doctypes built with `## Designs` have no design identity
`scripts/ddi.py:1331-1363` (`_design_handoff_line`), `scripts/ddi.py:1534/1572` (`designs`
is_default), `scripts/make_brand_kit.py:940`

The kit sets Reasoning Key `acme-cv`. No `designs` row has that Reasoning Key, so both default
lookups find nothing:
```
ddi.py handoff --json a.json --format docx     # a.json = resolve --brand acme --doctype acme-cv-uk
  HANDOFF (format=docx)
    page (docx-js DXA; ...                     <- no `design:` line
ddi.py designs --doctype acme-cv-uk | grep DEFAULT   # nothing marked
```
§2D says the handoff "gains `design:` on all 4 paths". Brand users are exactly the ones who picked
a design. The kit knows which design it picked (`cv-editorial`), but it throws that fact away.

Fix, pick one:
- (a) Add a nullable `Design Key` column to doc-reasoning, set on the `<slug>-<family>` rows. Both
  lookups then match on it. This needs a schema change plus a parity entry.
- (b) `ddi` reads `data/brand/<scope>/brand.md` `## Designs` for brand-scoped doctypes.

(a) is cleaner and FK-checkable.

### F3 — SHOULD — copied bias terms describe the design's generic palette, not the brand's
`scripts/make_brand_kit.py:759`

`derive_reasoning_rows` swaps Palette Key and Typeface Key but copies Palette/Typeface Bias Terms
unchanged. `resolve` shows them:
```
ddi.py resolve --brand acme --doctype acme-cv-uk | grep Bias
  Palette Bias Terms: near-black text, one Carbon Blue 60 accent restricted to headline/rule size only, ...
  Typeface Bias Terms: high-contrast editorial display serif heading + neutral grotesque body, ...
```
Acme's accent is #C8102E red, and its typefaces are Source Serif 4 + Source Sans 3. The agent reads
"Carbon Blue 60" next to a red brand palette.

Fix: blank `Palette Bias Terms` and `Typeface Bias Terms` in the kit row, or rewrite them from the
brand spec (e.g. "brand palette acme-core; accent #C8102E"). Keep Style Bias Terms, since the style
is inherited.

### F4 — SHOULD — `designs --query` reorders a family by document-length noise
`scripts/ddi.py:1556`

If a query term appears in every design (e.g. "cv", which is in every CV design's Keywords), its
IDF is about 0.07. The scores then differ only through BM25's length normalisation, so the order
becomes random-looking:
```
ddi.py designs --doctype cv-uk --query "cv" --json
  [cv-academic 0.1151, cv-editorial 0.1094, cv-dach-tabular 0.1067, cv-ats-strict 0.1054,
   cv-eu-europass 0.1018, cv-us-uk-designed 0.0984]      <- rank-1 default is now LAST
```
SKILL.md says to pass "their wording", and user wording nearly always contains the family noun.

Fix: drop query tokens whose document frequency equals N (present in every design) before scoring.
If no token is left, or every score is 0, fall back to `method=rank`. Or round scores to 2 d.p.
before the Rank tie-break. `library` has the same weakness (`ddi.py:1643`) but is less exposed.

### F5 — ADVISORY — a `## Designs` line for a family with no brand doctype emits an orphan row silently
`make_brand_kit.py:751`
```
acme2.md = acme.md with "deck: deck-generic" instead of the invoice line (no deck doctype)
make_brand_kit.py acme2.md -o acme2.zip   -> OK (palettes=1 typefaces=1 doctypes=4 type-scales=0)
  doc-reasoning.csv contains acme-deck,deck-bold-minimal,acme-core,...   (nothing references it)
```
The OK summary line (`:1007`, `:1023`) also never counts doc-reasoning rows.

Fix: print a NOTE (or fail) for a Designs family with no doctype, and add `doc-reasoning=N` to the
summary.

### F6 — ADVISORY — library `--brand` edge cases
`ddi.py:1754-1760`, docstring `:1720`
- `type-scales` ignores `--brand` and lists brand-kit scales in the generic browse: `ddi.py library
  type-scales` shows `ens-print [ens-print]` after the ENS kit is merged. Filter on
  `__file__`/brand origin.
- `ddi.py library palettes --brand nosuch` prints an empty list with rc=0. It should refuse (e.g.
  exit 1 `[NO SUCH BRAND]`).
- The docstring says "--brand is a no-op until a brand overlay authors one". That's stale now that
  P5 kits exist. `--brand acme` shows only acme rows (not brand + generic); document that
  explicitly.

### F7 — ADVISORY — `--query` with no match still reports `method=bm25` and lists everything
`ddi.py library palettes --query zzzqqq --limit 2` → `mono-ink score 0.0`,
`brand-accent-print score 0.0`. There's no "no match" signal, so an agent may treat these as hits.
Fix: when max score is 0, print `(no match — authored order)` or set `method=authored-order`.
Applies to `designs` too.

### F8 — ADVISORY — convention provenance renders as "(unnamed source)"
`ddi.py:1474`. For example, `mono-ink` has a convention provenance row with a blank Source Name:
`Evidence: (unnamed source)`. Use the Evidence Class: `convention (no cited source)`.

### F9 — ADVISORY — exit codes undocumented or wrong
- Exit 4 is missing from `resolve.py` module docstring (lines 65-74) and from `ddi.py:133`
  (`cmd_resolve`: "0/1/2/3").
- The `library` docstring (`ddi.py:1724`) says an unknown library name exits 1. It actually exits
  2 (argparse `invalid choice`, observed rc=2).

### F10 — ADVISORY — `--design` can contradict the doctype's constraint set without a word
`resolve --doctype cv-uk --design cv-editorial` exits 0. It keeps `ats-strict` constraints, but
cv-editorial's own Not For says "ATS-strict CVs". Consider a one-line NOTE when the design's Not For
names something the doctype's Constraint Set Keys contain. Or leave it to the agent. It's a policy
call, flagged only.

### F11 — ADVISORY — kit doc-reasoning rows break `test_provenance` in a dev tree
With `acme` merged: `pytest scripts/tests/test_provenance.py` →
`SUBFAILED doc-reasoning:acme-cv / acme-invoice has no provenance row`.

doc-reasoning has no Brand Scope column, so brand rows look generic. Tests aren't shipped
(`build_zip.py:73`), so this only affects anyone testing a merged tree. Fix: skip rows whose
`__file__` is under `data/brand/`. The same trap awaits P6.1 `build-portable.py` if it walks
doc-reasoning.

### F12 — ADVISORY (pre-existing, widened by P5.1) — brand doctypes with no `## Designs` line resolve to generic palette and typeface
```
ddi.py resolve --doctype acme-note-interne --json -> palettes=[mono-ink] typefaces=[safe-sans-arial]
ddi.py resolve --brand ens --doctype ens-note-interne   -> rc=0, generic palette/typeface
```
P5.1 now lets a kit list any of ~40 doctypes, and every family without a Designs line silently
ignores the brand's own palette and typeface. Suggestion: `make_brand_kit` either prints a NOTE per
such family, or auto-emits `<slug>-<family>` from the doctype's default design. Auto-emitting would
change the ENS bytes, so gate it on the kit having `## Designs` at all.

### F13 — ADVISORY — `## Designs` is case-sensitive; `## Doctypes` is not
`CV: cv-editorial` → `brand.md:15: unrecognised line in ## Designs`. `## Doctypes` lowercases its
input. Lowercase `stripped` before `DESIGN_LINE_RE` for consistency.
