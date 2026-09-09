# Notes — 41: marketing-class section model (v0.2 phase A3, the last six)

## Scope
brochure-3panel, brochure-gatefold, flyer-single-sheet, poster-single-canvas,
deck-standard, cover-letter-standard — the six structure_keys in
data/base/structures.csv with no Section Order left. Completes all fifteen.

## Only one new canonical section: `agenda` (3 rows, en/fr/de, all primary)
Every other token in all six orders resolves to an existing section from
research/39 or research/40 — no new rows needed for them. This is the
heaviest-reuse phase of the three; see per-structure reasoning below.

## Section Orders
- brochure-3panel: headline;introduction;key-points;call-to-action;contact
- brochure-gatefold: headline;introduction;key-points;call-to-action;contact
- flyer-single-sheet: headline;key-points;call-to-action;contact
- poster-single-canvas: headline;call-to-action
- deck-standard: cover;agenda;problem-statement;proposed-solution;findings;call-to-action;contact
- cover-letter-standard: sender;recipient;date;salutation;body;closing

## Reused sections (all from research/39 or research/40, none duplicated in this file)
- `headline`, `key-points`, `call-to-action`, `contact` (research/40, one-pager set) —
  the core marketing skeleton, used across both brochures, the flyer, the poster,
  and (contact/call-to-action) the deck.
- `introduction` (research/40, report set) — reused cross-class into both brochures
  for the first inner-panel copy. Passed the check: FR "Introduction" / DE
  "Einleitung" are plain generic openers, no report-specific reading.
- `cover`, `problem-statement`, `proposed-solution` (research/39, proposal set) and
  `findings` (research/40, report set) — all reused into deck-standard. See the
  deck reasoning below for why `proposed-solution` passes here after being
  rejected for whitepaper in A2.
- `sender`, `recipient`, `date`, `salutation`, `body`, `closing` (research/39,
  letter set) — reused wholesale into cover-letter-standard.

## PRE-RULING applied: panels and slides are not Section Orders
Per the lead's ruling, a Section Order is a content-reading-order, not a panel
or slide map. Both brochures got the identical content order for exactly that
reason: a 3-panel and a gate-fold format tell the same story (cover message →
opening copy → key points → ask → contact), just spread across a different
number of physical panels. That panel-count difference is a page-formats
concern, not a structures concern, so I did not invent extra sections to make
the two brochures look different — that would have been padding to fake a
distinction the data model doesn't carry. If page-formats later needs a
panel-to-section map for tri-fold vs gate-fold, that's a separate table, not
a longer Section Order here.

## The hard one — do panels/slides genuinely fit a Section Order at all?
**Partially, with a caveat worth flagging.** The CONTENT arc (what's said, in
what order) does fit a Section Order cleanly for all three physical formats
here. What does NOT fit is panel/slide COUNT or ADJACENCY — a Section Order is
a flat ordered list of content, but a real tri-fold's physical reading path
is not strictly linear (a reader may see the outer cover panel before *and*
after the inner spread, and a gate-fold's two inward flaps can be read in
either order before the center). The model can express "this content comes
before that content" but not "this content lives on a panel the reader may
revisit" or "these two panels are read in parallel, not series." For decks,
the fit is closer: slides genuinely are read start-to-end in one order, so
`cover;agenda;...;contact` as slide ROLES (not slide COUNT — a deck can spend
three slides on `findings`) is an honest fit, no caveat needed. Bottom line:
Section Order works for decks without qualification; for the two brochures it
works as an approximation of "what's said in what sequence," but the
physical fold structure is a real gap the model doesn't capture and
shouldn't be forced into pretending to.

## Poster — 2 sections, not padded
poster-single-canvas: headline;call-to-action. Considered `key-points` and
`contact` and dropped both: a single-canvas poster is read at a glance, not
studied — a separate itemized key-points block and a separate contact block
are two things real posters usually fold into the headline's supporting line
and the call-to-action's fine print (a QR code or URL sitting inside the CTA
block), not standalone content sections. Two is the honest count; a third
section here would be forcing the model, which the brief explicitly asked me
not to do.

## Deck-standard — slide roles, and why `proposed-solution` passes this time
Per the pre-ruling, this is the content ARC (title → agenda → problem →
solution → evidence → ask → close), not a slide-by-slide list.
`proposed-solution` was rejected for whitepaper-standard in A2 because its DE
primary `Lösungsvorschlag` carries commercial-bid flavor that's wrong for a
neutral argumentative document. deck-standard is the opposite case: grouped
in this marketing-class batch, it's being modeled as a pitch/sales deck, where
a commercial-bid register is exactly right — the "ask" slide (`call-to-action`)
only makes sense if the preceding slide is pitching something. So the same
word that was wrong for whitepaper's neutral tone is correct for a deck's
sales tone; this isn't a blanket "proposed-solution is safe," it's a
register match checked per target, same method as the two rejections it
contrasts with.

## Cover-letter-standard — not invented, confirmed as reuse
Checked before inventing, per the brief. A cover letter is a formal business
letter in every respect that matters here (sender/recipient/date/salutation/
body/closing), so its Section Order is letter-standard's set verbatim, zero
new sections. This isn't cross-class reuse in the sense the other checks
guard against — cover-letter-standard and letter-standard are the same kind
of document, so there's no register mismatch to check for.

## Verification (research/41-verify.py, run via the given python3.exe)
All six checks pass.
- Check 1 (every Section Order token resolves against base+39+40+41): NONE
  unresolved — all resolve. Token counts: brochure-3panel 5, brochure-gatefold
  5, flyer-single-sheet 4, poster-single-canvas 2, deck-standard 7,
  cover-letter-standard 6.
- Check 2 (single shared counter per (canonical_section,language) across all
  four sources, load order base→39→40→41): NONE — zero heading_key collisions.
- Check 3 (exactly one primary per (canonical_section,language)): NONE bad,
  both in the new file alone and in the base+39+40+41 union; no section
  missing a language.
- Check 4: both file headers match the required shapes exactly.
- Check 5 (blank source): NONE — every one of the 3 new rows carries a real
  citation.
- Check 6: all six expected structure_keys present, no duplicates.
