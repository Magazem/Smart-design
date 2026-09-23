# Installing the Document Design Intelligence pack

Two ways to use this project's design rules, depending on whether your
platform can execute code.

## Claude.ai

Skills **require code execution** to be enabled (individual plans: Settings >
Capabilities). With it on, upload the `document-design-intelligence` skill ZIP
from this project's GitHub Releases as a custom skill (Customize > Skills > +
> Create skill > upload the ZIP). Claude then follows `SKILL.md` and runs
`scripts/ddi.py` itself. Uploading the ZIP to a Project's files does NOT
install a skill. With code execution off, use this portable pack instead: paste
`AGENTS.md` into the Project's instructions and add `DDI-LIBRARY.md` as
Project knowledge.

## Claude Code

Copy (or symlink) `skill/document-design-intelligence/` into your skills
directory (see Claude Code's own skill-discovery docs for the exact path on
your platform). `SKILL.md` activates the same way any other skill does.

## ChatGPT

- **Custom GPT**: paste this pack's `AGENTS.md` into the GPT's Instructions
  field (limit 8,000 characters; `AGENTS.md` is under it), and upload
  `DDI-LIBRARY.md` as Knowledge. Unless you enable Code Interpreter & Data
  Analysis in the GPT's Capabilities it cannot run code, so it follows
  `AGENTS.md`'s instructions and reads exact values out of `DDI-LIBRARY.md`
  (Knowledge is retrieved in chunks, not read whole -- each block is headed
  with its doctype key for that reason).
- **ChatGPT Project**: add `AGENTS.md` and `DDI-LIBRARY.md` as project files
  and reference them in the project's instructions.
- **Code Interpreter (Advanced Data Analysis)**: upload the skill ZIP instead
  and run `python3 scripts/ddi.py ...` directly -- this gets you the live
  per-request search and the mechanical `preflight` gate, which the static
  pack cannot run for you.

ChatGPT usage of this pack is **untested by this project's maintainers** --
the file format (plain markdown instructions + a markdown knowledge file) is
standard for Custom GPTs and Projects, but no live run against ChatGPT has
been recorded here.

## Grok

Grok Projects (instructions + files) could not be verified against xAI's own
documentation, so treat this as **unverified and untested**: add `AGENTS.md`'s
contents to the project's instructions and upload `DDI-LIBRARY.md` as a project
file. Fallback: paste `AGENTS.md` into Settings > Customize Grok and attach
`DDI-LIBRARY.md` in each chat.

## Gemini Gems

Create a Gem, paste `AGENTS.md` into its instructions, and attach
`DDI-LIBRARY.md` as a knowledge file. **Untested by this project's
maintainers.**

## Any other agent (the AGENTS.md convention)

Any assistant or tool that reads a repo-root `AGENTS.md` for operating
instructions can point it at this pack's `AGENTS.md` directly, with
`DDI-LIBRARY.md` alongside it as a reference file. This is the generic,
platform-agnostic fallback the other sections above specialise.
