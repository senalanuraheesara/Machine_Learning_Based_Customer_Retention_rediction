# Final four optimized models

Selected: **Random Forest**, threshold **0.425**. Selection uses highest eligible validation accuracy; exact ties use CV accuracy then name.

| Model | Threshold | Train accuracy | Validation accuracy | Test accuracy | Selected |
| --- | --- | --- | --- | --- | --- |
| Random Forest | 0.425 | 71.56% | 68.63% | 67.12% | Yes |
| Logistic Regression | 0.425 | 68.67% | 68.29% | 67.37% | No |
| Gradient Boosting | 0.375 | 67.21% | 67.88% | 65.88% | No |
| Decision Tree | 0.425 | 65.28% | 66.10% | 65.69% | No |

Each joblib contains `pipeline` and `metadata`. Keep `src` importable, select inputs with `model_workflow.matrix(data)` and classify with `pipeline.predict_proba(X)[:, 1] >= metadata['Threshold']`. Calling `pipeline.predict()` would apply a different operating threshold. Load only trusted model files.

`accuracy_summary.csv` contains per-family results; `model_comparison.csv` ranks them and includes fitting eligibility; `selection.json` records source variants, thresholds, rule and data fingerprint. The individual model notebooks and final notebook verify these accuracies against saved pipelines.

See the [submission report](../../docs/submission_report.md), [decision log](../../docs/decision_log.md) and [method comparison](../../docs/model_method_comparison.md).

Validation and test periods were inspected during earlier development. These are reused-holdout results, not fresh independent confirmation. Customer-grouped CV is a diagnostic within the training period; repeated CV is not nested evaluation. Small fitting gaps do not prove absence of overfitting or underfitting. Confirm the frozen model on genuinely new future data before making performance claims.
