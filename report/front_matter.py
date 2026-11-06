"""Front matter pages for the MediPredict report."""
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

from docx_helpers import FONT, add_field, shade

GREEN = RGBColor(0x14, 0x5B, 0x50)
GREY = RGBColor(0x44, 0x44, 0x44)


def _line(doc, text, size=12, bold=False, italic=False, align="center", space_after=6,
          space_before=0, color=None, caps=False, underline=False, spacing=1.25):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.name = FONT
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    run.font.underline = underline
    run.font.all_caps = caps
    run.font.color.rgb = color if color else RGBColor(0, 0, 0)
    pf = p.paragraph_format
    pf.alignment = {"center": WD_ALIGN_PARAGRAPH.CENTER,
                    "left": WD_ALIGN_PARAGRAPH.LEFT,
                    "right": WD_ALIGN_PARAGRAPH.RIGHT,
                    "justify": WD_ALIGN_PARAGRAPH.JUSTIFY}[align]
    pf.space_after = Pt(space_after)
    pf.space_before = Pt(space_before)
    pf.line_spacing = spacing
    return p


def _hline(doc, width_pct=100, space_before=2, space_after=10, color="145B50", size=8):
    """Horizontal rule drawn as a bottom border on an empty paragraph."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    pPr = p._p.get_or_add_pPr()
    pbdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), str(size))
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), color)
    pbdr.append(bottom)
    pPr.append(pbdr)
    return p


# ------------------------------------------------------------------ cover page
def cover_page(doc, meta):
    _line(doc, meta["project"], size=13, bold=True, space_before=6, space_after=2, caps=True)
    _line(doc, "A PROJECT REPORT", size=12, space_after=1)
    _line(doc, "on", size=12, italic=True, space_after=10)

    _line(doc, "MEDIPREDICT", size=24, bold=True, color=GREEN, space_after=3)
    _line(doc, "Medical Insurance Cost Prediction\nusing Machine Learning", size=14, bold=True,
          space_after=4, spacing=1.3)

    _line(doc, "Submitted in partial fulfilment of the requirements for the award of the degree of",
          size=11, italic=True, space_after=3)
    _line(doc, meta["degree"], size=13, bold=True, space_after=3)
    _line(doc, f"({meta['programme']})", size=12, italic=True, space_after=12)

    _line(doc, "Submitted by", size=11, italic=True, space_after=4)
    _line(doc, meta["student"], size=14, bold=True, space_after=2)
    _line(doc, f"Registration No.: {meta['reg_no']}", size=12, space_after=12)

    _line(doc, "Under the guidance of", size=11, italic=True, space_after=4)
    _line(doc, meta["guide"], size=13, bold=True, space_after=2)
    _line(doc, meta["guide_desig"], size=11.5, space_after=14)

    _line(doc, "DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING",
          size=12, bold=True, space_after=2)
    _line(doc, meta["institute"], size=13, bold=True, color=GREEN, space_after=2)
    _line(doc, meta["university"], size=11, space_after=1)
    _line(doc, meta["session"], size=12, bold=True, space_after=0)


# ---------------------------------------------------------------- certificate
def certificate_page(doc, meta):
    _line(doc, "CERTIFICATE", size=18, bold=True, space_after=6, space_before=0)
    _hline(doc, space_before=0, space_after=20)

    body = (
        f'This is to certify that the project report entitled "MediPredict: Medical Insurance Cost '
        f'Prediction using Machine Learning" is the bona fide work of {meta["student"]} '
        f'(Registration No. {meta["reg_no"]}), a student of {meta["programme"]} in the '
        f'{meta["dept"]}, {meta["institute"]}, during the academic session {meta["session"]}.'
    )
    _line(doc, body, size=12, align="justify", space_after=12, spacing=1.5)

    body2 = (
        "The work has been carried out by him/her under my supervision and guidance, and the "
        "report has not been submitted elsewhere for the award of any other degree or diploma. "
        "To the best of my knowledge, the report is complete in all respects and is worthy of "
        "consideration for evaluation."
    )
    _line(doc, body2, size=12, align="justify", space_after=40, spacing=1.5)

    t = doc.add_table(rows=2, cols=2)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    labels = [
        ("____________________________", "____________________________"),
        ("Signature of the Project Guide", "Signature of the Head of the Department"),
        (meta["guide"], meta["hod"]),
    ]
    cells = t.rows[0].cells
    _cell_line(cells[0], "____________________________", bold=False)
    _cell_line(cells[1], "____________________________", bold=False)
    r2 = t.add_row().cells
    _cell_line(r2[0], "Signature of the Project Guide", bold=True, size=11)
    _cell_line(r2[1], "Signature of the Head of the Department", bold=True, size=11)
    r3 = t.add_row().cells
    _cell_line(r3[0], meta["guide"], bold=False, size=10.5, italic=True)
    _cell_line(r3[1], meta["hod"], bold=False, size=10.5, italic=True)

    doc.add_paragraph().paragraph_format.space_after = Pt(30)
    _line(doc, f"Place: {meta['place']}", size=11, align="left", space_after=2)
    _line(doc, f"Date: {meta['date']}", size=11, align="left", space_after=2)


def _cell_line(cell, text, bold=True, size=11, italic=False):
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(text)
    run.font.name = FONT
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic


# ---------------------------------------------------------------- declaration
def declaration_page(doc, meta):
    _line(doc, "DECLARATION", size=18, bold=True, space_after=6)
    _hline(doc, space_before=0, space_after=20)

    body = (
        f'I hereby declare that the project report entitled "MediPredict: Medical Insurance Cost '
        f'Prediction using Machine Learning", submitted to {meta["institute"]} in partial '
        f'fulfilment of the requirements for the award of the degree of {meta["degree"]} '
        f'({meta["programme"]}), is my own original work.'
    )
    _line(doc, body, size=12, align="justify", space_after=12, spacing=1.5)

    body2 = (
        "I further declare that the dataset used in this work is a publicly available dataset, "
        "and that the analysis, model building, application development and interpretation of "
        "results presented in this report have been carried out by me. The report has not been "
        "submitted, either in part or in full, to any other university or institution for the "
        "award of any degree, diploma or certificate, and it does not contain any material "
        "previously published or written by another person except where due reference has been "
        "made in the text."
    )
    _line(doc, body2, size=12, align="justify", space_after=44, spacing=1.5)

    _line(doc, "____________________________", size=12, align="left", space_after=2)
    _line(doc, meta["student"], size=12, bold=True, align="left", space_after=2)
    _line(doc, f"Registration No.: {meta['reg_no']}", size=11, align="left", space_after=2)
    _line(doc, f"{meta['dept']}, {meta['institute']}", size=11, align="left", space_after=24)
    _line(doc, f"Place: {meta['place']}", size=11, align="left", space_after=2)
    _line(doc, f"Date: {meta['date']}", size=11, align="left", space_after=2)


# -------------------------------------------------------------- acknowledgement
def acknowledgement_page(doc, meta):
    _line(doc, "ACKNOWLEDGEMENT", size=18, bold=True, space_after=6)
    _hline(doc, space_before=0, space_after=20)

    paras = [
        "The completion of this project has been possible only because of the guidance and "
        "support of several people, and I take this opportunity to express my sincere gratitude "
        "to all of them.",

        f"I am deeply grateful to my project guide, {meta['guide']}, {meta['guide_desig']}, for "
        "the continuous encouragement, valuable suggestions and constructive criticism offered "
        "throughout the course of this work. The clarity with which every stage of the project "
        "was reviewed has had a direct influence on the quality of the final outcome.",

        f"I sincerely thank {meta['hod']}, Head of the Department, and the faculty members of "
        f"the {meta['dept']}, {meta['institute']}, for providing the academic environment, "
        "laboratory facilities and moral support needed to carry out this study. I am also "
        "thankful to the examination committee for their valuable time and feedback.",

        "I acknowledge the creators and maintainers of the open-source tools that made this work "
        "possible: the scikit-learn developers for an exceptionally well-documented machine "
        "learning library, the Streamlit team for an accessible application framework, and the "
        "pandas, NumPy, Matplotlib and Seaborn communities. I am equally grateful to Kaggle and "
        "to the anonymous respondents of the original Medical Cost Personal Dataset, without "
        "whose publicly shared data this analysis could not have been performed.",

        "Finally, I thank my family and friends for their patience, constant motivation and "
        "unstinting support during the long hours of development, testing and documentation. Any "
        "shortcomings that remain in this report are entirely my own.",
    ]
    for text in paras:
        _line(doc, text, size=12, align="justify", space_after=12, spacing=1.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(24)
    _line(doc, meta["student"], size=12, bold=True, align="right", space_after=2)


# --------------------------------------------------------------------- abstract
def abstract_page(doc, meta):
    _line(doc, "ABSTRACT", size=18, bold=True, space_after=6)
    _hline(doc, space_before=0, space_after=18)

    paras = [
        "Medical insurance premiums are calculated from the statistical risk profile of an "
        "individual, yet most applicants have no clear idea of how personal attributes such as "
        "age, body mass index and smoking behaviour translate into the amount they are charged. "
        "This project, titled MediPredict, addresses that information gap by building a machine "
        "learning system that estimates annual medical insurance charges from six routinely "
        "collected attributes: age, sex, body mass index, number of dependent children, smoking "
        "status and residential region.",

        "The work uses the publicly available Medical Cost Personal Dataset, which contains 1,338 "
        "records and seven columns. After removing one duplicate record, exploratory data "
        "analysis was carried out with pandas, Matplotlib and Seaborn. Charges were found to be "
        "strongly right-skewed, smoking status alone separated the population into two clearly "
        "distinct cost groups (mean charge of USD 32,050 for smokers against USD 8,441 for "
        "non-smokers), and age and body mass index showed positive correlation with charges. "
        "Three regression algorithms, namely Linear Regression, Decision Tree Regression and "
        "Random Forest Regression, were trained and compared using mean absolute error, root mean "
        "squared error and the coefficient of determination. The Random Forest model performed "
        "best, with an R-squared value of 0.8786, a mean absolute error of USD 2,657.61 and a "
        "root mean squared error of USD 4,724.02 on the test set. The model was therefore tuned "
        "and retained, combining standard scaling and one-hot encoding in a scikit-learn "
        "pipeline, and was serialised with joblib.",

        "The trained model is deployed through an interactive Streamlit web application that "
        "accepts user inputs, returns an instant cost estimate, and provides a What-if Scenario "
        "Simulator that recomputes the estimate when selected factors are changed, reporting the "
        "absolute and percentage difference. Feature importance analysis shows that smoking "
        "status contributes about 70 per cent of the model's predictive power, followed by body "
        "mass index and age. The system is intended as an educational and awareness tool; the "
        "predictions are statistical estimates and not professional financial or medical advice.",
    ]
    for text in paras:
        _line(doc, text, size=12, align="justify", space_after=10, spacing=1.5)

    _line(doc, "Keywords:", size=12, bold=True, align="left", space_after=2)
    _line(doc, "medical insurance charges, machine learning, regression, Random Forest, "
               "feature importance, exploratory data analysis, scikit-learn, Streamlit, "
               "predictive modelling, what-if analysis",
          size=11.5, italic=True, align="justify", space_after=2, spacing=1.4)


# ----------------------------------------------------------------- TOC and lists
def toc_page(doc):
    _line(doc, "TABLE OF CONTENTS", size=18, bold=True, space_after=6)
    _hline(doc, space_before=0, space_after=16)

    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_before = Pt(6)
    add_field(p, ' TOC \\o "1-2" \\h \\z \\u ',
              "[ Click anywhere in this area, then press F9 and choose \u201cUpdate entire "
              "table\u201d to build the table of contents with page numbers. ]",
              size=11)

    _line(doc, "", size=8, space_after=22)
    _line(doc, "How to build or refresh this page", size=12, bold=True, align="left",
          space_after=6)
    _line(doc, "This table of contents is a live Word field, so the chapter titles and page "
               "numbers are read directly from the document rather than typed by hand. Word "
               "usually offers to update the field automatically when the file is opened; if it "
               "does not, select the whole document with Ctrl + A and press F9, then choose "
               "\u201cUpdate entire table\u201d. The List of Figures and the List of Tables are "
               "generated in the same way.",
          size=10.5, italic=True, align="justify", space_after=0, spacing=1.3, color=GREY)


def list_of_figures(doc):
    _line(doc, "LIST OF FIGURES", size=18, bold=True, space_after=6)
    _hline(doc, space_before=0, space_after=14)

    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_before = Pt(48)
    add_field(p, ' TOC \\h \\z \\t "FigureCaption,1" ',
              "Right-click here and choose Update Field to build the list of figures automatically.",
              size=11)

    _line(doc, "", size=8, space_after=18)
    _line(doc, "The list above is generated automatically from the figure captions in the "
               "document. If it appears empty or out of date, select the whole document "
               "(Ctrl + A) and press F9, then choose Update entire table.",
          size=10, italic=True, align="justify", space_after=0, color=GREY)


def list_of_tables(doc):
    _line(doc, "LIST OF TABLES", size=18, bold=True, space_after=6)
    _hline(doc, space_before=0, space_after=14)

    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_before = Pt(48)
    add_field(p, ' TOC \\h \\z \\t "TableCaption,1" ',
              "Right-click here and choose Update Field to build the list of tables automatically.",
              size=11)

    _line(doc, "", size=8, space_after=18)
    _line(doc, "The list above is generated automatically from the table captions in the document.",
          size=10, italic=True, align="justify", space_after=0, color=GREY)
