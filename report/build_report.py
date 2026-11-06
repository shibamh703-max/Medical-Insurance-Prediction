"""Build the MediPredict project report as a Word document."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from docx.shared import Pt, Inches
from docx.enum.section import WD_SECTION
from docx.enum.text import WD_BREAK

from docx_helpers import (setup_document, Report, add_page_number_footer,
                          set_page_numbering, enable_update_fields, clear_footer)
import front_matter as fm
import ch12, ch3, ch4, ch5, ch67

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "MediPredict_Project_Report.docx")

META = {
    "project": "MediPredict",
    "degree": "Bachelor of Technology",
    "programme": "Computer Science and Engineering",
    "student": "[YOUR NAME]",
    "reg_no": "[YOUR REGISTRATION NUMBER]",
    "guide": "[PROJECT GUIDE NAME]",
    "guide_desig": "Assistant Professor, Department of Computer Science and Engineering",
    "hod": "[HEAD OF DEPARTMENT NAME]",
    "dept": "Department of Computer Science and Engineering",
    "institute": "[YOUR COLLEGE / INSTITUTE NAME]",
    "university": "[AFFILIATED UNIVERSITY NAME]",
    "session": "Academic Session 2025 \u2013 2026",
    "place": "[CITY]",
    "date": "November 2025",
}


def build():
    doc = setup_document()
    r = Report(doc)

    first = doc.sections[0]

    # ---------------------------------------------------- front matter (i - vii)
    fm.cover_page(doc, META)
    r.page_break()
    fm.certificate_page(doc, META)
    r.page_break()
    fm.declaration_page(doc, META)
    r.page_break()
    fm.acknowledgement_page(doc, META)
    r.page_break()
    fm.abstract_page(doc, META)
    r.page_break()
    fm.toc_page(doc)
    r.page_break()
    fm.list_of_figures(doc)
    r.page_break()
    fm.list_of_tables(doc)

    # ------------------------------------------- numbering: roman then arabic
    new_sec = doc.add_section(WD_SECTION.NEW_PAGE)
    new_sec.page_width = first.page_width
    new_sec.page_height = first.page_height
    new_sec.top_margin = first.top_margin
    new_sec.bottom_margin = first.bottom_margin
    new_sec.left_margin = first.left_margin
    new_sec.right_margin = first.right_margin

    # NOTE: after add_section(), doc.sections[0] is the *front-matter* section.
    front = doc.sections[0]
    set_page_numbering(front, "lowerRoman", start=1)
    front.different_first_page_header_footer = True
    add_page_number_footer(front, size=11)          # visible from page ii onward
    clear_footer(front.first_page_footer)           # cover page carries no number

    set_page_numbering(new_sec, "decimal", start=1)
    add_page_number_footer(new_sec, size=11)

    r.skip_pagebreak_next = True

    # ------------------------------------------------------------- chapters
    ch12.chapter1(r)
    ch12.chapter2(r)
    ch3.chapter3(r)
    ch4.chapter4(r)
    ch5.chapter5(r)
    ch67.chapter6(r)
    ch67.chapter7(r)
    ch67.references(r)
    ch67.appendices(r)

    enable_update_fields(doc)
    doc.save(OUT)
    print("saved", OUT)
    print("figures:", len(r.figures), "tables:", len(r.tables))


if __name__ == "__main__":
    build()
