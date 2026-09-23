# Report corpus - GitHub L1 `"report template" NOT OSCP NOT pentest` (F.a)

Coder: Design Researcher. Retrieved 2026-09-23/24. Conventions as `flyer-corpus.md`; 82a C1-C16 applied (C13: header/heading/colour from the COVER; columns/body/rules/density from the FIRST RUNNING-TEXT PAGE, page numbers recorded per item; C14 A3 on covers). Contrast values are estimates from renders (C9). This file is the report L1; the juried ARC L3 file is `report-corpus-l3.md` (its rows are NOT mixed into these shares).

## R.1 Corpus
- URL: `https://api.github.com/search/repositories?q=%22report+template%22+NOT+OSCP+NOT+pentest&sort=stars&order=desc&per_page=100` (+ `&page=2` after an 8 s pause). Sort stars desc. total_count = **2729**. Pages 1-2 fetched (200 raw items); the walk stopped at rank 148.
- Walk: native order, ranks 1-148 evaluated; **N = 40 on-topic codeable** items reached at rank 148 (walk cap 200 not reached). L1 valid (F2).
- Preview: README image, or a committed example PDF found from the github.com repo root page (HTML), rendered at 55 dpi to the temp dir. Codeable requires BOTH a cover and a running-text page in the preview (C13); cover-only or contents-only previews are uncodeable. Running page = first page after the cover with >=250 words, else the page with most words / the most text-like previewed page (`fallback`, disclosed per item) - many templates only contain a contents or sample-heading page, so `columns`, `body`, `rules`, `density` for those rest on contents/skeleton pages.
- Ranking Metric string for provenance: `share:GH:k/40 by stars`.
- Skew: **Most coded items are university coursework / lab / internship / thesis report templates** (LaTeX or Typst), heavily Chinese (ZJU, UESTC, SHU, SYSU, NJU, HUST, GUET, Tongji...) plus Vietnamese/Persian/Arabic/Moroccan/Indian institutions; the query term `report template` also surfaces security tooling (excluded off-topic) and Power BI/test-report engines. The corpus reflects student LaTeX covers, not business/annual reports (see report-corpus-l3.md for ARC). No cover here is `image-hero` (0/40; logo-only covers), unlike ARC where it is universal.

## R.2 Raw list, ranks 1-148 (status)
| rank | repo | stars | status |
|---|---|---|---|
| 1 | [DevCop95/bugbounty-lab101](https://github.com/DevCop95/bugbounty-lab101) | 380 | off-topic: bug-bounty lab tooling |
| 2 | [memset0/ZJU-Project-Report-Template](https://github.com/memset0/ZJU-Project-Report-Template) | 125 | coded GH:002 |
| 3 | [jaikishantulswani/bb-reports-templates](https://github.com/jaikishantulswani/bb-reports-templates) | 124 | off-topic: bug-bounty report markdown collection (no design preview) |
| 4 | [zxc479773533/HUST-CS-Report-Template](https://github.com/zxc479773533/HUST-CS-Report-Template) | 124 | uncodeable: no README image, no preview file in repo root |
| 5 | [NetEase/arrow](https://github.com/NetEase/arrow) | 101 | off-topic: TestNG plugin |
| 6 | [harrelfe/rscripts](https://github.com/harrelfe/rscripts) | 92 | off-topic: R scripts |
| 7 | [k4rtik/latex-project-report-template](https://github.com/k4rtik/latex-project-report-template) | 81 | uncodeable: README badge only, no report preview |
| 8 | [spearbit-audits/report-template](https://github.com/spearbit-audits/report-template) | 68 | uncodeable: markdown template, no preview |
| 9 | [erfnzdeh/sharif-course-project-report-template](https://github.com/erfnzdeh/sharif-course-project-report-template) | 68 | coded GH:009 |
| 10 | [thuanmazda/hcmut-report-template](https://github.com/thuanmazda/hcmut-report-template) | 67 | coded GH:010 |
| 11 | [michaelroland/jku-templates-report-latex](https://github.com/michaelroland/jku-templates-report-latex) | 59 | uncodeable: no preview in repo root or README |
| 12 | [Editst/SYSU-HealthReport-Template](https://github.com/Editst/SYSU-HealthReport-Template) | 55 | off-topic: GitHub Action config |
| 13 | [Rapporter/rapport](https://github.com/Rapporter/rapport) | 49 | off-topic: R package |
| 14 | [cyber-cfreg/Penetration-Test-Report-Template](https://github.com/cyber-cfreg/Penetration-Test-Report-Template) | 46 | off-topic: penetration-test report template (query intent excludes pentest) |
| 15 | [R4EPI/sitrep](https://github.com/R4EPI/sitrep) | 45 | off-topic: R package |
| 16 | [nathansmithbi/powerbi-resources](https://github.com/nathansmithbi/powerbi-resources) | 43 | off-topic: Power BI resources |
| 17 | [akretion/odoo-py3o-report-templates](https://github.com/akretion/odoo-py3o-report-templates) | 36 | off-topic: Odoo report engine samples |
| 18 | [longqianh/ZJU-experiment-report-template](https://github.com/longqianh/ZJU-experiment-report-template) | 36 | uncodeable: README image host returns 403 (sinaimg) |
| 19 | [ZoeyW061/Assignment-Report-Template](https://github.com/ZoeyW061/Assignment-Report-Template) | 35 | coded GH:019 |
| 20 | [caojiele/automation-report](https://github.com/caojiele/automation-report) | 32 | off-topic: automation-report product |
| 21 | [AnttiKurittu/incident-report-template](https://github.com/AnttiKurittu/incident-report-template) | 31 | off-topic: DFIR markdown template (no preview) |
| 22 | [ahmedsilinii/INSAT-PFE-Report-Template](https://github.com/ahmedsilinii/INSAT-PFE-Report-Template) | 31 | coded GH:022 |
| 23 | [MathSoc/mathWorkReportTemplate](https://github.com/MathSoc/mathWorkReportTemplate) | 29 | uncodeable: no preview (no README report image, no committed PDF/PNG found in the repo root listing) |
| 24 | [Darboux-hub/uestcreport-skill](https://github.com/Darboux-hub/uestcreport-skill) | 29 | off-topic: Claude/Codex agent skill |
| 25 | [rvce-latex/Project-Report-Template](https://github.com/rvce-latex/Project-Report-Template) | 27 | coded GH:025 |
| 26 | [khongsomeo/hcmus-unofficial-report-template](https://github.com/khongsomeo/hcmus-unofficial-report-template) | 26 | uncodeable: no preview in repo root |
| 27 | [MarcinKilarski/Website-Audit](https://github.com/MarcinKilarski/Website-Audit) | 26 | uncodeable: README image is a cropped TOC text snippet, not the report design (C2) |
| 28 | [anontuttuvenus/eWPT-Report-Template](https://github.com/anontuttuvenus/eWPT-Report-Template) | 24 | off-topic: eWPT exam report template (pentest) |
| 29 | [mzky/jmeter5.x-cn-report-template](https://github.com/mzky/jmeter5.x-cn-report-template) | 22 | off-topic: JMeter HTML report skin |
| 30 | [nju-lug/NJURepo](https://github.com/nju-lug/NJURepo) | 22 | uncodeable: no preview in repo root |
| 31 | [404-NOTFOUND-Coder/UESTC--report--template](https://github.com/404-NOTFOUND-Coder/UESTC--report--template) | 22 | coded GH:031 |
| 32 | [Yuxiang-Xiao/NUS-Report-Template-LaTex](https://github.com/Yuxiang-Xiao/NUS-Report-Template-LaTex) | 21 | coded GH:032 |
| 33 | [thomasbenas/LaTeX-report-template](https://github.com/thomasbenas/LaTeX-report-template) | 21 | uncodeable: README image is a presentation slide, not the report design (C2) |
| 34 | [LeoJhonSong/UESTC-Glasgow-Final-Year-Report-Template](https://github.com/LeoJhonSong/UESTC-Glasgow-Final-Year-Report-Template) | 21 | coded GH:034 |
| 35 | [ayodejiayodele/github-developer-metrics](https://github.com/ayodejiayodele/github-developer-metrics) | 21 | off-topic: metrics dashboards |
| 36 | [nenhang/ZJU-report-templates](https://github.com/nenhang/ZJU-report-templates) | 21 | uncodeable: previews are covers only (no running-text page, C13) |
| 37 | [RedGridTactical/RedGridMGRS](https://github.com/RedGridTactical/RedGridMGRS) | 21 | off-topic: mobile app |
| 38 | [LaureatePoet/HFUT_Course_Report_Template](https://github.com/LaureatePoet/HFUT_Course_Report_Template) | 20 | coded GH:038 |
| 39 | [data-goblin/power-bi-visual-templates](https://github.com/data-goblin/power-bi-visual-templates) | 20 | off-topic: Power BI visual templates |
| 40 | [snario/pd2report](https://github.com/snario/pd2report) | 20 | coded GH:040 |
| 41 | [devanshbatham/autoreport](https://github.com/devanshbatham/autoreport) | 20 | off-topic: security bug-report generator |
| 42 | [hust-latex/hustreport](https://github.com/hust-latex/hustreport) | 20 | uncodeable: no preview |
| 43 | [TobyYang7/cuhksz_report_template](https://github.com/TobyYang7/cuhksz_report_template) | 20 | coded GH:043 |
| 44 | [povvo/sleuth](https://github.com/povvo/sleuth) | 20 | off-topic: agent workflow |
| 45 | [Sensente/NJU_LaTex_Template](https://github.com/Sensente/NJU_LaTex_Template) | 19 | coded GH:045 |
| 46 | [kuanhoong/FCI_FYP_Template](https://github.com/kuanhoong/FCI_FYP_Template) | 18 | uncodeable: no preview |
| 47 | [TheNetAdmin/ZjuReportTemplate](https://github.com/TheNetAdmin/ZjuReportTemplate) | 18 | uncodeable: no preview |
| 48 | [DRGagit/ak_befundung](https://github.com/DRGagit/ak_befundung) | 17 | uncodeable: logo only |
| 49 | [LuminolT/SHU-Lab-Report-Template](https://github.com/LuminolT/SHU-Lab-Report-Template) | 17 | coded GH:049 |
| 50 | [BenAcord/AutoRpt](https://github.com/BenAcord/AutoRpt) | 17 | uncodeable: tool screenshots, not a report design |
| 51 | [praseodym/tudelft-report-latex](https://github.com/praseodym/tudelft-report-latex) | 16 | coded GH:051 |
| 52 | [CustomerVoice/PowerBI](https://github.com/CustomerVoice/PowerBI) | 16 | off-topic: Power BI template |
| 53 | [UnexpectedLobster/utt-ST09-ST10](https://github.com/UnexpectedLobster/utt-ST09-ST10) | 16 | uncodeable: PDFs are personal carnets (not the template); no template preview |
| 54 | [dewcode91/report-templates](https://github.com/dewcode91/report-templates) | 15 | off-topic: bug-bounty report collection |
| 55 | [Viktor-Kirk-Almann-Hansen/AAU-LaTeX-Template](https://github.com/Viktor-Kirk-Almann-Hansen/AAU-LaTeX-Template) | 15 | uncodeable: no preview |
| 56 | [ongun-kanat/itu-report-templates](https://github.com/ongun-kanat/itu-report-templates) | 14 | coded GH:056 |
| 57 | [hoang-himself/hcmut-report](https://github.com/hoang-himself/hcmut-report) | 14 | uncodeable: no preview |
| 58 | [Nelson-Cheung/SYSU_Report_Template](https://github.com/Nelson-Cheung/SYSU_Report_Template) | 14 | coded GH:058 |
| 59 | [nipreps/nireports](https://github.com/nipreps/nireports) | 13 | off-topic: neuroimaging reportlets library |
| 60 | [DocF/LaTex-LabReport-Template](https://github.com/DocF/LaTex-LabReport-Template) | 13 | coded GH:060 |
| 61 | [edmullen/HTML-Report-Template](https://github.com/edmullen/HTML-Report-Template) | 13 | uncodeable: no static preview (HTML template) |
| 62 | [essmehdi/ensias-report-template](https://github.com/essmehdi/ensias-report-template) | 12 | uncodeable: no preview |
| 63 | [guluc3m/report-template-typst](https://github.com/guluc3m/report-template-typst) | 12 | uncodeable: no preview |
| 64 | [mzky/jmeter4.x-cn-report-template](https://github.com/mzky/jmeter4.x-cn-report-template) | 12 | off-topic: JMeter HTML report skin |
| 65 | [ongun-kanat/itu_graduation_report_template](https://github.com/ongun-kanat/itu_graduation_report_template) | 12 | coded GH:065 |
| 66 | [omar-besbes/pfe-report-template](https://github.com/omar-besbes/pfe-report-template) | 12 | uncodeable: no preview |
| 67 | [peylix/bdic-report-template-latex](https://github.com/peylix/bdic-report-template-latex) | 12 | coded GH:067 |
| 68 | [quang-tran0/HCMUT-LaTeX-Template](https://github.com/quang-tran0/HCMUT-LaTeX-Template) | 12 | uncodeable: cover preview only (no running-text page, C13) |
| 69 | [Hilbert777/TJU-OS-Lab-Report-Template](https://github.com/Hilbert777/TJU-OS-Lab-Report-Template) | 12 | coded GH:069 |
| 70 | [azmatt/OSINTReportTemplates](https://github.com/azmatt/OSINTReportTemplates) | 12 | uncodeable: no preview |
| 71 | [mvalipour/specflow-report-templates](https://github.com/mvalipour/specflow-report-templates) | 11 | off-topic: SpecFlow test-report XSLT |
| 72 | [roadfoodr/6.419x_report_template](https://github.com/roadfoodr/6.419x_report_template) | 11 | uncodeable: no preview |
| 73 | [firesofmay/BE-Project-Final-Report-Latex-Template](https://github.com/firesofmay/BE-Project-Final-Report-Latex-Template) | 11 | coded GH:073 |
| 74 | [im-rootkid/Vulnerability-Report-Template](https://github.com/im-rootkid/Vulnerability-Report-Template) | 11 | off-topic: bug-bounty vulnerability template |
| 75 | [dkilfoyle/shiny-explorer](https://github.com/dkilfoyle/shiny-explorer) | 11 | off-topic: Shiny explorer |
| 76 | [krestenlaust/AAU-Typst-Template](https://github.com/krestenlaust/AAU-Typst-Template) | 11 | uncodeable: GIF demo only (upload demonstration), no report page |
| 77 | [SOMEAIDI/preprint-clean-elegant-technical-report-template](https://github.com/SOMEAIDI/preprint-clean-elegant-technical-report-template) | 11 | coded GH:077 |
| 78 | [beatussum/typst-bei-report-template](https://github.com/beatussum/typst-bei-report-template) | 11 | uncodeable: cover thumbnail only (no running-text page, C13) |
| 79 | [chrrel/latex-report-template](https://github.com/chrrel/latex-report-template) | 10 | coded GH:079 |
| 80 | [ascuet/puc-report-template](https://github.com/ascuet/puc-report-template) | 10 | uncodeable: logo only |
| 81 | [markwinspear/specflow-selenium-framework](https://github.com/markwinspear/specflow-selenium-framework) | 10 | off-topic: test framework |
| 82 | [azwisec/Bug-Bounty-Reporting-Templates](https://github.com/azwisec/Bug-Bounty-Reporting-Templates) | 10 | off-topic: bug-bounty reporting templates |
| 83 | [bryango/PKUGeneralPhyLabReport_LaTeX](https://github.com/bryango/PKUGeneralPhyLabReport_LaTeX) | 10 | uncodeable: no preview |
| 84 | [WoodyBryant/Report_Template](https://github.com/WoodyBryant/Report_Template) | 10 | coded GH:084 |
| 85 | [xmdjy/sdu-report-template](https://github.com/xmdjy/sdu-report-template) | 10 | coded GH:085 |
| 86 | [MohaElbadry/PFE-Report-Template-Latex](https://github.com/MohaElbadry/PFE-Report-Template-Latex) | 10 | coded GH:086 |
| 87 | [amidaware/reporting-templates](https://github.com/amidaware/reporting-templates) | 9 | uncodeable: no preview |
| 88 | [httprunner/extent-report-templates](https://github.com/httprunner/extent-report-templates) | 9 | off-topic: test-report (Extent) templates |
| 89 | [bartblaze/Cybercrime-Report-Template](https://github.com/bartblaze/Cybercrime-Report-Template) | 9 | off-topic: fill-in incident FORM (form family) |
| 90 | [spo0ds/audit-report-template](https://github.com/spo0ds/audit-report-template) | 9 | uncodeable: single report-image (cover-like) only, no running-text page (C13) |
| 91 | [guluc3m/report-template-latex](https://github.com/guluc3m/report-template-latex) | 9 | uncodeable: no preview |
| 92 | [YuxueYang1204/Literature_Reading_Report_Template](https://github.com/YuxueYang1204/Literature_Reading_Report_Template) | 9 | coded GH:092 |
| 93 | [phuocan803/uit-course-report-template](https://github.com/phuocan803/uit-course-report-template) | 9 | uncodeable: no preview |
| 94 | [Samashi47/latex-pfe-report-template](https://github.com/Samashi47/latex-pfe-report-template) | 9 | coded GH:094 |
| 95 | [MelekElloumi/English-PFE-LaTeX-Report-Template](https://github.com/MelekElloumi/English-PFE-LaTeX-Report-Template) | 9 | uncodeable: no preview |
| 96 | [songjianghu/AppiumAir](https://github.com/songjianghu/AppiumAir) | 9 | off-topic: Appium automation framework |
| 97 | [AndrePatri/PhDBiorobReportTemplate](https://github.com/AndrePatri/PhDBiorobReportTemplate) | 8 | uncodeable: GIF overview only |
| 98 | [AdikaStyle/go-report-builder](https://github.com/AdikaStyle/go-report-builder) | 8 | off-topic: HTML report exporter tool |
| 99 | [SoraShu/HITsz-Lab-report-Template](https://github.com/SoraShu/HITsz-Lab-report-Template) | 8 | uncodeable: cover thumbnail only (no running-text page, C13) |
| 100 | [rimblas/apex-report-templates-demo](https://github.com/rimblas/apex-report-templates-demo) | 8 | off-topic: APEX report templates demo |
| 101 | [adamrees89/LaTeX-Templates](https://github.com/adamrees89/LaTeX-Templates) | 8 | uncodeable: no preview |
| 102 | [AAGI-AUS/AAGITemplates](https://github.com/AAGI-AUS/AAGITemplates) | 8 | uncodeable: cover preview only for the report design (C13); one-page layout is a second design |
| 103 | [kamperh/stellenbosch_ee_report_template](https://github.com/kamperh/stellenbosch_ee_report_template) | 8 | coded GH:103 |
| 104 | [onefact/datathinking.org-report-template](https://github.com/onefact/datathinking.org-report-template) | 8 | coded GH:104 |
| 105 | [berkaycubuk/uludag-university-latex-report-template](https://github.com/berkaycubuk/uludag-university-latex-report-template) | 8 | uncodeable: no preview |
| 106 | [wrm244/GUETReport](https://github.com/wrm244/GUETReport) | 8 | coded GH:106 |
| 107 | [chriswipat/Forensic-Expert-Witness-Report-Module](https://github.com/chriswipat/Forensic-Expert-Witness-Report-Module) | 8 | off-topic: forensic module |
| 108 | [w3c/wai-eval-report-templates](https://github.com/w3c/wai-eval-report-templates) | 7 | off-topic: W3C evaluation report template (markdown, no preview) |
| 109 | [awiloQMH/CancerReportingTemplate](https://github.com/awiloQMH/CancerReportingTemplate) | 7 | uncodeable: no preview |
| 110 | [votinginfoproject/csv-templates](https://github.com/votinginfoproject/csv-templates) | 7 | off-topic: CSV templates |
| 111 | [pan2013e/Report-Template](https://github.com/pan2013e/Report-Template) | 7 | uncodeable: no preview |
| 112 | [jsreport/jsreport-mongodb-store](https://github.com/jsreport/jsreport-mongodb-store) | 7 | off-topic: jsreport store |
| 113 | [ThiroshMadhusha/Bug-Report-Template](https://github.com/ThiroshMadhusha/Bug-Report-Template) | 7 | off-topic: bug-report template |
| 114 | [0xJavlonbeck/CRTM-Report-Template](https://github.com/0xJavlonbeck/CRTM-Report-Template) | 7 | off-topic: red-team exam report template (pentest) |
| 115 | [antran28/Power-BI-Report-Template](https://github.com/antran28/Power-BI-Report-Template) | 7 | off-topic: Power BI template |
| 116 | [frinkleko/SCUT-Experiment-Report-Template](https://github.com/frinkleko/SCUT-Experiment-Report-Template) | 7 | coded GH:116 |
| 117 | [chillchilllei/uestc-Internship-report-template-of-inforandsoftschool](https://github.com/chillchilllei/uestc-Internship-report-template-of-inforandsoftschool) | 7 | uncodeable: no preview |
| 118 | [kargaranamir/girt-data](https://github.com/kargaranamir/girt-data) | 7 | off-topic: dataset tooling |
| 119 | [yourfrienddhruv/SPARTA](https://github.com/yourfrienddhruv/SPARTA) | 7 | off-topic: test-report tool |
| 120 | [GuillaumeHERMOSO/Rapport-TN09-TN10-LaTeX-UTC](https://github.com/GuillaumeHERMOSO/Rapport-TN09-TN10-LaTeX-UTC) | 7 | uncodeable: single cover-like preview (rapport.png) only (C13) |
| 121 | [RickyXu99/MUST-PPT-Template](https://github.com/RickyXu99/MUST-PPT-Template) | 7 | off-topic: PPT template |
| 122 | [SGYSY/lab_report-in-Latex](https://github.com/SGYSY/lab_report-in-Latex) | 7 | uncodeable: previews are contents + figure pages, no cover page (C13) |
| 123 | [ziyu-xie/EIE3810_Report_Latex](https://github.com/ziyu-xie/EIE3810_Report_Latex) | 7 | coded GH:123 |
| 124 | [pliffdax/Labs-Markdown-Template](https://github.com/pliffdax/Labs-Markdown-Template) | 6 | uncodeable: preview links dead (404) |
| 125 | [sanjibnarzary/latex-project-report-template](https://github.com/sanjibnarzary/latex-project-report-template) | 6 | uncodeable: no preview (images are figure assets) |
| 126 | [Poseidon-ng/VirtualHackingLabs_Report_Templates](https://github.com/Poseidon-ng/VirtualHackingLabs_Report_Templates) | 6 | off-topic: hacking-lab report templates |
| 127 | [oaimli/ConfirmationReportTemplate](https://github.com/oaimli/ConfirmationReportTemplate) | 6 | uncodeable: no preview |
| 128 | [CLopMan/PAE-Report_template](https://github.com/CLopMan/PAE-Report_template) | 6 | coded GH:128 |
| 129 | [a1exxd0/uow-report-template](https://github.com/a1exxd0/uow-report-template) | 6 | coded GH:129 |
| 130 | [madneal/oswe-report-template](https://github.com/madneal/oswe-report-template) | 6 | off-topic: OSWE exam report (query excludes OSCP-type) |
| 131 | [iks-ran/LATEX-ZJU-report-template](https://github.com/iks-ran/LATEX-ZJU-report-template) | 6 | uncodeable: no preview |
| 132 | [ChaoFan996/Experiment-Report-Template-SZU](https://github.com/ChaoFan996/Experiment-Report-Template-SZU) | 6 | uncodeable: no preview |
| 133 | [jphernandezdev/trivy-html-report-template](https://github.com/jphernandezdev/trivy-html-report-template) | 6 | off-topic: Trivy HTML scanner template |
| 134 | [baoyunfan0101/rice-university-report-template](https://github.com/baoyunfan0101/rice-university-report-template) | 6 | coded GH:134 |
| 135 | [arnold117/NCHU_Bachelor_Proposal_Report_Template](https://github.com/arnold117/NCHU_Bachelor_Proposal_Report_Template) | 6 | uncodeable: single cover-like preview only (C13) |
| 136 | [AzyzHm/ISAMM-Custom-Latex-Report-Template](https://github.com/AzyzHm/ISAMM-Custom-Latex-Report-Template) | 6 | uncodeable: banner image only |
| 137 | [heydc7/DailyProgressReport](https://github.com/heydc7/DailyProgressReport) | 6 | off-topic: progress-report tool |
| 138 | [Kian-Chen/TongjiReport](https://github.com/Kian-Chen/TongjiReport) | 6 | coded GH:138 |
| 139 | [CrazySpottedDove/PhysicsLabReportTemplate_LaTeX](https://github.com/CrazySpottedDove/PhysicsLabReportTemplate_LaTeX) | 6 | uncodeable: no preview |
| 140 | [ISE-Research/GIRT-Model](https://github.com/ISE-Research/GIRT-Model) | 6 | off-topic: model/UI tooling |
| 141 | [imharshag/Latex-Report](https://github.com/imharshag/Latex-Report) | 6 | coded GH:141 |
| 142 | [AntoineJo/MEMPowerBI](https://github.com/AntoineJo/MEMPowerBI) | 6 | off-topic: Power BI |
| 143 | [yamadharma/academic-laboratory-report-template](https://github.com/yamadharma/academic-laboratory-report-template) | 5 | uncodeable: no preview |
| 144 | [LearnTeachCode/debugging-report-template](https://github.com/LearnTeachCode/debugging-report-template) | 5 | off-topic: debugging report template (markdown) |
| 145 | [FuckyouBB/extent_report_template_httprunner2](https://github.com/FuckyouBB/extent_report_template_httprunner2) | 5 | off-topic: test-report templates |
| 146 | [rapid7/nexpose-warehouse-jasper-templates](https://github.com/rapid7/nexpose-warehouse-jasper-templates) | 5 | off-topic: Jasper templates |
| 147 | [kac89/nmap-report-template](https://github.com/kac89/nmap-report-template) | 5 | off-topic: nmap report template |
| 148 | [pisceskkk/NUDT_ExperimentReportTemplate](https://github.com/pisceskkk/NUDT_ExperimentReportTemplate) | 5 | coded GH:148 |

Totals ranks 1-148: coded 40, off-topic 54, uncodeable 54. (Off-topic vs uncodeable split is by repo description only.)

## R.3 Coded table (N = 40)
Pages: `cover` = page used for header/heading/colour; `run` = page used for columns/body/rules/density (`fb` = fallback, no >=250-word page in the preview).

| id | repo | stars | cover pg | run pg | columns | head | body | colour | header | rules | dens | cover? | adm | note |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| GH:002 | memset0/ZJU-Project-Report-Template | 125 | image 1 | image 3 fb | 1 | serif | serif | mono | plain-centered | none | airy | yes | y | ZJU data-structures report (first design fds_report); centred title + seal image; running page = TOC (fallback) |
| GH:009 | erfnzdeh/sharif-course-project-report-template | 68 | p1 | p17 | 1 | serif | serif | mono | plain-centered | none | standard | yes | y | Persian/English cover, logo image centred; running page 17 = references |
| GH:010 | thuanmazda/hcmut-report-template | 67 | p1 | p3 | 1 | serif | serif | one-accent | plain-centered | boxes | airy | yes | y | blue double page-frame on cover (frame = boxes on cover only); running page 3 = acknowledgements; frame top edge NOT counted as header rule (borderline) |
| GH:019 | ZoeyW061/Assignment-Report-Template | 35 | p1 | p1 | 1 | serif | serif | mono | plain-centered | rules | standard | no | y | title block sits on the same page as running text (no cover); page 1 coded for both |
| GH:022 | ahmedsilinii/INSAT-PFE-Report-Template | 31 | p1 | p7 | 1 | sans | serif | mono | ruled | none | airy | yes | y | thin rule under the logo/ministry block on cover; running page 7 = contents |
| GH:025 | rvce-latex/Project-Report-Template | 27 | p1 | p4 | 1 | serif | serif | mono | plain-centered | boxes | standard | yes | n | A3 crest watermark behind running text (p4 executive summary); black page frame |
| GH:031 | 404-NOTFOUND-Coder/UESTC--report--template | 22 | image 1 | image 2 fb | 1 | sans | serif | mono | plain-centered | rules | airy | yes | y | cover = image 1, running page = abstract page (image 2, fallback); running header rule |
| GH:032 | Yuxiang-Xiao/NUS-Report-Template-LaTex | 21 | p1 | p3 fb | 1 | serif | serif | one-accent | plain-centered | none | standard | yes | y | logo top; title between two full-width rules mid-page (not in top 20%); blue instruction text on running page |
| GH:034 | LeoJhonSong/UESTC-Glasgow-Final-Year-Report-Template | 21 | p1 | p5 | 1 | serif | serif | one-accent | plain-centered | none | airy | yes | y | salmon/orange contents links; running page 5 = contents |
| GH:038 | LaureatePoet/HFUT_Course_Report_Template | 20 | p1 | p3 | 1 | sans | serif | mono | plain-centered | none | standard | yes | y | huge hei-style title; running page 3 = contents |
| GH:040 | snario/pd2report | 20 | p1 | p3 | 1 | serif | serif | mono | plain-centered | none | airy | yes | y | Waterloo PD2; running page 3 = contents |
| GH:043 | TobyYang7/cuhksz_report_template | 20 | p1 | p2 fb | 1 | serif | serif | mono | plain-centered | none | airy | yes | y | crest image + rules around the title (mid-page); running page 2 = contents (fallback) |
| GH:045 | Sensente/NJU_LaTex_Template | 19 | p1 | p2 fb | 1 | sans | serif | mono | plain-centered | none | airy | yes | y | NJU logo image + hei title; running page 2 = sample sections |
| GH:049 | LuminolT/SHU-Lab-Report-Template | 17 | p1 | p2 fb | 1 | sans | sans | mono | plain-centered | rules | airy | yes | y | SHU logo; underlined fields; running page 2 = section list + code listing |
| GH:051 | praseodym/tudelft-report-latex | 16 | p1 | p7 | 1 | sans | sans | fill-blocks | band | none | airy | yes | n | A6 white small text on #00adef = 2.55:1 (color.py, cover render sample; estimate); cyan band ~48% of page |
| GH:056 | ongun-kanat/itu-report-templates | 14 | p1 | p2 fb | 1 | serif | serif | mono | plain-centered | none | airy | yes | y | ITU BLG100E; running page 2 = contents |
| GH:058 | Nelson-Cheung/SYSU_Report_Template | 14 | p1 | p2 | 1 | sans | serif | mono | plain-centered | none | standard | yes | y | SYSU logo, spaced hei title, underlined fields; running page 2 = contents |
| GH:060 | DocF/LaTex-LabReport-Template | 13 | p1 | p7 | 1 | serif | serif | multi | plain-centered | rules | dense | yes | y | NUS-SRI cover; running page 7 = MATLAB listing with green/blue/purple syntax colours (multi: coloured code marks); running header rule |
| GH:065 | ongun-kanat/itu_graduation_report_template | 12 | p1 | p6 fb | 1 | sans | sans | mono | plain-centered | none | airy | yes | y | all-caps bold sans cover; running page 6 = contents |
| GH:067 | peylix/bdic-report-template-latex | 12 | image 1 | image 3 | 1 | serif | serif | multi | plain-centered | boxes | standard | yes | y | two round logos; running page: boxed abstract + blue/green/yellow proposition boxes (theorem boxes) |
| GH:069 | Hilbert777/TJU-OS-Lab-Report-Template | 12 | p1 | p2 fb | 1 | sans | serif | mono | plain-centered | none | airy | yes | y | TJU logo + hei title; running page 2 = contents |
| GH:073 | firesofmay/BE-Project-Final-Report-Latex-Template | 11 | p1 | p6 | 1 | serif | serif | mono | plain-centered | none | standard | yes | y | Pune BE final report; running page 6 = contents |
| GH:077 | SOMEAIDI/preprint-clean-elegant-technical-report-template | 11 | p1 | p1 | 1 | serif | serif | one-accent | ruled | boxes | standard | no | y | title between two thin rules; pale-blue abstract box; no separate cover (title + running text on page 1) |
| GH:079 | chrrel/latex-report-template | 10 | p1 | p11 | 1 | serif | serif | one-accent | plain-centered | none | standard | yes | y | two 16:9 image placeholders on cover; navy contents page numbers; running page 11 = contents |
| GH:084 | WoodyBryant/Report_Template | 10 | p1 | p4 | 1 | sans | serif | mono | plain-centered | none | standard | yes | y | HUST logo + hei title; running page 4 = contents |
| GH:085 | xmdjy/sdu-report-template | 10 | p1 | p2 fb | 1 | sans | sans | multi | plain-centered | boxes | standard | yes | y | SDU cover; running page 2: page frame, blue text and yellow highlight, table |
| GH:086 | MohaElbadry/PFE-Report-Template-Latex | 10 | p1 | p7 | 1 | serif | serif | one-accent | ruled | none | standard | yes | y | three logos + blue rule under the logo row (full width); blue labels; running page 7 = contents |
| GH:092 | YuxueYang1204/Literature_Reading_Report_Template | 9 | p1 | p2 | 1 | sans | serif | mono | ruled | none | standard | yes | y | header line + rule at top of cover; running page 2 = abstract page |
| GH:094 | Samashi47/latex-pfe-report-template | 9 | p1 | p3 | 1 | serif | serif | mono | plain-centered | none | standard | yes | y | logos + rounded title box on cover; running page 3 = acknowledgements |
| GH:103 | kamperh/stellenbosch_ee_report_template | 8 | p1 | p2 | 1 | sans | serif | mono | plain-centered | boxes | standard | yes | y | maroon corner band ~7% (<10%) so not fill-blocks (borderline); running page 2 = declaration with bordered signature table |
| GH:104 | onefact/datathinking.org-report-template | 8 | p1 | p1 | 2-equal | serif | serif | fill-blocks | plain-centered | none | dense | no | y | two-column article; grey abstract box ~13% of page; no separate cover; pages 1 and 2 coded |
| GH:106 | wrm244/GUETReport | 8 | image 1 | image 2 fb | 1 | sans | serif | mono | plain-centered | rules | airy | yes | y | GUET cover; running page = abstract (image 2, fallback); header rule |
| GH:116 | frinkleko/SCUT-Experiment-Report-Template | 7 | p1 | p2 | 1 | sans | serif | mono | plain-centered | none | airy | yes | y | SCUT logo + heavy hei title; running page 2 = contents |
| GH:123 | ziyu-xie/EIE3810_Report_Latex | 7 | p1 | p3 fb | 1 | serif | serif | multi | plain-centered | boxes | standard | yes | y | plain cover; running page 3: code box, red TO-BE-WRITTEN text, blue link |
| GH:128 | CLopMan/PAE-Report_template | 6 | image 2 | image 3 fb | 1 | serif | serif | mono | plain-centered | rules | standard | yes | y | uc3m internship memoria; cover = portada_es.jpeg, running page = datos_en.jpg (tables with rules) |
| GH:129 | a1exxd0/uow-report-template | 6 | image 1 | image 3 | 1 | serif | serif | fill-blocks | band | boxes | dense | yes | y | Warwick purple full cover fill ~55%; running page: justified serif text + boxed theorem |
| GH:134 | baoyunfan0101/rice-university-report-template | 6 | p1 | p2 | 1 | serif | serif | one-accent | plain-left | rules | standard | yes | y | Rice logo left, title left; navy contents; running page 2 |
| GH:138 | Kian-Chen/TongjiReport | 6 | image 1 | image 3 | 1 | sans | serif | one-accent | plain-centered | none | standard | yes | y | Tongji calligraphy logo + title; blue TOC/link text; running page = 03.png |
| GH:141 | imharshag/Latex-Report | 6 | p1 | p3 | 1 | serif | serif | mono | plain-centered | boxes | standard | yes | y | framed cover with logo; running page 3 = contents (frame on cover only) |
| GH:148 | pisceskkk/NUDT_ExperimentReportTemplate | 5 | image 1 | image 3 fb | 1 | serif | serif | mono | plain-centered | none | airy | yes | y | NUDT cover, spaced Song title, underlined fields; running page = description.png |

## R.4 Exclusions log (item stays in N)
| id | rule | evidence |
|---|---|---|
| GH:025 | A3 | A3 crest watermark behind running text (p4 executive summary); black page frame |
| GH:051 | A6 | A6 white small text on #00adef = 2.55:1 (color.py, cover render sample; estimate); cyan band ~48% of page |

Admissible 38 / 40, excluded 2 (A3 x1: GH:025 watermark behind running text; A6 x1: GH:051 white small text on cyan, sampled 2.55:1). C14: no cover title set on a photo excluded here (logo covers only; GH:051 title is black on cyan, 8.2:1).

## R.5 Frequency table k/40 (denominator includes inadmissible; [x] = inadmissible)
| archetype `columns\|heading\|colour\|header` | k | k/40 | admissible k | exemplars |
|---|---|---|---|---|
| `1\|serif\|mono\|plain-centered` | 12 | 0.300 | 11 | GH:002, GH:009, GH:019, GH:025[x], GH:040, GH:043, GH:056, GH:073, GH:094, GH:128, GH:141, GH:148 |
| `1\|sans\|mono\|plain-centered` | 11 | 0.275 | 11 | GH:031, GH:038, GH:045, GH:049, GH:058, GH:065, GH:069, GH:084, GH:103, GH:106, GH:116 |
| `1\|serif\|one-accent\|plain-centered` | 4 | 0.100 | 4 | GH:010, GH:032, GH:034, GH:079 |
| `1\|serif\|multi\|plain-centered` | 3 | 0.075 | 3 | GH:060, GH:067, GH:123 |
| `1\|sans\|mono\|ruled` | 2 | 0.050 | 2 | GH:022, GH:092 |
| `1\|serif\|one-accent\|ruled` | 2 | 0.050 | 2 | GH:077, GH:086 |
| `1\|sans\|fill-blocks\|band` | 1 | 0.025 | 0 | GH:051[x] |
| `1\|sans\|multi\|plain-centered` | 1 | 0.025 | 1 | GH:085 |
| `1\|sans\|one-accent\|plain-centered` | 1 | 0.025 | 1 | GH:138 |
| `1\|serif\|fill-blocks\|band` | 1 | 0.025 | 1 | GH:129 |
| `1\|serif\|one-accent\|plain-left` | 1 | 0.025 | 1 | GH:134 |
| `2-equal\|serif\|fill-blocks\|plain-centered` | 1 | 0.025 | 1 | GH:104 |

12 distinct archetypes; 38 admissible items in 11 admissible archetypes; archetypes with k>=2: 6; singleton admissible items 5/38.
Coarsening trigger (>=15 admissible, >50% of admissible items singletons, <5 archetypes with k>=2): not triggered.

Variant modes over admissible items: cover page [('yes', 35), ('no', 3)]; body [('serif', 35), ('sans', 3)]; rules/boxes [('none', 23), ('boxes', 8), ('rules', 7)]; density [('standard', 20), ('airy', 15), ('dense', 3)].
Feature distributions over all 40: header [('plain-centered', 33), ('ruled', 4), ('band', 2), ('plain-left', 1)]; colour [('mono', 25), ('one-accent', 8), ('multi', 4), ('fill-blocks', 3)]; columns [('1', 39), ('2-equal', 1)].

C16 check: no identity feature is single-valued here (header takes 4 values); header is plain-centered on 33/40 items.

## R.6 Second-coder ids and seed
Ids (GH report corpus, 40): GH:002 GH:009 GH:010 GH:019 GH:022 GH:025 GH:031 GH:032 GH:034 GH:038 GH:040 GH:043 GH:045 GH:049 GH:051 GH:056 GH:058 GH:060 GH:065 GH:067 GH:069 GH:073 GH:077 GH:079 GH:084 GH:085 GH:086 GH:092 GH:094 GH:103 GH:104 GH:106 GH:116 GH:123 GH:128 GH:129 GH:134 GH:138 GH:141 GH:148
Per C10 the second-coder sample is FAMILY-WIDE (this corpus + the 14 ARC25 items of report-corpus-l3.md), computed by the orchestrator; corpus-only sample under `random.Random("82:report")`: GH:043 GH:104 GH:106 GH:032 GH:116 GH:123 GH:049 GH:025 GH:034 GH:069

## R.7 Ambiguities met
1. Running text page: most previews show only contents/sample-headings pages; flagged `fb` per item. Columns=1 is therefore the default for 39/40; only GH:104 (two-column article) differs. The columns feature has almost no discriminating power in this corpus.
2. Heading class of CJK covers: hei (sans) vs song/kai (serif) judged from stroke contrast at 55 dpi; body Song coded serif.
3. `colour` counts chromatic text/rules/marks/fills excluding logos, photos and syntax-highlighted code only when a single hue; coloured code listings with >=2 hues (GH:060) and coloured callout boxes (GH:067, 085, 123) coded multi.
4. `header` on covers where the title is mid-page (most student covers): top-20% block is a logo/institution line, centred -> plain-centered; rules mid-page around a title (GH:032, 043, 149) do not qualify as header rules. Page frames (GH:010, 025, 141) counted as boxes on the cover only; GH:010 borderline for `ruled` (top edge of the frame).
5. Dedup: sibling re-themes of the same university template family (HCMUT #10/#68, INSAT PFE vs INSAT #22/#66/#94, ITU #56/#65) are different repos with different assets; counted separately. No declared forks within the coded set.
6. GH:089 (Cybercrime report form) treated as form-family off-topic; pentest/exam-report templates excluded by the query intent even where a PDF exists (GH:014, 114).
7. Page-count checks: GH:104 uses `example-document.pdf` (the 1-page file in the same repo is the README stub); GH:019/077/104 have no separate cover (title + running text on page 1).
