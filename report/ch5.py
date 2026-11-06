"""Chapter 5: Implementation."""
import os

FIG = "/home/user/Medical-Insurance-Prediction/report/figures"


def chapter5(r):
    r.h1("Implementation")

    r.p("This chapter describes how the design presented in the previous chapter was realised. It "
        "begins with the tools and technologies used, then covers the environment setup and the "
        "structure of the source code, and finally explains the implementation of each functional "
        "block: preprocessing, model building and tuning, serialisation, the Streamlit application "
        "and the what-if simulator.")

    r.h2("5.1  Tools and Technologies Used")
    r.p("The project uses a deliberately small technology stack. Every component is open source, "
        "and no component requires specialised hardware. The tools are listed with their purpose "
        "in Table 5.1.", space_after=4)
    r.table(
        ["Technology", "Version", "Purpose in This Project"],
        [
            ["Python", "3.10+", "Primary programming language for analysis, modelling and the "
                                 "application"],
            ["pandas", "3.1.0", "Loading the CSV file, removing the duplicate record, descriptive "
                                "statistics, grouping and aggregation"],
            ["NumPy", "2.5.4", "Numerical operations and array handling underneath pandas and "
                               "scikit-learn"],
            ["Matplotlib", "3.11.2", "Histograms, scatter plots, bar charts and the pipeline "
                                     "diagram used in this report"],
            ["Seaborn", "0.13.2", "Statistical plots such as box plots and correlation heat maps "
                                  "during exploratory analysis"],
            ["scikit-learn", "1.9.1", "Regression algorithms, ColumnTransformer, StandardScaler, "
                                      "OneHotEncoder, Pipeline and evaluation metrics"],
            ["joblib", "1.6.0", "Serialising the fitted pipeline to a .pkl file and loading it at "
                                "run time"],
            ["Streamlit", "1.66.1", "The web framework used to build and serve the interactive "
                                    "application"],
            ["Git and GitHub", "\u2014", "Version control and source hosting"],
            ["Streamlit Community Cloud", "\u2014", "Free public deployment of the application"],
        ],
        caption="Tools and technologies used in the project",
        col_widths=[1.35, 0.85, 3.8],
        font_size=10,
        first_col_bold=True,
        align_center_cols=[1],
    )

    r.h2("5.2  Environment Setup and Project Structure")
    r.p("The project was developed in an isolated Python virtual environment so that the library "
        "versions declared in the requirements file do not conflict with any other project on the "
        "development machine. The setup sequence is reproduced below.")
    r.code_block([
        "git clone https://github.com/OrioRiko-09/Medical-Insurance-Prediction",
        "cd Medical-Insurance-Prediction",
        "python -m venv .venv",
        ".venv\\Scripts\\activate        # Windows",
        "source .venv/bin/activate      # Linux or macOS",
        "pip install -r requirements.txt",
        "streamlit run app.py",
    ])
    r.p("The application then becomes available at http://localhost:8501. The repository is "
        "organised as shown in Table 5.2. The structure is intentionally flat: the modelling work "
        "is complete, and only the application, the trained artefact and the dependency list are "
        "needed at run time.", space_after=4)
    r.table(
        ["Path", "Description"],
        [
            ["app.py", "The complete Streamlit application, approximately 1,160 lines, organised "
                       "into commented sections for configuration, styling, model loading, input "
                       "handling, prediction, what-if simulation and the footer."],
            ["models/random_forest_model.pkl", "The serialised scikit-learn Pipeline containing "
                                               "the fitted preprocessor and the tuned Random "
                                               "Forest regressor, approximately 2.5 MB."],
            ["requirements.txt", "Pinned versions of the seven third-party libraries required by "
                                 "the application."],
            ["README.md", "Project overview, features, dataset description, evaluation table and "
                          "installation instructions."],
            [".gitignore", "Excludes virtual environments, Python bytecode, notebook checkpoints "
                           "and editor configuration from version control."],
            [".devcontainer/devcontainer.json", "Optional development container that installs the "
                                                "dependencies and forwards port 8501."],
        ],
        caption="Project structure and the role of each file",
        col_widths=[1.95, 4.05],
        font_size=10,
    )

    r.h2("5.3  Data Preprocessing Implementation")
    r.p("Preprocessing was implemented in four steps. The raw file was loaded with pandas, the "
        "single duplicate row was dropped, the descriptive statistics were inspected, and the "
        "feature matrix and target vector were separated. The relevant operations are shown below.",
        space_after=4)
    r.code_block([
        "import pandas as pd",
        "",
        "df = pd.read_csv('insurance.csv')          # 1338 rows, 7 columns",
        "print(df.shape, df.isnull().sum().sum())   # (1338, 7) and 0",
        "print(df.duplicated().sum())               # 1",
        "",
        "df = df.drop_duplicates()                  # 1337 rows remain",
        "",
        "X = df.drop(columns=['charges'])           # six input attributes",
        "y = df['charges']                          # continuous target",
    ])
    r.p("The transformations themselves were not applied at this stage. They were declared as "
        "transformers inside a ColumnTransformer, as described in Section 4.6, so that they are "
        "fitted on the training split only. Fitting the scaler on the whole dataset before "
        "splitting would leak information about the test set into the training process and would "
        "produce an optimistic evaluation. Placing the transformers inside the pipeline guarantees "
        "that the scaler sees only the training rows during fit, and that the identical fitted "
        "parameters are applied to the test rows and to any single row submitted at prediction "
        "time.")
    r.p("Because the numerical attributes were standardised, the resulting coefficients and "
        "feature importances are comparable across attributes despite the difference in their "
        "original units. Because the categorical encoder drops the first category of each "
        "attribute, the reference levels are female, non-smoker and the north-east region; the "
        "interpretation of the model is therefore relative to a non-smoking woman from the "
        "north-east.")

    r.h2("5.4  Model Building and Hyperparameter Tuning")
    r.p("Three regression algorithms were trained on a common split of the data, with eighty per "
        "cent of the 1,337 records used for training and twenty per cent held out for testing, and "
        "with a fixed random seed so that the comparison is reproducible. Linear Regression was "
        "included as a baseline because it represents the conventional actuarial approach and "
        "establishes how much of the variance a purely additive model can explain. A single "
        "Decision Tree was included to show the effect of using one non-linear model without "
        "ensembling. Random Forest was included as the expected best performer because it averages "
        "many decorrelated trees and therefore reduces the variance that affects a single tree.")
    r.p("The Random Forest was tuned on four hyperparameters. The number of trees was raised to "
        "six hundred so that the averaging is stable. The maximum depth was restricted to five, "
        "and the minimum number of samples per leaf was set to six; both restrictions regularise "
        "the forest, because an unrestricted forest on a dataset of this size memorises the "
        "training rows and generalises poorly to unseen individuals. The number of features "
        "considered at each split was set to eighty per cent of the available features, which "
        "introduces additional decorrelation between the trees. The parameter grid that was "
        "explored and the final values retained are shown in Table 5.3.", space_after=4)
    r.table(
        ["Hyperparameter", "Values Explored", "Final Value", "Reason for the Choice"],
        [
            ["n_estimators", "100, 300, 600", "600",
             "Accuracy improves up to a few hundred trees and then plateaus; 600 gives a stable "
             "average at negligible cost."],
            ["max_depth", "None, 4, 5, 6, 8", "5",
             "Deeper trees overfit the 1,069 training rows; depth 5 gave the best validation "
             "score."],
            ["min_samples_leaf", "1, 3, 6, 10", "6",
             "Larger leaves smooth the prediction, which matters because the target has a long "
             "right tail."],
            ["max_features", "1.0, 0.8, 'sqrt'", "0.8",
             "Slightly fewer features per split decorrelates the trees and improved the test "
             "score."],
            ["random_state", "\u2014", "42", "Guarantees a reproducible split and reproducible "
                                            "forest."],
        ],
        caption="Hyperparameter grid explored and values retained for the final model",
        col_widths=[1.2, 1.35, 0.8, 2.65],
        font_size=9.5,
        first_col_bold=True,
        align_center_cols=[1, 2],
    )
    r.p("The evaluation code itself is straightforward, and it is worth noting that the same "
        "three metrics are computed for each of the three models so that the comparison in "
        "Chapter 6 is exact.", space_after=4)
    r.code_block([
        "from sklearn.model_selection import train_test_split",
        "from sklearn.metrics import mean_absolute_error, \\",
        "                        mean_squared_error, r2_score",
        "",
        "X_train, X_test, y_train, y_test = train_test_split(",
        "    X, y, test_size=0.2, random_state=42)      # 1069 / 268 rows",
        "",
        "model.fit(X_train, y_train)",
        "pred = model.predict(X_test)",
        "",
        "mae  = mean_absolute_error(y_test, pred)",
        "rmse = mean_squared_error(y_test, pred) ** 0.5",
        "r2   = r2_score(y_test, pred)",
    ])

    r.h2("5.5  Model Serialisation and Loading")
    r.p("The fitted pipeline was serialised with joblib rather than with the standard pickle "
        "module because joblib handles NumPy arrays, which the forests contain, more efficiently, "
        "and produces a smaller file. The saved artefact is approximately 2.5 MB and contains the "
        "fitted StandardScaler, the fitted OneHotEncoder and the six hundred fitted decision "
        "trees, so a single load call restores the entire prediction path.",
        space_after=4)
    r.code_block([
        "import joblib",
        "joblib.dump(model, 'models/random_forest_model.pkl')",
    ])
    r.p("On the application side, loading is wrapped in a Streamlit caching decorator. Without "
        "caching, the model file would be read from disk and unpickled on every re-run of the "
        "script, which happens on every user interaction; with caching, it is loaded once and the "
        "same object is reused for all subsequent predictions in that session. The path is "
        "resolved relative to the location of app.py rather than to the current working "
        "directory, which avoids a common deployment failure in which the file cannot be found "
        "because the process was started from a different directory.", space_after=4)
    r.code_block([
        "from pathlib import Path",
        "import joblib, streamlit as st",
        "",
        "BASE_DIR   = Path(__file__).resolve().parent",
        "MODEL_PATH = BASE_DIR / 'models' / 'random_forest_model.pkl'",
        "",
        "@st.cache_resource",
        "def load_model():",
        "    return joblib.load(MODEL_PATH)",
        "",
        "try:",
        "    model = load_model()",
        "except Exception as e:",
        "    st.error(f'Could not load the trained model: {e}')",
        "    st.stop()",
    ])
    r.p("Two details deserve comment. The cache_resource decorator is used rather than "
        "cache_data because the loaded object is a model, not data, and should be shared across "
        "all users of the application rather than copied. The try block is deliberate: a missing "
        "or incompatible model file is the most likely deployment failure, and catching it allows "
        "the application to display a readable message instead of an unhandled traceback. The "
        "call to st.stop then prevents the rest of the script from executing with an undefined "
        "model.")

    r.h2("5.6  Implementation of the Web Application")
    r.p("The application is a single script. Streamlit re-executes the whole script from top to "
        "bottom on every user interaction, and the design of the code takes this into account: "
        "configuration, styling and model loading are at the top and are cached or idempotent, "
        "while the interactive sections follow in the order in which they appear on the page.")
    r.p("The page configuration sets the browser title, the favicon and the wide layout. The wide "
        "layout is necessary because the main area is divided into two equal columns, an input "
        "panel on the left and a result panel on the right; in the default centred layout the two "
        "columns would be too narrow to display the currency value comfortably.",
        space_after=4)
    r.code_block([
        "st.set_page_config(",
        "    page_title='MediPredict | Insurance Estimator',",
        "    page_icon='\\U0001F3E5',",
        "    layout='wide')",
    ])
    r.p("The form itself is created with st.form, which is an important choice. Inside a form, "
        "widget values are not sent to the server until the submit button is pressed; without a "
        "form, every keystroke in the age field would trigger a full re-run of the script and a "
        "prediction. The six widgets are arranged in two columns and their ranges enforce the "
        "functional requirement FR-02 at the level of the interface, so that an out-of-range value "
        "cannot reach the model. The ranges are age 18 to 100 with a default of 25, body mass "
        "index 10.0 to 60.0 with a step of 0.1 and a default of 25.0, number of children 0 to 10 "
        "with a default of 0, and select boxes for sex, smoking status and region.",
        space_after=4)
    r.code_block([
        "with st.form('prediction_form'):",
        "    col1, col2 = st.columns(2)",
        "    with col1:",
        "        age   = st.number_input('Age', 18, 100, 25, step=1)",
        "        sex   = st.selectbox('Sex', ['male', 'female'])",
        "        bmi   = st.number_input('BMI', 10.0, 60.0, 25.0, step=0.1)",
        "    with col2:",
        "        children = st.number_input('Number of Children', 0, 10, 0, step=1)",
        "        smoker   = st.selectbox('Smoker', ['no', 'yes'])",
        "        region   = st.selectbox('Region', ['southwest', 'southeast',",
        "                                          'northwest', 'northeast'])",
        "    submitted = st.form_submit_button('Calculate Insurance Estimate')",
    ])
    r.p("When the form is submitted, the six values are assembled into a one-row pandas data "
        "frame whose column names match the names the pipeline was trained on. Matching the names "
        "is essential, because the ColumnTransformer selects columns by name; a frame with the "
        "same values in a different column order would still work, whereas a frame with different "
        "names would fail. The frame is passed directly to the pipeline, which applies the "
        "preprocessing steps and the forest automatically.", space_after=4)
    r.code_block([
        "if submitted:",
        "    input_data = pd.DataFrame({",
        "        'age': [age], 'sex': [sex], 'bmi': [bmi],",
        "        'children': [children], 'smoker': [smoker], 'region': [region]})",
        "    prediction = float(model.predict(input_data)[0])",
        "    st.session_state.original_prediction = prediction",
        "    st.session_state.original_input = {...}",
    ])
    r.p("The prediction is stored in st.session_state rather than in a local variable. Streamlit "
        "re-runs the entire script on every interaction, and local variables are lost between "
        "runs; session state is the mechanism that preserves values for the duration of a user's "
        "session. Without it the result card would disappear the moment the user touched any "
        "other widget. The same mechanism holds the input profile, which is displayed underneath "
        "the amount so that the user can see exactly which combination of attributes produced it.")

    r.h2("5.7  Implementation of the What-if Simulator")
    r.p("The What-if Scenario Simulator is the distinguishing feature of this application. It is "
        "implemented as an expander that is rendered only when an original prediction already "
        "exists in the session state, so that a first-time visitor is not confronted with a second "
        "form before they have seen a result.")
    r.p("The simulator presents five inputs, namely age, body mass index, smoking status, number "
        "of children and region, each initialised to the value used in the original estimate. Sex "
        "is intentionally not modifiable, since it is not something a person can change; instead a "
        "badge states which value is being held constant, so that the comparison is not mistaken "
        "for a like-for-like change of every attribute. Age is constrained to be no lower than the "
        "original age, which prevents a nonsensical backward comparison.",
        space_after=4)
    r.code_block([
        "with st.expander('Explore What-if Scenarios', expanded=True):",
        "    with st.form('whatif_form'):",
        "        w_col1, w_col2, w_col3 = st.columns(3)",
        "        whatif_age    = st.number_input('What-if Age', orig['age'], 100,",
        "                                        orig['age'], key=f'age_{ver}')",
        "        whatif_bmi    = st.number_input('What-if BMI', 10.0, 60.0,",
        "                                        float(orig['bmi']), key=f'bmi_{ver}')",
        "        whatif_smoker = st.selectbox('What-if Smoker', ['no', 'yes'],",
        "                                      key=f'smoker_{ver}')",
        "        whatif_submitted = st.form_submit_button('Compare Scenario')",
    ])
    r.p("When the comparison form is submitted, a second data frame is built with the original "
        "sex and the modified values for the other five attributes. It is passed through the same "
        "model, and the difference and the percentage change are computed from the two "
        "predictions. The sign of the difference determines which of three banners is shown, so "
        "that an increase, a decrease and a negligible change are visually distinct.",
        space_after=4)
    r.code_block([
        "whatif_pred = float(model.predict(whatif_df)[0])",
        "diff        = whatif_pred - orig_pred",
        "pct_change  = (diff / orig_pred * 100.0) if orig_pred > 0 else 0.0",
        "",
        "if diff > 0.01:       direction, icon = 'Estimated Cost Increased', 'up'",
        "elif diff < -0.01:    direction, icon = 'Estimated Cost Decreased', 'down'",
        "else:                 direction, icon = 'No Significant Cost Change', 'neutral'",
    ])
    r.p("A small tolerance of one cent is used in the comparison rather than an exact test against "
        "zero. Two predictions that are mathematically identical can differ by a fraction of a cent "
        "because of floating point representation, and without the tolerance the interface would "
        "report an increase or a decrease for a scenario in which nothing changed.")
    r.p("Finally, the widget keys include a version counter that is incremented every time a new "
        "original estimate is calculated. Streamlit persists widget state by key, so without "
        "versioned keys the what-if inputs would retain the values from a previous, unrelated "
        "estimate. Incrementing the version effectively resets the simulator whenever the basis of "
        "comparison changes, which is the behaviour a user expects.")

    r.h2("5.8  Challenges Faced During Implementation")
    r.p("Several practical difficulties arose during implementation and are recorded here because "
        "they are typical of the transition from a notebook to a deployed application.")
    r.bullets([
        "Training-serving mismatch. The first version applied scaling and encoding in the "
        "notebook and then saved only the regressor. Predictions from the application were "
        "grossly wrong because the input was never transformed. The problem was solved by "
        "serialising the complete pipeline, so that the transformations are applied automatically "
        "at prediction time.",
        "Repeated model loading. The first deployment reloaded the 2.5 MB model on every "
        "interaction, which made the interface feel sluggish. Wrapping the loader in "
        "st.cache_resource reduced the load to one per session.",
        "Loss of the result card. Before session state was introduced, the predicted amount "
        "vanished as soon as the user touched another widget. Storing the prediction and the "
        "input profile in st.session_state resolved this.",
        "Stale what-if values. Changing the original estimate left the simulator showing values "
        "from the previous estimate. Versioned widget keys fixed the problem.",
        "Styling limitations. Streamlit does not expose a full styling API, and a considerable "
        "part of app.py is custom CSS injected with st.markdown. Selectors had to be chosen from "
        "the rendered DOM and re-checked whenever the Streamlit version changed.",
        "Deployment path resolution. The application initially failed on the hosting platform "
        "because the model path was relative to the working directory. Resolving the path from "
        "__file__ made the load independent of how the process was started.",
    ])
