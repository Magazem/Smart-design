# Document Design Intelligence

A free, open-source Claude Skill that raises output quality and removes
"AI slop" in documents — presentations, CVs, brochures, reports, and similar
print/office artifacts — the way UI/UX Pro Max does for web interfaces.
It works by resolving requests against a curated, validated document-design
library instead of leaving layout, typography, and color choices to free
model judgment, and it supports a per-user brand overlay so generated
documents can inherit your own colors, fonts, and voice by default.

This skill does not generate `.docx`/`.pptx` files itself — it resolves the
design decision (layout, typography, color, structure) and hands the actual
file-building step to Anthropic's own built-in `docx` and `pptx` skills,
which already know how to produce those formats correctly. PDF output is the
one exception: this skill renders PDFs natively (HTML through headless
Chromium, with WeasyPrint as an optional fallback), since that's its primary
output path, not a handoff. See `research/24-builtin-alignment.md` for why.

**Status**: scaffolding only. The retrieval library, resolver, and renderers
are not built yet — see `research/09-library-schema.md` and
`research/15-distribution-model.md` for their design before relying on this
repo as a working skill.

## Install

**You'll need**: a Claude Pro, Max, Team, or Enterprise plan, with Code Execution
turned on. (Free plans and Code Execution being off will make this skill unable
to run its scripts — Anthropic's help center article "Create and edit files with
Claude" explains where to turn it on if you're not sure.)

1. **Download** the latest `document-design-intelligence-vX.Y.Z.zip` from this
   project's [Releases page](../../releases) — click the `.zip` file under the
   newest release, no need to unzip it yourself.
2. In claude.ai, go to **Settings → Customize → Skills → Add**, and choose the
   file you just downloaded. That's it — the skill is installed and Claude will
   use it automatically whenever you ask for a document, deck, CV, brochure, or
   report.

## Give it your brand (optional, one-time)

Start a new chat with the skill on and tell Claude about your brand — your
colors, fonts, and voice, or just attach your existing brand guidelines. Ask
it to set your brand up by name. Under the hood this is a one-file flow:
Claude writes a single `brand.md` (slug, palette, typefaces, doctypes — see
`data/brand/README.md` for the exact grammar) from what you told it, then
runs `scripts/make_brand_kit.py` on it, which self-checks the result against
the same validation gate the release build uses and zips it into a brand kit
— you never have to write or touch that file yourself. It will hand you back
**two files** (downloadable from that chat message):

- `my-brand-kit.zip` — small, just your brand's own data. **Save this
  somewhere you'll find it again, outside claude.ai** — nothing written during
  a chat is kept once that chat ends, even inside the skill's own folder, so
  this file is the *only* copy of your brand once you close the conversation.
  You'll reuse it every time this skill gets updated (see below).
- an updated skill `.zip` — upload this one in Settings → Skills, replacing the
  base-only version from step 2 above. From now on, every document it makes
  will default to your brand.

## Updating to a new version

Every update replaces the whole skill, and nothing carries over automatically
— not your brand, and not anything a script wrote during a previous chat.
This has been directly tested and confirmed, so here's what actually works,
not a guess:

1. Download the new `.zip` from Releases and upload it in Settings → Skills,
   same as a first install. (Your brand is temporarily gone at this point —
   that's expected, keep going.)
2. Start a **new chat** with the skill on — it's now running the new version
   you just uploaded — and **attach only the `my-brand-kit.zip` you saved**
   when you first set up your brand. Ask Claude to merge your brand kit in.
   You don't need to attach the base skill zip again: the skill locates its
   own currently-running files automatically and merges your brand kit into
   *that*, then hands you back one merged `.zip`, downloadable from that
   message.
3. Download that merged `.zip` and upload it in Settings → Skills, replacing
   what you uploaded in step 1. Your brand and the new version are now both in
   place, together — until the next update, when you repeat this with the
   same saved `my-brand-kit.zip`.

(If the skill ever can't locate its own files automatically, it will say so
and ask you to attach the base `.zip` too — attach both files to the same
message in that case, and it merges the one you attached instead.)

## License

This project is MIT licensed (see `document-design-intelligence/LICENSE`). Its
retrieval/validation architecture was independently studied from UI/UX Pro Max
(MIT, © 2024 Next Level Builder) — see `document-design-intelligence/NOTICE.md`
for the full attribution. No code, data rows, or text from that project are
reused here.

### What this project takes from UI/UX Pro Max, and what it doesn't

This project studied how UI/UX Pro Max is built — not what it says. What we
took is the *architecture*: matching a request against a small, curated table
with keyword search (BM25), picking the best match with a deterministic
tie-break instead of leaving it to free-form judgment, resolving the rest of
the decision through foreign keys instead of a second fuzzy search, and
checking the result against hard-coded rules (validators) instead of trusting
the model's taste. None of that is UI/UX Pro Max's *content* — we wrote our
own tables, our own rules, and our own thresholds for documents from scratch,
sourced from our own research into CVs, print production, and ATS behavior.
Zero lines of their code and zero rows of their data are in this project.
Where the two disagree on how something should work, ours is the one built
for paginated documents, not for a single web screen.
