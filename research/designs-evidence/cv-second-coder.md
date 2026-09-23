# research/designs-evidence/cv-second-coder.md — Independent second coder (cv family, §7)

Independence note: I read only research/82 §4 (rubric) and §5 (admissibility), plus
research/82a-clarifications-1.md. Item ids/names/URLs were extracted from
cv-corpus-github.md and cv-corpus-npm-ms.md by a python script
(research/designs-evidence/tmp-cv2/extract.py, since deleted with the tmp folder) that
printed only id, repo/package name, and preview URL columns — never the feature or
admissibility columns.

**Disclosure:** two early shell commands (`awk`/`grep` used to inspect table structure
before the extraction script was written) inadvertently printed feature-column data for
GH:001, GH:003, GH:006–GH:010, GH:013, GH:019, GH:021, GH:023 and NPM pos 1–4 into my
context. None of those ids besides GH:003 and GH:007/GH:008 landed in my sample (GH:003,
GH:007, GH:008 did — see below); for those three I re-derived every feature value below
solely from the fetched preview image, not from memory of the leaked table rows, but a
reader should weight agreement on GH:003/GH:007/GH:008 accordingly. All other sampled
items were coded from preview images only, with no prior exposure.

## Family-wide coded-id list (extracted, not shown here — 80 ids: GH 40 + NPM 40)

ids sorted lexicographically, then:

```python
import math, random
sample = random.Random("82:cv").sample(ids, max(min(10, len(ids)), math.ceil(0.25 * len(ids))))
```

`len(ids) = 80` → `n = max(min(10,80), ceil(0.25*80)) = max(10,20) = 20`.

**Sample (n=20):**

`GH:038, NPM:038, NPM:003, NPM:028, NPM:001, GH:077, NPM:049, NPM:080, NPM:044, NPM:061,
GH:008, NPM:075, GH:054, NPM:027, GH:024, GH:007, NPM:014, GH:003, NPM:057, GH:055`

## Coding table

Identity: columns | heading | colour | header. Variant: body, rules/boxes, density, photo.
Admissible = §5 pass/fail; rule id cited for excludes.

| id | Repo/package | Preview URL used | columns | heading | body | colour | header | rules/boxes | density | photo | Admissible |
|---|---|---|---|---|---|---|---|---|---|---|---|
| GH:038 | zachscrivena/simple-resume-cv | raw.githubusercontent.com/zachscrivena/simple-resume-cv/master/Miscellaneous/CV-01.png | 1 | serif | serif | mono | plain-centered | none | standard | no | yes |
| NPM:038 | jsonresume-theme-claude | raw.githubusercontent.com/jsonresume/jsonresume.org/.../claude.png | 1 | sans | sans | one-accent | ruled | boxes | standard | no | yes |
| NPM:003 | jsonresume-theme-engineering | github.com/skoenig/jsonresume-theme-engineering/blob/main/resume.png?raw=true | 1 | serif | serif | mono | plain-centered | rules | dense | no | yes |
| NPM:028 | jsonresume-theme-minyma | raw.githubusercontent.com/jsonresume/jsonresume.org/.../minyma.png | 2-equal | sans | sans | fill-blocks | plain-left | boxes | dense | yes | **no — C1** (multi-column body: two independently-flowing skill-category columns) |
| NPM:001 | jsonresume-theme-even | raw.githubusercontent.com/jsonresume/jsonresume.org/.../even.png | 1 | sans | sans | multi | band | none | airy | yes | yes |
| GH:077 | maksymilan/zju-resume-template | raw.githubusercontent.com/maksymilan/zju-resume-template/master/CV.jpg | 1 | sans | sans | one-accent | plain-centered | rules | dense | no | yes |
| NPM:049 | jsonresume-theme-caffeine | i.imgur.com/yktvc8m.png | 2-sidebar | sans | sans | one-accent | ruled | rules | dense | yes | **no — C1** (left sidebar: About/skills/languages/interests independent of right column) |
| NPM:080 | jsonresume-theme-berlin-grid | raw.githubusercontent.com/jsonresume/jsonresume.org/.../berlin-grid.png | 1 | sans | sans | mono | plain-left | boxes | airy | no | yes |
| NPM:044 | jsonresume-theme-data-driven | raw.githubusercontent.com/jsonresume/jsonresume.org/.../data-driven.png | 1 | sans | sans | one-accent | plain-left | boxes | dense | no | yes |
| NPM:061 | jsonresume-theme-executive-slate | raw.githubusercontent.com/jsonresume/jsonresume.org/.../executive-slate.png | 2-sidebar | serif | serif | fill-blocks | band | rules | standard | no | **no — C1** (dark left sidebar independent of right column) |
| GH:008 | jakegut/resume | raw.githubusercontent.com/jakegut/resume/master/resume.png | 1 | serif | serif | mono | plain-centered | rules | dense | no | yes |
| NPM:075 | jsonresume-theme-modern-plain | github.com/user-attachments/assets/9e74bc13-415c-471e-abaa-20f81cc29a76 | 1 | sans | sans | one-accent | split | rules | standard | no | yes |
| GH:054 | eddiewebb/hugo-resume | raw.githubusercontent.com/eddiewebb/hugo-resume/master/images/about.png | 2-sidebar | sans | sans | fill-blocks | band | boxes | standard | yes | **no — C1** (left nav/sidebar column) |
| NPM:027 | jsonresume-theme-professional | raw.githubusercontent.com/jsonresume/jsonresume.org/.../professional.png | 1 | serif | serif | mono | plain-centered | rules | standard | no | yes |
| GH:024 | liweitianux/resume | raw.githubusercontent.com/liweitianux/resume/master/resume-zh+en.pdf (page 1) | 1 | serif | serif | mono | plain-centered | rules | dense | no | yes |
| GH:007 | jankapunkt/latexcv | raw.githubusercontent.com/jankapunkt/latexcv/master/docs/media/classic.png | 1 | sans | sans | one-accent | plain-centered | rules | standard | no | yes |
| NPM:014 | jsonresume-theme-engineering-leader | github.com/sjw7444/jsonresume-theme-engineering-leader/.../example-resume.png?raw=true | 1 | sans | sans | mono | plain-centered | rules | dense | no | yes |
| GH:003 | billryan/resume | user-images.githubusercontent.com/25968335/131621921-65ab1862-1f56-47ef-9d58-8d5149bec841.png | 1 | serif | serif | mono | plain-centered | rules | airy | no | yes |
| NPM:057 | jsonresume-theme-simple-red | raw.githubusercontent.com/aandrewww/jsonresume-theme-simple-red/master/screenshots/screenshot-1.jpg | 1 | sans | sans | one-accent | plain-left | none | airy | no | yes |
| GH:055 | crispgm/resume | raw.githubusercontent.com/crispgm/resume/master/screenshots/resume-desktop.png | 1 | sans | sans | one-accent | split | rules | airy | no | yes |
