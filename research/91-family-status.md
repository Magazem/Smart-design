# 91 — Family status dashboard and path to 8–10 designs (Opus planner, 2026-09-24)

This is the handover for any fresh orchestrator. **Numbers are copied from the evidence files
named in each row.** The evidence file wins over this summary. "Projected" ranges are my
estimates, not measurements.

**Sources read:**
- research/80, 82, all 82a-*.md, 82b-ADOPTED.md, ORCHESTRATOR-STATE.md;
- every file in research/designs-evidence/ (as of the working tree at 02eed1e plus uncommitted
  work).

**Legend:**
- N/adm = coded on-topic items / admissible items.
- K≥2 = admissible archetypes with support ≥ 2, *before* the 82a-general header/colour recode,
  so they are provisional wherever a recode is pending.
- Gate = research/82 §7 second-coder agreement.
- A5 = 82b structural-twin borrowing.
- Seeds = the `research/designs/<family>.csv` rows shipping today. Every family except cv has
  exactly 1 seed, which is the doctype default.

---

## 1. Dashboard

| Family | Corpora coded (source: N / adm) | Gate | 82a-general / 82a-deck recode | K≥2 (provisional) | L3 available | A5 | Projected shippable | Remaining steps, in order |
|---|---|---|---|---|---|---|---|---|
| **cv** | GH L1 40/31; NPM L1 40/25; MS resumes unreachable (SPA) | **PASSED**: header r2 17/20 = 0.85, colour 0.80, others pass; density dropped from fill | done under 82a-cv (+ Addendum A) | 14 → 10 kept (cv-fill.md §4) | Europass (merged at rank 2) | — | **12** (10 ranked/authority + 2 exempt defaults; cv-editorial retired) | 1. Repo Keeper commits cv-fill outputs (`research/library/{doc-styles,doc-reasoning}/cv.csv`, `designs/cv.csv`, `provenance/cv.csv`, cv-fill.md, generate_cv_fill.py) together with the cv-editorial fixture repoint. 2. `load-base.py` → `build-portable.py` → pytest green. |
| **deck** | NPM L1 40/25; LO L1 40/23; MS L2 25/17 (105 ids); proposal pptx pool MSPD 20 deferred | **FAILED r1**: heading 0.77, colour 0.67, title-layout 0.73, admissible 0.78; body and density dropped | 82a-deck recode **in progress** (`tmp-deckrc/`) | per corpus 5 / 3 / 1; combined not yet computed; LO alone meets the coarsening trigger | none | — | 6–10 if the r2 gate passes; **1 (seed)** if ≥2 identity features fail again (82a-deck §6) | 1. Finish the recode (all 105). 2. Fresh second coder, seed `"82a:deck"`, n=27, from deck-items.csv, with a sensitivity run excluding the 17 worked-example ids. 3. agreement.py. 4. Decide coarsening family-wide (§4). 5. Fill (F.c). 6. Optionally add the MSPD pool as a 4th corpus **only by a pre-registered ruling before coding**. |
| **invoice** | GH L1 40/31; MS L2 8/8 (all singletons); LO 4 corroboration | **FAILED r1**: header 0.33, colour 0.50; density and table rules dropped | 82a-general recode **in progress** (`invoice-recode-82ag.md` partial, `tmp-invrc/`) | ~7 (combined GH+MS) | none | lender to quote | 6–10 if r2 passes; 3-feature archetypes if one feature drops; 1 if both fail | 1. Finish the recode (48). 2. Fresh second coder `"82a:invoice"`. **Exclude** the round-1 coder, Opus Reviewer, and the recoder. Sensitivity run excluding the 82a-general §C invoice ids (GH:004, 030, 075, 097, MS:005, 006). 3. agreement. 4. Fill. 5. Then quote borrows ≤ 3. |
| **letter** | MSL L2 17 + LOL L2 17 → 34 / 32 adm; GH L1 **not coded** | not yet run | recode **in progress** (`letter-recode-82ag.md` partial) | 8 | DIN 5008 via typst-letter-pro README (authority, merges) | — | **7–10** | 1. Finish the recode. 2. Code GH `"letter template"` L1 when the GitHub API is free. It adds a corpus; its 40 items join the second-coder population, so run the gate **after** GH. 3. Second coder `"82a:letter"`. 4. Fill. |
| **cover-letter** | MSC L2 15/12 (after C22); LO 5 corroboration; GH L1 **not coded** | not yet run | recode **in progress** (MSC in `tmp-letrc/`) | 2 (+ 8 singletons) | none | — | 3–10 (without GH: 2 ranked + singletons, which carry no popularity information) | 1. Recode. 2. GH `"cover letter template"` corpus (L1 if ≥ 40 on-topic, else thin → L2). 3. Second coder `"82a:cover-letter"`. 4. Fill. |
| **report** | GH L1 40/38; MS L2 10/10; ARC 2025 L3: 14 coded, 6 admissible (all singletons, after the C13/C14 re-check) | not yet run | **needed**: report MS is listed in C26; report GH does not cite 82a-general, so verify, and treat it as needing recode | GH 6, MS 3 | ARC singletons (L3 cap 3) | lender to whitepaper | **7–10** | 1. Recode header and colour for GH + MS under 82a-general (fresh worker). 2. Second coder `"82a:report"` over report-items-github.csv + report-items-ms.csv (+ ARC ids if coded as items). 3. Fill (C13 cover/running-page split). 4. Then whitepaper borrows ≤ 3. |
| **poster** | GH L1 40/34 (academic/LaTeX skew); MS 8 corroboration; C27 pool (MS 8 + Typst 8) pending | not yet run | **needed** (C26) | 9 | D&AD Posters (presence) | — | **7–10** (academic skew disclosed) | 1. Recode (C26). 2. Build the MS+Typst pool (GitHub worker dedups, C27) if it reaches ≥ 10. 3. Second coder `"82a:poster"`. 4. Fill. |
| **brochure** | MS+LO pool N=11 / 9 adm | not yet run | recode **in progress** (`tmp-bfrc/`) | 1 (K=7) + 2 singletons | D&AD Catalogues & Brochures (presence, not coded) | — | 3–6 | 1. Recode. 2. Second coder `"82a:brochure"`. 3. Code up to 3 D&AD items as L3 if fetchable. 4. Fill; disclose the Shortfall. |
| **flyer** | MS L2 N=20 / 6 adm (82b recount; 0 K≥2, 6 singletons); A1 pool (LO 4 + Typst 6 + GH flyer/typst) **not built** | not yet run | recode **in progress** (`tmp-bfrc/`) | **0** | none | — | 1–7 (singletons only unless the pool reaches ≥ 10) | 1. Recode. 2. GitHub worker builds the A1 pool (dedup; ≥ 10 or stays corroboration). 3. Second coder `"82a:flyer"` over the 20 (+ pool). 4. Fill via §6 step 3 (ranked singletons); Shortfall disclosed. |
| **memo** | A1 pool MS 7 + Overleaf 4 = 11 / 11 adm | not yet run | recode **in progress**; C28 recodes MSM:006 / OLM:009 columns → 1, which merges archetypes | 3 (4 singletons) | AR 25-50, Purdue OWL (distinct, both fetched) | — | **5–6** | 1. Apply C28 plus the header/colour recode, then recount. 2. Second coder `"82a:memo"` (memo-items.csv). 3. Fill: 3 ranked + 2 L3 + default. |
| **form** | none (MS unreachable, LO noise); L3 only: USWDS+GOV.UK, NHS, ABS | n/a (authority coding; the gate applies only if the orchestrator treats L3 codes as items) | colour recheck done (Fm.8.4) | 0 | 3 distinct archetypes (82b A3 cap 5) | no twin (palette differs) | **3–4** (3 L3 + form-handfilled default) | 1. Fill the 3 L3 archetypes. 2. Retry DSFR/AGDS once (403/timeout): each could add 1 if distinct. 3. Disclose: no ranked source exists. |
| **quote** | none of its own; cross-listing found 0 | n/a | n/a | 0 | none | **borrows from invoice** (twin: same style/palette/page) | 1–4 (seed + ≤ 3 borrowed) | Blocked on invoice fill. Then copy ≤ 3 invoice designs as `borrowed:invoice:…`, re-check C7, rank after own evidence (none). |
| **whitepaper** | none (GH templates < 5; specimens off-topic) | n/a | n/a | 0 | ARC covers report only | **borrows from report** | 1–4 | Blocked on report fill. Then borrow ≤ 3; typeface refilled per §8. |
| **proposal** | MS 7 Word + LO 2 = corroboration; GH `proposal template latex` L1 **not coded** (academic skew) | not yet run | needed for MS (C26) if later pooled | 0 | none | no twin | 1–8 (depends entirely on GH) | 1. Code GH L1 (GitHub worker queue). 2. If ≥ 40 → L1; 10–39 → thin L2; < 10 → A1-pool with MS 7 + LO 2 if ≥ 10 after dedup. 3. Second coder + fill, or seed + Shortfall. |
| **one-pager** | none (82b: no structured source; MS "Executive summary" 1 item, corroboration) | n/a | n/a | 0 | none | no twin | **1–2** (seed + ≤ 1 convention) | Ship the seed + disclose. No further research is justified by 82b. |
| **infographic** | IIB 2022–24 winners: 94 raw, **4 on-topic** (corroboration); MS PPT 3, LO 1 corroboration | n/a | n/a | 0 | IIB (juried) as an A2 pool only if ≥ 10 on-topic | no twin | 1–5 | 1. Per the pre-registered I.7 ruling, extend IIB backwards one edition at a time (2019, 2018 … 2012), stopping at the first edition where the cumulative on-topic count ≥ 10. 2. If reached: code the pool, second coder `"82b:infographic"`, fill. Else seed + Shortfall. |

**Totals, projected:**
- About **75–100 designs** across 16 families.
- 6 families can realistically reach 8–10 ranked designs: cv (done), deck, invoice, letter,
  report, poster.
- 4 will ship short lists (3–6): cover-letter, memo, brochure, form.
- 6 will ship seeds, borrowed or singleton designs with a disclosed shortfall: flyer, quote,
  whitepaper, proposal, one-pager, infographic.

---

## 2. Critical path to v0.5.0

These are sequential constraints; everything else can run in parallel.

1. **GitHub search API is one user at a time** (10 req/min per IP). Queue it in value order:
   1. letter GH (moves letter to a 3-corpus family);
   2. cover-letter GH;
   3. poster Typst pool dedup;
   4. flyer A1 pool;
   5. proposal GH.

   **Gates that include a GH corpus must wait for it** (letter, cover-letter).
2. **Recode → fresh second coder → agreement → fill**, per family. Each fill is about 1 worker
   session. Twins borrow only after their lender is filled: quote after invoice, whitepaper
   after report.
3. **Independence roster.**
   - A second coder must not have coded, recoded or authored rules with worked examples on that
     family's items.
   - Opus Reviewer is excluded from invoice (round-1 second coder) and has worked-example
     exposure on deck, invoice, letter and cover-letter (82a-deck, 82a-general), so those
     families need a sensitivity run excluding the named ids.
   - Keep a roster in ORCHESTRATOR-STATE.
4. **One load per batch.** `load-base.py` → `build-portable.py` → pytest → Repo Keeper commit.
   Never load a family whose fill has not passed §12 F4/F5 review (recount and fill
   determinism).
5. **Non-Phase-4 release blockers:**
   - R5 fixes (research/89 F1: old brand kits break all queries; F2 "letter paper"; F3 name
     particles);
   - R6 fixes (research/90 F2/F3: failing brand colour and handoff text-safe roles; F6
     bilingual kits);
   - a green suite on the committed tree;
   - the P6.5 portable trial actually run (harness committed, not yet run);
   - a fresh release ZIP so the pack and the skill match (research/87 I8).
6. **Hygiene.** Delete `research/designs-evidence/tmp-{bfrc,deckrc,invrc,letrc}/` (scratch
   previews) before any commit that touches that directory. They must never be committed.

## 3. Recommended release bar for v0.5.0

**Ship v0.5.0 when all of these are true:**
- (a) **cv** is loaded (done on disk; commit pending).
- (b) **deck, invoice, letter, report, poster** have each passed the §7 gate, or applied the
  second-failure rule (a feature dropped and disclosed), **and** been filled and reviewed
  (F4/F5).
- (c) **quote and whitepaper** have their borrowed designs (cheap once invoice and report are
  filled).
- (d) Every other family ships whatever passed, plus its seed, with a one-line Shortfall in
  `designs.csv` notes and in the release notes. That covers cover-letter, memo, brochure, flyer,
  form, proposal, one-pager and infographic. Examples:
  - "form: 3 authority designs, no ranked source exists";
  - "one-pager: convention only".
- (e) The non-Phase-4 blockers in §2.5 are closed.

**Do not hold v0.5.0** for the GH corpora of cover-letter and proposal, or for the IIB backwards
extension. Those go to v0.5.x. If letter GH is not coded by the time (b) is otherwise met, ship
letter on its two L2 corpora (already 32 admissible, 8 K≥2), gated on those alone. Record that
the gate must re-run when GH lands.

**Honesty rule, restated:** a family that falls short of 8–10 ships what the evidence supports.
Its list order carries no popularity information where only singletons exist (§13). This
dashboard's projections are estimates. Replace each row with the evidence file's numbers when
that family's fill lands.
