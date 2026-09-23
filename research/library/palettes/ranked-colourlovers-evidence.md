# research/library/palettes/ranked-colourlovers-evidence.md

Task P3.5 -- ~15 ranked palettes from a numeric popularity source, admitted through a
pre-registered mechanical filter (research/80 SS3, this brief). Per research/81, the
COLOURlovers API itself is confirmed dead as of this session: `curl`
`http://www.colourlovers.com/api/palettes/top?format=json&numResults=100` returns HTTP 403
(Cloudflare challenge page) over plain HTTP; the `https://` form of the same path returns
HTTP 410 with body `{"error":"gone","message":"The COLOURlovers API closed when the site was
rebuilt in 2026."}` (quoted verbatim from the actual response, not paraphrased). Coolors and
Color Hunt were already confirmed not fetchable per research/81 (client-side injected
results, no numeric metric in the static payload). Fell through to fallback #2 of the brief.

**Auditor re-probe 2026-09-23** (fix 11): `curl` of the https, http and apex forms of
`www.colourlovers.com/api/palettes/top?format=json&numResults=100` all returned **403**
(Cloudflare "Just a moment…" challenge), with and without a browser User-Agent. The quoted
410 "gone" body above could **not** be reproduced in this re-probe. The conclusion (API not
fetchable, must use a fallback) is unaffected either way, but the exact HTTP status/body
quoted for the `https://` form should be read as observed once by the original researcher,
not reproduced in audit.

## Source

`https://unpkg.com/nice-color-palettes@4.0.0/1000.json` (pinned; fix 10 -- the unpinned
`.../nice-color-palettes/1000.json` 302-redirects here today, but an unpinned URL would
silently change ranks under a future major version) -- curl, HTTP 200, 51585 bytes: a flat
JSON array of 992 palettes, 5 hex strings each (the package's own README notes
duplicates/short palettes are pre-filtered out, hence 992 not 1000). `100.json`, `200.json`
and `500.json` at the same pinned version were also fetched and have exactly 100, 200 and 500
entries respectively, and share the `1000.json` prefix -- so array position for any rank
<=500 (all 15 admitted rows are ranks <=137) is an exact, stable API position, not an
artefact of the 1000-entry file alone.

`https://unpkg.com/nice-color-palettes/README.md` -- curl, HTTP 200. States verbatim: "A JSON
of the top color palettes on ColourLovers.com, as RGB hex strings". This confirms the corpus
is COLOURlovers-sourced but does **not** by itself establish that array order is populatity
rank (fix 8/9): the ordering evidence is `bin/fetch.js` in the same package (curl, HTTP 200),
which pages `http://www.colourlovers.com/api/palettes/top?format=json&numResults=100&resultOffset=…`
in increasing offset order, concatenates the pages, lowercases the hex strings, and drops
only (a) palettes with fewer than 5 colours and (b) exact whole-palette duplicates -- it does
not re-sort by any vote/heart/view count. Array position is therefore the API's `top`-endpoint
order, preserved verbatim; the README's "top color palettes" phrase is packaging metadata, not
the ordering proof. The README is dated "Last updated Oct 14 2018" -- the snapshot is
historical, not live, but it is the only fetchable numeric-order corpus found for palettes in
this session (research/81 already ruled out live COLOURlovers, Coolors, Color Hunt, and Adobe
Color as not fetchable).

No numeric vote/heart/view count is exposed in this JSON (unlike the dead COLOURlovers API's
`numVotes`/`numHearts`/`numViews` fields) -- only rank order survives. Rank Value in the
provenance file is therefore the 1-indexed array position, per the brief's fallback
instruction #2 ("order = popularity rank").

No palette in this corpus carries a title/name field (the JSON is `[[hex,hex,hex,hex,hex],
...]` only, no metadata) -- Display Name below is mechanically derived from hue/lightness
(formula documented per-row below), not transcribed from source, since research/80 SS2B's
"source palette's title if present" does not apply to this source.

## Mechanical admissibility filter (applied in popularity order, first failure wins)

- (a) contains a colour usable as Foreground/Primary with >=7:1 against the palette's
  lightest colour OR against #FFFFFF
- (b) at most ONE saturated hue (HSL S>40% and 25%<L<75%) among the 5 source colours
- (c) if a saturated hue exists, its hue is NOT 200-230 deg with S>60% (default-blue slop,
  research/68)
- (d) after the mapping below, every manifest-required On-X pair (On Primary/Primary, On
  Secondary/Secondary, On Accent/Accent if an accent exists, On Muted/Muted) plus
  Foreground/Background reaches >=4.5:1, computed with
  `skill/document-design-intelligence/scripts/lib/color.py:contrast_ratio` (imported
  read-only, not modified)

Mapping (pre-registered, applied identically to every candidate):

- darkest of the 5 source hexes (by HSL lightness) -> Primary and Foreground
- lightest of the 5 -> Background; if its HSL lightness < 90, Background is instead #FFFFFF
  (derived, recorded per row below) -- the source lightest colour is still excluded from the
  remaining pool either way (it is the lightest role, not reusable as Secondary/Muted)
- the one saturated colour, if any -> Accent; zero saturated colours -> no Accent (left
  blank, matching the `lib-carbon-mono` / `lib-radix-burgundy` precedent in the authority
  sibling batch, which also ships accent-less rows rather than inventing a hue)
- of the remaining source colours (5 minus darkest, lightest, accent), the one at the
  midpoint of their HSL-lightness order -> Secondary; if only one colour remains it is
  Secondary; if none remain, Secondary falls back to the darkest colour (`mono-ink`
  precedent, where Primary and Secondary can be the same ink). **As actually applied (fix
  5)**: with 3 remaining, the true median (middle by HSL L) is Secondary. With 2 remaining
  (always the case in accent-bearing rows), Secondary is the **lighter** of the two -- an
  "upper median" reading that was never spelled out in the pre-registration text; ties in
  HSL L are broken by source order (affects rank 49's secondary vs muted split, see rank-75
  log entry note below for the analogous tie in rule (a)).
- Muted = the **lightest non-background tint** among the source colours still unused after
  Primary/Foreground, Background, Accent and Secondary are assigned; or, if no such colour
  remains (either because none is left, or the only one left is not a light tint), Muted is
  derived as #F2F2F2 (the synthetic light-neutral constant already used by `mono-ink`,
  `brand-accent-print`, `print-neutral`, `cv-harvard`, `cv-europass`, `cv-editorial` in the
  base library). **Rules applied that were not pre-registered**: the pre-registration text
  said only "any source colour still unused -> Muted", which is ambiguous whenever 2 source
  colours are left unused (every accent-less row leaves exactly 2 after Secondary is taken).
  The rule now stated -- take the lighter of the 2, and fall back to #F2F2F2 only when the
  sole remaining colour is not itself a light tint -- is the corrected, actually-intended
  rule; the original run instead kept "the first unused colour in source order" for those
  rows, which silently produced a **dark** Muted (fails as a panel-tint) in 7 of the 15 rows.
  This correction changes Muted (and its derived On Muted) in `lib-cl-r6-orange`,
  `lib-cl-r13-lime`, `lib-cl-r14-red`, `lib-cl-r21-red`, `lib-cl-r49-orange`,
  `lib-cl-r60-neutral`, `lib-cl-r116-red`, `lib-cl-r121-neutral` and `lib-cl-r134-neutral`
  relative to the original (unaudited) run; it leaves `lib-cl-r33-neutral`, `lib-cl-r65-neutral`,
  `lib-cl-r90-neutral`, `lib-cl-r108-red`, `lib-cl-r124-neutral` and `lib-cl-r136-neutral`
  unchanged because their original leftover pick was already the lighter/only tint.
- On-X = whichever of #FFFFFF or the palette's darkest (Foreground) colour has the higher
  `contrast_ratio` against that role's colour (mirrors `color.py`'s own `on_color` logic)
- Rule Hair fixed at #CCCCCC -- the constant every base-library palette without a real
  design-system border token already uses (`mono-ink`, `brand-accent-print`, `cv-harvard`,
  `cv-europass`), since a bare 5-hex source palette carries no separate border-token scale to
  transcribe. Rule Strong = Foreground. Rule Brand = Accent where an accent exists; blank
  otherwise. **Corrected (fix 4)**: accent-less precedent in the base library is *not*
  unanimous -- `mono-ink`, `lib-carbon-mono` and `lib-radix-burgundy` set Rule Brand =
  Primary when there is no accent, while `cv-dach-formal` and `deck-high-contrast` leave it
  blank. This batch leaves Rule Brand blank for its accent-less rows, matching the
  blank-precedent minority, not majority precedent; the earlier "matches every row with no
  exception" claim was false.
- Text-Safe Roles always includes `foreground;primary` (Primary/Foreground always clears
  4.5:1 against Background here because filter (a) already requires >=7:1). **Corrected
  (fix 1/2)**: Secondary and Accent are each added to Text-Safe Roles independently, only if
  `contrast_ratio(role, Background) >= 4.5` -- the same rule `make_brand_kit.derive_palette_row`
  uses for its own Text-Safe/Fill-Only split. The original evidence claimed Secondary was
  *always* Text-Safe; that was true only for `make_brand_kit`'s own light-ink secondaries and
  was never actually checked here. 11 of the (previous) 15 rows had Secondary below 4.5:1
  against Background (as low as 1.21:1) and are Fill-Only for Secondary in the corrected
  data; see the per-row tables below for the exact ratio in every row. Fill-Only Roles is
  always at least `muted`, plus `secondary` and/or `accent` whichever fails the 4.5:1 test.
  Category Marker Roles is left blank for all 15 rows (in the authority batch it is only ever
  used by the two deck-specific dark-theme rows; these are generic, not deck-specific,
  palettes).

## Source palettes in popularity order (all 137 processed; stopped once 15 were admitted)

| Rank | Source hexes | Result | Reason |
|---|---|---|---|
| 1 | `#69d2e7 #a7dbd8 #e0e4cc #f38630 #fa6900` | REJECT | (a) no colour reaches 7:1 vs lightest (2.28:1) or vs #FFFFFF (2.96:1) |
| 2 | `#fe4365 #fc9d9a #f9cdad #c8c8a9 #83af9b` | REJECT | (a) no colour reaches 7:1 vs lightest (1.68:1) or vs #FFFFFF (2.45:1) |
| 3 | `#ecd078 #d95b43 #c02942 #542437 #53777a` | REJECT | (b) 3 saturated hues (S>40%,25%<L<75%): ['#ecd078', '#d95b43', '#c02942'] |
| 4 | `#556270 #4ecdc4 #c7f464 #ff6b6b #c44d58` | REJECT | (a) no colour reaches 7:1 vs lightest (2.25:1) or vs #FFFFFF (6.24:1) |
| 5 | `#774f38 #e08e79 #f1d4af #ece5ce #c5e0dc` | REJECT | (d) On-X contrast below 4.5:1: {'On Accent/Accent': 2.8091474592259282} |
| 6 | `#e8ddcb #cdb380 #036564 #033649 #031634` | ADMIT | passes (a)(b)(c)(d) |
| 7 | `#490a3d #bd1550 #e97f02 #f8ca00 #8a9b0f` | REJECT | (b) 4 saturated hues (S>40%,25%<L<75%): ['#bd1550', '#e97f02', '#f8ca00', '#8a9b0f'] |
| 8 | `#594f4f #547980 #45ada8 #9de0ad #e5fcc2` | REJECT | (b) 2 saturated hues (S>40%,25%<L<75%): ['#45ada8', '#9de0ad'] |
| 9 | `#00a0b0 #6a4a3c #cc333f #eb6841 #edc951` | REJECT | (b) 4 saturated hues (S>40%,25%<L<75%): ['#00a0b0', '#cc333f', '#eb6841', '#edc951'] |
| 10 | `#e94e77 #d68189 #c6a49a #c6e5d9 #f4ead5` | REJECT | (a) no colour reaches 7:1 vs lightest (3.02:1) or vs #FFFFFF (3.61:1) |
| 11 | `#3fb8af #7fc7af #dad8a7 #ff9e9d #ff3d7f` | REJECT | (a) no colour reaches 7:1 vs lightest (1.22:1) or vs #FFFFFF (2.42:1) |
| 12 | `#d9ceb2 #948c75 #d5ded9 #7a6a53 #99b2b7` | REJECT | (a) no colour reaches 7:1 vs lightest (3.81:1) or vs #FFFFFF (5.23:1) |
| 13 | `#ffffff #cbe86b #f2e9e1 #1c140d #cbe86b` | ADMIT | passes (a)(b)(c)(d) -- **corrected (fix 7)**: the original run rejected this rank for "duplicate hex within source palette", a rule that is not one of the pre-registered (a)-(d) and is not the package's own dedupe either (which drops whole duplicate palettes, and this one was kept). Read literally, (b) ("at most ONE saturated hue") passes here: the two `#cbe86b` entries are the same hue, counted once. With the duplicate collapsed to a single usable colour, this palette admits: Primary/Foreground/Rule Strong `#1c140d`, Background `#ffffff` (the source's own lightest, transcribed), Secondary `#f2e9e1` (the sole non-duplicate leftover), Accent/Rule Brand `#cbe86b` (hue 74 deg, S 73%, L 67%), Muted derived `#F2F2F2` (the duplicate leaves no second leftover colour for Muted, so the fallback triggers on first use in this batch). Pre-registration ranks the admitted set by first-15-admitted-in-order, so admitting rank 13 pushes what would otherwise have been the 15th admission (rank 137) out of the batch; rank 137 is dropped, not re-admitted elsewhere. |
| 14 | `#efffcd #dce9be #555152 #2e2633 #99173c` | ADMIT | passes (a)(b)(c)(d) |
| 15 | `#343838 #005f6b #008c9e #00b4cc #00dffc` | REJECT | (b) 3 saturated hues (S>40%,25%<L<75%): ['#008c9e', '#00b4cc', '#00dffc'] |
| 16 | `#413e4a #73626e #b38184 #f0b49e #f7e4be` | REJECT | (d) On-X contrast below 4.5:1: {'On Secondary/Secondary': 3.2863682414414126} |
| 17 | `#ff4e50 #fc913a #f9d423 #ede574 #e1f5c4` | REJECT | (a) no colour reaches 7:1 vs lightest (1.25:1) or vs #FFFFFF (1.45:1) |
| 18 | `#99b898 #fecea8 #ff847c #e84a5f #2a363b` | REJECT | (b) 2 saturated hues (S>40%,25%<L<75%): ['#ff847c', '#e84a5f'] |
| 19 | `#655643 #80bca3 #f6f7bd #e6ac27 #bf4d28` | REJECT | (b) 2 saturated hues (S>40%,25%<L<75%): ['#e6ac27', '#bf4d28'] |
| 20 | `#00a8c6 #40c0cb #f9f2e7 #aee239 #8fbe00` | REJECT | (a) no colour reaches 7:1 vs lightest (1.98:1) or vs #FFFFFF (2.20:1) |
| 21 | `#351330 #424254 #64908a #e8caa4 #cc2a41` | ADMIT | passes (a)(b)(c)(d) |
| 22 | `#554236 #f77825 #d3ce3d #f1efa5 #60b99a` | REJECT | (b) 2 saturated hues (S>40%,25%<L<75%): ['#f77825', '#d3ce3d'] |
| 23 | `#5d4157 #838689 #a8caba #cad7b2 #ebe3aa` | REJECT | (d) On-X contrast below 4.5:1: {'On Muted/Muted': 3.66087957819156} |
| 24 | `#8c2318 #5e8c6a #88a65e #bfb35a #f2c45a` | REJECT | (b) 3 saturated hues (S>40%,25%<L<75%): ['#8c2318', '#bfb35a', '#f2c45a'] |
| 25 | `#fad089 #ff9c5b #f5634a #ed303c #3b8183` | REJECT | (a) no colour reaches 7:1 vs lightest (3.10:1) or vs #FFFFFF (4.51:1) |
| 26 | `#ff4242 #f4fad2 #d4ee5e #e1edb9 #f0f2eb` | REJECT | (a) no colour reaches 7:1 vs lightest (3.05:1) or vs #FFFFFF (3.44:1) |
| 27 | `#f8b195 #f67280 #c06c84 #6c5b7b #355c7d` | REJECT | (b) 2 saturated hues (S>40%,25%<L<75%): ['#f67280', '#355c7d'] |
| 28 | `#d1e751 #ffffff #000000 #4dbce9 #26ade4` | REJECT | (b) 3 saturated hues (S>40%,25%<L<75%): ['#d1e751', '#4dbce9', '#26ade4'] |
| 29 | `#1b676b #519548 #88c425 #bef202 #eafde6` | REJECT | (a) no colour reaches 7:1 vs lightest (6.16:1) or vs #FFFFFF (6.56:1) |
| 30 | `#5e412f #fcebb6 #78c0a8 #f07818 #f0a830` | REJECT | (b) 2 saturated hues (S>40%,25%<L<75%): ['#f07818', '#f0a830'] |
| 31 | `#bcbdac #cfbe27 #f27435 #f02475 #3b2d38` | REJECT | (b) 3 saturated hues (S>40%,25%<L<75%): ['#cfbe27', '#f27435', '#f02475'] |
| 32 | `#452632 #91204d #e4844a #e8bf56 #e2f7ce` | REJECT | (b) 3 saturated hues (S>40%,25%<L<75%): ['#91204d', '#e4844a', '#e8bf56'] |
| 33 | `#eee6ab #c5bc8e #696758 #45484b #36393b` | ADMIT | passes (a)(b)(c)(d) |
| 34 | `#f0d8a8 #3d1c00 #86b8b1 #f2d694 #fa2a00` | REJECT | (d) On-X contrast below 4.5:1: {'On Accent/Accent': 3.9544883970709677} |
| 35 | `#2a044a #0b2e59 #0d6759 #7ab317 #a0c55f` | REJECT | (b) 2 saturated hues (S>40%,25%<L<75%): ['#7ab317', '#a0c55f'] |
| 36 | `#f04155 #ff823a #f2f26f #fff7bd #95cfb7` | REJECT | (a) no colour reaches 7:1 vs lightest (3.45:1) or vs #FFFFFF (3.76:1) |
| 37 | `#b9d7d9 #668284 #2a2829 #493736 #7b3b3b` | REJECT | (d) On-X contrast below 4.5:1: {'On Muted/Muted': 4.124766377465286} |
| 38 | `#bbbb88 #ccc68d #eedd99 #eec290 #eeaa88` | REJECT | (a) no colour reaches 7:1 vs lightest (1.46:1) or vs #FFFFFF (1.99:1) |
| 39 | `#b3cc57 #ecf081 #ffbe40 #ef746f #ab3e5b` | REJECT | (a) no colour reaches 7:1 vs lightest (4.86:1) or vs #FFFFFF (5.88:1) |
| 40 | `#a3a948 #edb92e #f85931 #ce1836 #009989` | REJECT | (a) no colour reaches 7:1 vs lightest (1.09:1) or vs #FFFFFF (3.55:1) |
| 41 | `#300030 #480048 #601848 #c04848 #f07241` | REJECT | (b) 2 saturated hues (S>40%,25%<L<75%): ['#c04848', '#f07241'] |
| 42 | `#67917a #170409 #b8af03 #ccbf82 #e33258` | REJECT | (b) 3 saturated hues (S>40%,25%<L<75%): ['#b8af03', '#ccbf82', '#e33258'] |
| 43 | `#aab3ab #c4cbb7 #ebefc9 #eee0b7 #e8caaf` | REJECT | (a) no colour reaches 7:1 vs lightest (1.82:1) or vs #FFFFFF (2.15:1) |
| 44 | `#e8d5b7 #0e2430 #fc3a51 #f5b349 #e8d5b9` | REJECT | (b) 2 saturated hues (S>40%,25%<L<75%): ['#fc3a51', '#f5b349'] |
| 45 | `#ab526b #bca297 #c5ceae #f0e2a4 #f4ebc3` | REJECT | (a) no colour reaches 7:1 vs lightest (4.22:1) or vs #FFFFFF (5.06:1) |
| 46 | `#607848 #789048 #c0d860 #f0f0d8 #604848` | REJECT | (d) On-X contrast below 4.5:1: {'On Secondary/Secondary': 3.5705217404581022} |
| 47 | `#b6d8c0 #c8d9bf #dadabd #ecdbbc #fedcba` | REJECT | (a) no colour reaches 7:1 vs lightest (1.19:1) or vs #FFFFFF (1.55:1) |
| 48 | `#a8e6ce #dcedc2 #ffd3b5 #ffaaa6 #ff8c94` | REJECT | (a) no colour reaches 7:1 vs lightest (1.62:1) or vs #FFFFFF (2.23:1) |
| 49 | `#3e4147 #fffedf #dfba69 #5a2e2e #2a2c31` | ADMIT | passes (a)(b)(c)(d) |
| 50 | `#fc354c #29221f #13747d #0abfbc #fcf7c5` | REJECT | (b) 3 saturated hues (S>40%,25%<L<75%): ['#fc354c', '#13747d', '#0abfbc'] |
| 51 | `#cc0c39 #e6781e #c8cf02 #f8fcc1 #1693a7` | REJECT | (a) no colour reaches 7:1 vs lightest (3.41:1) or vs #FFFFFF (3.64:1) |
| 52 | `#1c2130 #028f76 #b3e099 #ffeaad #d14334` | REJECT | (b) 3 saturated hues (S>40%,25%<L<75%): ['#028f76', '#b3e099', '#d14334'] |
| 53 | `#a7c5bd #e5ddcb #eb7b59 #cf4647 #524656` | REJECT | (b) 2 saturated hues (S>40%,25%<L<75%): ['#eb7b59', '#cf4647'] |
| 54 | `#dad6ca #1bb0ce #4f8699 #6a5e72 #563444` | REJECT | (d) On-X contrast below 4.5:1: {'On Secondary/Secondary': 4.03654157225894, 'On Accent/Accent': 4.135287755090164} |
| 55 | `#5c323e #a82743 #e15e32 #c0d23e #e5f04c` | REJECT | (b) 4 saturated hues (S>40%,25%<L<75%): ['#a82743', '#e15e32', '#c0d23e', '#e5f04c'] |
| 56 | `#edebe6 #d6e1c7 #94c7b6 #403b33 #d3643b` | REJECT | (d) On-X contrast below 4.5:1: {'On Accent/Accent': 3.7130034128665033} |
| 57 | `#fdf1cc #c6d6b8 #987f69 #e3ad40 #fcd036` | REJECT | (a) no colour reaches 7:1 vs lightest (3.34:1) or vs #FFFFFF (3.77:1) |
| 58 | `#230f2b #f21d41 #ebebbc #bce3c5 #82b3ae` | REJECT | (d) On-X contrast below 4.5:1: {'On Accent/Accent': 4.2799177848496885} |
| 59 | `#b9d3b0 #81bda4 #b28774 #f88f79 #f6aa93` | REJECT | (a) no colour reaches 7:1 vs lightest (1.68:1) or vs #FFFFFF (3.18:1) |
| 60 | `#3a111c #574951 #83988e #bcdea5 #e6f9bc` | ADMIT | passes (a)(b)(c)(d) |
| 61 | `#5e3929 #cd8c52 #b7d1a3 #dee8be #fcf7d3` | REJECT | (d) On-X contrast below 4.5:1: {'On Accent/Accent': 3.5681615416794807} |
| 62 | `#1c0113 #6b0103 #a30006 #c21a01 #f03c02` | REJECT | (b) 3 saturated hues (S>40%,25%<L<75%): ['#a30006', '#c21a01', '#f03c02'] |
| 63 | `#000000 #9f111b #b11623 #292c37 #cccccc` | REJECT | (b) 2 saturated hues (S>40%,25%<L<75%): ['#9f111b', '#b11623'] |
| 64 | `#382f32 #ffeaf2 #fcd9e5 #fbc5d8 #f1396d` | REJECT | (d) On-X contrast below 4.5:1: {'On Accent/Accent': 3.786355250039913} |
| 65 | `#e3dfba #c8d6bf #93ccc6 #6cbdb5 #1a1f1e` | ADMIT | passes (a)(b)(c)(d) |
| 66 | `#f6f6f6 #e8e8e8 #333333 #990100 #b90504` | REJECT | (b) 2 saturated hues (S>40%,25%<L<75%): ['#990100', '#b90504'] |
| 67 | `#1b325f #9cc4e4 #e9f2f9 #3a89c9 #f26c4f` | REJECT | (b) 2 saturated hues (S>40%,25%<L<75%): ['#3a89c9', '#f26c4f'] |
| 68 | `#a1dbb2 #fee5ad #faca66 #f7a541 #f45d4c` | REJECT | (a) no colour reaches 7:1 vs lightest (1.63:1) or vs #FFFFFF (2.02:1) |
| 69 | `#c1b398 #605951 #fbeec2 #61a6ab #accec0` | REJECT | (a) no colour reaches 7:1 vs lightest (5.95:1) or vs #FFFFFF (6.90:1) |
| 70 | `#5e9fa3 #dcd1b4 #fab87f #f87e7b #b05574` | REJECT | (a) no colour reaches 7:1 vs lightest (1.98:1) or vs #FFFFFF (3.02:1) |
| 71 | `#951f2b #f5f4d7 #e0dfb1 #a5a36c #535233` | REJECT | (d) On-X contrast below 4.5:1: {'On Muted/Muted': 3.0715814702081095} |
| 72 | `#8dccad #988864 #fea6a2 #f9d6ac #ffe9af` | REJECT | (a) no colour reaches 7:1 vs lightest (2.90:1) or vs #FFFFFF (3.48:1) |
| 73 | `#2d2d29 #215a6d #3ca2a2 #92c7a3 #dfece6` | REJECT | (b) 2 saturated hues (S>40%,25%<L<75%): ['#215a6d', '#3ca2a2'] |
| 74 | `#413d3d #040004 #c8ff00 #fa023c #4b000f` | REJECT | (b) 2 saturated hues (S>40%,25%<L<75%): ['#c8ff00', '#fa023c'] |
| 75 | `#eff3cd #b2d5ba #61ada0 #248f8d #605063` | REJECT | **corrected (fix 6)**: (d) On-X below 4.5: On Primary 3.90, On Secondary 2.63, Fg/Bg 3.90, On Muted 2.43, On Accent 3.90 -- outcome (REJECT) is unchanged. Rule (a) as originally logged is wrong: `#605063` vs `#FFFFFF` = 7.43:1, so (a) actually **passes**; the original log tested (a) only against the HSL-darkest colour by construction, and `#248f8d` and `#605063` tie at HSL L 35.1, with the first-in-source-order colour (`#248f8d`) winning that comparison and being reported as "the" darkest even though `#605063` also qualifies and is in fact the true Foreground/Primary candidate once the tie is broken toward source order. Because rule (d) fails regardless, the admit/reject outcome does not change. |
| 76 | `#ffefd3 #fffee4 #d0ecea #9fd6d2 #8b7a5e` | REJECT | (a) no colour reaches 7:1 vs lightest (4.07:1) or vs #FFFFFF (4.16:1) |
| 77 | `#cfffdd #b4dec1 #5c5863 #a85163 #ff1f4c` | REJECT | (a) no colour reaches 7:1 vs lightest (6.27:1) or vs #FFFFFF (6.93:1) |
| 78 | `#9dc9ac #fffec7 #f56218 #ff9d2e #919167` | REJECT | (a) no colour reaches 7:1 vs lightest (3.14:1) or vs #FFFFFF (3.26:1) |
| 79 | `#4e395d #827085 #8ebe94 #ccfc8e #dc5b3e` | REJECT | (d) On-X contrast below 4.5:1: {'On Accent/Accent': 3.7439007399188813} |
| 80 | `#a8a7a7 #cc527a #e8175d #474747 #363636` | REJECT | (b) 2 saturated hues (S>40%,25%<L<75%): ['#cc527a', '#e8175d'] |
| 81 | `#f8edd1 #d88a8a #474843 #9d9d93 #c5cfc6` | REJECT | (d) On-X contrast below 4.5:1: {'On Muted/Muted': 3.373468703919497, 'On Accent/Accent': 3.480875338889614} |
| 82 | `#046d8b #309292 #2fb8ac #93a42a #ecbe13` | REJECT | (a) no colour reaches 7:1 vs lightest (3.35:1) or vs #FFFFFF (5.89:1) |
| 83 | `#f38a8a #55443d #a0cab5 #cde9ca #f1edd0` | REJECT | (d) On-X contrast below 4.5:1: {'On Accent/Accent': 3.864658873936465} |
| 84 | `#a70267 #f10c49 #fb6b41 #f6d86b #339194` | REJECT | (b) 5 saturated hues (S>40%,25%<L<75%): ['#a70267', '#f10c49', '#fb6b41', '#f6d86b', '#339194'] |
| 85 | `#ff003c #ff8a00 #fabe28 #88c100 #00c176` | REJECT | (a) no colour reaches 7:1 vs lightest (1.29:1) or vs #FFFFFF (2.17:1) |
| 86 | `#ffedbf #f7803c #f54828 #2e0d23 #f8e4c1` | REJECT | (b) 2 saturated hues (S>40%,25%<L<75%): ['#f7803c', '#f54828'] |
| 87 | `#4e4d4a #353432 #94ba65 #2790b0 #2b4e72` | REJECT | (b) 2 saturated hues (S>40%,25%<L<75%): ['#2790b0', '#2b4e72'] |
| 88 | `#0ca5b0 #4e3f30 #fefeeb #f8f4e4 #a5b3aa` | REJECT | (d) On-X contrast below 4.5:1: {'On Accent/Accent': 3.3810771553948413} |
| 89 | `#4d3b3b #de6262 #ffb88c #ffd0b3 #f5e0d3` | REJECT | (d) On-X contrast below 4.5:1: {'On Accent/Accent': 3.482956470658038} |
| 90 | `#fffbb7 #a6f6af #66b6ab #5b7c8d #4f2958` | ADMIT | passes (a)(b)(c)(d) |
| 91 | `#edf6ee #d1c089 #b3204d #412e28 #151101` | REJECT | (b) 2 saturated hues (S>40%,25%<L<75%): ['#d1c089', '#b3204d'] |
| 92 | `#9d7e79 #ccac95 #9a947c #748b83 #5b756c` | REJECT | (a) no colour reaches 7:1 vs lightest (2.35:1) or vs #FFFFFF (4.99:1) |
| 93 | `#fcfef5 #e9ffe1 #cdcfb7 #d6e6c3 #fafbe3` | REJECT | (a) no colour reaches 7:1 vs lightest (1.56:1) or vs #FFFFFF (1.59:1) |
| 94 | `#9cddc8 #bfd8ad #ddd9ab #f7af63 #633d2e` | REJECT | (b) 2 saturated hues (S>40%,25%<L<75%): ['#9cddc8', '#f7af63'] |
| 95 | `#30261c #403831 #36544f #1f5f61 #0b8185` | REJECT | (b) 2 saturated hues (S>40%,25%<L<75%): ['#1f5f61', '#0b8185'] |
| 96 | `#aaff00 #ffaa00 #ff00aa #aa00ff #00aaff` | REJECT | (a) no colour reaches 7:1 vs lightest (2.08:1) or vs #FFFFFF (1.23:1) |
| 97 | `#d1313d #e5625c #f9bf76 #8eb2c5 #615375` | REJECT | (a) no colour reaches 7:1 vs lightest (4.24:1) or vs #FFFFFF (6.99:1) |
| 98 | `#ffe181 #eee9e5 #fad3b2 #ffba7f #ff9c97` | REJECT | (a) no colour reaches 7:1 vs lightest (1.38:1) or vs #FFFFFF (1.67:1) |
| 99 | `#73c8a9 #dee1b6 #e1b866 #bd5532 #373b44` | REJECT | (b) 3 saturated hues (S>40%,25%<L<75%): ['#73c8a9', '#e1b866', '#bd5532'] |
| 100 | `#805841 #dcf7f3 #fffcdd #ffd8d8 #f5a2a2` | REJECT | (a) no colour reaches 7:1 vs lightest (5.96:1) or vs #FFFFFF (6.19:1) |
| 101 | `#379f7a #78ae62 #bbb749 #e0fbac #1f1c0d` | REJECT | (b) 2 saturated hues (S>40%,25%<L<75%): ['#379f7a', '#bbb749'] |
| 102 | `#caff42 #ebf7f8 #d0e0eb #88abc2 #49708a` | REJECT | (a) no colour reaches 7:1 vs lightest (4.84:1) or vs #FFFFFF (5.29:1) |
| 103 | `#c2412d #d1aa34 #a7a844 #a46583 #5a1e4a` | REJECT | (b) 3 saturated hues (S>40%,25%<L<75%): ['#c2412d', '#d1aa34', '#a7a844'] |
| 104 | `#75616b #bfcff7 #dce4f7 #f8f3bf #d34017` | REJECT | (a) no colour reaches 7:1 vs lightest (4.48:1) or vs #FFFFFF (5.71:1) |
| 105 | `#111625 #341931 #571b3c #7a1e48 #9d2053` | REJECT | (b) 2 saturated hues (S>40%,25%<L<75%): ['#7a1e48', '#9d2053'] |
| 106 | `#82837e #94b053 #bdeb07 #bffa37 #e0e0e0` | REJECT | (a) no colour reaches 7:1 vs lightest (1.06:1) or vs #FFFFFF (1.40:1) |
| 107 | `#7e5686 #a5aad9 #e8f9a2 #f8a13f #ba3c3d` | REJECT | (a) no colour reaches 7:1 vs lightest (5.19:1) or vs #FFFFFF (5.89:1) |
| 108 | `#312736 #d4838f #d6abb1 #d9d9d9 #c4ffeb` | ADMIT | passes (a)(b)(c)(d) |
| 109 | `#395a4f #432330 #853c43 #f25c5e #ffa566` | REJECT | (b) 2 saturated hues (S>40%,25%<L<75%): ['#f25c5e', '#ffa566'] |
| 110 | `#fde6bd #a1c5ab #f4dd51 #d11e48 #632f53` | REJECT | (b) 2 saturated hues (S>40%,25%<L<75%): ['#f4dd51', '#d11e48'] |
| 111 | `#84b295 #eccf8d #bb8138 #ac2005 #2c1507` | REJECT | (b) 3 saturated hues (S>40%,25%<L<75%): ['#eccf8d', '#bb8138', '#ac2005'] |
| 112 | `#058789 #503d2e #d54b1a #e3a72f #f0ecc9` | REJECT | (b) 3 saturated hues (S>40%,25%<L<75%): ['#058789', '#d54b1a', '#e3a72f'] |
| 113 | `#6da67a #77b885 #86c28b #859987 #4a4857` | REJECT | (d) On-X contrast below 4.5:1: {'On Secondary/Secondary': 3.0418664549720225, 'On Muted/Muted': 3.1352187746337443} |
| 114 | `#bed6c7 #adc0b4 #8a7e66 #a79b83 #bbb2a1` | REJECT | (a) no colour reaches 7:1 vs lightest (2.59:1) or vs #FFFFFF (3.99:1) |
| 115 | `#261c21 #6e1e62 #b0254f #de4126 #eb9605` | REJECT | (b) 4 saturated hues (S>40%,25%<L<75%): ['#6e1e62', '#b0254f', '#de4126', '#eb9605'] |
| 116 | `#efd9b4 #d6a692 #a39081 #4d6160 #292522` | ADMIT | passes (a)(b)(c)(d) |
| 117 | `#e21b5a #9e0c39 #333333 #fbffe3 #83a300` | REJECT | (b) 3 saturated hues (S>40%,25%<L<75%): ['#e21b5a', '#9e0c39', '#83a300'] |
| 118 | `#f2e3c6 #ffc6a5 #e6324b #2b2b2b #353634` | REJECT | (d) On-X contrast below 4.5:1: {'On Accent/Accent': 4.266177216096234} |
| 119 | `#c75233 #c78933 #d6ceaa #79b5ac #5e2f46` | REJECT | (b) 2 saturated hues (S>40%,25%<L<75%): ['#c75233', '#c78933'] |
| 120 | `#793a57 #4d3339 #8c873e #d1c5a5 #a38a5f` | REJECT | (d) On-X contrast below 4.5:1: {'On Secondary/Secondary': 3.7166568850109005} |
| 121 | `#512b52 #635274 #7bb0a8 #a7dbab #e4f5b1` | ADMIT | passes (a)(b)(c)(d) |
| 122 | `#11644d #a0b046 #f2c94e #f78145 #f24e4e` | REJECT | (b) 4 saturated hues (S>40%,25%<L<75%): ['#a0b046', '#f2c94e', '#f78145', '#f24e4e'] |
| 123 | `#59b390 #f0ddaa #e47c5d #e32d40 #152b3c` | REJECT | (b) 2 saturated hues (S>40%,25%<L<75%): ['#e47c5d', '#e32d40'] |
| 124 | `#fdffd9 #fff0b8 #ffd6a3 #faad8e #142f30` | ADMIT | passes (a)(b)(c)(d) |
| 125 | `#b5ac01 #ecba09 #e86e1c #d41e45 #1b1521` | REJECT | (b) 4 saturated hues (S>40%,25%<L<75%): ['#b5ac01', '#ecba09', '#e86e1c', '#d41e45'] |
| 126 | `#c7fcd7 #d9d5a7 #d9ab91 #e6867a #ed4a6a` | REJECT | (a) no colour reaches 7:1 vs lightest (3.17:1) or vs #FFFFFF (3.63:1) |
| 127 | `#11766d #410936 #a40b54 #e46f0a #f0b300` | REJECT | (b) 4 saturated hues (S>40%,25%<L<75%): ['#11766d', '#a40b54', '#e46f0a', '#f0b300'] |
| 128 | `#595643 #4e6b66 #ed834e #ebcc6e #ebe1c5` | REJECT | (b) 2 saturated hues (S>40%,25%<L<75%): ['#ed834e', '#ebcc6e'] |
| 129 | `#f1396d #fd6081 #f3ffeb #acc95f #8f9924` | REJECT | (a) no colour reaches 7:1 vs lightest (3.01:1) or vs #FFFFFF (3.11:1) |
| 130 | `#331327 #991766 #d90f5a #f34739 #ff6e27` | REJECT | (b) 4 saturated hues (S>40%,25%<L<75%): ['#991766', '#d90f5a', '#f34739', '#ff6e27'] |
| 131 | `#efeecc #fe8b05 #fe0557 #400403 #0aabba` | REJECT | (b) 3 saturated hues (S>40%,25%<L<75%): ['#fe8b05', '#fe0557', '#0aabba'] |
| 132 | `#bf496a #b39c82 #b8c99d #f0d399 #595151` | REJECT | (d) On-X contrast below 4.5:1: {'On Secondary/Secondary': 4.366601890861444, 'On Muted/Muted': 2.9385407952375378} |
| 133 | `#b7cbbf #8c886f #f9a799 #f4bfad #f5dabd` | REJECT | (a) no colour reaches 7:1 vs lightest (2.67:1) or vs #FFFFFF (3.58:1) |
| 134 | `#ffb884 #f5df98 #fff8d4 #c0d1c2 #2e4347` | ADMIT | passes (a)(b)(c)(d) |
| 135 | `#e5eaa4 #a8c4a2 #69a5a4 #616382 #66245b` | REJECT | (d) On-X contrast below 4.5:1: {'On Secondary/Secondary': 3.819790663071899} |
| 136 | `#e0eff1 #7db4b5 #ffffff #680148 #000000` | ADMIT | passes (a)(b)(c)(d) |
| 137 | `#b1e6d1 #77b1a9 #3d7b80 #270a33 #451a3e` | DROPPED | passes (a)(b)(c)(d), same as the original run, but **fix 7 (Orchestrator ruling)**: pre-registration wins and rank 13 admits (see corrected row 13 above). Admitting rank 13 makes it the batch's 3rd admission, so the stop-at-15 rule now closes the batch one palette earlier and rank 137 -- originally the 15th and last admission -- falls outside the cut. It is not carried as a 16th row; the batch keeps exactly 15. |

**15 admitted (ranks 6, 13, 14, 21, 33, 49, 60, 65, 90, 108, 116, 121, 124, 134, 136), 122
rejected**, out of 137 source palettes processed (ranks 1-137 of the 992-entry corpus). Rank
137 passed the filter but is not in the admitted 15 (see its row above); it remains logged
here as a passing-but-excluded candidate, not a rejection.

## Admitted palettes: mapping + contrast ratios

### `lib-cl-r6-orange` -- CL-ranked #6, warm orange accent

Source (rank 6 of nice-color-palettes@4.0.0/1000.json): `#e8ddcb, #cdb380, #036564, #033649, #031634`

| Role | Hex | Derived? |
|---|---|---|
| Primary / Foreground | #031634 | transcribed (darkest source colour) |
| Background | #ffffff | derived -- lightest source colour HSL L<90, substituted #ffffff per mapping rule |
| Secondary | #036564 | transcribed (mid-lightness remaining colour) |
| Accent | #cdb380 | transcribed (sole saturated hue: 40 deg, S=44%, L=65%) |
| Muted | #f2f2f2 | corrected (fix 5/12) -- derived #F2F2F2; the only leftover source colour (#033649, HSL L 15) is not a light tint, so the fallback applies instead of keeping it as Muted |
| Rule Hair | #CCCCCC | derived (fixed constant, see mapping notes above) |

| Pair | Foreground | Background | Ratio | Result |
|---|---|---|---|---|
| On Primary / Primary | #ffffff | #031634 | 17.98:1 | OK |
| On Secondary / Secondary | #ffffff | #036564 | 6.89:1 | OK |
| On Accent / Accent | #031634 | #cdb380 | 8.86:1 | OK |
| Foreground / Background | #031634 | #ffffff | 17.98:1 | OK |
| On Muted / Muted | #031634 | #f2f2f2 | 16.06:1 | OK |
| Secondary / Background (Text-Safe test, fix 2) | #036564 | #ffffff | 6.89:1 | OK (Text-Safe) |

### `lib-cl-r13-lime` -- CL-ranked #13, warm lime accent

Source (rank 13 of nice-color-palettes@4.0.0/1000.json): `#ffffff, #cbe86b, #f2e9e1, #1c140d, #cbe86b (the source repeats #cbe86b)`

| Role | Hex | Derived? |
|---|---|---|
| Primary / Foreground | #1c140d | transcribed (darkest source colour) |
| Background | #ffffff | transcribed (the source own lightest colour, HSL L 100) |
| Secondary | #f2e9e1 | transcribed (the sole non-duplicate leftover colour) |
| Accent | #cbe86b | transcribed (sole saturated hue: 74 deg, S=73%, L=67%); the duplicate #cbe86b entry is the same hue and does not create a second saturated colour under rule (b) |
| Muted | #f2f2f2 | derived #F2F2F2 -- the duplicate hex leaves no second leftover colour available for Muted, so the fallback triggers on its first use in this batch |
| Rule Hair | #CCCCCC | derived (fixed constant, see mapping notes above) |

| Pair | Foreground | Background | Ratio | Result |
|---|---|---|---|---|
| On Primary / Primary | #ffffff | #1c140d | 18.18:1 | OK |
| On Secondary / Secondary | #1c140d | #f2e9e1 | 15.16:1 | OK |
| On Accent / Accent | #1c140d | #cbe86b | 13.24:1 | OK |
| Foreground / Background | #1c140d | #ffffff | 18.18:1 | OK |
| On Muted / Muted | #1c140d | #f2f2f2 | 16.24:1 | OK |
| Secondary / Background (Text-Safe test, fix 2) | #f2e9e1 | #ffffff | 1.20:1 | FAIL (Fill-Only) -- fix 1/2 |

### `lib-cl-r14-red` -- CL-ranked #14, warm red accent

Source (rank 14 of nice-color-palettes@4.0.0/1000.json): `#efffcd, #dce9be, #555152, #2e2633, #99173c`

| Role | Hex | Derived? |
|---|---|---|
| Primary / Foreground | #2e2633 | transcribed (darkest source colour) |
| Background | #efffcd | transcribed (lightest source colour, HSL L 90.2 >= 90) |
| Secondary | #dce9be | transcribed (mid-lightness remaining colour) |
| Accent | #99173c | transcribed (sole saturated hue: 343 deg, S=74%, L=35%) |
| Muted | #f2f2f2 | corrected (fix 5/12) -- derived #F2F2F2; the only leftover source colour (#555152, HSL L 33) is not a light tint |
| Rule Hair | #CCCCCC | derived (fixed constant, see mapping notes above) |

| Pair | Foreground | Background | Ratio | Result |
|---|---|---|---|---|
| On Primary / Primary | #ffffff | #2e2633 | 14.57:1 | OK |
| On Secondary / Secondary | #2e2633 | #dce9be | 11.41:1 | OK |
| On Accent / Accent | #ffffff | #99173c | 8.26:1 | OK |
| Foreground / Background | #2e2633 | #efffcd | 13.78:1 | OK |
| On Muted / Muted | #2e2633 | #f2f2f2 | 13.02:1 | OK |
| Secondary / Background (Text-Safe test, fix 2) | #dce9be | #efffcd | 1.21:1 | FAIL (Fill-Only) -- fix 1/2 |

### `lib-cl-r21-red` -- CL-ranked #21, warm red accent

Source (rank 21 of nice-color-palettes@4.0.0/1000.json): `#351330, #424254, #64908a, #e8caa4, #cc2a41`

| Role | Hex | Derived? |
|---|---|---|
| Primary / Foreground | #351330 | transcribed (darkest source colour) |
| Background | #ffffff | derived -- lightest source colour HSL L<90, substituted #ffffff per mapping rule |
| Secondary | #64908a | transcribed (mid-lightness remaining colour) |
| Accent | #cc2a41 | transcribed (sole saturated hue: 351 deg, S=66%, L=48%) |
| Muted | #f2f2f2 | corrected (fix 5/12) -- derived #F2F2F2; the only leftover source colour (#424254, HSL L 29) is not a light tint |
| Rule Hair | #CCCCCC | derived (fixed constant, see mapping notes above) |

| Pair | Foreground | Background | Ratio | Result |
|---|---|---|---|---|
| On Primary / Primary | #ffffff | #351330 | 16.31:1 | OK |
| On Secondary / Secondary | #351330 | #64908a | 4.58:1 | OK |
| On Accent / Accent | #ffffff | #cc2a41 | 5.28:1 | OK |
| Foreground / Background | #351330 | #ffffff | 16.31:1 | OK |
| On Muted / Muted | #351330 | #f2f2f2 | 14.57:1 | OK |
| Secondary / Background (Text-Safe test, fix 2) | #64908a | #ffffff | 3.56:1 | FAIL (Fill-Only) -- fix 1/2 |

### `lib-cl-r33-neutral` -- CL-ranked #33, mid-tone neutral

Source (rank 33 of nice-color-palettes@4.0.0/1000.json): `#eee6ab, #c5bc8e, #696758, #45484b, #36393b`

| Role | Hex | Derived? |
|---|---|---|
| Primary / Foreground | #36393b | transcribed (darkest source colour) |
| Background | #ffffff | derived -- lightest source colour HSL L<90, substituted #ffffff per mapping rule |
| Secondary | #696758 | transcribed (true median-by-lightness of the 3 remaining colours) |
| Accent | (none) | no source colour met S>40%/25%<L<75%; left blank, not invented |
| Muted | #c5bc8e | transcribed (the lighter of the 2 leftover colours, HSL L 66 vs 28 for #45484b) -- already the lightest-tint pick, unchanged by fix 5/12 |
| Rule Hair | #CCCCCC | derived (fixed constant, see mapping notes above) |

| Pair | Foreground | Background | Ratio | Result |
|---|---|---|---|---|
| On Primary / Primary | #ffffff | #36393b | 11.63:1 | OK |
| On Secondary / Secondary | #ffffff | #696758 | 5.70:1 | OK |
| On Accent / Accent | (blank) | (blank) | n/a | n/a (no accent) |
| Foreground / Background | #36393b | #ffffff | 11.63:1 | OK |
| On Muted / Muted | #36393b | #c5bc8e | 6.07:1 | OK |
| Secondary / Background (Text-Safe test, fix 2) | #696758 | #ffffff | 5.70:1 | OK (Text-Safe) |

### `lib-cl-r49-orange` -- CL-ranked #49, warm orange accent

Source (rank 49 of nice-color-palettes@4.0.0/1000.json): `#3e4147, #fffedf, #dfba69, #5a2e2e, #2a2c31`

| Role | Hex | Derived? |
|---|---|---|
| Primary / Foreground | #2a2c31 | transcribed (darkest source colour) |
| Background | #fffedf | transcribed (lightest source colour, HSL L 93.7 >= 90) |
| Secondary | #5a2e2e | transcribed (lighter of the 2 remaining colours: HSL L 26.7 vs 26.1 for #3e4147 -- a near-tie broken toward the lighter value) |
| Accent | #dfba69 | transcribed (sole saturated hue: 41 deg, S=65%, L=64%) |
| Muted | #f2f2f2 | corrected (fix 5/12) -- derived #F2F2F2; the only leftover source colour (#3e4147, HSL L 26) is not a light tint |
| Rule Hair | #CCCCCC | derived (fixed constant, see mapping notes above) |

| Pair | Foreground | Background | Ratio | Result |
|---|---|---|---|---|
| On Primary / Primary | #ffffff | #2a2c31 | 13.97:1 | OK |
| On Secondary / Secondary | #ffffff | #5a2e2e | 11.26:1 | OK |
| On Accent / Accent | #2a2c31 | #dfba69 | 7.56:1 | OK |
| Foreground / Background | #2a2c31 | #fffedf | 13.63:1 | OK |
| On Muted / Muted | #2a2c31 | #f2f2f2 | 12.48:1 | OK |
| Secondary / Background (Text-Safe test, fix 2) | #5a2e2e | #fffedf | 10.99:1 | OK (Text-Safe) |

### `lib-cl-r60-neutral` -- CL-ranked #60, mid-tone neutral

Source (rank 60 of nice-color-palettes@4.0.0/1000.json): `#3a111c, #574951, #83988e, #bcdea5, #e6f9bc`

| Role | Hex | Derived? |
|---|---|---|
| Primary / Foreground | #3a111c | transcribed (darkest source colour) |
| Background | #ffffff | derived -- lightest source colour HSL L<90, substituted #ffffff per mapping rule |
| Secondary | #83988e | transcribed (true median-by-lightness of the 3 remaining colours) |
| Accent | (none) | no source colour met S>40%/25%<L<75%; left blank, not invented |
| Muted | #bcdea5 | corrected (fix 5/12) -- the lighter of the 2 leftover colours (HSL L 76 vs 31 for #574951); the original run kept #574951 (first-in-source-order), a dark colour that is not a usable light-tint Muted on this row white background |
| Rule Hair | #CCCCCC | derived (fixed constant, see mapping notes above) |

| Pair | Foreground | Background | Ratio | Result |
|---|---|---|---|---|
| On Primary / Primary | #ffffff | #3a111c | 16.45:1 | OK |
| On Secondary / Secondary | #3a111c | #83988e | 5.36:1 | OK |
| On Accent / Accent | (blank) | (blank) | n/a | n/a (no accent) |
| Foreground / Background | #3a111c | #ffffff | 16.45:1 | OK |
| On Muted / Muted | #3a111c | #bcdea5 | 11.07:1 | OK |
| Secondary / Background (Text-Safe test, fix 2) | #83988e | #ffffff | 3.07:1 | FAIL (Fill-Only) -- fix 1/2 |

### `lib-cl-r65-neutral` -- CL-ranked #65, mid-tone neutral

Source (rank 65 of nice-color-palettes@4.0.0/1000.json): `#e3dfba, #c8d6bf, #93ccc6, #6cbdb5, #1a1f1e`

| Role | Hex | Derived? |
|---|---|---|
| Primary / Foreground | #1a1f1e | transcribed (darkest source colour) |
| Background | #ffffff | derived -- lightest source colour HSL L<90, substituted #ffffff per mapping rule |
| Secondary | #93ccc6 | transcribed (true median-by-lightness of the 3 remaining colours) |
| Accent | (none) | no source colour met S>40%/25%<L<75%; left blank, not invented |
| Muted | #c8d6bf | transcribed (the lighter of the 2 leftover colours, HSL L 79 vs 58 for #6cbdb5) -- already the lightest-tint pick, unchanged by fix 5/12 |
| Rule Hair | #CCCCCC | derived (fixed constant, see mapping notes above) |

| Pair | Foreground | Background | Ratio | Result |
|---|---|---|---|---|
| On Primary / Primary | #ffffff | #1a1f1e | 16.68:1 | OK |
| On Secondary / Secondary | #1a1f1e | #93ccc6 | 9.29:1 | OK |
| On Accent / Accent | (blank) | (blank) | n/a | n/a (no accent) |
| Foreground / Background | #1a1f1e | #ffffff | 16.68:1 | OK |
| On Muted / Muted | #1a1f1e | #c8d6bf | 10.99:1 | OK |
| Secondary / Background (Text-Safe test, fix 2) | #93ccc6 | #ffffff | 1.80:1 | FAIL (Fill-Only) -- fix 1/2 |

### `lib-cl-r90-neutral` -- CL-ranked #90, mid-tone neutral

Source (rank 90 of nice-color-palettes@4.0.0/1000.json): `#fffbb7, #a6f6af, #66b6ab, #5b7c8d, #4f2958`

| Role | Hex | Derived? |
|---|---|---|
| Primary / Foreground | #4f2958 | transcribed (darkest source colour) |
| Background | #ffffff | derived -- lightest source colour HSL L<90, substituted #ffffff per mapping rule |
| Secondary | #66b6ab | transcribed (true median-by-lightness of the 3 remaining colours) |
| Accent | (none) | no source colour met S>40%/25%<L<75%; left blank, not invented |
| Muted | #a6f6af | transcribed (the lighter of the 2 leftover colours, HSL L 81 vs 46 for #5b7c8d) -- already the lightest-tint pick, unchanged by fix 5/12 |
| Rule Hair | #CCCCCC | derived (fixed constant, see mapping notes above) |

| Pair | Foreground | Background | Ratio | Result |
|---|---|---|---|---|
| On Primary / Primary | #ffffff | #4f2958 | 11.73:1 | OK |
| On Secondary / Secondary | #4f2958 | #66b6ab | 4.94:1 | OK |
| On Accent / Accent | (blank) | (blank) | n/a | n/a (no accent) |
| Foreground / Background | #4f2958 | #ffffff | 11.73:1 | OK |
| On Muted / Muted | #4f2958 | #a6f6af | 9.17:1 | OK |
| Secondary / Background (Text-Safe test, fix 2) | #66b6ab | #ffffff | 2.37:1 | FAIL (Fill-Only) -- fix 1/2 |

### `lib-cl-r108-red` -- CL-ranked #108, warm red accent

Source (rank 108 of nice-color-palettes@4.0.0/1000.json): `#312736, #d4838f, #d6abb1, #d9d9d9, #c4ffeb`

| Role | Hex | Derived? |
|---|---|---|
| Primary / Foreground | #312736 | transcribed (darkest source colour) |
| Background | #ffffff | derived -- lightest source colour HSL L<90, substituted #ffffff per mapping rule |
| Secondary | #d9d9d9 | transcribed (lighter of the 2 remaining colours) |
| Accent | #d4838f | transcribed (sole saturated hue: 351 deg, S=49%, L=67%) |
| Muted | #d6abb1 | transcribed (the other of the 2 remaining colours, HSL L 76 -- already a light tint, unchanged by fix 5/12) |
| Rule Hair | #CCCCCC | derived (fixed constant, see mapping notes above) |

| Pair | Foreground | Background | Ratio | Result |
|---|---|---|---|---|
| On Primary / Primary | #ffffff | #312736 | 14.25:1 | OK |
| On Secondary / Secondary | #312736 | #d9d9d9 | 10.09:1 | OK |
| On Accent / Accent | #312736 | #d4838f | 5.05:1 | OK |
| Foreground / Background | #312736 | #ffffff | 14.25:1 | OK |
| On Muted / Muted | #312736 | #d6abb1 | 7.00:1 | OK |
| Secondary / Background (Text-Safe test, fix 2) | #d9d9d9 | #ffffff | 1.41:1 | FAIL (Fill-Only) -- fix 1/2 |

### `lib-cl-r116-red` -- CL-ranked #116, warm red accent

Source (rank 116 of nice-color-palettes@4.0.0/1000.json): `#efd9b4, #d6a692, #a39081, #4d6160, #292522`

| Role | Hex | Derived? |
|---|---|---|
| Primary / Foreground | #292522 | transcribed (darkest source colour) |
| Background | #ffffff | derived -- lightest source colour HSL L<90, substituted #ffffff per mapping rule |
| Secondary | #a39081 | transcribed (lighter of the 2 remaining colours) |
| Accent | #d6a692 | transcribed (sole saturated hue: 18 deg, S=45%, L=71%) |
| Muted | #f2f2f2 | corrected (fix 5/12) -- derived #F2F2F2; the only leftover source colour (#4d6160, HSL L 34) is not a light tint |
| Rule Hair | #CCCCCC | derived (fixed constant, see mapping notes above) |

| Pair | Foreground | Background | Ratio | Result |
|---|---|---|---|---|
| On Primary / Primary | #ffffff | #292522 | 15.20:1 | OK |
| On Secondary / Secondary | #292522 | #a39081 | 4.97:1 | OK |
| On Accent / Accent | #292522 | #d6a692 | 7.04:1 | OK |
| Foreground / Background | #292522 | #ffffff | 15.20:1 | OK |
| On Muted / Muted | #292522 | #f2f2f2 | 13.57:1 | OK |
| Secondary / Background (Text-Safe test, fix 2) | #a39081 | #ffffff | 3.06:1 | FAIL (Fill-Only) -- fix 1/2 |

### `lib-cl-r121-neutral` -- CL-ranked #121, mid-tone neutral

Source (rank 121 of nice-color-palettes@4.0.0/1000.json): `#512b52, #635274, #7bb0a8, #a7dbab, #e4f5b1`

| Role | Hex | Derived? |
|---|---|---|
| Primary / Foreground | #512b52 | transcribed (darkest source colour) |
| Background | #ffffff | derived -- lightest source colour HSL L<90, substituted #ffffff per mapping rule |
| Secondary | #7bb0a8 | transcribed (true median-by-lightness of the 3 remaining colours) |
| Accent | (none) | no source colour met S>40%/25%<L<75%; left blank, not invented |
| Muted | #a7dbab | corrected (fix 5/12) -- the lighter of the 2 leftover colours (HSL L 76 vs 39 for #635274); the original run kept #635274 (first-in-source-order), a dark colour that is not a usable light-tint Muted on this row white background |
| Rule Hair | #CCCCCC | derived (fixed constant, see mapping notes above) |

| Pair | Foreground | Background | Ratio | Result |
|---|---|---|---|---|
| On Primary / Primary | #ffffff | #512b52 | 11.56:1 | OK |
| On Secondary / Secondary | #512b52 | #7bb0a8 | 4.74:1 | OK |
| On Accent / Accent | (blank) | (blank) | n/a | n/a (no accent) |
| Foreground / Background | #512b52 | #ffffff | 11.56:1 | OK |
| On Muted / Muted | #512b52 | #a7dbab | 7.35:1 | OK |
| Secondary / Background (Text-Safe test, fix 2) | #7bb0a8 | #ffffff | 2.44:1 | FAIL (Fill-Only) -- fix 1/2 |

### `lib-cl-r124-neutral` -- CL-ranked #124, light neutral

Source (rank 124 of nice-color-palettes@4.0.0/1000.json): `#fdffd9, #fff0b8, #ffd6a3, #faad8e, #142f30`

| Role | Hex | Derived? |
|---|---|---|
| Primary / Foreground | #142f30 | transcribed (darkest source colour) |
| Background | #fdffd9 | transcribed (lightest source colour, HSL L 92.5 >= 90) |
| Secondary | #ffd6a3 | transcribed (true median-by-lightness of the 3 remaining colours) |
| Accent | (none) | no source colour met S>40%/25%<L<75%; left blank, not invented |
| Muted | #fff0b8 | transcribed (the lighter of the 2 leftover colours, HSL L 86 vs 77 for #faad8e) -- already the lightest-tint pick, unchanged by fix 5/12 |
| Rule Hair | #CCCCCC | derived (fixed constant, see mapping notes above) |

| Pair | Foreground | Background | Ratio | Result |
|---|---|---|---|---|
| On Primary / Primary | #ffffff | #142f30 | 14.20:1 | OK |
| On Secondary / Secondary | #142f30 | #ffd6a3 | 10.41:1 | OK |
| On Accent / Accent | (blank) | (blank) | n/a | n/a (no accent) |
| Foreground / Background | #142f30 | #fdffd9 | 13.85:1 | OK |
| On Muted / Muted | #142f30 | #fff0b8 | 12.45:1 | OK |
| Secondary / Background (Text-Safe test, fix 2) | #ffd6a3 | #fdffd9 | 1.33:1 | FAIL (Fill-Only) -- fix 1/2 |

### `lib-cl-r134-neutral` -- CL-ranked #134, light neutral

Source (rank 134 of nice-color-palettes@4.0.0/1000.json): `#ffb884, #f5df98, #fff8d4, #c0d1c2, #2e4347`

| Role | Hex | Derived? |
|---|---|---|
| Primary / Foreground | #2e4347 | transcribed (darkest source colour) |
| Background | #fff8d4 | transcribed (lightest source colour, HSL L 91.6 >= 90) |
| Secondary | #f5df98 | transcribed (true median-by-lightness of the 3 remaining colours) |
| Accent | (none) | no source colour met S>40%/25%<L<75%; left blank, not invented |
| Muted | #c0d1c2 | corrected (fix 5/12) -- the lighter of the 2 leftover colours (HSL L 79 vs 76 for #ffb884, a near-tie); the original run kept #ffb884 (first-in-source-order) instead of the marginally lighter tint |
| Rule Hair | #CCCCCC | derived (fixed constant, see mapping notes above) |

| Pair | Foreground | Background | Ratio | Result |
|---|---|---|---|---|
| On Primary / Primary | #ffffff | #2e4347 | 10.45:1 | OK |
| On Secondary / Secondary | #2e4347 | #f5df98 | 7.91:1 | OK |
| On Accent / Accent | (blank) | (blank) | n/a | n/a (no accent) |
| Foreground / Background | #2e4347 | #fff8d4 | 9.77:1 | OK |
| On Muted / Muted | #2e4347 | #c0d1c2 | 6.54:1 | OK |
| Secondary / Background (Text-Safe test, fix 2) | #f5df98 | #fff8d4 | 1.24:1 | FAIL (Fill-Only) -- fix 1/2 |

### `lib-cl-r136-neutral` -- CL-ranked #136, mid-tone neutral

Source (rank 136 of nice-color-palettes@4.0.0/1000.json): `#e0eff1, #7db4b5, #ffffff, #680148, #000000`

| Role | Hex | Derived? |
|---|---|---|
| Primary / Foreground | #000000 | transcribed (darkest source colour) |
| Background | #ffffff | transcribed (the source own lightest colour, HSL L 100) |
| Secondary | #7db4b5 | transcribed (true median-by-lightness of the 3 remaining colours) |
| Accent | (none) | no source colour met S>40%/25%<L<75%; left blank, not invented |
| Muted | #e0eff1 | transcribed (the lighter of the 2 leftover colours, HSL L 91 vs 21 for #680148) -- already the lightest-tint pick, unchanged by fix 5/12 |
| Rule Hair | #CCCCCC | derived (fixed constant, see mapping notes above) |

| Pair | Foreground | Background | Ratio | Result |
|---|---|---|---|---|
| On Primary / Primary | #ffffff | #000000 | 21.00:1 | OK |
| On Secondary / Secondary | #000000 | #7db4b5 | 9.07:1 | OK |
| On Accent / Accent | (blank) | (blank) | n/a | n/a (no accent) |
| Foreground / Background | #000000 | #ffffff | 21.00:1 | OK |
| On Muted / Muted | #000000 | #e0eff1 | 17.79:1 | OK |
| Secondary / Background (Text-Safe test, fix 2) | #7db4b5 | #ffffff | 2.32:1 | FAIL (Fill-Only) -- fix 1/2 |

## Notes

- All 15 rows pass every manifest-required On-X pair at >=4.5:1 and Foreground/Background at
  >=7:1; most clear 10:1+ in practice, a side effect of filter (a) itself always seeding a
  near-black or very-dark Primary/Foreground.
- 7 of 15 admitted palettes carry an Accent (ranks 6, 13, 14, 21, 49, 108, 116); the other 8
  have none, because no source colour in them met the S>40%/25%<L<75% saturated-hue test --
  these ship as accent-less palettes (Accent/On Accent left blank) rather than promoting a
  low-saturation or out-of-range tone to Accent, matching the `lib-carbon-mono` /
  `lib-radix-burgundy` precedent.
- No admitted palette's Accent falls in the 200-230 deg default-blue-slop range (rule c);
  the rejection log above shows rule (b) -- more than one saturated hue -- as the single most
  common rejection reason in this corpus slice, well ahead of (a), (c), or (d).
- **Corrected (fix 3)**: the palette identity (5 source hexes) is **not** transcribed exactly
  as fetched in every row. Only `lib-cl-r14-red` and `lib-cl-r49-orange` carry all 5 source
  hexes untouched. Every other row drops or substitutes at least one value: 10 of 15 rows
  substitute a derived `#ffffff` Background where the source's own lightest colour was under
  HSL L 90 (`lib-cl-r6-orange`, `lib-cl-r21-red`, `lib-cl-r33-neutral`, `lib-cl-r60-neutral`,
  `lib-cl-r65-neutral`, `lib-cl-r90-neutral`, `lib-cl-r108-red`, `lib-cl-r116-red`,
  `lib-cl-r121-neutral`, `lib-cl-r137` (dropped)); and 6 of the 15 admitted rows now substitute
  a derived `#F2F2F2` Muted where no leftover source colour was a usable light tint
  (`lib-cl-r6-orange`, `lib-cl-r13-lime`, `lib-cl-r14-red`, `lib-cl-r21-red`,
  `lib-cl-r49-orange`, `lib-cl-r116-red` -- six rows, see the per-row "Derived?" column above
  for the exact reason in each). Every "Derived?" column above states plainly whether each
  role's hex is transcribed or derived; the "transcribed exactly as fetched in every row"
  sentence from the original evidence is false and has been replaced by this row-accurate
  statement.
- **Corrected (fix 5, two-colour midpoint rule)**: whenever exactly 2 source colours remain
  after Primary/Foreground, Background and Accent are assigned (every accent-bearing row),
  Secondary is the *lighter* of the two, not a literal "midpoint" (there is no middle value of
  a 2-item set). This "upper median" reading was applied consistently across all 7 accent rows
  but was never written down in the pre-registration text; it is recorded here as the rule
  that was actually used.
