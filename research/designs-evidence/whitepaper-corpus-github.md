# Whitepaper corpus - GitHub `whitepaper template` (F.a, Design Researcher, 2026-09-24)

Written as a separate file because `whitepaper-corpus.md` does not exist yet (Design Researcher 2 has not finished it); the orchestrator merges. Conventions: `flyer-corpus.md`; C13 (cover page family: header/heading/colour from the cover or title block, columns/body/rules/density from the first running-text page; whitepaper templates mostly start with title + abstract on page 1 = `cover no`); header/colour per research/82a-general.md; A1-A8 (no family fail constraints). Contrast/measurements are estimates from renders (C9).

## WP.1 Sources
- Searches (one call each, 8 s apart, `curl -s -A smart-design-research`, sort stars desc, per_page 100, retrieved 2026-09-24): `whitepaper+template` (total_count 45), `white+paper+template` (20), `whitepaper+latex` (76), `whitepaper+typst` (0). Union of distinct repos: 125.
- On-topic test (section 3.2): a TEMPLATE whose output is a whitepaper. Off-topic: real project/blockchain whitepapers (Solana, Aeternity, BigchainDB, OpenZeppelin, Bitcoin re-typesets and many others), websites/apps/tools (`white-paper` Angular/Bootstrap sites, RAG tools, generators), prompt/skill bundles. Candidates kept: 31 (real papers shipped as the repo's "template" excluded except where the repo describes itself as a template).
- Previews: committed example PDF page 1 and the running page (55 dpi, temp dir); only **8 of the 31 candidates ship any preview**. Candidates without a preview (no PDF/PNG in the root or the first-level directories checked): MCSC, SuperMairio, FamilyOfficeOrg (only screenshots of git), sartimo, SMARTHEP, llnl-proposal, acts, AskerJ, onyxtw, shedali, bobg, Omegapoint (cat.jpg only), MiCAR, cod3xpl0it (figure only), tanjaeh (how-to PDFs, not the template), anboas, seanwestfall, Bear-Wynd (screenshot is a web app), benhunter (list), GrawRadiosondes, mgalloy, mggg (logo only). odinblockchain/latex-whitepaper has a PDF but is the ODIN project's own whitepaper, not a template (off-topic).
- **On-topic codeable = 8 < 10** (WP:002 is cross-listed from the proposal corpus, GH:029, under 82b A4). Per 82 section 2 and 82a C15 a catalogue with fewer than 10 on-topic items is **corroboration only**: no k/N, no `prevalence:` string. The table below is descriptive.

## WP.2 Coded table (N = 8, presence only)
| id | repo | stars | columns | head | body | colour | header | rules | dens | cover | adm | note | preview (page 1 / running page) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| WP:001 | [saboyle/latex-template-whitepaper-basic](https://github.com/saboyle/latex-template-whitepaper-basic) | 37 | 1 | sans | serif | mono | plain-centered | rules | dense | no | y | saboyle: title/author/date centred, narrow centred abstract, numbered bold sans sections; running-head rule on p2; run p2 | https://raw.githubusercontent.com/saboyle/latex-template-whitepaper-basic/master/out/whitepaper.pdf (p1 / p2) |
| WP:002 | [lungetech/proposal-template](https://github.com/lungetech/proposal-template) | 11 | 1 | sans | serif | mono | plain-left | boxes | dense | yes | y | lungetech proposal/whitepaper template (cross-listed from proposal GH:029): cover = OpenBSD-logo page with all-cells data table and "Use and Disclosure" heading (logo excluded); run p6 = references | https://raw.githubusercontent.com/lungetech/proposal-template/master/proposal.pdf (p1 / p6 fb) |
| WP:003 | [mlouhivu/prace-latex-whitepaper](https://github.com/mlouhivu/prace-latex-whitepaper) | 4 | 1 | serif | serif | mono | plain-centered | none | dense | no | y | PRACE white paper: logo (blue, excluded) + org line, centred title/authors/abstract on p1; run p2 | https://raw.githubusercontent.com/mlouhivu/prace-latex-whitepaper/master/example.pdf (p1 / p2) |
| WP:005 | [Iki-Software/iki.whitepaper.template](https://github.com/Iki-Software/iki.whitepaper.template) | 0 | 1 | serif | serif | mono | plain-centered | boxes | standard | no | y | Iki: centred title, bold name, monospaced e-mail, abstract; all-cells table on p1; run p2 = code/equation examples (fb) | https://raw.githubusercontent.com/Iki-Software/iki.whitepaper.template/main/src/template.pdf (p1 / p2 fb) |
| WP:006 | [orelyx/white-paper](https://github.com/orelyx/white-paper) | 0 | 1 | serif | serif | one-accent | plain-centered | none | airy | no | y | orelyx R Markdown white paper: centred title/author/date/abstract; blue links x3 (one cluster); grey code chunk fill (L>0.9) ignored; run p2 = references (fb) | https://raw.githubusercontent.com/orelyx/white-paper/main/white-paper.pdf (p1 / p2 fb) |
| WP:012 | [dominiek/moonfish-whitepaper](https://github.com/dominiek/moonfish-whitepaper) | 0 | 2-equal | serif | serif | mono | plain-centered | none | dense | no | y | Moonfish token-sale white paper (repo describes an open-source whitepaper template; a real paper, disclosed): centred title, two-author block, abstract; two equal text columns from section 1; run p2 | https://raw.githubusercontent.com/dominiek/moonfish-whitepaper/master/whitepaper.pdf (p1 / p2) |
| WP:013 | [browric2/Metrasens_Technical_Document_Template](https://github.com/browric2/Metrasens_Technical_Document_Template) | 0 | 2-equal | sans | serif | multi | ruled | rules | standard | no | y | Metrasens template: logo (multicolour, excluded) + orange rule + big teal bold title + teal author + orange rule; orange drop cap; teal + orange = 2 clusters; two-column body; run p2 | https://raw.githubusercontent.com/browric2/Metrasens_Technical_Document_Template/main/main.pdf (p1 / p2) |
| WP:017 | [taryune/whitepaper-template](https://github.com/taryune/whitepaper-template) | 0 | 1 | serif | serif | mono | plain-centered | none | airy | yes | y | taryune: title page with placeholder title/URL/version + abstract; run p2 = contents (fb) | https://raw.githubusercontent.com/taryune/whitepaper-template/main/whitepaper.pdf (p1 / p2 fb) |

Excluded from coding (listed): odinblockchain/latex-whitepaper (ODIN's own whitepaper, illustrated cover; off-topic as a template).

## WP.3 Exclusions and presence tally
No A1-A8 exclusions: 8/8 admissible (one serif/sans family each, no gradients or icon repeats; blue links in WP:006 are not an A7 default-blue accent). Archetype presence (`columns|heading|colour|header`):
| archetype | items |
|---|---|
| `1\|serif\|mono\|plain-centered` | WP:003, WP:005, WP:017 |
| `1\|sans\|mono\|plain-centered` | WP:001 |
| `1\|sans\|mono\|plain-left` | WP:002 |
| `1\|serif\|one-accent\|plain-centered` | WP:006 |
| `2-equal\|sans\|multi\|ruled` | WP:013 |
| `2-equal\|serif\|mono\|plain-centered` | WP:012 |

6 distinct archetypes over 8 items; `1|serif|mono|plain-centered` appears 3 times (WP:003, 005, 017). Whitepaper remains a shortfall family: no ranked corpus, seeds + a possible 82b A5 borrow from report (structural twin).

## WP.4 Bias and second-coder
GitHub whitepaper templates are LaTeX/R Markdown/Typst, developer- and crypto-adjacent; most real whitepapers on GitHub are project papers, not templates. Header is plain-centered on 6/8, and the cover is `no` on 6/8. Second-coder ids: WP:001 WP:002 WP:003 WP:005 WP:006 WP:012 WP:013 WP:017 (`random.Random("82:whitepaper")` sample under C10 is family-wide, drawn by the orchestrator; over these 8: WP:017 WP:003 WP:005 WP:001 WP:006 WP:013 WP:002 WP:012).

## WP.5 Ambiguities
1. Whitepaper front matter is a title block, not a cover (cover=no on 6/8), so C13 page pairs coincide for header and body features. 2. WP:012 (Moonfish) is a real token-sale whitepaper whose repo is described as a template. 3. WP:002 is a proposal/whitepaper hybrid, coded once here and once in the proposal corpus (same coding). 4. Contents/reference pages served as the running page for four items (fb).
