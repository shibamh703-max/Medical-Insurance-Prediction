# MediPredict — Project Report (Documentation)

This folder contains the full academic project report for **MediPredict: Medical Insurance Cost
Prediction using Machine Learning**, generated as a Word document with all figures and tables.

| File | What it is |
|---|---|
| `MediPredict_Project_Report.docx` | The complete report — front matter, 7 chapters, references and 2 appendices (~12,000 words, 17 figures, 12 tables) |
| `figures/` | Every figure used in the report, as individual PNG files (300 dpi) |
| `build_report.py` | The script that regenerates the .docx from `figures/` |

## Formatting already applied

- A4 paper, 1 inch margins on all four sides
- Times New Roman throughout — headings 14–16 pt bold, body 12 pt
- 1.5 line spacing, body text justified
- Page numbers centred in the footer (roman numerals on front matter, arabic from Chapter 1)
- Figures centred with captions below; tables with a shaded header row, captions above

## What is in the report

**Front matter:** Cover page · Certificate · Declaration · Acknowledgement · Abstract (with
keywords) · Table of Contents · List of Figures · List of Tables

**Chapters**

1. Introduction — background, problem statement, objectives, scope, motivation
2. Literature Review — actuarial methods vs. ML, summary table of 5 reviewed works, research gap
3. System Analysis — existing system, proposed system, functional & non-functional requirements,
   feasibility study, hardware/software requirements
4. System Design — architecture, DFD level 0 & 1, use case, ER diagram, dataset design, ML pipeline
   design, UI design
5. Implementation — tools table, environment setup, preprocessing, tuning grid, serialisation,
   app code walkthrough, what-if simulator, challenges faced
6. Results & Discussion — EDA findings, metric definitions, model comparison, feature importance,
   app screenshots, discussion, limitations
7. Conclusion & Future Work — summary, achievements, enhancements, conclusion

**Back matter:** References (18 entries, IEEE style — papers, books and websites) · Appendix A
(project structure & commands) · Appendix B (17 viva questions with answers)

## Before you print — two things to do

1. **Fill in the placeholders.** Search for `[` in Word and replace: `[YOUR NAME]`,
   `[YOUR REGISTRATION NUMBER]`, `[PROJECT GUIDE NAME]`, `[HEAD OF DEPARTMENT NAME]`,
   `[YOUR COLLEGE / INSTITUTE NAME]`, `[AFFILIATED UNIVERSITY NAME]`, `[CITY]`.
   They are all defined once at the top of the report build, and appear on the cover, certificate
   and declaration pages.

2. **Update the fields.** The Table of Contents, List of Figures and List of Tables are live Word
   fields. Press `Ctrl + A` then `F9`, choose *Update entire table*, and Word will fill in every
   page number automatically. (Word usually offers to do this when the file is opened.)

Then export to PDF with *File → Save As → PDF*, which is the copy you submit along with the
spiral-bound print.

## Regenerating the document

```bash
pip install python-docx matplotlib seaborn scikit-learn pandas joblib
python build_report.py
```

The figures are produced from the real `insurance.csv` dataset and from the actual trained model
(`models/random_forest_model.pkl`), so every number in the report — the EDA statistics, the
correlation values, the feature importances (smoker 69.7 %, BMI 16.5 %, age 12.3 %) and the
what-if example (USD 42,741.54 → USD 9,344.13) — matches what the deployed app actually computes.
