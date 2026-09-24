# research/82a — Clarifications round 5 (orchestrator, 2026-09-24)

C25 RATIFIED (report-corpus-ms.md RM.8): where a catalogue publishes only a cover thumbnail, body class may
    be read from the template file's DECLARED theme minor font and columns from the declared section
    columns (w:cols) — consistent with §4's "declared font wins". Features that cannot be observed
    (rules/boxes, density) are coded `unknown` (82a C7) and fall back to the family default in filling.
C26 Families coded before research/82a-general.md landed (report MS, proposal MS, poster, cover-letter,
    letter, invoice, brochure, flyer, memo, form) have header treatment and colour use RECODED by a fresh
    worker under 82a-general before their second-coder check; the first coders' header/colour values are
    kept as (r1) for the record only.
C27 (answers flyer/poster question, 2026-09-24) An A1 pool (several catalogues each <10 on-topic items,
    pooled to >=10) IS a corpus in its own right and MAY sit beside other corpora (L1 or L2 >=10) of the same
    family; the family's combined share is the unweighted mean across corpora (§6), the pool counting once.
    Items appearing in more than one corpus are deduplicated (keep the first by corpus order: L1, then L2,
    then pool). The pool must reach >=10 on-topic items AFTER dedup, else it stays corroboration-only.
    Flyer pool (LO + Typst + GH flyer/typst) and poster pool (MS 8 + Typst 8) are assembled by the GitHub
    worker, who alone can dedup against GitHub items.
C28 (extends C22a to all families, 2026-09-24) Routing / address / metadata blocks — sender, recipient, TO/FROM/
    CC/DATE/SUBJECT, issuer, bill-to/ship-to, reference/number/date panels — NEVER make a column or sidebar in ANY
    family, wherever they sit. `columns` counts running body text only. Applies to memo (MSM:006, OLM:009 -> 1),
    invoice, quote and any family coded later; already-coded items affected only by this rule are recoded in place
    with a note.
C29 (form, 2026-09-24) Thresholds are applied LITERALLY at the boundary (S >= 0.20 is chromatic, including exactly
    0.2000): NHS codes 1|sans|one-accent|box as coded; the grey-reading is kept only as the disclosed sensitivity.
    C7 (all-cells table) targets DATA tables; a grid of answer boxes on a form is field style `box`, not C7
    (ABS contact grid admissible).
C30 RATIFIED (infographic-corpus-iib.md I.8.4, 2026-09-25) Charts are MARKS, not illustrations: data-encoding
    graphics (bars, lines, dots, maps used as data) count as §B elements/shapes and never make `image-hero`; only
    pictorial imagery (photos, illustrations) can. Applies to every family.
C31 (cover-letter on-topic test, 2026-09-25) The cover-letter family = letters accompanying an application
    (job, internship, scholarship, programme admission) — the skill's doctype keywords are cover letter / motivation
    letter / job application letter. Journal/manuscript-submission cover letters are a different document (academic
    correspondence): they are OFF-TOPIC for cover-letter and cross-listed to `letter` (82b A4). A corpus walk that
    loses items to this test continues down the ranking to restore N=40 on-topic, per §3.
C32 (faint watermarks, 2026-09-25) A single faint watermark (seal, crest, "DRAFT") behind running text is NOT A3
    "busy fill" when BOTH hold, measured with lib/color.contrast_ratio: (a) watermark vs page background <= 1.3:1,
    and (b) body text vs the watermark-tinted area >= 4.5:1. Such items are admissible; the watermark is ignored for
    colour use (like editor artefacts, C20) and is never reproduced in filling. Either test failing -> A3 stands.
    "DRAFT" stamps are editor artefacts and always ignored. Journal reviewer-response letters stay on-topic for
    letter (correspondence), disclosed.
C33 (corpus growth after second-coder sampling, 2026-09-25) The §7 sample is drawn from the coded ids that exist
    when the second coder is assigned. Items added to the family afterwards by the SAME first coder under the SAME
    rules (e.g. memo pool 11 -> 25 via Overleaf + GitHub) do not invalidate the gate: agreement measures rule
    reliability, not corpus completeness. Disclose the sample frame and the later additions in the agreement file.
    If a DIFFERENT first coder adds items, draw a supplementary sample (seed "82a:<family>:supp") of
    max(3, ceil(25% of the added items)) from the additions only.
