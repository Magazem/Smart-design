# cv — inter-coder agreement, round 2 (header treatment only)

Per research/82a-cv.md step 4 (gate: header A ≥ 0.80 → header stays in cv identity with the
recoded values; a second failure would remove header treatment from cv's identity features).
This is the round-2 re-test after `research/82a-cv.md`'s sharpened header-treatment decision
procedure and Addendum A.

Recomputed independently (script `research/designs-evidence/compute_r2_agreement.py`, stdlib
only, no external deps) by parsing:
- `research/designs-evidence/cv-header-recode.md` per-item table, column **header (r2a)**
  (r2 values plus the four Addendum A flips: GH:055 ruled→split, NPM:039 ruled→plain-left,
  NPM:048 plain-left→ruled, NPM:063 split→ruled) — this is the recoder's final call for all
  80 coded cv items (GH 40 + NPM 40).
- `research/designs-evidence/cv-second-coder-r2.md` Results table (n=20), the fresh,
  independent second coder's `header` codes for the family-wide sample drawn per
  `research/82a-cv.md` step 3: ids sorted lexicographically from `cv-items.csv` (80 coded
  items), then `random.Random("82a:cv").sample(ids, max(min(10, len(ids)),
  math.ceil(0.25 * len(ids))))` = 20 ids.

## Result

| Feature | Role | n | Agreements | A_f | Gate (≥0.80) |
|---|---|---|---|---|---|
| header | identity | 20 | 17 | 0.8500 | **PASS** |

## Disagreements (3 of 20)

| id | recode (header r2a) | second coder (r2) |
|---|---|---|
| NPM:068 | image-hero | ruled |
| GH:019 | plain-left | band |
| NPM:005 | band | plain-left |

All three sit on the low-confidence / borderline boundaries the recoder herself flagged in
`cv-header-recode.md`: NPM:068 (image own area 44% but only ~18% visible around the card —
recoder kept image-hero "under the literal 'own area'"), GH:019 (band width 0.599 vs the 0.60
threshold, BORDERLINE), and NPM:005 (no borderline flag from the recoder, but the second coder
read the fill boundary as coinciding with the first section heading rather than sitting
between the header block and that heading — a band/ruled-precondition judgement call, not a
rubric gap). No new pattern emerges beyond what `research/82a-cv.md`'s Addendum A already
anticipated as residual ambiguity at these specific thresholds.

## Gate verdict

**PASS.** header A_f = 0.85 ≥ 0.80. Per `research/82a-cv.md` step 4, `header treatment` stays
in the cv identity feature set (`columns | heading | colour | header`) with the r2a recoded
values, and the cv family's F.a corpus phase is closed:

- columns 0.95, heading 0.90, colour 0.80 (round 1, `cv-agreement.md`) — unchanged, not
  recoded, still pass.
- header 0.85 (this file, round 2) — pass, recode adopted.
- `density` (variant) failed round 1 (A_f=0.65) and was not recoded (research/82a-cv.md: "not
  used in cv filling"); the cv family default density value is used wherever filling would
  otherwise consult the archetype's own modal density.

The cv family therefore clears the pre-registered second-coder gate (research/82 §7) on every
identity feature and is eligible for the F.c filling task (research/82 §8-§9), using the r2a
header values, `density` excluded from filling per the round-1 ruling.
