# research/82a-cv — cv header-treatment rule, sharpened (Opus, 2026-09-23)

**Trigger.** research/82 §7 falsifier fired for cv (`designs-evidence/cv-agreement.md`, n=20):
`header treatment` (identity) A=0.70 < 0.80; 5 of 6 mismatches sit on the band / ruled / split /
plain-centered boundary. This file replaces ONLY the cv `header treatment` decision rule of §4.
Nothing else changes: other features, value sets, identity set, image-hero test (82a C1),
thresholds and §5-§8 all stay as written. (`colour` passed the gating full sample at 0.80 and is
not amended here.)

**Density.** `density` (variant) A=0.65 failed. Per §7 last sentence it is **not used in cv
filling**; the cv family default applies. No recode of density.

## Definitions (measure on physical page 1 of the file as rendered; for web screenshots the "page" is the document sheet, excluding browser chrome, shadow and canvas outside the sheet)

- **Live width** = horizontal distance from the leftmost to the rightmost body text on page 1.
- **Name** = bounding box of the largest heading text (the person's name).
- **Header block** = the name plus every contiguous line after it (title, contact/meta lines,
  an un-headed summary paragraph, photo) down to, but excluding, the first section heading.
  Logos, crests, mascots and avatars are neither "title" nor "meta" text.
- **Background** = the page colour at the body text. A **fill** is a solid area differing from
  the background by HSL ΔL ≥ 0.03 or by a chromatic colour (§4 definition).
- **Body line** = the line pitch of body text on page 1.

## Decision procedure (strict priority, first match wins; scope: element starts in top 20% of page 1)

1. **image-hero** — unchanged (82a C1).
2. **band** — ALL of: (a) a fill lies behind the name's glyphs; (b) fill height ≥ the name's
   cap height; (c) fill width ≥ 60% of page width; (d) the fill ends (returns to background) above
   40% of page height in the column where the name sits. A fill running the full page height
   (sidebar, full-page tint) fails (d) → not a band; continue.
3. **ruled** — a horizontal line OR any fill that is not behind the name, with ALL of:
   (a) length ≥ 80% of page width or ≥ 90% of live width; (b) it is either above the name or
   between the last header-block line and the first section heading; (c) no text lies between it
   and the header block; (d) gap to the nearest header-block line ≤ 4 body lines. Section-heading
   underlines (rules below a section heading) never count. Sidebar-only or column-only rules fail (a).
4. **split** — ALL of: (a) the name is flush to one side (its outer edge within 5% of live width of
   that margin) and a meta/contact TEXT block is flush to the opposite side; (b) their bounding
   boxes do not overlap horizontally; (c) their vertical extents overlap, or the meta block starts
   ≤ 1 name line-height below the name's baseline. Contacts centred or aligned under the name are
   not split. Images/logos on either side never create split.
5. **plain-centered** — name's horizontal centre within ±5% of page width of the page centre.
6. **plain-left** — everything else.

A coder records the measured quantity for any test decided within 10% of its threshold
(evidence column `header-note`).

## Worked edge cases (from the round-1 disagreements)

- **NPM:001 jsonresume-theme-even** (coder1 plain-centered, coder2 band). Full-width tint
  `#F3F4F5` on white (ΔL ≈ 0.045 ≥ 0.03) behind photo, name, contacts; ends at ~7% of sheet
  height. Band tests a-d pass → **band**. Tint strength is not a judgement call.
- **NPM:049 jsonresume-theme-caffeine** (band vs ruled). A full-width teal stripe at the top edge
  (≈15 px of 2232), name not on it; gap to name ≈ 2.8 body lines. Fails band (a) → rule tests
  pass → **ruled**.
- **NPM:061 jsonresume-theme-executive-slate** (plain-left vs band). The name sits on a dark
  sidebar fill that runs the full page height: band (d) fails. The rule under the title spans the
  sidebar only (<90% live width) → not ruled; no split; name centre far left of page centre →
  **plain-left**.
- **GH:077 maksymilan/zju-resume-template** (split vs plain-centered). University logo left,
  mascot right, name and contacts centred. Images never make split; the blue rule lies under the
  section heading 教育背景 (excluded) → name centre ≈ page centre → **plain-centered**.

Also resolved: **NPM:044** data-driven (ruled vs plain-left): the heavy blue line below the
un-headed summary spans ~100% of live width, above the first section heading → **ruled**.
**GH:024** liweitianux/resume (plain-left vs plain-centered): code PDF page 1 (Chinese); name
centre ≈ 12% of page width → **plain-left**.

## Recode and re-test

1. A single **fresh worker** (not either round-1 coder) recodes `header treatment` ONLY, with this
   procedure, for **all coded cv items in both corpora** (GH 40 + NPM 40), writing the new value
   and `header-note` into `cv-corpus-github.md` and `cv-corpus-npm-ms.md`; the old values are kept
   in a `header (r1)` column. Admissibility and all other codes are untouched.
2. The orchestrator generates `research/designs-evidence/cv-items.csv` by script (82a C11: id,
   name, url, preview_url; coded items only) before step 3.
3. A **fresh, independent second coder** reads ONLY `cv-items.csv`, research/82 §4-§5, the 82a
   clarification files and this file (evidence .md files off-limits; C12 exposure disclosure
   applies). Sample: all 80 coded ids, family-wide (C10), sorted, then
   `random.Random("82a:cv").sample(ids, max(min(10, len(ids)), math.ceil(0.25 * len(ids))))`
   (= 20). The second coder codes `header treatment` for the sample.
4. Gate: header A ≥ 0.80 → header stays in cv identity with the recoded values. **A second failure
   removes `header treatment` from cv's identity features** (archetype = columns|heading|colour),
   disclosed in the cv evidence file, per §7.

## Addendum A (orchestrator, 2026-09-24) — gaps met by the recoder, fixed BEFORE the second coder runs
A1 The header block is the name plus any title/tagline and contact lines. An un-headed summary
   paragraph is NOT part of the header block. A full-width rule between the header block and such a
   summary is therefore "directly below the header block" and satisfies the ruled test (NPM:048, NPM:063).
A2 Rules belonging to SECTION headings (over- or underlines of "Experience", etc.) never count for
   the header test, whichever side of the heading they sit on (GH:013).
A3 "Page" is the document sheet only; any web canvas, mockup background or device frame around it
   is ignored for every test (NPM:007, promo mockups). Sheets rendered under ~300 px tall are coded
   but flagged low-confidence.
A4 (reconciles A1 with worked example NPM:044) A1 WIDENS the ruled test, it never narrows it. A full-width
   rule counts as "directly below the header block" if the only text between it and the header block is an
   un-headed summary of <= 6 lines, i.e. a rule below the summary and directly above the first section
   heading is ruled (NPM:044, 054, 069, 073 stay ruled, as the recoder coded them).
