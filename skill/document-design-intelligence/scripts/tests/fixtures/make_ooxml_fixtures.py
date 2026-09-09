#!/usr/bin/env python3
"""Hand-build minimal sample.docx / sample.pptx fixtures for preflight tests.

python-docx / python-pptx are not available in this environment (checked:
`ModuleNotFoundError`), so these are built directly with `zipfile` — real,
valid-enough OOXML packages exercising exactly the structures preflight.py
inspects: an embedded font (via a real .rels-resolved FontFile-equivalent
reference) alongside a non-embedded one, a table, a header with contact
info absent from the first body paragraph (docx), and an embedded-font-list
entry alongside a plain theme/slide font reference (pptx).

Re-run this script to regenerate the fixtures; both are then committed
alongside it, the same pattern as sample.pdf + sample.html in lib/tests/.
"""
import zipfile
from pathlib import Path

HERE = Path(__file__).parent

_CT = "http://schemas.openxmlformats.org/package/2006/content-types"
_PR = "http://schemas.openxmlformats.org/package/2006/relationships"
_R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
_W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def build_docx(path):
    content_types = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="{_CT}">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Default Extension="odttf" ContentType="application/vnd.openxmlformats-officedocument.obfuscatedFont"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/fontTable.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.fontTable+xml"/>
  <Override PartName="/word/header1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"/>
</Types>"""

    root_rels = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="{_PR}">
  <Relationship Id="rId1" Type="{_R}/officeDocument" Target="word/document.xml"/>
</Relationships>"""

    document_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="{_W}" xmlns:r="{_R}">
  <w:body>
    <w:p><w:r><w:t>Note interne sur les conges</w:t></w:r></w:p>
    <w:tbl>
      <w:tr><w:tc><w:p><w:r><w:t>Cellule</w:t></w:r></w:p></w:tc></w:tr>
    </w:tbl>
    <w:sectPr>
      <w:headerReference w:type="default" r:id="rId2"/>
      <w:cols w:num="1"/>
    </w:sectPr>
  </w:body>
</w:document>"""

    document_rels = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="{_PR}">
  <Relationship Id="rId2" Type="{_R}/header" Target="header1.xml"/>
</Relationships>"""

    header_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:hdr xmlns:w="{_W}">
  <w:p><w:r><w:t>Eng nei Schaff - jane@example.com - Tel 00352 54 66 70</w:t></w:r></w:p>
</w:hdr>"""

    font_table_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:fonts xmlns:w="{_W}" xmlns:r="{_R}">
  <w:font w:name="Calibri">
    <w:embedRegular r:id="rId1" w:fontKey="{{00000000-0000-0000-0000-000000000000}}"/>
  </w:font>
  <w:font w:name="Arial"/>
</w:fonts>"""

    font_table_rels = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="{_PR}">
  <Relationship Id="rId1" Type="{_R}/font" Target="fonts/fontCalibriRegular.odttf"/>
</Relationships>"""

    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types)
        zf.writestr("_rels/.rels", root_rels)
        zf.writestr("word/document.xml", document_xml)
        zf.writestr("word/_rels/document.xml.rels", document_rels)
        zf.writestr("word/header1.xml", header_xml)
        zf.writestr("word/fontTable.xml", font_table_xml)
        zf.writestr("word/_rels/fontTable.xml.rels", font_table_rels)
        zf.writestr("word/fonts/fontCalibriRegular.odttf", b"FAKE-EMBEDDED-FONT-BYTES")


def build_pptx(path):
    content_types = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="{_CT}">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Default Extension="fntdata" ContentType="application/x-fontdata"/>
  <Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>
  <Override PartName="/ppt/slides/slide1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>
</Types>"""

    root_rels = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="{_PR}">
  <Relationship Id="rId1" Type="{_R}/officeDocument" Target="ppt/presentation.xml"/>
</Relationships>"""

    presentation_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
                xmlns:r="{_R}">
  <p:sldIdLst>
    <p:sldId id="256" r:id="rId2"/>
  </p:sldIdLst>
  <p:embeddedFontLst>
    <p:embeddedFont>
      <p:font typeface="EmbeddedFont"/>
      <p:regular r:id="rId3"/>
    </p:embeddedFont>
  </p:embeddedFontLst>
</p:presentation>"""

    presentation_rels = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="{_PR}">
  <Relationship Id="rId2" Type="{_R}/slide" Target="slides/slide1.xml"/>
  <Relationship Id="rId3" Type="{_R}/font" Target="fonts/font1.fntdata"/>
</Relationships>"""

    slide_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
       xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
  <p:cSld>
    <p:spTree>
      <p:sp>
        <p:txBody>
          <a:p><a:r><a:rPr><a:latin typeface="EmbeddedFont"/></a:rPr><a:t>Title</a:t></a:r></a:p>
          <a:p><a:r><a:rPr><a:latin typeface="NotEmbeddedFont"/></a:rPr><a:t>Body</a:t></a:r></a:p>
        </p:txBody>
      </p:sp>
    </p:spTree>
  </p:cSld>
</p:sld>"""

    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types)
        zf.writestr("_rels/.rels", root_rels)
        zf.writestr("ppt/presentation.xml", presentation_xml)
        zf.writestr("ppt/_rels/presentation.xml.rels", presentation_rels)
        zf.writestr("ppt/slides/slide1.xml", slide_xml)
        zf.writestr("ppt/fonts/font1.fntdata", b"FAKE-EMBEDDED-FONT-BYTES")


if __name__ == "__main__":
    build_docx(HERE / "sample.docx")
    build_pptx(HERE / "sample.pptx")
    print(f"wrote {HERE / 'sample.docx'}")
    print(f"wrote {HERE / 'sample.pptx'}")
