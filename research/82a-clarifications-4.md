# research/82a — Clarifications round 4 (orchestrator, 2026-09-24)

Raised by the cover-letter/letter L2 coder (letter-corpus-l2.md L.0). Coder-defined rules are
either RATIFIED (binding for every family from now on) or OVERRULED (affected items recoded).

C17 RATIFIED — fill threshold: a "non-white fill" (§4 colour use, band) is any area with HSL
    L <= 0.90, the same L bound §4 already uses for "chromatic". Gradients count as fills.
C18 RATIFIED — `band` requires header text to sit ON the filled area.
C19 RATIFIED — letterhead position (letter, cover-letter), first match wins: a return-address line
    above the recipient -> `address-window`; else sender text in the top 25% -> top-left /
    top-centered / top-right by its alignment; else sender logo in the top 25% -> same; else
    record the sender block's position in the note ("foot") and code `top-left`.
C20 RATIFIED — A5 (repeated decoration) applies to identical discrete motifs, not to continuous
    pattern bands. Editor UI (field shading, text boundaries, application background) is ignored.
C21 RATIFIED — shares count ADMISSIBLE exemplars (k); inadmissible items stay in N (§6).
C22 OVERRULED (coder's rule h) — columns are counted in the BODY only (from the salutation / first
    section onward). Sender, recipient, date and reference blocks above the salutation are header
    zone and NEVER make a column or sidebar. -> recode `columns` and admissibility for every
    cover-letter and letter item excluded by C1 on that ground (cover letters: 9 exclusions).
C23 DIN 5008 in filling: design filling uses the archetype's MODAL variant values (§4). DIN 5008
    geometry (fetched secondary: Sematre/typst-letter-pro) is recorded as an authority provenance
    row and applies to German-language letter doctypes' PAGE FORMAT (address window, fold marks,
    margins), not to the design's letterhead variant.

## Round 4 addendum (orchestrator, 2026-09-24)
C22a C22 is read by INTENT: sender, recipient, date and reference blocks never make a column or sidebar
     WHEREVER they sit (above or beside the salutation/first body lines). Only running body text columns
     count. The coder's intent reading in cover-letter-corpus-l2.md CL.11 and letter-corpus-l2.md L.13 is
     confirmed; the strictly geometric alternative is recorded there but not used.
C24  Items csv (C11) may carry ONE extra column `pages` listing the page numbers a second coder must view
     (e.g. report cover + first running-text page per C13). It holds page numbers only, never codes.
     report-items.csv gains it from report-corpus-l3.md R.8.1.
