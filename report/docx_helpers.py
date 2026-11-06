"""Helper functions for building the MediPredict report with python-docx."""
from docx import Document
from docx.shared import Pt, Inches, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

FONT = "Times New Roman"
ACCENT = RGBColor(0x14, 0x5B, 0x50)      # deep green used in the app
INK = RGBColor(0x00, 0x00, 0x00)


# --------------------------------------------------------------------- fields
def add_field(paragraph, instr, placeholder="1", bold=False, size=11):
    run = paragraph.add_run()
    run.font.name = FONT
    run.font.size = Pt(size)
    run.bold = bold
    r = run._r
    for tag, attr, text in (("w:fldChar", "begin", None),
                            ("w:instrText", None, instr),
                            ("w:fldChar", "separate", None),
                            ("w:t", None, placeholder),
                            ("w:fldChar", "end", None)):
        el = OxmlElement(tag)
        if attr:
            el.set(qn("w:fldCharType"), attr)
        if tag == "w:instrText":
            el.set(qn("xml:space"), "preserve")
        if text is not None:
            el.text = text
        r.append(el)
    return run


def enable_update_fields(doc):
    """Ask Word to refresh the TOC / list of figures when the file is opened."""
    settings = doc.settings.element
    uf = settings.find(qn("w:updateFields"))
    if uf is None:
        uf = OxmlElement("w:updateFields")
        settings.append(uf)
    uf.set(qn("w:val"), "true")


def set_page_numbering(section, fmt="decimal", start=None):
    sectPr = section._sectPr
    pgNumType = sectPr.find(qn("w:pgNumType"))
    if pgNumType is None:
        pgNumType = OxmlElement("w:pgNumType")
        sectPr.append(pgNumType)
    pgNumType.set(qn("w:fmt"), fmt)
    if start is not None:
        pgNumType.set(qn("w:start"), str(start))


def add_page_number_footer(section, size=11):
    section.footer.is_linked_to_previous = False
    p = section.footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    add_field(p, " PAGE ", "1", size=size)


def clear_footer(footer):
    if hasattr(footer, "footer"):
        footer = footer.footer
    footer.is_linked_to_previous = False
    for p in footer.paragraphs:
        for r in list(p.runs):
            r._r.getparent().remove(r._r)


# --------------------------------------------------------------------- styles
def setup_document():
    doc = Document()

    # A4 + 1 inch margins
    for s in doc.sections:
        s.page_width = Cm(21.0)
        s.page_height = Cm(29.7)
        s.top_margin = Inches(1)
        s.bottom_margin = Inches(1)
        s.left_margin = Inches(1)
        s.right_margin = Inches(1)

    # Normal
    normal = doc.styles["Normal"]
    normal.font.name = FONT
    normal.font.size = Pt(12)
    normal.font.color.rgb = INK
    normal.element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
    pf = normal.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    pf.space_before = Pt(0)
    pf.space_after = Pt(6)
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf.widow_control = True

    def heading(name, size, before, after, italic=False, cap=False, page_break=False):
        st = doc.styles[name]
        st.font.name = FONT
        st.font.size = Pt(size)
        st.font.bold = True
        st.font.italic = italic
        st.font.color.rgb = INK
        rpr = st.element.get_or_add_rPr()
        rf = rpr.find(qn("w:rFonts"))
        if rf is None:
            rf = OxmlElement("w:rFonts")
            rpr.append(rf)
        rf.set(qn("w:ascii"), FONT)
        rf.set(qn("w:hAnsi"), FONT)
        rf.set(qn("w:eastAsia"), FONT)
        if cap:
            c = OxmlElement("w:caps")
            rpr.append(c)
        p = st.paragraph_format
        p.space_before = Pt(before)
        p.space_after = Pt(after)
        p.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
        p.keep_with_next = True
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        if page_break:
            p.page_break_before = True
        return st

    heading("Heading 1", 16, 0, 12, page_break=True)
    heading("Heading 2", 14, 14, 8)
    heading("Heading 3", 13, 12, 6)
    heading("Title", 20, 0, 12)

    # caption styles (used by the List of Figures / Tables fields)
    for style_name in ("FigureCaption", "TableCaption"):
        st = doc.styles.add_style(style_name, 1)  # paragraph style
        st.base_style = doc.styles["Normal"]
        st.font.name = FONT
        st.font.size = Pt(11)
        st.font.bold = False
        st.font.italic = False
        st.font.color.rgb = INK
        st.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        st.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
        st.paragraph_format.space_before = Pt(4)
        st.paragraph_format.space_after = Pt(12)
        st.paragraph_format.keep_with_next = False
    return doc


# ---------------------------------------------------------------- content api
class Report:
    def __init__(self, doc):
        self.doc = doc
        self.chapter = 0
        self.fig_no = 0
        self.tab_no = 0
        self.figures = []
        self.tables = []

    # ---------------------------------------------------------------- text
    def p(self, text="", size=12, bold=False, italic=False, align="justify",
          space_after=8, space_before=0, indent_first=0.0, line_spacing=1.5,
          keep_with_next=False, style=None):
        par = self.doc.add_paragraph(style=style)
        run = par.add_run(text)
        run.font.name = FONT
        run.font.size = Pt(size)
        run.bold = bold
        run.italic = italic
        run.font.color.rgb = INK
        pf = par.paragraph_format
        pf.alignment = {"justify": WD_ALIGN_PARAGRAPH.JUSTIFY,
                        "center": WD_ALIGN_PARAGRAPH.CENTER,
                        "left": WD_ALIGN_PARAGRAPH.LEFT,
                        "right": WD_ALIGN_PARAGRAPH.RIGHT}[align]
        pf.space_after = Pt(space_after)
        pf.space_before = Pt(space_before)
        pf.first_line_indent = Inches(indent_first)
        pf.keep_with_next = keep_with_next
        if line_spacing == 1.5:
            pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
        else:
            pf.line_spacing = line_spacing
        return par

    def rich(self, parts, align="justify", size=12, space_after=8, line_spacing=1.5,
             indent_first=0.0):
        """parts = list of (text, bold, italic)."""
        par = self.doc.add_paragraph()
        for text, bold, italic in parts:
            run = par.add_run(text)
            run.font.name = FONT
            run.font.size = Pt(size)
            run.bold = bold
            run.italic = italic
            run.font.color.rgb = INK
        pf = par.paragraph_format
        pf.alignment = {"justify": WD_ALIGN_PARAGRAPH.JUSTIFY,
                        "center": WD_ALIGN_PARAGRAPH.CENTER,
                        "left": WD_ALIGN_PARAGRAPH.LEFT}[align]
        pf.space_after = Pt(space_after)
        pf.first_line_indent = Inches(indent_first)
        if line_spacing == 1.5:
            pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
        else:
            pf.line_spacing = line_spacing
        return par

    def bullets(self, items, size=12, space_after=4):
        for it in items:
            par = self.doc.add_paragraph(style="List Bullet")
            run = par.add_run(it)
            run.font.name = FONT
            run.font.size = Pt(size)
            run.font.color.rgb = INK
            pf = par.paragraph_format
            pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            pf.space_after = Pt(space_after)
            pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE

    def numbers(self, items, size=12, space_after=4):
        """Manually numbered list (avoids Word continuing numbering across chapters)."""
        for i, it in enumerate(items, start=1):
            par = self.doc.add_paragraph()
            run = par.add_run(f"{i}.\t{it}")
            run.font.name = FONT
            run.font.size = Pt(size)
            run.font.color.rgb = INK
            pf = par.paragraph_format
            pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            pf.space_after = Pt(space_after)
            pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
            pf.left_indent = Inches(0.35)
            pf.first_line_indent = Inches(-0.35)
            pf.tab_stops.add_tab_stop(Inches(0.35))

    # ------------------------------------------------------------- headings
    def h1(self, text):
        self.chapter += 1
        self.fig_no = 0
        self.tab_no = 0
        h = self.doc.add_heading(f"{self.chapter}. {text.upper()}", level=1)
        if getattr(self, "skip_pagebreak_next", False):
            h.paragraph_format.page_break_before = False
            self.skip_pagebreak_next = False
        for r in h.runs:
            r.font.name = FONT
            r.font.size = Pt(16)
            r.bold = True
            r.font.color.rgb = INK
        return h

    def h1_raw(self, text, size=16):
        h = self.doc.add_heading(text, level=1)
        for r in h.runs:
            r.font.name = FONT
            r.font.size = Pt(size)
            r.bold = True
            r.font.color.rgb = INK
        return h

    def h2(self, text):
        h = self.doc.add_heading(text, level=2)
        for r in h.runs:
            r.font.name = FONT
            r.font.size = Pt(14)
            r.bold = True
            r.font.color.rgb = INK
        return h

    def h3(self, text):
        h = self.doc.add_heading(text, level=3)
        for r in h.runs:
            r.font.name = FONT
            r.font.size = Pt(13)
            r.bold = True
            r.font.color.rgb = INK
        return h

    # --------------------------------------------------------------- figures
    def figure(self, path, caption, width=6.0):
        width = min(width, 6.2)
        self.fig_no += 1
        number = f"Figure {self.chapter}.{self.fig_no}"
        par = self.doc.add_paragraph()
        par.alignment = WD_ALIGN_PARAGRAPH.CENTER
        par.paragraph_format.space_before = Pt(8)
        par.paragraph_format.space_after = Pt(2)
        par.paragraph_format.keep_with_next = True
        par.add_run().add_picture(path, width=Inches(width))
        cap = self.doc.add_paragraph(f"{number}: {caption}", style="FigureCaption")
        self.figures.append((number, caption))
        return cap

    # ---------------------------------------------------------------- tables
    def table(self, headers, rows, caption, col_widths=None, font_size=11,
              header_fill="D9EEE7", align_center_cols=None, first_col_bold=False):
        self.tab_no += 1
        number = f"Table {self.chapter}.{self.tab_no}"

        cap = self.doc.add_paragraph(f"{number}: {caption}", style="TableCaption")
        cap.paragraph_format.space_before = Pt(10)
        cap.paragraph_format.space_after = Pt(4)
        cap.paragraph_format.keep_with_next = True

        t = self.doc.add_table(rows=1, cols=len(headers))
        t.style = "Table Grid"
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        t.autofit = False

        hdr = t.rows[0]
        hdr.cells  # touch
        for i, h in enumerate(headers):
            cell = hdr.cells[i]
            cell.text = ""
            par = cell.paragraphs[0]
            par.alignment = WD_ALIGN_PARAGRAPH.CENTER
            par.paragraph_format.space_after = Pt(2)
            par.paragraph_format.space_before = Pt(2)
            par.paragraph_format.line_spacing = 1.0
            run = par.add_run(h)
            run.font.name = FONT
            run.font.size = Pt(font_size)
            run.bold = True
            shade(cell, header_fill)
        repeat_header(hdr)

        for row in rows:
            cells = t.add_row().cells
            for i, val in enumerate(row):
                cells[i].text = ""
                par = cells[i].paragraphs[0]
                par.paragraph_format.space_after = Pt(2)
                par.paragraph_format.space_before = Pt(2)
                par.paragraph_format.line_spacing = 1.0
                par.alignment = (WD_ALIGN_PARAGRAPH.CENTER
                                 if (align_center_cols and i in align_center_cols)
                                 else WD_ALIGN_PARAGRAPH.LEFT)
                run = par.add_run(str(val))
                run.font.name = FONT
                run.font.size = Pt(font_size)
                run.font.color.rgb = INK
                if first_col_bold and i == 0:
                    run.bold = True

        if col_widths:
            for row in t.rows:
                for i, w in enumerate(col_widths):
                    row.cells[i].width = Inches(w)

        self.tables.append((number, caption))
        # small gap after the table
        self.doc.add_paragraph().paragraph_format.space_after = Pt(2)
        return t

    def code_block(self, lines, size=9.5):
        t = self.doc.add_table(rows=1, cols=1)
        t.style = "Table Grid"
        cell = t.rows[0].cells[0]
        shade(cell, "F5F5F5")
        cell.text = ""
        first = True
        for line in lines:
            par = cell.paragraphs[0] if first else cell.add_paragraph()
            first = False
            par.paragraph_format.space_after = Pt(0)
            par.paragraph_format.space_before = Pt(0)
            par.paragraph_format.line_spacing = 1.0
            par.alignment = WD_ALIGN_PARAGRAPH.LEFT
            run = par.add_run(line)
            run.font.name = "Consolas"
            run.font.size = Pt(size)
            run.font.color.rgb = RGBColor(0x1B, 0x1B, 0x1B)
        self.doc.add_paragraph().paragraph_format.space_after = Pt(2)
        return t

    def page_break(self):
        from docx.enum.text import WD_BREAK
        self.doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

    def spacer(self, pts=10):
        par = self.doc.add_paragraph()
        par.paragraph_format.space_after = Pt(pts)
        par.paragraph_format.line_spacing = 1.0
        return par


# --------------------------------------------------------------- low-level ooxml
def shade(cell, color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), color)
    tcPr.append(shd)


def repeat_header(row):
    trPr = row._tr.get_or_add_trPr()
    el = OxmlElement("w:tblHeader")
    el.set(qn("w:val"), "true")
    trPr.append(el)


def cant_split(row):
    trPr = row._tr.get_or_add_trPr()
    el = OxmlElement("w:cantSplit")
    trPr.append(el)
