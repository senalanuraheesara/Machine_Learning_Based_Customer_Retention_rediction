# Submission documentation

Start with the [submission report](submission_report.md). The two requested submission components are the [decision log](decision_log.md) and [model/method comparison](model_method_comparison.md).

| Document | Purpose |
| --- | --- |
| [Preprocessing log](preprocessing_log.md) | Sequential cleaning counts, rolling target and temporal splits |
| [Data dictionary](data_dictionary.md) | Raw fields, quality issues and derived identifiers |
| [Feature engineering log](feature_engineering_log.md) | Feature decisions and limitations |
| [Feature contract](snapshot_feature_contract.md) | Exact input semantics and per-model processing |
| [Accuracy review](accuracy_review.md) | Current final scores |
| [Fitting review](fit_control_review.md) | CV, thresholds, gaps and heuristic controls |
| [Gradient Boosting assessment](gradient_boosting_assessment.md) | Final comparison model, not the selected incumbent |
| [Optimization provenance](classical_ml_optimization.md) | Search history and final variant mapping |
| [Segmentation assessment](segmentation_assessment.md) | Final 1,577/119 result and interpretation limits |
| [Documentation audit](documentation_audit.md) | Corrections, evidence checks and reproducibility limits |

Use `outputs/final_four/` for final classifier numbers. `outputs/evidence/` retains only the audit/search records and source needed for provenance; its historical scores must not be mixed with final results.


## Reproducibility update

The four individual notebooks now display historical tuning trials and final-settings three-fold CV evidence. Training/tuning can be rerun with the supported clean-package workflow; see [reproducibility instructions](reproducibility.md). Historical and newly computed evidence are distinguished, and the published final models remain unchanged.
