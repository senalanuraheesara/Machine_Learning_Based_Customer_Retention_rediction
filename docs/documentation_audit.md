# Documentation audit â€” 11 October 2026

All nine active notebooks were inspected through their source and saved textual outputs, together with the final CSV/JSON records, preprocessing tables and relevant helper scripts. The cleanup retains only relevant historical search/audit evidence under `outputs/evidence/`.

## Corrections

| Previous issue | Documentation correction |
| --- | --- |
| Gradient Boosting described as final incumbent | Current selection is Random Forest at threshold 0.425. |
| Older model scores mixed with final artifacts | Final results consistently use `outputs/final_four/` and its source-variant mapping. |
| Single-window and rolling preprocessing conflated | Separate exploratory export from six-month lookback/two-month outcome snapshots. |
| Three-invoice eligibility presented as current | Rolling cohort requires two distinct invoices and 60 history days; invoices may include returns. |
| Raw row count reused for sequential filter inputs | Report actual sequential inputs/removals and explain overlapping raw quality counts. |
| Recent features described as excluded | Document the 13 positive-invoice additions, full 35-input contract and compact forest subset. |
| CV scores at different thresholds conflated | Separate default-threshold CV accuracy from frozen-threshold audit scores/gaps. |
| Segmentation presented without outcome limitations | Updated by the segmentation cleanup: disclose final 1,577/119 cluster sizes, observed outcomes and untested stability. |
| No consolidated submission decision/comparison documents | Add decision log, model/method comparison, submission report and documentation index. |

## Verification and scope

`src/verify_submission_docs.py` recomputes all 12 training/validation/test accuracies from the four saved pipelines, compares them with the final CSV, checks the model/data fingerprints and selection rule, validates relative Markdown links and scans active notebooks for saved error outputs. Its machine-readable result is `outputs/evidence/documentation_verification.json`.

This verification does not retrain models, rerun CV or execute the notebooks. Saved secondary metrics and parameter tables were read from the individual model notebooks. All nine active notebooks and final model files were retained. The comparison notebook's audit path now points to `outputs/evidence/optimization/`. EDA/preprocessing generated notes now go to `outputs/generated_docs/`; numerical methods and saved results were not changed. Superseded models, stale predictions, duplicate review exports and one-off builders were deleted at the user's request. The exact removal list is `outputs/evidence/cleanup_manifest.json`.

The supplied `.venv` launcher failed because its referenced Python path could not start. Verification instead uses the available bundled Python 3.12 runtime with this project's existing site-packages. No package installation or environment repair was performed. Some saved notebook outputs include paths from the project's former folder; these are historical execution text, not current path configuration.

Curated Markdown is maintained directly; the one-off documentation generator was removed. The clean package retains historical search source for review but does not claim a turnkey rerun of all removed experiments.

No standalone assignment rubric was present. The requested decision logs and model/method comparison are included; assessment-specific formatting and other requirements are not independently confirmed.

## Cleanup validation

Removed 223 obsolete files (18,207,432 bytes), including superseded bundles, duplicate notebooks/reports, stale classifier outputs, temporary logs and caches. Necessary audit/search records were copied into `outputs/evidence/` before deletion. After cleanup, all 12 saved-model accuracy checks, fingerprints, selection checks and document links passed. The comparison notebook's code cells were also executed successfully using the relocated fitting audit; no model was retrained. The distributable ZIP excludes the machine-specific `.venv` and bytecode caches.


## Reproducibility update

The four individual notebooks now display historical tuning trials and final-settings three-fold CV evidence. Training/tuning can be rerun with the supported clean-package workflow; see [reproducibility instructions](reproducibility.md). Historical and newly computed evidence are distinguished, and the published final models remain unchanged.

## Final segmentation cleanup

The segmentation notebook now contains one ten-feature workflow. See [population definitions](customer_populations.md) and the revised [assessment](segmentation_assessment.md). The legacy assignments are regenerated from the final 1,696-customer solution. Unreferenced old figures were archived under outputs/evidence/obsolete_segmentation; outputs/tables was already empty. Earlier verification statements above describe the previous audit, not this cleanup.

Verification for this cleanup: the consolidated notebook executed successfully in a fresh local environment installed from requirements.txt (scikit-learn 1.9.1, NumPy 2.5.4, pandas 3.0.6). src/verify_segmentation.py passed source/assignment alignment, identical compatibility export, counts, observed outcomes, candidate metrics, executed-cell checks and all curated Markdown links. Evidence is outputs/evidence/segmentation_verification.json. Classifier models were not retrained.

## Compatibility and full tuning follow-up

The saved estimator versions were inspected and matched scikit-learn 1.9.1; requirements.txt now pins it. The documented 32-trial randomized tuning protocol completed for all four families (106 configurations and 318 CV fits total), preserving published model hashes. A fresh lock-file environment and extracted submission copy passed saved-model score/fingerprint checks and segmentation execution. See reproducibility.md and the environment/full-tuning verification JSON files for current evidence. This was an isolated local setup test, not a separate physical computer.
