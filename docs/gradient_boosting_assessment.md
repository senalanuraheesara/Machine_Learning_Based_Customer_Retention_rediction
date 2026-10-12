# Gradient Boosting assessment

Gradient Boosting is one of the final four comparison models; **it is not the selected model**. Earlier documents describing it as the retained incumbent belong to a superseded development stage.

The final standard GradientBoostingClassifier uses 80 estimators, learning_rate=0.05, max_depth=1, min_samples_leaf=60, subsample=0.7 and random_state=42. Its frozen threshold is **0.375**, not the previous 0.410.

| Measure | Final value |
| --- | --- |
| Training accuracy | 67.21% |
| Validation accuracy | 67.88% |
| Test accuracy | 65.88% |
| Threshold-matched CV gap | 2.40 percentage points |
| Test recall (inactive class) | 72.95% |
| Test F1 | 0.619346 |

It passes the current fitting screens but falls below Random Forest's validation accuracy (68.63%). Higher test recall is a tradeoff, not a reason to change an accuracy-based selection after viewing test results. A threshold change can change accuracy without changing the fitted trees.

Evidence: [Gradient Boosting notebook](../notebooks/03_04_gradient_boosting.ipynb), [final comparison](../outputs/final_four/model_comparison.csv). See [evaluation limits and comparison](model_method_comparison.md).
