# cv — inter-coder agreement (research/82 §7, amended by research/82a-clarifications-1.md C10)

Computed by `research/designs-evidence/agreement.py` (generic, reusable — takes `--family`,
one or more `--first LABEL:path` first-coder evidence files, and `--second path`; see that
file's docstring). Exact invocation used for this file:

```
python research/designs-evidence/agreement.py --family cv \
  --first GH:research/designs-evidence/cv-corpus-github.md \
          NPM:research/designs-evidence/cv-corpus-npm-ms.md \
  --second research/designs-evidence/cv-second-coder.md \
  --exclude GH:003 GH:007 GH:008
```

## Inputs

- First coder [GH] `research/designs-evidence/cv-corpus-github.md`: 40 coded rows.
- First coder [NPM] `research/designs-evidence/cv-corpus-npm-ms.md`: 40 coded rows.
- Second coder `research/designs-evidence/cv-second-coder.md`: 20 coded rows (the sample).

## id-scheme check

Both first-coder files already key rows with an explicit `id` column of the form
`<corpus-id>:<position zero-padded to 3>` (`GH:001`… = GitHub native stars-desc rank;
`NPM:001`… — inferred from the NPM file's `Pos` column, since its coded table has no bare
`id` column — = npm native `downloads.monthly`-desc walk position). The second-coder file's
sample ids use the identical scheme (`GH:038`, `NPM:038`, …).

**The two schemes match — no reconciliation was needed.** All 20 sampled ids resolved to a
first-coder row by direct id lookup; the script's name-based fallback path (matching by
normalized repo/package name when an id lookup fails) was never triggered. As an extra check,
every one of the 20 sample rows' repo/package name in the second-coder file was manually
cross-read against the first-coder row of the same id and found identical (e.g. `GH:038` =
`zachscrivena/simple-resume-cv` in both files; `NPM:049` = `jsonresume-theme-caffeine` in
both). No id-to-id mapping table is required.

Per C10, the sample is the correct **family-wide** one (all 80 coded ids, GH 40 + NPM 40,
sorted lexicographically, `random.Random("82:cv").sample(ids, 20)`) — the per-corpus n=10
samples computed inside each corpus evidence file are superseded and not used here.

## Per-feature agreement (full sample, n=20)

| Feature | Role | n | Agreements | A_f | Cohen's kappa | Gate (≥0.80) |
|---|---|---|---|---|---|---|
| columns | identity | 20 | 19 | 0.9500 | 0.83 | PASS |
| heading | identity | 20 | 18 | 0.9000 | 0.78 | PASS |
| colour | identity | 20 | 16 | 0.8000 | 0.68 | PASS (at threshold) |
| header | identity | 20 | 14 | 0.7000 | 0.59 | **FAIL** |
| body | variant | 20 | 18 | 0.9000 | 0.76 | PASS |
| rules/boxes | variant | 20 | 17 | 0.8500 | 0.71 | PASS |
| density | variant | 20 | 13 | 0.6500 | 0.45 | **FAIL** |
| photo | variant (cv) | 20 | 20 | 1.0000 | 1.00 | PASS |
| admissible | admit/exclude | 20 | 18 | 0.9000 | 0.69 | PASS |

## Disagreements (full sample)

27 disagreements across 11 of the 20 sampled ids (9 ids matched on every feature):

| id | feature | coder1 (first) | coder2 (second) |
|---|---|---|---|
| GH:038 | density | dense | standard |
| NPM:038 | admissible | no (A7) | yes |
| NPM:028 | columns | 1 | 2-equal |
| NPM:028 | colour | mono | fill-blocks |
| NPM:028 | admissible | yes | no (C1) |
| NPM:001 | colour | one-accent | multi |
| NPM:001 | header | plain-centered | band |
| NPM:001 | rules/boxes | rules | none |
| NPM:001 | density | dense | airy |
| GH:077 | header | split | plain-centered |
| NPM:049 | header | band | ruled |
| NPM:080 | rules/boxes | rules | boxes |
| NPM:080 | density | standard | airy |
| NPM:044 | header | ruled | plain-left |
| NPM:061 | body | sans | serif |
| NPM:061 | header | plain-left | band |
| GH:054 | rules/boxes | none | boxes |
| GH:054 | density | airy | standard |
| NPM:027 | density | dense | standard |
| GH:024 | heading | sans | serif |
| GH:024 | body | sans | serif |
| GH:024 | colour | one-accent | mono |
| GH:024 | header | plain-left | plain-centered |
| GH:007 | heading | serif | sans |
| NPM:014 | density | standard | dense |
| NPM:057 | density | standard | airy |
| GH:055 | colour | mono | one-accent |

Notable pattern: `header` disagreements are concentrated on the split/plain-centered/band/
ruled boundary (5 of 6 mismatches), not random noise — several previews have a title-and-meta
layout that reads as ambiguous between "split" (opposite sides of the header block) and
"plain-centered"/"band"/"ruled" depending on which visual cue the coder weighted first.
`density` disagreements run in both directions (denser and airier), consistent with a
genuinely soft threshold (55/30 lines) rather than a one-sided bias.

## Disclosed exposure and sensitivity run

The second coder disclosed brief accidental exposure to first-coder feature values for
`GH:001, GH:003, GH:006–GH:010, GH:013, GH:019, GH:021, GH:023` and `NPM:001–004` (leaked via
early inspection commands before the extraction script was written). Of these, only
`GH:003, GH:007, GH:008` landed in the n=20 sample. Per the task brief, a sensitivity run
excludes these three ids (n=17):

| Feature | Role | n | Agreements | A_f | Cohen's kappa | Gate (≥0.80) |
|---|---|---|---|---|---|---|
| columns | identity | 17 | 16 | 0.9412 | 0.83 | PASS |
| heading | identity | 17 | 16 | 0.9412 | 0.85 | PASS |
| colour | identity | 17 | 13 | 0.7647 | 0.63 | **FAIL** |
| header | identity | 17 | 11 | 0.6471 | 0.54 | **FAIL** |
| body | variant | 17 | 15 | 0.8824 | 0.68 | PASS |
| rules/boxes | variant | 17 | 14 | 0.8235 | 0.69 | PASS |
| density | variant | 17 | 10 | 0.5882 | 0.35 | **FAIL** |
| photo | variant (cv) | 17 | 17 | 1.0000 | 1.00 | PASS |
| admissible | admit/exclude | 17 | 15 | 0.8824 | 0.67 | PASS |

Disagreements list for the sensitivity run is the full-sample list above **minus** the one
disagreement carried only by an excluded id: `GH:007 | heading | serif | sans` drops out
(`GH:003` and `GH:008` had zero disagreements in the full sample, so removing them changes no
counts). All 26 remaining disagreements are unchanged.

Removing the three disclosed-exposure ids does not improve any failing feature — it makes
things worse: `colour` moves from a marginal PASS (0.80) to a clear FAIL (0.76), because two of
`GH:003/GH:007/GH:008`'s three items had been full agreements that were propping up the
full-sample colour rate. This indicates the exposure disclosure is not masking an inflated
result; if anything the exposed items were coded more carefully (all three exactly matched or
differed on only one feature), consistent with the second coder's own account of re-deriving
them from the image rather than from memory.

## Gate verdict

Per research/82 §7, the literal gate is **every** `A_f ≥ 0.80` across all nine features
(identity + variant + admissibility). That is **not** met, in both the full sample and the
sensitivity run:

- **Full sample: FAIL.** `header` (identity, A_f=0.70) and `density` (variant, A_f=0.65) are
  both below 0.80. `columns`, `heading`, `colour` (identity) and `body`, `rules/boxes`,
  `photo`, `admissible` all pass.
- **Sensitivity run (excluding GH:003/007/008): FAIL, and worse.** `colour` (identity,
  A_f=0.76) additionally drops below 0.80, alongside `header` (0.65) and `density` (0.59).

Because the failure is on an **identity** feature (`header` fails in both runs; `colour` also
fails in the sensitivity run), this is a full **F1 falsifier failure**, not merely a variant
shortfall: research/82 §7 requires an Opus-authored `research/82a-cv.md` amendment sharpening
the `header` (and, per the sensitivity finding, arguably `colour`) rubric text, a full recode
of the cv family by the first coder, and a fresh second-coder sample seeded `"82a:cv"`. This
report does not perform that recode — it only computes and discloses the agreement numbers,
per the task brief.

If the gate is read narrowly per the task brief's own framing (identity features
columns/heading/colour/header must each individually clear 0.80 for the *identity* gate,
while a failing *variant* feature merely disqualifies that variant from filling rather than
failing the whole family, per §7's last sentence): the **identity gate fails** in the full
sample because `header` (A_f=0.70) is below 0.80 — `columns` (0.95), `heading` (0.90) and
`colour` (0.80, at the threshold) all individually clear it. Separately and independently,
the **variant feature `density`** (A_f=0.65) fails and — under §7's "failing variant feature
is not used in filling" rule — would be **disqualified from filling**: the family default's
density value would be used instead of the archetype's own modal density wherever `density`
would otherwise inform a Style/Checklist decision (§8). `body`, `rules/boxes`, `photo` all
pass and remain usable for filling. `admissible` (admit/exclude only) passes at 0.90.

**Net statement:** cv fails the family-wide second-coder gate on `header` (an identity
feature, which under §7's literal text blocks the whole family pending rubric amendment and
recode) and on `density` (a variant feature, which on its own would only be dropped from
filling). The sensitivity run shows the failure is not an artifact of the three
disclosed-exposure items — excluding them adds a third failing feature (`colour`) rather than
resolving either existing failure.
