# Infographic corpus — Information is Beautiful Awards winners (82b A2 juried pool): 2022-2024 gave 4 on-topic (< 10); extended per the I.7 ruling to 2019 and 2018 → **pool N = 12 (see I.8, which supersedes I.4/I.6)**

Coder: Design Researcher 3 (Phase 4 first coder; counts, never judges; research/82 §1). Retrieved **2026-09-23**. Binding: research/82, 82a C1-C23, 82b A1-A5 (adopted 2026-09-24). Format precedents: `brochure-corpus.md`, `poster-corpus-ms.md`.

**Plain result.** Of the 94 distinct IIB winners in the 2022, 2023 and 2024 editions, **4** pass 82b's on-topic test ("single static composition"). A2 needs **≥10** on-topic codeable winners, so **no `prevalence:award:` pool can be issued**. The 82b fallback ("add 2021 if 2022-2024 yields fewer than 10") **cannot run**, because the site has **no 2021 edition** (I.1). The 4 items are listed below as corroboration, with feature codes for information only. They are not counted, have no k/N and carry no Ranking Metric string. Infographic stays **seeds + 1 convention** (research/82 §10) unless the orchestrator authorises older editions (I.6).

## I.1 Source
- URL pattern (82b §1f): `https://www.informationisbeautifulawards.com/showcase?action=index&award=<YYYY>&controller=showcase&page=<n>&pcategory=winner&type=awards`. Fetched with `curl -s -L -A "smart-design-research"`, pages 1-3 per year. Every page returned HTTP 200.
- Distinct winners (by showcase id): **2022 = 30, 2023 = 29, 2024 = 35, total 94**. Page 2 of 2024 holds 5; the other page-2 and page-3 URLs hold none.
- Each card carries `data-random-order`, so page order is **not a metric** and may not be stable. Ids below are assigned in fetch order: year ascending, then page order as served on 2026-09-23. Medal level (Gold/Silver/Bronze, from the card icons) is recorded but **not used** as a weight (A2).
- Every item page `https://www.informationisbeautifulawards.com/showcase/<id>-<slug>` was fetched (94 × HTTP 200). From each one the coder read the entrant's own description, the "See more" target and the full-size preview (`…/large.<ext>`).
- **2021:** `award=2021` returns **HTTP 404** on pages 1-3. The edition selector on the 2022 page lists 2012-2019, 2022, 2023 and 2024 only; there is no 2020 or 2021 edition. So 82b's "add 2021" fallback has no input. Editions 2019 and older are **not** authorised by 82b, and they were **not** fetched or coded.
- Malofiej (82b §3, infographic row 2, "one probe allowed") is outside this task's assignment and was not probed.

## I.2 On-topic test (82b A2, operationalised before any preview was coded)
An item is **on-topic** iff its primary published form is **one static composition**: one poster, sheet, printed card, static chart image or static map. The test is decided from (1) the entrant's own description on the item page, (2) the "See more" target (e.g. a `.png` versus an `/interactive/` article) and (3) the full-size preview. Off-topic classes (82b A2: "interactive-only, video, physical object, web app"; plus §3.2 "other families"):
- **W** — interactive or scrolling web story or article (several graphics in one web page), including newspaper web graphics such as Reuters, SCMP multimedia and pudding.cool;
- **D** — dashboard, tool, browser or web app;
- **V** — video, animation, GIF or sonification;
- **P** — physical object, installation or exhibit;
- **S** — series, book, booklet, report or other multi-page work (not one composition; a book belongs to another family).

Counts: W 60, D 9, S 9, P 7, V 5, **on-topic 4** (2022: 1, 2023: 2, 2024: 1). Total 94.

Borderline, disclosed: **IIB:033** "My digital double and me" is a single printed panel. It was published and previewed as an exhibition installation: a framed acrylic print hanging on chains, and the preview is a photograph of the room. It is therefore classed P. Counting it on-topic would give 5, still < 10, so the outcome is the same.

## I.3 Raw list (94 winners; decision per I.2)

| id | year | item | medal | primary form (from item page) | decision |
|---|---|---|---|---|---|
| IIB:001 | 2022 | [HR Attrition Dashboard](https://www.informationisbeautifulawards.com/showcase/4646-hr-attrition-dashboard) | Bronze | Tableau dashboard with toggle | off: dashboard/tool/web app |
| IIB:002 | 2022 | [How You Play Spades is How You Play Life: Spades in the African-American Community](https://www.informationisbeautifulawards.com/showcase/5420-how-you-play-spades-is-how-you-play-life-spades-in-the-african-american-community) | Bronze | "built the interactive story" (pudding.cool) | off: interactive/web story |
| IIB:003 | 2022 | [Culture in the Crosshairs](https://www.informationisbeautifulawards.com/showcase/4823-culture-in-the-crosshairs) | Gold | 3D javascript fly-through, web article | off: interactive/web story |
| IIB:004 | 2022 | [Anatomy of the Lismore disaster](https://www.informationisbeautifulawards.com/showcase/5341-anatomy-of-the-lismore-disaster) | Gold | web story smh.com.au/interactive | off: interactive/web story |
| IIB:005 | 2022 | [Spain lives in flats: why we have built our cities vertically](https://www.informationisbeautifulawards.com/showcase/5409-spain-lives-in-flats-why-we-have-built-our-cities-vertically) | Bronze | "interactive journalistic project" | off: interactive/web story |
| IIB:006 | 2022 | [Stopping the spread](https://www.informationisbeautifulawards.com/showcase/5700-stopping-the-spread) | Bronze | Reuters web graphics story (simulation) | off: interactive/web story |
| IIB:007 | 2022 | [A Song of Crowns and Tears](https://www.informationisbeautifulawards.com/showcase/4961-a-song-of-crowns-and-tears) | Bronze | visualisation + sonification, YouTube | off: video/animation |
| IIB:008 | 2022 | [Rough Justice](https://www.informationisbeautifulawards.com/showcase/4894-rough-justice) | Bronze | web investigation series part 1 (abc.net.au) | off: interactive/web story |
| IIB:009 | 2022 | [Western Monarch Butterfly Population Decline](https://www.informationisbeautifulawards.com/showcase/5790-western-monarch-butterfly-population-decline) | Silver | "timelapse animation" | off: video/animation |
| IIB:010 | 2022 | [Life under curfew](https://www.informationisbeautifulawards.com/showcase/5559-life-under-curfew) | Gold | "interactive real life data experience" | off: interactive/web story |
| IIB:011 | 2022 | [Afghanistan20](https://www.informationisbeautifulawards.com/showcase/5322-afghanistan20) | Bronze | web historical document (afghanistan20.emergency.it) | off: interactive/web story |
| IIB:012 | 2022 | [I am a book. I am a portal to the universe.](https://www.informationisbeautifulawards.com/showcase/5308-i-am-a-book-i-am-a-portal-to-the-universe) | Silver | 112-page book | off: series/book/multi-page |
| IIB:013 | 2022 | [Gender and language](https://www.informationisbeautifulawards.com/showcase/5703-gender-and-language) | Gold | "illustrated and animated graphics story" | off: interactive/web story |
| IIB:014 | 2022 | [hong kong artists, women](https://www.informationisbeautifulawards.com/showcase/4971-hong-kong-artists-women) | Bronze | three.js/webGL + scroll visualisations | off: interactive/web story |
| IIB:015 | 2022 | [Thunder Roads](https://www.informationisbeautifulawards.com/showcase/5229-thunder-roads) | Gold | "series of interactive visuals" | off: interactive/web story |
| IIB:016 | 2022 | [Animated Sport Results](https://www.informationisbeautifulawards.com/showcase/5373-animated-sport-results) | Silver | "collection of animated gifs" | off: video/animation |
| IIB:017 | 2022 | [The Shape of Dreams](https://www.informationisbeautifulawards.com/showcase/5563-the-shape-of-dreams) | Bronze | web exploration (the-shape-of-dreams.com) | off: interactive/web story |
| IIB:018 | 2022 | [Degrees of Uncertainty](https://www.informationisbeautifulawards.com/showcase/5495-degrees-of-uncertainty) | Gold | "animated data-driven documentary", film | off: video/animation |
| IIB:019 | 2022 | [Abandoned at sea: The desperate journeys of Rohingya refugees](https://www.informationisbeautifulawards.com/showcase/5529-abandoned-at-sea-the-desperate-journeys-of-rohingya-refugees) | Gold | web story (kontinentalist.com/stories) | off: interactive/web story |
| IIB:020 | 2022 | [The perfect storm](https://www.informationisbeautifulawards.com/showcase/5701-the-perfect-storm) | Bronze | Reuters web graphics story | off: interactive/web story |
| IIB:021 | 2022 | [The first 100 days of protests rocking Hong Kong](https://www.informationisbeautifulawards.com/showcase/5645-the-first-100-days-of-protests-rocking-hong-kong) | Silver | SCMP multimedia web article | off: interactive/web story |
| IIB:022 | 2022 | [Made to Measure](https://www.informationisbeautifulawards.com/showcase/5490-made-to-measure) | Gold | "interactive story" | off: interactive/web story |
| IIB:023 | 2022 | [Sweet & Slim, Greasy & Grim: The Physical Traits that Define Men & Women in Literature](https://www.informationisbeautifulawards.com/showcase/5419-sweet-slim-greasy-grim-the-physical-traits-that-define-men-women-in-literature) | Silver | pudding.cool web story | off: interactive/web story |
| IIB:024 | 2022 | [MTA Ridership Changes due to Covid-19](https://www.informationisbeautifulawards.com/showcase/5554-mta-ridership-changes-due-to-covid-19) | Gold | web data-driven narrative (projects.two-n.com) | off: interactive/web story |
| IIB:025 | 2022 | [Metroverse - The Growth Lab’s Urban Economy Navigator](https://www.informationisbeautifulawards.com/showcase/5371-metroverse-the-growth-lab-s-urban-economy-navigator) | Silver | "urban economy navigator" web tool | off: dashboard/tool/web app |
| IIB:026 | 2022 | [The threatened tribe](https://www.informationisbeautifulawards.com/showcase/4850-the-threatened-tribe) | Silver | Reuters web graphics story | off: interactive/web story |
| IIB:027 | 2022 | [What Spotify data show about the decline of English](https://www.informationisbeautifulawards.com/showcase/5164-what-spotify-data-show-about-the-decline-of-english) | Silver | economist.com/interactive article | off: interactive/web story |
| IIB:028 | 2022 | [Privacy Preserving Proximity Tracing](https://www.informationisbeautifulawards.com/showcase/5362-privacy-preserving-proximity-tracing) | Silver | "interactive and animated network visualisations" | off: interactive/web story |
| IIB:029 | 2022 | [The star of our work](https://www.informationisbeautifulawards.com/showcase/4880-the-star-of-our-work) | Gold | printed greeting card, one composition (preview = the card) | **on-topic** |
| IIB:030 | 2022 | [K-Means Clustering: An Explorable Explainer](https://www.informationisbeautifulawards.com/showcase/5767-k-means-clustering-an-explorable-explainer) | Silver | "interactive article", scrollytelling | off: interactive/web story |
| IIB:031 | 2023 | [On Upward Mobility](https://www.informationisbeautifulawards.com/showcase/5888-on-upward-mobility) | Gold | pudding.cool web data story | off: interactive/web story |
| IIB:032 | 2023 | [HR Cross Functional Mobility](https://www.informationisbeautifulawards.com/showcase/6347-hr-cross-functional-mobility) | Bronze | Tableau series of Sankey charts (dashboard) | off: dashboard/tool/web app |
| IIB:033 | 2023 | [My digital double and me](https://www.informationisbeautifulawards.com/showcase/6301-my-digital-double-and-me) | Silver | framed acrylic print photographed hanging in an exhibition; preview is an installation photo (BORDERLINE: a single print) | off: physical object/installation |
| IIB:034 | 2023 | [Wrenching open the black box](https://www.informationisbeautifulawards.com/showcase/6605-wrenching-open-the-black-box) | Bronze | web story with 3D animation cold open | off: interactive/web story |
| IIB:035 | 2023 | [Ripple Effect](https://www.informationisbeautifulawards.com/showcase/6320-ripple-effect) | Gold | "art installation" water/sound/light | off: physical object/installation |
| IIB:036 | 2023 | [Say "Cheese" with your Chart](https://www.informationisbeautifulawards.com/showcase/5934-say-cheese-with-your-chart) | Gold | book, 74 charts | off: series/book/multi-page |
| IIB:037 | 2023 | [LeBron James has captured the scoring title. We visualized every shot.](https://www.informationisbeautifulawards.com/showcase/6293-lebron-james-has-captured-the-scoring-title-we-visualized-every-shot) | Gold | USA Today in-depth web graphics | off: interactive/web story |
| IIB:038 | 2023 | [And the Earth shakes](https://www.informationisbeautifulawards.com/showcase/6089-and-the-earth-shakes) | Silver | web page (…foldrengesatlasz.html); preview is a title screen | off: interactive/web story |
| IIB:039 | 2023 | [Football legend Pele’s greatest achievements](https://www.informationisbeautifulawards.com/showcase/6380-football-legend-pele-s-greatest-achievements) | Silver | SCMP multimedia web article | off: interactive/web story |
| IIB:040 | 2023 | [Traditional Chinese Color Libraries Browser](https://www.informationisbeautifulawards.com/showcase/6353-traditional-chinese-color-libraries-browser) | Silver | colour-library browser (web tool) | off: dashboard/tool/web app |
| IIB:041 | 2023 | [Journey into sleep](https://www.informationisbeautifulawards.com/showcase/6478-journey-into-sleep) | Silver | Reuters web graphics story | off: interactive/web story |
| IIB:042 | 2023 | [Market Map](https://www.informationisbeautifulawards.com/showcase/6628-market-map) | Silver | web map of the stock market (experimental tool) | off: dashboard/tool/web app |
| IIB:043 | 2023 | [Modern Art Movements](https://www.informationisbeautifulawards.com/showcase/5971-modern-art-movements) | Silver | "interactive timeline" | off: dashboard/tool/web app |
| IIB:044 | 2023 | [This is time for us](https://www.informationisbeautifulawards.com/showcase/5972-this-is-time-for-us) | Bronze | "booklet and poster series" | off: series/book/multi-page |
| IIB:045 | 2023 | [Turkey's toxic dust](https://www.informationisbeautifulawards.com/showcase/6481-turkey-s-toxic-dust) | Gold | Reuters web investigative report | off: interactive/web story |
| IIB:046 | 2023 | [Screens Of August](https://www.informationisbeautifulawards.com/showcase/6426-screens-of-august) | Bronze | "tangible data visualisation" | off: physical object/installation |
| IIB:047 | 2023 | [1 dataset 100 visualizations](https://www.informationisbeautifulawards.com/showcase/6223-1-dataset-100-visualizations) | Bronze | 100 visualisations (series) | off: series/book/multi-page |
| IIB:048 | 2023 | [Fentynal is fast, cheap and deadly](https://www.informationisbeautifulawards.com/showcase/6484-fentynal-is-fast-cheap-and-deadly) | Bronze | Reuters web story, hand-drawn animations | off: interactive/web story |
| IIB:049 | 2023 | [15-minute in-state phone rates increments in U.S state prisons](https://www.informationisbeautifulawards.com/showcase/5975-15-minute-in-state-phone-rates-increments-in-u-s-state-prisons) | Bronze | single static chart image (link is a .png) | **on-topic** |
| IIB:050 | 2023 | [Jesus Christ Superstar](https://www.informationisbeautifulawards.com/showcase/6063-jesus-christ-superstar) | Bronze | "Data-driven poster" | **on-topic** |
| IIB:051 | 2023 | [Britain’s shadowy border](https://www.informationisbeautifulawards.com/showcase/6638-britain-s-shadowy-border) | Gold | cnn.com/interactive story | off: interactive/web story |
| IIB:052 | 2023 | [Atlas of Sustainable Development Goals 2023](https://www.informationisbeautifulawards.com/showcase/6530-atlas-of-sustainable-development-goals-2023) | Gold | "interactive storytelling" atlas (web) | off: interactive/web story |
| IIB:053 | 2023 | [Boreal ablaze](https://www.informationisbeautifulawards.com/showcase/6469-boreal-ablaze) | Bronze | Reuters web graphics story | off: interactive/web story |
| IIB:054 | 2023 | [Die Stadtflucht / The Urban Escape](https://www.informationisbeautifulawards.com/showcase/5910-die-stadtflucht-the-urban-escape) | Silver | zeit.de web article | off: interactive/web story |
| IIB:055 | 2023 | [How do we compare?](https://www.informationisbeautifulawards.com/showcase/6559-how-do-we-compare) | Gold | "interactive dashboard" | off: dashboard/tool/web app |
| IIB:056 | 2023 | [North Korea's missiles](https://www.informationisbeautifulawards.com/showcase/6467-north-korea-s-missiles) | Bronze | Reuters web graphics story | off: interactive/web story |
| IIB:057 | 2023 | [The collapse of insects](https://www.informationisbeautifulawards.com/showcase/6476-the-collapse-of-insects) | Gold | Reuters web graphics story | off: interactive/web story |
| IIB:058 | 2023 | [The Sounds of CDMX](https://www.informationisbeautifulawards.com/showcase/5889-the-sounds-of-cdmx) | Silver | pudding.cool web story (sound) | off: interactive/web story |
| IIB:059 | 2023 | [A Woman's World: Creating spaces for joy, leisure, and resistance in South and Southeast Asia](https://www.informationisbeautifulawards.com/showcase/6232-a-woman-s-world-creating-spaces-for-joy-leisure-and-resistance-in-south-and-southeast-asia) | Silver | web story (kontinentalist.com/stories) | off: interactive/web story |
| IIB:060 | 2024 | [Hello From The Data Vandals (or free as air and water, or whatsoever things are true)](https://www.informationisbeautifulawards.com/showcase/7407-hello-from-the-data-vandals-or-free-as-air-and-water-or-whatsoever-things-are-true) | Bronze | exhibition: sculpture, performance | off: physical object/installation |
| IIB:061 | 2024 | [Databeads](https://www.informationisbeautifulawards.com/showcase/7521-databeads) | Silver | bracelets (wearable objects) | off: physical object/installation |
| IIB:062 | 2024 | [Beyond Crisis: Lives Saved](https://www.informationisbeautifulawards.com/showcase/6810-beyond-crisis-lives-saved) | Bronze | "scrollytelling resource" website | off: interactive/web story |
| IIB:063 | 2024 | [Buildings wrapped in solid gasoline](https://www.informationisbeautifulawards.com/showcase/7037-buildings-wrapped-in-solid-gasoline) | Bronze | Reuters web graphics article | off: interactive/web story |
| IIB:064 | 2024 | [Zoonotic Web](https://www.informationisbeautifulawards.com/showcase/7158-zoonotic-web) | Gold | "interactive project" | off: dashboard/tool/web app |
| IIB:065 | 2024 | [Moody's - Office Vacancies Data Story](https://www.informationisbeautifulawards.com/showcase/7225-moody-s-office-vacancies-data-story) | Gold | Moody's web data story | off: interactive/web story |
| IIB:066 | 2024 | [Lives in limbo: struggles of asylum seekers in Hong Kong](https://www.informationisbeautifulawards.com/showcase/7167-lives-in-limbo-struggles-of-asylum-seekers-in-hong-kong) | Bronze | SCMP multimedia web article | off: interactive/web story |
| IIB:067 | 2024 | [Swiss Mountains · Schweizer Bergwelten · Montagnes suisses](https://www.informationisbeautifulawards.com/showcase/6972-swiss-mountains-schweizer-bergwelten-montagnes-suisses) | Gold | 200-page book | off: series/book/multi-page |
| IIB:068 | 2024 | [The world’s hunger watchdog warned of catastrophe in Sudan. Famine struck anyway.](https://www.informationisbeautifulawards.com/showcase/7241-the-world-s-hunger-watchdog-warned-of-catastrophe-in-sudan-famine-struck-anyway) | Gold | Reuters web graphics story | off: interactive/web story |
| IIB:069 | 2024 | [Vertical Momentum: High Jump & Pole Vault](https://www.informationisbeautifulawards.com/showcase/7194-vertical-momentum-high-jump-pole-vault) | Silver | "animated data visualizations" | off: video/animation |
| IIB:070 | 2024 | [Gaza Lives: Resisting Cultural Genocide](https://www.informationisbeautifulawards.com/showcase/6939-gaza-lives-resisting-cultural-genocide) | Bronze | web story in three chapters (kontinentalist) | off: interactive/web story |
| IIB:071 | 2024 | [World in Tangible Fragments](https://www.informationisbeautifulawards.com/showcase/7536-world-in-tangible-fragments) | Gold | sketchbook, one story per page (series, physical) | off: series/book/multi-page |
| IIB:072 | 2024 | [Moody's - 10 Major Risks Shaping Insurance Today Data Story](https://www.informationisbeautifulawards.com/showcase/7224-moody-s-10-major-risks-shaping-insurance-today-data-story) | Bronze | Moody's web data story | off: interactive/web story |
| IIB:073 | 2024 | [Pathways to Prosperity for Adolescent Girls in Africa.](https://www.informationisbeautifulawards.com/showcase/7058-pathways-to-prosperity-for-adolescent-girls-in-africa) | Silver | web storytelling (a3.popcouncil.org) | off: interactive/web story |
| IIB:074 | 2024 | [Material Interactions: Data-Driven Community Quilting](https://www.informationisbeautifulawards.com/showcase/7043-material-interactions-data-driven-community-quilting) | Silver | community-made patchwork quilts | off: physical object/installation |
| IIB:075 | 2024 | [Total Eclipse](https://www.informationisbeautifulawards.com/showcase/6846-total-eclipse) | Bronze | single static map poster (preview = the map) | **on-topic** |
| IIB:076 | 2024 | [This is a Teenager](https://www.informationisbeautifulawards.com/showcase/7177-this-is-a-teenager) | Gold | pudding.cool web story | off: interactive/web story |
| IIB:077 | 2024 | [Visual Aids for a Survey on Child Nutrition in Telangana](https://www.informationisbeautifulawards.com/showcase/7010-visual-aids-for-a-survey-on-child-nutrition-in-telangana) | Silver | "set of visual aids" | off: series/book/multi-page |
| IIB:078 | 2024 | ['Building a Climate Conscious India': Conscious Trends Report, 2024](https://www.informationisbeautifulawards.com/showcase/7014-building-a-climate-conscious-india-conscious-trends-report-2024) | Silver | 100-page report | off: series/book/multi-page |
| IIB:079 | 2024 | [Navigate the obstacles to transportation electrification.](https://www.informationisbeautifulawards.com/showcase/7179-navigate-the-obstacles-to-transportation-electrification) | Silver | radio-canada web article | off: interactive/web story |
| IIB:080 | 2024 | [Singapore's divisive ethnic-based housing policy](https://www.informationisbeautifulawards.com/showcase/6912-singapore-s-divisive-ethnic-based-housing-policy) | Bronze | web story (kontinentalist) | off: interactive/web story |
| IIB:081 | 2024 | [Ukraine Regional Response: Needs, Intentions, and Border Crossings Dashboard](https://www.informationisbeautifulawards.com/showcase/7364-ukraine-regional-response-needs-intentions-and-border-crossings-dashboard) | Silver | "dashboard" | off: dashboard/tool/web app |
| IIB:082 | 2024 | [Accelerating the Dairy Cold Chain’s Transition to Renewable Energy in India](https://www.informationisbeautifulawards.com/showcase/7436-accelerating-the-dairy-cold-chain-s-transition-to-renewable-energy-in-india) | Silver | "interactive storytelling" digital story | off: interactive/web story |
| IIB:083 | 2024 | [Beyond the Score - Wynton Marsalis' Musical Legacy Visualized](https://www.informationisbeautifulawards.com/showcase/7422-beyond-the-score-wynton-marsalis-musical-legacy-visualized) | Bronze | book | off: series/book/multi-page |
| IIB:084 | 2024 | [How the 2024 U.S. election was decided, vote by vote](https://www.informationisbeautifulawards.com/showcase/7396-how-the-2024-u-s-election-was-decided-vote-by-vote) | Silver | washingtonpost.com interactive 3D mapping | off: interactive/web story |
| IIB:085 | 2024 | [Is the Love Song Dying?](https://www.informationisbeautifulawards.com/showcase/7176-is-the-love-song-dying) | Gold | pudding.cool web story | off: interactive/web story |
| IIB:086 | 2024 | [I Want a Better Catastrophe: A Flowchart for Navigating our Climate Predicament](https://www.informationisbeautifulawards.com/showcase/7487-i-want-a-better-catastrophe-a-flowchart-for-navigating-our-climate-predicament) | Gold | flowchart with audio narration and interactive elements (web) | off: interactive/web story |
| IIB:087 | 2024 | [A Six-Foot Tall Cubical Dataviz Exhibit For Google News Summit](https://www.informationisbeautifulawards.com/showcase/7358-a-six-foot-tall-cubical-dataviz-exhibit-for-google-news-summit) | Silver | six-foot physical exhibit | off: physical object/installation |
| IIB:088 | 2024 | [Aguayos: Exploring the Beauty of Migratory Flows within Latin America and the Caribbean](https://www.informationisbeautifulawards.com/showcase/7588-aguayos-exploring-the-beauty-of-migratory-flows-within-latin-america-and-the-caribbean) | (none shown) | web project (aguayos.netlify.app) | off: interactive/web story |
| IIB:089 | 2024 | [Games of two eras](https://www.informationisbeautifulawards.com/showcase/7166-games-of-two-eras) | Bronze | SCMP multimedia web article | off: interactive/web story |
| IIB:090 | 2024 | [A torrent of trash](https://www.informationisbeautifulawards.com/showcase/7142-a-torrent-of-trash) | Bronze | Reuters web graphics story | off: interactive/web story |
| IIB:091 | 2024 | [What’s driving up burger prices?](https://www.informationisbeautifulawards.com/showcase/7147-what-s-driving-up-burger-prices) | Silver | abc.net.au web article, rotating photography | off: interactive/web story |
| IIB:092 | 2024 | [The Birdsong of Sorrow above Ukraine](https://www.informationisbeautifulawards.com/showcase/7590-the-birdsong-of-sorrow-above-ukraine) | Gold | web artistic visualisation (github.io site) | off: interactive/web story |
| IIB:093 | 2024 | [The Roots of Racism](https://www.informationisbeautifulawards.com/showcase/7437-the-roots-of-racism) | Silver | "interactive data story" | off: interactive/web story |
| IIB:094 | 2024 | [Seeking shadow. A cool fix for hot cities](https://www.informationisbeautifulawards.com/showcase/6995-seeking-shadow-a-cool-fix-for-hot-cities) | Silver | web atlas story (atlas.urbi.ae) | off: interactive/web story |

## I.4 On-topic items: corroboration only (feature codes for information, NOT counted)
Coded from the full-size IIB preview, which was downloaded to the system temp dir and never into the repo. Identity per §4 is `columns|heading|colour|header`. Density uses the poster/flyer/infographic rule. Contrast is `lib/color.contrast_ratio` on hexes sampled from the preview; these are estimates (82a C9).

| id | item | columns | head | body | colour | header | rules | dens | adm (information) | note | preview |
|---|---|---|---|---|---|---|---|---|---|---|---|
| IIB:029 | The star of our work (Voilà:, 2022, Gold) | 1 | sans | sans | fill-blocks | image-hero | rules | airy | y | Full-page near-black ground #101920 (L=0.09) → fill-blocks. The radial chart intersects the top 20% and covers ≥30% of the page → image-hero (82a C1). White on #101920 = 17.8:1 | https://iibawards-prod.s3.amazonaws.com/projects/images/000/004/880/large.jpg |
| IIB:049 | 15-minute in-state phone rates increments in U.S state prisons (2023, Bronze) | grid | serif | serif | multi | plain-left | rules | standard | y | 50 state small multiples → grid. Cream page #fbfbe1 has L=0.93 > 0.90, so it is paper, not a fill (82a C17). Green lines plus pink marks → multi. Serif title top-left with the legend to its right; the dotted separators are not full-width → plain-left | https://iibawards-prod.s3.amazonaws.com/projects/images/000/005/975/large.png |
| IIB:050 | Jesus Christ Superstar (2023, Bronze) | 1 | serif | mono | fill-blocks | image-hero | none | airy | **n — A6** | Full-page grey #8f8f8f (L=0.56) → fill-blocks. The crystal illustration intersects the top 20% and covers ≥30% of the page → image-hero. The small white mono song labels on #8f8f8f measure **3.23:1 < 4.5** → A6. The italic serif title is display-size | https://iibawards-prod.s3.amazonaws.com/projects/images/000/006/063/large.jpg |
| IIB:075 | Total Eclipse (2024, Bronze) | 1 | sans | sans | fill-blocks | image-hero | none | standard | **n — A3** | Full-bleed red-brown gradient ground (#734420 → #711d00) → fill-blocks (gradients count, C17). The map intersects the top 20% and covers ≥30% → image-hero. The explanatory text block (bottom right) and the lyric text around the border sit directly on the gradient → A3 (82a C8) | https://iibawards-prod.s3.amazonaws.com/projects/images/000/006/846/large.png |

Observation only, not a rate: 3 of 4 are image-hero, 3 of 4 are fill-blocks (dark or grey full-page grounds), and 2 of 4 are admissible. These are bespoke editorial graphics, not templates (82b §3 caveat).

## I.5 Bias statement
IIB winners are juried data-visualisation work (Data Visualization Society). Newsroom and agency **web** work dominates: Reuters, SCMP, pudding.cool, ABC and Kontinentalist account for most of the 60 web stories out of 94 winners. The static, print-like share is small (4/94 = 4%), so IIB is a poor population for a print infographic family. The awards are English-dominant. Point in time: 2026-09-23. A jury's choice is not quality (§13).

## I.6 Shortfall and handoff (for the orchestrator)
- The A2 floor (≥10 on-topic codeable winners) is **not met**: 4.
- The 82b fallback (2021) has no input, because there is no 2021 edition.
- A possible next step **needs an orchestrator ruling**, since 82b authorises only 2021: apply the same test to the 2019, 2018 and 2017 editions (same URL pattern; the edition selector lists them). At the 2022-2024 on-topic rate (4/94), an edition of about 30 winners adds about 1 item, so reaching 10 would take about 6 more editions. This is an extrapolation from the observed rate, not a count.
- The other sources for this family (82b §3) are MS PowerPoint infographic-maker (3) and LO 99332 (1). Both are corroboration only (<10) and were not re-fetched here.
- The items file `infographic-items-iib.csv` holds the 4 on-topic items (id, name, url, preview_url), ready in case the orchestrator extends the pool. With no pool, a second coder has nothing to sample.

## I.7 Orchestrator ruling (2026-09-24), recorded BEFORE any older edition is fetched
Pre-registered by the orchestrator: extend the IIB A2 pool **backwards one edition at a time**, in the order 2019, 2018, 2017 … 2012. Apply the same "single static composition" test (I.2) to every winner of each edition, and **STOP at the end of the first edition where the pooled on-topic count reaches ≥10**. No cherry-picking within an edition: every winner of an edition is classified before the stopping check. Disclosure: older editions may reflect dated styles. Scheduled after the rest of this task (proposal, report, flyer/poster recount, memo, form). Results go in I.8.


## I.8 Backward extension under the I.7 ruling (Design Researcher 3, 2026-09-24): **pool reached at 2018, N = 12**

**This section supersedes the "NOT a pool" result above and the information-only codes in I.4.** The I.7 ruling was applied as pre-registered: editions were taken one at a time in the order 2019, then 2018. Every winner of an edition was classified with the unchanged I.2 test before the stop check.

| edition | winners (distinct) | W | D | V | P | S | on-topic | pooled on-topic | stop? |
|---|---|---|---|---|---|---|---|---|---|
| 2022-2024 (I.3) | 94 | 60 | 9 | 5 | 7 | 9 | 4 | 4 | no |
| 2019 | 43 | 25 | 8 | 0 | 3 | 4 | 3 | 7 | no |
| 2018 | 38 | 21 | 6 | 0 | 5 | 1 | 5 | **12** | **yes: ≥10 at the end of 2018** |

Editions 2017 and older were **not fetched**. Sensitivity for the two BORDERLINE 2018 calls: IIB:163 (dead link, decided from the preview) out gives 11; IIB:150 (a web "poster" page with hover) in gives 13. Either way the stop falls at 2018. Disclosure required by the ruling: 2018-2019 winners may reflect dated styles.

**Juried pool (82b A2).** N = 12, Evidence Class `juried`, Ranking Metric `prevalence:award:Information is Beautiful Awards:2018-2024:k/12` (editions 2018, 2019, 2022, 2023, 2024; there were no 2020/2021 editions). Medal level is not used. The pool counts as one corpus in §6. Items file (C11): `infographic-items-iib.csv`, rewritten with the 12 coded items.

### I.8.1 Sources
Same URL pattern and method as I.1: `award=2019` pages 1-2 (30 + 13 cards; page 3 empty) and `award=2018` pages 1-2 (30 + 8; page 3 empty), all HTTP 200, retrieved 2026-09-24. All 81 item pages were fetched for the description, the "See more" target and the full-size preview. For three items the linked page itself was fetched as well: IIB:163's link now redirects to the northeastern.edu home page; IIB:150's page is a React "poster" layout with hover styles; IIB:110's link is a `.mov` capture. Ids continue I.3's fetch order: IIB:095-137 = 2019, IIB:138-175 = 2018.

### I.8.2 Raw list, 2019 (43 winners)

| id | year | item | medal | primary form (from item page) | decision |
|---|---|---|---|---|---|
| IIB:095 | 2019 | [Rich School, Poor School: Australia’s Great Education Divide](https://www.informationisbeautifulawards.com/showcase/3965-rich-school-poor-school-australia-s-great-education-divide) | Bronze | abc.net.au web investigation | off: interactive/web story |
| IIB:096 | 2019 | [A View On Despair](https://www.informationisbeautifulawards.com/showcase/4313-a-view-on-despair) | Gold | "large data-art landscape and accompanying charts"; entrant supplied 3 files (a set) | off: series/book/multi-page |
| IIB:097 | 2019 | [Commute](https://www.informationisbeautifulawards.com/showcase/4203-commute) | Silver | "immersive experience" with sonification (web) | off: interactive/web story |
| IIB:098 | 2019 | [Wedding Data Viz: How We Designed For Feelings](https://www.informationisbeautifulawards.com/showcase/4163-wedding-data-viz-how-we-designed-for-feelings) | Silver | individualised printed wedding badges + network graph (set of objects) | off: physical object/installation |
| IIB:099 | 2019 | [IBM Technology Garden](https://www.informationisbeautifulawards.com/showcase/3948-ibm-technology-garden) | Bronze | "realtime installation" | off: physical object/installation |
| IIB:100 | 2019 | [Visualizing The History Of Fugazi](https://www.informationisbeautifulawards.com/showcase/3905-visualizing-the-history-of-fugazi) | Gold | "A series of visualizations" (fanzine + exhibition prints) | off: series/book/multi-page |
| IIB:101 | 2019 | [Drowning In Plastic: Visualising The World’s Addiction To Plastic Bottles](https://www.informationisbeautifulawards.com/showcase/4009-drowning-in-plastic-visualising-the-world-s-addiction-to-plastic-bottles) | Silver | Reuters web graphics story | off: interactive/web story |
| IIB:102 | 2019 | [Codex Atlanticus](https://www.informationisbeautifulawards.com/showcase/4312-codex-atlanticus) | Gold | "interactive visualization" website/museum | off: dashboard/tool/web app |
| IIB:103 | 2019 | [OneSoil](https://www.informationisbeautifulawards.com/showcase/4417-onesoil) | Bronze | "interactive map" | off: dashboard/tool/web app |
| IIB:104 | 2019 | [How God Has Spoken: Before And After The Silence](https://www.informationisbeautifulawards.com/showcase/4059-how-god-has-spoken-before-and-after-the-silence) | Bronze | book graphics; preview shows 4 separate charts | off: series/book/multi-page |
| IIB:105 | 2019 | [Mercator. It’s A Flat, Flat World](https://www.informationisbeautifulawards.com/showcase/4196-mercator-it-s-a-flat-flat-world) | Silver | "interactive digital special project" | off: interactive/web story |
| IIB:106 | 2019 | [Going Gray](https://www.informationisbeautifulawards.com/showcase/4052-going-gray) | Bronze | Reuters web graphics story | off: interactive/web story |
| IIB:107 | 2019 | [A Visual Introduction To Machine Learning—Part II: Model Tuning And The Bias-Variance Tradeoff](https://www.informationisbeautifulawards.com/showcase/3796-a-visual-introduction-to-machine-learning-part-ii-model-tuning-and-the-bias-variance-tradeoff) | Bronze | scroll-linked animation explainer (r2d3) | off: interactive/web story |
| IIB:108 | 2019 | [Social Credit System: Breathing Scores?](https://www.informationisbeautifulawards.com/showcase/4517-social-credit-system-breathing-scores) | Bronze | student web project (github.io) | off: interactive/web story |
| IIB:109 | 2019 | [Simulation Shows Which Children Are Adopted (And Which Are Not) In Brazil](https://www.informationisbeautifulawards.com/showcase/3793-simulation-shows-which-children-are-adopted-and-which-are-not-in-brazil) | Gold | estadao web simulation | off: interactive/web story |
| IIB:110 | 2019 | [Ahead Of The Fire](https://www.informationisbeautifulawards.com/showcase/3794-ahead-of-the-fire) | Bronze | newspaper web investigation; linked asset is a .mov capture | off: interactive/web story |
| IIB:111 | 2019 | [Earth At Night, Mountains Of Light](https://www.informationisbeautifulawards.com/showcase/4257-earth-at-night-mountains-of-light) | Gold | "3D web mapping experiment" | off: dashboard/tool/web app |
| IIB:112 | 2019 | [China's Muslim Gulag: Turning The Desert Into Detention Camps](https://www.informationisbeautifulawards.com/showcase/4113-china-s-muslim-gulag-turning-the-desert-into-detention-camps) | Silver | Reuters investigates web report | off: interactive/web story |
| IIB:113 | 2019 | [Super Kamiokande](https://www.informationisbeautifulawards.com/showcase/3764-super-kamiokande) | (none shown) | ABC 360-degree digital tour | off: interactive/web story |
| IIB:114 | 2019 | [Plot Parade](https://www.informationisbeautifulawards.com/showcase/3922-plot-parade) | Silver | "experimental chart creator tool" | off: dashboard/tool/web app |
| IIB:115 | 2019 | [3,121 Desperate Journeys: Exposing A Week Of Chaos Under Trump's Zero Tolerance](https://www.informationisbeautifulawards.com/showcase/4322-3-121-desperate-journeys-exposing-a-week-of-chaos-under-trump-s-zero-tolerance) | Bronze | Guardian ng-interactive | off: interactive/web story |
| IIB:116 | 2019 | [All The Ways Of Winning In Sports](https://www.informationisbeautifulawards.com/showcase/3913-all-the-ways-of-winning-in-sports) | Gold | "This infographic comprehensively maps…" one static infographic | **on-topic** |
| IIB:117 | 2019 | [The History Of The Forbidden City: A Visual Explainer](https://www.informationisbeautifulawards.com/showcase/4119-the-history-of-the-forbidden-city-a-visual-explainer) | Silver | SCMP multimedia web package (VR, video) | off: interactive/web story |
| IIB:118 | 2019 | [The Invisible Crime: Are We Failing Victims Of Sexual Violence?](https://www.informationisbeautifulawards.com/showcase/4130-the-invisible-crime-are-we-failing-victims-of-sexual-violence) | Gold | smh.com.au/interactive | off: interactive/web story |
| IIB:119 | 2019 | [Cartographers Of North Korea](https://www.informationisbeautifulawards.com/showcase/4249-cartographers-of-north-korea) | Gold | web project (cartographers-nk.wonyoung.so) | off: interactive/web story |
| IIB:120 | 2019 | [Counting The Cost Of The Education Revolution](https://www.informationisbeautifulawards.com/showcase/3924-counting-the-cost-of-the-education-revolution) | (none shown) | abc.net.au web investigation | off: interactive/web story |
| IIB:121 | 2019 | [Flowmap.blue](https://www.informationisbeautifulawards.com/showcase/3815-flowmap-blue) | Bronze | "flow map visualization tool" | off: dashboard/tool/web app |
| IIB:122 | 2019 | [Legends, One-Club Men And Journeymen](https://www.informationisbeautifulawards.com/showcase/4082-legends-one-club-men-and-journeymen) | Silver | "visual essay … exploratory tool" (web) | off: interactive/web story |
| IIB:123 | 2019 | [10 Years On](https://www.informationisbeautifulawards.com/showcase/4048-10-years-on) | Gold | Reuters web graphics story | off: interactive/web story |
| IIB:124 | 2019 | [Starbucks Data Wall Experience](https://www.informationisbeautifulawards.com/showcase/3845-starbucks-data-wall-experience) | Gold | floor-to-ceiling engraved brass data wall + interactive | off: physical object/installation |
| IIB:125 | 2019 | [Migration Waves](https://www.informationisbeautifulawards.com/showcase/4191-migration-waves) | Gold | National Geographic magazine infographic, one spread ("This infographic is entitled Migration Waves") | **on-topic** |
| IIB:126 | 2019 | [Tour De Drugs - Data Narrative](https://www.informationisbeautifulawards.com/showcase/4364-tour-de-drugs-data-narrative) | Gold | web narrative UI (navigation tabs, timeline); 6 files | off: dashboard/tool/web app |
| IIB:127 | 2019 | [How Life Has Changed For People Your Age](https://www.informationisbeautifulawards.com/showcase/3757-how-life-has-changed-for-people-your-age) | (none shown) | abc.net.au web story | off: interactive/web story |
| IIB:128 | 2019 | [How Kerala’s Dams Failed To Prevent Catastrophe](https://www.informationisbeautifulawards.com/showcase/3966-how-kerala-s-dams-failed-to-prevent-catastrophe) | Gold | Reuters web graphics ("series of data visualisations") | off: interactive/web story |
| IIB:129 | 2019 | [What People In Switzerland Worry About](https://www.informationisbeautifulawards.com/showcase/4304-what-people-in-switzerland-worry-about) | Silver | swissinfo web article | off: interactive/web story |
| IIB:130 | 2019 | [Market Cafe Magazine - A Zine About Data Visualization](https://www.informationisbeautifulawards.com/showcase/4224-market-cafe-magazine-a-zine-about-data-visualization) | Gold | a magazine (periodical) | off: series/book/multi-page |
| IIB:131 | 2019 | [Explore The Ocean – Interactive Scientific Poster](https://www.informationisbeautifulawards.com/showcase/3978-explore-the-ocean-interactive-scientific-poster) | Gold | "interactive scientific poster" on a multi-touch display | off: dashboard/tool/web app |
| IIB:132 | 2019 | [The Millions Who Left](https://www.informationisbeautifulawards.com/showcase/4025-the-millions-who-left) | Silver | zeit.de web article | off: interactive/web story |
| IIB:133 | 2019 | [How Hard Is It To Make A Believable Deepfake?](https://www.informationisbeautifulawards.com/showcase/3779-how-hard-is-it-to-make-a-believable-deepfake) | (none shown) | abc.net.au web story (video) | off: interactive/web story |
| IIB:134 | 2019 | [She Said More](https://www.informationisbeautifulawards.com/showcase/4245-she-said-more) | Silver | nesta web data story | off: interactive/web story |
| IIB:135 | 2019 | [Plastic Profusion](https://www.informationisbeautifulawards.com/showcase/4192-plastic-profusion) | Gold | National Geographic magazine graphic, one page ("The graphic shows…") | **on-topic** |
| IIB:136 | 2019 | [The Irregular Outfields Of Baseball](https://www.informationisbeautifulawards.com/showcase/3770-the-irregular-outfields-of-baseball) | Bronze | thedataface web story | off: interactive/web story |
| IIB:137 | 2019 | [Live BMX Data Visualization](https://www.informationisbeautifulawards.com/showcase/4212-live-bmx-data-visualization) | Gold | live data-visualisation platform | off: dashboard/tool/web app |

### I.8.3 Raw list, 2018 (38 winners)

| id | year | item | medal | primary form (from item page) | decision |
|---|---|---|---|---|---|
| IIB:138 | 2018 | [30°](https://www.informationisbeautifulawards.com/showcase/3199-30) | (none shown) | "in the form of an installation" (translucent surfaces 3×4 m) | off: physical object/installation |
| IIB:139 | 2018 | [Shifting Gears: Visualizing Cycle Rides](https://www.informationisbeautifulawards.com/showcase/3204-shifting-gears-visualizing-cycle-rides) | (none shown) | single static poster (classroom visualisation project, one sheet) | **on-topic** |
| IIB:140 | 2018 | [Women's Pockets are Inferior](https://www.informationisbeautifulawards.com/showcase/3250-women-s-pockets-are-inferior) | Bronze | pudding.cool web story | off: interactive/web story |
| IIB:141 | 2018 | [Satellites: 60 Years In Orbit](https://www.informationisbeautifulawards.com/showcase/3035-satellites-60-years-in-orbit) | (none shown) | "interactive 3D-map" | off: dashboard/tool/web app |
| IIB:142 | 2018 | [Frames of Mind](https://www.informationisbeautifulawards.com/showcase/3231-frames-of-mind) | Gold | National Geographic magazine infographic, one spread | **on-topic** |
| IIB:143 | 2018 | [What Happens To The Plastic We Throw Out](https://www.informationisbeautifulawards.com/showcase/3504-what-happens-to-the-plastic-we-throw-out) | Gold | National Geographic web interactive (preview shows "DRAG TO SEE MORE") | off: interactive/web story |
| IIB:144 | 2018 | [The Long Run](https://www.informationisbeautifulawards.com/showcase/3112-the-long-run) | Bronze | "physical dataviz installation" (marble runs; video) | off: physical object/installation |
| IIB:145 | 2018 | [Good Dogs](https://www.informationisbeautifulawards.com/showcase/3388-good-dogs) | (none shown) | Reuters web graphics story | off: interactive/web story |
| IIB:146 | 2018 | [Artificial Senses](https://www.informationisbeautifulawards.com/showcase/3467-artificial-senses) | Bronze | web project (artificial-senses.kimalbrecht.com) | off: interactive/web story |
| IIB:147 | 2018 | [The Myth of the Criminal Immigrant](https://www.informationisbeautifulawards.com/showcase/3424-the-myth-of-the-criminal-immigrant) | Silver | Marshall Project web visual piece | off: interactive/web story |
| IIB:148 | 2018 | [Trump's Trade War](https://www.informationisbeautifulawards.com/showcase/3113-trump-s-trade-war) | Bronze | "Infographic designed for La Repubblica newspaper": one printed newspaper page/spread | **on-topic** |
| IIB:149 | 2018 | [Dynamic Planet Interactive Scientific Poster](https://www.informationisbeautifulawards.com/showcase/2728-dynamic-planet-interactive-scientific-poster) | Silver | "Interactive Scientific Poster" (digital display) | off: dashboard/tool/web app |
| IIB:150 | 2018 | [A Night Under The Stars](https://www.informationisbeautifulawards.com/showcase/2873-a-night-under-the-stars) | Bronze | web page styled as a poster with hover states (jordan-vincent.com; CSS classes .poster-header, hover). BORDERLINE | off: interactive/web story |
| IIB:151 | 2018 | [What Lies in Irma’s Path](https://www.informationisbeautifulawards.com/showcase/3435-what-lies-in-irma-s-path) | Silver | fivethirtyeight web article, "two maps and a chart" | off: interactive/web story |
| IIB:152 | 2018 | [M U L T I P L I C I T Y](https://www.informationisbeautifulawards.com/showcase/3427-m-u-l-t-i-p-l-i-c-i-t-y) | Gold | "interactive installation" | off: physical object/installation |
| IIB:153 | 2018 | [Reimagine the Game](https://www.informationisbeautifulawards.com/showcase/3442-reimagine-the-game) | Gold | economist.com web experience | off: interactive/web story |
| IIB:154 | 2018 | [Physical Diagram - Interventions In Public Space](https://www.informationisbeautifulawards.com/showcase/2820-physical-diagram-interventions-in-public-space) | (none shown) | physical diagram interventions in public space | off: physical object/installation |
| IIB:155 | 2018 | [DayDohViz](https://www.informationisbeautifulawards.com/showcase/3267-daydohviz) | Silver | Play-Doh physical visualisations (daily series) | off: physical object/installation |
| IIB:156 | 2018 | [Coins - A Journey Through a Rich Cultural Collection](https://www.informationisbeautifulawards.com/showcase/3155-coins-a-journey-through-a-rich-cultural-collection) | Silver | web collection browser | off: dashboard/tool/web app |
| IIB:157 | 2018 | [Rape In India](https://www.informationisbeautifulawards.com/showcase/3321-rape-in-india) | Silver | web visual enquiry (github.io) | off: interactive/web story |
| IIB:158 | 2018 | [From Data to Viz](https://www.informationisbeautifulawards.com/showcase/2727-from-data-to-viz) | Bronze | web decision-tree guide (data-to-viz.com) | off: dashboard/tool/web app |
| IIB:159 | 2018 | [Streetscapes - Mozart, Marx and a Dictator](https://www.informationisbeautifulawards.com/showcase/3135-streetscapes-mozart-marx-and-a-dictator) | Bronze | zeit.de web feature | off: interactive/web story |
| IIB:160 | 2018 | [What Happened to All the Jobs Trump Promised?](https://www.informationisbeautifulawards.com/showcase/3487-what-happened-to-all-the-jobs-trump-promised) | (none shown) | ProPublica web graphics | off: interactive/web story |
| IIB:161 | 2018 | [Mass Exodus](https://www.informationisbeautifulawards.com/showcase/3356-mass-exodus) | Bronze | Reuters web graphics | off: interactive/web story |
| IIB:162 | 2018 | [Casting Shakespeare](https://www.informationisbeautifulawards.com/showcase/3282-casting-shakespeare) | Bronze | web narrative + explorable (ericwilliamlin.com) | off: interactive/web story |
| IIB:163 | 2018 | [Simulated Dendrochronology of U.S. Immigration  1790-2016](https://www.informationisbeautifulawards.com/showcase/3312-simulated-dendrochronology-of-u-s-immigration-1790-2016) | Gold | single static tree-ring composition; the linked page now redirects to northeastern.edu home (dead), so decided from the description and preview. BORDERLINE | **on-topic** |
| IIB:164 | 2018 | [What 1.2 million parliamentary speeches can teach us about gender representation](https://www.informationisbeautifulawards.com/showcase/3222-what-1-2-million-parliamentary-speeches-can-teach-us-about-gender-representation) | Silver | pudding.cool web story | off: interactive/web story |
| IIB:165 | 2018 | [Life in the Camps](https://www.informationisbeautifulawards.com/showcase/3357-life-in-the-camps) | Gold | Reuters web graphics | off: interactive/web story |
| IIB:166 | 2018 | [Historia De Zainab](https://www.informationisbeautifulawards.com/showcase/3492-historia-de-zainab) | (none shown) | a comic (multi-page) | off: series/book/multi-page |
| IIB:167 | 2018 | [Here’s How America Uses Its Land](https://www.informationisbeautifulawards.com/showcase/3257-here-s-how-america-uses-its-land) | Gold | Bloomberg "scrolling web experience" | off: interactive/web story |
| IIB:168 | 2018 | [Elected Leaders Are Making the World Less Democratic](https://www.informationisbeautifulawards.com/showcase/3262-elected-leaders-are-making-the-world-less-democratic) | Bronze | Bloomberg web graphics | off: interactive/web story |
| IIB:169 | 2018 | [20 Years 20 Titles](https://www.informationisbeautifulawards.com/showcase/3060-20-years-20-titles) | Silver | srf.ch web data story | off: interactive/web story |
| IIB:170 | 2018 | [How the Thai Cave Rescue Mission Unfolded](https://www.informationisbeautifulawards.com/showcase/3343-how-the-thai-cave-rescue-mission-unfolded) | Gold | SCMP multimedia web article | off: interactive/web story |
| IIB:171 | 2018 | [Quartetto Sincronie performing Beethoven op. 74 num. 10](https://www.informationisbeautifulawards.com/showcase/2809-quartetto-sincronie-performing-beethoven-op-74-num-10) | Bronze | single static poster (behance) | **on-topic** |
| IIB:172 | 2018 | [Italia: The Airship Crash Chronicle](https://www.informationisbeautifulawards.com/showcase/3509-italia-the-airship-crash-chronicle) | Silver | "multimedia long read" (TASS) | off: interactive/web story |
| IIB:173 | 2018 | [Chartable. A Blog by Datawrapper.](https://www.informationisbeautifulawards.com/showcase/3194-chartable-a-blog-by-datawrapper) | Silver | a blog | off: dashboard/tool/web app |
| IIB:174 | 2018 | [Kepler.gl](https://www.informationisbeautifulawards.com/showcase/3082-kepler-gl) | Gold | "web-based application" | off: dashboard/tool/web app |
| IIB:175 | 2018 | [Bussed Out: How America Moves Its Homeless](https://www.informationisbeautifulawards.com/showcase/3134-bussed-out-how-america-moves-its-homeless) | Gold | Guardian ng-interactive scrollytelling | off: interactive/web story |

### I.8.4 Coded table: the 12 on-topic items, all coded under research/82a-general.md (§A header, §B colour; D.6)
Coder operationalisations for infographics (stated here, flagged for 82a):
- **Charts are marks, not illustrations.** Data-encoding marks (bars, lines, dots, chart areas, maps of data) are counted as shapes and elements under §B, and they do **not** make `image-hero` under C1. Only pictorial imagery (photos; drawings of objects, people or scenes) is "image/illustration". Under this reading the I.4 codes for IIB:029, 050 and 075 (image-hero there) change to plain-centered, plain-left and plain-left.
- The title is the largest text on the sheet (§A.1), with logos and wordmarks excluded. Mock-up canvases around a sheet are ignored (82a-cv A3).
- Measurements come from `measure.py` on previews scaled to ≤600 px (B1a background; B3 blocks by opening with a square of side 5% of the short side; B4 hue bins).

| id | item | columns | head | body | colour | header | rules | dens | adm | rule | header-note | colour-note | preview |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| IIB:029 | [The star of our work](https://www.informationisbeautifulawards.com/showcase/4880-the-star-of-our-work) | 1 | sans | sans | one-accent | plain-centered | rules | airy | y | - | wordmark "Voilà:" is a logo (excluded); largest remaining text "2021" at the page centre (±5%); the radial chart is data marks, not a pictorial image → not image-hero | bg #101920 (B1a); blocks 1.36%; yellow cluster (30-60°: petal marks ≥0.5% area); thin navy grid lines <2 px achromatic (B2) | https://iibawards-prod.s3.amazonaws.com/projects/images/000/004/880/large.jpg |
| IIB:049 | [15-minute in-state phone rates increments in U.S state prisons](https://www.informationisbeautifulawards.com/showcase/5975-15-minute-in-state-phone-rates-increments-in-u-s-state-prisons) | grid | serif | serif | multi | plain-left | rules | standard | y | - | serif title top-left; dotted legend separators, no full-width rule | bg #fbfbe1 (L 0.93); blocks 0%; green line cluster (60-150°) + pink dot cluster (330-0°) | https://iibawards-prod.s3.amazonaws.com/projects/images/000/005/975/large.png |
| IIB:050 | [Jesus Christ Superstar](https://www.informationisbeautifulawards.com/showcase/6063-jesus-christ-superstar) | 1 | serif | mono | multi | plain-left | none | airy | n | A6 | largest text "JESUS CHRIST SUPERSTAR" bottom-left; crystal chart = data marks → not image-hero | bg #8f8f8f (B1a); blocks 1.86%; red, orange, yellow, cyan, magenta facet clusters | https://iibawards-prod.s3.amazonaws.com/projects/images/000/006/063/large.jpg |
| IIB:075 | [Total Eclipse](https://www.informationisbeautifulawards.com/showcase/6846-total-eclipse) | 1 | sans | sans | fill-blocks | plain-left | none | standard | n | A3 | title "TOTAL ECLIPSE" top-right (align=right); the map is data marks → not image-hero | bg #50051a (modal class of the gradient, B1a); the other gradient zones = blocks 24.48% (gradients count as fills, C17) | https://iibawards-prod.s3.amazonaws.com/projects/images/000/006/846/large.png |
| IIB:116 | [All The Ways Of Winning In Sports](https://www.informationisbeautifulawards.com/showcase/3913-all-the-ways-of-winning-in-sports) | 1 | sans | sans | fill-blocks | plain-left | none | standard | y | - | title "all the ways of winning in sports:" in a black disc at left middle (disc = page black, not a fill); no rule | bg #020202; dark-grey concentric bands = blocks 62.67% | https://iibawards-prod.s3.amazonaws.com/projects/images/000/003/913/large.png |
| IIB:125 | [Migration Waves](https://www.informationisbeautifulawards.com/showcase/4191-migration-waves) | 3+ | serif | sans | fill-blocks | plain-left | none | standard | y | - | title "MIGRATION WAVES" left on the yellow ground; 6+ short text blocks across the top → columns 3+ | bg NatGeo yellow #fecb05 (B1a); black page frame (carries the NatGeo logo, so part of the sheet) + black data shapes = blocks 16.67% | https://iibawards-prod.s3.amazonaws.com/projects/images/000/004/191/large.png |
| IIB:135 | [Plastic Profusion](https://www.informationisbeautifulawards.com/showcase/4192-plastic-profusion) | 1 | serif | serif | multi | plain-left | none | airy | y | - | title "Plastic profusion" left inside the nested bars | bg #fbfbfc; blocks 3.57%; blue/cyan (180-210°), orange (30°) and red (0°) bar clusters | https://iibawards-prod.s3.amazonaws.com/projects/images/000/004/192/large.png |
| IIB:139 | [Shifting Gears: Visualizing Cycle Rides](https://www.informationisbeautifulawards.com/showcase/3204-shifting-gears-visualizing-cycle-rides) | 1 | serif | sans | multi | plain-left | rules | standard | y | - | title "Shifting Gears" top-left; no full-width rule directly below the header block | bg #fcfbf2; blocks 0%; orange (0-30°) + blue (180-210°) mark clusters | https://iibawards-prod.s3.amazonaws.com/projects/images/000/003/204/large.jpg |
| IIB:142 | [Frames of Mind](https://www.informationisbeautifulawards.com/showcase/3231-frames-of-mind) | 1 | sans | serif | fill-blocks | plain-left | none | standard | n | A3 | title "FRAMES OF MIND" in the right text column (align=right) | bg #f1f1f1 (sheet margin); painted treemap areas = blocks 63.88% | https://iibawards-prod.s3.amazonaws.com/projects/images/000/003/231/large.jpg |
| IIB:148 | [Trump's Trade War](https://www.informationisbeautifulawards.com/showcase/3113-trump-s-trade-war) | 3+ | serif | serif | fill-blocks | plain-left | rules | dense | y | - | mock-up on a grey canvas: the canvas is ignored (82a-cv A3). Headline top-left of the left page sits on the pale-blue chart column, which runs the full page height → band (d) fails. The page-top rule has chart labels and a callout between it and the headline → ruled (c) fails | sheet ≈ #ebebeb; blue/red chart bars = blocks 11.18% of the image ≈ 13% of the sheet (canvas excluded) → fill-blocks, BORDERLINE | https://iibawards-prod.s3.amazonaws.com/projects/images/000/003/113/large.jpg |
| IIB:163 | [Simulated Dendrochronology of U.S. Immigration  1790-2016](https://www.informationisbeautifulawards.com/showcase/3312-simulated-dendrochronology-of-u-s-immigration-1790-2016) | 1 | sans | sans | multi | plain-left | none | airy | y | - | no display title on the sheet: largest text = the legend "Immigration to the U.S. 1830-2016" (bottom right) → plain-left | bg #fefefd; stippled rings are not solid fills (blocks 2.12%); pink, blue, green, orange clusters. Year labels on white ring gaps (A3 not hit; BORDERLINE) | https://iibawards-prod.s3.amazonaws.com/projects/images/000/003/312/large.png |
| IIB:171 | [Quartetto Sincronie performing Beethoven op. 74 num. 10](https://www.informationisbeautifulawards.com/showcase/2809-quartetto-sincronie-performing-beethoven-op-74-num-10) | 1 | serif | serif | multi | plain-left | none | airy | y | - | serif title at right-centre of the sheet, left-aligned text block | bg #e8e4e3 (L 0.90); blocks 0%; yellow, purple, red, blue-green clusters | https://iibawards-prod.s3.amazonaws.com/projects/images/000/002/809/large.png |

### I.8.5 Exclusions log
| id | rule | evidence |
|---|---|---|
| IIB:050 | A6 | white mono song labels on #8f8f8f = 3.23:1 (`color.contrast_ratio`) |
| IIB:075 | A3 (C8) | the explanatory text block and the border lyric text sit directly on the gradient |
| IIB:142 | A3 (C8) | "Frames of Mind": the category labels sit directly on the oil-paint-textured treemap areas |

Checked and not excluded: IIB:163 year labels sit on the white gaps between stippled rings (BORDERLINE A3). IIB:029 flower glyphs are data symbols, not decorative repeats (A5). IIB:148 is a newspaper spread with serif headline, serif body and sans chart labels, so it stays within A1 (≤3 families). Infographic has no family fail constraint in §5.

### I.8.6 Frequency (k counts admissible exemplars, C21; N = 12 includes the 3 excluded)
Script output (`pool.py`):

| archetype `columns\|heading\|colour\|header` | k | share = k/12 | exemplars | modes: body ; rules ; density |
|---|---|---|---|---|
| `1\|serif\|multi\|plain-left` | 3 | 3/12 = 0.250 | IIB:135, IIB:139, IIB:171 | serif:2/sans:1 ; none:2/rules:1 ; airy:2/standard:1 |
| `3+\|serif\|fill-blocks\|plain-left` | 2 | 2/12 = 0.167 | IIB:125, IIB:148 | sans:1/serif:1 ; none:1/rules:1 ; standard:1/dense:1 |
| `1\|sans\|one-accent\|plain-centered` | 1 | 1/12 = 0.083 | IIB:029 | sans:1 ; rules:1 ; airy:1 |
| `grid\|serif\|multi\|plain-left` | 1 | 1/12 = 0.083 | IIB:049 | serif:1 ; rules:1 ; standard:1 |
| `1\|sans\|fill-blocks\|plain-left` | 1 | 1/12 = 0.083 | IIB:116 | sans:1 ; none:1 ; standard:1 |
| `1\|sans\|multi\|plain-left` | 1 | 1/12 = 0.083 | IIB:163 | sans:1 ; none:1 ; airy:1 |

N=12 admissible=9 distinct=6 k>=2=2 singletons=4. §4 coarsening needs ≥15 admissible; there are 9 → **not triggered**. Two archetypes have K≥2: `1|serif|multi|plain-left` (3: IIB:135 Plastic profusion, IIB:139 Shifting Gears, IIB:171 Quartetto Sincronie) and `3+|serif|fill-blocks|plain-left` (2: IIB:125 Migration Waves, IIB:148 La Repubblica spread). All other archetypes are singletons. Marginals over the 12: header plain-left 11 / plain-centered 1; heading serif 7 / sans 5.

**Header is near non-discriminating** (11/12 plain-left; 82a C16 reports it and keeps it). Infographic titles are rarely set on a band or under a full-width rule.

### I.8.7 Bias statement (pool)
IIB is juried data-visualisation work, not templates. The 12 on-topic items are 3 National Geographic magazine graphics, 1 newspaper spread (La Repubblica), 1 studio greeting card and 7 independent/student posters. English and European dominated. Web work (106 of 175 winners are W) is off-topic by construction, so the pool reflects IIB's minority of print-like entries. 2018-2019 items may reflect dated styles (ruling disclosure). Rebuilding these as designs reconstructs identity features only (§13; 82b §3 caveat).

### I.8.8 Second coder (82a C10/C11; 82a-general D.6)
Ids (12): IIB:029, 049, 050, 075, 116, 125, 135, 139, 142, 148, 163, 171, in `infographic-items-iib.csv` (preview_url = the IIB full-size image). The sample is drawn by the orchestrator: `random.Random("82:infographic")` over the sorted ids, max(min(10, 12), ⌈0.25·12⌉) = 10. The second coder needs I.8.4's "charts are marks" reading, which is flagged for ratification.
