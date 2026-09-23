# legacy-backfill notes

Per row: the citation relied on (file:line under research/ unless noted). `Retrieved`: none of research/19, 29-32, 57, 59, 69, 70 states a day-level retrieval date (19-notes says only 'September 2026'; 69/70 give none), so every row uses 2026-09-23, the date of those files and of the neighbouring provenance batches; it is an upper bound, not a stated retrieval date. `Fetch` follows the research wording; where 70's header says search-derived (USWDS, GOV.UK, Carbon) it is `search-corroborated` even though 70:29 says GOV.UK 'fetched'.

Convention rows cite nothing external; the note says what was checked.

| Table | Row Key | Class | Fetch | Citation relied on |
|---|---|---|---|---|
| palettes | mono-ink | convention | - | 32-notes.md:39: hand-authored, contrast ratios computed in-house, no external source cited |
| palettes | brand-accent-print | convention | - | 32-notes.md:70: hand-authored, contrast ratios computed in-house, no external source cited |
| palettes | print-neutral | convention | - | 32-notes.md:61: hand-authored, contrast ratios computed in-house, no external source cited |
| palettes | deck-high-contrast | convention | - | 32-notes.md:79: hand-authored, contrast ratios computed in-house, no external source cited |
| palettes | cv-harvard | authority | search-corroborated | 70-cv-type-and-colour.md:3 (USWDS search-derived, hex quoted from token tables), :13-21; rationale/palettes.md |
| palettes | cv-dach-formal | authority | search-corroborated | 70:3 lists GOV.UK as search-derived (70:29 says 'fetched'; the more conservative header wording is used); :29 |
| palettes | cv-europass | authority | search-corroborated | 70:3, :35-41 (link colour #1a65a6); same search-derived caveat |
| palettes | cv-editorial | authority | search-corroborated | 70:3 (Carbon direct fetch truncated, hexes corroborated via search only), :53 |
| typefaces | safe-sans-arial | convention | - | 19-notes.md:17-25, :37-53: availability grid verified against web sources (wps.com, Microsoft Q&A, Wikipedia, Debian wiki) but the notes never say which were fetched vs searched and give no per-cell citation; not upgraded |
| typefaces | safe-serif-times | convention | - | 19-notes.md:17-25, :37-53: availability grid verified against web sources (wps.com, Microsoft Q&A, Wikipedia, Debian wiki) but the notes never say which were fetched vs searched and give no per-cell citation; not upgraded |
| typefaces | safe-serif-georgia | convention | - | 19-notes.md:17-25, :37-53: availability grid verified against web sources (wps.com, Microsoft Q&A, Wikipedia, Debian wiki) but the notes never say which were fetched vs searched and give no per-cell citation; not upgraded |
| typefaces | safe-sans-deck | convention | - | 57-deck-projection-fix.md:18 (same Arial faces as safe-sans-arial, no new source) |
| typefaces | safe-sans-infographic | convention | - | 59-infographic-content.md:28 (Arial/Arial; size stated as CONVENTION) |
| typefaces | ofl-source-sans-serif | authority | fetched | 19-notes.md:165-205 (Source Sans 3 / Source Serif 4 files fetched, fsType=0); supports the licence/embedding claim, not the pairing choice |
| typefaces | ofl-plex-superfamily | authority | fetched | 19-notes.md:165-205 (IBM Plex Sans/Serif/Mono files fetched, fsType=0); supports the licence/embedding claim, not the pairing choice |
| typefaces | ofl-public-sans | authority | fetched | 19-notes.md:165-205 (Public Sans file fetched, fsType=0); supports the licence/embedding claim, not the pairing choice |
| typefaces | ofl-roboto-slab | authority | fetched | 19-notes.md:165-205 (Roboto Slab under apache/ path, Apache-2.0 LICENSE.txt 'confirmed by direct fetch'; Roboto file fetched); supports the licence/embedding claim, not the pairing choice |
| typefaces | source-serif-sans | authority | fetched | 70-cv-type-and-colour.md:15 (README: 'designed to complement Source Sans'); rationale/typefaces.md |
| typefaces | pt-serif-sans | authority | fetched | 70:25 (Typewolf 'Suggested Font Pairing - PT Serif + PT Sans'); rationale/typefaces.md |
| typefaces | ibm-plex-sans | convention | - | 70:3, :35: grounded on Google Fonts Knowledge 'Pairing typefaces within a family' - direct fetch returned only the page shell, corroborated by search snippet, and no URL is recorded in research; cannot cite without inventing a URL |
| typefaces | fraunces-work-sans | authority | fetched | 70:47 (Typewolf Fraunces page, Flask & Field example); rationale/typefaces.md |
| doc-styles | cv-restrained | convention | - | 31-notes.md:1-12: structural fields hand-authored from T2 needs; no source cited |
| doc-styles | cv-academic-plain | convention | - | 31-notes.md:1-12: structural fields hand-authored from T2 needs; no source cited |
| doc-styles | letter-restrained | convention | - | 31-notes.md:1-12: structural fields hand-authored from T2 needs; no source cited |
| doc-styles | letter-formal-grid | convention | - | 31-notes.md:1-12: structural fields hand-authored from T2 needs; no source cited |
| doc-styles | memo-plain | convention | - | 31-notes.md:1-12: structural fields hand-authored from T2 needs; no source cited |
| doc-styles | form-grid-underline | convention | - | 31-notes.md:1-12: structural fields hand-authored from T2 needs; no source cited |
| doc-styles | marketing-print-bold | convention | - | 31-notes.md:1-12: structural fields hand-authored from T2 needs; no source cited |
| doc-styles | infographic-bold | convention | - | 31-notes.md:1-12: structural fields hand-authored from T2 needs; no source cited |
| doc-styles | report-classic-serif | convention | - | 31-notes.md:1-12: structural fields hand-authored from T2 needs; no source cited |
| doc-styles | deck-bold-minimal | convention | - | 31-notes.md:1-12: structural fields hand-authored from T2 needs; no source cited |
| doc-styles | one-pager-tight | convention | - | 31-notes.md:1-12: structural fields hand-authored from T2 needs; no source cited |
| doc-styles | cv-harvard | authority | fetched | 69-cv-design-directions.md:10 (Butterick: generous margins, whitespace); rationale/doc-styles.md cv-harvard |
| doc-styles | cv-dach-tabular | authority | fetched | 69:34 (photo accepted, not mandatory) - covers only the photo element; the table grid itself rests on search-derived aggregators (69:32), not citable as authority |
| doc-styles | cv-europass | authority | fetched | 69:53 (language-proficiency table 'a real Europass structural element'); rationale/doc-styles.md cv-europass |
| doc-styles | cv-editorial | convention | - | rationale/doc-styles.md cv-editorial: cites only 70's own scope note (70:43-53), no external source |
| doc-reasoning | cv-ats-strict | convention | - | rationale/doc-reasoning.md: cites the schema's own worked example (09-library-schema.md:442-444) |
| doc-reasoning | cv-academic | convention | - | rationale/doc-reasoning.md: internal T1 reachability only |
| doc-reasoning | cover-letter-professional | convention | - | rationale/doc-reasoning.md: internal T1 reachability only |
| doc-reasoning | letter-formal | convention | - | rationale/doc-reasoning.md: no closed condition, no source |
| doc-reasoning | memo-internal | convention | - | rationale/doc-reasoning.md: cites schema worked example only |
| doc-reasoning | form-handfilled | convention | - | rationale/doc-reasoning.md: T9 wiring, flagged as gap in 29-notes.md; no source |
| doc-reasoning | print-marketing | convention | - | rationale/doc-reasoning.md: T1/T9 wiring, no source |
| doc-reasoning | report-classic | convention | - | rationale/doc-reasoning.md: schema worked example (09-library-schema.md:525-528) |
| doc-reasoning | whitepaper-formal | convention | - | rationale/doc-reasoning.md: shares style key, no source |
| doc-reasoning | proposal-narrative | convention | - | rationale/doc-reasoning.md: no source |
| doc-reasoning | quote-devis | convention | - | rationale/doc-reasoning.md: cites research/69 Direction 2 risk framing only, no fetched source |
| doc-reasoning | deck-generic | convention | - | rationale/doc-reasoning.md: internal design decisions (09-library-schema.md:569-586; 57-deck-projection-fix.md), no external source |
| doc-reasoning | one-pager-restrained | convention | - | rationale/doc-reasoning.md: no source |
| doc-reasoning | infographic-scaffold | convention | - | rationale/doc-reasoning.md: 59-infographic-content.md: size explicitly 'CONVENTION, not sourced' |
| doc-reasoning | invoice-tabular | convention | - | rationale/doc-reasoning.md: same as quote-devis, no source |
| doc-reasoning | cv-us-uk-designed | authority | fetched | 69:10; doc-reasoning.md cv-us-uk-designed |
| doc-reasoning | cv-us-uk-designed | authority | fetched | 69:12 (fetched) |
| doc-reasoning | cv-us-uk-designed | authority | fetched | 69:13 (fetched; single column, no headers/footers/text boxes) |
| doc-reasoning | cv-us-uk-designed | authority | fetched | 70:15 (fetched) |
| doc-reasoning | cv-us-uk-designed | authority | search-corroborated | 70:3 (search-derived); gray-90 #1b1b1b, blue-60v #005ea2 |
| doc-reasoning | cv-dach-tabular | authority | fetched | 69:34 (fetched, photo permitted) |
| doc-reasoning | cv-dach-tabular | authority | fetched | 70:25 (fetched) |
| doc-reasoning | cv-dach-tabular | authority | search-corroborated | 70:3, :29; #0b0c0c / #484949 |
| doc-reasoning | cv-eu-europass | authority | fetched | 69:53 (fetched) |
| doc-reasoning | cv-eu-europass | authority | fetched | 69:55 (fetched) |
| doc-reasoning | cv-eu-europass | authority | search-corroborated | 70:3, :35-41 (link colour #1a65a6) |
| doc-reasoning | cv-editorial | authority | fetched | 70:47 (fetched; illustrative, explicitly not Fonts In Use) |
| doc-reasoning | cv-editorial | authority | fetched | 70:47 (fetched; illustrative) |
| doc-reasoning | cv-editorial | authority | search-corroborated | 70:3, :53 (search-corroborated after truncated fetch) |
