"""Generate research/fixtures/badly-formatted-report.docx.

Test scaffolding for Ruling H (prompt 4 "attach this file" activation test).
Not part of the skill build - lives under research/, which build_zip.py never
walks (see collect_members() in skill/document-design-intelligence/scripts/build_zip.py,
which only rglob()s SKILL_DIR).

Requires python-docx, which is NOT a project dependency. Run in a throwaway venv:
    uv venv /tmp/badreport-venv --python 3.12
    uv pip install --python /tmp/badreport-venv/Scripts/python.exe python-docx
    /tmp/badreport-venv/Scripts/python.exe research/fixtures/make_bad_report.py
"""

from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm, Pt, RGBColor

OUT_PATH = Path(__file__).resolve().parent / "badly-formatted-report.docx"

BULLET_COLORS = [RGBColor(0xCC, 0x00, 0x00), RGBColor(0x00, 0x99, 0x33), RGBColor(0xFF, 0x99, 0x00)]

BODY_PARAGRAPHS = {
    "Executive Summary": [
        "Northwind Fabricators Ltd. closed the third quarter with revenue of $4.82 million, "
        "an increase of 6.1% over the prior quarter. Gross margin held steady at 41.3%, "
        "supported by lower input costs in the Midland production facility and a favorable "
        "shift in product mix toward higher-margin fastener lines.",
        "Management remains cautiously optimistic about Q4 demand, citing a healthy order "
        "backlog of $2.1 million across the Industrial and Consumer segments. The backlog "
        "figure represents the largest quarter-end position in company history, driven in "
        "part by a multi-year supply agreement signed with a regional infrastructure "
        "contractor during the period.",
        "The executive team also completed a review of the company's five-year capital "
        "plan, concluding that the current pace of warehouse automation investment remains "
        "appropriate given projected volume growth. No changes to the plan were proposed "
        "at this time, though the finance committee will revisit assumptions again ahead "
        "of the annual budget cycle.",
    ],
    "Financial Highlights": [
        "Operating expenses rose modestly to $1.36 million, driven by planned increases in "
        "logistics spend ahead of the holiday shipping season. Net income for the quarter was "
        "$612,000, compared to $558,000 in the prior quarter, representing growth of 9.7% "
        "on a sequential basis and 14.2% on a year-over-year basis.",
        "The board approved a continuation of the quarterly dividend at $0.08 per share, "
        "payable to shareholders of record as of the fifteenth of next month. This marks "
        "the eleventh consecutive quarter of stable or increasing dividend payments, a "
        "streak the board reaffirmed as consistent with its long-standing capital return "
        "policy.",
        "Cash and short-term investments stood at $3.4 million at quarter end, down "
        "slightly from $3.6 million in the prior quarter due to seasonal inventory "
        "build ahead of the fourth-quarter shipping window. The company's revolving "
        "credit facility remained undrawn throughout the period.",
    ],
    "Segment Performance": [
        "The Industrial segment contributed $2.9 million in revenue, up 4.4% quarter over "
        "quarter, led by strong demand for structural fasteners used in commercial "
        "construction projects. Unit volumes in this segment increased 5.1%, partially "
        "offset by modest price softening in the mid-tier product tier.",
        "The Consumer segment contributed $1.92 million, roughly flat against the prior "
        "period. Management attributed the flat performance to a temporary slowdown in "
        "big-box retail reorders, which is expected to normalize as retailers rebuild "
        "inventory ahead of the holiday season.",
        "Regional performance was mixed: the Northern territory grew 9%, while the "
        "Southern territory declined 2% amid a temporary distributor transition following "
        "the planned retirement of a long-tenured regional sales partner. A replacement "
        "distributor agreement was finalized in the final week of the quarter and is "
        "expected to restore normal order flow by the start of Q4.",
    ],
    "Outlook": [
        "Management expects full-year revenue to land between $18.6 million and $19.1 million, "
        "assuming no material disruption to raw material supply. Capital expenditure guidance "
        "for the coming year remains unchanged at $1.4 million, primarily for warehouse "
        "automation equipment at the Midland facility.",
        "A detailed risk assessment, including commentary on input cost volatility and "
        "logistics capacity, is provided in the appendix of the full filing. Key risks "
        "identified include continued volatility in steel and resin input costs, potential "
        "freight capacity constraints during peak shipping periods, and general "
        "macroeconomic softness affecting construction spending in certain regions.",
        "The company plans to open a new regional distribution point in the Southeast "
        "during the first half of next year, subject to final site approval. This "
        "expansion is intended to reduce average delivery times to key accounts in that "
        "territory and to support anticipated growth in the Industrial segment.",
    ],
}

HEADING_FONTS = ["Comic Sans MS", "Courier New", "Papyrus"]
BULLETS = [
    "Revenue growth accelerated in the Industrial segment",
    "Logistics costs increased ahead of peak season",
    "Dividend maintained at prior-quarter level",
]


def set_margins(document):
    for section in document.sections:
        section.top_margin = Cm(1)
        section.bottom_margin = Cm(1)
        section.left_margin = Cm(1)
        section.right_margin = Cm(1)


def add_heading(document, text, font_name):
    p = document.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    run.bold = True
    run.font.name = font_name
    run.font.size = Pt(20)
    return p


def add_body(document, text):
    p = document.add_paragraph()
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(10)


def add_bullets(document):
    for i, text in enumerate(BULLETS):
        p = document.add_paragraph(style="List Bullet")
        run = p.add_run(text)
        run.font.color.rgb = BULLET_COLORS[i % len(BULLET_COLORS)]
        run.font.size = Pt(10)
        run.font.name = "Calibri"


def add_garish_chart_placeholder(document):
    # No real chart object inserted (python-docx has no native chart API);
    # a garish default-colored table stands in for a "default-styled chart".
    table = document.add_table(rows=4, cols=3)
    table.style = "Table Grid"
    headers = ["Segment", "Q3 Revenue ($M)", "QoQ Change"]
    rows = [
        ("Industrial", "2.90", "+4.4%"),
        ("Consumer", "1.92", "-0.3%"),
        ("Other", "0.00", "n/a"),
    ]
    for col, text in enumerate(headers):
        cell = table.rows[0].cells[col]
        cell.text = text
        for p in cell.paragraphs:
            for run in p.runs:
                run.bold = True
                run.font.color.rgb = RGBColor(0xFF, 0xFF, 0x00)
    for r, row in enumerate(rows, start=1):
        for c, text in enumerate(row):
            table.rows[r].cells[c].text = text


def build():
    document = Document()
    set_margins(document)

    add_heading(document, "Northwind Fabricators Ltd.", HEADING_FONTS[0])
    add_heading(document, "Q3 Quarterly Business Report", HEADING_FONTS[1])

    for i, (heading, paras) in enumerate(BODY_PARAGRAPHS.items()):
        add_heading(document, heading, HEADING_FONTS[i % len(HEADING_FONTS)])
        for para in paras:
            add_body(document, para)
        if heading == "Financial Highlights":
            add_bullets(document)
            add_garish_chart_placeholder(document)

    document.save(str(OUT_PATH))
    return OUT_PATH


if __name__ == "__main__":
    path = build()
    print(f"wrote {path} ({path.stat().st_size} bytes)")
