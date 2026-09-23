# Installing the Document Design Intelligence pack

Two ways to use this project's design rules, depending on whether your
platform can execute code.

## Claude.ai (no code execution needed, or with it)

Upload the `document-design-intelligence` skill ZIP from this project's
GitHub Releases as a custom skill (Settings -> Capabilities -> Skills, or a
Project's file upload for Projects). Claude then follows `SKILL.md` and runs
`scripts/ddi.py` itself -- no extra setup.

## Claude Code

Copy (or symlink) `skill/document-design-intelligence/` into your skills
directory (see Claude Code's own skill-discovery docs for the exact path on
your platform). `SKILL.md` activates the same way any other skill does.

## ChatGPT

- **Custom GPT**: paste this pack's `AGENTS.md` into the GPT's Instructions
  field, and upload `DDI-LIBRARY.md` as Knowledge. The GPT has no code
  execution by default, so it follows `AGENTS.md`'s step-by-step instructions
  and reads exact values out of `DDI-LIBRARY.md`.
- **ChatGPT Project**: add `AGENTS.md` and `DDI-LIBRARY.md` as project files;
  reference them in the project's custom instructions.
- **Code Interpreter (Advanced Data Analysis)**: upload the skill ZIP instead
  and run `python3 scripts/ddi.py ...` directly -- this gets you the live
  per-request search and the mechanical `preflight` gate, which the static
  pack cannot run for you.

ChatGPT usage of this pack is **untested by this project's maintainers** --
the file format (plain markdown instructions + a markdown knowledge file) is
standard for Custom GPTs and Projects, but no live run against ChatGPT has
been recorded here.

## Grok

Add `AGENTS.md`'s contents to a Grok Project's custom instructions, and
upload `DDI-LIBRARY.md` as a project knowledge file. **Untested by this
project's maintainers** -- verify the two-file split is honoured the way it
is described here before relying on it.

## Gemini Gems

Create a Gem, paste `AGENTS.md` into its instructions, and attach
`DDI-LIBRARY.md` as a knowledge file. **Untested by this project's
maintainers.**

## Any other agent (the AGENTS.md convention)

Any assistant or tool that reads a repo-root `AGENTS.md` for operating
instructions can point it at this pack's `AGENTS.md` directly, with
`DDI-LIBRARY.md` alongside it as a reference file. This is the generic,
platform-agnostic fallback the other sections above specialise.
