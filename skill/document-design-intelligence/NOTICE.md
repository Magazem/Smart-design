# Attribution

This project's routing/validation architecture — BM25 retrieval, closed-form
rerank, foreign-key resolution chain, and deterministic anti-slop validators —
was independently studied from **UI/UX Pro Max**
(https://github.com/nextlevelbuilder/ui-ux-pro-max-skill), MIT License,
Copyright (c) 2024 Next Level Builder — architecture studied against commit
`4aad0584d92131626b16d4ff4d77f0455385013c` (2026-09-06). Cited by commit
rather than by upstream's own version number, because that field has been
found to be unreliable (see `research/11-upstream-releases.md` §5) —
upstream's `plugin.json`/`skill.json` have read "2.13.0" since 2026-08-06
regardless of what code is actually present.

**No upstream source code, CSV rows, or text content is reproduced in this
project.** All data tables (`data/base/*.csv`) and prose (`references/*.md`,
`SKILL.md`) are authored independently for the document domain.

See `LICENSE` for this project's own MIT terms.
