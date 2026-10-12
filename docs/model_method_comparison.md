# Model and method comparison

The final classifier predicts **no positive, non-cancelled purchase during the next two months** (class 1). Random Forest is selected by validation accuracy after fitting screens, at threshold **0.425**.

## Final quantitative comparison

| Model | Threshold | Train accuracy | Validation accuracy | Test accuracy | Selected |
| --- | --- | --- | --- | --- | --- |
| Random Forest | 0.425 | 71.56% | 68.63% | 67.12% | Yes |
| Logistic Regression | 0.425 | 68.67% | 68.29% | 67.37% | No |
| Gradient Boosting | 0.375 | 67.21% | 67.88% | 65.88% | No |
| Decision Tree | 0.425 | 65.28% | 66.10% | 65.69% | No |

All split accuracies use each model's frozen threshold. Random Forest leads Logistic Regression by 0.34 percentage points on validation; this small difference is not evidence of statistically established superiority. Logistic Regression's test accuracy is 0.25 points higher, but test rank is not the selection rule. Random Forest exceeds the always-active test baseline (61.95%) by 5.18 points.

## Method tradeoffs

| Method | Role and benefit | Tradeoff / observed result |
| --- | --- | --- |
| Majority-class baseline | Always predict active (class 0); reference for accuracy | Training 62.20%, validation 54.32%, test 61.95%; no risk differentiation. |
| Logistic Regression | Regularized linear probability classifier with transformed behavioral features | Simple benchmark; 68.29% validation. Best final test accuracy, but test ranking does not select the winner. |
| Decision Tree | Shallow, pruned rules for interpretability | 66.10% validation; lowest validation score among the four. |
| Random Forest | Bagged trees using compact behavioral features | 68.63% validation; selected. More complex and larger fitting gap than Logistic Regression. |
| Gradient Boosting | Sequential shallow trees | 67.88% validation; higher inactive-class recall in saved test output, but lower accuracy. |
| K-means | Unsupervised behavioral segmentation, independent of classifier labels during fitting | Final k=2 groups 1,696 customers into 1,577 and 119. Not comparable to classifiers by accuracy; statistical separation is not business usefulness. |
| PCA | Two-dimensional clustering visualization | Display only; not a competing classifier or clustering selection criterion. |
| Spline/kernel logistic, histogram boosting, soft voting | Historical alternative models in archived optimization | Excluded from final four-family scope; not an untested proposal and not the current deliverable. |

## Frozen parameters

| Model | Frozen estimator settings |
| --- | --- |
| Logistic Regression | C=0.01; max_iter=3000; solver=lbfgs; class_weight=None; random_state=42 |
| Decision Tree | max_depth=2; min_samples_leaf=30; ccp_alpha=0.005; random_state=42 |
| Random Forest | 350 trees; max_depth=8; min_samples_leaf=60; max_features=0.7; max_samples=1.0; bootstrap=True; random_state=42 |
| Gradient Boosting | 80 estimators; learning_rate=0.05; max_depth=1; min_samples_leaf=60; subsample=0.7; random_state=42 |

These are the displayed settings of the saved final models, not a new search. The individual notebooks load bundles by default. `RETRAIN=True` refits fixed settings on training data without replacing the published artifacts.

## Additional classification metrics

| Model | Test precision | Test recall | Test F1 | Test ROC-AUC | Test PR-AUC |
| --- | --- | --- | --- | --- | --- |
| Random Forest | 0.556617 | 0.668852 | 0.607595 | 0.731184 | 0.592246 |
| Logistic Regression | 0.560333 | 0.662295 | 0.607062 | 0.730448 | 0.580260 |
| Gradient Boosting | 0.538089 | 0.729508 | 0.619346 | 0.737313 | 0.604435 |
| Decision Tree | 0.539474 | 0.672131 | 0.598540 | 0.704729 | 0.531898 |

Values above are copied from the individual notebooks' saved test outputs (six decimal places). Precision, recall and F1 treat inactivity as the positive class. ROC-AUC and PR-AUC summarize probability ranking; the helper computes PR-AUC using average precision. Gradient Boosting's higher recall/F1 does not override the implemented accuracy objective. A cost-sensitive objective would need an explicit business decision and fresh validation.

## Fitting evidence

| Model | CV accuracy at 0.50 | CV accuracy at frozen threshold | CV gap at frozen threshold (pp) | Train–validation gap (pp) | Train–test gap (pp) |
| --- | --- | --- | --- | --- | --- |
| Random Forest | 69.59% | 67.61% | 4.15 | 2.93 | 4.43 |
| Logistic Regression | 69.18% | 68.52% | 0.81 | 0.39 | 1.30 |
| Gradient Boosting | 69.54% | 65.74% | 2.40 | -0.67 | 1.33 |
| Decision Tree | 68.22% | 65.59% | 1.16 | -0.81 | -0.41 |

CV accuracy at 0.50 and threshold-matched audit accuracy use different operating points and potentially different fold partitions; do not subtract them to calculate a fitting gap. Each reported gap compares training and held-out scores within its own audit. See [fitting review](fit_control_review.md).

## Evaluation limits

Validation and test periods were inspected during earlier development. These are reused-holdout results, not fresh independent confirmation. Customer-grouped CV is a diagnostic within the training period; repeated CV is not nested evaluation. Small fitting gaps do not prove absence of overfitting or underfitting. Confirm the frozen model on genuinely new future data before making performance claims.

Evidence: [final comparison CSV](../outputs/final_four/model_comparison.csv), [selection record](../outputs/final_four/selection.json), the four individual [model notebooks](../notebooks/), and [final verification notebook](../notebooks/FINAL_Four_Optimized_Models.ipynb).


## Reproducibility update

The four individual notebooks now display historical tuning trials and final-settings three-fold CV evidence. Training/tuning can be rerun with the supported clean-package workflow; see [reproducibility instructions](reproducibility.md). Historical and newly computed evidence are distinguished, and the published final models remain unchanged.
