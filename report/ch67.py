"""Chapters 6 and 7, references and appendices."""
import os

FIG = "/home/user/Medical-Insurance-Prediction/report/figures"


def chapter6(r):
    r.h1("Results and Discussion")

    r.p("This chapter presents the results obtained at each stage of the project. It reports the "
        "findings of the exploratory data analysis, defines the metrics used for evaluation, "
        "compares the three regression models, describes the final model and its behaviour, shows "
        "the deployed application, and closes with a discussion of the results and of the "
        "limitations of the study.")

    r.h2("6.1  Results of Exploratory Data Analysis")
    r.p("The dataset contained 1,338 records and seven columns, with no missing values and exactly "
        "one duplicate record. After the duplicate was removed, 1,337 unique records remained. The "
        "descriptive statistics of the numerical attributes are given in Table 6.1.",
        space_after=4)
    r.table(
        ["Statistic", "age", "bmi", "children", "charges (USD)"],
        [
            ["Count", "1337", "1337", "1337", "1337"],
            ["Mean", "39.22", "30.66", "1.10", "13,279.12"],
            ["Standard deviation", "14.04", "6.10", "1.21", "12,110.36"],
            ["Minimum", "18.00", "15.96", "0.00", "1,121.87"],
            ["First quartile", "27.00", "26.29", "0.00", "4,746.34"],
            ["Median", "39.00", "30.40", "1.00", "9,386.16"],
            ["Third quartile", "51.00", "34.70", "2.00", "16,657.72"],
            ["Maximum", "64.00", "53.13", "5.00", "63,770.43"],
        ],
        caption="Descriptive statistics of the numerical attributes after removing the duplicate",
        col_widths=[1.5, 1.1, 1.1, 1.1, 1.4],
        font_size=10,
        first_col_bold=True,
        align_center_cols=[1, 2, 3, 4],
    )

    r.p("The distribution of the target variable is shown in Figure 6.1. The shape is strongly "
        "right-skewed, with a skewness of 1.52: the mean charge of USD 13,279 is substantially "
        "higher than the median of USD 9,386, and a long tail of high-cost individuals extends to "
        "USD 63,770. The histogram is visibly bimodal in the sense that a large mass of "
        "individuals lies below USD 15,000 while a secondary cluster appears between USD 30,000 "
        "and USD 45,000. That secondary cluster is not random; it is the smoking population, as "
        "the next figure demonstrates.", space_after=4)
    r.figure(os.path.join(FIG, "fig_eda_charges_hist.png"),
             "Distribution of annual insurance charges (right-skewed)", width=5.6)

    r.p("Figure 6.2 compares the charge distribution of smokers and non-smokers. The separation is "
        "stark. Non-smokers have a mean charge of USD 8,440.66 and a median near USD 7,300, "
        "whereas smokers have a mean charge of USD 32,050.23, almost four times higher. The "
        "interquartile range of the non-smoking group is narrow and its upper whisker terminates "
        "well below the median of the smoking group, so the two distributions overlap only "
        "slightly. This single attribute, therefore, divides the population into two populations "
        "with different cost behaviour, and any model that does not capture this division will "
        "perform poorly.", space_after=4)
    r.figure(os.path.join(FIG, "fig_eda_smoker_box.png"),
             "Comparison of charges between non-smokers and smokers", width=5.6)

    r.p("Figure 6.3 shows charges against age, with the two smoking groups distinguished by colour. "
        "Three bands are visible among smokers, corresponding to low, moderate and high body mass "
        "index, which is evidence of the interaction between smoking and body mass index that was "
        "anticipated in Chapter 2. Among non-smokers the relationship with age is positive but "
        "much shallower, and the band is narrower. The figure also reveals a horizontal floor "
        "around USD 1,100, which is the minimum charge in the dataset.", space_after=4)
    r.figure(os.path.join(FIG, "fig_eda_age_scatter.png"),
             "Age against charges, segmented by smoking status", width=5.8)

    r.p("The correlation matrix in Figure 6.4 quantifies the linear association between the "
        "numerical attributes and the target. Age has the strongest linear correlation with "
        "charges (0.30), followed by body mass index (0.20) and number of children (0.07). The "
        "correlations among the predictors themselves are negligible, the largest being 0.11 "
        "between age and body mass index, so multicollinearity is not a concern. It is important "
        "to note that these coefficients understate the true influence of the attributes, because "
        "they measure only linear association; smoking status, which is categorical and therefore "
        "absent from this matrix, is in fact the dominant driver, as the feature importance "
        "analysis in Section 6.4 confirms.", space_after=4)
    r.figure(os.path.join(FIG, "fig_eda_corr.png"),
             "Correlation matrix of the numerical attributes", width=4.6)

    r.p("The main findings of the exploratory analysis can be summarised as follows.")
    r.bullets([
        "The dataset is clean: no missing values, one duplicate removed, and no implausible "
        "values requiring correction.",
        "The target is strongly right-skewed and should not be modelled by a method that assumes "
        "normally distributed errors without consideration.",
        "Smoking status is the single most discriminating attribute, with a mean charge nearly "
        "four times that of non-smokers.",
        "Age and body mass index have positive but individually modest linear correlation with "
        "charges, which is consistent with a strong interaction between them.",
        "The predictors are essentially uncorrelated with one another, so all three can be "
        "retained without risk of instability.",
    ])

    r.h2("6.2  Evaluation Metrics Used")
    r.p("Three metrics were used to compare the models. Each captures a different aspect of "
        "predictive quality, and reporting all three avoids the distortions that arise from "
        "relying on a single number.")
    r.rich([("Mean Absolute Error (MAE). ", True, False),
            ("The average of the absolute differences between the predicted and the actual "
             "charges. Because it is expressed in dollars, it has a direct interpretation: an MAE "
             "of USD 2,657 means that a prediction is, on average, about USD 2,657 away from the "
             "true charge. It treats all errors in proportion to their size and is therefore less "
             "sensitive to extreme values than the next metric.", False, False)],
           indent_first=0.3)
    r.rich([("Root Mean Squared Error (RMSE). ", True, False),
            ("The square root of the average of the squared differences. Squaring penalises large "
             "errors disproportionately, so RMSE is sensitive to how badly the model fails on the "
             "few very expensive individuals. A large gap between MAE and RMSE is a warning that "
             "the model handles typical cases far better than unusual ones, which is exactly the "
             "situation in this dataset.", False, False)],
           indent_first=0.3)
    r.rich([("Coefficient of Determination (R\u00b2). ", True, False),
            ("The proportion of the variance in the target that is explained by the model, with a "
             "value of one indicating a perfect fit and a value of zero indicating that the model "
             "does no better than predicting the mean. It is scale-free and therefore convenient "
             "for comparison, but it should be read alongside the error metrics because it can "
             "appear favourable even when individual predictions are far off in absolute terms.",
             False, False)], indent_first=0.3)

    r.h2("6.3  Comparative Performance of the Models")
    r.p("The three models were trained on the same 1,069 records and evaluated on the same 268 "
        "held-out records. The results are presented in Table 6.2 and visualised in Figure 6.5.",
        space_after=4)
    r.table(
        ["Model", "MAE (USD)", "RMSE (USD)", "R\u00b2 Score", "Rank"],
        [
            ["Linear Regression", "4,177.05", "5,956.34", "0.8069", "3"],
            ["Decision Tree Regressor", "2,787.72", "5,904.67", "0.8103", "2"],
            ["Random Forest Regressor (tuned)", "2,657.61", "4,724.02", "0.8786", "1"],
        ],
        caption="Performance comparison of the three regression models on the test set",
        col_widths=[2.5, 1.05, 1.05, 0.95, 0.6],
        font_size=10.5,
        first_col_bold=True,
        align_center_cols=[1, 2, 3, 4],
    )
    r.figure(os.path.join(FIG, "fig_model_compare.png"),
             "Graphical comparison of MAE, RMSE and R\u00b2 across the three models", width=6.3)

    r.p("Linear Regression achieves an R\u00b2 of 0.8069 with an MAE of USD 4,177.05. This is a "
        "respectable result for a model that assumes a purely additive relationship, and it is "
        "consistent with the actuarial baseline discussed in Chapter 2. Its weakness is visible in "
        "the error: an average absolute error of more than four thousand dollars is far too large "
        "for the estimate to be useful to an individual. The residual behaviour is systematic "
        "rather than random, because the model cannot express the fact that the effect of body "
        "mass index depends on smoking status.")
    r.p("The Decision Tree reduces the MAE to USD 2,787.72, a substantial improvement, but its "
        "R\u00b2 of 0.8103 is almost unchanged, and its RMSE of USD 5,904.67 remains high. This "
        "combination is diagnostic: the single tree fits typical cases better than the linear "
        "model, but it produces occasional very large errors, which inflate the RMSE and hold the "
        "R\u00b2 down. The cause is variance. A single unpruned tree partitions the training rows "
        "into small groups and then predicts a constant within each group, so an unusual test "
        "record that falls into the wrong leaf is predicted badly.")
    r.p("The tuned Random Forest improves on both. Its MAE of USD 2,657.61 is the lowest of the "
        "three, its RMSE of USD 4,724.02 is lower than the other two models by roughly a fifth, "
        "and its R\u00b2 of 0.8786 is the highest. The reduction in RMSE is the more informative "
        "result, because it shows that the ensemble has specifically addressed the large-error "
        "problem that affected the single tree. Averaging six hundred decorrelated trees, each "
        "trained with a restricted depth and a minimum leaf size, converts the high variance of a "
        "single tree into a stable prediction. On the basis of these results, the Random Forest was "
        "retained as the production model.")

    r.h2("6.4  Final Model Configuration and Feature Importance")
    r.p("The final artefact is a scikit-learn Pipeline whose parameters are summarised in "
        "Table 6.3. The complete object, including the fitted scaler, the fitted encoder and all "
        "six hundred trees, is stored in models/random_forest_model.pkl.", space_after=4)
    r.table(
        ["Component", "Configuration", "Effect"],
        [
            ["Numerical preprocessing", "StandardScaler on age, bmi and children",
             "Centres and scales the three numerical attributes to unit variance."],
            ["Categorical preprocessing", "OneHotEncoder(drop='first', "
                                           "handle_unknown='ignore') on sex, smoker and region",
             "Produces five indicator columns and avoids exact collinearity; unseen categories "
             "become zeros instead of raising an error."],
            ["Regressor", "RandomForestRegressor", "Ensemble of bootstrapped decision trees."],
            ["n_estimators", "600", "Averaging over 600 trees gives a stable prediction."],
            ["max_depth", "5", "Restricts tree depth to control overfitting on 1,069 rows."],
            ["min_samples_leaf", "6", "Smooths predictions in the long right tail of the target."],
            ["max_features", "0.8", "Decorrelates the trees by restricting the split candidates."],
            ["random_state", "42", "Makes training fully reproducible."],
            ["Artefact size", "Approximately 2.5 MB", "Small enough for free-tier hosting."],
        ],
        caption="Final configuration of the deployed Random Forest pipeline",
        col_widths=[1.35, 2.4, 2.25],
        font_size=9.5,
        first_col_bold=True,
    )

    r.p("Feature importance provides the explanation of the model. Scikit-learn computes, for "
        "each input feature, the average reduction in impurity that splits on that feature "
        "achieve across all trees, normalised so that the importances sum to one. The results for "
        "the eight encoded features are given in Table 6.4 and shown in Figure 6.6.",
        space_after=4)
    r.table(
        ["Feature (after encoding)", "Relative Importance", "Interpretation"],
        [
            ["smoker_yes", "69.70 %", "Dominant driver of the predicted charge"],
            ["bmi", "16.46 %", "Second most important; interacts strongly with smoking"],
            ["age", "12.28 %", "Steady positive effect on cost"],
            ["children", "1.13 %", "Small but non-zero effect"],
            ["region_southeast", "0.14 %", "Negligible"],
            ["sex_male", "0.11 %", "Negligible"],
            ["region_northwest", "0.10 %", "Negligible"],
            ["region_southwest", "0.09 %", "Negligible"],
        ],
        caption="Feature importance of the tuned Random Forest model",
        col_widths=[1.85, 1.35, 2.8],
        font_size=10.5,
        first_col_bold=True,
        align_center_cols=[1],
    )
    r.figure(os.path.join(FIG, "fig_feature_importance.png"),
             "Feature importance of the final Random Forest model", width=5.7)

    r.p("Three observations follow. First, smoking status alone accounts for nearly seventy per "
        "cent of the model's explanatory power, which formally confirms the impression given by "
        "the box plot in Figure 6.2. Second, body mass index and age together account for almost "
        "thirty per cent, and the fact that body mass index ranks above age is notable given that "
        "age had the higher linear correlation with charges; the forest has captured the "
        "interaction between body mass index and smoking that the correlation coefficient cannot "
        "represent. Third, the remaining features are essentially irrelevant. Sex, region and, to "
        "a lesser extent, number of children contribute almost nothing. This does not mean that "
        "those attributes are uninformative in general, only that within this sample and in the "
        "presence of smoking and body mass index they add very little.")
    r.p("The closeness of the fit is illustrated in Figure 6.7, which plots predicted against "
        "actual charges for the held-out test records. Points cluster around the diagonal, and the "
        "colour coding shows that the residual scatter is concentrated among smokers, whose "
        "charges have a genuinely wider spread. The model compresses the very highest charges "
        "somewhat, which is the expected consequence of an ensemble that averages over trees and of "
        "the depth restriction that was applied to control overfitting.", space_after=4)
    r.figure(os.path.join(FIG, "fig_pred_vs_actual.png"),
             "Predicted against actual charges on the test set", width=4.9)

    r.h2("6.5  Application Output and Screenshots")
    r.p("The application implements the design described in Section 4.7. Its initial state is "
        "shown in Figure 6.8. The header identifies the project, the left panel presents the six "
        "inputs with their default values, and the right panel displays a placeholder that "
        "explains what the user should do. No result is shown until a prediction has been "
        "requested, which avoids presenting a meaningless zero.")
    r.figure(os.path.join(FIG, "app_01_initial.png"),
             "Initial state of the deployed MediPredict application", width=5.9)

    r.p("Figure 6.9 shows the result of an estimate for a forty-five year old female smoker with a "
        "body mass index of 32.5, two dependent children, resident in the south-east region. The "
        "model returns an estimated annual charge of USD 42,741.54, displayed in large type with "
        "the input profile underneath. This individual lies in the high-cost segment of the "
        "dataset, and the estimate is consistent with the visual position of such a record in "
        "Figures 6.2 and 6.3.", space_after=4)
    r.figure(os.path.join(FIG, "app_02_result.png"),
             "Estimation result for a high-risk profile", width=5.9)

    r.p("Figure 6.10 shows the What-if Scenario Simulator after a comparison has been run. The "
        "original profile is retained, and the user has changed two attributes: smoking status "
        "from yes to no, and body mass index from 32.5 to 27.0. The estimated charge falls from "
        "USD 42,741.54 to USD 9,344.13, a reduction of USD 33,397.40 or 78.14 per cent. The "
        "banner states that the cost decreased, and four cards report the original cost, the "
        "what-if cost, the absolute difference and the percentage change.", space_after=4)
    r.figure(os.path.join(FIG, "app_03_whatif.png"),
             "What-if Scenario Simulator showing a cost reduction", width=6.0)

    r.p("This single interaction conveys more than the raw prediction does. It shows that in this "
        "profile almost four-fifths of the estimated cost is attributable to smoking, a factor "
        "that is modifiable. The figure is consistent with the feature importance report, in which "
        "smoking alone accounts for about seventy per cent of the model's explanatory power, and "
        "with the group means in Section 6.1. The simulator therefore does two things at once: it "
        "gives the user a concrete comparison, and it validates the model's internal logic in a "
        "way that a metric alone cannot. The practical interpretation must nevertheless be stated "
        "carefully. The system is reporting what the model has learned from historical data about "
        "the association between smoking and charges; it is not claiming that an individual who "
        "stops smoking will see their premium fall by exactly that amount, since premiums also "
        "depend on policy terms, underwriting rules and future claims experience.")

    r.h2("6.6  Discussion of Results")
    r.p("The results support three conclusions. First, the choice of algorithm matters "
        "substantially on this dataset. Moving from Linear Regression to a tuned Random Forest "
        "reduced the mean absolute error by roughly thirty-six per cent and the root mean squared "
        "error by roughly twenty-one per cent, while raising R\u00b2 from 0.81 to 0.88. The "
        "improvement is not a marginal refinement; it is the difference between an estimate that "
        "is several thousand dollars off on average and one that is within about two and a half "
        "thousand. This is precisely the benefit that the literature reviewed in Chapter 2 "
        "predicts for ensemble methods on tabular data with interactions.")
    r.p("Second, the residual performance is governed by the structure of the population rather "
        "than by the algorithm. Because smoking divides the data into two groups with very "
        "different cost levels, the model's errors are much larger among smokers than among "
        "non-smokers. An aggregate R\u00b2 of 0.88 therefore conceals a considerable asymmetry, "
        "and any serious deployment of such a model would report error metrics separately for the "
        "two groups. This is a limitation of the single aggregate figure rather than of the model, "
        "but it is an important one to state.")
    r.p("Third, the interpretability work is not an afterthought. The feature importance ranking "
        "and the what-if simulator lead to the same conclusion by different routes, which gives "
        "the user a reason to trust the interface. A model that produced the same numbers but "
        "offered no explanation would be of considerably less value even if its accuracy were "
        "identical.")

    r.h2("6.7  Limitations of the Study")
    r.p("The following limitations should be borne in mind when interpreting the results.")
    r.bullets([
        "Small sample. The dataset contains 1,337 unique records after de-duplication, which is "
        "modest for a regression problem with a heavy-tailed target. A larger sample would reduce "
        "the variance of the error estimates and would support a proper three-way split into "
        "training, validation and test sets.",
        "No external validation. All results are from a single random split of one dataset. There "
        "is no second dataset from a different population, so the generalisation of the model "
        "beyond this sample has not been demonstrated.",
        "Limited feature set. The dataset provides six attributes only. It contains no information "
        "on pre-existing conditions, family history, occupation, income, exercise habits or "
        "geography below the level of a four-way region, all of which are known to be relevant to "
        "medical cost.",
        "No time dimension. The records are a single cross-section, so the model cannot represent "
        "trends in medical inflation or changes in an individual's circumstances over time.",
        "Aggregate error reporting. Error metrics are reported for the whole test set. Separate "
        "metrics for the smoking and non-smoking sub-populations would be more informative, as "
        "noted in Section 6.6.",
        "Currency and geography. Charges are in US dollars for a United States population. The "
        "magnitudes are not transferable to another country or healthcare system without "
        "retraining on local data.",
        "Not a pricing engine. The application is an educational estimator. It does not implement "
        "underwriting rules, regulatory constraints or the risk loadings that a real insurer "
        "would apply.",
    ])


def chapter7(r):
    r.h1("Conclusion and Future Work")

    r.h2("7.1  Summary of the Work")
    r.p("This project set out to determine whether the annual medical insurance charges of an "
        "individual can be predicted with useful accuracy from a small set of routinely collected "
        "personal attributes, and whether such a model can be delivered in a form that a "
        "non-technical user can operate and understand. Both questions are answered in the "
        "affirmative.")
    r.p("A publicly available dataset of 1,338 records was cleaned, analysed and modelled. "
        "Exploratory analysis established that charges are strongly right-skewed and that smoking "
        "status divides the population into two groups with markedly different cost behaviour. "
        "Three regression algorithms were trained on a common split and compared on mean absolute "
        "error, root mean squared error and the coefficient of determination. The tuned Random "
        "Forest Regressor performed best, achieving an R\u00b2 of 0.8786, an MAE of USD 2,657.61 "
        "and an RMSE of USD 4,724.02, against 0.8069, USD 4,177.05 and USD 5,956.34 for Linear "
        "Regression. The complete preprocessing and modelling pipeline was serialised and embedded "
        "in a Streamlit web application that returns an estimate in a fraction of a second and "
        "provides an interactive simulator for comparing alternative scenarios.")

    r.h2("7.2  Key Achievements")
    r.p("The principal achievements of the project are listed below.")
    r.numbers([
        "A complete, reproducible machine learning workflow was built, covering data cleaning, "
        "exploratory analysis, feature encoding and scaling, model training, hyperparameter "
        "tuning, evaluation and serialisation.",
        "Three regression algorithms were compared on identical data splits and identical metrics, "
        "so that the benefit of ensembling is demonstrated rather than assumed. The Random Forest "
        "reduced the mean absolute error by approximately thirty-six per cent relative to the "
        "linear baseline.",
        "A leakage-free preprocessing pipeline was designed by placing the scaler and encoder "
        "inside a scikit-learn Pipeline, which eliminates the training-serving mismatch that "
        "commonly breaks deployed models.",
        "A distinct interactive feature, the What-if Scenario Simulator, was implemented. It "
        "reports the absolute and percentage change in the estimated charge when selected "
        "attributes are modified, and thereby converts a single prediction into an explanation.",
        "The model was interpreted through feature importance, which showed that smoking status "
        "accounts for about seventy per cent of the predictive power, followed by body mass index "
        "and age.",
        "The system was deployed publicly on Streamlit Community Cloud at no cost, and the source "
        "code and trained artefact are version controlled on GitHub.",
    ])

    r.h2("7.3  Future Enhancements")
    r.p("Several directions for further work follow naturally from the limitations identified in "
        "Section 6.7.")
    r.bullets([
        "Evaluation of gradient boosting implementations such as XGBoost, LightGBM and CatBoost, "
        "which frequently outperform a random forest on tabular data of this size, together with a "
        "systematic grid or Bayesian search over their hyperparameters.",
        "Replacement of the single train-test split with k-fold cross-validation, and reporting of "
        "the mean and standard deviation of each metric so that the stability of the result is "
        "visible.",
        "Separate evaluation of error metrics for the smoking and non-smoking sub-populations, "
        "which would give a truer picture of where the model fails.",
        "Incorporation of additional features such as pre-existing conditions, occupational risk "
        "category, family history, physical activity and finer geographical detail, subject to the "
        "availability of legitimately sourced data.",
        "Generation of explanation artefacts at the level of the individual prediction, for "
        "example SHAP values, so that the application can state which attributes pushed a "
        "particular estimate up or down and by how much.",
        "Modelling of the target on a logarithmic scale or with a quantile regression objective, "
        "which may improve performance on the long right tail where the current model compresses "
        "the highest charges.",
        "Addition of downloadable PDF reports, comparison of multiple saved profiles, and a small "
        "analytics panel showing where the user's profile lies within the population.",
        "Introduction of automated tests for the prediction path and continuous integration to "
        "verify that a newly trained model reproduces the expected metrics before deployment.",
    ])

    r.h2("7.4  Conclusion")
    r.p("MediPredict demonstrates that a modest, carefully validated machine learning model can "
        "convert an opaque pricing process into something a policyholder can actually inspect. The "
        "technical contribution is small and honest: a tuned Random Forest, correctly packaged and "
        "correctly evaluated. The practical contribution lies in the delivery, because the "
        "comparison facility turns a number into an insight and lets a user see, in a single "
        "interaction, that the dominant determinant of their estimated cost is a modifiable habit "
        "rather than an unchangeable characteristic.")
    r.p("The project also illustrates the value of restraint. A larger feature set was not "
        "available, a more complex algorithm was not required, and an elaborate front-end "
        "framework would have added nothing. What mattered was getting the fundamentals right: "
        "removing the duplicate record, keeping the preprocessing inside the pipeline, splitting "
        "the data before fitting anything, reporting more than one metric, and checking that the "
        "deployed application reproduces the results obtained during development. These are "
        "unglamorous steps, and they are the ones that determine whether a model that performs "
        "well in a notebook also performs well in front of a user. The system is offered as an "
        "educational tool, and as such it achieves its purpose: it makes the relationship between "
        "personal attributes and insurance cost visible, quantitative and testable.")


def references(r):
    r.h1_raw("REFERENCES", size=16)

    refs = [
        "L. Breiman, \u201cRandom Forests,\u201d Machine Learning, vol. 45, no. 1, pp. 5\u201332, "
        "Oct. 2001, doi: 10.1023/A:1010933404324.",

        "J. H. Friedman, \u201cGreedy function approximation: A gradient boosting machine,\u201d "
        "The Annals of Statistics, vol. 29, no. 5, pp. 1189\u20131232, Oct. 2001, doi: "
        "10.1214/aos/1013203451.",

        "P. McCullagh and J. A. Nelder, Generalized Linear Models, 2nd ed. London, U.K.: Chapman "
        "and Hall, 1989.",

        "E. Ohlsson and B. Johansson, Non-Life Insurance Pricing with Generalized Linear Models. "
        "Berlin, Germany: Springer-Verlag, 2010, doi: 10.1007/978-3-642-10791-7.",

        "F. Pedregosa et al., \u201cScikit-learn: Machine learning in Python,\u201d Journal of "
        "Machine Learning Research, vol. 12, pp. 2825\u20132830, Oct. 2011.",

        "W. McKinney, \u201cData structures for statistical computing in Python,\u201d in "
        "Proceedings of the 9th Python in Science Conference, Austin, TX, USA, 2010, pp. 56\u201361, "
        "doi: 10.25080/Majora-92bf1922-00a.",

        "C. R. Harris et al., \u201cArray programming with NumPy,\u201d Nature, vol. 585, no. "
        "7825, pp. 357\u2013362, Sep. 2020, doi: 10.1038/s41586-020-2649-2.",

        "J. D. Hunter, \u201cMatplotlib: A 2D graphics environment,\u201d Computing in Science & "
        "Engineering, vol. 9, no. 3, pp. 90\u201395, May 2007, doi: 10.1109/MCSE.2007.55.",

        "M. L. Waskom, \u201cSeaborn: Statistical data visualization,\u201d Journal of Open Source "
        "Software, vol. 6, no. 60, art. 3021, Apr. 2021, doi: 10.21105/joss.03021.",

        "T. Chen and C. Guestrin, \u201cXGBoost: A scalable tree boosting system,\u201d in "
        "Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and "
        "Data Mining, San Francisco, CA, USA, 2016, pp. 785\u2013794, doi: "
        "10.1145/2939672.2939785.",

        "G. Ke et al., \u201cLightGBM: A highly efficient gradient boosting decision tree,\u201d in "
        "Advances in Neural Information Processing Systems 30, Long Beach, CA, USA, 2017, pp. "
        "3146\u20133154.",

        "S. M. Lundberg and S.-I. Lee, \u201cA unified approach to interpreting model "
        "predictions,\u201d in Advances in Neural Information Processing Systems 30, Long Beach, "
        "CA, USA, 2017, pp. 4765\u20134774.",

        "M. T. Ribeiro, S. Singh, and C. Guestrin, \u201c\u2018Why should I trust you?\u2019: "
        "Explaining the predictions of any classifier,\u201d in Proceedings of the 22nd ACM SIGKDD "
        "International Conference on Knowledge Discovery and Data Mining, San Francisco, CA, USA, "
        "2016, pp. 1135\u20131144, doi: 10.1145/2939672.2939778.",

        "Streamlit Inc., \u201cStreamlit documentation \u2014 API reference,\u201d Streamlit, 2025. "
        "[Online]. Available: https://docs.streamlit.io. [Accessed: 05-Nov-2025].",

        "scikit-learn developers, \u201cscikit-learn user guide: Ensemble methods,\u201d "
        "scikit-learn, 2025. [Online]. Available: "
        "https://scikit-learn.org/stable/modules/ensemble.html. [Accessed: 05-Nov-2025].",

        "Kaggle, \u201cMedical Cost Personal Datasets,\u201d Kaggle Inc., 2025. [Online]. "
        "Available: https://www.kaggle.com/datasets/mirichoi0218/insurance. [Accessed: "
        "05-Nov-2025].",

        "U.S. Centers for Disease Control and Prevention, \u201cSmoking and Tobacco Use: Health "
        "Effects,\u201d CDC, 2025. [Online]. Available: "
        "https://www.cdc.gov/tobacco/data_statistics/fact_sheets/health_effects/. [Accessed: "
        "05-Nov-2025].",

        "Python Software Foundation, \u201cThe Python Language Reference, version 3.10,\u201d "
        "2025. [Online]. Available: https://docs.python.org/3/. [Accessed: 05-Nov-2025].",
    ]

    for i, ref in enumerate(refs, start=1):
        p = r.p(f"[{i}]\t{ref}", size=11.5, align="justify", space_after=8, line_spacing=1.3)
        p.paragraph_format.left_indent = __import__("docx").shared.Inches(0.45)
        p.paragraph_format.first_line_indent = __import__("docx").shared.Inches(-0.45)


def appendices(r):
    r.h1_raw("APPENDIX A", size=16)
    r.h2("Project Structure and Useful Commands")
    r.p("The repository is available at https://github.com/OrioRiko-09/Medical-Insurance-Prediction "
        "and the deployed application at https://med-pred.streamlit.app/. The commands required to "
        "reproduce the environment and to run the application locally are listed below.",
        space_after=6)
    r.code_block([
        "# 1. Clone the repository",
        "git clone https://github.com/OrioRiko-09/Medical-Insurance-Prediction",
        "cd Medical-Insurance-Prediction",
        "",
        "# 2. Create and activate a virtual environment",
        "python -m venv .venv",
        ".venv\\Scripts\\activate          # Windows",
        "source .venv/bin/activate        # Linux / macOS",
        "",
        "# 3. Install the pinned dependencies",
        "pip install -r requirements.txt",
        "",
        "# 4. Run the application locally",
        "streamlit run app.py             # opens http://localhost:8501",
        "",
        "# 5. Inspect the trained artefact",
        "python -c \"import joblib; m = joblib.load("
        "'models/random_forest_model.pkl'); print(m)\"",
    ])

    r.h1_raw("APPENDIX B", size=16)
    r.h2("Viva Voce Preparation \u2014 Questions and Answers")
    r.p("The following questions are those most likely to be asked during the evaluation of this "
        "project. The answers are deliberately concise and point to the relevant section of the "
        "report where a fuller treatment is available.", space_after=6)

    qas = [
        ("Why was Random Forest chosen over Linear Regression?",
         "Because the relationship between the attributes and the charges is not additive. Body "
         "mass index matters far more for a smoker than for a non-smoker, and a linear model "
         "cannot express that interaction unless the term is specified by hand. The Random Forest "
         "learns such interactions automatically. Empirically, it reduced the mean absolute error "
         "from USD 4,177 to USD 2,658 and raised R\u00b2 from 0.8069 to 0.8786 (Section 6.3)."),
        ("What does an R\u00b2 of 0.8786 actually mean?",
         "It means that the model explains about 87.9 per cent of the variance in insurance charges "
         "in the held-out test set. It does not mean that each prediction is 87.9 per cent "
         "accurate. For the absolute accuracy of individual predictions, the mean absolute error "
         "of USD 2,657.61 is the more useful figure (Section 6.2)."),
        ("Why did you drop only one duplicate record, and does it matter?",
         "Because the dataset contains exactly one fully duplicated row, which is almost certainly "
         "an entry error and carries no information. The effect on the model is negligible, but "
         "removing it is correct practice because duplicated rows distort both the training data "
         "and any cross-validation split."),
        ("Why did you standardise the numerical features if Random Forests are scale-invariant?",
         "The forest is scale-invariant, so scaling does not change its accuracy here. The scaler "
         "is retained for two reasons: it keeps the pipeline reusable if a linear or distance-based "
         "model is later substituted, and it makes feature importances and any future coefficient "
         "inspection directly comparable across attributes of different units (Section 4.6)."),
        ("What is the purpose of OneHotEncoder(drop='first')?",
         "It converts each categorical attribute into k minus one binary columns. Dropping the "
         "first category avoids perfect collinearity between the indicator columns, which would "
         "destabilise a linear model. The dropped level becomes the reference category, so "
         "interpretations are relative to a non-smoking woman from the north-east."),
        ("Why is the preprocessing inside the pipeline rather than applied beforehand?",
         "To prevent data leakage. If the scaler were fitted on the whole dataset before splitting, "
         "information from the test set would influence the training data and the evaluation would "
         "be optimistic. Inside the pipeline, the transformers are fitted only on the training "
         "split, and the identical fitted parameters are then applied at prediction time. This also "
         "eliminates any mismatch between training and serving (Section 5.3)."),
        ("What does st.cache_resource do and why is it used?",
         "Streamlit re-runs the whole script on every interaction. Without caching, the 2.5 MB "
         "model file would be read from disk and unpickled on every keystroke. cache_resource "
         "loads it once and shares the same object across all re-runs and all users of the session, "
         "which makes the interface responsive (Section 5.5)."),
        ("Why is the prediction stored in st.session_state?",
         "Because local variables are discarded on every re-run of the script. If the prediction "
         "were kept in a local variable, the result card would disappear as soon as the user "
         "touched another widget. Session state preserves both the predicted amount and the input "
         "profile for the duration of the session (Section 5.6)."),
        ("How does the What-if Simulator differ from simply predicting twice?",
         "Functionally it does predict twice, but the value is in the presentation. It holds sex "
         "constant and states that it is doing so, it constrains age so that a backward comparison "
         "is impossible, it computes the absolute and percentage difference, and it uses colour and "
         "a banner to communicate the direction of the change. It converts two numbers into an "
         "interpretable comparison (Section 5.7)."),
        ("Why is sex not modifiable in the simulator?",
         "Because sex is not a modifiable characteristic, and allowing it to be changed would invite "
         "an interpretation that the tool does not support. Holding it constant keeps the comparison "
         "focused on factors that a person could actually act upon. The interface displays a badge "
         "stating which value is being held constant, so the basis of comparison is explicit."),
        ("Which feature matters most, and how do you know?",
         "Smoking status, at approximately 69.7 per cent of total feature importance, followed by "
         "body mass index at 16.5 per cent and age at 12.3 per cent. The ranking comes from the "
         "impurity-based importance computed by scikit-learn across all six hundred trees, and it "
         "is corroborated independently by the group means in the exploratory analysis and by the "
         "what-if demonstration (Section 6.4)."),
        ("What are the limitations of impurity-based feature importance?",
         "It is biased towards features with many distinct values, and it measures importance only "
         "within the training distribution, so it can be misleading when features are correlated. "
         "In this dataset the predictors are almost uncorrelated, so the bias is small, but "
         "permutation importance or SHAP values would be a more robust alternative and are listed "
         "as future work."),
        ("How did you tune the hyperparameters?",
         "Four parameters were explored: the number of trees, the maximum depth, the minimum number "
         "of samples per leaf and the number of features considered per split. Depth and leaf size "
         "were the parameters that mattered, because an unrestricted forest overfits 1,069 training "
         "rows. The retained configuration is 600 trees, depth 5, minimum leaf size 6 and 0.8 "
         "features per split with random_state 42 (Table 5.3)."),
        ("Why not use deep learning?",
         "Because the dataset is small, tabular and contains only six attributes. Neural networks "
         "require far more data to generalise, offer no accuracy advantage on data of this shape, "
         "and are considerably harder to explain. Tree ensembles are the established best practice "
         "for tabular regression of this kind."),
        ("What would you do differently with more time?",
         "Three things: replace the single split with k-fold cross-validation and report the spread "
         "of each metric, evaluate gradient boosting implementations, and report error metrics "
         "separately for smokers and non-smokers, since the aggregate R\u00b2 conceals a large "
         "asymmetry between those groups (Sections 6.7 and 7.3)."),
        ("How do you know the deployed application gives the same result as your notebook?",
         "The same serialised pipeline is used in both cases, so the transformation and the "
         "prediction are identical by construction. Spot checks were performed by recomputing a "
         "handful of predictions directly from the .pkl file and comparing them with the values "
         "displayed by the application."),
        ("Is the output a premium quotation?",
         "No. It is a statistical estimate of the medical charges associated with a profile, "
         "learned from a public dataset of 1,337 individuals in the United States. It does not "
         "implement underwriting rules, loadings, deductibles or regulatory constraints, and the "
         "application states this in its disclaimer."),
    ]

    for i, (q, a) in enumerate(qas, start=1):
        r.rich([(f"Q{i}.  ", True, False), (q, True, False)], align="left",
               space_after=2, line_spacing=1.3)
        r.p(a, size=11.5, align="justify", space_after=9, line_spacing=1.3)
