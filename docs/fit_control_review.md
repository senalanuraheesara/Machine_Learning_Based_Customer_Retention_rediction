# Final model fitting review

The final selection is **Random Forest**, not the older Gradient Boosting incumbent. All four packaged variants pass the saved fitting screens.

| Model | CV accuracy at 0.50 | CV accuracy at frozen threshold | CV gap at frozen threshold (pp) | Train–validation gap (pp) | Train–test gap (pp) |
| --- | --- | --- | --- | --- | --- |
| Random Forest | 69.59% | 67.61% | 4.15 | 2.93 | 4.43 |
| Logistic Regression | 69.18% | 68.52% | 0.81 | 0.39 | 1.30 |
| Gradient Boosting | 69.54% | 65.74% | 2.40 | -0.67 | 1.33 |
| Decision Tree | 68.22% | 65.59% | 1.16 | -0.81 | -0.41 |

The search selector requires mean train–CV gap ≤ 5 percentage points, CV accuracy ≥ training majority baseline + 3 points, and accuracy within 1 point of the best searched candidate. Within 0.2 points of the best eligible score it prefers a smaller non-negative gap. No eligible configuration means failure rather than an unsafe fallback.

The clean optimization adds repeat three-fold customer-grouped CV (seed 137) and a train–validation gap ≤ 5 points. The subsequent frozen-threshold audit checks default/repeated/threshold-matched CV gaps and temporal gap, plus CV improvement over baseline. Selection packaging requires both optimization eligibility and audit pass. Search CV uses seed 42 and default 0.50 predictions; threshold-matched audit uses each frozen threshold.

Random Forest's matched CV gap is 4.15 points, train–validation gap 2.93 and descriptive train–test gap 4.43. These are within the chosen limits. Threshold-matched CV accuracy is 67.61%, above the training majority baseline of 62.20%. This indicates useful signal under the current screen, not proof of optimal complexity or absence of missing predictors.

Validation and test periods were inspected during earlier development. These are reused-holdout results, not fresh independent confirmation. Customer-grouped CV is a diagnostic within the training period; repeated CV is not nested evaluation. Small fitting gaps do not prove absence of overfitting or underfitting. Confirm the frozen model on genuinely new future data before making performance claims.

Evidence: [saved fitting audit](../outputs/evidence/optimization/fitting_audit.csv), [audit implementation](../outputs/evidence/source/audit_clean_fitting.py), [selection implementation](../outputs/evidence/source/finalize_four_models.py). Earlier `outputs/tables/fit_control_status.csv` and selected-model assessments can describe older variants; use the final bundle source mapping.
