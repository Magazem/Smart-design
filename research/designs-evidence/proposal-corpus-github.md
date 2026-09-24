# Proposal corpus - GitHub `proposal template latex` (F.a)

Coder: Design Researcher. Conventions as `flyer-corpus.md`; cover-page family (C13): header treatment, heading class and colour use from the COVER (page 1), columns/body/rules/density from the FIRST RUNNING-TEXT PAGE (>=250 words, else the most text-like previewed page, `fb`); header/colour per 82a-general (cover = title block). Contrast values are estimates (C9). **Academic skew (disclosed): almost all are university thesis/dissertation-proposal LaTeX templates (Chinese, Indonesian, Persian, Vietnamese, US/EU), plus grant-agency templates (NSF, NIH, NASA, DFG, ERC, NSERC, NWO); business/consulting proposals are absent** (a `consult` Pandoc template exists at rank 34 but has no preview).

## PR.1 Corpus
- URL: `https://api.github.com/search/repositories?q=proposal+template+latex&sort=stars&order=desc&per_page=100 (+ &page=2)`, sort stars desc, per_page 100. **total_count = 196**. Retrieved 2026-09-24.
- Walk: native order, ranks 1-115 evaluated; **N = 40 on-topic codeable** items reached at rank 115 (walk cap 200 not reached). **L1 valid** (>=40 on-topic codeable, F2 satisfied). Ranking Metric string: `share:GH:k/40 by stars`.
- Preview: committed example PDF (rendered pages 1 and running page at 55 dpi, temp dir) or README image; codeable needs a cover and a running-text page (C13) unless the template has no cover (then page 1 serves both, `cover=no`).
- Ranks 1-122 were walked and previewed (total_count 196); coding stopped at N=40 (rank 115). MS/other proposal catalogues: none exist for this family in research/82 section 10.
- Skew: thesis-proposal templates dominate; forms (GH:073, 092, 099, 104) are proposal application forms and are disclosed as form-like; GH:104 is excluded (A8).

## PR.2 Raw list, ranks 1-115 (status)
| rank | repo | stars | status |
|---|---|---|---|
| 1 | [mohuangrui/ucasproposal](https://github.com/mohuangrui/ucasproposal) | 762 | uncodeable/off-topic: README preview is a GIF of the compile output (no static page) |
| 2 | [YimianDai/iNSFC](https://github.com/YimianDai/iNSFC) | 520 | uncodeable/off-topic: no preview |
| 3 | [2black0/Template-LaTeX-Tugas-Akhir-Sarjana-Terapan-UNY](https://github.com/2black0/Template-LaTeX-Tugas-Akhir-Sarjana-Terapan-UNY) | 265 | uncodeable/off-topic: previews are TeXstudio screenshots (C2) |
| 4 | [NemoYuan2008/SJTU-Thesis-Proposal](https://github.com/NemoYuan2008/SJTU-Thesis-Proposal) | 191 | uncodeable/off-topic: no preview (no README image, no committed example PDF/PNG proposal found in the repo root listing) |
| 5 | [stefantruehl/research-proposal-template](https://github.com/stefantruehl/research-proposal-template) | 131 | coded GH:005 |
| 6 | [jeremygibbs/nsf-proposal-latex](https://github.com/jeremygibbs/nsf-proposal-latex) | 128 | coded GH:006 |
| 7 | [hoelzer/dfg](https://github.com/hoelzer/dfg) | 119 | uncodeable/off-topic: no preview (no README image, no committed example PDF/PNG proposal found in the repo root listing) |
| 8 | [oist/LaTeX-templates](https://github.com/oist/LaTeX-templates) | 69 | uncodeable/off-topic: no preview (no README image, no committed example PDF/PNG proposal found in the repo root listing) |
| 9 | [PierreSenellart/erc-latex-template](https://github.com/PierreSenellart/erc-latex-template) | 31 | uncodeable/off-topic: no preview (no README image, no committed example PDF/PNG proposal found in the repo root listing) |
| 10 | [emtpb/proposal_dfg](https://github.com/emtpb/proposal_dfg) | 30 | uncodeable/off-topic: no preview (no README image, no committed example PDF/PNG proposal found in the repo root listing) |
| 11 | [whutug/whu-proposal](https://github.com/whutug/whu-proposal) | 29 | uncodeable/off-topic: no preview (no README image, no committed example PDF/PNG proposal found in the repo root listing) |
| 12 | [cgdsss/thesis_proposal_ustc](https://github.com/cgdsss/thesis_proposal_ustc) | 28 | coded GH:012 |
| 13 | [b201lab/template-proposal-ta-its](https://github.com/b201lab/template-proposal-ta-its) | 25 | uncodeable/off-topic: no preview (no README image, no committed example PDF/PNG proposal found in the repo root listing) |
| 14 | [MingfuYAN/UCAS-Proposal](https://github.com/MingfuYAN/UCAS-Proposal) | 24 | coded GH:014 |
| 15 | [haimingz/NSFC-LaTeX](https://github.com/haimingz/NSFC-LaTeX) | 24 | coded GH:015 |
| 16 | [yhbcode000/sustech-slides-template](https://github.com/yhbcode000/sustech-slides-template) | 20 | uncodeable/off-topic: off-topic: beamer slides template |
| 17 | [birnstiel/erc_template](https://github.com/birnstiel/erc_template) | 19 | uncodeable/off-topic: no preview (no README image, no committed example PDF/PNG proposal found in the repo root listing) |
| 18 | [alexfikl/erc-stg](https://github.com/alexfikl/erc-stg) | 19 | coded GH:018 |
| 19 | [corenel/ZJUProposal](https://github.com/corenel/ZJUProposal) | 18 | uncodeable/off-topic: no preview (no README image, no committed example PDF/PNG proposal found in the repo root listing) |
| 20 | [amrabed/NSF-LaTeX-Template](https://github.com/amrabed/NSF-LaTeX-Template) | 17 | coded GH:020 |
| 21 | [adamnovak/ucscthesis](https://github.com/adamnovak/ucscthesis) | 17 | uncodeable/off-topic: no preview (no README image, no committed example PDF/PNG proposal found in the repo root listing) |
| 22 | [shanhaoli/pkuszdp](https://github.com/shanhaoli/pkuszdp) | 17 | uncodeable/off-topic: no preview (no README image, no committed example PDF/PNG proposal found in the repo root listing) |
| 23 | [bernhold/doe-proposal-latex-template](https://github.com/bernhold/doe-proposal-latex-template) | 16 | uncodeable/off-topic: no preview (no README image, no committed example PDF/PNG proposal found in the repo root listing) |
| 24 | [jhkennedy/DOE_latex_template](https://github.com/jhkennedy/DOE_latex_template) | 16 | uncodeable/off-topic: no preview (no README image, no committed example PDF/PNG proposal found in the repo root listing) |
| 25 | [jiadong5/ZJU_PI_Thesis_Proposal](https://github.com/jiadong5/ZJU_PI_Thesis_Proposal) | 13 | coded GH:025 |
| 26 | [sylvainhalle/nserc-alliance-latex-template](https://github.com/sylvainhalle/nserc-alliance-latex-template) | 12 | uncodeable/off-topic: logo only |
| 27 | [a2s-institute/project-proposal](https://github.com/a2s-institute/project-proposal) | 11 | coded GH:027 |
| 28 | [hpides/thesis-proposal-template](https://github.com/hpides/thesis-proposal-template) | 11 | coded GH:028 |
| 29 | [lungetech/proposal-template](https://github.com/lungetech/proposal-template) | 11 | coded GH:029 |
| 30 | [cyc-987/zju-isee3in1-bachelor-thesis-template](https://github.com/cyc-987/zju-isee3in1-bachelor-thesis-template) | 10 | uncodeable/off-topic: no preview (no README image, no committed example PDF/PNG proposal found in the repo root listing) |
| 31 | [CharlieLeee/BIT-Report-LaTeX](https://github.com/CharlieLeee/BIT-Report-LaTeX) | 10 | coded GH:031 |
| 32 | [lowrank/nsf-template](https://github.com/lowrank/nsf-template) | 9 | uncodeable/off-topic: no preview (no README image, no committed example PDF/PNG proposal found in the repo root listing) |
| 33 | [r02b/Latex-PhD_Proposal_Template](https://github.com/r02b/Latex-PhD_Proposal_Template) | 9 | coded GH:033 |
| 34 | [ramanshahdatascience/consult](https://github.com/ramanshahdatascience/consult) | 9 | uncodeable/off-topic: no preview (no README image, no committed example PDF/PNG proposal found in the repo root listing) |
| 35 | [haoruilee/Proposal_templates](https://github.com/haoruilee/Proposal_templates) | 8 | coded GH:035 |
| 36 | [klb2/dfg-proposal-template](https://github.com/klb2/dfg-proposal-template) | 8 | coded GH:036 |
| 37 | [gtrdp/template-proposal-skripsi](https://github.com/gtrdp/template-proposal-skripsi) | 7 | coded GH:037 |
| 38 | [Ashad001/Latex-Templates](https://github.com/Ashad001/Latex-Templates) | 7 | uncodeable/off-topic: no preview (no README image, no committed example PDF/PNG proposal found in the repo root listing) |
| 39 | [larseggert/h2020proposal](https://github.com/larseggert/h2020proposal) | 7 | uncodeable/off-topic: no preview (no README image, no committed example PDF/PNG proposal found in the repo root listing) |
| 40 | [Noble-Lab/nih-latex](https://github.com/Noble-Lab/nih-latex) | 6 | coded GH:040 |
| 41 | [seqcentral/nih_latex](https://github.com/seqcentral/nih_latex) | 6 | coded GH:041 |
| 42 | [vityasyyy/template-skripsi-dike-ugm](https://github.com/vityasyyy/template-skripsi-dike-ugm) | 6 | uncodeable/off-topic: no preview (no README image, no committed example PDF/PNG proposal found in the repo root listing) |
| 43 | [MrShoza/SJTU-Bachelor-Thesis-Proposal-Latex-Template](https://github.com/MrShoza/SJTU-Bachelor-Thesis-Proposal-Latex-Template) | 6 | uncodeable/off-topic: preview URL broken (404) |
| 44 | [WizenZhang/NMUProposal](https://github.com/WizenZhang/NMUProposal) | 6 | coded GH:044 |
| 45 | [hust-latex/hustproposal](https://github.com/hust-latex/hustproposal) | 5 | uncodeable/off-topic: no preview (no README image, no committed example PDF/PNG proposal found in the repo root listing) |
| 46 | [yueneiqi/ECNU-Thesis-Proposal](https://github.com/yueneiqi/ECNU-Thesis-Proposal) | 5 | coded GH:046 |
| 47 | [eivindml/mist-proposal](https://github.com/eivindml/mist-proposal) | 4 | uncodeable/off-topic: no preview (no README image, no committed example PDF/PNG proposal found in the repo root listing) |
| 48 | [klb2/dfg-cv-template](https://github.com/klb2/dfg-cv-template) | 4 | uncodeable/off-topic: no preview (no README image, no committed example PDF/PNG proposal found in the repo root listing) |
| 49 | [EhsanShahbazii/SBU-Msc-CE-Proposal-Template](https://github.com/EhsanShahbazii/SBU-Msc-CE-Proposal-Template) | 4 | uncodeable/off-topic: banner only |
| 50 | [upb-cn/student-templates-latex](https://github.com/upb-cn/student-templates-latex) | 3 | uncodeable/off-topic: no preview (no README image, no committed example PDF/PNG proposal found in the repo root listing) |
| 51 | [ShuzhaoXie/thu-sigs-ct-proposal-latex-template](https://github.com/ShuzhaoXie/thu-sigs-ct-proposal-latex-template) | 3 | uncodeable/off-topic: no preview (no README image, no committed example PDF/PNG proposal found in the repo root listing) |
| 52 | [satishjhanwer/IITJ-MTP-Template-Generator](https://github.com/satishjhanwer/IITJ-MTP-Template-Generator) | 3 | uncodeable/off-topic: no preview (no README image, no committed example PDF/PNG proposal found in the repo root listing) |
| 53 | [Misoknisky/Proposal-Template](https://github.com/Misoknisky/Proposal-Template) | 3 | coded GH:053 |
| 54 | [thomasgredig/NSF-LaTeX-template](https://github.com/thomasgredig/NSF-LaTeX-template) | 3 | uncodeable/off-topic: no preview (no README image, no committed example PDF/PNG proposal found in the repo root listing) |
| 55 | [gonuke/NEUP-template](https://github.com/gonuke/NEUP-template) | 3 | uncodeable/off-topic: no preview (no README image, no committed example PDF/PNG proposal found in the repo root listing) |
| 56 | [00shiki/template-proposal-skripsi-unj](https://github.com/00shiki/template-proposal-skripsi-unj) | 3 | coded GH:056 |
| 57 | [wanwanbeen/columbia_phd_proposal](https://github.com/wanwanbeen/columbia_phd_proposal) | 3 | uncodeable/off-topic: no preview (no README image, no committed example PDF/PNG proposal found in the repo root listing) |
| 58 | [NoHaitch/Template-Proposal-dan-TA-IF-ITB](https://github.com/NoHaitch/Template-Proposal-dan-TA-IF-ITB) | 3 | uncodeable/off-topic: no preview (no README image, no committed example PDF/PNG proposal found in the repo root listing) |
| 59 | [Liesese/shaanxi-kaiti-template](https://github.com/Liesese/shaanxi-kaiti-template) | 3 | uncodeable/off-topic: no preview (no README image, no committed example PDF/PNG proposal found in the repo root listing) |
| 60 | [soto97/NASA_ROSES_LaTeX_Template](https://github.com/soto97/NASA_ROSES_LaTeX_Template) | 2 | uncodeable/off-topic: no preview (no README image, no committed example PDF/PNG proposal found in the repo root listing) |
| 61 | [mrsunny0-dump/template-mit-be-thesis-proposal](https://github.com/mrsunny0-dump/template-mit-be-thesis-proposal) | 2 | uncodeable/off-topic: unrelated file-list screenshot (C2) |
| 62 | [oist/LaTeX-template-lab-rotation-proposal](https://github.com/oist/LaTeX-template-lab-rotation-proposal) | 2 | uncodeable/off-topic: one-page fill-in form, no cover/running-text pair (C13) |
| 63 | [iangmitchell/proposal](https://github.com/iangmitchell/proposal) | 2 | coded GH:063 |
| 64 | [BryanG13/FWO-Postdoc-ProposalTemplate](https://github.com/BryanG13/FWO-Postdoc-ProposalTemplate) | 2 | uncodeable/off-topic: no preview (no README image, no committed example PDF/PNG proposal found in the repo root listing) |
| 65 | [mathren/proposals_template](https://github.com/mathren/proposals_template) | 2 | uncodeable/off-topic: no preview (no README image, no committed example PDF/PNG proposal found in the repo root listing) |
| 66 | [hossainlab/research-proposal-template](https://github.com/hossainlab/research-proposal-template) | 2 | coded GH:066 |
| 67 | [ethan-jtaylor/UAB_PROPOSAL_TEMPLATE](https://github.com/ethan-jtaylor/UAB_PROPOSAL_TEMPLATE) | 2 | uncodeable/off-topic: no preview (no README image, no committed example PDF/PNG proposal found in the repo root listing) |
| 68 | [2black0/template-latex-proposal-disertasi-its](https://github.com/2black0/template-latex-proposal-disertasi-its) | 2 | coded GH:068 |
| 69 | [wangyunduo/buaa-proposal](https://github.com/wangyunduo/buaa-proposal) | 2 | coded GH:069 |
| 70 | [differentialprivacyir/SUT-MS-Proposal-Template](https://github.com/differentialprivacyir/SUT-MS-Proposal-Template) | 2 | uncodeable/off-topic: no preview (no README image, no committed example PDF/PNG proposal found in the repo root listing) |
| 71 | [Arisudana/template-proposal-tesis-si-its](https://github.com/Arisudana/template-proposal-tesis-si-its) | 2 | uncodeable/off-topic: no preview (no README image, no committed example PDF/PNG proposal found in the repo root listing) |
| 72 | [jsdhami/NAST-Research-Proposal-LaTeX-Format](https://github.com/jsdhami/NAST-Research-Proposal-LaTeX-Format) | 2 | coded GH:072 |
| 73 | [smmsadrnezh/thesis_proposal_template](https://github.com/smmsadrnezh/thesis_proposal_template) | 2 | coded GH:073 |
| 74 | [Zhanghaohao666/hust-grad-proposal](https://github.com/Zhanghaohao666/hust-grad-proposal) | 2 | uncodeable/off-topic: no preview (no README image, no committed example PDF/PNG proposal found in the repo root listing) |
| 75 | [sadimanna/research-statement-templates](https://github.com/sadimanna/research-statement-templates) | 2 | uncodeable/off-topic: no preview (no README image, no committed example PDF/PNG proposal found in the repo root listing) |
| 76 | [TheBarzani/concordia-tex](https://github.com/TheBarzani/concordia-tex) | 2 | uncodeable/off-topic: logo assets only |
| 77 | [oist/LaTeX-template-phd-thesis-proposal](https://github.com/oist/LaTeX-template-phd-thesis-proposal) | 1 | coded GH:077 |
| 78 | [Swepz/latex-templates](https://github.com/Swepz/latex-templates) | 1 | uncodeable/off-topic: no preview (no README image, no committed example PDF/PNG proposal found in the repo root listing) |
| 79 | [ucu-ai-course/project-proposal-template](https://github.com/ucu-ai-course/project-proposal-template) | 1 | uncodeable/off-topic: TeXstudio screenshots (C2) |
| 80 | [zhiyzuo/HK-RGC-Grant-Proposal-Template](https://github.com/zhiyzuo/HK-RGC-Grant-Proposal-Template) | 1 | uncodeable/off-topic: no preview (no README image, no committed example PDF/PNG proposal found in the repo root listing) |
| 81 | [emiapwil/nsfc-template](https://github.com/emiapwil/nsfc-template) | 1 | uncodeable/off-topic: no preview (no README image, no committed example PDF/PNG proposal found in the repo root listing) |
| 82 | [melvincabatuan/ThesisProposalLatexTemplate](https://github.com/melvincabatuan/ThesisProposalLatexTemplate) | 1 | coded GH:082 |
| 83 | [mcps5601/NSTC-proposal-LaTeX](https://github.com/mcps5601/NSTC-proposal-LaTeX) | 1 | uncodeable/off-topic: one-page grant form, no cover (C13) |
| 84 | [nathanatgit/NSFC-proposal-youth-template](https://github.com/nathanatgit/NSFC-proposal-youth-template) | 1 | coded GH:084 |
| 85 | [ross23/latexproposaltemplate](https://github.com/ross23/latexproposaltemplate) | 1 | uncodeable/off-topic: no preview (no README image, no committed example PDF/PNG proposal found in the repo root listing) |
| 86 | [ppak10-archives/Proposal-Template](https://github.com/ppak10-archives/Proposal-Template) | 1 | uncodeable/off-topic: no preview (no README image, no committed example PDF/PNG proposal found in the repo root listing) |
| 87 | [qKTPq/EE490_proposal_template_latex](https://github.com/qKTPq/EE490_proposal_template_latex) | 1 | uncodeable/off-topic: no preview (no README image, no committed example PDF/PNG proposal found in the repo root listing) |
| 88 | [SunnyBingoMe/BTH_Proposal_Template_Latex](https://github.com/SunnyBingoMe/BTH_Proposal_Template_Latex) | 1 | coded GH:088 |
| 89 | [Mhz95/Proposal-LaTeX-Template](https://github.com/Mhz95/Proposal-LaTeX-Template) | 1 | uncodeable/off-topic: off-topic: project proposal FORM with field boxes (form family) |
| 90 | [Ashurinnnn/WMG-upgrade-proposal-template-Latex](https://github.com/Ashurinnnn/WMG-upgrade-proposal-template-Latex) | 1 | coded GH:090 |
| 91 | [mkmcc/NASA-ATP-template](https://github.com/mkmcc/NASA-ATP-template) | 1 | coded GH:091 |
| 92 | [erfanhamdi/proposal-template](https://github.com/erfanhamdi/proposal-template) | 1 | coded GH:092 |
| 93 | [rriley/nprp-template](https://github.com/rriley/nprp-template) | 1 | uncodeable/off-topic: no preview (no README image, no committed example PDF/PNG proposal found in the repo root listing) |
| 94 | [Vallykrie/proposal-skripsi-filkom-latex](https://github.com/Vallykrie/proposal-skripsi-filkom-latex) | 1 | uncodeable/off-topic: no preview (no README image, no committed example PDF/PNG proposal found in the repo root listing) |
| 95 | [zh1-z/SJTU-Bachelor-Thesis-Proposal-Latex-Template](https://github.com/zh1-z/SJTU-Bachelor-Thesis-Proposal-Latex-Template) | 1 | uncodeable/off-topic: cover-only thumbnails (no running page, C13) |
| 96 | [Lowell-DCT/proposal-template](https://github.com/Lowell-DCT/proposal-template) | 1 | uncodeable/off-topic: no preview (no README image, no committed example PDF/PNG proposal found in the repo root listing) |
| 97 | [2black0/Template-LaTeX-Proposal-Praktik-Industri](https://github.com/2black0/Template-LaTeX-Proposal-Praktik-Industri) | 1 | uncodeable/off-topic: TeXstudio screenshots (C2) |
| 98 | [ZHAODONG-LYU/Overleaf-Template-for-Research-Proposal-Report-in-Southeast-University-](https://github.com/ZHAODONG-LYU/Overleaf-Template-for-Research-Proposal-Report-in-Southeast-University-) | 1 | uncodeable/off-topic: no preview (no README image, no committed example PDF/PNG proposal found in the repo root listing) |
| 99 | [MMMPeeters1981/NWO_LaTeX_Template](https://github.com/MMMPeeters1981/NWO_LaTeX_Template) | 1 | coded GH:099 |
| 100 | [shyamkkhadka/tu_ioe_thesis_latex_template](https://github.com/shyamkkhadka/tu_ioe_thesis_latex_template) | 1 | uncodeable/off-topic: no preview (no README image, no committed example PDF/PNG proposal found in the repo root listing) |
| 101 | [Falkor/fnr-latex-template](https://github.com/Falkor/fnr-latex-template) | 1 | uncodeable/off-topic: no preview |
| 102 | [iamgmujtaba/practicum_proposal_template](https://github.com/iamgmujtaba/practicum_proposal_template) | 1 | coded GH:102 |
| 103 | [Krzmbrzl/projectproposal](https://github.com/Krzmbrzl/projectproposal) | 1 | uncodeable/off-topic: one-page sample, no cover/running pair |
| 104 | [teymourlouie/ui_proposal](https://github.com/teymourlouie/ui_proposal) | 1 | coded GH:104 |
| 105 | [ptal-io/Canada_Tri-Council_LaTeX_Template](https://github.com/ptal-io/Canada_Tri-Council_LaTeX_Template) | 1 | coded GH:105 |
| 106 | [khalilullahalfaath/template-tesis-fmipa](https://github.com/khalilullahalfaath/template-tesis-fmipa) | 1 | uncodeable/off-topic: no preview (no README image, no committed example PDF/PNG proposal found in the repo root listing) |
| 107 | [aliensunmin/NSFgrantTemplateTaiwan](https://github.com/aliensunmin/NSFgrantTemplateTaiwan) | 1 | uncodeable/off-topic: no preview (no README image, no committed example PDF/PNG proposal found in the repo root listing) |
| 108 | [guwuDx/MBI6013-RP-LT](https://github.com/guwuDx/MBI6013-RP-LT) | 1 | uncodeable/off-topic: no preview (no README image, no committed example PDF/PNG proposal found in the repo root listing) |
| 109 | [cs-cmuq/nprp-tex](https://github.com/cs-cmuq/nprp-tex) | 1 | uncodeable/off-topic: no preview (no README image, no committed example PDF/PNG proposal found in the repo root listing) |
| 110 | [korpling/CRC-template](https://github.com/korpling/CRC-template) | 1 | uncodeable/off-topic: no preview (no README image, no committed example PDF/PNG proposal found in the repo root listing) |
| 111 | [charcoaltea/Bsc4_tu_iost_proposal_template](https://github.com/charcoaltea/Bsc4_tu_iost_proposal_template) | 1 | uncodeable/off-topic: no preview (no README image, no committed example PDF/PNG proposal found in the repo root listing) |
| 112 | [festradasolano/template-thesis_proposal-fiet_unicauca](https://github.com/festradasolano/template-thesis_proposal-fiet_unicauca) | 1 | uncodeable/off-topic: no preview (no README image, no committed example PDF/PNG proposal found in the repo root listing) |
| 113 | [bean5/project-management-template-latex](https://github.com/bean5/project-management-template-latex) | 1 | uncodeable/off-topic: no preview (no README image, no committed example PDF/PNG proposal found in the repo root listing) |
| 114 | [X-Hozmi/Template-LaTeX-Tugas-Akhir-Sarjana-UBS](https://github.com/X-Hozmi/Template-LaTeX-Tugas-Akhir-Sarjana-UBS) | 1 | uncodeable/off-topic: no preview (no README image, no committed example PDF/PNG proposal found in the repo root listing) |
| 115 | [ashokpant/masters-thesis-proposal-latex](https://github.com/ashokpant/masters-thesis-proposal-latex) | 0 | coded GH:115 |

Totals ranks 1-115: coded 40, uncodeable/off-topic 75.

## PR.3 Coded table (N = 40)
| id | repo | stars | columns | head | body | colour | header | rules | dens | cover? | adm | note |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| GH:005 | stefantruehl/research-proposal-template | 131 | 1 | sans | serif | mono | plain-centered | none | standard | no | y | no cover: centred bold sans title + subtitle + author on page 1 (p1 = title block + abstract + first section); run p2 = contents/related work (fb) |
| GH:006 | jeremygibbs/nsf-proposal-latex | 128 | 1 | sans | serif | mono | plain-left | none | standard | no | y | p1 = "List of Suggested Reviewers" table (not a cover); run p4; all-cells table on p1 only |
| GH:012 | cgdsss/thesis_proposal_ustc | 28 | 1 | sans | serif | mono | plain-centered | rules | airy | yes | y | USTC cover: centred bold CJK title, underlined field lines (rules on cover); run p5 = references |
| GH:014 | MingfuYAN/UCAS-Proposal | 24 | 1 | sans | serif | mono | plain-centered | rules | airy | yes | y | UCAS cover: logo (blue, excluded) + centred bold title, underlined fields; run p14 = references |
| GH:015 | haimingz/NSFC-LaTeX | 24 | 1 | sans | serif | one-accent | plain-centered | none | standard | no | y | NSFC: no cover, centred "report body" heading; blue instruction text #006FC0 x many elements (one cluster; not an A7 default blue); run p3 |
| GH:018 | alexfikl/erc-stg | 19 | 1 | serif | serif | mono | plain-centered | boxes | standard | yes | y | ERC B1: cover page with centred title + grey bordered placeholder boxes; run p2 plain |
| GH:020 | amrabed/NSF-LaTeX-Template | 17 | 1 | serif | serif | mono | ruled | rules | standard | no | y | NSF: p1 = Project Summary; title + heading then a full-width rule under the block; run p2 |
| GH:025 | jiadong5/ZJU_PI_Thesis_Proposal | 13 | 1 | serif | serif | mono | plain-centered | rules | airy | yes | y | ZJU cover: seal (excluded), centred CJK titles, underlined fields; run p2 = contents |
| GH:027 | a2s-institute/project-proposal | 11 | 1 | serif | serif | mono | plain-centered | none | standard | yes | y | a2s cover: two logos top-left (excluded), centred serif titles; run p3 |
| GH:028 | hpides/thesis-proposal-template | 11 | 1 | serif | serif | mono | plain-centered | rules | standard | yes | y | HPI cover: centred; logo (orange/red, excluded); run p2 has a table with rules |
| GH:029 | lungetech/proposal-template | 11 | 1 | sans | serif | mono | plain-left | boxes | dense | yes | y | OpenBSD-logo cover with all-cells data table (boxes) and "Use and Disclosure" heading; run p6 = references |
| GH:031 | CharlieLeee/BIT-Report-LaTeX | 10 | 1 | serif | serif | mono | ruled | rules | airy | yes | y | BIT cover: small-caps title between two heavy full-width rules (image previews: cover=image 1, run=image 2 abstract fb) |
| GH:033 | r02b/Latex-PhD_Proposal_Template | 9 | 1 | serif | serif | mono | plain-centered | none | standard | yes | y | title page + abstract on one page (image preview, run = same image); logo placeholder excluded |
| GH:035 | haoruilee/Proposal_templates | 8 | 1 | serif | serif | mono | plain-centered | none | standard | yes | y | SEU cover (a2s derivative): logos excluded; run p2 has blue headings (not counted, cover colour rule) |
| GH:036 | klb2/dfg-proposal-template | 8 | 1 | sans | sans | mono | plain-centered | none | airy | yes | y | DFG cover: centred bold sans; run p2 red TODO text not counted (cover colour) |
| GH:037 | gtrdp/template-proposal-skripsi | 7 | 1 | serif | serif | mono | plain-centered | none | airy | yes | y | UGM skripsi cover: centred bold serif caps, seal excluded; run p4 = contents |
| GH:040 | Noble-Lab/nih-latex | 6 | 1 | sans | sans | mono | plain-centered | none | dense | yes | y | NIH cover: centred "INSERT TITLE HERE" sans; run p6 dense small-caps sans |
| GH:041 | seqcentral/nih_latex | 6 | 1 | sans | serif | mono | plain-left | none | dense | no | y | no cover: p1 = heading demo; left bold sans headings; run p3 |
| GH:044 | WizenZhang/NMUProposal | 6 | 1 | sans | serif | mono | plain-centered | boxes | standard | yes | y | NMU cover: centred bold CJK title with underlined fields; run p11 has a single frame |
| GH:046 | yueneiqi/ECNU-Thesis-Proposal | 5 | 1 | sans | serif | mono | plain-centered | rules | airy | yes | y | ECNU cover/form: centred title + field table with rules; run p3 framed body |
| GH:053 | Misoknisky/Proposal-Template | 3 | 1 | serif | serif | mono | plain-centered | none | standard | no | y | title + contents on one page (image preview, no cover); centred |
| GH:056 | 00shiki/template-proposal-skripsi-unj | 3 | 1 | serif | serif | mono | plain-centered | none | airy | yes | y | UNJ cover: centred bold, seal excluded; run p3 = contents |
| GH:063 | iangmitchell/proposal | 2 | 1 | serif | serif | mono | plain-centered | none | standard | no | y | no cover: centred title + intro on p1; run p4 is an ethics form (p1 coded) |
| GH:066 | hossainlab/research-proposal-template | 2 | 1 | serif | serif | mono | plain-centered | none | airy | yes | y | HDRO cover: centred serif, logo excluded; run p2 |
| GH:068 | 2black0/template-latex-proposal-disertasi-its | 2 | 1 | sans | serif | fill-blocks | plain-left | none | standard | yes | y | ITS cover: yellow fill ~65% of the page + blue stripe (fill-blocks); title on the fill, but fill height >40% so not band (82a-general A.2 step 2d); logo excluded; run p6 abstract |
| GH:069 | wangyunduo/buaa-proposal | 2 | 1 | sans | serif | mono | plain-centered | boxes | dense | yes | y | BUAA cover: centred bold CJK title, underlined fields; run p8 = appendix scale table (all-cells) |
| GH:072 | jsdhami/NAST-Research-Proposal-LaTeX-Format | 2 | 1 | serif | serif | mono | plain-centered | none | standard | yes | y | NAST cover: centred serif title; run p3 = contents |
| GH:073 | smmsadrnezh/thesis_proposal_template | 2 | 1 | sans | sans | mono | plain-centered | boxes | dense | no | y | Sharif MSc proposal form (Persian): centred bold heading + seal (excluded); tables/boxes on p1-p2 but not every block; form-like (disclosed) |
| GH:077 | oist/LaTeX-template-phd-thesis-proposal | 1 | 1 | serif | serif | mono | ruled | rules | airy | yes | y | OIST cover: small-caps title between two rules ~72% of page (~100% of live width); red squiggle is an illustration (excluded, B1b); borderline for image-hero (starts below top 20%) |
| GH:082 | melvincabatuan/ThesisProposalLatexTemplate | 1 | 1 | serif | serif | mono | plain-centered | rules | standard | yes | y | DLSU cover: centred seal excluded; run p7 = contents with full-width green rules (rules) |
| GH:084 | nathanatgit/NSFC-proposal-youth-template | 1 | 1 | sans | serif | one-accent | plain-centered | none | standard | no | y | NSFC youth: no cover, centred heading; blue #006FC0 text x many (not an A7 default); run p2 |
| GH:088 | SunnyBingoMe/BTH_Proposal_Template_Latex | 1 | 1 | sans | sans | mono | plain-left | none | dense | no | y | BTH proposal form: p1 = base information, left bold sans title; run p2 |
| GH:090 | Ashurinnnn/WMG-upgrade-proposal-template-Latex | 1 | 1 | serif | serif | mono | plain-centered | none | airy | yes | y | WMG cover: multicolour logo excluded, centred bold serif; run p3 = contents |
| GH:091 | mkmcc/NASA-ATP-template | 1 | 1 | serif | serif | mono | plain-centered | none | standard | no | y | NASA ATP: p1 = contents under a centred title/PI block; no cover; run p3 |
| GH:092 | erfanhamdi/proposal-template | 1 | 1 | display | serif | mono | plain-centered | boxes | dense | no | y | Sharif form (Persian): centred calligraphic heading + seal; run p2 has a Gantt all-cells grid |
| GH:099 | MMMPeeters1981/NWO_LaTeX_Template | 1 | 1 | sans | serif | mono | plain-left | rules | dense | no | y | NWO registration form (grant application, form-like; disclosed): bold sans headings, logo excluded; run p12 |
| GH:102 | iamgmujtaba/practicum_proposal_template | 1 | 1 | serif | serif | mono | plain-centered | rules | dense | no | y | IEEE-style paper title block on p1 (image, page 1 only): centred, small-caps section heads; single-page preview |
| GH:104 | teymourlouie/ui_proposal | 1 | 1 | sans | sans | mono | plain-centered | boxes | dense | no | n | A8 every content block in a rounded frame or boxed table (Persian approval form); form-like |
| GH:105 | ptal-io/Canada_Tri-Council_LaTeX_Template | 1 | 1 | serif | serif | mono | plain-left | none | airy | no | y | Tri-Council: p1 = "Summary" heading only (mostly blank), run p3 = references; low information |
| GH:115 | ashokpant/masters-thesis-proposal-latex | 0 | 1 | serif | serif | mono | plain-centered | none | standard | yes | y | Nepal cover: logo (colour) excluded, centred bold serif; run p2 |

## PR.4 Exclusions log (item stays in N)
| id | rule | evidence |
|---|---|---|
| GH:104 | A8 | A8 every content block in a rounded frame or boxed table (Persian approval form); form-like |

Admissible 39 / 40, excluded 1. A8 (every block bordered) x1: GH:104. GH:073 (Persian form) was first also coded A8 but re-read: only the tables/boxes on p1-2 are bordered, kept admissible.

## PR.5 Frequency table k/40 (denominator includes inadmissible; [x] = inadmissible)
| archetype `columns\|heading\|colour\|header` | k | k/40 | admissible k | exemplars |
|---|---|---|---|---|
| `1\|serif\|mono\|plain-centered` | 17 | 0.425 | 17 | GH:018, GH:025, GH:027, GH:028, GH:033, GH:035, GH:037, GH:053, GH:056, GH:063, GH:066, GH:072, GH:082, GH:090, GH:091, GH:102, GH:115 |
| `1\|sans\|mono\|plain-centered` | 10 | 0.250 | 9 | GH:005, GH:012, GH:014, GH:036, GH:040, GH:044, GH:046, GH:069, GH:073, GH:104[x] |
| `1\|sans\|mono\|plain-left` | 5 | 0.125 | 5 | GH:006, GH:029, GH:041, GH:088, GH:099 |
| `1\|serif\|mono\|ruled` | 3 | 0.075 | 3 | GH:020, GH:031, GH:077 |
| `1\|sans\|one-accent\|plain-centered` | 2 | 0.050 | 2 | GH:015, GH:084 |
| `1\|display\|mono\|plain-centered` | 1 | 0.025 | 1 | GH:092 |
| `1\|sans\|fill-blocks\|plain-left` | 1 | 0.025 | 1 | GH:068 |
| `1\|serif\|mono\|plain-left` | 1 | 0.025 | 1 | GH:105 |

8 distinct archetypes; 39 admissible items in 8 admissible archetypes; archetypes with k>=2: 5; singleton admissible items 3/39. Coarsening trigger (>=15 admissible, >50% of admissible items singletons, <5 archetypes with k>=2): not triggered.
Variant modes over admissible items: cover [('yes', 24), ('no', 15)]; body [('serif', 35), ('sans', 4)]; rules/boxes [('none', 22), ('rules', 11), ('boxes', 6)]; density [('standard', 18), ('airy', 12), ('dense', 9)].
Distribution over all 40: header [('plain-centered', 30), ('plain-left', 7), ('ruled', 3)]; colour [('mono', 37), ('one-accent', 2), ('fill-blocks', 1)]; cover [('yes', 24), ('no', 16)].

## PR.6 Second-coder ids and seed
Ids (40): GH:005 GH:006 GH:012 GH:014 GH:015 GH:018 GH:020 GH:025 GH:027 GH:028 GH:029 GH:031 GH:033 GH:035 GH:036 GH:037 GH:040 GH:041 GH:044 GH:046 GH:053 GH:056 GH:063 GH:066 GH:068 GH:069 GH:072 GH:073 GH:077 GH:082 GH:084 GH:088 GH:090 GH:091 GH:092 GH:099 GH:102 GH:104 GH:105 GH:115
Sample `random.Random("82:proposal")` (single coded corpus here; other corpora of the family join under C10): GH:025 GH:066 GH:041 GH:029 GH:015 GH:012 GH:044 GH:033 GH:035 GH:005

## PR.7 Ambiguities met
1. `Cover?` = yes only where page 1 is a title/cover page separate from running text; 11 templates open with title + text on the same page (cover=no), coded from page 1 for both feature groups.
2. GH:077 (OIST): rules above and below the title are ~72% of page width but ~100% of the live width; ruled under the live-width reading (82a-cv); the red squiggle illustration starts below the top 20% so image-hero fails.
3. GH:068 (ITS): full-cover yellow fill; band fails 82a-general step 2(d); header therefore plain-left, colour fill-blocks.
4. Forms (GH:073, 088, 092, 099, 104) are proposal application forms; on-topic by name but form-like; disclosed. GH:089 was excluded as a pure form.
5. GH:105 preview is almost empty (heading only), kept as low information; GH:033/053/102 previews are images with only one page, so cover/run pages coincide.
6. NSFC blue (#006FC0) is not one of the A7 default blues (#4472C4/#4F81BD/#156082/#0563C1), so GH:015/084 stay admissible.

## PR.8 Notes on preview pages
Per C13 the cover page is p1 of the example PDF (or the first README image) and the running page is the first page with >=250 words; `fb` marks fallbacks (contents/sample pages). Items with a single-page preview code both from the same page. See proposal-items-github.csv for preview URLs (PDF url for PDFs; README image for images).

