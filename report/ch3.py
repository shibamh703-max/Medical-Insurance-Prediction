"""Chapter 3: System Analysis."""
from docx_helpers import FONT


def chapter3(r):
    r.h1("System Analysis")

    r.h2("3.1  Existing System")
    r.p("The conventional system for estimating medical insurance charges can be described in "
        "three steps. The applicant submits a proposal form containing personal details; an "
        "underwriter or a rating engine applies a tariff containing relativities for age, sex, "
        "smoking status and body mass index; and the resulting premium is communicated to the "
        "applicant as a single figure, usually with no breakdown. In a small number of cases the "
        "applicant may be told that a loading has been applied, but the magnitude of the loading "
        "is generally not disclosed.")
    r.p("Two categories of limitations follow from this system. The first is analytical. Tariff "
        "based rating relies on pre-specified functional forms and manually chosen interaction "
        "terms. When the true effect of one attribute depends on the level of another, as it "
        "demonstrably does for body mass index and smoking status in this dataset, the additive "
        "model either misses the effect or requires the analyst to discover it in advance. The "
        "second is informational. The applicant receives an outcome without a mechanism, cannot "
        "test how the outcome responds to a change in circumstances, and has no way of knowing "
        "which attribute contributes most to the quoted amount.")
    r.p("Prototype spreadsheets and generic online calculators attempt to address the second "
        "limitation, but they typically hard-code the tariff rather than learn it from data, and "
        "they therefore inherit exactly the analytical limitation described above. Neither of the "
        "two existing arrangements provides both an empirically learned model and an interactive "
        "explanation.")

    r.h2("3.2  Proposed System")
    r.p("MediPredict is proposed as a machine learning based estimation system with an interactive "
        "web interface. The proposed system consists of four components.")
    r.bullets([
        "A data preparation component that cleans the dataset, removes the duplicate record and "
        "encodes categorical attributes using one-hot encoding while scaling numerical attributes.",
        "A learning component that trains and compares three regression algorithms and retains "
        "the best performing one as a serialised artefact.",
        "An estimation component that loads the serialised model once per session, accepts six "
        "attribute values from the user and returns the predicted annual charge.",
        "A comparison component, the What-if Scenario Simulator, that recomputes the prediction "
        "for a modified set of attributes and reports the absolute and percentage difference "
        "against the original estimate.",
    ])
    r.p("Compared with the existing system, the proposed system is learned rather than "
        "tariff-based, it exposes the magnitude of the effect of each attribute through the "
        "comparison facility, and it reports importance at the level of the whole model so that "
        "the dominant drivers can be explained. It is explicitly an educational and awareness "
        "tool, not an underwriting engine, and this distinction is stated in the application "
        "itself.")

    r.h2("3.3  Requirement Analysis")
    r.p("Requirements were gathered by examining the dataset, by studying the behaviour expected "
        "of similar public calculators and by identifying the questions that a prospective "
        "policyholder would ask. They are classified below as functional and non-functional "
        "requirements.")

    r.h3("3.3.1  Functional Requirements")
    r.p("The functional requirements, identified by number for traceability, are listed in "
        "Table 3.1.", space_after=4)
    r.table(
        ["ID", "Functional Requirement", "Priority"],
        [
            ["FR-01", "The system shall accept the six input attributes: age, sex, body mass "
                      "index, number of dependent children, smoking status and region.", "High"],
            ["FR-02", "The system shall restrict each input to a valid range (age 18\u2013100, BMI "
                      "10\u201360, children 0\u201310) and to the categories present in the "
                      "training data.", "High"],
            ["FR-03", "The system shall compute and display an estimated annual insurance charge "
                      "in US dollars when the user submits the form.", "High"],
            ["FR-04", "The system shall display the input profile that produced the estimate "
                      "alongside the prediction.", "Medium"],
            ["FR-05", "The system shall provide a What-if Scenario Simulator that accepts a "
                      "modified set of attributes and returns a second prediction.", "High"],
            ["FR-06", "The system shall display the absolute difference and the percentage "
                      "difference between the original and the what-if estimate, indicating "
                      "increase, decrease or no significant change.", "High"],
            ["FR-07", "The system shall keep the estimated sex constant while simulating other "
                      "factors and shall state this to the user.", "Medium"],
            ["FR-08", "The system shall retain the original estimate across interactions until a "
                      "new estimate is calculated.", "Medium"],
            ["FR-09", "The system shall display an instructional placeholder before the first "
                      "prediction is made.", "Low"],
            ["FR-10", "The system shall show a disclaimer stating that the prediction is for "
                      "educational purposes only.", "Medium"],
            ["FR-11", "The system shall handle a missing or unreadable model file gracefully by "
                      "displaying an error instead of terminating with a stack trace.", "Medium"],
        ],
        caption="Functional requirements of the MediPredict system",
        col_widths=[0.7, 4.3, 1.0],
        font_size=10.5,
        align_center_cols=[0, 2],
    )

    r.h3("3.3.2  Non-Functional Requirements")
    r.p("The non-functional requirements are listed in Table 3.2.", space_after=4)
    r.table(
        ["ID", "Non-Functional Requirement", "Category"],
        [
            ["NFR-01", "A prediction shall be returned within one second of form submission, "
                       "excluding network latency.", "Performance"],
            ["NFR-02", "The trained model shall be loaded at most once per application session, "
                       "using a caching mechanism.", "Performance"],
            ["NFR-03", "The application shall run in a standard web browser without any client "
                       "side installation.", "Portability"],
            ["NFR-04", "The interface shall remain usable on screens as narrow as 800 pixels "
                       "through responsive layout rules.", "Usability"],
            ["NFR-05", "Input validation shall prevent out-of-range values from reaching the "
                       "model.", "Reliability"],
            ["NFR-06", "The model artefact shall be stored in a stable, version-tolerant format "
                       "loadable by the joblib library.", "Maintainability"],
            ["NFR-07", "All dependencies shall be declared with pinned versions so that the "
                       "environment can be reproduced.", "Reproducibility"],
            ["NFR-08", "The source code shall be organised into documented sections covering "
                       "configuration, styling, input handling, prediction and simulation.",
             "Maintainability"],
            ["NFR-09", "The application shall not require user authentication or the collection "
                       "of personally identifying data.", "Privacy"],
        ],
        caption="Non-functional requirements of the MediPredict system",
        col_widths=[0.75, 4.25, 1.0],
        font_size=10.5,
        align_center_cols=[0, 2],
    )

    r.h2("3.4  Feasibility Study")
    r.p("Before implementation, three dimensions of feasibility were examined.")

    r.h3("3.4.1  Technical Feasibility")
    r.p("The entire system is built with mature, freely available Python libraries. Scikit-learn "
        "provides the regression algorithms, the preprocessing transformers and the pipeline "
        "abstraction; pandas and NumPy handle data manipulation; joblib serialises the fitted "
        "pipeline; and Streamlit renders the interface. Training a Random Forest with six hundred "
        "trees on 1,069 training records takes only a few seconds on an ordinary laptop, and the "
        "resulting artefact is approximately 2.5 MB, which is small enough to be committed to a "
        "repository and loaded by a free cloud instance. No specialised hardware, accelerator or "
        "licensed software is required. The system is therefore technically feasible.")

    r.h3("3.4.2  Economic Feasibility")
    r.p("The direct cost of the project is nil. All libraries used are open source under "
        "permissive licences, the dataset is in the public domain, and the application is hosted "
        "on the free tier of Streamlit Community Cloud. Development was carried out on hardware "
        "already available to the author. The only notional costs are the time invested in "
        "development and the optional cost of printing and binding this report, which is an "
        "academic requirement rather than a system cost. The system is therefore economically "
        "feasible.")

    r.h3("3.4.3  Operational Feasibility")
    r.p("The interface requires no training to use. A visitor is presented with six labelled "
        "inputs, a single submit button and a result card; the comparison facility is an expander "
        "that appears only after a first estimate has been produced. Because the application runs "
        "in a browser, there is nothing to install for the end user. The model file and the "
        "application code are both version controlled, so a maintainer can reproduce or replace "
        "the model without touching the interface. The main operational caveat is that the "
        "prediction is a statistical estimate, and the system addresses this by displaying a "
        "disclaimer on every page. With that caveat stated, the system is operationally feasible.")

    r.h2("3.5  Hardware and Software Requirements")
    r.p("The requirements for development and for end use are listed separately in Table 3.3, "
        "since a user of the deployed application needs nothing beyond a browser.", space_after=4)
    r.table(
        ["Component", "Development Environment", "End-User Environment"],
        [
            ["Processor", "Intel Core i3 (8th generation) or equivalent, or better",
             "Any modern processor"],
            ["Memory", "4 GB RAM minimum (8 GB recommended)", "1 GB RAM available to the browser"],
            ["Storage", "500 MB free space for Python, libraries and the model artefact",
             "Not applicable"],
            ["Operating system", "Windows 10/11, Ubuntu 20.04+ or macOS 11+",
             "Any operating system with a modern browser"],
            ["Programming language", "Python 3.10 or later", "Not applicable"],
            ["Libraries", "streamlit 1.66.1, pandas 3.1.0, numpy 2.5.4, scikit-learn 1.9.1, "
                          "joblib 1.6.0, matplotlib 3.11.2, seaborn 0.13.2", "Not applicable"],
            ["Browser", "Chrome, Edge or Firefox (latest version)",
             "Chrome, Edge, Firefox or Safari (latest version)"],
            ["Network", "Internet connection for installation and deployment",
             "Internet connection to reach the hosted application"],
        ],
        caption="Hardware and software requirements",
        col_widths=[1.35, 2.6, 2.05],
        font_size=10,
        first_col_bold=True,
    )
