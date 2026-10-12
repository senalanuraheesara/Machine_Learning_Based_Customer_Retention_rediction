# Project decision log

This log is reconstructed from the current notebook code, saved outputs and helper scripts. It is not a timestamped record of original deliberations. Alternatives are documented design tradeoffs; only explicitly identified experiments have measured results.

| ID | Implemented decision | Alternative | Reason / consequence | Evidence location |
| --- | --- | --- | --- | --- |
| D01 | Remove exact duplicates | Keep all rows | Avoid double-counted activity; 541,909 → 536,641 rows. | 02_preprocessing, cleaning |
| D02 | Drop missing CustomerID | Impute or assign one placeholder ID | Cannot reliably join transactions to customers; 536,641 → 401,604 rows. Excludes anonymous customers. | 02_preprocessing, cleaning |
| D03 | Require UnitPrice > 0 | Impute invalid prices | Avoid invented revenue; 401,604 → 401,564 rows. | 02_preprocessing, cleaning |
| D04 | Retain returns and cancellations in legacy features | Delete all negative transactions | Preserve return behavior; positive-only features distinguish purchases. Returns do not count as outcome activity. | 02_preprocessing; model_workflow.enrich_snapshots |
| D05 | Recompute 99th-percentile caps and top-five country groups per lookback | Use full-period caps/groups | Avoid future information in rolling features. Caps are snapshot-wide, not refitted within customer CV folds. | 02_preprocessing, rolling snapshots |
| D06 | Six-month lookback; two-month inactivity target | Fixed-day lapse, spend decline or frequency decline | Provides a common prediction horizon. Earliest lookbacks are truncated by the source start date. | 02_preprocessing, rolling snapshots |
| D07 | At least two distinct invoices and 60 history days | Include one-invoice/new customers; old three-invoice rule | Require some history. Invoice eligibility can include returns and limits applicability to new customers. | 02_preprocessing, rolling snapshots |
| D08 | March/April train; June validation; August test | Random row split; all monthly snapshots | Keep adjacent outcome windows from crossing into the next selected prediction period. May/July excluded. Customers can recur across temporal splits. | model_workflow.load_features |
| D09 | Customer-disjoint three-fold CV, seed 42; repeat seed 137 | Ordinary random row CV | Avoid the same customer appearing on both sides of a training CV fold. Repeat is a sensitivity check. | clean_optimization; audit_clean_fitting |
| D10 | Pipeline imputation/encoding; log and scaling for Logistic Regression | Globally fitted preprocessing | Fit learned pipeline transforms within CV training folds. Unseen countries are ignored by encoding. | model_workflow; accuracy_experiments |
| D11 | Compare four classical model families | Include every experimental variant in final submission | Final scope is Logistic Regression, Decision Tree, Random Forest and standard Gradient Boosting; other trials retained as history. | finalize_four_models |
| D12 | Apply gap/baseline/capacity fitting screens | Select on training accuracy or gap alone | Limit complexity without accepting weak near-baseline models; heuristic screens are not guarantees. | clean_optimization; audit_clean_fitting |
| D13 | Select threshold by validation accuracy on 17 values from 0.25 to 0.65 | Default 0.50 or previous finer grid | Common 0.025 grid; ties prefer nearest 0.50, then lower threshold. Threshold optimization can overfit validation. | accuracy_experiments.select_threshold |
| D14 | Select Random Forest at 0.425 | Choose by test accuracy or retain old Gradient Boosting selection | Highest eligible validation accuracy: 68.63%. Exact ties use CV accuracy then name. Logistic Regression has slightly higher test accuracy, which does not change this selection. | final_four/selection.json |
| D15 | K-means, k=2–6; choose maximum silhouette on final transformed inputs | Other k values; other clustering algorithms | Final ten-feature workflow uses Yeo–Johnson, robust scaling and 1%/99% clipping; k=2 yields 1,577/119 customers. Earlier experiments are superseded; stability remains unvalidated. | 04_segmentation |
| D16 | Disclose holdout reuse and segmentation limitations | Claim unseen-test validation or actionable clusters | Maintain an accurate account of what the saved evidence supports. Fresh temporal evaluation and cluster stability assessment remain future work. | Final notebooks; documentation review |

See [preprocessing details](preprocessing_log.md), [model/method comparison](model_method_comparison.md) and [segmentation assessment](segmentation_assessment.md).
