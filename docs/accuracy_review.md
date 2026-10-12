# Final accuracy review

| Model | Threshold | Train accuracy | Validation accuracy | Test accuracy | Selected |
| --- | --- | --- | --- | --- | --- |
| Random Forest | 0.425 | 71.56% | 68.63% | 67.12% | Yes |
| Logistic Regression | 0.425 | 68.67% | 68.29% | 67.37% | No |
| Gradient Boosting | 0.375 | 67.21% | 67.88% | 65.88% | No |
| Decision Tree | 0.425 | 65.28% | 66.10% | 65.69% | No |

Random Forest is the validation-selected model at threshold 0.425. Its test accuracy is 67.12%; Logistic Regression scores 67.37% on the same reused test period. The latter does not change the validation-based selection. The improvement over the always-active test baseline (61.95%) is 5.18 percentage points for Random Forest.

Validation and test periods were inspected during earlier development. These are reused-holdout results, not fresh independent confirmation. Customer-grouped CV is a diagnostic within the training period; repeated CV is not nested evaluation. Small fitting gaps do not prove absence of overfitting or underfitting. Confirm the frozen model on genuinely new future data before making performance claims.

See the complete [model/method comparison](model_method_comparison.md) for additional metrics, parameters and fitting evidence.

Evidence: [final comparison CSV](../outputs/final_four/model_comparison.csv), [selection record](../outputs/final_four/selection.json), the four individual [model notebooks](../notebooks/), and [final verification notebook](../notebooks/FINAL_Four_Optimized_Models.ipynb).
