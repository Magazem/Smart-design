# research/82a — Clarifications round 7: gate-failure rulings (orchestrator, 2026-09-25)

Ratifies the draft rulings in research/82a-gate-failures.md (Design Researcher 2), with the changes
below. The draft's clarification texts in §10 are RATIFIED verbatim under NEW NUMBERS, because C33
already exists (82a-clarifications-5):

| draft | ratified as | subject |
|---|---|---|
| C33 | **C42** | colour background is exactly B1a; voids reading R2 |
| C34 | **C43** | brochure header scope (front panel) |
| C35 | **C44** | full-page scenes and patterned strips |
| C36 | **C45** | memo header |
| C37 | **C46** | A3/A5 scope, every family |
| C38 | **C47** | unit of coding = prescribed specimen, never site chrome |
| C39 | **C48** | charts vs fills |
| C40 | **C49** | columns with panels and tiles |
| C41 | **C50** | A6 sampling of thin strokes |

Re-test seed for every family below: `random.Random("82a-r2:<family>")`.

## Independent check by the orchestrator
- **VOID of the brochure and flyer colour re-tests: ACCEPTED.** 82a-general B1a is mechanical: the
  background is "the most common colour class on a 20×20 sample grid". The recoder's disclosed
  reading R2 (brochure-recode-82ag.md, lines 19–25) demotes a saturated majority colour to a B3
  fill. That departs from the literal text and from worked example §C MSC:002. The re-test
  therefore tested R2, not the rule. A coder departing from the literal text is recoded (82a-1
  preamble); it is not a rubric failure. The colour recode goes to a FRESH worker who has not
  read either agreement file.
- **Deck r2: full run binds.** Confirmed from 82a-deck §6 step 2: "Both numbers are published,
  and the gate uses the full sample". Result:
  - colour 0.70 is a second failure, so colour is DROPPED;
  - heading 0.81 passes;
  - deck identity = background | heading | title layout;
  - ranked archetypes ship.

  deck-agreement-r2.md's net statement is corrected accordingly.

## Rulings per family
| family | ruling |
|---|---|
| brochure | header DROPPED (2nd failure). Colour: void, then fresh recode under C42 and re-test. If it fails again, colour is dropped and §D.5 applies: no ranked archetypes. |
| flyer | header DROPPED. Colour: void, then fresh recode under C42 and re-test. Admissible (1st failure): recode all 20 under C46 and re-test. If admissibility fails again, every disputed item is adjudicated individually. |
| memo | header (1st failure): the first coder recodes it under C45, then re-test. If it fails again, header is dropped. |
| form | void (scope), then fresh coding of all 4 under C47 plus a clean second coder on all 4. **Small-n: the gate is applied literally** (n=4, so 3/4 = 0.75 FAILS). A second failure means form ships seeds + L3 authority rows and a shortfall. |
| deck | colour DROPPED; ranked archetypes on 3 identity features; fill proceeds (after the R7 engine fixes). |
| poster | colour DROPPED (2nd failure), so identity = columns \| heading \| header. Admissible (1st failure): fresh recode of all 55 under C46, then re-test. If it fails again, every disputed item is adjudicated individually. Fill waits for the admissibility outcome. |
| invoice | identity passed. Admissibility is re-run family-wide by the first coder (mechanical A2 emoji scan; A6 per C50). GH:090 and GH:005 are excluded now (both mechanical). MS:004 is decided under C50. Re-test. The fill waits for the re-run, so the admitted set is final. |
| infographic | 1st failure: recode columns, colour and rules/boxes under C48 and C49, then re-test. If it fails again, the failing features are dropped. |

agreement.py: strip parentheticals and after-comma notes on the non-override path too (DR2 §9).
The parser artifacts in DR2's §4 (form FMA:004, brochure MSB:010) are fixed by this change.
