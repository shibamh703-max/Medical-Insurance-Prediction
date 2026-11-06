"""Chapter 4: System Design."""
import os
from docx_helpers import FONT

FIG = "/home/user/Medical-Insurance-Prediction/report/figures"


def chapter4(r):
    r.h1("System Design")

    r.p("This chapter describes the design of the MediPredict system before its implementation is "
        "discussed. It presents the overall architecture, the flow of data through the system, the "
        "interaction between the user and the application, the structure of the data, and the "
        "design of the machine learning pipeline and of the user interface. The diagrams have been "
        "drawn in the notation conventionally used for structured system analysis.")
    r.p("At the highest level the system consists of three layers: a presentation layer that the "
        "user sees in the browser, an application layer that holds the prediction and simulation "
        "logic, and a data layer that holds the training dataset and the serialised model. The "
        "layers are described in the sections that follow.")

    r.h2("4.1  System Architecture")
    r.p("The architecture is shown in Figure 4.1. The presentation layer is the Streamlit user "
        "interface rendered in the browser. It sends the six attribute values to the application "
        "layer and receives back a single floating point value, which it formats as a currency "
        "amount. The application layer contains the prediction module, the What-if Scenario "
        "Simulator and the session state that preserves the original estimate between "
        "interactions. The data layer holds the insurance dataset, which is used once during "
        "offline training, and the serialised model artefact, which is read at the start of every "
        "session through the joblib loader wrapped in a Streamlit cache.")
    r.p("The separation of the training phase from the serving phase is an important design "
        "decision. Training is performed offline, and the web application never touches the "
        "dataset; it interacts only with the fitted pipeline stored in the model file. This keeps "
        "the deployed application light, removes any dependency on the original data at run time "
        "and makes it possible to replace the model with a retrained version without modifying a "
        "single line of interface code.")
    r.figure(os.path.join(FIG, "fig_architecture.png"),
             "Three-layer system architecture of MediPredict", width=5.9)

    r.h2("4.2  Data Flow Diagrams")
    r.p("The flow of data through the system is documented at two levels of detail. The level 0 "
        "diagram, also called the context diagram, treats the entire system as a single process "
        "and shows only its interaction with the external entity and the data store it depends on.")
    r.p("In the level 0 diagram of Figure 4.2 the user supplies personal details, which enter the "
        "single process labelled 0, MediPredict System. The process returns the estimated charges "
        "to the user and reads the trained model from the data store D1. This level is useful for "
        "establishing the system boundary: nothing other than the user and the model store crosses "
        "it.", space_after=4)
    r.figure(os.path.join(FIG, "fig_dfd0.png"),
             "Data flow diagram, level 0 (context diagram)", width=5.6)

    r.p("The level 1 diagram in Figure 4.3 decomposes the single process into four sub-processes. "
        "Process 1.0 collects and validates the six input values. Process 2.0 preprocesses them, "
        "that is, it applies the scaling and one-hot encoding that were fitted during training. "
        "Process 3.0 loads the model from store D1, applies it to the encoded feature vector and "
        "produces the estimated charge. Process 4.0 receives the original estimate and a modified "
        "attribute set and computes the difference. Store D2 holds the training data, which is "
        "read only during the offline training step and therefore appears in the diagram with a "
        "dashed flow.", space_after=4)
    r.figure(os.path.join(FIG, "fig_dfd1.png"),
             "Data flow diagram, level 1", width=5.8)

    r.h2("4.3  Use Case Diagram")
    r.p("The actors of the system and the use cases available to them are shown in Figure 4.4. "
        "There is a single actor, the User, who is not required to authenticate. The primary use "
        "cases are the entry of personal details and the calculation of an insurance estimate. The "
        "secondary use cases are the exploration of what-if scenarios and the comparison of the "
        "resulting cost with the original estimate. The loading of the trained model is a use case "
        "that is included by each of the prediction use cases, since no prediction can be produced "
        "without it.", space_after=4)
    r.figure(os.path.join(FIG, "fig_usecase.png"),
             "Use case diagram of MediPredict", width=5.6)

    r.h2("4.4  Entity-Relationship Diagram")
    r.p("The dataset is a single flat table and therefore produces a simple entity-relationship "
        "structure with one entity and no relationships, as shown in Figure 4.5. The entity "
        "insurance has seven attributes: six descriptive attributes and one target attribute. "
        "Because the data are a statistical sample rather than a transactional record set, no "
        "natural primary key exists; each row represents one anonymous individual.", space_after=4)
    r.figure(os.path.join(FIG, "fig_er.png"),
             "Entity-relationship diagram of the insurance dataset", width=6.2)

    r.h2("4.5  Dataset Design")
    r.p("The dataset used for this project is the Medical Cost Personal Dataset, distributed "
        "publicly through Kaggle and widely used as a teaching dataset for regression. It contains "
        "1,338 records and seven columns. Each record describes one individual who was covered by "
        "a health insurance policy in the United States, and the target column records the medical "
        "charges billed to the insurer for that individual during the year. The attributes are "
        "described in Table 4.1.", space_after=4)
    r.table(
        ["Attribute", "Data Type", "Description", "Range / Categories"],
        [
            ["age", "Integer", "Age of the primary beneficiary", "18 \u2013 64 years"],
            ["sex", "Categorical", "Gender of the beneficiary", "male, female"],
            ["bmi", "Float", "Body mass index, ratio of weight in kilograms to the square of "
                             "height in metres", "15.96 \u2013 53.13"],
            ["children", "Integer", "Number of dependants covered by the policy", "0 \u2013 5"],
            ["smoker", "Categorical", "Whether the beneficiary smokes regularly", "yes, no"],
            ["region", "Categorical", "Residential region in the United States",
             "southeast, southwest,\nnorthwest, northeast"],
            ["charges", "Float (target)", "Annual medical insurance charges billed to the insurer "
                                          "in US dollars", "1,121.87 \u2013 63,770.43"],
        ],
        caption="Attributes of the insurance dataset",
        col_widths=[0.95, 1.15, 2.65, 1.35],
        font_size=10,
        first_col_bold=True,
    )
    r.p("Three properties of the dataset shaped the design of the preprocessing stage. First, "
        "there are no missing values, so no imputation strategy was required. Second, exactly one "
        "duplicate record was found and removed, leaving 1,337 unique records. Third, three of the "
        "six attributes are categorical and must therefore be encoded numerically before any "
        "regression algorithm can use them, while the three numerical attributes have very "
        "different scales: age ranges over roughly forty-six units, body mass index over "
        "thirty-seven, and children over five. Scaling was applied to the numerical attributes so "
        "that the model is not biased by the difference in magnitude.")
    r.p("The target variable has a mean of USD 13,279.12 and a standard deviation of USD "
        "12,110.36, and its skewness is 1.52, indicating a pronounced right tail. Because the "
        "extreme values are genuine high-cost individuals and not measurement errors, they were "
        "retained rather than removed as outliers; removing them would have made the model "
        "systematically underestimate the cost of the exact group that matters most to an insurer. "
        "The complete statistical summary of the dataset is presented in Chapter 6.")

    r.h2("4.6  Machine Learning Pipeline Design")
    r.p("The pipeline was designed according to the principle that every transformation applied "
        "during training must be reproduced identically during prediction. Instead of applying "
        "scaling and encoding as separate steps before training, the transformers were placed "
        "inside a scikit-learn Pipeline together with the regressor. This has three consequences: "
        "the fitted parameters of the scaler and encoder travel with the model, the same object "
        "can be applied to a single new record at prediction time, and the risk of a subtle "
        "training-serving mismatch is eliminated.")
    r.p("The design of the preprocessing stage is shown below. Numerical attributes are passed "
        "through a StandardScaler, which centres each attribute on zero and scales it to unit "
        "variance. Categorical attributes are passed through a OneHotEncoder with the first "
        "category dropped, which converts each categorical attribute into k minus one binary "
        "columns and thereby avoids the exact collinearity that would otherwise arise. The "
        "encoder is configured to ignore unknown categories, so an unexpected value at prediction "
        "time produces a row of zeros rather than an exception.", space_after=4)
    r.code_block([
        "Pipeline(",
        "    steps=[",
        "        ('preprocessor', ColumnTransformer(",
        "            transformers=[",
        "                ('num', StandardScaler(), ['age', 'bmi', 'children']),",
        "                ('cat', OneHotEncoder(drop='first',",
        "                                      handle_unknown='ignore'),",
        "                 ['sex', 'smoker', 'region'])])),",
        "        ('regressor', RandomForestRegressor(",
        "            n_estimators=600, max_depth=5,",
        "            min_samples_leaf=6, max_features=0.8,",
        "            random_state=42))])",
    ])
    r.p("The six input columns become eight features after encoding: three scaled numerical "
        "columns (age, bmi, children) and five indicator columns (sex_male, smoker_yes, "
        "region_southeast, region_northwest, region_southwest). The regressor receives these eight "
        "features and returns one continuous value. The serialised artefact stores the whole "
        "pipeline, which is why the web application only needs to pass a six-column data frame to "
        "the predict method and does not need to know anything about scaling or encoding.")
    r.p("The design of the complete data path, from the raw file to the deployed interface, is "
        "summarised in Figure 4.6.", space_after=4)
    r.figure(os.path.join(FIG, "fig_pipeline.png"),
             "End-to-end data and model pipeline", width=6.3)

    r.h2("4.7  User Interface Design")
    r.p("The interface was designed around a single principle: a user should be able to obtain an "
        "estimate without reading any instructions, and should immediately understand what the "
        "number means. The resulting layout has four regions, described below and illustrated in "
        "Figure 4.7.")
    r.bullets([
        "Header. A pale pink card carries the project name and a one-line description of the "
        "application. It establishes the identity of the page and is the only decorative element.",
        "Input panel. The left half of the main area holds a form with six labelled fields, "
        "arranged in two columns of three. Number inputs are provided with stepper controls and "
        "hard limits so that invalid values are impossible to submit. The single submit button is "
        "placed inside the form.",
        "Result card. The right half holds a card that is initially a placeholder explaining what "
        "to do. After submission it is replaced by the predicted amount in large type, with the "
        "input profile displayed underneath as a reminder of what was estimated.",
        "Comparison panel. The What-if Scenario Simulator appears below the two panels only after "
        "the first prediction. It presents five modifiable inputs in the same visual style as the "
        "main form, a submit button, a coloured banner stating whether the cost increased, "
        "decreased or stayed the same, and four cards giving the original cost, the what-if cost, "
        "the absolute difference and the percentage change.",
    ])
    r.p("A consistent colour scheme is used throughout: deep green for primary text and values, "
        "mint for panels and result cards, and dusty rose for the header and for increases in "
        "cost. Increases are shown in rose and decreases in green, so that the direction of a "
        "change is legible at a glance without reading the number. All sections use a light "
        "animation when they first appear, which draws attention to the newly computed result "
        "without being distracting.", space_after=4)
    r.figure(os.path.join(FIG, "app_01_initial.png"),
             "User interface of MediPredict in its initial state", width=5.9)
