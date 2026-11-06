"""Chapter 1 and 2 of the MediPredict report."""


def chapter1(r):
    r.h1("Introduction")

    r.h2("1.1  Background of the Study")
    r.p("Health insurance is a financial instrument through which the cost of medical treatment is "
        "pooled across a large number of people, so that an individual does not have to bear the "
        "full expense of an illness at the moment it occurs. The amount that an insurer charges "
        "for covering one person, known as the premium, is not arbitrary. It is derived from an "
        "estimate of how much that person is likely to cost the insurer, and that estimate is "
        "built from attributes that are known to be associated with medical expenditure.")
    r.p("For decades this estimation has been done through actuarial rating tables and generalised "
        "linear models, which fit a smooth mathematical relationship between the input attributes "
        "and the expected claim amount. These methods have the advantage of being transparent and "
        "easy to audit, which matters in a regulated industry. They also carry a well-known "
        "limitation: they assume that the effect of each attribute is additive and that the "
        "relationship follows a specified functional form. Real medical expenditure does not "
        "behave in this way. The same increase in body mass index, for example, may be almost "
        "irrelevant for a non-smoker while being a very strong predictor of cost for a smoker. "
        "Interactions of this kind are exactly what tree-based machine learning models are able to "
        "capture without being told in advance that they exist.")
    r.p("At the same time, the ordinary applicant has very little visibility into this process. A "
        "person filling an insurance form knows their own age, weight and smoking status, but has "
        "no practical way of knowing what those attributes mean in monetary terms. This project, "
        "MediPredict, is built around that second problem. Using a publicly available dataset of "
        "1,338 insured individuals, it trains a regression model that maps six personal attributes "
        "to annual insurance charges, and exposes the model through a web application so that any "
        "user can obtain an estimate in a few seconds and can explore how the estimate changes "
        "when one factor is altered.")

    r.h2("1.2  Problem Statement")
    r.p("The problem addressed by this project can be stated as follows: given the personal and "
        "lifestyle attributes of an individual, namely age, sex, body mass index, number of "
        "dependent children, smoking status and residential region, can a machine learning model "
        "predict that individual's annual medical insurance charges with useful accuracy, and can "
        "that model be delivered in a form that a non-technical user can operate?")
    r.p("Two difficulties make this a non-trivial problem. First, the target variable is "
        "continuous, strongly right-skewed and heavily influenced by a single binary attribute "
        "(smoking status), which means that a naive model can appear acceptable on average while "
        "being badly wrong for whole segments of the population. Second, a prediction on its own "
        "is of limited practical value to a user; the useful insight lies in comparison, that is, "
        "in understanding how much of the estimated cost is attributable to a factor that the "
        "individual could potentially change. The system therefore has to support both accurate "
        "estimation and interactive comparison.")

    r.h2("1.3  Objectives of the Project")
    r.p("The specific objectives of the work are listed below.", space_after=4)
    r.numbers([
        "To study the Medical Cost Personal Dataset and to characterise the distribution of "
        "insurance charges and their relationship with the available attributes.",
        "To perform data cleaning and exploratory data analysis in order to identify missing "
        "values, duplicate records, outliers and the strength of association between each "
        "attribute and the target variable.",
        "To build a preprocessing pipeline that encodes categorical attributes and scales "
        "numerical attributes so that the data are suitable for regression algorithms.",
        "To train and evaluate three regression models, namely Linear Regression, Decision Tree "
        "Regression and Random Forest Regression, and to compare them on the basis of mean "
        "absolute error, root mean squared error and the coefficient of determination.",
        "To tune the best performing model and to serialise it so that it can be reused by an "
        "application without retraining.",
        "To design and develop an interactive web application using Streamlit that accepts user "
        "inputs and returns an estimated insurance charge.",
        "To implement a What-if Scenario Simulator that recomputes the estimate for modified "
        "inputs and reports the absolute and percentage change with respect to the original "
        "estimate.",
        "To interpret the model through feature importance analysis so that the factors that "
        "drive the prediction can be explained to a non-technical user.",
    ])

    r.h2("1.4  Scope of the Project")
    r.p("The scope of the present work is deliberately limited in order to keep the study focused "
        "and reproducible. The project covers the analysis, modelling and deployment of a "
        "regression system for a single tabular dataset. The following items are within scope.")
    r.bullets([
        "Analysis of one publicly available dataset containing 1,338 records and seven columns.",
        "Use of six input attributes and one continuous target variable (charges).",
        "Training, comparison and tuning of three supervised regression algorithms.",
        "Comparison of models using three standard regression metrics.",
        "Interpretation of the final model using built-in feature importance.",
        "Development of a single-page web application with an estimation form and a comparison "
        "module, deployed on Streamlit Community Cloud.",
    ])
    r.p("The following items are outside the scope of this work.", space_after=4)
    r.bullets([
        "Use of medical records, diagnostic history or prescription data, which are not present "
        "in the dataset.",
        "Time-series or survival modelling of claim events; the dataset provides only a single "
        "annual charge figure per individual.",
        "Any use of the system for actual underwriting, pricing or claim settlement decisions.",
        "Multi-user authentication, database storage or audit logging, which a production "
        "insurance system would require.",
    ])

    r.h2("1.5  Motivation")
    r.p("The motivation for the project came from three observations. First, insurance pricing is "
        "one of the few everyday financial decisions in which the individual has almost no "
        "information advantage, and a transparent estimator gives the applicant a basis for "
        "asking informed questions. Second, the dataset, although small, contains a genuine and "
        "well-documented interaction between smoking status and body mass index, which makes it an "
        "excellent teaching case for why non-linear models outperform linear ones on tabular data. "
        "Third, the project offered an opportunity to carry a machine learning model through the "
        "complete life cycle, from raw data to a deployed interface, which is precisely the "
        "sequence of steps that a data science practitioner performs in practice.")

    r.h2("1.6  Organisation of the Report")
    r.p("The remainder of this report is organised as follows. Chapter 2 reviews the existing "
        "approaches to insurance risk rating and the relevant machine learning literature, and "
        "identifies the gap that this project addresses. Chapter 3 presents the system analysis, "
        "including the study of the existing system, the requirements of the proposed system and "
        "the feasibility study. Chapter 4 describes the system design with the help of "
        "architecture, data flow, use case and entity-relationship diagrams. Chapter 5 documents "
        "the implementation, covering the tools used, the preprocessing and modelling code and the "
        "construction of the web application. Chapter 6 presents the results of the exploratory "
        "data analysis and of the model comparison, together with the application screenshots and "
        "a discussion of the findings and limitations. Chapter 7 concludes the report and outlines "
        "directions for future work. References and two appendices follow the final chapter.")


def chapter2(r):
    r.h1("Literature Review")

    r.h2("2.1  Introduction")
    r.p("This chapter places the present work in the context of existing practice. It begins with "
        "the conventional actuarial methods that insurance companies have used for decades, then "
        "reviews studies that apply machine learning to insurance cost prediction, and finally "
        "summarises the reviewed work in a table in order to identify the specific gap that "
        "MediPredict attempts to fill.")

    r.h2("2.2  Conventional Actuarial Rating Methods")
    r.p("Traditional personal lines pricing is based on rating factors that are individually "
        "assessed and then combined multiplicatively. In health and medical insurance the standard "
        "factors are age, sex, smoking status and an anthropometric measure such as body mass "
        "index, and each factor is assigned a relativities table derived from historical claims "
        "experience. The statistical backbone of this approach is the generalised linear model, "
        "most commonly with a Poisson or gamma error distribution and a logarithmic link function, "
        "as described in the widely used actuarial texts of Ohlsson and Johansson and of "
        "McCullagh and Nelder.")
    r.p("The strength of generalised linear models is interpretability. Each coefficient has a "
        "direct multiplicative interpretation, the model can be audited by a regulator, and the "
        "effect of a single rating factor can be read off without any computational tool. Their "
        "weakness is the additivity assumption on the scale of the linear predictor. If the true "
        "effect of body mass index depends on smoking status, a model without an explicit "
        "interaction term will attribute a misleading average effect to both variables. Actuaries "
        "address this by manually specifying interaction terms, but the search space grows quickly "
        "and the process is labour intensive. A second weakness is that tariff tables are "
        "notoriously difficult for a policyholder to interpret, so the transparency of the model "
        "does not translate into transparency for the customer.")

    r.h2("2.3  Machine Learning Approaches to Risk Rating")
    r.p("The application of machine learning to insurance pricing has grown steadily since the "
        "mid-2010s, driven by the availability of larger data sets and by the maturation of "
        "gradient boosting libraries. The recurring findings relevant to the present work are "
        "summarised below.")
    r.p("Ensemble tree methods dominate tabular prediction tasks. Breiman's Random Forest, which "
        "averages many decorrelated decision trees, and the later gradient boosting family of "
        "Friedman reduce the high variance that affects a single decision tree while retaining the "
        "ability to model non-linear effects and interactions automatically. Comparative studies "
        "on medical cost data consistently report that a tuned Random Forest or gradient boosting "
        "model achieves a coefficient of determination in the range of 0.85 to 0.90, whereas "
        "linear regression on the same data typically reaches only about 0.75 to 0.81.")
    r.p("Smoking status is repeatedly identified as the dominant predictor of medical charges, "
        "with body mass index and age following. This is consistent with the actuarial literature "
        "on mortality and morbidity, and it has an important methodological consequence: because "
        "a single binary attribute explains the majority of the variance, overall error metrics "
        "can conceal large systematic errors within the non-smoking sub-population. Recent "
        "studies therefore recommend reporting errors separately for the smoker and non-smoker "
        "groups rather than a single aggregate figure.")
    r.p("On the deployment side, the literature increasingly emphasises explainability. A model "
        "that is accurate but opaque is of limited use to a policyholder or a regulator. "
        "Techniques such as permutation importance, local interpretable model-agnostic "
        "explanations and SHAP values are now standard companions to predictive models, and "
        "several studies recommend exposing a small number of high-level drivers to the end user "
        "instead of a raw numeric output. Lightweight interactive dashboards built with frameworks "
        "such as Streamlit and Shiny have become a common way of delivering such explanations "
        "without requiring a software engineering team.")
    r.p("Finally, a consistent limitation across the reviewed studies is that few of them provide "
        "the end user with an interactive comparison facility. Most report aggregate metrics and, "
        "at most, a static prediction form. The insight that a user actually needs, namely how "
        "much of the estimated cost is attributable to a modifiable factor such as smoking, is "
        "rarely delivered directly.")

    r.h2("2.4  Summary of Reviewed Literature")
    r.p("Table 2.1 summarises the five principal strands of work reviewed above and indicates how "
        "each of them relates to the present project.")

    r.table(
        ["Ref.", "Area / Approach", "Key Finding", "Relevance to This Work"],
        [
            ["[1]", "Generalised linear models for insurance rating (Ohlsson & Johansson; "
                    "McCullagh & Nelder)",
             "Linear predictors with a log link give interpretable rating factors but cannot "
             "capture interactions unless they are specified by hand.",
             "Explains why a non-linear model is expected to outperform Linear Regression on this "
             "dataset."],
            ["[2]", "Random Forest regression (Breiman, 2001)",
             "Averaging many decorrelated trees reduces variance and captures interactions "
             "without explicit feature engineering.",
             "Provides the algorithm that is finally adopted and tuned in this project."],
            ["[3]", "Comparative study of regression models on medical cost data (Kaggle "
                    "community analyses of the Medical Cost Personal Dataset)",
             "Random Forest and gradient boosting reach R\u00b2 of 0.85\u20130.90, against "
             "0.75\u20130.81 for linear regression.",
             "Establishes the benchmark against which the results of Chapter 6 are compared."],
            ["[4]", "Interpretability of insurance models (feature importance, SHAP, LIME)",
             "Smoking status, BMI and age dominate importance rankings; users need high-level "
             "explanations rather than raw output.",
             "Motivates the feature importance analysis and the plain-language explanation in the "
             "application."],
            ["[5]", "Deployment of models through lightweight dashboards (Streamlit, Shiny)",
             "A script-based web framework is sufficient to expose a model to non-technical users "
             "without a separate front-end team.",
             "Justifies the choice of Streamlit for the MediPredict interface."],
        ],
        caption="Summary of the reviewed literature and its relevance to the present work",
        col_widths=[0.55, 1.75, 2.0, 1.9],
        font_size=10,
    )

    r.h2("2.5  Research Gap and Approach Adopted")
    r.p("The review shows that accurate prediction of medical insurance charges from personal "
        "attributes is a well-understood problem, and that ensemble tree models are the accepted "
        "solution for tabular data of this kind. The gap lies not in the modelling but in the "
        "delivery. Most published work stops at the report of metrics, and the few deployable "
        "systems present a single numeric prediction without context.")
    r.p("The approach adopted in this project is therefore to combine three elements in one "
        "artefact: a properly validated and tuned Random Forest model; a comparative evaluation "
        "against a linear baseline and a single decision tree so that the benefit of the ensemble "
        "is demonstrated rather than assumed; and an interface that reports not only the estimated "
        "charge but also the change in that charge when individual factors are varied. The "
        "comparison facility is, to the best of the author's knowledge, the element that "
        "distinguishes this implementation from the existing publicly documented versions of this "
        "dataset.")
