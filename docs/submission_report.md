# Retail customer inactivity prediction — submission report

## Objective and data

Predict which established customers will make no positive, non-cancelled purchase in the next two months, using prior retail transactions. Inactivity is an operational proxy; it does not establish permanent customer churn. The source contains 541,909 transaction lines, eight fields and dates from December 2010 to December 2011.

Cleaning removes exact duplicates, missing customer identities and non-positive prices, leaving 401,564 rows. Returns remain available as behavior. Rolling customer snapshots use a six-month lookback and two-month outcome horizon, with at least two distinct invoices and 60 history days. Early lookbacks have incomplete history because the source starts in December 2010.

## Experimental design

| Prediction date | Snapshots | Inactive rate | Classifier use |
| --- | --- | --- | --- |
| 2011-03-31 | 854 | 35.95% | Train |
| 2011-04-30 | 1122 | 39.22% | Train |
| 2011-05-31 | 1412 | 44.33% | Excluded from classifier splits |
| 2011-06-30 | 1460 | 45.68% | Validation |
| 2011-07-31 | 1553 | 42.63% | Excluded from classifier splits |
| 2011-08-31 | 1603 | 38.05% | Test |

The classifier has 1,976 training rows, 1,460 validation rows and 1,603 test rows. Customer identities may recur across temporal splits; customer-grouped three-fold CV separates identities within training folds. Pipelines fit imputation/encoding and model-specific scaling inside CV. The input contract contains 35 columns; individual pipelines use their saved subsets/derived features. Caps and country grouping use past snapshot cohorts, rather than customer-disjoint fold fitting.

For each prediction date t, features use transactions in [t − 6 calendar months, t), while the inactivity label uses [t, t + 2 calendar months). Training uses 31 March and 30 April 2011 snapshots; validation uses 30 June; test uses 31 August. May and July snapshots are excluded so the earlier partition's outcome window finishes before the next selected prediction date. This chronological design reduces future-information leakage but does not make an already inspected holdout independent again.

Hyperparameter selection uses three-fold StratifiedGroupKFold within the training partition (shuffle=True, seed 42). All snapshots of a customer stay on the same side of each fold. The seed-137 repeated audit is a sensitivity check, not an independent temporal test or nested CV. These folds evaluate held-out customers within the training period; they do not measure generalization to a genuinely new future period.

After fitting on training data, the operating threshold is chosen using June validation accuracy over 17 thresholds from 0.25 to 0.65 in steps of 0.025. Ties prefer the threshold closest to 0.50, then the lower threshold. Eligible model variants are compared by validation accuracy, with exact ties resolved by CV accuracy and name. This produces Random Forest with threshold 0.425. The implemented final selection rule does not use August test ranking, but previous inspection of that period still limits the independence of the reported results.

## Decisions and method comparison

The complete [decision log](decision_log.md) records 16 choices with alternatives, reasons, consequences and evidence, covering cleaning, target, features, splits, CV, tuning, thresholds, selection and segmentation.

| Model | Threshold | Train accuracy | Validation accuracy | Test accuracy | Selected |
| --- | --- | --- | --- | --- | --- |
| Random Forest | 0.425 | 71.56% | 68.63% | 67.12% | Yes |
| Logistic Regression | 0.425 | 68.67% | 68.29% | 67.37% | No |
| Gradient Boosting | 0.375 | 67.21% | 67.88% | 65.88% | No |
| Decision Tree | 0.425 | 65.28% | 66.10% | 65.69% | No |

Random Forest is selected at **0.425** by the highest validation accuracy among fitting-eligible variants. Its validation advantage over Logistic Regression is only 0.34 percentage points and is not established as statistically significant. Logistic Regression has slightly higher test accuracy; that result does not change the validation rule. Random Forest's test precision is 0.556617, recall 0.668852, F1 0.607595, ROC-AUC 0.731184 and average precision 0.592246, as displayed in its saved notebook.

The [model/method comparison](model_method_comparison.md) provides baseline performance, all final parameters, additional metrics, model tradeoffs and CV diagnostics. The always-active test baseline is 61.95%, compared with 67.12% for Random Forest.

## Fitting and evaluation

All four final variants pass the saved heuristic fitting screens. Random Forest's threshold-matched train–CV gap is 4.15 percentage points and train–validation gap is 2.93 points, both below the chosen five-point limit. Training accuracy is in-sample, and gap screening alone cannot establish generalization.

Validation and test periods were inspected during earlier development. These are reused-holdout results, not fresh independent confirmation. Customer-grouped CV is a diagnostic within the training period; repeated CV is not nested evaluation. Small fitting gaps do not prove absence of overfitting or underfitting. Confirm the frozen model on genuinely new future data before making performance claims.

**The reported 67.12% Random Forest test accuracy is descriptive performance on a reused holdout, not a fully independent estimate of generalization.** Repeated inspection can influence development choices even when the final selection code excludes test scores. Repeating CV, changing a random seed or renaming an existing split cannot remove this limitation.

### Evaluation on genuinely untouched later data

No new dataset with verified untouched status has been supplied for this revision, so no independent future-period evaluation is claimed. Later dates already present in the source workbook must not automatically be treated as untouched: their prior use and inspection would first need to be established.

If suitable later data becomes available, record its provenance and define the cohort, cutoff, two-month outcome window and reporting metrics before inspecting outcomes. Freeze the existing Random Forest bundle, feature definitions, fitted preprocessing and threshold **0.425**; do not retrain, recalibrate, retune or select a different model using this evaluation cohort. Compute features only from transactions available before each cutoff, and wait until the full two-month outcome window is observed. Apply the frozen pipeline and threshold, then report sample size, class balance, accuracy, precision, recall, F1, ROC-AUC and average precision alongside the always-active baseline and uncertainty estimates. If customers contribute repeated snapshots, account for that dependence when estimating uncertainty.

Report that future result separately from the reused August holdout. If the new results subsequently guide model changes, reserve another untouched period for independent confirmation of the revised model.

## Segmentation outcome

The final K-means workflow selects k=2 by silhouette (0.689517) on 1,696 fixed-window customers. Cluster sizes are 1,577 and 119 after Yeo–Johnson transformation, robust scaling and percentile clipping of ten behavioral features. Observed inactivity is 30.18% versus 26.89%; these are not classifier predictions. Stability and business usefulness remain unvalidated. See [segmentation assessment](segmentation_assessment.md).

## Deliverables and reproducibility

The final artifacts are the four bundles, comparison CSVs and selection JSON in [outputs/final_four](../outputs/final_four/). Each bundle stores its pipeline, metadata and frozen threshold. The individual model notebooks and final verification notebook compare predictions against the published accuracies and check the data fingerprint. [START_HERE](../START_HERE.md) explains execution order and environment limitations.

This report follows the supplied notebooks and artifacts. No separate assignment rubric was present, so institution-specific formatting, word limits or additional submission requirements have not been verified.


## Reproducibility update

The four individual notebooks now display historical tuning trials and final-settings three-fold CV evidence. Training/tuning can be rerun with the supported clean-package workflow; see [reproducibility instructions](reproducibility.md). Historical and newly computed evidence are distinguished, and the published final models remain unchanged.
