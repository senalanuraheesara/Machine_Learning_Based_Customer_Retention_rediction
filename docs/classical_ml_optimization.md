# Optimization provenance and final scope

The submission contains exactly four model families: Logistic Regression, Decision Tree, Random Forest and standard Gradient Boosting. Final variants and thresholds are recorded in [selection.json](../outputs/final_four/selection.json); [model/method comparison](model_method_comparison.md) is the current results reference.

The earlier bounded search in `src/accuracy_experiments.py` considers compact/full features, regularization, depth/leaf limits and nonlinear classical alternatives. `outputs/evidence/source/clean_optimization.py` reassesses existing candidates and searches seven updated families with up to 32 configurations per family using three-fold customer-grouped CV. Updated searches use seed 73, primary folds seed 42 and repeated folds seed 137. Their outputs are archived under `outputs/evidence/optimization/`.

Threshold selection for the clean comparison uses 17 validation thresholds from 0.25 to 0.65. Eligibility includes default and repeated CV, baseline improvement, capacity loss and temporal gap controls. `outputs/evidence/source/audit_clean_fitting.py` adds a threshold-matched audit. `outputs/evidence/source/finalize_four_models.py` retains the best eligible validation variant within each requested family and then selects across those four. Exact ties use CV accuracy, then name.

| Final family | Saved source variant |
| --- | --- |
| Logistic Regression | optimized_logistic_regression |
| Decision Tree | decision_tree |
| Random Forest | random_forest |
| Gradient Boosting | gradient_boosting |

Spline/kernel logistic regression, histogram boosting and voting ensembles remain historical experiments. Results from different thresholds or model revisions are not interchangeable. The final Random Forest is the archived clean-optimization variant, so an earlier report about a separately retrained forest must not be substituted for its evidence.

The current model notebooks verify saved bundles; their optional RETRAIN switch refits frozen settings, not hyperparameter search. The packaging script copies archived fitted pipelines and regenerates its README and final notebook. Historical scripts may expect pre-archive paths and should not be treated as a turnkey clean rebuild. Revalidate data/model provenance before repackaging; do not simply stamp old models with a changed data fingerprint.

Validation/test reuse remains a limitation. See [fitting review](fit_control_review.md) and [decision log](decision_log.md).


## Reproducibility update

The four individual notebooks now display historical tuning trials and final-settings three-fold CV evidence. Training/tuning can be rerun with the supported clean-package workflow; see [reproducibility instructions](reproducibility.md). Historical and newly computed evidence are distinguished, and the published final models remain unchanged.
