# rationale/typefaces.md

Hand-authored (T5 has no rationale generator in `research/load-base.py`; the loader only
derives `Safe Stack Availability` from `Safe Stack Fallback`). Entries below cover the four
rows added at A4 for the CV design directions in `research/69-cv-design-directions.md` and
`research/70-cv-type-and-colour.md`. Every other row's rationale is unchanged and not
repeated here.

### `source-serif-sans` -- Source Serif 4 + Source Sans 3

Direction 1 "Harvard Reverse-Chronological" (research/70 sec "Direction 1"). Source:
[adobe-fonts/source-serif README](https://github.com/adobe-fonts/source-serif) (fetched),
which states the family is "designed to complement Source Sans" -- a publisher-documented
companion pair, not an aggregator's guess. Both OFL-1.1, both on Google Fonts, hence
`Embedding Licence=installable`. Replaces research/69's original Lora/Open Sans option,
which had no fetchable pairing source. research/70 names two fallbacks, `Georgia (heading) /
Arial (body)`, per Butterick's [system-fonts
page](https://practicaltypography.com/system-fonts.html) (fetched); `Safe Stack Fallback` is
a single-value column (`research/09-library-schema.md` T5, one cell), so `Georgia` is
recorded as the one representative fallback (the heading-role family, since `Heading Family`
is the first-listed role on every T5 row) rather than inventing a `/`-joined value the loader
does not parse -- see the note below. Scale Key `cv-major-third` -- see `type-scales.md`.

### `pt-serif-sans` -- PT Serif + PT Sans

Direction 2 "DACH Tabellarisch" (research/70 sec "Direction 2"). Source:
[Typewolf's PT Serif page](https://www.typewolf.com/pt-serif) (fetched), "Suggested Font
Pairing -- PT Serif + PT Sans" -- a direct first-party pairing recommendation. Both OFL-1.1,
both cover Latin Extended (umlauts), which is the reason this pair rather than 69's original
Merriweather option (Typewolf's Merriweather page pairs it with FF Mark, not free/OFL).
research/70 names `Times New Roman / Arial`; `Times New Roman` recorded as the single
`Safe Stack Fallback` value, same heading-role convention as `source-serif-sans` above, both
OS-bundled either way. Scale Key `cv-major-third` (shared with Direction 1 by Manager
decision -- see the type-scales rationale for why only two new scale keys were authored
instead of one per direction).

### `ibm-plex-sans` -- IBM Plex Sans (single family)

Direction 3 "Europass-Compatible Multilingual" (research/70 sec "Direction 3"). Single
family, weight-differentiated, per Google Fonts Knowledge's companion article "Pairing
typefaces within a family & superfamily" (search-derived, corroborated in research/70),
which documents within-family pairing as a legitimate named strategy for multilingual
documents where accented glyphs must render consistently -- avoids importing a second
family purely for headings. Fallback `Arial` (OS-bundled, and the only fallback 70 names for
this direction, so no single-vs-compound question here). Scale Key `cv-major-third`.

### `fraunces-work-sans` -- Fraunces + Work Sans

Direction 4 "Editorial / Creative-Industry CV" (research/70 sec "Direction 4"; new
direction, not in research/69). Source: [Typewolf's Fraunces
page](https://www.typewolf.com/fraunces) (fetched) -- Fraunces is Typewolf's own
suggested-pairing subject, illustrated there with a real production pairing (Flask & Field,
Fraunces + DM Mono); [Typewolf's IBM Plex Sans
page](https://www.typewolf.com/ibm-plex-sans) (fetched) shows real creative-portfolio sites
(Andrea Arqués, Alyssa Martin) pairing a grotesque sans with an expressive serif, the same
structural pattern used here (Fraunces heading, Work Sans body). Both OFL-1.1. research/70
names `Georgia / Arial`; `Georgia` recorded as the single `Safe Stack Fallback` value, same
heading-role convention as `source-serif-sans`. Scale Key `cv-editorial-fourth` -- the one
direction using the Perfect Fourth (1.333) ratio instead of Major Third (1.25), per
research/70's own type-scale method section: Direction 4 carries no ATS point-size ceiling,
so a more expressive step is used.

### `Safe Stack Fallback` single-value note

`research/09-library-schema.md` T5 defines `Safe Stack Fallback` as one text cell, and
`research/load-base.py`'s `OS_BUNDLED` check does an exact-match lookup on that one string
(`fb = r["Safe Stack Fallback"].strip(); ... if fb in OS_BUNDLED`) -- it is not touched by
this task (out of A4's writable scope: scripts are not a draft CSV, generated output,
rationale file, or test). research/70 names two role-specific fallbacks per direction
(heading serif / body sans) for three of these four rows, which the column cannot hold as
two values without a loader change nobody authorized here. Each row therefore records the
**heading-role** fallback as the representative single value -- the same convention the
pre-existing two-family rows already use one column over is inverted here (`ofl-source-sans-
serif` and `ofl-roboto-slab` both record `Arial`, a body-role choice); heading-role was
picked instead because `Heading Family` is the first-listed role on every T5 row and because
it keeps each new row's fallback visibly tied to its more distinctive family (Georgia for a
serif heading, Times New Roman for a serif label). All four chosen fallbacks -- Georgia,
Times New Roman, Arial -- are OS-bundled on both Windows and macOS, so all four rows load as
`Safe Stack Availability=os-bundled` regardless of which role was picked. The body-role
fallback these rows do not carry (Arial, in three of the four cases) is not lost: it is the
`Safe Stack Fallback` already recorded on `safe-sans-arial`, an existing T5 row every CV
doctype's ATS-strict sibling already resolves to.
