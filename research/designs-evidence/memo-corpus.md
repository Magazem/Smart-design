# Memo corpus — Microsoft Create memos (L2, below the 10-item floor → corroborate only); LibreOffice memo (corroborate only); GOV.UK (no memo guidance found)

Coder: Design Researcher. Counts only (research/82 §1). Retrieved 2026-09-23. **Plain statement: there is no rankable memo evidence. This is a Shortfall family; nothing below enters a frequency table or a Rank Value.**

## M.1 Sources
- **MS(memos):** `https://create.microsoft.com/en-us/templates/memos` → `curl -sL` redirected (HTTP 200) to `https://word.cloud.microsoft/create/en/memo-templates/?source=create_flow` (same vendor catalogue, items are in the static payload → codeable under 82a C5). Page order, no metric. **10 cards; on-topic memos = 7** (pos 1-7). Off-topic: pos 8 "Modern celebration of life program", pos 9 "Thank you card", pos 10 "Hats off graduation card". 7 < 10 → per §2 "a catalogue with <10 on-topic items is not coded as a corpus; its items may only corroborate (listed, not counted)". The research/82 probe found 9 cards; the page now shows 10.
- **LO(memo):** `https://extensions.libreoffice.org/en/extensions?Tags%5B%5D=118&q=memo&ord=download_d` (HTTP 200) returned 5 items (ids 3881, 5049, 99351, 20655, fattura-artigiani-commercianti-e-piccole-imprese). Titles seen: 3881 "Business Document Templates", 20655 "E-learning Course Authoring Methodology", 99351 a meeting-invitation template; 5049 is the three-column leaflet; the invoice item is another family. **0 memos** (full-text `q=` noise). Corroboration count: 0.
- **L3 GOV.UK content guidance:** fetched `https://www.gov.uk/guidance/content-design/writing-for-gov-uk` (301 → `https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/tone-of-voice/`); WebFetch of the redirected page reports "no mention of memo found". No GOV.UK page prescribing a memo format was located → **no L3 memo source**. (One retry done, as §10 says "retry".)

## M.2 MS memos listed for corroboration (NOT counted, NOT ranked)
Descriptive notes only, from the 400-px thumbnails (one look each; no §4 admissibility applied because nothing is coded as a corpus).

| pos | Item | Notes (not a rank input) |
|---|---|---|
| 1 | Logo memo | logo box top-left; purple diagonal bands top-right and bottom; To/From/CC block stacked; sans heading |
| 2 | Memo (simple design) | large grey serif "MEMO"; pale-yellow full-page fill; To/From/CC/Date/Re in a label-left column; hairline rule |
| 3 | Angles and curves memo | serif "Memorandum"; logo box; orange/mauve square blocks top-right and bottom-left; stacked To/From/CC |
| 4 | Modern memo (simple design) | large orange lowercase display "memo"; cream fill; label-left To/From/CC/Date/Re; orange rules top/bottom |
| 5 | Prism memo | multicolour triangle strips top and bottom; date top-right; To/From/Subject/CC caps labels |
| 6 | Business memo (bold design) | red "Memo" over a heavy black rule; date top-left; label-left TO/FROM/CC/RE column; COMMENTS body; company footer with rule |
| 7 | Blue spheres memo | round logo art top-right; blue "Memo"; stacked To/From/CC; blue body text |

Observation only: all 7 put a To/From/(CC/Date/Subject|Re) block at the head; 3 of 7 use a label-left column, 4 of 7 stack the labels; 5 of 7 carry decorative header/footer art. With 7 items no share is quoted as evidence.

## M.3 Consequences for shipping
- No ranked memo design, no L3 design. The seeded doctype default keeps its place as the doctype default (evidence class convention, disclosed). Filling has nothing to fill from.
- Expected Shortfall (§10: "2-5, Shortfall") is not met even at its floor: **0 ranked, 0 juried/authority, ≥1 convention.** The floor of 5 non-convention designs cannot be reached from the public sources reachable on 2026-09-23.

## M.4 Bias statement
Only Microsoft's editorial selection (7 memo templates, Word-authored, decoration-heavy) was reachable. No juried award category exists for memos, GOV.UK has no memo format, LibreOffice returned no memo. Prevalence of curation, not usage; popularity is not quality (§13).

## M.5 Ambiguities met
1. Card count moved from 9 (research/82 probe) to 10; three cards are other families and were not counted.
2. 82a C5 applies: the redirect target is static and reachable, but holds only 7 on-topic items.
3. No second-coder list: nothing is coded (82 §7 has nothing to sample).
