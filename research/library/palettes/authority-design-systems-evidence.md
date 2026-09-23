# research/library/palettes/authority-design-systems-evidence.md

Per-palette token -> hex mapping and computed WCAG contrast ratios (P3.4). Contrast computed with `skill/document-design-intelligence/scripts/lib/color.contrast_ratio`. All On-X/X pairs and Foreground/Background pass >=4.5:1 (mechanical filter, research/80 §3 / research/81).

## `lib-govuk-ink` — GOV.UK, ink & blue

Source: GOV.UK Design System colours: text #0b0c0c, secondary text #484949, border #cecece, template background #f4f8fb, blue (brand) #1d70b8 (fetched, retrieved 2026-09-23) — https://design-system.service.gov.uk/styles/colour/

| Pair | Foreground | Background | Ratio | Result |
|---|---|---|---|---|
| On Primary / Primary | #ffffff | #0b0c0c | 19.59:1 | OK |
| On Secondary / Secondary | #ffffff | #484949 | 9.03:1 | OK |
| On Accent / Accent | #ffffff | #1d70b8 | 5.17:1 | OK |
| Foreground / Background | #0b0c0c | #ffffff | 19.59:1 | OK |
| On Muted / Muted | #0b0c0c | #f4f8fb | 18.34:1 | OK |

## `lib-uswds-navy` — USWDS, navy ink

Source: USWDS theme tokens: base-darkest #1b1b1b, base-dark #565c65, base-lighter #dfe1e2, base-light #a9aeb1, primary blue-60v #005ea2 (fetched, retrieved 2026-09-23) — https://designsystem.digital.gov/design-tokens/color/theme-tokens/

| Pair | Foreground | Background | Ratio | Result |
|---|---|---|---|---|
| On Primary / Primary | #ffffff | #1b1b1b | 17.22:1 | OK |
| On Secondary / Secondary | #ffffff | #565c65 | 6.74:1 | OK |
| On Accent / Accent | #ffffff | #005ea2 | 6.72:1 | OK |
| Foreground / Background | #1b1b1b | #ffffff | 17.22:1 | OK |
| On Muted / Muted | #1b1b1b | #dfe1e2 | 13.13:1 | OK |

## `lib-atlassian-ink` — Atlassian, neutral ink

Source: Atlassian Design System tokens: text #292A2E, text-subtle #505258, border-input #8C8F97, background-code-gutter #F0F1F2, text-brand/link #1868DB (fetched, retrieved 2026-09-23) — https://atlassian.design/DESIGN.md

| Pair | Foreground | Background | Ratio | Result |
|---|---|---|---|---|
| On Primary / Primary | #FFFFFF | #292A2E | 14.34:1 | OK |
| On Secondary / Secondary | #FFFFFF | #505258 | 7.81:1 | OK |
| On Accent / Accent | #FFFFFF | #1868DB | 5.20:1 | OK |
| Foreground / Background | #292A2E | #FFFFFF | 14.34:1 | OK |
| On Muted / Muted | #505258 | #F0F1F2 | 6.91:1 | OK |

## `lib-carbon-mono` — IBM Carbon, monochrome

Source: IBM Carbon color tokens: Gray 100 #161616, Gray 70 #525252, Gray 20 #e0e0e0, Gray 10 #f4f4f4 (fetched, retrieved 2026-09-23) — https://raw.githubusercontent.com/carbon-design-system/carbon/main/packages/colors/src/dtcg/colors.json

| Pair | Foreground | Background | Ratio | Result |
|---|---|---|---|---|
| On Primary / Primary | #ffffff | #161616 | 18.10:1 | OK |
| On Secondary / Secondary | #ffffff | #525252 | 7.81:1 | OK |
| On Accent / Accent | (blank) | (blank) | n/a | n/a (no accent) |
| Foreground / Background | #161616 | #ffffff | 18.10:1 | OK |
| On Muted / Muted | #161616 | #f4f4f4 | 16.45:1 | OK |

## `lib-govuk-forest` — GOV.UK, forest green

Source: GOV.UK Design System colours: text #0b0c0c, secondary text #484949, green (success/web palette) #0f7a52 (fetched, retrieved 2026-09-23) — https://design-system.service.gov.uk/styles/colour/

| Pair | Foreground | Background | Ratio | Result |
|---|---|---|---|---|
| On Primary / Primary | #ffffff | #0b0c0c | 19.59:1 | OK |
| On Secondary / Secondary | #ffffff | #484949 | 9.03:1 | OK |
| On Accent / Accent | #ffffff | #0f7a52 | 5.35:1 | OK |
| Foreground / Background | #0b0c0c | #ffffff | 19.59:1 | OK |
| On Muted / Muted | #0b0c0c | #f4f8fb | 18.34:1 | OK |

## `lib-carbon-forest` — IBM Carbon, forest green

Source: IBM Carbon color tokens: Gray 100 #161616, Gray 70 #525252, Green 60 #198038 (fetched, retrieved 2026-09-23) — https://raw.githubusercontent.com/carbon-design-system/carbon/main/packages/colors/src/dtcg/colors.json

| Pair | Foreground | Background | Ratio | Result |
|---|---|---|---|---|
| On Primary / Primary | #ffffff | #161616 | 18.10:1 | OK |
| On Secondary / Secondary | #ffffff | #525252 | 7.81:1 | OK |
| On Accent / Accent | #ffffff | #198038 | 5.02:1 | OK |
| Foreground / Background | #161616 | #ffffff | 18.10:1 | OK |
| On Muted / Muted | #161616 | #f4f4f4 | 16.45:1 | OK |

## `lib-govuk-burgundy` — GOV.UK, burgundy red

Source: GOV.UK Design System colours: text #0b0c0c, secondary text #484949, red (error/web palette) #ca3535 (fetched, retrieved 2026-09-23) — https://design-system.service.gov.uk/styles/colour/

| Pair | Foreground | Background | Ratio | Result |
|---|---|---|---|---|
| On Primary / Primary | #ffffff | #0b0c0c | 19.59:1 | OK |
| On Secondary / Secondary | #ffffff | #484949 | 9.03:1 | OK |
| On Accent / Accent | #ffffff | #ca3535 | 5.16:1 | OK |
| Foreground / Background | #0b0c0c | #ffffff | 19.59:1 | OK |
| On Muted / Muted | #0b0c0c | #f4f8fb | 18.34:1 | OK |

## `lib-radix-burgundy` — Radix Colors, burgundy

Source: Radix Colors red scale (light theme): red-12 #641723, red-11 #ce2c31, red-6 #fdbdbe, red-3 #feebec, red-1 #fffcfc (fetched, retrieved 2026-09-23) — https://www.radix-ui.com/colors/docs/palette-composition/scales

| Pair | Foreground | Background | Ratio | Result |
|---|---|---|---|---|
| On Primary / Primary | #ffffff | #641723 | 12.44:1 | OK |
| On Secondary / Secondary | #ffffff | #ce2c31 | 5.21:1 | OK |
| On Accent / Accent | (blank) | (blank) | n/a | n/a (no accent) |
| Foreground / Background | #641723 | #fffcfc | 12.19:1 | OK |
| On Muted / Muted | #641723 | #feebec | 10.84:1 | OK |

## `lib-fluent-burgundy` — Fluent 2, burgundy

Source: Fluent UI shared color tokens: grey14 #242424, grey20 #333333, grey92 #ebebeb, grey94 #f0f0f0, burgundy (primary) #a4262c (fetched, retrieved 2026-09-23) — https://raw.githubusercontent.com/microsoft/fluentui/master/packages/tokens/src/global/colors.ts

| Pair | Foreground | Background | Ratio | Result |
|---|---|---|---|---|
| On Primary / Primary | #ffffff | #242424 | 15.52:1 | OK |
| On Secondary / Secondary | #ffffff | #333333 | 12.63:1 | OK |
| On Accent / Accent | #ffffff | #a4262c | 7.26:1 | OK |
| Foreground / Background | #242424 | #ffffff | 15.52:1 | OK |
| On Muted / Muted | #242424 | #f0f0f0 | 13.62:1 | OK |

## `lib-carbon-teal` — IBM Carbon, teal

Source: IBM Carbon color tokens: Gray 100 #161616, Gray 70 #525252, Teal 60 #007d79 (fetched, retrieved 2026-09-23) — https://raw.githubusercontent.com/carbon-design-system/carbon/main/packages/colors/src/dtcg/colors.json

| Pair | Foreground | Background | Ratio | Result |
|---|---|---|---|---|
| On Primary / Primary | #ffffff | #161616 | 18.10:1 | OK |
| On Secondary / Secondary | #ffffff | #525252 | 7.81:1 | OK |
| On Accent / Accent | #ffffff | #007d79 | 4.99:1 | OK |
| Foreground / Background | #161616 | #ffffff | 18.10:1 | OK |
| On Muted / Muted | #161616 | #f4f4f4 | 16.45:1 | OK |

## `lib-govuk-teal` — GOV.UK, teal

Source: GOV.UK Design System colours: text #0b0c0c, secondary text #484949, teal (web palette) #158187 (fetched, retrieved 2026-09-23) — https://design-system.service.gov.uk/styles/colour/

| Pair | Foreground | Background | Ratio | Result |
|---|---|---|---|---|
| On Primary / Primary | #ffffff | #0b0c0c | 19.59:1 | OK |
| On Secondary / Secondary | #ffffff | #484949 | 9.03:1 | OK |
| On Accent / Accent | #ffffff | #158187 | 4.64:1 | OK |
| Foreground / Background | #0b0c0c | #ffffff | 19.59:1 | OK |
| On Muted / Muted | #0b0c0c | #f4f8fb | 18.34:1 | OK |

## `lib-tailwind-sand` — Tailwind, warm sand

Source: Tailwind CSS default palette: stone-900 #1c1917, stone-700 #44403c, stone-300 #d6d3d1, stone-200 #e7e5e4, stone-50 #fafaf9, amber-700 #b45309 (fetched, retrieved 2026-09-23) — https://unpkg.com/tailwindcss@3.4.1/lib/public/colors.js

| Pair | Foreground | Background | Ratio | Result |
|---|---|---|---|---|
| On Primary / Primary | #ffffff | #1c1917 | 17.49:1 | OK |
| On Secondary / Secondary | #ffffff | #44403c | 10.27:1 | OK |
| On Accent / Accent | #ffffff | #b45309 | 5.02:1 | OK |
| Foreground / Background | #1c1917 | #fafaf9 | 16.74:1 | OK |
| On Muted / Muted | #1c1917 | #e7e5e4 | 13.93:1 | OK |

## `lib-radix-sand` — Radix Colors, warm sand

Source: Radix Colors sand + bronze scales (light theme): sand-12 #21201c, sand-11 #63635e, sand-6 #dad9d6, sand-3 #f1f0ef, sand-1 #fdfdfc, bronze-11 #7d5e54 (fetched, retrieved 2026-09-23) — https://www.radix-ui.com/colors/docs/palette-composition/scales

| Pair | Foreground | Background | Ratio | Result |
|---|---|---|---|---|
| On Primary / Primary | #ffffff | #21201c | 16.30:1 | OK |
| On Secondary / Secondary | #ffffff | #63635e | 6.04:1 | OK |
| On Accent / Accent | #ffffff | #7d5e54 | 5.83:1 | OK |
| Foreground / Background | #21201c | #fdfdfc | 16.02:1 | OK |
| On Muted / Muted | #21201c | #f1f0ef | 14.32:1 | OK |

## `lib-material3-purple` — Material 3, baseline purple

Source: Material Design 3 baseline color roles: on-surface #1C1B1F, on-surface-variant #49454F, surface #FFFBFE, surface-variant #E7E0EC, outline-variant #CAC4D0, primary #6750A4 (search-corroborated: m3.material.io color roles/system pages are client-rendered, JS-hydrated, not statically fetchable) (search-corroborated, retrieved 2026-09-23) — https://m3.material.io/styles/color/roles

| Pair | Foreground | Background | Ratio | Result |
|---|---|---|---|---|
| On Primary / Primary | #ffffff | #1C1B1F | 17.13:1 | OK |
| On Secondary / Secondary | #ffffff | #49454F | 9.34:1 | OK |
| On Accent / Accent | #ffffff | #6750A4 | 6.44:1 | OK |
| Foreground / Background | #1C1B1F | #FFFBFE | 16.71:1 | OK |
| On Muted / Muted | #1C1B1F | #E7E0EC | 13.27:1 | OK |

## `lib-carbon-purple` — IBM Carbon, purple

Source: IBM Carbon color tokens: Gray 100 #161616, Gray 70 #525252, Purple 60 #8a3ffc (fetched, retrieved 2026-09-23) — https://raw.githubusercontent.com/carbon-design-system/carbon/main/packages/colors/src/dtcg/colors.json

| Pair | Foreground | Background | Ratio | Result |
|---|---|---|---|---|
| On Primary / Primary | #ffffff | #161616 | 18.10:1 | OK |
| On Secondary / Secondary | #ffffff | #525252 | 7.81:1 | OK |
| On Accent / Accent | #ffffff | #8a3ffc | 5.00:1 | OK |
| Foreground / Background | #161616 | #ffffff | 18.10:1 | OK |
| On Muted / Muted | #161616 | #f4f4f4 | 16.45:1 | OK |

## `lib-fluent-grape` — Fluent 2, grape

Source: Fluent UI shared color tokens: grey14 #242424, grey20 #333333, grey92 #ebebeb, grey94 #f0f0f0, grape (primary) #881798 (fetched, retrieved 2026-09-23) — https://raw.githubusercontent.com/microsoft/fluentui/master/packages/tokens/src/global/colors.ts

| Pair | Foreground | Background | Ratio | Result |
|---|---|---|---|---|
| On Primary / Primary | #ffffff | #242424 | 15.52:1 | OK |
| On Secondary / Secondary | #ffffff | #333333 | 12.63:1 | OK |
| On Accent / Accent | #ffffff | #881798 | 8.01:1 | OK |
| Foreground / Background | #242424 | #ffffff | 15.52:1 | OK |
| On Muted / Muted | #242424 | #f0f0f0 | 13.62:1 | OK |

## `lib-govuk-orange-brown` — GOV.UK, warm brown

Source: GOV.UK Design System colours: text #0b0c0c, secondary text #484949, brown (web palette) #99704a (fetched, retrieved 2026-09-23) — https://design-system.service.gov.uk/styles/colour/

| Pair | Foreground | Background | Ratio | Result |
|---|---|---|---|---|
| On Primary / Primary | #ffffff | #0b0c0c | 19.59:1 | OK |
| On Secondary / Secondary | #ffffff | #484949 | 9.03:1 | OK |
| On Accent / Accent | #000000 | #99704a | 4.77:1 | OK |
| Foreground / Background | #0b0c0c | #ffffff | 19.59:1 | OK |
| On Muted / Muted | #0b0c0c | #f4f8fb | 18.34:1 | OK |

## `lib-uswds-orange` — USWDS, warm orange

Source: USWDS theme tokens: base-darkest #1b1b1b, base-dark #565c65, base-lighter #dfe1e2, base-light #a9aeb1, accent-warm-dark #c05600 (fetched, retrieved 2026-09-23) — https://designsystem.digital.gov/design-tokens/color/theme-tokens/

| Pair | Foreground | Background | Ratio | Result |
|---|---|---|---|---|
| On Primary / Primary | #ffffff | #1b1b1b | 17.22:1 | OK |
| On Secondary / Secondary | #ffffff | #565c65 | 6.74:1 | OK |
| On Accent / Accent | #ffffff | #c05600 | 4.59:1 | OK |
| Foreground / Background | #1b1b1b | #ffffff | 17.22:1 | OK |
| On Muted / Muted | #1b1b1b | #dfe1e2 | 13.13:1 | OK |

## `lib-carbon-dark-slide` — IBM Carbon, dark slide

Source: IBM Carbon color tokens (g100 dark theme family): Gray 100 #161616, Gray 10 #f4f4f4, Gray 20 #e0e0e0, Gray 70 #525252, Gray 80 #393939, Blue 60 #0f62fe, White #ffffff (fetched, retrieved 2026-09-23) — https://raw.githubusercontent.com/carbon-design-system/carbon/main/packages/colors/src/dtcg/colors.json

| Pair | Foreground | Background | Ratio | Result |
|---|---|---|---|---|
| On Primary / Primary | #161616 | #ffffff | 18.10:1 | OK |
| On Secondary / Secondary | #161616 | #e0e0e0 | 13.71:1 | OK |
| On Accent / Accent | #ffffff | #0f62fe | 5.00:1 | OK |
| Foreground / Background | #f4f4f4 | #161616 | 16.45:1 | OK |
| On Muted / Muted | #ffffff | #525252 | 7.81:1 | OK |

## `lib-fluent-dark-slide` — Fluent 2, dark slide

Source: Fluent UI shared color tokens: grey4 #0a0a0a, grey8 #141414, grey14 #242424, grey20 #333333, grey94 #f0f0f0, white #ffffff, blue (primary) #0078d4 (fetched, retrieved 2026-09-23) — https://raw.githubusercontent.com/microsoft/fluentui/master/packages/tokens/src/global/colors.ts

| Pair | Foreground | Background | Ratio | Result |
|---|---|---|---|---|
| On Primary / Primary | #242424 | #ffffff | 15.52:1 | OK |
| On Secondary / Secondary | #242424 | #f0f0f0 | 13.62:1 | OK |
| On Accent / Accent | #ffffff | #0078d4 | 4.53:1 | OK |
| Foreground / Background | #f0f0f0 | #0a0a0a | 17.37:1 | OK |
| On Muted / Muted | #f0f0f0 | #333333 | 11.09:1 | OK |

