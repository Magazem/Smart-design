# rationale/palettes.md

Hand-authored (T4 has no rationale generator). Four rows added at A4 --
`cv-harvard`, `cv-dach-formal`, `cv-europass`, `cv-editorial` -- one per CV direction in
`research/70-cv-type-and-colour.md`. Every hex sourced there is carried verbatim; every
additional cell needed to fill all 20 columns (Secondary/On Secondary, Muted/On Muted, Rule
Hair) that 70 did not itself specify is tagged **CONVENTION** below and derived from the same
published design system 70 already cites for that direction, not invented independently.

### `cv-harvard`

`Primary`/`On Primary` = USWDS `gray-90` `#1b1b1b` on white, **17.2:1** (research/70,
computed there). `Accent`/`On Accent` = USWDS `blue-60v` `#005ea2` on white, **6.7:1**
(research/70, computed there), used only for the name/header rule per research/69's
Direction 1 slop-avoidance section (no default-blue-everywhere). `Secondary`,
`Muted`/`On Muted` and `Rule Hair` are CONVENTION: reused from `mono-ink`'s equivalent
neutral-gray cells (`#4A4A4A`/`#F2F2F2`/`#555555`/`#CCCCCC` family), since 70 authored only
the text/accent pair for this direction and a secondary/muted role was not in its scope.
`Text-Safe Roles=foreground;primary;secondary;accent` (accent clears 4.5:1 at any size, so it
is safe as body-scale text, unlike `cv-editorial`'s accent below). `Fill-Only Roles=muted`.

### `cv-dach-formal`

`Primary`/`On Primary` = GOV.UK Design System text colour `#0b0c0c` on white, **19.6:1**
(research/70, computed there). `Secondary` = GOV.UK "dark grey" `#484949`, **9.0:1** on white
(research/70, computed there) -- reused directly as `Secondary` here since 70 names it as the
direction's rule-line colour and it already clears AA at that ratio for text use too.
`Accent`/`On Accent` left blank: research/70 states "No accent colour; formality signalled by
structure, not hue," matching `mono-ink`'s blank-accent pattern. `Muted`/`On Muted`/
`Rule Hair` are CONVENTION, reusing `mono-ink`'s neutral values since 70 gives no
second/third grey step for this direction. `Rule Brand` = `#0b0c0c` (no accent to carry it,
so the strong rule takes the primary ink colour, matching how `mono-ink`'s own
`Rule Brand=Foreground` works). `Text-Safe Roles=foreground;primary;secondary`.

### `cv-europass`

`Primary`/`On Primary` = `#0b0c0c` on white (same GOV.UK text token as `cv-dach-formal`,
re-cited from research/70 Direction 3, which states the same text colour). `Accent`/
`On Accent` = GOV.UK "link colour" `#1a65a6`, **6.1:1** on white (research/70, computed
there), restricted per 70 to "section-label underscores only, never a full-block fill" --
still clears AA at body-text contrast, so it stays in `Text-Safe Roles` unlike
`cv-editorial`'s accent. `Secondary`/`Muted`/`Rule Hair` CONVENTION, same GOV.UK-family
reuse as `cv-dach-formal` (both directions cite GOV.UK Design System as their colour
authority). `Rule Brand=#1a65a6` (the accent carries the brand rule here, unlike
`cv-dach-formal` which has no accent to give it).

### `cv-editorial`

`Primary`/`On Primary` = IBM Carbon `Gray 100` `#161616` on white, **18.1:1** (research/70,
computed there). `Accent`/`On Accent` = IBM Carbon `Blue 60` `#0f62fe`, **5.0:1** on white
(research/70, computed there) -- 70 explicitly flags this as the *lowest*-margin accent of
all four directions and restricts it to "headline-size text/rules... not small print, where
Gray 100 should carry it instead." That restriction is why `Accent` is placed in
`Fill-Only Roles` here rather than `Text-Safe Roles` (the only one of the four new palettes
where the accent is excluded from the text-safe set) -- `Text-Safe Roles=
foreground;primary;secondary`, `Fill-Only Roles=muted;accent`. `Secondary`/`Muted`/
`Rule Hair` CONVENTION, reusing `mono-ink`'s neutral-gray family since 70 authors only the
Gray 100 / Blue 60 pair for this direction.
